#!/usr/bin/env python3
"""Full-sn-lattice divisor inventories for ROOT's later candidate.

Conditional on the candidate's g_+/- pole/zero divisors; standard library only.
Preserves the original independent report and does not import its verifier.
"""
from math import gcd
from pathlib import Path
from datetime import datetime,timezone
from collections import defaultdict
import json

counts=defaultdict(int)
classes=defaultdict(int)

def ck(name,value):
    assert value,name
    counts[name]+=1

def inventory(n,tau,focus,repeats):
    # Full sn lattice: 4K=4n grid units; delta=4tau; 2K=2n.
    # g_minus zeros K+-v => n+-2tau; g_plus zeros -K+-v.
    modulus=4*n
    poles=[0]*modulus;zeros=[0]*modulus
    zero_center=focus*n
    for j in range(repeats*n):
        poles[(-4*j*tau)%modulus]+=1
        poles[(2*n-4*j*tau)%modulus]+=1
        for sign in (-1,1):
            zeros[(zero_center+sign*2*tau-4*j*tau)%modulus]+=1
    return poles,zeros

for n in range(3,62):
    for tau in range(1,(n+1)//2):
        if gcd(tau,n)!=1:continue
        category='odd' if n%2 else ('two_mod_four' if n%4==2 else 'zero_mod_four')
        classes[category]+=1
        H={4*j*tau%(4*n) for j in range(n)}
        ck('full_translation_order',len(H)==n)
        if n%2:
            ck('odd_half_period_outside_subgroup',2*n not in H)
            for sign in (-1,1):
                # A zero z has 2z=2K+-delta modulo4K, which is outsideH.
                z=n+sign*2*tau
                ck('odd_doubled_zero_torsion_obstruction',(2*z)%(4*n) not in H)
        for focus in (-1,1):
            poles,zeros=inventory(n,tau,focus,1)
            divisor=[zeros[j]-poles[j] for j in range(4*n)]
            ck('candidate_constancy_parity_inventory',
               all(z==0 for z in divisor)==(n%4==2))
            ck('total_degree_balance',sum(poles)==sum(zeros)==2*n)
            if n%2:
                ck('odd_uncancelled_simple_poles',
                   sum(z>0 for z in poles)==2*n and
                   all(z in (0,1) for z in poles) and
                   all(zeros[j]==0 for j in range(4*n) if poles[j]))
                ck('odd_double_zero_orbit',sum(z>0 for z in zeros)==n and all(z in (0,2) for z in zeros))
            elif n%4==0:
                ck('zero_mod_four_uncancelled_double_poles',
                   sum(z>0 for z in poles)==n and
                   all(z in (0,2) for z in poles) and
                   all(zeros[j]==0 for j in range(4*n) if poles[j]))
            for r in (2,3,4):
                rp,rz=inventory(n,tau,focus,r)
                rd=[rz[j]-rp[j] for j in range(4*n)]
                ck('repeated_return_divisor_scales',rd==[r*z for z in divisor])
                ck('repeated_return_constancy_equivalence',
                   all(z==0 for z in rd)==all(z==0 for z in divisor))

result={'status':'SCOPED_PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),
        'exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),
        'primitive_rotation_cases_by_least_period_class':dict(classes),
        'repetition_factors':[2,3,4],'numerical_diagnostics':0,
        'limitations':'Finite inventories are conditional on full-sn g_+/- divisors. The independent torsion/identity-theorem/repetition proof read is in CLASSIFICATION_ADDENDUM.md. Exact period3 and4 geometric counterexamples are preserved in the earlier REVIEW.md.'}
out=Path(__file__).resolve().parent/'classification_results.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
