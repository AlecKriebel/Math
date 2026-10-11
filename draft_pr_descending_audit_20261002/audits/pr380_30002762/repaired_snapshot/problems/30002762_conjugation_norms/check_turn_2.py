from itertools import product
import json
checks=0
def ck(x):
 global checks
 checks+=1
 assert x
# Finite Heisenberg groups: central transfer is a homomorphism and c maps to c^index.
for p in [2,3,5,7]:
 E=list(product(range(p),repeat=3));T=[(a,b,0) for a,b in product(range(p),repeat=2)]
 def mul(x,y):return ((x[0]+y[0])%p,(x[1]+y[1])%p,(x[2]+y[2]+x[0]*y[1])%p)
 def transfer(g):
  return sum(mul(t,g)[2] for t in T)%p
 for g in E:
  for h in E:ck(transfer(mul(g,h))==(transfer(g)+transfer(h))%p)
 for z in range(p):ck(transfer((0,0,z))==(p*p*z)%p)
# Integer dihedral parity decomposition and conjugation, with no finite torus wrap.
for d in range(1,6):
 zero=(0,)*d
 def mul(x,y):return (tuple(a+x[1]*b for a,b in zip(x[0],y[0])),x[1]*y[1])
 def inv(x):return (tuple(-x[1]*a for a in x[0]),x[1])
 t=(zero,-1)
 for v in product(range(-2,3),repeat=d):
  g=(v,1);comm=mul(mul(mul(g,t),inv(g)),inv(t));ck(comm==(tuple(2*a for a in v),1))
  r=tuple(a%2 for a in v);w=tuple((a-b)//2 for a,b in zip(v,r));ck(tuple(2*a+b for a,b in zip(w,r))==v)
  wg=(w,1);ref=(r,-1);ck(mul(mul(wg,ref),inv(wg))==(v,-1))
  ck(sum(r)+1<=d+1)
print(json.dumps({'assertions':checks,'central_extension_primes':[2,3,5,7],'dihedral_ranks':[1,5],'scope':'Exact finite transfer and integer parity identities; infinite theorem proved in text'},indent=2,sort_keys=True))
