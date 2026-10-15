"""Independent reconstruction from TURN_3 mathematical tuples only."""
import json
from pathlib import Path
O=Path(__file__).resolve().parent

def red(w):
 r=[]
 for x in w:
  if r and r[-1]==-x:r.pop()
  else:r.append(x)
 return tuple(r)
def inverse(w):return tuple(-x for x in w[::-1])
def substitute(w,A):
 r=()
 for x in w:r=red(r+(A[x-1] if x>0 else inverse(A[-x-1])))
 return r
I=((1,),(2,),(3,),(4,))
A=[((1,),(1,2),(1,3),(1,4)),((1,-2,1),(1,),(3,),(4,)),((1,),(2,-3,2),(2,),(4,)),((1,),(2,),(3,-4,3),(3,)),((1,),(2,),(3,),(3,-2,1,4))]
AI=[((1,),(-1,2),(-1,3),(-1,4)),((2,),(2,-1,2),(3,),(4,)),((1,),(3,),(3,-2,3),(4,)),((1,),(2,),(4,),(4,-3,4)),((1,),(2,),(3,),(-1,2,-3,4))]
def comp(B,C):return tuple(substitute(w,C) for w in B)
def action(w):
 r=I
 for x in w:r=comp(r,A[x-1] if x>0 else AI[-x-1])
 return r
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5)
checks={}
for i in range(5):
 checks[f'inverse_left_{i+1}']=comp(A[i],AI[i])==I
 checks[f'inverse_right_{i+1}']=comp(AI[i],A[i])==I
 for j in range(i+1,5):
  u=(i+1,j+1,i+1) if j==i+1 else (i+1,j+1)
  v=(j+1,i+1,j+1) if j==i+1 else (j+1,i+1)
  checks[f'relation_{i+1}_{j+1}']=action(u)==action(v)
checks['added_relation']=action(c)==action(h)
target=action(c*2)
allwords=[];count=[]
for start in range(6):
 words=[]
 def walk(pos,w,counts):
  if len(w)==20:
   if pos==start:words.append(w)
   return
  for nxt in (pos-1,pos+1):
   if 0<=nxt<6:
    edge=min(pos,nxt)
    if counts[edge]<4:
     co=list(counts);co[edge]+=1
     walk(nxt,w+(edge+1,),co)
 walk(start,(),[0]*5)
 count.append(len(words));allwords.extend(words)
survivors=[w for w in allwords if action(w)==target]
rotations=sorted(set((h*2)[i:]+(h*2)[:i] for i in range(20)))
checks['all_survivors_exactly_rotations']=sorted(survivors)==rotations
report={'checks':checks,'all_checks_pass':all(checks.values()),'walk_counts_by_start':count,'total_walks':len(allwords),'survivors':survivors,'survivor_count':len(survivors),'target_images':target,
 'limitation':'This is reconstructed from mathematical narrative; no candidate checker/output read. Non-survivors safely reject Q equality; survivors have explicit Q equality by central cyclic rotation of h².'}
(O/'independent_f4_reduction.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert all(checks.values())
