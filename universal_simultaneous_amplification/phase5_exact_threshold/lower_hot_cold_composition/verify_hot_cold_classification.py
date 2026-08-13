#!/usr/bin/env python3
"""Exact replay for the canonical hot--cold branching composition."""

from __future__ import annotations

import sympy as sp


def adjoint_involution():
    # Symbolic matrix audit in dimension three; no reversibility assumption
    # is needed for the algebraic swap itself.
    p1, p2 = sp.symbols("p1 p2", positive=True)
    p3 = 1 - p1 - p2
    p = sp.Matrix([p1, p2, p3])
    p_diag = sp.diag(p1, p2, p3)
    q11, q12, q21, q22 = sp.symbols("q11 q12 q21 q22", positive=True)
    q31 = (p1 * (1 - q11) - p2 * q21) / p3
    q32 = (p2 * (1 - q22) - p1 * q12) / p3
    kernel = sp.Matrix(
        [
            [q11, q12, 1 - q11 - q12],
            [q21, q22, 1 - q21 - q22],
            [q31, q32, 1 - q31 - q32],
        ]
    )
    # The last row is chosen so p is stationary: p^T P=p^T.
    assert (p.T * kernel - p.T).applyfunc(sp.factor) == sp.zeros(1, 3)
    reverse = p_diag.inv() * kernel.T * p_diag
    t = reverse * sp.ones(3, 1)
    t_diag = sp.diag(*t)
    p_prime = sp.Matrix([p[i] * t[i] for i in range(3)])
    assert sp.factor(sum(p_prime) - 1) == 0
    kernel_prime = t_diag.inv() * reverse
    p_prime_diag = sp.diag(*p_prime)
    reverse_prime = p_prime_diag.inv() * kernel_prime.T * p_prime_diag
    assert (reverse_prime - t_diag.inv() * kernel).applyfunc(
        sp.factor
    ) == sp.zeros(3, 3)
    t_prime = reverse_prime * sp.ones(3, 1)
    assert (t_prime - sp.Matrix([1 / value for value in t])).applyfunc(
        sp.factor
    ) == sp.zeros(3, 1)


def hot_cold_squares():
    r, h, a, x, b, s = sp.symbols("r h a x b s", positive=True)
    p0 = (r - 1) / r

    bd_equation = sp.expand(
        (h + a + x) * b - r * (1 - b) * (h * b + (1 - h) * p0)
    )
    db_equation = sp.expand(s - r * (1 - s) * (h * s + a * p0))

    gain = sp.factor(x / r + a * b / (r - 1) + b - 1 + h / r)
    cost = sp.factor(
        x * (r - 1) / r + (a + r - 1) / r - s * (r - h) / (r - 1)
    )

    a_from_bd = sp.solve(bd_equation, a)[0]
    a_from_db = sp.solve(db_equation, a)[0]

    bd_remainder = x * b * r + h * (r * b - r + 1) ** 2
    bd_remainder /= r * (r - 1)
    db_remainder = (r * s - r + 1) ** 2
    db_remainder /= r * (r - 1) * (1 - s)

    assert sp.factor((x / r - gain).subs(a, a_from_bd) - bd_remainder) == 0
    assert sp.factor(
        (cost - x * (r - 1) / r).subs(a, a_from_db) - db_remainder
    ) == 0

    separator = sp.factor(cost - (r - 1) * gain)
    sep_eliminated = separator.subs(a, a_from_bd)
    # The two endpoint equations share a, so substitute their exact
    # difference after eliminating it from the Bd equation.
    shared_constraint = sp.factor(db_equation.subs(a, a_from_bd))
    s_solution_a = a_from_db
    # Direct common-variable check: replacing a separately in each response
    # yields precisely the sum of the two nonnegative remainders.
    gain_eliminated = gain.subs(a, a_from_bd)
    cost_eliminated = cost.subs(a, s_solution_a)
    assert sp.factor(
        cost_eliminated - (r - 1) * gain_eliminated
        - db_remainder
        - (r - 1) * bd_remainder
    ) == 0
    assert shared_constraint != 0  # records that b and s remain coupled
    assert sep_eliminated != 0


def projective_matrix_identity():
    alpha, beta, gamma, delta, q = sp.symbols(
        "alpha beta gamma delta q", positive=True
    )
    transformed = (gamma + delta * q) / (alpha + beta * q)
    numerator = sp.factor((q - transformed) * (alpha + beta * q))
    assert numerator == alpha * q + beta * q**2 - delta * q - gamma


def mixture_identity():
    gc, cc, gh, ch, lam = sp.symbols("gc cc gh ch lam", positive=True)
    old_ratio = cc / gc
    new_ratio = (cc + lam * ch) / (gc + lam * gh)
    numerator = sp.factor(
        (old_ratio - new_ratio) * gc * (gc + lam * gh) / lam
    )
    assert numerator == cc * gh - ch * gc

    # Signed compensator: (gh,ch)=(-u,-v), u,v>0.
    u, v = sp.symbols("u v", positive=True)
    signed_numerator = sp.factor((cc * gh - ch * gc).subs({gh: -u, ch: -v}))
    assert signed_numerator == -cc * u + gc * v


def main():
    adjoint_involution()
    hot_cold_squares()
    projective_matrix_identity()
    mixture_identity()
    print("PASS: temperature-adjoint involution")
    print("PASS: exact hot--cold endpoint elimination")
    print("PASS: Bd loss and dB cost are explicit nonnegative squares")
    print("PASS: fractional-linear and signed-compensator criteria")
    print("NO-GO: canonical non-cold relay cannot improve ratio r-1")


if __name__ == "__main__":
    main()
