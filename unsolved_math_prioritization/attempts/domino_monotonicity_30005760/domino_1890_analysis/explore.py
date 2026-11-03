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
A=[()]; records=[]
for n in range(10):
 c=Counter(map(inv,A)); blocked=[]
 for p in A:
  if not good((0,)+tuple(x+1 for x in p)) and not good(p+(n,)):blocked.append(p)
 rec={'n':n,'total':len(A),'counts':[c[k] for k in range(n*(n-1)//2+1)],'both_end_extensions_fail':len(blocked),'example':blocked[:1]}
 records.append(rec);print(rec,flush=True)
 if n<9:A=[p[:i]+(n,)+p[i:] for p in A for i in range(n+1) if good(p[:i]+(n,)+p[i:])]
json.dump(records,open('domino_1890_analysis/counts.json','w'),indent=2)
