---
name: datalint
description: Project-specific guidance for working on DataLint.
---

# DataLint project skill

When helping with DataLint, keep findings deterministic, explain each rule and threshold, and include row/column evidence. Never silently mutate a dataset. Bound example values and avoid printing potentially sensitive records. Prefer offline behavior; do not add an LLM to decide whether data is valid.

## Before changing code

- Read docs/PRD.md, docs/DESIGN.md, and AGENTS.md.
- Prefer the smallest complete implementation of the documented MVP.
- Update documentation when behavior, limitations, or data handling changes.
- Do not add dependencies or services without a concrete MVP need.
