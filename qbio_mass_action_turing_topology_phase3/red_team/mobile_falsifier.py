#!/usr/bin/env python3
"""Independent stress test of the designated-mobile positive-lambda theorem."""
from __future__ import annotations

import itertools
import json
import random
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]


def principal_coeff(J: sp.Matrix, lam: sp.Expr, I: tuple[int, ...]) -> sp.Expr:
    if not I:
        return sp.Integer(1)
    return sp.expand((lam * sp.eye(len(I)) - J.extract(I, I)).det())


def expansion(J: sp.Matrix, lam: sp.Expr, mobile: tuple[int, ...], d: dict[int, sp.Expr]) -> sp.Expr:
    n = J.rows
    immobile = set(range(n)) - set(mobile)
    total = 0
    for size in range(len(immobile), n + 1):
        for I in itertools.combinations(range(n), size):
            if not immobile.issubset(I):
                continue
            total += principal_coeff(J, lam, I) * sp.prod(d[j] for j in set(mobile) - set(I))
    return sp.expand(total)


def construct_d(J: sp.Matrix, lam: sp.Rational, mobile: tuple[int, ...], I: tuple[int, ...]) -> tuple[dict[int, sp.Rational], sp.Expr]:
    if principal_coeff(J, lam, I) >= 0:
        raise ValueError("not a negative coefficient")
    selected = set(I)
    for power in range(1, 25):
        t = 2**power
        d = {j: (sp.Integer(t) if j not in selected else sp.Rational(1, t)) for j in mobile}
        value = sp.expand((lam * sp.eye(J.rows) - J + sp.diag(*[d.get(j, 0) for j in range(J.rows)])).det())
        if value < 0:
            return d, value
    raise AssertionError("mobile multiscale construction failed")


def random_hurwitz(rng: random.Random, n: int) -> sp.Matrix:
    # Strict row diagonal dominance with negative diagonal gives an exact Hurwitz matrix.
    rows = []
    for i in range(n):
        off = [sp.Rational(rng.randint(-3, 3), rng.randint(1, 4)) if j != i else 0 for j in range(n)]
        radius = sum(abs(x) for x in off)
        off[i] = -(radius + sp.Rational(rng.randint(1, 4), rng.randint(1, 3)))
        rows.extend(off)
    return sp.Matrix(n, n, rows)


