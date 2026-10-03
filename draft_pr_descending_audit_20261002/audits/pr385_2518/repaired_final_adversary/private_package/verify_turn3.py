#!/usr/bin/env python3
import math,json
checks=0
def ck(x):
 global checks
 assert x;checks+=1
def T(v):return [v[(i-1)%len(v)]-v[i] for i in range(len(v))]
def pw(v,k):
 for _ in range(k):v=T(v)
 return v
def vp(x,p):
 if x==0:return 10**9
 x=abs(x);a=0
 while x%p==0:x//=p;a+=1
 return a
def plus(a,b):return [x+y for x,y in zip(a,b)]
for p in (2,3,5,7,11,13):
 e0=[1]+[0]*(p-1);v=e0
 for k in range(1,121):
  v=T(v);a=(k-1)//(p-1)
  ck(sum(v)==0);ck(any(v));ck(min(vp(x,p) for x in v)==a)
  for e in range(1,13):
   ck(all(x%(p**e)==0 for x in v)==(k>=e*(p-1)+1))
 # T^(p-1)=pB on each augmentation basis vector e_i-e_0.
 for i in range(1,p):
  b=[0]*p;b[i]=1;b[0]=-1
  B=[-x for x in b]
  for j in range(1,p-1):
   c=math.comb(p,j+1);ck(c%p==0)
   B=plus(B,[-(c//p)*x for x in pw(b,j)])
  ck(pw(b,p-1)==[p*x for x in B])
print(json.dumps({'turn':3,'assertions':checks,'primes':[2,3,5,7,11,13],'max_power':120,'scope':'exact integer cyclic-module controls; infinite statements have separate proofs'},sort_keys=True,indent=2))
