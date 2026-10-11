#!/usr/bin/env python3
"""Fresh exact controls: all admissible 4+4+4 theta=1/2 ordinary graphs.

Q is not preconditioned on exact regularity. Nonfull cases test the claimed
rigidity, distinct-type extraction, and missed-mass bound. No psi minimum
or universal proof is inferred from a finite census. Output only, no writes.
"""
from itertools import product
from fractions import Fraction
import json

checks=0
def check(condition):
 global checks
 assert condition
 checks+=1

m=na=nc=4
row_masks=[s for s in range(1<<m) if s.bit_count()>=2]
patterns=[rows for rows in product(row_masks,repeat=4)
 if all(sum(bool(row&(1<<j)) for row in rows)>=2 for j in range(4))]
# For Q, these masks describe each actual C vertex's neighborhood in B;
# the same bidirectional degree filter is valid by matrix transposition.
full=nonfull=irregular=repeat=extra=0
for p in patterns:
 for q in patterns:
  reached=[sum(bool(a&c) for a in p) for c in q]
  if max(reached)==na:
   full+=1
   irregular+=any(c.bit_count()!=2 for c in q) or any(sum(bool(c&(1<<j)) for c in q)!=2 for j in range(4))
   continue
  nonfull+=1
  check(all(c.bit_count()==2 for c in q))
  check(all(sum(bool(c&(1<<j)) for c in q)==2 for j in range(4)))
  types=sorted(set(q))
  missing={c:[a for a in range(na) if not(p[a]&c)] for c in types}
  for c,inds in missing.items():
   check(bool(inds))
   check(all(p[a]==15^c for a in inds))
  check(sum(map(len,missing.values()))==len(set(a for inds in missing.values() for a in inds)))
  t=min(map(len,missing.values()))
  D=max(sum(bool(c&(1<<j)) for c in types) for j in range(4))
  check(t*D*4<=2*na)
  check(Fraction(max(reached),na)==1-Fraction(t,na))
  for j in range(4):
   check(sum(len(missing[c]) for c in types if c&(1<<j))*4<=2*na)
  repeat+=len(types)<len(q)
  extra+=sum(map(len,missing.values()))<na
check(nonfull>0 and full>0 and irregular>0 and repeat>0 and extra>0)

# A valid repeated-C zero-residual witness defeats counting every C copy
# as a distinct incidence column. A=2, B=2, C=4 (two copies per support).
p=(1,2);q=(1,1,2,2)
ungrouped=max(sum(bool(c&(1<<j)) for c in q) for j in range(2))
grouped=max(sum(bool(c&(1<<j)) for c in set(q)) for j in range(2))
check(Fraction(1,2)*ungrouped>Fraction(1,2))
check(Fraction(1,2)*grouped==Fraction(1,2))

# On a rational boundary incompatible middle cardinality, a missed pair
# is impossible by exact integer ceiling sums, independent of any census.
for den in range(2,20):
 for numerator in range(1,den):
  theta=Fraction(numerator,den)
  for size in range(1,20):
   check((theta*size).__ceil__()+((1-theta)*size).__ceil__()==size+(theta*size).denominator.__ne__(1))

print(json.dumps(dict(status='PASS',assertions=checks,ordinary_patterns=len(patterns),
 census_pairs=len(patterns)**2,full_cases=full,nonfull_cases=nonfull,
 irregular_Q_full_cases=irregular,repeated_C_nonfull=repeat,extra_A_nonfull=extra,
 scope='Fresh exhaustive ordinary4+4+4 theta1/2 support census without exact-regular Q prefilter, plus countercontrol and rational ceiling identities. Finite evidence only; no true d minima, psi values, ordering or global priority claim.'),indent=2,sort_keys=True))
