"""Build content/exercises/index.json from topic-level exercise metadata.

This first builder only creates the future /practice summary index. It does not
compile LaTeX, copy assets, or generate PDFs.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SUMMARY_FIELDS = [
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
]

EXERCISE_BANK_FILENAMES = (
    "exercises_t0.json",
    "exercises_t1.json",
    "exercises_t2.json",
    "exercises_t3.json",
    "exercises_t4.json",
    "exercises_t5.json",
    "exercises_t6.json",
    "exercises.json",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def topic_files(root: Path) -> list[Path]:
    content_root = root / "content" / "exercises"
    if not content_root.exists():
        return []
    return sorted(
        path
        for filename in EXERCISE_BANK_FILENAMES
        for path in content_root.rglob(filename)
    )


def summarize_exercise(exercise: dict[str, Any]) -> dict[str, Any]:
    summary = {field: exercise.get(field) for field in SUMMARY_FIELDS}
    summary["version"] = exercise.get("version", 1)
    summary["concept"] = exercise.get("concept") or exercise.get("topic")
    explicit_type = str(exercise.get("exercise_type") or "").strip()
    summary["exercise_type"] = (
        explicit_type
        if len(explicit_type) > 1
        else exercise.get("block") or exercise.get("concept") or exercise.get("response_mode")
    )
    summary["estimated_time_min"] = exercise.get("estimated_time_min") or exercise.get("estimated_minutes")
    workflow = exercise.get("workflow") if isinstance(exercise.get("workflow"), dict) else {}
    summary["workflow"] = {
        "status": workflow.get("status") or exercise.get("status")
    }
    return summary


def collect_exercises(root: Path) -> list[dict[str, Any]]:
    exercises: list[dict[str, Any]] = []
    for path in topic_files(root):
        data = load_json(path)
        for exercise in data.get("exercises", []):
            if isinstance(exercise, dict) and exercise.get("status") != "retired":
                exercises.append(summarize_exercise(exercise))
    return exercises


def build_index(root: Path | None = None, write: bool = True) -> dict[str, Any]:
    root = root or repo_root()
    exercises = collect_exercises(root)
    index = {
        "version": 1,
        "generated": True,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source": "content/exercises",
        "exercises": exercises,
    }

    if write:
        output_path = root / "content" / "exercises" / "index.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(index, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return index


def main() -> int:
    root = repo_root()
    files = topic_files(root)
    print("Building exercise index...")
    print(f"Found {len(files)} topic exercise file{'s' if len(files) != 1 else ''}.")
    index = build_index(root)
    print(f"Wrote content/exercises/index.json with {len(index['exercises'])} exercises.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
