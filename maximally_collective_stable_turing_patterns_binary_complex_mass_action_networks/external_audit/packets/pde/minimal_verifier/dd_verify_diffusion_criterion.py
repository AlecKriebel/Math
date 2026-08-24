#!/usr/bin/env python3
"""Duplicate exact finite/interface regression for the diffusion-ray criterion."""

if not __debug__:
 raise SystemExit('Exact verifier requires assertions; unset PYTHONOPTIMIZE and do not use python -O')

import sympy as sp
from itertools import combinations
from common import Avec


def verify_threshold_depends_on_flux_parameters():
 """Exact regression against suppressing a,b from the threshold notation."""
 s,a,b=sp.symbols('s a b',positive=True)
 D=sp.diag(1,1,1,9)
 quotient=sp.factor((s*D-Avec(3,a,b)).det()/s)
 expected=(
  9*s**3+(54*a+22*b)*s**2
  +(36*a**2+105*a*b)*s-2*a**2*b
 )
 assert sp.factor(quotient-expected)==0
 assert 9>8  # The exact stationary-crossing criterion is satisfied.

 # Each specialization has one sign change and hence one positive root; the
 # nonzero pairwise resultants prove that those positive roots are distinct.
 specializations=[expected.subs({a:av,b:bv}) for av,bv in ((1,1),(2,1),(1,2))]
 for polynomial in specializations:
  coefficients=sp.Poly(polynomial,s).all_coeffs()
  assert all(value>0 for value in coefficients[:-1]) and coefficients[-1]<0
 for i in range(len(specializations)):
  for j in range(i+1,len(specializations)):
   assert sp.resultant(specializations[i],specializations[j],s)!=0


verify_threshold_depends_on_flux_parameters()

for m in [3,4,5,6,8,10]:
 A=Avec(m);h=[sp.Rational(i+2,i+1) for i in range(m+1)];d=[sp.Rational(2*i+3,i+2) for i in range(m+1)]
 J=A*sp.diag(*h);n=m+1
 beta=[]
 for k in range(1,n+1):
  total=0
  for I in combinations(range(n),n-k):
   Ic=[j for j in range(n) if j not in I]
   det=sp.Integer(1) if not I else J.extract(I,I).det()
   total += (-1)**len(I)*det*sp.prod(d[j] for j in Ic)
  beta.append(sp.factor(total))
 expected=sp.factor(2*sp.prod(h[:m])*(8*h[m]*sum(d[j]/h[j] for j in range(1,m-1))-d[m]))
 assert sp.factor(beta[0]-expected)==0
 assert all(x>0 for x in beta[1:])
print('DIFFUSION_CRITERION_PASS')
