from simplicial import *
from itertools import product

def cycle(n,offset=0):return closure([(offset+i,offset+(i+1)%n) for i in range(n)])
def inflate(K,multiplicity):
 vs,_=graph(K);fib={v:[(v,j) for j in range(multiplicity.get(v,1))] for v in sorted(vs)}
 labels=[x for v in sorted(vs) for x in fib[v]];ix={x:i for i,x in enumerate(labels)}
 facets=[tuple(ix[x] for v in f for x in fib[v]) for f in K]
 return closure(facets),labels

def cone(K):
 vs,_=graph(K);a=max(vs,default=-1)+1;return closure([f+(a,) for f in K]),a

def profile(K,p=0):
 best=-1
 for f in [()]+list(K):
  C=puncture(K,f);b=betti(C,p)
  if not b:best=max(best,-1);continue
  b[0]-=1
  best=max([best]+[i for i,x in enumerate(b) if x])
 return best+1
