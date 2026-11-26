---
name: code-metrics
description: >
  Conventions for collecting model performance signals by task kind (quality,
  latency, cost, success). Hooks append JSONL automatically; coordinators may
  run metrics-summarize before spawning to pick a model from data.
---

# Code metrics (conventions)

## Purpose

Collect performance signals **by task type** to feed model routing later. Durable writes go through the plugin stubs (`scripts/metrics_append.py` / hooks), not ad hoc files.

## Dimensions

| Dimension | Example signals |
|---|---|
| Quality | Visual QA score, mockup gaps, human review OK/KO |
| Latency | Wall-clock duration of task / sub-agent (`duration_ms` from hooks) |
| Cost | Tokens in/out, model slug, credit estimate — **usually null from hooks** (Cursor does not expose usage on hook payloads) |
| Success | Hook status completed vs error/aborted; CI green; rework count |

## Storage (priority)

| Option | When |
|---|---|
| Plugin `metrics/` (daily `metrics-YYYY-MM-DD.jsonl`) | **Default** via `settings.json` → `metricsStorePath: "./metrics"` |
| Env `AGENTIC_METRICS_STORE` | Override path (file `.jsonl` or directory) |
| Host KV / network / DB | **Future** — not wired yet |

Relative store paths resolve against the plugin root (`CURSOR_PLUGIN_ROOT` or the repo that contains `scripts/`). If `metricsEnabled` is false, append is a safe no-op.

## Minimal event schema (one JSON object per line)

`role` and `task_kind` are open strings. Examples: `role` = `agent|subagent|coordinator|review`; `task_kind` = `explore|implement|review|shell|browser|docs|other`.

```json
{
  "ts": "ISO-8601",
  "task_id": "conversation-or-task-id",
  "role": "agent|subagent|coordinator|…",
  "task_kind": "explore|implement|review|other",
  "model": "model-slug",
  "latency_ms": 0,
  "cost_est": null,
  "success": true,
  "signals": { "hook": "stop|subagentStop", "status": "completed" }
}
```

## Who writes / when

| Author | Moment |
|---|---|
| Hook `stop` / `subagentStop` | End of agent loop or Task subagent — automatic via `hooks/hooks.json` |
| Manual / Visual QA | After a gate: optional `signals` + rework |
| Coordinator | Aggregate / correction; **may** read summarize before spawn |

## Opt-in routing before spawn (2A)

Hooks **cannot** override the model on `subagentStart` (allow/deny only). Before spawning a Task subagent, the coordinator **may**:

```bash
./bin/metrics-summarize --task-kind explore --json
```

Pick `recommended_model` when sample count is enough; if thin data, fall back to `inherit` or an explicit user choice. Passing `model` on the Task tool is how routing actually happens.

## How to append (manual)

```bash
./bin/metrics-append \
  --task-id AIP-88 \
  --role coordinator \
  --task-kind other \
  --model composer \
  --success true
```

Or pipe a full JSON event:

```bash
echo '{"task_id":"AIP-88","role":"coordinator","task_kind":"other","success":true}' \
  | ./bin/metrics-append --stdin
```
