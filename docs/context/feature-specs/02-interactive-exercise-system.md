# Sistema interactivo de ejercicios

> Repository cleanup (2026-09-14): this document preserves the original planning paths.
> The generated index now lives at `content/exercises/index.json`, shared exercise
> LaTeX at `content/exercises/latex/`, and agent context at `docs/context/`.
> See `docs/context/02-architecture.md` for the current structure.

## 1. Vision de producto

El sistema de ejercicios debe evolucionar hacia una experiencia de aprendizaje guiada. No debe comportarse como el modelo actual de apuntes en PDF.

Modelo actual de apuntes:

- El PDF es el objeto principal.
- El usuario abre, lee y descarga.
- La pagina funciona como un indice de recursos.

Modelo futuro de ejercicios:

- El ejercicio es una pagina interactiva guiada.
- El PDF es solo un recurso dentro de la pagina.
- La pagina ayuda al estudiante a identificar el tipo de problema, resolver paso a paso, comprobar respuestas y revisar una solucion.

La pagina de un ejercicio debe contener:

- Enunciado visual compacto.
- Metadatos del ejercicio.
- Panel de resolucion.
- Pregunta de identificacion.
- Campos numericos o conceptuales.
- Boton de comprobacion.
- Feedback en la misma pagina.
- Solucion guiada.
- PDF de solucion completa.

Formula conceptual:

```text
Pagina de ejercicio =
metadatos + PDF visual del enunciado + panel interactivo de resolucion + feedback + solucion guiada + PDF formal de solucion
```

El PDF no debe ser "toda la pagina". La pagina debe ser un entorno de aprendizaje interactivo donde el PDF aporta el enunciado formal o imprimible, pero el aprendizaje ocurre en el panel.

Esta direccion apoya el objetivo a largo plazo: entrenar por tipo de problema, no solo acumular examenes o documentos. Un estudiante debe poder practicar "variacion de flujo por cambio de area", "ley de Lenz", "graficas de fem inducida" o cualquier subtipo concreto, independientemente de que el ejercicio venga de una PAU, de un PDF del profesor o de material propio.

## 2. Panel de resolucion del ejercicio

El `panel de resolucion` es el componente central del sistema. Es la parte de la pagina donde el estudiante piensa, responde, comprueba y recibe feedback.

### Layout de escritorio

Parte superior:

- Titulo.
- Curso.
- Tema.
- Tipo de ejercicio.
- Subtipo.
- Dificultad.
- Origen.

Area principal:

- Columna izquierda: visor del enunciado.
- Columna derecha: panel de resolucion.

### Layout movil

En movil la pagina debe priorizar una lectura lineal:

1. Cabecera.
2. Visor del enunciado.
3. Panel de resolucion.
4. Resultados.
5. Solucion.

### A. Estado del intento

El panel debe mostrar de forma clara el estado actual del intento. Ejemplos:

- Sin comprobar.
- Respuestas incompletas.
- Comprobado.
- 3/4 correctas.
- Solucion consultada.

Este estado no implica todavia persistencia en base de datos. En el MVP puede existir solo en el navegador mientras la pagina esta abierta.

### B. Paso de identificacion

Antes de calcular, el estudiante debe identificar el tipo de problema. Esto entrena la lectura del enunciado y evita que el alumno empiece aplicando formulas sin saber que esta cambiando.

Ejemplo para Faraday-Lenz:

```text
Pregunta:
Que magnitud provoca la variacion del flujo magnetico?

Opciones:
- Campo magnetico B
- Area efectiva A
- Angulo theta
- Numero de espiras N

Respuesta correcta para una varilla movil sobre railes:
Area efectiva A
```

Proposito: el estudiante debe reconocer que en una varilla que se desplaza sobre railes cambia el area efectiva, no necesariamente el campo magnetico ni el angulo.

### C. Campos de respuesta numerica

Ejemplos:

