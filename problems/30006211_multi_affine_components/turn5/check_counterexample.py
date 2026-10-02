#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import product
import json,math
checks=0
def ck(x):
 global checks
 assert x;checks+=1

def add(P,Qp):
 R=P.copy()
 for e,c in Qp.items():R[e]=R.get(e,0)+c
 return {e:c for e,c in R.items() if c}
def scale(P,c):return {e:c*a for e,a in P.items() if c*a}
def mul(P,Qp):
 R={}
 for e,a in P.items():
  for f,b in Qp.items():
   g=tuple(x+y for x,y in zip(e,f));R[g]=R.get(g,0)+a*b
 return {e:c for e,c in R.items() if c}
def evaluate(P,x):
 z=Q(0)
 for e,c in P.items():
  y=Q(c)
  for a,b in zip(x,e):y*=a**b
  z+=y
 return z
records=[]
for m in range(2,13):
 n=2*m;zero=(0,)*n;fs=[]
 for i in range(m):
  e=[0]*n;e[2*i]=e[2*i+1]=1;fs.append({tuple(e):1,zero:-1})
 F={};H={};S={}
 for f in fs:F=add(F,f);S=add(S,mul(f,f))
 for i in range(m):
  for j in range(i+1,m):H=add(H,mul(fs[i],fs[j]))
 ck(add(mul(F,F),scale(H,-2))==S)
 for P in (F,H,add(H,F)):
  ck(all(all(a<=1 for a in e) for e in P));ck(max(map(sum,P)) in (2,4))
 ck(max(map(sum,H))==max(map(sum,add(H,F)))==4)
 records.append({'blocks':m,'variables':n,'degrees':[max(map(sum,F)),max(map(sum,H))],'components':2**m,'F_terms':len(F),'H_terms':len(H)})
 # Exact witnesses in every component through m=8, and selected signs beyond.
 signs=list(product((-1,1),repeat=m)) if m<=8 else [tuple([1]*m),tuple([-1]*m)]
 for sig in signs:
  x=[]
  for i,s in enumerate(sig):x.extend([Q(s*(i+1)),Q(s,i+1)])
  ck(evaluate(F,x)==evaluate(H,x)==0);ck(all(x[2*i]*x[2*i+1]==1 for i in range(m)))
# Direct real-domain bounded grid consistency, excluding a numerical-only inference.
for m in range(2,5):
 for zs in product((-2,-1,0,1,2,3),repeat=m):
  f=sum(z-1 for z in zs);h=sum((zs[i]-1)*(zs[j]-1) for i in range(m) for j in range(i+1,m))
  ck(f*f-2*h==sum((z-1)**2 for z in zs));ck((f==0 and h==0)==all(z==1 for z in zs))
print(json.dumps({'assertions':checks,'symbolic_families':records,'status':'exact identities pass; infinite family proof required','scope':'No finite scan is used to infer the unbounded component count. The proof gives all m and exact sign components.'},indent=2))
