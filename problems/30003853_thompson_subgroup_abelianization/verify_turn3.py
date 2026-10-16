#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1
P=list(itertools.permutations(range(3)));E=tuple(range(3))
def pmul(a,b):return tuple(a[b[i]] for i in range(3))
def pinv(a):return tuple(a.index(i) for i in range(3))
def clean(a):return {i:v for i,v in a.items() if v!=E}
def bmul(a,b):return clean({i:pmul(a.get(i,E),b.get(i,E)) for i in a.keys()|b.keys()})
def shift(a,n):return {i+n:v for i,v in a.items()}
def mul(x,y):a,n=x;b,m=y;return bmul(a,shift(b,n)),n+m
def inv(x):a,n=x;return shift({i:pinv(v) for i,v in a.items()},-n),-n
lamps=[clean(dict(zip((-1,0,2),v))) for v in itertools.product(P,repeat=3)]
for a in lamps:
 for b in lamps[::13]:
  for m in (-3,-1,1,2):
   s=(b,m);k=(a,0)
   ck(mul(s,inv(s))==({},0));ck(mul(inv(s),s)==({},0))
   c=mul(mul(inv(s),k),s)
   ck(set(c[0])=={i-m for i in a});ck(c[1]==0)
   if a:ck(not {i-8*m for i in a}.issubset({-1,0,2}))
# Finite support of products cannot leave the union of input supports.
for a,b in itertools.product(lamps[::7],repeat=2):
 ck(set(bmul(a,b)).issubset(set(a)|set(b)))
 ck(set({i:pinv(v) for i,v in a.items()})==set(a))
print(json.dumps({'turn':3,'assertions':checks,'lamp_group':'S3','base_samples':216,'scope':'bounded exact nonabelian-lamp controls, no finiteness-property oracle'},sort_keys=True,indent=2))
