#!/usr/bin/env python3
"""Exact replay for the endpoint-support autocorrelation reduction."""

import sympy as sp


def centered_algebra() -> None:
    r, x, y = sp.symbols("r x y", nonzero=True)
    c = r - 1
    p0 = c / r

    # The two scalar rational identities used after endpoint averaging.
    b = p0 + x
    q = 1 / r - x
    assert sp.factor(b * x / q - (c * x + r * x**2 / q)) == 0

    s = p0 + y
    h = 1 / r - y
    assert sp.factor(s * y / h - (c * y + r * y**2 / h)) == 0

    # If c Ex+rJ=0 and c Eu+rU=0, the support is r(J+U/c).
    J, U = sp.symbols("J U")
    Ex = -r * J / c
    Eu = -r * U / c
    T = -c * Ex - Eu
    assert sp.factor(T - r * (J + U / c)) == 0


def deterministic_two_cycle() -> None:
    r, kappa = sp.symbols("r kappa", positive=True)
    c = r - 1
    p1, p2 = 1 / (1 + kappa), kappa / (1 + kappa)

    q1 = (kappa * r + 1) / (r * (kappa + r))
    q2 = (kappa + r) / (r * (kappa * r + 1))
    s1 = kappa * (r**2 - 1) / (r * (kappa * r + 1))
    s2 = (r**2 - 1) / (r * (kappa + r))
    x1, x2 = 1 / r - q1, 1 / r - q2
    u1, u2 = s1 - c / r, s2 - c / r
    h1, h2 = 1 - s1, 1 - s2

    # P is the deterministic swap, so E_p(xPx)=x1*x2.
    J = sp.factor(x1 * x2)
    U = sp.factor(p1 * u1**2 / h1 + p2 * u2**2 / h2)
    T = sp.factor(r * (J + U / c))

    assert sp.factor(U + r * J) == 0
    assert sp.factor(
        T
        - (kappa - 1) ** 2 * c
        / (r * (kappa + r) * (kappa * r + 1))
    ) == 0


def singular_family() -> None:
    r, gamma, theta = sp.symbols("r gamma theta", positive=True)
    c = r - 1
    A = 1 - gamma
    temp = 1 + A * theta / gamma

    U = A * c**2 / r**2
    J = -A * c * (1 - theta) / r**2
    N = A / (2 * r**2) * (
        1 + (1 - theta) * c**2
        + A * theta**2 * (1 + temp) / gamma
    )

    assert sp.factor(r * (J + U / c) - A * theta * c / r) == 0
    assert sp.factor(U / (-J) - c / (1 - theta)) == 0

    special = sp.factor(
        (U - c * N).subs({gamma: sp.Rational(1, 14),
                           theta: sp.Rational(1, 50)})
    )
    sign_polynomial = (
        2 * c - 1 - sp.Rational(49, 50) * c**2
        - sp.Rational(1469, 125000)
    )
    positive_prefactor = (
        sp.Rational(13, 14) * c / (2 * r**2)
    )
    assert sp.factor(special - positive_prefactor * sign_polynomial) == 0

    # On 1/2 <= c <= 51/100:
    # 2c-1 <= 1/50 and 49c^2/50 >= 49/200, already proving negativity.
    assert sp.Rational(1, 50) - sp.Rational(49, 200) < 0


def main() -> None:
    centered_algebra()
    deterministic_two_cycle()
    singular_family()
    print("PASS exact endpoint-support autocorrelation reduction")


if __name__ == "__main__":
    main()
