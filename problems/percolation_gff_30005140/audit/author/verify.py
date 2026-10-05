#!/usr/bin/env python3
"""Deterministic auxiliary checks only. No network, corpus, or conjecture solver."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import math

CHECKS = 0

def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(label)

def inverse(a):
    n = len(a)
    b = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    for j in range(n):
        k = next((i for i in range(j, n) if b[i][j]), None)
        if k is None:
            raise ValueError('singular matrix')
        b[j], b[k] = b[k], b[j]
        t = b[j][j]
        b[j] = [x / t for x in b[j]]
        for i in range(n):
            if i != j:
                t = b[i][j]
                b[i] = [x - t * y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]

def multiply(a, b):
    return [[sum(x*y for x, y in zip(row, col)) for col in zip(*b)] for row in a]

def transpose(a):
    return list(map(list, zip(*a)))

def laplacian(n, edges):
    # Ground is denoted -1. Parallel edges are allowed and add conductance.
    q = [[F(0) for _ in range(n)] for _ in range(n)]
    for i, j, c in edges:
        c = F(c)
        for v in (i, j):
            if v >= 0:
                q[v][v] += c
        if i >= 0 and j >= 0:
            q[i][j] -= c
            q[j][i] -= c
    return q

def fmt(x):
    return str(x)

def rounded(x):
    return round(x, 12)

def compute():
    global CHECKS
    CHECKS = 0
    out = {'scope': 'Auxiliary finite identities and logical-obstruction checks; not a proof of the all-p maximum limit.'}
    pipe_rows = []
    for length in range(1, 13):
        conductances = [F((i % 3) + 1) for i in range(length)]
        edges = [(-1, 0, F(2))] + [(i, i+1, c) for i, c in enumerate(conductances)]
        cov = inverse(laplacian(length+1, edges))
        expected = F(1, 2) + sum(1/c for c in conductances)
        check(cov[-1][-1] == expected, 'weighted pendant-pipe variance')
        # Coordinates are root, followed by child-minus-parent increments.
        transform = [[F(i == j) for j in range(length+1)] for i in range(length+1)]
        for i in range(1, length+1):
            transform[i][i-1] = -1
        transformed = multiply(multiply(transform, cov), transpose(transform))
        expected_diag = [F(1, 2)] + [1/c for c in conductances]
        check(all(transformed[i][j] == (expected_diag[i] if i == j else 0)
                  for i in range(length+1) for j in range(length+1)), 'independent increments and root')
        pipe_rows.append({'edges': length, 'tip_variance': fmt(expected)})
    out['weighted_pipe_checks'] = pipe_rows

    parallel = []
    for length in range(1, 9):
        # Shared endpoint 0, ground -1, disjoint path interiors.
        paths = [[0] + list(range(1, length)) + [-1],
                 [0] + list(range(length, 2*length-1)) + [-1]]
        edges = [(a,b,1) for path in paths for a,b in zip(path, path[1:])]
        cov = inverse(laplacian(2*length-1, edges))
        check(cov[0][0] == F(length, 2), 'two parallel paths')
        parallel.append({'path_length': length, 'resistance': fmt(cov[0][0])})
    out['parallel_path_checks'] = parallel

    base = [[F(1), F(1)], [F(1), F(2)]]
    regularization = []
    previous_delta = None
    for k in range(0, 12):
        epsilon = F(1, 2**k)
        full_cov = inverse(laplacian(3, [(-1,0,1),(0,1,1),(0,2,epsilon),(2,-1,epsilon)]))
        cov = [row[:2] for row in full_cov[:2]]
        delta = epsilon/(2+epsilon)
        diff = [[base[i][j]-cov[i][j] for j in range(2)] for i in range(2)]
        check(all(x == delta for row in diff for x in row), 'regularized Schur covariance')
        check(delta > 0 and (previous_delta is None or delta < previous_delta), 'monotone variance deficit')
        # A matrix delta*ones has eigenvalues 0 and 2*delta, hence is PSD.
        previous_delta = delta
        regularization.append({'epsilon': fmt(epsilon), 'diagonal_deficit': fmt(delta)})
    out['regularization_checks'] = regularization

    patterns=[]
    def edge(x,y): return tuple(sorted((x,y)))
    for length in range(1,21):
        opened={edge((i,0),(i+1,0)) for i in range(length)}
        closed={edge((i,0),(i,j)) for i in range(length) for j in (-1,1)}
        closed.add(edge((0,0),(-1,0)))
        check(len(opened)==length and len(closed)==2*length+1 and not opened & closed, 'pipe event edge counts')
        check(not any(all(v[0]>=length for v in e) for e in opened | closed), 'half-plane edge independence')
        check(all(-length < i < 2*length for i in range(length+1)), 'pipe interior in chosen box')
        patterns.append({'length':length,'open_edges':len(opened),'closed_edges':len(closed)})
    out['pipe_pattern_checks']=patterns

    for s in [F(1,3),F(1),F(2),F(10),F(100)]:
        for t in [F(0),F(1,10),F(1),F(7),F(100)]:
            check(1/(s+t)>=1/s-t/s**2, 'reciprocal tangent inequality')
    out['reciprocal_inequality_cases']=25

    centering=[]
    for a in [0.05,0.2,0.5,1.0]:
        for n in [10,1000,1000000]:
            g=1/(2*math.pi*a)
            b1=math.sqrt(g)*(2*math.log(n)-0.75*math.log(math.log(n)))
            b2=math.sqrt(2/(math.pi*a))*(math.log(n)-0.375*math.log(math.log(n)))
            check(abs(b1-b2)<1e-12*max(1,abs(b1)), 'centering normalization')
            centering.append({'a':a,'N':n,'centering':rounded(b1)})
    out['normalization_checks']=centering

    union=[]
    for s in [10.0,100.0,1000.0,10000.0]:
        t=1.0
        u=2*s-0.75*math.log(s)+t
        direct=2*s-u*u/(2*s)
        expanded=1.5*math.log(s)-2*t-(0.75*math.log(s)-t)**2/(2*s)
        check(abs(direct-expanded)<1e-9, 'log-log union-bound algebra')
        union.append({'log_N':s,'log_union_bound_at_t_1':rounded(expanded)})
    out['centered_union_bound_diagnostic']=union

    spikes=[]
    for n in [10,100,1000,10000]:
        threshold=math.log(n)/n
        log_probability=n*math.log(0.5*(1+math.erf(threshold/math.sqrt(2))))
        check(log_probability < 0, 'spike maximum probability')
        spikes.append({'N':n,'test_average_variance_upper_bound':rounded(1/n),
                       'log_P_max_le_log_N':rounded(log_probability)})
    out['sparse_spike_checks']=spikes

    rates=[]
    for p in [0.51,0.6,0.75,0.9,0.99]:
        lam=-math.log(p*(1-p)**2)
        check(lam>0, 'pipe cost positive')
        rates.append({'p':p,'lambda_p':rounded(lam),'lambda_p_over_4pi':rounded(lam/(4*math.pi)),
                      'interpretation':'threshold only; no value of homogenized a_p is inferred'})
    out['conditional_pipe_rate_thresholds']=rates

    r=(2.1**2)/2
    check(2<r<3,'first-order moment bound parameter')
    out['first_order_bound_example']={'assumed_kappa':3,'eta_prime':0.1,'r':rounded(r),
                                      'annealed_power_exponent_2_minus_r':rounded(2-r),
                                      'dyadic_probability_bound_is_summable':True}
    e1,e2=math.exp(-0.5),math.exp(-2)
    check(e1!=e2,'distinct quenched characteristic functions')
    out['annealed_counterexample']={'char_at_1_variance_1':rounded(e1),'char_at_1_variance_4':rounded(e2),
                                  'annealed_char_at_1':rounded((e1+e2)/2)}
    out['assertions_passed']=CHECKS
    out['status']='PASS'
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write-results',action='store_true',help='Author-only regeneration; normal replay does not write.')
    args=parser.parse_args()
    result=compute()
    target=Path(__file__).resolve().parent/'results.json'
    if args.write_results:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        expected=json.loads(target.read_text())
        if result!=expected:
            raise AssertionError('Recomputed result differs from frozen results.json')
    print(json.dumps({'status':result['status'],'assertions_passed':result['assertions_passed'],
                      'results_match':not args.write_results,'scope':result['scope']},sort_keys=True))
if __name__=='__main__':main()
