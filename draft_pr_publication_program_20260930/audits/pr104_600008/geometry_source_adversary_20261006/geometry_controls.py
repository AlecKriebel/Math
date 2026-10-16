#!/usr/bin/env python3
"""Independent standard-library geometry controls; numerical checks are diagnostic.

Run: python3 geometry_controls.py
The tiny polynomial kernel proves the stated rational identities exactly, without
the original author's checker or a symbolic-algebra dependency.
"""
from fractions import Fraction
from itertools import product
from math import atan2, cos, gcd, hypot, lcm, pi, sin, sqrt
from pathlib import Path
import json

NV = 5
ZERO = (0,) * NV


class P:
    def __init__(self, value=0):
        self.d = ({ZERO: Fraction(value)} if value else {}) if not isinstance(value, dict) else {k: Fraction(v) for k, v in value.items() if v}

    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        d = dict(self.d)
        for k, v in other.d.items():
            d[k] = d.get(k, 0) + v
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.d.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, P) else -P(other))

    def __rsub__(self, other):
        return P(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, P) else P(other)
        d = {}
        for k1, v1 in self.d.items():
            for k2, v2 in other.d.items():
                k = tuple(x + y for x, y in zip(k1, k2))
                d[k] = d.get(k, 0) + v1 * v2
        return P(d)

    __rmul__ = __mul__

    def __pow__(self, power):
        out = P(1)
        for _ in range(power):
            out = out * self
        return out


def var(i):
    key = tuple(int(j == i) for j in range(NV))
    return P({key: 1})


a, b, c, v, w = map(var, range(NV))
D = (a + c) * (b + c)
F = b + (a - b) * w
identities = {
    "ellipsoid_after_multiplication_by_D": (a + v) * (1 - w) * (b + c) + (b + v) * w * (a + c) + (c + F) * (c - v) - D,
    "normal_Q_equals_Fv_over_abc": b * c * (a + v) * (1 - w) * (b + c) + a * c * (b + v) * w * (a + c) - a * b * (c + F) * (c - v) - F * v * D,
    "metric_cross_coefficient": -a * (b + c) + b * (a + c) + c * (a - b),
    "metric_tt_after_clearing_denominators": a * (a + v) * w * (b + c) * (c + F) + b * (b + v) * (1 - w) * (a + c) * (c + F) - c * (c - v) * (a - b) ** 2 * w * (1 - w) - (v + F) * F * D,
    "metric_vv_after_clearing_denominators": a * (1 - w) * (b + c) * (c - v) * (b + v) + b * w * (a + c) * (c - v) * (a + v) - c * (c + F) * (a + v) * (b + v) + (v + F) * v * D,
}
for name, polynomial in identities.items():
    assert not polynomial.d, (name, polynomial.d)


def simpson(f, left, right, count=8192):
    assert count % 2 == 0
    h = (right - left) / count
    return h / 3 * (f(left) + f(right) + sum((4 if k % 2 else 2) * f(left + k * h) for k in range(1, count)))


def periods(aa, bb, cc):
    LL = simpson(lambda t: sqrt((aa * sin(t) ** 2 + bb * cos(t) ** 2) / (cc + aa * sin(t) ** 2 + bb * cos(t) ** 2)), 0.0, 2 * pi)
    # v=c sin²(phi): this removes both endpoint square roots.
    II = simpson(lambda phi: 2 * cc * sin(phi) ** 2 / sqrt((aa + cc * sin(phi) ** 2) * (bb + cc * sin(phi) ** 2)), 0.0, pi / 2)
    return LL, II


period_cases = [(1, 1, 3), (1, 1, 8), (1, 1, 16 / 9), (9, 1, 2), (1, 9, 2), (1e-3, 7, 2e-2), (7, 1e-3, 2e3), (2, 2 * (1 + 1e-10), 5), (2, 5, 1e-8), (2, 5, 1e6)]
period_results = []
for aa, bb, cc in period_cases:
    LL, II = periods(aa, bb, cc)
    defect = II + LL / 2 - pi
    # Tight tolerance is used for ordinary cases; extreme anisotropy can need
    # a finer mesh, which is diagnostic quadrature, not a validated enclosure.
    if abs(defect) > 1e-9:
        LL = simpson(lambda t: sqrt((aa * sin(t) ** 2 + bb * cos(t) ** 2) / (cc + aa * sin(t) ** 2 + bb * cos(t) ** 2)), 0, 2 * pi, 262144)
        II = simpson(lambda phi: 2 * cc * sin(phi) ** 2 / sqrt((aa + cc * sin(phi) ** 2) * (bb + cc * sin(phi) ** 2)), 0, pi / 2, 262144)
        defect = II + LL / 2 - pi
    assert abs(defect) < 1e-8, (aa, bb, cc, defect)
    period_results.append({"a": aa, "b": bb, "c": cc, "L": LL, "Iv": II, "Iv_plus_L_over_2_minus_pi": defect, "positive_path_rotation": II / LL})


