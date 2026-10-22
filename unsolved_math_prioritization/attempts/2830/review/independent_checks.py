"""Independent finite controls of cosets and shortcuts; no topology algorithm."""
from itertools import permutations,product
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
count=Counter()
def ck(k,v):
 if not v:raise AssertionError(k)
 count[k]+=1
G=list(permutations(range(4)));e=(0,1,2,3)
def mult(a,b):return tuple(a[b[i]] for i in range(4))
def inv(a):return tuple(a.index(i) for i in range(4))
def subgroup(gens):
 S={e};todo=[e]
 while todo:
  x=todo.pop()
  for y in gens:
   z=mult(x,y)
   if z not in S:S.add(z);todo.append(z)
 return frozenset(S)
subs={subgroup((a,b)) for a,b in product(G,repeat=2)}
ck('S4_subgroups',len(subs)==30)
order_difference=False
for A,B in product(subs,repeat=2):
 AB={mult(a,b) for a,b in product(A,B)};BA={mult(b,a) for a,b in product(A,B)}
 for c in G:
  leftcoset={mult(a,c) for a in A}
  ck('gluing_product_order',bool(leftcoset&B)==(c in AB))
  x=min(A);y=max(B);changed=mult(mult(x,c),inv(y))
  ck('reference_trace_independence',(changed in AB)==(c in AB))
  if (c in AB)!=(c in BA):order_difference=True
ck('noncommuting_order_is_detected',order_difference)
# Exact 2-by-2 action, implemented without symbolic-matrix dependencies.
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def pp(m):return ((1,m),(0,1))
def qq(n):return ((1,0),(-n,1))
R=mm(mm(pp(1),qq(1)),pp(-1));ck('conjugate',R==((0,1),(-1,2)))
for m,n in product(range(-20,21),repeat=2):
 A=mm(pp(m),qq(n));ck('ordered_power_identity',A==((1-m*n,m),(-n,1)))
 ck('noncommuting_shortcut_fails',A[1][1]==1 and R[1][1]==2 and A!=R)
ck('twist_noncommutation',mm(pp(1),qq(1))!=mm(qq(1),pp(1)))
def reduceword(w):
 out=[]
 for x in w:
  if out and out[-1]==-x:out.pop()
  else:out.append(x)
 return tuple(out)
def power(a,n):return (a,)*n if n>=0 else (-a,)*(-n)
for m,n in product(range(-15,16),repeat=2):
 w=power(1,m)+power(2,n)+power(1,-m)+power(2,-n)
 ck('word_vs_abelian_test',(reduceword(w)==())==(m*n==0))
 ck('all_commutators_homologically_zero',sum((1 if x>0 else -1) for x in w if abs(x)==1)==sum((1 if x>0 else -1) for x in w if abs(x)==2)==0)
for m,n in product(range(-30,31),repeat=2):
 ck('disjoint_power_addition',mm(pp(m),pp(n))==pp(m+n))
 ck('orientation_reverse_exponents',mm(pp(m),pp(-m))==pp(0))
x=(1,0,2,3);y=(0,2,1,3)
ck('trefoil_relator',mult(mult(x,y),x)==mult(mult(y,x),y))
ck('trefoil_nonabelian_quotient',mult(x,y)!=mult(y,x) and len(subgroup((x,y)))==6)
root=Path(__file__).resolve().parent
r={'artifact_sha256':sha256((root/'author_replay/PARTIAL_RESULT.md').read_bytes()).hexdigest(),'independent_assertions':sum(count.values()),'categories':dict(count),'scope':'Exact group cosets, signed twist matrices, free-word nullity and trefoil quotient. No JSJ recognition, triangulation, ambient isotopy or implementation of the imported algorithms.'}
(root/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
