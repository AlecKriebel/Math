#!/usr/bin/env python3
"""Independent exact replay for the star--reservoir diode and obstruction."""

from __future__ import annotations

import sympy as sp


def solve_star(order: int, q: sp.Expr, rule: str) -> tuple[sp.Expr, sp.Expr]:
    """Solve all changing-event equations on (hub, mutant-leaf count)."""
    L = order
    states = [(h, k) for h in (0, 1) for k in range(L + 1)]
    empty, full = (0, 0), (1, L)
    transient = [state for state in states if state not in (empty, full)]
    index = {state: row for row, state in enumerate(transient)}
    matrix = sp.zeros(len(transient))
    rhs = sp.zeros(len(transient), 1)
    for state, row in index.items():
        h, k = state
        moves: list[tuple[tuple[int, int], sp.Expr]] = []
        if rule == "Bd":
            if h == 0 and k:
                moves.extend([((1, k), q * k), ((0, k - 1), sp.Rational(k, L))])
            if h == 1 and k < L:
                moves.extend([((1, k + 1), q * sp.Rational(L - k, L)), ((0, k), L - k)])
        elif rule == "dB":
            if h == 0 and k:
                moves.extend([((1, k), q * k / (q * k + L - k)), ((0, k - 1), k)])
            if h == 1 and k < L:
                moves.extend([((0, k), (L - k) / (q * k + L - k)), ((1, k + 1), L - k)])
        else:
            raise ValueError(rule)
        total = sum(rate for _, rate in moves)
        matrix[row, row] = total
        for target, rate in moves:
            if target == full:
                rhs[row] += rate
            elif target != empty:
                matrix[row, index[target]] -= rate
    value = matrix.inv() * rhs
    return sp.factor(value[index[(1, 0)]]), sp.factor(value[index[(0, 1)]])


def main() -> None:
    r = sp.symbols("r", positive=True)
    L, C = sp.symbols("L C", integer=True, positive=True)

    theta = (L + r) / (r * (r * L + 1))
    denom = r / L + (1 - theta**L) / (1 - theta)
    hb = r / (L * denom)
    eb = r**2 * theta / denom
    hd = (r * L + 1) / ((r + 1) * (L + 1))
    ed = r * (r * L + 1) / ((r + 1) * L * (L + 2 * r - 1))

    # Independent exact orbit solves at several symbolic integer orders.
    for order in range(1, 8):
        h_b, e_b = solve_star(order, r, "Bd")
        h_d, e_d = solve_star(order, r, "dB")
        assert sp.factor(h_b - hb.subs(L, order)) == 0
        assert sp.factor(e_b - eb.subs(L, order)) == 0
        assert sp.factor(h_d - hd.subs(L, order)) == 0
        assert sp.factor(e_d - ed.subs(L, order)) == 0

    hb_reverse = hb.subs(r, 1 / r)
    hd_reverse = hd.subs(r, 1 / r)
    # theta_(1/r)=1/theta_r and
    # D_(1/r)=theta_r^(-L) D_r/r^2.  Keeping this intermediate
    # identity explicit avoids relying on heuristic power simplification.
    reverse_denom = 1 / (r * L) + (1 - theta ** (-L)) / (1 - theta ** (-1))
    assert sp.factor(reverse_denom - theta ** (-L) * denom / r**2) == 0
    ratio_b = r * L * theta ** (1 - L)
    expanded_ratio_b = L * (L + r) * (r * (L * r + 1)) ** L / ((L + r) ** L * (L * r + 1))
    ratio_d = r * (L + 1) * (L * r + 1) / (L * (L + r) * (L + 2 * r - 1))
    assert sp.factor(ed / hd_reverse - ratio_d) == 0
    for order in range(1, 8):
        assert sp.factor((eb / hb_reverse - ratio_b).subs(L, order)) == 0
        assert sp.factor((ratio_b - expanded_ratio_b).subs(L, order)) == 0

    kbp = (1 - 1 / r) / (1 - r ** (-C))
    kbm = (r - 1) / (r**C - 1)
    kdp = (C - 1) / C * (1 - 1 / r) / (1 - r ** (-(C - 1)))
    kdm = (C - 1) / C * (r - 1) / (r ** (C - 1) - 1)
    assert sp.factor(kbp / kbm - r ** (C - 1)) == 0
    assert sp.factor(kdp / kdm - r ** (C - 2)) == 0

    odds_b = sp.factor(r**2 / L * ratio_b * kbp / kbm)
    odds_d = sp.factor(r**4 * L * ratio_d * kdp / kdm)
    expected_b = r ** (C + 1) * (L + r) / (L * r + 1) * (r * (L * r + 1) / (L + r)) ** L
    expected_d = r ** (C + 3) * (L + 1) * (L * r + 1) / ((L + r) * (L + 2 * r - 1))
    for order in range(1, 8):
        assert sp.factor((odds_b - expected_b).subs(L, order)) == 0
    assert sp.factor(odds_d - expected_d) == 0

    total_star = sp.factor(hd + L * ed)
    expected_total = (L * r + 1) * (L * r + L + 3 * r - 1) / ((L + 1) * (r + 1) * (L + 2 * r - 1))
    assert sp.factor(total_star - expected_total) == 0
    p = (r - 1) / r
    excess = sp.factor(total_star - p * (L + 2))
    excess_one = sp.factor(excess.subs(L, 1))
    assert sp.factor(excess_one + (2 * r - 3) / r) == 0
    difference = sp.factor(excess - excess_one)
    expected_difference = -(
        (L - 1)
        * (r - 1)
        * (L**2 * r + L**2 + L * r**2 + L * r + r - 1)
        / (r * (L + 1) * (r + 1) * (L + 2 * r - 1))
    )
    assert sp.factor(difference - expected_difference) == 0
    assert sp.factor(excess_one + p / 2 + (3 * r - 5) / (2 * r)) == 0

    # A finite exact instance already has the predicted strict comparison.
    rr = sp.Rational(19, 10)
    cc, ll, mm = 20, 3, 2
    pp = (rr - 1) / rr
    clique_mass = (cc - 1) * pp / (1 - rr ** (-(cc - 1)))
    star_mass = expected_total.subs({r: rr, L: ll})
    upper = sp.factor((clique_mass + star_mass) / (cc + ll + 1))
    n = mm * (cc + ll + 1)
    baseline = sp.factor((n - 1) * pp / (n * (1 - rr ** (-(n - 1)))))
    assert upper < baseline

    print("PASS: exact star orbit formulas for L=1,...,7")
    print("PASS: exact Bd/dB star--reservoir diode odds")
    print("PASS: exact separated entrance obstruction for r>5/3")


if __name__ == "__main__":
    main()
