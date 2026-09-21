"""Validate exercise metadata files.

This script checks the future exercise content skeleton before any web UI uses it.
Missing LaTeX/PDF/asset files are warnings for now because planned exercises can
point to files that will be created in later branches.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_EXERCISE_FIELDS = [
    "id",
    "version",
    "title",
    "course",
    "block",
    "topic",
    "concept",
    "exercise_type",
    "subtype",
    "difficulty",
    "estimated_time_min",
    "origin",
    "statement_tex",
    "solution_tex",
    "statement_pdf",
    "solution_pdf",
    "assets",
    "tags",
    "interactions",
    "solution",
    "common_mistakes",
    "workflow",
]

PATH_FIELDS = [
    "statement_tex",
    "solution_tex",
    "statement_pdf",
    "solution_pdf",
]

INDEX_REQUIRED_FIELDS = [
    "id",
    "version",
    "title",
    "course",
    "block",
    "topic",
    "concept",
    "exercise_type",
    "subtype",
    "difficulty",
    "estimated_time_min",
    "statement_pdf",
    "solution_pdf",
    "tags",
    "workflow",
]

LIGHTWEIGHT_EXERCISE_FIELDS = [
    "id",
    "version",
    "title",
    "course",
    "block",
    "topic",
    "response_mode",
    "statement",
    "solution",
    "assets",
    "tags",
    "origin",
    "status",
]


@dataclass
class ValidationResult:
    topic_file_count: int = 0
    exercise_count: int = 0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path, result: ValidationResult) -> Any:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as exc:
        result.errors.append(f"{path}: invalid JSON ({exc})")
    except OSError as exc:
        result.errors.append(f"{path}: could not be read ({exc})")
    return None


def relative_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_path_field(
    exercise: dict[str, Any],
    exercise_id: str,
    field_name: str,
    root: Path,
    result: ValidationResult,
) -> None:
    value = exercise.get(field_name)
    if not is_non_empty_string(value):
        result.errors.append(f"{exercise_id}: {field_name} must be a non-empty string.")
        return

    if not (root / value).exists():
        result.warnings.append(f"{field_name} file does not exist yet for {exercise_id}: {value}")


def validate_interactions(exercise: dict[str, Any], exercise_id: str, result: ValidationResult) -> None:
    interactions = exercise.get("interactions")
    if not isinstance(interactions, list):
        result.errors.append(f"{exercise_id}: interactions must be a list.")
        return

    for index, interaction in enumerate(interactions, start=1):
        if not isinstance(interaction, dict):
            result.errors.append(f"{exercise_id}: interaction {index} must be an object.")
            continue
        if not is_non_empty_string(interaction.get("id")):
            result.errors.append(f"{exercise_id}: interaction {index} is missing id.")
        if not is_non_empty_string(interaction.get("type")):
            result.errors.append(f"{exercise_id}: interaction {index} is missing type.")


def validate_workflow(exercise: dict[str, Any], exercise_id: str, result: ValidationResult) -> None:
    workflow = exercise.get("workflow")
    if not isinstance(workflow, dict):
        result.errors.append(f"{exercise_id}: workflow must be an object.")
        return
    if not is_non_empty_string(workflow.get("status")):
        result.errors.append(f"{exercise_id}: workflow.status is required.")


def validate_solution(exercise: dict[str, Any], exercise_id: str, result: ValidationResult) -> None:
    solution = exercise.get("solution")
    if not isinstance(solution, dict):
        result.errors.append(f"{exercise_id}: solution must be an object.")
        return
    if not isinstance(solution.get("summary_steps"), list):
        result.errors.append(f"{exercise_id}: solution.summary_steps must be a list.")


def validate_assets_list(exercise: dict[str, Any], exercise_id: str, root: Path, result: ValidationResult) -> None:
    assets = exercise.get("assets")
    if not isinstance(assets, list):
        result.errors.append(f"{exercise_id}: assets must be a list.")
        return

    for asset in assets:
        asset_path = asset
        if isinstance(asset, dict):
            asset_path = asset.get("path")
        if not is_non_empty_string(asset_path):
            result.errors.append(f"{exercise_id}: every asset path must be a non-empty string.")
        elif not (root / asset_path).exists():
            result.warnings.append(f"asset file does not exist yet for {exercise_id}: {asset_path}")


def is_lightweight_exercise(exercise: dict[str, Any]) -> bool:
    return "response_mode" in exercise and ("statement" in exercise or "statement_source" in exercise)


def validate_lightweight_exercise(
    exercise: dict[str, Any],
    exercise_id: str,
    root: Path,
    result: ValidationResult,
) -> None:
    for field_name in LIGHTWEIGHT_EXERCISE_FIELDS:
        if field_name in {'statement', 'solution'} and is_non_empty_string(exercise.get(field_name + '_source')):
            continue
        if field_name not in exercise:
            result.errors.append(f"{exercise_id}: missing required field {field_name}.")

    difficulty = exercise.get("difficulty")
    if difficulty is not None and (
        not isinstance(difficulty, int) or isinstance(difficulty, bool) or not 1 <= difficulty <= 5
    ):
        result.errors.append(f"{exercise_id}: difficulty must be an integer from 1 to 5.")

    estimated_minutes = exercise.get("estimated_minutes")
    if estimated_minutes is not None and not isinstance(estimated_minutes, int):
        result.errors.append(f"{exercise_id}: estimated_minutes must be an integer.")

    version = exercise.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        result.errors.append(f"{exercise_id}: version must be a positive integer.")

    if not isinstance(exercise.get("origin"), dict):
        result.errors.append(f"{exercise_id}: origin must be an object.")
    elif not is_non_empty_string(exercise["origin"].get("kind")):
        result.errors.append(f"{exercise_id}: origin.kind is required.")

    if not isinstance(exercise.get("tags"), list):
        result.errors.append(f"{exercise_id}: tags must be a list.")

    if not is_non_empty_string(exercise.get("status")):
        result.errors.append(f"{exercise_id}: status is required.")

    validate_assets_list(exercise, exercise_id, root, result)


def validate_exercise(
    exercise: Any,
    source_file: Path,
    root: Path,
    seen_ids: set[str],
    result: ValidationResult,
) -> None:
    source = relative_path(source_file, root)
    if not isinstance(exercise, dict):
        result.errors.append(f"{source}: every exercise must be an object.")
        return

    exercise_id = exercise.get("id", "<missing id>")
    if not is_non_empty_string(exercise_id):
        result.errors.append(f"{source}: exercise is missing id.")
        exercise_id = "<missing id>"
    elif exercise_id in seen_ids:
        result.errors.append(f"{exercise_id}: duplicated exercise id.")
    else:
        seen_ids.add(exercise_id)

    if is_lightweight_exercise(exercise):
        validate_lightweight_exercise(exercise, exercise_id, root, result)
        return

    for field_name in REQUIRED_EXERCISE_FIELDS:
        if field_name not in exercise:
            result.errors.append(f"{exercise_id}: missing required field {field_name}.")

    difficulty = exercise.get("difficulty")
    if not isinstance(difficulty, int) or isinstance(difficulty, bool) or not 1 <= difficulty <= 5:
        result.errors.append(f"{exercise_id}: difficulty must be an integer from 1 to 5.")

    version = exercise.get("version")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        result.errors.append(f"{exercise_id}: version must be a positive integer.")

    if not isinstance(exercise.get("estimated_time_min"), int):
        result.errors.append(f"{exercise_id}: estimated_time_min must be an integer.")

    if not isinstance(exercise.get("origin"), dict):
        result.errors.append(f"{exercise_id}: origin must be an object.")
    elif not is_non_empty_string(exercise["origin"].get("kind")):
        result.errors.append(f"{exercise_id}: origin.kind is required.")

    if not isinstance(exercise.get("tags"), list):
        result.errors.append(f"{exercise_id}: tags must be a list.")

    if not isinstance(exercise.get("common_mistakes"), list):
        result.errors.append(f"{exercise_id}: common_mistakes must be a list.")

    validate_workflow(exercise, exercise_id, result)
    validate_solution(exercise, exercise_id, result)
    validate_interactions(exercise, exercise_id, result)

    for field_name in PATH_FIELDS:
        validate_path_field(exercise, exercise_id, field_name, root, result)

    validate_assets_list(exercise, exercise_id, root, result)


def load_topic_exercises(root: Path, result: ValidationResult) -> tuple[list[dict[str, Any]], set[str]]:
    content_root = root / "content" / "exercises"
    bank_filenames = (
        "exercises_t0.json",
        "exercises_t1.json",
        "exercises_t2.json",
        "exercises_t3.json",
        "exercises_t4.json",
        "exercises_t5.json",
        "exercises_t6.json",
        "exercises.json",
    )
    topic_files = (
        sorted(
            path
            for filename in bank_filenames
            for path in content_root.rglob(filename)
        )
        if content_root.exists()
        else []
    )
    result.topic_file_count = len(topic_files)

    if not topic_files:
        result.errors.append("No topic exercise files found under content/exercises/.")
        return [], set()

    exercises: list[dict[str, Any]] = []
    seen_ids: set[str] = set()

    for topic_file in topic_files:
        data = load_json(topic_file, result)
        if data is None:
            continue
        if not isinstance(data, dict):
            result.errors.append(f"{relative_path(topic_file, root)}: top-level JSON must be an object.")
            continue

        file_exercises = data.get("exercises")
        if not isinstance(file_exercises, list):
            result.errors.append(f"{relative_path(topic_file, root)}: exercises must be a list.")
            continue

        for exercise in file_exercises:
            validate_exercise(exercise, topic_file, root, seen_ids, result)
            if isinstance(exercise, dict):
                exercises.append(exercise)

    result.exercise_count = len(exercises)
    indexable_ids = {
        exercise["id"]
        for exercise in exercises
        if isinstance(exercise, dict)
        and is_non_empty_string(exercise.get("id"))
        and exercise.get("status") != "retired"
    }
    return exercises, indexable_ids


def validate_data_index(root: Path, topic_ids: set[str], result: ValidationResult) -> None:
    index_path = root / "content" / "exercises" / "index.json"
    if not index_path.exists():
        result.warnings.append("content/exercises/index.json does not exist yet.")
        return

    data = load_json(index_path, result)
    if data is None:
        return
    if not isinstance(data, dict):
        result.errors.append("content/exercises/index.json: top-level JSON must be an object.")
        return

    index_exercises = data.get("exercises")
    if not isinstance(index_exercises, list):
        result.errors.append("content/exercises/index.json: exercises must be a list.")
        return

    index_ids: set[str] = set()
    for exercise in index_exercises:
        if not isinstance(exercise, dict):
            result.errors.append("content/exercises/index.json: every exercise must be an object.")
            continue

        exercise_id = exercise.get("id", "<missing id>")
        for field_name in INDEX_REQUIRED_FIELDS:
            if field_name not in exercise:
                result.errors.append(f"content/exercises/index.json {exercise_id}: missing {field_name}.")

        if is_non_empty_string(exercise_id):
            if exercise_id in index_ids:
                result.errors.append(f"content/exercises/index.json {exercise_id}: duplicated id.")
            index_ids.add(exercise_id)
        else:
            result.errors.append("content/exercises/index.json: exercise is missing id.")

        difficulty = exercise.get("difficulty")
        if not isinstance(difficulty, int) or isinstance(difficulty, bool) or not 1 <= difficulty <= 5:
            result.errors.append(f"content/exercises/index.json {exercise_id}: difficulty must be 1 to 5.")

        version = exercise.get("version")
        if not isinstance(version, int) or isinstance(version, bool) or version < 1:
            result.errors.append(f"content/exercises/index.json {exercise_id}: version must be a positive integer.")

        workflow = exercise.get("workflow")
        if not isinstance(workflow, dict) or not is_non_empty_string(workflow.get("status")):
            result.errors.append(f"content/exercises/index.json {exercise_id}: workflow.status is required.")

    missing_from_index = sorted(topic_ids - index_ids)
    extra_in_index = sorted(index_ids - topic_ids)
    if missing_from_index:
        result.warnings.append(f"content/exercises/index.json is missing topic exercises: {', '.join(missing_from_index)}")
    if extra_in_index:
        result.warnings.append(f"content/exercises/index.json has exercises not present in content/: {', '.join(extra_in_index)}")


def validate_all(root: Path | None = None) -> ValidationResult:
    root = root or repo_root()
    result = ValidationResult()
    _, topic_ids = load_topic_exercises(root, result)
    validate_data_index(root, topic_ids, result)
    return result


def plural(count: int, singular: str, plural_text: str) -> str:
    return singular if count == 1 else plural_text


def print_report(result: ValidationResult) -> None:
    print("Validating exercise metadata...")
    topic_word = plural(result.topic_file_count, "topic exercise file", "topic exercise files")
    exercise_word = plural(result.exercise_count, "exercise", "exercises")
    print(f"Found {result.topic_file_count} {topic_word}.")
    print(f"Found {result.exercise_count} {exercise_word}.")

    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    if result.errors:
        print("Errors:")
        for error in result.errors:
            print(f"- {error}")
        print("Validation failed.")
        return

    if result.warnings:
        print("Validation passed with warnings.")
    else:
        print("Validation passed.")


def main() -> int:
    result = validate_all()
    print_report(result)
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
