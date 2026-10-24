#!/usr/bin/env python3
"""Extract direct cellular cocycle certificates; independent verifier needs no solver."""
from check_iterated_covers import analyze
from pathlib import Path
from fractions import Fraction as Q
import argparse,collections,json
p=argparse.ArgumentParser();p.add_argument('--search',type=Path,required=True);p.add_argument('--candidates',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
frozen=json.loads(args.search.read_text())['found']['result'];candidates=json.loads(args.candidates.read_text())['results']
a=analyze(frozen['m'],frozen['permutations'],frozen['stable_letter_power'],characters=True)
m=a['m'];perms=a['permutations'];q=len(perms[0]); r=a['stable_letter_power']; ind={tuple(e):j for j,e in enumerate(a['basis_edges'])}
paths={0:[]}; queue=collections.deque([0])
while queue:
 v=queue.popleft()
 for i in range(m):
  w=perms[i][v]
  if w not in paths:paths[w]=paths[v]+[i];queue.append(w)
tw=[[i] for i in range(m)]
for _ in range(r):tw=[[j for k in w for j in ([k] if k==0 else [k,k-1])] for w in tw]
chars=[]
for j in sorted(set(x['character_index'] for x in candidates if x['visible'])):
 ell={int(k):Q(v) for k,v in a['invariant_characters'][j].items()}
 assert all(x.denominator==1 for x in ell.values())
 weights={str(v)+','+str(i):int(ell.get(k,0)) for (v,i),k in ind.items() if ell.get(k,0)}
 def walk(word,start=0):
  value=0;v=start
  for i in word:value+=weights.get(str(v)+','+str(i),0);v=perms[i][v]
  return v,value
 potentials=[]
 for v in range(q):
  end,value=walk([j for i in paths[v] for j in tw[i]]);assert end==v
  end,oldvalue=walk(paths[v]);assert end==v
  potentials.append(value-oldvalue)
 chars.append({'index':j,'positive_edge_weights':weights,'vertex_potentials':potentials})
cert={'claim':'Explicit index1024 subgroup of G5 admits integral characters detecting all recorded powers; this refutes candidate persistent-homology obstructions, not virtual specialness',
 'm':m,'fiber_cover_degree':q,'stable_letter_power':r,'index':q*r,'permutations':perms,'characters':chars,'targets':candidates}
args.output.write_text(json.dumps(cert,indent=2)+'\n')
