#!/usr/bin/env python3
"""Independent exact observable-word span controls; no author imports."""
from fractions import Fraction as Q
from itertools import product
import json,random

def rank(vectors):
 a=[list(v) for v in vectors];r=0
 if not a:return 0
 for c in range(len(a[0])):
  pivot=next((i for i in range(r,len(a)) if a[i][c]),None)
  if pivot is None:continue
  a[r],a[pivot]=a[pivot],a[r];p=a[r][c];a[r]=[x/p for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    q=a[i][c];a[i]=[x-q*y for x,y in zip(a[i],a[r])]
  r+=1
 return r

def extend(P,e,v,a):return [Q(e[i]==a)*sum(x*y for x,y in zip(P[i],v)) for i in range(len(P))]
def independent(P,e):
 n=len(P);basis=[[Q(1)]*n];dims=[1];last=1;stabilized=None
 for k in range(1,n+3):
  old=list(basis)
  for v in old:
   for a in sorted(set(e)):
    w=extend(P,e,v,a)
    if rank(basis+[w])>len(basis):basis.append(w)
  dims.append(len(basis))
  if len(basis)==last and stabilized is None:stabilized=k-1
  last=len(basis)
 assert stabilized<=n-1
 # Full all-word columns through n+2 must belong to final reachable span.
 word_cols=[[Q(1)]*n]
 for k in range(n+2):
  word_cols=[extend(P,e,v,a) for v in word_cols for a in sorted(set(e))]
  assert all(rank(basis+[v])==len(basis) for v in word_cols)
 return {'states':n,'emission':e,'dimensions':dims,'stabilization_word_length':stabilized,'full_words_through_length':n+2}

rng=random.Random(37330004435);rows=[]
for n in range(1,7):
 for t in range(5):
  weights=[[rng.randrange(1,5) for j in range(n)] for i in range(n)]
  P=[[Q(w,sum(row)) for w in row] for row in weights]
  e=[rng.randrange(2) for i in range(n)];rows.append(independent(P,e))
# Independent direct bridge denominator normalization over all central words.
P=[[Q(2,3),Q(1,3)],[Q(1,4),Q(3,4)]]
def mm(A,B):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*B)] for row in A]
def power(k):
 R=[[Q(i==j) for j in range(2)] for i in range(2)]
 for j in range(k):R=mm(R,P)
 return R
bridges=[]
for m in range(2,7):
 L=power(m-1);T=power(2*m)
 for i,j in product(range(2),repeat=2):
  total=sum(L[i][a]*P[a][b]*P[b][c]*L[c][j]/T[i][j] for a,b,c in product(range(2),repeat=3))
  assert total==1
  bridges.append({'m':m,'endpoints':[i,j],'normalization':str(total)})
print(json.dumps({'wordspan_cases':rows,'bridge_cases':bridges,'status':'PASS; exact finite controls only'},indent=2,sort_keys=True))
