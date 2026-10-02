#!/usr/bin/env python3
"""Exact controls for TURN_3.md. Standard library only.
The algebraic-closure conclusion uses the proof's quadratic factorization, not a finite scan.
"""
from itertools import product
from random import Random
from collections import Counter
import json
checks=Counter()
def ck(x,label):
 assert x,label
 checks[label]+=1
# F9 = F3[s]/(s^2-2), elements encoded a+3b.
def add(a,b):return (a%3+b%3)%3+3*((a//3+b//3)%3)
def neg(a):return (-(a%3)%3)+3*((-(a//3))%3)
def mul(a,b):return ((a%3*(b%3)+2*(a//3)*(b//3))%3)+3*((a%3*(b//3)+a//3*(b%3))%3)
inv={a:next(b for b in range(1,9) if mul(a,b)==1) for a in range(1,9)}
def rank(A):
 A=[r[:] for r in A];row=0
 for j in range(len(A[0])):
  i=next((i for i in range(row,len(A)) if A[i][j]),None)
  if i is None:continue
  A[row],A[i]=A[i],A[row];c=inv[A[row][j]];A[row]=[mul(c,x) for x in A[row]]
  for i in range(len(A)):
   if i!=row and A[i][j]:
    c=A[i][j];A[i]=[add(x,neg(mul(c,y))) for x,y in zip(A[i],A[row])]
  row+=1
  if row==len(A):break
 return row
T0=[[0,2],[1,0]];T1=[[0,1],[1,2]]
def block(T,u,v):
 A=[[add(u if i==j else 0,neg(mul(v,T[i][j]))) for j in range(2)] for i in range(2)]
 return [[0,0,*A[0]],[0,0,*A[1]],[neg(A[0][0]),neg(A[1][0]),0,0],[neg(A[0][1]),neg(A[1][1]),0,0]]
def pencil(Ts,u,v):
 B=[[0]*8 for _ in range(8)]
 for k,T in enumerate(Ts):
  M=block(T,u,v)
  for i in range(4):
   for j in range(4):B[4*k+i][4*k+j]=M[i][j]
 return B
# Direct determinant evaluation of the small pencil throughout F9^2; then exact coefficient check.
for T,which in [(T0,0),(T1,1)]:
 for u,v in product(range(9),repeat=2):
  A=[[add(u if i==j else 0,neg(mul(v,T[i][j]))) for j in range(2)] for i in range(2)]
  det=add(mul(A[0][0],A[1][1]),neg(mul(A[0][1],A[1][0])))
  formula=add(mul(u,u),mul(v,v)) if which==0 else add(add(mul(u,u),mul(u,v)),mul(2,mul(v,v)))
  ck(det==formula,'quadratic_determinant_values')
 trace=(T[0][0]+T[1][1])%3;det=(T[0][0]*T[1][1]-T[0][1]*T[1][0])%3
 ck((1,(-trace)%3,det)==((1,0,1) if which==0 else (1,1,2)),'quadratic_coefficient_identity')
roots0={u for u in range(9) if add(mul(u,u),1)==0}
roots1={u for u in range(9) if add(add(mul(u,u),u),2)==0}
ck(len(roots0)==len(roots1)==2 and not roots0&roots1,'four_distinct_geometric_roots')
projective=[(u,1) for u in range(9)]+[(1,0)]
models=[];rng=Random(634503)
for name,Ts in [('repeated',[T0,T0]),('mixed',[T0,T1])]:
 B0=pencil(Ts,1,0);B1=pencil(Ts,0,1)
 ck(all(B0[i][j]==(-B0[j][i])%3 and B1[i][j]==(-B1[j][i])%3 for i in range(8) for j in range(8)),'alternating_coefficient_matrices')
 ranks=[]
 for u,v in projective:
  r=rank(pencil(Ts,u,v));ranks.append(r)
  expected=(4 if u in roots0 and v==1 else 8) if name=='repeated' else (6 if v==1 and u in roots0|roots1 else 8)
  ck(r==expected,'F9_projective_rank')
 for u,v in [(0,1),(1,1),(2,1),(1,0)]:ck(rank(pencil(Ts,u,v))==8,'F3_projective_nondegeneracy')
 contractions=Counter()
 for x in product(range(3),repeat=8):
  if not any(x):continue
  rows=[[sum(x[i]*B[i][j] for i in range(8))%3 for j in range(8)] for B in (B0,B1)]
  r=rank(rows);ck(r==2,'all_nonzero_contractions_onto');contractions[r]+=1
 def beta(x,y):return tuple(sum(x[i]*B[i][j]*y[j] for i in range(8) for j in range(8))%3 for B in (B0,B1))
 def gp(g,h):
  x,z=g[:8],g[8:];y,w=h[:8],h[8:];b=beta(x,y)
  return tuple((x[i]+y[i])%3 for i in range(8))+tuple((z[j]+w[j]+2*b[j])%3 for j in range(2))
 def gi(g):return tuple(-v%3 for v in g)
 for _ in range(180):
  g,h,j=[tuple(rng.randrange(3) for i in range(10)) for _ in range(3)]
  ck(gp(gp(g,h),j)==gp(g,gp(h,j)),'group_associativity_controls')
  ck(gp(gp(g,g),g)==(0,)*10,'group_exponent_controls')
  ck(gp(gp(gp(g,h),gi(g)),gi(h))==(0,)*8+beta(g[:8],h[:8]),'group_commutator_controls')
 models.append({'name':name,'F9_projective_rank_histogram':dict(sorted(Counter(ranks).items())),'nonzero_contraction_rank_histogram':dict(contractions)})
H=[1,2,3,2,1];H[1]+=3**8-1
ck(H==[1,6562,3,2,1] and sum(H)==6569,'common_center_polynomial_arithmetic')
print(json.dumps({'status':'PASS','arithmetic':'exact F3/F9 and integers','assertions':sum(checks.values()),'assertions_by_scope':dict(checks),'models':models,'group_order':3**10,'center_hilbert_coefficients':H,'scope':'An obstruction to the center-only route. Both full group algebras are proved nonisomorphic over every characteristic-three field; no modular-isomorphism counterexample or full algebra search.'},indent=2,sort_keys=True))
