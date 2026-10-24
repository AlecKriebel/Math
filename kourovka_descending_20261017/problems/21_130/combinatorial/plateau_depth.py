#!/usr/bin/env python3
import itertools,json,collections
from pathlib import Path
from monotone_landscape import canonical

def probe(A,mods):
 n=len(A);C=[[tuple((x+y)%m for x,y,m in zip(a,b,mods)) for b in A] for a in A]
 cycles=[(0,)+t for t in itertools.permutations(range(1,n)) if t[0]<t[-1]]
 scores={a:len({C[a[i]][a[(i+1)%n]] for i in range(n)}) for a in cycles}
 sw=[(i,j) for i in range(n) for j in range(i+2,n) if(i,j)!=(0,n-1)]
 dist={a:0 for a in cycles if scores[a]==n};q=collections.deque(dist);nxt={}
 while q:
  a=q.popleft()
  for i,j in sw:
   b=canonical(a[:i+1]+tuple(reversed(a[i+1:j+1]))+a[j+1:])
   if b not in dist and scores[b]<=scores[a]:dist[b]=dist[a]+1;nxt[b]=a;q.append(b)
 maxby={s:max(dist[a] for a in cycles if scores[a]==s) for s in set(scores.values())}
 nonimproving=[]
 for a in cycles:
  if scores[a]==n:continue
  bscore=max(scores[canonical(a[:i+1]+tuple(reversed(a[i+1:j+1]))+a[j+1:])] for i,j in sw)
  if bscore<=scores[a]:nonimproving.append(a)
 worst=max(nonimproving,key=lambda a:dist[a]) if nonimproving else max(cycles,key=lambda a:dist[a])
 path=[worst]
 while path[-1] in nxt:path.append(nxt[path[-1]])
 return {'moduli':mods,'subset':A,'max_distance_by_score':maxby,'strict_local_maxima_or_plateaux':len(nonimproving),'worst_plateau_repair':path,'worst_path_scores':[scores[a] for a in path],'unreached':len(cycles)-len(dist)}
instances=[([(x,) for x in range(6)],(7,)), ([(x,) for x in range(9)],(9,)), (list(itertools.product(range(3),repeat=2)),(3,3)), ([(x,) for x in range(10)],(11,))]
out=[probe(A,M) for A,M in instances]
Path('plateau_depth_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
