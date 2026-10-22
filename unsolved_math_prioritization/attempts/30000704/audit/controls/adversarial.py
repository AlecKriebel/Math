#!/usr/bin/env python3
"""Independent exact algebraic stress controls; not a theorem prover."""
import json
import sympy as s
r, R, a, N, x, y, q, theta = s.symbols('r R a N x y q theta', positive=True)
checks=[]
def record(name, assertion, category='exact_identity'):
    ok=bool(assertion)
    checks.append({'name':name,'passed':ok,'category':category})
    if not ok: raise AssertionError(name)
def zero(z): return s.simplify(s.factor(s.together(z))) == 0

def laprad(z): return s.diff(z,r,2)+s.diff(z,r)/r
# Fixed exponent uses elementary expressions independently of the author's
# general-real-exponent simplification predicate.
l=1/(2*s.sqrt(r)*(1-r))
record('half-cone curvature directly from logarithm',zero(laprad(s.log(l))-4*l*l))
record('half-cone primitive atanh(sqrt(r))',zero(s.diff(s.atanh(s.sqrt(r)),r)-l))
record('half-cone diverges at puncture',s.limit(l,r,0,dir='+')==s.oo,'exact_limit')
record('half-cone primitive finite at puncture',s.limit(s.atanh(s.sqrt(r)),r,0,dir='+')==0,'exact_limit')
record('half-cone outer boundary coefficient',s.limit((1-r)*l,r,1,dir='-')==s.Rational(1,2),'exact_limit')

# Punctured disk regularization fills the hole. At r=1/4 the cone equals
# 4/3 whereas h_D*=1/log(2)>4/3, since log(2)<3/4.
record('half-cone value at quarter radius',l.subs(r,s.Rational(1,4))==s.Rational(4,3))
t=s.symbols('t',positive=True)
upper=t-1-(t-1)**2/(2*t)
record('log bound certificate derivative and base value',zero(s.diff(upper-s.log(t),t)-(t-1)**2/(2*t*t)) and (upper-s.log(t)).subs(t,1)==0)
record('log2 rational upper bound endpoint',upper.subs(t,2)==s.Rational(3,4))
# Previous identity integrates positively from t=1 to t=2, so log2<3/4.
record('filled-neighborhood density limit',s.limit(R/(R*R-s.Rational(1,4)),R,1,dir='+')==s.Rational(4,3),'exact_limit')

# Singleton pullback at exponent 1/2, evaluated in Cartesian coordinates.
t=s.sqrt((1-x)**2+y*y)
eta=1/(s.sqrt(2*t)*(2-t))
ulog=-s.log(2*t)/2-s.log(2-t)
cart_lap=s.diff(ulog,x,2)+s.diff(ulog,y,2)
# General simplification with radicals can depend on branch choices; evaluate
# three interior rational Cartesian points instead, with exact radicals.
for xx,yy in [(s.Rational(0),s.Rational(0)),(s.Rational(1,2),s.Rational(1,4)),(s.Rational(-1,3),s.Rational(1,5))]:
    record('singleton Cartesian curvature at '+str((xx,yy)),zero((cart_lap-4*eta**2).subs({x:xx,y:yy})),'exact_point_identity')
rho=1/(s.sqrt(2*r)*(2-r))
record('singleton radial primitive',zero(s.diff(s.atanh(s.sqrt(r/2)),r)-rho))
record('singleton density blows up',s.limit(rho,r,0,dir='+')==s.oo,'exact_limit')
record('singleton length remains finite',s.limit(s.atanh(s.sqrt(r/2)),r,0,dir='+')==0,'exact_limit')

# Nonsmooth reentrant sector angle 3*pi/2. It is a Jordan patch and its
# conformal chart from a half-plane has derivative vanishing at the vertex.
p=s.Rational(2,3)
h=p/(2*r*s.sin(p*theta))
u=s.log(p/2)-s.log(r)-s.log(s.sin(p*theta))
polar_lap=s.diff(u,r,2)+s.diff(u,r)/r+s.diff(u,theta,2)/r**2
record('reentrant-sector metric curvature minus four',zero(polar_lap-4*h*h))
record('sector bisector has logarithmic radial primitive',zero(s.diff(p*s.log(r)/2,r)-h.subs(theta,3*s.pi/4)))
record('reentrant chart derivative vanishes',s.limit(s.Rational(3,2)*s.sqrt(r),r,0,dir='+')==0,'exact_limit')
record('reentrant chart cancellation remains valid',zero((p/(2*r**s.Rational(3,2)))*(s.Rational(3,2)*s.sqrt(r))-1/(2*r)))

# Addition of positive flat metrics is not curvature-safe.
summed=s.exp(N*x)+s.exp(-N*x)
curv_sum=-s.diff(s.log(summed),x,2)/(summed*summed)
record('sum of flat densities can have arbitrary negative curvature',zero(curv_sum.subs(x,0)+N*N/4))
record('each exponential constituent is flat',zero(s.diff(N*x,x,2)))

# Demonstrate lower-curvature necessity on the entire analytic boundary.
tau=(1-r*r)**(-s.Rational(1,2))
k=-laprad(s.log(tau))/(tau*tau)
record('square-root disk blow-up has curvature minus two over gap',zero(k+2/(1-r*r)))
record('square-root disk metric finite radial primitive',zero(s.diff(s.asin(r),r)-tau))
record('square-root disk curvature unbounded below',s.limit(k,r,1,dir='-')==-s.oo,'exact_limit')

# Independent normalization, cutoff and integral-control checks.
L=s.symbols('L',positive=True)
cut=s.log(L)-s.log(R*R-r*r)
record('constant-density cutoff curvature',zero(-laprad(cut)/(L/(R*R-r*r))**2+4*R*R/(L*L)))
F=s.log(s.log(R/r))
record('last-crossing potential absolute derivative',zero(s.diff(F,r)+1/(r*s.log(R/r))))
record('last-crossing lower bound diverges',s.limit(F,r,0,dir='+')==s.oo,'exact_limit')

print(json.dumps({'problem_id':30000704,'status':'PASS','count':len(checks),
  'sympy_version':s.__version__,'checks':checks,
  'scope':'Exact formulas, limits and counterexample stress only; topology and all quantified analytic proof steps are separately reviewed in AUDIT.md.'},indent=2,sort_keys=True))
