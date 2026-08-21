#!/usr/bin/env python3
"""Exact E7/E6 probe with binary lower summands initially set to zero.

For a fixed (h,R), the script reconstructs the r^1 and r^0 E7 syzygy
spaces, builds their complete nonbinary tangent, and computes the exact
quadratic compatibility ideal for E6.  This is a representative-scoped
construction probe, not an orbit classification.
"""

from __future__ import annotations

import sys

import sympy as sp

if not __debug__:
    print("FAIL: assertions disabled", file=sys.stderr)
    raise SystemExit(2)

p, q, r, wt = sp.symbols("p q r wt")
coords = (p, q, r)


def homogeneous_exponents(degree, variables=3):
    if variables == 2:
        return tuple((degree - j, j) for j in range(degree + 1))
    return tuple(
        (i, j, degree - i - j)
        for i in range(degree, -1, -1)
        for j in range(degree - i, -1, -1)
    )


def homogeneous_coefficients(poly, degree, variables=3):
    if variables == 2:
        pp = sp.Poly(sp.expand(poly), p, q)
        return [pp.coeff_monomial(p**i * q**j) for i, j in homogeneous_exponents(degree, 2)]
    pp = sp.Poly(sp.expand(poly), p, q, r)
    return [
        pp.coeff_monomial(p**i * q**j * r**k)
        for i, j, k in homogeneous_exponents(degree, 3)
    ]


