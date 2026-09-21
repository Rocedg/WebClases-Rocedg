from app import app as flask_app
from database import db
from models import (
    UserActivityEvent,
    UserQuizAttempt,
    UserResourceAccess,
    UserStudyState,
    UserTopicProgress,
)
from services.activity_service import (
    mark_topic_opened,
    record_activity_event,
    record_quiz_attempt,
)


def login(client):
    return client.post(
        "/login",
        data={"username": "Guest", "password": "studentpass"},
        follow_redirects=False,
    )


def test_database_can_initialize_in_temporary_sqlite():
    with flask_app.app_context():
        db.create_all()
        assert UserActivityEvent.query.count() == 0


def test_record_activity_event_creates_row():
    with flask_app.app_context():
        record_activity_event(
            "Guest",
            "topic_view",
            "topic",
            object_id="1",
            object_title="Introduccion",
            metadata={"source": "test"},
        )

        event = UserActivityEvent.query.one()
        assert event.username == "Guest"
        assert event.event_type == "topic_view"
        assert event.metadata_json is not None


def test_mark_topic_opened_creates_and_updates_one_row():
    with flask_app.app_context():
        mark_topic_opened("Guest", "1", "Tema 1")
        mark_topic_opened("Guest", "1", "Tema 1")

        progress = UserTopicProgress.query.one()
        assert progress.username == "Guest"
        assert progress.topic_id == "1"
        assert progress.open_count == 2


def test_record_quiz_attempt_creates_row():
    with flask_app.app_context():
        record_quiz_attempt(
            "Guest",
            "1",
            quiz_title="Introduccion",
            score=80,
            total_questions=5,
            correct_answers=4,
            percentage=80.0,
            metadata={"answers": ["A", "B"]},
        )

        attempt = UserQuizAttempt.query.one()
        assert attempt.quiz_id == "1"
        assert attempt.correct_answers == 4
        assert attempt.percentage == 80.0


def test_reserved_quizzes_are_not_accessible_from_the_web():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    assert client.get("/topics").status_code == 200
    homework = client.get("/homework")
    assert homework.status_code == 200
    assert "Cuestionarios PDF".encode("utf-8") not in homework.data
    assert client.get("/quiz/1").status_code == 404
    assert client.post("/submit-quiz/1", data={"answer_1": "C"}).status_code == 404
    assert client.get("/quiz-results").status_code == 404
    assert client.get("/resource/quiz_question_pdf/1/open").status_code == 404
    assert client.get("/static/pdfs/quizzes/quiz1.questions.pdf").status_code == 404


def test_induction_exercises_are_not_in_the_public_catalogue():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    homework = client.get("/homework")

    assert homework.status_code == 200
    assert "Inducción electromagnética".encode("utf-8") not in homework.data
    assert client.get("/exercise/faraday_area_motional_001").status_code == 404


def test_tracked_resource_route_records_logged_in_access():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get("/resource/topic_pdf/1/open", follow_redirects=False)
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.headers["Content-Disposition"].startswith("inline")
    assert response.headers["Cache-Control"] == "no-store, max-age=0"

    with flask_app.app_context():
        assert UserResourceAccess.query.filter_by(
            username="Guest",
            resource_type="topic_pdf",
            action="open",
        ).count() == 1
        assert UserTopicProgress.query.filter_by(username="Guest", topic_id="1").count() == 1


def test_lesson_viewer_route_records_logged_in_lesson_view():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get("/lesson/T0-introduccion")

    assert response.status_code == 200
    assert b"/lesson/T0-introduccion/pdf-source" in response.data
    assert b"data-pdf-viewer" in response.data
    assert b"data-pdf-canvas" in response.data
    assert b"<object" not in response.data
    assert b"/resource/lesson_pdf/T0-introduccion/open" in response.data
    assert b"/resource/lesson_pdf/T0-introduccion/download" in response.data
    assert b"/homework?topic=t0" in response.data

    with flask_app.app_context():
        event = UserActivityEvent.query.filter_by(
            username="Guest",
            object_type="lesson",
            object_id="T0-introduccion",
            event_type="lesson_viewed",
        ).one()

        assert event.object_title == "T0 - Herramientas para empezar Física"
        state = UserStudyState.query.filter_by(username="Guest").one()
        assert state.last_lesson_id == "T0-introduccion"
        assert UserResourceAccess.query.count() == 0


