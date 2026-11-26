---
name: code-metrics
description: >
  Conventions for collecting model performance signals by task kind (quality,
  latency, cost, success). Documents when to measure and where to store JSONL.
  Writing is done via plugin scripts/hooks stubs — not ad hoc files.
---

# Code metrics (conventions)

## Purpose

Collect performance signals **by task type** to feed model routing later. This skill defines **when** and **what** to measure; durable writes go through the plugin stubs (`scripts/metrics_append.py`), not ad hoc files.

## Dimensions

| Dimension | Example signals |
|---|---|
| Quality | Visual QA score, mockup gaps, human review OK/KO |
| Latency | Wall-clock duration of task / sub-agent |
| Cost | Tokens in/out, model slug, credit estimate |
| Success | CI green, clippy/check OK, merge without revert, rework count |

## Storage (priority)

| Option | When |
|---|---|
| Project store `internal/metrics/` (JSONL or 1 file/day) | Default cloud Project — readable by coordinator + workers |
| Host KV (`host.kv`) | Agent SDK / runtime with shared session state |
| Repo `.cursor/metrics/` | Non-sensitive aggregates only; never secrets |

Configure path via env `AGENTIC_METRICS_STORE` or plugin `settings.json` → `metricsStorePath`. If unset / missing, the append script is a **safe no-op** (exit 0, logs skip).

## Minimal event schema (one JSON object per line)

```json
{
  "ts": "ISO-8601",
  "task_id": "AIP-…",
  "role": "designer|dev-front|dev-back|visual-qa|coordinator|triage",
  "task_kind": "figcraft|ui-impl|rust|visual-qa|triage|other",
  "model": "model-slug",
  "latency_ms": 0,
  "cost_est": null,
  "success": true,
  "signals": { "ci": true, "clippy": true, "visual_qa": "ok|fail|skip", "rework": 0 }
}
```

## Who writes / when

| Author | Moment |
|---|---|
| Hook / script post-task | End of sub-agent run — automatic when wired |
| Visual QA / Quality | After gate G3: `visual_qa` + optional rework |
| Coordinator | Aggregate / manual correction; read before spawn |

## How to append (plugin stub)

```bash
./bin/metrics-append \
  --task-id AIP-88 \
  --role coordinator \
  --task-kind other \
  --model composer \
  --success true
```

Or pipe a full JSON event (no task flags required):

```bash
echo '{"task_id":"AIP-88","role":"coordinator","task_kind":"other","success":true}' \
  | ./bin/metrics-append --stdin
```

Hooks in this plugin are intentionally empty stubs until a store path is configured — agents must still follow these conventions when recording manually.