- `|epsilon| = [input] V`
- `I = [input] A`
- `E = [input] J`

Cada campo numerico debe poder definir:

- `expected_value`
- `tolerance`
- `unit`
- `accepted_formats`, mas adelante
- `feedback_correct`
- `feedback_incorrect`

En el MVP, la comprobacion numerica puede ser sencilla:

1. Leer el texto introducido.
2. Convertir coma decimal a punto decimal.
3. Convertir a numero.
4. Comparar con `expected_value` usando `tolerance`.

No hace falta resolver todavia todos los formatos posibles de notacion cientifica, unidades escritas o expresiones algebraicas. Eso puede crecer por fases.

### D. Campos conceptuales o de opcion unica

El panel debe soportar respuestas no numericas, especialmente de opcion unica.

Ejemplos:

- Sentido de corriente inducida.
- Tipo de grafica.
- Relacion de proporcionalidad.
- Opcion correcta.

Estos campos son importantes porque muchos errores de fisica no son numericos. A veces el calculo esta bien, pero el estudiante no entiende el signo, el sentido fisico o la relacion cualitativa.

### E. Botones de accion

Antes de comprobar:

- `Comprobar respuestas`
- `Ver pista`
- `No se hacerlo / Ver solucion`

Despues de comprobar:

- `Reintentar`
- `Ver solucion`
- `Practicar otro parecido`, solo como idea futura

La accion principal debe ser `Comprobar respuestas`. La solucion no debe ser el primer camino visual, aunque debe existir una salida clara para el estudiante bloqueado.

### F. Bloque de resultados

Al pulsar `Comprobar respuestas`, la pagina debe mostrar los resultados en linea. No debe redirigir a otra pagina.

Ejemplo de resultado:

```text
Resultado del intento:
3/4 correctas

✓ Tipo de ejercicio:
Correcto. Cambia el area efectiva.

✓ Fem inducida:
Correcto. |epsilon| = 1,95 × 10^-3 V.

✗ Intensidad:
Tu respuesta: 2,0 × 10^-4 A.
Esperado: 2,29 × 10^-4 A.
Revisa I = |epsilon| / R.

✓ Sentido:
Correcto. La corriente inducida es antihoraria.
```

El feedback debe estar junto a la respuesta revisada. El estudiante debe entender que ha fallado y que debe repasar, no solo ver una marca roja.

### G. Comportamiento de la solucion

La solucion debe estar oculta por defecto.

Comportamiento recomendado para el MVP:

- El boton normal `Ver solucion` aparece despues de pulsar `Comprobar respuestas`.
- Puede existir una opcion secundaria: `No se hacerlo -> Ver solucion`.
- En el futuro, si el estudiante consulta la solucion antes de intentar, se puede registrar `solution_viewed_before_attempt = true`.

La solucion debe tener dos capas:

1. Solucion guiada en HTML:
   - Corta y paso a paso.
   - Legible.
   - Util para movil.
   - Puede incorporar MathJax mas adelante.

2. PDF formal de solucion:
   - Imprimible.
   - Compacto pero completo.
   - Generado desde LaTeX.

Importante: esta rama no implementa el panel ni la solucion. Solo documenta el comportamiento esperado.

## 3. Modelo de datos de ejercicios

Cada ejercicio debe poder describirse con metadatos suficientes para filtrar, renderizar, comprobar interacciones y escalar despues hacia seguimiento.

Campos previstos:

- `id`
- `title`
- `course`
- `block`
- `topic`
- `concept`
- `exercise_type`
- `subtype`
- `difficulty`
- `estimated_time_min`
- `origin`
- `statement_tex`
- `solution_tex`
- `statement_pdf`
- `solution_pdf`
- `assets`
- `tags`
- `interactions`
- `solution.summary_steps`
- `common_mistakes`
- `workflow/status`

No todos los campos tienen que usarse en el MVP, pero conviene diseñar la estructura ahora para no rehacer el modelo cuando aparezcan filtros, panel interactivo, generacion de PDFs o seguimiento.

