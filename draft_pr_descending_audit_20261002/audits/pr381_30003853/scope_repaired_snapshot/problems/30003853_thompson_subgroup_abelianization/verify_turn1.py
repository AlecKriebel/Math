#!/usr/bin/env python3
import itertools,json
checks=0
def ck(x):
 global checks
 assert x
 checks+=1
def clean(p):return {i:a for i,a in p.items() if a}
def add(a,b):return clean({i:a.get(i,0)+b.get(i,0) for i in a.keys()|b.keys()})
def neg(a):return {i:-v for i,v in a.items()}
def shift(a,n):return {i+n:v for i,v in a.items()}
def diff(a):return add(shift(a,1),neg(a))
def aug(a):return sum(a.values())
def der(a):return sum(i*v for i,v in a.items())
def divide(a):
 assert aug(a)==0
 if not a:return {}
 lo,hi=min(a),max(a)
 g={};v=0
 for i in range(lo,hi):
  v-=a.get(i,0);g[i]=v
 return clean(g)
def mul(x,y):a,n=x;b,m=y;return add(a,shift(b,n)),n+m
def inv(x):a,n=x;return neg(shift(a,-n)),-n
polys=[clean(dict(zip(range(-2,3),a))) for a in itertools.product((-1,0,1),repeat=5)]
for m in range(1,10):
 for f in polys:
  g=diff(f)
  ck(aug(g)==0);ck(der(g)==aug(f));ck(divide(g)==f)
  if aug(f)%m==0:
   ck(aug(diff(f))==0 and der(diff(f))%m==0)
   if aug(f)==0 and der(f)%m==0:
    ck(aug(divide(f))%m==0)
   for k in (-3,-1,0,1,4):
    delta=add(shift(f,k),neg(f))
    ck(aug(delta)==0 and der(delta)%m==0)
    ck(aug(divide(delta))%m==0)
 for a in range(-8,9):
  for b in range(m):
   f=add({0:m*a},{0:-b,1:b})
   ck((aug(f)//m,der(f)%m)==(a,b))
for f in polys:
 for n in (-3,-1,1,2):
  a=(f,0);s=({0:7,2:-1},n)
  conjugate=mul(mul(inv(s),a),s)
  ck(conjugate==(shift(f,-n),0))
  if f:
   S=set(range(-2,3));k=6
   ck(not set(shift(f,k*n)).issubset(S))
for m in range(1,10):
 f={0:-m,1:m}
 ck(divide(f)=={0:m})
 ck(der({0:-1,1:1})%m==(1%m))
print(json.dumps({'turn':1,'assertions':checks,'polynomials':len(polys),'moduli':list(range(1,10)),'scope':'exact finite controls, not an FP2 decision procedure'},sort_keys=True,indent=2))
