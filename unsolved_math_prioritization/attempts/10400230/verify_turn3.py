#!/usr/bin/env python3
"""Exact network and quadratic-ring controls for the scoped 5p^2 theorem."""
from fractions import Fraction
from itertools import product
from math import gcd,isqrt
import json
checks=0
def ok(x):
 global checks
 assert x
 checks+=1
def det(M):
 A=[list(map(Fraction,r)) for r in M];z=Fraction(1)
 for k in range(len(A)):
  j=next((j for j in range(k,len(A)) if A[j][k]),None)
  if j is None:return 0
  if j!=k:A[k],A[j]=A[j],A[k];z=-z
  q=A[k][k];z*=q
  for j in range(k+1,len(A)):
   t=A[j][k]/q
   for l in range(k+1,len(A)):A[j][l]-=t*A[k][l]
 return z
def treecount(n,E):
 L=[[0]*n for _ in range(n)]
 for u,v in E:L[u][u]+=1;L[v][v]+=1;L[u][v]-=1;L[v][u]-=1
 return det([r[1:] for r in L[1:]])
def connected(n,E,removed=None):
 V=set(range(n))-{removed};seen={next(iter(V))}
 while True:
  new=seen|{u for u,v in E if v in seen and u!=removed}|{v for u,v in E if u in seen and v!=removed}
  if new==seen:return seen==V
  seen=new
def word(u,v):
 assert gcd(u,v)==1 and min(u,v)>0
 ops=[]
 while (u,v)!=(1,1):
  if u>v:ops.append('P');u-=v
  else:ops.append('S');v-=u
 return ops
def install(ops,s,t,E,count,dual=False):
 if not ops:E.append((s,t));return
 op=ops[0]
 if dual:op={'P':'S','S':'P'}[op]
 if op=='P':E.append((s,t));install(ops[1:],s,t,E,count,dual)
 else:
  w=count[0];count[0]+=1
  install(ops[1:],s,w,E,count,dual);E.append((w,t))
def pairgraph(u,v,dual=False):
 E=[];count=[2];install(word(u,v),0,1,E,count,dual);return count[0],E
def wheel(pairs):
 E=[];count=[5]
 for i,(u,v) in enumerate(pairs):
  ops=word(u,v);install(ops,4,i,E,count);j=(-i)%4;install(ops,j,(j+1)%4,E,count,True)
 return count[0],E
def FHbar(pairs):
 (A,a),(B,b),(C,c),(D,d)=pairs
 return (A*B*C*D+A*B*c*d+A*C*b*d-B*D*a*c+C*D*a*b,
 A*B*D*c+B*C*D*a+A*b*c*d+B*a*c*d+C*a*b*d+D*a*b*c)
network_tests=0
for u,v in product(range(1,10),repeat=2):
 if gcd(u,v)>1:continue
 for dual in [False,True]:
  n,E=pairgraph(u,v,dual);T=treecount(n,E);S=treecount(n,E+[(0,1)])-T
  ok((T,S)==((v,u) if dual else (u,v)));network_tests+=1
# Exact positive norm-Euclidean rounding bounds on a rational grid.
for den in range(1,16):
 for a,b in product(range(-den,den+1),repeat=2):
  r=Fraction(a,2*den);s=Fraction(b,2*den)
  ok(r*r+r*s+s*s<=Fraction(3,4));ok(abs(r*r-3*s*s)<=Fraction(3,4))
N=100000;prime=bytearray(b'\1')*(N+1);prime[0:2]=b'\0\0'
for p in range(2,isqrt(N)+1):
 if prime[p]:prime[p*p:N+1:p]=b'\0'*(((N-p*p)//p)+1)
records=[]
for p in range(3,N+1,4):
 if not prime[p]:continue
 if p==3:u=v=1;pairs=[(u,v),(1,1),(v,u),(1,1)];kind='positive'
 elif p%3==1:
  rep=None
  for u in range(1,isqrt(p)+1):
   D=4*p-3*u*u
   if D<0:continue
   q=isqrt(D)
   if q*q==D and (q-u)%2==0 and q>u:rep=u,(q-u)//2;break
  ok(rep is not None);u,v=rep;ok(u*u+u*v+v*v==p);ok(gcd(u,v)==1)
  pairs=[(u,v),(1,1),(v,u),(1,1)];kind='positive'
 else:
  rep=None
  for x in range(1,isqrt(p//2)+1):
   z=3*x*x-p
   if z>=0 and isqrt(z)**2==z:rep=x,isqrt(z);break
  ok(rep is not None);x,t=rep;ok(3*x*x-t*t==p);ok(abs(t)<x and gcd(t,x)==1)
  pairs=[(1,1),(x,x-t),(1,1),(x,x+t)];kind='indefinite'
  ok((p//3-p//6)%2==0)
  if p<1000:
   for j in range(-5,6):
    tt,xx=t,x
    for _ in range(abs(j)):
     if j>=0:tt,xx=2*tt+3*xx,tt+2*xx
     else:tt,xx=2*tt-3*xx,2*xx-tt
    while abs(tt)>=xx:
     old=xx
     if tt>=xx:tt,xx=2*tt-3*xx,2*xx-tt
     else:tt,xx=2*tt+3*xx,2*xx+tt
     ok(0<xx<old);ok(tt*tt-3*xx*xx==-p)
    ok(abs(tt)<xx)
 F,H=FHbar(pairs);ok((F,H)==(p,2*p));ok(F*F+H*H==5*p*p)
 records.append((p,pairs,kind))
actual=0
for p,pairs,kind in records:
 if p>200:continue
 n,E=wheel(pairs);ok(treecount(n,E)==5*p*p);ok(all(u!=v for u,v in E))
 for v in range(n):ok(connected(n,E,v))
 actual+=1
print(json.dumps(dict(status='PASS',assertions=checks,primitive_network_tests=network_tests,prime_bound=N,primes_3_mod_4=len(records),actual_expanded_wheels=actual,examples=[dict(p=p,pairs=pairs,determinant=5*p*p) for p,pairs,_ in records if p in (3,7,11,23,59)],scope='finite exact controls for the proved prime-ray realization; no general composite claim'),indent=2,sort_keys=True))
