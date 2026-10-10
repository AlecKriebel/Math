#!/usr/bin/env python3
"""Independent exact controls for the audit; no PDE integration or proof certification."""
import json
import sympy as S

checks = []
rejected = []

def equal(name, lhs, rhs=0):
    difference = S.factor(S.simplify(lhs-rhs))
    if difference != 0:
        raise RuntimeError(f"{name}: residual {difference}")
    checks.append(name)

def require(name, condition):
    if condition is not True and condition != S.true:
        raise RuntimeError(f"{name}: {condition}")
    checks.append(name)

def reject(name, expression):
    if S.factor(S.simplify(expression)) == 0:
        raise RuntimeError(f"Incorrect control survived: {name}")
    rejected.append(name)

c, lam, e, b, dc, dp, x = S.symbols('c lam e b dc dp x', positive=True)
K,N,L = S.symbols('K N L', positive=True)
for m in (2,3,4):
    q=S.Rational(5-m,m+3)
    p=S.Rational(4,m+3)
    alpha=S.Rational(2,m-1)-S.Rational(1,2)
    beta=S.Rational(1,m-1)-S.Rational(1,2)
    # Eliminate all fractional invariant powers before differentiating.
    G=c**(5-m)*((m+3)*lam-(5-m)*c)**(2*m-2)
    drift=e*p*c*(c-lam/q)*b
    deriv=S.diff(G,c)/G
    equal(f'm{m} polynomial invariant cancellation',deriv*drift,4*e*b*(c-lam))
    equal(f'm{m} polynomial error identity',
          deriv*(drift+dc)-4*e*b*(c-lam+dp),deriv*dc-4*e*b*dp)
    equal(f'm{m} critical polynomial derivative',S.diff(G,c).subs(c,lam))
    equal(f'm{m} normalized polynomial curvature',
          (S.diff(G,c,2)/G).subs(c,lam),-(m+3)*q/(lam**2*(1-q)))
    equal(f'm{m} energy exponent',alpha,q/(1-q))
    equal(f'm{m} signed integral exponent',beta,S.Rational(3-m,2*(m-1)))
    # Solve, rather than substitute claimed solutions into, the two Pohozaev relations.
    sol=S.solve([K+c*L-N, K/2-c*L/2+N/(m+1)],(K,N),dict=True)[0]
    equal(f'm{m} kinetic ratio',sol[K]/L,S.Rational(m-1,m+3)*c)
    equal(f'm{m} nonlinear ratio',sol[N]/L,S.Rational(2*(m+1),m+3)*c)
    energy=(K/2+lam*L/2-N/(m+1)).subs(sol)/L
    equal(f'm{m} normalized energy',energy,(lam-q*c)/2)
    f=c**alpha*(lam-q*c)
    equal(f'm{m} energy slope',S.diff(f,c),alpha*c**(alpha-1)*(lam-c))
    equal(f'm{m} defect curvature',-S.diff(f,c,2).subs(c,lam),alpha*lam**(alpha-1))
    # Explicit mass derivative follows from integrating u_x a u^m once.
    equal(f'm{m} mass flux coefficient',S.Rational(m,m+1)-1,-S.Rational(1,m+1))
    k=S.Rational(m-1,2)
    Q=(S.Rational(m+1,2)/S.cosh(k*x)**2)**S.Rational(1,m-1)
    equal(f'm{m} explicit soliton differential equation',(S.diff(Q,x,2)-Q+Q**m)/Q)
    # Taylor coefficient from the logarithm of G; do not use author's H code.
    hcurv=-(S.diff(G,c,2)/G).subs(c,lam)/(m+3)
    equal(f'm{m} potential-tail square coefficient',p/hcurv,p*lam**2*(1-q)/q)
    equal(f'm{m} invariant-perturbation square coefficient',2/hcurv,2*lam**2*(1-q)/q)
    require(f'm{m} positive alpha',alpha>0)
    reject(f'm{m} positive mass-production sign',-S.Rational(1,m+1)-S.Rational(1,m+1))
    reject(f'm{m} missing factor two in invariant defect',2/hcurv-1/hcurv)

