#!/usr/bin/env python3
"""Independent controls of candidate math, before reading its programs.

Exact full-future disagreement probability for finite-memory approximations,
not only disagreement at a selected coordinate. Finite checks supplement proof.
"""
from fractions import Fraction as F
from itertools import product
import json


def p_one(h):
    return F(1, 2) + F(1, 4) * sum(F(2*x-1, 2**j)
               for j, x in enumerate(reversed(h), 1))


def transition(h, k):
    ph, pk = p_one(h), p_one(k)
    out = {}
    for a, b in product(range(2), repeat=2):
        pa, qb = (ph if a else 1-ph), (pk if b else 1-pk)
        if a == b:
            mass = min(pa, qb)
        else:
            # For binary marginals, only one off-diagonal direction is positive:
            # mass(a,b)=max(p(a)-q(a),0), with b=1-a.
            qa = pk if a else 1-pk
            mass = max(F(0), pa-qa)
        if mass:
            out[(h[1:]+(a,), k[1:]+(b,))] = mass
    assert sum(out.values()) == 1
    return out


def any_future_failure(kernels, state):
    """No mismatch for M steps forces identical histories and permanent agreement."""
    m = len(state[0])
    survival = {state: F(1)}
    for _ in range(m):
        nxt = {}
        for z, mass in survival.items():
            for zz, t in kernels[z].items():
                if zz[0][-1] == zz[1][-1]:
                    nxt[zz] = nxt.get(zz, F(0)) + mass*t
        survival = nxt
    assert all(z[0] == z[1] for z in survival)
    return 1-sum(survival.values())


def run(m, all_pairs, nmax):
    hs = list(product(range(2), repeat=m))
    states = list(product(hs, repeat=2))
    kernels = {z: transition(*z) for z in states}
    failure = {z: any_future_failure(kernels, z) for z in states}
    seeds = states if all_pairs else [((0,)*m, (1,)*m)]
    checks, worst = 0, F(0)
    last = []
    for seed in seeds:
        law = {seed: F(1)}
        for n in range(1, nmax+1):
            nxt = {}
            for z, mass in law.items():
                for zz, t in kernels[z].items():
                    nxt[zz] = nxt.get(zz, F(0)) + mass*t
            law = nxt
            assert sum(law.values()) == 1
            full_future = sum(mass*failure[z] for z, mass in law.items())
            bound = min([F(1)] + [(1-F(1, 2)**l)**(n//l)+F(1, 2**l)
                         for l in range(1, n+1)])
            assert full_future <= bound
            for l in range(1, n+1):
                # Candidate displayed bound without the minimum also valid.
                assert full_future <= (1-F(1, 2)**l)**(n//l)+F(1, 2**l)
                checks += 1
            worst = max(worst, full_future/bound)
            if seed == seeds[-1] and n == nmax:
                last = [str(full_future), str(bound)]
    return {"history_length": m, "initial_pairs": len(seeds),
            "nmax": nmax, "displayed_bound_comparisons": checks,
            "maximum_observed_ratio": float(worst),
            "last_full_future_disagreement": last[0], "last_bound": last[1]}


if __name__ == '__main__':
    print(json.dumps({"status": "pass", "controls": [run(3, True, 12),
                                                      run(4, False, 32)],
                      "infinite_memory_scope": "finite approximations only; see universal proof"},
                     indent=2, sort_keys=True))
