from datetime import datetime
from functools import wraps
import json
import os

import click
from sqlalchemy import inspect, text
from flask import Flask, jsonify, redirect, render_template, request, send_file, session, url_for

from database import db, init_app as init_database
from services.exercise_presentation import render_exercise_source, response_format_notes, response_placeholder
from services.activity_service import (
    get_user_activity_snapshot,
    mark_topic_opened,
    record_activity_event,
    record_quiz_attempt,
    record_resource_access,
)
from services.exercise_attempt_service import (
    ExerciseAttemptError,
    ExerciseAttemptForbidden,
    attempt_correction_summary,
    field_map,
    format_duration,
    get_catalogue_attempt_summaries,
    get_owned_attempt,
    get_student_attempt_history,
    latest_started_attempt,
    next_exercise_after,
    response_fields,
    response_map,
    regrade_submitted_attempts,
    save_draft,
    start_or_resume_attempt,
    sync_attempt_timer,
    submit_attempt,
)


app = Flask(__name__)
app.jinja_env.filters['exercise_source'] = render_exercise_source
app.jinja_env.globals.update(response_format_notes=response_format_notes, response_placeholder=response_placeholder)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
init_database(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

USERS = {
    'Paul': ['fisica2026', 'student'],
    'Guest': ['studentpass', 'student']
}

NAV_ITEMS = [
    {
        'endpoint': 'topics',
        'label': 'Apuntes',
        'description': 'Lecciones en PDF',
        'icon': 'fa-book-open'
    },
    {
        'endpoint': 'homework',
        'label': 'Ejercicios',
        'description': 'Cuestionarios autocorregibles',
        'icon': 'fa-pen-ruler'
    },
    {
        'endpoint': 'exams',
        'label': 'Exámenes',
        'description': 'Simulacros y correcciones',
        'icon': 'fa-file-circle-check'
    },
    {
        'endpoint': 'progress',
        'label': 'Progreso',
        'description': 'Ruta recomendada y refuerzo',
        'icon': 'fa-chart-line'
    }
]


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def load_json_file(path, fallback):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return fallback


def content_path(filename):
    return os.path.join(CONTENT_DIR, filename)


def load_topics():
    return load_json_file(content_path('lessons/topics.json'), {'topics': []})


def load_quizzes():
    quizzes_path = content_path('exercises/quizzes.json')

    try:
        if not os.path.exists(quizzes_path):
            with open(quizzes_path, 'w', encoding='utf-8') as f:
                json.dump({'quizzes': []}, f)

        with open(quizzes_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        valid_quizzes = []
        for quiz in data.get('quizzes', []):
            required = ['id', 'title', 'question_count', 'correct_answers', 'pdfs']
            if all(key in quiz for key in required):
                valid_quizzes.append(quiz)
            else:
                print(f"Quiz inválido omitido: {quiz.get('title', 'Sin título')}")

        return {'quizzes': valid_quizzes}
    except Exception as e:
        print(f"Error cargando quizzes: {str(e)}")
        return {'quizzes': []}


def load_exams():
    return load_json_file(content_path('exams/exams.json'), {'exams': []})


def load_summaries():
    return load_json_file(content_path('lessons/summaries.json'), {'summaries': []})


def load_lessons():
    return load_json_file(content_path('lessons/lessons.json'), {'lessons': []})


def load_exercise_index():
    return load_json_file(content_path('exercises/index.json'), {'exercises': []})


EXERCISE_BANK_FILENAMES = (
    'exercises_t0.json',
    'exercises_t1.json',
    'exercises_t2.json',
    'exercises.json',
)


def exercise_bank_paths():
    exercises_root = os.path.join(CONTENT_DIR, 'exercises')
    paths = []
    for root, dirs, files in os.walk(exercises_root):
        dirs.sort()
        for filename in EXERCISE_BANK_FILENAMES:
            if filename in files:
                paths.append(os.path.join(root, filename))
    return paths


def load_exercise_catalogue():
    exercises = []

    for bank_path in exercise_bank_paths():
        data = load_json_file(bank_path, {'exercises': []})
        for exercise in data.get('exercises', []):
            if isinstance(exercise, dict) and exercise.get('id') and exercise.get('status') != 'retired':
                exercise.setdefault('version', 1)
                exercises.append(exercise)

    if exercises:
        return {'exercises': exercises}

    data = load_exercise_index()
    for exercise in data.get('exercises', []):
        if isinstance(exercise, dict):
            exercise.setdefault('version', 1)
    return data


def asset_url(path):
    if not path:
        return ''
    if path.startswith(('http://', 'https://', '/')):
        return path
    if path.startswith('static/'):
        return url_for('static', filename=path.replace('static/', '', 1))
    return url_for('static', filename=path)


def static_resource_path(path):
    if not path or path.startswith(('http://', 'https://', '/')):
        return None

    normalized_path = path.replace('\\', '/').lstrip('/')
    if normalized_path.startswith('static/'):
        normalized_path = normalized_path.replace('static/', '', 1)

    parts = [part for part in normalized_path.split('/') if part]
    if not parts or any(part in {'.', '..'} for part in parts):
        return None

    candidate = os.path.abspath(os.path.join(STATIC_DIR, *parts))
    static_root = os.path.abspath(STATIC_DIR)
    try:
        if os.path.commonpath([static_root, candidate]) != static_root:
            return None
    except ValueError:
        return None

    return candidate


def content_disposition_header(action, filename):
    disposition = 'attachment' if action == 'download' else 'inline'
    try:
        filename.encode('ascii')
    except UnicodeEncodeError:
        return None

    safe_filename = filename.replace('\\', '_').replace('/', '_').replace('"', '\\"')
    return f'{disposition}; filename="{safe_filename}"'


def send_tracked_pdf(resource, action):
    local_path = static_resource_path(resource['path'])
    if not local_path or not os.path.isfile(local_path):
        return render_template('errors/404.html'), 404

    filename = os.path.basename(local_path)
    response = send_file(
        local_path,
        mimetype='application/pdf',
        as_attachment=action == 'download',
        download_name=filename,
        conditional=False,
        etag=False,
    )
    content_disposition = content_disposition_header(action, filename)
    if content_disposition:
        response.headers['Content-Disposition'] = content_disposition
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


def send_inline_lesson_pdf(lesson):
    local_path = static_resource_path(lesson.get('url'))
    if not local_path or not os.path.isfile(local_path):
        return render_template('errors/404.html'), 404

    response = send_file(
        local_path,
        mimetype='application/pdf',
        as_attachment=False,
        download_name=os.path.basename(local_path),
        conditional=True,
    )
    response.headers['Cache-Control'] = 'private, max-age=300'
    return response


def current_username():
    return session.get('username')


def find_by_id(items, item_id):
    item_id = str(item_id)
    return next((item for item in items if str(item.get('id')) == item_id), None)


def exercise_response_values(form):
    values = {}
    prefix = 'response_'
    for key, value in form.items():
        if key.startswith(prefix):
            values[key[len(prefix):]] = value
    return values


def exercise_timer_values(form):
    if 'timer_duration_seconds' not in form:
        return None
    return {
        'duration_seconds': form.get('timer_duration_seconds'),
        'timer_enabled': form.get('timer_enabled'),
        'timer_paused': form.get('timer_paused'),
    }


def exercise_titles_by_id():
    titles = {
        str(exercise.get('id')): exercise.get('title')
        for exercise in load_exercise_catalogue().get('exercises', [])
    }
    for bank_path in exercise_bank_paths():
        data = load_json_file(bank_path, {})
        for exercise in data.get('exercises', []):
            if isinstance(exercise, dict) and exercise.get('id'):
                titles.setdefault(str(exercise.get('id')), exercise.get('title'))
        for exercise in data.get('retired_exercises', []):
            if isinstance(exercise, dict) and exercise.get('id'):
                titles.setdefault(str(exercise.get('id')), exercise.get('title'))
    return titles


def active_exercise_ids():
    return {
        str(exercise.get('id'))
        for exercise in load_exercise_catalogue().get('exercises', [])
        if exercise.get('id')
    }


def exercise_time(exercise):
    return exercise.get('estimated_time_min') or exercise.get('estimated_minutes')


def exercise_type(exercise):
    value = exercise.get('exercise_type') or exercise.get('family')
    labels = {
        'units': 'Analisis dimensional',
        'vectors': 'Vectores',
        'measurement': 'Medida y error',
        'calculus_graphs': 'Calculo y graficas',
    }
    return labels.get(value, value or exercise.get('concept') or exercise.get('topic'))


def exercise_status_filter(summary):
    return summary.get('status', 'new')


def exercise_filter_options(exercises):
    return {
        'courses': sorted({exercise.get('course') for exercise in exercises if exercise.get('course')}),
        'topics': sorted({exercise.get('topic') for exercise in exercises if exercise.get('topic')}),
        'types': sorted({exercise_type(exercise) for exercise in exercises if exercise_type(exercise)}),
        'difficulties': sorted({str(exercise.get('difficulty')) for exercise in exercises if exercise.get('difficulty')}),
        'statuses': [
            ('new', 'Nuevo'),
            ('started', 'En progreso'),
            ('completed', 'Completado'),
        ],
    }


def selected_exercise_filters(args):
    return {
        'course': args.get('course', '').strip(),
        'topic': args.get('topic', '').strip(),
        'type': args.get('type', '').strip(),
        'difficulty': args.get('difficulty', '').strip(),
        'status': args.get('status', '').strip(),
        'q': args.get('q', '').strip(),
    }


def filter_exercises(exercises, attempt_summaries, filters):
    filtered = []
    search = filters.get('q', '').casefold()

    for exercise in exercises:
        exercise_id = str(exercise.get('id'))
        summary = attempt_summaries.get(exercise_id, {'status': 'new'})

        if filters.get('course') and exercise.get('course') != filters['course']:
            continue
        if filters.get('topic') and exercise.get('topic') != filters['topic']:
            continue
        if filters.get('type') and exercise_type(exercise) != filters['type']:
            continue
        if filters.get('difficulty') and str(exercise.get('difficulty')) != filters['difficulty']:
            continue
        if filters.get('status') and exercise_status_filter(summary) != filters['status']:
            continue
        if search:
            searchable = ' '.join(
                str(value or '')
                for value in [
                    exercise.get('title'),
                    exercise.get('concept'),
                    exercise.get('subtype'),
                    exercise.get('topic'),
                    exercise_type(exercise),
                ]
            ).casefold()
            if search not in searchable:
                continue

        filtered.append(exercise)

    return filtered


def public_static_exists(path):
    local_path = static_resource_path(path)
    return bool(local_path and os.path.isfile(local_path))


def ensure_database_schema():
    inspector = inspect(db.engine)
    if 'exercise_attempts' in inspector.get_table_names():
        columns = {column['name'] for column in inspector.get_columns('exercise_attempts')}
        additions = {
            'active_duration_seconds': 'INTEGER',
            'timer_enabled': 'BOOLEAN NOT NULL DEFAULT 1',
            'timer_paused': 'BOOLEAN NOT NULL DEFAULT 0',
        }
        for column, ddl in additions.items():
            if column not in columns:
                db.session.execute(text(f'ALTER TABLE exercise_attempts ADD COLUMN {column} {ddl}'))
    if 'exercise_responses' in inspector.get_table_names():
        columns = {column['name'] for column in inspector.get_columns('exercise_responses')}
        if 'canonical_value' not in columns:
            db.session.execute(text('ALTER TABLE exercise_responses ADD COLUMN canonical_value TEXT'))
    db.session.commit()


def find_tracked_resource(resource_type, resource_id):
    if resource_type == 'topic_pdf':
        item = find_by_id(load_topics().get('topics', []), resource_id)
        object_type = 'topic'
    elif resource_type == 'lesson_pdf':
        item = find_by_id(load_lessons().get('lessons', []), resource_id)
        object_type = 'lesson'
    elif resource_type == 'summary_pdf':
        item = find_by_id(load_summaries().get('summaries', []), resource_id)
        object_type = 'summary'
    elif resource_type == 'exam_pdf':
        item = find_by_id(load_exams().get('exams', []), resource_id)
        object_type = 'exam'
    elif resource_type in {'quiz_question_pdf', 'solution_pdf'}:
        quiz = find_by_id(load_quizzes().get('quizzes', []), resource_id)
        if not quiz:
            return None

        pdf_key = 'solutions' if resource_type == 'solution_pdf' else 'questions'
        item = {
            'id': quiz.get('id'),
            'title': quiz.get('title'),
            'url': quiz.get('pdfs', {}).get(pdf_key),
        }
        object_type = 'quiz'
    elif resource_type == 'exercise_solution_pdf':
        exercise = find_by_id(load_exercise_catalogue().get('exercises', []), resource_id)
        if not exercise:
            return None
        item = {
            'id': exercise.get('id'),
            'title': exercise.get('title'),
            'url': exercise.get('solution_pdf'),
        }
        object_type = 'exercise'
    else:
        return None

    if not item or not item.get('url'):
        return None
    if resource_type == 'exercise_solution_pdf' and not public_static_exists(item.get('url')):
        return None

    return {
        'id': str(item.get('id')) if item.get('id') is not None else str(resource_id),
        'title': item.get('title'),
        'path': item.get('url'),
        'object_type': object_type,
    }


def store_quiz_start_time(quiz_id):
    quiz_id = str(quiz_id)
    quiz_start_times = session.get('quiz_start_times', {})
    quiz_start_times[quiz_id] = datetime.utcnow().isoformat()
    session['quiz_start_times'] = quiz_start_times


def pop_quiz_start_time(quiz_id):
    quiz_id = str(quiz_id)
    quiz_start_times = session.get('quiz_start_times', {})
    start_value = quiz_start_times.pop(quiz_id, None)
    session['quiz_start_times'] = quiz_start_times

    if not start_value:
        return None, None

    try:
        started_at = datetime.fromisoformat(start_value)
    except ValueError:
        return None, None

    duration_seconds = max(0, int((datetime.utcnow() - started_at).total_seconds()))
    return started_at, duration_seconds


@app.context_processor
def inject_layout_context():
    return {
        'asset_url': asset_url,
        'nav_items': NAV_ITEMS,
        'public_static_exists': public_static_exists,
        'format_duration': format_duration,
        'attempt_correction_summary': attempt_correction_summary,
    }


@app.cli.command('init-db')
def init_db_command():
    with app.app_context():
        db.create_all()
        ensure_database_schema()
    database_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if database_uri.startswith('sqlite:///') and database_uri.endswith('web_clases_rocedg.sqlite'):
        database_location = 'instance/web_clases_rocedg.sqlite'
    else:
        database_location = 'configured DATABASE_URL'
    click.echo(f"Database tables created at {database_location}")


@app.cli.command('regrade-exercise-attempts')
@click.option('--apply', 'apply_changes', is_flag=True, help='Persist changed grading results. Omit for dry run.')
def regrade_exercise_attempts_command(apply_changes):
    with app.app_context():
        db.create_all()
        ensure_database_schema()
        exercises = {
            str(exercise.get('id')): exercise
            for exercise in load_exercise_catalogue().get('exercises', [])
            if exercise.get('id')
        }
        result = regrade_submitted_attempts(exercises, dry_run=not apply_changes)
    mode = 'applied' if apply_changes else 'dry run'
    click.echo(
        f"Regrade {mode}: checked {result['attempts_checked']} attempts; "
        f"{result['responses_changed']} responses would change."
    )


@app.route('/')
def home():
    topics_data = load_topics()
    quiz_data = load_quizzes()
    exams_data = load_exams()
    summaries_data = load_summaries()
    stats = {
        'topics': len(topics_data['topics']),
        'quizzes': len(quiz_data['quizzes']),
        'exams': len(exams_data['exams']),
        'summaries': len(summaries_data['summaries'])
    }

    return render_template(
        'home.html',
        featured_quizzes=quiz_data['quizzes'][:3],
        recent_topics=topics_data['topics'][-3:],
        stats=stats
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in USERS and USERS[username][0] == password:
            session['username'] = username
            session['role'] = USERS[username][1]
            return redirect(url_for('home'))
        return render_template('login.html', error='Credenciales incorrectas')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/topics')
@login_required
def topics():
    lessons_data = load_lessons()
    y1_lessons = [lesson for lesson in lessons_data['lessons'] if lesson.get('year') == 'y1']
    record_activity_event(
        current_username(),
        'topics_page_view',
        'page',
        object_id='topics',
        object_title='Apuntes',
    )
    return render_template(
        'user/topics.html',
        lessons=y1_lessons
    )


@app.route('/lesson/<lesson_id>')
@login_required
def lesson_viewer(lesson_id):
    lessons = load_lessons().get('lessons', [])
    lesson = find_by_id(lessons, lesson_id)
    if not lesson or not lesson.get('url'):
        return render_template('errors/404.html'), 404

    lesson_id = str(lesson.get('id')) if lesson.get('id') is not None else str(lesson_id)
    record_activity_event(
        current_username(),
        'lesson_viewed',
        'lesson',
        object_id=lesson_id,
        object_title=lesson.get('title'),
        metadata={'source': 'lesson_viewer'},
    )

    return render_template(
        'user/lesson_viewer.html',
        lesson=lesson,
        available_lessons=[item for item in lessons if item.get('year') == lesson.get('year')],
        pdf_url=url_for('lesson_pdf_source', lesson_id=lesson_id),
        open_url=url_for(
            'tracked_resource',
            resource_type='lesson_pdf',
            resource_id=lesson_id,
            action='open',
        ),
        download_url=url_for(
            'tracked_resource',
            resource_type='lesson_pdf',
            resource_id=lesson_id,
            action='download',
        ),
    )


@app.route('/lesson/<lesson_id>/pdf-source')
@login_required
def lesson_pdf_source(lesson_id):
    lesson = find_by_id(load_lessons().get('lessons', []), lesson_id)
    if not lesson or not lesson.get('url'):
        return render_template('errors/404.html'), 404

    return send_inline_lesson_pdf(lesson)


@app.route('/homework')
@login_required
def homework():
    quiz_data = load_quizzes()
    exercises = load_exercise_catalogue().get('exercises', [])
    attempt_summaries = get_catalogue_attempt_summaries(current_username(), exercises)
    filters = selected_exercise_filters(request.args)
    filtered_exercises = filter_exercises(exercises, attempt_summaries, filters)
    return render_template(
        'user/homework.html',
        quizzes=quiz_data['quizzes'],
        exercises=filtered_exercises,
        exercise_count=len(exercises),
        attempt_summaries=attempt_summaries,
        filter_options=exercise_filter_options(exercises),
        selected_filters=filters,
        has_active_filters=any(filters.values()),
        exercise_time=exercise_time,
        exercise_type=exercise_type,
    )


@app.route('/exercise/<exercise_id>')
@login_required
def exercise_detail(exercise_id):
    exercise = find_by_id(load_exercise_catalogue().get('exercises', []), exercise_id)
    if not exercise:
        return render_template('errors/404.html'), 404

    attempt = latest_started_attempt(current_username(), exercise)
    if attempt:
        return redirect(url_for('exercise_attempt_detail', exercise_id=exercise_id, attempt_id=attempt.id))

    return render_template(
        'user/exercise_detail.html',
        exercise=exercise,
        attempt=attempt,
        fields=response_fields(exercise),
        responses=response_map(attempt) if attempt else {},
        field_results={},
        next_exercise=None,
        next_attempt_summary=None,
        solution_pdf_available=public_static_exists(exercise.get('solution_pdf')),
        exercise_time=exercise_time,
        exercise_type=exercise_type,
    )


@app.route('/exercise/<exercise_id>/start', methods=['POST'])
@login_required
def start_exercise_attempt(exercise_id):
    exercise = find_by_id(load_exercise_catalogue().get('exercises', []), exercise_id)
    if not exercise:
        return render_template('errors/404.html'), 404

    attempt, _ = start_or_resume_attempt(current_username(), exercise)
    return redirect(url_for('exercise_attempt_detail', exercise_id=exercise_id, attempt_id=attempt.id))


@app.route('/exercise/<exercise_id>/attempt/<int:attempt_id>')
@login_required
def exercise_attempt_detail(exercise_id, attempt_id):
    exercises = load_exercise_catalogue().get('exercises', [])
    exercise = find_by_id(exercises, exercise_id)
    if not exercise:
        return render_template('errors/404.html'), 404

    try:
        attempt = get_owned_attempt(current_username(), attempt_id)
    except ExerciseAttemptForbidden:
        return render_template('errors/403.html'), 403
    except ExerciseAttemptError:
        return render_template('errors/404.html'), 404

    if attempt.exercise_id != str(exercise.get('id')):
        return render_template('errors/404.html'), 404

    next_exercise = next_exercise_after(exercise, exercises) if attempt.status != 'started' else None
    next_summary = None
    if next_exercise:
        next_summary = get_catalogue_attempt_summaries(current_username(), [next_exercise]).get(str(next_exercise.get('id')))

    return render_template(
        'user/exercise_detail.html',
        exercise=exercise,
        attempt=attempt,
        fields=response_fields(exercise),
        responses=response_map(attempt),
        field_results=field_map(exercise),
        next_exercise=next_exercise,
        next_attempt_summary=next_summary,
        solution_pdf_available=public_static_exists(exercise.get('solution_pdf')),
        exercise_time=exercise_time,
        exercise_type=exercise_type,
    )


@app.route('/exercise/<exercise_id>/attempt/<int:attempt_id>/draft', methods=['POST'])
@login_required
def save_exercise_draft(exercise_id, attempt_id):
    exercise = find_by_id(load_exercise_catalogue().get('exercises', []), exercise_id)
    if not exercise:
        return render_template('errors/404.html'), 404

    try:
        timer_payload = exercise_timer_values(request.form)
        if timer_payload:
            sync_attempt_timer(
                current_username(),
                attempt_id,
                timer_payload['duration_seconds'],
                timer_payload.get('timer_enabled'),
                timer_payload.get('timer_paused'),
            )
        save_draft(current_username(), attempt_id, exercise, exercise_response_values(request.form))
    except ExerciseAttemptForbidden:
        return render_template('errors/403.html'), 403
    except ExerciseAttemptError:
        return render_template('errors/404.html'), 404

    return redirect(url_for('exercise_attempt_detail', exercise_id=exercise_id, attempt_id=attempt_id, saved='1'))


@app.route('/exercise/<exercise_id>/attempt/<int:attempt_id>/submit', methods=['POST'])
@login_required
def submit_exercise_attempt(exercise_id, attempt_id):
    exercise = find_by_id(load_exercise_catalogue().get('exercises', []), exercise_id)
    if not exercise:
        return render_template('errors/404.html'), 404

    try:
        values = exercise_response_values(request.form)
        timer_payload = exercise_timer_values(request.form)
        if timer_payload:
            values['_timer'] = timer_payload
        submit_attempt(current_username(), attempt_id, exercise, values)
    except ExerciseAttemptForbidden:
        return render_template('errors/403.html'), 403
    except ExerciseAttemptError:
        return render_template('errors/404.html'), 404

    return redirect(url_for('exercise_attempt_detail', exercise_id=exercise_id, attempt_id=attempt_id, submitted='1'))


@app.route('/exercise/<exercise_id>/attempt/<int:attempt_id>/timer', methods=['POST'])
@login_required
def sync_exercise_attempt_timer(exercise_id, attempt_id):
    exercise = find_by_id(load_exercise_catalogue().get('exercises', []), exercise_id)
    if not exercise:
        return jsonify({'ok': False, 'error': 'not_found'}), 404

    try:
        attempt = get_owned_attempt(current_username(), attempt_id)
        if attempt.exercise_id != str(exercise.get('id')):
            return jsonify({'ok': False, 'error': 'not_found'}), 404
        payload = request.get_json(silent=True) or request.form
        sync_attempt_timer(
            current_username(),
            attempt_id,
            payload.get('duration_seconds'),
            payload.get('timer_enabled'),
            payload.get('timer_paused'),
        )
    except ExerciseAttemptForbidden:
        return jsonify({'ok': False, 'error': 'forbidden'}), 403
    except ExerciseAttemptError:
        return jsonify({'ok': False, 'error': 'invalid'}), 400

    return jsonify({'ok': True})


@app.route('/practice/history')
@login_required
def exercise_attempt_history():
    attempts = get_student_attempt_history(current_username())
    return render_template(
        'user/exercise_history.html',
        attempts=attempts,
        exercise_titles=exercise_titles_by_id(),
        active_exercise_ids=active_exercise_ids(),
    )


@app.route('/quiz/<quiz_id>')
@login_required
def take_quiz(quiz_id):
    try:
        quiz_id_str = str(quiz_id)
        quiz_data = load_quizzes()
        quiz = next((q for q in quiz_data['quizzes'] if str(q.get('id')) == quiz_id_str), None)

        if not quiz:
            return render_template(
                'errors/404.html',
                message=f"Quiz ID {quiz_id} no encontrado"
            ), 404

        required_fields = ['id', 'title', 'question_count', 'correct_answers', 'pdfs']
        for field in required_fields:
            if field not in quiz:
                return render_template(
                    'errors/500.html',
                    error=f"Campo requerido faltante: {field}"
                ), 500

        questions_pdf = quiz['pdfs'].get('questions')
        if questions_pdf and not os.path.exists(os.path.join(BASE_DIR, questions_pdf)):
            return render_template(
                'errors/404.html',
                message='Archivo PDF de preguntas no encontrado'
            ), 404

        store_quiz_start_time(quiz_id_str)
        record_activity_event(
            current_username(),
            'quiz_started',
            'quiz',
            object_id=quiz_id_str,
            object_title=quiz['title'],
        )

        return render_template('user/quiz.html', quiz=quiz)
    except Exception as e:
        print(f"Error en take_quiz: {str(e)}")
        return render_template('errors/500.html', error=str(e)), 500


@app.route('/submit-quiz/<quiz_id>', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz_id_str = str(quiz_id)
    quiz_data = load_quizzes()
    quiz = next((q for q in quiz_data['quizzes'] if str(q.get('id')) == quiz_id_str), None)

    if not quiz:
        return render_template('errors/404.html'), 404

    user_answers = []
    correct_count = 0

    for q_num in range(1, quiz['question_count'] + 1):
        user_answer = request.form.get(f'answer_{q_num}', '')
        correct_answer = quiz['correct_answers'][q_num - 1]
        is_correct = user_answer == correct_answer

        if is_correct:
            correct_count += 1

        user_answers.append({
            'question_num': q_num,
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct
        })

    score_percentage = (correct_count / quiz['question_count']) * 100
    started_at, duration_seconds = pop_quiz_start_time(quiz_id_str)
    attempt = record_quiz_attempt(
        current_username(),
        quiz_id_str,
        quiz_title=quiz['title'],
        score=round(score_percentage),
        total_questions=quiz['question_count'],
        correct_answers=correct_count,
        percentage=score_percentage,
        started_at=started_at,
        duration_seconds=duration_seconds,
        metadata={'user_answers': user_answers},
    )
    record_activity_event(
        current_username(),
        'quiz_submitted',
        'quiz',
        object_id=quiz_id_str,
        object_title=quiz['title'],
        metadata={
            'attempt_id': attempt.id if attempt else None,
            'correct_answers': correct_count,
            'total_questions': quiz['question_count'],
            'percentage': score_percentage,
        },
        duration_seconds=duration_seconds,
    )

    session['quiz_results'] = {
        'quiz_id': quiz['id'],
        'quiz_title': quiz['title'],
        'user_answers': user_answers,
        'score': score_percentage,
        'correct_count': correct_count,
        'question_count': quiz['question_count'],
        'solutions_pdf': quiz['pdfs']['solutions'],
        'attempt_id': attempt.id if attempt else None
    }

    return redirect(url_for('quiz_results'))


@app.route('/quiz-results')
@login_required
def quiz_results():
    if 'quiz_results' not in session:
        return redirect(url_for('homework'))

    return render_template('user/quiz_results.html', results=session['quiz_results'])


@app.route('/resource/<resource_type>/<resource_id>/<action>')
def tracked_resource(resource_type, resource_id, action):
    if action not in {'open', 'download'}:
        return render_template('errors/404.html'), 404

    resource = find_tracked_resource(resource_type, resource_id)
    if not resource:
        return render_template('errors/404.html'), 404

    username = current_username()
    if username:
        record_resource_access(
            username,
            resource_type,
            action,
            resource_id=resource['id'],
            resource_title=resource['title'],
            path=resource['path'],
        )

        if resource_type == 'topic_pdf':
            mark_topic_opened(username, resource['id'], resource['title'])
            event_type = 'topic_view' if action == 'open' else 'resource_download'
        elif resource_type == 'solution_pdf' and action == 'open':
            event_type = 'solution_viewed'
        else:
            event_type = 'resource_open' if action == 'open' else 'resource_download'

        record_activity_event(
            username,
            event_type,
            resource['object_type'],
            object_id=resource['id'],
            object_title=resource['title'],
            metadata={'resource_type': resource_type, 'action': action},
        )

    if resource['path'].lower().endswith('.pdf'):
        return send_tracked_pdf(resource, action)

    return redirect(asset_url(resource['path']))


@app.route('/progress')
@login_required
def progress():
    snapshot = get_user_activity_snapshot(current_username())
    return render_template('user/progress.html', snapshot=snapshot)


@app.route('/miscellaneous')
@login_required
def miscellaneous():
    summaries_data = load_summaries()
    y1_summaries = [s for s in summaries_data['summaries'] if s.get('year') == 'y1']
    y2_summaries = [s for s in summaries_data['summaries'] if s.get('year') == 'y2']
    return render_template(
        'user/miscellaneous.html',
        y1_summaries=y1_summaries,
        y2_summaries=y2_summaries
    )


@app.route('/exams')
def exams():
    exams_data = load_exams()
    y1_exams = [e for e in exams_data['exams'] if e.get('year') == 'y1']
    y2_exams = [e for e in exams_data['exams'] if e.get('year') == 'y2']
    return render_template('user/exams.html', y1_exams=y1_exams, y2_exams=y2_exams)


@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    os.makedirs(content_path('exercises'), exist_ok=True)
    app.run(debug=True)
