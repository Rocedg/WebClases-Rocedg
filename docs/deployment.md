# Despliegue: Render y Neon

Cómo está montada la web en producción y qué hay que tener en cuenta al subir
cambios. Lo que se puede comprobar en el repositorio está descrito tal cual.
Lo marcado con ⚠ depende de la configuración de los paneles de Render o Neon y
hay que confirmarlo allí.

## Piezas

| Pieza | Qué hace | Dónde se configura |
| --- | --- | --- |
| Render (servicio web) | Instala `requirements.txt` y arranca `gunicorn app:app`. | Panel de Render. No hay `render.yaml` en el repo. |
| Neon (Postgres) | Guarda usuarios, intentos, respuestas y actividad. | Panel de Neon. La cadena de conexión va en `DATABASE_URL` de Render. |
| GitHub `main` | Código y contenido que se despliegan. | ⚠ Confirmar en Render → Settings si el despliegue automático desde `main` está activado. |

Todo el contenido educativo (JSON, PDFs, SVG) va dentro del repositorio. Neon
solo guarda lo que hacen los usuarios.

## Variables de entorno en Render

| Variable | Obligatoria | Notas |
| --- | --- | --- |
| `SECRET_KEY` | sí | Sin ella la app no arranca (`RuntimeError` al importar `app.py`). Firma las sesiones: si cambia, se cierran todas las sesiones abiertas. |
| `DATABASE_URL` | sí en producción | Cadena de Neon. `database.py` convierte `postgres://` y `postgresql://` a `postgresql+psycopg2://`. Sin ella la app usa SQLite en el disco de Render, que se borra en cada despliegue o reinicio. |

Estas cadenas son contraseñas: no se copian en el repositorio, en el chat ni
en archivos del proyecto.

## Base de datos

- Al arrancar, `app.py` ejecuta `db.create_all()` y `ensure_database_schema()`.
  Crea las tablas y columnas que falten y no borra nada. No hay migraciones
  ni hace falta ejecutar `init-db` en Render.
- Neon se duerme tras unos minutos sin uso. `database.py` usa
  `pool_pre_ping` y `pool_recycle=280` para que la primera visita después de
  dormir no dé error 500.
- Cambiar el esquema (tablas o columnas nuevas) no está cubierto por este
  arranque automático más allá de lo que añade `ensure_database_schema()`.
  Cualquier cambio de tablas necesita aprobación explícita
  (`docs/context/04-ai-workflow-rules.md`).
- ⚠ Copias de seguridad: el plan gratuito de Neon permite restaurar a un
  momento reciente con una ventana corta. Confirmar la ventana en el panel.

## Cuentas

- El arranque no crea cuentas. Los alumnos se crean desde **Cuentas** en el
  panel del profesor.
- `flask create-local-account` solo funciona con SQLite local: se niega a
  ejecutarse si `DATABASE_URL` apunta a Postgres.
- ⚠ No hay un comando para crear una cuenta de profesor directamente en Neon.
  Si se pierde el acceso de profesor, hay que hacerlo con SQL desde el panel de
  Neon.

## Qué no va a Render

- LaTeX: los PDFs de lecciones se compilan en local y se publican ya generados
  en `static/lessons/`. Ninguna petición compila LaTeX.
- PyMuPDF y las herramientas de revisión de `scripts/`.
- `instance/`, `.env`, `tmp/`: están en `.gitignore`.

## Antes de subir a `main`

1. Tests en local: `python -m pytest`.
2. Si has tocado ejercicios: los pasos de validación de
   [exercise-workflow.md](exercise-workflow.md).
3. Si has tocado lecciones: PDFs compilados y revisados en `static/lessons/` y
   páginas actualizadas en `content/lessons/lessons.json`.
4. Recorrido rápido de [release-checklist.md](release-checklist.md).

## Después de desplegar

1. En Render → **Events** o **Logs**, comprueba que el despliegue terminó y no
   hay `Traceback` al arrancar.
2. Abre la web, entra y abre un ejercicio.
3. Si algo falla, copia del log las líneas del error (nunca las variables de
   entorno) para revisarlas.

## Volver atrás

- Lo más seguro es revertir el commit en GitHub (`git revert`) y dejar que
  Render despliegue de nuevo. No se reescribe la historia de `main`.
- ⚠ Render también permite volver a desplegar un despliegue anterior desde
  **Events**. Comprobar si el plan actual lo permite.
- Revertir código no deshace cambios en Neon. Hasta ahora ningún despliegue
  borra datos, porque el arranque solo añade tablas y columnas.

## Local frente a producción

| | Local | Producción |
| --- | --- | --- |
| Base de datos | `instance/web_clases_rocedg.sqlite` | Neon vía `DATABASE_URL` |
| `SECRET_KEY` | Aleatoria si arrancas con `python app.py`; obligatoria con `flask` o `gunicorn` | Variable de Render |
| Arranque | `scripts/run-local.ps1` | `gunicorn app:app` |

No pongas la cadena de Neon en tu ordenador salvo que quieras trabajar a
propósito contra los datos reales de los alumnos.
