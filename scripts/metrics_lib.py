"""Shared helpers for code-metrics store resolution and JSONL append."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def plugin_root() -> Path:
    """Resolve plugin root: CURSOR_PLUGIN_ROOT, else parent of scripts/."""
    env = (os.environ.get("CURSOR_PLUGIN_ROOT") or "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


def load_settings() -> dict[str, Any]:
    path = plugin_root() / "settings.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def metrics_enabled(settings: dict[str, Any] | None = None) -> bool:
    data = settings if settings is not None else load_settings()
    return bool(data.get("metricsEnabled", True))


def resolve_store_path(explicit: str | None = None) -> Path | None:
    """Return store Path (file .jsonl or directory), or None if unset."""
    raw = (
        (explicit or "").strip()
        or (os.environ.get("AGENTIC_METRICS_STORE") or "").strip()
        or (os.environ.get("AGENTIC_DEV_TOOLKIT_METRICS_STORE") or "").strip()
    )
    settings = load_settings()
    if not raw:
        raw = (settings.get("metricsStorePath") or "").strip()
    if not raw:
        return None

    path = Path(raw).expanduser()
    if not path.is_absolute():
        path = (plugin_root() / path).resolve()
    else:
        path = path.resolve()
    return path


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def append_event(event: dict[str, Any], store: Path | None = None) -> Path | None:
    """
    Append one JSONL event. Returns written path, or None if skipped.
    Skips when metrics disabled or store unset. Never raises for skip cases.
    """
    settings = load_settings()
    if not metrics_enabled(settings):
        print("metrics: metricsEnabled=false — skip (no-op)", file=sys.stderr)
        return None

    target = store or resolve_store_path()
    if target is None:
        print(
            "metrics: no store configured "
            "(AGENTIC_METRICS_STORE / settings.metricsStorePath) — skip (no-op)",
            file=sys.stderr,
        )
        return None

    if "ts" not in event:
        event = {**event, "ts": utc_now_iso()}

    if target.suffix == ".jsonl":
        path = target
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        target.mkdir(parents=True, exist_ok=True)
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        path = target / f"metrics-{day}.jsonl"

    line = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return path


def _model_from_payload(payload: dict[str, Any]) -> str:
    for key in ("model_id", "model", "subagent_model"):
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return "unknown"


def _success_from_status(status: Any) -> bool:
    if not isinstance(status, str):
        return True
    return status.lower() in {"completed", "success", "ok", "pass"}


def _task_kind_from_subagent(subagent_type: str | None) -> str:
    if not subagent_type:
        return "other"
    mapping = {
        "explore": "explore",
        "shell": "shell",
        "generalPurpose": "implement",
        "browserUse": "browser",
        "computerUseV2": "browser",
        "ci-investigator": "review",
        "bugbot": "review",
        "security-review": "review",
        "cursor-guide": "docs",
        "best-of-n-runner": "implement",
    }
    return mapping.get(subagent_type, "other")


def event_from_stop_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Map Cursor `stop` hook stdin JSON → metrics event."""
    conversation_id = payload.get("conversation_id") or payload.get("session_id")
    generation_id = payload.get("generation_id")
    task_id = conversation_id or generation_id or "unknown"
    status = payload.get("status")
    latency = payload.get("duration_ms")
    if latency is None and isinstance(payload.get("duration"), (int, float)):
        latency = int(payload["duration"])

    signals: dict[str, Any] = {
        "hook": "stop",
        "status": status,
        "loop_count": payload.get("loop_count"),
    }
    if generation_id:
        signals["generation_id"] = generation_id
    if conversation_id:
        signals["conversation_id"] = conversation_id

    return {
        "ts": utc_now_iso(),
        "task_id": str(task_id),
        "role": "agent",
        "task_kind": "other",
        "model": _model_from_payload(payload),
        "latency_ms": int(latency) if isinstance(latency, (int, float)) else None,
        "cost_est": None,
        "success": _success_from_status(status),
        "signals": {k: v for k, v in signals.items() if v is not None},
    }


def event_from_subagent_stop_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Map Cursor `subagentStop` hook stdin JSON → metrics event."""
    subagent_type = payload.get("subagent_type")
    if isinstance(subagent_type, str):
        subagent_type = subagent_type.strip() or None
    else:
        subagent_type = None

    task_id = (
        payload.get("subagent_id")
        or payload.get("tool_call_id")
        or payload.get("parent_conversation_id")
        or payload.get("conversation_id")
        or "unknown"
    )
    status = payload.get("status")
    latency = payload.get("duration_ms")

    signals: dict[str, Any] = {
        "hook": "subagentStop",
        "status": status,
        "subagent_type": subagent_type,
        "message_count": payload.get("message_count"),
        "tool_call_count": payload.get("tool_call_count"),
        "loop_count": payload.get("loop_count"),
    }
    modified = payload.get("modified_files")
    if isinstance(modified, list):
        signals["modified_file_count"] = len(modified)
    desc = payload.get("description")
    if isinstance(desc, str) and desc.strip():
        signals["description"] = desc.strip()[:200]

    return {
        "ts": utc_now_iso(),
        "task_id": str(task_id),
        "role": "subagent",
        "task_kind": _task_kind_from_subagent(subagent_type),
        "model": _model_from_payload(payload),
        "latency_ms": int(latency) if isinstance(latency, (int, float)) else None,
        "cost_est": None,
        "success": _success_from_status(status),
        "signals": {k: v for k, v in signals.items() if v is not None},
    }


def iter_jsonl_events(store: Path) -> list[dict[str, Any]]:
    """Load all metrics events from a .jsonl file or a directory of daily files."""
    files: list[Path] = []
    if store.suffix == ".jsonl":
        if store.is_file():
            files = [store]
    elif store.is_dir():
        files = sorted(store.glob("metrics-*.jsonl"))
    events: list[dict[str, Any]] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                events.append(obj)
    return events
