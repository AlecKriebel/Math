#!/usr/bin/env python3
"""Independent exact controls for the quadratic projection obstruction."""
import sympy as S
from fractions import Fraction as F
from collections import Counter
import json
count=Counter()
def ck(v,n):
 assert v,n
 count[n]+=1
def eq(a,b,n):ck(S.simplify(a-b)==0,n)
t=S.symbols('t',positive=True,real=True);z=S.symbols('z');ii=S.I
p=z*z+t*t*z+t*t+ii*t**3
expansion=(z+ii*t)*(z+t*t-ii*t)
eq(p,expansion,'exact_factorization')
lam=-ii*t;D=2*lam+t*t;scale=2/(t*(t*t+4))
vec=[]
for x in [lam,1]:
 deriv=-x/D
 vec.extend([S.simplify(S.re(deriv)),S.simplify(S.re(ii*deriv))])
n=S.Matrix([-t,-t*t/2,-t/2,1])
for x,y in zip(vec,scale*n):eq(x,y,'full_four_coordinate_root_derivative')
lvec=[S.re(-lam*lam/D),S.re(-ii*lam*lam/D)]
N=S.Matrix([t**3/2,-t*t,*n])
for x,y in zip(lvec+vec,scale*N):eq(x,y,'full_six_coordinate_root_derivative')
x,y,u,v=S.symbols('x y u v',real=True)
phi=v-x*y/2-x*S.sqrt(u+y*y/4)
for j,c in enumerate([x,y,u,v]):eq(S.diff(phi,c).subs({x:t*t,y:0,u:t*t,v:t**3}),n[j],'independent_stability_chart_normal')
q=p.subs(t,S.sqrt(2)*t)
delta=S.Matrix([t*t,0,t*t,(2*S.sqrt(2)-1)*t**3])
coef=2*S.sqrt(2)-S.Rational(5,2)
eq(n.dot(delta),coef*t**3,'positive_support_defect')
eq(delta.dot(delta),2*t**4+(2*S.sqrt(2)-1)**2*t**6,'displacement_order_four')
ck(8>S.Rational(25,4),'strict_positive_coefficient_squared')
eq(S.limit(t*n.dot(delta)/delta.dot(delta),t,0,dir='+'),coef/2,'exact_divergence_rate')
Ndelta=S.Matrix([0,0,*delta]);eq(N.dot(Ndelta),n.dot(delta),'nonmonic_defect_unchanged')
# Exact epigraph scaling and its horizontal limiting direction.
epi=S.Matrix([*n,-t*(t*t+4)/2]);grad=S.Matrix([*vec,-1])
for a,b in zip(grad,scale*epi):eq(a,b,'full_epigraph_gradient_scaling')
for a,b in zip(epi,[0,0,0,1,0]):eq(S.limit(a,t,0,dir='+'),b,'horizontal_epigraph_limit')
eq(epi.dot(S.Matrix([*delta,0])),n.dot(delta),'epigraph_defect_unchanged')
ck(S.limit(vec[-1],t,0,dir='+')==S.oo,'unscaled_gradient_not_finite')
# Stability chart inequality after shifting away imaginary linear coefficient.
shift=(z-ii*y/2)**2+(x+ii*y)*(z-ii*y/2)+u+ii*v
eq(shift,z*z+x*z+(u+y*y/4)+ii*(v-x*y/2),'imaginary_translation_preserves_root_real_parts')
X,U,V=S.symbols('X U V',real=True)
eq((X*X+4*U)**2-((X*X-4*U)**2+16*V*V),16*(X*X*U-V*V),'quadratic_stability_chart_squared_test')
# Metric covectors: explicit non-diagonal positive-definite examples in all ambient dimensions.
for dimension,normal,disp in [(4,n,delta),(6,N,Ndelta),(5,epi,S.Matrix([*delta,0]))]:
 for seed in range(1,8):
  A=S.eye(dimension)
  for j in range(dimension-1):A[j,j+1]=S.Rational(seed,j+seed+1)
  G=A.T*A+S.eye(dimension);Gn=G.inv()*normal
  eq((Gn.T*G*disp)[0],normal.dot(disp),'positive_definite_metric_covector_pairing')
  eq(S.limit((disp.T*G*disp)[0]/t**4,t,0,dir='+'),(S.Matrix([int(j in ([0,2] if dimension in [4,5] else [2,4])) for j in range(dimension)]).T*G*S.Matrix([int(j in ([0,2] if dimension in [4,5] else [2,4])) for j in range(dimension)]))[0],'metric_displacement_still_order_four')
# Rational/algebraic controls; no numerical projection solver is used.
for j in range(1,101):
 tt=S.Rational(1,j)
 ck(S.simplify(p.subs({z:-ii*tt,t:tt}))==0,'first_exact_boundary_root')
 ck(S.simplify(p.subs({z:-tt*tt+ii*tt,t:tt}))==0,'second_exact_interior_root')
 ck(-tt*tt<0,'strict_other_root_gap')
 ck(S.simplify(n.dot(delta).subs(t,tt))>0,'positive_exact_defect_at_rational_scale')
 ratio=S.simplify((t*n.dot(delta)/delta.dot(delta)).subs(t,tt))
 ck(ratio>coef/(2+(2*S.sqrt(2)-1)**2)/2,'uniform_positive_scaled_quotient')
# Real monic quadratic control by roots rather than using the complex counterexample.
for a in range(0,15):
 for b in range(0,15):
  disc=a*a-4*b
  if disc>=0:ck(S.sqrt(disc)<=a,'real_nonnegative_coefficients_stable_real_roots')
  else:ck(-S.Rational(a,2)<=0,'real_nonnegative_coefficients_stable_conjugate_roots')
print(json.dumps({'status':'PASS','exact_assertions':sum(count.values()),'categories':dict(count),'scope':'Exact identities, ambient normals, cubic-versus-quartic asymptotics and metric controls only. Projection equivalence, closed-set localization and original source scope are audited in the report. No explicit pair of nearest projections or finite-subgradient counterexample is asserted.'},indent=2))
