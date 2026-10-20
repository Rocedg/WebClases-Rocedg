# Progress Tracker

## 2026-10-12

- Added T0 unit-vector practice exercises `t0_v_050` through `t0_v_057` in the ordered split bank.
- Added independent numerical checks and updated T0 catalogue/test counts.

## Current Phase

Repository cleanup on `chore/repository-cleanup`, based on safety checkpoint `5d6ad08`. The user explicitly authorized checkpoint/push and repository reorganization on 2026-09-14. Current content paths are documented in `docs/context/02-architecture.md`; dated entries below retain historical paths.

## Completed

- Panel de profesor en modo lectura añadido: resumen de alumnos, seguimiento individual, historial de intentos y respuestas enviadas, con acceso protegido por `teacher_required`.

- First provisional complete 1.º Bachillerato version prepared on `main`: T0–T6 lessons and guided practice are connected by topic, the public exercise catalogue is limited to 1.º, and reserved quiz PDFs plus the unrelated 2.º induction pilot remain stored but inaccessible from web routes.
- Real study continuity and progress dashboard implemented locally: the database now records the last lesson and last exercise topic/type, the guided-practice landing groups exercises by readable pedagogical type with catalogue metrics, and progress uses persisted visits, attempts, scores and active time instead of placeholder values.

- Repository history cleaned.
- Visual/site structure redesign merged to `main`.
- Executive documentation added to `main`.
- Local launch scripts and smoke tests branch created and pushed, pending merge unless already merged.
- Generated local/cache artifact cleanup branch created.
- Executive code documentation refreshed on `main`.
- UI redesign foundation started on `dev/ui-redesign-foundation`.
- Exercise system stack/spec documented.
- First content skeleton branch merged to `main`.
- User activity backend persistence spike merged to `main`.
- UI redesign foundation merged to `main` with the activity backend preserved.
- T0 introductory lesson PDF pilot created, compiled, and connected to Apuntes with existing resource tracking.
- T0 lesson PDF open/download actions separated with explicit inline/attachment headers.
- T0 lesson viewer page added so students open the lesson inside the Web Clases Rocedg layout before downloading or practicing.
- T0 lesson PDF refined to v0.2 with a nine-page, one-column guided layout and updated app page-count metadata.
- T0 lesson PDF refined to v0.3 with four didactic blocks, expanded measurement-quality explanations, and a fuller calculus section.
- T1 Movimiento rectilíneo PDF v0.1 created as a 12-page four-block lesson, compiled locally, and registered in lesson metadata for viewer/download review.
- T2 Movimiento en el plano PDF v0.1 created as a 15-page four-block lesson, compiled locally, and registered in lesson metadata for viewer/download review.

- T0, T1, and T2 lesson PDFs updated with consistent visual differentiation: white theory cards with blue headings, pale teal solved-example cards, pale amber practice cards, labeled attention boxes, and separated solution/check areas.
- T0, T1, and T2 lesson PDFs recompiled from the latest LaTeX content in `content/latex`; T0 metadata now reflects the generated 14-page PDF.
- Persistent exercise-attempt MVP implemented on `dev/exercise-attempts-mvp`: JSON-backed exercises now support explicit SQL attempts, draft saves, deterministic submission grading, pending-review responses, and a minimal student history.
- Guided exercise student UX polished on `dev/exercise-practice-ux-polish`: catalogue cards now start or continue attempts directly via POST/link, filters are server-rendered, MathJax renders exercise notation, submitted attempts show guided solutions plus retry/next actions, and diagrams are contained.
- T0 exercise bank v4 implemented on `dev/t0-exercise-bank-v4`: active Tema 0 practice now contains 80 versioned exercises across units, vectors, measurement/error, and calculus/graphs, with retired IDs preserved in metadata for historical attempts.
- Exercise grading/timer polish implemented on `dev/exercise-grading-timer-polish`: semantic unit-expression grading replaces string comparison, pending-review scoring is provisional, student exercise UI hides internal metadata, catalogue cards show New/In progress/Completed backgrounds, active attempts persist an optional active-time timer, and submitted/history views display measured active duration.

