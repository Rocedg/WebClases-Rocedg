from pathlib import Path

from app import app as flask_app
from database import db
from models import ExerciseAttempt, ExerciseResponse, UserActivityEvent
from services.exercise_attempt_service import (
    GRADE_CORRECT,
    GRADE_INCORRECT,
    GRADE_PENDING_REVIEW,
    attempt_correction_summary,
    normalize_numeric_value,
    parse_unit_expression,
    regrade_submitted_attempts,
    save_draft,
    start_or_resume_attempt,
    sync_attempt_timer,
    submit_attempt,
)


EXERCISE_ID = "t1_r_001"
EXERCISE_TYPE_KEY = "1bach:t1:r"


def login(client, username="Guest"):
    password = "studentpass" if username == "Guest" else "fisica2026"
    return client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )


def sample_exercise():
    return {
        "id": "sample_mixed_001",
        "version": 1,
        "title": "Sample mixed exercise",
        "interactions": [
            {
                "id": "choice",
                "type": "single_choice",
                "correct_option_id": "a",
                "feedback_correct": "Bien",
                "feedback_incorrect": "Revisa",
            },
            {
                "id": "number",
                "type": "numeric",
                "expected_value": 8.66,
                "tolerance": 0.01,
            },
            {
                "id": "reasoning",
                "type": "short_text",
            },
        ],
    }


def test_opening_exercise_without_start_does_not_create_attempt():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get(f"/exercise/{EXERCISE_ID}")

    assert response.status_code == 200
    with flask_app.app_context():
        assert ExerciseAttempt.query.count() == 0


def test_starting_exercise_creates_attempt_and_event():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.post(f"/exercise/{EXERCISE_ID}/start", follow_redirects=False)

    assert response.status_code == 302
    with flask_app.app_context():
        attempt = ExerciseAttempt.query.one()
        assert attempt.username == "Guest"
        assert attempt.exercise_id == EXERCISE_ID
        assert attempt.exercise_version == 1
        assert attempt.status == "started"
        assert UserActivityEvent.query.filter_by(event_type="exercise_started").count() == 1


def test_reopening_started_exercise_resumes_same_draft():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.post(f"/exercise/{EXERCISE_ID}/start")

    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.one().id

    response = client.get(f"/exercise/{EXERCISE_ID}", follow_redirects=False)

    assert response.status_code == 302
    assert f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}" in response.headers["Location"]
    with flask_app.app_context():
        assert ExerciseAttempt.query.count() == 1


def test_homework_new_exercise_cta_does_not_create_attempt_before_click():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    response = client.get("/homework", query_string={"type": EXERCISE_TYPE_KEY})

    assert response.status_code == 200
    assert b"Empezar ejercicio" in response.data
    assert f"/exercise/{EXERCISE_ID}/start".encode() in response.data
    with flask_app.app_context():
        assert ExerciseAttempt.query.count() == 0


def test_homework_landing_groups_real_exercise_types_with_catalogue_metrics():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    landing = client.get("/homework")

    assert landing.status_code == 200
    assert "Referencia y posición".encode("utf-8") in landing.data
    assert "Dificultad media".encode("utf-8") in landing.data
    assert b"Tiempo total" in landing.data
    assert b"type=1bach:t1:r" in landing.data
    assert b">r<" not in landing.data

    practice = client.get("/homework", query_string={"type": "1bach:t1:r"})
    assert practice.status_code == 200
    assert b"t1_r_001" in practice.data
    assert b"Empezar ejercicio" in practice.data
    assert b"expected_value" not in practice.data


def test_clicking_new_exercise_start_creates_exactly_one_attempt():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    first = client.post(f"/exercise/{EXERCISE_ID}/start")
    second = client.post(f"/exercise/{EXERCISE_ID}/start")

    assert first.status_code == 302
    assert second.status_code == 302
    with flask_app.app_context():
        assert ExerciseAttempt.query.count() == 1


def test_started_exercise_is_shown_as_continue_and_reopens_attempt():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.post(f"/exercise/{EXERCISE_ID}/start")
    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.one().id

    response = client.get("/homework", query_string={"type": EXERCISE_TYPE_KEY})

    assert response.status_code == 200
    assert b"Continuar ejercicio" in response.data
    assert f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}".encode() in response.data


