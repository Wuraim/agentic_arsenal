---
name: design-source-access
description: >
  Locate and use the design source of truth (Figma, FigCraft, static mockups,
  or any other tool named in context). Use before UI work, visual QA, or when
  design feedback / comments must be read or escalated. Does not assume one
  design product — fill access details from conversation or project context.
---

# Design source access

## When to use

- Starting or continuing **UI / layout** work.
- Running `visual-quality-gate` or verify gates **G0 / G1 / G3**.
- Need to open mockups, read designer comments, or wake a design owner.

## Rule

Do **not** invent a design tool. Use the source of truth **named in context** (Figma, FigCraft, checked-in mockups, PDF/spec, etc.). If missing, ask once for the fields below — then proceed.

## Access card (fill from context)

| Field | What to capture |
|---|---|
| **Tool** | e.g. Figma, FigCraft, repo mockups, other |
| **Locator** | URL, file path, project/board id, version/tag |
| **Auth** | How agents/humans authenticate (SSO, link, vault ref) — never paste secrets into skills |
| **Owner** | Designer / design-owner handle or escalation path |
| **Comments** | Where feedback lives and how to mark resolved vs open |
| **Export** | How to get screenshots / frames for visual compare |

## Required behavior

1. Resolve the access card before writing UI that depends on a mockup.
2. Prefer the **versioned** locator (file in repo, pinned frame, tagged export) over a floating “latest”.
3. Read open design comments; resolve or escalate (gate **G1**).
4. For visual Done: compare implementation to this SoT and attach proof (`visual-quality-gate`, gate **G3**).
5. Mockup gap: fix, or document + notify the owner from the access card.

## Anti-patterns

- Hardcoding one vendor as the only allowed design tool in a shareable plugin.
- Skipping access because “I know the stack” without a locator.
- Storing API keys or passwords inside skill text.

## Related

- `visual-quality-gate`, `verify-handoff` (G0/G1/G3)
