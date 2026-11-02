"""Independent numerical checks for every T1 expected answer.

Each value is recomputed from the statement data with the lesson method (position law, derivative,
condition, root). The script also fails if a numeric or function field is left unchecked, and checks
that the answer rounded to three significant figures is graded as correct.
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.exercise_attempt_service import _functions_equivalent
from services.exercise_bank_loader import load_topic_bank

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "content" / "exercises" / "1bach" / "t1"


def quadratic_roots(a: float, b: float, c: float) -> list[float]:
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    return sorted({(-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)})


def turning_time(v0: float, a: float) -> float:
    """Instant where v = v0 + a t (derivative of the position law) vanishes."""
    return -v0 / a


def mrua(x0: float, v0: float, a: float):
    return lambda t: x0 + v0 * t + 0.5 * a * t * t


def three_sig_figs(value: float) -> float:
    if value == 0:
        return 0.0
    return round(value, 2 - int(math.floor(math.log10(abs(value)))))


# Every checked numeric answer: (exercise, field) -> independently computed value.
def expected_values() -> dict[tuple[str, str], float]:
    E: dict[tuple[str, str], float] = {}

    def put(eid, **values):
        for fid, value in values.items():
            E[(eid, fid)] = value

    # r · reference and position
    put("t1_r_001", xa=-300, xb=500, dx=-300 - 500, d=abs(-300 - 500))
    put("t1_r_002", dx=1 - (-4), d=abs(9 + 4) + abs(1 - 9), vm=(1 + 4) / 7, um=(13 + 8) / 7)
    v = (0 + 6) / 2
    put("t1_r_003", x8=-6 + v * 8)
    put("t1_r_004", x0=18, x4=18 - 2 * 4, x10=18 - 2 * 10, t0=18 / 2, v=-2)
    put("t1_r_005", vp=-4, dx=(10 + 4 * 5) - 10, dxp=(30 - (10 + 20)) - (30 - 10), d=20)
    put("t1_r_006", va=3 - 1 * 1, vb=-2 - 1 * 1)
    put("t1_r_007", x_t0=2, x_t2=2 + 3 * 2, x_t4=2 + 3 * 4, x_t6=2 + 3 * 4)
    put("t1_r_008", vg=(16 - 8) / 4, xf=8 - 2 * 4)

    # u · MRU
    put("t1_u_001", x7=-24 + 6 * 7, t=(90 + 24) / 6)
    v = (6 - 30) / (8 - 2)
    put("t1_u_002", v=v, x0=30 - v * 2, x10=30 - v * 2 + v * 10)
    put("t1_u_003", t=90 / 6, x=4 * 90 / 6, db=90 - (90 - 2 * 15))
    t = 5 * 8 / (5 - 3)
    put("t1_u_004", t=t, tb=t - 8, x=3 * t)
    va, vb = 18 / 3.6, -12 / 3.6
    t = 1200 / (va - vb)
    put("t1_u_005", va=va, vb=vb, t=t, x=va * t)
    put("t1_u_006", vrel=10 - 6, t=30 / 4)
    put("t1_u_007", dur=840 / 1.75, ts=300 - 840 / 1.75, x0=1.75 * (0 - (300 - 840 / 1.75)))
    v = (900 - 2400) / 150
    put("t1_u_008", v=v, t=-2400 / v)
    put("t1_u_009", t=(180 + 120) / 15)
    t_home = 50 + 2 * 30 / 1.5
    put("t1_u_010", tt=t_home, vm=0, um=(2 * 30 * 2) / t_home)
    put("t1_u_011", root=30 / (4 - 6), sep=30 + 6 * 5 - 4 * 5)
    x = 60 + 2 * 25
    put("t1_u_012", x=x, vb=x / (25 - 5))

    # a · MRUA and vertical motion
    x = mrua(5, -4, 2)
    put("t1_a_001", x3=x(3), v3=-4 + 2 * 3)
    a = (-3 - (-12)) / 6
    put("t1_a_002", a=a, dx=mrua(0, -12, a)(6))
    tf = turning_time(24, -6)
    put("t1_a_003", tf=tf, d=mrua(0, 24, -6)(tf), x6=mrua(0, 24, -6)(tf))
    x = mrua(0, 0, 1.6)
    put("t1_a_004", x2=x(2), x4=x(4), d24=x(4) - x(2), ratio=(x(4) - x(2)) / x(2))
    x = mrua(-2, 8, -2)
    tg = turning_time(8, -2)
    put("t1_a_005", tg=tg, xg=x(tg), xf=x(7), dx=x(7) - x(0), d=(x(tg) - x(0)) + (x(tg) - x(7)))
    v0 = (28 - 4 - 0.5 * (-1) * 16) / 4
    put("t1_a_006", v0=v0, vf=v0 - 4, dx=28 - 4)
    t = max(quadratic_roots(-5, 0, 45))
    put("t1_a_007", t=t, v=-10 * t, speed=10 * t)
    y = mrua(0, 16, -10)
    up = turning_time(16, -10)
    flight = max(quadratic_roots(-5, 16, 0))
    put("t1_a_008", up=up, h=y(up), flight=flight, v=16 - 10 * flight, d=2 * y(up))
    # y_A - y_B = 20 - 5 (2t - 1) = 0
    t = 25 / 10
    put("t1_a_009", t=t, y=mrua(0, 20, -10)(t), va=20 - 10 * t, vb=20 - 10 * (t - 1))
    put("t1_a_010", v2=2 * 2, v5=2 * 2, y5=mrua(0, 0, 2)(2) + 4 * 3)
    put("t1_a_011", x0=7, v0=-6, a=2 * 1.5, t=turning_time(-6, 3), x=mrua(7, -6, 3)(turning_time(-6, 3)))
    put("t1_a_012", x2=mrua(-3, 2, 4)(2))
    tau = turning_time(18, -4.5)
    put("t1_a_013", dr=18 * 0.75, df=mrua(0, 18, -4.5)(tau), total=18 * 0.75 + mrua(0, 18, -4.5)(tau), time=0.75 + tau)
    vmax = max(quadratic_roots(1 / 10, 1, -55))
    put("t1_a_014", d25=25 * 1 + mrua(0, 25, -5)(turning_time(25, -5)), vmax=vmax, kmh=vmax * 3.6)

    # g · slopes
    put("t1_g_001", v1=(10 + 2) / 3, v2=0, v3=(2 - 10) / 4, dx=2 + 2, d=12 + 8)
    put("t1_g_002", d1=2 * 4, d2=2 * 4 + 0.5 * 4 * 4, x8=-5 + 8 + 16, a=(6 - 2) / 4)
    x = mrua(3, 6, -2)
    put("t1_g_003", turn=turning_time(6, -2), dx=x(5) - x(0), d=(x(3) - x(0)) + (x(3) - x(5)), x5=x(5))
    v2 = -3 + 2 * 2
    put("t1_g_004", v2=v2, v5=v2 - 1 * 3, t1=turning_time(-3, 2), t2=2 + turning_time(v2, -1))
    put("t1_g_005", v_mid=0, v_last=-2, d=4 + 4)
    put("t1_g_006", a1=(4 + 2) / 2, a2=0, a3=(0 - 4) / 2, x7=0.5 * (-2 + 4) * 2 + 4 * 3 + 0.5 * 2 * 4)
    put("t1_g_007", x3=mrua(1, 2, 2)(3))
    put("t1_g_008", v1=0, v2=(1 - 5) / 2, v3=(5 - 1) / 2, d=4 + 4, dx=0)

    # g · areas and models
    v = (19 - 7) / 3
    x0 = 7 - v
    put("t1_g_009", prediction=x0 + 6 * v, residual=26 - (x0 + 6 * v))
    # 2 v0 + 2 a = 8 and v0 + 2 a = 6
    a = 6 - 8 / 2
    v0 = 4 - a
    put("t1_g_010", a=a, v0=v0, x4=mrua(2, v0, a)(4))
    put("t1_g_011", dx_given=4 * 3, dx_area=0.5 * 3 * 6)
    put("t1_g_012", a=-1, speed1=abs(3 - 1), speed5=abs(3 - 5))
    x8 = mrua(15, 4, -2)(3)
    put("t1_g_013", turn=5 + turning_time(4, -2), xf=x8 - 2 * 2,
        distance=(mrua(15, 4, -2)(2) - (-1)) + (mrua(15, 4, -2)(2) - (x8 - 4)))
    a = (-4 - 2) / 3
    v0 = 2 - a * 1
    x0 = 5 - (v0 * 1 + 0.5 * a)
    put("t1_g_014", a=a, v0=v0, x0=x0, x4=mrua(x0, v0, a)(4))
    put("t1_g_015", t=60 / 8, x=-10 + 4 * 60 / 8, ta=10 / 4, tb=50 / 4)
    xg = mrua(-6, -3, 2)(turning_time(-3, 2))
    put("t1_g_016", x2=-6, xg=xg, x7=mrua(-6, -3, 2)(3) + 3 * 2, d=2 * abs(xg))

    # i · integrated problems
    vc = 0.8 * 25
    tb = turning_time(vc, -1)
    d = mrua(0, 0, 0.8)(25) + vc * 120 + mrua(0, vc, -1)(tb)
    put("t1_i_001", time=25 + 120 + tb, d=d, mean=d / (25 + 120 + tb))
    t = (90 + 7.5 * 20) / (7.5 - 1.5)
    put("t1_i_002", t=t, x=1.5 * t, dc=1.5 * t + 90)
    brake = mrua(10, 20, -4)
    tau = min(r for r in quadratic_roots(-2, 20, 10 - 50) if 0 <= r <= turning_time(20, -4))
    put("t1_i_003", stop=brake(turning_time(20, -4)), impact_time=0.5 + tau, impact_v=20 - 4 * tau)
    y = mrua(25, 15, -10)
    t = max(quadratic_roots(-5, 15, 25))
    put("t1_i_004", max=y(1.5), t=t, v=15 - 10 * t, distance=(y(1.5) - 25) + y(1.5))
    vmax = 1.2 * 3
    tau = turning_time(vmax, -0.9)
    put("t1_i_005", vmax=vmax, duration=7 + tau,
        height=mrua(0, 0, 1.2)(3) + vmax * 4 + mrua(0, vmax, -0.9)(tau), v=vmax - 0.9 * tau)
    # x0 = 2; v0 + a/2 = 3; 2 v0 + 2 a = 8
    a = (8 - 2 * 3) / (2 - 1)
    v0 = 3 - a / 2
    x = mrua(2, v0, a)
    put("t1_i_006", v0=v0, a=a, res3=18 - x(3), res4=26 - x(4))
    put("t1_i_007", arr=0.5 * 4 * 12, brake=0.5 * 6 * 12, xf=24 + 12 * 6 + 36, equal=2 * 24 / 12)
    t = max(quadratic_roots(1, -5, -25))
    assert t < turning_time(20, -2)
    put("t1_i_008", t=t, x=-25 + 15 * t, va=20 - 2 * t)
    put("t1_i_009", da=mrua(0, 12, -12 / 3)(3), db=mrua(0, 12, -12 / 6)(6),
        xa4=mrua(0, 12, -4)(3), xb4=mrua(0, 12, -2)(4))
    delivery = mrua(0, 0, 1)(4) + 4 * 6
    total = 15 + delivery / 2
    put("t1_i_010", delivery=delivery, distance=2 * delivery, time=total, mean=2 * delivery / total, velocity=0)
    return E


# Every function field: (exercise, field) -> independent function of t.
FUNCTIONS = {
    ("t1_r_003", "func"): lambda t: -6 + 3 * t,
    ("t1_r_005", "xp"): lambda t: 30 - (10 + 4 * t),
    ("t1_r_007", "func"): lambda t: 2 + 3 * t,
    ("t1_r_008", "correct"): lambda t: 8 - 2 * t,
    ("t1_u_001", "x"): lambda t: -24 + 6 * t,
    ("t1_u_002", "x"): lambda t: 38 - 4 * t,
    ("t1_u_003", "a"): lambda t: 4 * t,
    ("t1_u_003", "b"): lambda t: 90 - 2 * t,
    ("t1_u_006", "rel"): lambda t: (-10 + 10 * t) - (20 + 6 * t),
    ("t1_u_007", "x"): lambda t: 1.75 * (t + 180),
    ("t1_u_008", "x"): lambda t: 2400 - 10 * t,
    ("t1_u_009", "front"): lambda t: 15 * t,
    ("t1_u_009", "rear"): lambda t: 15 * t - 120,
    ("t1_u_012", "b"): lambda t: 5.5 * (t - 5),
    ("t1_a_001", "x"): mrua(5, -4, 2),
    ("t1_a_001", "v"): lambda t: -4 + 2 * t,
    ("t1_a_003", "x"): mrua(0, 24, -6),
    ("t1_a_007", "y"): mrua(45, 0, -10),
    ("t1_a_010", "y"): mrua(0, 0, 2),
    ("t1_g_003", "x"): mrua(3, 6, -2),
    ("t1_g_005", "v"): lambda t: 2 * t,
    ("t1_g_009", "fit"): lambda t: 3 + 4 * t,
    ("t1_g_010", "x"): mrua(2, 2, 2),
    ("t1_g_014", "x"): mrua(2, 4, -2),
    ("t1_i_006", "model"): mrua(2, 2, 2),
}

CHOICES = {
    ("t1_r_006", "motion_a"): "forward_slower",
    ("t1_r_006", "motion_b"): "back_faster",
    ("t1_u_007", "hora"): "h0957",
    ("t1_u_011", "meeting"): "no",
    ("t1_a_012", "model"): "B",
    ("t1_g_007", "trio"): "A",
    ("t1_g_009", "compatible"): "no",
    ("t1_g_011", "correct"): "quadratic",
    ("t1_g_012", "trend"): "up",
}


def validate_math() -> list[str]:
    exercises = load_topic_bank(BANK_PATH)["exercises"]
    expected = expected_values()
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for exercise in exercises:
        for field in exercise["response_fields"]:
            key = (exercise["id"], field["id"])
            label = f"{key[0]}.{key[1]}"
            if field["type"] == "numeric":
                if key not in expected:
                    errors.append(f"{label}: numeric field without an independent check")
                    continue
                seen.add(key)
                value, tolerance = float(field["expected_value"]), float(field["tolerance"])
                if abs(value - expected[key]) > max(1e-6, 1e-9 * abs(value)) and abs(value - expected[key]) > tolerance / 10:
                    errors.append(f"{label}: stored {value}, recomputed {expected[key]}")
                if abs(three_sig_figs(expected[key]) - value) > tolerance + 1e-12:
                    errors.append(f"{label}: 3 s.f. answer {three_sig_figs(expected[key])} is outside tolerance {tolerance}")
            elif field["type"] == "function":
                function = FUNCTIONS.get(key)
                if function is None:
                    errors.append(f"{label}: function field without an independent check")
                    continue
                seen.add(key)
                forms = [field["canonical_expression"], *field.get("accepted_forms", [])]
                for form in forms:
                    for t in (0.0, 1.0, 2.5, 4.0):
                        given = eval(form.replace("^", "**"), {"__builtins__": {}}, {"t": t})  # noqa: S307 - trusted bank text
                        if abs(given - function(t)) > 1e-9:
                            errors.append(f"{label}: {form} differs from the recomputed law at t={t}")
                            break
                    if not _functions_equivalent(form, field["canonical_expression"]):
                        errors.append(f"{label}: accepted form {form} is not graded as equivalent")
                if "**" in field["canonical_expression"]:
                    errors.append(f"{label}: use ^ for powers")
            elif field["type"] == "single_choice":
                if CHOICES.get(key) != field["correct_option_id"]:
                    errors.append(f"{label}: correct option {field['correct_option_id']} not confirmed")
                seen.add(key)
            else:
                errors.append(f"{label}: unexpected field type {field['type']}")
    missing = set(expected) - seen
    if missing:
        errors.append(f"checks for fields that no longer exist: {sorted(missing)}")
    return errors


def main() -> int:
    errors = validate_math()
    if errors:
        print("T1 mathematical validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    count = len(expected_values()) + len([k for k in FUNCTIONS if k[1]]) + len(CHOICES)
    print(f"T1 mathematical validation passed ({count} fields checked).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
