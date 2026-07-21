#!/usr/bin/env python3
"""Exact checks for the all-degree full-monodromy Keller family.

This verifies polynomial cancellation, determinant 1, inverse-equation
identities, and the rational two-point collision for any requested finite
range of n. The proof that the generic Galois group is S_n is mathematical;
the checker verifies its displayed discriminant parametrization and the
simple-branch base point.
"""

from __future__ import annotations

import argparse
import sympy as sp


x, y, z, T, U, V, t = sp.symbols("x y z T U V t")


def family(n: int):
    if n < 3:
        raise ValueError("n must be at least 3")

    u = 1 + x * y
    gamma = 1 - sp.Rational(n, n - 1) * x * y + x**2 * z
    alpha = (
        (n - 2) * u + u**2 - (n - 1) * u**n * gamma ** (n - 2)
    ) / (n - 2)
    beta = (
        (n - 2) + 2 * u - n * u ** (n - 1) * gamma ** (n - 2)
    ) / (n - 2)

    A = sp.cancel(alpha / x**2)
    B = sp.cancel(beta / x)
    C = sp.expand(x * gamma)
    return tuple(sp.expand(f) for f in (A, B, C)), u, gamma


def seed_p(n: int, value):
    return sp.Rational(1, n - 2) * (2 * value - n * value ** (n - 1))


def collision_point(n: int, root: int):
    target = sp.Rational(4 - 2**n, n - 2)
    gamma = sp.factor(target - seed_p(n, sp.Integer(root)))
    xx = 1 / gamma
    uu = sp.Rational(root, 1) / gamma
    vv = uu - 1
    yy = sp.factor(vv / xx)
    tau = gamma - 1 + sp.Rational(n, n - 1) * vv
    zz = sp.factor(tau / xx**2)
    return tuple(map(sp.factor, (xx, yy, zz))), target, gamma


def check(n: int):
    (A, B, C), u, gamma = family(n)

    # The apparent x denominators in the definition cancel.
    assert sp.denom(A) == 1
    assert sp.denom(B) == 1

    degrees = tuple(sp.Poly(f, x, y, z).total_degree() for f in (A, B, C))
    assert degrees == (5 * n - 8, 5 * n - 9, 4)

    jacobian = sp.factor(sp.Matrix([A, B, C]).jacobian((x, y, z)).det())
    assert jacobian == 1

    w = sp.expand(u * gamma)
    p_symbolic = seed_p(n, T)
    q_symbolic = (T**2 - (n - 1) * T**n) / (n - 2)
    assert sp.expand(sp.diff(q_symbolic, T) - T * sp.diff(p_symbolic, T)) == 0
    p = p_symbolic.subs(T, w)
    q = q_symbolic.subs(T, w)
    R = (w**2 - w**n) / (n - 2)
    assert sp.expand(q - (w * p - R)) == 0

    P = sp.expand(B * C)
    Q = sp.expand(A * C**2)
    assert sp.expand(P - (gamma + p)) == 0
    assert sp.expand(Q - (w * gamma + q)) == 0
    assert sp.expand(R - (w * P - Q)) == 0

    # The two uniform collision points map exactly to the same target.
    points = []
    for root in (1, 2):
        point, target, root_gamma = collision_point(n, root)
        assert root_gamma != 0
        image = tuple(
            sp.factor(f.subs(dict(zip((x, y, z), point)))) for f in (A, B, C)
        )
        assert image == (target, target, 1)
        points.append(point)
    assert points[0] != points[1]

    # Discriminant parametrization: H(t)=H'(t)=0.
    H = T**n - T**2 + U * T + V
    parametrization = {
        U: 2 * t - n * t ** (n - 1),
        V: (n - 1) * t**n - t**2,
        T: t,
    }
    assert sp.expand(H.subs(parametrization)) == 0
    assert sp.expand(sp.diff(H, T).subs(parametrization)) == 0
    assert sp.diff(parametrization[U], t).subs(t, 0) == 2

    # At (U,V)=(0,0), zero is exactly a double root and all others are simple.
    H0 = H.subs({U: 0, V: 0})
    assert sp.expand(H0 - T**2 * (T ** (n - 2) - 1)) == 0
    assert sp.gcd(sp.diff(T ** (n - 2) - 1, T), T ** (n - 2) - 1) == 1

    return {
        "n": n,
        "degrees": degrees,
        "target": target,
        "points": points,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=8)
    args = parser.parse_args()
    if args.max_n < 3:
        parser.error("--max-n must be at least 3")

    for n in range(3, args.max_n + 1):
        result = check(n)
        print(
            f"n={n}: det=1, degrees={result['degrees']}, "
            f"target=({result['target']},{result['target']},1)"
        )
        print(f"  preimages: {result['points'][0]} and {result['points'][1]}")
    print(f"All exact checks passed for 3 <= n <= {args.max_n}.")


if __name__ == "__main__":
    main()
