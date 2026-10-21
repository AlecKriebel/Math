#!/usr/bin/env python3
"""Reproducible author checks, not a replacement for independent proof review."""
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import linprog
from scipy.special import gammainc, gammaln
from scipy.stats import norm

SEED = 9700002
rng = np.random.default_rng(SEED)


def tree_matrix(h):
    n = 2**h
    N = 2*n-1
    A = np.zeros((N-1, n))
    for i, v0 in enumerate(range(n-1, N)):
        v = v0
        while v:
            A[v-1, i] = 1
            v = (v-1)//2
    return A


def graph_component_size(A, y):
    N = A.shape[0]+1
    caps = 2*A.sum(axis=1)
    spare = caps-A@y > 1e-8
    adj = [[] for _ in range(N)]
    for child in range(1, N):
        if spare[child-1]:
            parent = (child-1)//2
            adj[parent].append(child)
            adj[child].append(parent)
    seen = set()
    sizes = []
    for v in range(N):
        if v in seen:
            continue
        stack = [v]
        seen.add(v)
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            for w in adj[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        sizes.append(size)
    return max(sizes), sorted(sizes, reverse=True)


def ancestor_count(active):
    a = np.asarray(active, dtype=bool)
    count = int(a.sum())
    while len(a)>2:
        a = a.reshape(-1, 2).any(axis=1)
        count += int(a.sum())
    return count+1  # Root remains a vertex even if no leaf is active.


def p_R(m, t):
    if t == 1:
        return 1., 1.
    z = m/(t-1)
    return float(gammainc(m, z)), float(gammainc(m+1, z))


def H(m, t):
    p, R = p_R(m, t)
    return 2-p+(t-1)*R


def G(p, terms=55):
    if p == 0:
        return 0.
    if p == 1:
        return 1.
    return sum(2.**(-j-1)*(-math.expm1(2.**j*math.log1p(-p)))
               for j in range(terms))


def expected_component(h, p):
    n = 2**h
    if p == 1:
        return 2*n-1
    if p == 0:
        return 1.
    return 1+sum(2.**(h-j)*(-math.expm1(2.**j*math.log1p(-p)))
                 for j in range(h))


def main():
    checks = []
    max_lp_error = 0.
    max_uniqueness_error = 0.
    lp_cases = 0
    for h in range(1, 6):
        A = tree_matrix(h)
        caps = 2*A.sum(axis=1)
        n = 2**h
        for m in (1, 3, 10):
            W = rng.gamma(m, 1/m, size=n)
            for t in (1., 1.2, 2., 3., 10.):
                demand = 1+(t-1)*W
                expected = np.minimum(demand, 2)
                sol = linprog(-np.ones(n), A_ub=A, b_ub=caps,
                              bounds=list(zip(np.zeros(n), demand)), method='highs')
                assert sol.success, sol.message
                err = abs(-sol.fun-float(expected.sum()))
                max_lp_error = max(max_lp_error, err)
                assert err < 1e-7
                assert np.max(np.abs(sol.x-expected)) < 1e-7
                size, sizes = graph_component_size(A, expected)
                assert size == ancestor_count(demand<2)
                assert all(x == 1 for x in sizes[1:])
                lp_cases += 1
                if h<=3:
                    for k in range(n):
                        for sign in (-1, 1):
                            objective = np.zeros(n)
                            objective[k] = sign
                            alt = linprog(objective, A_ub=A, b_ub=caps,
                                          A_eq=np.ones((1, n)),
                                          b_eq=[expected.sum()],
                                          bounds=list(zip(np.zeros(n), demand)),
                                          method='highs')
                            assert alt.success, alt.message
                            e = abs(alt.x[k]-expected[k])
                            max_uniqueness_error = max(max_uniqueness_error, e)
                            assert e<1e-7
    checks.append({'name':'full path LP and all-optimum coordinate checks',
                   'cases':lp_cases, 'max_objective_error':max_lp_error,
                   'max_coordinate_error':max_uniqueness_error, 'pass':True})

    # Exact tie, all-saturated, all-unsaturated, and heterogeneous controls.
    A = tree_matrix(3)
    for W in (np.ones(8), np.array([.1,.2,.5,1,1,2,3,5]), np.zeros(8)):
        for t in (1.,2.,3.):
            d = 1+(t-1)*W
            y = np.minimum(d, 2)
            size, sizes = graph_component_size(A, y)
            assert size == ancestor_count(d<2)
            assert all(x==1 for x in sizes[1:])
    checks.append({'name':'ties and degenerate graph controls','pass':True})

    max_integral_error = 0.
    max_derivative_error = 0.
    for m in (1,2,5,20):
        for t in (1.2,1.5,2.,3.,5.):
            a = 1/(t-1)
            p, R = p_R(m,t)
            def density(w):
                if w == 0:
                    return float(m) if m==1 else 0.
                return math.exp(m*math.log(m)+(m-1)*math.log(w)-m*w-gammaln(m))
            num_p = quad(density,0,a,epsabs=1e-11)[0]
            num_R = quad(lambda w:w*density(w),0,a,epsabs=1e-11)[0]
            max_integral_error = max(max_integral_error, abs(p-num_p), abs(R-num_R))
            dt = 1e-5
            numerical_derivative = (H(m,t+dt)-H(m,t-dt))/(2*dt)
            max_derivative_error = max(max_derivative_error, abs(R-numerical_derivative))
    assert max_integral_error<1e-8
    assert max_derivative_error<1e-7
    checks.append({'name':'Gamma integral and expected-throughput derivative',
                   'max_integral_error':max_integral_error,
                   'max_derivative_error':max_derivative_error,'pass':True})

    for h in range(1,18):
        n = 2**h
        for p in (0.,1e-6,.001,.1,.5,.9,1.):
            error = abs(expected_component(h,p)/(2*n-1)-G(p))
            assert error <= 4/n+1e-14
    checks.append({'name':'finite component expectation versus limiting series',
                   'pass':True,'G_half':G(.5)})

    fixed_noise = []
    for t in (2.,3.,10.,100.):
        p,R = p_R(1,t)
        fixed_noise.append({'m':1,'t':t,'p':p,'R':R,'giant_density':G(p)})
        assert p>0 and G(p)>0

    windows = []
    for m in (100,1000,10000):
        for x in (-2.,-1.,0.,1.,2.):
            t = 2+x/math.sqrt(m)
            p,R = p_R(m,t)
            target = float(norm.cdf(-x))
            windows.append({'m':m,'x':x,'R':R,'normal_target':target,
                            'giant':G(p),'giant_target':G(target)})

    monte_carlo = []
    h = 13
    n = 2**h
    for m in (1,h):
        W = rng.gamma(m,1/m,size=n)
        for t in (1.5,2.,2.5,3.,10.):
            p,R = p_R(m,t)
            r = float(W[(t-1)*W<1].sum()/W.sum())
            c = ancestor_count((t-1)*W<1)/(2*n-1)
            monte_carlo.append({'h':h,'m':m,'t':t,'empirical_r':r,
                                'analytic_R':R,'empirical_giant':c,'analytic_G':G(p)})

    out = {'seed':SEED,'all_assertions_passed':True,'checks':checks,
           'fixed_noise_negative_control':fixed_noise,
           'critical_window_profiles':windows,'monte_carlo_diagnostics':monte_carlo,
           'interpretation':'Author numerical checks only. They do not certify novelty or primary-target adequacy.'}
    Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'all_assertions_passed':True,'checks':checks,
                      'fixed_noise_negative_control':fixed_noise},indent=2))


if __name__ == '__main__':
    main()
