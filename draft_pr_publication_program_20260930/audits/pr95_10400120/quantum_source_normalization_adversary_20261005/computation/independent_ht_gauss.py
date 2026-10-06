#!/usr/bin/env python3
"""Independent exact HT Theorem5.1 calculation. Uses only Python standard library.
Category existence is a cited construction input; finite computation is exact.
All ring elements are 20 rational coefficients modulo Φ50=z20-z15+z10-z5+1.
"""
from pathlib import Path
from itertools import permutations, product
from fractions import Fraction as Q
import json,sys,platform

def ring(cs):
 cs=list(map(Q,cs));cs += [Q(0)]*max(0,20-len(cs))
 for n in range(len(cs)-1,19,-1):
  c=cs[n]
  if c:
   cs[n-5]+=c;cs[n-10]-=c;cs[n-15]+=c;cs[n-20]-=c
 return tuple(cs[:20])
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,c):return tuple(x*c for x in a)
def mul(a,b):
 cs=[Q(0)]*39
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:cs[i+j]+=x*y
 return ring(cs)
def divide(a,b):
 cols=[mul(b,ring([0]*i+[1])) for i in range(20)]
 mat=[[cols[j][i] for j in range(20)]+[a[i]] for i in range(20)]
 for j in range(20):
  n=next(i for i in range(j,20) if mat[i][j]);mat[j],mat[n]=mat[n],mat[j]
  d=mat[j][j];mat[j]=[v/d for v in mat[j]]
  for i in range(20):
   if i!=j and mat[i][j]:
    c=mat[i][j];mat[i]=[u-c*v for u,v in zip(mat[i],mat[j])]
 result=tuple(mat[i][-1] for i in range(20));assert mul(result,b)==a;return result
P=[ring([0]*n+[1]) for n in range(50)]
def zp(n):return P[n%50]
def conjugate(a):
 ans=ring([0])
 for i,c in enumerate(a):ans=add(ans,scale(zp(-i),c))
 return ans
def sign(w):return (-1)**sum(w[i]>w[j] for i in range(5) for j in range(i+1,5))
def dump(a):return [str(v) for v in a]
rho=(2,1,0,-1,-2)
s2=ring([Q(1,50000)])
for j in range(1,5):
 factor=add(ring([2]),scale(add(zp(5*j),zp(-5*j)),-1))
 for unused in range(5-j):s2=mul(s2,factor)
sqrt5=add(ring([1]),scale(add(zp(10),zp(-10)),2));assert mul(sqrt5,sqrt5)==ring([5])
records=[]
for q in (1,2,3,4):
 good=[];G=ring([0]);nontrivial=0
 for w in permutations(range(5)):
  wr=tuple(rho[w[i]] for i in range(5));alpha=tuple(q*rho[i]-wr[i] for i in range(5));counts=[0]*5
  for ns in product(range(5),repeat=4):counts[sum(ns[i]*(alpha[i]-alpha[4]) for i in range(4))%5]+=1
  qualifies=all((alpha[i]-alpha[4])%5==0 for i in range(4))
  assert counts==([625,0,0,0,0] if qualifies else [125]*5)
  if not qualifies:nontrivial+=1;continue
  dot=sum(rho[i]*wr[i] for i in range(5));sg=sign(w);G=add(G,scale(zp(-dot),sg))
  good.append({'permutation':w,'rho_dot_w_rho':dot,'sign':sg,'coordinate_residue':alpha[0]%5,'character_counts':counts})
 assert len(good)==5 and nontrivial==115
 G2=mul(G,conjugate(G));ht2=scale(G2,Q(1,80));normalized=divide(ht2,s2)
 A,B=(3475,1550) if q in (1,4) else (4025,1800);target=add(ring([A]),scale(sqrt5,B));assert normalized==target
 records.append({'q':q,'qualifying_permutations':good,'G_cyclotomic':dump(G),'G_abs_squared':dump(G2),'HT_abs_squared':dump(ht2),'S3_normalized_abs_squared':dump(normalized),'radical':[A,B],'matches_claim_exactly':True,'approx_normalized':A+B*5**0.5})
result={'method':'HT Theorem5.1 root-lattice character sums, exact rational polynomial arithmetic modulo Φ50; no submitted code','python':sys.version,'platform':platform.platform(),'phi50':'z^20-z^15+z^10-z^5+1','rho':rho,'S00_squared':dump(s2),'D_squared':dump(divide(ring([1]),s2)),'sqrt5_cyclotomic':dump(sqrt5),'results':records,'difference_q2_minus_q1':{'radical':[550,250],'positive_proof':'550+250*sqrt(5)>0'},'construction_input':'Hansen–Takata Sections4/5 category V_r^g; not independently re-proved'}
Path('computation/independent_ht_gauss.result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
