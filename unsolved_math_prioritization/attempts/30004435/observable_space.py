"""Exact observable-column span for a finite deterministic Markov observation."""
from fractions import Fraction as F

def mv(M,v):return tuple(sum((a*b for a,b in zip(row,v)),F(0)) for row in M)
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def basis(vectors):
 rows={}
 for v in vectors:
  v=list(v)
  for p,r in sorted(rows.items()):
   c=v[p]
   if c:v=[x-c*y for x,y in zip(v,r)]
  if not any(v):continue
  p=next(i for i,x in enumerate(v) if x);c=v[p];v=[x/c for x in v];rows[p]=v
 return [tuple(v) for p,v in sorted(rows.items())]
def matrices(P,labels):return {a:[[x if labels[i]==a else F(0) for x in row] for i,row in enumerate(P)] for a in sorted(set(labels))}
def observable_basis(M):
 n=len(next(iter(M.values())));B=[tuple([F(1)]*n)];dims=[1]
 while True:
  C=basis(B+[mv(A,v) for A in M.values() for v in B])
  if len(C)==len(B):return B,dims
  B=C;dims.append(len(B))
