---
name: figcraft-designer-dev
description: >
  FigCraft maquette workflow for designer↔dev: live collab vs versioned
  `.figcraft`, comments, and when to override file-first rules so a human
  reviewer sees edits immediately. Use for FigCraft UX/mockup work.
---

# FigCraft designer ↔ dev

## When to use

- Editing or inspecting a **FigCraft** maquette.
- Designer ↔ dev handoff that depends on mockup frames or comments.
- Ambiguous UI that needs a mockup change before code.

## Locators (fill from project context)

| Field | What it is |
|---|---|
| **Versioned SoT** | Checked-in `.figcraft` (+ assets) in the consumer repo |
| **Live collab** | FigCraft collab WebSocket host + **file id** |
| **Join / auth** | Owner invite links minted at `collab.publish` — pattern `…&token=…`. **Never** hardcode tokens in skills, rules, or commits. Store/retrieve tokens via the project’s secret store or fresh owner links. |

### Example access card (AI Plan — from Project prefs, not a secret)

| Field | Value |
|---|---|
| Versioned | Consumer repo `design/ai-plan.figcraft` + `design/assets/` |
| Live host | `wss://figcraft.gregoirelorgnier.me:443/` |
| File id | `002c1cb55ec8e2f7` |
| Token | Owner join link only — do not paste into skills |

Other projects: replace host / file id / path from **their** context. This plugin does not ship product UI code.

## Live-first override (mandatory when stated)

When the project preference or task says the **owner / reviewer must see mockup edits immediately** (e.g. Grégoire reviewing UX):

1. Edit on the **live collab server** (host + file id above / from context) via FigCraft collab MCP or client.
2. **Override** any file-first guidance in `design-source-access` or older vault notes that say “always edit the versioned `.figcraft` first”.
3. Sync back to the versioned `.figcraft` in a later commit when persistence / Quality SoT needs it — do not skip live if immediacy was requested.

When immediacy is **not** required: prefer the versioned file (or project default).

## Designer → Dev

- After a maquette change the reviewer must see: confirm it is on **live** (and link/frames), then comment if the component or data vs placeholder needs explanation.
- UX that changed the maquette: show the live result and wait for owner go before Dev handoff when project prefs require it.
- If the versioned file already covers the need: no maquette edit — hand off Dev.

## Dev → Designer

- Missing context: leave a FigCraft comment + **explicitly wake** the designer agent; wait — do not invent UI.
- Do not treat Obsidian/vault notes as the visual SoT; FigCraft is.

## Quality compare

For `visual-quality-gate` / verify **G3**, prefer the **versioned** `.figcraft` (or a pinned export) unless context says to compare against live frames. Live is for collaborative edit visibility; versioned is the durable SoT for Quality.

## Anti-patterns

- Committing or embedding join `token=` values in this plugin or consumer skills.
- Editing only the repo `.figcraft` when the task required live visibility for the owner.
- Hardcoding one product’s frames as the only allowed FigCraft file inside generic gates — always fill locators from context.

## Related

- `design-source-access`, `figcraft-comments`, `visual-quality-gate`, `verify-handoff` (G0/G1/G3)
