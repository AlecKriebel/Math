"""Finite exact controls for the binary-section cut classifier; no infinite proof inferred."""
from itertools import product
from collections import Counter
import json
C=Counter(); width=8
pad=lambda s:tuple(s)+(0,)*(width-len(s))
a=pad((-4,));b=pad((4,))
def node(s):return pad((0,)+tuple(s))
B=sorted({a,b}|{node(s) for n in range(7) for s in product((-2,2),repeat=n)})
def retract(x):
 if x[0]<0:return a
 if x[0]>0:return b
 lo,hi=a,b;s=[]
 for v in x[1:]:
  t=node(s)
  if v < -2:return lo
  if v > 2:return hi
  if v == -2:hi=t;s.append(v);continue
  if v == 2:lo=t;s.append(v);continue
  return t
 raise AssertionError('Finite support termination missing')
X=sorted({pad(x) for n in range(1,6) for x in product((-4,-2,-1,0,1,2,4),repeat=n) if a<=pad(x)<=b})
vals=[]
for x in X:
 y=retract(x);vals.append(y)
 assert y in B;C['output_in_section']+=1
 if x in B:assert y==x;C['fixes_section_sample']+=1
 for z in B:
  if z<x:assert z<=y
  elif z>x:assert z>=y
  else:assert z==y
  C['cut_inequalities']+=1
for i in range(len(X)-1):assert vals[i]<=vals[i+1];C['monotone_adjacent_inputs']+=1
# Every sampled tree node, including depths beyond X, is fixed.
for z in B:assert retract(z)==z;C['fixes_all_tree_nodes']+=1
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'ambient_samples':len(X),'section_samples':len(B),'scope':'Finite-support lexicographic classifier controls only. Infinite density, gluing, and countable quotient are proved in TURN_3.md.'},indent=2))
