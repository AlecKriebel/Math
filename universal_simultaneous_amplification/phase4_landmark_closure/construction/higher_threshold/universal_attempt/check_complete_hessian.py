#!/usr/bin/env python3
"""Numerical Hessian reconnaissance at the unit complete graph.

Permutation symmetry splits zero-sum edge perturbations into the vertex-degree
and zero-row-sum cycle subspaces.  The script evaluates one representative of
each by symmetric finite differences of the exact full subset-chain solve.
It is discovery code, not an exact certificate.
"""

from __future__ import annotations

import importlib.util
import pathlib

import numpy as np


HERE = pathlib.Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("finite_pairs", HERE / "check_finite_dense_pairs.py")
MOD = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(MOD)


def directions(n):
    a = np.full(n, -1.0 / (n - 1)); a[0] = 1.0
    degree = a[:, None] + a[None, :]; np.fill_diagonal(degree, 0.0)
    cycle = np.zeros((n, n))
    for i, j, value in ((0, 1, 1), (2, 3, 1), (0, 2, -1), (1, 3, -1)):
        cycle[i, j] = cycle[j, i] = value
    assert np.max(abs(cycle.sum(axis=1))) == 0
    return degree, cycle


def hessian(n, r, rule, direction, h=2e-3):
    K = np.ones((n, n)) - np.eye(n)
    f0 = MOD.fixation(K, r, rule)
    fp = MOD.fixation(K + h * direction, r, rule)
    fm = MOD.fixation(K - h * direction, r, rule)
    return (fp + fm - 2 * f0) / h**2


def main():
    for r in (1.1, 1.4, 1.5, 1.51, 2.0, 5.0):
        for n in (4, 5, 6, 7, 8):
            degree, cycle = directions(n)
            vals = []
            for rule in ("Bd", "dB"):
                vals.extend((hessian(n, r, rule, degree), hessian(n, r, rule, cycle)))
            print(r, n, *vals)


if __name__ == "__main__":
    main()
