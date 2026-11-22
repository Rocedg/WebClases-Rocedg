# Repository cleanup — WebClases-Rocedg

Date: 2026-09-14. Branch: `chore/repository-cleanup`.

GitHub is renamed and the structural cleanup is validated. Two local operations
remain incomplete: renaming the canonical folder (Windows reports it is in use)
and deleting the paginated worktree's residual folder (automatic approval review
blocked deletion). No PR was opened, no branches were merged, and no force push
or history rewrite was performed.

## Initial state

- Original path: `C:\Users\Asus\OneDrive\💼Work💼\Tutoria🏫\web-clases-fisica`.
- Branch: `dev/exercise-grading-timer-polish`.
- HEAD: `fdcef8751ac671e3b13a97b46f6a01ea1d5ec214`.
- Origin: `https://github.com/Rocedg/web-clases-fisica`.
- The original branch matched its remote before the checkpoint.
- 23 tracked paths were modified/deleted. The deleted reference image was
  actually renamed with identical bytes.
- Legitimate untracked work: 14 SVGs, the PDF viewer JavaScript, three PDF.js
  files, the renamed reference image and four review utilities under `tmp/`.
- Other `tmp/` files were generated PDF/text/image review output and downloaded
  review libraries. They were retained locally and excluded from Git.
- Existing ignored state included `.venv/`, `instance/`, Python caches and logs.

Initial status:

```text
M app.py
 M content/latex/T0-introduccion.tex
 M content/latex/T1-movimiento-rectilineo.tex
 M content/latex/T2-movimiento-en-el-plano.tex
 M content/latex/T3-leyes-de-newton.tex
 M content/latex/T4-rozamiento-y-aplicaciones.tex
 M content/latex/T5-energia-y-trabajo.tex
 M content/latex/T6-momento-lineal.tex
 M content/latex/webclases-lesson.sty
 M content/lessons.json
 M context/06-progress-tracker.md
 D "context/ui-redesign-reference/Image 22.jpeg"
 M static/css/pages.css
 M static/css/responsive.css
 M static/lessons/T0-introduccion.pdf
 M static/lessons/T1-movimiento-rectilineo.pdf
 M static/lessons/T2-movimiento-en-el-plano.pdf
 M static/lessons/T3-leyes-de-newton.pdf
 M static/lessons/T4-rozamiento-y-aplicaciones.pdf
 M static/lessons/T5-energia-y-trabajo.pdf
 M static/lessons/T6-momento-lineal.pdf
 M templates/user/lesson_viewer.html
 M tests/test_activity_backend.py
?? context/ui-redesign-reference/pdf_viewer.jpeg
?? static/exercises/1bach/t0/assets/c011_odd.svg
?? static/exercises/1bach/t0/assets/c020_slopes.svg
?? static/exercises/1bach/t0/assets/c021_tangents.svg
?? static/exercises/1bach/t0/assets/c022_area.svg
?? static/exercises/1bach/t0/assets/c024_derivative_sign.svg
?? static/exercises/1bach/t0/assets/v004_parallel.svg
?? static/exercises/1bach/t0/assets/v014_punta_cola.svg
?? static/exercises/1bach/t0/assets/v021_ejes_girados.svg
?? static/exercises/1bach/t0/assets/v022_plano_inclinado.svg
?? static/exercises/1bach/t0/assets/v025_cartel.svg
?? static/exercises/1bach/t0/assets/v026_barca.svg
?? static/exercises/1bach/t0/assets/v033_cross.svg
?? static/exercises/1bach/t0/assets/v035_entra_sale.svg
?? static/exercises/1bach/t0/assets/v036_qvb.svg
?? static/js/
?? static/vendor/
?? tmp/
```

Inspection included `pwd`, `git status --short`, `git branch --show-current`,
`git branch -a`, `git log --oneline --decorate -15`, `git remote -v`, repository
and parent listings, a useful directory tree, tracked/untracked/ignored files,
and `git worktree list --porcelain`. The complete local inspection record is
`.git/repository-cleanup-initial.json`.

## Preservation

