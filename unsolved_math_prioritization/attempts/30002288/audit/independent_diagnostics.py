"""Independent finite diagnostics. These do not replace the continuum proof."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit('Use python -I -S')
from fractions import Fraction as Q
import json
import math
import random

def check(ok, label):
    if not ok:
        raise RuntimeError(label)

# Exercise the central algebra over a rational grid with asymmetric base points.
scalar_cases = 0
for A in (Q(1,7), Q(1,2), Q(1), Q(7,3), Q(9)):
    for B in (Q(0), Q(1,8), Q(1), Q(11,3)):
        for C in (Q(0), Q(1,9), Q(2), Q(8)):
            for D in (Q(0), Q(2,7), Q(3), Q(13)):
                if C+D == 0:
                    continue
                H = max(abs(C-A), abs(D-B))
                difference = Q(C,C+D)-Q(A,A+B)
                check(abs(difference) <= H/(A+B), 'independent rational scalar bound')
                scalar_cases += 1

# Disconnected intervals, duplicate poles and dominated weights are deliberately included.
# Euclidean distances and alpha=1 make every operation exact.
poles = (Q(-2), Q(2), Q(2))
weights_cases = ((Q(1),Q(3,4),Q(1,8)), (Q(2,9),Q(1),Q(1)),
                 (Q(1),Q(1),Q(1)), (Q(1),Q(1,20),Q(1,30)))
def interval_delta(x):
    return max(Q(0), min(x+3,-1-x), min(x-1,3-x))
def iv_profile(x,z):
    D=interval_delta(x)
    return D/(D+abs(x-z))
xs=[Q(k,13) for k in range(-38,39) if interval_delta(Q(k,13))>0]+list(poles)
ys=[Q(k,11) for k in range(-55,56)]+[Q(-1000),Q(1000),Q(-3),Q(-1),Q(1),Q(3)]
exact_pairs=0
for weights in weights_cases:
    def u(x): return max(w*iv_profile(x,z) for w,z in zip(weights,poles))
    for x in xs:
        value=u(x); D=interval_delta(x); bound=value/D
        for y in ys:
            if x!=y:
                check(abs(u(y)-value)<=bound*abs(y-x),'disconnected weighted max slope')
                exact_pairs+=1
        boundary=min((Q(-3),Q(-1),Q(1),Q(3)),key=lambda y:abs(y-x))
        check((u(boundary)-value)/abs(boundary-x)==-bound,'exact exterior witness')
        if x not in poles:
            active=next(i for i in range(len(poles)) if weights[i]*iv_profile(x,poles[i])==value)
            z=poles[active]
            check(u(z)==weights[active],'active pole cannot be dominated')
            check((u(z)-value)/abs(z-x)==bound,'exact positive witness')
        else:
            check(D==1,'pole eigenbranch')

# Independently generated random full-space points: a rectangle, a 3-D box,
# an annulus and two disjoint disks. The annulus is smooth with a circular ridge.
rng=random.Random(30002288)
def rect_delta(x):return max(0.0,min(2-abs(x[0]),1-abs(x[1])))
def box_delta(x):return max(0.0,min(3-abs(x[0]),2-abs(x[1]),1-abs(x[2])))
def annulus_delta(x):
    radius=math.hypot(*x)
    return max(0.0,min(radius-1,3-radius))
def disks_delta(x):return max(0.0,1-math.dist(x,(-2.,0.)),1-math.dist(x,(2.,0.)))
def nearest_rect(x):
    if 2-abs(x[0])<1-abs(x[1]):return (math.copysign(2,x[0]),x[1])
    return (x[0],math.copysign(1,x[1]))
def nearest_box(x):
    i=min(range(3),key=lambda i:(3,2,1)[i]-abs(x[i]));y=list(x);y[i]=math.copysign((3,2,1)[i],x[i]);return tuple(y)
def nearest_annulus(x):
    radius=math.hypot(*x);b=1 if radius<2 else 3
    return tuple(b*v/radius for v in x)
def nearest_disks(x):
    c=min(((-2.,0.),(2.,0.)),key=lambda c:math.dist(x,c));radius=math.dist(x,c)
    return (c[0]+1,c[1]) if radius==0 else tuple(c[i]+(x[i]-c[i])/radius for i in range(2))
configs=[('rectangle',rect_delta,nearest_rect,2,[(-1.,0.),(0.,0.),(1.,0.)]),
         ('box',box_delta,nearest_box,3,[(-2.,-1.,0.),(0.,0.,0.),(2.,1.,0.)]),
         ('annulus',annulus_delta,nearest_annulus,2,[(2.,0.),(0.,2.),(-2.,0.)]),
         ('disks',disks_delta,nearest_disks,2,[(-2.,0.),(2.,0.),(2.,0.)])]
numeric_pairs=0; witnesses=0; kink_cases=0; alpha_cases=(.01,.125,.37,.5,.9,1.)
for name,delta,nearest,n,zs in configs:
    inside=[]
    while len(inside)<45:
        p=tuple(rng.uniform(-3.9,3.9) for _ in range(n))
        if delta(p)>.03:inside.append(p)
    inside+=zs
    exterior=[tuple(rng.uniform(-8.,8.) for _ in range(n)) for _ in range(35)]
    exterior +=[tuple(1000. for _ in range(n)),tuple(-1000. for _ in range(n))]
    for alpha in alpha_cases:
        weights=(1.,.73,.21)
        def profile(x,z):
            d=delta(x)**alpha;return d/(d+math.dist(x,z)**alpha)
        def u(x):return max(w*profile(x,z) for w,z in zip(weights,zs))
        for x in inside:
            value=u(x);bound=value/delta(x)**alpha
            for y in inside+exterior:
                if x==y:continue
                slope=(u(y)-value)/math.dist(y,x)**alpha
                check(abs(slope)<=bound+2e-10,name+' numerical global slope')
                numeric_pairs+=1
            y=nearest(x)
            # The analytically projected boundary has value exactly zero. Re-evaluating
            # a rounded radial point at tiny alpha spuriously magnifies 1e-16 errors.
            check(delta(y)<2e-14,name+' boundary projection residual')
            check(abs(-value/math.dist(y,x)**alpha+bound)<2e-10,name+' exterior witness')
            witnesses+=1
            if x not in zs:
                active=max(range(len(zs)),key=lambda i:weights[i]*profile(x,zs[i]))
                z=zs[active]
                check(abs(u(z)-weights[active])<2e-12,name+' active pole not dominated')
                check(abs((u(z)-value)/math.dist(z,x)**alpha-bound)<2e-10,name+' positive witness')
                witnesses+=1

# Off-ridge profile switches are included explicitly; a max kink is not smoothed.
a=(-1.,0.);b=(1.,0.)
for alpha in alpha_cases:
    for ordinate in (.2,.6,.9):
        def f(x,z):
            d=rect_delta(x)**alpha;return d/(d+math.dist(x,z)**alpha)
        left,right=-1.,1.
        for _ in range(80):
            m=(left+right)/2;x=(m,ordinate)
            if f(x,a)>.75*f(x,b):left=m
            else:right=m
        x=((left+right)/2,ordinate)
        # For very small alpha the weak pole does not dominate at this height,
        # so there is no switch. Only genuine bracketing roots count as kinks.
        if abs(f(x,a)-.75*f(x,b))>2e-12:continue
        U=lambda y:max(f(y,a),.75*f(y,b))
        bound=U(x)/rect_delta(x)**alpha
        for z in (a,b):check(abs((U(z)-U(x))/math.dist(z,x)**alpha-bound)<2e-10,'kink both pole witnesses')
        check(rect_delta(x)<1,'off-ridge kink')
        kink_cases+=1
check(kink_cases>0,'off-ridge kink diagnostic exercised')

# An exact max-switching point on the rectangle ridge at alpha=1.
x=Q(2,7); value=Q(7,16)
check(1/(2+x)==Q(3,4)/(2-x)==value,'exact kink value')
check((1-value)/(x+1)==(Q(3,4)-value)/(1-x)==value,'exact kink positive slopes')

result={'schema':'independent-finite-diagnostics-v1','problem_id':30002288,'status':'PASS',
        'rational_scalar_cases':scalar_cases,'disconnected_exact_ordered_pairs':exact_pairs,
        'numerical_full_space_pairs':numeric_pairs,'explicit_witness_checks':witnesses,
        'off_ridge_kink_cases':kink_cases,'exact_ridge_kink':'x=(2/7,0), U=7/16 at alpha=1',
        'domains':[x[0] for x in configs], 'scope':'Finite diagnostics only; mathematical audit proves the continuum claims.'}
sys.stdout.write(json.dumps(result,sort_keys=True,indent=2)+'\n')
