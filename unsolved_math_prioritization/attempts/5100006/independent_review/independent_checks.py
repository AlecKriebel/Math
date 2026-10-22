#!/usr/bin/env python3
"""Independent exact divisor/positivity controls for k114, standard library only."""
from fractions import Fraction as F
from math import gcd
from pathlib import Path
from hashlib import sha256
import json
counts={}
def ck(name,ok):
    assert ok,name
    counts[name]=counts.get(name,0)+1
primitive_cases=0
# 2K=1. Use a denominator-2m integer grid rather than the submitted
# Fraction/Counter zero-orbit construction.
for m in range(3,62):
    for tau in range(1,m):
        if gcd(tau,2*m)!=1:continue
        primitive_cases+=1
        modulus=2*m
        # delta=tau/m; poles at -j*delta have index -2*j*tau.
        pole_positions=[(-2*j*tau)%modulus for j in range(m)]
        ck('order_of_translation',len(set(pole_positions))==m)
        ck('primitive_full_billiard_order',(2*m)//gcd(tau,2*m)==2*m)
        ck('half_orbit_antipodal',tau%2==1)
        divisor=[0]*modulus
        for z in pole_positions:divisor[z]-=2
        # K+-v have indices m+-tau.
        for j in range(m):
            divisor[(m+tau-2*j*tau)%modulus]+=1
            divisor[(m-tau-2*j*tau)%modulus]+=1
        if m%2:
            ck('full_divisor_cancellation',all(x==0 for x in divisor))
            for sign in (-1,1):
                h=(m+sign)//2
                ck('explicit_zero_shift_integer',(m+sign*tau-2*h*tau)%modulus==0)
            # The two zeros are distinct; no one zero is mistakenly counted twice.
            ck('distinct_zero_classes',(m+tau)%modulus!=(m-tau)%modulus)
            ck('two_distinct_cancelling_factors',((m+1)//2)%m!=((m-1)//2)%m)
        else:
            ck('excluded_even_m_nonzero_divisor',any(x!=0 for x in divisor))
            ck('excluded_even_m_zero_pole_cosets',all(divisor[z]==-2 for z in pole_positions))
# A nonprimitive N=6,tau=2 control: half-displacement is not antipodal.
ck('repeated_odd_not_reclassified',(3*F(2,3))%2==0)
# Independent rational checks of axes, ordinary-distance pairing, and the
# squared derivative at each proposed complex zero.
for alpha2,c2 in [(F(5),F(1)),(F(7,3),F(2,5)),(F(13,7),F(5,7))]:
    for t in [F(1,9),F(2,7),F(3,5),F(7,8)]:
        k2=c2/alpha2;beta2=alpha2-c2;cn2=1-t;dn2=1-k2*t
        a2=alpha2*dn2/cn2;b2=beta2/cn2;lam=a2-alpha2
        ck('valid_modulus_and_shift',0<k2<1 and 0<cn2<1 and dn2>0)
        ck('confocal_axes',a2-b2==c2 and a2-alpha2==b2-beta2)
        ck('strict_nested',0<lam<b2 and a2>alpha2 and b2>beta2)
        proposed_sn2=dn2/(k2*cn2)
        ck('complex_zero_relation',a2-c2*proposed_sn2==0)
        derivative_squared=4*c2*c2*proposed_sn2*(1-proposed_sn2)*(1-k2*proposed_sn2)
        ck('zeros_are_simple',derivative_squared==4*a2*b2*lam/alpha2>0)
        for real_sn2 in [F(0),F(1,7),F(3,4),F(1)]:
            ck('real_F_positive',a2-c2*real_sn2>=b2>0)
# The ordinary distance formula, checked after eliminating y^2 via the
# ellipse equation with rational a,c,x. All positive square roots have fixed sign.
for a,c in [(F(2),F(1)),(F(5,2),F(3,2)),(F(7,3),F(1,2))]:
    b2=a*a-c*c
    for r in [F(-1),F(-2,3),F(0),F(3,5),F(1)]:
        x=a*r;y2=b2*(1-r*r)
        for sign in (-1,1):
            distance=a-sign*c*x/a
            ck('ordinary_distance_square',(x-sign*c)**2+y2==distance**2)
            ck('ordinary_distance_positive',distance>0)
        ck('antipodal_pair_product',(a-c*r)*(a+c*r)==a*a-c*c*r*r)
# Exact N6 controls from squared x coordinates, independent of Jacobi numerics.
H_x2=[F(4),F(16,9),F(16,9)]
V_x2=[F(0),F(32,9),F(32,9)]
def paired_product(xs):
    out=F(1)
    for x2 in xs:out*=4-F(3,4)*x2
    return out
ck('six_period_H_focal_product',paired_product(H_x2)==F(64,9))
ck('six_period_V_focal_product',paired_product(V_x2)==F(64,9))
root=Path(__file__).resolve().parent
result={'status':'PASS','artifact_sha256':sha256((root/'author_replay/PROOF.md').read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'primitive_rotation_cases_including_negative_controls':primitive_cases,'counts':counts,'numerical_diagnostics':0,'limitations':'Finite diagnostics support the written universal divisor proof; the published parametrization and Jacobi analytic facts are source-checked, not established by these tests.'}
out=json.dumps(result,indent=2,sort_keys=True)+'\n';(root/'independent_results.json').write_text(out);print(out,end='')

