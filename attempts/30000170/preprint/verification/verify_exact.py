#!/usr/bin/env python3
"""Exact rational controls for the revised limiting-normal proof.

Standard-library only. No network, filesystem mutation, floating diagnostics,
or projection solver. Infinite claims are proved analytically in nonunique_nearest_stable_complex_quadratics.tex.
"""
from collections import Counter
from fractions import Fraction as F
import json

counts = Counter()
def ck(value, name):
    assert bool(value), name
    counts[name] += 1
def add(a,b):
    return (a[0]+b[0],a[1]+b[1])
def mul(a,b):
    return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def neg(a):
    return (-a[0],-a[1])
def div(a,b):
    den=b[0]*b[0]+b[1]*b[1]
    assert den>0
    return ((a[0]*b[0]+a[1]*b[1])/den,
            (a[1]*b[0]-a[0]*b[1])/den)
def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),F(0))

one=(F(1),F(0)); imaginary=(F(0),F(1))
for j in range(1,81):
    t=F(1,2**j)
    lam=(F(0),-t); other=(-t*t,t)
    ck(add(lam,other)==(-t*t,F(0)),"exact_root_sum")
    ck(mul(lam,other)==(t*t,t**3),"exact_root_product")
    ck(lam[0]==0 and other[0]<0,"closed_stability_and_strict_gap")
    D=(t*t,-2*t)
    ck(D!= (0,0),"simple_active_root")
    gamma=2/(t*(t*t+4))
    n=[-t,-t*t/2,-t/2,F(1)]
    N=[t**3/2,-t*t,*n]
    dirs=[lam,mul(imaginary,lam),one,imaginary]
    full=[mul(lam,lam),mul(imaginary,mul(lam,lam)),*dirs]
    for direction,component in zip(dirs,n):
        ck(div(neg(direction),D)[0]==gamma*component,
           "all_four_monic_real_derivatives")
    for direction,component in zip(full,N):
        ck(div(neg(direction),D)[0]==gamma*component,
           "all_six_full_real_derivatives")
    w=[t*t,F(0),t*t,t**3]
    n0=[F(0),F(0),F(0),F(1)]
    ck(dot(n0,w)==t**3,"base_limiting_normal_support")
    ck(dot(n,[-x for x in w])==t**3/2,"rational_moving_normal_to_base")
    ck(dot(w,w)==2*t**4+t**6,"quartic_distance")
    quotient=dot(n0,w)/dot(w,w)
    ck(quotient==1/(t*(2+t*t)),"exact_support_quotient")
    ck(quotient>1/(3*t),"rational_uniform_lower_bound")
    ck(dot(n,n)==1+5*t*t/4+t**4/4,"bounded_monic_normal_identity")
    ck(dot(N,N)==1+5*t*t/4+5*t**4/4+t**6/4,
       "bounded_full_normal_identity")
    epin=[*n,-1/gamma]; epifull=[*N,-1/gamma]
    ck(epin[-1]==-t*(t*t+4)/2,"epigraph_height_normal")
    ck(dot([*n0,F(0)],[*w,F(0)])==t**3,
       "horizontal_epigraph_base_support")
    ck(dot([F(0),F(0),*n0,F(0)],
           [F(0),F(0),*w,F(0)])==t**3,
       "horizontal_full_epigraph_base_support")
    # A displacement tau=4t tends to zero, and the base is not nearest along it.
    # This is a nonproximal-normal control, not a nonunique-projection input.
    tau=4*t
    ck(dot(w,w)-2*tau*t**3<0,"exact_distance_improvement_against_base")

# A mixed SPD metric illustrates why horizontal covector need not mean vector.
# H is identity except H[3,4]=H[4,3]=1/2; its 2x2 block has eigenvalues 1/2,3/2.
covector=[F(0),F(0),F(0),F(1),F(0)]
vector=[F(0),F(0),F(0),F(4,3),F(-2,3)]
Hv=[*vector]
Hv[3]=vector[3]+vector[4]/2
Hv[4]=vector[3]/2+vector[4]
ck(Hv==covector,"mixed_spd_covector_to_normal")
ck(vector[-1]!=0,"mixed_spd_normal_can_tilt")
for t in [F(1,2),F(1,8),F(1,128)]:
    displacement=[t*t,F(0),t*t,t**3,F(0)]
    ck(dot(vector,displacement)+
       (vector[3]*displacement[4]+vector[4]*displacement[3])/2==t**3,
       "mixed_spd_support_pairing")

print(json.dumps({"status":"PASS","exact_assertions":sum(counts.values()),
                  "counts":dict(sorted(counts.items())),
                  "arithmetic":"fractions.Fraction; standard library only",
                  "floating_diagnostics":0,
                  "scope":"Current simpler-proof rational identities and controls. Limiting-normal membership, uniform failure, every fixed SPD metric, and attained global nonunique projections rely on the analytic proof. No nearest pair is asserted."},
                 indent=2,sort_keys=True))
