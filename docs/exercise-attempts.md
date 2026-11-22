# Persistent Exercise Attempts MVP

## Scope

This MVP stores student work for JSON-backed exercises without moving the exercise bank into SQL.

The exercise catalogue remains file based:

- `content/exercises/**/exercises_<topic>.json` keeps the full exercise definition for the renamed 1bach banks.
- `content/exercises/index.json` keeps the public practice index.
- SQL stores only user attempts and responses.

## Persistence Contract

Each `ExerciseAttempt` stores:

- `username`
- `exercise_id`
- `exercise_version`
- `status`
- lifecycle timestamps
- optional auto score fields
- nullable review fields for a future teacher workflow

Each `ExerciseResponse` stores:

- `attempt_id`
- `field_id`
- `response_type`
- `raw_value`
- `normalized_value`
- `grading_status`
- optional auto score and feedback

The browser never submits correct answers, tolerances, score, user identity, or exercise version as trusted data. Those values are resolved server-side from the authenticated session, stored attempt, and JSON catalogue.

## Lifecycle

Opening `/exercise/<exercise_id>` does not create database rows.

The student explicitly starts with `POST /exercise/<exercise_id>/start`.

If the same student already has a `started` attempt for the same exercise and version, the app resumes that draft. If previous attempts are submitted, starting again creates a new attempt.

Drafts use `POST /exercise/<exercise_id>/attempt/<attempt_id>/draft`.

Submissions use `POST /exercise/<exercise_id>/attempt/<attempt_id>/submit`. Submitted attempts are read-only; a new attempt is required to try again.

## Grading

Automatic grading is deterministic and server-side (`_grade_response()` in
`services/exercise_attempt_service.py`):

- `numeric`: value within the absolute `tolerance` of `expected_value`, or one of `accepted_forms`.
- `vector`: each component of `(x; y)` within `tolerance` of `expected_components`.
- `single_choice`: matches `correct_option_id`.
- `function`: numerically equivalent to `canonical_expression` or an accepted form.
- `unit_expression`: dimensionally equal to the expected unit.
- `short_text`: matches an accepted form after normalization.

Decision (2026-11-22): the grader checks the value only. Units are shown as a
fixed label and significant figures are not graded.

Fields without the data needed for these checks, or answers that cannot be
parsed, become `pending_review`. Field details: `docs/exercise-bank-format.md`.

Numeric normalization preserves the original typed value in `raw_value` and stores a conservative normalized value such as `8.66` for input `8,66`.

## Student History

`/practice/history` lists the authenticated student's attempts, most recently active first. Started attempts link to continue; submitted or reviewed attempts link to inspect the saved attempt.

## Ownership

Every attempt read/write checks that `attempt.username` matches the authenticated session username. Teacher review and role-based access are deliberately deferred.

## Deferred

This MVP does not include:

- teacher dashboard
- manual review UI
- analytics or mastery
- recommendations
- AI grading
- symbolic algebra grading
- unit parsing
- uploads or OCR
- graph/vector widgets
- database migrations