def test_draft_response_persists_and_can_be_updated_with_raw_and_normalized_numeric():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.post(f"/exercise/{EXERCISE_ID}/start")

    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.one().id

    client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/draft",
        data={"response_xa": " -300,0 "},
    )
    client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/draft",
        data={"response_xa": "-299"},
    )

    with flask_app.app_context():
        response = ExerciseResponse.query.filter_by(field_id="xa").one()
        assert response.raw_value == "-299"
        assert response.normalized_value == "-299"
        assert response.grading_status == "ungraded"


def test_decimal_comma_normalization():
    assert normalize_numeric_value("8,66") == "8.66"
    assert normalize_numeric_value(" 8.66 ") == "8.66"
    assert normalize_numeric_value("8,66 V") is None


def test_submission_grades_supported_fields_and_marks_open_pending_review():
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", sample_exercise())
        submit_attempt(
            "Guest",
            attempt.id,
            sample_exercise(),
            {"choice": "a", "number": "8,665", "reasoning": "Porque si."},
        )

        saved = db.session.get(ExerciseAttempt, attempt.id)
        responses = {response.field_id: response for response in saved.responses}

        assert saved.status == "submitted"
        assert saved.submitted_at is not None
        assert saved.score == 2
        assert saved.max_score == 2
        assert responses["choice"].grading_status == GRADE_CORRECT
        assert responses["number"].grading_status == GRADE_CORRECT
        assert responses["number"].normalized_value == "8.665"
        assert responses["reasoning"].grading_status == GRADE_PENDING_REVIEW


def test_single_choice_incorrect_and_numeric_invalid_do_not_crash():
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", sample_exercise())
        submit_attempt(
            "Guest",
            attempt.id,
            sample_exercise(),
            {"choice": "b", "number": "no es numero", "reasoning": ""},
        )

        responses = {response.field_id: response for response in attempt.responses}
        assert responses["choice"].grading_status == GRADE_INCORRECT
        assert responses["number"].grading_status == GRADE_PENDING_REVIEW
        assert responses["number"].normalized_value is None


def test_unit_expression_parser_semantic_equivalence_and_case_sensitivity():
    pairs = [
        ("N*m^2/kg^2", "N m^2 kg^-2"),
        ("m^3/(kg*s^2)", "m^3 kg^-1 s^-2"),
        ("N·m²·kg⁻¹", "N*m^2/kg"),
        ("N m^2", "N*m^2"),
    ]
    for left, right in pairs:
        parsed_left = parse_unit_expression(left)
        parsed_right = parse_unit_expression(right)
        assert parsed_left.ok
        assert parsed_right.ok
        assert parsed_left.dimensions == parsed_right.dimensions
        assert parsed_left.scale == parsed_right.scale

    assert parse_unit_expression("N").ok
    assert not parse_unit_expression("n").ok
    assert parse_unit_expression("kg m^-3").scale != parse_unit_expression("g cm^-3").scale
    assert parse_unit_expression("kg apples").ok is False


def test_unit_parser_does_not_use_unrestricted_eval():
    source = Path("services/exercise_attempt_service.py").read_text(encoding="utf-8")
    assert "eval(" not in source
    assert "exec(" not in source


def test_submitted_attempt_cannot_be_edited_and_new_start_creates_later_attempt():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.post(f"/exercise/{EXERCISE_ID}/start")

    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.one().id

    submit_response = client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/submit",
        data={"response_xa": "-300"},
    )
    assert submit_response.status_code == 302

    edit_response = client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/draft",
        data={"response_xa": "-299"},
    )
    assert edit_response.status_code == 403

    client.post(f"/exercise/{EXERCISE_ID}/start")
    with flask_app.app_context():
        assert ExerciseAttempt.query.filter_by(username="Guest", exercise_id=EXERCISE_ID).count() == 2


def test_timer_persistence_and_submission_immutability():
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", sample_exercise())
        assert attempt.active_duration_seconds == 0
        assert attempt.timer_enabled is True
        sync_attempt_timer("Guest", attempt.id, 42, timer_enabled=True, timer_paused=True)
        assert db.session.get(ExerciseAttempt, attempt.id).active_duration_seconds == 42
        submit_attempt("Guest", attempt.id, sample_exercise(), {"choice": "a", "number": "8.66", "reasoning": ""})
        try:
            sync_attempt_timer("Guest", attempt.id, 43)
        except Exception as exc:
            assert exc.__class__.__name__ == "ExerciseAttemptForbidden"
        else:
            raise AssertionError("submitted attempt accepted timer mutation")


