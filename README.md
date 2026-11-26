# DataLint

> A clear, reproducible health check for tabular data.

Before analysis, teams need to find missing values, duplicates, suspicious types, inconsistent categories, and likely quality issues without trusting an opaque AI verdict.

## Why this project

Analysts, students, and developers preparing CSV or Parquet datasets.

DataLint is a portfolio project focused on a narrow, demonstrable workflow: useful AI assistance with visible evidence, predictable limits, and a clear local-first story.

## Product snapshot

- **Input:** CSV file and optional YAML configuration for expectations and thresholds.
- **Output:** Profile summary, findings with severity and affected rows, reproducible rule IDs, and a report.
- **MVP:** Inspect a local CSV, infer column types, run configurable deterministic quality checks, and produce a concise Markdown/JSON report with examples and suggested fixes.

## Planned architecture

Read input in bounded/chunked mode and never modify it. A profiler infers schema and basic distributions. A registry of pure checks evaluates nulls, duplicates, constant columns, suspicious mixed types, category whitespace/casing, and configured expectations. Findings have stable IDs, severity, evidence counts, and limited examples. Render JSON for automation and Markdown for humans.

## Current status

**Planning scaffold.** The product requirements, design, project skill, and agent guidance are in place. Application implementation has not started.

## Getting started

The MVP is planned for Python 3.11+. Clone this repository and review the product and design docs before implementation. Runtime setup instructions will be added with the first working release.

For local LLM configuration, copy the variable names from .env and add your own values. .env is intentionally ignored by Git; never commit API keys.

## Roadmap

1. Implement the smallest end-to-end MVP described in the PRD.
2. Add representative fixtures and quality checks.
3. Document setup, limitations, and a short demo.
4. Revisit optional integrations only when they solve a demonstrated need.

## Safety and privacy

Large files, sensitive data, misleading type inference, expensive profiling, and accidental mutation of source files.

The design defaults to local processing where practical and minimizes what is sent to external model providers. Do not use real sensitive data in examples or screenshots.

## Project documents

- [Product requirements](docs/PRD.md)
- [Technical design](docs/DESIGN.md)
- [Project skill](.agents/skills/datalint/SKILL.md)
- [Agent guidance](AGENTS.md)

## License

License not selected yet.