## In Progress

- None.

## Next Recommended Work

1. Review the repository cleanup branch and the preserved lesson/PDF changes before any separately authorized merge.
2. Remove generated LaTeX `.aux`/`.out` review artifacts if they appear in the working tree before commit.
3. Review the T0 v0.3 PDF and embedded lesson viewer if not already approved.
4. Later: add database migrations before relying on production schema changes.
5. Later: replace hardcoded users with a real user table.
6. Later: build teacher review for submitted exercise responses.
7. Later: replace rough generated exercise diagrams with a shared SVG diagram system.

## Decisions

- Keep Flask/Jinja templates.
- Keep JSON for learning content for now.
- Use small branches and PRs.
- Use specs before Codex implements changes.
- Keep Render compatibility.
- Keep the app understandable for a non-expert maintainer.
- Use `Web Clases Rocedg` as the brand name, with `Física` as a subject pill.
- Use SQLAlchemy/Flask-SQLAlchemy for the persistence spike.
- Use SQLite locally by default.
- Keep `DATABASE_URL` PostgreSQL-ready for production later.
- Store PDF/image paths and metadata only, not files.
- Do not refactor authentication yet; associate activity by session username.
- Do not build the full dashboard yet.
- Do not build the teacher dashboard yet.
- Do not expand the exercise system in the UI redesign update branch.
- Exercise attempts use dedicated `ExerciseAttempt` and `ExerciseResponse` tables instead of extending quiz attempts.
- Exercise content stays in JSON; SQL rows store user work keyed by `exercise_id` and `exercise_version`.
- Exercise catalogue filtering stays server-rendered with GET query parameters.
- Exercise math rendering uses MathJax 3 loaded on exercise detail pages only.

## Limitations

- Exact PDF page tracking requires a controlled PDF viewer later.
- Direct static file downloads are not trackable unless users enter through a Flask route.
- The current tracked resource route records open/download clicks before serving or redirecting resources.
- Current hardcoded users are associated by username only.
- Tracked PDF routes now serve local PDFs directly with explicit `Content-Disposition` and no-store cache headers.
- The T0 lesson viewer records `lesson_viewed` on `/lesson/T0-introduccion`, embeds the static PDF to avoid double-counting, and tracks downloads through `/resource/lesson_pdf/.../download`.

## Risks

- Maintainer losing understanding due to too many AI-generated changes.
- Overengineering too early.
- Mixing UI polish with future exercise-system/backend changes.
- Accidentally changing app behavior during documentation or tooling tasks.
- Adding a database before the product model is clear.
- Letting old design reference locations or placeholder branding leak into review.

## Update Log
- 2026-10-12: Añadido el panel de profesor en modo lectura con resumen de alumnos, seguimiento individual y consulta de respuestas de intentos sin relajar la propiedad de los intentos estudiantiles.
- 2026-10-12: La lista de seed de `app.py` queda limitada a las cuentas de prueba `Guest` y `Edgar`. Los alumnos reales se conservan en `users` y se crean desde `/teacher/accounts`; los tests aíslan sus cuentas auxiliares sin cambiar el comportamiento aditivo del seed ni la autenticación basada en la base de datos.

- 2026-10-12: Añadida la gestión de cuentas de alumnos para el profesor: creación con contraseña inicial, restablecimiento, desactivación/reactivación, validación de usuarios y navegación protegida por `teacher_required`.

- 2026-10-12: Añadida la tabla `users` como fuente única de autenticación, con contraseñas hash, sembrado inicial idempotente por `USERS` y cambio de contraseña en `/account/password`. La navegación enlaza la cuenta y se añadieron pruebas de roles, validación de contraseñas y persistencia del cambio.


- 2026-10-12: Fijado SQLAlchemy en `2.0.52` y normalizadas las URLs `postgres://` y `postgresql://` a `postgresql+psycopg2://`, manteniendo intactas las URLs con driver explícito y SQLite. Añadida cobertura unitaria para las cuatro formas de URL.

