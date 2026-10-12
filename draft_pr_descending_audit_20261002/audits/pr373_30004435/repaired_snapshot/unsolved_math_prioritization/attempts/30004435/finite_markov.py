"""Exact finite-chain structural utilities. Standard library only."""
from fractions import Fraction as F
from math import gcd

def matmul(A,B):
 return [[sum((a*B[k][j] for k,a in enumerate(row)),F(0)) for j in range(len(B[0]))] for row in A]
def power(P,k):
 n=len(P);R=[[F(i==j) for j in range(n)] for i in range(n)]
 while k:
  if k&1:R=matmul(R,P)
  P=matmul(P,P);k//=2
 return R
def classes_phases(P,pi):
 S=[i for i,p in enumerate(pi) if p>0];R={(i,j):i==j or P[i][j]>0 for i in S for j in S}
 for k in S:
  for i in S:
   for j in S:R[i,j]=R[i,j] or (R[i,k] and R[k,j])
 unused=set(S);out=[]
 while unused:
  root=min(unused);C=sorted(j for j in S if R[root,j] and R[j,root]);unused.difference_update(C)
  assert all(not P[i][j] for i in C for j in range(len(P)) if j not in C)
  dist={root:0};todo=[root]
  for i in todo:
   for j in C:
    if P[i][j] and j not in dist:dist[j]=dist[i]+1;todo.append(j)
  d=0
  for i in C:
   for j in C:
    if P[i][j]:d=gcd(d,abs(dist[i]+1-dist[j]))
  assert d>0
  phases=[[i for i in C if dist[i]%d==r] for r in range(d)]
  out.append(dict(states=C,period=d,phases=phases))
 return out
