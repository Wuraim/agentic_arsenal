---
name: create-verify-cli
description: >
  Create or extend a versioned verification CLI in the consumer repo that plugs
  into verify-handoff gates (pass/fail/skip proofs, stable exit codes). Use when
  checks are recurrent, agents reach for disposable bash, or project-specific
  verify beyond the plugin’s verify-checklist is needed.
---

# Create a verify CLI

## When to use

- Recurrent verify/smoke/lint/visual-proof steps that agents keep re-scripting.
- Project needs checks **beyond** the generic plugin `bin/verify-checklist`.
- Enforcing gate **G6** (toolbox) / skill `no-disposable-scripts`.

## Rule

Ship a **versioned** CLI in the **consumer repo** (or extend this plugin’s toolbox when the check is truly cross-project). Never leave verify as a forgotten `/tmp` script in a Done handoff.

## Where it lives (consumer repo)

Prefer one of:

```text
<consumer-repo>/
├── bin/<name>           # stable entry (chmod +x)
├── scripts/<name>.py    # or .ts / .sh implementation
└── tools/<name>         # optional alias → bin/
```

Document the path in README or the project’s agent rules. Agents call the bin with flags — they do not regenerate the script each task.

## Contract (compatible with verify-handoff)

Align with the plugin checklist semantics so coordinators can reason uniformly:

| Concern | Convention |
|---|---|
| **Invocation** | `bin/<name> --task-id …` plus explicit flags (no hidden cwd magic) |
| **Gate ids** | Reuse `G0`–`G6` when mapping to handoff, or document custom ids clearly |
| **Statuses** | `pass` · `fail` · `skip` · `pending` |
| **Exit codes** | `0` ok · `1` fail · `2` usage · `3` pending (same as `verify-checklist`) |
| **Proofs** | Print paths or attach artefacts (logs, screenshots); machine `--json` optional |
| **Idempotent** | Safe to re-run; no destructive defaults |

Minimal shape:

```bash
./bin/verify-<domain> --list
./bin/verify-<domain> --task-id T-1 --gates G2,G4 --status G2=pass,G4=pass
# optional: --json
```

For domain checks (e.g. “front lint”, “api contract”), either wrap those commands inside this CLI or call them and map exit status → gate status.

## Authoring steps (agent)

1. Search existing toolbox (`bin/`, `tools/`, `package.json` scripts, CI). Extend before creating.
2. Name the tool (`verify-<domain>`); add `bin/` entry + implementation under `scripts/`.
3. Implement `--list`, `--gates`, `--status`, exit codes above; add `--json` if coordinators need it.
4. Wire docs: when to run, which gates it covers, example Done invocation.
5. Prefer calling **project quality commands** from `code-quality` context rather than duplicating logic in bash.
6. Run once successfully; use results as proofs for `verify-handoff` / `verify-checklist`.
7. Commit the CLI in the same deliverable that needed it (no “temporary” verify script).

## Relationship to the plugin checklist

- Keep using plugin `bin/verify-checklist` for the **generic** G0–G6 status rollup.
- Use the **project** verify CLI for stack-specific automation; report its outcomes into `--status` on `verify-checklist` or attach both outputs.

## Anti-patterns

- One-shot `python - <<'PY'` / `/tmp/verify.sh` as the Done artefact.
- CLI that always exits 0.
- Duplicating the entire plugin checklist with different exit-code meanings.

## Related

- `no-disposable-scripts`, `verify-handoff`, `code-quality`, plugin `bin/verify-checklist`
