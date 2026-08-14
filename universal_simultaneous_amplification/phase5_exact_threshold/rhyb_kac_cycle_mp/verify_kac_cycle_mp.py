#!/usr/bin/env python3
"""Exact replay of the singleton Kac-cycle MP reduction.

The script verifies identities and scoped path-space obstructions only.  It
does not claim the open full-cycle inequality and performs no graph search.
"""

from __future__ import annotations

import sympy as sp


def stationary(generator: sp.Matrix) -> sp.Matrix:
    """Return the exact stationary row of an irreducible generator."""

    system = generator.T.copy()
    rhs = sp.zeros(generator.rows, 1)
    for column in range(generator.cols):
        system[-1, column] = 1
    rhs[-1] = 1
    solution = list(sp.linsolve((system, rhs)).args[0])
    row = sp.Matrix(1, len(solution), solution)
    assert row * generator == sp.zeros(1, generator.cols)
    assert sp.factor(sum(solution) - 1) == 0
    return row


def kac_green_audit() -> None:
    """Check root-by-root Kac time and signed reward identities exactly."""

    generator = sp.Matrix(
        [
            [-3, 1, 2, 0],
            [2, -5, 1, 2],
            [1, 2, -4, 1],
            [3, 0, 1, -4],
        ]
    )
    reward = sp.Matrix(
        [sp.Rational(-2, 5), sp.Rational(1, 7), sp.Rational(3, 4), -1]
    )
    invariant = stationary(generator)
    stationary_reward = sp.factor((invariant * reward)[0])

    for root in range(generator.rows):
        rest = [index for index in range(generator.rows) if index != root]
        q = -generator[root, root]
        green = (-generator.extract(rest, rest)).inv()
        entrance = generator.extract([root], rest)
        time = sp.factor((1 + (entrance * green * sp.ones(len(rest), 1))[0]) / q)
        cycle_reward = sp.factor(
            (reward[root] + (entrance * green * reward.extract(rest, [0]))[0]) / q
        )
        psi = sp.factor(q * cycle_reward)
        assert sp.factor(invariant[root] - 1 / (q * time)) == 0
        assert sp.factor(stationary_reward - cycle_reward / time) == 0
        assert sp.factor(stationary_reward - invariant[root] * psi) == 0


def portal_and_pair_audit() -> None:
    """Replay cancellation to KMP and its pair polynomial."""

    beta_b, beta_d, r = sp.symbols("beta_B beta_D r", positive=True)
    pbi, pbj, pdi, pdj = sp.symbols(
        "psi_Bi psi_Bj psi_Di psi_Dj", positive=True
    )
    ei, ej, xi, xj = sp.symbols("e_i e_j x_i x_j", positive=True)

    ui, uj = beta_b / pbi, beta_b / pbj
    vi, vj = beta_d / pdi, beta_d / pdj
    raw_gap = (
        (xi * ui + xj * uj) * (xi * ei * vi + xj * ej * vj)
        - r**3 * beta_b * beta_d * (xi + xj) * (ei * xi + ej * xj)
    )
    kac_gap = (
        (xi / pbi + xj / pbj) * (ei * xi / pdi + ej * xj / pdj)
        - r**3 * (xi + xj) * (ei * xi + ej * xj)
    )
    assert sp.factor(raw_gap - beta_b * beta_d * kac_gap) == 0

    diagonal_i = ei * (1 / (pbi * pdi) - r**3)
    diagonal_j = ej * (1 / (pbj * pdj) - r**3)
    cross = ej / (pbi * pdj) + ei / (pbj * pdi) - r**3 * (ei + ej)
    pair = diagonal_i * xi**2 + cross * xi * xj + diagonal_j * xj**2
    assert sp.factor(pair - kac_gap) == 0

    # Orientation split of the two swapped root assignments.
    ai = 1 / pbi
    aj = 1 / pbj
    ci = ei / pdi
    cj = ej / pdj
    square = (sp.sqrt(ai * cj) - sp.sqrt(aj * ci)) ** 2
    assert sp.simplify(ai * cj + aj * ci - 2 * sp.sqrt(ai * cj * aj * ci) - square) == 0


def two_root_trace_audit() -> None:
    """Check the literal two-root trace scaling into Kac variables."""

    a, b, c, d, r = sp.symbols("a b c d r", positive=True)
    phi_bi, phi_bj, phi_di, phi_dj = sp.symbols(
        "phi_Bi phi_Bj phi_Di phi_Dj", real=True
    )
    ei, ej = sp.symbols("e_i e_j", positive=True)
    yb = b * phi_bi + a * phi_bj
    yd = d * phi_di + c * phi_dj
    psi_bi, psi_bj = yb / b, yb / a
    psi_di, psi_dj = yd / d, yd / c
    qhat = r**3 * yb * yd

    di = sp.factor(ei * (1 / (psi_bi * psi_di) - r**3) * yb * yd)
    dj = sp.factor(ej * (1 / (psi_bj * psi_dj) - r**3) * yb * yd)
    cross = sp.factor(
        (
            ej / (psi_bi * psi_dj)
            + ei / (psi_bj * psi_di)
            - r**3 * (ei + ej)
        )
        * yb
        * yd
    )
    assert sp.factor(di - ei * (b * d - qhat)) == 0
    assert sp.factor(dj - ej * (a * c - qhat)) == 0
    assert sp.factor(cross - (ej * b * c + ei * a * d - qhat * (ei + ej))) == 0


