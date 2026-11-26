# Agentic Dev Toolkit (Cursor plugin)

Cross-cutting skills, rules, hooks, and a minimal versioned CLI for agentic
workflows (AIP-88).

Standalone Cursor plugin repository — install by cloning or adding as a Cursor
plugin source.

Personal tech stacks and product-specific design tools are **not** baked into
this plugin; supply them as conversation context when needed.

## Layout

```
.
├── .cursor-plugin/plugin.json   # displayName, description, skills/rules/hooks
├── rules/                       # always-apply mdc → skills + verify before Done
├── skills/                      # SKILL.md per domain
├── scripts/                     # Python implementations (metrics, checklist)
├── bin/                         # stable CLI entry points for agents
├── tools/                       # documented aliases
├── hooks/                       # stop + subagentStop → JSONL metrics
├── metrics/                     # default JSONL store (*.jsonl gitignored)
└── settings.json                # metricsStorePath, flags
```

## Skills

| Skill | Trigger |
|---|---|
| `visual-quality-gate` | Any visual UI change — proof vs design SoT from context |
| `verify-handoff` | Before Done — gates G0–G6 (criteria from context) |
| `no-disposable-scripts` | Prefer versioned CLI over `/tmp` bash |
| `code-metrics` | Conventions + JSONL append/summarize; hooks auto-record |

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

## Metrics store

Default: `./metrics` (daily `metrics-YYYY-MM-DD.jsonl` under the plugin root).

```bash
export AGENTIC_METRICS_STORE="/path/to/store/or/metrics.jsonl"
# or edit settings.json → "metricsStorePath"
```

Set `"metricsEnabled": false` in `settings.json` to disable writes. File store
only for now; a database / network sink can replace the append path later.

Without a store (and with metrics enabled), `metrics-append` is a **safe no-op**
only if `metricsStorePath` is cleared.

## Hooks

`hooks/hooks.json` records performance on:

- `stop` — end of an agent loop
- `subagentStop` — end of a Task subagent

Scripts map Cursor payloads (model, duration, status, subagent type) into the
code-metrics JSONL schema. `cost_est` stays null (hooks do not expose tokens).

## CLI toolbox (versioned — use these)

### `verify-checklist`

Pre-Done gate status. Agents must call this (or document equivalent) before Done.

```bash
./bin/verify-checklist --list

./bin/verify-checklist \
  --task-id AIP-88 \
  --role implement \
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

### `metrics-summarize`

Aggregate JSONL by `task_kind` / model for **opt-in** routing before spawn.
Hooks cannot set the model on spawn; the coordinator reads this and passes
`model` to the Task tool when data is thick enough.

```bash
./bin/metrics-summarize --task-kind explore
./bin/metrics-summarize --json --min-samples 3

# also: ./tools/metrics-summarize (alias)
```