Ejemplo JSON basado en Faraday-Lenz:

```json
{
  "id": "faraday_area_motional_001",
  "title": "Varilla conductora que se desplaza sobre railes",
  "course": "2bach",
  "block": "Electromagnetismo",
  "topic": "Induccion electromagnetica",
  "concept": "Ley de Faraday-Lenz",
  "exercise_type": "Variacion de flujo magnetico",
  "subtype": "Cambio de area efectiva",
  "difficulty": 3,
  "estimated_time_min": 12,
  "origin": {
    "kind": "teacher_pdf_adapted",
    "region": "",
    "year": "",
    "session": "",
    "exercise_number": "",
    "source_ref": "source_refs/original_pdf_crops/ex1.png",
    "adaptation": "adapted"
  },
  "statement_tex": "content/exercises/2bach/electromagnetismo/induccion/statements/faraday_area_motional_001.tex",
  "solution_tex": "content/exercises/2bach/electromagnetismo/induccion/solutions/faraday_area_motional_001.tex",
  "statement_pdf": "static/exercises/2bach/electromagnetismo/induccion/pdfs/faraday_area_motional_001_statement.pdf",
  "solution_pdf": "static/exercises/2bach/electromagnetismo/induccion/pdfs/faraday_area_motional_001_solution.pdf",
  "assets": [
    "static/exercises/2bach/electromagnetismo/induccion/assets/faraday_area_motional_001.svg"
  ],
  "tags": [
    "faraday",
    "lenz",
    "flujo magnetico",
    "area variable",
    "varilla movil"
  ],
  "interactions": [
    {
      "id": "identify_flux_change",
      "type": "single_choice",
      "label": "Tipo de variacion del flujo",
      "prompt": "Que magnitud provoca la variacion del flujo magnetico?",
      "options": [
        { "id": "b_field", "label": "Campo magnetico B" },
        { "id": "area", "label": "Area efectiva A" },
        { "id": "angle", "label": "Angulo theta" },
        { "id": "turns", "label": "Numero de espiras N" }
      ],
      "correct_option_id": "area",
      "feedback_correct": "Correcto. El area efectiva cambia porque la varilla se desplaza.",
      "feedback_incorrect": "Revisa Phi = BAcos(theta). En este caso B y theta permanecen constantes."
    },
    {
      "id": "emf_magnitude",
      "type": "numeric",
      "label": "Fem inducida",
      "prompt": "Introduce el modulo de la fem inducida.",
      "expected_value": 0.00195,
      "unit": "V",
      "tolerance": 0.00005,
      "feedback_correct": "Correcto. Se obtiene |epsilon| = BLv.",
      "feedback_incorrect": "Revisa la expresion |epsilon| = BLv y las conversiones de unidades."
    }
  ],
  "solution": {
    "summary_steps": [
      "El flujo magnetico es Phi = BAcos(theta).",
      "En este ejercicio B y theta son constantes.",
      "La varilla cambia el area efectiva A.",
      "Como A = Lx y x = x0 + vt, se cumple dA/dt = Lv.",
      "Por Faraday: |epsilon| = BLv.",
      "La corriente se calcula con I = |epsilon|/R.",
      "El sentido se determina con la ley de Lenz."
    ]
  },
  "common_mistakes": [
    "No identificar que magnitud cambia en Phi = BAcos(theta).",
    "Confundir area total con area efectiva.",
    "No convertir centimetros a metros.",
    "No convertir militeslas a teslas.",
    "Olvidar el sentido fisico impuesto por la ley de Lenz."
  ],
  "workflow": {
    "status": "draft",
    "reviewed": false,
    "copyright_review": "pending"
  }
}
```

Notas de diseño:

