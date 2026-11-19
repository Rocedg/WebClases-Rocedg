# 03 · Banco de ejercicios PAU (Física, 2º Bachillerato)

Estado: **borrador de diseño**, pendiente de validar con el piloto.
Ámbito: PAU de Física de Cataluña primero; otras comunidades después.

## 1. Principio

Un ejercicio PAU es **un ejercicio más del banco**, con el mismo formato que los
bancos de 1º (modelo: `content/exercises/1bach/t1/`). Lo que lo distingue es su
`origin`. Así se cumple la idea de la spec 02: el alumno practica por **tipo de
problema**, venga de una PAU o de material propio.

Un examen es otra cosa: un **manifiesto** que lista ejercicios por id, en orden.
De ahí salen los simulacros. Un ejercicio puede vivir en el banco de su tema y
formar parte de un examen a la vez, sin duplicarse.

```
content/exercises/2bach/<tema>/_topic.json      # banco por tema (igual que 1bach)
content/exercises/2bach/<tema>/<familia>.json
content/exams/pau/cat/2024-setembre-s3.json      # manifiesto de examen
static/exercises/2bach/<tema>/assets/             # figuras recortadas del PDF oficial
content/exercises/2bach/<tema>/source_refs/       # PDF/pauta oficial, uso interno
```

El loader actual (`services/exercise_bank_loader.py`) ya descubre cualquier
`_topic.json` bajo `content/exercises`, así que los temas de 2º no necesitan
cambios en el loader.

## 2. Licencia (verificado el 2026-11-19)

