#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1
for p in (2,3,5):
 def mul(u,v):a,b,c=u;d,e,f=v;return (a+d)%p,(b+e)%p,(c+f+a*e)%p
 def inv(u):a,b,c=u;return -a%p,-b%p,(-c+a*b)%p
 def th(u):a,b,c=u;return b,a,(a*b-c)%p
 P=list(itertools.product(range(p),repeat=3));U={(0,b,c) for b,c in itertools.product(range(p),repeat=2)}
 for u in P:
  ck(th(th(u))==u);ck(mul(u,inv(u))==(0,0,0))
  for v in P:
   ck(th(mul(u,v))==mul(th(u),th(v)))
   co=mul(mul(mul(u,v),inv(u)),inv(v))
   ck(co==(0,0,(u[0]*v[1]-v[0]*u[1])%p))
 ck({th(u) for u in U}!=U)
 vectors=set(itertools.product(range(p),repeat=2));zero=frozenset({(0,0)})
 subspaces={zero,frozenset(vectors)}
 for a,b in vectors-{(0,0)}:subspaces.add(frozenset((k*a%p,k*b%p) for k in range(p)))
 invariant=[]
 for V in subspaces:
  # These two transvections and swap already force irreducibility.
  maps=[lambda v:(v[1],v[0]),lambda v:((v[0]+v[1])%p,v[1]),lambda v:(v[0],(v[0]+v[1])%p)]
  if all({f(v) for v in V}==set(V) for f in maps):invariant.append(V)
 ck(set(invariant)=={zero,frozenset(vectors)})
 ck({(c,b) for b,c in [(0,c) for c in range(p)]}!={(0,c) for c in range(p)})
 for length in range(1,5):
  for ks in itertools.product(range(6),repeat=length):
   k=max(ks)
   for a in ks:ck(p**a*p**(k-a)==p**k)
# Equality p^a Z^d = p^b diag(p^ki) Z^d has exactly equal exponents.
for d in (2,3):
 for ks in itertools.product(range(4),repeat=d):
  for a in range(7):
   possible=[b for b in range(7) if all(a==b+k for k in ks)]
   ck(bool(possible)==(len(set(ks))==1 and a>=ks[0]))
print(json.dumps({'turn':5,'assertions':checks,'finite_Heisenberg_primes':[2,3,5],'scope':'comparison groups only; none is a nonabelian free pro-p counterexample'},sort_keys=True,indent=2))
