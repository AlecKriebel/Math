"""Exact algebra controls for the final scalar transform and sector Schur estimate."""
import sympy as s
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(x,k):
 assert x,k
 C[k]+=1
A,B,p,lam,c,v,vp,P,w,Lambda,b,z,q,V=s.symbols('A B p lam c v vp P w Lambda b z q V',real=True)
Apr=lam-A*A-2*A*B+A*p
J=A+2*B-p
ck(s.expand(Apr+J*A-lam)==0,'weighted_log_warp_Poisson_identity')
Hw=c*(Apr+J*A)+(2-c*c)*A*A
ck(s.expand(Hw-(c*lam+(2-c*c)*A*A))==0,'positive_power_solution_formula')
ck(s.simplify(Hw.subs(c,s.sqrt(2))-s.sqrt(2)*lam)==0,'sqrt_two_exact_solution')
# q=w*v; (log(P*w*w))'=J-2*c*A.
left=-2*c*A*v*vp+((c*c+2)*A*A-c*lam)*v*v
boundary=-2*c*A*v*vp-c*(Apr+(J-2*c*A)*A)*v*v
ck(s.expand(left-boundary-(2-c*c)*A*A*v*v)==0,'ground_transform_divergence_identity')
ck(s.simplify((left-boundary).subs(c,s.sqrt(2)))==0,'ground_transform_exact_square')
ck(s.expand((Lambda/b**2+Hw)-(Lambda/b**2+c*lam+(2-c*c)*A*A))==0,'spherical_potential')
ck(s.expand(lam-A*A-Apr-(2*A*B-A*p))==0,'Riccati_comparison_residual')
ck(s.expand(z*z/V-(2*z*q-V*q*q)-(z-V*q)**2/V)==0,'variational_inverse_bound_square')
ck(s.simplify(1/(s.sqrt(2)*s.Rational(1,2))-s.sqrt(2))==0,'target_inverse_normalization')
ck(s.simplify(4/(s.sqrt(2)*s.Rational(1,2))-4*s.sqrt(2))==0,'target_Schur_normalization')
# The power-law lower bound proving non-integrability has exponent > -1.
ck(3-2*s.sqrt(2)>-1,'formal_solution_not_L2_power_test')
for av,bv,pv,lv in product([F(0),F(1,3),F(2,3)],[F(1,4),F(1),F(3)],[-F(2),-F(1,2),F(0)],[F(1,2),F(1),F(2)]):
 ap=lv-av*av-2*av*bv+av*pv;j=av+2*bv-pv
 ck(ap+j*av==lv,'rational_log_warp_identity')
 ck(ap<=lv-av*av,'rational_Riccati_comparison')
 for cv in [F(0),F(1,2),F(1),F(3,2),F(2)]:
  ck(cv*(ap+j*av)+(2-cv*cv)*av*av==cv*lv+(2-cv*cv)*av*av,'rational_power_identity')
# Resolvent order for V positive diagonal and H=V+M^t M, exact principal minors.
for x,y,z0,t in product(range(-2,3),repeat=4):
 M=s.Matrix([[x,y],[z0,t]])
 for v1,v2 in [(1,1),(1,2),(2,3),(3,1)]:
  D=s.diag(v1,v2);H=D+M.T*M;R=D.inv()-H.inv()
  ck(R==R.T and R[0,0]>=0 and R[1,1]>=0 and R.det()>=0,'exact_resolvent_order')
  for z1,z2 in [(1,0),(0,1),(1,1),(1,-2)]:
   zz=s.Matrix([z1,z2]);cor=(zz.T*H.inv()*zz)[0];upper=(zz.T*D.inv()*zz)[0]
   ck(0<=cor<=upper,'exact_sector_Schur_upper_bound')
# One positive scalar block with a negative effective tensor block.
K=s.Matrix([[1,2],[2,2]])
ck(K.det()==-2 and K.trace()==3,'positive_scalar_does_not_force_coupled_positivity')
ck(1-F(4,2)==-1,'negative_effective_countercontrol')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact identities and finite block controls only. Analytic form domains, known soliton input, and the unresolved tensor/global-degree gaps are in TURN_5.md.'},sort_keys=True,indent=2))