# Exact rational threshold controls, separately reconstructing the powered equation.
for m,left,right in [(2,S.Rational(63,100),S.Rational(64,100)),
                     (3,S.Rational(42,100),S.Rational(43,100))]:
    q=S.Rational(5-m,m+3)
    poly=lam**(m+3)*(1-q)**(2*m-2)-16*(lam-q)**(2*m-2)
    require(f'm{m} lower threshold sign',poly.subs(lam,left)>0)
    require(f'm{m} upper threshold sign',poly.subs(lam,right)<0)
q=S.Rational(1,7);p=S.Rational(4,7);lc=S.Rational(1,4)
equal('quartic positive-base threshold',lc**7*(1-q)**6,16*(lc-q)**6)
equal('quartic signed integral exact cancellation',2**(-S.Rational(1,3))*lc**(-S.Rational(1,6)),1)
equal('quartic energy endpoint',2**(-S.Rational(2,3))*lc**S.Rational(1,6)*(lc-q*lc),lc-q)
require('quartic critical interval',q<lc<1)
reject('quartic claimed nonzero signed-integral mismatch',1)

# A compactly supported C1, H1 tail gives exact integral and norm controls.
z=S.symbols('z',real=True)
phi=S.Rational(15,16)*(1-z*z)**2
equal('tail integral normalization',S.integrate(phi,(z,-1,1)),1)
equal('tail L2 coefficient',S.integrate(phi**2,(z,-1,1)),S.Rational(5,7))
equal('tail derivative L2 coefficient',S.integrate(S.diff(phi,z)**2,(z,-1,1)),S.Rational(15,7))
equal('tail boundary value',phi.subs(z,1))
equal('tail boundary derivative',S.diff(phi,z).subs(z,1))
ell=S.symbols('ell',positive=True)
equal('tail H1 norm limit',S.limit(S.Rational(5,7)/ell+S.Rational(15,7)/ell**3,ell,S.oo))
reject('H1 convergence forces integral convergence',S.integrate(phi,(z,-1,1)))

# Flat-crossing counterexample: a(r)=1+L(r^3), a(0)=3/2.
r=S.symbols('r',real=True)
a=1+1/(1+S.exp(-r**3))
equal('flat potential central value',a.subs(r,0),S.Rational(3,2))
equal('flat potential first derivative',S.diff(a,r).subs(r,0))
equal('flat potential second derivative',S.diff(a,r,2).subs(r,0))
equal('flat potential cubic coefficient',S.diff(a,r,3).subs(r,0)/6,S.Rational(1,4))
equal('flat potential left limit',S.limit(a,r,-S.oo),1)
equal('flat potential right limit',S.limit(a,r,S.oo),2)
equal('flat potential nonnegative derivative factorization',S.diff(a,r),
      3*r*r*S.exp(-r**3)/(1+S.exp(-r**3))**2)
G=c*((7-4*c)/3)**6 # H(c)^7, quartic normalization.
equal('flat quartic maximum value',G.subs(c,lc),16)
equal('flat quartic maximum derivative',S.diff(G,c).subs(c,lc))
require('flat quartic nondegenerate maximum',S.diff(G,c,2).subs(c,lc)<0)
J7=S.Rational(4,3)**4
equal('flat turning invariant match',J7*S.Rational(3,2)**4,16)
equal('flat right-hand cubic coefficient',
      S.diff(J7*a**4,r,3).subs(r,0)/6,S.Rational(32,3))
v= S.symbols('v',positive=True)
require('flat arrival-time integral diverges',S.integrate(v**(-S.Rational(3,2)),(v,0,1))==S.oo)
equal('positive-slope arrival-time integral finite',S.integrate(v**(-S.Rational(1,2)),(v,0,1)),2)
reject('strict increase permits asserted positive derivative at zero',S.diff(a,r).subs(r,0)-1)

# Stationary integration constant: a scaled plateau has growing dual ratio.
require('constant distribution fails Hminus1 bound',S.limit(ell/S.sqrt(ell+1/ell),ell,S.oo)==S.oo)
# Signed integral has no positivity restriction, unlike an L1 norm.
require('negative tail integral permitted',-S.integrate(phi,(z,-1,1))<0)

print(json.dumps({'status':'PASS','exact_controls':len(checks),'checks':checks,
                  'adversarial_mathematical_controls_rejected':rejected,
                  'scope':'Exact identities and edge controls only. Written analysis audits regularity and infinite-time claims; no PDE classification is certified.'},indent=2,sort_keys=True))
