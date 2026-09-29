# Panel del profesor

> Estado: **preparado, no implementado.** Ya existen el rol `teacher`, la cuenta
> `Edgar` y el decorador `teacher_required` en `app.py`. Falta la vista del panel.

## Goal

Que el profesor vea, de forma resumida, lo que los alumnos van dejando en la web
(intentos de ejercicios, lecciones abiertas, progreso), sin tener que revisar la
base de datos a mano.

## User-facing behavior

- El profesor (rol `teacher`) ve todo lo que ve un alumno: apuntes, ejercicios,
  exámenes y progreso. Esto ya funciona porque esas rutas usan `login_required`.
- Además tendrá una sección propia, por ejemplo `/teacher`, protegida con
  `teacher_required`. Un alumno que entre recibe 403.
- Ideas para la primera versión del panel:
  - Resumen por alumno: último acceso, ejercicios intentados/entregados, tasa de
    acierto y tiempo total.
  - Resumen por ejercicio o tipo: cuántos alumnos lo han intentado, acierto medio,
    campos que más fallan.
  - Actividad reciente: últimas lecciones abiertas y ejercicios entregados.

## Datos disponibles hoy (`models.py`)

Todas las tablas se agrupan por `username`:

- `exercise_attempts` / `exercise_responses`: intentos, estado, duración, versión y
  resultado de cada campo (`grading_status`, `auto_score`).
- `user_activity_events`: eventos genéricos con tipo, objeto y duración.
- `user_topic_progress`: lecciones abiertas, última página y tiempo.
- `user_resource_access`: accesos a PDFs y recursos.
- `user_quiz_attempts`: cuestionarios (desactivados en la web ahora mismo).
- `user_study_state`: última lección y último ejercicio de cada alumno.

## Files likely to change

- `app.py` (ruta `/teacher` con `teacher_required`, entrada de navegación solo para profesores)
- `services/teacher_dashboard_service.py` (consultas de agregación, nuevo)
- `templates/teacher/dashboard.html` (nuevo)
- `tests/test_teacher_dashboard.py` (nuevo)

## Out of scope

- Editar o borrar datos de alumnos desde el panel.
- Cambiar el sistema de login (sigue siendo el diccionario `USERS`).
- Nuevas tablas o migraciones, salvo que una spec posterior lo apruebe.

## Implementation notes

- Requisito previo: **persistencia.** Con SQLite en el disco efímero de Render los
  datos se borran en cada deploy o reinicio, así que el panel mostraría poco. Hay
  que configurar antes una Postgres con `DATABASE_URL`.
- Excluir de las estadísticas las cuentas de prueba (`Guest`) y al propio profesor.
- **Antes de publicar el panel, cambiar la contraseña de `Edgar`.** Hoy está
  escrita en `app.py` (un espacio) y el repositorio es público, así que
  cualquiera podría entrar como profesor y ver los datos de los alumnos. Lo
  mínimo es leerla de una variable de entorno (por ejemplo `EDGAR_PASSWORD`).

## Validation checklist

- [ ] Un alumno recibe 403 en `/teacher`; sin sesión, redirige a `/login`.
- [ ] El profesor sigue viendo todas las páginas de alumno.
- [ ] El panel funciona con la base vacía.
- [ ] Pytest passes.

## Rollback notes

Quitar la ruta `/teacher` y su plantilla. El rol y la cuenta pueden quedarse.
