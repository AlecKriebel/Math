from itertools import permutations,product
from collections import deque
import random,json
rng=random.Random(300027623);checks=0
def ck(x):
 global checks
 checks+=1
 assert x
perms=list(permutations(range(3)));ident=(0,1,2)
def pmul(s,t):return tuple(s[t[i]] for i in range(3))
def pinv(s):return tuple(s.index(i) for i in range(3))
for p in [2,3,5]:
 Z=(0,0,0);one=(Z,ident);G=list(product(list(product(range(p),repeat=3)),perms))
 def act(s,v):return tuple(v[s.index(i)] for i in range(3))
 def op(x,y):
  sv=act(x[1],y[0]);return (tuple((a+b)%p for a,b in zip(x[0],sv)),pmul(x[1],y[1]))
 def iv(x):
  si=pinv(x[1]);v=act(si,x[0]);return (tuple(-a%p for a in v),si)
 X=[((1,0,0),ident),(Z,(1,0,2)),(Z,(1,2,0))]
 S={op(op(g,s),iv(g)) for g in G for s in X+[iv(s) for s in X]};S.discard(one)
 dist={one:0};todo=deque([one])
 while todo:
  g=todo.popleft()
  for s in S:
   h=op(g,s)
   if h not in dist:dist[h]=dist[g]+1;todo.append(h)
 ck(len(dist)==len(G))
 K={(v,ident) for v in product(range(p),repeat=3) if sum(v)%p==0}
 for k in K:ck(dist[k]<=6)
 phi=lambda g:(sum(g[0])%p,g[1])
 for _ in range(3000):
  g=rng.choice(G);h=rng.choice(G);u=phi(g);v=phi(h);ck(phi(op(g,h))==((u[0]+v[0])%p,pmul(u[1],v[1])))
 for g in G:
  qnorm=min(dist[op(g,k)] for k in K);ck(qnorm<=dist[g]<=qnorm+6)
# Integral Heisenberg identities for both positive and negative powers.
def op(g,h):return(g[0]+h[0],g[1]+h[1],g[2]+h[2]+g[0]*h[1])
def iv(g):return(-g[0],-g[1],-g[2]+g[0]*g[1])
y=(0,1,0)
for n in range(-1000,1001):
 x=(n,0,0);ck(op(op(op(x,y),iv(x)),iv(y))==(0,0,n))
print(json.dumps({'assertions':checks,'nonabelian_quotient':'S3 acts on three-coordinate permutation module','module_primes':[2,3,5],'scope':'Exact finite quotient and integral central-extension controls'},indent=2,sort_keys=True))
