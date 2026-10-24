#!/usr/bin/env python3
"""Small exact combinatorial certificate for all five-vertex sum colorings."""
import itertools,json,collections
from pathlib import Path
V=tuple(range(5)); quads=list(itertools.combinations(V,4))
matchings=[]
for a,b,c,d in quads:
 matchings.append([((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))])
cycles=[(0,)+p for p in itertools.permutations(range(1,5)) if p[0]<p[-1]]
edges=[{tuple(sorted((a[i],a[(i+1)%5]))) for i in range(5)} for a in cycles]
perms=list(itertools.permutations(V))
def canon_pair(M,p):return tuple(sorted(tuple(sorted((p[a],p[b]))) for a,b in M))
def image(choice,p):
 out=[None]*5
 for j,c in enumerate(choice):
  M=canon_pair(matchings[j][c],p)
  Q=tuple(sorted(x for e in M for x in e));i=quads.index(Q)
  out[i]=matchings[i].index(M)
 return tuple(out)
seen=set();orbits=[]
for choice in itertools.product(range(3),repeat=5):
 if choice in seen:continue
 orbit={image(choice,p) for p in perms};seen.update(orbit)
 bad=set()
 for j,c in enumerate(choice):
  M=matchings[j][c]
  bad.update(i for i,E in enumerate(edges) if all(e in E for e in M))
 good=[cycles[i] for i in range(12) if i not in bad]
 orbits.append({'choice':choice,'matchings':[matchings[j][c] for j,c in enumerate(choice)],'orbit_size':len(orbit),'bad_cycles':len(bad),'rainbow_witness_cycles':good})
result={'total_assignments':len(seen),'orbit_count':len(orbits),'orbits':orbits,'all_have_rainbow_witness':all(x['rainbow_witness_cycles'] for x in orbits)}
Path('five_vertex_orbits.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
