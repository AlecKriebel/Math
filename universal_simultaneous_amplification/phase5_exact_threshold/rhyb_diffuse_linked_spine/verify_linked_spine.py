#!/usr/bin/env python3
"""Exact replay of the general-r linked endpoint spine reduction."""

from __future__ import annotations

import sympy as sp


Q = sp.Rational
r, kappa = sp.symbols("r kappa", positive=True)


def weighted_pair(left, right, measure):
    return sp.factor(sum(measure[i] * left[i] * right[i] for i in range(2)))


def verify_local_transport():
    """Verify the scalar potential form of the spine transport identity."""

    X, s, a, Vw = sp.symbols("X s a Vw", positive=True)
    h = 1 - s
    Vv = 1 / (r * h)
    h1 = 1 / (1 + r * X * Vw)
    x = X / s

    # Kx=x Vw/Vv and K1=1.
    Ky = x * Vw / Vv - 1
    assert sp.factor(s * h1 * Ky - (h - h1)) == 0

    # The target weight A is p*s*h1/m when
    # m=p*a*s^2/(r*h).
    p = sp.symbols("p", positive=True)
    m = p * a * s**2 / (r * h)
    A = r * h * h1 / (a * s)
    assert sp.factor(m * A - p * s * h1) == 0


def verify_abstract_dirichlet_polarization():
    """Check (3) for an abstract reversible two-state Markov kernel."""

    m1, k12, k21 = sp.symbols("m1 k12 k21", positive=True)
    m2 = m1 * k12 / k21
    A1, A2, x1, x2 = sp.symbols("A1 A2 x1 x2")
    K = sp.Matrix([[1 - k12, k12], [k21, 1 - k21]])
    A = sp.Matrix([A1, A2])
    y = sp.Matrix([x1 - 1, x2 - 1])
    measure = sp.Matrix([m1, m2])

    gap = weighted_pair(A, K * y, measure)
    raw = weighted_pair(A, y, measure)
    cross = sp.factor(
        Q(1, 2)
        * sum(
            measure[i]
            * K[i, j]
            * (A[i] - A[j])
            * ((y[i]) - (y[j]))
            for i in range(2)
            for j in range(2)
        )
    )
    assert sp.factor(gap - raw + cross) == 0


def two_cycle_data():
    """Return an exact generic deterministic two-cycle endpoint system."""

    P = sp.Matrix([[0, 1], [1, 0]])
    pi = sp.Matrix([Q(1, 2), Q(1, 2)])
    a = sp.Matrix([2 / (1 + kappa), 2 * kappa / (1 + kappa)])
    p = sp.Matrix([1 / (1 + kappa), kappa / (1 + kappa)])
    Da = sp.diag(*a)
    R = sp.diag(*[1 / value for value in a]) * P * Da
    t = sp.diag(*[1 / value for value in a]) * (P * a)
    q = sp.Matrix(
        [
            (kappa * r + 1) / (r * (kappa + r)),
            (kappa + r) / (r * (kappa * r + 1)),
        ]
    )
    b = sp.ones(2, 1) - q
    survival = sp.Matrix([b[1], b[0]])
    return P, pi, a, p, R, t, q, b, survival


