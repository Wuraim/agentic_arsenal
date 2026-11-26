---
name: figcraft-designer-dev
description: >
  FigCraft mockup work, designer↔dev comments, UI ambiguity. Versioned mockups,
  FigCraft as visual source of truth, wake designer on missing context. Use for
  any FigCraft or design-handoff task.
---

# FigCraft designer ↔ dev

## When to use

FigCraft mockup work, designer↔dev comments, UI ambiguity.

## Rules

- Mockups are **exportable files, versioned** in the repo (or an artifact tied to the commit).
- FigCraft server: VPS; URL + password via **1Password** — never commit secrets.
- **Designer →** after mockup changes, leave a textual comment when relevant (complex component, data vs placeholder).
- **Dev →** if context is missing: comment on the mockup + **explicitly wake** the designer agent; wait for the reply before inventing UI.
- Do **not** edit Obsidian / vault for visual truth; **FigCraft** is the visual source of truth.

## Handoff notes

- Designer → Dev: mockup path + open comments list.
- Dev → Designer (blocking when needed): FigCraft comment + wake; pause work on that zone until answered.
