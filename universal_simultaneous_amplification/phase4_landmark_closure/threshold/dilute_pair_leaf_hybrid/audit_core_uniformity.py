#!/usr/bin/env python3
"""Numerical hostile audit of the claimed uniform clique-core error rate.

This diagnostic is not part of the proof.  It solves the established
three-coordinate clique--pendant quotient chain and prints the singleton
values separately, so that two-scale error claims can be screened before
they are used in a diagonal argument.
"""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import fmpq
from scipy.sparse import csr_matrix, lil_matrix
from scipy.sparse.linalg import spsolve


HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent / "clique_pendant_product_audit"
sys.path.insert(0, str(AUDIT))
from verify_clique_pendant_product import quotient_changes, states  # noqa: E402


def singleton_values(c: int, m: int, rule: str, r: float):
    """Return hub, ordinary-core, leaf, and core-averaged fixation values."""
    extinction = (0, 0, 0)
    fixation = (1, c, m)
    transient = [s for s in states(c, m) if s not in (extinction, fixation)]
    index = {s: k for k, s in enumerate(transient)}
    matrix = lil_matrix((len(transient), len(transient)), dtype=float)
    rhs = np.zeros(len(transient))
    rq0 = Fraction(r)
    rq = fmpq(rq0.numerator, rq0.denominator)
    for state, row_index in index.items():
        changes = quotient_changes(c, m, rq, rule, state)
        matrix[row_index, row_index] = float(sum(changes.values(), fmpq(0)))
        for target, probability in changes.items():
            probability = float(probability)
            if target == fixation:
                rhs[row_index] += probability
            elif target != extinction:
                matrix[row_index, index[target]] -= probability
    solution = spsolve(csr_matrix(matrix), rhs)
    hub = solution[index[(1, 0, 0)]]
    ordinary = solution[index[(0, 1, 0)]]
    leaf = solution[index[(0, 0, 1)]]
    core_average = (hub + c * ordinary) / (c + 1)
    return hub, ordinary, leaf, core_average


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--r", type=float, default=1.5)
    parser.add_argument(
        "--cases",
        nargs="*",
        default=["199,14", "399,20", "799,28", "999,32"],
        help="comma-separated c,m pairs; clique size is C=c+1",
    )
    args = parser.parse_args()
    p = 1.0 - 1.0 / args.r
    print("rule,c,m,C*(u_core-p),C/m*(u_core-p),(u_core-p)/(m/C)")
    for item in args.cases:
        c, m = map(int, item.split(","))
        C = c + 1
        for rule in ("Bd", "dB"):
            _, _, _, core = singleton_values(c, m, rule, args.r)
            error = core - p
            print(
                f"{rule},{c},{m},{C * error:.12g},"
                f"{C * error / m:.12g},{error / (m / C):.12g}"
            )


if __name__ == "__main__":
    main()
