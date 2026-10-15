#!/usr/bin/env python3
"""Exact finite controls for k403,a; topology/meromorphic proof remains separate."""
from fractions import Fraction as F
from math import gcd
from collections import Counter
import random,json
import sympy as S
C=Counter()
def ck(x,label):
    assert bool(x),label;C[label]+=1

def dot(p,q):return p[0]*q[0]+p[1]*q[1]
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def area(ps):return sum((cross(ps[i-1],ps[i]) for i in range(len(ps))),F(0))/2
def edge(p,q):
    hp,hq=dot(p,p),dot(q,q)
    return (hp*hq-(hp+hq)*dot(p,q)/2)/cross(p,q)
def meet(p,q):
    hp,hq=dot(p,p),dot(q,q);d=cross(p,q)
    return ((hp*q[1]-hq*p[1])/d,(p[0]*hq-q[0]*hp)/d)
rng=random.Random(5100020)
accepted=0
while accepted<300:
    n=rng.randrange(3,10);ps=[(F(rng.randrange(-8,9)),F(rng.randrange(-8,9))) for _ in range(n)]
    if any(cross(ps[i-1],ps[i])==0 for i in range(n)):continue
    rs=[meet(ps[i],ps[(i+1)%n]) for i in range(n)]
    ck(area(rs)==sum((edge(ps[i-1],ps[i]) for i in range(n)),F(0)),'shoelace_vs_edge_area')
    for i,p in enumerate(ps):
        q=ps[(i+1)%n];r=rs[i]
        ck(dot(p,r)==dot(p,p) and dot(q,r)==dot(q,q),'named_antipedal_lines')
        ck(edge(q,p)==-edge(p,q),'edge_antisymmetry')
        ck(edge(tuple(-z for z in p),tuple(-z for z in q))==edge(p,q),'simultaneous_negation')
        ck(edge((p[0],-p[1]),(q[0],-q[1]))==-edge(p,q),'reflection_character')
    accepted+=1
x,y,z,w=S.symbols('x y z w');hp=x*x+y*y;hq=z*z+w*w;d=x*z+y*w
num=hp*hq-(hp+hq)*d/2
ck(S.expand(num-((hp+hq)*((x-z)**2+(y-w)**2)-(hp-hq)**2)/4)==0,'coincident_numerator_factorization')
# Formal addition-formula numerator, reduced by the Jacobi quadratic identities.
s,c,dd,SS,CC,DD,k=S.symbols('s c d S C D k');den=1-k*k*s*s*SS*SS
snminus=SS*c*dd-s*CC*DD;snplus=SS*c*dd+s*CC*DD
cnminus=CC*c+SS*s*DD*dd;cnplus=CC*c-SS*s*DD*dd
expr=S.expand(snplus*cnminus-snminus*cnplus-2*s*c*DD*den)
ck(S.expand(expr.subs(CC**2,1-SS**2).subs(dd**2,1-k*k*s*s))==0,'chord_cross_addition_identity')
for sign in (-1,1):
    exp=S.expand(SS*dd*(SS*c*dd+sign*s*CC*DD)+CC*(CC*c-sign*SS*s*DD*dd)-c*den)
    ck(S.expand(exp.subs(CC**2,1-SS**2).subs(dd**2,1-k*k*s*s))==0,'named_caustic_tangent_identity')
eps=S.symbols('eps');aa=S.symbols('a0:5');H=aa[0]/eps**2+aa[1]/eps+aa[2]+aa[3]*eps+aa[4]*eps**2
ck(S.expand(H-H.subs(eps,-eps))==2*aa[1]/eps+2*aa[3]*eps,'incident_even_pole_cancellation')
# Rational bookkeeping with K=1. These tests do not establish the analytic poles.
families=0
for N in range(3,104,2):
    ell=F(2,N)
    for tau in range(1,N//2+1):
        if gcd(tau,N)!=1:continue
        v=F(2*tau,N);delta=2*v
        orbit={j*delta%2 for j in range(N)}
        ck(orbit=={j*ell for j in range(N)},'odd_orbit_quotient')
        ck(v/ell==tau,'midpoint_poles_same_classes')
        ck((1+v)%ell==ell/2,'pedal_half_period_shift')
        ck(delta%2!=0,'regular_neighbors_at_poles')
        ck(sum((j*delta+v)%2==0 for j in range(N))==1,'one_opposite_endpoint_edge')
        ck(all((-v-j*delta)%ell==0 for j in range(N)),'all_midpoint_poles_accounted')
        ck(1%ell==ell/2,'pedal_pole_real_class')
        families+=1
# Genuine four-orbit negative control: a^2=5,b^2=3, common caustic lambda=15/8.
A2,B2=F(5),F(3);lam=A2*B2/(A2+B2);alpha2=A2-lam;beta2=B2-lam
ck(alpha2/A2+beta2/B2==1,'four_orbit_axis_chord_tangent')
ck(alpha2==A2*A2/(A2+B2) and beta2==B2*B2/(A2+B2),'four_orbit_rectangle_vertices')
ck(alpha2/A2**2==beta2/B2**2,'four_orbit_rectangle_reflection')
ratio=(alpha2+beta2)**2/(2*alpha2*beta2)
ck(ratio==F(578,225) and ratio!=2,'reject_all_parity_antipedal_ratio')
ck(16*A2*A2*B2*B2/(A2+B2)**2==F(225,4),'even_diamond_product')
ck(4*(alpha2+beta2)**2==F(289,4),'even_rectangle_product')
# Circle pedal and antipedal radius factors cancel without dividing by signed area.
r,sn,cs=S.symbols('r sn cs',nonzero=True);n=S.symbols('n',positive=True)
ck(S.simplify((n*r*r*cs*cs*sn/2)*(n*r*r*sn/(2*cs*cs))-n*n*r**4*sn**2/4)==0,'circle_product')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'families':dict(C),'odd_lattice_families':families,'rational_polygons':accepted,'sympy_version':S.__version__,'scope':'Finite exact geometry/algebra/lattice controls only; the all-index meromorphic argument is in PROOF.md.'},indent=2))
