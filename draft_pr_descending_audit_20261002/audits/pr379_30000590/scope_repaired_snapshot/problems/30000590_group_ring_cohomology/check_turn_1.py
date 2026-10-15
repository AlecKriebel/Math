#!/usr/bin/env python3
from itertools import product
import json
checks=pairs=rings=0
for m in range(2,11):
 G=list(product(range(m),range(2)))
 def mul(a,b):return ((a[0]+(-1)**a[1]*b[0])%m,(a[1]+b[1])%2)
 for H in [[(i,0) for i in range(m)],[(0,0),(0,1)]]:
  H=set(H);reps=[];seen=set()
  for g in G:
   if g not in seen:reps.append(g);seen.update(mul(h,g) for h in H)
  coords=[]
  for a in G:
   vals=[(r,mul(r,a)) for r in reps if mul(r,a) in H]
   assert len(vals)==1;checks+=1;coords+=vals;pairs+=1
  assert len(set(coords))==len(G);checks+=1
  for g,a,h in product(G,G,H):
   ga=mul(g,a);gah=mul(ga,h)
   assert (gah in H)==(ga in H);checks+=1
   if ga in H:assert gah==mul(ga,h);checks+=1
  for g,k,a in product(G,G,G):
   assert mul(g,mul(k,a))==mul(mul(g,k),a);checks+=1
# Normal monomials: pure y^a is ('y',a); y^a*x*y^b is ('x',a,b).
def prod(a,b):
 if a is None or b is None:return None
 if a[0]=='y' and b[0]=='y':return ('y',a[1]+b[1])
 if a[0]=='y':return ('x',a[1]+b[1],b[2])
 if b[0]=='y':return ('x',a[1],a[2]+b[1])
 return None
B=[('y',a) for a in range(5)]+[('x',a,b) for a in range(4) for b in range(4-a)]
x=('x',0,0)
for a,b,c in product(B,repeat=3):
 assert prod(prod(a,b),c)==prod(a,prod(b,c));checks+=1;rings+=1
for N in range(1,61):
 pure=[('y',a) for a in range(N+1)]
 withx=[('x',a,b) for a in range(N) for b in range(N-a)]
 assert len(set(prod(x,a) for a in pure))==len(pure);checks+=1
 for a in withx:
  assert prod(x,a) is None;checks+=1
  for b in [('y',0),('y',1),('y',N),x,('x',N,0)]:
   c=prod(a,b);assert c is None or c[1]==a[1];checks+=1
 assert len({('x',a,0) for a in range(N+1)})==N+1;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_index_basis_pairs':pairs,'ring_associativity_triples':rings,'scope':'Finite-index coinduction pairing including nonnormal subgroups; monomial normal forms and kernel-support controls. Not a group-ring counterexample.'},indent=2,sort_keys=True))
