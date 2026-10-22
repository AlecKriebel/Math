#!/usr/bin/env python3
"""Exact algebra checks for a partial analysis, not a proof of the open target."""
import json
import sympy as s
checks=[]
def check(name, expr):
    ok = bool(expr)
    if not ok:
        raise RuntimeError('FAILED: '+name)
    checks.append(name)
def eq(name, left, right=0):
    check(name, s.simplify(left-right)==0)

# General potential Taylor/Bregman identities and antipodal pairing.
a,b,c,q,rho=s.symbols('a b c q rho', real=True)
W=lambda t:t**4
B=lambda aa,qq:W(aa-qq)-W(aa)+4*aa**3*qq
quart=lambda aa,qq:(aa-qq)**2/2-aa**2/2+aa*qq
eq('quadratic Bregman',quart(a,q),q*q/2)
eq('scaled quadratic Bregman',quart(a,q)-quart(b,rho*q),(1-rho**2)*q*q/2)
eq('fourth-power Bregman',B(a,q),6*a*a*q*q-4*a*q**3+q**4)
pair=s.expand((W(a-b-c)+W(a-b+c))/2-W(a)+4*a**3*b-6*a*a*c*c)
eq('parity Hessian residual',pair,6*a*a*b*b-4*a*b**3+b**4+(-12*a*b+6*b*b)*c*c+c**4)
parity=pair.subs({a:s.Rational(1,2),b:s.Rational(1,10),c:s.sqrt(s.Rational(1,10))})
eq('parity exact negative witness',parity,-s.Rational(309,10000))
check('parity witness geometrically feasible',s.Rational(1,10)<=4*s.Rational(1,2)*s.Rational(1,10))
u=s.Matrix([1/s.sqrt(2),0]);v=s.Matrix([1/s.sqrt(20),1/s.sqrt(20)])
eq('witness vector modulus u',u.dot(u),s.Rational(1,2))
eq('witness vector modulus v',v.dot(v),s.Rational(1,10))
eq('witness vector dot', (2*u.dot(v))**2,s.Rational(1,10))
check('paired arguments in potential domain', s.Rational(1,2)-s.Rational(1,10)+s.sqrt(s.Rational(1,10))<1)
left=B(s.Rational(1,10),s.Rational(1,100));right=B(s.Rational(1,2),s.Rational(5,9)*s.Rational(1,100))
eq('calibration left remainder',left,s.Rational(561,100000000))
eq('calibration right remainder',right,s.Rational(48241,1049760000))
eq('calibration exact negative difference',left-right,-s.Rational(1654369,41006250000))
check('both Bregman remainders positive',left>0 and right>0)

# Quartic relative-energy expansion after linear Euler-Lagrange cancellation.
u2,uv,v2,t=s.symbols('u2 uv v2 t', real=True)
pot=((1-u2-2*t*uv-t*t*v2)**2-(1-u2)**2)/4+(1-u2)*t*uv
eq('quartic energy expansion',pot,t*t*(-(1-u2)*v2/2+uv*uv)+t**3*uv*v2+t**4*v2*v2/4)

# Radial ground-state transform; the leftover is a total derivative.
r,N=s.symbols('r N', positive=True)
f=s.Function('f')(r);z=s.Function('z')(r);aa=s.Function('a')(r)
fp=s.diff(f,r);zp=s.diff(z,r)
original=(s.diff(f*z,r)**2+((N-1)/r**2-aa)*(f*z)**2)*r**(N-1)
rhs=f*f*zp*zp*r**(N-1)+s.diff(r**(N-1)*f*fp*z*z,r)
res=s.expand(original-rhs).subs(s.diff(f,r,2),-(N-1)*fp/r+(N-1)*f/r**2-aa*f)
eq('radial ground-state modulo ODE',res)

# Actual polynomial perturbation is clamped but has nonzero angular mean.
for n in [2,3,4,5,6]:
    x=s.symbols('x0:'+str(n));r2=sum(t*t for t in x);psi=x[0]*(1-r2)**2
    grad=[s.diff(psi,t) for t in x]
    expected=[(1-r2)**2*(1 if j==0 else 0)-4*x[0]*x[j]*(1-r2) for j in range(n)]
    check('gradient polynomial N='+str(n),all(s.expand(g-h)==0 for g,h in zip(grad,expected)))
    # Every component visibly contains the factor (1-r^2), hence zero trace.
    check('clamped gradient factor N='+str(n),all(s.rem(g,s.Poly(1-r2,x[0]),x[0])==0 for g in grad))
    m=(1-r*r)**2-4*r*r*(1-r*r)/n
    eq('dipole spherical mean N='+str(n),m,(n-(n+4)*r*r)*(1-r*r)/n)
    eq('nonzero mean at origin N='+str(n),m.subs(r,0),1)

# Rescaling and the explicit comparison-potential example.
eps,C,y=s.symbols('eps C y', positive=True)
delta=eps/s.sqrt(C)
eq('epsilon normalization',1/(4*delta**2),C/(4*eps**2))
t=s.symbols('t', real=True)
Wminus=C*t*t/2+t**4;Wplus=C*t*t/2
for k in [0,1,2]:
    eq('C2 matching derivative '+str(k),s.diff(Wminus,t,k).subs(t,0),s.diff(Wplus,t,k).subs(t,0))
eq('negative-side second derivative',s.diff(Wminus,t,2),C+12*t*t)
eq('negative-side domination',Wminus-Wplus,t**4)
eq('t4 no quadratic lower bound ratio',t**4/(t*t/2),2*t*t)
receipt={'result':'PASS','checks':len(checks),'scope':'Exact algebra only; general-potential target remains unsolved.','sympy_version':s.__version__,'names':checks,'negative_witnesses':{'parity':str(parity),'calibration':str(left-right)}}
print(json.dumps(receipt,indent=2,sort_keys=True))
