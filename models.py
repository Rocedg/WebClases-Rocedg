from datetime import datetime

from database import db


def utc_now():
    return datetime.utcnow()


class UserActivityEvent(db.Model):
    __tablename__ = "user_activity_events"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    event_type = db.Column(db.String(80), nullable=False)
    object_type = db.Column(db.String(80), nullable=False)
    object_id = db.Column(db.String(120), nullable=True)
    object_title = db.Column(db.String(255), nullable=True)
    metadata_json = db.Column(db.Text, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)


class UserTopicProgress(db.Model):
    __tablename__ = "user_topic_progress"
    __table_args__ = (
        db.UniqueConstraint(
            "username",
            "topic_id",
            name="uq_user_topic_progress_username_topic_id",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    topic_id = db.Column(db.String(120), nullable=False)
    topic_title = db.Column(db.String(255), nullable=True)
    last_page = db.Column(db.Integer, nullable=True)
    last_opened_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    total_time_seconds = db.Column(db.Integer, nullable=False, default=0)
    open_count = db.Column(db.Integer, nullable=False, default=1)


class UserResourceAccess(db.Model):
    __tablename__ = "user_resource_access"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    resource_type = db.Column(db.String(80), nullable=False)
    resource_id = db.Column(db.String(120), nullable=True)
    resource_title = db.Column(db.String(255), nullable=True)
    action = db.Column(db.String(40), nullable=False)
    path = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)


class UserQuizAttempt(db.Model):
    __tablename__ = "user_quiz_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    quiz_id = db.Column(db.String(120), nullable=False)
    quiz_title = db.Column(db.String(255), nullable=True)
    score = db.Column(db.Integer, nullable=True)
    total_questions = db.Column(db.Integer, nullable=True)
    correct_answers = db.Column(db.Integer, nullable=True)
    percentage = db.Column(db.Float, nullable=True)
    started_at = db.Column(db.DateTime, nullable=True)
    submitted_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    duration_seconds = db.Column(db.Integer, nullable=True)
    metadata_json = db.Column(db.Text, nullable=True)


class UserStudyState(db.Model):
    """The student's latest concrete study context for reliable continuation links."""

    __tablename__ = "user_study_state"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True, index=True)
    last_lesson_id = db.Column(db.String(120), nullable=True)
    last_lesson_title = db.Column(db.String(255), nullable=True)
    last_lesson_at = db.Column(db.DateTime, nullable=True)
    last_exercise_id = db.Column(db.String(120), nullable=True)
    last_exercise_title = db.Column(db.String(255), nullable=True)
    last_exercise_topic = db.Column(db.String(120), nullable=True)
    last_exercise_topic_title = db.Column(db.String(255), nullable=True)
    last_exercise_type_key = db.Column(db.String(255), nullable=True)
    last_exercise_type_title = db.Column(db.String(255), nullable=True)
    last_exercise_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)


class ExerciseAttempt(db.Model):
    __tablename__ = "exercise_attempts"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, index=True)
    exercise_id = db.Column(db.String(120), nullable=False, index=True)
    exercise_version = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(db.String(40), nullable=False, default="started")
    started_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)
    submitted_at = db.Column(db.DateTime, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    reviewer_username = db.Column(db.String(120), nullable=True)
    teacher_comment = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, nullable=True)
    max_score = db.Column(db.Float, nullable=True)
    active_duration_seconds = db.Column(db.Integer, nullable=True)
    timer_enabled = db.Column(db.Boolean, nullable=False, default=True)
    timer_paused = db.Column(db.Boolean, nullable=False, default=False)

    responses = db.relationship(
        "ExerciseResponse",
        back_populates="attempt",
        cascade="all, delete-orphan",
    )


class ExerciseResponse(db.Model):
    __tablename__ = "exercise_responses"
    __table_args__ = (
        db.UniqueConstraint(
            "attempt_id",
            "field_id",
            name="uq_exercise_responses_attempt_id_field_id",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(
        db.Integer,
        db.ForeignKey("exercise_attempts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    field_id = db.Column(db.String(120), nullable=False)
    response_type = db.Column(db.String(80), nullable=False)
    raw_value = db.Column(db.Text, nullable=True)
    normalized_value = db.Column(db.Text, nullable=True)
    canonical_value = db.Column(db.Text, nullable=True)
    grading_status = db.Column(db.String(40), nullable=False, default="ungraded")
    auto_score = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(db.DateTime, nullable=False, default=utc_now, onupdate=utc_now)

    attempt = db.relationship("ExerciseAttempt", back_populates="responses")
