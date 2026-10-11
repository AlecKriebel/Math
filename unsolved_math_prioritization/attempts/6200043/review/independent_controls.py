"""Independent finite checks; no finite test establishes analytic boundary claims."""
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

counts={'automata':0,'uniform_escape':0,'graph_assertions':0,'series_assertions':0,'holder_assertions':0,'scale_assertions':0}

def bfs(row, start, sink):
    q=deque([(start,0)]); seen={start}
    while q:
        s,d=q.popleft()
        for t in row[s]:
            if t==sink:return d+1
            if t not in seen:seen.add(t);q.append((t,d+1))
    return None

# Different algorithm from the author: forward BFS from each reachable vertex.
# Four-state binary enumeration expands beyond the frozen 1--3-state sample.
for b,max_m in ((2,4),(3,2)):
  for m in range(1,max_m+1):
    for raw in product(range(m+1),repeat=b*m):
      row=[raw[b*s:b*(s+1)] for s in range(m)]
      reach={0};todo=[0]
      while todo:
        for t in row[todo.pop()]:
          if t<m and t not in reach:reach.add(t);todo.append(t)
      ds=[bfs(row,s,m) for s in reach]
      counts['automata']+=1
      for d in ds:
        assert d is None or 1<=d<=len(reach)
        counts['graph_assertions']+=1
      if any(d is None for d in ds):continue
      counts['uniform_escape']+=1;N=max(ds)
      # Integer walk recurrence from EVERY reachable starting state.
      for s in reach:
        v=[int(t==s) for t in range(m)]
        for length in range(1,2*N+2):
          out=[0]*m
          for t,num in enumerate(v):
            for u in row[t]:
              if u<m:out[u]+=num
          v=out;k,r=divmod(length,N)
          assert sum(v)<=(b**N-1)**k*b**r
          counts['graph_assertions']+=1

# Required negative control: reject-first-1 language has an inescapable safe state.
row=[(1,2),(1,1)]
assert bfs(row,0,2)==1 and bfs(row,1,2) is None
counts['graph_assertions']+=1

# Similarity shell equality for several non-dyadic contractions.
for q,s,N in product(range(1,7),(F(1,3),F(2,3),F(3,4)),range(1,31)):
  r=s**q
  assert sum(((1-r)*r**n for n in range(N)),F(0))==1-r**N
  counts['series_assertions']+=1

# Finite-step Holder lower-bound controls, independent of scaling identities.
for widths in product((F(1,3),F(1,2),F(2,3)),repeat=3):
  L=sum(widths)
  for heights in product((F(1,2),F(1),F(2)),repeat=3):
    integral=sum((w*h for w,h in zip(widths,heights)),F(0))
    normalized=[h/integral for h in heights]
    for p in range(1,6):
      energy=sum((w*h**p for w,h in zip(widths,normalized)),F(0))
      assert energy>=L**(1-p)
      if len(set(heights))==1:assert energy==L**(1-p)
      counts['holder_assertions']+=1

# Exact metric-scale estimates at both ends and middle of each scale interval.
for rho,A,N,k in product((F(1,2),F(2,3),F(3,4)),(F(1),F(5,2)),range(1,7),range(1,21)):
  for theta in (F(0),F(1,2),F(99,100)):
    low=2*A*rho**k; high=2*A*rho**(k-1)
    r=low+theta*(high-low)
    assert A*rho**k<=r/2 and A*rho**(k-1)>r/2
    c0=F(1,7);c=c0*rho**(N+1)/(2*A)
    assert c0*rho**(k+N)>c*r
    counts['scale_assertions']+=2

result={'status':'pass','counts':counts,'scope':'Finite graph, exact shell, discrete Holder, and scale arithmetic only; analytic/geometric claims reviewed in prose.'}
print(json.dumps(result,sort_keys=True))
