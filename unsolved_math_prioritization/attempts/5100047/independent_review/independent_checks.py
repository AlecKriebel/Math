#!/usr/bin/env python3
"""Independent exact reconstruction; finite controls supplement the analytic review."""
import sympy as S
from fractions import Fraction as F
from collections import Counter
from math import gcd
import json
counts=Counter()
def check(b,n):
 assert b,n
 counts[n]+=1
s,t,k,c,e,d,f,b=S.symbols('s t k c e d f b')
rels=[(c,1-s*s),(e,1-t*t),(d,1-k*k*s*s),(f,1-k*k*t*t),(b,1-k*k)]
def reduce(z):
 z=S.fraction(S.cancel(z))[0]
 for x,y in rels:z=S.Poly(z,x).rem(S.Poly(x*x-y,x)).as_expr().expand()
 return S.factor(z)
def eq(x,y,n):check(reduce(x-y)==0,n)
def det(x,y):return x[0]*y[1]-x[1]*y[0]
def dot(x,y):return x[0]*y[0]+x[1]*y[1]
q=1-t*t;den=1-k*k*s*s*t*t
snm=(s*e*f-t*c*d)/den;snp=(s*e*f+t*c*d)/den
cnm=(c*e+s*t*d*f)/den;cnp=(c*e-s*t*d*f)/den
# Normalize caustic major axis to one, retain independent beta radical.
a=f/e;B=b/e
Pminus=(-a*snm,B*cnm);Pplus=(-a*snp,B*cnp)
Q=(-f*f*s/q,b*c/q)
for P in [Pminus,Pplus]:eq(Q[0]*P[0]/(a*a)+Q[1]*P[1]/(B*B),1,'named_outer_tangent_incidence')
normalminus=(Pminus[0]/(a*a),Pminus[1]/(B*B));normalplus=(Pplus[0]/(a*a),Pplus[1]/(B*B))
eq(det(normalminus,normalplus),2*t*e*d/(a*B*den),'actual_tangent_determinant')
U=1-2*k*k*t*t+k*k*t**4;V=1-2*t*t+k*k*t**4;W=1-k*k*t**4
L0=(U*U-k*k*V*V*t*t)/f;L1=(V*V-U*U*t*t)/e
Z=W*W-4*k*k*t**4*q*f*f
# Do not assume the distance factorization before checking the Euclidean norm.
qf=(Q[0]-k,Q[1]);eq(dot(qf,qf),(1+k*s)*(U+k*V*s)/q**2,'actual_outer_norm')
for P,ss in [(Pminus,snm),(Pplus,snp)]:
 z=(P[0]-k,P[1]);eq(dot(z,z),(a+k*ss)**2,'ordinary_original_distance_squared')
