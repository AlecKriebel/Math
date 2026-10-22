#!/usr/bin/env python3
"""Exact rational controls for the finite-cutoff Nyman--Beurling obstruction.
No source downloads or external dependencies; not a solver for the open target.
"""
from fractions import Fraction as Q
from math import isqrt
import json
from pathlib import Path


def mobius(n):
    sign, p = 1, 2
    while p*p <= n:
        if n % p == 0:
            n //= p
            sign = -sign
            if n % p == 0:
                return 0
            while n % p == 0:
                n //= p
        p += 1
    return -sign if n > 1 else sign


def floorq(x):
    return x.numerator // x.denominator


def witness(q, eps):
    """h=A*t on (0,1); h=t^2*k on piecewise-constant k intervals >=1."""
    q, eps = Q(q), Q(eps)
    assert q > 1 and 0 < eps < min(1, q-1)
    m = floorq(q+eps)
    events = {}
    A = Q(0)
    for n in range(1, m+1):
        mu = mobius(n)
        if not mu:
            continue
        for left, right, sign in [(q-eps,q,-1),(q,q+eps,1)]:
            lo, hi = max(Q(1),left/n), right/n
            if lo >= hi:
                continue
            # -mu*n*psi(n*t), the coefficient of t^2 in h.
            k = -mu*n*sign/eps
            events[lo] = events.get(lo,Q(0)) + k
            events[hi] = events.get(hi,Q(0)) - k
            # A = integral psi(t)*t*sum_{n<=t} mu(n)/n dt.
            A += mu*sign*((n*hi)**2-(n*lo)**2)/(2*n*eps)
    points = sorted(events)
    k, intervals = Q(0), []
    for i, lo in enumerate(points[:-1]):
        k += events[lo]
        hi = points[i+1]
        if k:
            intervals.append((lo,hi,k))
    norm2 = A*A + sum((k*k*(hi**3-lo**3)/3 for lo,hi,k in intervals),Q(0))
    chi = sum((k*(hi-lo) for lo,hi,k in intervals),Q(0))
    return A,intervals,norm2,chi


def pairing_e(A, intervals, alpha):
    alpha = Q(alpha)
    assert alpha >= 1
    ans = A/alpha
    for lo, hi, k in intervals:
        cuts = {lo,hi}
        for n in range(floorq(lo/alpha)+1,floorq(hi/alpha)+1):
            z = n*alpha
            if lo < z < hi:
                cuts.add(z)
        points = sorted(cuts)
        for x,y in zip(points,points[1:]):
            n = floorq((x+y)/(2*alpha))
            ans += k*((y*y-x*x)/(2*alpha)-n*(y-x))
    return ans


def rat(x):
    return str(x)


def run():
    rows = []
    # Every cutoff below q-eps is annihilated, for any real generator parameter.
    # Rational grid checks are supplemental; the proof establishes the continuum.
    for q in [2,3,5,7,11]:
        eps = Q(1,4)
        A,pieces,norm2,chi = witness(q,eps)
        assert chi == -mobius(q) == 1
        test = [Q(1)+Q(j,32) for j in range(int(32*(Q(q)-eps-Q(1)))+1)]
        assert all(pairing_e(A,pieces,a)==0 for a in test)
        # At the center, cumulative coefficients of e_q make a unit jump.
        assert pairing_e(A,pieces,Q(q)) == 1
        assert norm2 > 0
        rows.append({"squarefree_center":q,"epsilon":rat(eps),
                     "valid_cutoffs":"1 <= lambda <= "+rat(Q(q)-eps),
                     "h_chi":rat(chi),"h_e_center":rat(pairing_e(A,pieces,Q(q))),
                     "h_norm_squared":rat(norm2),
                     "lower_bound_D_squared":rat(1/norm2),
                     "rational_generator_tests":len(test),
                     "A":rat(A),"piece_count":len(pieces)})
    # The same separation mechanism handles a noninteger new generator.
    q,eps = Q(7,3),Q(1,10)
    A,pieces,norm2,chi = witness(q,eps)
    assert pairing_e(A,pieces,q)==1
    assert pairing_e(A,pieces,Q(2))==0
    assert chi==0  # No integer jump in this interval: not a distance lower bound.
    # Negative controls: nested proper subspaces need not improve a distance.
    # In R^3, x=(0,0,1), E=span(e1), F=span(e1,e2): both distances are 1.
    plateau = {"E_dimension":1,"F_dimension":2,"distance_to_E_squared":1,
               "distance_to_F_squared":1,"strict_space_inclusion":True}
    # Continuous nonincreasing approximants may have a right-discontinuous infimum.
    def d(n,x): return Q(1) if x<=2 else max(Q(0),Q(1)-n*(x-2))
    assert all(d(n,Q(2))==1 for n in range(1,10))
    assert d(100,Q(201,100))==0
    return {"status":"passed","arithmetic":"exact rational",
            "claim_scope":"partial controls; neither right continuity nor strict decrease proved",
            "prime_witnesses":rows,
            "noninteger_separation":{"center":rat(q),"epsilon":rat(eps),
                "h_e_center":rat(pairing_e(A,pieces,q)),"h_chi":rat(chi)},
            "plateau_negative_control":plateau,
            "continuous_infimum_negative_control":"d_n(x)=max(0,1-n*max(0,x-2)); inf is 1 at x<=2 and 0 at x>2"}

if __name__=='__main__':
    result=run()
    output=Path(__file__).with_name('control_results.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