def test_timer_endpoint_rejects_other_user_and_malformed_values():
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Paul", {**sample_exercise(), "id": EXERCISE_ID})
        attempt_id = attempt.id

    client = flask_app.test_client()
    assert login(client, "Guest").status_code == 302
    forbidden = client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/timer",
        json={"duration_seconds": 10, "timer_enabled": True, "timer_paused": False},
    )
    assert forbidden.status_code == 403

    with flask_app.app_context():
        guest_attempt, _ = start_or_resume_attempt("Guest", {**sample_exercise(), "id": EXERCISE_ID})
        guest_attempt_id = guest_attempt.id

    malformed = client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{guest_attempt_id}/timer",
        json={"duration_seconds": -1},
    )
    assert malformed.status_code == 400


def test_homework_filter_by_course_topic_difficulty_status_and_invalid_value():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.post(f"/exercise/{EXERCISE_ID}/start")

    course = client.get("/homework?course=1bach")
    topic = client.get("/homework?topic=t1")
    difficulty = client.get("/homework?difficulty=2")
    status = client.get("/homework?status=started")
    invalid = client.get("/homework?course=nope")

    assert course.status_code == 200
    assert topic.status_code == 200
    assert difficulty.status_code == 200
    assert status.status_code == 200
    assert invalid.status_code == 200
    assert EXERCISE_ID.encode() in course.data
    assert EXERCISE_ID.encode() in topic.data
    assert EXERCISE_ID.encode() in difficulty.data
    assert b"Continuar ejercicio" in status.data
    assert b"No encontramos ejercicios con estos filtros." in invalid.data


def test_homework_card_states_and_completed_cta():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    new_page = client.get("/homework", query_string={"type": EXERCISE_TYPE_KEY})
    assert b"exercise-card-new" in new_page.data
    assert b"Nuevo" in new_page.data

    client.post(f"/exercise/{EXERCISE_ID}/start")
    started_page = client.get("/homework", query_string={"type": EXERCISE_TYPE_KEY})
    assert b"exercise-card-started" in started_page.data
    assert b"En progreso" in started_page.data

    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.filter_by(exercise_id=EXERCISE_ID).one().id
    client.post(f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/submit", data={"response_xa": "-300"})
    completed_page = client.get("/homework", query_string={"type": EXERCISE_TYPE_KEY})
    assert b"exercise-card-completed" in completed_page.data
    assert b"Completado" in completed_page.data
    assert b"Practicar de nuevo" in completed_page.data


def test_submitted_retry_creates_new_attempt_and_guided_solution_is_submission_only():
    client = flask_app.test_client()
    assert login(client).status_code == 302
    client.post(f"/exercise/{EXERCISE_ID}/start")
    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.one().id

    active = client.get(f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}")
    assert b"Ver solucion guiada" not in active.data

    submitted = client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/submit",
        data={"response_xa": "-300", "response_xb": "500", "response_dx": "-800", "response_d": "800"},
        follow_redirects=True,
    )
    assert submitted.status_code == 200
    assert b"Ver solucion guiada" in submitted.data
    assert "Con origen".encode("utf-8") in submitted.data

    client.post(f"/exercise/{EXERCISE_ID}/start")
    with flask_app.app_context():
        assert ExerciseAttempt.query.filter_by(username="Guest", exercise_id=EXERCISE_ID).count() == 2


def test_next_exercise_action_is_deterministic_and_hidden_at_topic_end():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    first_id = "t1_r_001"
    next_id = "t1_r_002"
    last_id = "t6_a_012"

    client.post(f"/exercise/{first_id}/start")
    with flask_app.app_context():
        first_attempt_id = ExerciseAttempt.query.filter_by(exercise_id=first_id).one().id
    first_submitted = client.post(
        f"/exercise/{first_id}/attempt/{first_attempt_id}/submit",
        data={"response_xa": "-300"},
        follow_redirects=True,
    )
    assert f"/exercise/{next_id}/start".encode() in first_submitted.data
    assert b"Siguiente ejercicio" in first_submitted.data

    client.post(f"/exercise/{last_id}/start")
    with flask_app.app_context():
        last_attempt_id = ExerciseAttempt.query.filter_by(exercise_id=last_id).one().id
    last_submitted = client.post(
        f"/exercise/{last_id}/attempt/{last_attempt_id}/submit",
        data={},
        follow_redirects=True,
    )
    assert b"Siguiente ejercicio" not in last_submitted.data


