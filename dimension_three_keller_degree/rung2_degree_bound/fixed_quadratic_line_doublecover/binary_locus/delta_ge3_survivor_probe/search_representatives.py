#!/usr/bin/env python3
"""Search small exact representatives of the frozen delta=3 and delta=4 rows.

This is deliberately only a survivor/construction probe.  It does not
attempt to classify the incidence locus.
"""

from __future__ import annotations

from itertools import product

import sympy as sp

p, q = sp.symbols("p q")


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q) - sp.diff(f, q) * sp.diff(g, p))


def primitive(poly):
    return sp.Poly(poly, p, q).primitive()[1].as_expr()


def gcd3(a, b, c):
    return sp.factor(sp.gcd(sp.gcd(sp.Poly(a, p, q), sp.Poly(b, p, q)), sp.Poly(c, p, q)).as_expr())


def degree(poly):
    return sp.Poly(poly, p, q).total_degree()


def independent(a, b):
    pa, pb = sp.Poly(a, p, q), sp.Poly(b, p, q)
    va = sp.Matrix([pa.coeff_monomial(p ** (5 - i) * q**i) for i in range(6)])
    vb = sp.Matrix([pb.coeff_monomial(p ** (5 - i) * q**i) for i in range(6)])
    return sp.Matrix.hstack(va, vb).rank() == 2


def main():
    values = (-2, -1, 0, 1, 2)
    found = {3: [], 4: []}
    seen = set()
    fixed_divisors = (
        p**2,
        p * q,
        p * (p + q),
        p**2 + q**2,
        p**2 + p * q + q**2,
        p**2 + 2 * p * q + q**2,
        p**2 + 3 * p * q + q**2,
    )
    for h in fixed_divisors:
        hkey = str(sp.factor(h))
        P, Q = sp.expand(h * p**2), sp.expand(h * q**2)
        Pp, Pq = sp.diff(P, p), sp.diff(P, q)
        Qp, Qq = sp.diff(Q, p), sp.diff(Q, q)
        gamma = sp.Poly(sp.expand(Pp * Qq - Pq * Qp), p, q)
        for a, b, c, d in product(values, repeat=4):
            if (a, b, c, d) == (0, 0, 0, 0):
                continue
            R = a * p**3 + b * p**2 * q + c * p * q**2 + d * q**3
            Rp, Rq = sp.diff(R, p), sp.diff(R, q)
            alpha = sp.Poly(sp.expand(Qp * Rq - Qq * Rp), p, q)
            beta = sp.Poly(sp.expand(-(Pp * Rq - Pq * Rp)), p, q)
            if not independent(alpha.as_expr(), beta.as_expr()):
                continue
            gpoly = sp.gcd(sp.gcd(alpha, beta), gamma)
            g = sp.factor(gpoly.as_expr())
            delta = degree(g)
            if delta not in found:
                continue
            key = (hkey, str(sp.factor(primitive(R))), delta)
            if key in seen:
                continue
            seen.add(key)
            found[delta].append(
                (
                    h,
                    R,
                    g,
                    sp.factor(alpha.as_expr() / g),
                    sp.factor(beta.as_expr() / g),
                    sp.factor(gamma.as_expr() / g),
                )
            )
    for delta in (3, 4):
        print(f"DELTA {delta}: {len(found[delta])} samples")
        for index, data in enumerate(found[delta][:12], 1):
            h, R, g, a0, b0, c0 = data
            print(f"[{index}] h={sp.factor(h)}; R={sp.factor(R)}; g={g}")
            print(f"    reduced=({a0}, {b0}, {c0})")


if __name__ == "__main__":
    main()
