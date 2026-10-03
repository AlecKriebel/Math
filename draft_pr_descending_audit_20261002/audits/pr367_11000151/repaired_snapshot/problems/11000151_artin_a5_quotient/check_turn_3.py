#!/usr/bin/env python3
"""Exhaustive20-letter certificate; no search cap, no faithfulness assumption."""
import json,hashlib
from pathlib import Path
n=0
def ck(x):
 global n
 assert x;n+=1
def inv(w):return tuple(-a for a in w[::-1])
def red(w):
 out=[]
 for a in w:
  if out and out[-1]==-a:out.pop()
  else:out.append(a)
 return tuple(out)
def subst(w,im):return red(a for x in w for a in(im[x-1]if x>0 else inv(im[-x-1])))
I=((1,),(2,),(3,),(4,))
A={1:((1,),(1,2),(1,3),(1,4)),2:((1,-2,1),(1,),(3,),(4,)),3:((1,),(2,-3,2),(2,),(4,)),4:((1,),(2,),(3,-4,3),(3,)),5:((1,),(2,),(3,),(3,-2,1,4)),-1:((1,),(-1,2),(-1,3),(-1,4)),-2:((2,),(2,-1,2),(3,),(4,)),-3:((1,),(3,),(3,-2,3),(4,)),-4:((1,),(2,),(4,),(4,-3,4)),-5:((1,),(2,),(3,),(-1,2,-3,4))}
def act(w):
 im=I
 for a in w:im=tuple(subst(x,A[a])for x in im)
 return im
for i in range(1,6):
 ck(act((i,-i))==I);ck(act((-i,i))==I)
 if i<5:ck(act((i,i+1,i))==act((i+1,i,i+1)))
 for j in range(i+2,6):ck(act((i,j))==act((j,i)))
c=(1,2,3,4)*5;h=(5,4,3,2,1,1,2,3,4,5);ck(act(c+inv(h))==I)
target=act(c+c);ck(target==act(h+h))
# The positive central-strand word is exactly its nearest-neighbour position walk.
def words(k):
 def visit(pos,counts,w):
  if len(w)==20:
   if pos==k:yield w
   return
  for q in(pos-1,pos+1):
   if 0<=q<6:
    e=min(pos,q)
    if counts[e]<4:
     new=list(counts);new[e]+=1;yield from visit(q,tuple(new),w+(e+1,))
 yield from visit(k,(0,)*5,())
allwords=set();accepted=set();counts=[];kept=[]
for k in range(6):
 ws=list(words(k));ck(len(ws)==(81 if k in(0,5)else 162));counts.append(len(ws));matches=[]
 for w in ws:
  ck(len(w)==20 and all(w.count(i)==4 for i in range(1,6)))
  allwords.add(w)
  if act(w)==target:accepted.add(w);matches.append(w)
 kept.append(len(matches))
ck(len(allwords)==810);ck(len(accepted)==10)
rotations={(h+h)[i:]+(h+h)[:i]for i in range(20)}
ck(accepted==rotations)
for w in rotations:ck(act(w)==target)
stream='\n'.join(''.join(map(str,w))for w in sorted(accepted))+'\n'
p=Path(__file__).with_name('TURN_3_SURVIVORS.txt')
if p.exists():ck(p.read_bytes()==stream.encode())
else:p.write_bytes(stream.encode());ck(True)
print(json.dumps({'status':'PASS','exact_assertions':n,'center_candidate_counts':counts,'center_survivor_counts':kept,'candidate_words':len(allwords),'survivors':len(accepted),'survivor_sha256':hashlib.sha256(stream.encode()).hexdigest(),'all_survivors_cyclic_rotations_of_h_squared':True,'scope':'Exhaustive under the proved star-linking reduction. Automorphism representation is used only as a necessary test; accepted words have direct central cyclic-rotation certificates in G. Thirty-letter classification remains unresolved.'},indent=2,sort_keys=True))
