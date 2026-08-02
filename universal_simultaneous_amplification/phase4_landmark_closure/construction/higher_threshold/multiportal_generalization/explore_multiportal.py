#!/usr/bin/env python3
"""First-principles reconnaissance for q exchangeable active portals.

This script works only with the limiting protected-pair trace.  It keeps the
full portal-count chain and computes its marked-child hitting transform by a
tridiagonal solve.  Numerical output is discovery evidence, not proof.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.linalg import solve
from scipy.optimize import brentq


def episode_transform(
    q_portals: int,
    death: np.ndarray,
    birth: np.ndarray,
    child_rate: np.ndarray,
    z: float,
) -> float:
    """Return E[z**children] from portal count one before hitting zero."""
    q = q_portals
    matrix = np.zeros((q, q), dtype=float)
    rhs = np.zeros(q, dtype=float)
    for k in range(1, q + 1):
        row = k - 1
        discount = child_rate[k] * (1.0 - z)
        matrix[row, row] = death[k] + birth[k] + discount
        if k == 1:
            rhs[row] = death[k]
        else:
            matrix[row, row - 1] = -death[k]
        if k < q:
            matrix[row, row + 1] = -birth[k]
    values = solve(matrix, rhs, assume_a="gen")
    return float(values[0])


def rates_bd(q: int, r: float, c: float, g: float):
    death = np.zeros(q + 1)
    birth = np.zeros(q + 1)
    child = np.zeros(q + 1)
    beta = r * r * (1.0 - g) / (r + 1.0)
    for k in range(1, q + 1):
        death[k] = k * (2.0 * c + (q - k) * g / (q - 1.0))
        birth[k] = r * k * (q - k) * g / (q - 1.0)
        child[k] = k * beta
    return death, birth, child


def rates_db(q: int, r: float, c: float, g: float):
    death = np.zeros(q + 1)
    birth = np.zeros(q + 1)
    child = np.zeros(q + 1)
    for k in range(1, q + 1):
        death[k] = (
            k
            * (q - 1.0 - g * (k - 1.0))
            / (q - 1.0 + g * (r - 1.0) * (k - 1.0))
        )
        birth[k] = (
            r
            * k
            * (q - k)
            * g
            / (q - 1.0 + g * (r - 1.0) * k)
        )
        child[k] = k * r * c
    return death, birth, child


def extinction(q: int, r: float, c: float, g: float, rule: str) -> float:
    if rule == "Bd":
        rates = rates_bd(q, r, c, g)
        kappa = 2.0 * r * (r + 1.0) * c / (1.0 - g)
    else:
        rates = rates_db(q, r, c, g)
        kappa = r * r * (1.0 - g) / c

    def lifetime_pgf(z: float) -> float:
        f = episode_transform(q, *rates, z)
        return 1.0 / (1.0 + kappa * (1.0 - f))

    def residual(z: float) -> float:
        return lifetime_pgf(z) - z

    edge = 1.0 - 1.0e-10
    if residual(edge) >= 0.0:
        return 1.0
    return brentq(residual, 0.0, edge, xtol=2e-14, rtol=2e-14)


def scan(q: int, r: float) -> None:
    baseline = 1.0 - 1.0 / r
    best = None
    count = 0
    for c in np.geomspace(0.005, 50.0, 321):
        for g in np.linspace(0.0, 0.999, 321):
            qb = extinction(q, r, c, g, "Bd")
            qd = extinction(q, r, c, g, "dB")
            alpha_b = r / (r + 1.0) * (1.0 - qb)
            alpha_d = 0.5 * (1.0 - qd)
            margin = min(alpha_b - baseline, alpha_d - baseline)
            row = (margin, c, g, alpha_b, alpha_d)
            if best is None or row > best:
                best = row
            if margin > 0.0:
                count += 1
    print(f"q={q} r={r:.12g} p={baseline:.12g}")
    print("best margin,c,g,alpha_B,alpha_D:", best)
    print("simultaneous count:", count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--r", type=float, default=1.6)
    args = parser.parse_args()
    scan(args.q, args.r)
