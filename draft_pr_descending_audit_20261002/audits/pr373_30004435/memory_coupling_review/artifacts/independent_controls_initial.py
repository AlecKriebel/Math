#!/usr/bin/env python3
"""Original exact finite controls, written before reading candidate code.

The universal claims are proved in SOURCE_FIRST_BASELINE.md; these controls
validate formulas and disambiguate false implications. No external packages.
"""
from fractions import Fraction as F
from itertools import product
import json


def maximal(p, q):
    d = [min(a, b) for a, b in zip(p, q)]
    t = 1 - sum(d)
    n = len(p)
    m = [[F(0) for _ in p] for _ in p]
    for i in range(n):
        m[i][i] = d[i]
    if t:
        for i in range(n):
            for j in range(n):
                if i != j:
                    m[i][j] = (p[i] - d[i]) * (q[j] - d[j]) / t
    return m


def coupling_grid():
    ps = [tuple(F(x, 4) for x in z) for z in product(range(5), repeat=3)
          if sum(z) == 4]
    for p, q in product(ps, repeat=2):
        m = maximal(p, q)
        assert all(x >= 0 for row in m for x in row)
        assert [sum(row) for row in m] == list(p)
        assert [sum(m[i][j] for i in range(3)) for j in range(3)] == list(q)
        tv = sum(abs(a - b) for a, b in zip(p, q)) / 2
        assert sum(m[i][i] for i in range(3)) == 1 - tv
    triangle = [(F(1, 2), F(1, 2), F(0)),
                (F(0), F(1, 2), F(1, 2)),
                (F(1, 2), F(0), F(1, 2))]
    eta = min(sum(min(a, b) for a, b in zip(p, q))
              for p, q in product(triangle, repeat=2))
    common = sum(min(p[i] for p in triangle) for i in range(3))
    assert eta == F(1, 2) and common == 0
    return {"rational_pairs_checked": len(ps)**2,
            "triangle_pair_overlap": str(eta), "triangle_common_mass": str(common)}


def finite_housecard():
    bs = [F(1, 2), F(1, 4), F(1, 8)]
    def b(i):
        return bs[i] if i < len(bs) else F(0)
    c = F(1)
    fs = [F(0)]
    prefix = F(1)
    for x in bs:
        fs.append(prefix * x)
        prefix *= 1 - x
    c = prefix
    assert sum(fs) == 1-c
    law = {0: F(1)}
    us = [F(1)]
    nmax = 96
    for n in range(1, nmax+1):
        nxt = {}
        for k, mass in law.items():
            nxt[0] = nxt.get(0, F(0)) + mass*b(k)
            nxt[k+1] = nxt.get(k+1, F(0)) + mass*(1-b(k))
        law = nxt
        assert sum(law.values()) == 1
        u = sum(fs[j]*us[n-j] for j in range(1, min(n, len(bs))+1))
        assert u == law.get(0, 0)
        us.append(u)
    partial_last_mass = c*sum(us)
    assert partial_last_mass <= 1
    expected_last = sum(i*fs[i] for i in range(1, len(fs))) / c
    assert expected_last == F(47, 21)
    steps = 0
    for s in range(8):
        for l in range(s, 9):
            for q in [F(0), b(l)/2, b(l)]:
                thresholds = sorted({F(0), 1-b(s), 1-q, F(1)})
                for a, z in zip(thresholds, thresholds[1:]):
                    u = (a+z)/2
                    sn = s+1 if u <= 1-b(s) else 0
                    ln = l+1 if u <= 1-q else 0
                    assert ln >= sn
                    steps += 1
    return {"b": [str(x) for x in bs], "escape_probability": str(c),
            "first_return_masses": [str(x) for x in fs[1:]],
            "expected_last_return": str(expected_last),
            "recurrence_times_checked": nmax,
            "monotone_transition_cases_checked": steps,
            "partial_last_return_mass_96": float(partial_last_mass),
            "total_expected_visits_formula": str(1/c)}


def future_countercontrol():
    # Q probability of no 1 in t=n,...,k telescopes to n/(k+1).
    out = []
    for n, k in [(1, 16), (4, 32), (25, 256)]:
        prob = F(1)
        for t in range(n, k+1):
            prob *= 1-F(1, t+1)
        assert prob == F(n, k+1)
        out.append({"n": n, "k": k, "no_1_probability": str(prob)})
    return {"finite_telescoping_controls": out,
            "infinite_future_tv_by_limit": 1,
            "scope": "logical implication control; nonstationary"}


def weighted_countercontrol():
    # Exact partial sums do not prove convergence/divergence; the baseline's
    # comparisons with sum 1/(m+1)^2 and the harmonic series do.
    out = []
    for cutoff in [16, 64, 256]:
        bs = [F(1, 2*(m+1)**2) for m in range(cutoff)]
        c = F(1)
        for x in bs:
            c *= 1-x
        out.append({"cutoff": cutoff,
                    "unweighted_sum": float(sum(bs)),
                    "weighted_sum": float(sum((m+1)*x for m, x in enumerate(bs))),
                    "partial_escape_product": float(c)})
    return {"partial_values": out,
            "unweighted_summable": True, "weighted_divergent": True,
            "last_return_finite_almost_surely": True,
            "last_return_expectation": "infinite by analytic harmonic comparison"}


if __name__ == "__main__":
    result = {"status": "pass", "maximal_coupling": coupling_grid(),
              "renewal_and_domination": finite_housecard(),
              "coordinate_vs_full_future": future_countercontrol(),
              "finite_time_vs_finite_mean": weighted_countercontrol()}
    print(json.dumps(result, indent=2, sort_keys=True))
