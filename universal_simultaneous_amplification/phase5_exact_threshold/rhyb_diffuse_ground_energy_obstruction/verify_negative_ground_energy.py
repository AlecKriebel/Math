#!/usr/bin/env python3
"""Exact replay for negative diffuse ground energy at R_hyb."""

import sympy as sp


def main():
    r, gamma, theta, eta = sp.symbols("r gamma theta eta", positive=True)
    c = r - 1
    A = 1 - gamma
    temperature = 1 + A * theta / gamma

    # Reconstruct the symmetric family and its exact adjoint orientation.
    A_eta = 1 - gamma - eta
    type_law = sp.Matrix([A_eta, eta, gamma])
    weights = sp.Matrix([
        [eta, (1 - theta) / eta, theta / gamma],
        [(1 - theta) / eta, 1, 1],
        [theta / gamma, 1, 1 / eta],
    ])
    degree = sp.Matrix([
        sp.factor(sum(type_law[j] * weights[i, j] for j in range(3)))
        for i in range(3)
    ])
    asserted_degree = sp.Matrix([
        1 + A_eta * eta,
        A_eta * (1 - theta) / eta + eta + gamma,
        A_eta * theta / gamma + eta + gamma / eta,
    ])
    assert all(sp.factor(degree[i] - asserted_degree[i]) == 0 for i in range(3))

    kernel = sp.Matrix(3, 3, lambda i, j: type_law[j] * weights[i, j] / degree[i])
    adjoint = sp.Matrix(3, 3, lambda i, j: type_law[j] * kernel[j, i] / type_law[i])
    tvec = sp.simplify(adjoint * sp.ones(3, 1))
    kernel_limit = kernel.applyfunc(lambda z: sp.limit(z, eta, 0, dir="+"))
    asserted_kernel_limit = sp.Matrix([
        [0, 1 - theta, theta],
        [1, 0, 0],
        [0, 0, 1],
    ])
    assert all(
        sp.factor(kernel_limit[i, j] - asserted_kernel_limit[i, j]) == 0
        for i in range(3) for j in range(3)
    )

    L = A + 1 / A + theta / gamma
    assert sp.factor(sp.limit(tvec[0] / eta, eta, 0, dir="+") - L) == 0
    assert sp.factor(sp.limit(eta * tvec[1], eta, 0, dir="+") - A * (1 - theta)) == 0
    assert sp.factor(sp.limit(tvec[2], eta, 0, dir="+") - temperature) == 0

    # Reconstruct every contribution in (21) and (24) from the singular
    # endpoint labels rather than assuming the displayed final formulas.
    qA_over_eta = L / (theta * (r - temperature))
    x_limit = sp.Matrix([1 / r, -c / r, (1 - temperature) / r])
    occupation_A = sp.factor(A * L / qA_over_eta * x_limit[0] ** 2)
    occupation_B = sp.factor(A * (1 - theta) * x_limit[1] ** 2)
    occupation_C = sp.factor(
        gamma * temperature * x_limit[2] ** 2 / (temperature / r)
    )

    occupation = (
        A * theta * (r - temperature) / r**2
        + A * (1 - theta) * c**2 / r**2
        + A**2 * theta**2 / (gamma * r)
    )
    assert sp.factor(occupation - occupation_A - occupation_B - occupation_C) == 0

    px_limit = sp.simplify(kernel_limit * x_limit)
    field_A = sp.factor(px_limit[0] - x_limit[0])
    field_C = sp.factor(px_limit[2] - r * x_limit[2])
    excursion_A = sp.factor(A * field_A**2)
    excursion_C = sp.factor(gamma / r * field_C**2)
    excursion = (
        A / r**2 * (1 + c * (1 - theta) + A * theta**2 / gamma) ** 2
        + c**2 * A**2 * theta**2 / (gamma * r**3)
    )
    assert sp.factor(excursion - excursion_A - excursion_C) == 0
    k_limit = sp.factor(4 * occupation / c - excursion)

    g0 = sp.Rational(1, 14)
    th0 = sp.Rational(1, 50)
    specialized = sp.factor(k_limit.subs({gamma: g0, theta: th0}))
    Q = (
        6002500 * r**3
        - 24158800 * r**2
        + 23808969 * r
        + 32500
    )
    asserted = -sp.Rational(13, 87500000) * Q / r**3
    assert sp.factor(specialized - asserted) == 0

    left = sp.Rational(3, 2)
    right = sp.Rational(151, 100)
    Qp = sp.diff(Q, r)
    Qpp = sp.diff(Qp, r)
    assert Qpp.subs(r, left) > 0
    assert Qp.subs(r, right) == -sp.Rational(32366825, 4)
    assert Qp.subs(r, right) < 0
    assert Q.subs(r, right) == sp.Rational(25054027, 16)
    assert Q.subs(r, right) > 0

    sextic = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    assert sextic.subs(r, left) == sp.Rational(1, 64)
    assert sextic.subs(r, right) == -sp.Rational(39866792399, 10**12)
    assert sp.polys.polytools.count_roots(sextic, left, right) == 1

    mean_b_limit = sp.factor(A + gamma * (1 - temperature / r))
    mean_s_limit = sp.factor(gamma * c / r)
    support = sp.factor(c * (1 - mean_b_limit) - mean_s_limit)
    assert sp.factor(support - A * theta * c / r) == 0
    specialized_support = sp.factor(support.subs({gamma: g0, theta: th0}))
    assert sp.factor(specialized_support - sp.Rational(13, 700) * c / r) == 0

    # The singular branch is admissible throughout the isolating interval.
    specialized_temperature = sp.factor(
        temperature.subs({gamma: g0, theta: th0})
    )
    assert specialized_temperature == sp.Rational(63, 50)
    assert specialized_temperature < left

    print("PASS: exact three-type ground-energy limit (25)")
    print("PASS: exact negative factorization (28)")
    print("PASS: Q(r)>0 on [3/2,151/100]")
    print("PASS: unique hybrid sextic root in the isolating interval")
    print("PASS: positive full support deficit (36)")


if __name__ == "__main__":
    main()
