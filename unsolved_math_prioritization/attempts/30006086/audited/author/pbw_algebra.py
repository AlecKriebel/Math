"""Exact PBW/cyclic rank algebra for the bounded statements in RESULT.md.
Original implementation; Python standard library only.
"""
from collections import defaultdict,Counter
from functools import lru_cache
from fractions import Fraction as F
from itertools import product
import json
from math import factorial
if not __debug__:
 raise RuntimeError("Run without -O: exact verification uses assertions.")

def add(a,b,s=1):
 r=dict(a)
 for k,v in b.items():
  r[k]=r.get(k,0)+s*v
  if not r[k]:del r[k]
 return r

def mul(a,b):
 r=defaultdict(int)
 for u,x in a.items():
  for v,y in b.items():r[u+v]+=x*y
 return {u:x for u,x in r.items() if x}

@lru_cache(None)
def lyndon(w):return bool(w) and all(w<w[k:] for k in range(1,len(w)))
@lru_cache(None)
def bracket(w):
 if len(w)==1:return {w:1}
 for k in range(1,len(w)):
  if lyndon(w[k:]):
   a,b=bracket(w[:k]),bracket(w[k:]); return add(mul(a,b),mul(b,a),-1)
 raise ValueError(w)
@lru_cache(None)
def cfl(w):
 # Duval's Lyndon factorization.
 n=len(w);i=0;out=[]
 while i<n:
  j=i+1;k=i
  while j<n and w[k]<=w[j]:
   k=i if w[k]<w[j] else k+1
   j+=1
  while i<=k:out.append(w[i:i+j-k]);i+=j-k
 return tuple(out)
@lru_cache(None)
def pbw(w):
 r={():1}
 for a in cfl(w):r=mul(r,bracket(a))
 assert min(r)==w and r[w]==1
 return r
@lru_cache(None)
def words(content):
 if not any(content):return ((),)
 out=[]
 for a,m in enumerate(content):
  if m:
   c=list(content);c[a]-=1
   out.extend((a,)+w for w in words(tuple(c)))
 return tuple(out)
@lru_cache(None)
def vwords(content):return tuple(w for w in words(content) if all(len(x)>1 for x in cfl(w)))

def coordinates(v,content):
 r=dict(v);out={};basis=set(vwords(content))
 while r:
  w=min(r);assert w in basis, ('Not in V',w)
  z=r[w];out[w]=z;r=add(r,pbw(w),-z)
 return out

def neck(w):return min(w[i:]+w[:i] for i in range(len(w))) if w else ()

def rank(rows):
 piv={}
 for row in rows:
  r={k:F(v) for k,v in row.items() if v}
  while r:
   p=min(r);a=r[p]
   if p not in piv:
    piv[p]={k:v/a for k,v in r.items()};break
   for k,v in piv[p].items():
    t=r.get(k,0)-a*v
    if t:r[k]=t
    elif k in r:del r[k]
 return len(piv)

def check(content):
 vw=vwords(content)
 brow=[]
 for a,m in enumerate(content):
  if not m:continue
  c=list(content);c[a]-=1
  for w in vwords(tuple(c)):
   b=bracket((a,)); z=add(mul(pbw(w),b),mul(b,pbw(w)),-1)
   cyc=defaultdict(int)
   for u,t in z.items():cyc[neck(u)]+=t
   assert all(t==0 for t in cyc.values())
   brow.append(coordinates(z,content))
 br=rank(brow)
 nrows=[]
 for w in vw:
  r=defaultdict(int)
  for u,z in pbw(w).items():r[neck(u)]+=z
  nrows.append({u:z for u,z in r.items() if z})
 nr=rank(nrows)
 ans={'content':list(content),'words':len(words(content)),'V':len(vw),'bracket_rank':br,'loop_quotient':len(vw)-br,'cyclic_rank':nr,'linear_cyclic_defect':len(vw)-br-nr,'field':'Q'}
 return ans
