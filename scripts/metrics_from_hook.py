#!/usr/bin/env python3
"""Map Cursor hook stdin payloads to metrics events and append JSONL.

Used by hooks/record-stop.py and hooks/record-subagent-stop.py.
Always prints `{}` on stdout so Cursor treats the hook as a successful no-op
response. Failures are logged to stderr; exit 0 (fail-open for metrics).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from metrics_lib import (  # noqa: E402
    append_event,
    event_from_stop_payload,
    event_from_subagent_stop_payload,
)


def read_payload() -> dict:
    try:
        raw = sys.stdin.read()
    except OSError as exc:
        print(f"metrics_from_hook: stdin read failed: {exc}", file=sys.stderr)
        return {}
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"metrics_from_hook: invalid JSON: {exc}", file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Record metrics from a Cursor hook.")
    parser.add_argument(
        "--event",
        required=True,
        choices=("stop", "subagentStop"),
        help="Which hook payload mapper to use",
    )
    args = parser.parse_args()

    payload = read_payload()
    if not payload:
        print("{}", flush=True)
        return 0

    if args.event == "stop":
        event = event_from_stop_payload(payload)
    else:
        event = event_from_subagent_stop_payload(payload)

    path = append_event(event)
    if path is not None:
        print(f"metrics_from_hook: wrote → {path}", file=sys.stderr)
    # Hook stdout: empty object (no followup_message).
    print("{}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
