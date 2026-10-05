"""Finite simplicial complexes and exact homology over Q and prime fields."""
from itertools import combinations
from exact_linear import rank,zeros,mm

def closure(facets):
 return {tuple(sorted(c)) for f in facets for k in range(1,len(f)+1) for c in combinations(f,k)}
def barycentric(K):
 fs=sorted(K,key=lambda x:(len(x),x));sets=list(map(set,fs));fac=[]
 def visit(chain,last):
  fac.append(tuple(chain))
  for j in range(last+1,len(fs)):
   if sets[last]<sets[j]:visit(chain+[j],j)
 for i in range(len(fs)):visit([i],i)
 return closure(fac),fs

def puncture(K,sigma):return {f for f in K if not set(f)&set(sigma)}
def boundaries(K):
 d=max(map(len,K),default=0)-1;cs=[sorted(f for f in K if len(f)==k+1) for k in range(d+1)];D=[]
 for k in range(1,d+1):
  ix={f:i for i,f in enumerate(cs[k-1])};M=zeros(len(cs[k-1]),len(cs[k]))
  for j,f in enumerate(cs[k]):
   for a in range(len(f)):M[ix[f[:a]+f[a+1:]]][j]=(-1)**a
  D.append(M)
 return cs,D

def betti(K,p=0):
 cs,D=boundaries(K)
 if not cs:return []
 rs=[rank(M,p) for M in D]
 return [len(c)-(rs[k-1] if k else 0)-(rs[k] if k<len(rs) else 0) for k,c in enumerate(cs)]
def graph(K):
 vs={f[0] for f in K if len(f)==1};E={frozenset(f) for f in K if len(f)==2};return vs,E

def cliques(K):
 vs,E=graph(K);out=set()
 def rec(cur,cands):
  for i,v in enumerate(cands):
   nxt=cur+(v,);out.add(nxt);rec(nxt,[w for w in cands[i+1:] if frozenset((v,w)) in E])
 rec((),sorted(vs));return out

def square(K):
 vs,E=graph(K)
 for a,c in combinations(sorted(vs),2):
  if frozenset((a,c)) in E:continue
  common=[b for b in vs if frozenset((a,b)) in E and frozenset((c,b)) in E]
  for b,d in combinations(common,2):
   if frozenset((b,d)) not in E:return a,b,c,d
 return None

def surface_models():
 rp=closure([(1,2,3),(1,2,4),(1,3,5),(1,4,6),(1,5,6),(2,3,6),(2,4,5),(2,5,6),(3,4,5),(3,4,6)])
 fs=[]
 for i in range(5):
  T=lambda j:1+j%5
  B=lambda j:6+j%5
  fs.extend([(0,T(i),T(i+1)),(11,B(i),B(i+1)),(T(i),T(i+1),B(i)),(T(i),B(i-1),B(i))])
 return rp,closure(fs)