def jac2(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def syzygy_space(alpha, beta, gamma, degree):
    """Return coefficient vectors for (a,b,c) with degrees (degree,degree,degree-1)."""
    avars = sp.symbols(f"sa{degree}_0:{degree + 1}")
    bvars = sp.symbols(f"sb{degree}_0:{degree + 1}")
    cvars = sp.symbols(f"sc{degree}_0:{degree}")
    amons = [p ** (degree - j) * q**j for j in range(degree + 1)]
    cmons = [p ** (degree - 1 - j) * q**j for j in range(degree)]
    aa = sum(value * monomial for value, monomial in zip(avars, amons))
    bb = sum(value * monomial for value, monomial in zip(bvars, amons))
    cc = sum(value * monomial for value, monomial in zip(cvars, cmons))
    variables = avars + bvars + cvars
    equation = sp.expand(alpha * aa + beta * bb + gamma * cc)
    matrix, rhs = sp.linear_eq_to_matrix(
        homogeneous_coefficients(equation, 5 + degree, variables=2),
        variables,
    )
    assert rhs == sp.zeros(matrix.rows, 1)
    nullspace = matrix.nullspace()
    triples = []
    for vector in nullspace:
        substitution = dict(zip(variables, vector))
        triples.append(
            (
                sp.factor(aa.subs(substitution)),
                sp.factor(bb.subs(substitution)),
                sp.factor(cc.subs(substitution)),
            )
        )
    return triples


def unique_nonzero(polynomials):
    out = []
    for polynomial in polynomials:
        value = sp.factor(polynomial)
        if value == 0:
            continue
        pp = sp.Poly(value)
        _, primitive = pp.primitive()
        value = sp.factor(primitive.as_expr())
        lead = sp.Poly(value).LC()
        if lead < 0:
            value = -value
        if value not in out:
            out.append(value)
    return tuple(out)


def analyze(label, h, R):
    P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
    alpha, beta, gamma = jac2(Q, R), -jac2(P, R), jac2(P, Q)
    g = sp.gcd(sp.gcd(sp.Poly(alpha, p, q), sp.Poly(beta, p, q)), sp.Poly(gamma, p, q))
    assert sp.Matrix(
        [
            homogeneous_coefficients(alpha, 5, variables=2),
            homogeneous_coefficients(beta, 5, variables=2),
        ]
    ).rank() == 2
    syz1 = syzygy_space(alpha, beta, gamma, 1)
    syz2 = syzygy_space(alpha, beta, gamma, 2)
    delta = g.total_degree()
    assert len(syz1) == delta - 2
    assert len(syz2) == delta

    parameters1 = sp.symbols(f"{label}_x0:{len(syz1)}")
    parameters2 = sp.symbols(f"{label}_y0:{len(syz2)}")
    U2 = sum((value * triple[0] for value, triple in zip(parameters1, syz1)), sp.S.Zero)
    V2 = sum((value * triple[1] for value, triple in zip(parameters1, syz1)), sp.S.Zero)
    T2 = sum((value * triple[2] for value, triple in zip(parameters1, syz1)), sp.S.Zero)
    U1 = sum((value * triple[0] for value, triple in zip(parameters2, syz2)), sp.S.Zero)
    V1 = sum((value * triple[1] for value, triple in zip(parameters2, syz2)), sp.S.Zero)
    T1 = sum((value * triple[2] for value, triple in zip(parameters2, syz2)), sp.S.Zero)

    # Factors 1/2 are inserted because differentiating r^2 doubles its
    # coefficient; this makes E7 exactly the displayed syzygy relation.
    U = sp.expand(r * U1 + sp.Rational(1, 2) * r**2 * U2)
    V = sp.expand(r * V1 + sp.Rational(1, 2) * r**2 * V2)
    T = sp.expand(r * T1 + sp.Rational(1, 2) * r**2 * T2)

    avars = sp.symbols(f"{label}_a0:3")
    bvars = sp.symbols(f"{label}_b0:3")
    l33 = sp.symbols(f"{label}_l33")
    A = r * (avars[0] * p + avars[1] * q) + avars[2] * r**2
    B = r * (bvars[0] * p + bvars[1] * q) + bvars[2] * r**2
    L = sp.zeros(3)
    L[2, 2] = l33
    H2 = sp.Matrix([A, B, T])
    H3 = sp.Matrix([U, V, R])
    H4 = sp.Matrix([P, Q, 0])
    determinant = sp.Poly(
        sp.expand(
            (
                L
                + wt * H2.jacobian(coords)
                + wt**2 * H3.jacobian(coords)
                + wt**3 * H4.jacobian(coords)
            ).det()
        ),
        wt,
    )
    assert determinant.coeff_monomial(wt**7) == 0
    e6 = determinant.coeff_monomial(wt**6)
    lower = avars + bvars + (l33,)
    equations = homogeneous_coefficients(e6, 6)
    matrix, rhs = sp.linear_eq_to_matrix(equations, lower)
    compatibility = unique_nonzero(
        (left.T * rhs)[0] for left in matrix.T.nullspace()
    )
    tangent_parameters = parameters1 + parameters2
    groebner_basis = sp.groebner(compatibility, *tangent_parameters, order="grevlex")

    print(f"{label}: delta={delta}, h={sp.factor(h)}, R={sp.factor(R)}")
    print(f"  gcd={sp.factor(g.as_expr())}")
    print(f"  degree-1 syzygies={syz1}")
    print(f"  degree-2 syzygies={syz2}")
    print(f"  E6 lower matrix shape={matrix.shape}, rank={matrix.rank()}")
    print(f"  E6 compatibility={compatibility}")
    print(f"  E6 Groebner={tuple(sp.factor(poly.as_expr()) for poly in groebner_basis.polys)}")
    return {
        "label": label,
        "delta": delta,
        "syzygies1": syz1,
        "syzygies2": syz2,
        "parameters": tangent_parameters,
        "compatibility": compatibility,
    }


def main():
    branches = (
        ("D3_P2_A", p**2, p**2 * (p + q)),
        ("D3_P2_B", p**2, p * (p**2 + q**2)),
        ("D3_PQ", p * q, p**3),
        ("D3_PELL_1", p * (p + q), p**3),
        ("D3_PELL_2", p * (p + q), p**2 * (p + q)),
        ("D4_DOUBLE_H", (p + q) ** 2, (p + q) ** 3),
        ("D4_DOUBLE_Q", (p + q) ** 2, (p + q) **2 * (2 * p - q)),
        ("D4_DOUBLE_P", (p + q) ** 2, (p + q) **2 * (p - 2 * q)),
        (
            "D4_DOUBLE_MIX",
            (p + q) ** 2,
            (p + q) * (2 * p**2 + p * q + 2 * q**2),
        ),
    )
    selected = set(sys.argv[1:])
    for branch in branches:
        if not selected or branch[0] in selected:
            analyze(*branch)


if __name__ == "__main__":
    main()
