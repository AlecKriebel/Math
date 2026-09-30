#!/usr/bin/env python3
"""Exact Polyak--Viro calibration against a separate Kauffman bracket state sum.
No floating-point arithmetic or external packages. Arrow counts are by subsets.
"""
from itertools import combinations,product
from fractions import Fraction as F
from collections import Counter
import random,json


def canon(arrows):
 m=2*len(arrows)
 return min(tuple(sorted(((a-s)%m,(b-s)%m) for a,b in arrows)) for s in range(m))
P=canon(((3,0),(5,1),(2,4)))
T=canon(((3,0),(1,4),(5,2)))
def pv(arrows,signs):
 ans=F(0); stats=Counter()
 for S in combinations(range(len(arrows)),3):
  endpoints=sorted(x for i in S for x in arrows[i]); r={x:i for i,x in enumerate(endpoints)}
  c=canon(tuple((r[arrows[i][0]],r[arrows[i][1]]) for i in S))
  sign=1
  for i in S:sign*=signs[i]
  if c==P:ans+=F(sign,2);stats['P']+=1
  if c==T:ans+=sign;stats['T']+=1
 return ans,dict(stats)
def gauss(m,word):
 histories=[[] for _ in range(m)]; origins=list(range(m))
 for k,g in enumerate(word):
  i=abs(g)-1
  histories[origins[i]].append((k,g>0))
  histories[origins[i+1]].append((k,g<0))
  origins[i],origins[i+1]=origins[i+1],origins[i]
 position={a:j for j,a in enumerate(origins)}
 seq=[];visited=set();origin=0
 while origin not in visited:
  visited.add(origin);seq+=histories[origin];origin=position[origin]
 if len(visited)!=m:return None
 endpoints=[[] for _ in word]
 for j,(k,over) in enumerate(seq):endpoints[k].append((j,over))
 arrows=[tuple(next(j for j,over in entries if over==flag) for flag in [True,False])
         for entries in endpoints]
 return arrows,[1 if g>0 else -1 for g in word]
def jones_v3(m,word):
 n=len(word); w=sum(1 if g>0 else -1 for g in word);answer=F(0)
 for state in product([0,1],repeat=n):
  parent=list(range((n+1)*m))
  def root(x):
   while parent[x]!=x:
    parent[x]=parent[parent[x]];x=parent[x]
   return x
  def join(x,y):parent[root(x)]=root(y)
  exponent=0
  for t,(g,s) in enumerate(zip(word,state)):
   i=abs(g)-1
   exponent+=(1 if g>0 else -1)*(1 if s==0 else -1)
   for j in range(m):
    if s==0 or j not in (i,i+1):join(t*m+j,(t+1)*m+j)
   if s:
    join(t*m+i,t*m+i+1);join((t+1)*m+i,(t+1)*m+i+1)
  for j in range(m):join(j,n*m+j)
  L=len({root(j) for j in range((n+1)*m)})
  u=3*w-exponent;l=L-1
  answer-=(1 if (w+l)%2==0 else -1)*2**l*(F(u**3,384)+F(u*l,32))/6
 return answer

def main():
 rng=random.Random(10400033)
 examples=[]
 for m,word,known in [(2,[1]*3,1),(2,[1]*5,5),(2,[1]*7,14),(3,[1,-2,1,-2],0),(3,[1,2]*4,10),(3,[1,2]*5,20)]:
  G=gauss(m,word)
  if G:
   val,stats=pv(*G);jv=jones_v3(m,word)
   examples.append({'braid':word,'PV':str(val),'Jones':str(jv),'stats':stats})
   assert val==jv,(m,word,val,jv,stats)
   assert val==known
   assert val.denominator==1
   n=len(word);limit=F(n*(n*n-1),24) if n%2 else F(n*(n*n-4),24)
   assert abs(val)<=limit
 count=0
 for m in [2,3,4]:
  for _ in range(50):
   n=rng.randrange(3,10)
   word=[rng.choice([-1,1])*rng.randrange(1,m) for i in range(n)]
   G=gauss(m,word)
   if not G:continue
   val,stats=pv(*G);jv=jones_v3(m,word)
   if val!=jv:
    print(json.dumps({'FAIL':[m,word,str(val),str(jv),G,stats]}));raise AssertionError
   assert val.denominator==1
   limit=F(n*(n*n-1),24) if n%2 else F(n*(n*n-4),24)
   assert abs(val)<=limit
   count+=1
 print(json.dumps({'examples':examples,'random_classical_checks':count,'classical_diagrams':len(examples)+count,'exact_assertions':4*len(examples)+3*count,'status':'PASS','limitation':'Bounded normalization checks; the general proof is in CANDIDATE.md.'},indent=2))

if __name__=='__main__':
 main()