- `id` debe ser estable. No se debe renombrar sin revisar enlaces, intentos futuros o PDFs asociados.
- `difficulty` puede empezar como escala 1-5.
- `origin` permite distinguir ejercicio propio, PAU oficial, PDF del profesor o adaptacion.
- `interactions` permite empezar con `single_choice` y `numeric`, y ampliar despues a otros tipos.
- `workflow` ayuda a separar ejercicios en borrador, revisados o pendientes de revision de fuente.

## 4. Estructura de archivos

Principio importante:

```text
content/ es el taller interno.
static/ es lo que la web sirve publicamente.
```

Estructura futura recomendada:

```text
content/
  exercises/
    2bach/
      electromagnetismo/
        induccion/
          exercises_<tema>.json
          statements/
            faraday_area_motional_001.tex
            faraday_b_variable_001.tex
            faraday_theta_rotation_001.tex
          solutions/
            faraday_area_motional_001.tex
            faraday_b_variable_001.tex
            faraday_theta_rotation_001.tex
          assets/
            faraday_area_motional_001.svg
            faraday_b_variable_001.png
            faraday_theta_rotation_001.svg
          source_refs/
            original_pdf_crops/
            notes/

static/
  exercises/
    2bach/
      electromagnetismo/
        induccion/
          assets/
          pdfs/
          thumbs/

data/
  exercises_<tema>.json

scripts/
  build_exercises.py
  validate_exercises.py

templates/
  user/
    practice.html
    exercise_detail.html

static/
  js/
    exercise-panel.js
  css/
    practice.css
```

Explicacion de carpetas:

### `content/exercises/`

Contiene los archivos editables de trabajo:

- Fuentes LaTeX.
- `exercises_<tema>.json` por tema.
- Assets internos.
- Referencias de fuente.
- Recortes originales usados para revisar o adaptar material.

Esta carpeta no tiene por que servirse directamente en Flask.

### `static/exercises/`

Contiene los archivos publicos:

- PDFs generados.
- Imagenes optimizadas.
- Miniaturas.
- Assets que Flask puede servir con seguridad.

Los PDFs e imagenes que vea el estudiante deben estar aqui, no en `content/`.

### `data/exercises.json`

Indice consolidado para Flask:

- Se generara mas adelante desde los metadatos por tema.
- Flask debe leer este archivo, no recorrer toda la estructura `content/`.
- Cuando exista automatizacion, no deberia editarse manualmente.

### `scripts/`

Herramientas futuras:

- `build_exercises.py` para compilar, copiar y consolidar.
- `validate_exercises.py` para validar metadatos, rutas e interacciones.

No son obligatorias en la primera rama de implementacion, pero quedan planificadas.

### `templates/user/practice.html`

Pagina futura de listado y filtrado de ejercicios.

### `templates/user/exercise_detail.html`

Pagina futura de detalle del ejercicio con visor del enunciado y panel de resolucion.

### `static/js/exercise-panel.js`

JavaScript futuro para comprobacion local de respuestas.

### `static/css/practice.css`

Estilos futuros para la interfaz de practica.

No se deben crear todos estos archivos en esta rama salvo que se haga como documentacion vacia aprobada. Para esta tarea, solo se documenta la estructura.

## 5. Flujo de LaTeX y generacion de PDFs

Decisiones principales:

- El codigo fuente LaTeX vive en `content/`.
- La web publica no compila LaTeX al recibir una peticion.
- Los PDFs se generan localmente antes de hacer commit o deploy.
- La web sirve PDFs ya generados desde `static/`.
- Render no necesita instalar LaTeX.

Esto evita:

- Complejidad en Render.
- Lentitud en runtime.
- Errores por dependencias LaTeX en produccion.
- Bloqueos si muchos usuarios abren ejercicios a la vez.

### Estilo del PDF de enunciado

El PDF del enunciado debe ser compacto, parecido en densidad a un enunciado de PAU/selectividad:

- Margenes compactos.
- Poco espacio decorativo.
- Titulo claro.
- Apartados visibles.
- Ecuaciones legibles.
- Figura cerca del texto.
- Sin padding tipo tarjeta dentro del PDF.
- Apto para movil y para imprimir.

