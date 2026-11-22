# Code Standards

## Python and Flask

- Keep route functions small and readable.
- Prefer helper functions for repeated JSON loading or URL handling.
- Keep `app.py` understandable for a non-expert maintainer.
- Use clear function names such as `load_topics()` or `load_quizzes()`.
- Do not introduce blueprints or packages unless a dedicated architecture spec approves it.
- Keep environment-sensitive values, such as `SECRET_KEY`, configurable through environment variables.
- Persistence uses the existing Flask-SQLAlchemy setup (`database.py`, `models.py`). Do not add tables, columns, another ORM or a migration tool without an approved spec; there are no migrations, so schema changes are risky in production.

## Jinja Templates

- Extend `base.html` for normal pages.
- Use macros from `templates/components/` when a pattern repeats.
- Keep template logic simple.
- Do not hide complex product behavior inside templates.
- Prefer route-provided data over hardcoded repeated resource cards.
- Use `asset_url()` for JSON-provided static paths.

## CSS

- Respect the current split:
  - `tokens.css`
  - `layout.css`
  - `components.css`
  - `pages.css`
  - `responsive.css`
  - `style.css`
- Put design variables in `tokens.css`.
- Put reusable card/button/form styles in `components.css`.
- Put page-specific layout in `pages.css`.
- Put media queries and small-screen adaptations in `responsive.css`.
- Do not invent a new visual identity unless explicitly requested.

## JSON

- Use UTF-8.
- Keep top-level keys stable.
- Keep arrays readable and consistently ordered.
- Ensure every static PDF path exists.
- Do not rename IDs or paths casually.
- Validate JSON after editing.

## Naming Conventions

- Routes and Python helpers: `snake_case`.
- Template files: lowercase descriptive names.
- CSS classes: kebab-case or existing project naming style.
- JSON keys: lowercase with underscores where needed.
- Branches: small, descriptive names such as `dev/local-run-and-tests`.

## Error Handling

- For missing resources, prefer clear 404 responses.
- For invalid internal data, prefer clear 500 responses.
- Avoid exposing sensitive internal details to users.
- Keep user-facing error text friendly and understandable.

## Testing

- Use pytest for smoke tests.
- Keep tests simple.
- Prefer Flask test client checks for route behavior.
- Check JSON validity when JSON changes.
- Run tests when code changes are made.
- Documentation-only changes do not require full app testing, but `git status` should still be checked.

## Commit Style

- Use concise professional commit messages.
- One commit should represent one coherent unit of work.
- Avoid mixing unrelated work.
- Examples:
  - `Add local launch scripts and smoke tests`
  - `Add project context system for AI-assisted development`
  - `Fix broken exam PDF link`

