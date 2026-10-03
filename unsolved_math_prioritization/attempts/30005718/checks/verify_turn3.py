#!/usr/bin/env python3
"""Exact marking bounds and leading-word controls; standard library only."""
from fractions import Fraction as Q
from math import factorial
from collections import Counter
import json
C=Counter()
def ck(b,key):assert b,key;C[key]+=1
def add(*ps):
 a=[0]*max(map(len,ps))
 for p in ps:
  for j,v in enumerate(p):a[j]+=v
 while len(a)>1 and not a[-1]:a.pop()
 return a
def mul(p,q):
 a=[0]*(len(p)+len(q)-1)
 for i,u in enumerate(p):
  for j,v in enumerate(q):a[i+j]+=u*v
 return a
D=[2];Qp=[0,1]
for m in range(497):
 F=add(mul([2,1],D),mul([2],Qp));d=len(F)-1;r=m//2
 for j in range(d):
  ck((j+1)*F[j+1]>=(m-j)*F[j],'lower_marking_bound')
  if j<Q(m-1,2):ck(F[j+1]>F[j],'strict_lower_increase')
 A=F[::-1]
 for h in range(d):
  ck(3*(h+2)*A[h+1]>=5*(r-h-1)*A[h],'reversed_marking_bound')
  if 8*h<5*r-11:ck(A[h+1]>A[h],'strict_upper_decrease')
 direction=1
 for a,b in zip(F,F[1:]):
  if b<a:direction=-1
  ck(not(direction==-1 and b>a),'finite_unimodality_control')
 D,Qp=add(mul([1,2],D),mul([0,1],Qp)),add(mul([0,1,1],D),mul([1,1],Qp))
# Explicit eventual-unimodality interval overlap, separately from the asymptotic threshold.
for m in range(256,10001):
 p=m//3;q=(6*m+4)//5;d=3*(m+1)//2;r=m//2;h=d-q-1
 ck(4*p>=m and 4*q<=5*m,'middle_band_overlap')
 ck(2*p<m-1 and 0<=8*h<5*r-11,'strict_edge_overlap')
# Every fixed lower distance: Fibonacci leading term and strict normalized gap.
fib=[0,1]
for i in range(203):fib.append(sum(fib[-2:]))
Apow=[[1,0],[0,1]];AA=[[2,1],[1,1]]
for j in range(101):
 val=4*(Apow[0][0]+Apow[1][0]);ck(val==4*fib[2*j+2],'Fibonacci_matrix_leading_weight')
 if j:
  cm=Q(4*fib[2*j],factorial(j-1));c0=Q(4*fib[2*j+2],factorial(j));cp=Q(4*fib[2*j+4],factorial(j+1))
  lhs=(j+3)*c0*c0-(j+4)*cm*cp
  rhs=Q(16,factorial(j)**2)*Q(3*fib[2*j+2]**2+j*(j+4),j+1)
  ck(fib[2*j+2]**2-fib[2*j]*fib[2*j+4]==1,'even_Cassini')
  ck(lhs==rhs and rhs>0,'positive_fixed_lower_ULC_leading_term')
 Apow=[[sum(Apow[i][k]*AA[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
# Truncated matrix words in w. No interpolation in the return count r.
HMAX=12;cut=HMAX+2
pm=lambda p,q:mul(p,q)[:cut]
def mm(A,B):return [[add(*(pm(A[i][k],B[k][j]) for k in range(len(B))))[:cut] for j in range(len(B[0]))] for i in range(len(A))]
I=[[[1],[0]],[[0],[1]]]
H=[[[0,5,4,1],[0,3,2]],[[3,5,2],[0,2,2,1]]]
U=[[[1,2],[0,2]]];Uodd=[[[4,7,2],[1,4,2]]];b=[[[0,2]],[[1]]]
powers=[I]
for ell in range(2*HMAX+4):powers.append(mm(powers[-1],H))
def coef(P,i):return P[i] if i<len(P) else 0
for h in range(HMAX+1):
 even=[coef(mm(mm(U,P),b)[0][0],h+1) for P in powers]
 odd=[coef(mm(mm(Uodd,P),b)[0][0],h) for P in powers]
 ck(even[2*h+1]==3**(2*h+1),'even_maximal_word_weight')
 ck(odd[2*h]==3**(2*h),'odd_maximal_word_weight')
 for ell in range(2*h+2,len(powers)):ck(even[ell]==0,'even_higher_word_vanishing')
 for ell in range(2*h+1,len(powers)):ck(odd[ell]==0,'odd_higher_word_vanishing')
for h in range(1,101):
 for parity in [0,1]:
  # parity0 is even n, factorial offset1; parity1 is odd n, offset0.
  o=1-parity
  a=lambda j:Q(3**(2*j+o),factorial(2*j+o))
  actual=h*a(h)**2-(h+1)*a(h+1)*a(h-1)
  expected=Q(2*h,2*h+3 if parity==0 else 2*h+1)*a(h)**2
  ck(actual==expected and actual>0,'positive_fixed_upper_ULC_leading_term')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact coefficient marking, overlap constants and leading-word identities. Eventual full-row unimodality and fixed-distance asymptotics rely on the proofs; no uniform ULC transition threshold is inferred.'},indent=2,sort_keys=True))
