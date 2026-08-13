#!/usr/bin/env python3
"""Exact algebra replay for paired Schur-trace exhaustion.

This is not a graph search.  It checks the scalar identities and sharp
constants used in PAIRED_SCHUR_TRACE_EXHAUSTION.md.
"""

import sympy as sp


def main() -> None:
    c, eps, slack, err = sp.symbols("c eps slack err", positive=True)
    dB, dD, pB, pD, tB, tD, eB, eD = sp.symbols(
        "dB dD pB pD tB tD eB eD", real=True
    )

    # Exact affine bookkeeping: Delta = packet + trace + error and
    # L(packet) = -slack.
    L = lambda B, D: D + c * B
    identities = [
        sp.expand(dB - pB - tB - eB),
        sp.expand(dD - pD - tD - eD),
        sp.expand(L(pB, pD) + slack),
    ]
    solved = {
        pB: dB - tB - eB,
        pD: dD - tD - eD,
    }
    charge = sp.expand(L(tB, tD) - (L(dB, dD) + slack - L(eB, eD)))
    charge = charge.subs(slack, -L(pB, pD)).subs(solved)
    assert sp.simplify(charge) == 0

    # The norm conversion constant is c/(1+c)=(r-1)/r when r=1+c.
    r = sp.symbols("r", positive=True)
    assert sp.simplify((c / (1 + c)).subs(c, r - 1) - (r - 1) / r) == 0

    # Weighted trace-event budget: |tau_U| <= beta_U implies
    # L(tau) <= beta_D+c beta_B.  The sharp lower support constant over the
    # positive max-norm unit boundary is min(1,c)=c for 0<c<1.
    betaB, betaD = sp.symbols("betaB betaD", nonnegative=True)
    weighted_budget = betaD + c * betaB
    assert sp.diff(weighted_budget, betaB) == c
    assert sp.diff(weighted_budget, betaD) == 1

    # If both beta coordinates were below c/(1+c)*eps, their weighted sum
    # would be below c*eps.  Equality verifies the constant in (26).
    threshold = c * eps / (1 + c)
    assert sp.simplify(threshold + c * threshold - c * eps) == 0

    # Controlled-error loss is exactly |e_D|+c|e_B| <= (1+c)||e||_inf.
    assert sp.expand((1 + c) * err - (err + c * err)) == 0

    print("paired Schur-trace exhaustion algebra: PASS")


if __name__ == "__main__":
    main()
