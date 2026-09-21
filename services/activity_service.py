import json
from datetime import datetime

from flask import current_app, has_app_context

from database import db
from models import (
    ExerciseAttempt,
    UserActivityEvent,
    UserQuizAttempt,
    UserResourceAccess,
    UserStudyState,
    UserTopicProgress,
)
from services.exercise_taxonomy import (
    exercise_topic_key,
    exercise_topic_title,
    exercise_type_key,
    exercise_type_title,
)


def _warn(message, error):
    if has_app_context():
        current_app.logger.warning("%s: %s", message, error)
    else:
        print(f"Warning: {message}: {error}")


def _metadata_to_json(metadata):
    if metadata is None:
        return None

    try:
        return json.dumps(metadata, ensure_ascii=False)
    except TypeError:
        return json.dumps({"unserializable_metadata": str(metadata)}, ensure_ascii=False)


def _commit_or_none(message):
    try:
        db.session.commit()
        return True
    except Exception as error:
        db.session.rollback()
        _warn(message, error)
        return False


def record_activity_event(
    username,
    event_type,
    object_type,
    object_id=None,
    object_title=None,
    metadata=None,
    duration_seconds=None,
):
    if not username:
        return None

    event = UserActivityEvent(
        username=username,
        event_type=event_type,
        object_type=object_type,
        object_id=str(object_id) if object_id is not None else None,
        object_title=object_title,
        metadata_json=_metadata_to_json(metadata),
        duration_seconds=duration_seconds,
    )
    db.session.add(event)

    if _commit_or_none("Activity event could not be recorded"):
        return event
    return None


def mark_topic_opened(username, topic_id, topic_title=None, last_page=None):
    if not username or topic_id is None:
        return None

    topic_id = str(topic_id)

    try:
        progress = UserTopicProgress.query.filter_by(
            username=username,
            topic_id=topic_id,
        ).one_or_none()

        if progress is None:
            progress = UserTopicProgress(
                username=username,
                topic_id=topic_id,
                topic_title=topic_title,
                last_page=last_page,
                last_opened_at=datetime.utcnow(),
                total_time_seconds=0,
                open_count=1,
            )
            db.session.add(progress)
        else:
            progress.topic_title = topic_title or progress.topic_title
            progress.last_page = last_page if last_page is not None else progress.last_page
            progress.last_opened_at = datetime.utcnow()
            progress.open_count = (progress.open_count or 0) + 1

        if _commit_or_none("Topic progress could not be recorded"):
            return progress
    except Exception as error:
        db.session.rollback()
        _warn("Topic progress could not be recorded", error)

    return None


def _study_state(username):
    state = UserStudyState.query.filter_by(username=username).one_or_none()
    if state is None:
        state = UserStudyState(username=username)
        db.session.add(state)
    return state


def mark_lesson_opened(username, lesson):
    if not username or not lesson or lesson.get("id") is None:
        return None
    try:
        state = _study_state(username)
        state.last_lesson_id = str(lesson["id"])
        state.last_lesson_title = lesson.get("title")
        state.last_lesson_at = datetime.utcnow()
        state.updated_at = state.last_lesson_at
        if _commit_or_none("Last lesson could not be recorded"):
            return state
    except Exception as error:
        db.session.rollback()
        _warn("Last lesson could not be recorded", error)
    return None


def mark_exercise_worked(username, exercise):
    if not username or not exercise or exercise.get("id") is None:
        return None
    try:
        state = _study_state(username)
        state.last_exercise_id = str(exercise["id"])
        state.last_exercise_title = exercise.get("title")
        state.last_exercise_topic = exercise_topic_key(exercise)
        state.last_exercise_topic_title = exercise_topic_title(exercise)
        state.last_exercise_type_key = exercise_type_key(exercise)
        state.last_exercise_type_title = exercise_type_title(exercise)
        state.last_exercise_at = datetime.utcnow()
        state.updated_at = state.last_exercise_at
        if _commit_or_none("Last exercise context could not be recorded"):
            return state
    except Exception as error:
        db.session.rollback()
        _warn("Last exercise context could not be recorded", error)
    return None


