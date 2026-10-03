#!/usr/bin/env python3
"""Independent exact block-matrix checks, using only the Python standard library.

These checks certify finite lattice identities, not any topological theorem.
Run with Python 3; the JSON output is deterministic.
"""
import json


def add(*matrices):
    return [[sum(M[i][j] for M in matrices) for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def multiply(A, B):
    return [[sum(a*b for a, b in zip(row, col)) for col in zip(*B)] for row in A]


def block(P, Q, R, S):
    return [p+q for p, q in zip(P, Q)] + [r+s for r, s in zip(R, S)]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def scalar(c, A):
    return [[c*x for x in row] for row in A]


def vector_product(A, v):
    return [sum(a*x for a, x in zip(row, v)) for row in A]


def norm(A, v):
    return sum(x*y for x, y in zip(v, vector_product(A, v)))


def run():
    rows = []
    for n in range(1, 13):
        I = identity(n)
        # T = S + S^T for the permutation matrix of one cyclic shift.
        # Addition (rather than boolean adjacency) retains multiplicities n=1,2.
        S = [[int(j == (i+1) % n) for j in range(n)] for i in range(n)]
        T = add(S, list(map(list, zip(*S))))
        T2 = multiply(T, T)
        A = block(add(I, T, T2), add(T, T2), add(T, T2), add(I, T, T2))
        B = block(add(I, T), T, T, add(I, T))
        I2 = identity(2*n)
        L = block(A, B, B, scalar(2, I2))
        assert L == list(map(list, zip(*L)))
        # Schur complement: A - B (2I)^(-1) B^T = I/2.
        # This gives positive definiteness and determinant 1 exactly.
        schur_identity = add(scalar(2, A), scalar(-1, multiply(B, B))) == I2
        assert schur_identity
        w = [0]*(2*n) + [1]*(2*n)
        wp = w[:]
        wp[0] -= 2
        vw, vwp = vector_product(L, w), vector_product(L, wp)
        assert vw == [5]*(2*n) + [2]*(2*n)
        characteristic_w = all((vw[i]-L[i][i]) % 2 == 0 for i in range(4*n))
        characteristic_wp = all((vwp[i]-L[i][i]) % 2 == 0 for i in range(4*n))
        assert characteristic_w and characteristic_wp
        assert norm(L, w) == 4*n
        e1_norm = 7 if n == 1 else 5 if n == 2 else 3
        assert L[0][0] == e1_norm
        assert norm(L, wp) == 4*n-20+4*e1_norm
        rows.append({
            'n': n, 'rank': 4*n, 'determinant': 1,
            'positive_definite_exact': schur_identity,
            'characteristic_w': characteristic_w,
            'characteristic_wprime': characteristic_wp,
            'norm_w': norm(L, w), 'norm_wprime': norm(L, wp),
            'standard_lattice_obstructed': norm(L, wp) < 4*n,
        })
    return {
        'method': 'Independent cyclic-shift matrices and exact Schur-complement certificate',
        'lattice_checks': rows,
        'finite_checks_only': True,
        'topological_theorems_formally_verified': False,
        'full_problem_resolved': False,
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
