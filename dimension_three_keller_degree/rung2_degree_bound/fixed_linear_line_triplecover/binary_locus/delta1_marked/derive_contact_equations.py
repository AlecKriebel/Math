#!/usr/bin/env python3
"""Coefficient equations K=lambda*alpha+mu*beta in the two marked S2 orbits."""

from __future__ import annotations

import sympy as sp

import explore_contact as E


lam, mu = sp.symbols("lam mu")


def equations(label: str, substitutions) -> None:
    alpha = sp.factor(E.alpha.subs(substitutions) / E.p)
    beta = sp.factor(E.beta.subs(substitutions) / E.p)
    curvature = sp.factor(E.K.subs(substitutions) / E.p)
    residual = sp.Poly(
        sp.expand(curvature - lam * alpha - mu * beta), E.p, E.q
    )
    print("\nORBIT", label)
    print("alpha/p =", alpha)
    print("beta/p =", beta)
    print("K/p =", curvature)
    for index in range(5):
        monomial = E.p ** (4 - index) * E.q**index
        print(monomial, ":", sp.factor(residual.coeff_monomial(monomial)))


equations("S=q^2", {E.s0: 0, E.s1: 0})
equations("S=p^2+q^2", {E.s0: 1, E.s1: 0})
