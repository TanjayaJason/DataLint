# Agent instructions

You are the DataLint project agent. Build an explainable, read-only data quality CLI. Read docs/PRD.md and docs/DESIGN.md before implementation. Every finding must map to a deterministic rule and evidence. Preserve the input file. Never commit datasets, .env, or real personal data.

## Repository conventions

- Treat docs/PRD.md as the scope boundary and docs/DESIGN.md as the current technical plan.
- Keep changes focused and explain any departure from those documents.
- Do not add secrets, private user data, or generated large artifacts.
- Do not claim features work until they are implemented and verified.

## Current owner preference

Local tests and dependency installation are authorized. Do not make live LLM calls. Record the checks actually run in README and STATUS.md; keep live model behavior marked unverified. Synthetic examples are allowed; never commit user input or real personal data.
