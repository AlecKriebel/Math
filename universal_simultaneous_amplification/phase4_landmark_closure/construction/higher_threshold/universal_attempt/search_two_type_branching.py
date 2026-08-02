#!/usr/bin/env python3
"""Numerical reconnaissance for reversible two-class rare-mutant branching.

This is a discovery tool, not a proof certificate.  The class proportions are
``a=1-b`` and ``b``.  A resident random walk jumps A->B with probability x
and B->A with probability y.  Every x,y in (0,1) is realized by a symmetric
weighted two-class complete graph after choosing the two internal weights.

The continuous-time rare-mutant generators are derived directly from the
update rules.  If P is the resident neighbor-class transition matrix and t_i
is the incoming temperature, then

  Bd: mutant i gives birth to j at rate r P_ij and dies at rate t_i;
  dB: mutant i gives birth to j at rate r (pi_j/pi_i) P_ji and dies at rate 1.

The maximal survival vector s solves

  d_i s_i = (1-s_i) sum_j B_ij s_j.
"""

from __future__ import annotations

import argparse
import math

import numpy as np


def matrices(b: float, x: float, y: float, r: float, rule: str):
    a = 1.0 - b
    P = np.array([[1.0 - x, x], [y, 1.0 - y]])
    t = np.array([1.0 - x + b * y / a, 1.0 - y + a * x / b])
    if rule == "Bd":
        births = r * P
        deaths = t
    elif rule == "dB":
        births = r * np.array(
            [[1.0 - x, b * y / a], [a * x / b, 1.0 - y]]
        )
        deaths = np.ones(2)
    else:
        raise ValueError(rule)
    assert np.max(np.abs(births.sum(axis=1) - r * (1 if rule == "Bd" else t))) < 1e-9
    assert abs(a * t[0] + b * t[1] - 1.0) < 1e-9
    return births, deaths, t


def survival(b: float, x: float, y: float, r: float, rule: str):
    births, deaths, temperatures = matrices(b, x, y, r, rule)
    s = np.ones(2)
    for _ in range(100000):
        load = births @ s
        new = load / (deaths + load)
        if np.max(np.abs(new - s)) < 2e-14:
            break
        s = new
    else:
        raise RuntimeError("survival iteration did not converge")
    residual = np.max(np.abs(deaths * s - (1.0 - s) * (births @ s)))
    if residual > 2e-10:
        raise AssertionError(residual)
    return s, temperatures


def evaluate(b: float, x: float, y: float, r: float):
    a = 1.0 - b
    sb, t = survival(b, x, y, r, "Bd")
    sd, _ = survival(b, x, y, r, "dB")
    p = 1.0 - 1.0 / r
    return a * sb[0] + b * sb[1] - p, a * sd[0] + b * sd[1] - p, sb, sd, t


def random_search(r: float, samples: int, seed: int):
    rng = np.random.default_rng(seed)
    best = []
    for _ in range(samples):
        # Resolve both vanishing classes and boundary-layer mixing laws.
        b = math.exp(rng.uniform(math.log(1e-6), math.log(0.5)))
        x = math.exp(rng.uniform(math.log(1e-8), math.log(1.0)))
        y = math.exp(rng.uniform(math.log(1e-8), math.log(1.0)))
        gb, gd, sb, sd, t = evaluate(b, x, y, r)
        best.append((min(gb, gd), gb, gd, b, x, y, *sb, *sd, *t))
    best.sort(reverse=True)
    return best[:20]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--r", type=float, default=1.51)
    parser.add_argument("--samples", type=int, default=100000)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    for row in random_search(args.r, args.samples, args.seed):
        print(" ".join(f"{value:.10g}" for value in row))


if __name__ == "__main__":
    main()
