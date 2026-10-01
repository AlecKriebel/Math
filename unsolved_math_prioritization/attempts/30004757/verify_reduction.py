#!/usr/bin/env python3
"""Independently derived symbolic checks of author turn 2; not a PDE solver."""
import json
import sympy as s
p,z,r,R,lam=s.symbols('p z r R lam', positive=True)
a,b,c=s.symbols('a b c', positive=True)
checks=[]
def verify(name,expr):
    assert s.simplify(expr)==0,(name,s.factor(expr))
    checks.append(name)
# Non-separable-in-(r,z) polynomial potential; inverse radial gradient is explicit.
u=a*r*r/2+b*r*r*z*z+c*z*z/2
ur=s.diff(u,r); urr=s.diff(u,r,2)
D=s.diff(u,r,2)*s.diff(u,z,2)-s.diff(u,r,z)**2
rho=p/(a+2*b*z*z)
F=p*rho-u.subs(r,rho)
for n in range(3,7):
    det=(ur/r)**(n-2)*D
    residual=s.diff(F,z,2)+(s.diff(F,p)/p)**(n-2)*s.diff(F,p,2)
    claimed=((r/ur)**(n-2)*(1-det)/urr).subs(r,rho)
    verify(f'partial Legendre residual n={n}',residual-claimed)
    verify(f'divergence form n={n}',p**(n-2)*residual-(p**(n-2)*s.diff(F,z,2)+s.diff(s.diff(F,p)**(n-1),p)/(n-1)))
# Positive quadratic calibration has determinant one.
F0=(p*p-z*z)/2
for n in [3,4]:
    verify(f'quadratic calibration n={n}',s.diff(F0,z,2)+(s.diff(F0,p)/p)**(n-2)*s.diff(F0,p,2))
# Separated exact equation and balanced edge exponent.
A=s.Function('A')(z);B=s.Function('B')(p)
for n in [3,4]:
    lhs=s.diff(A*B,z,2)+(s.diff(A*B,p)/p)**(n-2)*s.diff(A*B,p,2)
    expected=s.diff(A,z,2)*B+A**(n-1)*s.diff(B,p)**(n-2)*s.diff(B,p,2)/p**(n-2)
    verify(f'separation n={n}',lhs-expected)
    alpha=s.Rational(n,n-2)
    verify(f'exponent balance n={n}',(alpha-1)*(n-2)+(alpha-2)-alpha)
    verify(f'Legendre dual power n={n}',alpha/(alpha-1)-s.Rational(n,2))
    verify(f'endpoint homogeneous balance n={n}',s.Rational(n,2)-s.Rational(n-2,2)-1)
# Linearized Euler equations for B=C*x^alpha*(1+epsilon*x^k).
x,k,e=s.symbols('x k e', positive=True)
for n in [3,4]:
    alpha=s.Rational(n,n-2)
    w=1+e*x**k
    D=lambda f:s.expand(x*s.diff(f,x))
    left=(alpha*w+D(w))**(n-2)*(alpha*(alpha-1)*w+(2*alpha-1)*D(w)+D(D(w)))
    right=alpha**(n-1)*(alpha-1)*w # p=R in indicial linearization
    linear=s.diff(left-right,e).subs(e,0)/x**k
    target=3*(k+1)*(k+6) if n==3 else 4*(k+1)*(k+4)
    verify(f'Frobenius indicial polynomial n={n}',linear-target)
print(json.dumps({'status':'PASS','checks':len(checks),'sympy_version':s.__version__,
                  'verified':checks,
                  'limitation':'Algebra identities only. Does not classify global solutions, prove rim matching, or validate numerical asymptotics.'},indent=2))
