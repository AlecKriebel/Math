#!/usr/bin/env python3
"""Exact algebra and scope controls; not a numerical plate-positivity proof."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from math import factorial
from collections import Counter
import json
import sympy as S
C=Counter()
def ck(g,v):
 assert v,g
 C[g]+=1
x,y,p,q,r,sigma=S.symbols('x y p q r sigma',real=True)
Q=p*p+q*q+2*sigma*p*q+2*(1-sigma)*r*r
ck('hessian_decomposition',S.expand(Q-((1+sigma)*(p+q)**2/2+(1-sigma)*(p-q)**2/2+2*(1-sigma)*r*r))==0)
ck('determinant_form',S.expand(Q-((p+q)**2-2*(1-sigma)*(p*q-r*r)))==0)
ck('steklov_lower_bound_identity',S.expand((p+q)**2-4*(p*q-r*r)-((p-q)**2+4*r*r))==0)
for sig in [F(i,10) for i in range(-9,10)]:
 for pp in range(-2,3):
  for qq in range(-2,3):
   for rr in range(-2,3):
    value=pp*pp+qq*qq+2*sig*pp*qq+2*(1-sig)*rr*rr
    ck('coercivity_control',value>=(1-abs(sig))*(pp*pp+qq*qq+2*rr*rr))

# Integrate polynomial identities on the unit disk and its boundary, divided by pi.
def disk(poly):
 out=S.Rational(0)
 for (a,b),coef in S.Poly(S.expand(poly),x,y).terms():
  if a%2 or b%2:continue
  a//=2;b//=2
  out+=coef*S.Rational(factorial(2*a)*factorial(2*b),4**(a+b)*factorial(a)*factorial(b)*factorial(a+b+1))
 return S.simplify(out)
def circle(poly):
 out=S.Rational(0)
 for (a,b),coef in S.Poly(S.expand(poly),x,y).terms():
  if a%2 or b%2:continue
  a//=2;b//=2
  out+=coef*S.Rational(2*factorial(2*a)*factorial(2*b),4**(a+b)*factorial(a)*factorial(b)*factorial(a+b))
 return S.simplify(out)
polys=[x**a*y**b for a in range(5) for b in range(5-a)]
polys += [1+x+y,1-2*x+3*y*y,x*x-x*y+y*y]
for P in polys:
 u=(1-x*x-y*y)*P
 ux=S.diff(u,x,2);uy=S.diff(u,y,2);uxy=S.diff(u,x,y)
 determinant=ux*uy-uxy**2
 boundary=4*circle(P*P)
 ck('disk_boundary_identity',2*disk(determinant)==boundary)
 ck('weighted_steklov_control',disk((ux+uy)**2)>=2*boundary)
ck('disk_sharp_steklov_constant',disk(S.Integer(16))==2*circle(S.Integer(4)))

# Nonstrict boundary normal comparison suffices for the energy argument.
for un in [F(i,3) for i in range(-6,7)]:
 for extra in [F(0),F(1,5),F(2)]:
  wn=-abs(un)-extra
  ck('normal_trace_square',wn<=un and wn<=-un and wn*wn>=un*un)
  for sig in [F(-9,10),F(0),F(9,10)]:
   for curvature in [F(0),F(1,2),F(2)]:
    ck('boundary_energy_comparison',-(1-sig)*curvature*(wn*wn-un*un)/2<=0)

t=S.symbols('t',real=True)
graph=S.sqrt(1-t*t)
ck('stadium_tangent_match',S.limit(graph,t,0,dir='+')==1 and S.limit(S.diff(graph,t),t,0,dir='+')==0)
ck('stadium_not_C2',S.limit(S.diff(graph,t,2),t,0,dir='+')==-1)
for rad in [F(1),F(2),F(3,2)]:
 ck('annular_curvature_signs',F(1,1)/rad>0 and -F(1,1)/rad<0)

# These are hypothetical theorem constants, never computed constants of the annulus.
for d1 in [F(1,3),F(1),F(5)]:
 for dc in [F(-1,7),F(-1),F(-3),None]:
  eta=min(d1,F(1),-dc if dc is not None else F(1))/2
  for K in [F(1,2),F(1),F(4)]:
   epsilon=min(F(1),eta/(1+K))
   for frac in [F(1,4),F(1,2),F(3,4)]:
    sig=1-epsilon*frac
    ck('near_Navier_parameter',-1<sig<1 and 1-epsilon<sig)
    for kap in [-K,F(0),K]:
     alpha=(1-sig)*kap
     ck('boundary_coefficient_window',-eta<alpha<eta<d1 and (dc is None or dc<alpha))

root=Path(__file__).resolve().parent
out={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'artifact_sha256':sha256((root/'PARTIAL_SOURCE_AUDIT.md').read_bytes()).hexdigest(),'scope':'Exact energy, boundary-identity, regularity and abstract parameter-window diagnostics only; no computation of an annular Green function or its critical constants.'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