El PDF del enunciado no debe intentar ser una pagina web bonita. Debe ser un documento academico claro, corto y funcional.

### Estilo del PDF de solucion

El PDF de solucion puede ser mas detallado que el enunciado, pero tambien debe evitar exceso de espacio en blanco. Debe ser imprimible, ordenado y suficientemente completo para revisar el ejercicio.

### Proceso futuro de construccion

1. El mantenedor edita:
  - `content/.../exercises_<tema>.json`
   - `content/.../statements/*.tex`
   - `content/.../solutions/*.tex`
   - `content/.../assets/*`

2. El mantenedor ejecuta:

   ```powershell
   python scripts/build_exercises.py
   ```

3. El script:
   - Valida todos los IDs de ejercicios.
   - Comprueba campos obligatorios.
   - Comprueba rutas.
   - Comprueba interacciones.
   - Compila PDFs de enunciado.
   - Compila PDFs de solucion.
   - Copia PDFs a `static/exercises/.../pdfs/`.
   - Copia assets publicos optimizados a `static/exercises/.../assets/`.
   - Opcionalmente genera miniaturas.
   - Genera o actualiza `data/exercises.json`.

4. Flask lee solo `data/exercises.json`.

5. Render sirve PDFs y assets estaticos. Render no necesita LaTeX.

El script futuro puede usar `latexmk` u otro comando local de compilacion LaTeX. La implementacion concreta queda fuera de esta rama.

### Archivos LaTeX independientes y plantillas comunes

Al principio puede ser util que cada `.tex` sea completo e independiente para probarlo en TeXstudio o en una instalacion local. A largo plazo, conviene introducir plantillas o preambulos compartidos para mantener una apariencia comun.

Objetivo a largo plazo:

- Cada ejercicio se puede editar de forma independiente.
- Todos los ejercicios comparten un estilo visual coherente.
- El mantenedor puede probar un ejercicio suelto sin entender toda la automatizacion.

## 6. Flujo de imagenes y graficas

Principios:

- Las imagenes o recortes originales de PDFs son referencias internas, no assets publicos finales.
- Los assets publicos deben recrearse, limpiarse u optimizarse cuando sea razonable.
- Para diagramas simples de fisica, usar SVG siempre que sea posible.
- Usar PNG cuando recrear en SVG no compense.
- Usar TikZ solo cuando aporte valor claro y no ralentice la produccion.
- Mantener un estilo visual consistente entre ejercicios.

### Flujo recomendado

1. Material de origen:
   - PDF de PAU.
   - PDF del profesor.
   - Problema de una web.
   - Ejercicio propio.

2. Extraer o inspeccionar la figura original:
   - Recortar si hace falta.
   - Guardar en `content/.../source_refs/original_pdf_crops/`.
   - Usar solo como referencia interna.

3. Decidir estrategia:
   - Diagrama simple: recrear como SVG.
   - Grafica: recrear como SVG o imagen generada.
   - Figura compleja puntual: usar PNG limpiado si es aceptable.
   - Figura reutilizable de alto valor: recrear cuidadosamente como SVG.

4. Asset publico:
   - Guardar en `static/exercises/.../assets/`.

5. Enunciado LaTeX:
   - Incluir el asset publico en el PDF.

6. Pagina web:
   - Puede reutilizar el mismo asset publico si lo necesita.

### Politica operativa para reducir riesgo de copyright

Esto no es asesoramiento legal. Es una politica practica de trabajo para mantener el proyecto ordenado y prudente:

- No publicar figuras originales de terceros tal cual cuando sea evitable.
- Recrear diagramas con un estilo propio y consistente.
- Guardar metadatos sobre la fuente original.
- Preservar la fisica, los valores y el razonamiento cuando proceda.
- Adaptar ligeramente nombres, contexto y redaccion para evitar copiar texto literal.
- No presentar soluciones de terceros como propias sin adaptacion y reescritura.

