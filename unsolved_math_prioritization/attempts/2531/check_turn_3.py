#!/usr/bin/env python3
from itertools import product
import json,random
checks=0
K=[(a,b,c,d) for a,b,c,d in product(range(5),repeat=4) if (a*d-b*c)%5==1]
idx={a:i for i,a in enumerate(K)}
E=idx[(1,0,0,1)];Z=idx[(4,0,0,4)]
def raw(a,b):
 x,y,z,w=a;p,q,r,s=b
 return ((x*p+y*r)%5,(x*q+y*s)%5,(z*p+w*r)%5,(z*q+w*s)%5)
M=[[idx[raw(a,b)] for b in K] for a in K]
I=[idx[(a[3],-a[1]%5,-a[2]%5,a[0])] for a in K]
def cg(a,b):return M[M[a][b]][I[a]]
def comm(a,b):return M[M[M[a][b]][I[a]]][I[b]]
assert len(K)==120;checks+=1
center=[a for a in range(120) if all(M[a][b]==M[b][a] for b in range(120))]
assert set(center)=={E,Z};checks+=1
# Exact derived subgroup closure.
gs={comm(a,b) for a,b in product(range(120),repeat=2)}
seen={E};todo=[E]
while todo:
 a=todo.pop()
 for b in gs:
  c=M[a][b]
  if c not in seen:seen.add(c);todo.append(c)
assert len(seen)==120;checks+=1
# Quotient by +/-I, with every nontrivial normal closure checked.
def q(a):return min(a,M[Z][a])
Q=sorted({q(a) for a in range(120)});qe=q(E)
assert len(Q)==60;checks+=1
for a in Q:
 if a==qe:continue
 gens={q(cg(g,a)) for g in range(120)};seen={qe};todo=[qe]
 while todo:
  x=todo.pop()
  for y in gens:
   z=q(M[x][y])
   if z not in seen:seen.add(z);todo.append(z)
 assert len(seen)==60;checks+=1
# Central product by diagonal (-I,-I).
def canon(a,b):return min((a,b),(M[Z][a],M[Z][b]))
CP={canon(a,b) for a,b in product(range(120),repeat=2)}
def cm(a,b):return canon(M[a[0]][b[0]],M[a[1]][b[1]])
ce=canon(E,E);cz=canon(Z,E)
assert len(CP)==7200;checks+=1
assert cz==canon(E,Z)!=ce;checks+=1
assert canon(Z,Z)==ce;checks+=1
# Four elementary generators suffice to test the center of the central product.
u=idx[(1,1,0,1)];v=idx[(1,0,1,1)]
gens=[canon(u,E),canon(v,E),canon(E,u),canon(E,v)]
cc=[a for a in CP if all(cm(a,b)==cm(b,a) for b in gens)]
assert set(cc)=={ce,cz};checks+=1
for a in cc:
 for b in CP:assert cm(a,b)==cm(b,a);checks+=1
assert len({(q(a),q(b)) for a,b in CP})==3600;checks+=1
# Two distinct coordinates cannot cancel the shared central element.
assert (cz,cz)!=(ce,ce);checks+=1
# Centerful quasisimple lamp: all base configurations over C2,
# with a quotient shift, a GL2 outer conjugation and an inner coboundary.
D=(2,0,0,1);Di=(3,0,0,1)
psi=[idx[raw(raw(D,a),Di)] for a in K];pinv=[psi.index(i) for i in range(120)]
V=[u,v];seen=set()
for f in product(range(120),repeat=2):
 out=tuple(cg(V[y],psi[f[1-y]]) for y in range(2))
 back=tuple(pinv[cg(I[V[1-h]],out[1-h])] for h in range(2))
 assert back==f;checks+=1
 assert out not in seen;seen.add(out);checks+=1
 assert all((f[h] in center)==(out[1-h] in center) for h in range(2));checks+=1
assert len(seen)==14400;checks+=1
# Perfect direct-factor projection identities with a nontrivial center.
rng=random.Random(253103)
for _ in range(5000):
 a,b,c,d=[rng.randrange(120) for _ in range(4)]
 x=(a,b);y=(c,d);p0=lambda z:(z[0],E);p1=lambda z:(E,z[1])
 mul=lambda z,w:(M[z[0]][w[0]],M[z[1]][w[1]])
 assert mul(p0(x),p1(x))==x;checks+=1
 assert p0(p1(x))==(E,E) and p1(p0(x))==(E,E);checks+=1
 assert mul(p0(x),p1(y))==mul(p1(y),p0(x));checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'SL2_F5_order':120,'simple_central_quotient_order':60,'central_product_order':7200,'central_product_center_order':2,'quasisimple_C2_base_configurations':14400,'scope':'Exact finite central-extension and inverse controls; general perfect-base arguments are in TURN_3.md.'},indent=2))
