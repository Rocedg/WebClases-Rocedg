# Architecture

## Runtime

`app.py` owns the Flask `app` object, routes, sessions, content loaders and CLI
commands. Render still starts with `gunicorn app:app`. `templates/` and `static/`
remain at Flask's conventional locations. There are no new blueprints, frontend
build tools or application packages.

`database.py` configures the existing Flask-SQLAlchemy extension. `models.py`
defines activity, quiz attempt, exercise attempt and response tables. `services/`
contains activity and exercise logic. Local persistence remains
`instance/web_clases_rocedg.sqlite`; production can use `DATABASE_URL`.

## Content map

| Concern | Editable content / metadata | Public delivery |
| --- | --- | --- |
| Proprietary lessons | `content/lessons/lessons.json`, `content/lessons/latex/` | `static/lessons/` |
| Lesson preparation | `content/lessons/intake/` (processing/unchecked stages) | Sources are not served |
| Reference topics | `content/lessons/topics.json` | Existing `static/pdfs/topics_y1/`, `topics_y2/` |
| Summaries and formula sheet | `content/lessons/summaries.json` | Existing `static/pdfs/resumenes/`, `formulario.pdf` |
| Guided exercises | `content/exercises/<course>/<topic>/exercises_<topic>.json` | `static/exercises/<course>/<topic>/` |
| Exercise LaTeX templates | `content/exercises/latex/` | Generated PDFs under `static/exercises/` |
| Exercise summary index | `content/exercises/index.json` (generated) | Loaded by Flask, not served statically |
| Quizzes | `content/exercises/quizzes.json` | Existing `static/pdfs/quizzes/` |
| Exams | `content/exams/exams.json` | Existing `static/pdfs/examenes/` |

The full exercise catalogue is loaded from topic JSON, with the generated index
as a fallback. The current 1bach banks are separate files:
`exercises_t0.json`, `exercises_t1.json`, and `exercises_t2.json`. The loader
reads each bank independently. The existing 2bach editorial fixture still uses
its own legacy `exercises.json` path and remains supported separately. SQL stores
student work keyed by exercise ID and version; it does not replace JSON
educational content.

Keep source/reference material and public assets separate. Existing public URLs
are stable because bookmarks and activity rows may contain those paths. Intake
PDFs are working source copies; legacy static PDFs are the public reference
library. This is an intentional source/public distinction, not competing content
roots. No compatibility symlinks or duplicate runtime loaders are used.

## Templates and frontend

- `templates/base.html`: layout, shared navigation and footer.
- `templates/components/`: reusable Jinja macros.
- `templates/user/`: study, practice, history and progress pages.
- `templates/errors/`: error pages.
- `static/css/`: tokens, layout, components, pages, responsive rules and the main
  `style.css` import file.
- `static/js/`: PDF lesson viewer, exercise MathJax configuration, existing
  exercise timer, and quiz progress behavior. Jinja passes dynamic values through
  HTML attributes.
- `static/images/`: shared brand assets.
- `static/vendor/pdfjs/`: pinned third-party browser runtime.

Use `asset_url()` and `url_for()` for resource references. Lesson PDFs are built
before deployment; requests never invoke LaTeX. Protected viewer routes and
resource tracking behavior are unchanged by the repository cleanup.

## Tools and documentation

`scripts/` contains Windows launch/setup scripts, exercise index generation,
content validation, lesson builds and review utilities. Launchers resolve the
repository from their own location. Lesson builds write to ignored
`tmp/lesson-review/`; approved PDFs are published separately.

`tests/` contains pytest smoke and integration tests. Tests use a temporary
database and must not replace the user's `instance/` database.

`docs/` is the documentation root. `docs/context/` holds agent context, feature
specifications and the chronological progress tracker; `docs/design/` holds
visual references. `README.md` and `AGENTS.md` remain discoverable entry points.
Older planning documents retain historical paths, with a current-path note.

## Invariants

- Keep Flask, Jinja and `gunicorn app:app`.
- Keep JSON learning content and the existing SQLAlchemy schema.
- Keep public PDF/asset URLs and resource IDs stable.
- Keep dependencies in `requirements.txt`; Render does not need LaTeX.
- Keep local databases, credentials, environments, caches and build output out of Git.
- Avoid moving backend modules or adding frameworks merely to change the tree.
