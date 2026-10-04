#!/usr/bin/env python3
"""Independent finite checks for the compact-plane theorem; not convergence proof."""
import json
import math
from fractions import Fraction as F
from pathlib import Path
import numpy as np


def compact_step(A, VT, u, v, w=None, x=None):
    U = np.column_stack([u] if w is None else [u, w])
    Q = np.column_stack([v] if x is None else [v, x])
    # Use precisely the allowed queries. B is never formed in the update.
    AQ = np.column_stack([A(q) for q in Q.T])
    GU = np.column_stack([VT(p) for p in U.T])
    C = U.T @ AQ - GU.T @ Q
    left, sigma, right = np.linalg.svd(C, full_matrices=False)
    p, q = left[:, 0], right[0]
    return U @ p, Q @ q, float(sigma[0]), C, AQ @ q, GU @ p


def rational_rank_one():
    r = [F(1), F(0), F(0)]
    u = v = [F(3, 5), F(4, 5), F(0)]
    w = x = [F(-4, 5), F(3, 5), F(0)]
    def dot(a, b): return sum(i*j for i, j in zip(a, b))
    def bilinear(a, b): return dot(a, r)*dot(r, b)
    a, b, c, d = bilinear(u, v), bilinear(w, v), bilinear(u, x), bilinear(w, x)
    assert a*d-b*c == 0
    # The hypothesis excluding singular-vector pairs is respected.
    bv = [v[0], F(0), F(0)]
    assert bv != [a*e for e in u]
    assert a > 0 and a*b+c*d != 0 and a*c+b*d != 0
    return {'entries': [str(i) for i in [a,b,c,d]],
            'determinant': '0', 'initial_pair_is_not_singular': True}


def boundary_checks():
    cases = [
        ('null_pair', np.zeros((3,3)), np.array([1.,0.,0.]), np.array([1.,0.,0.]), np.array([0.,1.,0.]), np.array([0.,1.,0.]), 0.),
        ('nonglobal_stationary_endpoint', np.diag([3.,1.,0.]), np.array([0.,1.,0.]), np.array([0.,1.,0.]), np.array([1.,0.,0.]), np.array([1.,0.,0.]), 3.),
        ('null_stationary_endpoint', np.diag([3.,1.,0.]), np.array([0.,0.,1.]), np.array([0.,0.,1.]), np.array([1.,0.,0.]), np.array([1.,0.,0.]), 3.),
        ('repeated_top', np.diag([3.,3.,1.]), np.array([0.,0.,1.]), np.array([0.,0.,1.]), np.array([1.,0.,0.]), np.array([1.,0.,0.]), 3.),
        ('scalar_negative', np.array([[-7.]]), np.array([1.]), np.array([1.]), None, None, 7.),
        ('one_output', np.array([[3.,4.]]), np.array([1.]), np.array([1.,0.]), None, np.array([0.,1.]), 5.),
        ('one_input', np.array([[3.],[4.]]), np.array([1.,0.]), np.array([1.]), np.array([0.,1.]), None, 5.),
        ('rank_one', np.diag([1.,0.,0.]), np.array([.6,.8,0.]), np.array([.6,.8,0.]), np.array([-.8,.6,0.]), np.array([-.8,.6,0.]), 1.),
    ]
    results=[]
    for label,B,u,v,w,x,target in cases:
        V=np.arange(B.size,dtype=float).reshape(B.shape)/7
        A=V+B
        un,vn,value,C,av,gu=compact_step(lambda q:A@q, lambda p:V.T@p, u,v,w,x)
        assert abs(value-target)<1e-12
        assert abs(np.linalg.norm(un)-1)<1e-12 and abs(np.linalg.norm(vn)-1)<1e-12
        assert abs(un@B@vn-value)<1e-12
        assert np.linalg.norm(av-A@vn)<1e-12 and np.linalg.norm(gu-V.T@un)<1e-12
        results.append({'case':label,'objective':value,'expected':target,'passed':True})
    return results


def projection_checks():
    rng=np.random.default_rng(8317)
    count=0; maximum_error=0.0
    # Includes both beta=0 branches, near beta=0, and target orthogonality.
    for n in [2,3,8,31]:
        a=np.zeros(n); a[0]=1
        z=np.zeros(n); z[1]=1
        for alpha in [-1.,-1+1e-12,0.,1-1e-12,1.]:
            beta=math.sqrt(max(0,1-alpha*alpha)); t=alpha*a+beta*z
            for _ in range(20):
                g=rng.standard_normal(n); g[0]=0; g/=np.linalg.norm(g)
                candidate=alpha*a+beta*g
                error=abs(np.linalg.norm(candidate-t)-beta*np.linalg.norm(g-z))
                assert abs(np.linalg.norm(candidate)-1)<1e-12 and error<1e-12
                maximum_error=max(maximum_error,error); count+=1
    return {'cases':count,'maximum_identity_error':maximum_error}


def probability_logic():
    p1,p2=F(1,2),F(1,3)
    both=p1*p2
    correct=1-both
    proposed=(1-p1)*(1-p2)
    assert correct>proposed
    # Four equiprobable cases supply a direct complement-of-product witness.
    event_states=[(a,b) for a in [False,True] for b in [False,True]]
    assert sum(not (a and b) for a,b in event_states)==3
    assert sum((not a) and (not b) for a,b in event_states)==1
    return {'both_success_probability':str(both),'correct_failure_bound':str(correct),
            'invalid_product_of_failures':str(proposed),'counterexample_passed':True}


def main():
    result={'status':'pass','exact_rank_one':rational_rank_one(),
            'compact_boundary_checks':boundary_checks(),
            'uniform_plane_identity_boundary_checks':projection_checks(),
            'probability_event_check':probability_logic(),
            'scope':'Exact rational counterexample plus finite floating-point and event-algebra checks. These do not establish almost-sure convergence or floating-point error guarantees.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
