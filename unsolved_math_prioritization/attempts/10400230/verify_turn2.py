#!/usr/bin/env python3
"""Exact coefficient, graph and classification controls; no universal knot claim."""
from fractions import Fraction
from itertools import combinations,product
from collections import Counter
from math import isqrt,gcd
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
def connected(n,E,removed=None):
 V=set(range(n))-{removed};seen={next(iter(V))}
 while True:
  new=seen|{u for u,v in E if v in seen and u!=removed}|{v for u,v in E if u in seen and v!=removed}
  if new==seen:return seen==V
  seen=new
def FH(a,b,c,d):return a*b*c*d+a*b+a*c-b*d+c*d,(a+c)*(b*d+1)+b+d
def Q(d,b):return {1:5*b*b+14*b+9,2:10*b*b+18*b+8,4:20*b*b+26*b+9}[d]
E=[(4,i) for i in range(4)]+[(i,(i+1)%4) for i in range(4)];powers=[]
for T in combinations(range(8),4):
 if connected(5,[E[i] for i in T]):powers.append(tuple(1+(i in T)-((4+(-i)%4) in T) for i in range(4)))
ok(len(powers)==45)
for x in product(range(1,8),repeat=4):
 F,H=FH(*x)
 P=sum(__import__('math').prod(v**e for v,e in zip(x,ex)) for ex in powers)
 ok(P==F*F+H*H);ok(F>0 and H>0)
# 3^4 evaluation points already certify the identity by per-variable degree <=2.
for x in product(range(1,4),repeat=4):
 edges=[];n=5
 for i,a in enumerate(x):edges +=[(4,i)]*a
 for i in range(4):
  a=x[(-i)%4];path=[i]+list(range(n,n+a-1))+[(i+1)%4];n+=a-1;edges+=list(zip(path,path[1:]))
 L=[[0]*n for _ in range(n)]
 for u,v in edges:L[u][u]+=1;L[v][v]+=1;L[u][v]-=1;L[v][u]-=1
 F,H=FH(*x);ok(det([r[:-1] for r in L[:-1]])==F*F+H*H)
 for v in range(n):ok(connected(n,edges,v))
solutions=Counter()
for a,b,c,d in product(range(1,21),repeat=4):
 F,H=FH(a,b,c,d)
 ok(F-H*2==(a*c-2*a-2*c-1)*b*d+(a-2)*b+(c-2)*d+(a*c-2*a-2*c))
 ok(2*F-H==(2*a*c-a-c-2)*b*d+(2*a-1)*b+(2*c-1)*d+(2*a*c-a-c))
 if F==2*H or 2*F==H:
  aa,bb,cc,dd=(a,b,c,d) if a<=c else (c,d,a,b)
  if 2*F==H:
   ok((aa,cc,bb,dd) in [(1,1,1,1),(1,2,7,2),(1,2,5,3),(1,2,4,5)])
  elif aa==2:ok(dd in (1,2,4) and cc==5*bb+2+4//dd and H==Q(dd,bb))
  else:ok((aa,cc,bb,dd) in [(3,5,2,1),(3,6,8,2),(3,6,6,3),(3,6,5,5),(4,4,3,6),(4,4,4,4),(4,4,6,3)])
  solutions['F=2H' if F==2*H else '2F=H']+=1
for d in (1,2,4):
 for b in range(1,1001):
  c=5*b+2+4//d;F,H=FH(2,b,c,d);ok(F==2*H);ok(H==Q(d,b))
ok({Q(1,b)%3 for b in range(3)}=={0,1});ok({Q(4,b)%3 for b in range(3)}=={0,1})
for b in range(1,1001):ok(Q(1,b)==(b+1)*(5*b+9));ok(Q(2,b)==2*(b+1)*(5*b+4))
ok({Q(2,b)%7 for b in range(7)}=={0,1,2,5});ok(gcd(11,12)==1)
ok(all(59%q for q in (2,3,5,7)));ok(5*59**2==17405)
F,H=FH(3,8,6,2);ok((F,H)==(326,163));ok(all(163%q for q in (2,3,5,7,11)))
print(json.dumps(dict(status='PASS',assertions=checks,polynomial_grid=2401,actual_graphs=81,classification_grid=160000,ray_solutions_in_grid=dict(solutions),missing_examples=[605,17405],scope='exact polynomial identity certificate and finite controls of a proved template classification'),indent=2,sort_keys=True))
