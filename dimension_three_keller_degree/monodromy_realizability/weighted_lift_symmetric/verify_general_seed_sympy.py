#!/usr/bin/python3
"""Symbolic checks of Gallagher's general admissible-seed identities.

For each generic degree 3 through 10, the seed coefficients remain symbolic
subject only to Gallagher's two linear endpoint/integral constraints.
"""

import sympy as sp


w = sp.symbols("w")


for d in range(3, 11):
    tail = sp.symbols(f"a2:{d}")
    coefficients = {j: tail[j - 2] for j in range(2, d)}

    # The integral constraint determines the linear coefficient.
    a1 = -2 * sum(coefficients[j] / sp.Integer(j + 1) for j in coefficients)
    p = a1 * w + sum(coefficients[j] * w**j for j in coefficients)
    c = -sp.expand(p.subs(w, 1))
    assert c != 0
    assert sp.expand(p.subs(w, 0)) == 0
    assert sp.cancel(p.subs(w, 1) + c) == 0
    assert sp.cancel(sp.integrate(p, (w, 0, 1))) == 0

    phi = sp.integrate(p, w)
    q = sp.cancel((w * p - phi) / c)
    assert sp.cancel(q.subs(w, 0)) == 0
    assert sp.cancel(sp.diff(q, w).subs(w, 0)) == 0
    assert sp.cancel(sp.diff(q, w) - w * sp.diff(p, w) / c) == 0
    assert sp.cancel(phi - w * p + c * q) == 0
    assert sp.cancel(q.subs(w, 1) + 1) == 0

    kappa = sp.cancel(sp.diff(p, w).subs(w, 1) / c)
    assert sp.cancel(2 + kappa) != 0
    a = sp.cancel(-(1 + kappa) / (2 + kappa))

    # At (v,t)=(0,0), one has u=gamma=w=1.  These three jet
    # identities are exactly the divisibility conditions for beta/x and
    # alpha/x^2; evaluating them before composition avoids exponential
    # expression growth while retaining all symbolic seed coefficients.
    beta_origin = c + p.subs(w, 1)
    alpha_origin = 1 + q.subs(w, 1)
    alpha_v_origin = (
        1
        + sp.diff(q, w).subs(w, 1) * (1 + a)
        - 2 * a * q.subs(w, 1)
    )
    assert sp.cancel(beta_origin) == 0
    assert sp.cancel(alpha_origin) == 0
    assert sp.cancel(alpha_v_origin) == 0

print("PASS: symbolic general-seed identities for generic degrees 3,...,10")