## 7. Tema piloto: induccion / Faraday-Lenz

El primer piloto debe ser induccion electromagnetica, especialmente Faraday-Lenz.

Motivos:

- Tiene tipos de problema claros.
- Soporta diagramas visuales.
- Entrena muy bien la identificacion antes de calcular.
- Sus subtipos se organizan de forma natural a partir de la expresion del flujo.

Formula central:

```text
Phi = B A cos(theta)
```

Clasificacion de problemas:

- Cambio de `B`.
- Cambio de area efectiva `A`.
- Cambio de angulo `theta`.
- Casos combinados.
- Interpretacion de graficas `Phi(t)`, `B(t)` o `epsilon(t)`.
- Ley de Lenz y sentido de corriente.
- Fem maxima y casos de corriente alterna.

Ejercicios piloto planificados:

### 1. `faraday_area_motional_001`

- Varilla movil sobre railes.
- Cambio de area efectiva.
- Calculo de fem inducida.
- Calculo de corriente.
- Sentido de la corriente.

### 2. `faraday_b_variable_001`

- Campo magnetico variable en el tiempo.
- Area y angulo constantes.
- Calculo de `epsilon(t)`.
- Identificacion del tipo de grafica.

### 3. `faraday_theta_rotation_001`

- Espira que gira.
- Cambio de angulo.
- Flujo sinusoidal.
- Fem inducida.
- Fem maxima.

### 4. `faraday_period_ratio_001`, opcional mas adelante

- Espira giratoria.
- Cambio de periodo.
- `epsilon_max` proporcional a `1/T`.

No se deben crear estos ejercicios en esta rama. Solo quedan documentados como plan de piloto.

## 8. Plan de implementacion web

### Fase 1: Especificacion

- Rama actual.
- Sin cambios de comportamiento.
- Sin UI nueva.
- Sin scripts nuevos.
- Sin datos reales de ejercicios.

### Fase 2: Esqueleto de contenido

- Crear `content/exercises/`.
- Crear `static/exercises/`.
- Anadir archivos de metadatos de ejemplo.
- Sin UI web todavia.

### Fase 3: Ejercicios piloto

- Anadir 3-5 ejercicios de induccion.
- Incluir enunciados y soluciones LaTeX.
- Incluir PDFs generados manualmente.
- Incluir assets SVG/PNG publicos.
- Incluir interacciones en metadatos.

### Fase 4: Pagina indice de practica

- Ruta futura: `/practice`.
- Cargar `data/exercises.json`.
- Mostrar tarjetas de ejercicios.
- Filtrar por curso, tema, tipo, subtipo, dificultad y origen.
- Sin seguimiento avanzado.

### Fase 5: Pagina de detalle del ejercicio

- Ruta futura: `/exercise/<id>`.
- Cabecera con metadatos.
- Enunciado incrustado como PDF o visor de imagen.
- Panel de resolucion.
- Interacciones `single_choice`.
- Interacciones `numeric`.
- Boton `Comprobar`.
- Resultados en linea.
- `Ver solucion` despues de comprobar.
- Solucion guiada.
- Enlace o visor del PDF de solucion.

### Fase 6: Automatizacion de construccion

- `scripts/build_exercises.py`.
- `scripts/validate_exercises.py`.
- Compilar PDFs desde LaTeX.
- Copiar assets.
- Generar `data/exercises.json` consolidado.

### Fase 7: Escalado de contenido

- Ingerir ejercicios por tema.
- Anadir 10-20 ejercicios por lote.
- Revisar despues de cada lote.
- Evitar importaciones de 200 ejercicios sin validacion.

### Fase 8: Seguimiento futuro

Fuera de alcance por ahora:

- Base de datos.
- Intentos persistentes.
- Panel del profesor.
- Analitica de estudiantes.
- Recomendaciones.
- PostgreSQL.
- Refactor de cuentas.

