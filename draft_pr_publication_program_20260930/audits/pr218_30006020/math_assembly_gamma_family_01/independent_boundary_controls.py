#!/usr/bin/env python3
"""Exact original audit controls; no supplied verification code imported."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import json
from independent_exact_controls import beta_interval

OUT=Path(__file__).resolve().parent

def prefactor(g,k):
    return F(factorial(6*g-5-2*k)*2**(2*k),8*factorial(g-k)*factorial(3*g-3-k)*3**(g-k))

def controls():
    checks=0
    for g in range(2,41):
        for k in range(1,g):
            assert prefactor(g,k+1)/prefactor(g,k)==F(12*(g-k)*(3*g-3-k),(6*g-5-2*k)*(6*g-6-2*k))
            checks+=1
    p=beta_interval(2,2,F(1,10),F(1,5))
    assert p==F(19,250)
    assert 2*F(1,5)<1 # the corresponding two-coordinate joint probability is zero
    upper=3*F(2)*F(1,100)**2*F(1250,1249)
    assert upper==F(3,4996) and upper<F(1,1000)<F(1,4)
    return {'all_assertions_passed':True,'exact_prefactor_ratio_checks':checks,'g_range':[2,40],
            'normalized_two_mark_marginal':str(p),'independence_false_product':str(p*p),
            'actual_normalized_two_mark_joint':0,'q_fixed':str(F(1,100)),
            'microscopic_window_mean_strict_upper_bound':str(upper),
            'intermediate_claim_mean_lower_bound':str(F(1,4))}

if __name__=='__main__':
    result=controls();(OUT/'BOUNDARY_EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
