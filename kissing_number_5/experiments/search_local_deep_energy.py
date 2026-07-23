"""Discovery-only scalar relaxations for the local deep-edge energy.

For a fixed code point x, write each <-1/2 neighbor as
    y_i = -p_i x + sqrt(1-p_i**2) u_i,  p_i > 1/2.
This script maximizes sum p_i^2(p_i^2-1/4) under inexpensive necessary
conditions.  It is not a certificate and no theorem relies on its output.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import minimize


def energy(p: np.ndarray) -> float:
    q = p * p
    return float(np.sum(q * (q - 0.25)))


def constraints(p: np.ndarray) -> np.ndarray:
    vals: list[float] = []
    m = len(p)

    # Sort order.  It makes every prefix the set of largest depths.
    vals.extend(float(p[i] - p[i + 1]) for i in range(m - 1))

    # Exact simplex/dimension consequences for the residual S^3 code.
    for k in range(2, min(m, 5) + 1):
        vals.append((k + 1) / (2 * k) - float(p[k - 1] ** 2))
    if m >= 6:
        vals.extend(0.5 - float(p[k - 1] ** 2) for k in range(6, min(m, 8) + 1))

    # The two deepest cap radii must sum to at least pi/3.
    if m >= 2:
        vals.append(
            math.acos(float(p[0])) + math.acos(float(p[1])) - math.pi / 3
        )

    # Apply the nonnegative-weight residual Gram estimate to each prefix,
    # first with weights 1 and then with weights p_i.
    for k in range(1, m + 1):
        a = p[:k]
        s = float(np.sum(a))
        q = float(np.dot(a, a))
        vals.append(k * (k + 1) / 2 - s * s)
        vals.append(s * s + q - 2 * q * q)

    return np.asarray(vals)


def solve(m: int, starts: int = 100) -> tuple[float, np.ndarray, float]:
    rng = np.random.default_rng(20260723 + m)
    best = (-math.inf, np.empty(m), -math.inf)
    bounds = [(0.500000001, 0.999999999)] * m
    for trial in range(starts):
        if trial == 0:
            x0 = np.full(m, math.sqrt((m + 1) / (2 * m)))
        else:
            x0 = np.sort(rng.uniform(0.5001, 0.9, size=m))[::-1]
            while np.min(constraints(x0)) < 0:
                x0 = 0.5 + 0.9 * (x0 - 0.5)
        out = minimize(
            lambda z: -energy(z),
            x0,
            method="SLSQP",
            bounds=bounds,
            constraints={"type": "ineq", "fun": constraints},
            options={"ftol": 1e-13, "maxiter": 3000},
        )
        margin = float(np.min(constraints(out.x)))
        if out.success and margin >= -1e-8 and -out.fun > best[0]:
            best = (-float(out.fun), out.x.copy(), margin)
    return best


if __name__ == "__main__":
    max_m = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    starts = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    for degree in range(1, max_m + 1):
        value, point, margin = solve(degree, starts)
        print(
            degree,
            f"{value:.15f}",
            f"{margin:.3e}",
            " ".join(f"{z:.12f}" for z in point),
            flush=True,
        )
