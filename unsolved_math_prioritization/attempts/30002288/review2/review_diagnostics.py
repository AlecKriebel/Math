"""Independent finite diagnostics. Analytic acceptance is in REVIEW.md."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    raise SystemExit('Run under python -I -S through the pinned external bootstrap')
import json
import math
import random
from fractions import Fraction as F

def need(test, label):
    if not test:
        raise RuntimeError(label)

# Exact switch missed by uniform grids: alpha=1, rectangle ridge.
x=F(2,7); u=F(7,16)
need(F(1)/(x+2)==u, 'left exact switch value')
need(F(3,4)/(2-x)==u, 'right exact switch value')
need((1-u)/(x+1)==u, 'switch slope to left pole')
need((F(3,4)-u)/(1-x)==u, 'switch slope to right pole')
need((0-u)/1==-u, 'switch slope to nearest exterior')

# Different finite rational range and direct ratio comparison, without using
# the author's rearranged-polynomial implementation.
algebra=0
for a in [F(k,3) for k in range(1,8)]:
    for b in [F(k,4) for k in range(9)]:
        for c in [F(k,5) for k in range(8)]:
            for d in [F(k,6) for k in range(9)]:
                if c+d==0:
                    continue
                h=max(abs(c-a),abs(d-b))
                difference=abs(c/(c+d)-a/(a+b))
                need(difference<=h/(a+b), 'rational ratio slope at x')
                need(difference<=h/(c+d), 'rational ratio slope at y')
                algebra+=1

# Truncation error min(t,epsilon) is a contraction; this is the precise
# domination used in the independently reviewed W_0 approximation.
truncations=0
for a in [F(k,17) for k in range(25)]:
    for b in [F(k,19) for k in range(27)]:
        for eps in [F(1,31),F(2,7),F(1,1)]:
            need(abs(min(a,eps)-min(b,eps))<=abs(a-b), 'truncation contraction')
            truncations+=1

rng=random.Random(300022882)
domain_specs=[
    ('rectangle', (2.,1.), [(-1.,0.),(1.,0.),(0.,0.)]),
    ('box3', (3.,2.,1.), [(-2.,-1.,0.),(2.,1.,0.),(0.,0.,0.)]),
]
pairs=0; pole_equalities=0; boundary_equalities=0; ties=0
for label,half,poles in domain_specs:
    n=len(half)
    def delta(v):
        return max(0.,min(h-abs(q) for h,q in zip(half,v)))
    def nearest(v):
        axis=min(range(n),key=lambda k:half[k]-abs(v[k]))
        w=list(v);w[axis]=math.copysign(half[axis],v[axis]);return tuple(w)
    interior=[tuple(rng.uniform(-.999*h,.999*h) for h in half) for _ in range(90)]+poles
    if n==2:
        interior+=[(2./7.,0.),(0.,.999999999),(-1.999999999,0.)]
    exterior=[nearest(v) for v in interior]+[tuple(1000*h for h in half)]
    ys=interior+exterior
    for alpha in (.03125,.2,.5,.83,1.):
        for weights in ((1.,.75,.1),(.125,1.,.9),(1.,1.,1.)):
            def profiles(v):
                a=delta(v)**alpha
                return [weight*a/(a+math.dist(v,pole)**alpha) for weight,pole in zip(weights,poles)]
            def envelope(v):return max(profiles(v))
            for v in interior:
                uv=envelope(v); a=delta(v)**alpha; bound=uv/a
                need(a>0., 'interior point')
                for w in ys:
                    if v==w:continue
                    slope=(envelope(w)-uv)/(math.dist(v,w)**alpha)
                    need(abs(slope)<=bound+2e-10, 'full-space sampled envelope bound')
                    pairs+=1
                q=nearest(v)
                need(abs((envelope(q)-uv)/math.dist(v,q)**alpha+bound)<=2e-10, 'exterior attainment')
                boundary_equalities+=1
                active=[i for i,t in enumerate(profiles(v)) if abs(t-uv)<1e-14]
                if len(active)>1:ties+=1
                if v not in poles:
                    for i in active:
                        p=poles[i]
                        need(abs((envelope(p)-uv)/math.dist(v,p)**alpha-bound)<=2e-10, 'active pole equality')
                        pole_equalities+=1
                else:
                    need(abs(delta(v)-1.)<1e-14, 'ridge branch at poles')

# Disconnected one-dimensional domain with a nonunit inradius.
# Delta on disjoint balls is max of the separate positive distances.
centers=(-2.,2.); radius=.5
for alpha in (.03125,.5,1.):
    def delta1(x):return max(0.,*(radius-abs(x-c) for c in centers))
    def profile1(x,c):
        a=delta1(x)**alpha;return a/(a+abs(x-c)**alpha)
    def u1(x):return max(profile1(x,-2.),.75*profile1(x,2.))
    xs=[c+radius*j/13. for c in centers for j in range(-12,13)]+list(centers)
    ys=xs+[c+s*radius for c in centers for s in (-1,1)]+[-100.,0.,100.]
    for x in xs:
        bound=u1(x)/delta1(x)**alpha
        for y in ys:
            if x==y:continue
            need(abs(u1(y)-u1(x))<=bound*abs(y-x)**alpha+2e-10,'nonunit disconnected envelope')
            pairs+=1
    need(abs(u1(-2.)-1)<1e-14 and abs(u1(2.)-.75)<1e-14,'nonunit maximum obstruction')
    need(abs(1/radius**alpha-2**alpha)<1e-14,'nonunit exact Holder constant')

# The exponent of the radial tail is strictly less than -1 precisely
# when alpha*p>n. Exercise both endpoints of p choices using rationals.
tails=0
for n in (1,2,3,7):
    for alpha in (F(1,32),F(1,5),F(1,2),F(1)):
        p=F(n,1)/alpha+1
        need(F(n-1)-alpha*p < -1, 'tail exponent integrable')
        s=alpha-F(n,1)/p
        need(0<s<1, 'Gagliardo exponent in zero-one interval')
        need(F(n,1)+s*p==alpha*p,'exact kernel exponent identity')
        tails+=1

result={
 'status':'PASS',
 'scope':'Finite exact and floating-point diagnostics only; not a substitute for the analytic continuum proof.',
 'exact_switch':{'x':'2/7','U':'7/16','positive_slopes':'7/16 at both poles','negative_slope':'-7/16'},
 'rational_ratio_cases':algebra,
 'truncation_contraction_cases':truncations,
 'sampled_full_space_pairs':pairs,
 'sampled_nearest_exterior_equalities':boundary_equalities,
 'sampled_active_pole_equalities':pole_equalities,
 'sampled_multiple_active_points':ties,
 'rational_tail_parameter_cases':tails,
 'numerical_tolerance':'2e-10',
 'general_finite_p_selection':'UNRESOLVED_BY_THIS_WORK'
}
sys.stdout.write(json.dumps(result,sort_keys=True,indent=2)+'\n')
