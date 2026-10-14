"""Bounded exact-cover search with a prescribed periodic interior.
A failed/capped search is scoped to its frozen-interior model only.
"""
from tile_model import P,D4
from collections import Counter
import sys,json,time
W,H,margin,phase=map(int,sys.argv[1:5]);cap=int(sys.argv[5]) if len(sys.argv)>5 else 10000
allmask=(1<<(W*H))-1;fixed=[];blocked=0
for y in range(H-2):
 for x in range(W-5):
  if (x+4*y)%14!=phase:continue
  q={(x+a,y+b) for a,b in P}
  if all(margin<=a<W-margin and margin<=b<H-margin for a,b in q):
   mask=sum(1<<(a+W*b) for a,b in q);assert not blocked&mask;blocked|=mask;fixed.append({'x':x,'y':y,'orientation':D4.index(tuple(sorted(P)))})
holes=allmask^blocked;bycell={};placements=[]
for ori,q in enumerate(D4):
 for y in range(H-max(b for a,b in q)):
  for x in range(W-max(a for a,b in q)):
   mask=sum(1<<(x+a+W*(y+b)) for a,b in q)
   if mask&blocked:continue
   j=len(placements);placements.append((mask,{'x':x,'y':y,'orientation':ori}))
   for a,b in q:bycell.setdefault(x+a+W*(y+b),[]).append(j)
# Component divisibility is sound because the tile is edge-connected.
remaining={(i%W,i//W) for i in range(W*H) if holes>>i&1};components=[]
while remaining:
 root=remaining.pop();todo=[root];size=1
 while todo:
  x,y=todo.pop()
  for z in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if z in remaining:remaining.remove(z);todo.append(z);size+=1
 components.append(size)
nodes=0;capped=False;dead=set();path=[]
def solve(uncovered):
 global nodes,capped
 if not uncovered:return True
 if nodes>=cap:capped=True;return False
 if uncovered in dead:return False
 nodes+=1;i=(uncovered&-uncovered).bit_length()-1
 for j in bycell.get(i,[]):
  mask,_=placements[j]
  if mask&uncovered!=mask:continue
  path.append(j)
  if solve(uncovered^mask):return True
  path.pop()
  if capped:return False
 dead.add(uncovered);return False
components.sort()
bad=any(n%14 for n in components);found=False if bad else solve(holes)
out={'width':W,'height':H,'target_tiles':W*H//14,'margin':margin,'phase':phase,'fixed_tiles':len(fixed),'hole_cells':holes.bit_count(),'hole_component_sizes':components,'component_divisibility_obstruction':bad,'legal_repair_placements':len(placements),'nodes':nodes,'node_cap':cap,'capped':capped,'exhausted_for_this_fixed_interior':not capped,'found':found}
if found:
 tiles=fixed+[placements[j][1] for j in path];seen=0
 for t in tiles:
  mask=sum(1<<(t['x']+a+W*(t['y']+b)) for a,b in D4[t['orientation']]);assert not seen&mask;seen|=mask
 assert seen==allmask and len(tiles)==W*H//14
 out['tiles']=tiles
print(json.dumps(out))
