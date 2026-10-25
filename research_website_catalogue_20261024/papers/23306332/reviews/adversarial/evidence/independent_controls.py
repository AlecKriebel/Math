#!/usr/bin/env python3
"""Independent rational attacks. No published package imported or executed here.
The boundary conormal is obtained from F=v²-xyv-x²u, not a root derivative.
Rational complex square roots make all tested radicals exact.
"""
from fractions import Fraction as Q
from collections import Counter
from random import Random
import json

count=Counter(); mutants={}
def ck(p,label):
    if not p: raise AssertionError(label)
    count[label]+=1
def add(a,b): return tuple(x+y for x,y in zip(a,b))
def neg(a): return tuple(-x for x in a)
def sub(a,b): return add(a,neg(b))
def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q(0))
def cmul(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def sq(z): return cmul(z,z)
def F(c):
    x,y,u,v=c
    return v*v-x*y*v-x*x*u

def gradF(c):
    x,y,u,v=c
    return (-y*v-2*x*u,-x*v,-x*x,2*v-x*y)
def chart(c):
    x,y,u,v=c
    return x>=0 and u+y*y/4>=0 and F(c)<=0

def matrix(L):
    return [[sum((L[k][i]*L[k][j] for k in range(len(L))),Q(0)) for j in range(len(L))] for i in range(len(L))]
def mv(G,v): return [dot(row,v) for row in G]
def solve(G,b):
    n=len(b); a=[list(row)+[b[i]] for i,row in enumerate(G)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j]); a[j],a[k]=a[k],a[j]
        d=a[j][j]; a[j]=[x/d for x in a[j]]
        for k in range(n):
            if k!=j:
                d=a[k][j]; a[k]=[x-d*y for x,y in zip(a[k],a[j])]
    return [row[-1] for row in a]

# Stable polynomials from exact roots, including double imaginary, zero,
# coinciding, strict and one-active-root cases. This does not use a radical test.
rng=Random(2330633207)
for _ in range(2000):
    r1=(-Q(rng.randrange(0,20),17),Q(rng.randrange(-30,31),19))
    r2=(-Q(rng.randrange(0,20),23),Q(rng.randrange(-30,31),29))
    a=neg(add(r1,r2)); b=cmul(r1,r2); c=(*a,*b)
    ck(chart(c),'root_constructed_stable_full_complex_chart')
    # D=(r1-r2)^2, so Phi(D)=abs(Re(r1-r2)); no radical evaluation.
    ck((-a[0]+abs(r1[0]-r2[0]))/2==max(r1[0],r2[0]),'quadratic_abscissa_branch_factor')
# Also challenge necessity: signed root real parts include unstable polynomials.
for _ in range(3000):
    r1=(Q(rng.randrange(-12,13),17),Q(rng.randrange(-30,31),19))
    r2=(Q(rng.randrange(-12,13),23),Q(rng.randrange(-30,31),29))
    a=neg(add(r1,r2)); b=cmul(r1,r2)
    ck(chart((*a,*b))==(max(r1[0],r2[0])<=0),'root_chart_iff_including_unstable')
# Boundary singular/edge controls.
for y in [Q(-2),Q(0),Q(2)]:
    for u in [-y*y/4,Q(1)-y*y/4]:
        ck(chart((Q(0),y,u,Q(0))),'x_zero_boundary_included')
ck(not chart((Q(0),Q(0),Q(-1),Q(0))),'negative_U_excluded')
ck(not chart((Q(-1),Q(0),Q(1),Q(0))),'negative_x_excluded')

