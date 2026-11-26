---
name: verify-handoff
description: >
  Pre-Done verification checklist (gates G0–G6). Run before any Done / merge
  handoff. Implement without Verify is incomplete. Prefer the plugin CLI
  verify-checklist over ad hoc bash.
---

# Verify handoff

## When to use

**Before** every Done / merge handoff. Not optional.

## Rule

Implement without Verify = incomplete work. The coordinator must refuse Done if an applicable verify gate did not run.

## Gates (blocking)

| Gate | Criterion |
|---|---|
| **G0 Maquette** | FigCraft file present and versioned before UI code. |
| **G1 Commentaires** | Designer comments read; open questions resolved or thread open + designer woken. |
| **G2 Stack** | Front: PNPM/Nuxt/Vite/TS + Prettier/Vitest. Back: Tokio/SQLx/clippy without allow/unsafe. |
| **G3 Visuel** | Visual comparison mockup ↔ implementation for any UI. |
| **G4 Rust** | `cargo check` + clippy green after backend writes. |
| **G5 Verify** | Applicable verify skills ran; proofs attached. |
| **G6 Toolbox** | No disposable scripts; actions via versioned CLI/toolbox (or CLI added in the same deliverable). |

## How to run

Prefer the versioned plugin CLI (do **not** invent a one-shot shell script):

```bash
# from repo root, or via plugin bin path
.cursor-plugin/agentic-dev-toolkit/bin/verify-checklist \
  --task-id AIP-… \
  --role dev-front \
  --gates G0,G1,G2,G3,G5,G6
```

Mark each applicable gate pass/fail. Attach artefacts (screenshots, check logs). Skip gates that do not apply (e.g. G4 when no Rust) and record them as `skip`.

## Related skills

- `web-stack`, `rust-backend`, `visual-quality-gate`, `no-disposable-scripts`, `figcraft-designer-dev`
