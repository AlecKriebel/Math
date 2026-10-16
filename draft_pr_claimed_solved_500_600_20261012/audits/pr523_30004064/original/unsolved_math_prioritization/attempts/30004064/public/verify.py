#!/usr/bin/env python3
"""Small exact checks for the binary-tomography dual counterexample.

Python standard library only. No optimization package, floating-point arithmetic,
network access, external source files, or large enumeration is used.
"""
from fractions import Fraction as Q
from itertools import product
import json


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def mv(a, x):
    return tuple(dot(row, x) for row in a)


def tr(a):
    return tuple(zip(*a))


def mm(a, b):
    return tuple(tuple(dot(row, col) for col in tr(b)) for row in a)


def rank(a):
    a = [list(map(Q, row)) for row in a]
    r = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][j]
        a[r] = [v / p for v in a[r]]
        for i in range(len(a)):
            if i != r:
                p = a[i][j]
                a[i] = [x - p * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def line_sums(k, omit_last_column=True):
    rows = [tuple(int(i == r) for i in range(k) for j in range(k))
            for r in range(k)]
    cols = [tuple(int(j == c) for i in range(k) for j in range(k))
            for c in range(k - int(omit_last_column))]
    return tuple(rows + cols)


def binary_solutions(a, y):
    return [s for s in product((-1, 1), repeat=len(a[0])) if mv(a, s) == y]


def common(solutions):
    return tuple(col[0] if len(set(col)) == 1 else 0 for col in zip(*solutions))


def norm2(x):
    return dot(x, x)


def objective(a, y, mu):
    return Q(1, 2) * norm2(tuple(x - b for x, b in zip(mu, y))) + sum(map(abs, mv(tr(a), mu)))


def main():
    a = line_sums(3)
    sp = (1, 1, 1, 1, 1, -1, 1, -1, 1)
    sm = (1, 1, 1, 1, -1, 1, 1, 1, -1)
    y = (3, 1, 1, 3, 1)
    assert rank(a) == 5
    assert mv(a, sp) == mv(a, sm) == y
    ss = binary_solutions(a, y)
    assert set(ss) == {sp, sm}
    c = common(ss)
    assert c == (1, 1, 1, 1, 0, 0, 1, 0, 0)
    assert c != (0,) * 9
    y_unique = (3, 3, 3, 3, 3)
    assert binary_solutions(a, y_unique) == [(1,) * 9]

    a2 = line_sums(2)
    mixed = (1, 1, -1, -1)
    assert binary_solutions(a2, mv(a2, mixed)) == [mixed]
    scalar_count = 0
    for s in (-1, 1):
        assert binary_solutions(((1,),), (s,)) == [(s,)]
        scalar_count += 2
    binary_images_checked = 512 + 512 + 16 + scalar_count
    assert binary_images_checked == 1044

    # Finite rational spot-checks of the universal algebraic identity.
    identity_checks = 0
    for s in (sp, sm, (1,) * 9):
        data = mv(a, s)
        for denominator in (1, 3):
            for integers in product((-1, 0, 1), repeat=5):
                mu = tuple(Q(v, denominator) for v in integers)
                q = mv(tr(a), mu)
                slack = sum(abs(v) - t * v for v, t in zip(q, s))
                gap = objective(a, data, mu) - objective(a, data, (0,) * 5)
                assert gap == Q(1, 2) * norm2(mu) + slack
                assert slack >= 0
                assert gap >= Q(1, 2) * norm2(mu)
                assert (gap == 0) == (mu == (0,) * 5)
                identity_checks += 1

    # Full six-row tomography: the only row dependency is w=(1,1,1,-1,-1,-1).
    b = line_sums(3, False)
    assert rank(b) == 5
    w = (1, 1, 1, -1, -1, -1)
    assert mv(tr(b), w) == (0,) * 9
    p = tuple(tuple(Q(i == j) - Q(w[i] * w[j], 6) for j in range(6)) for i in range(6))
    assert tr(p) == p and mm(p, p) == p
    assert mm(p, b) == b and rank(p) == 5
    assert mv(p, w) == (0,) * 6
    data = mv(b, sp)
    assert data == (3, 1, 1, 3, 1, 1)
    assert mv(p, data) == data
    projected_checks = 0
    g0 = Q(1, 2) * norm2(data)
    for integers in product((-1, 0, 1), repeat=6):
        mu = tuple(map(Q, integers))
        q = mv(tr(b), mu)
        residual = mv(p, tuple(x - d for x, d in zip(mu, data)))
        gap = Q(1, 2) * norm2(residual) + sum(map(abs, q)) - g0
        rhs = Q(1, 2) * norm2(mv(p, mu)) + sum(abs(v) - t * v for v, t in zip(q, sp))
        assert gap == rhs and gap >= 0
        assert (gap == 0) == (mv(p, mu) == (0,) * 6)
        if gap == 0:
            assert q == (0,) * 9
        projected_checks += 1

    for epsilon in (Q(1), Q(1, 10), Q(1, 100), Q(1, 1000)):
        f0 = objective(((1,),), (1,), (0,))
        assert objective(((1,),), (1,), (epsilon,)) - f0 == epsilon * epsilon / 2
        assert objective(((1,),), (1,), (-epsilon,)) - f0 == 2 * epsilon + epsilon * epsilon / 2

    return {
        "status": "all_exact_checks_passed",
        "arithmetic": "Python integers and fractions.Fraction; no floating point",
        "binary_images_checked": binary_images_checked,
        "objective_identity_checks": identity_checks,
        "projected_objective_checks": projected_checks,
        "scalar_approximation_checks": 8,
        "matrix": [list(row) for row in a],
        "matrix_rank": rank(a),
        "datum": list(y),
        "binary_solution_count": len(ss),
        "binary_solutions": [list(s) for s in ss],
        "common_coordinate_vector": list(c),
        "exact_optimizer_by_proved_inequality": [0] * 5,
        "exact_recovered_vector": [0] * 9,
        "unique_solution_example_verified": True,
        "mixed_sign_unique_example_verified": True,
        "projector_identities_verified": True,
        "scope": "Finite checks supplement, and do not prove, the universal inequality in PROOF.md."
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
