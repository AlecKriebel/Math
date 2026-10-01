#!/usr/bin/env python3
"""Exact controls for the uniform-rate uniqueness proof and the route obstruction."""
from pathlib import Path
from collections import Counter
import sympy as s,json
C=Counter()
def ck(cat,test):
 assert test,cat
 C[cat]+=1
z=s.symbols('z');e,nu,q,a=s.symbols('e nu q a',positive=True)
ss=q*e/(nu+q*e)
for N in range(1,31):
 # Algebra in s: terminal fraction and total receptor-complex sum.
 total=sum(z**i for i in range(N))+z**N/(1-z)
 ck('geometric_total_identity',s.cancel(total-1/(1-z))==0)
 ck('terminal_fraction_identity',s.cancel((z**N/(1-z))/total-z**N)==0)
 derivative=1-z**N-N*z**N*(1-z)
 positive=(1-z)*sum(z**j-z**N for j in range(N))
 ck('positive_derivative_decomposition',s.expand(derivative-positive)==0)
 for rational in [s.Rational(1,100),s.Rational(1,4),s.Rational(1,2),s.Rational(3,4),s.Rational(99,100)]:
  ck('derivative_positive_controls',derivative.subs(z,rational)>0)
 if N<=8:
  theta=a*e*(1-ss**N)
  ck('theta_differentiation',s.cancel(s.diff(theta,e)-a*derivative.subs(z,ss))==0)
# Derive the negative-cycle Jacobian from the original homogeneous N=2 ODE.
r,c0,c1,c2,b0,b1,E,D,u,v,w=s.symbols('r c0 c1 c2 b0 b1 E D u v w',real=True)
kap=s.symbols('kap');ee=E-b0-b1;f=kap*r*(r+D)
F=s.Matrix([-f+nu*(c0+c1+c2),f-nu*c0-u*ee*c0+v*b0,w*b0-nu*c1-u*ee*c1+v*b1,w*b1-nu*c2,u*ee*c0-(v+w)*b0,u*ee*c1-(v+w)*b1])
vars=s.Matrix([r,c0,c1,c2,b0,b1]);J=F.jacobian(vars)
for j in range(6):ck('ambient_zero_column_sums',s.expand(sum(J[:,j]))==0)
ck('cycle_B0_to_C1',s.expand(J[2,4]-(w+u*c1))==0)
ck('cycle_C1_to_B1',s.expand(J[5,2]-u*ee)==0)
ck('cycle_B1_to_B0',s.expand(J[4,5]+u*c0)==0)
ck('negative_cycle_product',s.expand(J[2,4]*J[5,2]*J[4,5]+(w+u*c1)*u*ee*u*c0)==0)
# All 2^3 sign switches retain that directed cycle's product sign.
for s1 in [-1,1]:
 for s2 in [-1,1]:
  for s3 in [-1,1]:ck('sign_switch_cycle_invariance',(s1*s2)*(s2*s3)*(s3*s1)==1)
out={'status':'PASS_EXACT','assertions':sum(C.values()),'categories':dict(C),'scope':'Supporting identities and obstruction only; no global convergence theorem for N>=2','numeric_eigenvalue_claim':False}
Path(__file__).with_name('shared_rates_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
