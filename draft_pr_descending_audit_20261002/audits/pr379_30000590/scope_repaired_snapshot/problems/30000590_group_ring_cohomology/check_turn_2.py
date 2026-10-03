#!/usr/bin/env python3
from itertools import product
from fractions import Fraction as F
import json
checks=graded=fox=0
mats=list(product(range(2),repeat=4))
vecs=list(product(range(2),repeat=2))
def act(M,v):return ((M[0]*v[0]+M[1]*v[1])%2,(M[2]*v[0]+M[3]*v[1])%2)
def add(v,w):return ((v[0]+w[0])%2,(v[1]+w[1])%2)
for N in range(1,6):
 for M in mats:
  for xs in product(vecs,repeat=N):
   if not any(x!=(0,0) for x in xs):continue
   k=next(i for i,x in enumerate(xs) if x!=(0,0))
   ys=[add(xs[i],act(M,xs[i-1]) if i else (0,0)) for i in range(N)]+[act(M,xs[-1])]
   assert ys[k]==xs[k]!=(0,0);checks+=1;graded+=1
# BS(1,m) normal-form control on Z[1/m] semidirect Z,
# with t acting by multiplication by 1/m.
for m in range(1,11):
 def mult(a,b):return (a[0]+F(m)**(-a[1])*b[0],a[1]+b[1])
 def inv(a):return (-F(m)**a[1]*a[0],-a[1])
 a=(F(1),0);t=(F(0),1);one=(F(0),0)
 assert mult(mult(inv(t),a),t)==(F(m),0);checks+=1
 def ga(xs,ys):
  d={}
  for c,g in xs:
   for e,h in ys:d[mult(g,h)]=d.get(mult(g,h),0)+c*e
  return {g:c for g,c in d.items() if c}
 Sm=[(1,(F(i),0)) for i in range(m)]
 left=ga([(1,t)],Sm)
 lhs=ga([(c,g) for g,c in left.items()],[(1,a),(-1,one)])
 rhs=ga([(1,a),(-1,one)],[(1,t)])
 assert lhs==rhs;checks+=1;fox+=1
 for g,h in product([(F(i),k) for i in range(-3,4) for k in range(-2,3)],repeat=2):
  gh=mult(g,h);assert gh[1]==g[1]+h[1];checks+=1
  assert mult(g,inv(g))==one;checks+=1
print(json.dumps({'status':'PASS','exact_assertions':checks,'finite_height_controls':graded,'baumslag_solitar_fox_identities':fox,'scope':'Finite-height injectivity even for singular/zero transport, stable-letter normal forms and exact Fox identity. No general nonascending kernel theorem.'},indent=2,sort_keys=True))
