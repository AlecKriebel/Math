#!/usr/bin/env python3
"""Exact symbolic replay of the orientation-preserving portal minimax."""

from __future__ import annotations

from hashlib import sha256

import sympy as sp


def generic_portal_algebra():
    U1, U2, V1, V2, e1, e2, Q, x1, x2 = sp.symbols(
        "U1 U2 V1 V2 e1 e2 Q x1 x2", positive=True
    )
    W1, W2 = e1 * V1, e2 * V2

    gap = (x1 * U1 + x2 * U2) * (x1 * W1 + x2 * W2) - Q * (
        x1 + x2
    ) * (x1 * e1 + x2 * e2)
    d1 = e1 * (U1 * V1 - Q)
    d2 = e2 * (U2 * V2 - Q)
    cross = U1 * W2 + U2 * W1 - Q * (e1 + e2)
    assert sp.expand(gap - (d1 * x1**2 + cross * x1 * x2 + d2 * x2**2)) == 0

    # The global arithmetic--geometric balance is exact.  The square on
    # the right vanishes only at one global lambda^2=B/A.
    A, B, lam = sp.symbols("A B lam", positive=True)
    assert sp.expand((lam * A + B / lam) ** 2 - 4 * A * B) == sp.expand(
        (lam * A - B / lam) ** 2
    )

    # Parameterize square roots to replay the root-orientation identity
    # without asking the CAS to choose branches of symbolic radicals.
    a, b, c, d = sp.symbols("a b c d", positive=True)
    assert sp.expand(a**2 * d**2 + b**2 * c**2 - 2 * a * b * c * d) == sp.expand(
        (a * d - b * c) ** 2
    )

    return {
        "gap": sp.expand(gap),
        "d1": d1,
        "d2": d2,
        "cross": cross,
    }


def reciprocal_probability_transform():
    theta1, theta2, c1, c2, e1, e2 = sp.symbols(
        "theta1 theta2 c1 c2 e1 e2", positive=True
    )
    C = theta1 * c1 + theta2 * c2
    E = theta1 * e1 + theta2 * e2
    eta1 = theta1 * c1 / C
    eta2 = theta2 * c2 / C

    # Work on the probability simplex theta1+theta2=1.
    simplex = {theta2: 1 - theta1}
    assert sp.factor((eta1 + eta2 - 1).subs(simplex)) == 0
    reciprocal_product = (eta1 / c1 + eta2 / c2) * (
        eta1 * e1 / c1 + eta2 * e2 / c2
    )
    assert sp.factor((reciprocal_product - E / C**2).subs(simplex)) == 0

    # Scalar AM--GM minimization used in Sion's minimax step.
    aa, bb, t = sp.symbols("aa bb t", positive=True)
    root_a, root_b, root_t = sp.symbols("root_a root_b root_t", positive=True)
    substituted = (t * aa + bb / t - 2 * sp.sqrt(aa * bb)).subs(
        {aa: root_a**2, bb: root_b**2, t: root_t**2}
    )
    assert sp.factor(substituted - (root_t * root_a - root_b / root_t) ** 2) == 0

    return sp.factor(reciprocal_product.subs(simplex))


def normalization_audit():
    cB, cD, LB1, LB2, LD1, LD2, e1, e2, Q0, x1, x2 = sp.symbols(
        "cB cD LB1 LB2 LD1 LD2 e1 e2 Q0 x1 x2", positive=True
    )
    raw_U = [cB * LB1, cB * LB2]
    raw_V = [cD * LD1, cD * LD2]
    raw_Q = cB * cD * Q0
    raw_gap = (
        (x1 * raw_U[0] + x2 * raw_U[1])
        * (x1 * e1 * raw_V[0] + x2 * e2 * raw_V[1])
        - raw_Q * (x1 + x2) * (x1 * e1 + x2 * e2)
    )
    normalized_gap = (
        (x1 * LB1 + x2 * LB2)
        * (x1 * e1 * LD1 + x2 * e2 * LD2)
        - Q0 * (x1 + x2) * (x1 * e1 + x2 * e2)
    )
    assert sp.factor(raw_gap - cB * cD * normalized_gap) == 0

    # The PTR portal denominators cancel to the same abstract homogeneous
    # gap; tau variables need no additional stationary normalizer.
    tauB1, tauB2, tauD1, tauD2, QT = sp.symbols(
        "tauB1 tauB2 tauD1 tauD2 QT", positive=True
    )
    gamma_den = x1 + x2
    alpha_den = x1 * e1 + x2 * e2
    tree_left = (x1 * tauB1 + x2 * tauB2) / gamma_den * (
        x1 * e1 * tauD1 + x2 * e2 * tauD2
    ) / alpha_den
    cleared_tree = sp.factor(
        (tree_left - QT) * gamma_den * alpha_den
    )
    expected_tree = (
        (x1 * tauB1 + x2 * tauB2)
        * (x1 * e1 * tauD1 + x2 * e2 * tauD2)
        - QT * gamma_den * alpha_den
    )
    assert sp.factor(cleared_tree - expected_tree) == 0
    return sp.expand(normalized_gap), sp.expand(expected_tree)


def one_root_operator_norm_audit():
    """Check every factor in Q_*=N^-2 on a one-root exact datum."""

    U = sp.Integer(3)
    V = sp.Integer(5)
    e = sp.Integer(7)
    W = e * V

    # The inner t minimum is 2sqrt(e); the outer lambda supremum occurs
    # when lambda U + lambda^-1 W is minimal, namely 2sqrt(UW).
    norm_value = sp.factor(2 * sp.sqrt(e) / (2 * sp.sqrt(U * W)))
    sharp_portal_constant = sp.factor(norm_value ** -2)
    assert norm_value == 1 / sp.sqrt(15)
    assert sharp_portal_constant == U * V == 15
    return norm_value, sharp_portal_constant