- Fuente oficial: repositorio Eureka (Biblioteca Digital de la Generalitat).
  Ejemplo: [Física PAU setembre 2024](https://eureka.bibliotecadigital.gencat.cat/handle/20.500.14344/299).
- Licencia de la ficha: **CC BY-NC-SA 4.0**. No es CC0. El avís legal general de
  gencat menciona CC0/Llicència oberta, pero dice que prevalece la licencia propia
  de cada obra.
- Atribución que pide la ficha: *Generalitat de Catalunya. Departament de Recerca i
  Universitats. Consell Interuniversitari de Catalunya.*
- Eureka cubre 2021–2024 en el listado consultado. **Pendiente:** origen y licencia
  de 2000–2020 y de 2025.

Consecuencias prácticas (no es asesoramiento legal):

| Cláusula | Qué implica aquí |
|---|---|
| BY | Cada ejercicio muestra fuente + licencia + "adaptado" si se ha cambiado. |
| NC | Uso no comercial. Ver §2.1. |
| SA | Enunciados y figuras derivados se publican bajo CC BY-NC-SA 4.0. Las soluciones propias son obra propia. |

Webs de terceros: solo para **localizar** exámenes. Nunca como fuente de contenido.

### 2.1 Riesgo NC

La web es gratuita, pero hoy los ejercicios están detrás de `login_required` y las
cuentas las crea el profesor. En la práctica, el contenido PAU solo lo verían
alumnos que pagan clases. Eso acerca el uso a "parte de un servicio de pago".

Mitigación propuesta: que la sección PAU sea **consultable sin cuenta**. La cuenta
solo serviría para guardar intentos. Sin anuncios ni llamadas a contratar clases
en esas páginas.

## 3. Esquema del ejercicio

Campos del formato T1 sin cambios: `id, number, version, title, course, topic,
concept, block, family, subtype, difficulty, estimated_minutes, response_mode,
response_prompt, response_fields[], assets[], tags[], status, learning_objective,
prerequisites[], difficulty_reason, common_mistakes[], parts_count,
statement_source, solution_source, solution_reference`.

Campos nuevos o ampliados:

```jsonc
{
  "id": "pau_cat_2024_set_s3_p2",          // estable: pau_<region>_<año>_<jun|set>_s<serie>_p<n>
  "course": "2bach",
  "origin": {
    "kind": "pau_oficial",                 // nuevo valor; los de 1º usan "original_teacher_bank"
    "region": "CAT",
    "year": 2024,
    "session": "setembre",                 // juny | setembre
    "call": "ordinaria",                   // ordinaria | extraordinaria
    "series": 3,
    "exercise_number": 2,
    "source_url": "https://eureka.bibliotecadigital.gencat.cat/handle/20.500.14344/299",
    "license": "CC BY-NC-SA 4.0",
    "attribution": "Generalitat de Catalunya. Departament de Recerca i Universitats. Consell Interuniversitari de Catalunya",
    "statement_fidelity": "literal",       // literal | traducido | adaptado
    "adaptation_note": null
  },
  "syllabus": {
    "current": true,                       // ¿entra en el temario vigente (LOMLOE)?
    "note": null                           // p. ej. "apartado c fuera de temario"
  },
  "part_points": { "a": 1.0, "b": 1.0 },   // puntuación oficial por apartado
  "relative_level": null,                  // solo otras comunidades: "inferior" | "similar" | "superior"
  "assets": [
    {
      "path": "static/exercises/2bach/<tema>/assets/pau_cat_2024_set_s3_p2_fig1.svg",
      "alt": "...",
      "source": "crop_original",           // crop_original | redrawn | own
      "license": "CC BY-NC-SA 4.0"
    }
  ],
  "status": "draft",                       // draft -> reviewed -> published
  "review": {
    "math_check": "pending",               // pending | ok | discrepancy
    "official_key_match": "pending",       // contraste con la pauta oficial
    "discrepancies": [],
    "reviewed_by": null,
    "reviewed_at": null
  },
  "solution_reference": "Elaboración propia; resultados contrastados con la pauta oficial."
}
```

Reglas:

- `solution_source` siempre es propia. La pauta oficial solo se usa para verificar.
- La web solo muestra `status: "published"`, y a `published` solo se llega con la
  revisión del profesor.
- `response_fields[].part` enlaza cada respuesta con su apartado y su `part_points`.

Unificación pendiente (deuda previa, no exclusiva de PAU): el piloto
`2bach/electromagnetismo/induccion/exercises.json` usa `estimated_time_min`,
`interactions` y `workflow.status`; los bancos de 1º usan `estimated_minutes`,
`response_fields` y `status`. Los ejercicios PAU usarán el formato de 1º.

## 4. Manifiesto de examen

```jsonc
{
  "id": "pau_cat_2024_set_s3",
  "region": "CAT",
  "year": 2024,
  "session": "setembre",
  "call": "ordinaria",
  "series": 3,
  "duration_minutes": 90,                  // a confirmar con cada examen
  "instructions": "...",                   // estructura de elección (p. ej. "responde X de Y")
  "exercises": ["pau_cat_2024_set_s3_p1", "pau_cat_2024_set_s3_p2"],
  "source_url": "...",
  "license": "CC BY-NC-SA 4.0",
  "syllabus_current": true
}
```

Los simulacros solo usan manifiestos de `region: "CAT"`. Los ejercicios de otras
comunidades aparecen solo en práctica por tema, con su `relative_level` visible.

## 5. Figuras

Esto **cambia la política de la spec 02 §6 solo para fuentes oficiales con
licencia abierta**:

- PAU oficial: recortar la figura del PDF original, en vectorial si el PDF lo
  permite (SVG). La licencia lo permite con atribución y evita errores al redibujar.
- Fuentes de terceros o sin licencia clara: se mantiene la política de redibujar.

## 6. Taxonomía de 2º (provisional)

El temario de 2º está por definir. Hasta entonces se usa la estructura de T1
(tema → familias con código corto y `block` legible) con estos temas provisionales:

| topic | Tema |
|---|---|
| `g` | Campo gravitatorio |
| `e` | Campo eléctrico |
| `m` | Campo magnético |
| `ind` | Inducción electromagnética |
| `osc` | Oscilaciones y ondas |
| `opt` | Óptica |
| `mod` | Física moderna (relatividad, cuántica, nuclear) |

Las familias dentro de cada tema se definen con el piloto, a partir de los
ejercicios reales. La lista es cerrada: el agente no crea categorías nuevas.

## 7. Pipeline

1. **Extracción**: página → imagen → transcripción del enunciado; recorte de figuras.
2. **Etiquetado**: tema/familia de la lista cerrada; `syllabus.current`.
3. **Solución propia** paso a paso.
4. **Verificación**: recálculo con Python de cada `expected_value`; contraste con la
   pauta oficial; discrepancias en `review.discrepancies`.
5. **Revisión del profesor** → `reviewed` → `published`.

## 8. Piloto

3 exámenes, para ajustar esquema y figuras antes de cargar en lote:

1. Setembre 2024, sèrie 3 (Eureka, licencia verificada).
2. Un examen de 2025, con el modelo nuevo (fuente y licencia por confirmar).
3. Un examen antiguo (≤ 2010), cuando se localice la fuente oficial.

Después: lotes de unos 10 exámenes al ritmo de revisión, empezando por los más
recientes.
