#!/usr/bin/env python3
"""Independent high-precision re-evaluation of retained optimizer candidates.

This is explicitly numerical, not an interval proof or global optimization.
Only derived verification metadata is output; no input arrays are copied.
"""
from decimal import Decimal as D, localcontext
from pathlib import Path
import hashlib
import itertools
import json
import sys

def run(path, precision=80):
    data = Path(path).read_bytes()
    records = json.loads(data,parse_float=D)
    output = []
    with localcontext() as context:
        context.prec = precision
        for row in records['results']:
            n = row['n']
            states = list(itertools.permutations(range(n)))
            assert states == list(map(tuple,row['permutations']))
            rho, psi = row['rho'], row['psi']
            assert len(rho) == len(psi) == len(states) and min(rho) > 0
            q = D(2)/D(n*(n-1)); mu = D(1)/D(len(states))
            adj = [[j for j,t in enumerate(states) if sum(x != y for x,y in zip(state,t)) == 2]
                   for state in states]
            lr = [q*sum((rho[j]-rho[i] for j in neighbors),D(0)) for i,neighbors in enumerate(adj)]
            lp = [q*sum((psi[j]-psi[i] for j in neighbors),D(0)) for i,neighbors in enumerate(adj)]
            A = B = D(0)
            for i,neighbors in enumerate(adj):
                for j in neighbors:
                    a,b = rho[i],rho[j]
                    if a == b:
                        mean,d1,d2 = a,D('0.5'),D('0.5')
                    else:
                        z = a.ln()-b.ln()
                        mean = (a-b)/z
                        d1 = 1/z-(a-b)/(a*z*z)
                        d2 = -1/z+(a-b)/(b*z*z)
                    g = psi[j]-psi[i]
                    A += mu*q*mean*g*g/2
                    B += mu*q*((d1*lr[i]+d2*lr[j])*g*g/4-mean*g*(lp[j]-lp[i])/2)
            value = B/A
            difference = abs(value-row['ratio'])
            assert difference < D('1e-6')
            assert abs(sum(rho)/D(len(rho))-1) < D('1e-14')
            output.append({'n':n,'retained_reported_ratio':str(row['ratio']),
                           'recomputed_ratio':str(value),
                           'absolute_difference':str(difference),
                           'agreement_with_reported_within_1e-9':difference < D('1e-9'),
                           'agreement_with_reported_within_1e-6':difference < D('1e-6'),
                           'positive_density':True,'mean_one_to_1e-14':True})
    return {'status':'passed_with_exploratory_precision_caveat','input_sha256':hashlib.sha256(data).hexdigest(),
            'method':str(precision)+'-digit Decimal directed-edge evaluation',
            'precision_caveat':'The n=3 displayed optimizer value differs from the saved test-pair quotient by approximately 7.27e-9. It is not a precision-certified value.',
            'results':output,'optimizer_rerun':False,
            'interval_or_global_optimum_certificate':False}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python3 check_exploration.py ORIGINAL_EXPLORATORY_RESULTS.json')
    result = run(sys.argv[1])
    confirmation = run(sys.argv[1], 120)
    for first, second in zip(result['results'], confirmation['results']):
        difference = abs(D(first['recomputed_ratio'])-D(second['recomputed_ratio']))
        assert difference < D('1e-70')
        first['80_vs_120_digit_difference'] = str(difference)
    result['higher_precision_stability_check'] = 'passed at absolute tolerance 1e-70'
    print(json.dumps(result,indent=2,sort_keys=True))