Main checkpoint: **`5d6ad0811f7e0932afbe72db0fe7d0016035778d`**, with message
`Checkpoint current project before repository cleanup`.

It includes the current T0–T6 LaTeX/PDF edits, lesson metadata, PDF viewer and
its CSS/tests, PDF.js runtime, new exercise diagrams, renamed visual reference,
progress log and four useful review scripts. Ignore rules exclude temporary
review output and LaTeX auxiliary files. There were 46 affected files.

The checkpoint was pushed to `origin/dev/exercise-grading-timer-polish`
**before structural moves or deletion**. `git ls-remote` returned the exact
local SHA, and the working tree was clean.

The alternate PDF.js worktree was checkpointed separately at
`04184253086c06525a2a8ec6e118c012f90c3332` on `dev/lesson-pdfjs-viewer` and pushed.
The clean paginated worktree's branch remains at
`4a42046abda5e55a950aa64ace2325b4ca0a0d23` on `dev/paginated-pdf-viewer-ui`, also
verified remotely. Both histories are accessible through the canonical repo's
shared Git store and named branches, without merging their alternate designs.

A verified local `.git/repository-cleanup-worktrees.bundle` contains complete
history for both viewer branches. No database, virtual environment, cache, `.env`
or LaTeX build artifact was committed. Pattern scanning found no service tokens
or private keys. Existing documented demonstration accounts were unchanged.

## Rename

| Item | Result |
| --- | --- |
| GitHub repository | **Succeeded:** `Rocedg/WebClases-Rocedg` |
| Repository URL | `https://github.com/Rocedg/WebClases-Rocedg` |
| Origin URL | `https://github.com/Rocedg/WebClases-Rocedg.git` |
| Account / permission | `Rocedg`, admin permission verified using GitHub API |
| Repository identity | ID `967050807` preserved; no second repository created |
| Fetch / push with corrected URL | Succeeded |
| Local directory | **Pending:** still `web-clases-fisica` |

The attached request originally specified `WebClases-Roceh`, and that name was
initially applied. The user's subsequent correction was applied to the same
GitHub repository, origin, README and launcher messages: **WebClases-Rocedg**.
The misspelling remains only in this historical explanation.

The canonical folder rename was attempted from its parent after the audit
processes finished. Windows returned: “El proceso no puede obtener acceso al
archivo porque está siendo utilizado en otro proceso.” User processes were not
terminated, and no copy or symlink was created to simulate a successful rename.
Runtime paths and launchers do not depend on the old absolute directory name.

## Structure

Before:

```text
web-clases-fisica/
├── app.py, database.py, models.py, services/
├── content/
│   ├── exercises/
│   ├── intake/
│   ├── latex/                  # Lessons and exercise templates mixed
│   └── lessons.json
├── data/                       # Five JSON files from different domains
├── context/                    # Agent context and visual references
├── docs/
├── scripts/
├── run-local.ps1, setup-local.ps1, start-web.bat
├── tmp/                        # Included four useful review scripts
├── templates/                  # Two pages contained substantial JavaScript
├── static/{css,js,lessons,exercises,pdfs,images,vendor}/
└── tests/
```

After (tracked structure; physical root rename remains pending):

```text
WebClases-Rocedg/
├── app.py, database.py, models.py, services/
├── content/
│   ├── lessons/
│   │   ├── latex/, intake/
│   │   └── lessons.json, topics.json, summaries.json
│   ├── exercises/
│   │   ├── 1bach/, 2bach/, latex/
│   │   └── index.json, quizzes.json
│   └── exams/exams.json
├── docs/
│   ├── context/                # Rules, architecture, progress and specs
│   ├── design/ui-redesign-reference/
│   └── Feature guides and cleanup report
├── scripts/                    # Launch, setup, builds and validation
├── templates/                  # HTML/Jinja
├── static/{css,js,lessons,exercises,pdfs,images,vendor}/
└── tests/
```

The backend remains small, with `app.py`, the existing SQLAlchemy modules and
`services/`. `gunicorn app:app`, Flask, Jinja, schema and dependencies are unchanged.
Templates, styles and shared assets retain their conventional roots.

