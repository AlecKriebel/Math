"""Standalone exact verification of the credited even rectangle certificate."""
from pathlib import Path
from collections import Counter
import json
from tile_model import P,D4,normalize
C=Counter();assert len(P)==14;C['tile_area']+=1
assert len(D4)==8;C['complete_distinct_orientations']+=1
for q in D4:
 assert len(q)==14;C['orientation_area']+=1
 todo=set(q);stack=[todo.pop()]
 while stack:
  x,y=stack.pop()
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   if (x+dx,y+dy) in todo:todo.remove((x+dx,y+dy));stack.append((x+dx,y+dy))
 assert not todo;C['orientation_connected']+=1
w=json.loads(Path(__file__).with_name('known_even_witness.json').read_text());W,H=w['width'],w['height'];seen=set()
for t in w['tiles']:
 q={(t['x']+x,t['y']+y) for x,y in D4[t['orientation']]}
 assert len(q)==14;C['placement_area']+=1
 for x,y in q:
  assert 0<=x<W and 0<=y<H;C['cell_in_bounds']+=1
  assert (x,y) not in seen;C['cell_not_repeated']+=1
  seen.add((x,y))
assert seen==set((x,y) for x in range(W) for y in range(H));C['exact_cover']+=1
assert len(w['tiles'])==396==W*H//14 and len(w['tiles'])%2==0;C['even_count']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'rectangle':[W,H],'tiles':len(w['tiles']),'scope':'Verifies the credited even witness and discrete model. The Euclidean-to-grid theorem is analytical, and no minimum or odd-case conclusion is inferred.'},indent=2))