def record_resource_access(
    username,
    resource_type,
    action,
    resource_id=None,
    resource_title=None,
    path=None,
):
    if not username:
        return None

    access = UserResourceAccess(
        username=username,
        resource_type=resource_type,
        action=action,
        resource_id=str(resource_id) if resource_id is not None else None,
        resource_title=resource_title,
        path=path,
    )
    db.session.add(access)

    if _commit_or_none("Resource access could not be recorded"):
        return access
    return None


def record_quiz_attempt(
    username,
    quiz_id,
    quiz_title=None,
    score=None,
    total_questions=None,
    correct_answers=None,
    percentage=None,
    started_at=None,
    duration_seconds=None,
    metadata=None,
):
    if not username or quiz_id is None:
        return None

    attempt = UserQuizAttempt(
        username=username,
        quiz_id=str(quiz_id),
        quiz_title=quiz_title,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers,
        percentage=percentage,
        started_at=started_at,
        submitted_at=datetime.utcnow(),
        duration_seconds=duration_seconds,
        metadata_json=_metadata_to_json(metadata),
    )
    db.session.add(attempt)

    if _commit_or_none("Quiz attempt could not be recorded"):
        return attempt
    return None


def empty_activity_snapshot():
    return {
        "latest_topic": None,
        "study_state": None,
        "quiz_attempt_count": 0,
        "last_quiz_attempt": None,
        "recent_events": [],
        "exercise_attempt_count": 0,
        "completed_exercise_count": 0,
        "exercise_accuracy": None,
        "total_active_seconds": 0,
        "topic_progress": [],
        "visited_lessons": [],
    }


def _friendly_events(events):
    labels = {
        "lesson_viewed": ("Apunte consultado", "fa-book-open"),
        "resource_open": ("Material abierto", "fa-file-arrow-up"),
        "exercise_started": ("Ejercicio empezado", "fa-play"),
        "exercise_draft_saved": ("Ejercicio guardado", "fa-floppy-disk"),
        "exercise_submitted": ("Ejercicio corregido", "fa-circle-check"),
        "quiz_started": ("Cuestionario empezado", "fa-list-check"),
        "quiz_submitted": ("Cuestionario corregido", "fa-square-check"),
    }
    result = []
    for event in events:
        if event.event_type not in labels:
            continue
        label, icon = labels[event.event_type]
        result.append(
            {
                "label": label,
                "icon": icon,
                "title": event.object_title or "Material de estudio",
                "created_at": event.created_at,
                "duration_seconds": event.duration_seconds,
            }
        )
    return result


def _topic_progress(exercises, attempts):
    catalog = {}
    by_id = {}
    for exercise in exercises:
        exercise_id = str(exercise.get("id"))
        topic_key = exercise_topic_key(exercise)
        by_id[exercise_id] = exercise
        item = catalog.setdefault(
            topic_key,
            {"key": topic_key, "title": exercise_topic_title(exercise), "total": 0, "completed": 0,
             "attempted": 0, "active_seconds": 0, "score": 0.0, "max_score": 0.0},
        )
        item["total"] += 1

    attempted_ids = set()
    completed_ids = set()
    for attempt in attempts:
        exercise = by_id.get(attempt.exercise_id)
        if not exercise:
            continue
        item = catalog[exercise_topic_key(exercise)]
        attempted_ids.add((item["key"], attempt.exercise_id))
        item["active_seconds"] += attempt.active_duration_seconds or 0
        if attempt.status in {"submitted", "reviewed"}:
            completed_ids.add((item["key"], attempt.exercise_id))
            if attempt.score is not None and attempt.max_score:
                item["score"] += attempt.score
                item["max_score"] += attempt.max_score

    for item in catalog.values():
        item["attempted"] = sum(1 for topic, _ in attempted_ids if topic == item["key"])
        item["completed"] = sum(1 for topic, _ in completed_ids if topic == item["key"])
        item["completion_percentage"] = round(100 * item["completed"] / item["total"]) if item["total"] else 0
        item["accuracy"] = round(100 * item["score"] / item["max_score"]) if item["max_score"] else None
    return list(catalog.values())


