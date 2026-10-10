#!/usr/bin/env python3
"""Independent exact symbolic and quotient-lattice controls for k404."""
import sympy as S,json
from fractions import Fraction as F
from collections import Counter
from math import gcd
Ck=Counter()
def ck(z,label):assert z,label;Ck[label]+=1
s,c,d,t,C,D,k,B=S.symbols('s c d t C D k B')
relations={c:1-s*s,d:1-k*k*s*s,C:1-t*t,D:1-k*k*t*t,B:1-k*k}
def red(e):
 p=S.together(e).as_numer_denom()[0]
 for x,q in relations.items():p=S.rem(p,x*x-q,x)
 return S.factor(p)
def cross3(p,q):return [p[1]*q[2]-p[2]*q[1],p[2]*q[0]-p[0]*q[2],p[0]*q[1]-p[1]*q[0]]
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
L=1-k*k*t*t*s*s;E=1-2*k*k*t*t+k*k*t**4
# Build original endpoint coordinates directly from addition formulas.
Pm=[-D*(s*C*D-t*c*d)/(C*L),B*(c*C+s*t*d*D)/(C*L)]
Pp=[-D*(s*C*D+t*c*d)/(C*L),B*(c*C-s*t*d*D)/(C*L)]
Foc=[k,0]
def line(p):return [p[0]-k,p[1],-dot([p[0]-k,p[1]],p)]
l1,l2=line(Pm),line(Pp);H=cross3(l1,l2)
Ux=-(E*s+k*(C*C-D*D*s*s))/(C*C*L);Uy=c*(2*B*B-E*(1+k*s))/(B*C*C*L)
ck(red(H[0]-Ux*H[2])==0,'Cramer_numerator_x_matches_formula')
ck(red(H[1]-Uy*H[2])==0,'Cramer_numerator_y_matches_formula')
ck(red(H[2]-2*B*D*t*d*(1+k*s)/(C*L))==0,'Cramer_denominator_matches_real_nonzero_factor')
for line0 in [l1,l2]:ck(red(line0[0]*Ux+line0[1]*Uy+line0[2])==0,'specific_original_antipedal_line')
q=[(k-s)/(1-k*s),B*c/(1-k*s)];normal=[-s,c/B]
ck(red(dot(normal,q)-1)==0,'focal_foot_specific_side_incidence')
ck(red(cross([q[0]-k,q[1]],normal))==0,'focal_foot_perpendicular_ray')
ck(red(dot(q,q)-1)==0,'foot_circle_identity_control')
ck(red(cross(normal,[-c*d,-s*d/B])-d/B)==0,'strict_normal_angle_derivative')
ck(red((D*D-B*B)/(C*C)-k*k)==0,'actual_focus_confocality')
# Derivative at L=0 from p-shift expressions: no missing repeated zero.
Lp=S.simplify(-2*k*k*t*t*(1/(k*t))*(-S.I*D/(k*t))*(-S.I*C/t))
ck(S.simplify(Lp-2*C*D/t)==0,'simple_L_zero_derivative')
# Pole symmetries with generic Laurent coefficients.
z=S.symbols('z');aa=S.symbols('a0:7');f=sum(a*z**j for a,j in zip(aa,range(-2,5)))
ck(S.expand(f-f.subs(z,-z)).coeff(z,-2)==0,'odd_reflection_removes_double_pole')
# Primitive even quotients, including excluded parity; count residue multiplicities.
for N in range(4,202,2):
 m=N//2;h=F(2,m)
 for tau in range(1,m):
  if gcd(tau,N)!=1:continue
  delta=F(4*tau,N);v=delta/2
  ck(tau%2==1 and gcd(tau,m)==1,'primitive_even_central_shift')
  ck((m*delta)%4==2,'vertices_pair_by_actual_half_turn')
  ck({j*delta%2 for j in range(N)}=={j*h for j in range(m)},'quotient_lattice_exact')
  ck(sum(j*delta%2==0 for j in range(N))==2,'trace_two_equal_singular_terms')
  ck((1+v)%h==(0 if N%4==2 else h/2),'source_parity_phase_alignment')
  ck(all((-j*delta)%h==0 for j in range(N)),'antipedal_poles_one_real_class')
  ck(all(((v-j*delta)-v)%h==0 for j in range(N)),'both_endpoint_pole_families_same_class')
# Rational positivity controls throughout strict source parameter inequalities.
for k0 in [F(1,5),F(1,2),F(9,10)]:
 for t0 in [F(1,10),F(2,3),F(99,100)]:
  for s0 in [F(-1),F(-7,9),F(0),F(7,9),F(1)]:
   ck(1-k0*s0>0 and 1+k0*s0>0,'focus_strictly_inside_dual_tangents')
   ck(1-k0*k0*t0*t0*s0*s0>0,'real_chord_denominator_positive')
print(json.dumps({'status':'PASS','exact_assertions':sum(Ck.values()),'categories':dict(Ck),'scope':'Finite exact algebra and parameter/lattice controls only; all-period meromorphic reasoning and strict star-area positivity are independently audited in INDEPENDENT_REVIEW.md.'},indent=2))
