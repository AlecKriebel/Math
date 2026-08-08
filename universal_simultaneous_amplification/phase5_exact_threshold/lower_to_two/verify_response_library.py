#!/usr/bin/env python3
"""Independent exact checks for the machine-readable response library."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

import response_library as lib


def main() -> None:
    r = lib.r
    sigma, lam, tau, a, u = sp.symbols("sigma lambda tau a u", positive=True)

    pair = lib.clique_satellite(2, sigma)
    expected_pair = (
        2 * (sigma - 1) / (1 + sigma * (r**2 - 1)),
        2 * (r * (2 - r) - sigma) / (sigma + 2 * r * (r - 1)),
    )
    assert all(sp.factor(left - right) == 0 for left, right in zip(pair, expected_pair))

    hybrid = lib.pair_leaf_hybrid(sigma, lam)
    leaf = lib.ordinary_leaf()
    assert all(
        sp.factor(hybrid[i] - pair[i] - lam * leaf[i]) == 0 for i in range(2)
    )

    # Recover every K_s response from the invariant separated-gadget form.
    s = sp.symbols("s", integer=True, positive=True)
    forward_bd = r ** (s - 1) * (r - 1) / (r**s - 1)
    forward_db = (s - 1) * (r - 1) * r ** (s - 2) / (s * (r ** (s - 1) - 1))
    z_bd = sigma * (r**s - 1)
    z_db = s * r * (r ** (s - 1) - 1) / ((s - 1) * sigma)
    invariant = lib.separated_gadget_from_invariants(
        s, forward_bd, forward_db, z_bd * z_db, z_bd
    )
    clique = lib.clique_satellite(s, sigma)
    assert all(sp.factor(invariant[i] - clique[i]) == 0 for i in range(2))

    weighted = lib.common_hub_weighted_leaf(a)
    q = sp.symbols("q", positive=True)
    weighted_q = weighted[0].subs(r, 1 + q)
    assert sp.factor(sp.limit(weighted_q, a, sp.oo) - 1 / q) == 0
    # At a=0 the smaller killed-branching root is exactly 1/r^2: it solves
    # the quadratic and lies below one for r>1.
    root_zero = 1 / r**2
    assert sp.factor(r**2 * root_zero**2 - (r**2 + 1) * root_zero + 1) == 0
    assert sp.factor((1 - root_zero) / lib.p - 1 - 1 / r) == 0
    assert weighted[1] == -1

    heavy = lib.distinct_hub_heavy_leaf(tau)
    heavy_32 = tuple(sp.factor(value.subs(r, sp.Rational(3, 2))) for value in heavy)
    assert sp.factor(
        heavy_32[0]
        + 4
        * (tau - 1)
        * (2 * tau + 1)
        * (7 * tau**2 + 9 * tau + 3)
        / ((tau + 1) * (7 * tau + 5) * (4 * tau**2 + 9 * tau + 3))
    ) == 0
    assert sp.factor(heavy_32[1] + (7 * tau**2 + tau + 10) / (10 * (tau + 1) ** 2)) == 0

    doublet = lib.symmetric_pair_doublet(sigma, u)
    uncoupled = tuple(sp.factor(value.subs(u, 0)) for value in doublet)
    assert all(sp.factor(uncoupled[i] - 2 * pair[i]) == 0 for i in range(2))

    x1, x2 = sp.symbols("x1 x2", positive=True)
    clones = lib.portal_clones([x1, x2])
    assert clones[0] == 0
    assert sp.factor(
        clones[1]
        + (x1 - 1) ** 2 / (1 + (r - 1) * x1)
        + (x2 - 1) ** 2 / (1 + (r - 1) * x2)
    ) == 0

    A, X, Y = sp.symbols("A X Y", real=True)
    second = lib.clone_second_order([X, Y], [[0, A], [A, 0]])
    expected_second = -(X**2 + Y**2 + 2 * A * (X + Y) + 2 * r * A**2) / r
    assert second[0] == 0 and sp.factor(second[1] - expected_second) == 0

    target = Path(__file__).with_name("response_library.json")
    lib.write_registry(target)
    payload = json.loads(target.read_text())
    assert payload["schema"] == "phase5-exact-response-v1"
    assert set(payload["entries"]) == {
        "ordinary_leaf",
        "common_hub_weighted_leaf",
        "distinct_hub_heavy_leaf",
        "clique_satellite",
        "pair_leaf_hybrid",
        "separated_gadget_invariants",
        "integrated_gadget_summaries",
        "portal_clone_single",
        "clone_second_order_symmetric2",
        "symmetric_pair_doublet",
    }

    print("PASS: K2, K_s, weighted-leaf, clone, and doublet formulas recovered")
    print("PASS: separated invariant form specializes exactly to every K_s")
    print("PASS: deterministic machine-readable response_library.json regenerated")


if __name__ == "__main__":
    main()