def main() -> None:
    rng = random.Random(9132026)
    exact_expansions = 0
    constructed_witnesses = 0
    sampled_positive_eigenvalues = 0
    necessity_confirmations = 0
    for n in (2, 3, 4):
        for _ in range(250):
            J = random_hurwitz(rng, n)
            mobile = tuple(i for i in range(n) if rng.random() < 0.65)
            if not mobile:
                mobile = (rng.randrange(n),)
            immobile = set(range(n)) - set(mobile)
            for lam in (sp.Rational(1, 5), sp.Rational(3, 2)):
                d = {j: sp.Rational(rng.randint(1, 7), rng.randint(1, 5)) for j in mobile}
                direct = sp.expand((lam * sp.eye(n) - J + sp.diag(*[d.get(j, 0) for j in range(n)])).det())
                if sp.expand(direct - expansion(J, lam, mobile, d)) != 0:
                    raise AssertionError("mobile principal-block expansion failed")
                exact_expansions += 1
                candidates = []
                for size in range(len(immobile), n + 1):
                    for I in itertools.combinations(range(n), size):
                        if immobile.issubset(I) and principal_coeff(J, lam, I) < 0:
                            candidates.append(I)
                if candidates:
                    _, value = construct_d(J, lam, mobile, candidates[0])
                    if value >= 0:
                        raise AssertionError("constructed mobile determinant is not negative")
                    constructed_witnesses += 1

            # Random necessity attacks.  A numerically positive real eigenvalue provides
            # its own lambda; evaluate every coefficient at that lambda.
            for _d in range(3):
                vals = [rng.uniform(0.02, 20.0) if i in mobile else 0.0 for i in range(n)]
                shifted = np.array(J.evalf(30).tolist(), dtype=float) - np.diag(vals)
                eigs = np.linalg.eigvals(shifted)
                positives = [z.real for z in eigs if abs(z.imag) < 1e-8 and z.real > 1e-8]
                if positives:
                    sampled_positive_eigenvalues += 1
                    lam = max(positives)
                    found = False
                    for size in range(len(immobile), n + 1):
                        for I in itertools.combinations(range(n), size):
                            if immobile.issubset(I):
                                block = np.array(J.extract(I, I).evalf(30).tolist(), dtype=float)
                                if np.linalg.det(lam * np.eye(len(I)) - block) < -1e-7:
                                    found = True
                    if not found:
                        raise AssertionError("numeric positive mode found no negative principal-block coefficient")
                    necessity_confirmations += 1

    J = sp.Matrix([[-10, 20, -50], [1, 1, 0], [1, 0, 2]])
    D = sp.diag(sp.Rational(257, 2), 0, 0)
    vector = sp.Matrix([sp.Rational(-1, 2), -1, 1])
    if (J - D) * vector != sp.Rational(3, 2) * vector:
        raise AssertionError("designated-mobile counterexample eigenpair failed")
    lam_exact = sp.Rational(3, 2)
    diagnostic_I = (1, 2)
    if principal_coeff(J, lam_exact, diagnostic_I) >= 0:
        raise AssertionError("positive-lambda diagnostic failed")
    if J.extract(diagnostic_I, diagnostic_I).det() < 0:
        raise AssertionError("zero-lambda proposal was not actually missed")
    d_exact, exact_value = construct_d(J, lam_exact, (0,), diagnostic_I)
    if exact_value >= 0:
        raise AssertionError("exact designated-mobile construction failed")
    constructed_witnesses += 1

    # Exercise necessity on a known all-mobile stationary-destabilizable matrix and
    # 120 exact diagonal similarities/permutations of it.
    Jbase = sp.Matrix([[-7, -1, -2], [-7, -4, -4], [-3, -7, -6]])
    Dbase = np.diag([9.0, 1.0 / 9.0, 1.0 / 9.0])
    for rep in range(120):
        scales = [sp.Rational(rng.randint(1, 7), rng.randint(1, 7)) for _ in range(3)]
        R = sp.diag(*scales)
        perm = list(range(3)); rng.shuffle(perm)
        P = sp.zeros(3)
        for i, j in enumerate(perm): P[i, j] = 1
        Jsim = sp.simplify(P * R * Jbase * R.inv() * P.T)
        Dsim = P * sp.diag(9, sp.Rational(1, 9), sp.Rational(1, 9)) * P.T
        eigs = np.linalg.eigvals(np.array((Jsim - Dsim).evalf(40).tolist(), dtype=float))
        positives = [z.real for z in eigs if abs(z.imag) < 1e-8 and z.real > 1e-8]
        if not positives:
            raise AssertionError("known all-mobile witness lost its positive eigenvalue")
        sampled_positive_eigenvalues += 1
        lam = max(positives)
        found = False
        for size in range(1, 4):
            for I in itertools.combinations(range(3), size):
                block = np.array(Jsim.extract(I, I).evalf(40).tolist(), dtype=float)
                if np.linalg.det(lam * np.eye(size) - block) < -1e-7:
                    found = True
        if not found:
            raise AssertionError("known positive eigenvalue had no negative coefficient")
        necessity_confirmations += 1

    result = {
        "status": "PASS",
        "exact_expansion_checks": exact_expansions,
        "constructed_negative_determinants": constructed_witnesses,
        "sampled_positive_eigenvalues": sampled_positive_eigenvalues,
        "necessity_confirmations": necessity_confirmations,
        "exact_zero_lambda_counterexample": True,
    }
    (ROOT / "release" / "mobile_falsifier.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
