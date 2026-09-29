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


def components(exercises, exercise_id: str, field_id: str) -> list[float]:
    exercise = next(item for item in exercises if item["id"] == exercise_id)
    response_field = next(item for item in exercise["response_fields"] if item["id"] == field_id)
    return [float(value) for value in response_field["expected_components"]]


def rotate(vector: tuple[float, float], degrees: float) -> tuple[float, float]:
    """Components of a fixed vector in axes rotated counterclockwise by `degrees`."""
    c, s = math.cos(math.radians(degrees)), math.sin(math.radians(degrees))
    return (vector[0] * c + vector[1] * s, -vector[0] * s + vector[1] * c)


def assert_vector(errors: list[str], label: str, actual: list[float], expected, tolerance: float) -> None:
    if len(actual) != len(expected) or any(abs(a - e) > tolerance for a, e in zip(actual, expected)):
        errors.append(f"{label}: expected {list(expected)}, got {actual}")


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

    # Measurement v5: expected value vs mean, farthest datum as error.
    g = [9.62, 9.71, 9.68, 9.75, 9.64]
    g_mean = sum(g) / len(g)
    assert_close(errors, "t0_m_021.mean", field(exercises, "t0_m_021", "mean"), g_mean, 0.005)
    assert_close(errors, "t0_m_021.abs_error", field(exercises, "t0_m_021", "abs_error"), abs(g_mean - 9.81), 0.005)
    assert_close(errors, "t0_m_021.max_dev", field(exercises, "t0_m_021", "max_dev"), max(abs(x - g_mean) for x in g), 0.005)
    rods = [25.3, 25.6, 25.4, 25.8, 25.4]
    rod_mean = sum(rods) / len(rods)
    assert_close(errors, "t0_m_022.max_dev", field(exercises, "t0_m_022", "max_dev"), max(abs(x - rod_mean) for x in rods), 0.005)
    assert_close(errors, "t0_m_022.half_range", field(exercises, "t0_m_022", "half_range"), (max(rods) - min(rods)) / 2, 0.005)
    q = [1.38, 1.62, 1.47, 1.53]
    assert_close(errors, "t0_m_023.dev_Q", field(exercises, "t0_m_023", "dev_Q"), max(abs(x - sum(q) / 4) for x in q), 0.003)
    rho = [2.62, 2.66, 2.64, 2.68]
    assert_close(errors, "t0_m_024.err_mean", field(exercises, "t0_m_024", "err_mean"), abs(sum(rho) / 4 - 2.70), 0.003)
    temps = [101.4, 101.6, 101.5, 101.5]
    assert_close(errors, "t0_m_025.corrected", field(exercises, "t0_m_025", "corrected"), 38.2 - (sum(temps) / 4 - 100.0), 0.005)

    # Vectors v5: dot/cross products and change of axes.
    assert_close(errors, "t0_v_037.angle", field(exercises, "t0_v_037", "angle"), math.degrees(math.acos(8 / math.sqrt(14 * 21))), 0.1)
    assert_close(errors, "t0_v_038.angle", field(exercises, "t0_v_038", "angle"), math.degrees(math.acos(10 / math.sqrt(21 * 29))), 0.1)
    assert_vector(errors, "t0_v_040.AxB", components(exercises, "t0_v_040", "AxB"), (-10, 7, 9), 1e-9)
    assert_close(errors, "t0_v_042.angle", field(exercises, "t0_v_042", "angle"), math.degrees(math.acos(-2 / math.sqrt(200))), 0.1)
    assert_vector(errors, "t0_v_046.A_new", components(exercises, "t0_v_046", "A_new"), rotate((6.0, 2.0), 30), 0.01)
    assert_vector(errors, "t0_v_047.v_new", components(exercises, "t0_v_047", "v_new"), rotate((4.0, -3.0), -20), 0.01)
    assert_vector(errors, "t0_v_048.F", components(exercises, "t0_v_048", "F"), rotate((5.0, 2.0), -40), 0.01)
    assert_vector(errors, "t0_v_049.F_ramp2", components(exercises, "t0_v_049", "F_ramp2"), rotate(rotate((10.0, 0.0), -30), -15), 0.01)
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
