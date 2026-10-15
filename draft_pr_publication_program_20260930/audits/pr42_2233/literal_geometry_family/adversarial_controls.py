"""Own exact boundary and negative controls for the candidate's scoped lemmas."""
from collections import Counter
from fractions import Fraction as F
from itertools import product
import json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
tested=0
def require(b):
 global tested
 tested+=1
 if not b: raise AssertionError(tested)
def lengths(pin, points):
 return Counter((pin[0]-p[0])**2+(pin[1]-p[1])**2 for p in points if p!=pin)
def data(points):
 require(len(set(points))==len(points))
 values=[len(lengths(p,points)) for p in points]
 return values,{len(points)-1-v for v in values}
def allowed(blocks):
 flat=[p for b in blocks for p in b]
 if len(flat)!=len(set(flat)):return False
 for block in blocks:
  for pin in block:
   internal=lengths(pin,block)
   external=Counter((pin[0]-p[0])**2+(pin[1]-p[1])**2 for other in blocks if other is not block for p in other)
   if internal.keys()&external.keys() or any(v!=1 for v in external.values()):return False
 return True
families=[[(0,0)],[(0,0),(2,0)],[(0,0),(1,0),(0,1)],[(0,0),(1,0),(1,1),(0,1)]]
generic=bad=0
for A,B in product(families,repeat=2):
 av,ad=data(A);bv,bd=data(B)
 for dx,dy in product(range(-4,5),repeat=2):
  moved=[(x+dx,y+dy) for x,y in B]
  if not allowed([A,moved]):bad+=1;continue
  cv,cd=data(A+moved)
  require(cd==ad|bd)
  require(cv==[v+len(B) for v in av]+[v+len(A) for v in bv])
  require(len(cd)<=max(1,max(len(A),len(B))-1))
  generic+=1
require(generic>0 and bad>0)
single_v,single_d=data([(7,9)])
require(single_v==[0] and single_d=={0})
square=[(0,0),(1,0),(0,1),(1,1)]
require(not allowed([square[:2],square[2:]]))
require(data(square)[1]=={1})
# Constrained translations can destroy genericity: the full R^(2k) hypothesis matters.
for dy in range(-20,21):
 require(not allowed([[(0,0)],[(-1,dy),(1,dy)]]))

support_examples=0
for m in range(2,21):
 t=F(1,10*m);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
 arc=[];p=(F(1),F(0))
 for _ in range(m):
  arc.append(p);p=(c*p[0]-s*p[1],s*p[0]+c*p[1])
 require(all(x*x+y*y==1 for x,y in arc))
 require(data(arc)[0]==[max(i,m-1-i) for i in range(m)])
 require(len(data(arc)[1])==(m+1)//2)
 for support in [arc,[(i,0) for i in range(m)]]:
  for exceptions in [[],[(0,0)] if support is arc else [(0,1)],[(0,0),(7,11)] if support is arc else [(0,1),(7,11)],[(7+j,11+j*j) for j in range(m+2)]]:
   if any(p in support for p in exceptions):continue
   points=support+exceptions;n=len(points);q=len(exceptions)
   values,deficits=data(points)
   bound=min(n-1,n+q-m//2)
   require(len(deficits)<=bound)
   require(all(values[i]>=m//2 for i in range(m)))
   if support is arc and exceptions==[(0,0)]:require(values[m]==1)
   support_examples+=1
result={'exact_assertions_passed':tested,'generic_two_block_cases':generic,'nongeneric_or_coincident_cases':bad,
 'support_boundary_cases':support_examples,'arithmetic':'exact integer/Fraction squared distances via multiplicity counters',
 'original_helper_scripts_executed':False,
 'scope':'Audit diagnostics of scoped lemmas only; universal proofs checked separately; zero new substantive attempts/audit turns'}
(ROOT/'adversarial_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
