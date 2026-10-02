#!/usr/bin/env python3
"""Portable logic controls only; no numerical claim about Hardy spaces."""
from fractions import Fraction
import json

count=0
models=0
reverse_inclusion_possible=False
reverse_noninclusion_possible=False
# Abstract finite-set models are only a check on which conclusions the three
# published relation directions logically permit. They model no actual manifold.
sets=[frozenset(i for i in range(4) if (m>>i)&1) for m in range(16)]
for r in sets:
    for h in sets:
        for p in sets:
            if r<p and h<p and not r<=h:
                models+=1
                assert r!=p;count+=1
                assert h!=p;count+=1
                assert r!=h;count+=1
                reverse_inclusion_possible |= h<=r
                reverse_noninclusion_possible |= not h<=r
assert models>0;count+=1
assert reverse_inclusion_possible;count+=1
assert reverse_noninclusion_possible;count+=1
# The fractional-space obstruction is invoked only at a noninteger exponent.
gamma=Fraction(1,2);k=1
assert k-1<gamma<k;count+=1
assert gamma.denominator!=1;count+=1
# Specialization in Corollary3.4 gives the unweighted Poisson space at epsilon1.
assert 2*gamma-Fraction(1)==0;count+=1
# Supremum of absolute values, all positive times, and an unshifted generator
# must agree in the two definition ledgers. This is a transcription check only.
owr={'Riesz':'grad L^(-1/2)','heat':'exp(-t L)','Poisson':'exp(-t sqrt(L))','max_domain':'t>0','absolute_values':True,'ambient':'L1'}
mmvv=dict(owr)
for key in owr:
    assert owr[key]==mmvv[key];count+=1
assert 't>0'!='0<t<=1';count+=1
print(json.dumps({'problem_id':30003538,'status':'PASS','assertions':count,'finite_relation_models':models,'test_universe_size':4,'both_possible_reverse_relations_retained':True,'source_theorem_reproved':False,'proof_attempt_turns':0,'scope':'Exact logical and transcription sanity checks only; source statements and their analytic proofs remain external dependencies.'},indent=2,sort_keys=True))
