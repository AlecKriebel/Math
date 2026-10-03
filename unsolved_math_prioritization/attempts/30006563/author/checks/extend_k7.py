"""Bounded exact search: extend the specified K7 seed to K9 with three colors.
A negative result concerns only this fixed seed; no general K9 lower bound.
"""
from itertools import combinations, product
import json, signal, time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
A={0,1,2};B={3,4,5};z=6
seed={(i,j):int(i==z or j==z or (i in A and j in A)) for i,j in combinations(range(7),2)}
pairs=list(combinations(range(7),2))
trips=list(combinations(range(7),3))
def sig(cs):return tuple(sorted(cs))
old=[(set(t),sig(seed[e] for e in combinations(t,2))) for t in trips]
def pattern_ok(p):
 for i,j in pairs:
  s=sig((p[i],p[j],seed[i,j]))
  if any(i not in t and j not in t and ttype==s for t,ttype in old):return False
 return True
patterns=[p for p in product(range(3),repeat=7) if pattern_ok(p)]
canonical=[p for p in patterns if tuple(sorted(p[:3]))==p[:3] and tuple(sorted(p[3:6]))==p[3:6]]
wedges={p:[(set((i,j)),sig((p[i],p[j],seed[i,j]))) for i,j in pairs] for p in patterns}

def combined_ok(p,r,d):
 # Triangles with one different new vertex each must not repeat disjointly.
 if any(not(s&t) and a==b for s,a in wedges[p] for t,b in wedges[r]):return False
 # Triangles containing both new vertices need only be compared with old ones.
 for i in range(7):
  ty=sig((p[i],r[i],d))
  if any(i not in t and ty==b for t,b in old):return False
 return True

def direct_verify(color,n):
 signatures={};checked=0
 for t in combinations(range(n),3):
  ty=sig(color[e] for e in combinations(t,2)); ss=set(t)
  for oldt in signatures.get(ty,[]):
   assert ss&oldt
  signatures.setdefault(ty,[]).append(ss)
 for t,u in combinations(list(combinations(range(n),3)),2):
  if set(t).isdisjoint(u):
   checked+=1
   assert sig(color[e] for e in combinations(t,2))!=sig(color[e] for e in combinations(u,2))
 return checked

if __name__=='__main__':
 signal.alarm(30);start=time.monotonic();found=None;tested=0
 for p in canonical:
  for r in patterns:
   for d in range(3):
    tested+=1
    if combined_ok(p,r,d):
     found=(p,r,d);break
   if found:break
  if found:break
 result={'seed_vertices':7,'target_vertices':9,'q':3,'valid_one_vertex_patterns':len(patterns),'canonical_first_patterns':len(canonical),'tested_combinations':tested}
 if found:
  p,r,d=found;color=dict(seed)
  color.update({(i,7):p[i] for i in range(7)})
  color.update({(i,8):r[i] for i in range(7)})
  color[7,8]=d
  result.update(status='FOUND',first_pattern=p,second_pattern=r,new_edge=d,disjoint_pairs_checked=direct_verify(color,9),edge_colors=[[*e,c] for e,c in sorted(color.items())])
 else:result.update(status='NO_EXTENSION_OF_FIXED_SEED',warning='Not a general lower bound for g(9).')
 result['elapsed_seconds']=round(time.monotonic()-start,3)
 (ROOT/'extend_k7_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
