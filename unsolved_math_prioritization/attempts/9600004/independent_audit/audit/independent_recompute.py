#!/usr/bin/env python3
"""Independent exact certificate audit: infinite configurations and antichains.

No author module imports; only standard-library integer/rational arithmetic.
A state is the finite set of sites whose occupation differs from the chosen
infinite step. Polynomial monomials in r are kept as separate signed integers.
"""
import argparse
from collections import defaultdict, Counter
from fractions import Fraction
from itertools import combinations
from math import factorial, comb
from pathlib import Path
import json

C = (-1, 0, 1, 2)
N = 6

def require(ok, message):
    if not ok:
        raise ValueError(message)

def occupation(state, x, reversed_step=False):
    base = (x > 0) if reversed_step else (x <= 0)
    return int(base != (x in state))

def infinite_derivatives(reverse_rates=False, reversed_step=False):
    v = {(frozenset(), 0): 1}
    out = []
    history = []
    for n in range(N + 1):
        marginal = defaultdict(int)
        for (state, power), value in v.items():
            mask = sum(occupation(state, x, reversed_step) << j for j, x in enumerate(C))
            marginal[mask, power] += value
        marginal = {k:v for k,v in marginal.items() if v}
        for power in range(N + 1):
            require(sum(v for (mask,p),v in marginal.items() if p == power) ==
                    int(n == 0 and power == 0), 'mass conservation failed')
        out.append(marginal)
        states = {s for s,p in v}
        history.append({'order': n, 'states': len(states),
                        'deviation_sites': sorted(set().union(*states))})
        if n == N:
            break
        nxt = defaultdict(int)
        for (state, power), value in v.items():
            # Outside these bonds both occupations equal the constant background.
            bonds = {0}
            for x in state:
                bonds.update((x-1, x))
            for x in bonds:
                a = occupation(state, x, reversed_step)
                b = occupation(state, x+1, reversed_step)
                if a == b:
                    continue
                extra = (a == 1) if reverse_rates else (a == 0)
                dst = state ^ frozenset((x, x+1))
                nxt[dst, power + int(extra)] += value
                nxt[state, power + int(extra)] -= value
        v = {k:v for k,v in nxt.items() if v}
    return out, history

def antichain_events(support):
    cube = range(1 << len(support))
    ans = []
    for size in range(1, len(cube) + 1):
        for mins in combinations(cube, size):
            if any((a & b) in (a,b) for a,b in combinations(mins, 2)):
                continue
            truth = sum(1 << x for x in cube if any((x & a) == a for a in mins))
            if truth == (1 << len(cube)) - 1:
                continue
            maskset = frozenset(s for s in range(16) if truth & (1 << sum(
                ((s >> C.index(x)) & 1) << j for j,x in enumerate(support))))
            ans.append((truth, maskset))
    return sorted(ans)

def mean(jets, masks):
    result = []
    for n, layer in enumerate(jets):
        terms = defaultdict(Fraction)
        for (mask,power), value in layer.items():
            if mask in masks:
                terms[power] += Fraction(value, factorial(n))
        result.append({p:v for p,v in terms.items() if v})
    return result

def covariance(a,b,ab):
    result = []
    for n in range(N+1):
        c = defaultdict(Fraction, ab[n])
        for i in range(n+1):
            for p,x in a[i].items():
                for q,y in b[n-i].items():
                    c[p+q] -= x*y
        c = {p:v for p,v in c.items() if v}
        result.append([str(c.get(p, Fraction(0))) for p in range(max(c, default=0)+1)])
    return result

def all_cases(jets):
    supports = [s for n in range(1,4) for s in combinations(C,n)]
    events = {s:antichain_events(s) for s in supports}
    require([len(events[C[:i]]) for i in (1,2,3)] == [1,4,18], 'antichain counts')
    cases = {}
    event_pairs = set()
    for A,B in combinations(sorted(supports),2):
        if set(A) & set(B):
            continue
        for aid, am in events[A]:
            for bid, bm in events[B]:
                cov = covariance(mean(jets,am),mean(jets,bm),mean(jets,am & bm))
                key = (A,B,aid,bid)
                require(key not in cases, 'duplicate support/event key')
                cases[key] = cov
                event_pairs.add(tuple(sorted((tuple(sorted(am)),tuple(sorted(bm))))))
    require(len(cases) == 174, 'independent enumeration count')
    return cases, len(event_pairs)

def derivative_bounds():
    d = [1]
    for j in range(7):
        d.append(d[-1]*2*(5+2*j))
    for j in range(8):
        for i in range(j+1):
            require(d[i]*d[j-i] <= d[j], 'submultiplicative derivative bound')
    return d

def validate(cert, cases):
    require(cert['sites'] == list(C) and cert['order'] == N, 'site/order mismatch')
    require(cert['initial_occupied'] == 'all integers <= 0', 'step mismatch')
    require(cert['rates'] == 'right p > 0; left 0 <= q <= p', 'rates mismatch')
    require(cert['normalized_time'] == 'tau = p*t' and cert['formal_variable'] == 'r = q/p', 'normalization mismatch')
    expected = {}
    for c in cert['cases']:
        key = (tuple(c['A']),tuple(c['B']),c['A_truth_table'],c['B_truth_table'])
        require(key not in expected, 'duplicate certificate case')
        expected[key] = c
    require(set(expected) == set(cases), 'event key coverage mismatch')
    d = derivative_bounds()
    hist = Counter()
    bounds = []
    for key, cov in cases.items():
        c = expected[key]
        require(c['covariance_taylor_in_tau'] == cov, 'coefficient mismatch')
        lead = next((j for j,row in enumerate(cov) if any(Fraction(v) for v in row)), None)
        require(lead is not None and lead > 0, 'missing strictly negative leading term')
        row = cov[lead]
        require(len(row) == 1 and Fraction(row[0]) < 0, 'nonnegative or parameter-dependent leading term')
        require(c['leading_order'] == lead and c['leading_coefficient'] == row[0], 'leading metadata mismatch')
        hist[lead,row[0]] += 1
        bounds.append(-Fraction(row[0])*factorial(lead+1)/(2*(1+2**(lead+1))*d[lead+1]))
    require(cert['case_count'] == len(cases), 'case count mismatch')
    histogram = [{'order':k,'coefficient':a,'count':n} for (k,a),n in sorted(hist.items())]
    require(cert['histogram'] == histogram, 'histogram mismatch')
    delta = min(bounds)
    require(Fraction(cert['delta']) == delta, 'time bound mismatch')
    require(delta == Fraction(1,10837981440), 'independent time constant')
    return {'histogram':histogram,'delta':str(delta),'derivative_bounds':d,
            'minimum_attaining_cases':sum(x == delta for x in bounds)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--certificate', type=Path, default=Path(__file__).resolve().parents[1]/'original'/'asymmetric_exclusion_9600004'/'certificate.json')
    p.add_argument('--reverse-rates',action='store_true')
    p.add_argument('--reverse-step',action='store_true')
    args=p.parse_args()
    jets,history=infinite_derivatives(args.reverse_rates,args.reverse_step)
    cases,unique=all_cases(jets)
    cert=json.loads(args.certificate.read_text())
    result=validate(cert,cases)
    print(json.dumps({'ok':True,'method':'infinite deviations, integer polynomial jets, antichain enumeration',
                     'cases':len(cases),'distinct_lifted_event_pairs':unique,'history':history,**result},indent=2))

if __name__ == '__main__':
    main()
