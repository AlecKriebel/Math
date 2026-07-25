#!/usr/bin/python3
"""Exact geometric regressions for the symmetric-monodromy theorem.

These finite checks do not replace the all-degree proof in NOTE.md.
"""

import sympy as sp


T, U, V, r, w = sp.symbols("T U V r w")


def geometric_sum(m: int):
    return sum(r**j for j in range(m + 1))


for d in range(3, 11):
    # The collision elimination in equations (9)--(11).
    s_dm2 = geometric_sum(d - 2)
    s_dm1 = geometric_sum(d - 1)
    lhs = (r - 1) * (
        2 * (d - 1) * s_dm1 - d * (r + 1) * s_dm2
    )
    n_d = (d - 2) * r**d - d * r ** (d - 1) + d * r - (d - 2)
    assert sp.expand(lhs - n_d) == 0
    assert sp.Poly(n_d, r).degree() == d

    # The seed and tangent-sweep identities used in the weighted lift.
    p_d = (2 * w - d * w ** (d - 1)) / sp.Integer(d - 2)
    q_d = (w**2 - (d - 1) * w**d) / sp.Integer(d - 2)
    assert sp.expand(sp.diff(q_d, w) - w * sp.diff(p_d, w)) == 0
    assert sp.cancel(p_d.subs(w, 0)) == 0
    assert sp.cancel(p_d.subs(w, 1)) == -1
    assert sp.cancel(sp.integrate(p_d, (w, 0, 1))) == 0

    # One exact complex Morse specialization per row.  U=0 works for odd
    # d; U=1 avoids the symmetric collision in the even rows.
    u0 = 0 if d % 2 else 1
    g = T**d - T**2 + u0 * T
    derivative = sp.Poly(sp.diff(g, T), T)
    assert sp.gcd(derivative, derivative.diff()).degree() == 0

    branch = sp.Poly(sp.resultant(g + V, sp.diff(g, T), T), V)
    assert branch.degree() == d - 1
    assert sp.gcd(branch, branch.diff()).degree() == 0

print(
    "PASS: exact critical-value, seed, and Morse checks for d=3,...,10"
)
