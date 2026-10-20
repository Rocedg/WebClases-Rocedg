"""Independent numerical checks for selected T0 v4 expected values."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.exercise_bank_loader import load_topic_bank

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t0"


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
    exercises = load_topic_bank(BANK_PATH)["exercises"]

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

    # Calculus v5: derivatives and integrals recomputed from the statements.
    def num_derivative(f, x, h=1e-5):
        return (f(x + h) - f(x - h)) / (2 * h)

    def num_integral(f, a, b, n=2000):
        step = (b - a) / n
        return sum(f(a + (i + 0.5) * step) for i in range(n)) * step

    x001 = lambda t: 7 - 3 * t + 2 * t**4
    v001 = lambda t: num_derivative(x001, t)
    assert_close(errors, "t0_c_001.v_1", field(exercises, "t0_c_001", "v_1"), v001(1.0), 0.001)
    assert_close(errors, "t0_c_001.a_1", field(exercises, "t0_c_001", "a_1"), num_derivative(v001, 1.0, 1e-3), 0.01)
    g002 = lambda x: 5 * x**-1 - 2 * x**-3
    assert_close(errors, "t0_c_002.value", field(exercises, "t0_c_002", "value"), num_derivative(g002, 2.0), 1e-6)
    h003 = lambda x: 3 * math.sqrt(x) - 4 / math.sqrt(x)
    assert_close(errors, "t0_c_003.slope_1", field(exercises, "t0_c_003", "slope_1"), num_derivative(h003, 1.0), 1e-6)
    assert_close(errors, "t0_c_003.slope", field(exercises, "t0_c_003", "slope"), num_derivative(h003, 4.0), 1e-6)
    x005 = lambda t: t**3 - 4 * t
    assert_close(errors, "t0_c_005.average_velocity", field(exercises, "t0_c_005", "average_velocity"), x005(2) - x005(1), 1e-9)
    assert_close(errors, "t0_c_005.instant_velocity", field(exercises, "t0_c_005", "instant_velocity"), num_derivative(x005, 2.0), 1e-6)
    assert_close(errors, "t0_c_005.acceleration", field(exercises, "t0_c_005", "acceleration"), num_derivative(lambda t: num_derivative(x005, t), 2.0, 1e-3), 0.01)
    assert_close(errors, "t0_c_008.v_2", field(exercises, "t0_c_008", "v_2"), -2 + num_integral(lambda t: 4 + 3 * t**2, 0, 2), 1e-6)
    a009 = lambda t: 6 * t**2 - 4 * t + 1
    assert_close(errors, "t0_c_009.delta_v", field(exercises, "t0_c_009", "delta_v"), num_integral(a009, 0, 2), 1e-6)
    assert_close(errors, "t0_c_009.v_2", field(exercises, "t0_c_009", "v_2"), 3 + num_integral(a009, 0, 2), 1e-6)
    displacement010 = num_integral(lambda t: 2 * t + 1, 1, 3)
    assert_close(errors, "t0_c_010.displacement", field(exercises, "t0_c_010", "displacement"), displacement010, 1e-6)
    assert_close(errors, "t0_c_010.average_velocity", field(exercises, "t0_c_010", "average_velocity"), displacement010 / 2, 1e-6)
    assert_close(errors, "t0_c_017.C", field(exercises, "t0_c_017", "C"), 3 - (3 * 1**2 - 4 * 1), 1e-9)

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
    assert_close(errors, "t0_v_050.mod_11", field(exercises, "t0_v_050", "mod_11"), math.sqrt(2), 0.01)
    assert_close(errors, "t0_v_050.mod_05", field(exercises, "t0_v_050", "mod_05"), math.sqrt(0.5), 0.01)
    assert_close(errors, "t0_v_051.wrong_modulus", field(exercises, "t0_v_051", "wrong_modulus"), math.sqrt(0.43**2 + 0.57**2), 0.01)
    assert_close(errors, "t0_v_052.magnitude", field(exercises, "t0_v_052", "magnitude"), math.hypot(-5, 12), 1e-9)
    assert_vector(errors, "t0_v_053.unit_30", components(exercises, "t0_v_053", "unit_30"), (math.cos(math.radians(30)), math.sin(math.radians(30))), 0.005)
    assert_vector(errors, "t0_v_054.displacement", components(exercises, "t0_v_054", "displacement"), (6, 8), 1e-9)
    assert_close(errors, "t0_v_054.distance", field(exercises, "t0_v_054", "distance"), 10, 1e-9)
    assert_vector(errors, "t0_v_055.force", components(exercises, "t0_v_055", "force"), (-40, 30), 1e-9)
    assert_close(errors, "t0_v_056.angle", field(exercises, "t0_v_056", "angle"), math.degrees(math.atan2(-16, 12)) % 360, 0.1)
    assert_close(errors, "t0_v_057.magnitude", field(exercises, "t0_v_057", "magnitude"), math.sqrt(9), 1e-9)
    assert_vector(errors, "t0_v_057.force", components(exercises, "t0_v_057", "force"), (8, -4, 8), 1e-9)

    # Prompt 8: determinants, normal vectors, cross product as a determinant, first calculus drills.
    def det2(m):
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    def det3(m):
        return sum(m[0][j] * (-1) ** j * det2([[m[1][k] for k in range(3) if k != j],
                                                 [m[2][k] for k in range(3) if k != j]]) for j in range(3))

    def cross(a, b):
        return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

    def dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    assert_close(errors, "t0_v_058.det_a", field(exercises, "t0_v_058", "det_a"), det2([[3, 2], [1, 4]]))
    assert_close(errors, "t0_v_058.det_b", field(exercises, "t0_v_058", "det_b"), det2([[-2, 5], [3, -1]]))
    assert_close(errors, "t0_v_058.det_c", field(exercises, "t0_v_058", "det_c"), det2([[6, 3], [4, 2]]))
    assert_close(errors, "t0_v_058.area", field(exercises, "t0_v_058", "area"), abs(det2([[3, 1], [1, 4]])))
    m059 = [[2, 1, 0], [1, 3, -1], [4, 0, 2]]
    right = sum(math.prod(m059[i][(i + j) % 3] for i in range(3)) for j in range(3))
    left = sum(math.prod(m059[i][(j - i) % 3] for i in range(3)) for j in range(3))
    assert_close(errors, "t0_v_059.sarrus_right", field(exercises, "t0_v_059", "sarrus_right"), right)
    assert_close(errors, "t0_v_059.sarrus_left", field(exercises, "t0_v_059", "sarrus_left"), left)
    assert_close(errors, "t0_v_059.det_M", field(exercises, "t0_v_059", "det_M"), det3(m059))
    assert_close(errors, "t0_v_059.sarrus_vs_row", right - left, det3(m059))
    for j, field_id in enumerate(("minor_11", "minor_12", "minor_13")):
        minor = det2([[m059[1][k] for k in range(3) if k != j], [m059[2][k] for k in range(3) if k != j]])
        assert_close(errors, f"t0_v_059.{field_id}", field(exercises, "t0_v_059", field_id), minor)
    assert_close(errors, "t0_v_059.det_d", field(exercises, "t0_v_059", "det_d"), det3([[1, 2, 3], [2, 4, 6], [0, 1, 5]]))
    a060, b060 = (2, -1, 1), (1, 1, -2)
    axb060 = cross(a060, b060)
    assert_vector(errors, "t0_v_060.AxB", components(exercises, "t0_v_060", "AxB"), axb060, 1e-9)
    assert_close(errors, "t0_v_060.check", field(exercises, "t0_v_060", "check"), dot(a060, axb060))
    assert_close(errors, "t0_v_060.modulus", field(exercises, "t0_v_060", "modulus"), math.sqrt(dot(axb060, axb060)), 0.005)
    assert_close(errors, "t0_v_060.wrong_dot", field(exercises, "t0_v_060", "wrong_dot"), dot(a060, (axb060[0], -axb060[1], axb060[2])))
    a061 = (3, -4)
    n061 = (-a061[1], a061[0])
    assert_vector(errors, "t0_v_061.normal", components(exercises, "t0_v_061", "normal"), n061, 1e-9)
    assert_close(errors, "t0_v_061.dot", field(exercises, "t0_v_061", "dot"), dot(a061, n061))
    unit061 = tuple(c / math.hypot(*n061) for c in n061)
    assert_vector(errors, "t0_v_061.unit_normal", components(exercises, "t0_v_061", "unit_normal"), unit061, 0.001)
    assert_vector(errors, "t0_v_061.other_unit", components(exercises, "t0_v_061", "other_unit"), tuple(-c for c in unit061), 0.001)
    a062, b062 = (1, 1, 0), (0, 1, 1)
    n062 = cross(a062, b062)
    assert_vector(errors, "t0_v_062.normal", components(exercises, "t0_v_062", "normal"), n062, 1e-9)
    assert_close(errors, "t0_v_062.dot_A", field(exercises, "t0_v_062", "dot_A"), dot(a062, n062))
    assert_close(errors, "t0_v_062.dot_B", field(exercises, "t0_v_062", "dot_B"), dot(b062, n062))
    assert_close(errors, "t0_v_062.modulus", field(exercises, "t0_v_062", "modulus"), math.sqrt(dot(n062, n062)), 0.005)
    assert_vector(errors, "t0_v_062.unit_normal", components(exercises, "t0_v_062", "unit_normal"),
                  tuple(c / math.sqrt(dot(n062, n062)) for c in n062), 0.001)
    m063 = cross((0.20, 0.30, 0), (10, -5, 0))
    assert_vector(errors, "t0_v_063.M", components(exercises, "t0_v_063", "M"), m063, 1e-9)
    assert_close(errors, "t0_v_063.modulus", field(exercises, "t0_v_063", "modulus"), math.sqrt(dot(m063, m063)), 0.05)
    def assert_function(label, exercise_id, field_id, reference, points=(0.5, 1.0, 1.5, 2.0, 3.0)):
        exercise = next(item for item in exercises if item["id"] == exercise_id)
        response_field = next(item for item in exercise["response_fields"] if item["id"] == field_id)
        expression = response_field["canonical_expression"].replace("^", "**")
        variable = response_field.get("variable", "x")
        for point in points:
            value = eval(expression, {"__builtins__": {}}, {variable: point})  # trusted repo content
            assert_close(errors, f"{label}({point})", value, reference(point), 1e-4)

    assert_function("t0_c_025.d_a", "t0_c_025", "d_a", lambda x: num_derivative(lambda u: u**3, x))
    assert_function("t0_c_025.d_b", "t0_c_025", "d_b", lambda x: num_derivative(lambda u: 5 * u**2 - 3 * u + 2, x))
    assert_function("t0_c_025.d_c", "t0_c_025", "d_c", lambda x: num_derivative(lambda u: 2 * u**4 - u, x))
    assert_function("t0_c_025.d_d", "t0_c_025", "d_d", lambda x: num_derivative(lambda u: 6 / u**2, x))
    assert_function("t0_c_026.prim_a", "t0_c_026", "prim_a", lambda x: num_integral(lambda u: 3 * u**2, 0, x))
    assert_function("t0_c_026.prim_b", "t0_c_026", "prim_b", lambda x: num_integral(lambda u: 4 * u + 1, 0, x))
    assert_function("t0_c_026.x_t", "t0_c_026", "x_t", lambda t: 1 + num_integral(lambda u: 4 * u, 0, t))
    # Prompt 12: slopes, average and instantaneous velocity, extrema.
    vertices = [(0, 0), (2, 4), (5, 4), (7, 0), (8, 3)]
    slopes = [(x2 - x1) / (t2 - t1) for (t1, x1), (t2, x2) in zip(vertices, vertices[1:])]
    for stretch, slope in zip("ABCD", slopes):
        assert_close(errors, f"t0_c_027.v_{stretch}", field(exercises, "t0_c_027", f"v_{stretch}"), slope)
    x029 = lambda t: 4 * t - t**2
    assert_close(errors, "t0_c_029.v_Q", field(exercises, "t0_c_029", "v_Q"), num_derivative(x029, 2.0), 1e-6)
    x030 = lambda t: t**2 + 1
    assert_close(errors, "t0_c_030.x_1", field(exercises, "t0_c_030", "x_1"), x030(1))
    assert_close(errors, "t0_c_030.x_3", field(exercises, "t0_c_030", "x_3"), x030(3))
    assert_close(errors, "t0_c_030.vmed_13", field(exercises, "t0_c_030", "vmed_13"), (x030(3) - x030(1)) / 2)
    assert_close(errors, "t0_c_030.vmed_02", field(exercises, "t0_c_030", "vmed_02"), (x030(2) - x030(0)) / 2)
    x031 = lambda t: 3 * t**2 - 2 * t
    assert_close(errors, "t0_c_031.v_1", field(exercises, "t0_c_031", "v_1"), num_derivative(x031, 1.0), 1e-6)
    assert_close(errors, "t0_c_031.v_2", field(exercises, "t0_c_031", "v_2"), num_derivative(x031, 2.0), 1e-6)
    for field_id, end in (("vmed_4", 4), ("vmed_35", 3.5), ("vmed_31", 3.1), ("vmed_301", 3.01)):
        assert_close(errors, f"t0_c_032.{field_id}", field(exercises, "t0_c_032", field_id), (end**2 - 9) / (end - 3), 1e-9)
    assert_close(errors, "t0_c_032.v_3", field(exercises, "t0_c_032", "v_3"), num_derivative(lambda t: t**2, 3.0), 1e-6)
    x033 = lambda t: t**3 - 6 * t**2 + 9 * t
    v033 = lambda t: num_derivative(x033, t)
    discriminant = 12**2 - 4 * 3 * 9  # roots of v(t) = 3t^2 - 12t + 9
    roots = ((12 - math.sqrt(discriminant)) / 6, (12 + math.sqrt(discriminant)) / 6)
    assert_close(errors, "t0_c_033.t_first", field(exercises, "t0_c_033", "t_first"), roots[0], 1e-9)
    assert_close(errors, "t0_c_033.t_second", field(exercises, "t0_c_033", "t_second"), roots[1], 1e-9)
    assert_close(errors, "t0_c_033.x_first", field(exercises, "t0_c_033", "x_first"), x033(roots[0]), 1e-9)
    assert_close(errors, "t0_c_033.x_second", field(exercises, "t0_c_033", "x_second"), x033(roots[1]), 1e-9)
    if not (v033(roots[0] - 0.1) > 0 > v033(roots[0] + 0.1) and v033(roots[1] - 0.1) < 0 < v033(roots[1] + 0.1)):
        errors.append("t0_c_033: expected a maximum at the first root and a minimum at the second")
    assert_close(errors, "t0_c_034.g_zero", field(exercises, "t0_c_034", "g_zero"), 4 / 2)
    assert_close(errors, "t0_c_034.g_value", field(exercises, "t0_c_034", "g_value"), 2**2 - 4 * 2)
    assert_close(errors, "t0_c_034.f_prime_0", field(exercises, "t0_c_034", "f_prime_0"), num_derivative(lambda x: x**3, 0.0), 1e-6)
    assert_function("t0_c_031.v", "t0_c_031", "v", lambda t: num_derivative(x031, t))
    assert_function("t0_c_033.v", "t0_c_033", "v", v033)

    assert_close(errors, "t0_c_025.value_b", field(exercises, "t0_c_025", "value_b"), num_derivative(lambda x: 5 * x**2 - 3 * x + 2, 1.0), 1e-6)
    assert_close(errors, "t0_c_025.value_d", field(exercises, "t0_c_025", "value_d"), num_derivative(lambda x: 6 / x**2, 2.0), 1e-6)
    assert_close(errors, "t0_c_026.integral_c", field(exercises, "t0_c_026", "integral_c"), num_integral(lambda x: 2 * x + 3, 1, 2), 1e-6)
    assert_close(errors, "t0_c_026.x_2", field(exercises, "t0_c_026", "x_2"), 1 + num_integral(lambda t: 4 * t, 0, 2), 1e-6)
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