- 2026-10-12: Configuradas las opciones de SQLAlchemy `pool_pre_ping` y `pool_recycle` para que las conexiones de Neon Postgres se recuperen tras periodos de inactividad. SQLite local y los tests mantienen su configuración existente. Documentado el uso de Neon mediante `DATABASE_URL` y la necesidad de `SECRET_KEY` en Render.

- 2026-10-12: Ordered the homework exercise-type filter by topic and lesson order, grouped with topic optgroups while preserving stable type keys and selected GET filters. Added T0 ordering coverage and validated the catalogue rendering.

- 2026-10-12: Added exercise numbers next to titles in the guided catalogue, exercise detail page and attempt history. Numbers are derived from the numeric ID suffix without changing exercise IDs or ordering. Added the shared Jinja helper, muted tabular-number styling and unit coverage for numbered and legacy IDs. Validation: pytest and `git diff --check`.

- 2026-09-29: Added the `teacher` role on `feat/teacher-role`. New accounts `Sandro` (student) and `Edgar` (teacher) with hard-coded passwords, as the maintainer chose (the GitHub repository is public; the teacher password must move to an environment variable before the dashboard ships). Teachers already see every student page through `login_required`. Added a `teacher_required` decorator (403 for non-teachers) reserved for the future dashboard, Spanish role labels in the navigation (`Alumno`/`Profesor`), and the spec `feature-specs/teacher-dashboard.md`. No dashboard route, template, model or dependency changes. Validation: 90 pytest tests, including 4 new role tests.

- 2026-09-29: Fixed the Render 500 on `/homework`, `/exercise/<id>` and `/practice/history` (`no such table: exercise_attempts`) on `fix/render-db-schema`. Render has no `DATABASE_URL`, so the app uses SQLite on an ephemeral disk that starts empty after every deploy or restart, and tables were only created by `flask --app app init-db`. `app.py` now runs `db.create_all()` and `ensure_database_schema()` once at import inside an app context (idempotent; failures are logged, nothing is dropped). Boolean defaults in `ensure_database_schema()` now use `TRUE`/`FALSE` for Postgres compatibility, and the 500 handler logs the original exception with its traceback. Validation: 86 pytest tests; a brand-new SQLite file without `init-db` served login, `/homework`, an exercise, "Empezar", the attempt view and `/practice/history` without a 500; an old database missing `user_study_state`, the timer columns and `canonical_value` was repaired at startup while keeping an existing attempt row. Not tested against Postgres (no local server). Known risk: student attempts and progress are still lost on every Render deploy/restart until a persistent Postgres `DATABASE_URL` is configured.

- 2026-09-21: Implemented the local T3–T6 exercise banks from their reviewed Markdown specifications. Added 60 `draft` exercises per topic (240 total) using compact `statement_source`/`solution_source`, structured server-side grading fields, part associations, no hints or open responses, and one responsive SVG per exercise. Added the reproducible `scripts/build_t3_t6_exercise_banks.py` builder, which checks by default and writes only with `--write`; a second check reported zero differences. Extended catalogue, index and metadata discovery through `exercises_t6.json`; the index now contains 441 visible exercises. Added bank completeness, source safety, SVG validity, idempotence and catalogue tests. Validation: 82 pytest tests; 444 metadata records with only the pre-existing planned 2bach resource warnings; 12 representative T3–T6 exercises reviewed in Chromium at 1440px and 390px (24 views) without overflow, MathJax errors, broken SVGs, hint blocks, metadata leaks or browser exceptions. All changes remain local and uncommitted for user testing.

