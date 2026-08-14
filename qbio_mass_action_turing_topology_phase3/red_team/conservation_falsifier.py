#!/usr/bin/env python3
"""Exact conservation-law and nonzero-mode regression tests."""
from __future__ import annotations

import json
import random

import sympy as sp


def random_unimodular(rng: random.Random, n: int) -> sp.Matrix:
    U = sp.eye(n)
    for _ in range(4 * n + 5):
        mode = rng.randrange(3)
        if mode == 0:
            i, j = rng.sample(range(n), 2)
            U.row_swap(i, j)
        elif mode == 1:
            i = rng.randrange(n)
            U.row_op(i, lambda value, _: -value)
        else:
            i, j = rng.sample(range(n), 2)
            c = rng.choice((-2, -1, 1, 2))
            source = list(U.row(j))
            U.row_op(i, lambda value, col: value + c * source[col])
    if abs(int(U.det())) != 1:
        raise AssertionError("elementary operations did not produce a unimodular matrix")
    return U


def main() -> int:
    rng = random.Random(20260813)
    cases = 0
    for n in range(2, 7):
        for s in range(1, n):
            for _ in range(40):
                U = random_unimodular(rng, n)
                Uinv = U.inv()
                B = U[:, :s]
                C = Uinv[:s, :]
                R = sp.diag(*[-sp.Rational(j + 1, j + 2) for j in range(s)])
                J = B * R * C
                expected = sp.diag(*list(R.diagonal()), *([0] * (n - s)))
                if C * B != sp.eye(s):
                    raise AssertionError("left inverse failed")
                if Uinv * J * U != expected:
                    raise AssertionError("conservation block similarity failed")
                N = U[:, s:]
                if J * B != B * R or J * N != sp.zeros(n, n - s):
                    raise AssertionError("invariant image/kernel decomposition failed")
                for lam in (sp.Rational(1, 7), sp.Integer(1), sp.Integer(5)):
                    actual = (lam * sp.eye(n) - J).det(method="domain-ge")
                    target = lam ** (n - s) * (lam * sp.eye(s) - R).det(method="domain-ge")
                    if actual != target or actual <= 0:
                        raise AssertionError("positive-axis determinant factorization failed")
                cases += 1

    B = sp.Matrix([[1], [1]])
    J = sp.Matrix([[-sp.Rational(1, 2), -sp.Rational(1, 2)],
                   [-sp.Rational(1, 2), -sp.Rational(1, 2)]])
    D = sp.diag(1, 2)
    if J * B != -B or sp.Matrix.hstack(B, D * B).rank() == 1:
        raise AssertionError("unequal-diffusion counterexample failed")

    # Integral of cos(x) on (0,pi), evaluated exactly without numerical quadrature.
    phi_integral = sp.sin(sp.pi) - sp.sin(0)
    if phi_integral != 0:
        raise AssertionError("nonzero Neumann mode did not have zero mean")

    print(json.dumps({
        "status": "PASS",
        "random_conservative_cases": cases,
        "noninvariant_diffusion_example": {
            "S_basis": [[1], [1]],
            "D_times_basis": [[1], [2]],
        },
        "neumann_mode_integral": str(phi_integral),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
