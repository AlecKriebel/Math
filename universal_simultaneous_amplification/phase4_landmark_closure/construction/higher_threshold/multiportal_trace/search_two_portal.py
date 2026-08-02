#!/usr/bin/env python3
"""Reconnaissance for the homogeneous symmetric two-portal pair module.

This uses only the limiting trace formulas derived from the update rules.
It does not treat branching survival as fixation: the density drift is checked
separately on a fine grid.
"""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import brentq


def pgf_bd(q: float, r: float, c: float, theta: float) -> float:
    gamma = theta / (1.0 + theta)
    beta = r * r * (1.0 - gamma) / (r + 1.0)
    a0 = 2.0 * c + gamma
    a1 = r * gamma
    u = 1.0 - q
    return a0 * (4.0 * c + 2.0 * beta * u) / (
        (a0 + a1 + beta * u) * (4.0 * c + 2.0 * beta * u)
        - 4.0 * c * a1
    )


def pgf_db(q: float, r: float, c: float, theta: float) -> float:
    a = theta * r / (1.0 + theta * r)
    b0 = 1.0 / (1.0 + theta * r)
    beta = r * c
    u = 1.0 - q
    return (b0 + beta * u) / (
        (1.0 + a + beta * u) * (b0 + beta * u) - a * b0
    )


def extinction_bd(r: float, c: float, theta: float) -> float:
    gamma = theta / (1.0 + theta)
    kappa = 2.0 * r * (r + 1.0) * c / (1.0 - gamma)
    def h(q: float) -> float:
        return 1.0 / (1.0 + kappa * (1.0 - pgf_bd(q, r, c, theta))) - q

    edge = 1.0 - 1e-10
    if h(edge) >= 0.0:
        return 1.0
    return brentq(h, 0.0, edge, xtol=2e-14, rtol=2e-14)


def extinction_db(r: float, c: float, theta: float) -> float:
    gamma = theta / (1.0 + theta)
    def h(q: float) -> float:
        return c / (
            c + r * r * (1.0 - gamma) * (1.0 - pgf_db(q, r, c, theta))
        ) - q

    edge = 1.0 - 1e-10
    if h(edge) >= 0.0:
        return 1.0
    return brentq(h, 0.0, edge, xtol=2e-14, rtol=2e-14)


def portal_moments_bd(y: float, r: float, c: float, theta: float) -> tuple[float, float]:
    gamma = theta / (1.0 + theta)
    u0 = 4.0 * r * c * y
    d1 = 2.0 * c * (1.0 - y) + gamma
    u1 = 2.0 * r * c * y + r * gamma
    d2 = 4.0 * c * (1.0 - y)
    a = u0 / d1
    b = u1 / d2
    z = 1.0 + a + a * b
    probs = (1.0 / z, a / z, a * b / z)
    ek = probs[1] + 2.0 * probs[2]
    return ek, 2.0 - ek


def portal_moments_db(y: float, r: float, c: float, theta: float) -> tuple[float, float]:
    del c
    u0_single = r * y / (r * y + 1.0 - y + theta)
    d1 = (1.0 - y + theta) / (r * y + 1.0 - y + theta)
    u1 = r * (y + theta) / (r * (y + theta) + 1.0 - y)
    d2_single = (1.0 - y) / (r * (y + theta) + 1.0 - y)
    a = (2.0 * u0_single) / d1
    b = u1 / (2.0 * d2_single)
    z = 1.0 + a + a * b
    probs = (1.0 / z, a / z, a * b / z)
    ek = probs[1] + 2.0 * probs[2]
    return ek, 2.0 - ek


def min_log_drift(r: float, c: float, theta: float, rule: str) -> float:
    vals = []
    for y in np.linspace(1e-5, 1.0 - 1e-5, 2001):
        if rule == "Bd":
            ek, er = portal_moments_bd(y, r, c, theta)
            ratio = r * r * (1.0 - y) * ek / (y * er)
        else:
            ek, er = portal_moments_db(y, r, c, theta)
            ratio = r * r * (1.0 - y) * ek / (y * er)
        vals.append(math.log(ratio))
    return min(vals)


def scan(r: float) -> None:
    p = 1.0 - 1.0 / r
    best = None
    both = []
    cs = np.geomspace(0.02, 20.0, 241)
    thetas = np.concatenate(([0.0], np.geomspace(1e-4, 100.0, 241)))
    for c in cs:
        for theta in thetas:
            qb = extinction_bd(r, c, theta)
            qd = extinction_db(r, c, theta)
            ab = r / (r + 1.0) * (1.0 - qb)
            ad = 0.5 * (1.0 - qd)
            margin = min(ab - p, ad - p)
            if best is None or margin > best[0]:
                best = (margin, c, theta, ab, ad)
            if ab > p and ad > p:
                mb = min_log_drift(r, c, theta, "Bd")
                md = min_log_drift(r, c, theta, "dB")
                both.append((margin, c, theta, ab, ad, mb, md))
    assert best is not None
    print(f"r={r:.12g} p={p:.12g}")
    print("best establishment margin,c,theta,alphaBd,alphadB:", best)
    print("count both establishment:", len(both))
    for row in sorted(both, reverse=True)[:20]:
        print("candidate", row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--r", type=float, default=8.0 / 5.0)
    args = parser.parse_args()
    scan(args.r)
