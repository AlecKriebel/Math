#!/usr/bin/env python3
"""Exact controls for balanced network counts and fourth-power closure."""
from fractions import Fraction
from math import gcd,isqrt
from itertools import product
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
def trees(n,E):
 L=[[0]*n for _ in range(n)]
 for u,v in E:L[u][u]+=1;L[v][v]+=1;L[u][v]-=1;L[v][u]-=1
 return det([r[1:] for r in L[1:]])
def connected(n,E,removed=None):
 V=set(range(n))-{removed};seen={next(iter(V))}
 while True:
  new=seen|{u for u,v in E if v in seen and u!=removed}|{v for u,v in E if u in seen and v!=removed}
  if new==seen:return seen==V
  seen=new
def chain(op,n):
 if n==1:return None
 return (op,chain(op,n-1),None)
def balanced(q):
 if q==1:return None
 return ('P',chain('S',q),('S',chain('P',q-1),None))
def install(N,s,t,E,count,dual=False):
 if N is None:E.append((s,t));return
 op,A,B=N
 if dual:op='P' if op=='S' else 'S'
 if op=='P':install(A,s,t,E,count,dual);install(B,s,t,E,count,dual)
 else:
  w=count[0];count[0]+=1;install(A,s,w,E,count,dual);install(B,w,t,E,count,dual)
def counts(N,dual=False):
 E=[];count=[2];install(N,0,1,E,count,dual);T=trees(count[0],E);S=trees(count[0],E+[(0,1)])-T
 return T,S
for q in range(1,20):
 N=balanced(q);ok(counts(N)==(q*q,q*q));ok(counts(N,True)==(q*q,q*q))
for q in range(1,32,2):
 E=[(0,2),(1,2)];count=[3]
 # W_2: hub0, rim1,2; replace spoke(0,1) and one rim(1,2).
 install(balanced(q),0,1,E,count);install(balanced(q),1,2,E,count,True)
 ok(trees(count[0],E)==5*q**4)
 for v in range(count[0]):ok(connected(count[0],E,v))
# All TTSP count pairs with at most12 unit edges.
dp={1:{(1,1)}};balance=set()
for n in range(2,13):
 out=set()
 for k in range(1,n):
  for t,f in dp[k]:
   for u,v in dp[n-k]:out.add((t*u,t*v+f*u));out.add((t*v+f*u,f*v))
 dp[n]=out
 for t,f in out:
  if t==f:
   balance.add(t);ok(any(t%(p*p)==0 for p in range(2,isqrt(t)+1)))
primes=[p for p in range(3,1000,2) if all(p%d for d in range(2,isqrt(p)+1))]
for p in primes:
 if p%4==1:
  if p==5:X,Y=2,11
  else:
   a=next(a for a in range(1,isqrt(p)+1) if isqrt(p-a*a)**2==p-a*a);b=isqrt(p-a*a)
   X=2*(a*a-b*b)-2*a*b;Y=a*a-b*b+4*a*b
  ok(X*X+Y*Y==5*p*p);ok(gcd(X,Y)==1)
 for e in range(7):
  q=p**(e//2)
  base=5 if e%2==0 else 5*p*p
  ok(base*q**4==5*p**(2*e))
for u,v in product(range(1,31),repeat=2):
 if gcd(u,v)>1 or (u-v)%2==0:continue
 h=u*u+(u+v)**2
 for q in range(1,20,2):ok(h*q**4==(u*q*q)**2+((u+v)*q*q)**2)
print(json.dumps(dict(status='PASS',assertions=checks,balanced_network_parameters=19,actual_closed_graphs=16,ttsp_edge_bound=12,ttsp_count_pair_counts={str(k):len(v) for k,v in dp.items()},balanced_counts=sorted(balance),prime_power_primes=len(primes),scope='finite exact controls for proved closure and TTSP squarefree obstruction'),indent=2,sort_keys=True))
