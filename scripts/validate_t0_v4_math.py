"""Independent numerical checks for selected T0 v4 expected values."""

from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t0" / "exercises_t0.json"


def field(exercises, exercise_id: str, field_id: str) -> float:
    exercise = next(item for item in exercises if item["id"] == exercise_id)
    response_field = next(item for item in exercise["response_fields"] if item["id"] == field_id)
    return float(response_field["expected_value"])


def assert_close(errors: list[str], label: str, actual: float, expected: float, tolerance: float = 1e-9) -> None:
    if abs(actual - expected) > tolerance:
        errors.append(f"{label}: expected {expected}, got {actual}")


def validate_math() -> list[str]:
    with BANK_PATH.open(encoding="utf-8") as file:
        exercises = json.load(file)["exercises"]

    errors: list[str] = []
    assert_close(errors, "t0_u_001.speed", field(exercises, "t0_u_001", "speed"), 12600 / 1080, 0.04)
    assert_close(errors, "t0_u_002.density_si", field(exercises, "t0_u_002", "density_si"), 2700, 1e-9)
    assert_close(errors, "t0_u_007.phi", field(exercises, "t0_u_007", "phi"), math.pi / 6, 0.005)
    assert_close(errors, "t0_u_008.a", field(exercises, "t0_u_008", "a"), 0.5, 1e-9)
    assert_close(errors, "t0_u_008.b", field(exercises, "t0_u_008", "b"), -0.5, 1e-9)
    assert_close(errors, "t0_c_015.x_intercept", field(exercises, "t0_c_015", "x_intercept"), 11 / 3, 0.003)

    zero_time = 4 / (7 / 2) + 4
    positive_area = 0.5 * 2 * 4 + 2 * 4 + 0.5 * (zero_time - 4) * 4
    negative_signed = -0.5 * (6 - zero_time) * 3
    displacement = positive_area + negative_signed
    distance = positive_area - negative_signed
    assert_close(errors, "t0_c_020.zero_time", field(exercises, "t0_c_020", "zero_time"), zero_time, 0.003)
    assert_close(errors, "t0_c_020.positive_area", field(exercises, "t0_c_020", "positive_area"), positive_area, 0.01)
    assert_close(errors, "t0_c_020.negative_signed", field(exercises, "t0_c_020", "negative_signed"), negative_signed, 0.01)
    assert_close(errors, "t0_c_020.displacement", field(exercises, "t0_c_020", "displacement"), displacement, 0.01)
    assert_close(errors, "t0_c_020.distance", field(exercises, "t0_c_020", "distance"), distance, 0.01)
    return errors


def main() -> int:
    errors = validate_math()
    if errors:
        print("T0 v4 mathematical validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("T0 v4 mathematical validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
