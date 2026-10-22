"""Locally authored exact Q(omega) interpolation of four fixed small configurations.
Not a search over arbitrary point sets. omega^2+omega+1=0.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json,sys
Z=(F(0),F(0));O=(F(1),F(0));W=(F(0),F(1))
def add(x,y):return(x[0]+y[0],x[1]+y[1])
def neg(x):return(-x[0],-x[1])
def sub(x,y):return add(x,neg(y))
def mul(x,y):return(x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]-x[1]*y[1])
def inv(x):
 d=x[0]*x[0]-x[0]*x[1]+x[1]*x[1];assert d
 return((x[0]-x[1])/d,-x[1]/d)
def div(x,y):return mul(x,inv(y))
def normalized(x):
 q=next(v for v in x if v!=Z)
 return tuple(div(v,q) for v in x)
def ver(p):
 x,y,z=p;return[mul(x,x),mul(y,y),mul(z,z),mul(x,y),mul(x,z),mul(y,z)]
def dot(x,y):
 out=Z
 for a,b in zip(x,y):out=add(out,mul(a,b))
 return out
def rref(rows):
 A=[r[:] for r in rows];piv=[];i=0
 for j in range(6):
  k=next((k for k in range(i,len(A)) if A[k][j]!=Z),None)
  if k is None:continue
  A[i],A[k]=A[k],A[i];q=inv(A[i][j]);A[i]=[mul(v,q) for v in A[i]]
  for k in range(len(A)):
   if k!=i and A[k][j]!=Z:
    v=A[k][j];A[k]=[sub(x,mul(v,y)) for x,y in zip(A[k],A[i])]
  piv.append(j);i+=1
  if i==len(A):break
 return A,piv
def enc(v):return [[str(a),str(b)] for a,b in v]
def inspect(name,P):
 P=list(dict.fromkeys(normalized(p) for p in P));V=[ver(p) for p in P];rank=len(rref(V)[1]);ranks=Counter();cones={};ordinary=None
 for inds in combinations(range(len(P)),5):
  A,piv=rref([V[j] for j in inds]);ranks[len(piv)]+=1
  if len(piv)!=5:continue
  f=next(j for j in range(6) if j not in piv);c=[Z]*6;c[f]=O
  for k,j in enumerate(piv):c[j]=neg(A[k][f])
  c=normalized(c)
  if c not in cones:
   support=tuple(j for j,row in enumerate(V) if dot(row,c)==Z);assert all(j in support for j in inds);cones[c]=support
   if len(support)==5 and ordinary is None:ordinary={'point_indices':list(support),'coefficients':enc(c)}
 out={'configuration':name,'points':enc_points(P),'number_of_points':len(P),'full_quadratic_rank':rank,'five_subset_rank_counts':dict(sorted(ranks.items())),'distinct_determined_conic_support_counts':dict(sorted(Counter(map(len,cones.values())).items())),'ordinary_example':ordinary}
 print(json.dumps(out,sort_keys=True),flush=True)
 return out
def enc_points(P):return[enc(p) for p in P]
roots=[O,W,mul(W,W)]
hesse=[]
for r in roots:
 hesse.extend([(Z,O,neg(r)),(neg(r),Z,O),(O,neg(r),Z)])
dual=[(O,Z,Z),(Z,O,Z),(Z,Z,O)]+[(O,r,s) for r in roots for s in roots]
roots6=roots+[neg(r) for r in roots];fermat18=[]
for r in roots6:fermat18.extend([(Z,O,neg(r)),(neg(r),Z,O),(O,neg(r),Z)])
sets={'hesse9':hesse,'dual_hesse12':dual,'fermat18':fermat18,'hesse21':hesse+dual}
for name in sys.argv[1:] or ['hesse9','dual_hesse12']:
 inspect(name,sets[name])
