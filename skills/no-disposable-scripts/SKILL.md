---
name: no-disposable-scripts
description: >
  Forbid one-shot disposable scripts when a versioned CLI/toolbox already exists
  or the need is recurrent. Search toolbox first; extend CLI in the same
  deliverable instead of /tmp bash. Use whenever automation is needed.
---

# No disposable scripts

## When to use

Any need to automate: check, scrape, publish, compare, migrate, smoke, verify.

## Forbidden

An agent must **not** invent a disposable one-shot script (`/tmp/foo.sh`, paste-once bash then forget) when:

1. a **reusable tool / CLI** already exists (repo, PATH, plugin), **or**
2. the need is recurrent → **create / extend** the versioned CLI instead of a disposable script.

## Required

1. Search the toolbox first (this plugin `bin/` / `tools/`, repo `cli/`, `package.json` scripts, cargo bins).
2. **Call the CLI** with stable flags rather than regenerating ad hoc bash.
3. If the CLI is missing: **add it** (versioned, documented) **in the same deliverable**, then call it — not « just for this task ».
4. Narrow exception: interactive debug that is **not committed**, immediately replaced or discarded — never part of a Done handoff.

## Golden rule

If an agent writes more than ~15 lines of bash for a reproducible need → **promote to CLI** (repo or plugin) before Done.

## Plugin toolbox entry points

- `bin/verify-checklist` — pre-Done gate checklist
- `bin/metrics-append` / `bin/metrics-summarize` — code-metrics JSONL
- For a **project-specific** verify tool, follow skill `create-verify-cli`
