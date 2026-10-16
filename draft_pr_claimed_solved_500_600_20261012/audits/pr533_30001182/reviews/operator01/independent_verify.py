#!/usr/bin/env python3
"""Independent exact finite controls for the operator audit.

Written before reading/running the authored verifier. Standard library only.
Infinite quantifiers and extremality are established in REPORT.md, not inferred
from finite enumeration here. All arithmetic is rational and exact.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path


def eye(n):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def diagonal(xs):
    return tuple(tuple(F(x) if i == j else F(0) for j in range(len(xs)))
                 for i, x in enumerate(xs))


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def scale(s, a):
    return tuple(tuple(s * x for x in ar) for ar in a)


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def transpose(a):
    return tuple(zip(*a))


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def outer(a, b):
    return tuple(tuple(x * y for y in b) for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def matvec(a, b):
    return tuple(dot(row, b) for row in a)


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    r = 0
    for j in range(len(a[0])):
        pivot = next((k for k in range(r, len(a)) if a[k][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        c = a[r][j]
        a[r] = [x / c for x in a[r]]
        for k in range(len(a)):
            if k != r:
                c = a[k][j]
                a[k] = [x - c * y for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** j * a[0][j]
               * det(tuple(tuple(a[i][k] for k in range(len(a)) if k != j)
                           for i in range(1, len(a))))
               for j in range(len(a)))


def saturated_graph_connected(n):
    vertices = set(product("PQ", range(n)))
    reached = {("P", 0)}
    frontier = list(reached)
    while frontier:
        kind, i = frontier.pop()
        for other in vertices - reached:
            if other[0] != kind and other[1] != i:
                reached.add(other)
                frontier.append(other)
    return reached == vertices


def run():
    unit = (F(1),) * 4
    p = tuple(map(F, (0, 0, 1, 1)))
    q = tuple(map(F, (0, 1, 0, 1)))
    pq = tuple(x * y for x, y in zip(p, q))
    assert rank([unit, p, q, pq]) == 4
    assert rank([unit, p]) == rank([unit, q]) == 2
    assert rank([unit, p, q]) == 3
    assert 2 + 2 - rank([unit, p, q]) == 1
    assert p != q
    i4, pm, qm = eye(4), diagonal(p), diagonal(q)
    assert mul(pm, pm) == pm and mul(qm, qm) == qm
    assert mul(pm, qm) == mul(qm, pm) == diagonal(pq)

    rational_weights = []
    gram_minor_count = 0
    basis_word_count = 0
    affine_word_count = 0
    for a, b in ((1, 1), (1, 2), (2, 1), (2, 3), (1, 0), (0, 1)):
        w = tuple(map(F, (a, 0, 0, b)))
        norm2 = dot(w, w)
        t = F(b * b, a * a + b * b)
        rho = scale(1 / norm2, outer(w, w))
        assert transpose(rho) == rho
        assert trace(rho) == 1 and mul(rho, rho) == rho and rank(rho) == 1

        def phi(m):
            return dot(w, matvec(m, w)) / norm2

        def diag_phi(vals):
            return (1 - t) * vals[0] + t * vals[3]

        for j in range(4):
            ej = diagonal(tuple(F(k == j) for k in range(4)))
            assert phi(ej) == diag_phi(tuple(F(k == j) for k in range(4)))
        assert phi(pm) == phi(qm) == phi(mul(pm, qm)) == t

        gram = ((F(1), t, t), (t, t, t), (t, t, t))
        assert matvec(gram, (0, 1, -1)) == (0, 0, 0)
        for k in range(1, 4):
            for subset in combinations(range(3), k):
                minor = tuple(tuple(gram[i][j] for j in subset) for i in subset)
                assert det(minor) >= 0
                gram_minor_count += 1

        # All binary-generator words up to degree ten. The source B*C map
        # allows arbitrary alternating affine letters; multilinearity reduces
        # those to these basis letters. No generator commutation is assumed
        # by this finite matrix loop.
        for length in range(11):
            for word in product((0, 1), repeat=length):
                upstairs = i4
                point_values = unit
                for letter in word:
                    upstairs = mul(upstairs, (pm, qm)[letter])
                    point_values = tuple(x * y for x, y in
                                         zip(point_values, (p, q)[letter]))
                assert phi(upstairs) == diag_phi(point_values)
                assert phi(upstairs) == (F(1) if not word else t)
                basis_word_count += 1

        # Deterministic rational affine letters, with subtraction and zeros.
        affine = ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)),
                  (F(1), F(-1)), (F(-3, 2), F(5, 3)))
        for length in range(6):
            for choices in product(range(len(affine)), repeat=length):
                upstairs = i4
                point_values = unit
                for position, choice in enumerate(choices):
                    c, d = affine[choice]
                    generator = (p, q)[position % 2]
                    letter_values = tuple(c + d * x for x in generator)
                    upstairs = mul(upstairs, diagonal(letter_values))
                    point_values = tuple(x * y for x, y in
                                         zip(point_values, letter_values))
                assert phi(upstairs) == diag_phi(point_values)
                affine_word_count += 1

        # Positive-state controls for rational test matrices, off-diagonal too.
        for seed in range(10):
            matrix = tuple(tuple(F(((seed + 3*i + 5*j) % 11) - 5, j + 1)
                                 for j in range(4)) for i in range(4))
            positive = mul(transpose(matrix), matrix)
            assert phi(positive) == dot(matvec(matrix, w), matvec(matrix, w)) / norm2
            assert phi(positive) >= 0

        # Explicit two-dimensional GNS quotient model with a weighted metric.
        r = diagonal((0, 1))
        omega, v = (F(1), F(1)), (F(0), F(1))
        g = diagonal((1 - t, t))
        assert matvec(r, omega) == matvec(r, v) == v
        assert dot(omega, matvec(g, omega)) == 1
        assert dot(omega, matvec(g, v)) == t
        assert det(g) == t * (1 - t)
        rational_weights.append(str(t))

    assert not saturated_graph_connected(2)
    assert all(saturated_graph_connected(n) for n in range(3, 10))
    rho_half = scale(F(1, 2), outer((1, 0, 0, 1), (1, 0, 0, 1)))
    e01 = tuple(tuple(F(i == 0 and j == 1) for j in range(4)) for i in range(4))
    e10 = transpose(e01)
    assert trace(mul(rho_half, mul(e01, e10))) == F(1, 2)
    assert trace(mul(rho_half, mul(e10, e01))) == 0
    assert trace(mul(rho_half, diagonal((0, 1, 0, 0)))) == 0

    return {
        "status": "PASS",
        "arithmetic": "Python standard-library Fraction; no floating point",
        "basis_rank": 4,
        "coordinate_dimensions": [2, 2],
        "intersection_dimension": 1,
        "tested_t": rational_weights,
        "density_checks": "trace one, rank one, symmetric, idempotent",
        "gram_principal_minor_checks": gram_minor_count,
        "binary_generator_word_checks": basis_word_count,
        "alternating_affine_word_checks": affine_word_count,
        "positive_matrix_checks": 60,
        "collapse_graph": "disconnected for n=2, connected for n=3,...,9",
        "nontracial_upstairs_pair": "E01 E10 moment 1/2; E10 E01 moment 0",
        "nonfaithful_upstairs_projection": "E11 moment 0",
        "limitations": "Finite exact controls only; proof covers every witness, copy, word and quotient category."
    }


if __name__ == "__main__":
    result = run()
    target = Path(__file__).with_name("independent_results.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