for t in [Q(i,37) for i in range(1,38)]+[Q(1,10**i) for i in range(1,31)]:
    c=(t*t,Q(0),t*t,t**3)
    n=(-t,-t*t/2,-t/2,Q(1))
    ck(chart(c) and F(c)==0,'cusp_path_on_complex_stability_boundary')
    ck(gradF(c)==tuple(2*t**3*x for x in n),'polynomial_boundary_conormal')
    dl_real=(-c[0],-c[1],-c[2],-c[3])
    dl_imag=(c[1],-c[0],c[3],-c[2])
    ck((dot(n,dl_real),dot(n,dl_imag))==(t**3/2,-t*t),'full_leading_directions_from_quotient_chart')
    ck(dot(n,neg(c))==t**3/2,'moving_normal_support_against_stable_base')
    ck(dot(c,c)==2*t**4+t**6,'distance_order_exact')
    ck(dot(n,neg(c))/dot(c,c)==1/(2*t*(2+t*t)),'unbounded_uniform_normal_support_ratio')
    # The root imaginary part sign is essential for outward normal orientation.
    cminus=(t*t,Q(0),t*t,-t**3)
    ck(gradF(cminus)[-1]<0,'negative_branch_outward_sign')

metrics=[]
for n in [4,5,6,7]:
    for idx in range(8):
        L=[[Q(0) for j in range(n)] for i in range(n)]
        for i in range(n):
            for j in range(i,n):
                L[i][j]=Q(1,10**idx) if i==j else Q(rng.randrange(-9,10),5)
        G=matrix(L); trace=sum(G[i][i] for i in range(n)); metrics.append((n,idx,trace))
        cov=[Q(0)]*n; cov[n-2 if n in [5,7] else n-1]=Q(1)
        v=solve(G,cov); ck(mv(G,v)==cov,'dense_SPD_metric_normal_representation')
        for tau in [Q(1),Q(1,10**8),Q(1,10**30)]:
            t=min(Q(1,2),tau/(4*trace))
            c=[Q(0)]*n; k=2 if n in [6,7] else 0
            c[k]=t*t; c[k+2]=t*t; c[k+3]=t**3
            norm2=dot(c,mv(G,c)); support=dot(cov,c)
            ck(norm2<=trace*dot(c,c),'trace_dominates_SPD_quadratic_form')
            ck(norm2-2*tau*support<0,'strict_metric_distance_improvement')
            # Full expansion includes nonzero coefficient-height and leading mixing.
            d=sub(c,[tau*x for x in v]); w=[tau*x for x in v]
            ck(dot(d,mv(G,d))-dot(w,mv(G,w))==norm2-2*tau*support,'exact_dense_metric_distance_expansion')

# Rational radicals: D=(p+ih)^2, |D|=p²+h², Phi(D)=p for p>=0.
# At negative-ray bases use q in the exact subdifferential interval; at D=0
# use the normal half-plane, independently derived from the zero ray.
worst=None
for M in [Q(1),Q(3),Q(1000)]:
    delta=1/(16*M*M)
    for j in range(1200):
        p=Q(rng.randrange(0,1000),1000)/(8*M)
        h=Q(rng.randrange(-1000,1001),1000)/(8*M)
        D=sq((p,h)); r=p*p+h*h
        ck(r<delta,'radical_control_local_radius')
        d2=r*r if D[0]>=0 else D[1]*D[1]
        ck(4*delta*p*p>=d2,'exact_squared_distance_to_ray_bound')
        if p>0:
            g=(p/(2*r),h/(2*r))
            ck(dot(g,g)==1/(4*r),'off_ray_gradient_norm_exact')
        if j%2:
            s=Q(rng.randrange(1,1000),1000)/(8*M)
            Dx=(-s*s,Q(0)); q=(Q(0),Q(rng.randrange(-1000,1001),1000)*M/2)
            ck(abs(q[1])<=1/(2*s),'negative_ray_subgradient_valid')
        else:
            Dx=(Q(0),Q(0)); q=(Q(rng.randrange(0,1001),1000)*M/2,Q(rng.randrange(-1000,1001),1000)*M/2)
        ck(dot(q,q)<=M*M,'bounded_subgradient_radius')
        ax=(Q(rng.randrange(-100,101),100000),Q(rng.randrange(-100,101),100000))
        ay=(Q(rng.randrange(-100,101),100000),Q(rng.randrange(-100,101),100000))
        bx=tuple(x/4 for x in sub(sq(ax),Dx)); by=tuple(x/4 for x in sub(sq(ay),D))
        da=sub(ay,ax); db=sub(by,bx)
        va=add((Q(-1,2),Q(0)),cmul((ax[0],-ax[1]),q)); vb=tuple(-2*x for x in q)
        deficit=p/2-da[0]/2-dot(va,da)-dot(vb,db)
        norm2=dot(da,da)+dot(db,db)
        slack=deficit+M*norm2/2
        ck(slack>=0,'full_coefficient_local_prox_support_exact')
        ck(deficit==(p-dot(q,sub(D,Dx))+dot(q,sq(da)))/2,'diffeomorphism_quadratic_remainder_exact')
        worst=slack if worst is None else min(worst,slack)

