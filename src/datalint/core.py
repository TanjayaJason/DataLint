import csv
import io
import math
from collections import Counter
from pathlib import Path
import yaml
from pydantic import BaseModel, ConfigDict, Field
from .support import read_text

class Expectation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    required: bool = False
    unique: bool = False
    type: str | None = Field(default=None, pattern=r'^(number|text)$')
    minimum: float | None = None
    maximum: float | None = None
    allowed: list[str] | None = None

class Config(BaseModel):
    model_config = ConfigDict(extra='forbid')
    max_null_fraction: float = Field(default=0, ge=0, le=1)
    columns: dict[str, Expectation] = Field(default_factory=dict)

def numeric(value):
    try:
        return math.isfinite(float(value))
    except (ValueError, OverflowError):
        return False

def inspect(path: Path, config_path: Path | None = None):
    config = Config.model_validate(yaml.safe_load(read_text(config_path, 100_000)) or {}) if config_path else Config()
    reader = csv.reader(io.StringIO(read_text(path)), strict=True)
    header = next(reader, None)
    if not header or any(not h.strip() for h in header) or len(set(header)) != len(header):
        raise ValueError('CSV needs nonempty, unique column names.')
    if len(header) > 500:
        raise ValueError('Maximum 500 columns.')
    rows = []
    for row in reader:
        if len(row) != len(header):
            raise ValueError(f'Record {len(rows)+1} has {len(row)} fields; expected {len(header)}.')
        rows.append(row)
        if len(rows) > 100_000:
            raise ValueError('Maximum 100,000 records.')
    findings = []
    def add(rule, column, ids, severity, fix):
        if ids:
            findings.append({'rule': rule, 'column': column, 'severity': severity,
                             'count': len(ids), 'record_examples': ids[:5], 'suggestion': fix})
    seen, duplicates = set(), []
    for i, row in enumerate(rows, 1):
        key = tuple(row)
        if key in seen:
            duplicates.append(i)
        seen.add(key)
    add('DL001', None, duplicates, 'warning', 'Review duplicate records before removing any.')
    profiles = []
    for index, column in enumerate(header):
        values = [row[index] for row in rows]
        populated = [v for v in values if v.strip()]
        nulls = [i for i, v in enumerate(values, 1) if not v.strip()]
        numbers = sum(numeric(v) for v in populated)
        inferred = 'empty' if not populated else 'number' if numbers == len(populated) else 'mixed' if numbers else 'text'
        profiles.append({'column': column, 'inferred_type': inferred, 'nulls': len(nulls), 'distinct': len(set(populated))})
        if rows and len(nulls)/len(rows) > config.max_null_fraction:
            add('DL002', column, nulls, 'warning', 'Review missing values or adjust max_null_fraction.')
        if len(set(populated)) == 1 and len(populated) > 1:
            add('DL003', column, [i for i,v in enumerate(values,1) if v.strip()], 'info', 'Review whether this constant column is useful.')
        if inferred == 'mixed':
            add('DL004', column, [i for i,v in enumerate(values,1) if v.strip() and not numeric(v)], 'warning', 'Review mixed numeric and text values; identifiers may intentionally be text.')
        canonical = {}
        for value in populated:
            canonical.setdefault(value.strip().casefold(), set()).add(value)
        inconsistent = [i for i,v in enumerate(values,1) if v.strip() and (v != v.strip() or len(canonical[v.strip().casefold()]) > 1)]
        add('DL005', column, inconsistent, 'warning', 'Review whitespace and case variants before normalizing.')
        exp = config.columns.get(column)
        if exp:
            if exp.required:
                add('DL006', column, nulls, 'error', 'Populate required values.')
            if exp.unique:
                counts = Counter(populated)
                add('DL007', column, [i for i,v in enumerate(values,1) if v.strip() and counts[v]>1], 'error', 'Review repeated identifiers.')
            if exp.type == 'number':
                add('DL008', column, [i for i,v in enumerate(values,1) if v.strip() and not numeric(v)], 'error', 'Use finite numeric values.')
            if exp.minimum is not None or exp.maximum is not None:
                add('DL009', column, [i for i,v in enumerate(values,1) if numeric(v) and ((exp.minimum is not None and float(v)<exp.minimum) or (exp.maximum is not None and float(v)>exp.maximum))], 'error', 'Review values outside the configured range.')
            if exp.allowed is not None:
                add('DL010', column, [i for i,v in enumerate(values,1) if v.strip() and v not in exp.allowed], 'error', 'Use one of the configured allowed values.')
    for missing in sorted(config.columns.keys() - set(header)):
        findings.append({'rule':'DL011', 'column': missing, 'severity':'error', 'count':1, 'record_examples':[], 'suggestion':'Add the configured column or correct the configuration.'})
    return {'records':len(rows), 'columns':profiles, 'findings':findings,
            'note':'Record numbers are 1-based data records, excluding the header; they are not physical line numbers. Raw cell values are not included.'}

def markdown(report):
    out = ['# DataLint report', '', f"Records: {report['records']} · Columns: {len(report['columns'])} · Findings: {len(report['findings'])}", '', '## Column profile', '']
    for p in report['columns']:
        out.append(f"- {p['column']}: {p['inferred_type']}, {p['nulls']} missing, {p['distinct']} distinct")
    out.extend(['', '## Findings', ''])
    for f in report['findings']:
        out.append(f"- {f['rule']} [{f['severity']}] {f['column'] or 'dataset'}: {f['count']} affected; examples {f['record_examples']}. {f['suggestion']}")
    out.extend(['', report['note']])
    return '\n'.join(out)
