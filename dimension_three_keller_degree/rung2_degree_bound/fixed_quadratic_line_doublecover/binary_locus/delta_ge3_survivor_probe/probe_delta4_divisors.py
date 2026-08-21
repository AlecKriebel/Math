#!/usr/bin/env python3
"""Exact fixed-representative probe for possible delta=4 points.

For each standard split fixed quadratic h, every degree-four homogeneous
divisor of gamma=J(h*p^2,h*q^2) is tested.  Divisibility of alpha and beta
is imposed by a linear coefficient system, without Gröbner elimination.
The script reports only existence/nonexistence for the displayed h's.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

p, q = sp.symbols("p q")
a, b, c, d = sp.symbols("a b c d")
u0, u1, v0, v1 = sp.symbols("u0 u1 v0 v1")
R_VARS = (a, b, c, d)
ALL_VARS = R_VARS + (u0, u1, v0, v1)


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def coeffs(poly, degree):
    pp = sp.Poly(sp.expand(poly), p, q)
    return [pp.coeff_monomial(p ** (degree - j) * q**j) for j in range(degree + 1)]


def homogeneous_factor_multiset(poly):
    scalar, factors = sp.factor_list(poly)
    del scalar
    out = []
    for factor, multiplicity in factors:
        if sp.Poly(factor, p, q).total_degree() != 1:
            raise AssertionError(f"nonlinear factor in split test: {factor}")
        out.append((sp.factor(factor), multiplicity))
    return out


def exponent_vectors(bounds, total):
    for exponents in product(*(range(bound + 1) for bound in bounds)):
        if sum(exponents) == total:
            yield exponents


def projected_vectors(nullspace):
    return [sp.Matrix(vector[:4, :]) for vector in nullspace if any(vector[index] != 0 for index in range(4))]


def candidate_combinations(vectors):
    yielded = set()
    coefficients = (-2, -1, 0, 1, 2)
    for weights in product(coefficients, repeat=len(vectors)):
        if not any(weights):
            continue
        vector = sum((weight * vec for weight, vec in zip(weights, vectors)), sp.zeros(4, 1))
        if vector == sp.zeros(4, 1):
            continue
        # Projective integer normalization for de-duplication.
        den = sp.ilcm(*(entry.q for entry in vector))
        ints = [int(entry * den) for entry in vector]
        common = abs(sp.igcd(*ints))
        ints = [entry // common for entry in ints]
        first = next(entry for entry in ints if entry)
        if first < 0:
            ints = [-entry for entry in ints]
        key = tuple(ints)
        if key not in yielded:
            yielded.add(key)
            yield sp.Matrix(ints)


def analyze(h):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    R = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
    factor_data = homogeneous_factor_multiset(gamma)
    solutions = []
    print(f"h={sp.factor(h)} gamma={sp.factor(gamma)}")
    for exponents in exponent_vectors([mult for _, mult in factor_data], 4):
        g = sp.prod(factor**exponent for (factor, _), exponent in zip(factor_data, exponents))
        equations = coeffs(alpha - g * (u0 * p + u1 * q), 5)
        equations += coeffs(beta - g * (v0 * p + v1 * q), 5)
        matrix, rhs = sp.linear_eq_to_matrix(equations, ALL_VARS)
        assert rhs == sp.zeros(12, 1)
        nullspace = matrix.nullspace()
        projected = projected_vectors(nullspace)
        if not projected:
            continue
        witness = None
        for vector in candidate_combinations(projected):
            substitution = dict(zip(R_VARS, vector))
            aa, bb = sp.expand(alpha.subs(substitution)), sp.expand(beta.subs(substitution))
            if sp.Matrix(
                [
                    coeffs(aa, 5),
                    coeffs(bb, 5),
                ]
            ).rank() != 2:
                continue
            gg = sp.gcd(sp.gcd(sp.Poly(aa, p, q), sp.Poly(bb, p, q)), sp.Poly(gamma, p, q))
            if gg.total_degree() == 4:
                witness = (vector, sp.factor(gg.as_expr()), sp.factor(aa), sp.factor(bb))
                break
        print(
            f"  divisor={sp.factor(g)} nullity={len(nullspace)} "
            f"R-proj={len(projected)} witness={witness}"
        )
        if witness:
            solutions.append((g, witness))
    print(f"  EXACT-DELTA4 WITNESSES: {len(solutions)}")
    return solutions


def main():
    representatives = (
        p**2,
        p * q,
        p * (p + q),
        (p + q) ** 2,
        (p + q) * (p + 2 * q),
    )
    total = 0
    for h in representatives:
        total += len(analyze(h))
    print(f"DELTA4_SPLIT_REPRESENTATIVE_WITNESS_COUNT={total}")


if __name__ == "__main__":
    main()
