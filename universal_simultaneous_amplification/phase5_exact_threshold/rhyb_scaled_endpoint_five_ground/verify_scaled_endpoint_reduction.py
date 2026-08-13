#!/usr/bin/env python3
"""Exact symbolic replay for the scaled endpoint five-ground reduction."""

import sympy as sp


def main():
    r, X, s, Vw, a = sp.symbols("r X s Vw a", positive=True)
    h = 1 - s
    Vv = 1 / (r * h)
    h1 = 1 / (1 + r * X * Vw)

    # The dB fixed-point potential and first-orbit potential identities.
    assert sp.factor(1 - h - r * h * s * Vv) == 0
    assert sp.factor(1 - h1 - r * X * Vw * h1) == 0

    # Subtracting the two reciprocal equations gives the resolvent (7).
    RX = X * Vw
    Rs = s * Vv
    reciprocal_difference = h * h1 * (
        (1 + r * RX) - (1 + r * Rs)
    )
    assert sp.factor(reciprocal_difference - r * h * h1 * (RX - Rs)) == 0

    # Equations (12) and (13).
    target = sp.factor(a * r * h * h1 * (RX - Rs))
    assert sp.factor(target - a * (h - h1)) == 0
    split = a * (
        h / (h + X) * (X - s)
        + r * X * h * h1 / (h + X) * (Vw - Vv)
    )
    assert sp.factor(target - split) == 0

    # Three-ground linkage (18), checked for abstract positive grounds.
    f, g, k, Vf, Vg, Vk = sp.symbols(
        "f g k Vf Vg Vk", positive=True
    )
    d_fg = f * g * (Vg - Vf)
    d_gk = g * k * (Vk - Vg)
    d_fk = f * k * (Vk - Vf)
    assert sp.factor(d_fk - k / g * d_fg - f / g * d_gk) == 0
    assert sp.factor(k / f - (g / f) * (k / g)) == 0

    # The symmetrized two-node summand in the cut-Picone identity (15a).
    fi, fj, zi, zj, psi_i, psi_j = sp.symbols(
        "fi fj zi zj psi_i psi_j"
    )
    oriented_ij = fi * fj * (zj - zi) * psi_i
    oriented_ji = fi * fj * (zi - zj) * psi_j
    symmetrized = fi * fj * (zj - zi) * (psi_i - psi_j)
    assert sp.factor(oriented_ij + oriented_ji - symmetrized) == 0

    # Prefix summation by parts underlying the Farkas condition.  If the
    # total a1+...+a4 is zero, an increasing label makes this nonpositive
    # whenever all lower prefixes are nonnegative.
    a1, a2, a3, a4, u1, u2, u3, u4 = sp.symbols(
        "a1 a2 a3 a4 u1 u2 u3 u4"
    )
    weighted = a1 * u1 + a2 * u2 + a3 * u3 + a4 * u4
    prefixes = (
        a1 * (u1 - u2)
        + (a1 + a2) * (u2 - u3)
        + (a1 + a2 + a3) * (u3 - u4)
    )
    assert sp.factor(weighted.subs(a4, -a1 - a2 - a3) - prefixes) == 0

    # Exact single-order obstruction (26)--(28).
    common_potential = 1 / (r * (1 - s))
    obstruction_target = sp.factor(
        target.subs(Vw, common_potential)
    )
    asserted_target = a * (1 - s) * (X - s) / (1 - s + X)
    assert sp.factor(obstruction_target - asserted_target) == 0
    d_wv = sp.factor(a**2 * X * s * (Vv - Vw))
    assert sp.factor(d_wv.subs(Vw, common_potential)) == 0

    # The rational-in-r specialization (29) lies in the physical scalar
    # ranges for every 3/2 <= r <= 151/100 and has strictly negative target.
    c = r - 1
    X0 = c / 4
    s0 = c / 2
    specialized = sp.factor(
        asserted_target.subs({X: X0, s: s0, a: 1})
    )
    assert sp.factor(specialized + c * (3 - r) / (2 * (5 - r))) == 0
    assert sp.Rational(0) < X0.subs(r, sp.Rational(3, 2))
    assert s0.subs(r, sp.Rational(151, 100)) < 1
    assert specialized.subs(r, sp.Rational(3, 2)) < 0
    assert specialized.subs(r, sp.Rational(151, 100)) < 0

    print("PASS: corrected scaling X=(r-1)q")
    print("PASS: exact endpoint resolvent and local split")
    print("PASS: exact three-ground linkage")
    print("PASS: potential-only single (w,v)-order obstruction")


if __name__ == "__main__":
    main()
