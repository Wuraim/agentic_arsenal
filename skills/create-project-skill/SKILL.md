---
name: create-project-skill
description: >
  Create or update project-local Cursor skills in a repo that uses this plugin.
  Put stack-specific, product-specific, or team workflow knowledge in the
  consumer repo under .cursor/skills/ — never into this shareable plugin.
  Use when the user asks to add a skill, capture recurring context, encode a
  tech stack, or turn conversation guidance into a durable SKILL.md.
---

# Create a project-local skill

## When to use

- User asks to **create / add / update a skill** for their project.
- Recurring stack, design SoT, deploy, or review knowledge should survive chats.
- Personal or team conventions must **not** be committed into this plugin.

## Where skills go (consumer repo)

Prefer the **project that uses the plugin**, not the plugin repo itself:

```text
<consumer-repo>/
└── .cursor/skills/
    └── <skill-name>/
        ├── SKILL.md          # required
        ├── scripts/          # optional helpers
        ├── references/       # optional long docs (load on demand)
        └── assets/           # optional templates
```

Also valid: `.agents/skills/`, nested categories (e.g. `.cursor/skills/frontend/web-stack/`), or package-scoped `apps/web/.cursor/skills/…`.

**Do not** add consumer stack skills under this plugin’s `skills/` unless the user explicitly asks to extend the **shareable** toolkit for all users.

## Skills vs rules

| Need | Put it in |
|---|---|
| Short standing constraints (always / file-scoped) | `.cursor/rules/*.mdc` |
| Multi-step procedure, checklist, or domain playbook | `.cursor/skills/<name>/SKILL.md` |

If unsure: procedure → skill; one-liner policy → rule.

## Required SKILL.md shape

1. Folder name = skill `name` (lowercase, digits, hyphens).
2. YAML frontmatter with **`name`** and **`description`**.
3. `description` must state **what** and **when** (agents discover skills from it).

```markdown
---
name: example-stack
description: >
  Enforce this repo’s front stack and test commands. Use for any frontend
  change in this repository.
---

# Example stack

## When to use
- …

## Instructions
- …
```

Optional frontmatter: `paths` (globs to scope auto-use), `disable-model-invocation: true` (slash/`@` only).

## Authoring steps (agent)

1. Confirm target repo root (workspace that **consumes** the plugin).
2. Ask only if missing: skill purpose, when to trigger, hard constraints vs soft guidance.
3. Choose `name`; create `.cursor/skills/<name>/SKILL.md` (mkdir as needed).
4. Write a sharp `description` (discovery copy).
5. Keep the body focused: when / rules / steps / commands. Move long reference material to `references/` and link it.
6. If scripts are needed, put them under the skill’s `scripts/` and document exact invocations (prefer versioned repo/plugin CLI per `no-disposable-scripts`).
7. Do **not** duplicate this plugin’s verify / metrics / visual-gate skills — link or say “follow plugin skill X”.
8. Commit in the **consumer** repo when the user wants it persisted.

## Good project-skill topics (examples)

- Declared language/framework/package-manager conventions for **this** repo
- Design SoT location and review handoff for **this** product
- Deploy / release / env-specific checklists
- Domain glossary or API shapes agents keep getting wrong

## Anti-patterns

- Baking one team’s stack into the **shareable** Agentic Dev Toolkit plugin
- Empty or vague `description` (skill won’t auto-select reliably)
- Huge monolithic SKILL.md that should be split or use `references/`
- Replacing plugin gates (`verify-handoff`, `visual-quality-gate`) instead of specializing them with local paths/commands

## After creating

- Tell the user the path and how to invoke (`/` name, `@` skill, or auto via description).
- For Cloud Agents / shared team use: skill must live **in the repo** (committed), not only under `~/.cursor/skills/`.