def verify_physical_spine():
    """Replay all spine identities on an exact endpoint family."""

    P, pi, a, p, R, t, q, b, survival = two_cycle_data()
    h = sp.ones(2, 1) - survival
    X = (r - 1) * q

    # Both endpoint equations.
    assert all(
        sp.factor(t[i] * b[i] - r * q[i] * (P * b)[i]) == 0
        for i in range(2)
    )
    assert all(
        sp.factor(survival[i] - r * h[i] * (R * survival)[i]) == 0
        for i in range(2)
    )

    v = sp.Matrix([a[i] * survival[i] for i in range(2)])
    w = sp.Matrix([a[i] * X[i] for i in range(2)])
    Vv = sp.Matrix([sp.factor((P * v)[i] / v[i]) for i in range(2)])
    Vw = sp.Matrix([sp.factor((P * w)[i] / w[i]) for i in range(2)])
    assert all(sp.factor(Vv[i] - 1 / (r * h[i])) == 0 for i in range(2))
    assert all(sp.factor(Vw[i] - (R * q)[i] / q[i]) == 0 for i in range(2))

    K = sp.zeros(2)
    for i in range(2):
        for j in range(2):
            K[i, j] = sp.factor(P[i, j] * v[j] / (Vv[i] * v[i]))
    assert all(sp.factor(sum(K[i, j] for j in range(2)) - 1) == 0 for i in range(2))

    measure = sp.Matrix(
        [sp.factor(pi[i] * Vv[i] * v[i] ** 2) for i in range(2)]
    )
    assert sp.factor(measure[0] * K[0, 1] - measure[1] * K[1, 0]) == 0

    x = sp.Matrix([sp.factor(w[i] / v[i]) for i in range(2)])
    y = x - sp.ones(2, 1)
    assert all(
        sp.factor((K * x)[i] - x[i] * Vw[i] / Vv[i]) == 0
        for i in range(2)
    )

    h1 = sp.Matrix([sp.factor(1 / (1 + r * (R * X)[i])) for i in range(2)])
    first = sp.ones(2, 1) - h1
    displacement = first - survival
    assert all(
        sp.factor(displacement[i] - survival[i] * h1[i] * (K * y)[i]) == 0
        for i in range(2)
    )

    A = sp.Matrix(
        [sp.factor(r * h[i] * h1[i] / (a[i] * survival[i])) for i in range(2)]
    )
    gap = weighted_pair(displacement, sp.ones(2, 1), p)
    spine = weighted_pair(A, K * y, measure)
    adjoint_spine = weighted_pair(K * A, y, measure)
    raw = weighted_pair(A, y, measure)
    cross = sp.factor(
        Q(1, 2)
        * sum(
            measure[i]
            * K[i, j]
            * (A[i] - A[j])
            * (x[i] - x[j])
            for i in range(2)
            for j in range(2)
        )
    )
    assert sp.factor(gap - spine) == 0
    assert sp.factor(gap - adjoint_spine) == 0
    assert sp.factor(gap - raw + cross) == 0


def verify_temperature_adjoint_obstruction():
    """Check the residual mismatch and exact negative orientation energy."""

    P, _pi, _a, p, R, t, q, b, survival = two_cycle_data()
    h = sp.ones(2, 1) - survival
    c = r - 1
    d = c * q - survival
    dstar = c * h - b
    assert all(
        sp.factor(d[i] - dstar[i] - (r - 2) * (q[i] - h[i])) == 0
        for i in range(2)
    )

    h1 = sp.Matrix([1 / (1 + r * (R * (c * q))[i]) for i in range(2)])
    q1 = sp.Matrix([t[i] / (t[i] + r * c * (P * h)[i]) for i in range(2)])
    assert all(
        sp.factor(h[i] - h1[i] - r * h[i] * h1[i] * (R * d)[i]) == 0
        for i in range(2)
    )
    assert all(
        sp.factor(
            q[i]
            - q1[i]
            - r * q[i] * q1[i] * (P * dstar)[i] / t[i]
        )
        == 0
        for i in range(2)
    )

    energy = weighted_pair(d, P * d, p)
    dual_energy = weighted_pair(dstar, P * dstar, p)
    assert sp.factor(energy - dual_energy) == 0

    specialized = sp.factor(energy.subs(kappa, Q(1, 4)))
    claimed = -(
        9
        * (r - 1) ** 2
        * (r**2 - r - 5)
        * (4 * r**2 - 4 * r - 5)
        / (r**2 * (r + 4) ** 2 * (4 * r + 1) ** 2)
    )
    assert sp.factor(specialized - claimed) == 0
    assert specialized.subs(r, Q(3, 2)) == -Q(34, 5929)

    # Both quadratic factors are negative throughout the isolating interval.
    right = Q(151, 100)
    assert (r**2 - r - 5).subs(r, right) < 0
    assert (4 * r**2 - 4 * r - 5).subs(r, right) < 0
    assert sp.diff(r**2 - r - 5, r).subs(r, Q(3, 2)) > 0
    assert sp.diff(4 * r**2 - 4 * r - 5, r).subs(r, Q(3, 2)) > 0

    sextic = r**6 - 8 * r**5 + 22 * r**4 - 30 * r**3 + 21 * r**2 - 6 * r + 1
    assert sp.polys.polytools.count_roots(sextic, Q(3, 2), right) == 1
    return specialized


def main():
    verify_local_transport()
    verify_abstract_dirichlet_polarization()
    verify_physical_spine()
    energy = verify_temperature_adjoint_obstruction()
    print("PASS: exact signed fixed-point-spine transport")
    print("PASS: reversible cross-Dirichlet representation")
    print("PASS: general-r temperature-adjoint residual mismatch")
    print(f"two-cycle orientation energy at r=3/2: {energy.subs(r, Q(3, 2))}")
    print("OPEN: universal scaled endpoint-versus-first sign")


if __name__ == "__main__":
    main()
