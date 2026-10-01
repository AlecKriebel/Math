#!/usr/bin/env python3
"""Algebra controls for turn 3; no compactness/uniqueness assertion for source blow-ups."""
import json
import sympy as S
s,z,R,I,lam=S.symbols('s z R I lam',positive=True)
eta=S.symbols('eta',real=True)
checks=[]
def check(name,expr):
 assert S.simplify(expr)==0,(name,S.simplify(expr));checks.append(name)
for n in [3,4]:
 alpha=S.Rational(n,n-2)
 for power in [2,4,6]:
  phi=2+eta**2/S.Integer(2)+eta**power/S.Integer(11)
  V=s**alpha*phi.subs(eta,z/s**alpha)
  det2=S.diff(V,s,2)*S.diff(V,z,2)-S.diff(V,s,z)**2
  B=phi-eta*S.diff(phi,eta)
  expected=alpha*(alpha-1)*s**(-2)*(B*S.diff(phi,eta,2)).subs(eta,z/s**alpha)
  check(f'reduced Hessian n={n}, polynomial degree={power}',det2-expected)
 check(f'anisotropic MA scaling n={n}',n+2*alpha-n*alpha)
 c0=R**(n-2)/(alpha**(n-1)*(alpha-1))
 B0=(S.sqrt(2*c0/n)*I)**(S.Rational(2,n-2))
 eta0=S.sqrt(2*B0**n/(n*c0))
 check(f'profile endpoint slope n={n}',c0*eta0*B0**(1-n)*I-1)
 J=2*I/n
 A=(S.sqrt(S.Rational(n,2)/lam)*J)**(S.Rational(2,n-2))
 d=S.sqrt(2*lam/n)*A**(S.Rational(n,2))
 C=(lam*R**(n-2)/(alpha**(n-1)*(alpha-1)))**(S.Rational(1,n-2))
 check(f'agreement with turn2 rim coefficient n={n}',d*C-eta0)
print(json.dumps({'status':'PASS','checks':len(checks),'verified':checks,
 'limitation':'Algebra and cross-model consistency only. Does not show any normalized global source solution converges to this model.'},indent=2))
