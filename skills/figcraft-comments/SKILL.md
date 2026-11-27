---
name: figcraft-comments
description: >
  Read, leave, resolve, or escalate FigCraft mockup comments (designer↔dev).
  Use with figcraft-designer-dev and design-source-access for gate G1.
---

# FigCraft comments

## When to use

- Open design feedback on a FigCraft maquette.
- Designer left notes Dev must acknowledge; Dev needs to ask on the mockup.
- Verify gate **G1** (feedback resolved or escalated).

## Where comments live

On the FigCraft file itself (live collab and/or the versioned document), via FigCraft MCP / client comments APIs — **not** only in chat.

Fill host, file id, and auth from project context (see `figcraft-designer-dev`). Join tokens come from owner publish links (`&token=…`); never store them in skills.

## Required behavior

1. Before UI Done: list open comments on the relevant frames; resolve or escalate with an open thread (**G1**).
2. Prefer commenting **on the live file** when the reviewer is watching collab so they see the thread immediately.
3. Designer: after non-obvious maquette edits, add a short comment (complex component, real data vs placeholder).
4. Dev: if the mockup is ambiguous, comment + wake the designer agent; do not invent.
5. Escalate to the design owner named in the project access card when stuck.

## Anti-patterns

- Closing G1 while FigCraft still has unanswered threads on in-scope frames.
- Putting secrets or join tokens inside comment text that gets committed.
- Treating chat-only feedback as a substitute when the project uses FigCraft comments as SoT.

## Related

- `figcraft-designer-dev`, `design-source-access`, `verify-handoff` (G1)
