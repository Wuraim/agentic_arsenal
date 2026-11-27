#!/usr/bin/env python3
"""Versioned verify-handoff checklist. Agents call this instead of disposable bash."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

ALL_GATES = ("G0", "G1", "G2", "G3", "G4", "G5", "G6")

GATE_HELP = {
    "G0": "Design SoT — mockup/spec from context present (versioned preferred; live collab OK when immediacy required)",
    "G1": "Feedback — design feedback / open questions resolved or escalated",
    "G2": "Stack conventions — declared stack + format/lint/test from context followed",
    "G3": "Visual — design SoT ↔ implementation visual proof attached",
    "G4": "Backend checks — typecheck/lint/build green when backend changed (tooling from context)",
    "G5": "Verify — applicable verify skills ran; proofs attached",
    "G6": "Toolbox — no disposable scripts; versioned CLI used",
}


def parse_status_map(raw: str | None) -> dict[str, str]:
    """Parse G0=pass,G3=fail,G4=skip into a dict."""
    out: dict[str, str] = {}
    if not raw:
        return out
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            print(f"verify-checklist: bad status token {part!r}", file=sys.stderr)
            sys.exit(2)
        gate, status = part.split("=", 1)
        gate = gate.strip().upper()
        status = status.strip().lower()
        if gate not in ALL_GATES:
            print(f"verify-checklist: unknown gate {gate}", file=sys.stderr)
            sys.exit(2)
        if status not in {"pass", "fail", "skip", "pending"}:
            print(
                f"verify-checklist: status for {gate} must be pass|fail|skip|pending",
                file=sys.stderr,
            )
            sys.exit(2)
        out[gate] = status
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print / evaluate verify-handoff gates G0–G6 (versioned toolbox)."
    )
    parser.add_argument("--task-id", default="unspecified")
    parser.add_argument("--role", default="unspecified")
    parser.add_argument(
        "--gates",
        default=",".join(ALL_GATES),
        help="Comma-separated gates to require (default: all)",
    )
    parser.add_argument(
        "--status",
        default=None,
        help="Comma-separated G0=pass,G3=skip,… for applicable gates",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON summary",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List gate definitions and exit 0",
    )
    args = parser.parse_args()

    if args.list:
        for g in ALL_GATES:
            print(f"{g}\t{GATE_HELP[g]}")
        return 0

    requested = [g.strip().upper() for g in args.gates.split(",") if g.strip()]
    for g in requested:
        if g not in ALL_GATES:
            print(f"verify-checklist: unknown gate {g}", file=sys.stderr)
            return 2

    statuses = parse_status_map(args.status)
    results: list[dict] = []
    failed = False
    pending = False

    for g in requested:
        st = statuses.get(g, "pending")
        results.append({"gate": g, "status": st, "criterion": GATE_HELP[g]})
        if st == "fail":
            failed = True
        elif st == "pending":
            pending = True

    summary = {
        "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "task_id": args.task_id,
        "role": args.role,
        "gates": results,
        "ok": not failed and not pending,
        "failed": failed,
        "pending": pending,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"verify-checklist  task={args.task_id}  role={args.role}")
        for row in results:
            mark = {"pass": "✓", "fail": "✗", "skip": "–", "pending": "?"}.get(
                row["status"], "?"
            )
            print(f"  [{mark}] {row['gate']} {row['status']:7}  {row['criterion']}")
        if summary["ok"]:
            print("status: OK — all required gates pass/skip")
        elif failed:
            print("status: FAIL — fix failing gates before Done")
        else:
            print("status: PENDING — set --status for each required gate")

    if failed:
        return 1
    if pending:
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
