#!/usr/bin/env python3
"""Symbolic checks for the global-univalence proof identities."""
from __future__ import annotations

import sympy as s


def main():
    q, x, r = s.symbols("q x r", positive=True)
    X = x ** (2 - q)
    Z = x ** 3
    D = (1 - r) * x ** (2 + q / 2)
    M = q * (1 - X) / (2 - q) + (1 + 2 * r) * X / 3
    C = (q**2 * ((q - 2) * Z + 3 * X - (q + 1)) / ((q - 2) * (q + 1))
         + r * Z + q * (1 + 2 * r) * (X - Z) / (1 + q))
    minor = s.Matrix([[s.diff(D, x), s.diff(D, r)],
                      [s.diff(M, x), s.diff(M, r)]]).det()
    assert s.simplify(minor - x ** (3 - q / 2) * (2 - q * (1 + r))) == 0
    print("PASS positive (x,r) minor identity")

    # Determinant factor in p=2-q, X=x^p variables.
    p, XX, rr, h, S = s.symbols("p X r h S", positive=True)
    ZZ = XX ** (s.Rational(3, 1) / p)
    DD = (1 - rr) * XX ** ((6 - p) / (2 * p))
    MM = (2 - p) * (1 - XX) / p + (1 + 2 * rr) * XX / 3
    CC = ((2 - p)**2 * ((-p) * ZZ + 3 * XX - (3 - p)) / ((-p) * (3 - p))
          + rr * ZZ + (1 + 2 * rr) * (2 - p) * (XX - ZZ) / (3 - p))
    det = s.simplify(s.Matrix([DD, MM, CC]).jacobian([p, XX, rr]).det())

    alpha = -2 * p * (h * p - 3) * (h * p - 2 * h - 2)
    beta = -p * (p - 3) * (p - 2) * (h * p - 2 * h - 2)
    gamma = (p - 3) * (h * p - 6)
    eta = (3 - p) * (p - 1) * (p * h**2 - 3 * p * h + 6)
    delta = -alpha - beta - gamma
    H = (beta * s.exp(3 * S / p) + gamma * s.exp(S)
         + alpha * s.exp((3 / p - 1) * S) + delta + eta * S)
    Q = s.exp(-(1 + 3 / p) * S) * H
    pref = (p - 1)**2 * XX ** (3 / p - s.Rational(3, 2)) / (p**3 * (3 - p)**2)
    rhs = pref * Q
    # Substitute the model relations r=1-(p-1)h and S=-log X.
    diff = s.simplify(det.subs(rr, 1 - (p - 1) * h) - rhs.subs(S, -s.log(XX)))
    assert diff == 0
    print("PASS full Jacobian determinant factorization")

    H0 = s.simplify(H.subs(S, 0))
    H1 = s.factor(s.diff(H, S).subs(S, 0))
    assert H0 == 0
    assert s.simplify(H1 - p * h**2 * (3 - p)**2) == 0

    a0 = (3 - p) / p
    J = s.simplify(s.exp(-a0 * S) * s.diff(H, S, 2))
    J0 = s.factor(J.subs(S, 0))
    J1 = s.factor(s.diff(J, S).subs(S, 0))
    assert s.simplify(J0 + 2 * h * (p - 3)**2 * (h * p - 2 * h - 1)) == 0
    assert s.simplify(J1 + (p - 3)**2 * (7 * h * p - 12 * h - 6) / p) == 0
    print("PASS convexity identities H(0), H'(0), J(0), J'(0)")

    # Fixed-(D,M) path derivative of h in p,tau variables.
    tau = s.symbols("tau", positive=True)
    Xtau = s.exp(-p * tau)
    rtau = 1 - (p - 1) * h
    Dtau = (p - 1) * h * s.exp(-(3 - p / 2) * tau)
    Mtau = (2 - p) * (1 - Xtau) / p + (1 + 2 * rtau) * Xtau / 3
    A = s.Matrix([Dtau, Mtau]).jacobian([tau, h])
    rhsvec = -s.Matrix([s.diff(Dtau, p), s.diff(Mtau, p)])
    hp = s.factor((A.inv() * rhsvec)[1])
    N = (h * p**2 * (2 * (p - 1) * tau + p - 2)
         - 6 * p * (p - 1) * tau + (p - 6) * s.exp(p * tau)
         - 2 * p**2 - p + 6)
    claimed = -h * N / (p**2 * (p - 1) * (h * (p - 2) - 2))
    assert s.simplify(hp - claimed) == 0
    print("PASS fixed-(D,M) derivative identity for h")
    print("ALL GLOBAL-UNIVALENCE IDENTITIES PASSED")


if __name__ == "__main__":
    main()
