#!/usr/bin/env python3
"""Exact E6/E5 survivor search in frozen family D3-BS-N1-CONTACT.

The full E7 parameterization is retained.  Each sampled top point fixes the
binary cubic/quadratic summands, after which E6 and E5 are affine-linear in
the twelve coefficients of A,B and the nine entries of L.  We keep the full
affine solution fibre and test whether det(L) is nonzero on it.
"""

from __future__ import annotations

import argparse
import itertools
import random

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
coords = (p, q, r)
mon2 = (p**2, p*q, p*r, q**2, q*r, r**2)
mon2b = (p**2, p*q, q**2)
mon3b = (p**3, p**2*q, p*q**2, q**3)

aa = sp.symbols("a0:6")
bb = sp.symbols("b0:6")
ll = sp.symbols("l0:9")
lower = aa + bb + ll
A = sum(c*m for c, m in zip(aa, mon2))
B = sum(c*m for c, m in zip(bb, mon2))
L = sp.Matrix(3, 3, ll)

h = p**2
P = p**4
Q = p**2*q**2
R = p*(p**2+q**2)


def coeffs(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i*q**j*r**(degree-i-j))
        for i in range(degree, -1, -1)
        for j in range(degree-i, -1, -1)
    ]


def determinant(top):
    x, y0, y1, y2, uc, vc, tc = top
    U0 = sum(c*m for c, m in zip(uc, mon3b))
    V0 = sum(c*m for c, m in zip(vc, mon3b))
    T0 = sum(c*m for c, m in zip(tc, mon2b))
    U = U0 + 4*y0*p**2*r
    V = V0 + r*((-3*y0+y1)*p**2+y2*p*q+y0*q**2) + sp.Rational(1,2)*x*p*r**2
    T = T0 + r*(y1*p+y2*q) + sp.Rational(1,2)*x*r**2
    H2 = sp.Matrix([A, B, T])
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    det = sp.Poly(sp.expand((L+z*H2.jacobian(coords)+z**2*H3.jacobian(coords)+z**3*H4.jacobian(coords)).det()), z)
    assert all(det.coeff_monomial(z**d) == 0 for d in (9,8,7))
    return det, (U,V,T)


def solve_fibre(det):
    equations = coeffs(det.coeff_monomial(z**6), 6) + coeffs(det.coeff_monomial(z**5), 5)
    M, rhs = sp.linear_eq_to_matrix(equations, lower)
    if M.rank() != M.row_join(rhs).rank():
        return None
    solution = tuple(next(iter(sp.linsolve((M, rhs), lower))))
    sub = dict(zip(lower, solution))
    detL = sp.factor(L.subs(sub).det())
    return M.rank(), solution, sub, detL


def det_witness(solution, detL):
    if detL == 0:
        return None
    free = sorted(set().union(*(v.free_symbols for v in solution)) & set(lower), key=str)
    tests = [{v: 0 for v in free}]
    for v in free:
        tests.extend({w: (t if w == v else 0) for w in free} for t in (-2,-1,1,2))
    for vals in tests:
        if sp.factor(detL.subs(vals)) != 0:
            return vals
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trials", type=int, default=160)
    ap.add_argument("--seed", type=int, default=20260726)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    tops = []
    # Exhaust small tangent points on both irreducible E6 components first.
    vals = (-1,0,1)
    for x,y1,y2 in itertools.product(vals, repeat=3):
        if (x,y1,y2) != (0,0,0):
            tops.append((x,0,y1,y2))
    for y0,y1 in itertools.product((-1,1), vals):
        tops.append((0,y0,y1,0))
    while len(tops) < args.trials:
        x,y1,y2 = (rng.choice((-2,-1,0,1,2)) for _ in range(3))
        tops.append((x,0,y1,y2))

    binary_points = [(0,)*11]
    for i in range(11):
        for value in (-1,1):
            v = [0]*11
            v[i] = value
            binary_points.append(tuple(v))
    for _ in range(40):
        binary_points.append(tuple(rng.choice((-1,0,1)) for _ in range(11)))

    best = None
    tested = consistent = invertible = 0
    for tangent in tops:
        for bv in binary_points:
            tested += 1
            top = tangent + (bv[:4],bv[4:8],bv[8:])
            det, forms = determinant(top)
            fibre = solve_fibre(det)
            if fibre is None:
                continue
            consistent += 1
            rank, solution, sub, detL = fibre
            witness = det_witness(solution, detL)
            if witness is None:
                continue
            invertible += 1
            free_count = len(set().union(*(v.free_symbols for v in solution)) & set(lower))
            data = (free_count, -rank, tangent, bv, forms, solution, detL, witness, det)
            if best is None or data[:2] > best[:2]:
                best = data
                print("NEW_BEST", "free", free_count, "rank", rank,
                      "tangent", tangent, "binary", bv, "detL", detL,
                      "witness", witness, flush=True)
    print("SUMMARY", tested, consistent, invertible)
    if best:
        free_count, neg_rank, tangent, bv, forms, solution, detL, witness, det = best
        print("BEST_TANGENT", tangent)
        print("BEST_BINARY", bv)
        print("BEST_FORMS", tuple(sp.expand(v) for v in forms))
        print("BEST_RANK", -neg_rank, "FREE", free_count)
        print("BEST_SOLUTION", solution)
        print("BEST_DETL", detL)
        print("BEST_WITNESS", witness)
        full = dict(zip(lower, solution)) | witness
        for degree in (4,3,2,1):
            residual = tuple(sp.factor(v.subs(full)) for v in coeffs(det.coeff_monomial(z**degree),degree))
            print("RESIDUAL", degree, tuple(v for v in residual if v != 0))


if __name__ == "__main__":
    main()
