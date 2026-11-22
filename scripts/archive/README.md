# Archived exercise generators

These scripts built the first drafts of the exercise banks. They are kept for
reference only. Since 2026-11-22 the JSON files under
`content/exercises/1bach/tN/` are the only source of truth for every topic, and
they are edited directly.

| Script | What it did | Why it is archived |
| --- | --- | --- |
| `build_t3_t6_exercise_banks.py` | Built the T3-T6 JSON banks and SVGs from `content/exercises/1bach/tN/referencia-ejercicios-tN.md`. | Running it with `--write` would overwrite any later edit or audit of the T3-T6 JSON. |
| `build_t0_v4_bank.py` | Built the 80 T0 v4 exercises. | It writes without a `--write` flag and would wipe every later T0 extension. |

Do not run either script with `--write`. The `referencia-ejercicios-tN.md`
tables are a historical overview of the variety of exercises, not a source.
