#!/usr/bin/env python3
"""Exact scope, topology, scale, and likelihood-Hessian algebra checks."""
from __future__ import annotations

import sympy as s


def main() -> None:
    q, x, y, mu, c = s.symbols("q x y mu c", positive=True)
    lam = mu * q / (1 - q)
    t1 = -(1 - q) * s.log(x) / mu
    t2 = t1 - (1 - q) * s.log(y) / mu

    assert s.simplify(lam / (lam + mu) - q) == 0
    assert s.simplify(s.exp(-(lam + mu) * t1) - x) == 0
    assert s.simplify(s.exp(-(lam + mu) * (t2 - t1)) - y) == 0
    print("PASS fixed-mu cube transformation and inverse identities")

    # Unknown-rate scale invariance.
    assert s.simplify((lam / c) / ((lam / c) + (mu / c)) - q) == 0
    assert s.simplify(s.exp(-((lam + mu) / c) * (c * t1)) - x) == 0
    assert s.simplify(s.exp(-((lam + mu) / c) * c * (t2 - t1)) - y) == 0
    print("PASS unknown-mu common time-rate scale invariance")

    p0, p12, p13, pD = s.symbols("p0 p12 p13 pD")
    A = (4 * (p0 + p12) - 1) / 3
    B = (4 * (p0 + p13) - 1) / 3
    assert s.simplify(A - B - s.Rational(4, 3) * (p12 - p13)) == 0

    r = q + (1 - q) * y**2
    D = (1 - r) * x ** (2 + q / 2)
    assert s.simplify(D - (1 - q) * (1 - y**2) * x ** (2 + q / 2)) == 0
    print("PASS strict matching-pair factorization and site-pattern translation")

    # Exact source diagnostic conversion back to original parameters at mu=4/3.
    mu0 = s.Rational(4, 3)
    point = {q: s.Rational(1, 2), x: s.Rational(81, 100), y: s.Rational(1, 10), mu: mu0}
    assert s.simplify(lam.subs(point) - s.Rational(4, 3)) == 0
    assert s.simplify(t1.subs(point) - s.Rational(3, 8) * s.log(s.Rational(100, 81))) == 0
    assert s.simplify(t2.subs(point) - (s.Rational(3, 8) * s.log(s.Rational(100, 81)) + s.Rational(3, 8) * s.log(10))) == 0
    print("PASS exact source-diagnostic conversion to original parameters")

    # Population multinomial likelihood Hessian at an exact fit.  The last
    # pattern derivative and Hessian are fixed by sum_i p_i(theta)=1.
    m, d = 5, 3
    probs = s.symbols("p0:5", positive=True)
    Jfree = s.Matrix(m - 1, d, lambda i, j: s.symbols(f"j{i}{j}"))
    last_row = -s.ones(1, m - 1) * Jfree
    J = Jfree.col_join(last_row)
    Hfree = [s.Matrix(d, d, lambda a, b: s.symbols(f"h{i}{a}{b}"))
             for i in range(m - 1)]
    Hlast = -sum(Hfree, s.zeros(d, d))
    Hs = Hfree + [Hlast]
    assert sum(Hs, s.zeros(d, d)) == s.zeros(d, d)
    assert s.ones(1, m) * J == s.zeros(1, d)
    Hess = sum(Hs, s.zeros(d, d)) - J.T * s.diag(*[1 / p for p in probs]) * J
    expected = -J.T * s.diag(*[1 / p for p in probs]) * J
    assert s.simplify(Hess - expected) == s.zeros(d, d)
    print("PASS exact population-likelihood Hessian cancellation and Gram form")

    print("ALL SCOPE, TOPOLOGY, AND STATISTICAL IDENTITIES PASSED")


if __name__ == "__main__":
    main()
