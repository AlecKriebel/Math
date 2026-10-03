#!/usr/bin/env python3
"""Exact supplementary controls; the continuum argument is in TURN_1.md."""
import json
from fractions import Fraction as F
from math import comb
import sympy as s
N=0
def check(b):
 global N
 assert b;N+=1
r,R,m,L=s.symbols('r R m L',positive=True)
# Conformal volume and radius first-order coefficients, formal in inverse radius.
z=s.symbols('z');mu=s.symbols('mu')
check(s.expand((1+mu*z/2)**6).coeff(z,1)==3*mu)
I=2*s.pi*(R**2-(L*R)**2/3)
V=4*s.pi*R**3/3+3*mu*I
coefficient=s.simplify((V-4*s.pi*R**3/3)/(4*s.pi*R**2))
check(s.simplify(coefficient-mu*(3-L**2)/2)==0)
check(s.simplify(coefficient-mu/2-mu*(1-L**2/2))==0)
check((mu*(1-L**2/2)).subs({mu:-2,L:s.Rational(1,2)})==-s.Rational(7,4))
# Solid-ball shell calculation; all angular integrals use exact antiderivatives.
d=s.symbols('d',positive=True);rho=s.symbols('rho',positive=True)
shell=4*s.pi*(s.integrate(rho**2/d,(rho,0,d))+s.integrate(rho,(rho,d,R)))
check(s.simplify(shell-2*s.pi*(R**2-d**2/3))==0)
check(s.integrate(4*s.pi*R**2/rho**3,(rho,R,s.oo))==2*s.pi)
check(s.integrate(16*s.pi*R**2/rho**4,(rho,R,s.oo))/(4*s.pi)==4/(3*R))
# ADM coefficient and flux of a quotient expansion.
u=1+mu/(2*r)
check(s.limit(-2*r*r*u**3*s.diff(u,r),r,s.oo)==mu)
check(s.limit(((1-R/r)/u-1)*r,r,s.oo)==-(R+mu/2))
# Cubic mass and radius deficit equivalence factor tends to one.
a,c=s.symbols('a c',positive=True)
check(s.simplify((a**3-c**3)/(3*c**2)-(a-c)*(a*a+a*c+c*c)/(3*c*c))==0)
check(((a*a+a*c+c*c)/(3*c*c)).subs(a,c)==1)
# Exact rational nestedness and strict negative-mass separation.
for q in range(2,31):
 for p in range(1,q):
  lam=F(p,q)
  for M in (F(-1,3),F(-2),F(-7,2)):
   value=M*(1-lam*lam/2)
   check(value>M)
   check(value-M==-M*lam*lam/2)
  for rr,ss in ((F(6),F(7)),(F(8),F(20)),(F(100),F(100))):
   check(lam*(ss-rr)+rr<=ss)
   check((1-lam)*rr>0)
# Uniform algebraic remainder estimate used for the volume integral.
for j in range(3,301):
 x=F(1,j)
 rem=(1-x)**6-1+6*x
 check(abs(rem)<=57*x*x)
print(json.dumps({'status':'PASS','exact_assertions':N,'dependency':'SymPy','scope':'Exact scalar identities, asymptotic coefficients, nestedness and sign controls; not a numerical evaluation of global capacity-volume mass.'},indent=2,sort_keys=True))
