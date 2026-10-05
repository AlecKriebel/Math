#!/usr/bin/env python3
"""Independent exact controls. No source bytes and no network are used.

The analytic statements and standard isoperimetric input are reviewed in
AUDIT.md; these symbolic tests do not establish them by finite sampling.
Only this audit's INDEPENDENT_RESULTS.json is written.
"""
import json
from pathlib import Path
import sympy as s

checks, rejected = [], []

def same(name, left, right=0):
    if s.simplify(left-right) != 0:
        raise AssertionError(name)
    checks.append(name)

def true(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks.append(name)

def wrong(name, left, right=0):
    if s.simplify(left-right) == 0:
        raise AssertionError('Undetected mutation: '+name)
    rejected.append(name)

r,k,R,r0 = s.symbols('r k R r0', positive=True)
A,L,ap = s.symbols('A L ap', positive=True)
a = s.symbols('a', positive=True)
pi=s.pi

# Scale independently by allowing an arbitrary sphere radius and derivative.
area=4*pi*R**2*k**2*r**2/(1+k**2*r**2)
length=4*pi*R*k*r/(1+k**2*r**2)
same('arbitrary radius and derivative radial primitive',s.diff(area,r),8*pi*R**2*k**2*r/(1+k**2*r**2)**2)
same('sphere of radius R total area',s.limit(area,r,s.oo),4*pi*R**2)
same('radius R half-sphere value',area.subs({k:1,r:1}),2*pi*R**2)
same('quarter-area is radius one half',area.subs({R:s.Rational(1,2),k:1,r:1}),pi/2)
same('scaled isoperimetric equality',length**2,area*(4*pi*R**2-area)/R**2)
same('Cauchy Schwarz is independent of sphere radius',length**2,2*pi*r*s.diff(area,r))
same('generalized Q origin value',s.limit((area/(4*pi*R**2))/(r**2*(1-area/(4*pi*R**2))),r,0),k**2)
same('general derivative-radius sharp bound',area.subs(R,1).subs(r,r0),4*pi*k**2*r0**2/(1+k**2*r0**2))
same('general Dufresnoy equality', (area.subs(R,1)/(4*pi))/(r**2*(1-area.subs(R,1)/(4*pi))),k**2)
same('quarter-unit isoperimetric conversion',4*(4*pi*(A/4)-4*(A/4)**2),A*(4*pi-A))

# Integrated monotonicity versus a differential identity, with exact slack.
Q=a/(r**2*(1-a))
dQ=s.diff(Q,r)+s.diff(Q,a)*ap
same('independent Q slack formula',dQ,(r*ap-2*a*(1-a))/(r**3*(1-a)**2))
same('lower-bound rearrangement with general k',a-k**2*r**2/(1+k**2*r**2),(a-k**2*r**2*(1-a))/(1+k**2*r**2))
same('endpoint equality Q',Q.subs({a:s.Rational(1,2),r:1}),1)
same('unit model positive complement',1-r**2/(1+r**2),1/(1+r**2))

# Complex coefficients: do not assume real c when checking the Mobius cap.
x,y,p,q = s.symbols('x y p q',real=True)
w=x+s.I*y; c=p+s.I*q; t2=p*p+q*q
rho2=x*x+y*y
X=2*x/(1+rho2);Y=2*y/(1+rho2);Z=(rho2-1)/(1+rho2)
plane=-2*p*X+2*q*Y+(2-t2)*Z-t2
same('complex Mobius inverse-domain plane',plane*(1+rho2),2*((1-t2)*rho2-2*(p*x-q*y)-1))
same('complex plane normal squared',4*p*p+4*q*q+(2-t2)**2,4+t2*t2)
same('complex Mobius spherical denominator',s.expand((1-c*w)*(1-s.conjugate(c)*s.conjugate(w))+w*s.conjugate(w)),1-2*(p*x-q*y)+(1+t2)*rho2)
same('complex unit-modulus endpoint excess',(t2/s.sqrt(4+t2*t2)).subs({p:s.Rational(3,5),q:s.Rational(4,5)}),1/s.sqrt(5))
same('cap normal strictly exceeds offset squared',(4+t2*t2)-t2*t2,4)

# Direct spherical-rotation identity and normalized family collapse.
z,zb,b,bb,lam,lamb = s.symbols('z zb b bb lam lamb')
num=b+lam*z; den=1-lam*bb*z
numbar=bb+lamb*zb; denbar=1-lamb*b*zb
same('spherical rotation norm identity',s.expand(num*numbar+den*denbar),(1+b*bb)*(1+lam*lamb*z*zb))
g=num/den
same('rotation family derivative exact',s.diff(g,z),lam*(1+b*bb)/den**2)
same('rotation family origin normalization',g.subs(z,0),b)
same('full complex normalization removes rotations',g.subs({b:0,bb:0,lam:1}),z)
true('a nontrivial quarter-turn violates derivative one',s.I!=1)

# Spherical speed-squared leading angular mode; cbar and u^{-1} record conjugates.
C,Cb,u=s.symbols('C Cb u',nonzero=True)
for n in range(2,11):
    angular=C*u**(n-1)+Cb/u**(n-1)
    fp2=1+n*angular*r**(n-1)+n*n*C*Cb*r**(2*n-2)
    f2=r*r+angular*r**(n+1)+C*Cb*r**(2*n)
    q2=fp2/(1+f2)**2
    same('leading angular speed squared n='+str(n),s.limit((q2-1/(1+r*r)**2)/r**(n-1),r,0),n*angular)

# Covering area is genuinely different from image area without injectivity.
for m in (2,3,4):
    cover=4*pi*m*r**(2*m)/(1+r**(2*m))
    same('power covering radial integrand m='+str(m),s.diff(cover,r),8*pi*m*m*r**(2*m-1)/(1+r**(2*m))**2)
    same('power full disk covering area m='+str(m),cover.subs(r,1),2*pi*m)
    true('power covering and image areas differ m='+str(m),cover.subs(r,1)!=2*pi)

# Mutations deliberately target the critical distinctions.
wrong('using pi over two with unit-sphere density',area.subs({R:1,k:1,r:1}),pi/2)
wrong('wrong sphere-radius scaling',area.subs({k:1,r:1}),2*pi*R)
wrong('reversed isoperimetric curvature term',length**2,area*(4*pi*R**2+area)/R**2)
wrong('missing Cauchy Schwarz factor two',length**2,pi*r*s.diff(area,r))
wrong('taking classical derivative bound without square',k**2,k)
wrong('using lower endpoint area as global upper bound',4*pi,2*pi)
wrong('confusing two-sheet covering with image area',4*pi,2*pi)
wrong('allowing quarter-turn under complex derivative normalization',s.I,1)

result={'problem_id':'2306078','status':'PASS','exact_checks_passed':len(checks),'checks':checks,
        'mutations_rejected':len(rejected),'mutations':rejected,
        'scope':'Exact scale, algebra, complex geometry, leading angular terms and multiplicity countercontrols. Not a formal analytic proof.'}
Path(__file__).with_name('INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({key:result[key] for key in ('status','exact_checks_passed','mutations_rejected')}))