def two_root_operator_norm_audit():
    """Check the nontrivial fixed-c minimax factor on exact rational data."""

    theta, t = sp.symbols("theta t", positive=True)
    # c=(1,10), e=(1,100), with theta the mass on the first root.
    direct_ratio = (10 - 9 * theta) ** 2 / (100 - 99 * theta)
    theta_star = sp.Rational(10, 11)
    direct_minimum = sp.factor(direct_ratio.subs(theta, theta_star))
    assert sp.factor(sp.diff(direct_ratio, theta).subs(theta, theta_star)) == 0
    assert direct_minimum == sp.Rational(40, 121)

    first_gauge = t + 1 / t
    second_gauge = (t + 100 / t) / 10
    t_star = sp.sqrt(10)
    assert sp.factor(first_gauge.subs(t, t_star) - second_gauge.subs(t, t_star)) == 0
    gauge_value = sp.factor(first_gauge.subs(t, t_star))
    assert gauge_value == 11 * sp.sqrt(10) / 10
    assert sp.factor(4 / gauge_value**2) == direct_minimum
    return direct_minimum, gauge_value


def exact_strictness_audits():
    """Separate exact AP from the two previously used strengthenings."""

    # Audit A: exact AP passes while root-Hellinger fails.  The large
    # swapped-root orientation term is indispensable.
    e = [sp.Integer(100), sp.Integer(1)]
    U = [sp.Integer(100), sp.Integer(1)]
    V = [sp.Rational(1, 50), sp.Integer(2)]
    Q = sp.Integer(1)
    W = [e[i] * V[i] for i in range(2)]
    h = [U[i] * V[i] for i in range(2)]
    diagonal = [e[i] * (h[i] - Q) for i in range(2)]
    cross = U[0] * W[1] + U[1] * W[0] - Q * sum(e)
    exact_pair_margin = cross + 2 * sp.sqrt(diagonal[0] * diagonal[1])
    rhr_left = sp.sqrt(h[0] * h[1]) + sp.sqrt((h[0] - Q) * (h[1] - Q))
    rhr_right = Q * (sp.sqrt(sp.Rational(e[0], e[1])) + sp.sqrt(sp.Rational(e[1], e[0]))) / 2
    assert all(value >= 0 for value in diagonal)
    assert exact_pair_margin == 121 > 0
    assert rhr_left == 3
    assert rhr_right == sp.Rational(101, 20)
    assert rhr_left < rhr_right

    # Audit B: exact AP passes even though the entrywise cross coefficient
    # is negative; the diagonal copositive repayment closes it.
    e_b = [sp.Integer(100), sp.Integer(1)]
    U_b = [sp.Integer(10), sp.Integer(1)]
    V_b = [sp.Rational(2, 5), sp.Integer(4)]
    W_b = [e_b[i] * V_b[i] for i in range(2)]
    diagonal_b = [e_b[i] * (U_b[i] * V_b[i] - Q) for i in range(2)]
    cross_b = U_b[0] * W_b[1] + U_b[1] * W_b[0] - Q * sum(e_b)
    margin_b = cross_b + 2 * sp.sqrt(diagonal_b[0] * diagonal_b[1])
    assert diagonal_b == [300, 3]
    assert cross_b == -21
    assert margin_b == 39 > 0

    # Q=0 and diagonal equality are ordinary closed-boundary cases.
    q_zero_margin = U_b[0] * W_b[1] + U_b[1] * W_b[0] + 2 * sp.sqrt(
        e_b[0] * U_b[0] * V_b[0] * e_b[1] * U_b[1] * V_b[1]
    )
    assert q_zero_margin > 0
    equality_diagonal = sp.factor(sp.Integer(7) * (Q - Q))
    assert equality_diagonal == 0

    return {
        "orientation_margin": exact_pair_margin,
        "rhr_gap": rhr_left - rhr_right,
        "entrywise_cross": cross_b,
        "copositive_margin": margin_b,
    }


def main():
    generic = generic_portal_algebra()
    reciprocal = reciprocal_probability_transform()
    normalized_gap, tree_gap = normalization_audit()
    norm_value, one_root_constant = one_root_operator_norm_audit()
    two_root_minimum, two_root_gauge = two_root_operator_norm_audit()
    audits = exact_strictness_audits()

    serialization = "\n".join(
        [
            *(str(sp.factor(generic[key])) for key in sorted(generic)),
            str(reciprocal),
            str(normalized_gap),
            str(tree_gap),
            str(norm_value),
            str(one_root_constant),
            str(two_root_minimum),
            str(two_root_gauge),
            *(f"{key}:{audits[key]}" for key in sorted(audits)),
        ]
    )
    certificate_hash = sha256(serialization.encode()).hexdigest()
    expected_hash = "b474f939934d1d8e9cd3e069cc1ab2961b71263372b33ac881fdca46b023e6cf"
    assert certificate_hash == expected_hash

    print("PASS exact orientation-preserving portal minimax algebra")
    print("PASS raw/SRR/PTR normalization audit")
    print(f"one-root norm audit: N={norm_value}, Q_*={one_root_constant}")
    print(
        "two-root fixed-c audit: "
        f"m={two_root_minimum}, gauge={two_root_gauge}"
    )
    print(f"strictness audits: {audits}")
    print(f"certificate sha256: {certificate_hash}")
    print("OPEN: universal MP/PTR pair sign")


if __name__ == "__main__":
    main()