# Generate points from the ordinary ellipsoid latitude parameterization,
# independently of the submitted confocal coordinates. Reconstruct the belt.
coverage_count, axis_count, tropic_count = 0, 0, 0
max_reconstruction_error = 0.0
for aa, bb, cc in product([0.125, 1.0, 9.0], repeat=3):
    DD = (aa + cc) * (bb + cc)
    for theta in [0, pi / 7, pi / 2, pi, 8 * pi / 7, 3 * pi / 2]:
        A = cos(theta) ** 2 / aa + sin(theta) ** 2 / bb
        tropic_z2 = cc * cc * A / (1 + cc * A)
        for zfraction in [-1, -0.75, 0, 0.75, 1]:
            zz = zfraction * sqrt(tropic_z2)
            xx = sqrt(aa * (1 - zz * zz / cc)) * cos(theta)
            yy = sqrt(bb * (1 - zz * zz / cc)) * sin(theta)

            def root(value):
                return (aa + cc) * xx * xx / (aa * (aa + value)) + (bb + cc) * yy * yy / (bb * (bb + value))

            low, high = 0.0, cc
            for _ in range(100):
                mid = (low + high) / 2
                if root(mid) > 1:
                    low = mid
                else:
                    high = mid
            vv = (low + high) / 2
            tt = atan2(yy / sqrt(bb * (bb + vv) / (bb + cc)), xx / sqrt(aa * (aa + vv) / (aa + cc)))
            ff = aa * sin(tt) ** 2 + bb * cos(tt) ** 2
            recx = sqrt(aa * (aa + vv) / (aa + cc)) * cos(tt)
            recy = sqrt(bb * (bb + vv) / (bb + cc)) * sin(tt)
            recz = (-1 if zz < 0 else 1) * sqrt(max(0.0, cc * (cc + ff) * (cc - vv) / DD))
            error = max(abs(recx - xx) / sqrt(aa), abs(recy - yy) / sqrt(bb), abs(recz - zz) / sqrt(cc))
            # At the equator square-root inversion loses a few digits.
            assert error < 1e-7, (aa, bb, cc, theta, zfraction, error)
            max_reconstruction_error = max(max_reconstruction_error, error)
            coverage_count += 1
            axis_count += abs(sin(theta) * cos(theta)) < 1e-14
            tropic_count += abs(zfraction) == 1


count_cases = []
for pp, qq in product(range(1, 17), repeat=2):
    if gcd(pp, qq) != 1:
        continue
    rr = Fraction(pp, qq)
    folded = next(k for k in range(1, 2 * qq + 1) if (k * rr).denominator == 1)
    full = next(k for k in range(1, 2 * qq + 1) if k % 2 == 0 and (k * rr).denominator == 1)
    assert folded == qq and full == lcm(2, qq)
    if (pp, qq) in [(1, 1), (1, 2), (1, 3), (2, 3), (3, 4)]:
        count_cases.append({"rho": str(rr), "equator_least_iterations": folded, "full_chain_least_arcs": full, "full_chain_winding": int(full * rr), "axisymmetric_a": 1, "axisymmetric_c": str((1 + 2 * rr) ** 2 - 1)})

out = {
    "status": "PASS",
    "exact_polynomial_identities": list(identities),
    "polynomial_method": "Expansion over rational coefficients in five independent indeterminates a,b,c,v,w; each residual dictionary is empty.",
    "diagnostic_period_cases": period_results,
    "diagnostic_coverage": {"points": coverage_count, "axis_points": axis_count, "tropic_points": tropic_count, "max_scaled_reconstruction_error": max_reconstruction_error},
    "count_examples": count_cases,
    "limitations": "Exact identities and exact period arithmetic are proofs of those checks. Floating quadrature and inverse controls are diagnostics; globality, seam regularity, geodesic classification and contour identity require the written reasoning in REPORT.md.",
}
print(json.dumps(out, indent=2, sort_keys=True))
