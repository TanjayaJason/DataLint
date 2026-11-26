# Product Requirements — DataLint

## 1. Summary

A clear, reproducible health check for tabular data. Before analysis, teams need to find missing values, duplicates, suspicious types, inconsistent categories, and likely quality issues without trusting an opaque AI verdict.

## 2. Users and need

**Primary users:** Analysts, students, and developers preparing CSV or Parquet datasets.

**Need:** Inspect a local CSV, infer column types, run configurable deterministic quality checks, and produce a concise Markdown/JSON report with examples and suggested fixes.

## 3. Goals

- Deliver one narrow workflow that can be demonstrated from input to useful result.
- Make outputs inspectable and explain how they were produced.
- Keep data handling safe and document limitations clearly.
- Provide an approachable open-source portfolio project with reproducible examples.

## 4. Non-goals for the first release

- Multi-user accounts, hosted SaaS, billing, or team administration.
- Autonomous actions that modify user files or systems.
- Support for every file format, language, or model provider.
- Claims of perfect accuracy or production readiness.

## 5. MVP scope

Inspect a local CSV, infer column types, run configurable deterministic quality checks, and produce a concise Markdown/JSON report with examples and suggested fixes.

**Inputs:** CSV file and optional YAML configuration for expectations and thresholds.

**Outputs:** Profile summary, findings with severity and affected rows, reproducible rule IDs, and a report.

### Functional requirements

1. Validate inputs and show actionable errors for unsupported or unreadable files.
2. Produce structured results suitable for both people and scripts where appropriate.
3. Preserve references back to the original input so users can verify important output.
4. Support a useful deterministic path when the language model is unavailable, where applicable.
5. Keep the first-run experience documented and use only user-provided local data.

### Quality requirements

- No secret or source-data values are committed to the repository.
- Bound file size, context size, and output length.
- Clearly distinguish extracted facts from model-generated suggestions.
- Provide representative fixtures and measurable quality criteria before calling the MVP complete.

## 6. Success measures

Small fixtures per rule including clean and failing cases; deterministic outputs; bounded memory on larger inputs; no source mutation; report schema validity.

The first portfolio milestone is a reproducible demo and a small evaluation report, not production scale.

## 7. Risks and mitigations

- **Risk:** Large files, sensitive data, misleading type inference, expensive profiling, and accidental mutation of source files.
- **Mitigation:** Apply input limits, explicit data-flow boundaries, redaction or local processing as appropriate, and human-verifiable outputs. Document known unsupported cases.

## 8. Open decisions

- Choose the exact UI and packaging approach during implementation based on the first end-to-end slice.
- Select one model/provider configuration and document alternatives only after the core workflow works.
- Confirm license and contribution policy before inviting external contributions.