Ao=f*f/q;Bo=b/q
qm=(-Ao*snm-k,Bo*cnm);qp=(-Ao*snp-k,Bo*cnp)
pm=(Pminus[0]-k,Pminus[1]);pp=(Pplus[0]-k,Pplus[1])
# Assemble rational edge expressions from actual Euclidean inversions.
E=b/e*t*f*q*q*d*den/((1+k*s)*(U+k*V*s)**2)
G=Bo*t*f*q**4*d*den/(e*(f+k*e*s)**2*(L0+k*L1*s))
eq(det(pm,pp)/2,E*(a+k*snm)**2*(a+k*snp)**2,'actual_original_inverse_edge')
Nm=(1+k*snm)*(U+k*V*snm)/q**2;Np=(1+k*snp)*(U+k*V*snp)/q**2
eq(det(qm,qp)/2,G*Nm*Np,'actual_outer_inverse_edge')
eq(dot(qm,qm),Nm,'first_named_outer_inverse_norm');eq(dot(qp,qp),Np,'second_named_outer_inverse_norm')
# Derive triple-angle functions from two successive additions.
s2=2*t*e*f/W;c2=V/W;d2=U/W
c3=(c2*e-s2*t*d2*f)/(1-k*k*s2*s2*t*t)
d3=(d2*f-k*k*s2*t*c2*e)/(1-k*k*s2*s2*t*t)
eq(L0,Z*d3,'triple_dn_from_addition');eq(L1,Z*c3,'triple_cn_from_addition')
eq(L0*L0-k*k*L1*L1,(1-k*k)*Z*Z,'strict_outer_denominator_gap')
eq(U*U-k*k*V*V,(1-k*k)*W*W,'strict_original_denominator_gap')
eq(U*U-V*V,4*t*t*q*f*f*(1-k*k),'generic_dn_zero_separation')
eq(f*f-k*k*e*e,1-k*k,'outer_first_factor_gap')
eq(d*den*(1/(1+k*s)+1/(1-k*s)),2*(q/d+t*t*d),'N4_exception_pair')
# Critical sn values: (sn')^2=(1-sn^2)(1-k^2 sn^2), sn''=-(1+k^2)sn+2k^2sn^3.
x=S.symbols('x');second=-(1+k*k)*x+2*k*k*x**3
check(S.simplify(-k*second.subs(x,1/k))==k*k-1,'N3_exact_nonzero_second_derivative')
check(S.simplify(k*second.subs(x,-1/k))==k*k-1,'original_critical_zero_order_two')
# A reflected local double pole has negative quadratic coefficient: direct Laurent substitution.
z,A2,A1=S.symbols('z A2 A1');laurent=A2/z**2+A1/z
check(S.expand(-laurent.subs(z,-z)).coeff(z,-2)==-A2,'reflection_opposite_quadratic_coefficient')
# Exact quotient-lattice and multiplicity controls, independent finite test domain.
for N in range(3,87):
 for tau in range(1,(N+1)//2):
  if gcd(N,tau)!=1:continue
  v=F(2*tau,N);delta=2*v;ell=F(4,N);r=F(3)
  orbit=lambda x:Counter((x-j*delta)%4 for j in range(N))
  check(len(orbit(0))==N,'primitive_shift_order')
  check(orbit(r+delta)==orbit(r-delta),'original_quadratic_equal_multiplicity')
  check(orbit(r+v)==orbit(r-v),'outer_quadratic_equal_multiplicity')
  for sgn in [-1,1]:check(((r+sgn*3*v-(r+v))/ell).denominator==1,'outer_simple_pole_class')
  check((v==F(1,2))==(N==4 and tau==1),'original_exception_iff_N4')
  check((3*v==2)==(N==3 and tau==1),'critical_exception_iff_N3')
  check((3*v==1)==(N==6 and tau==1),'new_common_pole_iff_N6')
  check((r+v)-v==r,'correct_comparison_shift')
check((F(3)+F(1,3))/F(2,3)==5,'N6_common_pole_same_class')
# Rational four-orbit reconstructed with line equations, not hard-coded outer vertices.
def area(P):return sum(det(P[i],P[(i+1)%len(P)]) for i in range(len(P)))/2
def inv(P,f):
 ans=[]
 for x,y in P:
  v=(x-f,y);norm=dot(v,v);check(norm>0,'exact_named_inverse_finite');ans.append((v[0]/norm,v[1]/norm))
  check(dot(ans[-1],ans[-1])*norm==1,'exact_unit_inverse_radius_relation')
 return ans
for u in range(2,13):
 for v in range(1,u):
  a=F(u*u+v*v);b=F(2*u*v);c=F(u*u-v*v)
  P=[(F(0),b),(-a,F(0)),(F(0),-b),(a,F(0))];Q=[]
  for i in range(4):
   p=P[i];p1=P[(i+1)%4];n=(p[0]/a**2,p[1]/b**2);n1=(p1[0]/a**2,p1[1]/b**2);D=det(n,n1);X=((n1[1]-n[1])/D,(n[0]-n1[0])/D)
   check(dot(n,X)==1,'rational_first_named_tangent');check(dot(n1,X)==1,'rational_second_named_tangent');Q.append(X)
  for focus in [c,-c]:
   A=area(inv(P,focus));B=area(inv(Q,focus));check(A==2/(a*b),'rational_original_area');check(B==1/(a*b),'rational_outer_area');check(2*B==A,'table_reciprocal_typo_half')
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'categories':dict(counts),'scope':'Independent exact geometric identities, triple-angle algebra, critical orders, lattice multiplicities and rational N4 controls. Universal analysis is in the review.'},indent=2))
