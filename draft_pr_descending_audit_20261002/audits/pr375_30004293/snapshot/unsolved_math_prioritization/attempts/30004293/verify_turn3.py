#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product,combinations
from collections import defaultdict
import random,json
rng=random.Random(3000429303);checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def rank(rows):
 a=[[F(x)for x in r]for r in rows];nr=len(a)
 if not nr:return 0
 nc=len(a[0]);r=0
 for j in range(nc):
  p=next((i for i in range(r,nr)if a[i][j]),None)
  if p is None:continue
  a[r],a[p]=a[p],a[r];v=a[r][j];a[r]=[x/v for x in a[r]]
  for i in range(nr):
   if i!=r and a[i][j]:
    v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  r+=1
  if r==nr:break
 return r
flagcases=0
for n in range(3,10):
 A=list(range(1,n+1));fibers=defaultdict(list)
 for bits in range(1<<n):
  B=frozenset(a for j,a in enumerate(A)if bits>>j&1);fibers[sum(B)].append(B)
 for Bs in fibers.values():
  for k in range(2,min(4,len(Bs))+1):
   for tup in list(combinations(Bs,k))[:12]:
    one=(1,)*k;vs=[one];ks=[];ws=[];w={a:tuple(int(a in B)for B in tup)for a in A}
    for a in reversed(A):
     if rank(vs+[w[a]])>len(vs):vs.append(w[a]);ks.append(a);ws.append(w[a])
    t=len(ks);ck(k<=2**t);ck(rank(vs)==t+1)
    residual=[sum(a*w[a][i]for a in A if a not in ks)for i in range(k)]
    totals=[residual[i]+sum(a*omega[i]for a,omega in zip(ks,ws))for i in range(k)];ck(len(set(totals))==1)
    U=[1<<(a-1).bit_length()for a in ks]
    for j in range(t):
     low=U[j+1]if j+1<t else 0
     for a in A:
      if a not in ks and low<a<=U[j]:ck(rank(vs[:j+2]+[w[a]])==j+2)
    flagcases+=1
# Exact dimension/cube bounds for small rationally generated spaces.
cubecases=0
for k in range(2,6):
 cube=list(product((0,1),repeat=k))
 for _ in range(24):
  vs=[(1,)*k]
  for omega in rng.sample(cube,len(cube)):
   if rank(vs+[omega])>len(vs):vs.append(omega)
   if rng.randrange(3)==0:break
  d=rank(vs);inside=sum(rank(vs+[omega])==d for omega in cube);ck(inside<=2**d);cubecases+=1
for t in range(1,30):
 for _ in range(40):
  cs=sorted([F(rng.randrange(1,101),100)for _ in range(t+1)],reverse=True);c=cs[-1];S=sum(cs[:-1]);lhs=sum((cs[j]-cs[j+1])*(j+2)for j in range(t));ck(lhs==S+cs[0]-(t+1)*c)
  ck(S>=t*c)
# log2<7/10 via an exact convergent atanh series and tail bound.
s=sum((F(2, (2*j+1)*3**(2*j+1))for j in range(12)),F(0));tail=F(2,25*3**25)*F(9,8);ck(s+tail<F(7,10))
for r in range(2,100):ck(1-(1-F(1,r))*F(7,10)>0)
print(json.dumps({'exact_assertions':checks,'flag_exposure_cases':flagcases,'cube_dimension_cases':cubecases,'threshold_telescoping_cases':1160,'infinite_probabilistic_claims_tested':False},indent=2))
