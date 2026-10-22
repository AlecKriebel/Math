"""Fresh auditor's exact local row-space test. No candidate code imported.
Enumerate coarse relative strata and every possible zero face of nonnegative affine slack.
Compare all fine-grid trace rows with the proposed slope/jump/spike factorization.
"""
from itertools import product,combinations
from fractions import Fraction as Q
from pathlib import Path
import json
from sympy import Matrix
DIRECTIONS={}
for a,b in product(range(-2,3),repeat=2):
 s=lambda x:(x>0)-(x<0)
 DIRECTIONS[(s(a),s(b),s(a+b))]=(a,b)
assert len(DIRECTIONS)==13

def vec(N,k,state):
 a=[0]*(3*N);a[3*(k%N)+state]=1;return a

def combination(*terms):return [sum(t*c[i] for t,c in terms) for i in range(len(terms[0][1]))]
def row(N,x,y,d):
 a,b=d;st=lambda x:0 if x==0 else (1 if x>0 else 2)
 return combination((1,vec(N,x,st(a))),(1,vec(N,y,st(b))),(-1,vec(N,x+y,st(a+b))))
def sl(N,k):return combination((1,vec(N,k+1,2)),(-1,vec(N,k,1)))
def ju(N,k):return combination((1,vec(N,k,1)),(-1,vec(N,k,2)))
def sp(N,k):return combination((2,vec(N,k,0)),(-1,vec(N,k,1)),(-1,vec(N,k,2)))
def minus(a,b):return combination((1,a),(-1,b))
def contains(c,x):return c[0]<=x<=c[1]
def relative(c,x):return x==c[0] if c[0]==c[1] else c[0]<x<c[1]
def feasible(cells,v,d):
 for c,t,e in zip(cells,(v[0],v[1],sum(v)),(d[0],d[1],sum(d))):
  if not contains(c,t):return False
  if c[0]==c[1]:
   if e:return False
  elif t==c[0] and e<=0:return False
  elif t==c[1] and e>=0:return False
 return True

def vertices(cells):
 lines=[]
 for c,(a,b) in zip(cells,((1,0),(0,1),(1,1))):
  for k in c:lines.append((a,b,k))
 V=set()
 for (a,b,c),(d,e,f) in combinations(lines,2):
  det=a*e-b*d
  if det:
   x=Q(c*e-b*f,det);y=Q(a*f-c*d,det)
   if all(contains(c,t) for c,t in zip(cells,(x,y,x+y))):V.add((x,y))
 if not V:return None
 avg=(sum(x for x,y in V)/len(V),sum(y for x,y in V)/len(V))
 if not all(relative(c,t) for c,t in zip(cells,(avg[0],avg[1],sum(avg)))):return None
 return sorted(V)

def dim(V):
 if len(V)==1:return 0
 x,y=V[0];a,b=V[1]
 return 2 if any((a-x)*(d-y)!=(b-y)*(c-x) for c,d in V[2:]) else 1

def projected(V):return [(min(v[j] for v in V),max(v[j] for v in V)) for j in (0,1)]+[(min(sum(v) for v in V),max(sum(v) for v in V))]
def onzero(p,Z):
 if len(Z)==1:return p==Z[0]
 if dim(Z)==2:return True
 (x,y),(u,v)=Z[0],Z[-1]
 return (u-x)*(p[1]-y)==(v-y)*(p[0]-x) and min(x,u)<=p[0]<=max(x,u) and min(y,v)<=p[1]<=max(y,v)

def reference(N,cells,V,Z):
 out=[]
 for x,y in product(range(N+1),repeat=2):
  if onzero((x,y),Z):
   for d in DIRECTIONS.values():
    if feasible(cells,(x,y),d):out.append(row(N,x,y,d))
 return out

def factor(N,cells,V,Z):
 out=[]
 # Every zero vertex of the coarse face and every realizable sector.
 for x,y in Z:
  for d in DIRECTIONS.values():
   if feasible(cells,(x,y),d):out.append(row(N,int(x),int(y),d))
 P=[tuple(map(int,c)) for c in projected(Z)];zdim=dim(Z)
 def regular(c):
  for k in range(c[0]+1,c[1]):out.extend([ju(N,k),sp(N,k)])
 if zdim==2:
  first=None
  for c in P:
   regular(c)
   for k in range(*c):
    if first is None:first=sl(N,k)
    else:out.append(minus(first,sl(N,k)))
 elif zdim==1:
  fixed=[i for i,c in enumerate(P) if c[0]==c[1]];assert len(fixed)==1
  j=fixed[0];t=P[j][0];dom=P[1] if j==0 else P[0]
  mapcell=(lambda k:t-k-1) if j==2 else (lambda k:k+t)
  mappoint=(lambda k:t-k) if j==2 else (lambda k:k+t)
  for k in range(*dom):out.append(minus(sl(N,k),sl(N,mapcell(k))))
  if dim(V)==2:
   for c in P:regular(c)
  else:
   for k in range(dom[0]+1,dom[1]):
    out.append(minus(ju(N,k),ju(N,mappoint(k))))
    out.append(combination((1,sp(N,k)),(1 if j==2 else -1,sp(N,mappoint(k)))))
 return out

def rank(A):
 A=sorted(set(tuple(a) for a in A))
 return int(Matrix(A).to_DM().rank()) if A else 0

def run():
 result={'status':'PASS','sector_state_count':len(DIRECTIONS),'local_comparisons':0,'discarded_empty_relative_triples':0,'categories':{},'grid_sizes':[]}
 for N,B in [(4,[0,2,4]),(6,[0,1,4,6]),(8,[0,2,6,8])]:
  result['grid_sizes'].append(N)
  points=sorted(set(B+[x+N for x in B]));xy=[(x,x) for x in B]+list(zip(B[:-1],B[1:]));z=[(x,x) for x in points]+list(zip(points[:-1],points[1:]))
  for cells in product(xy,xy,z):
   V=vertices(cells)
   if V is None:
    result['discarded_empty_relative_triples']+=1;continue
   zerofaces={tuple(V)}|{(v,) for v in V}
   if dim(V)==2:
    for j,c in enumerate(cells):
     for a in c:
      W=tuple(v for v in V if (v[0],v[1],sum(v))[j]==a)
      if W:zerofaces.add(W)
   for Z in zerofaces:
    A=reference(N,cells,V,Z);C=factor(N,cells,V,Z)
    ra,rc,ru=rank(A),rank(C),rank(A+C)
    if not ra==rc==ru:raise AssertionError((N,cells,V,Z,ra,rc,ru))
    cat=f'{dim(V)}d_coarse_{dim(Z)}d_zero';result['categories'][cat]=result['categories'].get(cat,0)+1
    result['local_comparisons']+=1
  print('completed N',N, result['local_comparisons'],flush=True)
 Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
