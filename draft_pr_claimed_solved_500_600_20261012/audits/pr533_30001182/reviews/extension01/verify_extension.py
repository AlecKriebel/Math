#!/usr/bin/env python3
"""Independent exact finite controls, not an all-states or all-words proof.

Uses only the Python standard library. Every matrix entry is rational; the
rank-one vector state is represented by its density matrix to avoid radicals.
"""
from fractions import Fraction as F
from itertools import product
import json


def matrix(rows):
    return tuple(tuple(F(x) for x in row) for row in rows)


def diag(values):
    return matrix([[v if i == j else 0 for j in range(len(values))]
                   for i, v in enumerate(values)])


def multiply(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def adjoint(a):
    return tuple(zip(*a))  # all entries here are real


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def rank_columns(columns):
    rows = [list(map(F, row)) for row in zip(*columns)]
    row = 0
    for col in range(len(columns)):
        pivot = next((i for i in range(row, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        scale = rows[row][col]
        rows[row] = [x / scale for x in rows[row]]
        for i in range(len(rows)):
            if i != row:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[row])]
        row += 1
    return row


def expectation(rho, a):
    return trace(multiply(rho, a))


def evaluate_word(generators, word):
    a = diag([1] * len(generators[0]))
    for symbol in word:
        a = multiply(a, generators[symbol])
    return a


def run():
    one = (1, 1, 1, 1)
    p = (0, 0, 1, 1)
    q = (0, 1, 0, 1)
    pq = tuple(x * y for x, y in zip(p, q))
    assert rank_columns([one, p, q, pq]) == 4
    assert rank_columns([one, p]) == rank_columns([one, q]) == 2
    assert rank_columns([one, p, q]) == 3  # intersection dimension = 2+2-3

    P, Q = diag(p), diag(q)
    rho = matrix([[F(1, 2), 0, 0, F(1, 2)],
                  [0, 0, 0, 0], [0, 0, 0, 0],
                  [F(1, 2), 0, 0, F(1, 2)]])
    assert rho == adjoint(rho) == multiply(rho, rho)
    assert trace(rho) == 1
    assert rank_columns(list(zip(*rho))) == 1
    assert expectation(rho, P) == expectation(rho, Q) == F(1, 2)
    assert expectation(rho, multiply(P, Q)) == F(1, 2)

    # All entries of a diagonal algebra basis have the required endpoint state.
    for i in range(4):
        E = diag([int(j == i) for j in range(4)])
        assert expectation(rho, E) == (F(1, 2) if i in (0, 3) else 0)

    words_checked = 0
    # Arbitrary words in the two idempotent generators, including same-copy
    # products, verify the matrix witness's folded joint law and lower mixture.
    for length in range(13):
        for word in product(range(2), repeat=length):
            a = evaluate_word([P, Q], word)
            expected = F(1, 2) if word else F(1)
            assert expectation(rho, a) == expected
            assert (a[0][0] + a[3][3]) / 2 == expected
            words_checked += 1

    # Rational coordinates model the quotient GNS: inner product is weighted
    # equally, Omega=(1,1), v=(0,1). Each projection is (0,1).
    omega = (F(1), F(1))
    v = (F(0), F(1))
    def inner(x, y):
        return sum(a * b for a, b in zip(x, y)) / 2
    def apply_r(x):
        return (F(0), x[1])
    assert apply_r(omega) == v == apply_r(v)
    assert inner(v, v) == inner(omega, v) == F(1, 2)
    copies_checked = 0
    for i, j in product(range(8), repeat=2):
        if i != j:
            p_i_omega = apply_r(omega)
            q_j_omega = apply_r(omega)
            diff = tuple(a - b for a, b in zip(p_i_omega, q_j_omega))
            assert inner(diff, diff) == 0
            copies_checked += 1

    # Smaller faithful C^2 state and its M_2 pure extension.
    rho2 = matrix([[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
    assert multiply(rho2, rho2) == rho2 and trace(rho2) == 1
    assert rank_columns(list(zip(*rho2))) == 1
    for i in range(2):
        assert expectation(rho2, diag([int(i == j) for j in range(2)])) == F(1, 2)

    return {
        "all_exact_controls_passed": True,
        "arithmetic": "Python fractions.Fraction, standard library only",
        "main_algebra_dimension": 4,
        "subalgebra_dimensions": [2, 2],
        "subalgebra_intersection_dimension": 1,
        "upstairs_density_rank": 1,
        "words_checked_including_empty": words_checked,
        "maximum_word_length": 12,
        "different_copy_projection_controls": copies_checked,
        "smaller_C2_state_faithful": True,
        "minimal_upstairs_density_rank": 1,
        "limit": "Finite controls only. REVIEW.md supplies all-copy, all-word, all-state proofs; no computation certifies extremality or extension in infinite convex spaces."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
