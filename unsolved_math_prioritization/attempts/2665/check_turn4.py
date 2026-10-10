"""Exact algebra controls for the satellite/framing partial; no embedding checker."""
from collections import Counter
from math import gcd
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def mul(A,B):return [[sum(A[i][k]*B[k][j]for k in range(2))for j in range(2)]for i in range(2)]
def tr(A):return list(map(list,zip(*A)))
for a in range(-3,4):
 for b in range(-3,4):
  for c in range(-3,4):
   A=[[a,b+1],[b,c]]
   for x in range(-2,3):
    for y in range(-2,3):
     for f in [-3,-1,0,1,3]:
      w=[x,y];B=[[A[i][j]+f*w[i]*w[j]for j in range(2)]for i in range(2)]
      ck(det(B)==det(A)+f*(c*x*x-(2*b+1)*x*y+a*y*y),'rank_one_determinant_formula')
      ck(B[0][1]-B[1][0]==1,'skew_part_preserved')
      if f==0:ck(B==A,'zero_framing_preserves_all_entries')
examples=[(13,1,[[2,-1],[1,0]],[[30,-8],[-9,1]]),(13,12,[[3,-1],[-2,1]],[[30,-3],[-4,-1]]),(37,1,[[3,-1],[1,0]],[[120,-21],[-22,1]]),(37,3,[[15,1],[-1,0]],[[120,27],[26,3]])]
for N,a,P,B in examples:
 k=N//2;A=[[a,k+1],[k,0]]
 ck(det(P)==1,'basis_change_SL2')
 ck(mul(mul(tr(P),A),P)==B,'common_framing_normal_form')
 ck(det(B)==-k*(k+1),'determinant_unchanged_by_basis')
 ck(gcd(P[0][0],P[1][0])==1,'annulus_candidate_vector_primitive')
 ck(B[0][1]-B[1][0]==1,'new_basis_orientation')
for N,a,f in [(13,1,11),(37,1,2)]:
 k=N//2;A=[[a,k+1],[k,0]];B=[[a+f,k+1],[k,0]]
 ck(det(A)==det(B),'framing_route_same_polynomial')
for p,q,r in [(5,6,30),(8,15,120)]:ck(gcd(p,q)==1 and p*q==r,'torus_annulus_framing_arithmetic_only')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'scope':'Finite matrix/framing identities only. Does not prove confinement, linking factorization, annular embedding or boundary-knot equality.'},sort_keys=True,indent=2))
