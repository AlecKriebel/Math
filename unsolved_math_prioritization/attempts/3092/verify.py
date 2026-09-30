from itertools import combinations
from functools import lru_cache
from collections import defaultdict
from math import comb
from pathlib import Path
import hashlib,json
nchecks=0;edges=0;vertices=0
for n in range(4,31):
 m=(n+1)//2
 weight=lambda a,b:((a+b)%n)//2
 for a,b,c,d in combinations(range(n),4):
  assert weight(a,c)!=weight(b,d);nchecks+=1
 q=n//2;D=[(i,i+q) for i in range(q)]
 for (a,c),(b,d) in combinations(D,2):
  assert a<b<c<d;nchecks+=1
for n in range(3,11):
 def diag(a,b):return b-a>1 and (a,b)!=(0,n-1)
 @lru_cache(None)
 def tris(V):
  if len(V)<=2:return (frozenset(),)
  out=[]
  for k in range(1,len(V)-1):
   extra={e for e in [(V[0],V[k]),(V[k],V[-1])] if diag(*e)}
   for a in tris(V[:k+1]):
    for b in tris(V[k:]):out.append(a|b|extra)
  return tuple(out)
 Ts=tris(tuple(range(n)));assert len(set(Ts))==len(Ts)==comb(2*(n-2),n-2)//(n-1);nchecks+=1;vertices+=len(Ts)
 m=(n+1)//2;colors=[sum(((a+b)%n)//2 for a,b in T)%m for T in Ts]
 buckets=defaultdict(list)
 for i,T in enumerate(Ts):
  assert len(T)==n-3;nchecks+=1
  for e in T:buckets[frozenset(T-{e})].append(i)
 degs=[0]*len(Ts)
 for common,ids in buckets.items():
  assert len(ids)==2;nchecks+=1
  i,j=ids;assert colors[i]!=colors[j];nchecks+=1;edges+=1
  degs[i]+=1;degs[j]+=1
 assert all(d==n-3 for d in degs);nchecks+=1
r={'assertions':nchecks,'triangulations_checked':vertices,'flip_edges_checked':edges,'all_pass':True,'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Restricted additive coloring only; no exact chromatic-number or unboundedness computation.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