- 2026-09-21: Added preliminary editorial exercise-bank specifications for the remaining 1.º Bachillerato topics T3–T6, without creating JSON or changing runtime code. Each reference defines 60 original, structured exercises (240 total) with consecutive IDs, block distribution, scenario/data, grading key, required SVG or graph, shared response constraints and acceptance criteria. The plans emphasize free-body diagrams and system choice in T3, friction regimes and experimental/model selection in T4, state/transfer energy reasoning in T5, and system boundaries, impulse graphs and collision timelines in T6. No hints, uploads or ungradable free-response modes are planned. Minimum visual targets are 36 SVGs for T3, 42 for T4, 40 for T5 and 44 for T6. A local audit confirmed all 240 IDs and family sequences; `git diff --check` passed.

- 2026-09-17: Extended the compact exercise-source standard to every remaining visible T0-T2 exercise using the reproducible `scripts/migrate_compact_exercises.py` utility (read-only check by default, explicit `--write`). Migrated 75 additional T0, 58 T1 and 58 T2 records; together with the six-record pilot, the visible compact banks now contain 77 T0, 60 T1 and 60 T2 exercises. Preserved IDs, ordering, versions, expected answers, solution content, sources, assets and T1/T2 `draft` states. Removed hints and unstructured response fields; added deterministic vector, function and verifiable short-text grading while retaining numeric, selection and unit-expression grading. Retired `t0_m_007`, `t0_c_007` and `t0_c_018` in place because each depended completely on free development that could not be graded reliably; historical attempt titles remain resolvable. Replaced two clearly poor T2 SVGs (`t2_v_006`, which exposed component values, and `t2_c_005`, which used incoherent axes) with responsive contextual diagrams. Validation: 78 pytest tests; T0 bank and mathematical validators; all 10 content JSON files parsed; all 197 visible T0-T2 exercises use compact canonical statements, supported structured fields and no hint/interactions metadata; migration check is idempotent. Chromium reviewed nine exercises (three per topic) at 1440px and 390px: 18 views had no overflow, MathJax error, broken SVG, hint block, metadata leak or browser exception. The general metadata validator passed with only the pre-existing missing planned 2bach resource warnings.

- 2026-09-17: Implemented the compact-source exercise pilot only for `t0_v_018`, `t0_c_020`, `t1_r_004`, `t1_g_011`, `t2_h_001`, and `t2_c_001`. T0 remains active; the four T1/T2 exercises retain `draft` at the user's explicit request. Added escaped `statement_source` / `solution_source` rendering (blank-line paragraphs, lettered parts, inline/block TeX), legacy HTML/math compatibility, dynamic `MathJax.typesetPromise`, type-specific shared format guidance, and deterministic two-component vector grading. Pilot content uses only `response_fields`, with `part` associations, no hints or open-ended questions, and no duplicate canonical HTML/solution metadata. Corrected answer-bearing unit suffixes in `t0_c_020`; solution markup remains submission-only. Reviewed/replaced the six SVGs with local vector axes, Cartesian plots, stacked x(t)/v(t) panels, a contextual trajectory and a circular-motion diagram. IDs, versions, stored attempts, progress logic, database schema, dependencies and deployment entry point are unchanged. The other 194 exercises in the three banks were checked against pre-edit local snapshots and are unchanged. Validation: 74 pytest tests; metadata validation for 204 exercises (only the existing missing planned 2bach assets/PDFs warnings); T0 bank/math validators; Chromium checks for all six at desktop 1440px/mobile 390px, with no horizontal overflow, MathJax errors, broken diagrams or browser exceptions. Dynamic replacement, legacy formulas and submitted solution rendering passed. Captures and browser report are local ignored artifacts under `tmp/exercise-pilot/`. Existing unrelated working-tree changes were preserved. Stop at this pilot; extending the migration requires user confirmation.

