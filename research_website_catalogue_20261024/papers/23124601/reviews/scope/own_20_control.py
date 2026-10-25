#!/usr/bin/env python3
"""Independent literal-table/free-group/star-walk reconstruction; no support imports."""
from pathlib import Path
from itertools import combinations
import json,hashlib
E=Path(__file__).absolute().parent
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),((1,),(2,),(3,),(3,-2,1,4))]
Ai=[((1,),(-1,2),(-1,3),(-1,4)),((2,),(2,-1,2),(3,),(4,)),((1,),(3,),(3,-2,3),(4,)),((1,),(2,),(4,),(4,-3,4)),((1,),(2,),(3,),(-1,2,-3,4))]
def inv(w):return tuple(-x for x in w[::-1])
def substitute(w,images):
 s=[]
 for x in w:
  for y in (images[x-1] if x>0 else inv(images[-x-1])):
   if s and s[-1]==-y:s.pop()
   else:s.append(y)
 return tuple(s)
def act(word,maps=A,n=4):
 images=tuple((i,) for i in range(1,n+1))
 for i in word:images=tuple(substitute(w,maps[i-1]) for w in images)
 return images
identity=tuple((i,) for i in range(1,5)); checks=[]
for i in range(5):
 checks += [('inverse-forward-'+str(i+1),tuple(substitute(w,Ai[i]) for w in A[i])==identity),('inverse-backward-'+str(i+1),tuple(substitute(w,A[i]) for w in Ai[i])==identity)]
for i in range(1,5):checks.append(('braid-'+str(i),act((i,i+1,i))==act((i+1,i,i+1))))
for i,j in combinations(range(1,6),2):
 if abs(i-j)>1:checks.append(('commute-'+str(i)+str(j),act((i,j))==act((j,i))))
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5);z=(1,2,3,4,5)*6
checks.append(('quotient-c=h',act(c)==act(h)))
assert all(v for _,v in checks),checks
assert len(checks)==21
assert act(c+h)==act(z)==act(h+h)==act(c+c)
counts=[];rows=[];survivors=[]
def walks(start):
 def rec(pos,counts,w):
  if len(w)==20:
   if pos==start:yield w
   return
  for to in [pos-1,pos+1]:
   if not 1<=to<=6:continue
   edge=min(pos,to)
   if counts[edge-1]>=4:continue
   nxt=list(counts);nxt[edge-1]+=1
   yield from rec(to,nxt,w+(edge,))
 yield from rec(start,[0]*5,())
for start in range(1,7):
 words=list(walks(start));counts.append(len(words));good=0
 for w in words:
  ims=act(w);ok=ims==act(c+c)
  rows.append({'start':start,'word':list(w),'full_four_images':[list(x) for x in ims],'matches_target':ok})
  if ok:survivors.append(w);good+=1
 assert good==[1,2,2,2,2,1][start-1]
assert counts==[81,162,162,162,162,81]
assert len({tuple(x['word']) for x in rows})==810
rotations={((h+h)[i:]+(h+h)[:i]) for i in range(20)}
assert len(rotations)==10 and set(survivors)==rotations
pairs=list(combinations(range(1,7),2))
def crossing(w):
 order=list(range(1,7));d={ij:0 for ij in pairs}
 for i in w:
  a,b=order[i-1:i+1];d[tuple(sorted((a,b)))]+=1;order[i-1],order[i]=b,a
 return tuple(order),tuple(d[ij] for ij in pairs)
assert all(crossing(w)[0]==tuple(range(1,7)) for w in [c,h,z])
T=[]
for i in range(1,6):
 m=[(j,) for j in range(1,7)];m[i-1]=(i,i+1,-i);m[i]=(i,);T.append(tuple(m))
u=(1,1,2,2);v=(2,2,1,1)
assert crossing(u)==crossing(v) and act(u,T,6)!=act(v,T,6)
mut=list(A);mut[4]=mut[4][:-1]+((3,-2,-1,4),)
mut_failure=act(c,mut)!=act(h,mut);assert mut_failure
stream=''.join(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n' for r in rows)
(E/'own-20-full-records.jsonl').write_text(stream)
r={'presentation_checks':dict(checks),'all_21_exact_equalities_hold':True,'candidate_counts_by_start':counts,'distinct_candidates':len(rows),'survivors_by_start':[sum(x['matches_target'] and x['start']==i for x in rows) for i in range(1,7)],'survivors':[list(w) for w in sorted(set(survivors))],'exactly_ten_distinct_cyclic_rotations_h_squared':True,'central_model_actions_equal':True,'model_crossing_counts':{name:list(crossing(w)[1]) for name,w in [('c',c),('h',h),('z',z)]},'negative_controls':{'equal_pair_counts_prefixes_have_different_full_F6_actions':True,'changed_A5_relation_fails':mut_failure},'full_record_bytes':len(stream.encode()),'full_record_sha256':hashlib.sha256(stream.encode()).hexdigest(),'not_a_faithfulness_claim_for_F4':True}
(E/'own-20-results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['survivors','model_crossing_counts']},indent=2))