El modelo de datos debe ser compatible con estas capas futuras, pero no implementarlas todavia.

## 9. Reglas de trabajo Codex para este subsistema

Las sesiones futuras de Codex que trabajen en ejercicios deben seguir estas reglas:

- Leer siempre `AGENTS.md` y `context/` antes de editar.
- Trabajar en ramas pequenas.
- No combinar documentacion, ingesta de contenido, UI, automatizacion y base de datos en una sola rama.
- En cada rama de implementacion, listar archivos afectados antes de editar.
- En cada lote de contenido, limitarse a un numero manejable de ejercicios.
- Nunca importar mas de 100 ejercicios en un solo paso.
- No cambiar el comportamiento actual de apuntes, temas, examenes o quizzes salvo que la tarea lo pida explicitamente.
- Mantener Flask, Jinja y JSON.
- Mantener compatibilidad con Render.
- Mantener tests pasando.
- Si hay cambios de codigo, ejecutar `pytest`.
- Si hay cambios de contenido, ejecutar validacion cuando exista.
- Actualizar `context/06-progress-tracker.md` al terminar.

Secuencia recomendada de ramas:

1. `dev/exercise-system-spec`
2. `dev/exercise-content-skeleton`
3. `dev/induction-exercise-pilot`
4. `dev/practice-page-mvp`
5. `dev/exercise-detail-panel-mvp`
6. `dev/exercise-build-automation`

## 10. Fuera de alcance

No se debe implementar todavia:

- Base de datos.
- PostgreSQL.
- Persistencia de progreso del estudiante.
- Panel del profesor.
- Generacion de ejercicios por IA dentro de la web.
- Compilacion LaTeX en Render.
- Compilacion LaTeX dinamica en servidor.
- Integracion completa de PDF.js, salvo que una spec posterior la pida.
- Integracion de MathJax, salvo que una spec posterior la pida.
- Importacion masiva de ejercicios.
- Modificacion de quizzes actuales sin plan de migracion.
- Eliminacion del comportamiento actual de quizzes o homework.
- Migracion a React o Next.js.

## 11. Relacion con el tracker de progreso

Esta spec requiere actualizar `context/06-progress-tracker.md` con:

- Fase actual: planificacion del sistema de ejercicios y practica interactiva.
- Trabajo completado: consolidacion del sitio, scripts locales y smoke tests, sistema de contexto, decision inicial sobre ejercicios interactivos.
- Trabajo en curso: especificacion del sistema LaTeX/PDF/interactivo.
- Siguientes pasos: esqueleto de contenido, piloto de induccion, validacion del formato LaTeX/PDF, `/practice` MVP y `/exercise/<id>` MVP.
- Decisiones: Flask/Jinja/JSON, `content/` como fuente editable, `static/` como salida publica, LaTeX con PDFs pregenerados, sin compilacion en Render, panel interactivo con `single_choice` y `numeric`.
- Riesgos: sobreingenieria, importacion excesiva, gestion de fuentes, duplicacion entre fuente y salida, perdida de comprension del mantenedor.

## 12. Validacion esperada

Como esta rama es solo de documentacion:

- No ejecutar migraciones.
- No cambiar comportamiento.
- No tocar `app.py`, `templates/`, `static/`, `data/`, `tests/` ni dependencias.
- Ejecutar `git status`.
- Si existe entorno local, ejecutar:

  ```powershell
  .\.venv\Scripts\python.exe -m pytest
  ```

Al cerrar la tarea se debe reportar:

- Archivos creados.
- Archivos modificados.
- Si se ejecutaron tests.
- Si los tests pasaron.
- Suposiciones realizadas.

Commit recomendado:

```text
Document interactive exercise system plan
```

Rama:

```text
origin/dev/exercise-system-spec
```

No abrir ni fusionar la PR automaticamente. Si es posible, reportar la URL de comparacion o PR.
