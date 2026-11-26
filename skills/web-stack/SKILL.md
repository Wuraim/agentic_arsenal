---
name: web-stack
description: >
  Front / web app work (scaffold, UI features, deps, format, unit tests).
  Enforces TypeScript + Vite + Nuxt + PNPM + Vitest + Prettier. Use for any
  frontend change unless the task explicitly allows another stack.
---

# Web stack

## When to use

Any front / web app task: scaffold, UI feature, dependencies, formatting, unit tests.

## Rules

- **Imposed stack:** TypeScript, Vite, Nuxt, PNPM, Vitest, Prettier.
- **No alternatives** (npm/yarn, React/Next, etc.) unless the task explicitly asks.
- Run **Prettier** before commit.
- Run **Vitest** for touched logic.
- Use **PNPM** for install and scripts.

## Verify (before handoff)

- Prettier clean on changed files.
- Targeted Vitest green for logic you touched.
- Then run the plugin CLI `verify-checklist` (gate G2 stack) — see skill `verify-handoff`.
