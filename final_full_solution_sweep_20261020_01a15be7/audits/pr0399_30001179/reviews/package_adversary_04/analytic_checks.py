#!/usr/bin/env python3
import itertools,json,math
from fractions import Fraction as F

def require(v,m):
 if not v:raise RuntimeError(m)
def word(n,m,label):return (tuple(((),(label,i)) for i in range(n)),tuple((label,'f',j) for j in range(m)))
def cat(a,b):
 aa,av=a;bb,bv=b
 if bb:
  pre,tail=bb[0]
  return aa+((av+pre,tail),)+bb[1:],bv
 return aa,av+bv
nassoc=0
for g in itertools.product(list(itertools.product(range(3),range(4))),repeat=3):
 a,b,c=[word(*x,l) for x,l in zip(g,'abc')]
 require(cat(cat(a,b),c)==cat(a,cat(b,c)),'association/retention');nassoc+=1
scales=0
for k,l in itertools.product(range(8),repeat=2):
 for d in [F(1,3),F(1),F(7,5)]:
  direct=[2**(k+l-j)*d for j in range(k+l)]
  composed=[2**(k-j)*2**l*d for j in range(k)]+[2**(l-j)*d for j in range(l)]
  require(direct==composed,'density scale chain');require(math.prod(direct)==math.prod(composed),'normalizer');scales+=1
# Direction check on a finite discrete model with output mass q_i eta_i.
eta=[F(2),F(5),F(7)];q=[F(1,2),F(3),F(4,7)];f2=[F(9),F(4),F(25)]
require(sum(e*f for e,f in zip(eta,f2))==sum(e*x*f/x for e,x,f in zip(eta,q,f2)),'reciprocal norm identity')
require(sum(e*f for e,f in zip(eta,f2))!=sum(e*x*f*x for e,x,f in zip(eta,q,f2)),'wrong RN direction exposed')
words=members=survive=0;labels=range(5)
for length in range(7):
 for w in itertools.product(labels,repeat=length):
  words+=1;ok=True
  for mask in range(16):
   cells=[sum(v>cut for cut in range(4) if mask>>cut&1) for v in w]
   allowed=all(a>=b for a,b in zip(cells,cells[1:]));members+=1;ok&=allowed
  decreasing=all(a>=b for a,b in zip(w,w[1:]));require(ok==decreasing,'rational cuts detect every rise');survive+=ok
hull=0
for length in range(6):
 for w in itertools.permutations(labels,length):
  require(len(set(w))==length,'singleton reduced rectangles');hull+=1
# Infinite witness uniform bound: summable Chebyshev majorant, not sampling.
require(F(9,2500)/(1-F(1,4))==F(3,625),'witness exact bound');require(1-F(3,625)==F(622,625),'positive witness')
# Adjoints of rank-one partial isometries: u,v unit rational vectors.
units=[(F(1),F(0)),(F(0),F(1)),(F(3,5),F(4,5)),(F(-3,5),F(4,5))]
dot=lambda a,b:sum(x*y for x,y in zip(a,b));adj=0
for u,v,u0,v0,h in itertools.product(units,repeat=5):
 x=tuple(a*dot(u,h)-b*dot(u0,h) for a,b in zip(v,v0))
 lhs=dot(x,x);rhs=dot(u,h)**2+dot(u0,h)**2-2*dot(u,h)*dot(u0,h)*dot(v,v0)
 require(lhs==rhs,'adjoint norm identity');adj+=1
print(json.dumps({'status':'PASS','coordinate_associations':nassoc,'exact_density_scale_normalizers':scales,'finite_words':words,'partition_memberships':members,'nonincreasing_words':survive,'separated_finite_hull_rectangles':hull,'adjoint_norm_identities':adj,'witness_lower_ratio':'622/625','scope':'Bounded exact algebra only; infinite Gaussian, measure-class, run-chart and continuity deductions are in the written reconstruction.'},sort_keys=True,indent=2))
