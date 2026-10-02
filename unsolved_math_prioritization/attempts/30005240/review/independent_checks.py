#!/usr/bin/env python3
"""Independent rational controls; no imports from the author packet."""
from fractions import Fraction as Q
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def add(A,B):return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def scale(c,A):return [[c*a for a in row] for row in A]
def norm(A):return max(sum(abs(x) for x in col) for col in zip(*A))
I=[[Q(1),Q(0)],[Q(0),Q(1)]]
# Parametrize A by a rational correct optical q, so every identity is rational.
for den in range(2,43):
 for num in range(1,den):
  q=Q(num,den);a=(q+1/q)/2;A=a*a;s=(1/q**2-q**2)/4;P=1/q**2;Pp=A+s
  ck(P*P+(2-4*A)*P+1==0,'continued_fraction_product')
  ck((P+1)**2==4*A*P,'recurrence_elimination')
  ck(P==2*Pp-1,'printed_product_discrepancy')
  ck(Pp*Pp+(2-4*A)*Pp+1==-(A-1)*(2*A+1+2*s),'printed_residual')
  ck(1<P/Pp<2,'shortcut_ratio_squared')
  ck(2*a-q==1/q,'symmetric_two_cycle')
# Independent direct paraxial products, with unequal curvature and gaps.
for dn,c1n,c2n in product(range(1,10),range(1,8),range(1,9)):
 d=Q(dn,7);c1=Q(c1n,5);c2=Q(c2n,6)
 P=[[Q(1),d],[Q(0),Q(1)]];K1=[[Q(1),Q(0)],[2*c1,Q(1)]];K2=[[Q(1),Q(0)],[2*c2,Q(1)]]
 M=mm(mm(mm(K1,P),K2),P);A=(1+d*c1)*(1+d*c2)
 ck(M[0][0]*M[1][1]-M[0][1]*M[1][0]==1,'paraxial_determinant')
 ck(M[0][0]+M[1][1]==4*A-2,'paraxial_trace')
# Nontriangular two-way perturbations. Both Schur couplings are nonzero.
for theta,div,sgb,sgc in product([Q(0),Q(1,4),Q(1,2),Q(3,4)], [32,64],[-1,1],[-1,1]):
 Delta=1-theta;eps=Delta/div;b=sgb*eps/4;c=sgc*eps/4;zeta=1+eps/2;R=1/(zeta-theta);alpha=zeta-1-b*R*c
 S=[[1+alpha,b],[c,theta]];V=[[alpha,b],[c,Q(0)]];u=[[Q(1)],[R*c]];phi=[[Q(1),b*R]];d0=1+b*R*R*c;Pi=scale(1/d0,mm(u,phi));J=[[-b*R],[Q(1)]]
 qq=eps/(Delta-3*eps);beta=theta+2*eps;kap=beta/zeta;v=[[Q(1)],[Q(1,3)]];a0=Q(3,4);nv=Q(4,3)
 ck(norm(V)<=eps,'same_norm_perturbation')
 ck(mm(S,u)==scale(zeta,u),'right_mode')
 ck(mm(phi,S)==scale(zeta,phi),'left_mode')
 ck(mm(Pi,Pi)==Pi and mm(S,Pi)==scale(zeta,Pi),'spectral_projection')
 ck(mm(S,J)==scale(theta-c*b*R,J),'complementary_return')
 ck(norm(add(Pi,[[-1,Q(0)],[Q(0),Q(0)]]))<=3*qq,'projection_norm_bound')
 ck(kap<=1-3*Delta/4,'uniform_contraction_ratio')
 ck((1+qq)*(1+qq/(1-qq*qq))<2,'remainder_constant')
 power=I
 for j in range(36):
  err=add(power,scale(-zeta**j,Pi));ck(norm(err)<=2*beta**j,'all_power_bound')
  if kap**j<=a0/32:
   value=mm(power,v);next_value=mm(S,value)
   for t in [Q(-1),Q(-1,2),Q(0),Q(1,2),Q(1)]:
    y=value[0][0]+t*value[1][0];yn=next_value[0][0]+t*next_value[1][0]
    ck(abs(y)>=a0*zeta**j*nv/16,'excited_denominator')
    ck(abs(yn/y-zeta)<=96*kap**j/a0,'quotient_constant')
  power=mm(S,power)
# Independent bound checks for the analytic buffer constants.
for Dden,anum in product(range(2,30),range(1,16)):
 Delta=Q(1,Dden);a0=Q(anum,16);eps=a0*Delta/32;qq=eps/(Delta-3*eps)
 ck(eps<=Delta/16 and qq<=a0/2,'excitation_threshold')
 ck((a0-qq)*(1-qq)/(1+qq*qq)>=a0/8,'pointwise_mode_lower_bound')
# Direct rational clock matrices: independently detect the rank correction.
def rank(A):
 A=[list(row) for row in A];r=0
 for j in range(len(A[0])):
  pivot=next((i for i in range(r,len(A)) if A[i][j]),None)
  if pivot is None:continue
  A[r],A[pivot]=A[pivot],A[r];v=A[r][j];A[r]=[x/v for x in A[r]]
  for i in range(len(A)):
   if i!=r and A[i][j]:v=A[i][j];A[i]=[x-v*y for x,y in zip(A[i],A[r])]
  r+=1
 return r
for L in range(1,27):
 sigma=Q(4,5);rho=Q(2,7);T=[[Q(0)]*(L+1) for _ in range(L+1)]
 for i in range(L):T[i][i+1]=sigma
 T[L][L]=sigma
 ck(rank(T)==L,'corrected_clock_rank')
 ck(T[L-1]==T[L],'clock_repeated_output')
 f=[[(rho/sigma)**j] for j in range(L+1)]
 for m in range(2*L+6):
  u=f[0][0];ck(u==rho**min(m,L)*sigma**max(0,m-L),'clock_iterate')
  ck(0<u<=sigma**m,'clock_uniform_envelope')
  f=mm(T,f)
# A concrete slow diagonal with superexponentially growing fixed-j constants.
for ell in range(1,31):
 Kl=(ell+2)*2**((2*ell+1)**2);theta=Q(1,2);q=Q(1,3);Qa=2*q
 for multiple in [1,2,7]:
  k=multiple*Kl;eps=Q(1,ell+2)
  for j in range(ell,2*ell+1):
   e=Q((-1)**j*2**(j*j),k);ep=Q((-1)**(j+1)*2**((j+1)**2),k);bj=q*(1+theta**j);Y=bj*(1+ep)/(1+e)
   ck(abs(e)<=eps and abs(ep)<=eps,'finite_window_threshold')
   ck(1+e>0,'diagonal_denominator')
   ck(abs(Y-q)<=q*theta**ell+4*Qa*eps,'diagonal_window_bound')
# Envelope balance, independently cover exact rational limiting sigma/a ratios.
for aN,sN in product(range(1,30),range(0,30)):
 a=Q(aN,11);sig=Q(sN,13)
 if sig>=a:continue
 cc=2/(a+sig);tau=(a-sig)/(a+sig)
 ck(a*cc-1==tau and 1-sig*cc==tau and tau>0,'joint_window_exponent')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Independent finite algebra, nontriangular operator, exact corrected clock-rank and slow-window controls; no missing PDE hypothesis certified.'},indent=2,sort_keys=True))
