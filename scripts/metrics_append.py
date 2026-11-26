#!/usr/bin/env python3
"""Append one code-metrics JSONL event. Safe no-op if store path is unset/missing."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def resolve_store_path(explicit: str | None) -> Path | None:
    raw = (
        explicit
        or os.environ.get("AGENTIC_METRICS_STORE")
        or os.environ.get("AGENTIC_DEV_TOOLKIT_METRICS_STORE")
        or ""
    ).strip()
    if not raw:
        settings = Path(__file__).resolve().parent.parent / "settings.json"
        if settings.is_file():
            try:
                data = json.loads(settings.read_text(encoding="utf-8"))
                raw = (data.get("metricsStorePath") or "").strip()
            except (OSError, json.JSONDecodeError):
                raw = ""
    if not raw:
        return None
    return Path(raw).expanduser()


def build_event(args: argparse.Namespace) -> dict:
    signals: dict = {}
    if args.signals:
        try:
            signals = json.loads(args.signals)
            if not isinstance(signals, dict):
                raise ValueError("signals must be a JSON object")
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"metrics_append: invalid --signals: {exc}", file=sys.stderr)
            sys.exit(2)

    event = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "task_id": args.task_id,
        "role": args.role,
        "task_kind": args.task_kind,
        "model": args.model,
        "latency_ms": args.latency_ms,
        "cost_est": args.cost_est,
        "success": args.success,
        "signals": signals,
    }
    if args.extra:
        try:
            extra = json.loads(args.extra)
            if isinstance(extra, dict):
                event.update(extra)
        except json.JSONDecodeError as exc:
            print(f"metrics_append: invalid --extra: {exc}", file=sys.stderr)
            sys.exit(2)
    return event


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a code-metrics JSONL event (no-op if store unset)."
    )
    parser.add_argument("--store", default=None, help="Directory or .jsonl file path")
    parser.add_argument(
        "--task-id",
        default=None,
        help="Required unless --stdin provides the event JSON",
    )
    parser.add_argument(
        "--role",
        default=None,
        help="Required unless --stdin provides the event JSON",
    )
    parser.add_argument(
        "--task-kind",
        default=None,
        help="Required unless --stdin provides the event JSON",
    )
    parser.add_argument("--model", default="unknown")
    parser.add_argument("--latency-ms", type=int, default=None)
    parser.add_argument("--cost-est", type=float, default=None)
    parser.add_argument(
        "--success",
        type=lambda v: str(v).lower() in {"1", "true", "yes", "ok"},
        default=True,
    )
    parser.add_argument("--signals", default="{}", help="JSON object of signals")
    parser.add_argument("--extra", default=None, help="JSON object merged into event")
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read a full JSON event from stdin (overrides flag fields except store)",
    )
    args = parser.parse_args()

    if not args.stdin:
        missing = [
            flag
            for flag, val in (
                ("--task-id", args.task_id),
                ("--role", args.role),
                ("--task-kind", args.task_kind),
            )
            if not val
        ]
        if missing:
            parser.error(
                "the following arguments are required unless --stdin: "
                + ", ".join(missing)
            )

    store = resolve_store_path(args.store)
    if store is None:
        print(
            "metrics_append: no store configured "
            "(AGENTIC_METRICS_STORE / settings.metricsStorePath) — skip (no-op)",
            file=sys.stderr,
        )
        return 0

    if args.stdin:
        try:
            event = json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            print(f"metrics_append: invalid stdin JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(event, dict):
            print("metrics_append: stdin must be a JSON object", file=sys.stderr)
            return 2
        event.setdefault(
            "ts", datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        )
    else:
        event = build_event(args)

    if store.suffix == ".jsonl":
        path = store
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        store.mkdir(parents=True, exist_ok=True)
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        path = store / f"metrics-{day}.jsonl"

    line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(f"metrics_append: wrote → {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
