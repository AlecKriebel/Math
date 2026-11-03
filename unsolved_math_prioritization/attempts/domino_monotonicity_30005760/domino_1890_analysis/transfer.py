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
def cuts(p):return [i for i in range(1,len(p)) if max(p[:i])==i-1]
def standard(p):return tuple(sorted(p).index(v) for v in p)
def dec(p):return bool(cuts(p))
def tilde(p):
 c=cuts(p)[0];return p[:c]+(c,)+tuple(x+1 for x in p[c:])
def f(p):
 n=len(p)
 if dec(p):return tilde(p)
 q=standard(p[1:])
 if dec(q):
  q=tilde(q);v=p[0];return (v,)+tuple(x+(x>=v) for x in q)
 q=tuple(x-1 for x in p if x!=0)
 if dec(q):
  q=tuple(x+1 for x in tilde(q));i=p.index(0);return q[:i]+(0,)+q[i:]
 q=standard(p[:-1])
 if dec(q):
  q=tilde(q);v=p[-1]+1;return tuple(x+(x>=v) for x in q)+(v,)
 q=tuple(x for x in p if x!=n-1)
 if dec(q):
  q=tilde(q);i=p.index(n-1)+1;return q[:i]+(n,)+q[i:]
 return None
A=[()];bad=[]
for n in range(1,9):
 A=[p[:i]+(n-1,)+p[i:] for p in A for i in range(n) if good(p[:i]+(n-1,)+p[i:])]
 cnt=0
 for p in A:
  q=f(p)
  if q is not None:
   if inv(p)!=inv(q):raise ValueError((p,q))
   if not good(q):
    cnt+=1
    if len(bad)<10:bad.append({'p':[x+1 for x in p],'f':[x+1 for x in q],'k':inv(p)})
 print(n,cnt,flush=True)
print(bad)
