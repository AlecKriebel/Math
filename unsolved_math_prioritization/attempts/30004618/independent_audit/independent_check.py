#!/usr/bin/env python3
"""Independent exact reconstruction; stdout only, Python standard library.

This does not import or execute the author's verifier or public GP supplement.
It verifies a specified coefficient model, not a Kodaira dimension.
"""
from fractions import Fraction as Q
from math import lcm
import json


def scaled_subtraction(divisor):
    """Raw (lambda, Dh, Dgamma/ell) -> subtraction normalized to lambda 12."""
    a, b, c = divisor
    return (-12*b/a, -12*c/a)


def reconstruct(g, prongs):
    # Compute kappa as sum m(m+2)/(m+1), including signed bottom orders.
    kappa = lambda signature: sum((Q(m*(m+2), m+1) for m in signature), Q(0))
    top_orders = [p-1 for p in prongs]
    bottom_orders = [2*g-2]+[-p-1 for p in prongs]
    k = kappa([2*g-2])
    kt, kb = kappa(top_orders), kappa(bottom_orders)
    assert kt+kb == k
    reciprocal = sum((Q(1,p) for p in prongs), Q(0))
    ell = lcm(*prongs)
    ntop = sum(prongs)+1
    nbottom = 2*g-ntop
    compensation = reciprocal/(len(prongs)+1)
    canonical = (-1-k/(2*g), k/(2*g)*(nbottom-compensation)-kb)
    # Corollary 7.7, for one top vertex.
    w = scaled_subtraction((12/k+Q(1,2), -1/k-Q(1,8), -kb/k))
    # Reconstruct NF from eq. (46), the pointed W class, and eq. (39).
    # All eight edges are nonseparating; no compact-type correction occurs.
    bn = (Q(6), -Q(g+1,g+3), -Q(g+1,g+3)*reciprocal)
    psi = (12/(k*(2*g-1)), -1/(k*(2*g-1)), kt/(k*(2*g-1)))
    classical_w = tuple(Q(g*(g+1),2)*x - (1 if j == 0 else 0)
                        for j,x in enumerate(psi))
    raw_nf = tuple(bn[j]+Q(12,(g+3)*(g+2))*classical_w[j] for j in range(3))
    nf = scaled_subtraction(raw_nf)
    hur_slope = Q(3*g*g+12*g-6,(g+8)*(3*g-1))
    hur = scaled_subtraction((Q(6), -hur_slope, -hur_slope*reciprocal))
    return dict(k=k,kt=kt,kb=kb,ell=ell,reciprocal=reciprocal,
                compensation=compensation,canonical=canonical,w=w,nf=nf,
                hur=hur,bn=scaled_subtraction(bn),top_orders=top_orders,
                bottom_orders=bottom_orders)


def interval(c, a, b):
    base = [c[j]+b[j] for j in range(2)]
    slope = [a[j]-b[j] for j in range(2)]
    assert slope[0]>0>slope[1]
    return (-base[0]/slope[0], -base[1]/slope[1], base, slope)


def bridge_min_energy(length, prong, sigma):
    # Dynamic program over every permitted nonnegative integer bridge height.
    # Downward as well as upward increments are allowed, avoiding monotonicity
    # assumptions. Interior heights satisfy 0 <= s_k <= k*prong.
    states = {0:0}
    for k in range(1,length+1):
        heights = [sigma] if k==length else range(k*prong+1)
        states = {height:min(energy+(height-old)**2
                            for old,energy in states.items())
                  for height in heights}
    return states[sigma]


