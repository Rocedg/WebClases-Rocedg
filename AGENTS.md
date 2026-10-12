# Agent Instructions

This repository is a lightweight Flask web app for a Physics Bachillerato study platform. Any AI coding agent working here must keep the project understandable, small, and safe for a non-expert maintainer.

## Required Reading

Before implementing changes, read:

- `AGENTS.md`
- `docs/context/01-project-overview.md`
- `docs/context/02-architecture.md`
- `docs/context/03-code-standards.md`
- `docs/context/04-ai-workflow-rules.md`
- `docs/context/05-ui-context.md`
- `docs/context/06-progress-tracker.md`

For feature work, also read the relevant spec in `docs/context/feature-specs/`.

## Working Rules

- Work on one feature unit at a time.
- Never make broad unrelated changes.
- Never change architecture without explicit approval.
- Never rewrite Git history.
- Never force push.
- Keep Render compatibility.
- Keep `gunicorn app:app` working.
- Keep Flask as the web framework.
- Keep Jinja templates.
- Keep JSON content unless a dedicated spec approves a data-layer change.
- First-year exercise banks live under `content/exercises/1bach/tN/` as a
  `_topic.json` manifest plus ordered block files. Add new exercises to the
  corresponding block file.
- Keep the project understandable for a non-expert maintainer.
- Prefer small branches and pull requests.

## Before Editing

Before editing files:

- Restate the task scope.
- Summarize the plan.
- List the files expected to change.
- Identify any risky or broad changes that need approval.

## During Editing

- Keep changes focused.
- Do not mix product changes, visual redesign, architecture changes, and documentation cleanup unless the task explicitly asks for it.
- Do not change `app.py`, `templates/`, `static/`, `content/`, or dependencies during documentation-only tasks.
- If code changes are made, run tests.
- Preserve Render deployment assumptions.

## After Editing

After completing a unit:

- Summarize what changed.
- Summarize validation results.
- Update `docs/context/06-progress-tracker.md`.
- Report files changed.
- Report any known risks or follow-up work.

## Validation Expectations

- For documentation-only changes, run `git status`.
- If the local environment exists, run pytest when practical.
- For code changes, run the smoke tests and any relevant Flask import/test-client checks.
