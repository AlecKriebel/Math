#!/usr/bin/env python3
"""Independent algebraic tests of the bridge gauge and capped gluing bounds."""

from __future__ import annotations

from fractions import Fraction as Q
import json
from pathlib import Path
import random

import sympy as sp


def determinant_and_rank_for_degree(d):
    rows = []
    pairs = [(0, 1), (0, 2), (1, 2)] + [(0, k) for k in range(3, d)]
    for i, j in pairs:
        row = [0] * d
        row[i] = row[j] = 1
        rows.append(row)
    M = sp.Matrix(rows)
    return M.rank(), int(M[:d, :d].det())


def physical_margins(y):
    c, g, t = y
    return (c, g, t, 1-c, 1-g, 1-t,
            1+c-g-t, 1-c+g-t, 1-c-g+t,
            c-g*t, g-c*t, t-c*g)


def main():
    ranks = {}
    for d in range(3, 13):
        rank, det = determinant_and_rank_for_degree(d)
        assert rank == d and det == -2
        ranks[str(d)] = {"one_sector_rank": rank, "selected_determinant": det,
                         "three_sector_rank": 3*rank, "leading_three_sector_determinant": det**3}

    # Direct symbolic inversion of pair-anchor ratios.
    a1,a2,a3,a4 = sp.symbols("a1 a2 a3 a4", positive=True)
    r12,r13,r23,r14 = a1*a2,a1*a3,a2*a3,a1*a4
    recovered = (
        sp.sqrt(r12*r13/r23), sp.sqrt(r12*r23/r13),
        sp.sqrt(r13*r23/r12), r14/sp.sqrt(r12*r13/r23),
    )
    assert all(sp.simplify(x-y)==0 for x,y in zip(recovered,(a1,a2,a3,a4)))

    # The excluded unmarked degree-two case genuinely has a stabilizer:
    # (a1,a2)=(tau,tau^-1) fixes its sole pair anchor.
    tau=sp.symbols("tau", positive=True)
    assert sp.simplify(tau*(1/tau)-1)==0

    # Verify gauge cancellation on a three-component bridge path independently
    # in every sector.  Component factors collect incidence scales and each
    # bridge factor contributes their reciprocal product.
    rng=random.Random(20260826)
    cancellation=[]
    for sector in "CGT":
        P=[Q(rng.randint(2,11),rng.randint(12,23)) for _ in range(3)]
        k=[Q(rng.randint(2,11),rng.randint(12,23)) for _ in range(2)]
        a01=Q(rng.randint(2,9),rng.randint(10,19));a10=Q(rng.randint(2,9),rng.randint(10,19))
        a12=Q(rng.randint(2,9),rng.randint(10,19));a21=Q(rng.randint(2,9),rng.randint(10,19))
        before=P[0]*P[1]*P[2]*k[0]*k[1]
        after=(P[0]*a01)*(P[1]*a10*a12)*(P[2]*a21)*(k[0]/(a01*a10))*(k[1]/(a12*a21))
        assert before==after
        cancellation.append({"sector":sector,"contracted_value":str(before)})

    # Stress-test the capped construction at exact rational bounds, including
    # independent A_C,A_G,A_T at their worst allowed endpoints.
    trials=[]
    for _ in range(1000):
        U=Q(rng.randint(2,100),rng.randint(1,15))
        L=U*Q(rng.randint(1,9),10)
        eps=min(Q(1,4),L*L/(8*U))
        A=[L+(U-L)*Q(rng.randint(0,1000),1000) for _ in range(3)]
        x=tuple(eps/a for a in A)
        z=(eps,eps,eps)
        assert min(physical_margins(x))>0 and min(physical_margins(z))>0
        asserted_ct=7*eps/(8*U)
        actual_ct=min(x[0]-x[1]*x[2],x[1]-x[0]*x[2],x[2]-x[0]*x[1])
        assert actual_ct>=asserted_ct
        trials.append((min(physical_margins(x)),actual_ct-asserted_ct))

    # Symbolically expose the exact inequality used at the cap.
    L,U,eps=sp.symbols("L U eps", positive=True)
    algebra={
        "ct_lower_decomposition": str(sp.expand(eps/U-eps**2/L**2-7*eps/(8*U))),
        "needed_cap": "eps <= L^2/(8U)",
        "principal_needed": "eps/L <= 1/8",
    }
    result={
        "unmarked_degree_at_least_three_exponent_checks":ranks,
        "pair_anchor_inverse_verified":True,
        "marked_component_freeness_reason":"one-character leaf/bridge anchors have identity exponent matrix",
        "degree_two_boundary_counterexample":"An unmarked d=2 component has stabilizer (tau,tau^-1); the theorem therefore depends on its topological exclusion.",
        "sectorwise_gauge_cancellation":cancellation,
        "capped_gluing_random_exact_trials":len(trials),
        "smallest_actual_physical_margin_seen":str(min(x[0] for x in trials)),
        "smallest_excess_over_claimed_ct_bound":str(min(x[1] for x in trials)),
        "capped_bound_algebra":algebra,
        "limitation":"The algebraic freeness check is complete conditional on the article's marked-or-degree>=3 dichotomy. I did not independently enumerate every retained strong-class topology to re-prove exclusion of the unmarked degree-two K4-e factor."
    }
    Path("bridge_and_gluing_results.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__":
    main()