def check():
    prongs = (9,1,1,1,1,1,1,1)
    x = reconstruct(12,prongs)
    assert x['k']==Q(528,23) and x['kt']==Q(80,9) and x['kb']==Q(2912,207)
    assert x['canonical']==(Q(-45,23),Q(-15142,1863))
    assert x['w']==(Q(89,45),Q(2912,405))
    assert x['nf']==(Q(311,179),Q(19472,1611))
    assert x['hur']==(Q(57,35),Q(1216,105))
    lo,hi,base,slope=interval(x['canonical'],x['w'],x['nf'])
    assert lo==Q(1845,2024)>hi==Q(300065,371128)
    dual=-slope[1]/slope[0]
    vertex_values=[x['canonical'][1]+p[1]+dual*(x['canonical'][0]+p[0])
                   for p in (x['w'],x['nf'],x['hur'])]
    assert dual==Q(2017,99)
    assert vertex_values[:2]==[Q(-940,1863)]*2
    assert vertex_values[2]-vertex_values[0]==Q(-286,105)
    count=0
    for i in range(101):
        for j in range(101-i):
            weights=(Q(i,100),Q(j,100),Q(100-i-j,100))
            residual=[x['canonical'][k]+sum((weights[q]*x[name][k]
                        for q,name in enumerate(('w','nf','hur'))),Q(0))
                      for k in range(2)]
            assert residual[1]+dual*residual[0]==Q(-940,1863)-Q(286,105)*weights[2]<0
            assert min(residual)<0
            count+=1
    assert count==5151
    gains=[]
    for sigma in range(10):
        energy=sum(bridge_min_energy(9//p,p,sigma) for p in prongs)
        gain=Q(16*sigma-energy,2)
        assert gain==Q(sigma*(9-sigma),2)
        gains.append(gain)
    assert max(gains)==Q(9,8)*x['kt']==10
    deficit=-(base[1]+slope[1]*lo)
    critical_r=x['compensation']-deficit/(x['k']/24)
    raw_w_improvement=deficit/(12*lo/(12/x['k']+Q(1,2)))
    assert critical_r==Q(26,99) and raw_w_improvement==Q(470,9963)
    normalized_w_improvement=deficit/lo
    assert normalized_w_improvement==Q(16544,29889)
    assert normalized_w_improvement==12/(12/x['k']+Q(1,2))*raw_w_improvement
    # Verify strictness at equality and one exact feasible perturbed example.
    assert base[1]+slope[1]*lo+x['k']/24*(x['compensation']-critical_r)==0
    r=Q(1,4); y=lo+Q(1,10000)
    assert base[0]+slope[0]*y>0
    assert base[1]+slope[1]*y+x['k']/24*(x['compensation']-r)>0
    z=reconstruct(13,(11,1,1,1,1,1,1,1))
    lower,upper,b,s=interval(z['canonical'],z['w'],z['bn'])
    assert (lower,upper)==(Q(1071,1375),Q(40409,51625)) and lower<upper
    midpoint=(lower+upper)/2
    positive=[b[k]+s[k]*midpoint for k in range(2)]
    assert min(positive)>0 and b[1]+s[1]*lower==Q(64,3025)
    # Necessary graph consistency checks, not a smoothing theorem.
    assert 5+(8-2+1)==12
    assert sum(x['top_orders'])==2*5-2
    assert sum(x['bottom_orders'])==-2
    assert 2*5-2+8>0 and -2+8+1>0
    return dict(status='PASS in the stated numerical model',simplex_controls=count,
        horizontal_lower=str(lo),vertical_upper=str(hi),dual_multiplier=str(dual),
        dual_values_at_vertices=[str(v) for v in vertex_values],
        twist_gains=[str(v) for v in gains],twist_optima=[4,5],
        compensation_strict_threshold=str(critical_r),
        compensation_decrease_strict_threshold=str(x['compensation']-critical_r),
        raw_weierstrass_coefficient_strict_improvement=str(raw_w_improvement),
        lambda12_weierstrass_coefficient_strict_improvement=str(normalized_w_improvement),
        genus13_control={'classes':'W_mid and 2 BN','lower':str(lower),'upper':str(upper),
                         'test_weight':str(midpoint),'positive_residuals':[str(v) for v in positive]},
        graph_checks={'arithmetic_genus':12,'top_signature':x['top_orders'],
                      'bottom_signature':x['bottom_orders'],'stable':True,
                      'spin_smoothing_proved_by_code':False},
        full_problem_solved=False,author_or_upstream_code_imported=False)


if __name__=='__main__':
    print(json.dumps(check(),indent=2,sort_keys=True))
