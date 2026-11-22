# T0 Exercise Bank v4

This branch replaces the active Tema 0 exercise catalogue with the enriched v4 bank from `content/exercises/1bach/t0/exercise-bank-t0-v4-spec.md`.

## Active Catalogue

- Version: `4`.
- Active exercise count: `80`.
- Distribution:
  - Units and dimensional analysis: `t0_u_001` through `t0_u_016` (`16` exercises).
  - Vectors and axes: `t0_v_001` through `t0_v_024` (`24` exercises).
  - Measurement, error, uncertainty, and significant figures: `t0_m_001` through `t0_m_020` (`20` exercises).
  - Calculus and graphs: `t0_c_001` through `t0_c_020` (`20` exercises).
- Difficulty `1` is intentionally absent from the active v4 bank.

## Retired IDs

The following IDs are kept out of the active catalogue and are listed in top-level retired metadata so historical attempts can still display a title:

`t0_u_017`, `t0_u_018`, `t0_v_025` through `t0_v_036`, `t0_e_001`, `t0_e_002`, and `t0_c_021` through `t0_c_024`.

History rows for retired exercises no longer link to a missing attempt detail page; they show a retired-catalogue badge instead.

## Response Handling

The generated JSON keeps the current content-first model and uses `response_fields`/`interactions` for the guided form. Deterministic grading remains intentionally narrow:

- `numeric` accepts decimal input and exact fraction forms such as `36/7` when listed as accepted forms.
- `single_choice` uses stable option IDs.
- `unit_expression` normalizes common unit spellings before comparing expected and accepted forms.
- `open_text` and `written_upload` remain `pending_review`.

## Required SVG Assets

The v4 bank includes the requested accessible SVG diagrams for:

- `t0_v_012`: `static/exercises/1bach/t0/assets/v012_punta_cola.svg`
- `t0_v_017`: `static/exercises/1bach/t0/assets/v017_ejes_girados.svg`
- `t0_v_018`: `static/exercises/1bach/t0/assets/v018_plano_inclinado.svg`
- `t0_v_024`: `static/exercises/1bach/t0/assets/v024_entra_sale.svg`
- `t0_c_016`: `static/exercises/1bach/t0/assets/c016_piecewise.svg`
- `t0_c_019`: `static/exercises/1bach/t0/assets/c019_growth.svg`
- `t0_c_020`: `static/exercises/1bach/t0/assets/c020_signed_area.svg`

Each SVG includes `viewBox`, `title`, and `desc`.

## Validation

Use these checks after editing the bank:

```bash
python scripts/validate_exercises.py
python scripts/validate_t0_v4_bank.py
python scripts/validate_t0_v4_math.py
python -m pytest
```

The T0-specific math validator independently checks selected numeric answers, including the corrected `t0_c_020` values: zero time `36/7`, positive area `100/7`, negative signed area `-9/7`, displacement `13`, and distance `109/7`.
