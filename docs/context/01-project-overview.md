# Project Overview

## Product

WebClases-Rocedg is a guided Physics study platform for Bachillerato students. It gives students structured access to topics, summaries, exercises/quizzes, exams, homework, and additional PAU/selectividad-related information.

The app is intentionally lightweight. It uses Flask, Jinja templates, static CSS, static PDFs, and JSON data files. Learning content remains in JSON; the existing SQLAlchemy backend stores student activity, exercise attempts and responses.

## Users

- Students who need guided physics practice.
- The teacher/maintainer, who organizes materials, manages student accounts and follows progress from the read-only teacher panel.

## Core User Flows

1. A student opens the home page and chooses a study section.
2. A student logs in to access protected study materials.
3. A student reviews topic PDFs.
4. A student practices quizzes and receives immediate results.
5. A student opens exam and PAU/selectividad resources.
6. The maintainer adds or updates PDF references through JSON and templates.
7. The teacher creates student accounts and reviews their attempts from `/teacher`.

## Current Product Scope

In scope now:

- Flask app.
- Static PDFs.
- JSON-driven content.
- Clear navigation.
- Login-based protected sections.
- SQLAlchemy activity and exercise-attempt persistence.
- SQLite locally, with DATABASE_URL for PostgreSQL.
- Local testing workflow.
- Render deployment.

## Explicitly Out of Scope

Out of scope for now:

- New database models or schema migrations during repository cleanup.
- React/Next.js migration.
- AI-generated exercises inside the app.
- Payment/subscription features.
- Real-time collaboration.
- Complex admin dashboard.

## Success Criteria

The product is successful in its current phase if:

- Students can quickly find notes, exercises, exams, and PAU information.
- The maintainer can understand the project structure without specialist knowledge.
- The app runs locally on Windows with simple commands or helper scripts.
- The app remains deployable on Render with `gunicorn app:app`.
- JSON learning content can be edited independently of student activity records.
- Future AI-assisted work is guided by explicit context and small specs.

