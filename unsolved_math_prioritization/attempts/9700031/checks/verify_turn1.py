"""Exact arithmetic controls for the traffic moment theorem, not a SIRSN simulation."""
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def ck(ok,name):
    assert ok,name
    C[name]+=1
for s in [F(k,3) for k in range(3,61)]:
    a=1/(s+1);q=2*s/(s+1);edge=4-2/(s+1)
    ck(2-2*a==1+a*(s-1)==q,'balanced_short_route_exponents')
    ck(edge==2+q,'radial_integrability_threshold')
    for j in range(1,20):
        beta=2+(edge-2)*F(j,20)
        ck(1-beta+q>-1,'admissible_short_trip_integral')
        ck(s>(beta-2)/(4-beta),'equivalent_moment_requirement')
    ck(1-edge+q==-1,'threshold_is_logarithmic_not_strictly_integrable')
    ck(0<a<1 and 1-a>0,'tube_radius_shrinks')
values=[1,2,4,10];weights=[F(1,10),F(2,10),F(3,10),F(4,10)]
for s in range(1,13):
    mom=sum(w*d**s for d,w in zip(values,weights))
    for K in range(1,25):
        tail=sum(w*d for d,w in zip(values,weights) if d>K)
        ck(tail<=F(K)**(1-s)*mom,'truncated_first_moment_bound')
for a in [F(j,30) for j in range(1,15)]:
    ck(-2*a>-1,'beta_three_low_length_integrability')
for R in [F(1),F(3,2),F(10)]:
    for p in [F(1,4),F(1),F(7)]:
        # Coefficients of pi; E major length = (p/(M/2))*(2R)^2*pi.
        for k in range(8,16):
            M=F(2)**k
            ck((p/(M/2))*(2*R)**2==8*p*R**2/M,'far_endpoint_length_intensity')
            ck(M-2*R>M/2,'strict_far_endpoint_margin')
            partial=sum(8*p*R/(M*2**j) for j in range(30))
            ck(partial<16*p*R/M,'summable_dyadic_far_probability_bound')
for beta in [F(5,2),F(3),F(7,2),F(39,10)]:
    ck(beta>2,'large_trip_source_kernel_integrable')
    ck(4-beta+1==5-beta,'traffic_scaling_dimension')
    ck(-(5-beta)==beta-5,'pushforward_scaling_exponent')
for J in [F(1,10),F(1),F(100)]:
    for delta in [F(1,100),F(1,10),F(1)]:
        ck((3*J/delta)*4*delta**2==12*J*delta,'packing_tube_area_constant_without_pi')
for gamma in [F(5,2),F(3),F(5),F(10)]:
    for j in range(1,10):
        s=1+(gamma-2)*F(j,10)
        ck(s<gamma-1,'kahn_moment_used_strictly_below_endpoint')
        ck(4-2/(s+1)<4-2/gamma,'kahn_admissible_beta_range')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Finite rational checks of intensity constants, exponent balancing, moment truncation, scaling, and strict endpoint ranges. Geometric and measure-theoretic proof is in TURN_1.md; no finite SIRSN enumeration or simulation is claimed.'},indent=2,sort_keys=True))
