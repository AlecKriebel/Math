"""Exact finite frontier closure certificates plus a known positive path.
No solver, heuristic pruning, or height cutoff is used for the thirty exhausted widths.
"""
from tile_model import D4
from pathlib import Path
from collections import deque,Counter
import hashlib,json
C=Counter()
def options(W):
 out=[[] for _ in range(W)]
 for ori,q in enumerate(D4):
  for x in range(W):
   for a,b in q:
    if b:continue
    dx=x-a
    if min(a+dx for a,b in q)<0 or max(a+dx for a,b in q)>=W:continue
    z=(sum(1<<(a+dx+W*b) for a,b in q),ori,dx)
    if z not in out[x]:out[x].append(z)
 # Independently generate by every permitted bounding-box translation.
 direct=[set() for _ in range(W)]
 for ori,q in enumerate(D4):
  for dx in range(W-max(a for a,b in q)):
   mask=sum(1<<(a+dx+W*b) for a,b in q)
   for x in range(W):
    if mask>>x&1:direct[x].add((mask,ori,dx))
 for x in range(W):assert set(out[x])==direct[x];C['placement_enumerator_agreement']+=1
 return out
def advance(s,mask,W):
 full=(1<<W)-1;t=s|mask;drop=0
 while t&full==full:t>>=W;drop+=1
 return t,drop
def graph(W,cap=None):
 full=(1<<W)-1;opts=options(W);seen={(0,0)};Q=deque([(0,0)]);edges=0;returns=[0,0];digest=hashlib.sha256();maxbits=0
 while Q:
  s,p=Q.popleft();gap=(~s)&full;x=(gap&-gap).bit_length()-1
  assert x>=0;C['canonical_nonfull_frontier']+=1
  for mask,ori,dx in opts[x]:
   if s&mask:continue
   t,drop=advance(s,mask,W);z=(t,p^1);edges+=1
   assert t.bit_length()<=6*W;C['finite_horizon']+=1;maxbits=max(maxbits,t.bit_length())
   assert t.bit_count()==s.bit_count()+14-W*drop;C['area_conservation']+=1
   digest.update(f'{s},{p}>{t},{p^1}:{ori},{dx},{drop};'.encode())
   if not t:returns[p^1]+=1
   if z not in seen:seen.add(z);Q.append(z)
  if cap is not None and len(seen)>=cap:break
 exhausted=not Q
 statehash=hashlib.sha256(''.join(f'{s},{p};' for s,p in sorted(seen)).encode()).hexdigest()
 return {'width':W,'states':len(seen),'edges':edges,'remaining_queue':len(Q),'exhausted':exhausted,'return_edges_even_odd':returns,'edge_sha256':digest.hexdigest(),'state_sha256':statehash,'max_used_bits':maxbits,'state_cap':cap}
results=[graph(W) for W in range(1,31)]
for r in results:assert r['exhausted'] and r['return_edges_even_odd']==[0,0];C['no_rectangle_any_height_fixed_width']+=1
capped=graph(42,300000);assert not capped['exhausted'];C['capped_search_not_promoted']+=1
# Follow Reid's independently verified even rectangle as a positive frontier path.
w=json.loads(Path(__file__).with_name('known_even_witness.json').read_text());W=w['width'];full=(1<<W)-1;opts=options(W)
lookup={};placed=set()
for i,a in enumerate(w['tiles']):
 for x,y in D4[a['orientation']]:lookup[a['x']+x,a['y']+y]=i
s=h=0
for _ in w['tiles']:
 gap=(~s)&full;x=(gap&-gap).bit_length()-1;i=lookup[x,h];a=w['tiles'][i]
 assert i not in placed and a['y']==h;C['positive_path_new_tile_at_frontier']+=1
 mask=sum(1<<(a['x']+u+W*v) for u,v in D4[a['orientation']])
 assert (mask,a['orientation'],a['x']) in opts[x] and not s&mask;C['positive_path_legal_transition']+=1
 s,drop=advance(s,mask,W);h+=drop;placed.add(i)
assert s==0 and h==w['height'] and len(placed)==396;C['known_even_path_returns']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'complete_fixed_width_certificates':results,'incomplete_search':capped,'positive_control':{'width':W,'height':h,'tiles':len(placed)},'scope':'All heights excluded for widths1 through30 by complete finite-state closure. Widths31 and above remain unresolved here; width42 was additionally capped. No global impossibility or minimum claim.'},indent=2))
