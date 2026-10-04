from collections import Counter,deque
from itertools import product
import json,random
rng=random.Random(30002762);checks=0
def ck(x):
 global checks
 checks+=1
 assert x
# Exact noncommutative operator telescoping in integral 2x2 matrices.
def mul(A,B):return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2)) for i in range(2) for j in range(2))
def add(A,B):return tuple(x+y for x,y in zip(A,B))
def sub(A,B):return tuple(x-y for x,y in zip(A,B))
I=(1,0,0,1);Z=(0,0,0,0);T=[(1,1,0,1),(1,0,1,1)];inv=[(1,-1,0,1),(1,0,-1,1)]
for length in range(1,41):
 for trial in range(50):
  word=[(rng.randrange(2),rng.choice([-1,1])) for _ in range(length)];Q=[Z,Z];W=I
  # Prepend each next operator: UV-I=(U-I)V+(V-I).
  for i,s in reversed(word):
   A=T[i] if s==1 else inv[i];coef=I if s==1 else tuple(-x for x in inv[i])
   Q[i]=add(Q[i],mul(coef,W));W=mul(A,W)
  rhs=Z
  for i in range(2):rhs=add(rhs,mul(sub(T[i],I),Q[i]))
  ck(rhs==sub(W,I))
# Full finite affine semidirect products F_p additive by cyclic unit action.
examples=[]
for p in [3,5,7,11,13,17]:
 for a in range(1,p):
  order=1;v=a%p
  while v!=1:order+=1;v=v*a%p
  G=list(product(range(p),range(order)));one=(0,0)
  def op(x,y):return ((x[0]+pow(a,x[1],p)*y[0])%p,(x[1]+y[1])%order)
  def iv(x):return ((-pow(a,(-x[1])%order,p)*x[0])%p,(-x[1])%order)
  gens=[(1,0),(0,1%order)];normgens={op(op(g,s),iv(g)) for g in G for s in gens+[iv(s) for s in gens]};normgens.discard(one)
  dist={one:0};todo=deque([one])
  while todo:
   x=todo.popleft()
   for s in normgens:
    y=op(x,s)
    if y not in dist:dist[y]=dist[x]+1;todo.append(y)
  ck(len(dist)==len(G))
  derived={(0,0)} if a==1 else {(b,0) for b in range(p)}
  for x in derived:ck(dist[x]<=6)
  for x in G:
   # Quotient minimum over the explicitly known derived coset.
   qdist=min(dist[op(x,m)] for m in derived)
   ck(qdist<=dist[x]<=qdist+6)
  examples.append({'p':p,'action':a,'order':order,'derived_diameter':max(dist[x] for x in derived)})
print(json.dumps({'assertions':checks,'noncommuting_operator_telescopes':2000,'finite_affine_groups':len(examples),'largest_derived_diameter':max(x['derived_diameter'] for x in examples),'scope':'Exact finite controls; unrestricted theorem is algebraic'},indent=2,sort_keys=True))
