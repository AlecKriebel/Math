#!/usr/bin/env python3
"""Maximize the endpoint affine separator S=(Bd+2 dB)/3."""

from __future__ import annotations

import argparse
import math

import numpy as np
from scipy.optimize import minimize_scalar

from search_endpoint import ratios


def optimize(c: int, m: int, lo=-12.0, hi=16.0):
    def row(z):
        w = math.exp(z)
        x, y, M = ratios(c, m, w)
        return w, x, y, M, (x + 2 * y) / 3

    grid = np.linspace(lo, hi, 81)
    vals = np.array([row(z)[-1] for z in grid])
    candidates = [row(lo), row(hi)]
    for k in range(1, len(grid) - 1):
        if vals[k] >= vals[k - 1] and vals[k] >= vals[k + 1]:
            ans = minimize_scalar(
                lambda z: -row(z)[-1],
                bounds=(grid[k - 1], grid[k + 1]),
                method="bounded",
                options={"xatol": 2e-10},
            )
            candidates.append(row(ans.x))
    return max(candidates, key=lambda q: q[-1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=40)
    parser.add_argument("--min-n", type=int, default=3)
    args = parser.parse_args()
    best = None
    for n in range(args.min_n, args.max_n + 1):
        for m in range(1, n - 1):
            c = n - m - 1
            result = optimize(c, m)
            candidate = (result[-1], c, m, *result[:-1])
            if best is None or candidate > best:
                best = candidate
        print(
            f"through n={n}: S={best[0]:.15f} c={best[1]} m={best[2]} "
            f"w={best[3]:.12g} Bd={best[4]:.15f} dB={best[5]:.15f} "
            f"M={best[6]:.15f}",
            flush=True,
        )


if __name__ == "__main__":
    main()
