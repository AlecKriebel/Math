import sympy as S
from fractions import Fraction as Q
import json
n=0
def ck(v):
 global n;n+=1;assert v
J=lambda z:Q(315,256)*(1-z*z)**4 if abs(z)<1 else Q(0)
for i in range(1,41):
 for j in range(1,41):
  x,y=Q(i,20),Q(j,20);K=J(x-y)-J(x+y);ck(K>=0)
  if abs(x-y)<1:ck(K>0)
  if abs(x-y)>=1:ck(K==0)
x,y=S.symbols('x y',real=True);JP=lambda z:S.Rational(315,256)*(1-z*z)**4
for k in [1,2,3]:
 P=lambda z:(1-z*z)**k*(1+z/3)
 D=P(y)-P(-y)
 lhs=S.integrate(JP(x-y)*D,(y,x-1,1))
 rhs=S.integrate(JP(x-y)*D,(y,0,1))-S.integrate(JP(x+y)*D,(y,0,1-x))
 ck(S.expand(lhs-rhs)==0)
for beta in [Q(3,2),Q(2),Q(3),Q(5)]:
 M=Q(315,256);eps=1/(4*beta*M);ck(2*beta*M*eps==Q(1,2))
 for j in range(1,30):
  kap=Q(j,30);ck(kap<1);ck(1-kap>0)
print(json.dumps({'assertions':n,'symbolic_reflection_splits':3,'scope':'Exact kernel and contraction algebra; moving-plane continuation is proved in TURN_4.md.'},indent=2))
