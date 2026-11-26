#!/usr/bin/env python3
"""Summarize code-metrics JSONL for opt-in model routing before spawn."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from metrics_lib import iter_jsonl_events, resolve_store_path  # noqa: E402


def percentile(sorted_vals: list[float], p: float) -> float | None:
    if not sorted_vals:
        return None
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f)


def summarize(
    events: list[dict[str, Any]],
    *,
    task_kind: str | None,
    role: str | None,
    min_samples: int,
) -> dict[str, Any]:
    filtered: list[dict[str, Any]] = []
    for ev in events:
        if task_kind and str(ev.get("task_kind") or "") != task_kind:
            continue
        if role and str(ev.get("role") or "") != role:
            continue
        filtered.append(ev)

    by_kind: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ev in filtered:
        kind = str(ev.get("task_kind") or "other")
        by_kind[kind].append(ev)

    kinds_out: dict[str, Any] = {}
    recommendations: list[dict[str, Any]] = []

    for kind, rows in sorted(by_kind.items()):
        by_model: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for ev in rows:
            model = str(ev.get("model") or "unknown")
            by_model[model].append(ev)

        models_out: list[dict[str, Any]] = []
        for model, mrows in sorted(by_model.items()):
            successes = sum(1 for e in mrows if e.get("success") is True)
            latencies = [
                float(e["latency_ms"])
                for e in mrows
                if isinstance(e.get("latency_ms"), (int, float))
            ]
            latencies.sort()
            n = len(mrows)
            entry = {
                "model": model,
                "samples": n,
                "success_rate": round(successes / n, 4) if n else None,
                "latency_p50_ms": (
                    round(percentile(latencies, 50), 1) if latencies else None
                ),
                "latency_p90_ms": (
                    round(percentile(latencies, 90), 1) if latencies else None
                ),
            }
            models_out.append(entry)

        # Prefer higher success_rate, then more samples, then lower p50 latency.
        eligible = [m for m in models_out if m["samples"] >= min_samples]
        recommended = None
        if eligible:

            def sort_key(m: dict[str, Any]) -> tuple:
                rate = m["success_rate"] if m["success_rate"] is not None else -1.0
                p50 = m["latency_p50_ms"] if m["latency_p50_ms"] is not None else 1e18
                return (-rate, -m["samples"], p50)

            recommended = sorted(eligible, key=sort_key)[0]["model"]
            recommendations.append(
                {
                    "task_kind": kind,
                    "model": recommended,
                    "min_samples": min_samples,
                    "basis": "success_rate then samples then latency_p50",
                }
            )

        kinds_out[kind] = {
            "samples": len(rows),
            "recommended_model": recommended,
            "models": models_out,
        }

    return {
        "total_events": len(events),
        "matched_events": len(filtered),
        "filters": {"task_kind": task_kind, "role": role, "min_samples": min_samples},
        "by_task_kind": kinds_out,
        "recommendations": recommendations,
        "note": (
            "Thin data: fall back to inherit / explicit user model choice. "
            "cost_est is usually null (Cursor hooks do not expose tokens/cost)."
        ),
    }


def format_text(summary: dict[str, Any]) -> str:
    lines = [
        f"events: {summary['matched_events']} matched / {summary['total_events']} total",
        f"filters: {json.dumps(summary['filters'], separators=(',', ':'))}",
        "",
    ]
    by_kind = summary.get("by_task_kind") or {}
    if not by_kind:
        lines.append("No matching events. Fall back to inherit / user choice.")
        return "\n".join(lines)

    for kind, block in by_kind.items():
        rec = block.get("recommended_model") or "(insufficient samples)"
        lines.append(f"## task_kind={kind}  samples={block['samples']}  recommend={rec}")
        for m in block.get("models") or []:
            lines.append(
                "  - {model}: n={samples} success={success_rate} "
                "p50={latency_p50_ms}ms p90={latency_p90_ms}ms".format(**m)
            )
        lines.append("")
    lines.append(summary.get("note") or "")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize metrics JSONL for model routing before spawn."
    )
    parser.add_argument("--store", default=None, help="Directory or .jsonl file path")
    parser.add_argument("--task-kind", default=None, help="Filter by task_kind")
    parser.add_argument("--role", default=None, help="Filter by role")
    parser.add_argument(
        "--min-samples",
        type=int,
        default=3,
        help="Minimum samples before recommending a model (default: 3)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON summary",
    )
    args = parser.parse_args()

    store = resolve_store_path(args.store)
    if store is None:
        print(
            "metrics_summarize: no store configured "
            "(AGENTIC_METRICS_STORE / settings.metricsStorePath)",
            file=sys.stderr,
        )
        return 2
    if not store.exists():
        print(f"metrics_summarize: store path does not exist: {store}", file=sys.stderr)
        empty = summarize(
            [],
            task_kind=args.task_kind,
            role=args.role,
            min_samples=args.min_samples,
        )
        if args.json:
            print(json.dumps(empty, ensure_ascii=False, indent=2))
        else:
            print(format_text(empty))
        return 0

    events = iter_jsonl_events(store)
    summary = summarize(
        events,
        task_kind=args.task_kind,
        role=args.role,
        min_samples=args.min_samples,
    )
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