def test_mathjax_is_loaded_only_on_exercise_detail():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    detail = client.get(f"/exercise/{EXERCISE_ID}")
    homework = client.get("/homework")

    assert detail.status_code == 200
    assert b"tex-chtml.js" in detail.data
    config_url = b"/static/js/exercise-math.js"
    assert config_url in detail.data
    assert detail.data.index(config_url) < detail.data.index(b"tex-chtml.js")
    config = client.get(config_url.decode())
    assert config.status_code == 200
    assert b"inlineMath" in config.data
    assert config_url not in homework.data
    assert b"tex-chtml.js" not in homework.data


def test_student_pages_hide_internal_metadata_and_show_format_help():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    client.post("/exercise/t0_u_009/start")
    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.filter_by(exercise_id="t0_u_009").one().id
    active = client.get(f"/exercise/t0_u_009/attempt/{attempt_id}")

    assert active.status_code == 200
    assert b"short_text_plus_numeric" not in active.data
    assert b"Version" not in active.data
    assert b">unit_derived<" not in active.data
    assert "Unidad usando N".encode("utf-8") in active.data
    assert "Puedes usar espacios".encode("utf-8") in active.data

    submitted = client.post(
        f"/exercise/t0_u_009/attempt/{attempt_id}/submit",
        data={
            "response_unit_derived": "N*m^2/kg^2",
            "response_unit_base": "m^3/(kg*s^2)",
            "response_force_factor": "4/9",
        },
        follow_redirects=True,
    )
    assert submitted.status_code == 200
    assert b"Valor normalizado" not in submitted.data
    assert b"version" not in submitted.data.lower()


def test_history_contains_own_attempts_and_excludes_other_users():
    with flask_app.app_context():
        guest_attempt, _ = start_or_resume_attempt("Guest", sample_exercise())
        paul_attempt, _ = start_or_resume_attempt("Paul", {**sample_exercise(), "id": "sample_other_001"})
        guest_attempt_id = guest_attempt.id
        paul_attempt_id = paul_attempt.id

    client = flask_app.test_client()
    assert login(client).status_code == 302
    response = client.get("/practice/history")

    assert response.status_code == 200
    assert f"Intento #{guest_attempt_id}".encode() in response.data
    assert f"Intento #{paul_attempt_id}".encode() not in response.data


def test_direct_access_to_another_users_attempt_is_rejected():
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Paul", {"id": EXERCISE_ID, "version": 1, "title": "Owned"})
        attempt_id = attempt.id

    client = flask_app.test_client()
    assert login(client, "Guest").status_code == 302
    response = client.get(f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}")

    assert response.status_code == 403


def test_unknown_exercise_and_unknown_field_are_handled_cleanly():
    client = flask_app.test_client()
    assert login(client).status_code == 302

    assert client.get("/exercise/unknown").status_code == 404

    client.post(f"/exercise/{EXERCISE_ID}/start")
    with flask_app.app_context():
        attempt_id = ExerciseAttempt.query.one().id

    response = client.post(
        f"/exercise/{EXERCISE_ID}/attempt/{attempt_id}/draft",
        data={"response_not_a_real_field": "x"},
    )

    assert response.status_code == 404
    with flask_app.app_context():
        assert ExerciseResponse.query.count() == 0


def test_pending_score_is_provisional_and_regrading_is_idempotent():
    exercise = sample_exercise()
    with flask_app.app_context():
        attempt, _ = start_or_resume_attempt("Guest", exercise)
        submit_attempt("Guest", attempt.id, exercise, {"choice": "a", "number": "8.66", "reasoning": "texto"})
        summary = attempt_correction_summary(attempt)
        assert summary["correct"] == 2
        assert summary["pending"] == 1
        assert summary["provisional"] is True
        result1 = regrade_submitted_attempts({exercise["id"]: exercise}, dry_run=False)
        result2 = regrade_submitted_attempts({exercise["id"]: exercise}, dry_run=False)
        assert result1["attempts_checked"] == 1
        assert result2["responses_changed"] == 0
