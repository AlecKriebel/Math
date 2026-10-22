"""Independent finite checks for signed-orbit dimension and reconstruction.
This deliberately does not import the candidate reduction or implement AHT.
"""
import random,json
from pathlib import Path
from fractions import Fraction as F
from sympy import Matrix
class DSU:
 def __init__(self,n):self.p=list(range(n))
 def find(self,i):
  while self.p[i]!=i:self.p[i]=self.p[self.p[i]];i=self.p[i]
  return i
 def join(self,i,j):self.p[self.find(i)]=self.find(j)
 def count(self):return len({self.find(i) for i in range(len(self.p))})
def lift(n,edges,zeros=()):
 b=DSU(n);d=DSU(2*n)
 for x,y,s in edges:
  b.join(x,y)
  for e in (0,1):d.join(x+e*n,y+(e^(s<0))*n)
 for x in zeros:d.join(x,x+n)
 return b,d
def dim(n,edges,zeros=()):
 b,d=lift(n,edges,zeros);return d.count()-b.count()
def reps(n,edges,zeros=()):
 killed=list(zeros);out=[]
 while dim(n,edges,killed):
  before=dim(n,edges,killed);lo=0;hi=n-1
  while lo<hi:
   mid=(lo+hi)//2
   if dim(n,edges,killed+list(range(mid+1)))<before:hi=mid
   else:lo=mid+1
  out.append(lo);killed.append(lo)
 return out
rng=random.Random(1827001);cases=[]
for n in range(1,18):
 for trial in range(12):
  edges=[(rng.randrange(n),rng.randrange(n),rng.choice((-1,1))) for _ in range(rng.randrange(2*n+1))]
  zeros=[x for x in range(n) if rng.randrange(7)==0]
  A=[]
  for x,y,s in edges:
   row=[0]*n;row[y]+=1;row[x]-=s;A.append(row)
  for x in zeros:
   row=[0]*n;row[x]=1;A.append(row)
  rank=Matrix(A).rank() if A else 0
  d=dim(n,edges,zeros);assert d==n-rank
  R=reps(n,edges,zeros);assert len(R)==d
  _,D=lift(n,edges,zeros)
  cols=[]
  for r in R:
   c=D.find(r);vec=[int(D.find(k)==c)-int(D.find(k+n)==c) for k in range(n)]
   assert vec[r]==1;assert all(sum(a*b for a,b in zip(row,vec))==0 for row in A)
   cols.append(vec)
  assert (Matrix(cols).rank() if cols else 0)==d
  # Each prefix coefficient is exactly the two-sheet weight difference.
  for col,r in zip(cols,R):
   c=D.find(r)
   for t in range(n+1):
    wplus=sum(D.find(k)==c for k in range(t));wminus=sum(D.find(k+n)==c for k in range(t))
    assert wplus-wminus==sum(col[:t])
  cases.append({'n':n,'trial':trial,'edges':len(edges),'forced_zeros':len(zeros),'dimension':d})
# Check normalized trace reconstruction and inverse for random rational periodic PL functions.
for n in range(1,24):
 for trial in range(10):
  left=[F(rng.randrange(-9,10),rng.randrange(1,8)) for _ in range(n)]
  right=[F(rng.randrange(-9,10),rng.randrange(1,8)) for _ in range(n)]
  point=[F(rng.randrange(-9,10),rng.randrange(1,8)) for _ in range(n)];point[0]=0
  s=[n*(left[(k+1)%n]-right[k]) for k in range(n)]
  j=[right[k]-left[k] for k in range(n)]
  p=[point[k]-(right[k]+left[k])/2 for k in range(n)]
  assert sum(s,F(0))/n+sum(j,F(0))==0
  c=-j[0]/2-p[0]
  for k in range(n):
   l=c+sum(s[:k],F(0))/n+sum(j[:k],F(0))
   assert l==left[k] and l+j[k]==right[k] and l+j[k]/2+p[k]==point[k]
out={'status':'PASS','signed_graph_cases':len(cases),'trace_reconstruction_cases':230,'largest_N':23,'scope':'Dense independent lemma checks only; not an AHT implementation and not a proof of the full sparse reduction.','cases':cases}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print({k:v for k,v in out.items() if k!='cases'})
