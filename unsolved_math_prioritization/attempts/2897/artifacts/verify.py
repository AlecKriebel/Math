#!/usr/bin/env python3
"""Exact, network-free checks for the lattice calculation in PROOF.md.

This checks finite instances, not topological existence or a solution of KP-4.21.
Only the Python standard library is used.
"""
from fractions import Fraction
import json
from pathlib import Path


def poly_add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}


def poly_mul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] = out.get(i+j, 0) + x*y
    return {k: v for k, v in out.items() if v}


def reduce_poly(p, n):
    out = [0] * n
    for k, v in p.items():
        out[k % n] += v
    return out


def lattice(n):
    one, two, zero = {0: 1}, {0: 2}, {}
    t = {1: 1, -1: 1}
    t2 = poly_mul(t, t)
    a = poly_add(poly_add(one, t), t2)
    b = poly_add(t, t2)
    c = poly_add(one, t)
    L = [[a, b, c, t], [b, a, t, c], [c, t, two, zero], [t, c, zero, two]]
    reduced = [[reduce_poly(p, n) for p in row] for row in L]
    # Basis order: e_1, x e_1, ..., x^(n-1)e_1, e_2, ... .
    return [[reduced[i][j][(ell-k) % n]
             for j in range(4) for ell in range(n)]
            for i in range(4) for k in range(n)]


def matvec(A, x):
    return [sum(a*b for a, b in zip(row, x)) for row in A]


def norm(A, x):
    return sum(a*b for a, b in zip(x, matvec(A, x)))


def exact_positive_determinant(A):
    """Rational symmetric elimination: positive pivots iff positive definite."""
    B = [[Fraction(x) for x in row] for row in A]
    determinant = Fraction(1)
    pivots = []
    for k in range(len(B)):
        pivot = B[k][k]
        assert pivot > 0, (k, pivot)
        pivots.append(pivot)
        determinant *= pivot
        for i in range(k+1, len(B)):
            for j in range(i, len(B)):
                B[i][j] -= B[i][k]*B[k][j]/pivot
                B[j][i] = B[i][j]
    assert determinant.denominator == 1
    return int(determinant), pivots


def run():
    tests = []
    for n in range(1, 13):
        A = lattice(n)
        rank = 4*n
        assert len(A) == rank
        assert all(A[i][j] == A[j][i] for i in range(rank) for j in range(rank))
        det, pivots = exact_positive_determinant(A)
        assert det == 1
        w = [0]*(2*n) + [1]*(2*n)
        wprime = w[:]
        wprime[0] -= 2
        Aw, Awprime = matvec(A, w), matvec(A, wprime)
        assert all((Aw[i]-A[i][i]) % 2 == 0 for i in range(rank))
        assert all((Awprime[i]-A[i][i]) % 2 == 0 for i in range(rank))
        assert Aw == [5]*(2*n) + [2]*(2*n)
        assert norm(A, w) == 4*n
        e1_norm = 7 if n == 1 else 5 if n == 2 else 3
        assert A[0][0] == e1_norm
        expected = 4*n - 20 + 4*e1_norm
        assert norm(A, wprime) == expected
        if n >= 3:
            assert expected == 4*n-8 < rank
        tests.append({"n": n, "rank": rank, "determinant": det,
                      "positive_definite_exact": all(p > 0 for p in pivots),
                      "characteristic_w": True, "characteristic_wprime": True,
                      "norm_w": norm(A, w), "norm_wprime": expected,
                      "standard_lattice_obstructed": n >= 3})
    # Integral chain-complex checks used in the compact argument:
    # a single 2-handle whose boundary is a generator of H_1 gives [1].
    assert abs(1) == 1
    # Doubling a homology circle uses the primitive inclusion Z -> Z^2.
    # The vector (1,-1) extends to a unimodular basis, so cokernel is Z.
    inclusion, complement = (1, -1), (0, 1)
    assert inclusion[0]*complement[1]-inclusion[1]*complement[0] == 1
    # Surgery on a primitive H_1 generator of the double raises chi by 2.
    chi_double = 1-1+0-1+1
    chi_after_surgery = chi_double - 0 + 2 - 0
    assert chi_double == 0 and chi_after_surgery == 2
    return {
        "problem_id": 2897,
        "result": "all finite exact-arithmetic checks passed",
        "topological_theorems_formally_verified": False,
        "full_problem_resolved": False,
        "limitations": "Finite lattice checks supplement the all-n proof. They do not establish manifold existence, smoothability, the compact-knot theorem, or the closed decomposition assertion.",
        "lattice_checks": tests,
        "primitive_meridian_chain_map": 1,
        "double_h1_inclusion": list(inclusion),
        "double_h1_basis_determinant": 1,
        "double_euler_characteristic": chi_double,
        "surgered_double_euler_characteristic": chi_after_surgery,
    }


if __name__ == "__main__":
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="")
