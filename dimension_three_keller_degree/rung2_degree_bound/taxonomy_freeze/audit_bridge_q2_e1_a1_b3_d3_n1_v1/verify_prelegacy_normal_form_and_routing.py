#!/usr/bin/env python3
"""Exact checks for the frozen-only normal form and C00--C44 routing."""

from __future__ import annotations

from itertools import product
from random import Random

import sympy as sp


x, y, z, u, v, X, Y, Z = sp.symbols("x y z u v X Y Z")
VARS = (x, y, z)
MONOMIALS4 = (
    x**4,
    x**3 * y,
    x**3 * z,
    x**2 * y**2,
    x**2 * y * z,
    x**2 * z**2,
    x * y**3,
    x * y**2 * z,
    x * y * z**2,
    x * z**3,
    y**4,
    y**3 * z,
    y**2 * z**2,
    y * z**3,
    z**4,
)
PIVOTS = tuple(f"C{i:02d}" for i in range(45))

B_CUSP = sp.Matrix((u**3, u * v**2, v**3))
B_NODE = sp.Matrix((u**2 * v, u * v**2, u**3 - v**3))


def coefficients4(poly: sp.Expr) -> tuple[sp.Expr, ...]:
    """Return degree-four coefficients in the frozen order."""
    P = sp.Poly(sp.expand(poly), *VARS)
    return tuple(P.coeff_monomial(mon) for mon in MONOMIALS4)


def route(components: tuple[sp.Expr, sp.Expr, sp.Expr]) -> str:
    """Route a concrete exact leading triple to its frozen pivot."""
    coeffs = tuple(c for h in components for c in coefficients4(h))
    for i, coefficient in enumerate(coeffs):
        if sp.simplify(coefficient) != 0:
            return PIVOTS[i]
    raise AssertionError("H4 is zero")


def random_invertible_matrix(rng: Random) -> sp.Matrix:
    while True:
        matrix = sp.Matrix(
            3, 3, [rng.randint(-3, 3) for _ in range(9)]
        )
        if matrix.det() != 0:
            return matrix


def instantiate(
    kind: str, incidence: str, rng: Random
) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    source = random_invertible_matrix(rng)
    p = sum(source[0, j] * VARS[j] for j in range(3))
    q = sum(source[1, j] * VARS[j] for j in range(3))
    if incidence == "transverse":
        ell = sum(source[2, j] * VARS[j] for j in range(3))
    elif incidence == "aligned":
        alpha = rng.choice(tuple(i for i in range(-3, 4) if i))
        beta = rng.randint(-3, 3)
        ell = alpha * p + beta * q
    else:
        raise ValueError(incidence)
    binary = B_CUSP if kind == "cusp" else B_NODE
    target = random_invertible_matrix(rng)
    triple = target * binary
    return tuple(
        sp.expand(ell * entry.subs({u: p, v: q}, simultaneous=True))
        for entry in triple
    )


def check_implicit_equations() -> None:
    cusp_relation = Y**3 - X * Z**2
    node_relation = X**3 - Y**3 - X * Y * Z
    assert sp.expand(
        cusp_relation.subs(dict(zip((X, Y, Z), B_CUSP)))
    ) == 0
    assert sp.expand(
        node_relation.subs(dict(zip((X, Y, Z), B_NODE)))
    ) == 0

    cusp_gradient = [
        sp.diff(cusp_relation, coordinate) for coordinate in (X, Y, Z)
    ]
    node_gradient = [
        sp.diff(node_relation, coordinate) for coordinate in (X, Y, Z)
    ]
    assert all(g.subs({X: 1, Y: 0, Z: 0}) == 0 for g in cusp_gradient)
    assert all(g.subs({X: 0, Y: 0, Z: 1}) == 0 for g in node_gradient)


def check_coefficient_formula() -> None:
    lx, ly, lz = sp.symbols("L_x L_y L_z")
    names = (
        "g300",
        "g210",
        "g201",
        "g120",
        "g111",
        "g102",
        "g030",
        "g021",
        "g012",
        "g003",
    )
    gs = sp.symbols(" ".join(names))
    cubic_monomials = (
        x**3,
        x**2 * y,
        x**2 * z,
        x * y**2,
        x * y * z,
        x * z**2,
        y**3,
        y**2 * z,
        y * z**2,
        z**3,
    )
    ell = lx * x + ly * y + lz * z
    cubic = sum(a * b for a, b in zip(gs, cubic_monomials))
    derived = coefficients4(ell * cubic)
    g300, g210, g201, g120, g111, g102, g030, g021, g012, g003 = gs
    stated = (
        lx * g300,
        ly * g300 + lx * g210,
        lz * g300 + lx * g201,
        ly * g210 + lx * g120,
        lz * g210 + ly * g201 + lx * g111,
        lz * g201 + lx * g102,
        ly * g120 + lx * g030,
        lz * g120 + ly * g111 + lx * g021,
        lz * g111 + ly * g102 + lx * g012,
        lz * g102 + lx * g003,
        ly * g030,
        lz * g030 + ly * g021,
        lz * g021 + ly * g012,
        lz * g012 + ly * g003,
        lz * g003,
    )
    assert all(sp.expand(a - b) == 0 for a, b in zip(derived, stated))


def check_routes() -> None:
    rng = Random(20260726)
    observed: set[str] = set()
    for kind, incidence in product(
        ("cusp", "node"), ("aligned", "transverse")
    ):
        for _ in range(20):
            components = instantiate(kind, incidence, rng)
            assert all(component != 0 for component in components)
            pivot = route(components)
            assert 0 <= int(pivot[1:]) <= 14
            observed.add(pivot)
    assert not any(f"C{i:02d}" in observed for i in range(15, 45))


def main() -> None:
    assert sp.gcd_list(list(B_CUSP)) == 1
    assert sp.gcd_list(list(B_NODE)) == 1
    assert sp.Matrix(B_CUSP).jacobian((u, v)).rank() == 2
    assert sp.Matrix(B_NODE).jacobian((u, v)).rank() == 2
    check_implicit_equations()
    check_coefficient_formula()
    check_routes()
    print("PASS: intrinsic cusp/node forms and exact C00--C44 routing")


if __name__ == "__main__":
    main()
