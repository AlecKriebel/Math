"""Independent reverse-DAG certificate and labeled-strand star enumeration.
No candidate code is imported. Generic free substitutions use full automorphism tables.
"""
from pathlib import Path
from itertools import combinations
from datetime import datetime,timezone
import gzip,hashlib,json

OWN=Path(__file__).resolve().parent
def inverse(word):return tuple(-v for v in word[::-1])
def freely_reduce(word):
 stack=[]
 for v in word:
  if stack and stack[-1]==-v:stack.pop()
  else:stack.append(v)
 return tuple(stack)
def substitute(word,table):
 flat=[]
 for v in word:flat.extend(table[v-1] if v>0 else inverse(table[-v-1]))
 return freely_reduce(flat)
def append_action(images,table):return tuple(substitute(word,table) for word in images)
def action(word,tables,rank):
 out=tuple((j,) for j in range(1,rank+1))
 for g in word:out=append_action(out,tables[g-1])
 return out
f6=[]
for g in range(1,6):
 table=[(j,) for j in range(1,7)];table[g-1]=(g,g+1,-g);table[g]=(g,);f6.append(tuple(table))
pairs=list(combinations(range(6),2));powers={pair:3**j for j,pair in enumerate(pairs)}
FULL=3**15-1;ID=tuple(range(6))
def step(state,g,direction):
 code,perm=state;a,b=perm[g],perm[g+1];power=powers[tuple(sorted((a,b)))];digit=(code//power)%3
 if (direction==1 and digit==2) or (direction==-1 and digit==0):return None
 order=list(perm);order[g],order[g+1]=order[g+1],order[g]
 return code+direction*power,tuple(order)
def graph(start,direction):
 order=[start];perms={start[0]:start[1]};parents={start[0]:None};edges=0
 for state in order:
  for g in range(4,-1,-1):
   nxt=step(state,g,direction)
   if nxt is None:continue
   edges+=1;code,perm=nxt
   if code in perms:assert perms[code]==perm
   else:perms[code]=perm;parents[code]=(state[0],g+1);order.append(nxt)
 return order,perms,parents,edges
forward,fp,parent,fe=graph((0,ID),1)
backward,bp,_,be=graph((FULL,ID),-1)
co=set(fp)&set(bp)
assert all(fp[c]==bp[c] for c in co)
assert co=={c for c in fp if FULL-c in fp}
images={0:tuple((j,) for j in range(1,7))}
for code,perm in forward:
 if code==0 or code not in co:continue
 previous,g=parent[code];assert previous in images
 images[code]=append_action(images[previous],f6[g-1])
equalities=0
for code,perm in forward:
 if code not in co:continue
 for g in range(4,-1,-1):
  nxt=step((code,perm),g,1)
  if nxt is None or nxt[0] not in co:continue
  assert append_action(images[code],f6[g])==images[nxt[0]];equalities+=1
assert images[FULL]==action((1,2,3,4,5)*6,f6,6)
digest=hashlib.sha256();raw_bytes=0
with gzip.GzipFile(filename=str(OWN/'fullstreams/independent_backward_records.txt.gz'),mode='wb',mtime=0) as out:
 for code in sorted(co):
  packed=sum(v<<(3*j) for j,v in enumerate(fp[code]));line=('S|'+str(code)+'|'+str(packed)+'|'+'|'.join(','.join(map(str,word)) for word in images[code])+'\n').encode();digest.update(line);raw_bytes+=len(line);out.write(line)
assert digest.hexdigest()=='af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf'
# Equal crossing-vector positive pure prefixes can still be unequal braids.
def trace(word):
 state=(0,ID)
 for g in word:
  state=step(state,g-1,1);assert state is not None
 return state
left=(1,1,2,2);right=(2,2,1,1);collision=trace(left)
assert collision==trace(right) and action(left,f6,6)!=action(right,f6,6)
assert collision[0] in fp and collision[0] not in co
# Independent twenty-letter search follows the labeled permutation, rather than edge-count walks.
f4=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),
    ((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),
    ((1,),(2,),(3,),(3,-2,1,4))]
h=(5,4,3,2,1,1,2,3,4,5);target=action(h+h,f4,4);survivors=set();census=[];kept=[]
for center in range(6):
 count=[0];accepted=[0]
 def visit(perm,crossed,word,im):
  if len(word)==20:
   if perm!=ID:return
   assert all(crossed[v]==4 for v in range(6) if v!=center)
   count[0]+=1
   if im==target:survivors.add(word);accepted[0]+=1
   return
  location=perm.index(center)
  for adjacent in [location+1,location-1]:
   if not 0<=adjacent<6:continue
   other=perm[adjacent]
   if crossed[other]>=4:continue
   updated=list(crossed);updated[other]+=1;order=list(perm);order[location],order[adjacent]=order[adjacent],order[location];g=min(location,adjacent)+1
   visit(tuple(order),tuple(updated),word+(g,),append_action(im,f4[g-1]))
 visit(ID,(0,)*6,(),tuple((j,) for j in range(1,5)));census.append(count[0]);kept.append(accepted[0])
assert census==[81,162,162,162,162,81] and kept==[1,2,2,2,2,1]
assert survivors=={(h+h)[j:]+(h+h)[:j] for j in range(20)}
bad=list(f4);bad[-1]=((1,),(2,),(3,),(3,-2,4))
assert action((1,2,3,4)*5,bad,4)!=action(h,bad,4)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
 'mechanism':'Independent backward adjacency graph from full count state; generic free substitutions; reverse generator exploration order; labeled-permutation star recursion; no candidate imports',
 'forward_states':len(fp),'forward_edges':fe,'backward_states':len(bp),'backward_edges':be,
 'actual_forward_backward_intersection_states':len(co),'exact_coaccessible_edge_equalities':equalities,
 'complete_action_stream_raw_bytes':raw_bytes,'complete_action_stream_sha256':digest.hexdigest(),
 'negative_prefix_collision':{'left':left,'right':right,'count_code':collision[0],'same_count_permutation':True,'different_full_free_actions':True,'not_coaccessible':True},
 'twenty_candidate_counts':census,'twenty_survivor_counts':kept,'twenty_unique_survivors':len(survivors),
 'mutated_F4_generator_fails_relator':True}
(OWN/'receipts/independent_controls.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
