---
name: verify-handoff
description: >
  Pre-Done verification checklist (gates G0–G6). Run before any Done / merge
  handoff. Implement without Verify is incomplete. Prefer the plugin CLI
  verify-checklist over ad hoc bash. Fill gate criteria from the stack and
  design SoT stated in conversation context — not hardcoded product stacks.
---

# Verify handoff

## When to use

**Before** every Done / merge handoff. Not optional.

## Rule

Implement without Verify = incomplete work. The coordinator must refuse Done if an applicable verify gate did not run.

## Gates (blocking)

Fill each applicable criterion from **conversation context** (declared stack, lint/test tools, design source of truth). Skip gates that do not apply and record them as `skip`.

| Gate | Criterion |
|---|---|
| **G0 Design SoT** | When UI is in scope: design source of truth from context is present. Prefer a **versioned** locator for durable SoT; when prefs require owner **immediate** mockup visibility, live collab SoT satisfies G0 for the UX edit (sync versioned later). See `design-source-access` / `figcraft-designer-dev`. |
| **G1 Feedback** | Design feedback / open questions resolved, or escalated with an open thread (`figcraft-comments` when FigCraft). |
| **G2 Stack conventions** | Declared project stack + format/lint/test conventions from context were followed. |
| **G3 Visual** | For UI changes: visual proof attached (screenshot/recording vs design SoT) across **desktop + mobile**, and **light + dark** when the product has a theme toggle (document N/A for dark otherwise). See `visual-quality-gate`. |
| **G4 Backend checks** | When backend changed: typecheck/lint/build green using tooling named in context. |
| **G5 Verify** | Applicable verify skills ran; proofs attached. |
| **G6 Toolbox** | No disposable scripts; actions via versioned CLI/toolbox (or CLI added in the same deliverable). |

## How to run

Prefer the versioned plugin CLI (do **not** invent a one-shot shell script):

```bash
# from repo root, or via plugin bin path
.cursor-plugin/agentic-dev-toolkit/bin/verify-checklist \
  --task-id AIP-… \
  --role implement \
  --gates G0,G1,G2,G3,G5,G6
```

Mark each applicable gate pass/fail. Attach artefacts (screenshots, check logs).

## Related skills

- `design-source-access`, `figcraft-designer-dev`, `figcraft-comments`, `visual-quality-gate`, `code-quality`, `create-verify-cli`, `no-disposable-scripts`, `code-metrics`
