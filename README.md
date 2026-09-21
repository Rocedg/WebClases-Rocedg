# WebClases-Rocedg

Plataforma de Física de Bachillerato con apuntes PDF, ejercicios guiados, quizzes,
exámenes e historial de actividad.

Repositorio: [Rocedg/WebClases-Rocedg](https://github.com/Rocedg/WebClases-Rocedg).
La marca visible de la web sigue siendo **Web Clases Rocedg**.

Flask sirve plantillas Jinja, CSS y JavaScript convencional. El contenido editable
se guarda en JSON y LaTeX; SQLAlchemy guarda actividad, intentos y respuestas.
SQLite se usa en local y `DATABASE_URL` permite configurar PostgreSQL.

## Estructura

```text
WebClases-Rocedg/
├── app.py                   # Entrada Flask y rutas; gunicorn app:app
├── database.py, models.py    # SQLAlchemy y tablas existentes
├── services/                # Actividad e intentos/corrección
├── content/
│   ├── lessons/             # lessons.json, topics.json, summaries.json
│   │   ├── latex/           # T0–T6 y estilo común
│   │   └── intake/          # Material de referencia y preparación
│   ├── exercises/           # Banco por curso/tema, index.json, quizzes.json
│   │   └── latex/           # Plantillas de ejercicios
│   └── exams/               # exams.json
├── templates/               # HTML/Jinja
├── static/
│   ├── css/                 # Estilos de la aplicación
│   ├── js/                  # Visor, matemáticas, cronómetro y quizzes
│   ├── images/              # Logo y recursos compartidos
│   ├── lessons/             # PDFs publicados T0–T6
│   ├── exercises/           # Diagramas y recursos públicos de ejercicios
│   ├── pdfs/                # PDFs de referencia, quizzes y exámenes
│   └── vendor/              # PDF.js con versión fijada
├── scripts/                 # Arranque, generación y validación
├── tests/                   # pytest
├── docs/
│   ├── context/             # Arquitectura, reglas, progreso y specs
│   └── design/              # Referencias visuales
└── requirements.txt
```

Empieza por content/lessons/ para editar apuntes y content/exercises/ para editar
ejercicios. Sus archivos públicos se sirven desde static/: esta separación evita
publicar fuentes, respuestas internas y notas de preparación. Los PDFs conservan
sus URLs, incluidas las guardadas en el historial de actividad.

## Arranque en Windows

Desde la raíz, configura el entorno una vez:

```powershell
.\scripts\setup-local.ps1
.\.venv\Scripts\python.exe -m flask --app app init-db
```

Para iniciar, haz doble clic en scripts/start-web.bat o ejecuta:

```powershell
.\scripts\run-local.ps1
```

Abre <http://127.0.0.1:5000>. Mantén la terminal abierta y pulsa CTRL+C para parar.
Si la política de PowerShell bloquea los scripts, puedes usar el archivo .bat.

También puedes instalar y arrancar manualmente:

```powershell
py -m venv .venv
$env:PYTHONIOENCODING = "utf-8"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app init-db
.\.venv\Scripts\python.exe app.py
```

Usa python.exe -m pip y python.exe -m pytest: así los comandos no dependen de
lanzadores del entorno virtual creados antes del cambio de nombre de carpeta.
La base local sigue en instance/web_clases_rocedg.sqlite, fuera de Git.

La cuenta de demostración existente es Guest con contraseña studentpass.
La autenticación sigue usando los usuarios de prueba definidos en app.py.

## Contenido y validación

Cada banco se edita en content/exercises/<curso>/<tema>/exercises_<tema>.json.
El índice content/exercises/index.json es generado; no se edita a mano.

```powershell
.\.venv\Scripts\python.exe scripts/build_exercise_index.py
.\.venv\Scripts\python.exe scripts/validate_exercises.py
.\.venv\Scripts\python.exe scripts/validate_t0_v4_bank.py
.\.venv\Scripts\python.exe scripts/validate_t0_v4_math.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -B -c "from app import app; print(app.url_map)"
git diff --check
```

Para revisar una compilación de lecciones, con LaTeX instalado localmente:

```powershell
.\scripts\build_lessons.ps1
.\.venv\Scripts\python.exe scripts/check_lesson_numbers.py
```

La compilación queda en tmp/lesson-review/. Revisa los PDFs antes de copiar los
aprobados a static/lessons/ y actualizar sus páginas en
content/lessons/lessons.json. Render sirve los PDFs ya generados.

Las utilidades scripts/review_lessons.py <etapa> [carpeta_pdf] y
scripts/validate_lesson_delivery.py requieren PyMuPDF como herramienta local
de revisión (python -m pip install PyMuPDF). La validación de entrega compara
PDFs publicados, metadatos y enlaces, y necesita los .log y .aux de la compilación.
Capturas, registros y herramientas temporales se guardan en tmp/, fuera de Git.

## Render

Instala requirements.txt y conserva este comando:

```text
gunicorn app:app
```

Configura SECRET_KEY en producción y DATABASE_URL si usas PostgreSQL. Se conserva
el diseño actual de SQLAlchemy; esta limpieza no añade migraciones ni cambia
tablas. LaTeX y las herramientas de revisión no son necesarios en Render.

## Documentación

- [Arquitectura y mapa de contenido](docs/context/02-architecture.md).
- [Registro de progreso](docs/context/06-progress-tracker.md).
- [Persistencia de actividad](docs/context/user-activity-backend.md).
- [Intentos de ejercicios](docs/exercise-attempts.md).
- [Informe de reorganización](docs/repository-cleanup.md).
- [Instrucciones para agentes](AGENTS.md).

Las especificaciones originales y el registro cronológico se conservan en
docs/context/; sus entradas históricas pueden mencionar rutas anteriores.
