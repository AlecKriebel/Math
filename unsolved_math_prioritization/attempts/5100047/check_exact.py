#!/usr/bin/env python3
"""Exact symbolic/rational controls for k806,a; not a substitute for the pole proof."""
import sympy as S
from fractions import Fraction as F
from math import gcd
import json
counts={}
def ck(v,label):
 counts[label]=counts.get(label,0)+1
 if not v:raise AssertionError(label)
k,h,x,C,d,y,z=S.symbols('k h x C d y z')
t=h*h;q=1-t;m=k*k
U=1-2*m*t+m*t*t;V=1-2*t+m*t*t;W=1-m*t*t
D=1-m*t*x*x
# Exact quotient-ring reduction: cn(v)^2, dn(v)^2, cn(u)^2, dn(u)^2.
def red(e):
 n=S.fraction(S.cancel(e))[0]
 for var,val in [(C,1-h*h),(d,1-k*k*h*h),(y,1-x*x),(z,1-k*k*x*x)]:
  n=S.rem(S.Poly(n,var),S.Poly(var*var-val,var)).as_expr();n=S.expand(n)
 return S.factor(n)
def eq(a,b,label):ck(red(a-b)==0,label)
sp=(x*C*d+h*y*z)/D;sm=(x*C*d-h*y*z)/D
cp=(y*C-x*h*z*d)/D;cm=(y*C+x*h*z*d)/D
# Normalize alpha=1; beta factors cancel in determinant comparisons.
a=d/C; beta2=1-k*k
aprod=(a+k*sm)*(a+k*sp)
eq(aprod,(1+k*x)*(U+k*V*x)/(q*D),'original_focal_product')
det_original=(-a*sm-k)*cp-(-a*sp-k)*cm
eq(det_original,2*h*d*z*(1+k*x)/D,'original_translated_determinant_div_b')
# Outer locus and its exact distance factor.
Ao=d*d/q
outer_norm=(Ao*x+k)**2+beta2*(1-x*x)/q**2
eq(outer_norm,(1+k*x)*(U+k*V*x)/q**2,'outer_distance_factor')
L0=(U*U-m*V*V*t)/d;L1=(V*V-U*U*t)/C
O=(-Ao*sm-k)*cp-(-Ao*sp-k)*cm
eq(O,2*h*d*z*(d+k*C*x)/(C*D),'outer_determinant_div_Bo')
eq((1+k*sm)*(1+k*sp),(d+k*C*x)**2/D,'outer_first_distance_product')
eq((U+k*V*sm)*(U+k*V*sp),(d+k*C*x)*(L0+k*L1*x)/D,'outer_second_distance_product')
Z=W*W-4*m*t*t*q*(1-m*t)
D3=U*W-2*m*t*q*V;C3=V*W-2*t*(1-m*t)*U
eq(U*U-m*V*V*t,d*d*D3,'triple_dn_numerator')
eq(V*V-U*U*t,C*C*C3,'triple_cn_numerator')
eq(L0*L0-m*L1*L1,(1-m)*Z*Z,'triple_strict_gap')
eq(U+V,2*q*d*d,'UV_sum');eq(U-V,2*t*(1-m),'UV_difference')
eq(U*U-m*V*V,(1-m)*W*W,'UV_strict_gap')
eq(Z,W*W*(1-m*t*(2*h*C*d/W)**2),'triple_addition_denominator')
# Complete rational edge identities using the component equalities just checked.
orig_edge=det_original/(2*aprod**2)
# Left side is divided by b; right side C_P/b=h*d*q^2.
eq(orig_edge,h*d*q*q*z*D/((1+k*x)*(U+k*V*x)**2),'original_edge_identity')
outer_Dminus=(1+k*sm)*(U+k*V*sm)/q**2
outer_Dplus=(1+k*sp)*(U+k*V*sp)/q**2
# Here each determinant is divided by Bo; C_Q/Bo=h*d*q^4/C.
eq(O/(2*outer_Dminus*outer_Dplus),h*d*q**4*z*D/(C*(d+k*C*x)**2*(L0+k*L1*x)),'outer_edge_identity')
# N4 paired simplification, independent of the V=0 relation beyond the edge formula.
eq(z*D*(1/(1+k*x)+1/(1-k*x)),2*(q/z+t*z),'N4_pair_identity')
# Finite rational lattice controls for every primitive orientation in this range.
for N in range(3,101):
 for tau in range(1,(N+1)//2):
  if gcd(N,tau)!=1:continue
  v=F(2*tau,N);delta=2*v;ell=F(4,N);r=F(3)
  ck(delta/ell==tau,'real_period_lattice')
  ck(((r+delta-r)/ell).denominator==1,'original_pole_class_plus')
  ck(((r-delta-r)/ell).denominator==1,'original_pole_class_minus')
  for s in (-3,-1,1,3):ck(((r+s*v-(r+v))/ell).denominator==1,'outer_pole_class')
  ck((v==F(1,2))==(N==4 and tau==1),'N4_exception_unique')
  ck((3*v==2)==(N==3 and tau==1),'N3_exception_unique')
  ck((3*v==1)==(N==6 and tau==1),'N6_exception_unique')
  # Reflection pairs have equal counts at every reduced pole, not just equal locations.
  plus=[(r+delta-j*delta)%4 for j in range(N)]
  minus=[(r-delta-j*delta)%4 for j in range(N)]
  ck(sorted(plus)==sorted(minus),'original_double_multiplicity')
  plus=[(r+v-j*delta)%4 for j in range(N)]
  minus=[(r-v-j*delta)%4 for j in range(N)]
  ck(sorted(plus)==sorted(minus),'outer_double_multiplicity')
ck(F(3)+F(1,3)==5*F(2,3),'N6_extra_pole_alignment');ck(F(2)==3*F(2,3),'N6_other_extra_pole_alignment')
# Exact focus geometry and reflection for infinitely many rational-axis test instances.
def ar(P):return sum(x*v-y*u for (x,y),(u,v) in zip(P,P[1:]+P[:1]))/2
def invert(P,c):
 out=[]
 for x,y in P:
  x=F(x)-c;y=F(y);den=x*x+y*y;ck(den>0,'real_inverse_nonzero');out.append((x/den,y/den))
 return out
examples=[]
for R in range(2,18):
 for T in range(1,R):
  a=F(R*R+T*T);b=F(2*R*T);c=F(R*R-T*T)
  P=[(0,b),(-a,0),(0,-b),(a,0)];Q=[(-a,b),(-a,-b),(a,-b),(a,b)]
  # Strict confocal four-caustic axes squared; tangent discriminant vanishes.
  al2=a**4/(a*a+b*b);be2=b**4/(a*a+b*b)
  ck(al2-be2==c*c and 0<be2<b*b and 0<al2<a*a,'N4_strict_confocal_caustic')
  for (x0,y0),(x1,y1) in zip(P,P[1:]+P[:1]):
   dx=x1-x0;dy=y1-y0
   aa=dx*dx/al2+dy*dy/be2;bb=2*(x0*dx/al2+y0*dy/be2);cc=x0*x0/al2+y0*y0/be2-1
   ck(bb*bb-4*aa*cc==0,'N4_caustic_tangency')
   ck(0<-bb/(2*aa)<1,'N4_interior_contact')
  for focus in (c,-c):
   AP=ar(invert(P,focus));BQ=ar(invert(Q,focus))
   ck(AP==2/(a*b),'N4_original_inverse_area')
   ck(BQ==1/(a*b),'N4_outer_inverse_area')
   ck(BQ/AP==F(1,2),'N4_displayed_ratio_half')
  if (R,T)==(2,1):examples.append({'a':str(a),'b':str(b),'c':str(c),'A_inverse':str(AP),'B_inverse':str(BQ),'ratio':str(BQ/AP)})
# Explicit rational a=5,b=3 instance named in the proof.
P=[(0,F(3)),(F(-5),0),(0,F(-3)),(F(5),0)];Q=[(F(-5),F(3)),(F(-5),F(-3)),(F(5),F(-3)),(F(5),F(3))]
ck(ar(invert(P,F(4)))==F(2,15),'rational_source_typo_original');ck(ar(invert(Q,F(4)))==F(1,15),'rational_source_typo_outer')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':counts,'scope':'Exact polynomial identities, rational phase/multiplicity and geometric controls. The complex pole completeness and compactness argument are mathematical proof, not finite enumeration.','N4_displayed_ratio':'1/2','examples':examples},indent=2,sort_keys=True))
