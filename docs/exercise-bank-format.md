# Formato de los bancos de ejercicios (JSON)

Este documento describe el formato que usa hoy la web. Si algo de aquí no
coincide con el código, manda el código: `services/exercise_bank_loader.py`
(carga), `scripts/validate_exercises.py` (validación) y
`services/exercise_attempt_service.py` (corrección).

Los JSON son la **única fuente de verdad** de los ejercicios de todos los temas
(T0-T6). Se editan a mano. Los generadores antiguos están en `scripts/archive/`
y no se ejecutan con `--write`. Las tablas `referencia-ejercicios-tN.md` son
solo un resumen histórico.

> La sección 3 de `docs/context/feature-specs/02-interactive-exercise-system.md`
> describe un modelo anterior (`exercise_type`, `estimated_time_min`,
> `statement_tex`, `interactions`...) que solo conserva el piloto de 2.º.
> Para 1.º Bachillerato vale este documento.

## Dónde están

```text
content/exercises/
├── 1bach/
│   ├── t0/ … t6/
│   │   ├── _topic.json          # manifiesto del tema
│   │   ├── <bloque>.json        # ejercicios de un bloque, en orden
│   │   └── referencia-ejercicios-tN.md   # resumen histórico, no se edita
├── 2bach/electromagnetismo/induccion/exercises.json   # piloto antiguo, fuera del catálogo
├── index.json                   # generado; no se edita a mano
└── quizzes.json
static/exercises/1bach/tN/assets/   # SVG de los enunciados (públicos)
```

Los nombres de bloque cambian según el tema. En T0 son descriptivos
(`units.json`, `vectors_basics.json`...). En T1-T6 son la letra de la familia
(`f.json`, `n.json`...), y en T1 hay bloques partidos (`g_areas.json`,
`g_slopes.json`).

## Manifiesto `_topic.json`

```json
{
  "version": 1,
  "course": "1bach",
  "topic": "t3",
  "topic_slug": "leyes-de-newton",
  "block": "Leyes de Newton",
  "description": "Fuerzas, diagramas de cuerpo libre…",
  "exercise_files": ["f.json", "n.json", "p.json", "c.json", "i.json"]
}
```

- `exercise_files` es obligatorio y fija el **orden** en que se cargan los
  bloques. Un archivo que no esté en la lista no se carga.
- T0 añade `retired_ids` y `retired_exercises` (fichas mínimas `id`, `title`,
  `version`, `status: "retired"`). Sirven para que el historial siga mostrando
  el título de ejercicios que ya no existen en los bloques.

Cada archivo de bloque es `{"exercises": [ … ]}`.

## Campos de un ejercicio

Ejemplo recortado (`t1_u_001`):

```json
{
  "id": "t1_u_001",
  "number": 9,
  "version": 1,
  "title": "Paso por una baliza",
  "course": "1bach",
  "topic": "t1",
  "concept": "Movimiento rectilíneo",
  "block": "MRU y movimiento relativo",
  "family": "u",
  "subtype": "multi_step",
  "difficulty": 1,
  "estimated_minutes": 9,
  "response_mode": "structured",
  "response_prompt": "Responde los apartados en sus campos.",
  "response_fields": [ … ],
  "assets": [{"path": "static/exercises/1bach/t1/assets/t1_u_001.svg", "alt": "…"}],
  "tags": ["t1", "u", "cinematica"],
  "origin": {"kind": "original_teacher_bank", "reference": null, "source": "content/exercises/1bach/t1/referencia-ejercicios-t1.md", "adaptation_note": "…"},
  "status": "draft",
  "learning_objective": "…",
  "prerequisites": ["…"],
  "difficulty_reason": "…",
  "common_mistakes": ["…"],
  "parts_count": 2,
  "statement_source": "Una patinadora… (a) … (b) …",
  "solution_source": "…",
  "solution_reference": null
}
```

| Campo | Obligatorio | Qué es |
| --- | --- | --- |
| `id` | sí | `tN_<familia>_<NNN>`, único en todo el catálogo. No se reutiliza nunca. |
| `version` | sí | Entero ≥ 1. Los intentos se guardan con `id` + `version`. |
| `number` | no | Número visible en el catálogo. Si falta, se usa el sufijo del `id`. T1 lo usa para numerar de 1 a 60 en orden de bloque. |
| `title`, `course`, `topic`, `block`, `concept` | sí | `course` debe ser `1bach` para salir en la web. |
| `family`, `subtype` | sí | Agrupación y tipo de ejercicio para filtros (`services/exercise_taxonomy.py`). |
| `difficulty` | sí | Entero de 1 a 5. Dentro de cada bloque de T1 va de menor a mayor (lo comprueba un test). |
| `estimated_minutes` | recomendado | Entero. |
| `response_mode` | sí | Siempre `structured` en 1.º. |
| `response_prompt` | recomendado | Texto general encima de los campos. |
| `response_fields` | sí | Lista de campos de respuesta (ver abajo). |
| `statement_source` | sí | Enunciado en texto plano con LaTeX `\( … \)` y `\[ … \]`. Los apartados empiezan línea con `(a)`, `(b)`... Una línea en blanco separa párrafos. Sin HTML (`<`) ni `$`. |
| `solution_source` | sí | Solución, mismo formato. Se muestra al alumno después de entregar. |
| `assets` | sí | Lista de `{path, alt}`. Puede estar vacía. En T3-T6 cada ejercicio tiene un SVG con `viewBox="0 0 640 360"`. |
| `tags` | sí | Lista de cadenas. |
| `origin` | sí | Procedencia: `kind`, `reference` y `source` (ver abajo). |
| `status` | sí | `draft`, `active` o `retired` (ver abajo). |
| `learning_objective`, `prerequisites`, `difficulty_reason`, `common_mistakes`, `parts_count` | recomendados | Metadatos didácticos. Hoy la web no los muestra. |
| `solution_reference` | no | Documento del que sale la solución, si lo hay. |

