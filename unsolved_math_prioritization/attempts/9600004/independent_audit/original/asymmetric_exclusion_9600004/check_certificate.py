#!/usr/bin/env python3
"""Exact, dependency-free replay of the four-site small-time NA certificate."""
import argparse
from collections import defaultdict, Counter
from fractions import Fraction as F
from itertools import combinations
from math import factorial, prod
from pathlib import Path
import json

ORDER = 6
SITES = [-1, 0, 1, 2]

def need(ok, message):
    if not ok:
        raise ValueError(message)

def padd(a, b):
    c = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a): c[i] += x
    for i, x in enumerate(b): c[i] += x
    while len(c) > 1 and c[-1] == 0: c.pop()
    return tuple(c)

def scale(a, x): return tuple(x * z for z in a)
def mul(a, b):
    c = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): c[i + j] += x * y
    while len(c) > 1 and c[-1] == 0: c.pop()
    return tuple(c)

def encode(a): return [str(x) for x in a]
def nonzero(a): return any(a)

def marginal_series(half_width=8):
    """Normalize right rate to 1; retain left rate r as a formal indeterminate."""
    need(half_width > ORDER + 1, 'window too small')
    n = 2 * half_width
    v = {(1 << half_width) - 1: (F(1),)}
    out = []
    for k in range(ORDER + 1):
        z = [(F(0),) for _ in range(16)]
        for s, a in v.items():
            mask = (s >> (half_width - 2)) & 15
            z[mask] = padd(z[mask], scale(a, F(1, factorial(k))))
        total = (F(0),)
        for a in z: total = padd(total, a)
        need(total == ((F(1),) if k == 0 else (F(0),)), 'mass conservation')
        out.append(z)
        if k == ORDER: break
        w = {}
        for s, a in v.items():
            for i in range(n - 1):
                x, y = (s >> i) & 1, (s >> (i + 1)) & 1
                if x == y: continue
                rate = (F(1),) if x else (F(0), F(1))
                amount = mul(rate, a)
                dst = s ^ (3 << i)
                w[dst] = padd(w.get(dst, (F(0),)), amount)
                w[s] = padd(w.get(s, (F(0),)), scale(amount, -1))
        v = {s:a for s,a in w.items() if nonzero(a)}
    return out

def increasing_families(A):
    size = 1 << len(A)
    for family in range(1, (1 << size) - 1):
        if all(not (family >> x) & 1 or all((family >> y) & 1
               for y in range(size) if (x & y) == x) for x in range(size)):
            masks = tuple(s for s in range(16) if (family >> sum(
                ((s >> i) & 1) << j for j, i in enumerate(A))) & 1)
            yield family, masks

def mean_series(D, masks):
    out = []
    for z in D:
        a = (F(0),)
        for s in masks: a = padd(a, z[s])
        out.append(a)
    return out

def make_certificate(half_width=8):
    D = marginal_series(half_width)
    events = {A:list(increasing_families(A)) for n in range(1,4)
              for A in combinations(range(4), n)}
    need([len(events[tuple(range(n))]) for n in range(1,4)] == [1,4,18],
         'increasing-event enumeration count')
    cases = []
    for A in events:
        for B in events:
            if A >= B or set(A) & set(B): continue
            for aid, amasks in events[A]:
                for bid, bmasks in events[B]:
                    ea = mean_series(D, amasks)
                    eb = mean_series(D, bmasks)
                    ec = mean_series(D, sorted(set(amasks) & set(bmasks)))
                    cov = []
                    for k in range(ORDER + 1):
                        c = ec[k]
                        for j in range(k + 1): c = padd(c, scale(mul(ea[j], eb[k-j]), -1))
                        cov.append(c)
                    lead = next((k for k,c in enumerate(cov) if nonzero(c)), None)
                    need(lead is not None and lead > 0, 'missing strictly negative leading term')
                    need(len(cov[lead]) == 1 and cov[lead][0] < 0,
                         'leading term must be strictly negative, independent of r')
                    cases.append({'A':[SITES[i] for i in A], 'B':[SITES[i] for i in B],
                        'A_truth_table':aid, 'B_truth_table':bid,
                        'covariance_taylor_in_tau': [encode(c) for c in cov],
                        'leading_order':lead, 'leading_coefficient':str(cov[lead][0])})
    need(len(cases) == 174, 'case count')
    bounds = []
    for c in cases:
        k = c['leading_order']; a = -F(c['leading_coefficient']); m = k + 1
        Dm = 2**m * prod(5+2*j for j in range(m))
        bounds.append(a * factorial(m) / (2 * (1 + 2**m) * Dm))
    delta = min(bounds)
    histogram = Counter((c['leading_order'], c['leading_coefficient']) for c in cases)
    return {'schema':1, 'problem_id':9600004, 'status':'PROVED-LOCAL-PARTIAL',
        'sites':SITES, 'initial_occupied':'all integers <= 0',
        'rates':'right p > 0; left 0 <= q <= p',
        'normalized_time':'tau = p*t', 'formal_variable':'r = q/p',
        'order':ORDER, 'case_count':len(cases), 'delta':str(delta),
        'histogram':[{'order':k,'coefficient':a,'count':v} for (k,a),v in sorted(histogram.items())],
        'cases':cases}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    ap.add_argument('--emit', action='store_true')
    ap.add_argument('--cross-window', action='store_true')
    args = ap.parse_args()
    computed = make_certificate()
    if args.cross_window:
        need(computed == make_certificate(9), 'larger-window mismatch')
    if args.emit:
        args.certificate.write_text(json.dumps(computed, indent=2) + '\n')
    else:
        supplied = json.loads(args.certificate.read_text())
        need(supplied == computed, 'certificate differs from complete exact recomputation')
    print(json.dumps({'ok':True, 'cases':computed['case_count'], 'delta':computed['delta'],
        'histogram':computed['histogram'], 'cross_window':args.cross_window}, sort_keys=True))

if __name__ == '__main__': main()
