"""Exact arithmetic for the prior boundary example; no candidate-proof validation."""
from fractions import Fraction as Q
import json
from pathlib import Path

mu0=Q(1,2)
p00=p11=Q(3,4)
p01=p10=Q(1,4)
t0=mu0*p00
common=1+mu0
A=common+mu0*p00*(1+p01/(1-p11))
B=common+mu0*p01*(1+p10/(1-p00))
assert t0==Q(3,8)
assert A==Q(9,4) and B==Q(7,4)
assert A-B==Q(1,2)
result={'purpose':'Exact rational arithmetic for prior boundary comparison only',
        'rank':str(t0),'left_endpoint_mean':str(A),'right_endpoint_mean':str(B),
        'mean_gap':str(A-B),'checks_passed':4,
        'candidate_proof_revalidated':False,
        'probability_lemma':'Analytical proof in COMPARISON_DERIVATION.md, not numerically tested'}
Path(__file__).with_name('COMPARISON_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
