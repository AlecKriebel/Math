#!/opt/homebrew/bin/python3.11
"""Verify a floating-point interval Krawczyk certificate.

The certified system asks for a real rank-two
factorization C = X Y^T whose site-zero two-copy block Gram is

    beta = B (I_9 + (6/5) |vec I_3><vec I_3|)

and whose two site-zero marginals are scalar.  Fifty-three factor
coordinates are fixed binary rationals, leaving a square system of
56 equations.  Every interval operation is rounded outwards.
"""

from __future__ import annotations

import math
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "verification" / "data" / "n3_isotropic_local_stationary.json"


def down(x):
    return np.nextafter(x, -np.inf)


def up(x):
    return np.nextafter(x, np.inf)


def iadd(al, ah, bl, bh):
    return down(al + bl), up(ah + bh)


def imul(al, ah, bl, bh):
    p0 = al * bl
    p1 = al * bh
    p2 = ah * bl
    p3 = ah * bh
    return down(np.minimum(np.minimum(p0, p1), np.minimum(p2, p3))), up(
        np.maximum(np.maximum(p0, p1), np.maximum(p2, p3))
    )


class AD:
    __slots__ = ("lo", "hi", "dlo", "dhi")

    def __init__(self, lo, hi=None, dlo=None, dhi=None):
        self.lo = float(lo)
        self.hi = float(lo if hi is None else hi)
        if dlo is None:
            self.dlo = np.zeros(56)
            self.dhi = np.zeros(56)
        else:
            self.dlo = np.asarray(dlo, dtype=float)
            self.dhi = np.asarray(dhi, dtype=float)

    @classmethod
    def variable(cls, center: float, radius: float, index: int):
        dlo = np.zeros(56)
        dhi = np.zeros(56)
        dlo[index] = 1.0
        dhi[index] = 1.0
        return cls(
            math.nextafter(center - radius, -math.inf),
            math.nextafter(center + radius, math.inf),
            dlo,
            dhi,
        )

    def __add__(self, other):
        if not isinstance(other, AD):
            other = AD(other)
        lo, hi = iadd(self.lo, self.hi, other.lo, other.hi)
        dlo, dhi = iadd(self.dlo, self.dhi, other.dlo, other.dhi)
        return AD(lo, hi, dlo, dhi)

    __radd__ = __add__

    def __neg__(self):
        return AD(-self.hi, -self.lo, -self.dhi, -self.dlo)

    def __sub__(self, other):
        return self + (-other if isinstance(other, AD) else -AD(other))

    def __rsub__(self, other):
        return AD(other) - self

    def __mul__(self, other):
        if not isinstance(other, AD):
            other = AD(other)
        lo, hi = imul(self.lo, self.hi, other.lo, other.hi)
        xlo, xhi = imul(self.dlo, self.dhi, other.lo, other.hi)
        ylo, yhi = imul(self.lo, self.hi, other.dlo, other.dhi)
        dlo, dhi = iadd(xlo, xhi, ylo, yhi)
        return AD(lo, hi, dlo, dhi)

    __rmul__ = __mul__

    def div_positive_integer(self, denominator: int):
        return AD(
            math.nextafter(self.lo / denominator, -math.inf),
            math.nextafter(self.hi / denominator, math.inf),
            down(self.dlo / denominator),
            up(self.dhi / denominator),
        )


