from itertools import combinations,product
from collections import deque
import json
n=0
def ck(x):
 global n
 assert x;n+=1
for m in range(3,8):
 G=list(product(range(m),range(2)));one=(0,0)
 def mul(a,b):return ((a[0]+(-1)**a[1]*b[0])%m,(a[1]+b[1])%2)
 def inv(a):return ((-(-1)**a[1]*a[0])%m,a[1])
 def dist(S):
  D={one:0};q=deque([one])
  while q:
   a=q.popleft()
   for b in S:
    c=mul(a,b)
    if c not in D:D[c]=D[a]+1;q.append(c)
  return D
 non=[a for a in G if a!=one]
 for r in range(1,4):
  for tup in combinations(non,r):
   S=set(tup);D=dist(S)
   if len(D)!=len(G):continue
   sym=dist(S|{inv(s) for s in S});R=max(D[inv(s)] for s in S)
   ck(max(D.values())<=max(sym.values())*max(1,R))
   # Positive Schreier generators for the rotation subgroup, arbitrary S.
   reps=[one,min((g for g in G if g[1]),key=lambda g:D[g])]
   T={mul(mul(reps[q],s),inv(reps[(q+s[1])%2])) for q in range(2) for s in S}
   DT=dist(T);ck(set(DT)=={(a,0) for a in range(m)})
   q=max(D[x] for x in reps);c=max(D[inv(x)] for x in reps)
   ck(max(D[t] for t in T)<=q+1+c)
   ck(max(D.values())<=max(DT.values())*(q+1+c)+q)
# Exact Cartesian distances for directed cyclic factors.
for a,b in product(range(2,12),repeat=2):
 for x,y in product(range(a),range(b)):
  # Cartesian {0,1} in each factor has independent coordinate padding.
  D={(0,0):0};q=deque([(0,0)])
  while q:
   u,v=q.popleft()
   for du,dv in ((1,0),(0,1),(1,1)):
    w=((u+du)%a,(v+dv)%b)
    if w not in D:D[w]=D[(u,v)]+1;q.append(w)
  ck(D[x,y]==max(x,y))
print(json.dumps({'result':'PASS','assertions':n,'scope':'Bounded independent controls, no author imports; no infinite CB inference'},indent=2))
