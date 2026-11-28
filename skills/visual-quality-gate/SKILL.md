---
name: visual-quality-gate
description: >
  Mandatory visual check for any UI/layout/CSS change. Compare code render to
  the design source of truth from conversation context via screenshots or
  recording before Done — desktop and mobile, plus light and dark when the
  product has a theme toggle (document N/A otherwise). Use whenever visual
  code changes.
---

# Visual quality gate

## When to use

Any visual code change: layout, CSS, UI components.

## Rules

- Verification is **mandatory** by visual comparison code ↔ **design source of truth from context** (screenshots / recording), not code review alone.
- Design SoT path/tooling comes from the conversation (mockup, Figma export, FigCraft, static spec, etc.) — do not assume a single product. See `design-source-access`.
- For **compare / G3**, prefer the **versioned** locator (e.g. checked-in `.figcraft`) unless context says to use live frames. Live collab is for edit visibility (`figcraft-designer-dev`); versioned is the durable Quality SoT.
- Mockup gap: **fix** (live first when the owner must see immediately) or **document** + escalate to the design owner named in context.
- No merge / handoff as « done UI » without **attached visual proof**.
- A **visible gap** vs the design SoT is **NO-GO** even when CI / tests are green.

## Viewports and themes (required matrix)

Compare the rendered UI to the design SoT across the matrix below. Attach proof for each cell that applies; for cells that do not apply, **document N/A** with a one-line reason (do not silently skip).

| Axis | When required | When N/A |
|---|---|---|
| **Desktop** | Always for UI / layout / CSS changes | Never for visual UI work |
| **Mobile** | Always when layout can change by viewport (responsive / mobile frames exist, or the change touches layout/CSS) | Only if context proves the surface is desktop-only and has no mobile layout |
| **Light** | Always when the product has a light appearance (default for most UIs) | Only if the product is dark-only with no light theme |
| **Dark** | When the product has a **theme toggle**, `prefers-color-scheme` dark support, or dark design frames in the SoT | Document **N/A — no dark theme** when the product has neither a toggle nor dark SoT frames |

Practical expectations:

- Default visual QA = **desktop + mobile** (mirror typical product prefs such as AI Plan).
- When a theme toggle (or equivalent) exists, extend to **light + dark** — same pages/states as light, not a token-only glance.
- Prefer SoT frames that match each cell (e.g. FigCraft Desktop/Mobile and Light/Dark variants when present). If the SoT has no dark frames but the product toggles dark, still capture dark implementation proof and note the SoT gap.
- Proof may be screenshots and/or a short recording; label each artefact with viewport + theme (e.g. `desktop-light`, `mobile-dark`).

## Done criterion

- Visual evidence attached for every required matrix cell (or explicit N/A with reason).
- Gate G3 satisfied via `verify-checklist` — see skill `verify-handoff`.