def macro_support_audit() -> None:
    """Verify the exact positive dB two-neighbor union mass."""

    r, z = sp.symbols("r z", positive=True)
    geometric_hit = lambda value: value / (r - (r - 1) * value)
    union_both = sp.factor(1 - geometric_hit(z) - geometric_hit(1 - z))
    claimed = (
        (r**2 - 1)
        * z
        * (1 - z)
        / ((r - (r - 1) * z) * (1 + (r - 1) * z))
    )
    assert sp.factor(union_both - claimed) == 0
    exact_value = sp.factor(union_both.subs({r: sp.Rational(3, 2), z: sp.Rational(1, 18)}))
    assert exact_value > 0

    # Directly audit the two Bd support zeros on the 1--17 weighted path.
    # Vertices are u=0,v=1,w=2; P is the forward row kernel, while a Bd
    # dual arrow with source x and target y has rate P[x,y].
    transition = (
        (0, 1, 0),
        (sp.Rational(1, 18), 0, sp.Rational(17, 18)),
        (0, 1, 0),
    )

    def bd_rate(state: int, destination: int, fitness: sp.Expr) -> sp.Expr:
        answer = sp.Integer(0)
        for target in range(3):
            if not ((state >> target) & 1):
                continue
            for source in range(3):
                arrow = transition[source][target]
                if not arrow:
                    continue
                neutral = (state & ~(1 << target)) | (1 << source)
                selective = state | (1 << source)
                if neutral == destination:
                    answer += arrow
                if selective == destination:
                    answer += (fitness - 1) * arrow
        return sp.factor(answer)

    root_v = 1 << 1
    leaf_pair = (1 << 0) | (1 << 2)
    fitness = sp.Rational(3, 2)
    assert bd_rate(root_v, leaf_pair, fitness) == 0
    assert bd_rate(leaf_pair, root_v, fitness) == 0
    assert exact_value == sp.Rational(85, 1961)

    # At R_hyb, 3/2<r<2: singleton reward is negative and doubleton
    # reward is positive on an order-three module.
    g_singleton = sp.factor(sp.Rational(1, 3) - (r - 1) / r)
    g_doubleton = sp.factor(sp.Rational(2, 3) - (r - 1) / r)
    assert sp.factor(g_singleton - (3 - 2 * r) / (3 * r)) == 0
    assert sp.factor(g_doubleton - (3 - r) / (3 * r)) == 0
    assert g_singleton.subs(r, sp.Rational(151, 100)) < 0
    assert g_doubleton.subs(r, sp.Rational(151, 100)) > 0


def micro_history_audit() -> None:
    """Check non-coboundary likelihoods on the 1--17 weighted path."""

    a = sp.Integer(1)
    b = sp.Integer(17)
    t_v = sp.Integer(2)
    c_v = (a + b) / t_v
    p_c_u, p_c_w = a / (a + b), b / (a + b)
    p_l_u = p_l_w = sp.Rational(1, 2)
    ratio_u = sp.factor(p_l_u / p_c_u)
    ratio_w = sp.factor(p_l_w / p_c_w)
    assert (ratio_u, ratio_w, c_v) == (9, sp.Rational(9, 17), 9)

    # Same projected macroedge and return suffix, different hidden lengths.
    assert ratio_u**1 == 9
    assert ratio_u**2 == 81
    assert ratio_u != ratio_u**2

    # Removing the endpoint degree ratio leaves the repeated-source factor
    # from equation (39).
    for sample_count in (1, 2, 3):
        raw = sp.factor((c_v / a) ** sample_count)
        endpoint = sp.factor((a + b) / a)
        residual = sp.factor(
            sp.Rational(1, t_v) * c_v ** (sample_count - 1) * a ** (1 - sample_count)
        )
        assert sp.factor(raw / endpoint - residual) == 0


def main() -> None:
    kac_green_audit()
    portal_and_pair_audit()
    two_root_trace_audit()
    macro_support_audit()
    micro_history_audit()
    print("PASS: exact root-by-root Kac/Green identities")
    print("PASS: exact cancellation to KMP and pair coefficients")
    print("PASS: exact literal two-root Schur scaling")
    print("PASS: positive singular dB macro-cycle mass")
    print("PASS: non-coboundary expanded-history likelihood ratios")
    print("OPEN: signed assignment-valued full-cycle inequality")


if __name__ == "__main__":
    main()
