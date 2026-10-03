#!/usr/bin/env python3
import itertools,math,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1
for p,e in [(2,1),(2,2),(2,3),(3,1),(3,2),(3,3),(5,1),(5,2)]:
 q=p**e
 for a,b in itertools.product(range(q),repeat=2):
  for c in range(q):
   v=(a,b);w=((a+c*b)%q,b)
   ck(((w[0]-v[0])%q,(w[1]-v[1])%q)==(c*b%q,0))
   w=(a,(b+c*a)%q)
   ck(((w[0]-v[0])%q,(w[1]-v[1])%q)==(0,c*a%q))
  g=math.gcd(q,a,b)
  ck(a%g==0 and b%g==0)
for p in (2,3,5,7):
 for d in range(2,6):
  D=1+p*(d-1)
  cols=[(p,)+(0,)*(d-1)]
  for i in range(1,d):
   for j in range(p):cols.append(tuple(int(k==i) for k in range(d)))
  ck(len(cols)==D)
  for b in range(5):
   q=p**(b+2);v=[0]*d;v[1]=p**b
   ck(v[0]%(p**(b+1))==0 and all(x%(p**b)==0 for x in v))
   v[0],v[1]=v[1],v[0]
   ck(v[0]%(p**(b+1))!=0)
def canon(v,p):
 a=next(x for x in v if x)
 z=pow(a,-1,p)
 return tuple(x*z%p for x in v)
for p in (2,3,5):
 for d in (2,3,4):
  lines={canon(v,p) for v in itertools.product(range(p),repeat=d) if any(v)}
  start=(1,)+(0,)*(d-1);seen={start};todo=[start]
  while todo:
   v=todo.pop()
   for i in range(d):
    for j in range(d):
     if i==j:continue
     w=list(v);w[i]=(w[i]+w[j])%p;w=canon(w,p)
     if w not in seen:seen.add(w);todo.append(w)
     w=list(v);w[i],w[j]=w[j],w[i];w=canon(w,p)
     if w not in seen:seen.add(w);todo.append(w)
  ck(seen==lines);ck(len(lines)==(p**d-1)//(p-1))
print(json.dumps({'turn':1,'assertions':checks,'scope':'bounded exact module and hyperplane controls; no common-core triviality claim'},sort_keys=True,indent=2))
