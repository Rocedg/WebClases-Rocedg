# Progress Tracker

## Current Phase

Repository cleanup on `chore/repository-cleanup`, based on safety checkpoint `5d6ad08`. The user explicitly authorized checkpoint/push and repository reorganization on 2026-09-14. Current content paths are documented in `docs/context/02-architecture.md`; dated entries below retain historical paths.

## Completed

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
