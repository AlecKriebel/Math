#!/usr/bin/env python3
"""Author validations for the many-destination candidate. Not independent review."""
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

SEED = 970000202
rng = np.random.default_rng(SEED)


def physical_matrix(k):
    assert k >= 1 and k & (k-1) == 0
    n = 2*k
    N = 2*n-1
    paths = []
    for v0 in range(n-1, N):
        path = []
        v = v0
        while v:
            path.append(v-1)
            v = (v-1)//2
        paths.append(path)
    A = np.zeros((N-1,k*k))
    for i,j in itertools.product(range(k),repeat=2):
        A[paths[i]+paths[k+j], i*k+j] = 1
    caps = 2*A.sum(axis=1)
    assert np.all(A.sum(axis=0)==2*(int(math.log2(k))+1))
    return A,caps


def terminal_matrix(k):
    A = np.zeros((2*k,k*k))
    for i,j in itertools.product(range(k),repeat=2):
        A[i,i*k+j] = A[k+j,i*k+j] = 1
    return A,np.full(2*k,2*k,dtype=float)


def solve(X,t,physical=False):
    k = X.shape[0]
    A,caps = physical_matrix(k) if physical else terminal_matrix(k)
    d = (1+(t-1)*X).ravel()
    sol = linprog(-np.ones(k*k),A_ub=A,b_ub=caps,
                  bounds=list(zip(np.zeros(k*k),d)),method='highs')
    assert sol.success,sol.message
    return -float(sol.fun),sol.x,A,caps,d


def cut_lines(X):
    k = X.shape[0]
    masks = np.array([[(s>>i)&1 for i in range(k)] for s in range(2**k)],dtype=float)
    a = masks.sum(axis=1)[:,None]
    b = masks.sum(axis=1)[None,:]
    intercept = 2*k*(k-a+b)+a*(k-b)
    slope = masks@X@(1-masks).T
    return intercept,slope


def cut_value_derivative(X,t):
    intercept,slope = cut_lines(X)
    values = intercept+(t-1)*slope
    value = values.min()
    active = abs(values-value)<1e-8
    return float(value),float(slope[active].min())


def all_optimizer_load_range(A,caps,d,F):
    v = len(d)
    lo=[]
    hi=[]
    for row in A:
        bounds=list(zip(np.zeros(v),d))
        args=dict(A_ub=A,b_ub=caps,A_eq=np.ones((1,v)),b_eq=[F],bounds=bounds,method='highs')
        l=linprog(row,**args)
        u=linprog(-row,**args)
        assert l.success and u.success
        lo.append(l.fun)
        hi.append(-u.fun)
    return np.array(lo),np.array(hi)


def I(a):
    return a-1-math.log(a)


