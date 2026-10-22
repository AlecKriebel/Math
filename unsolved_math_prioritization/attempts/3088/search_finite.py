import itertools,math,time
from collections import defaultdict
N=3
# sign canonical robust
V=sorted({tuple((-x if next(t for t in v if t)<0 else x) for x in v) for v in itertools.product(range(-N,N+1),repeat=3) if any(v) and math.gcd(*v)==1})
def dot(a,b):return sum(x*y for x,y in zip(a,b))
E=[e for e in itertools.combinations(range(len(V)),3) if dot(V[e[0]],V[e[1]])*dot(V[e[0]],V[e[2]])*dot(V[e[1]],V[e[2]])<0]
inc=defaultdict(list)
for e in E:
 for v in e:inc[v].append(e)
d=[15]*len(V)
for v in [(1,1,0),(1,-1,0),(1,0,1),(1,0,-1)]:d[V.index(v)]=1
nodes=0
start=time.monotonic()
def search(d):
 global nodes
 nodes+=1
 changed=True
 while changed:
  changed=False
  for a,b,c in E:
   for x,y,z in [(a,b,c),(a,c,b),(b,c,a)]:
    if d[x] and d[x]&(d[x]-1)==0 and d[x]==d[y] and d[z]&d[x]:
     d[z]&=~d[x];changed=True
     if not d[z]:return None
 if all(x&(x-1)==0 for x in d):return d
 v=max((i for i in range(len(V)) if d[i]&(d[i]-1)),key=lambda i:(-d[i].bit_count(),len(inc[i])))
 for bit in [1,2,4,8]:
  if d[v]&bit:
   e=d[:];e[v]=bit;r=search(e)
   if r:return r
 return None
r=search(d)
assert r is not None
import json
from pathlib import Path
out={'height':N,'vectors':V,'colors':[v.bit_length()-1 for v in r],'bad_triples':len(E),'search_nodes':nodes,'meaning':'finite restriction only, no extension to RP2 asserted'}
(Path(__file__).parent/'finite_coloring.json').write_text(json.dumps(out,indent=2)+'\n')
print(len(V),len(E),nodes,'SAT')
