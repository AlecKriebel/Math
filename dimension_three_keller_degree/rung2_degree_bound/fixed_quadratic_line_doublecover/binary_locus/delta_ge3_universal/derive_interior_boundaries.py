#!/usr/bin/env python3
"""Derive exact-open boundary factors for the squarefree interior charts."""

from __future__ import annotations

import sympy as sp

p, q, s = sp.symbols("p q s")
A, B = sp.symbols("A B")
L = p - s * q
M = s * p - q
h = sp.expand(L * M)
P, Q = sp.expand(h * p**2), sp.expand(h * q**2)


def jac(f, g):
    return sp.expand(sp.diff(f, p) * sp.diff(g, q)
                     - sp.diff(f, q) * sp.diff(g, p))


def data(label, R):
    alpha, beta, gamma = jac(Q, R), -jac(P, R), jac(P, Q)
    p_contact = (
        sp.factor(alpha.subs(p, 0) / q**5),
        sp.factor(beta.subs(p, 0) / q**5),
    )
    q_contact = (
        sp.factor(alpha.subs(q, 0) / p**5),
        sp.factor(beta.subs(q, 0) / p**5),
    )
    eval_L = sp.factor(R.subs(p, s * q) / q**3)
    eval_M = sp.factor(R.subs(q, s * p) / p**3)
    print("===", label, "===")
    print("R =", sp.factor(R))
    print("p-contact pair =", p_contact)
    print("q-contact pair =", q_contact)
    print("R(L) =", eval_L)
    print("R(M) =", eval_M)
    print("gamma =", sp.factor(gamma))


data("L2M", L**2 * M)

# One fixed root L plus both branch contacts: the generic delta-three
# formula obtained by solving p- and q-contact equations.
R_L_pq = (
    M
    * (
        4 * p**2 * s**3
        - 12 * p**2 * s
        - 3 * p * q * s**4
        + 10 * p * q * s**2
        - 3 * p * q
        - 12 * q**2 * s**3
        + 4 * q**2 * s
    )
)
data("M_plus_two_contacts", R_L_pq)

# Double L plus p-contact; q-contact creates the delta-four boundary.
R_L2_p = L**2 * ((3 * s**2 - 5) * p - 4 * s * q)
data("L2_plus_p_contact", R_L2_p)

# L,M plus p-contact; q-contact creates the delta-four boundary.
R_LM_p = L * M * (4 * s * p + (s**2 + 1) * q)
data("LM_plus_p_contact", R_LM_p)