Each editable content domain has one obvious home. Public PDFs remain under
`static/lessons/` and `static/pdfs/`, and exercise assets under
`static/exercises/`, preserving URLs that may occur in bookmarks or stored
activity. Intake copies are working source material; legacy static PDFs are the
public reference library. This useful source/public separation is documented in
`docs/context/02-architecture.md`. No compatibility directories or symlinks were
introduced. Educational content, answers and UI appearance were not changed.

## Migrations

| Old path/group | New path |
| --- | --- |
| `content/latex/T*.tex`, `webclases-lesson.sty` | `content/lessons/latex/` |
| `content/latex/exercise-common.sty`, `statement-template.tex`, `solution-template.tex` | `content/exercises/latex/` |
| `content/intake/` | `content/lessons/intake/` |
| `content/lessons.json` | `content/lessons/lessons.json` |
| `data/topics.json`, `data/summaries.json` | `content/lessons/topics.json`, `summaries.json` |
| `data/exercises.json` | `content/exercises/index.json` |
| `data/quizzes.json` | `content/exercises/quizzes.json` |
| `data/exams.json` | `content/exams/exams.json` |
| `context/` | `docs/context/` |
| `context/ui-redesign-reference/` | `docs/design/ui-redesign-reference/` |
| Root `run-local.ps1`, `setup-local.ps1`, `start-web.bat` | `scripts/` |
| `tmp/build_lessons.ps1`, `check_lesson_numbers.py`, `review_lessons.py`, `validate_lesson_delivery.py` | `scripts/` |
| Inline JavaScript in `exercise_detail.html` | `static/js/exercise-math.js`, `exercise-timer.js` |
| Inline JavaScript in `quiz.html` | `static/js/quiz.js` |

Updated references include Flask content loaders, index generation/validation,
JSON and MathJax tests, Jinja script URLs, launch/build/review tools and docs.
The index is named `index.json` so recursive topic discovery does not load it
twice. The relocated JSON data remains identical.

The recovered lesson delivery validator had two outdated assumptions: literal
HTML page counts and only `LINK_GOTO` internal PDF links. It now checks the
existing PDF.js viewer and also accepts resolved named destinations returned by
PyMuPDF, still checking destination pages against LaTeX `.aux` labels. No PDF
content was changed to satisfy validation.

## Auxiliary directories

| Directory | Findings / preservation | Outcome |
| --- | --- | --- |
| `web-clases-fisica-pdfjs` | Worktree at `5959eef`, with five modified tracked paths and untracked JS/vendor files. Alternate viewer preserved completely at `0418425`, pushed and bundled. Its SQLite file was empty. | Removed with `git worktree remove` after clearing its read-only attributes. |
| `web-clases-fisica-paginated` | Clean worktree at `4a42046`. Two commits were not ancestors of the current working branch, but exist in the shared Git store and pushed named branch. Six apparently missing T0–T2 intake files exactly match the canonical processing copies; the old image exactly matches `pdf_viewer.jpeg`. | Removal partially failed on read-only files. Orphaned registration was pruned using Git; an unregistered residual folder remains. |
| Stale `web-clases-fisica-activity-spike` registration | Only `ORIG_HEAD` and empty metadata directories remained. Commit `83bd61a` is already in canonical history and multiple branches. No sibling checkout existed. | Pruned with `git worktree prune`. |

After partial removal, **every remaining paginated file** was checked: 129 files
match blobs at `4a42046`, 11 are Python caches, and one is an empty SQLite file.
No unique content remains there. Automatic approval review rejected the residual
directory deletion with the generic reason `blocked by policy`; deletion was not
performed by another mechanism.

Other parent folders—Academia Velazquez, Fisica Bach, Fisica SL, Maths AA HL,
Proyecto_CajaMusica and Simulacro_Paul—were unrelated and untouched.
`git worktree list` now registers only the canonical repository.

## Validation

