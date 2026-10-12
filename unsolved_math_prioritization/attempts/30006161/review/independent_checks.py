from fractions import Fraction as Q
from itertools import combinations,permutations
from pathlib import Path
import json
nchecks=0
def ck(x):
 global nchecks
 assert x
 nchecks+=1
# Partition-of-unity nerve: all clique supports are vertices/edges; use
# independent rational lifted coordinates and both orientations.
for n in range(4,25):
 adj=lambda i,j:(i-j)%n in (0,1,n-1)
 for triple in combinations(range(n),3):ck(not all(adj(i,j) for i,j in combinations(triple,2)))
 for i in range(n):
  for k in range(n):
   if k not in (i,(i+1)%n):ck(not(adj(k,i) and adj(k,(i+1)%n)))
 for den in range(2,13):
  u=[Q(1+(i*i+3*i)%(den-1),den) for i in range(n)]
  delta=[1+u[i]-u[(i-1)%n] for i in range(n)]
  ck(sum(delta)==n);ck(sum(-x for x in delta)==-n)
  for i in range(n):ck(0<delta[i]<2)
# Independent finite closed-incidence witness encoding for arbitrary chains
# drawn from all prefixes. No finite topology is confused with a surface.
for n in range(1,7):
 X=set(range(n))
 for shift in range(n):
  order=list(range(shift,n))+list(range(shift))
  chain=[set(order[:k]) for k in range(1,n+1)]
  for mask in range(1,1<<n):
   B={i for i in range(n) if mask>>i&1}
   bad=[K for K in chain if B<=K and K!=X]
   witnesses=[(K,j) for K in chain for j in X if B<=K and j not in K]
   ck(bool(bad)==bool(witnesses))
# Homomorphisms from cyclic torsion groups to Z: every generator image zero.
for torsion in range(2,33):
 for image in range(-40,41):ck((torsion*image==0)==(image==0))
Path('independent_results.json').write_text(json.dumps({'assertions':nchecks,'result':'PASS','scope':'Exact finite combinatorial and winding diagnostics only; no computational assertion of Baire category, ray density, or a generic orbit.'},indent=2)+'\n')
print(nchecks)
