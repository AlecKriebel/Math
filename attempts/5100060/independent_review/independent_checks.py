#!/usr/bin/env python3
"""Independent input identities and direct N4 corollary controls."""
import sympy as S,json
from fractions import Fraction as F
from math import gcd
from collections import Counter
C=Counter()
def ck(x,k):assert x,k;C[k]+=1
s,c,d,h,Cv,Dv,k,B=S.symbols('s c d h Cv Dv k B')
rels={c:1-s*s,d:1-k*k*s*s,Cv:1-h*h,Dv:1-k*k*h*h,B:1-k*k}
def red(x):
 p=S.together(x).as_numer_denom()[0]
 for v,q in rels.items():p=S.rem(p,v*v-q,v)
 return S.factor(p)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def cross(p,q):return p[0]*q[1]-p[1]*q[0]
def hom(p,q):return[p[1]*q[2]-p[2]*q[1],p[2]*q[0]-p[0]*q[2],p[0]*q[1]-p[1]*q[0]]
def area(P):return sum(cross(P[j],P[(j+1)%len(P)]) for j in range(len(P)))/2
L=1-k*k*h*h*s*s;snm=(s*Cv*Dv-h*c*d)/L;snp=(s*Cv*Dv+h*c*d)/L
Pm=[-Dv/Cv*snm,B/Cv*(c*Cv+s*h*d*Dv)/L];Pp=[-Dv/Cv*snp,B/Cv*(c*Cv-s*h*d*Dv)/L]
Vm=[Pm[0]-k,Pm[1]];Vp=[Pp[0]-k,Pp[1]];dm=Dv/Cv+k*snm;dp=Dv/Cv+k*snp
U=1-2*k*k*h*h+k*k*h**4;V=1-2*h*h+k*k*h**4;W=1-k*k*h**4;cc=B*h*Dv*Cv**3
ck(red(dot(Vm,Vm)-dm*dm)==0,'positive_focal_distance_squared_minus')
ck(red(dot(Vp,Vp)-dp*dp)==0,'positive_focal_distance_squared_plus')
ck(red(dm*dp-(1+k*s)*(U+k*V*s)/(Cv*Cv*L))==0,'inverse_input_distance_product')
ck(red(cross(Vm,Vp)-2*B*h*Dv*d*(1+k*s)/(Cv*L))==0,'inverse_input_actual_focal_cross')
Ep=cc*d*L/((1+k*s)*(U+k*V*s)**2)
ck(red(Ep*2*dm**2*dp**2-cross(Vm,Vp))==0,'inverse_edge_area_formula_from_actual_vertices')
Em=Ep.subs(s,-s)
paired=2*cc*L*(U*U+k*k*V*(V+2*U)*s*s)/(d*(U*U-k*k*V*V*s*s)**2)
ck(red(Ep+Em-paired)==0,'antipodal_inverse_pair_rational_identity')
ck(S.expand(U*U-k*k*V*V-(1-k*k)*W*W)==0,'no_real_inverse_pole_factor')
ck(S.expand(U-V-2*h*h*(1-k*k))==0,'simple_dn_zero_not_new_denominator_zero')
ck(S.expand(U+V-2*(1-h*h)*(1-k*k*h*h))==0,'positive_U_plus_V')
ck(red(L-((1-h*h)+h*h*d*d))==0,'N4_special_inverse_summand')
for N in range(4,205,4):
 m=N//2;ell=F(2,m)
 for t in range(1,N//2):
  if gcd(N,t)!=1:continue
  delta=F(4*t,N);v=delta/2
  ck((1+v)%ell==ell/2,'inverse_input_exact_half_shift')
  ck(sum(j*delta%2==0 for j in range(m))==1,'half_trace_nonzero_residue_multiplicity')
  ck((delta==1)==(N==4),'N4_only_generic_pole_collision')
  if N>4:
   ck((delta-(-delta))%2!=0,'generic_shifted_poles_distinct')
   ck(sum((j*delta-delta)%2==0 for j in range(m))==1 and sum((j*delta+delta)%2==0 for j in range(m))==1,'double_poles_pair_once_each')
# Actual rational 3-4-5 focal geometry, plus exact radius-scaling controls.
for a,b,f in [(F(5),F(3),F(4)),(F(13),F(5),F(12)),(F(17),F(15),F(8))]:
 P=[(F(0),b),(-a,F(0)),(F(0),-b),(a,F(0))]
 for focus in [f,-f]:
  inv=[];ant=[]
  for j,p in enumerate(P):
   q=P[(j+1)%4];v=(p[0]-focus,p[1]);w=(q[0]-focus,q[1]);rr=dot(v,v)
   ck(rr>0,'exact_N4_inversion_finite')
   inv.append((focus+v[0]/rr,v[1]/rr));ll=(*v,-dot(v,p));mm=(*w,-dot(w,q));R=hom(ll,mm);U0=(R[0]/R[2],R[1]/R[2]);ant.append(U0)
   ck(dot(v,U0)==dot(v,p) and dot(w,U0)==dot(w,q),'exact_N4_specific_antipedal_lines')
  ck(area(P)==2*a*b,'exact_N4_original_area')
  ck(area(inv)==2/(a*b),'exact_N4_inverse_area')
  ck(area(ant)==4*a*b,'exact_N4_antipedal_area')
  ck(area(inv)*area(ant)==8,'exact_N4_source_product')
  scaled=[(focus+4*(x-focus),4*y) for x,y in inv]
  ck(area(scaled)==16*area(inv),'radius_two_fourth_power')
A,IV,kappa=S.symbols('A IV kappa')
ck(S.expand(IV*(kappa*A)-kappa*(A*IV))==0,'corollary_no_division_identity')
ck((IV*(kappa*A)).subs(kappa,0)==0,'zero_antipedal_scalar_harmless')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Independent exact identities for the inverse input, pole-index arithmetic and direct focal N4 constructions. Full dependency and analytic/source scope are audited in INDEPENDENT_REVIEW.md.'},indent=2))