| Check | Result |
| --- | --- |
| pytest before preservation | 56 passed |
| pytest after reorganization | 56 passed |
| Flask `app:app` import and home response | Passed; HTTP 200 |
| `validate_exercises.py` | 84 exercises, 0 errors; 20 existing warnings for planned missing files in four induction skeleton exercises |
| `validate_t0_v4_bank.py` | Passed |
| `validate_t0_v4_math.py` | Passed |
| Index generation in isolated temporary content tree | 84 unique IDs, correct new output path |
| `scripts/build_lessons.ps1` | Seven lessons compiled, three passes each |
| `check_lesson_numbers.py` | 143 checks, 0 failures |
| `validate_lesson_delivery.py` | Passed: page counts, footers, index targets, source links, margins, inline/download/static routes |
| T0–T6 page counts | 6, 5, 6, 5, 5, 5, 5 |
| Chromium / Playwright desktop and mobile | Passed |
| Browser JavaScript errors, console errors, failed requests, HTTP errors | 0 |
| Static files served by Flask | 73, all HTTP 200 |
| Jinja templates compiled | 17 |
| CSS imports | All resolve |
| Existing material integrity | 87 identical hashes for assets, LaTeX and JSON; all five relocated data JSONs retain identical data |
| PowerShell scripts | Syntax valid; script-relative repository paths |
| `git diff --check`, `git diff --cached --check` | Passed |

Browser routes checked:

```text
/
/login
/topics
/homework
/practice/history
/progress
/exams
/miscellaneous
/lesson/T0-introduccion
/lesson/T1-movimiento-rectilineo
/lesson/T2-movimiento-en-el-plano
/lesson/T3-leyes-de-newton
/lesson/T4-rozamiento-y-aplicaciones
/lesson/T5-energia-y-trabajo
/lesson/T6-momento-lineal
/exercise/t0_u_001
/exercise/t0_v_012
/quiz/1
```

Checks included real Guest login in a disposable database, next-page rendering
for all seven PDFs, mobile rendering, SVG and MathJax loading, timer pause/resume,
draft save, exercise submission/history, and quiz progress reaching 100%.
The mobile viewer and exercise screenshots were visually inspected.

The real local database was untouched. Its row counts remain: 145 events,
1 topic-progress row, 22 resource accesses, 2 quiz attempts, 32 exercise attempts
and 14 responses. Browser evidence is in `tmp/cleanup-browser-report.json`.

Old paths remain only in dated history, the original planning spec (with a
current-path note), tree diagrams and this report. No active loader, template or
script refers to a retired content directory or old absolute local path.

## Git delivery

- Cleanup base: `5d6ad0811f7e0932afbe72db0fe7d0016035778d`.
- Branch: `chore/repository-cleanup`.
- Cleanup message: `Reorganize project structure and rename WebClases`.
- Remote delivery branch: `origin/chore/repository-cleanup`.
- The final commit SHA, exact clean status and complete diffstat are recorded in
  the final response and local `tmp/repository-cleanup-final-report.md` after the
  cleanup commit is created and verified remotely.
- No PR, merge or force push. `main` is unchanged.

## Remaining local actions

After closing windows/processes using the project, run from outside its root:

```powershell
Set-Location -LiteralPath 'C:\Users\Asus\OneDrive\💼Work💼\Tutoria🏫'
Rename-Item -LiteralPath '.\web-clases-fisica' -NewName 'WebClases-Rocedg'
git -C '.\WebClases-Rocedg' status --short
git -C '.\WebClases-Rocedg' remote -v
```

The residual deletion rejected by automatic approval review is:

```powershell
Remove-Item -LiteralPath 'C:\Users\Asus\OneDrive\💼Work💼\Tutoria🏫\web-clases-fisica-paginated' -Recurse -Force
```

Empty local `data/` and `static/img/` folders also remain: they contain no files
and are absent from Git. Automatic approval review rejected their non-recursive
removal as well. They are not compatibility directories and have no runtime role.

A real Render deployment and a run from an already renamed local root were not
tested. Windows blocked that rename. The deployment entry point and dependencies
remain unchanged. Published PDFs and academic material match the user's checkpoint.
