"""Exact independent checks of restricted additive colorings; standard library."""
from itertools import combinations,product
from math import comb
from pathlib import Path
from collections import Counter
import hashlib,json
C=Counter()
def ck(k,b):assert b,k;C[k]+=1
def edge(a,b):return tuple(sorted((a,b)))
def internal(e,n):return e[1]-e[0]>1 and e!=(0,n-1)
def cross(e,f):
 a,b=e;c,d=f
 return a<c<b<d or c<a<d<b
def valid(T,n):return len(T)==n-3 and all(not cross(e,f) for e,f in combinations(T,2))
def weight(e,n):return ((e[0]+e[1])%n)//2
# Construct the exact two completions for every tested crossing pair, not just
# test flips already produced by a triangulation recursion.
for n in range(4,16):
 for a,b,c,d in combinations(range(n),4):
  V=[a,b,c,d];common=set()
  for u,v in zip(V,V[1:]+V[:1]):
   arc=[u];x=u
   while x!=v:x=(x+1)%n;arc.append(x)
   chord=edge(u,v)
   if internal(chord,n):common.add(chord)
   for j in range(2,len(arc)-1):
    chord=edge(arc[0],arc[j])
    if internal(chord,n):common.add(chord)
  ac=edge(a,c);bd=edge(b,d);T=common|{ac};U=common|{bd}
  ck('crossing_pair_completion',valid(T,n) and valid(U,n))
  ck('one_flip_difference',T-U=={ac} and U-T=={bd})
  ck('explicit_weight_separation',weight(ac,n)!=weight(bd,n))
  m=(n+1)//2
  ck('actual_color_difference',(sum(weight(e,n) for e in U)-sum(weight(e,n) for e in T))%m==(weight(bd,n)-weight(ac,n))%m!=0)
# Independently enumerate maximal noncrossing sets (no recursive triangulator).
models={};flipcount=0
for n in range(3,9):
 D=[(a,b) for a,b in combinations(range(n),2) if internal((a,b),n)]
 Ts=[frozenset(T) for T in combinations(D,n-3) if valid(T,n)]
 ck('Catalan_count',len(Ts)==comb(2*(n-2),n-2)//(n-1))
 pairs=[(i,j) for i,j in combinations(range(len(Ts)),2) if len(Ts[i]-Ts[j])==1]
 flipcount+=len(pairs)
 ck('flip_edge_count',len(pairs)==len(Ts)*(n-3)//2)
 for i,j in pairs:
  e=next(iter(Ts[i]-Ts[j]));f=next(iter(Ts[j]-Ts[i]))
  ck('exchanged_diagonals_cross',cross(e,f))
 models[n]=(D,Ts,pairs)
# Exhaustive small assignments in cyclic and noncyclic groups; tests converse,
# actual used colors, and difference-set bound. No unrestricted chromatic search.
for n,q,kind in [(4,2,'cyclic'),(5,2,'cyclic'),(5,3,'cyclic'),(5,4,'xor')]:
 D,Ts,pairs=models[n];index={e:i for i,e in enumerate(D)}
 crossingpairs=[(i,j) for i,j in combinations(range(len(D)),2) if cross(D[i],D[j])]
 def add(a,b):return (a+b)%q if kind=='cyclic' else a^b
 def diff(a,b):return (a-b)%q if kind=='cyclic' else a^b
 for vals in product(range(q),repeat=len(D)):
  colors=[]
  for T in Ts:
   c=0
   for e in T:c=add(c,vals[index[e]])
   colors.append(c)
  proper=all(colors[i]!=colors[j] for i,j in pairs)
  separated=all(vals[i]!=vals[j] for i,j in crossingpairs)
  ck('small_group_iff',proper==separated)
  if proper:
   image=set(colors);dd={diff(a,b) for a,b in product(image,repeat=2)}
   ck('actual_image_bound',n//2<=len(dd)<=len(image)*(len(image)-1)+1)
   ck('ambient_order_bound',q>=(n+1)//2)
for n in range(4,51):
 m=n//2;D=[(i,i+m) for i in range(m)]
 ck('crossing_clique',all(cross(a,b) for a,b in combinations(D,2)))
 ck('diagonal_count',n*(n-3)//2==len([e for e in combinations(range(n),2) if internal(e,n)]))
root=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'independent_triangulation_range':[3,8],'independent_flip_edges':flipcount,'artifact_sha256':hashlib.sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Only fixed additive group-valued colorings; no unrestricted chromatic lower bound or original conjecture resolution.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
