#!/usr/bin/env python3
"""Exact Laurent arithmetic for the old-theorem corollary; no topology claimed."""
import json
from datetime import datetime, timezone
from pathlib import Path

def add(a,b):
    out=dict(a)
    for e,c in b.items():
        out[e]=out.get(e,0)+c
    return {e:c for e,c in out.items() if c}

def shift(a,k):
    return {e+k:c for e,c in a.items() if c}

def scale(a,k):
    return {e:c*k for e,c in a.items() if c*k}

def val1(a):
    return sum(a.values())

def deriv1(a):
    return sum(e*c for e,c in a.items())

primes=[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
checks=[]
for p in primes:
    N=p**3
    delta={-1:1,0:N-2,1:1}
    assert val1(delta)==N and deriv1(delta)==0
    assert delta=={-e:c for e,c in delta.items()}
    numerator=add(shift(delta,1),{1:-N})
    assert numerator=={0:1,1:-2,2:1}
    reduced_tdelta={e:c%p for e,c in shift(delta,1).items() if c%p}
    reduced_square={e:c%p for e,c in {0:1,1:-2,2:1}.items() if c%p}
    assert reduced_tdelta==reduced_square and reduced_square[2]==1
    for k in range(-10,11):
        # A Laurent polynomial numerator is divisible by (t-1)^2 iff
        # evaluation and formal derivative at 1 vanish. For nonzero N,
        # epsilon*N-N=0 forces epsilon=1; then N*(a-k-1)=0
        # forces a=k+1. Verify these exact values and the quotient identity.
        a=k+1
        num=add(shift(delta,a),{k+1:-N})
        assert val1(num)==0 and deriv1(num)==0
        assert num==shift({0:1,1:-2,2:1},k)
        quotient={k:0}
        assert val1(quotient)==1 and val1(quotient)%p==1
        # Negative sign always leaves an uncancelled pole.
        negative=add(scale(shift(delta,a),-1),{k+1:-N})
        assert val1(negative)==-2*N
        # The two adjacent monomial shifts leave a simple pole.
        for wrong_a in [a-1,a+1]:
            wrong=add(shift(delta,wrong_a),{k+1:-N})
            assert deriv1(wrong)==(wrong_a-k-1)*N!=0
    checks.append({"p":p,"torsion_order":N,"delta_augmentation":N,"delta_derivative_at_1":0,"forced_quotient_augmentation":1,"contradicts_divisibility_by_p":True})

result={
 "schema":"pr124-turaev-old-theorem-algebra-check/v1",
 "UTC":datetime.now(timezone.utc).isoformat(),
 "status":"PASS",
 "exact_arithmetic":True,
 "topological_or_source_claim_checked_by_script":False,
 "universal_identity":"t*(t+(N-2)+t^(-1))-N*t=(t-1)^2 for every integer N",
 "universal_pole_equations":["epsilon*N-N=0","epsilon*a*N-(k+1)*N=0"],
 "universal_deduction_for_nonzero_N":"epsilon=1, a=k+1, quotient=t^k, augmentation=1",
 "all_prime_theorem_corollary_relies_on_written_proof":True,
 "tested_primes":len(primes),
 "tested_integer_Euler_shifts_per_prime":21,
 "checks":checks
}
Path(__file__).with_name("ALGEBRA_CHECK.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