def main():
    checks=[]
    lp_cases=0
    max_reduction_error=0.
    max_cut_error=0.
    max_derivative_error=0.
    phase_tests={'full_demand':0,'full_capacity':0}
    for k in (1,2,4,8,16):
        for repetition in range(5):
            X=rng.exponential(size=(k,k))
            for t in (1.,1.5,1.9,2.,2.1,2.5,5.):
                F,y,A,caps,d=solve(X,t,True)
                F2,*_=solve(X,t,False)
                max_reduction_error=max(max_reduction_error,abs(F-F2))
                assert abs(F-F2)<1e-7
                loads=A@y
                if abs(F-d.sum())<1e-7 and max((d.reshape(k,k)).sum(axis=0).max(),(d.reshape(k,k)).sum(axis=1).max())<2*k-1e-7:
                    assert np.all(loads<caps-1e-7)
                    phase_tests['full_demand']+=1
                if abs(F-2*k*k)<1e-7:
                    assert np.max(abs(loads-caps))<1e-7
                    phase_tests['full_capacity']+=1
                if k<=4:
                    cf,derivative=cut_value_derivative(X,t)
                    max_cut_error=max(max_cut_error,abs(cf-F))
                    assert abs(cf-F)<1e-7
                    dt=1e-6
                    cf_next,_=cut_value_derivative(X,t+dt)
                    err=abs((cf_next-cf)/dt-derivative)
                    max_derivative_error=max(max_derivative_error,err)
                    assert err<1e-6
                lp_cases+=1
    checks.append({'name':'physical tree LP equals bipartite LP and explicit cuts',
                   'cases':lp_cases,'max_reduction_error':max_reduction_error,
                   'max_cut_error':max_cut_error,'max_derivative_error':max_derivative_error,
                   'phase_cases':phase_tests,'pass':True})

    # Exact synchronized ties verify right-derivative convention.
    for k in (1,2,4):
        X=np.ones((k,k))
        for t in (1.,1.5,2.,3.):
            F,derivative=cut_value_derivative(X,t)
            assert abs(F-k*k*min(t,2))<1e-9
            assert abs(derivative-(k*k if t<2 else 0))<1e-9
    checks.append({'name':'exact tie and right derivative controls','pass':True})

    # Check load invariance across the ENTIRE optimizer face in the proved phases.
    load_range_errors=[]
    for k in (2,4):
        X=rng.uniform(.5,1.5,size=(k,k))
        for t in (1.1,5.):
            F,y,A,caps,d=solve(X,t,True)
            lo,hi=all_optimizer_load_range(A,caps,d,F)
            err=float(np.max(abs(hi-lo)))
            load_range_errors.append(err)
            assert err<1e-7
            if t<2:
                assert np.all(hi<caps-1e-7)
            else:
                assert np.max(abs(lo-caps))<1e-7
    checks.append({'name':'all-optimizer physical edge load ranges',
                   'max_range_width':max(load_range_errors),'pass':True})

    # A necessary adversarial control: row/column totals alone do not ensure full flow.
    U=np.array([[3.,3.,1.1,1.1], [3.,3.,1.1,1.1],
                [3.,3.,1.1,1.1], [1.1,1.1,5.,5.]])
    assert np.all(U.sum(axis=0)>8) and np.all(U.sum(axis=1)>8)
    F,*_=solve(U-1,2.)
    cf,_=cut_value_derivative(U-1,2.)
    assert abs(F-30.6)<1e-8 and abs(cf-F)<1e-8 and F<32
    checks.append({'name':'all-cuts necessity adversarial example',
                   'row_totals':U.sum(axis=1).tolist(),
                   'column_totals':U.sum(axis=0).tolist(),
                   'max_flow':F,'full_capacity':32,
                   'violating_A':[0,1,2],'violating_B':[0,1],'pass':True})

    # Exhaustive cut-size enumeration and combinatorial counting controls.
    for k in range(2,21):
        count=0
        small_q_counts={q:0 for q in range(1,k//2+1)}
        for a in range(k+1):
            for d in range(k+1):
                if a+d<=k:
                    continue
                multiplicity=math.comb(k,a)*math.comb(k,d)
                count+=multiplicity
                q=min(a,d)
                ell=k-max(a,d)
                assert 0<=ell<q
                assert a*d==q*(k-ell)
                assert a*d>=k*(a+d-k)
                if q<=k//2:
                    small_q_counts[q]+=multiplicity
                    assert a*d>=q*k/2
                else:
                    assert a*d>k*k/4
        assert count==(4**k-math.comb(2*k,k))//2
        for q,count_q in small_q_counts.items():
            assert count_q<=2*q*k**(2*q)
    for delta in (.0001,.001,.01,.1,.3,.7,.99):
        assert I(1/(1-delta))+1e-14>=delta*delta/2
        assert I(1/(1+delta))+1e-14>=delta*delta/8
    checks.append({'name':'all positive cuts counted; rectangle and tail bounds','pass':True})

    bounds=[]
    for k in (512,1024,4096,65536,1048576):
        delta=8*math.sqrt(math.log(k)/k)
        assert delta<1
        eps=2*k**(-31)+2*k**(-2)/(1-k**(-2))**2+math.exp(k*math.log(4/k**2))
        bounds.append({'k':k,'delta':delta,'window_width':2*delta,'failure_bound':eps})

    out={'seed':SEED,'all_assertions_passed':True,'checks':checks,
         'explicit_large_k_bounds':bounds,
         'limitations':'Author checks only; no source-fidelity, novelty, or independent-review verdict.'}
    Path(__file__).with_name('CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
