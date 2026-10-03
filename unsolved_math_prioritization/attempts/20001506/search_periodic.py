#!/usr/bin/env python3
"""Exhaustive explicitly bounded search; NOT an atoroidality certificate."""
import json
from itertools import combinations
from verify import PHI,sub,cyc,conjugacy_key,inv,mat,mul,identity,mpow,det
PAIR=list(combinations(range(5),2))
V=(0,1,0,1,1,0,1,-1,-1,1)
def class2(w):
 v=[0]*5;c=[0]*10
 for x in w:
  j='abcde'.index(x.lower());s=1 if x.islower() else -1
  for k,(i,h) in enumerate(PAIR):
   if h==j:c[k]+=v[i]*s
  v[j]+=s
 assert not any(v)
 return tuple(c)
def survive(c):return c==tuple(c[-1]*z for z in V)
def balanced_words(n):
 alphabet='abcdeABCDE';v=[0]*5
 def go(w):
  k=n-len(w);norm=sum(map(abs,v))
  if norm>k or (k-norm)%2:return
  if not k:
   if w[-1]!=w[0].swapcase():yield w
   return
  for x in alphabet:
   if w and x==w[-1].swapcase():continue
   j='abcde'.index(x.lower());s=1 if x.islower() else -1
   v[j]+=s;yield from go(w+x);v[j]-=s
 yield from go('')
def run(max_len=8,max_period=12):
 counts=[];hits=[];samples=[]
 for n in range(2,max_len+1,2):
  allcount=0;classes=set()
  for w in balanced_words(n):
   allcount+=1;k=min(conjugacy_key(w),conjugacy_key(inv(w)));classes.add(k)
  filtered=[w for w in sorted(classes) if survive(class2(w))]
  for w in filtered:
   z=w;target={conjugacy_key(w),conjugacy_key(inv(w))}
   for p in range(1,max_period+1):
    z=cyc(sub(z))
    if conjugacy_key(z) in target:
     hits.append({'word':w,'unoriented_period':p,'image':z});break
  counts.append({'length':n,'cyclically_reduced_zero_homology_words':allcount,'unoriented_cyclic_classes':len(classes),'passed_class2_necessary_filter':len(filtered)})
  samples.extend(filtered[:3])
 return {'max_cyclic_length':max_len,'max_unoriented_period':max_period,'search_is_complete_only_within_bounds':True,'counts':counts,'hits':hits,'sample_filtered_words':samples}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
