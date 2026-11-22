from itertools import combinations
from collections import Counter
import json

def patterns(p):
 n=len(p); e=n; s=-1; a132=False;a213=False
 for i,j,k in combinations(range(n),3):
  if p[i]<p[k]<p[j]:e=min(e,k);a132=True
  if p[k]<p[i]<p[j]:s=max(s,i)
  if p[j]<p[i]<p[k]:a213=True
 return e,s,a132,a213

def good(p):
 n=len(p)
 for j in range(1,n-2):
  lo=min(p[:j])
  for k in range(j+1,n-1):
   if lo<p[k]<p[j] and max(p[k+1:])>p[j]:return False
 e,s,_,_=patterns(p)
 return s<e

def inv(p):return sum(a>b for i,a in enumerate(p) for b in p[i+1:])
from itertools import permutations
B=[]
for n in range(1,8):
 for p in permutations(range(n)):
  if good(p):continue
  if all(good(tuple(v-(v>x) for v in p if v!=x)) for x in p):B.append(p)
 print(n,[ ''.join(str(x+1) for x in p) for p in B if len(p)==n],flush=True)
