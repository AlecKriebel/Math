from itertools import combinations,permutations
import json
E=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3),(1,4),(2,5)];E=[tuple(sorted(e)) for e in E]
tri=[sum(1<<E.index(tuple(sorted(e))) for e in combinations(T,2)) for T in [(0,1,2),(3,4,5)]]
autos=[p for p in permutations(range(6)) if {tuple(sorted((p[a],p[b]))) for a,b in E}==set(E)]
def transform(mask,p):return sum(1<<E.index(tuple(sorted((p[a],p[b])))) for i,(a,b) in enumerate(E) if mask>>i&1)
valid=[m for m in range(1<<9) if all(m&t!=t for t in tri)]
reps=sorted({min(transform(m,p) for p in autos) for m in valid})
S=[sum(1<<x for x in c) for c in combinations(range(8),3)];ALL=(1<<len(S))-1
compat=[[0]*len(S) for _ in range(2)]
for i,s in enumerate(S):
 for j,t in enumerate(S):
  k=(s&t).bit_count()
  if k==0:compat[0][i]|=1<<j
  if k in (1,2):compat[1][i]|=1<<j
nodes=0

def solve(mask):
 adj=[[] for _ in range(6)]
 for i,(a,b) in enumerate(E):adj[a].append((b,0 if mask>>i&1 else 1));adj[b].append((a,0 if mask>>i&1 else 1))
 def dfs(domains):
  global nodes
  nodes+=1
  if nodes>10000000:raise RuntimeError('search cap')
  if any(x==0 for x in domains):return None
  # Arc consistency on the six-variable binary constraint network.
  changed=True
  while changed:
   changed=False
   for a in range(6):
    for b,k in adj[a]:
     d=domains[a];new=0
     while d:
      bit=d&-d;i=bit.bit_length()-1;d-=bit
      if compat[k][i]&domains[b]:new|=bit
     if new!=domains[a]:domains[a]=new;changed=True
     if not new:return None
  undec=[i for i,d in enumerate(domains) if d&(d-1)]
  if not undec:return [d.bit_length()-1 for d in domains]
  a=min(undec,key=lambda i:domains[i].bit_count());d=domains[a]
  while d:
   bit=d&-d;d-=bit;new=domains.copy();new[a]=bit;r=dfs(new)
   if r is not None:return r
  return None
 d=[ALL]*6;d[0]=1 # Global color symmetry fixes vertex0 to palette triple 012.
 return dfs(d)
res=[]
for m in reps:
 before=nodes;c=solve(m);res.append({'mask':m,'triples':None if c is None else [[i+1 for i in range(8) if S[j]>>i&1] for j in c],'nodes':nodes-before})
print(json.dumps({'valid_masks':len(valid),'automorphisms':len(autos),'orbits':len(reps),'nodes':nodes,'failures':[x for x in res if x['triples'] is None],'certificates':res},indent=2))
