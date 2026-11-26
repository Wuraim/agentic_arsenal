---
name: rust-backend
description: >
  Rust backend, Telegram bots, DB access, async services. Enforces Rust + Tokio
  + SQLx + Teloxide; SQLite by default; cargo check + clippy before handoff.
  Use for any backend Rust change.
---

# Rust backend

## When to use

Backend Rust, Telegram bots, database access, async services.

## Rules

- **Stack:** Rust + Tokio (async), SQLx (DB), Teloxide (Telegram).
- **SQLite by default**; Postgres only if the task justifies it.
- End of write: `cargo check` **and** `clippy` — failure = no handoff.
- **Forbidden:** `#[allow(clippy::…)]`, `unsafe` code.

## Verify (before handoff)

- `cargo check` green.
- Clippy green with no allows / no unsafe.
- Then run the plugin CLI `verify-checklist` (gate G4) — see skill `verify-handoff`.