def test_exercise_start_persists_last_exercise_topic_and_type():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.post("/exercise/t1_r_001/start")

    assert response.status_code == 302
    with flask_app.app_context():
        state = UserStudyState.query.filter_by(username="Guest").one()
        assert state.last_exercise_id == "t1_r_001"
        assert state.last_exercise_topic == "t1"
        assert state.last_exercise_topic_title.startswith("T1")
        assert state.last_exercise_type_title == "Referencia y posición"


def test_progress_uses_friendly_activity_labels_and_real_study_state():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.get("/lesson/T0-introduccion")
    client.post("/exercise/t1_r_001/start")

    response = client.get("/progress")

    assert response.status_code == 200
    assert "Último apunte".encode("utf-8") in response.data
    assert "Último tema de ejercicios".encode("utf-8") in response.data
    assert "Referencia y posición".encode("utf-8") in response.data
    assert b"lesson_viewed" not in response.data
    assert b"exercise_started" not in response.data


def test_invalid_lesson_viewer_route_returns_404_for_logged_in_user():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get("/lesson/invalid")

    assert response.status_code == 404


def test_lesson_pdf_source_serves_inline_without_resource_tracking():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get("/lesson/T0-introduccion/pdf-source")

    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.headers["Content-Disposition"].startswith("inline")
    assert response.data.startswith(b"%PDF")

    with flask_app.app_context():
        assert UserResourceAccess.query.count() == 0
        assert UserActivityEvent.query.count() == 0


def test_tracked_lesson_route_records_logged_in_access():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    open_response = client.get(
        "/resource/lesson_pdf/T0-introduccion/open",
        follow_redirects=False,
    )
    download_response = client.get(
        "/resource/lesson_pdf/T0-introduccion/download",
        follow_redirects=False,
    )

    assert open_response.status_code == 200
    assert open_response.mimetype == "application/pdf"
    assert open_response.headers["Content-Disposition"] == 'inline; filename="T0-introduccion.pdf"'
    assert open_response.headers["Cache-Control"] == "no-store, max-age=0"
    assert open_response.data.startswith(b"%PDF")

    assert download_response.status_code == 200
    assert download_response.mimetype == "application/pdf"
    assert download_response.headers["Content-Disposition"] == 'attachment; filename="T0-introduccion.pdf"'
    assert download_response.headers["Cache-Control"] == "no-store, max-age=0"
    assert download_response.data.startswith(b"%PDF")

    with flask_app.app_context():
        open_access = UserResourceAccess.query.filter_by(
            username="Guest",
            resource_type="lesson_pdf",
            resource_id="T0-introduccion",
            action="open",
        ).one()
        download_access = UserResourceAccess.query.filter_by(
            username="Guest",
            resource_type="lesson_pdf",
            resource_id="T0-introduccion",
            action="download",
        ).one()
        open_event = UserActivityEvent.query.filter_by(
            username="Guest",
            object_type="lesson",
            object_id="T0-introduccion",
            event_type="resource_open",
        ).one()
        download_event = UserActivityEvent.query.filter_by(
            username="Guest",
            object_type="lesson",
            object_id="T0-introduccion",
            event_type="resource_download",
        ).one()

        assert open_access.resource_title == "T0 - Herramientas para empezar Física"
        assert download_access.resource_title == "T0 - Herramientas para empezar Física"
        assert open_event.object_title == "T0 - Herramientas para empezar Física"
        assert download_event.object_title == "T0 - Herramientas para empezar Física"


def test_progress_page_requires_login_and_renders_for_user():
    client = flask_app.test_client()
    assert client.get("/progress").status_code == 302

    assert login(client).status_code == 302
    response = client.get("/progress")
    assert response.status_code == 200
