#!/usr/bin/env python3
"""Finite algebra controls, not examples with nontrivial finite residual."""
from itertools import permutations, combinations, product
from collections import Counter
import json
C=Counter()
def ck(v,k):
 C[k]+=1
 if not v:raise AssertionError(k)
def mul(p,q):return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
 q=[0]*len(p)
 for i,j in enumerate(p):q[j]=i
 return tuple(q)
def d(p,q):return sum(x!=y for x,y in zip(p,q))
def comp(p,X):
 X=tuple(X);idx={x:i for i,x in enumerate(X)};ans=[]
 for x in X:
  y=p[x]
  while y not in idx:y=p[y]
  ans.append(idx[y])
 return tuple(ans)
# Nonexpansion in raw disagreement cardinalities.
for m in range(1,6):
 ps=list(permutations(range(m)))
 for n in range(1,m+1):
  for X in combinations(range(m),n):
   cs=[comp(p,X) for p in ps]
   for i,p in enumerate(ps):
    for j,q in enumerate(ps):ck(d(cs[i],cs[j])<=d(p,q),'compression_nonexpansion')
# Quotient descent: all maps C4 -> S3, section of C4 -> C2 is 0,1.
ps=list(permutations(range(3)));id3=tuple(range(3))
for f in product(ps,repeat=4):
 def delta(a,b):return d(mul(f[a],f[b]),f[(a+b)%4])
 for q,u in product(range(2),repeat=2):
  sec=(q+u)%2;r=(q+u-sec)%4
  ck(d(mul(f[q],f[u]),f[sec])<=delta(q,u)+delta(r,sec)+d(f[r],id3),'quotient_defect_C4_C2')
 for g in range(4):
  sec=g%2;r=(g-sec)%4
  ck(d(f[g],f[sec])<=delta(r,sec)+d(f[r],id3),'quotient_comparison_C4_C2')
# Noncommutative model: S3 -> C2 (sign); all maps S3 -> S2.
grp=list(permutations(range(3)));idx={g:i for i,g in enumerate(grp)};e=idx[id3]
def parity(p):return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2
section=[e,next(i for i,g in enumerate(grp) if parity(g))]
small=list(permutations(range(2)));id2=tuple(range(2))
for f in product(small,repeat=6):
 def delta(i,j):return d(mul(f[i],f[j]),f[idx[mul(grp[i],grp[j])]])
 for q,u in product(range(2),repeat=2):
  a,b,c=section[q],section[u],section[(q+u)%2]
  r=idx[mul(mul(grp[a],grp[b]),inv(grp[c]))]
  ck(parity(grp[r])==0,'nonabelian_kernel_membership')
  ck(d(mul(f[a],f[b]),f[c])<=delta(a,b)+delta(r,c)+d(f[r],id2),'quotient_defect_S3_C2')
 for i,g in enumerate(grp):
  c=section[parity(g)];r=idx[mul(g,inv(grp[c]))]
  ck(d(f[i],f[c])<=delta(r,c)+d(f[r],id2),'quotient_comparison_S3_C2')
# Trivializing a reservoir: complete triples of permutations through degree 3.
for n in range(1,4):
 ps=list(permutations(range(n)))
 for a in range(n):
  for A in combinations(range(n),a):
   A=set(A);W=tuple(x for x in range(n) if x not in A)
   def tr(p):
    c=comp(p,W);ans=list(range(n))
    for j,x in enumerate(W):ans[x]=W[c[j]]
    return tuple(ans)
   ts=[tr(p) for p in ps]
   for i,p in enumerate(ps):ck(d(ts[i],p)<=2*a,'trivialization_closeness')
   for i,p in enumerate(ps):
    for j,q in enumerate(ps):
     for l,r in enumerate(ps):ck(d(mul(ts[i],ts[j]),ts[l])<=d(mul(p,q),r)+2*a,'trivialization_defect')
# Reservoir absorption, single-generator exact actions, all Y through five points.
# Each arbitrary psi here is a generator assignment for Z, fixing A.
qualified=0
for m in range(1,6):
 for n in range(1,m+1):
  X=tuple(range(n));k=m-n
  for a in range(n+1):
   for At in combinations(X,a):
    A=set(At)
    for rho in permutations(range(m)):
     F=sorted(x for x in A if rho[x]==x)
     for psi in permutations(X):
      if any(psi[x]!=x for x in A):continue
      err=sum(rho[x]!=psi[x] for x in X)
      if k+err>a:continue
      qualified+=1;ck(len(F)>=k,'reservoir_fixedpoint_count')
      Z=set(F[:k]);theta=list(X)
      for z,y in zip(sorted(Z),range(n,m)):theta[z]=y
      back={y:x for x,y in enumerate(theta)}
      ck(set(theta)==set(range(m))-Z,'reservoir_bijection')
      tau=tuple(back[rho[theta[x]]] for x in X)
      ck(sorted(tau)==list(X),'reservoir_repaired_permutation')
      ck(d(tau,psi)<=err+k,'reservoir_error_bound')
# Explicit two-generator sharp absorption example: two deleted old fixed points
# are relabelled into a new transposition orbit.
X=(0,1,2,3);A={0,1};Z={0,1};theta=(4,5,2,3);back={y:x for x,y in enumerate(theta)}
psY=[(0,1,2,3,5,4),(0,1,3,2,4,5)]
psX=[(0,1,2,3),(0,1,3,2)]
E=sum(sum(p[x]!=q[x] for x in X) for p,q in zip(psY,psX))
ck(2+E<=len(A),'two_generator_absorption_condition')
for rho,psi in zip(psY,psX):
 tau=tuple(back[rho[theta[x]]] for x in X)
 ck(d(tau,psi)<=2,'two_generator_absorption_bound')
ck(d(tuple(back[psY[0][theta[x]]] for x in X),psX[0])==2,'sharp_absorption_added_term')
print(json.dumps({'scope':'Finite algebra controls; no full KOU-21.85 resolution','checks_by_kind':dict(sorted(C.items())),'total_assertions':sum(C.values()),'qualified_reservoir_models':qualified},indent=2,sort_keys=True))
