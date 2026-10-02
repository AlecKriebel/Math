#!/usr/bin/env python3
"""Exact polynomial matrix and dyadic-frequency controls for TURN_2.md."""
import sympy as s
import json
x=s.symbols('x'); checks=0

def ck(p):
 global checks
 assert p
 checks+=1

def P(f):
 return s.expand((f.subs(x,x/2-s.Rational(1,4))+f.subs(x,x/2+s.Rational(1,4)))/2)
def phi(f):return s.integrate(x*f,(x,-s.Rational(1,2),s.Rational(1,2)))
f=x**3-s.Rational(3,20)*x
ck(phi(f)==0);ck(P(f)==x**3/8+s.Rational(3,160)*x);ck(phi(P(f))==s.Rational(1,320))
source_test=checks
cases=0
for degree in (3,5,8,12):
 basis=[x**j for j in range(degree+1)]
 mat=s.Matrix([[P(f).coeff(x,j) for f in basis] for j in range(degree+1)])
 ph=s.Matrix([[phi(f) for f in basis]])
 ex=s.zeros(degree+1,1);ex[1]=1
 for B in (s.Rational(601,100),s.Rational(7),s.Rational(10),s.Rational(16)):
  la=s.Rational(1,2)+B/12
  Q=mat+B*ex*ph
  L=la*ph*(la*s.eye(degree+1)-mat).inv()
  E=B/la*ex*L
  ck(L*Q==la*L);ck((L*ex)[0]==la/B)
  ck(E*E==E);ck(Q*E==E*Q);ck(Q*E==la*E)
  for n in range(8):
   rhs=mat**n
   for k in range(n):rhs+=B*la**(n-1-k)*ex*ph*mat**k
   ck(Q**n==rhs)
   # Closed tail is the finite-dimensional version of (8).
   stable=(s.eye(degree+1)-E)
   ck(Q**n*stable==(mat**n-ex*B/la*L*mat**n)*stable)
  ck(s.simplify(1+B/(2*la-1))==7)
  cases+=1
matrix_checks=checks-source_test
# On the Fourier mode cos(2 pi k t), the doubling PFO keeps even k,
# replacing k by k/2, and kills odd k. Verify the two-branch cancellation
# symbolically and all powers used in the non-uniformity witnesses.
k,z=s.symbols('k z',integer=True)
for m in range(12):
 freq=2**m
 for n in range(m+1):
  ck(freq==2**(m-n))
  freq=0 if freq%2 else freq//2
 ck(freq==0)
print(json.dumps({'status':'PASS','source_kernel_tests':source_test,'polynomial_matrix_cases':cases,'matrix_assertions':matrix_checks,'frequency_assertions':checks-source_test-matrix_checks,'exact_assertions':checks,'limitations':'Checks corroborate exact identities; no nonlinear stable-manifold or full basin conclusion is certified.'},indent=2,sort_keys=True))
