---
name: code-quality
description: >
  Define and enforce code quality checks for the current project from
  conversation or repo context (lint, format, typecheck, tests, clippy-class
  analyzers). Use when setting quality bars, before Done, or when backend/front
  changes must pass project checks. Commands come from context — not a fixed
  language stack.
---

# Code quality

## When to use

- User asks for **quality rules**, lint/format/test standards, or a Definition of Done for code health.
- Before Done / merge when gates **G2** (conventions) or **G4** (backend checks) apply.
- After substantive code changes that should not ship unchecked.

## Rule

Quality commands and fail criteria come from **this project’s context** (README, package scripts, CI, user message). Do not assume npm vs pnpm, ESLint vs clippy, etc.

## Quality card (fill from context)

| Field | What to capture |
|---|---|
| **Languages / packages** | What changed (front, back, both, scripts) |
| **Format** | Formatter command(s) and whether check-only is required |
| **Lint / analyze** | Linter/analyzer command(s); disallowed overrides (e.g. blanket allow) |
| **Typecheck / build** | Typecheck or compile command(s) |
| **Tests** | Unit/integration commands and required subsets |
| **CI parity** | Must match CI job names / scripts when they exist |
| **Fail criteria** | What counts as fail (nonzero exit, new warnings, coverage drop, …) |

## Required behavior

1. Before claiming quality OK, run the **applicable** commands from the card (or CI-equivalent).
2. Record outputs as proofs for `verify-handoff` (attach or summarize logs).
3. Prefer **versioned** repo/plugin CLI (`no-disposable-scripts`) over one-off shell when a check is recurrent.
4. If the card is incomplete, ask for missing commands once; do not invent a stack.
5. Map results into gates: conventions → **G2**; backend/typecheck/lint after backend edits → **G4**.

## Standing rules vs one-off runs

- Short always-on constraints → project `.cursor/rules/*.mdc` (or equivalent).
- Multi-step “how we run quality here” → keep this skill + the filled quality card in context or project docs.
- Do **not** bake one team’s toolchain into this shareable plugin.

## Anti-patterns

- Declaring “lint clean” without running the project’s real command.
- Silent `|| true` / ignoring failures to greenwash Done.
- Disposable `/tmp` lint wrappers when `package.json` / `Makefile` / `bin/` already exist.

## Related

- `verify-handoff` (G2, G4, G5), `no-disposable-scripts`, `create-verify-cli`