def equations_ad(z: np.ndarray, free: np.ndarray, radius: float):
    lookup = {int(global_index): local for local, global_index in enumerate(free)}
    variables = []
    for global_index, center in enumerate(z):
        if global_index in lookup:
            variables.append(
                AD.variable(float(center), radius, lookup[global_index])
            )
        else:
            variables.append(AD(float(center)))
    x = np.asarray(variables[:54], dtype=object).reshape(3, 9, 2)
    y = np.asarray(variables[54:108], dtype=object).reshape(3, 9, 2)
    scale = variables[108]

    blocks = np.empty((3, 3, 9, 9), dtype=object)
    for a in range(3):
        for p in range(3):
            for i in range(9):
                for j in range(9):
                    blocks[a, p, i, j] = (
                        x[a, i, 0] * y[p, j, 0]
                        + x[a, i, 1] * y[p, j, 1]
                    )

    def b2(a, p, b, q):
        out = AD(0.0)
        for i in range(9):
            for j in range(9):
                out += blocks[a, p, i, j] * blocks[b, q, i, j]
        for site in range(2):
            for i in range(3):
                for j in range(3):
                    left = AD(0.0)
                    right = AD(0.0)
                    for k in range(3):
                        if site == 0:
                            left += blocks[a, p, 3 * k + i, 3 * k + j]
                            right += blocks[b, q, 3 * k + i, 3 * k + j]
                        else:
                            left += blocks[a, p, 3 * i + k, 3 * j + k]
                            right += blocks[b, q, 3 * i + k, 3 * j + k]
                    out -= 0.5 * left * right
        left = AD(0.0)
        right = AD(0.0)
        for i in range(9):
            left += blocks[a, p, i, i]
            right += blocks[b, q, i, i]
        return out + 0.25 * left * right

    beta = np.empty((9, 9), dtype=object)
    for a in range(3):
        for p in range(3):
            for b in range(3):
                for q in range(3):
                    beta[3 * a + p, 3 * b + q] = b2(a, p, b, q)

    out = []
    for row in range(9):
        a, p = divmod(row, 3)
        for col in range(row, 9):
            b, q = divmod(col, 3)
            target = scale * (1.0 if row == col else 0.0)
            if a == p and b == q:
                target += (6.0 * scale).div_positive_integer(5)
            out.append(beta[row, col] - target)

    rho_left = np.empty((3, 3), dtype=object)
    rho_right = np.empty((3, 3), dtype=object)
    for a in range(3):
        for b in range(3):
            value = AD(0.0)
            for p in range(3):
                for i in range(9):
                    for j in range(9):
                        value += blocks[a, p, i, j] * blocks[b, p, i, j]
            rho_left[a, b] = value
    for p in range(3):
        for q in range(3):
            value = AD(0.0)
            for a in range(3):
                for i in range(9):
                    for j in range(9):
                        value += blocks[a, p, i, j] * blocks[a, q, i, j]
            rho_right[p, q] = value
    for rho in (rho_left, rho_right):
        out.extend(
            (
                rho[0, 0] - rho[2, 2],
                rho[1, 1] - rho[2, 2],
                rho[0, 1],
                rho[0, 2],
                rho[1, 2],
            )
        )

    norm = AD(0.0)
    for a in range(3):
        for p in range(3):
            for i in range(9):
                for j in range(9):
                    norm += blocks[a, p, i, j] * blocks[a, p, i, j]
    out.append(norm - 1.0)
    assert len(out) == 56
    return out


def interval_dot(coefficients, intervals):
    lo = 0.0
    hi = 0.0
    for coefficient, interval in zip(coefficients, intervals):
        if coefficient >= 0:
            pl = down(coefficient * interval[0])
            ph = up(coefficient * interval[1])
        else:
            pl = down(coefficient * interval[1])
            ph = up(coefficient * interval[0])
        lo = math.nextafter(lo + pl, -math.inf)
        hi = math.nextafter(hi + ph, math.inf)
    return lo, hi


