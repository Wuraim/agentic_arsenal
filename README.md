# Agentic Dev Toolkit (Cursor plugin)

Cross-cutting skills, rules, and a minimal versioned CLI for agentic workflows
(AIP-88).

Standalone Cursor plugin repository — install by cloning or adding as a Cursor
plugin source. Does **not** include or reactivate Hindsight.

## Layout

```
.
├── .cursor-plugin/plugin.json   # displayName, description, skills/rules/hooks
├── rules/                       # always-apply mdc → skills + verify before Done
├── skills/                      # SKILL.md per domain
├── scripts/                     # Python implementations (metrics, checklist)
├── bin/                         # stable CLI entry points for agents
├── tools/                       # documented aliases (verify-checklist)
├── hooks/hooks.json             # empty stubs (metrics hooks later)
└── settings.json                # metricsStorePath, flags
```

## Skills

| Skill | Trigger |
|---|---|
| `web-stack` | Front / web app (Nuxt/Vite/TS/PNPM/Vitest/Prettier) |
| `rust-backend` | Rust + Tokio/SQLx/Teloxide; check + clippy |
| `figcraft-designer-dev` | FigCraft mockups, designer↔dev comments |
| `visual-quality-gate` | Any visual UI change — proof required |
| `verify-handoff` | Before Done — gates G0–G6 |
| `no-disposable-scripts` | Prefer versioned CLI over `/tmp` bash |
| `code-metrics` | Conventions + JSONL append via plugin stubs |

## Install / activate in Cursor

### As a dedicated plugin repo

1. Clone this repository (or add it as a Cursor plugin / workspace folder).
2. Cursor reads `.cursor-plugin/plugin.json` at the plugin root.
3. Confirm **Agentic Dev Toolkit** in Cursor plugin settings and enable it.
4. Rules under `rules/*.mdc` apply automatically (`alwaysApply: true`).
5. Agents should **read the matching `skills/*/SKILL.md` before acting**, and
   call the toolbox bins below instead of disposable shell scripts.

### Vendored under another project

Copy or submodule this tree to `.cursor-plugin/agentic-dev-toolkit/` in the
target repo (same layout). CLI paths then become
`.cursor-plugin/agentic-dev-toolkit/bin/…`.

Optional metrics store:

```bash
export AGENTIC_METRICS_STORE="/path/to/store/or/metrics.jsonl"
# or edit settings.json → "metricsStorePath"
```

Without a store, `metrics-append` is a **safe no-op** (exit 0).

## CLI toolbox (versioned — use these)

### `verify-checklist`

Pre-Done gate status. Agents must call this (or document equivalent) before Done.

```bash
./bin/verify-checklist --list

./bin/verify-checklist \
  --task-id AIP-88 \
  --role dev-front \
  --gates G0,G1,G2,G3,G5,G6 \
  --status G0=pass,G1=pass,G2=pass,G3=pass,G5=pass,G6=pass

# also: ./tools/verify-checklist (alias)
```

Exit codes: `0` ok · `1` fail · `3` pending · `2` usage error.

### `metrics-append`

Append one JSONL metrics event (see skill `code-metrics`).

```bash
./bin/metrics-append \
  --task-id AIP-88 \
  --role coordinator \
  --task-kind other \
  --model composer \
  --success true
```
