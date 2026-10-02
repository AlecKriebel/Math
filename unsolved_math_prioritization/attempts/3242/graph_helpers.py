"""Small exact graph routines for bounded diagnostics; adjacency is a list of bitsets."""
from itertools import combinations

def graphs(n):
 es=list(combinations(range(n),2))
 for mask in range(1<<len(es)):
  a=[0]*n
  for i,(u,v) in enumerate(es):
   if mask>>i&1:a[u]|=1<<v;a[v]|=1<<u
  yield a

def chromatic(a):
 n=len(a)
 if not n:return 0
 order=sorted(range(n),key=lambda v:a[v].bit_count(),reverse=True)
 for k in range(1,n+1):
  cls=[0]*k
  def rec(i,used):
   if i==n:return True
   v=order[i]
   for c in range(min(used+1,k)):
    if a[v]&cls[c]:continue
    cls[c]|=1<<v
    if rec(i+1,max(used,c+1)):return True
    cls[c]^=1<<v
   return False
  if rec(0,0):return k

def induced(a,vertices):
 return [sum(1<<j for j,v in enumerate(vertices) if a[u]>>v&1) for u in vertices]

def core(a):return induced(a,[v for v in range(len(a)) if a[v]])

def core_property(a):
 h=core(a)
 if not h:return True
 n=len(h);w=len({x.bit_count() for x in h});k=chromatic(h)
 return n<=(2*k-1)*(n-w)

def split(a):
 n=len(a);allmask=(1<<n)-1
 for K in range(1<<n):
  I=allmask^K
  if all((a[v]&K)==(K^(1<<v)) for v in range(n) if K>>v&1) and all(not(a[v]&I) for v in range(n) if I>>v&1):return True
 return False

def union(a,b):return a+[v<<len(a) for v in b]

def join(a,b):
 n=len(a);m=len(b);am=(1<<n)-1;bm=((1<<m)-1)<<n
 return [v|bm for v in a]+[(v<<n)|am for v in b]
