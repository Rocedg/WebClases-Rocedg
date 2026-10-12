"""Load exercise banks from legacy files or per-topic block files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


LEGACY_BANK_FILENAMES = (
    "exercises_t0.json",
    "exercises_t1.json",
    "exercises_t2.json",
    "exercises_t3.json",
    "exercises_t4.json",
    "exercises_t5.json",
    "exercises_t6.json",
    "exercises.json",
)


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: exercise bank must be a JSON object")
    return data


def load_topic_bank(path: Path) -> dict[str, Any]:
    """Load one legacy bank file or one split topic directory."""
    if path.is_file():
        return _load_json(path)

    manifest_path = path / "_topic.json"
    if not manifest_path.exists():
        topic = path.name
        legacy_path = path / f"exercises_{topic}.json"
        if legacy_path.exists():
            return _load_json(legacy_path)
        legacy_path = path / "exercises.json"
        if legacy_path.exists():
            return _load_json(legacy_path)
    manifest = _load_json(manifest_path)
    block_files = manifest.get("exercise_files")
    if not isinstance(block_files, list) or not all(isinstance(item, str) for item in block_files):
        raise ValueError(f"{manifest_path}: exercise_files must be an ordered list of filenames")

    exercises: list[dict[str, Any]] = []
    for filename in block_files:
        block_data = _load_json(path / filename)
        block_exercises = block_data.get("exercises")
        if not isinstance(block_exercises, list):
            raise ValueError(f"{path / filename}: exercises must be a list")
        exercises.extend(block_exercises)

    data = {key: value for key, value in manifest.items() if key != "exercise_files"}
    data["exercises"] = exercises
    return data


def topic_bank_sources(content_root: Path) -> list[Path]:
    """Return logical topic sources in the same deterministic order as before."""
    if not content_root.exists():
        return []

    sources: list[Path] = []
    split_topics = {path.parent for path in content_root.rglob("_topic.json")}
    sources.extend(sorted(split_topics))
    for filename in LEGACY_BANK_FILENAMES:
        sources.extend(
            sorted(
                path
                for path in content_root.rglob(filename)
                if path.parent not in split_topics
            )
        )
    return sources


def load_topic_banks(content_root: Path) -> list[tuple[Path, dict[str, Any]]]:
    """Load all logical topic banks below a content root."""
    return [(source, load_topic_bank(source)) for source in topic_bank_sources(content_root)]


def load_exercise_banks(content_root: Path) -> list[dict[str, Any]]:
    """Load all logical topic banks below a content root."""
    return [data for _, data in load_topic_banks(content_root)]
