# Alta y cambio de ejercicios

Pasos para añadir un ejercicio nuevo o cambiar uno existente en 1.º
Bachillerato. El formato de cada campo está en
[exercise-bank-format.md](exercise-bank-format.md).

## 1. Preparar

1. Parte de `main` actualizado y crea una rama corta, por ejemplo
   `content/t1-nuevos-ejercicios`.
2. Decide el tema, el bloque y la familia. El bloque es el archivo
   `content/exercises/1bach/tN/<bloque>.json`. Si el bloque no existe,
   créalo y añádelo a `exercise_files` en `_topic.json`, en la posición donde
   debe aparecer.
3. Elige el `id`: el siguiente número libre de la familia (`t1_u_013`, por
   ejemplo). No reutilices el número de un ejercicio retirado. Busca el `id`
   en todo `content/exercises/` antes de usarlo.

## 2. Escribir el ejercicio

1. Copia un ejercicio del mismo bloque como plantilla y añade el nuevo en la
   posición que le toca dentro de la lista `exercises`. En T1 el orden importa:
   la dificultad no puede bajar dentro de un bloque y `number` debe ser
   consecutivo en todo el tema (si insertas uno en medio, renumera los que van
   detrás).
2. Escribe `statement_source` y `solution_source` en texto plano con LaTeX
   `\( … \)`. Cada apartado empieza línea con `(a)`, `(b)`...
3. Crea un campo en `response_fields` para cada resultado que se corrija, con
   la `part` del apartado. Calcula `expected_value` con precisión completa.
   Elige una `tolerance` que acepte la respuesta redondeada a las cifras que
   pide el enunciado.
4. Usa **g = 9,81 m/s²** salvo que el enunciado diga otra cosa.
5. Si lleva diagrama, guarda el SVG en `static/exercises/1bach/tN/assets/<id>.svg`
   con `viewBox="0 0 640 360"` y `style="max-width:100%;height:auto"`, y
   añádelo a `assets` con un `alt` que describa el dibujo. Criterios visuales:
   [exercise-diagrams.md](exercise-diagrams.md).
6. Rellena `origin` (`kind` obligatorio) y deja `status: "draft"` hasta que
   esté revisado. `draft` no oculta el ejercicio: los alumnos lo verán en
   cuanto se publique.

Recuerda: el corrector solo compara el valor. La unidad se muestra fija junto
al campo, y las cifras significativas no se corrigen.

## 3. Cambiar un ejercicio que ya existe

- Errata de texto que no cambia la respuesta: edita y listo.
- Cambio de datos, respuesta, tolerancia o campos: sube `version` en 1.
- Para retirar un ejercicio, pon `status: "retired"`. No lo borres ni
  reutilices su `id`.
- Si has corregido una clave equivocada y hay intentos entregados, recalcula
  las notas con `flask --app app regrade-exercise-attempts` (primero sin
  `--apply` para ver qué cambiaría).

## 4. Validar

Desde la raíz, con el entorno local (en Windows, `.\.venv\Scripts\python.exe`):

```powershell
python scripts/build_exercise_index.py      # regenera content/exercises/index.json
python scripts/validate_exercises.py        # formato de todos los bancos
python scripts/validate_t0_v4_bank.py       # si tocas T0
python scripts/validate_t0_v4_math.py       # si tocas T0
python scripts/validate_t1_math.py          # si tocas T1
python -m pytest
git diff --check
```

Algunos tests fijan el número de ejercicios por tema (127 en T0, 60 en T1 y en
cada uno de T3-T6) y que T3-T6 estén en `draft`. Si añades ejercicios o cambias
estados, actualiza esos números en el mismo commit:

- `tests/test_t0_v4_exercise_bank.py`
- `tests/test_t1_exercise_bank.py`
- `tests/test_t3_t6_exercise_banks.py`

En T1, `validate_t1_math.py` recalcula cada respuesta a partir del enunciado:
un ejercicio nuevo de T1 necesita su comprobación en ese script, o el script
falla.

## 5. Revisar en la web y publicar

1. Arranca la web en local (`scripts/run-local.ps1`) y abre el ejercicio:
   enunciado, diagrama, campos y solución.
2. Haz un intento con las respuestas correctas y comprueba que todas salen
   bien.
3. Abre la PR. En la descripción indica qué ejercicios añades o cambias y si
   has subido alguna `version`.
4. Al mergear en `main`, Render despliega (ver [deployment.md](deployment.md)).
