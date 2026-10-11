#!/usr/bin/env python3
"""Exact arithmetic/scope controls only; the signature theorem is credited literature."""
import json,hashlib
from pathlib import Path
checks=0
for components in range(1,9):
 for genus_sum in range(21):
  for boundary in range(components,components+13):
   b1=2*genus_sum+boundary-components
   chi=2*components-2*genus_sum-boundary
   assert chi==components-b1;checks+=1
   assert chi<=boundary;checks+=1
   for C in [24,48]:
    for sigma in range((b1+C-1)//C,b1+1):
     assert b1<=C*sigma;checks+=1
     assert chi>=1-C*sigma;checks+=1
# The disconnected-surface equality trap.
for r in range(1,101):
 chi=r;b1=0;sigma=0
 assert chi>=1-24*sigma;checks+=1
 assert (chi==1-b1)==(r==1);checks+=1
# Stronger2018 theorem implies the2015 bound; neither best-constant claim is made.
for sigma in range(101):
 assert 1-24*sigma>=1-48*sigma;checks+=1
# Empty link handled separately by the non-sharp bound.
assert 0>=-24*abs(0);checks+=1
print(json.dumps({'problem_id':10400228,'exact_controls':checks,'source_constants':{'arxiv_v1_2015':48,'arxiv_v2_2018':24},'scope':'Finite exact bookkeeping controls for chi=b0-b1, the fixed-signature implication, disconnected unlink and empty-link boundaries. These are not a proof or numerical test of the published all-positive-link signature theorem.','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2,sort_keys=True))