def _visited_lessons(events):
    visits = {}
    for event in events:
        if event.object_type != "lesson" or event.event_type not in {"lesson_viewed", "resource_open"}:
            continue
        key = event.object_id or event.object_title
        item = visits.setdefault(
            key,
            {"id": event.object_id, "title": event.object_title or "Apunte", "visits": 0, "last_at": event.created_at},
        )
        item["visits"] += 1
        if event.created_at > item["last_at"]:
            item["last_at"] = event.created_at
    return sorted(visits.values(), key=lambda item: item["last_at"], reverse=True)


def _backfill_study_state(username, exercises, events, attempts):
    """Populate the continuation row once from genuine pre-existing activity."""
    latest_lesson = next(
        (
            event for event in events
            if event.object_type == "lesson" and event.event_type in {"lesson_viewed", "resource_open"}
        ),
        None,
    )
    by_id = {str(exercise.get("id")): exercise for exercise in exercises}
    latest_exercise_attempt = next((attempt for attempt in attempts if attempt.exercise_id in by_id), None)
    if latest_lesson is None and latest_exercise_attempt is None:
        return None

    state = _study_state(username)
    if latest_lesson:
        state.last_lesson_id = latest_lesson.object_id
        state.last_lesson_title = latest_lesson.object_title
        state.last_lesson_at = latest_lesson.created_at
    if latest_exercise_attempt:
        exercise = by_id[latest_exercise_attempt.exercise_id]
        state.last_exercise_id = latest_exercise_attempt.exercise_id
        state.last_exercise_title = exercise.get("title")
        state.last_exercise_topic = exercise_topic_key(exercise)
        state.last_exercise_topic_title = exercise_topic_title(exercise)
        state.last_exercise_type_key = exercise_type_key(exercise)
        state.last_exercise_type_title = exercise_type_title(exercise)
        state.last_exercise_at = latest_exercise_attempt.updated_at
    dates = [value for value in (state.last_lesson_at, state.last_exercise_at) if value]
    state.updated_at = max(dates) if dates else datetime.utcnow()
    if _commit_or_none("Study state could not be backfilled"):
        return state
    return None


def get_user_activity_snapshot(username, exercises=None, recent_limit=8):
    if not username:
        return empty_activity_snapshot()

    try:
        latest_topic = (
            UserTopicProgress.query.filter_by(username=username)
            .order_by(UserTopicProgress.last_opened_at.desc())
            .first()
        )
        quiz_attempt_count = UserQuizAttempt.query.filter_by(username=username).count()
        last_quiz_attempt = (
            UserQuizAttempt.query.filter_by(username=username)
            .order_by(UserQuizAttempt.submitted_at.desc())
            .first()
        )
        all_events = (
            UserActivityEvent.query.filter_by(username=username)
            .order_by(UserActivityEvent.created_at.desc())
            .all()
        )
        attempts = (
            ExerciseAttempt.query.filter_by(username=username)
            .order_by(ExerciseAttempt.updated_at.desc(), ExerciseAttempt.id.desc())
            .all()
        )
        study_state = UserStudyState.query.filter_by(username=username).one_or_none()
        if study_state is None:
            study_state = _backfill_study_state(username, exercises or [], all_events, attempts)
        completed_ids = {
            attempt.exercise_id for attempt in attempts if attempt.status in {"submitted", "reviewed"}
        }
        score = sum(attempt.score or 0 for attempt in attempts if attempt.status in {"submitted", "reviewed"})
        max_score = sum(attempt.max_score or 0 for attempt in attempts if attempt.status in {"submitted", "reviewed"})

        return {
            "latest_topic": latest_topic,
            "study_state": study_state,
            "quiz_attempt_count": quiz_attempt_count,
            "last_quiz_attempt": last_quiz_attempt,
            "recent_events": _friendly_events(all_events)[:recent_limit],
            "exercise_attempt_count": len(attempts),
            "completed_exercise_count": len(completed_ids),
            "exercise_accuracy": round(100 * score / max_score) if max_score else None,
            "total_active_seconds": sum(attempt.active_duration_seconds or 0 for attempt in attempts),
            "topic_progress": _topic_progress(exercises or [], attempts),
            "visited_lessons": _visited_lessons(all_events),
        }
    except Exception as error:
        db.session.rollback()
        _warn("Activity snapshot could not be loaded", error)
        return empty_activity_snapshot()
