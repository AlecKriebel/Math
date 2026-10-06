#!/usr/bin/env python3
"""Independent exact enclosure, not the author's Taylor implementation.
For y=x/2^96 in [0,1): (1-y)^2^96 <= exp(-x) <= (1+y)^(-2^96).
Square with outward integer rounding at scale 10^70. Only stdlib; no assert.
"""
from fractions import Fraction as Q
import json

BASE = 10**70
POWER = 96
N = 1 << POWER

def need(condition, message):
    if not condition:
        raise ValueError(message)

def down(x):
    return x.numerator * BASE // x.denominator

def up(x):
    return -((-x.numerator * BASE) // x.denominator)

def enclosure(x):
    need(0 <= x < N, 'exponential argument out of range')
    lower = down(1 - x / N)
    upper = up(Q(N) / (N + x))
    for _ in range(POWER):
        lower = lower * lower // BASE
        upper = -((-upper * upper) // BASE)
    need(0 <= lower <= upper <= BASE, 'invalid enclosure')
    return Q(lower, BASE), Q(upper, BASE)

def q_interval(x):
    low, high = enclosure(x)
    factor = 2 - x
    return (factor * low, factor * high) if factor >= 0 else (factor * high, factor * low)

def decimal_bracket(q, places=24):
    unit = 10**places
    low = q.numerator * unit // q.denominator
    return [str(Q(low,unit)), str(Q(low+1,unit))]

def run():
    # Algebraic checks do not substitute for the accompanying analytic argument.
    for n in range(4, 101):
        c=Q(n-2,4*(n-1))
        need(Q(1,6)-c==Q(4-n,12*(n-1)), 'first coefficient algebra')
        need(Q(n,4)-Q(n+2,4)==-Q(1,2), 'left conjugation exponent')
        need(Q(n-2,4)-Q(n,4)==-Q(1,2), 'right conjugation exponent')
        need(Q(n,2)/Q(n*(n-2),4)==Q(2,n-2), 'ground-state time threshold')
        if n>=5:
            need(Q((n-2)**2,4)-Q((n-1)*(n-3),4)==Q(1,4), 'cylinder spectral shift')
    # Let X=int |E|^2 and Z=int R^2, in units pi^2.
    # GB: -X/2 + Z/24 = 16; curvature difference X-Z/12 = -32.
    need(-2*Q(16)==-32, 'Gauss-Bonnet contraction')
    need(Q(-32,180*16)==-Q(1,90), 'normalized coefficient')
    need(Q(3,2)<Q(2*3**2,3), 'cylinder range overlap, pi>3')
    m=Q(999,1000); M=Q(1001,1000)
    need(Q(110,4)/M>2, 'omitted spectral tail sign')
    worst_upper=None; worst_index=None; least_width=None
    worst_lower=None
    degree_multiplicities=[]
    for ell in range(9):
        d=Q((2*ell+3)*(ell+1)*(ell+2),6)
        need(d.denominator==1, 'noninteger multiplicity')
        degree_multiplicities.append(int(d))
    for i in range(750):
        a=Q(1,4)+Q(i,1000); b=a+Q(1,1000)
        lower=Q(0); upper=Q(0)
        for ell,d in enumerate(degree_multiplicities):
            mu=(ell+1)*(ell+2)
            l1,u1=q_interval(a*mu/M)
            l2,u2=q_interval(b*mu/m)
            lower+=d*max(l1,l2)
            upper+=d*max(u1,u2)
        need(lower<=upper<-Q(3,500), 'interval upper bound failed: '+str(i))
        if worst_upper is None or upper>worst_upper:
            worst_upper=upper;worst_lower=lower;worst_index=i
    model_margin=Q(1,3)-84*Q(3,8)**6/(1-4*Q(3,8)**4)-Q(240,2**50)
    need(model_margin>Q(1,20), 'abstract model margin')
    need(Q(25,7)<4 and 4*Q(3,8)**4<1, 'abstract tail ratios')
    return {
      'problem_id':30001169,
      'status':'PASS',
      'mathematical_status':'partial_unresolved',
      'method':'Bernoulli-reciprocal exponential bounds; 96 outward-rounded squarings; denominator 10^70',
      'interval_count':750,
      'exponential_enclosures':13500,
      'block_multiplicities':degree_multiplicities,
      'first_omitted_degree':9,
      'worst_interval_index':worst_index,
      'worst_upper_rational':str(worst_upper),
      'worst_upper_decimal_bracket_as_rationals':decimal_bracket(worst_upper),
      'worst_interval_enclosure_width':str(worst_upper-worst_lower),
      'all_upper_bounds_strictly_below':'-3/500',
      'abstract_model_margin_rational':str(model_margin),
      'abstract_model_margin_strictly_above':'1/20',
      'derivative_small_time_n4':'-t/45 + O_W(t^2), using differentiated heat-parametrix remainders',
      'not_certified':'General all-time weighted monotonicity; geometry and analytic theorems are audited in AUDIT.md, not formalized by this program.'
    }

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
