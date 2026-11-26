#!/usr/bin/env python3
"""Cursor `subagentStop` hook: record subagent metrics to JSONL."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "metrics_from_hook.py"


def main() -> int:
    payload = sys.stdin.buffer.read()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--event", "subagentStop"],
        input=payload,
        cwd=str(ROOT),
    )
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
