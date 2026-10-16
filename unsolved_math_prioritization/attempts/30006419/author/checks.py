#!/usr/bin/env python3
"""Exact algebra controls, not a verification of the analytic theorems."""
from fractions import Fraction as F
from math import factorial
import json

counts = {}
def check(condition, group):
    if not condition:
        raise RuntimeError('Failed control: ' + group)
    counts[group] = counts.get(group, 0) + 1

def poly(d): return {k:F(v) for k,v in d.items() if v}
def add(p,q):
    r=dict(p)
    for k,v in q.items(): r[k]=r.get(k,F(0))+v
    return poly(r)
def scale(p,c): return poly({k:v*c for k,v in p.items()})
def mul(p,q):
    r={}
    for (i,j),a in p.items():
        for (k,l),b in q.items(): r[i+k,j+l]=r.get((i+k,j+l),F(0))+a*b
    return poly(r)
def power(p,n):
    r={(0,0):F(1)}
    for _ in range(n): r=mul(r,p)
    return r
def deriv(p,axis):
    r={}
    for k,v in p.items():
        if k[axis]:
            z=list(k);z[axis]-=1;r[tuple(z)]=v*k[axis]
    return r
def integ(p,xb=F(1),yb=F(1)):
    return sum((v*xb**(i+1)*yb**(j+1)/((i+1)*(j+1)) for (i,j),v in p.items()), F(0))
def circle(p):
    ans=F(0)
    for (i,j),v in p.items():
        if i%2 or j%2: continue
        m,n=i//2,j//2
        ans += 2*v*F(factorial(2*m)*factorial(2*n),4**(m+n)*factorial(m)*factorial(n)*factorial(m+n))
    return ans
x={(1,0):F(1)};y={(0,1):F(1)};one={(0,0):F(1)}
x2=power(x,2);y2=power(y,2);xy=mul(x,y)
phi=mul(mul(x,add(one,scale(x,-1))),mul(y,add(one,scale(y,-1))))

def jac(p,q):return add(mul(deriv(p,0),deriv(q,1)),scale(mul(deriv(p,1),deriv(q,0)),-1))
def grad2(p):return add(power(deriv(p,0),2),power(deriv(p,1),2))

for k in range(-6,7):
    w=scale(mul(phi,add(one,scale(x,F(k,7)))),F(k,3))
    f=add(y,w)
    check(integ(grad2(f)) == 1+integ(grad2(w)), 'scalar_dirichlet_identity')
    check(integ(deriv(w,1)) == 0, 'zero_trace_cross_term')

for k in [-3,-1,0,1,3]:
    vx=add(x,scale(phi,F(k,2)));vy=add(y,scale(mul(phi,x),F(2-k,3)))
    for n,m in [(0,0),(1,0),(0,1),(2,1)]:
        pull=mul(mul(power(vx,n),power(vy,m)),jac(vx,vy))
        check(integ(pull)==F(1,(n+1)*(m+1)), 'exact_form_same_boundary')
check(integ(jac(scale(x,2),y)) != integ(jac(x,y)), 'negative_changed_boundary')

for numerator in range(1,20):
    mass=F(numerator,41);b=mass/(1-mass)
    check(0<b<1, 'calibration_comass')
    check((1+b)*mass-b==0, 'calibration_zero_integral')
    check((1+b)-b==1, 'calibration_saturation')
check(F(3,4)/(1-F(3,4))>1, 'negative_large_cutoff_mass')

for a in range(1,6):
    for c in range(1,5):
        b=F(1,3)
        sq=add(add(scale(x2,a),scale(xy,2*b)),scale(y2,c))
        t11=4*circle(mul(sq,x2))-2*circle(sq)
        t12=4*circle(mul(sq,xy))
        t22=4*circle(mul(sq,y2))-2*circle(sq)
        check((t11,t12,t22)==(a-c,2*b,c-a), 'quadratic_stress')
        check(t11+t22==0,'trace_free_stress')
        B=((F(a,7),F(c,5)),(F(-c,3),F(2-a,9)))
        direct=2*(a*B[0][0]+b*(B[0][1]+B[1][0])+c*B[1][1])-(a+c)*(B[0][0]+B[1][1])
        paired=t11*B[0][0]+t12*(B[0][1]+B[1][0])+t22*B[1][1]
        check(direct==paired,'domain_variation_pairing')
for L in [F(1,10),F(1,2),F(1),F(3)]:
    sq=scale(x2,L*L)
    check((4*circle(mul(sq,x2))-2*circle(sq),4*circle(mul(sq,y2))-2*circle(sq))==(L*L,-L*L), 'rank_one_stress')
    check(L*L>0,'negative_rank_one_balance')

for n in range(1,41):
    t=F(1,4*n);a=t*t
    check(1/a>n,'unbounded_distortion_witness')
    check(max(a*a,F(1))==1 and a<1,'belt_density_and_area_gap')
check(max(F(4),F(1))!=1,'negative_radial_stretch_above_one')

psi=mul(mul(x,add({(0,0):F(1,4)},scale(x,-1))),mul(y,add(one,scale(y,-1))))
linear=integ(scale(mul(x2,deriv(psi,0)),2),F(1,4))
by_parts=integ(scale(mul(x,psi),-4),F(1,4))
check(linear==by_parts and linear<0,'korevaar_schoen_lowering_variation')
quad=integ(grad2(psi),F(1,4))
eps=-linear/(2*quad)
check(eps>0 and eps*linear+eps*eps*quad<0,'finite_dirichlet_energy_decrease')
# Rational test of the bound: m^2 + 8m >= 1 is forced by the stress estimate.
check(F(1,8)**2+8*F(1,8)>1 and F(1,10)**2+8*F(1,10)<1,'distortion_bound_bracket')

print(json.dumps({'status':'PASS','total':sum(counts.values()),'groups':counts,
 'dirichlet_variation_linear':str(linear),'dirichlet_variation_quadratic':str(quad),
 'scope':'Finite exact algebra controls only. No analytic theorem, literature priority, or formal verification claim.'},indent=2,sort_keys=True))
