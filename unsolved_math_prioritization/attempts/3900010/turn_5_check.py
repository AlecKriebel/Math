"""Verify binary overlap certificate and replay each bounded boundary-repair model."""
from pathlib import Path
from collections import Counter
import json,subprocess,sys
from tile_model import D4
p=Path(__file__).parent;C=Counter();r=json.loads((p/'parity_42x31.json').read_text());W,H=r['width'],r['height'];area=W*H
seen_placements=set();counts=Counter();xor=0
for t in r['selected_placements']:
 key=(t['x'],t['y'],t['orientation']);assert key not in seen_placements;C['distinct_selected_placement']+=1;seen_placements.add(key)
 q={(t['x']+a,t['y']+b) for a,b in D4[t['orientation']]}
 assert len(q)==14;C['selected_tile_area']+=1
 bits=1<<area
 for x,y in q:
  assert 0<=x<W and 0<=y<H;C['selected_cell_in_bounds']+=1;counts[x,y]+=1;bits|=1<<(x+W*y)
 xor^=bits
assert xor==(1<<(area+1))-1;C['explicit_augmented_xor_identity']+=1
assert len(seen_placements)==403 and len(seen_placements)%2==1;C['odd_selected_count']+=1
assert len(counts)==area and all(n%2 for n in counts.values());C['all_cells_odd_coverage']+=1
hist=dict(sorted(Counter(counts.values()).items()));assert {str(k):v for k,v in hist.items()}==r['coverage_histogram'];C['coverage_histogram']+=1
assert any(n>1 for n in counts.values()) and len(seen_placements)!=area//14;C['not_positive_exact_cover']+=1
# Independent rank rebuild without the generator's combination-tracking mechanism.
basis={};ncol=0
for ori,q in enumerate(D4):
 for y in range(H-max(b for a,b in q)):
  for x in range(W-max(a for a,b in q)):
   v=(1<<area)|sum(1<<(x+a+W*(y+b)) for a,b in q);ncol+=1
   while v:
    k=v.bit_length()-1
    if k in basis:v^=basis[k]
    else:basis[k]=v;break
assert ncol==r['number_legal_placements']==8452 and len(basis)==r['rank']==1293;C['independent_rank_rebuild']+=1
b=json.loads((p/'boundary_repair_receipt.json').read_text());summary=Counter()
for m in b['models']:
 out=subprocess.check_output([sys.executable,str(p/'boundary_repair.py'),str(m['width']),str(m['height']),str(m['margin']),str(m['phase']),str(m['node_cap'])]);actual=json.loads(out)
 assert actual==m;C['boundary_model_exact_replay']+=1
 assert not m['found'];C['no_positive_model_witness']+=1
 if m['component_divisibility_obstruction']:
  assert any(n%14 for n in m['hole_component_sizes']);C['component_obstruction_sound']+=1;summary['component_obstructed']+=1
 elif m['capped']:
  assert not m['exhausted_for_this_fixed_interior'];C['cap_not_exhaustion']+=1;summary['capped_inconclusive']+=1
 else:summary['complete_no_repair_fixed_interior']+=1
assert dict(summary)=={'component_obstructed':14,'capped_inconclusive':5,'complete_no_repair_fixed_interior':9};C['model_scope_summary']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'parity_certificate':{'rectangle':[W,H],'selected_tiles':403,'positive_target_tile_count':area//14,'rank':len(basis),'coverage_histogram':hist,'positive_exact_cover':False},'boundary_model_summary':dict(summary),'scope':'Binary overlap cover and specified fixed-interior searches only. No positive odd rectangular tiling or general impossibility is claimed.'},indent=2))
