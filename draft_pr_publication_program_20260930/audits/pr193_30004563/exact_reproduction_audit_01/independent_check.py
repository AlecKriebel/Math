#!/usr/bin/env python3
"""Independent rational interval audit; Python standard library only.

Written from CANDIDATE equations before inspecting the submitted verifier.
Every proof comparison uses Fraction/int. Outputs stay beside this script.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
from pathlib import Path
import json

COUNTS = Counter()
ROOT_BITS = 224
GRID = 1 << ROOT_BITS
BOUNDARY_STEPS = 192
CENTER_STEPS = 112


def require(condition, category):
    COUNTS[category] += 1
    if not condition:
        raise ArithmeticError(category)


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self):
        object.__setattr__(self, "lo", F(self.lo))
        object.__setattr__(self, "hi", F(self.hi))
        if self.lo > self.hi:
            raise ValueError("backward interval")

    @staticmethod
    def of(x):
        return x if isinstance(x, I) else I(x, x)

    def __add__(self, other):
        o = I.of(other)
        return I(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -I.of(other)

    def __rsub__(self, other):
        return I.of(other) + -self

    def __mul__(self, other):
        o = I.of(other)
        values = [self.lo * o.lo, self.lo * o.hi,
                  self.hi * o.lo, self.hi * o.hi]
        return I(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = I.of(other)
        if o.lo <= 0 <= o.hi:
            raise ZeroDivisionError("divisor includes zero")
        return self * I(1 / o.hi, 1 / o.lo)

    def square(self):
        vals = (self.lo * self.lo, self.hi * self.hi)
        return I(0 if self.lo <= 0 <= self.hi else min(vals), max(vals))

    def nonnegative_power(self, n):
        if self.lo < 0 or not isinstance(n, int) or n < 1:
            raise ValueError("nonnegative power precondition")
        return I(self.lo ** n, self.hi ** n)

    def sign(self):
        if self.lo > 0:
            return 1
        if self.hi < 0:
            return -1
        raise ArithmeticError("unresolved strict sign")


def integer_eighth_floor(m):
    """Binary search using direct eighth powers, independently of isqrt."""
    if m < 0:
        raise ValueError("negative radicand")
    if m == 0:
        return 0
    lower = 0
    upper = 1 << ((m.bit_length() + 7) // 8)
    while upper - lower > 1:
        middle = (lower + upper) // 2
        if middle ** 8 <= m:
            lower = middle
        else:
            upper = middle
    return lower


def validate_root_cell(q, k):
    """These are direct integer inequalities for a rational q, not float tests."""
    q = F(q)
    require(q >= 0 and k >= 0, "root_cell_nonnegative")
    target = q.numerator * GRID ** 8
    require(k ** 8 * q.denominator <= target, "root_integer_lower")
    require(target < (k + 1) ** 8 * q.denominator, "root_integer_upper_strict")


def root_endpoint(q):
    q = F(q)
    if q == 0:
        require(q == 0, "root_exact_zero")
        return I(0, 0)
    if q < 0:
        raise ValueError("negative radicand")
    k = integer_eighth_floor((q.numerator * GRID ** 8) // q.denominator)
    validate_root_cell(q, k)
    return I(F(k, GRID), F(k + 1, GRID))


def eighth_root(q):
    q = I.of(q)
    if q.lo < 0:
        raise ValueError("root interval includes negative values")
    a = root_endpoint(q.lo)
    if q.lo == q.hi:
        return a
    b = root_endpoint(q.hi)
    return I(a.lo, b.hi)


def norm2(p):
    return p[0].square() + p[1].square()


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def point(x, y):
    return (I.of(x), I.of(y))


def distance16(p, q):
    return norm2(sub(p, q)).nonnegative_power(8)


def disjoint(p, q):
    return any(a.hi < b.lo or b.hi < a.lo for a, b in zip(p, q))


def strictly_inside(box, lower, upper, category):
    require(F(lower) < box.lo <= box.hi < F(upper), category)


def outgoing(s):
    u = eighth_root(s)
    v = eighth_root(I.of(s) + lam)
    w = eighth_root(I.of(s) + 1)
    x = (b * b + u - v) / (2 * b)
    y = (c * c + d * d + u - w - 2 * c * x) / (2 * d)
    return (x, y), x.square() + y.square() - u


def boundary_polynomial(qx, qy, h, level, t):
    magnitude16 = (qx * qx + qy * qy) ** 8
    return magnitude16 * (((t - 1) ** 2 + h * h) ** 8
                          - (t * t + h * h) ** 8) - level


def isolate_boundary(qx, qy, h, level):
    require(qx * qx + qy * qy > 0 and h != 0, "boundary_strict_convexity_parameters")
    left, right = F(-16), F(16)
    fn = lambda t: boundary_polynomial(qx, qy, h, level, t)
    require(fn(left) > 0 and fn(right) < 0, "boundary_initial_bracket")
    for _ in range(BOUNDARY_STEPS):
        middle = (left + right) / 2
        value = fn(middle)
        require(value != 0, "boundary_midpoint_nonzero")
        if value > 0:
            left = middle
        else:
            right = middle
    fl, fr = fn(left), fn(right)
    require(fl > 0, "boundary_final_left_positive")
    require(fr < 0, "boundary_final_right_negative")
    t = I(left, right)
    coords = (qx * t - h * qy, qy * t + h * qx)
    return coords, {"qx": qx, "qy": qy, "h": h, "level": level,
                    "t": t, "residual_left": fl, "residual_right": fr}


def incoming(s, boundary):
    a1, a2, a3, a4, a5, a6 = boundary
    level_l = distance16(a4, a5) - distance16(a4, a3)
    level_m = distance16(a2, a1) - distance16(a2, a3)
    require(level_l.lo > 0 and level_m.lo > 0, "incoming_positive_levels")
    bp, cp = sub(a5, a3), sub(a1, a3)
    determinant = det(bp, cp)
    require(determinant.sign() != 0, "incoming_invertible")
    u = eighth_root(s)
    v, w = eighth_root(I.of(s) + level_l), eighth_root(I.of(s) + level_m)
    r1, r2 = norm2(bp) + u - v, norm2(cp) + u - w
    yx = (r1 * cp[1] - r2 * bp[1]) / (2 * determinant)
    yy = (bp[0] * r2 - cp[0] * r1) / (2 * determinant)
    z = (a3[0] + yx, a3[1] + yy)
    return z, yx.square() + yy.square() - u, level_l, level_m, determinant


def encode(x):
    if isinstance(x, F):
        return {"n": str(x.numerator), "d": str(x.denominator)}
    if isinstance(x, I):
        return {"lo": encode(x.lo), "hi": encode(x.hi)}
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def expect_rejection(fn, label):
    try:
        fn()
    except (ArithmeticError, ValueError, ZeroDivisionError):
        return {"control": label, "rejected": True}
    raise ArithmeticError("false control accepted: " + label)


def basic_tests():
    require(I(-2, 3).square() == I(0, 9), "interval_self_test")
    require(I(-3, -2).square() == I(4, 9), "interval_self_test")
    require(I(-2, 3) * I(-4, 5) == I(-12, 15), "interval_self_test")
    require(I(-3, -2) / I(-4, -2) == I(F(1, 2), F(3, 2)), "interval_self_test")
    require(eighth_root(0) == I(0, 0), "interval_self_test")
    require(eighth_root(1).lo == 1 and eighth_root(1).hi > 1, "interval_self_test")
    for n in [0, 1, 2, 255, 256, 257, 10 ** 40]:
        k = integer_eighth_floor(n)
        require(k ** 8 <= n < (k + 1) ** 8, "integer_root_self_test")
    return [
        expect_rejection(lambda: validate_root_cell(F(1), GRID + 1), "root lower cell shifted up"),
        expect_rejection(lambda: validate_root_cell(F(1), GRID - 2), "root upper cell shifted down to exclude root"),
        expect_rejection(lambda: eighth_root(I(-1, 1)), "negative radicand interval"),
        expect_rejection(lambda: I(1, 2) / I(-1, 1), "zero divisor interval"),
        expect_rejection(lambda: I(-1, 1).sign(), "non-strict sign interval"),
    ]


b, c, d, lam = F(2073, 10000), F(4719, 10000), F(64, 10000), F(27, 1250)


def main():
    controls = basic_tests()
    a, bb, cc = point(0, 0), point(b, 0), point(c, d)
    determinant_even = det(sub(bb, a), sub(cc, a))
    require(determinant_even == I(F(132672, 100000000), F(132672, 100000000)), "even_determinant")
    require(b ** 16 != lam, "origin_not_outgoing_center")
    parameters = [F(9, 10000), F(11, 10000), F(13, 10000), F(1, 2), F(1), F(10 ** 17)]
    coarse = [(F(38, 100), F(39, 100)), (F(-28, 100), F(-27, 100)),
              (F(51, 100), F(52, 100)), (F(-91, 100), F(-90, 100)),
              (F(9), F(10)), (F(-39), F(-38))]
    samples = []
    for s, bounds in zip(parameters, coarse):
        xy, value = outgoing(s)
        strictly_inside(value, *bounds, "G_coarse_claim")
        samples.append({"s": s, "G": value, "xy": xy, "sign": value.sign()})
    for first, second in zip(samples, samples[1:]):
        require(first["s"] < second["s"] and first["sign"] * second["sign"] == -1,
                "G_five_alternating_brackets")
    controls.append(expect_rejection(lambda: require(samples[0]["G"].hi < 0, "forged_G_sign"),
                                     "reversed positive outgoing sign"))
    controls.append(expect_rejection(lambda: strictly_inside(samples[-1]["G"], -38, -37, "forged_large_s_enclosure"),
                                     "false large-s coarse enclosure"))

    a1, cert1 = isolate_boundary(c, d, F(10), F(1))
    a3, cert3 = isolate_boundary(b, F(0), F(1), lam)
    temp5, cert5 = isolate_boundary(c - b, d, F(-10), 1 - lam)
    a5 = (temp5[0] + b, temp5[1])
    boundary = (a1, a, a3, bb, a5, cc)
    coarse_boundary = [
        (a1[0], "0.17194", "0.17196"), (a1[1], "4.72219", "4.72221"),
        (a3[0], "-0.55229", "-0.55227"),
        (a5[0], "0.40359", "0.40361"), (a5[1], "-2.64281", "-2.64279")]
    for v, left, right in coarse_boundary:
        strictly_inside(v, left, right, "boundary_coarse_claim")
    require(a3[1] == I(b, b), "A3_y_exact")
    determinants_boundary = []
    for indices in combinations(range(6), 3):
        p, q, r = [boundary[j] for j in indices]
        value = det(sub(q, p), sub(r, p))
        require(value.sign() != 0, "all_boundary_triples_noncollinear")
        determinants_boundary.append({"vertices": [j + 1 for j in indices], "det": value})
    for j, k in combinations(range(6), 2):
        require(disjoint(boundary[j], boundary[k]), "all_boundary_pairs_distinct")
    odd_det = det(sub(a3, a1), sub(a5, a1))
    strictly_inside(odd_det, "6.37", "6.39", "odd_determinant_coarse_claim")
    a3_residual = distance16(a3, cc) - distance16(a3, a) - 1
    strictly_inside(a3_residual, "0.98", "0.99", "A3_not_outgoing_center")
    controls.append(expect_rejection(lambda: require(cert1["residual_left"] < 0, "forged_boundary_sign"),
                                     "reversed algebraic-root left sign"))

    centers = []
    for j in range(5):
        left, right = parameters[j:j+2]
        sign_left, sign_right = samples[j]["sign"], samples[j+1]["sign"]
        for _ in range(CENTER_STEPS):
            midpoint = (left + right) / 2
            middle_sign = outgoing(midpoint)[1].sign()
            require(middle_sign in (-1, 1), "G_bisection_strict_decision")
            if middle_sign == sign_left:
                left = midpoint
            else:
                require(middle_sign == sign_right, "G_bisection_opposite_side")
                right = midpoint
        left_g, right_g = outgoing(left)[1], outgoing(right)[1]
        require(left_g.sign() == sign_left and right_g.sign() == sign_right,
                "G_retained_sign_bracket")
        xy = outgoing(I(left, right))[0]
        line_dets = []
        for k, ell in combinations(range(6), 2):
            value = det(sub(boundary[ell], boundary[k]), sub(xy, boundary[k]))
            require(value.sign() != 0, "outgoing_avoids_boundary_lines")
            line_dets.append({"pair": [k + 1, ell + 1], "det": value})
        for vertex in boundary:
            require(disjoint(xy, vertex), "outgoing_disjoint_boundary_boxes")
        centers.append({"s": I(left, right), "G_left": left_g, "G_right": right_g,
                        "xy": xy, "line_determinants": line_dets})
    for j, k in combinations(range(5), 2):
        require(centers[j]["s"].hi < centers[k]["s"].lo,
                "outgoing_retained_brackets_disjoint")
        require(disjoint(centers[j]["xy"], centers[k]["xy"]), "outgoing_coordinate_boxes_disjoint")

    incoming_samples = []
    for s, bounds in [(F(1, 100), ("0.00037", "0.00038")),
                      (F(11, 1000), ("-0.00081", "-0.00080"))]:
        z, hval, level_l, level_m, incdet = incoming(s, boundary)
        strictly_inside(hval, *bounds, "H_coarse_claim")
        incoming_samples.append({"s": s, "H": hval, "Z": z})
    require(incoming_samples[0]["H"].sign() * incoming_samples[1]["H"].sign() == -1,
            "H_strict_sign_change")
    incoming_s = I(F(1, 100), F(11, 1000))
    z, _, level_l, level_m, incdet = incoming(incoming_s, boundary)
    strictly_inside(z[0], "0.1677", "0.1717", "incoming_x_coarse_claim")
    strictly_inside(z[1], "-0.0036", "-0.0026", "incoming_y_coarse_claim")
    for vertex in boundary:
        require(disjoint(z, vertex), "incoming_disjoint_boundary_boxes")
    incoming_line_dets = []
    for j, k in combinations(range(6), 2):
        value = det(sub(boundary[k], boundary[j]), sub(z, boundary[j]))
        require(value.sign() != 0, "incoming_avoids_boundary_lines")
        incoming_line_dets.append({"pair": [j + 1, k + 1], "det": value})
    controls.append(expect_rejection(lambda: require(incoming_samples[1]["H"].lo > 0, "forged_H_sign"),
                                     "reversed incoming negative sign"))
    output = {
        "status": "PASS", "arithmetic": "Python int and Fraction only",
        "root_bits": ROOT_BITS, "boundary_bisections_each": BOUNDARY_STEPS,
        "outgoing_bisections_each": CENTER_STEPS,
        "G_samples": samples, "boundary_parameters": [cert1, cert3, cert5],
        "boundary_boxes": boundary, "boundary_triple_determinants": determinants_boundary,
        "even_determinant": determinant_even, "odd_determinant": odd_det,
        "A3_outgoing_residual": a3_residual, "outgoing_root_brackets": centers,
        "incoming_samples": incoming_samples, "incoming_s": incoming_s,
        "incoming_Z": z, "incoming_L": level_l, "incoming_M": level_m,
        "incoming_determinant": incdet, "incoming_line_determinants": incoming_line_dets,
        "negative_controls": controls,
        "counts": dict(sorted(COUNTS.items())),
        "count_semantics": "require calls by category; includes intentional failing comparisons in rejected controls; distinct mathematical obligations are fewer",
    }
    dest = Path(__file__).resolve().parent / "independent_certificate.json"
    dest.write_text(json.dumps(encode(output), indent=2) + "\n")
    print(json.dumps({"status": "PASS", "outgoing_IVT_brackets": len(centers),
                      "incoming_IVT_brackets": 1, "negative_controls_rejected": len(controls),
                      "require_calls_including_controls": sum(COUNTS.values()),
                      "certificate": dest.name}, sort_keys=True))


if __name__ == "__main__":
    main()