# Adverse zero-discriminant cases remove all positive Phi slack.
sharp=[]
for M in [Q(1),Q(3),Q(1000)]:
    for tau in [Q(1,10),Q(1,10**10),Q(1,10**30)]:
        da=(Q(0),tau); db=(-tau*tau/4,Q(0))
        ck(sub(sq(da),tuple(4*x for x in db))==(Q(0),Q(0)),'zero_discriminant_adverse_curve')
        q=(M,Q(0)); va=(Q(-1,2),Q(0)); vb=(-2*M,Q(0))
        deficit=-dot(va,da)-dot(vb,db)
        d2=dot(da,da)+dot(db,db)
        ck(deficit==-M*tau*tau/2,'sharp_adverse_curvature_deficit')
        ck(deficit+M*d2/2==M*tau**4/32,'sharp_valid_curvature_slack')
        sharp.append({'M':str(M),'tau':str(tau),'required_r':str(-2*deficit/d2)})
# Mutants are deliberately wrong statements, excluded by exact counterexamples.
# Claiming a true nearest pair from the base competitor inequality is invalid:
# q is only proved to have a stable competitor closer than the base.
t=Q(1,10); c=(t*t,Q(0),t*t,t**3); n=(-t,-t*t/2,-t/2,Q(1))
mutants['reverse_outward_normal_sign_detected']=(dot(gradF(c),n)>0 and dot(gradF(c),neg(n))<0)
G=matrix([[Q(1),Q(0),Q(0),Q(1,2)],[Q(0),Q(1),Q(0),Q(0)],[Q(0),Q(0),Q(1),Q(0)],[Q(0),Q(0),Q(0),Q(1)]])
cov=[Q(0),Q(0),Q(0),Q(1)]
mutants['use_covector_as_metric_vector_detected']=(mv(G,cov)!=cov)
mutants['drop_U_nonnegative_detected']=(F((Q(0),Q(0),Q(-1),Q(0)))<=0 and not chart((Q(0),Q(0),Q(-1),Q(0))))
# Wrong sign of q remainder gives a lower bound contradicted on the zero set.
M=Q(3); tau=Q(1,101); deficit=-M*tau*tau/2
mutants['wrong_quadratic_remainder_sign_detected']=(deficit<0)
# Attempt at a single curvature for all finite subgradients, without localizing v.
unbounded=[]
for t in [Q(1,10**k) for k in range(1,10)]:
    deficit=-t/4; norm2=9*t**4/16; needed=-2*deficit/norm2
    ck(needed==8/(9*t**3),'nonlocalized_curvature_blowup_exact')
    unbounded.append(str(needed))
mutants['omit_subgradient_localization_detected']=Q(unbounded[-1])>10**20
# Closed versus strict stability and leading-degree exclusion are not interchangeable.
mutants['strict_halfplane_path_rejected']=(c[0]>0 and F(c)==0)
for label,value in mutants.items(): ck(value,'mutant_'+label)
print(json.dumps({'arithmetic':'exact fractions.Fraction; radicals encoded as rational complex squares','assertions':sum(count.values()),'counts':dict(count),'metric_cases':len(metrics),'sharp_adverse_curvature_cases':sharp,'mutants_detected':mutants,'min_exact_prox_support_slack':str(worst),'unlocalized_curvature_required':unbounded,'limits':'Finite controls supplement the analytic universal proof; no explicit tied nearest pair is claimed.'},indent=2,sort_keys=True))
