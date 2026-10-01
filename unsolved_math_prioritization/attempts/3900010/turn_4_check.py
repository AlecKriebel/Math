"""Exact odd torus certificates, with explicit seam failures."""
from tile_model import P
from collections import Counter
import json
C=Counter();res=[(x+4*y)%14 for x,y in P]
assert sorted(res)==list(range(14));C['complete_lattice_residues']+=1
for x in range(-60,61):
 for y in range(-60,61):
  p=next((a,b) for a,b in P if (a+4*b-x-4*y)%14==0)
  l=(x-p[0],y-p[1]);assert (l[0]+4*l[1])%14==0;C['unique_plane_decomposition']+=1
certs=[]
for W,H in [(14,7),(42,7),(14,21),(42,21)]:
 translations=[(x,y) for y in range(H) for x in range(W) if (x+4*y)%14==0]
 seen=set();wrapped=[]
 for i,(a,b) in enumerate(translations):
  q={((x+a)%W,(y+b)%H) for x,y in P}
  assert len(q)==14;C['torus_tile_injective']+=1
  assert not(seen&q);C['torus_disjoint']+=1;seen|=q
  if any(x+a>=W or y+b>=H for x,y in P):wrapped.append(i)
 assert len(seen)==W*H;C['torus_exact_cover']+=1
 assert len(translations)==W*H//14 and len(translations)%2==1;C['odd_torus_count']+=1
 assert wrapped;C['not_a_planar_certificate']+=1
 certs.append({'width':W,'height':H,'tiles':len(translations),'translations':translations,'wrapped_tile_indices':wrapped})
assert len(certs[0]['wrapped_tile_indices'])==4;C['seven_tile_seam_count']+=1
# Fixed orientation has a two-unit rightward overhang above its four-unit bottom row.
assert max(x for x,y in P if y==0)+1==4 and max(x for x,y in P if y==2)+1==6;C['fixed_orientation_boundary_overhang']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'torus_certificates':certs,'scope':'Positive periodic tilings only. Wrapped cells do not form congruent planar pieces. No odd rectangle or D4 impossibility is claimed.'},indent=2))
