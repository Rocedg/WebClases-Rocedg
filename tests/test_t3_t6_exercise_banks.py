from __future__ import annotations
import importlib.util
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from app import load_exercise_catalogue


ROOT = Path(__file__).resolve().parents[1]
TOPICS = ("t3", "t4", "t5", "t6")
ALLOWED_TYPES = {"numeric", "unit_expression", "single_choice", "vector", "function", "short_text"}


def load_builder():
    spec = importlib.util.spec_from_file_location("build_t3_t6_exercise_banks", ROOT / "scripts" / "build_t3_t6_exercise_banks.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_bank(topic: str) -> dict:
    path = ROOT / "content" / "exercises" / "1bach" / topic / f"exercises_{topic}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_t3_t6_banks_are_complete_compact_and_structured():
    all_ids: set[str] = set()
    for topic in TOPICS:
        bank = load_bank(topic)
        exercises = bank["exercises"]
        assert len(exercises) == 60
        assert bank["topic"] == topic
        for exercise in exercises:
            assert exercise["id"].startswith(f"{topic}_")
            assert exercise["id"] not in all_ids
            all_ids.add(exercise["id"])
            assert exercise["status"] == "draft"
            assert exercise["statement_source"]
            assert "<" not in exercise["statement_source"]
            assert "$" not in exercise["statement_source"]
            assert "statement" not in exercise
            assert "solution" not in exercise
            assert "hint" not in exercise and "hints" not in exercise and "interactions" not in exercise
            assert exercise["response_fields"]
            assert all(field["type"] in ALLOWED_TYPES and field.get("part") for field in exercise["response_fields"])
    assert len(all_ids) == 240


def test_t3_t6_assets_are_responsive_valid_svg_files():
    asset_paths: set[str] = set()
    for topic in TOPICS:
        for exercise in load_bank(topic)["exercises"]:
            assert len(exercise["assets"]) == 1
            asset = exercise["assets"][0]
            assert asset["alt"]
            assert asset["path"] not in asset_paths
            asset_paths.add(asset["path"])
            path = ROOT / asset["path"]
            root = ET.fromstring(path.read_text(encoding="utf-8"))
            assert root.tag.endswith("svg")
            assert root.attrib["viewBox"] == "0 0 640 360"
            assert "max-width:100%;height:auto" in root.attrib["style"]
    assert len(asset_paths) == 240


def test_t3_t6_builder_is_idempotent_in_check_mode():
    builder = load_builder()
    banks, assets = builder.build_all()
    assert not builder.validate(banks, assets)
    assert builder.changed_outputs(banks, assets) == []


def test_catalogue_discovers_all_first_year_topic_banks():
    exercises = load_exercise_catalogue()["exercises"]
    counts = {topic: sum(exercise["topic"] == topic for exercise in exercises) for topic in TOPICS}
    assert counts == {topic: 60 for topic in TOPICS}
