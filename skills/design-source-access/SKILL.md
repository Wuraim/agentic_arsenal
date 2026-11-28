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

For **FigCraft** designer↔dev and live collab details, also read `figcraft-designer-dev` and `figcraft-comments`.

## Access card (fill from context)

| Field | What to capture |
|---|---|
| **Tool** | e.g. Figma, FigCraft, repo mockups, other |
| **Locator (versioned)** | Repo path, pinned frame, tagged export |
| **Locator (live collab)** | Collab host / board / file id when the tool supports live edit (e.g. FigCraft `wss://…` + file id) |
| **Auth** | How agents/humans authenticate (SSO, owner invite link with `&token=…`, vault ref) — **never** paste secrets into skills |
| **Owner** | Designer / design-owner handle or escalation path |
| **Comments** | Where feedback lives and how to mark resolved vs open |
| **Export** | How to get screenshots / frames for visual compare |

## Live vs versioned

| Goal | Prefer |
|---|---|
| Owner / reviewer must **see mockup edits immediately** | **Live collab** locator — edit on the live server first |
| Durable SoT, Quality / visual compare, commit history | **Versioned** locator (file in repo, pinned export) |

**Override:** when project prefs or the task say the reviewer must see changes right away, **live collab wins** over any file-first default in this skill or older notes. Sync to the versioned file later if the project needs a durable SoT.

FigCraft example (values from project context — AI Plan): host `wss://figcraft.gregoirelorgnier.me:443/`, file id `002c1cb55ec8e2f7`; join via owner-minted `&token=…` (not stored in skills). Full workflow: `figcraft-designer-dev`.

## Required behavior

1. Resolve the access card before writing UI that depends on a mockup.
2. Default: prefer the **versioned** locator for Quality compare and durable SoT.
3. When immediacy is required: edit via **live collab** first (see override above).
4. Read open design comments; resolve or escalate (gate **G1**). For FigCraft use `figcraft-comments`.
5. For visual Done: compare implementation to this SoT and attach proof across desktop+mobile and light+dark when applicable (`visual-quality-gate`, gate **G3**).
6. Mockup gap: fix (live if immediacy required), or document + notify the owner from the access card.

## Anti-patterns

- Hardcoding one vendor as the only allowed design tool in a shareable plugin.
- Skipping access because “I know the stack” without a locator.
- Storing API keys, passwords, or join tokens inside skill text.
- Editing only the versioned file when context required live visibility for the owner.

## Related

- `figcraft-designer-dev`, `figcraft-comments`, `visual-quality-gate`, `verify-handoff` (G0/G1/G3)