def main():
    data = json.loads(CERTIFICATE.read_text())
    z = np.array([float.fromhex(value) for value in data["center_hex"]])
    free = np.array(data["free_indices"], dtype=int)
    radius = float.fromhex(data["radius_hex"])
    assert z.shape == (109,)
    assert free.shape == (56,)
    assert len(set(map(int, free))) == 56

    point = equations_ad(z, free, 0.0)
    midpoint_jacobian = np.array(
        [[0.5 * (entry.dlo[j] + entry.dhi[j]) for j in range(56)]
         for entry in point]
    )
    inverse = np.linalg.inv(midpoint_jacobian)

    box = equations_ad(z, free, radius)
    residual = [(entry.lo, entry.hi) for entry in point]
    jacobian = [
        [(entry.dlo[j], entry.dhi[j]) for j in range(56)]
        for entry in box
    ]
    correction = [interval_dot(inverse[i], residual) for i in range(56)]
    center = [
        (
            math.nextafter(z[free[i]] - correction[i][1], -math.inf),
            math.nextafter(z[free[i]] - correction[i][0], math.inf),
        )
        for i in range(56)
    ]

    row_radii = []
    row_norms = []
    max_center_shift = 0.0
    for i in range(56):
        row_sum = 0.0
        for j in range(56):
            product = interval_dot(
                inverse[i], [jacobian[k][j] for k in range(56)]
            )
            diagonal = 1.0 if i == j else 0.0
            rlo = math.nextafter(diagonal - product[1], -math.inf)
            rhi = math.nextafter(diagonal - product[0], math.inf)
            row_sum = math.nextafter(
                row_sum + max(abs(rlo), abs(rhi)), math.inf
            )
        row_radii.append(
            math.nextafter(row_sum * radius, math.inf)
        )
        row_norms.append(row_sum)
        max_center_shift = max(
            max_center_shift,
            abs(center[i][0] - z[free[i]]),
            abs(center[i][1] - z[free[i]]),
        )
    margins = []
    for i in range(56):
        shift = max(
            abs(center[i][0] - z[free[i]]),
            abs(center[i][1] - z[free[i]]),
        )
        margins.append(
            math.nextafter(
                math.nextafter(radius - shift, -math.inf) - row_radii[i],
                -math.inf,
            )
        )
    margin = min(margins)
    contraction_bound = max(row_norms)
    assert margin > 0.0
    assert contraction_bound < 1.0

    # The scale B is a free coordinate.  Its whole root box is
    # positive, so beta is positive definite.  On the antisymmetric
    # subspace beta^Gamma is (B-A)I_3=-B I_3/5.
    assert np.count_nonzero(free == 108) == 1
    b_interval = (
        math.nextafter(z[108] - radius, -math.inf),
        math.nextafter(z[108] + radius, math.inf),
    )
    assert b_interval[0] > 0.0

    # These two factor minors stay strictly nonzero on the box, so
    # X and Y both have column rank two and C=XY^T has rank exactly two.
    variables = []
    lookup = {int(g): j for j, g in enumerate(free)}
    for global_index, value in enumerate(z):
        if global_index in lookup:
            variables.append(
                AD.variable(value, radius, lookup[global_index])
            )
        else:
            variables.append(AD(value))
    x = np.asarray(variables[:54], dtype=object).reshape(27, 2)
    y = np.asarray(variables[54:108], dtype=object).reshape(27, 2)
    x_minor = x[13, 0] * x[22, 1] - x[13, 1] * x[22, 0]
    y_minor = y[12, 0] * y[20, 1] - y[12, 1] * y[20, 0]
    assert x_minor.hi < 0.0
    assert y_minor.lo > 0.0

    # Consequences of the certified equations:
    # q=(3/2)(5B-A)=57B/10 and the separate left/right local
    # Hessian has eigenvalue (3/2)A=9B/5 on the traceless space.
    q_lower = down(57.0 * b_interval[0] / 10.0)
    hessian_lower = down(9.0 * b_interval[0] / 5.0)
    crossed_upper = up(-b_interval[0] / 5.0)
    assert q_lower > 0.0
    assert hessian_lower > 0.0
    assert crossed_upper < 0.0

    print("verified Krawczyk margin", margin)
    print("verified contraction-factor upper bound", contraction_bound)
    print("certified B interval", b_interval)
    print("certified q lower bound", q_lower)
    print("certified local-Hessian gap", hessian_lower)
    print("certified threefold crossed-Hodge upper bound", crossed_upper)
    print("verified rank(C)=2 and a unique algebraic root in the box")


if __name__ == "__main__":
    main()
