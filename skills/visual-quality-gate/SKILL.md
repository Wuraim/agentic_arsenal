---
name: visual-quality-gate
description: >
  Mandatory visual check for any UI/layout/CSS change. Compare code render to
  the design source of truth from conversation context via screenshots or
  recording before Done. Use whenever visual code changes.
---

# Visual quality gate

## When to use

Any visual code change: layout, CSS, UI components.

## Rules

- Verification is **mandatory** by visual comparison code ↔ **design source of truth from context** (screenshots / recording), not code review alone.
- Design SoT path/tooling comes from the conversation (mockup, Figma export, FigCraft, static spec, etc.) — do not assume a single product. See `design-source-access`.
- Mockup gap: **fix** or **document** + escalate to the design owner named in context.
- No merge / handoff as « done UI » without **attached visual proof**.

## Done criterion

- Visual evidence attached (screenshot or recording vs design SoT).
- Gate G3 satisfied via `verify-checklist` — see skill `verify-handoff`.
