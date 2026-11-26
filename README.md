# DataLint

### Know your data before you trust it.

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Status](https://img.shields.io/badge/status-initial_implementation-orange)
![Validation](https://img.shields.io/badge/offline_tests-10_passed-brightgreen)

An offline CSV quality inspector with stable rule IDs, configurable expectations, and record-level evidence. Reports explain what to review while leaving source data untouched.

> **Portfolio release:** 10 offline tests pass on Windows with Python 3.11.9. Local CLI examples and dependency consistency were checked. Live LLM calls and answer quality remain unverified.

## What you can explore

| Capability | Implementation |
|---|---|
| DL001–DL005 | Duplicates, missing values, constants, mixed types, case/whitespace variants |
| DL006–DL008 | Required fields, uniqueness, and numeric expectations |
| DL009–DL011 | Numeric ranges, allowed categories, and missing configured columns |
| Evidence | Counts and up to five record numbers; no raw cell values in reports |
| Automation | JSON output and optional exit code 2 for error findings |

## How it fits together

```mermaid
flowchart LR
    A[CSV and optional YAML] --> B[Validate shape and limits]
    B --> C[Profile columns]
    C --> D[Deterministic quality rules]
    D --> E[Markdown or JSON report]
```

## Quick start

Use Python 3.11 or newer. Run from the repository root. Git is also required for CodeTrail.

```powershell
git clone https://github.com/TanjayaJason/DataLint.git
cd DataLint
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Skip the copy if `.env` already exists. On macOS/Linux, activate with `source .venv/bin/activate` and copy with `cp .env.example .env`.

```powershell
datalint examples/orders.csv
datalint examples/orders.csv --config examples/expectations.yaml --json
datalint examples/orders.csv --config examples/expectations.yaml --fail-on-error
```

## Configuration

No LLM or API key is required. Edit `examples/expectations.yaml` to define required and unique columns, numeric ranges, allowed values, and a missing-value threshold. The `.env.example` reserves names for a possible future explainer; the current inspector never calls a model.

## Limits you should know

UTF-8 comma-separated CSV only; 10 MB, 100,000 data records, and 500 columns. Rows are held in memory within those limits. Record numbers exclude the header and differ from physical lines for quoted multiline fields. Numeric inference is heuristic and can misclassify identifiers. Missing values mean empty or whitespace-only cells; strings such as NA remain text. Parquet and automatic fixes are outside this release.

User input is treated as evidence, never executable instructions. Model output remains advisory. Keep private documents, logs, datasets, repositories, and generated reports out of Git; `data/`, `reports/`, and `.env` are ignored.

## Repository guide

```text
src/datalint/
  core.py          Domain logic and evidence handling
  cli.py           Command-line entry point
  support.py       Bounded input and optional provider boundary
docs/
  PRD.md           Product scope and acceptance goals
  DESIGN.md        Architecture and implementation decisions
  STATUS.md        Delivery and validation status
.agents/skills/datalint/SKILL.md
AGENTS.md          Guidance for future coding work
.env.example       Empty configuration template
```

## Where this goes next

- Add large-file streaming profiles.
- Add Parquet as a separate input adapter.
- Consider optional AI explanations only after deterministic findings are established.

## Project notes

Read the [PRD](docs/PRD.md), [design](docs/DESIGN.md), and [delivery status](docs/STATUS.md) for scope and tradeoffs. Offline correctness checks are recorded in the delivery status; no model-quality or performance benchmark is claimed. A license has not been selected; no broad reuse rights are implied.

## Running the offline checks

```powershell
python -m pip install -r requirements.txt
python -m pytest -q
python -m pip check
```

Tests use synthetic inputs and block external connections. PageProof permits loopback sockets for Windows asyncio. Model response validation uses local fakes, never a live LLM. Local examples and the test suites do not need an API key.

## Dependency manifest

`requirements.txt` installs the editable project and all declared extras (including tests). It reads version constraints from `pyproject.toml`; pip resolves transitive dependencies. Run it from the repository root. This file is an installation entry point, not a frozen dependency lock. An API key is not required for installation or offline tests.