- 2026-05-03: Created initial project context system on `dev/project-context-system`.
- 2026-05-03: Cleaned generated local/cache artifacts and expanded `.gitignore` on `dev/cleanup-local-artifacts`.
- 2026-05-03: Refreshed executive code documentation and regenerated the PDF on `main`.
- 2026-05-03: Documented the future interactive exercise system on `dev/exercise-system-spec`.
- 2026-05-03: Started exercise content skeleton work on `dev/exercise-content-skeleton`.
- 2026-09-05: Began UI redesign foundation work on branch `dev/ui-redesign-foundation` - updated templates and CSS tokens to the "Web Clases Rocedg" visual system (brand, colors, layout, responsive rules). No backend or exercise-system changes were made.
- 2026-09-05: Cleaned the UI redesign branch scope by removing exercise/intake/backend artifacts, moving design references under `docs/design/ui-redesign-reference/`, adding the real logo as a static brand asset, and polishing existing templates/CSS. No route, data model, dependency, or authentication changes were made.
- 2026-09-05: Refined the home dashboard structure with a compact welcome panel, four real-count metric cards, a prominent illustrative route recommendation, four direct-access cards, and three recommended-practice cards. No backend, route, data, dependency, or authentication changes were made.
- 2026-09-06: Replaced the top-level PAU navigation item with a visual-only Progreso area, added a protected `/progress` mock page, moved summary resources into the Apuntes page presentation, and kept `/miscellaneous` available without promoting it in main navigation. No database, persistence, data-file, exercise-system, or dependency changes were made.
- 2026-09-06: Started `dev/user-activity-backend-spike` from latest `main` to add a minimal SQLAlchemy persistence foundation for activity events, topic/resource access, quiz attempts, and a simple real-data `/progress` page. No auth refactor, teacher dashboard, recommendation engine, PDF viewer, or exercise-system expansion is included.
- 2026-09-06: Merged latest `main` into `dev/ui-redesign-foundation`, preserving the activity backend and restyling `/progress` so it shows real saved activity inside the UI redesign system. PAU remains available at `/miscellaneous` but is not a top-level navigation item.
- 2026-09-07: Merged `dev/ui-redesign-foundation` into `main` after final pytest, database initialization, local launch, and route checks. Existing exercise skeleton files from `main` were preserved without starting new exercise-system work.
- 2026-09-07: Started `dev/t0-lesson-pdf-pilot` from latest `main`; created a polished T0 introductory lesson PDF in LaTeX, exposed it on `/topics`, and reused the existing activity tracking route for lesson PDF open/download clicks.
- 2026-09-07: Fixed tracked PDF response behavior so open actions return explicit inline PDFs and download actions return explicit attachments, while preserving activity tracking and avoiding stale tracked-route caches.
- 2026-09-08: Added `/lesson/T0-introduccion` as an embedded Web Clases Rocedg lesson viewer, changed the T0 Apuntes primary action to `Ver lección`, kept tracked downloads, and validated lesson view/download events on `/progress`.
- 2026-09-08: Refined the T0 lesson PDF to v0.2: added an introductory page, changed the PDF to a nine-page one-column guided layout, redrew diagrams in TikZ, compiled the static lesson PDF, and updated the lesson page count.
- 2026-09-08: Refined the T0 lesson PDF to v0.3: reorganized the lesson into four didactic blocks, replaced the visual roadmap with a linked vertical index, updated page numbering to `Página X de Y`, expanded uncertainty and calculus explanations, recompiled the static PDF, and updated the lesson page count.
- 2026-09-08: Created T1 Movimiento rectilíneo v0.1 locally: built a four-block LaTeX lesson, preserved and corrected the requested MRU/MRUA examples, compiled `static/lessons/T1-movimiento-rectilineo.pdf`, registered it in `content/lessons.json`, and validated tests plus local viewer/download behavior. No commit/push was made.
- 2026-09-08: Created T2 Movimiento en el plano v0.1 locally: built a four-block LaTeX lesson, preserved and corrected the requested composition/projectile/circular examples, compiled `static/lessons/T2-movimiento-en-el-plano.pdf`, and registered it in `content/lessons.json`. No commit/push was made.
- 2026-09-09: Applied a stable activity visual code across T0, T1, and T2 PDFs: theory remains white/blue, examples use pale teal cards labeled `Ejemplo resuelto`, practice uses pale amber cards labeled `Prueba tu`, checks are separated with `Solucion o comprobacion`, and generic warnings use labeled `Atencion` boxes instead of example/practice backgrounds. Recompiled the three lesson PDFs locally; no commit/push was made.
- 2026-09-09: Recompiled `static/lessons/T0-introduccion.pdf`, `static/lessons/T1-movimiento-rectilineo.pdf`, and `static/lessons/T2-movimiento-en-el-plano.pdf` from the latest `.tex` files in `content/latex`; updated T0 lesson metadata to 14 pages after recompilation.
- 2026-09-09: Created `dev/exercise-attempts-mvp` from the current SQL activity backend and exercise catalogue base; added dedicated exercise attempt/response persistence, explicit start/resume, draft save, submit with limited deterministic grading, ownership checks, `/practice/history`, focused tests, and `docs/exercise-attempts.md`.
- 2026-09-12: Created `dev/exercise-practice-ux-polish` from `dev/exercise-attempts-mvp`; removed the normal empty-start detour from the catalogue, added per-student exercise CTAs, GET filters, semantic badges, MathJax exercise rendering, submitted guided solutions, deterministic next-exercise actions, restrained diagram containment, and `docs/exercise-diagrams.md`.
- 2026-09-13: Created `dev/t0-exercise-bank-v4` from `dev/exercise-practice-ux-polish`; replaced the active T0 exercise catalogue with the 80-exercise v4 bank, added required SVG diagrams and T0 validators, normalized fraction/unit grading, and kept retired exercise attempts visible without linking to missing catalogue entries.
- 2026-09-13: Created `dev/exercise-grading-timer-polish` from `dev/t0-exercise-bank-v4`; fixed the `N*m^2/kg^2` and `m^3/(kg*s^2)` false-negative unit grading with a restricted semantic parser, added pending/provisional correction display, cleaned student-facing exercise metadata, added catalogue status backgrounds, persisted active-time timer fields and sync endpoint, added dry-run regrading support, and validated the screenshot regression as 3/3.
- 2026-09-13: Created `dev/rebalance-lesson-lengths-t0-t6` from `dev/t0-exercise-bank-v4`; rebalanced the T0-T6 LaTeX lessons around a shared compact style, shortened T0-T2, expanded T4-T6 with earned examples/visuals, compiled PDFs, and validated final page counts T0 7, T1 7, T2 8, T3 5, T4 6, T5 5, T6 7. LaTeX logs were clean for errors, overfull boxes, and unresolved references; only minor underfull warnings remain in T0 and T6.
- 2026-09-13: Updated the Apuntes page on `dev/rebalance-lesson-lengths-t0-t6` so the visible library shows only the seven proprietary 1º Bachillerato lesson PDFs, replaced the old pilot/original-PDF language with `Apunte propio`, added FisQuiWeb as an inspiration reference, corrected visible mojibake in the touched templates, and updated the footer copy/email.
- 2026-09-14: Applied the paginated PDF.js lesson viewer into the original working folder on dev/exercise-grading-timer-polish, preserving local lesson/PDF changes and exercise-work files while replacing the native embedded PDF viewer with the single-page application viewer.

