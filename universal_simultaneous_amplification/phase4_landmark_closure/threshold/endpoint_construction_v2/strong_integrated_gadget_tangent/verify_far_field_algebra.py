#!/usr/bin/env python3
"""Exact symbolic audit of the ordinary-core far-field correction.

The gadget is resident and the core contains ``k`` mutants.  We apply the
finite-C core transition rates to ``h_0(k)=1-r**(-k)`` and extract the
coefficient of ``k*r**(-k)/C``.  Abstract symbols collect the gadget sums;
the local-chain solver verifies their individual terms separately.
"""

from __future__ import annotations

import sympy as sp


def main() -> None:
    C, k, r = sp.symbols("C k r", positive=True)
    P, S0, UB, UD = sp.symbols("P S0 UB UD", finite=True)
    p = (r - 1) / r

    # Bd: S0=sum_i x_i/d_i and UB=sum_i x_i*u_B(i).
    up_bd = r * k * (C - k) / (C - 1 + P)
    down_bd = k * (C - k) / (C - 1 + P) + k * S0 / C
    core_bd = sp.factor(up_bd * p - down_bd * (r - 1))
    core_bd_limit = sp.factor(sp.limit(C * core_bd / k, C, sp.oo))
    assert sp.factor(core_bd_limit + (r - 1) * S0) == 0
    activation_bd_limit = r * UB
    source_bd = sp.factor(activation_bd_limit + core_bd_limit)
    assert sp.factor(source_bd - (r * UB - (r - 1) * S0)) == 0

    # dB: UD=sum_i x_i*u_D(i)/d_i.  The displayed rates are exact while
    # the gadget is resident; each gadget-target activation contributes
    # r*k*x_i/[C*d_i+(r-1)k*x_i], whose scaled sum tends to r*UD.
    up_db = (C - k) * r * k / (C - 1 + P + (r - 1) * k)
    down_db = k * (C - k + P) / (C + P - r + (r - 1) * k)
    core_db = sp.factor(up_db * p - down_db * (r - 1))
    core_db_limit = sp.factor(sp.limit(C * core_db / k, C, sp.oo))
    expected_core_db = -(r - 1) * (P + r - 1)
    assert sp.factor(core_db_limit - expected_core_db) == 0
    source_db = sp.factor(r * UD + core_db_limit)
    assert sp.factor(source_db - (r * UD + expected_core_db)) == 0

    # The leading core branching generator has up/down rates r*k and k.
    # Its action on g(k)=k*r^{-k} is exactly -(r-1)g(k).
    g = k * r ** (-k)
    generator_g = sp.factor(
        r * k * ((k + 1) * r ** (-(k + 1)) - g)
        + k * ((k - 1) * r ** (-(k - 1)) - g)
    )
    assert sp.factor(generator_g + (r - 1) * g) == 0

    print("Bd source = r*UB-(r-1)*S0")
    print("dB source = r*UD-(r-1)*(P+r-1)")
    print("PASS exact far-field residual and Poisson-response algebra")


if __name__ == "__main__":
    main()
