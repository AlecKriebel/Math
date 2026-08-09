#!/usr/bin/env python3
"""Hostile search for the special reversible ground-state energy K.

This is a discovery script, not a certificate.  It parameterizes every
strictly positive symmetric-W type kernel by type masses and logarithmic
edge weights, solves the two extinction fixed points at r=2, and minimizes
both the actual K defect and its Jensen marginal lower bound.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import differential_evolution


def fixed_points(p: np.ndarray, w: np.ndarray) -> tuple[np.ndarray, ...] | None:
    delta = w @ p
    P = w * p[None, :] / delta[:, None]
    R = P.T * p[None, :] / p[:, None]
    t = R.sum(axis=1)

    q = np.zeros_like(p)
    h = np.zeros_like(p)
    for _ in range(20000):
        q1 = t / (t + 2.0 * (1.0 - P @ q))
        h1 = 1.0 / (1.0 + 2.0 * (t - R @ h))
        if max(np.max(abs(q1 - q)), np.max(abs(h1 - h))) < 2e-13:
            q, h = q1, h1
            break
        q, h = q1, h1
    else:
        return None
    if np.any(q <= 0) or np.any(q >= 1) or np.any(h <= 0) or np.any(h >= 1):
        return None
    return P, R, t, q, h


def unpack(x: np.ndarray, n: int) -> tuple[np.ndarray, np.ndarray]:
    # Fix one mass logit and one edge log-weight to remove two scale gauges.
    logits = np.r_[x[: n - 1], 0.0]
    logits -= logits.max()
    p = np.exp(logits)
    p /= p.sum()
    w = np.empty((n, n))
    k = n - 1
    values = np.r_[x[k:], 0.0]
    k = 0
    for i in range(n):
        for j in range(i, n):
            w[i, j] = w[j, i] = np.exp(values[k])
            k += 1
    return p, w


def defects(
    x: np.ndarray, n: int, orbit_step: int = 0
) -> tuple[float, float, float, float, tuple[np.ndarray, ...] | None]:
    p, w = unpack(x, n)
    solved = fixed_points(p, w)
    if solved is None:
        return 1e3, 1e3, 1e3, 1e3, None
    P, R, t, q, h = solved
    v = 0.5 - q
    s = 1.0 - h
    lhs = np.dot(p, h * (P @ v - v / h) ** 2)
    rhs = 4.0 * np.dot(p, t * v * v / q)
    k_defect = rhs - lhs
    z = 2.0 * q - 1.0
    C = (4.0 - q) * z * z / (4.0 * q)
    A = z / 2.0 - z * z * (1.0 + h) / (8.0 * h)
    marginal = np.dot(p, t * C + A)
    endpoint = np.dot(p, q - s)
    y = q.copy()
    for _ in range(orbit_step):
        ry = R @ y
        y = 2.0 * ry / (1.0 + 2.0 * ry)
    ry = R @ y
    y_next = 2.0 * ry / (1.0 + 2.0 * ry)
    orbit_gap = np.dot(p, y - y_next)
    return k_defect, marginal, endpoint, orbit_gap, solved


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--span", type=float, default=16.0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--iterations", type=int, default=500)
    parser.add_argument("--orbit-step", type=int, default=0)
    parser.add_argument(
        "--objective", choices=("k", "marginal", "endpoint", "orbit"), default="marginal"
    )
    args = parser.parse_args()

    nedge = args.n * (args.n + 1) // 2
    dim = args.n - 1 + nedge - 1

    def objective(x: np.ndarray) -> float:
        values = defects(x, args.n, args.orbit_step)
        index = {"k": 0, "marginal": 1, "endpoint": 2, "orbit": 3}[args.objective]
        # Divide out the harmless distance from the homogeneous equality
        # while retaining the sign of the target.
        p, _ = unpack(x, args.n)
        solved = values[4]
        if solved is None:
            return 1e3
        q = solved[3]
        scale = np.dot(p, (2.0 * q - 1.0) ** 2)
        if args.objective == "orbit" and scale < 1e-8:
            return 1.0 + 1e-8 / max(scale, 1e-300)
        return values[index] / (scale + 1e-16)

    result = differential_evolution(
        objective,
        [(-args.span, args.span)] * dim,
        seed=args.seed,
        maxiter=args.iterations,
        popsize=12,
        tol=1e-10,
        polish=True,
        updating="immediate",
        workers=1,
    )
    p, w = unpack(result.x, args.n)
    k_defect, marginal, endpoint, orbit_gap, solved = defects(
        result.x, args.n, args.orbit_step
    )
    assert solved is not None
    P, R, t, q, h = solved
    print("objective", result.fun, "success", result.success, result.message)
    print("K defect", k_defect)
    print("marginal", marginal)
    print("endpoint", endpoint)
    print("orbit gap", orbit_gap, "at step", args.orbit_step)
    print("p", repr(p))
    print("W", repr(w))
    print("t", repr(t))
    print("q", repr(q))
    print("h", repr(h))
    print("P", repr(P))
    print("R", repr(R))


if __name__ == "__main__":
    main()
