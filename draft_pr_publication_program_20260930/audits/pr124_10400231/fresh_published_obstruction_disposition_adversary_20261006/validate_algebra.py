"""Exact validation of the published-formula consequence; no proof-search turn.
Explicit failures survive Python optimization. No inputs are mutated.
"""
from __future__ import annotations
import json,sys,datetime,hashlib
from pathlib import Path

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def clean(a):
    return {i:c for i,c in a.items() if c}

def add(a,b):
    o=dict(a)
    for i,c in b.items():o[i]=o.get(i,0)+c
    return clean(o)

def shift(a,k,mult=1):
    return clean({i+k:mult*c for i,c in a.items()})

def mul(a,b):
    o={}
    for i,c in a.items():
        for j,d in b.items():o[i+j]=o.get(i+j,0)+c*d
    return clean(o)

def value(a):return sum(a.values())
def deriv_value(a):return sum(i*c for i,c in a.items())
def order_modp_at1(a,p):
    # Multiply by a Laurent unit, expand (1+u)^i by exact integer binomial.
    a=shift(a,-min(a,default=0));coeff=[]
    import math
    for j in range(max(a,default=0)+1):
        coeff.append(sum(c*math.comb(i,j) for i,c in a.items() if i>=j)%p)
    return next((j for j,c in enumerate(coeff) if c),None)

primes=[2,3,5,7,11,13,17,19,23,29,31]
D={1:-1,0:2,-1:-1};u2={2:1,1:-2,0:1}
checks=[];wrong_sign=0;wrong_shift=0
for p in primes:
    N=p**3;Delta={1:1,0:N-2,-1:1}
    require(value(Delta)==N and deriv_value(Delta)==0,'candidate value/derivative')
    require(add(shift(Delta,1),{1:-N})==u2,'universal exact family identity')
    require(order_modp_at1(Delta,p)==2,'modp exact family order')
    for k in range(-12,13):
        for sign in (-1,1):
            for a in (k,k+1,k+2):
                num=add(shift(Delta,a,sign),{k+1:-N})
                poles_cancel=value(num)==0 and deriv_value(num)==0
                require(poles_cancel==(sign==1 and a==k+1),'pole cancellation criterion')
                if sign==-1 and not poles_cancel:wrong_sign+=1
                if sign==1 and a!=k+1 and not poles_cancel:wrong_shift+=1
        num=add(shift(Delta,k+1),{k+1:-N})
        require(num==shift(u2,k),'quotient is exactly t^k')
        require(value({k:1})==1 and value({k:1})%p!=0,'augmentation contradiction')
        # In the printed symmetric representative formula: Q D-Nt^k=-t^k Delta.
        require(add(mul({k:1},D),{k:-N})==shift(Delta,k,-1),'printed 5.b sign and unit bridge')
    checks.append({'p':p,'candidate_order_mod_p':2,'torsion_p_rank':3,'book_required_order_min':3,'Euler_shifts':25})
# Formal invariant-factor count: descending divisibility makes p-divisible factors initial.
counts=[]
for nfinite in range(0,13):
    for rp in range(nfinite+1):
        omitted=max(rp-2,0)
        projected_product_factors=sum(1 for i in range(3,nfinite+1) if i<=rp)
        require(projected_product_factors==omitted,'invariant-factor ideal exponent')
        required=0 if rp==0 else 2+omitted
        require(required>=rp,'general claimed bound follows from printed formula')
        counts.append([nfinite,rp,projected_product_factors,required])
require(4*2**3==32 and 4**4==256,'prime2 III.4.3 cardinalities')
# Adversarial false interpretations: each is contradicted by the exact checks.
controls={
 'primitive_content_normalization_rejected':'Integral Z[t^±1] units are ±t^k; p^3 cannot be divided away.',
 'wrong_sign_choices_rejected':wrong_sign,
 'wrong_Euler_unit_shifts_rejected':wrong_shift,
 'cyclic_vs_elementary_torsion_substitution_rejected':'Z/p^3 has p-rank1; (Z/p)^3 has p-rank3.',
 'III4_3_prime2_without_free_Hmod4_rejected':{'actual_cardinality':32,'free_rank4_cardinality':256},
 'general_bound_strengthening_to_rp_plus1_not_inferred':'Old integral route supplies rp in rp>=3; no strengthening asserted or falsity of a stronger bound proved here.',
 'express_old_refutation_inference_rejected':'Printed necessary theorem plus consequence does not establish express earlier named application.'
}
result={'schema':'pr124-fresh-disposition-independent-algebra-validation/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'PASS':True,'optimization':sys.flags.optimize,'exact_integer_arithmetic':True,'checks':checks,'general_invariant_factor_counts':len(counts),'false_controls':controls,'universal_deduction_written_in_report':True,'computations_certify_source_or_topology':False,'new_central_proof_search_turns':0}
print(json.dumps(result,indent=2))
