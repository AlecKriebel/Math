#!/usr/bin/env python3
"""Exact response vectors for the phase-5 dilute-module program.

Every public constructor returns a pair ``(Bd, dB)`` of SymPy expressions.
The normalization is the coefficient of the dilute module density after the
same number of complete-core vertices has been removed.  In particular, all
far-field and uniform-singleton terms are already included.
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


r = sp.symbols("r", positive=True)
p = (r - 1) / r


def ordinary_leaf() -> tuple[sp.Expr, sp.Expr]:
    return 1 / (r - 1), sp.Integer(-1)


def common_hub_weighted_leaf(mark_scale: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """Common-hub leaf response for finite killed-branching mark scale a."""
    a = sp.sympify(mark_scale)
    middle = r**2 + 1 + r * (r - 1) * a
    # Rationalized smaller root of r^2 z^2-middle*z+1=0.
    root = 2 / (middle + sp.sqrt(middle**2 - 4 * r**2))
    ell = 1 - root
    return sp.factor(ell / p - 1), sp.Integer(-1)


def distinct_hub_heavy_leaf(tau: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """One weight-tau*C leaf on its own hub, including far-field response."""
    t = sp.sympify(tau)
    bd = -(
        (2 * t + 1) * (r * t**3 - 2 * r * t - r + 2 * t**3 + t**2)
    ) / (
        (t + 1)
        * (r * t + r + 2 * t + 1)
        * (r**2 * t + r**2 - r + t**2)
    )
    db = -(
        r**2 * t**2 + r**2 * t + r * t**2 + r - 2 * t**2 - 2 * t + 1
    ) / ((r + 1) * (t + 1) * (2 * r * t - 2 * t + 1))
    return sp.factor(bd), sp.factor(db)


def clique_satellite(order: int | sp.Expr, sigma: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    """Separated internally regular K_s satellite."""
    s = sp.sympify(order)
    q = sp.sympify(sigma)
    bd = s * (q - 1) / (1 + q * (r**s - 1))
    db = s * (s * r - r**s - (s - 1) * q) / (
        (s - 1) * q + s * r * (r ** (s - 1) - 1)
    )
    return sp.factor(bd), sp.factor(db)


def pair_leaf_hybrid(sigma: sp.Expr, leaf_density: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    bd, db = clique_satellite(2, sigma)
    leaf_bd, leaf_db = ordinary_leaf()
    lam = sp.sympify(leaf_density)
    return sp.factor(bd + lam * leaf_bd), sp.factor(db + lam * leaf_db)


def separated_gadget_from_invariants(
    order: int | sp.Expr,
    forward_bd: sp.Expr,
    forward_db: sp.Expr,
    gate_product: sp.Expr,
    bd_gate: sp.Expr,
) -> tuple[sp.Expr, sp.Expr]:
    """Complete separated fixed-gadget normal form.

    ``forward_*`` are isolated-gadget uniform-singleton fixation averages at
    fitness r (not divided by p), ``gate_product`` is Z_B Z_D, and
    ``bd_gate`` is Z_B.  The reciprocal gate is Z_D=gate_product/bd_gate.
    """
    s = sp.sympify(order)
    ab = sp.sympify(forward_bd)
    ad = sp.sympify(forward_db)
    k = sp.sympify(gate_product)
    z = sp.sympify(bd_gate)
    bd = s * (ab * z / (p * (1 + z)) - 1)
    db = s * (ad * k / (p * (k + z)) - 1)
    return sp.factor(bd), sp.factor(db)


def integrated_gadget_from_summaries(
    order: int | sp.Expr,
    singleton_sum_bd: sp.Expr,
    singleton_sum_db: sp.Expr,
    portal_dot_bd: sp.Expr,
    portal_over_degree_dot_db: sp.Expr,
    portal_over_degree_sum: sp.Expr,
    portal_sum: sp.Expr,
) -> tuple[sp.Expr, sp.Expr]:
    """Full integrated-gadget response (local plus Poisson far field)."""
    s = sp.sympify(order)
    ub = sp.sympify(singleton_sum_bd)
    ud = sp.sympify(singleton_sum_db)
    xub = sp.sympify(portal_dot_bd)
    xodud = sp.sympify(portal_over_degree_dot_db)
    xod = sp.sympify(portal_over_degree_sum)
    total = sp.sympify(portal_sum)
    source_bd = r * xub - (r - 1) * xod
    source_db = r * xodud - (r - 1) * (total + r - 1)
    bd = ub / p - s + source_bd / (r - 1) ** 2
    db = ud / p - s + 1 + source_db / (r - 1) ** 2
    return sp.factor(bd), sp.factor(db)


def portal_clones(portals: list[sp.Expr]) -> tuple[sp.Expr, sp.Expr]:
    xs = [sp.sympify(value) for value in portals]
    return sp.Integer(0), sp.factor(
        -sum((value - 1) ** 2 / (1 + (r - 1) * value) for value in xs)
    )


def symmetric_pair_doublet(sigma: sp.Expr, coupling: sp.Expr) -> tuple[sp.Expr, sp.Expr]:
    q = sp.sympify(sigma)
    u = sp.sympify(coupling)

    def H(z: sp.Expr, theta: sp.Expr) -> sp.Expr:
        return z * (z + 1 + r**2 * theta) / (
            (z + 1) ** 2 + theta * (1 + (1 + r**2) * z)
        )

    h_bd = H(q * (r**2 - 1), q * u)
    h_db = H(2 * r * (r - 1) / q, u)
    bd = 4 * (r * h_bd / ((r + 1) * p) - 1)
    db = 4 * (h_db / (2 * p) - 1)
    return sp.factor(bd), sp.factor(db)


def leaf_eliminated_separator(response: tuple[sp.Expr, sp.Expr]) -> sp.Expr:
    bd, db = response
    return sp.factor(db + (r - 1) * bd)


def clone_second_order(
    portal_tangent: list[sp.Expr], internal_tangent: list[list[sp.Expr]]
) -> tuple[sp.Expr, sp.Expr]:
    """Coefficient of epsilon^2 at the portal-clone equality manifold."""
    xi = [sp.sympify(value) for value in portal_tangent]
    matrix = [[sp.sympify(value) for value in row] for row in internal_tangent]
    n = len(xi)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("internal tangent has the wrong shape")
    alpha = [sum(matrix[i][j] for j in range(n)) for i in range(n)]
    edges = sum(matrix[i][j] ** 2 for i in range(n) for j in range(i + 1, n))
    quadratic = sum((xi[i] + alpha[i]) ** 2 for i in range(n)) + 2 * (r - 1) * edges
    return sp.Integer(0), sp.factor(-quadratic / r)


def clone_bd_cubic(
    portal_tangent: list[sp.Expr], internal_tangent: list[list[sp.Expr]]
) -> sp.Expr:
    """Coefficient of epsilon^3 in Bd at portal-clone equality."""
    xi = [sp.sympify(value) for value in portal_tangent]
    matrix = [[sp.sympify(value) for value in row] for row in internal_tangent]
    n = len(xi)
    if len(matrix) != n or any(len(row) != n for row in matrix):
        raise ValueError("internal tangent has the wrong shape")
    alpha = [sum(matrix[i][j] for j in range(n)) for i in range(n)]
    c = [xi[i] + alpha[i] for i in range(n)]
    cubic = sum(
        matrix[i][j] ** 2 * (c[i] + c[j])
        + 2 * matrix[i][j] * c[i] * c[j]
        for i in range(n)
        for j in range(i + 1, n)
    )
    return sp.factor(-cubic / r**2)


def registry() -> dict[str, object]:
    sigma, lam, tau, a = sp.symbols("sigma lambda tau a", positive=True)
    s = sp.symbols("s", integer=True, positive=True)
    ab, ad, k, z = sp.symbols("A_B A_D K z", positive=True)
    u = sp.symbols("u", nonnegative=True)
    ub, ud, xub, xodud, xod, total = sp.symbols(
        "U_B U_D XU_B XODU_D XOD P", finite=True
    )
    x = sp.symbols("x", positive=True)
    A, X, Y = sp.symbols("A X Y", real=True)
    entries = {
        "ordinary_leaf": ordinary_leaf(),
        "common_hub_weighted_leaf": common_hub_weighted_leaf(a),
        "distinct_hub_heavy_leaf": distinct_hub_heavy_leaf(tau),
        "clique_satellite": clique_satellite(s, sigma),
        "pair_leaf_hybrid": pair_leaf_hybrid(sigma, lam),
        "separated_gadget_invariants": separated_gadget_from_invariants(s, ab, ad, k, z),
        "integrated_gadget_summaries": integrated_gadget_from_summaries(
            s, ub, ud, xub, xodud, xod, total
        ),
        "portal_clone_single": portal_clones([x]),
        "clone_second_order_symmetric2": clone_second_order(
            [X, Y], [[0, A], [A, 0]]
        ),
        "symmetric_pair_doublet": symmetric_pair_doublet(sigma, u),
    }
    return {
        "schema": "phase5-exact-response-v1",
        "fitness_symbol": "r",
        "normalization": "coefficient per dilute module relative to removed complete-core vertices",
        "entries": {
            name: {"Bd": sp.sstr(value[0]), "dB": sp.sstr(value[1])}
            for name, value in entries.items()
        },
        "derived": {
            name: {"leaf_eliminated_separator": sp.sstr(leaf_eliminated_separator(value))}
            for name, value in entries.items()
        },
        "higher_order": {
            "clone_bd_cubic_symmetric2": sp.sstr(
                clone_bd_cubic([X, Y], [[0, A], [A, 0]])
            )
        },
    }


def write_registry(path: Path) -> None:
    path.write_text(json.dumps(registry(), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    write_registry(Path(__file__).with_name("response_library.json"))
