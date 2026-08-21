#!/usr/bin/env python3
"""Explore the first E6 contact equation on exact-delta=2 {1,1} samples.

This is an exploratory derivation, not a verifier.  It computes the two
degree-(2,2,1) Hilbert--Burch tangents directly as the nullspace of the
E7 r^0 block, inserts their general linear combination, and extracts
[r]E6 with both quadratic r-coefficients of H2 retained.
"""

import sympy as sp

p, q, r, z = sp.symbols("p q r z")
c1, c2, x5, y5 = sp.symbols("c1 c2 x5 y5")
X, Y, Z = sp.symbols("X Y Z")
Apar, Bpar, Cpar, Dpar = sp.symbols(
    "Apar Bpar Cpar Dpar", nonzero=True
)


def jac(f, g):
    return sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p)


def homogeneous_coefficients(poly, degree):
    expanded = sp.Poly(sp.expand(poly), p, q)
    return [
        expanded.coeff_monomial(p ** (degree - j) * q**j)
        for j in range(degree + 1)
    ]


def coefficient_matrix(forms, unknowns):
    return sp.Matrix(
        [[sp.expand(form).coeff(unknown) for unknown in unknowns] for form in forms]
    )


def sample(label, h, R, verbose=False):
    P = sp.expand(h * p**2)
    Q = sp.expand(h * q**2)
    alpha = sp.expand(jac(Q, R))
    beta = sp.expand(-jac(P, R))
    gamma = sp.expand(jac(P, Q))

    uu = sp.symbols(f"{label}_u0:3")
    vv = sp.symbols(f"{label}_v0:3")
    tt = sp.symbols(f"{label}_t0:2")
    u = uu[0] * p**2 + uu[1] * p * q + uu[2] * q**2
    v = vv[0] * p**2 + vv[1] * p * q + vv[2] * q**2
    t = tt[0] * p + tt[1] * q
    unknowns = (*uu, *vv, *tt)
    equations = homogeneous_coefficients(alpha * u + beta * v + gamma * t, 7)
    matrix = coefficient_matrix(equations, unknowns)
    kernel = matrix.nullspace()
    assert matrix.rank() == 6 and len(kernel) == 2

    tangents = []
    for vector in kernel:
        substitution = dict(zip(unknowns, vector))
        tangents.append(
            (
                sp.factor(u.subs(substitution)),
                sp.factor(v.subs(substitution)),
                sp.factor(t.subs(substitution)),
            )
        )

    tangent = tuple(
        sp.expand(c1 * tangents[0][i] + c2 * tangents[1][i])
        for i in range(3)
    )
    U, V, T = r * tangent[0], r * tangent[1], r * tangent[2]
    A, B = x5 * r**2, y5 * r**2
    H4 = sp.Matrix([P, Q, 0])
    H3 = sp.Matrix([U, V, R])
    H2 = sp.Matrix([A, B, T])
    variables = (p, q, r)
    weighted = sp.Poly(
        sp.expand((z**3 * H4.jacobian(variables)
                   + z**2 * H3.jacobian(variables)
                   + z * H2.jacobian(variables)).det()),
        z,
    )
    E6r = sp.factor(
        sp.Poly(sp.expand(weighted.coeff_monomial(z**6)), r).coeff_monomial(r)
    )
    e6 = [sp.factor(value) for value in homogeneous_coefficients(E6r, 5)]
    lifted = []
    for value in e6:
        poly = sp.Poly(sp.expand(value), c1, c2)
        lifted.append(
            sp.expand(
                poly.coeff_monomial(c1**2) * X
                + poly.coeff_monomial(c1 * c2) * Y
                + poly.coeff_monomial(c2**2) * Z
                + poly.coeff_monomial(1)
            )
        )
    lifted_matrix = coefficient_matrix(lifted, (X, Y, Z, x5, y5))
    lifted_kernel = lifted_matrix.nullspace()
    ideal = sp.groebner(e6, x5, y5, c1, c2)

    print(f"=== {label} ===")
    print("h =", h)
    print("R =", R)
    print("gcd =", sp.factor(sp.gcd(sp.gcd(alpha, beta), gamma)))
    if verbose:
        print("tangents =", tangents)
        print("[r]E6 =", E6r)
    print("lifted rank =", lifted_matrix.rank())
    if len(lifted_kernel) == 1:
        generator = [sp.factor(value) for value in lifted_kernel[0]]
        print("lifted kernel =", generator)
        print("Veronese obstruction =", sp.factor(generator[1] ** 2 - generator[0] * generator[2]))
    print("Groebner =", [sp.factor(poly.as_expr()) for poly in ideal.polys])


sample("pq_two_roots", p * q, p * q * (p + q))
sample("pq_double_p", p * q, p**2 * (p + q))
sample("p2_order", p**2, p * q**2 + q**3)
sample("pq_two_roots_general", p * q, p * q * (Apar * p + Bpar * q))
sample("pq_double_p_general", p * q, p**2 * (Apar * p + Bpar * q))
sample(
    "p2_baseline_contact_general",
    p**2,
    Apar * p**3 + Cpar * p * q**2 + Dpar * q**3,
)
sample(
    "p2_simple_fixed_general",
    p**2,
    p * (Apar * p**2 + Bpar * p * q + Cpar * q**2),
)
sample(
    "p2_simple_fixed_e6_survivor",
    p**2,
    p * (-11 * p**2 + 16 * p * q + q**2),
    verbose=True,
)

ell = p + q
sample("pell_double_p", p * ell, p**2 * (2 * p + q))
sample("pell_double_ell", p * ell, ell**2 * (p + q))
sample("pell_two_fixed", p * ell, p * ell * (2 * p + q))
sample("pell_p_contact", p * ell, p * (4 * p**2 + 3 * p * q + q**2))
sample(
    "pell_ell_contact",
    p * ell,
    ell * (-4 * p**2 + p * q + q**2),
)

fixed_l = p - 2 * q
fixed_m = 2 * p - q
h_squarefree = sp.expand(fixed_l * fixed_m)
sample("interior_double_fixed", h_squarefree, fixed_l**2 * (p + q))
sample("interior_two_fixed", h_squarefree, h_squarefree * (p + q))
sample(
    "interior_fixed_contact",
    h_squarefree,
    fixed_l * (p**2 - 11 * p * q + 8 * q**2),
)
sample(
    "interior_two_contacts",
    h_squarefree,
    8 * p**3 - 15 * p**2 * q - 15 * p * q**2 + 8 * q**3,
)

h_double = (p + q) ** 2
sample("double_nonbranch_fixed", h_double, (p + q) * (p**2 + p * q + 3 * q**2))
sample(
    "double_nonbranch_contact",
    h_double,
    p**3 + p**2 * q + sp.Rational(3, 2) * p * q**2 + q**3,
)