- 2026-09-14: Preserved the canonical working tree in `5d6ad08` and the alternate PDF.js worktree in `0418425`, pushed both before cleanup, and renamed the existing GitHub repository to `Rocedg/WebClases-Rocedg`. Consolidated editable content under lessons/exercises/exams, documentation under docs, utilities under scripts and application JavaScript under static/js. Flask entry point, SQL schema, lesson/exercise content and public resource URLs are preserved. See `docs/repository-cleanup.md` for final validation and local-directory results.

- 2026-09-14: Cleanup validation completed: 56 pytest tests, 143 arithmetic checks, seven LaTeX builds and PDF delivery checks, Chromium desktop/mobile flows, 73 static resources and 17 templates passed. GitHub/origin use the corrected `WebClases-Rocedg` name. The PDF.js worktree was removed and obsolete registrations pruned; the paginated residual directory remains because automatic approval review blocked deletion. Windows blocked renaming the canonical local folder because another process is using it. Full details and remaining commands: `docs/repository-cleanup.md`. No PR or merge.
- 2026-09-16: Updated exercise-bank discovery to load `exercises_t0.json`, `exercises_t1.json`, and `exercises_t2.json` independently. Updated index/validation scripts, T0 checks, tests, and current documentation; preserved the separate legacy 2bach `exercises.json` fixture and the historical consolidated-index references.
- 2026-09-29: Revised the T0 bank on `feat/t0-errors-vectors-v5`: rewrote all 20 measurement exercises (`t0_m_*`) and 24 vector exercises (`t0_v_*`, except `t0_v_018`) with complete Spanish statements and field labels, replaced English `short_text` answers with Spanish `single_choice` options, restored lost fields and apartados, reactivated `t0_m_007` with auto-gradable fields, and added `t0_m_021`–`t0_m_025` (expected value vs mean, farthest datum as error, precision vs accuracy) and `t0_v_037`–`t0_v_049` (dot/cross products, decomposition, step-by-step change of axes). Exercises whose fields or grading changed are now `version: 5`; older attempts stay as history. `human_field_label()` now keeps labels with TeX subscripts instead of replacing them with "Respuesta". Validators, index, and tests updated.
- 2026-10-12: Split the 1bach exercise banks on `refactor/exercise-banks-per-block`: each `t0`–`t6` folder now has a `_topic.json` manifest and ordered per-block JSON files, with oversized T0/T1/T2 blocks split by contiguous subtopic ranges. Added a shared loader and adapted the index builder, validators, migration script, and generators; the legacy 2bach `exercises.json` layout remains unchanged. New exercises should be added to the block file named by the topic manifest.
- 2026-10-12: Started `feat/t0-statements-audit` from current `main`. Rewrote the 16 active T0 units exercises for first-year students: each statement now gives the situation, the rule being practised and explicit parts; labels and options are Spanish; field `part` values match the statement. Added the necessary `t0_u_005`, `t0_u_007`, `t0_u_015` and `t0_u_016` version-5 format changes so dimensional answers are gradable, and recorded the complete active-bank audit in ignored `tmp/t0-audit.md`. Other blocks remain pending teacher review.
- 2026-10-20: Updated the T0 lesson to v0.7 on `feat/t0-lesson-tools-definitions`. Added two additive boxes to `webclases-lesson.sty` (`toolbox`, violet "Herramienta: …"; `defbox`, slate "Definición: …") plus `\W` and `\Pa`. T0 now has eight definitions (magnitud física, SI, escalar, vector, módulo, precisión, exactitud, error) and six tools (análisis dimensional, descomposición, vector unitario, suma, producto escalar, producto vectorial); a derived-units table, unit deduction and dimensionless arguments; the polar form, the full unit-vector calculation and the 3D cross product by Sarrus and first-row expansion. Notation pass: arrows on every vector, `|\vec A|` for every modulus, `{,}` decimals and `;` separators. Block 5 only received notation fixes. The PDF grows from 7 to 10 pages (the maximum), so prompt 10 has no room left. Validation: all seven lessons build without Overfull/Underfull/undefined warnings; 169 numerical checks; 129 pytest tests; `git diff --check`. `validate_lesson_delivery.py` still stops at its "3 or 4 index links" assertion because T0 has had 5 index entries since `59b6475` (also failing on `main`); with that limit relaxed in a temporary copy, everything else passed.
- 2026-10-20: Updated the T0 lesson to v0.8 on `feat/t0-lesson-derivative-limit` (from `feat/t0-lesson-tools-definitions`, not yet in `main`). Block 5 now builds the derivative from average velocity: a shrinking-interval table and secant figure for `x=t^2/4` at `t=2 s`, the general step `1+h/4` and its limit, a `defbox` for the derivative, a table-football rod example (`x=2t^3-9t^2+12t`, horizontal tangents at the maximum and minimum), a short maxima/minima section with a warning (`x^3`) and an exercise (`x^3-3x^2`), plus "Derivada" and "Integral" tool boxes. The derivative half of "Reglas mínimas de cálculo" now comes right after the definition, because the rod example uses the power rule; the integrals part is unchanged. Following the prompt 9 review: removed the "el recorrido y la flecha final" and "medidas repetidas" examples, moved the relative uncertainty (≈ 0,24 %) into the ruler example, removed the Sarrus sign row, and moved torque and angular momentum to 2.º in the cross-product tool. T0 goes from 10 to 11 pages. `validate_lesson_delivery.py` now allows up to 12 pages and 3–6 index links. Validation: all seven lessons build cleanly; 182 numerical checks; delivery validator; 129 pytest tests; `git diff --check`.
- 2026-10-20: T0 lesson v0.9 on `feat/t0-lesson-derivative-limit`. Removed two "Prueba tú" boxes from block 1, "deducir la unidad" and "una conversión que cambia de escala", because the web exercises cover that practice; the text around them is unchanged. Block 5 now shows the average velocity as a displayed formula, \(v_{med}=\Delta x/\Delta t=[x(t_2)-x(t_1)]/(t_2-t_1)\), applied to the first row before the table and the graph. The futbolín example opens with a TikZ top view of the table: green field with centre line and goals, one rod with handle and three players, a ball, and a double arrow `x` with `x=0` along the rod. T0 goes from 11 back to 10 pages. Validation: all seven lessons build cleanly; 181 numerical checks; delivery validator; 129 pytest tests; `git diff --check`.
- 2026-10-20: **T0 lesson marked as finished** (v0.9, 10 pages) after Edgar's review. Includes prompts 9–11 (tools and definitions, the derivative built from average velocity, the futbolín example) and the fix to the ruler figure's mean label. Merged into `main` by fast-forward; the feature branches `feat/t0-lesson-tools-definitions` and `feat/t0-lesson-derivative-limit` were deleted locally and on GitHub.
- 2026-10-20: Added 8 T0 exercises on `feat/t0-determinants-normal-calculus` (prompt 8). In `vectors_products.json`, after `t0_v_043`: `t0_v_058`–`t0_v_063` (2×2 and 3×3 determinants by Sarrus and the first row, cross product as a determinant, normal vectors in 2D and 3D, torque of a spanner). New `calculus_basics.json`, listed before `calculus_graphs.json`: `t0_c_025` (power-rule derivatives) and `t0_c_026` (first antiderivatives and a definite integral). All values recomputed; none differed from the spec. Difficulty 1 is now allowed only for v5 exercises; v4 records still cannot use it. Recomputations added to `validate_t0_v4_math.py`, including the function answers; counts updated in `validate_t0_v4_bank.py` (114 records / 112 published) and in the tests. Index regenerated. Validation: pytest, the exercise and T0 validators, both decimal separators graded correct, and Chromium at 1440 px and 390 px (16 views, no MathJax errors and no overflow, `vmatrix` included).
- 2026-10-20: Added 13 T0 exercises on `feat/t0-graphs-units-video` (prompt 12), based on `feat/t0-determinants-normal-calculus`. First commit: `t0_c_027`–`t0_c_034` in `calculus_basics.json` (slope signs in piecewise and curved x–t graphs, choosing a graph, average and instantaneous velocity, shrinking intervals towards v(3), a table-football rod's maximum and minimum, f' = 0 without an extremum). Second commit: `t0_u_019`–`t0_u_021` (derived units, deducing a unit, dimensionless arguments), `t0_v_064` (polar form) and `t0_m_026` (velocity from video frames with uncertainty propagation). Five new SVGs: `c027_slopes`, `c028_four_graphs`, `c029_curve_tangents`, `v064_polar`, `m026_frames`. All values recomputed; none differed from the spec. Counts: 127 records / 125 published (units 19, vectors 52, measurement 26, calculus 28 published). Validation: pytest, the exercise and T0 validators, both decimal separators graded correct, and Chromium at 1440 px and 390 px (26 views, no MathJax errors, overflow or broken SVGs).
