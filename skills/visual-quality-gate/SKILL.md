---
name: visual-quality-gate
description: >
  Mandatory visual check for any UI/layout/CSS change. Compare code render to
  FigCraft mockup via screenshots or recording before Done. Use whenever visual
  code changes.
---

# Visual quality gate

## When to use

Any visual code change: layout, CSS, UI components.

## Rules

- Verification is **mandatory** by visual comparison code ↔ mockup (screenshots / recording), not code review alone.
- Mockup gap: **fix** or **document** + FigCraft comment + wake designer.
- No merge / handoff as « done UI » without **attached visual proof**.

## Done criterion

- Visual evidence attached (screenshot or recording vs mockup).
- Gate G3 satisfied via `verify-checklist` — see skill `verify-handoff`.
