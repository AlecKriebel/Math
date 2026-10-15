"""Small exact group tables and directed word metrics; standard library only."""
from collections import deque
from itertools import product

def cyclic(n):
 return f'C{n}', [[(a+b)%n for b in range(n)] for a in range(n)]
def dihedral(n):
 es=list(product(range(2),range(n)));ix={x:i for i,x in enumerate(es)}
 return f'D{2*n}',[[ix[((a+c)%2,(b+(-1)**a*d)%n)] for c,d in es] for a,b in es]
def abelian(a,b):
 es=list(product(range(a),range(b)));ix={x:i for i,x in enumerate(es)}
 return f'C{a}xC{b}',[[ix[((x+z)%a,(y+t)%b)] for z,t in es] for x,y in es]
def inverses(M):return [next(b for b in range(len(M)) if M[a][b]==M[b][a]==0) for a in range(len(M))]
def lengths(M,S):
 d={0:0};q=deque([0])
 while q:
  a=q.popleft()
  for s in S:
   b=M[a][s]
   if b not in d:d[b]=d[a]+1;q.append(b)
 return d

def subsets(n):
 for m in range(1,1<<(n-1)):yield [i+1 for i in range(n-1) if m>>i&1]
