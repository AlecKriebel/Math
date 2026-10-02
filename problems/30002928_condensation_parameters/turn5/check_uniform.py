from fractions import Fraction as Q
import sympy as S
import json
n=0
def ck(x):
 global n;n+=1;assert x
for M in range(1,11):
 for L in range(1,11):
  for C in range(1,11):
   r=Q(1,8*M*L);delta=min(r/(4*M*C),Q(1,8*M*L))
   ck(M*L*(r+delta)<Q(1,2));ck(M*C*delta<=r/2)
# Normalizing a positive subdensity with loss ell costs exactly another ell in L1.
for den in range(2,101):
 for k in range(1,den):
  ell=Q(k,den);mass=1-ell;ck((1/mass-1)*mass==ell)
# Scaling convolution variables: R J(R(x-y)) q(Ry) dy -> J(Rx-z)q(z)dz.
R,x,z=S.symbols('R x z',positive=True);ck(S.simplify(R*(x-z/R)-(R*x-z))==0);ck(S.simplify(R/R)==1)
for neg in range(1,101):
 for pos in range(neg):
  delta=neg-pos;ck(neg>=delta)
print(json.dumps({'assertions':n,'uniform_contraction_fixtures':1000,'scope':'Exact bookkeeping only; uniform Banach theorem and physical-kernel construction are proved in TURN_5.md.'},indent=2))
