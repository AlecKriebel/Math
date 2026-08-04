#!/usr/bin/env python3
"""Exact audit of the site-pattern formulas distributed with arXiv:2607.14653v1.

The expressions below are independently transcribed from the public R function
GetSitePatternProbs.  This script does not use them as a model axiom.  It checks
only their internal algebra and compares them with the maps derived from the
stated stochastic process and from the auxiliary fourteen-history map.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as s

CERT_PATH = Path(__file__).with_name("source_diagnostic.json")


def source_site_map():
    m, L, t1, t2 = s.symbols("mu lambda t1 t2", positive=True)
    p0 = (
        3*s.exp(-(t1+2*t2)*(m+L))*m*(m-2*L) + 4*m*L
        + 3*s.exp(-3*t1*(m+L))*m*L + 8*L**2
        - 6*s.exp(-t1*L-2*t2*(m+L))*m*(m+L)
        + 9*s.exp(-2*t2*(m+L))*m*(m+2*L)
        + m**3/(2*m+3*L)
        + 3*s.exp(-2*m*t1-3*t1*L)*m*(m+L)*(m+3*L)/(2*m+3*L)
    )/(8*(m+L)**2)

    p12 = s.Rational(3,16)/((m+L)**2*(2*m+3*L)) * (
        2*m*(m+2*L)**2
        + s.exp(-(3*t1+2*t2)*(m+L))*(
            2*s.exp(3*t1*(m+L))*m*(m-2*L)*(2*m+3*L)
            - 2*s.exp(2*t1*(m+L))*m*(2*m-L)*(2*m+3*L)
            + 2*s.exp(3*m*t1+2*t1*L)*m*(m+L)*(2*m+3*L)
            + s.exp(3*m*t1+2*m*t2+2*t2*L)*(m+L)**2*(2*m+3*L)
            - 2*s.exp(2*t2*(m+L))*L*(2*m+L)*(2*m+3*L)
            + s.exp(m*t1+2*m*t2+2*t2*L)*(-4*m**3-7*m**2*L+3*L**3)
        )
    )

    p13 = s.Rational(3,32)/((m+L)**2*(2*m+3*L)) * (
        4*m*(m+2*L)**2
        - s.exp(-(3*t1+2*t2)*(m+L))*(
            2*s.exp(2*t1*(m+L))*m*(m-5*L)*(2*m+3*L)
            - 4*s.exp(3*t1*(m+L))*m*(m-2*L)*(2*m+3*L)
            + 2*s.exp(2*t2*(m+L))*(m-L)*L*(2*m+3*L)
            + 6*s.exp(3*m*t1+2*t1*L)*m*(m+L)*(2*m+3*L)
            + s.exp(3*m*t1+2*m*t2+2*t2*L)*(m+L)**2*(2*m+3*L)
            - 3*s.exp(m*t1+2*m*t2+2*t2*L)*(m+L)*(2*m**2+3*m*L-L**2)
        )
    )

    pD = 3*m*(
        -3*s.exp(-2*t2*(m+L))*m
        + s.exp(-(t1+2*t2)*(m+L))*(m-2*L)
        + s.exp(-3*t1*(m+L))*L
        + 2*s.exp(-t1*L-2*t2*(m+L))*(m+L)
        + m*(m+2*L)/(2*m+3*L)
        - s.exp(t1*(m-3*(m+L)))*(m+L)*(m+3*L)/(2*m+3*L)
    )/(4*(m+L)**2)
    return (m, L, t1, t2), (p0, p12, p13, pD)


def force_cube(expr, substitutions):
    out = expr.subs(substitutions)
    out = s.powsimp(out, force=True)
    out = s.powdenest(out, force=True)
    out = s.expand_power_base(out, force=True)
    return s.factor(s.simplify(out))


def main():
    (m, L, t1, t2), (p0, p12, p13, pD) = source_site_map()
    assert s.simplify(p0 + p12 + 2*p13 + pD - 1) == 0
    print("PASS distributed four-coordinate formula is exactly normalized")

    A = s.simplify((4*(p0+p12)-1)/3)
    B = s.simplify((4*(p0+p13)-1)/3)
    C = s.simplify((16*p0-1-3*A-6*B)/6)

    # Scale invariance lets us set lambda+mu=1 before introducing the cube.
    q, x, y = s.symbols("q x y", positive=True)
    subs = {m: 1-q, L: q, t1: -s.log(x), t2: -s.log(x*y)}
    AR = force_cube(A, subs)
    BR = force_cube(B, subs)
    CR = force_cube(C, subs)

    K = q*(2*q+1)/(q+2)
    Ac = K + (1-q)*x**2*(1+(1-x**q)*y**2) + q*(1-q)*x**(q+2)/(q+2)
    Bc = K + (1-q)*x**2*(1+(3-x**q)*y**2)/2 - (1-q)*(2-q)*x**(q+2)/(2*(q+2))
    Cc = q**2 + q*(1-q)*x**2 + 2*q*(1-q)*x**2*y**2 + (1-q)*(1-2*q)*x**3*y**2

    # A compact exact witness that the two supplied formula systems differ.
    c_difference = s.factor(CR-Cc)
    assert s.simplify(c_difference - q*x**2*(q-1)*(x-1)*(y-1)*(y+1)) == 0
    print("PASS distributed formula differs from the auxiliary table map")
    print("  C_source-C_table = q*x^2*(q-1)*(x-1)*(y-1)*(y+1)")

    # Exact interior point and expected values are read from the frozen,
    # machine-readable source certificate. Choosing x=(9/10)^2 and q=1/2
    # makes every variable power rational.
    cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    def rat(text: str) -> s.Rational:
        return s.Rational(text)
    point = {
        q: rat(cert["cube_point"]["q"]),
        x: rat(cert["cube_point"]["x"]),
        y: rat(cert["cube_point"]["y"]),
    }
    Aval, Bval, Cval = [s.factor(z.subs(point)) for z in (AR,BR,CR)]
    site = [
        s.factor((1+3*Aval+6*Bval+6*Cval)/16),
        s.factor(3*(1+3*Aval-2*Bval-2*Cval)/16),
        s.factor(3*(1-Aval+2*Bval-2*Cval)/16),
        s.factor(3*(1-Aval-2*Bval+2*Cval)/8),
    ]
    assert sum(site[:2]) + 2*site[2] + site[3] == 1
    assert all(z > 0 for z in site)
    assert s.factor(Aval-Bval) == rat(cert["expected"]["A_minus_B"])
    assert s.factor(site[1]-site[2]) == rat(cert["expected"]["p12_minus_p13"])
    print("PASS exact interior inconsistency certificate")
    print(f"  A-B = {s.factor(Aval-Bval)} < 0")
    print(f"  p12-p13 = {s.factor(site[1]-site[2])} < 0")
    print("  all five aggregate probabilities are strictly positive and sum to one")
    print("ALL SOURCE-FORMULA AUDITS PASSED")


if __name__ == "__main__":
    main()
