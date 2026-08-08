#!/usr/bin/env python3
"""Hostile numerical search for the Q=2 direct-portal affine map.

Discovery only.  This strips away the blade incidence parameterization and
optimizes the exact two-portal episode directly over portal loads, the portal
edge, row marks, and the nonnegative weights of one prospective parent type.
"""

from __future__ import annotations

import argparse

import numpy as np
from scipy.optimize import differential_evolution


def episode_survival(rule: str, r: float, loads, edge: float, marks):
    """Return 1-F_{\{a\}}(1-marks), a=0,1, from the exact 3-state chain."""
    b1, b2 = loads
    d1, d2 = b1 + edge, b2 + edge
    if rule == "Bd":
        c = r * r / (r + 1.0)
        kill = np.array(
            [c * b1 * marks[0] / d1,
             c * b2 * marks[1] / d2,
             c * (b1 * marks[0] / d1 + b2 * marks[1] / d2)]
        )
        down1, up1 = b1 + edge / d2, r * edge / d1
        down2, up2 = b2 + edge / d1, r * edge / d2
        to1, to2 = b2, b1
    elif rule == "dB":
        c = r / 2.0
        kill = np.array(
            [c * b1 * marks[0], c * b2 * marks[1],
             c * (b1 * marks[0] + b2 * marks[1])]
        )
        down1, up1 = 1.0, r * edge / (b2 + r * edge)
        down2, up2 = 1.0, r * edge / (b1 + r * edge)
        to1 = b2 / (b2 + r * edge)
        to2 = b1 / (b1 + r * edge)
    else:
        raise ValueError(rule)

    # State order 1,2,12.  H is the probability that a marked child occurs
    # before the portal set empties: (transition+kill generator) H = kill.
    mat = np.array(
        [[down1 + up1 + kill[0], 0.0, -up1],
         [0.0, down2 + up2 + kill[1], -up2],
         [-to1, -to2, to1 + to2 + kill[2]]]
    )
    return np.linalg.solve(mat, kill)[:2]


def decode(v):
    loads = np.exp(v[:2])
    edge = np.exp(v[2])
    marks = 1.0 / (1.0 + np.exp(-np.asarray(v[3:5])))
    parent = 1.0 / (1.0 + np.exp(-v[5]))
    return loads, edge, marks, np.array([parent, 1.0 - parent])


def map_gap(v, r: float):
    """Return the dB affine-supersolution margin (positive is desired)."""
    loads, edge, marks, parent = decode(v)
    degrees = loads + edge
    hb = episode_survival("Bd", r, loads, edge, marks)
    a = 4.0 * (r - 1.0) / r
    k = 2.0 * r / (r + 1.0)
    dual_marks = np.minimum(1.0, a - k * marks)
    hd = episode_survival("dB", r, loads, edge, dual_marks)

    # parent[a] is a_a=B_a f_at/d_a, normalized to sum one.
    xodds = r * (r + 1.0) * np.dot(parent, degrees * hb)
    x = xodds / (1.0 + xodds)
    y = min(1.0, a - k * x)
    if y >= 1.0:
        return 1.0
    yodds = y / (1.0 - y)
    return yodds * np.dot(parent, degrees) - 2.0 * r * r * np.dot(parent, hd)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fitness", type=float, default=31 / 20)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--maxiter", type=int, default=1000)
    ap.add_argument("--popsize", type=int, default=25)
    args = ap.parse_args()
    result = differential_evolution(
        lambda v: map_gap(v, args.fitness),
        [(-14.0, 14.0)] * 6,
        seed=args.seed,
        maxiter=args.maxiter,
        popsize=args.popsize,
        tol=1e-11,
        polish=True,
        workers=1,
        updating="immediate",
    )
    loads, edge, marks, parent = decode(result.x)
    print("minimum affine-map margin", result.fun)
    print("loads", loads)
    print("edge", edge)
    print("marks", marks)
    print("parent weights a", parent)
    print("parameters", result.x)


if __name__ == "__main__":
    main()