## Campos de respuesta (`response_fields`)

Comunes a todos: `id` (único dentro del ejercicio), `label`, `type`,
`required`, `part` (letra del apartado; el conjunto de `part` debe coincidir
con los apartados del enunciado) y, opcionalmente, `prompt`, `input_help`,
`feedback_correct` y `feedback_incorrect`.

| `type` | Campos propios | Cómo se corrige |
| --- | --- | --- |
| `numeric` | `expected_value`, `tolerance` (absoluta), `unit`, opcional `accepted_forms`, `significant_figures`, `rounding` | Correcto si \|respuesta − esperado\| ≤ `tolerance`, o si coincide con una de `accepted_forms` (fracciones exactas, por ejemplo). Acepta coma o punto y notación científica. |
| `vector` | `expected_components`, `tolerance`, `component_order`, `unit` | El alumno escribe `(x; y)`. Cada componente se compara con la tolerancia. |
| `single_choice` | `options` (`[{id, label}]`), `correct_option_id` | Coincidencia exacta de la opción. |
| `function` | `canonical_expression`, `accepted_forms`, `variable`, `domain`, `unit`, `variable_unit` | Equivalencia numérica de la expresión. Se escribe con `*` y `^`; la expresión canónica no lleva `**`, `;` ni `<`. |
| `unit_expression` | `expected_value` (la unidad), `accepted_forms`, opcional `unit_system: "base_si"` | Compara dimensiones de la unidad escrita. Solo para ejercicios que preguntan la unidad. |
| `short_text` | `accepted_forms` | Coincidencia tras normalizar. T1 no lo usa. |

Si falta lo necesario para corregir, o la respuesta no se puede interpretar, la
respuesta queda en `pending_review`.

**Decisión (22/11/2026): el corrector solo comprueba el valor.** `unit` se
muestra como etiqueta fija junto al campo y el alumno no la escribe.
`significant_figures` y `rounding` son información para quien escribe el
ejercicio: el corrector no los mira. La tolerancia tiene que ser lo bastante
amplia para aceptar la respuesta redondeada a las cifras que pide el
enunciado.

## `origin` (procedencia)

Obligatorio en todos los ejercicios de 1.º. `validate_exercises.py` lo
comprueba así:

| Clave | Obligatoria | Valores |
| --- | --- | --- |
| `kind` | sí | `original_teacher_bank` (propio), `adapted_from_pau` (adaptado de un examen PAU) u `official_pau` (enunciado oficial PAU). |
| `reference` | sí, la clave siempre presente | `null` en los propios. En `adapted_from_pau` y `official_pau` es obligatoria: la fuente externa (convocatoria, año, número de ejercicio). |
| `source` | sí | El documento interno del que sale el ejercicio: la especificación, el prompt o la revisión. Por ejemplo `content/exercises/1bach/t1/referencia-ejercicios-t1.md`. |
| `batch` | no | Lote de trabajo que lo produjo. Lo usa T0 (`exercise_bank_t0_v4_spec`, `t0_unit_vector_extension`...). |
| `adaptation_note` | no | Qué se ha cambiado respecto a la fuente, o "propio". Lo usan T1-T6. |

Hoy todos los ejercicios de 1.º son `original_teacher_bank`. El piloto de 2.º
conserva su formato antiguo (`pilot_adapted`) y no pasa por esta regla.

## `status`

| Valor | Qué significa hoy |
| --- | --- |
| `draft` | **Marcador interno** (decisión del 22/11/2026): indica que el ejercicio no ha pasado la revisión final. No oculta nada: los alumnos lo ven igual que uno `active`. T1-T6 están en `draft`. |
| `active` | Revisado. T0 está en `active`. |
| `retired` | Se oculta del catálogo y de la página del ejercicio y no entra en `index.json`. El historial conserva el título. El ejercicio no se borra del JSON. |

## `version` y cambios en ejercicios publicados

- Corregir una errata del texto que no cambia la respuesta: no hace falta
  subir `version`.
- Cambiar datos, respuesta esperada, tolerancia o campos: sube `version`. Los
  intentos antiguos quedan asociados a la versión anterior.
- Para recalcular la nota de intentos ya entregados después de corregir una
  clave: `flask --app app regrade-exercise-attempts` (simulación) y luego con
  `--apply`. En producción solo se hace con la base de Neon y a propósito.

## Convenciones de contenido

- **g = 9,81 m/s²** en todos los temas (decisión del 22/11/2026). Si un
  enunciado da otro valor, debe decirlo explícitamente.
- Decimales con coma en el texto visible. En `expected_value` se usa número
  JSON (punto).
- Las respuestas se calculan con precisión intermedia completa y se redondean
  al final.
