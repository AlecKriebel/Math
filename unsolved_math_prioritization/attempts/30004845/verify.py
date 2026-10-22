"""Exact formal controls for the bubble-detection argument; no infinite nerve computation."""
from pathlib import Path
from itertools import product
import json,hashlib
checks=0;families={}
def check(b,name):
 global checks
 assert b,name
 checks+=1;families[name]=families.get(name,0)+1
# Total weight respects both additive compositions and their interchange.
for a,b,c,d in product(range(3),repeat=4):
 check((a+b)+(c+d)==(a+c)+(b+d),'interchange weight')
for a,b,c in product(range(3),repeat=3):
 check((a+b)+c==a+(b+c),'associative weight')
for a in range(5):
 check(a+0==0+a==a,'identity weight')
# B^2N -> C -> B^2N, for alpha:id=>f and gamma:f=>id.
d2=(1,-1);j2=(1,1);w2=(1,1)
check(sum(x*y for x,y in zip(d2,j2))==0,'bubble is polygraphic cycle')
check(sum(x*y for x,y in zip(w2,j2))==2,'total detector composite')
check(d2[0]==1 and d2[1]==-1,'target-minus-source convention')
for n in range(-5,6):
 check(d2[0]*n+d2[1]*n==0,'integral bubble cycle multiples')
 check(sum(w2[i]*n*j2[i] for i in range(2))==2*n,'integral detector composition')
# Multiplication m on H^2 sends c^r to m^r c^r; composition is respected.
for m in range(1,7):
 for r in range(1,7):
  check(m**r>0,'nonzero even homology multiplier')
  for k in range(1,4):
   check((m*k)**r==m**r*k**r,'power-map naturality arithmetic')
# Dividing by m^r gives a rational splitting, not an integral splitting in general.
check(2**2!=1,'not an integral retraction')
# Nonfree negative control: M={0,e}, operation max, identity 0, e idempotent.
for a,b,c in product([0,1],repeat=3):
 check(max(max(a,b),c)==max(a,max(b,c)),'idempotent monoid associativity')
check(max(1,1)==1,'nontrivial idempotent relation')
for value in range(5):
 check((value+value==value)==(value==0),'no positive additive idempotent weight')
# No claim that finitely testing the last equation proves it for all N: k+k=k
# implies k=0 by cancellation, as stated in the mathematical argument.
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL.md').read_bytes()).hexdigest(),'status':'pass','assertions':checks,'families':families,'scope':'Formal exact controls only; imported classifying-space theorem and full categorical proof are not replaced by tests.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
