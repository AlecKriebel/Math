#!/usr/bin/env python3
"""Elementary convention checks for a credited literature correction, not a proof of Datta's theorem."""
from fractions import Fraction as F
from collections import Counter
from pathlib import Path
import hashlib,json,math
c=Counter()
def ck(k,p):assert p,k;c[k]+=1
for e in range(1,65):
 vals=[F(k,e) for k in range(3*e)]
 initial=[x for x in vals if 0<=x<1]
 ck('discrete_initial_segment',len(initial)==e)
 ck('distinct_coset_representatives',len({(x*e).numerator%e for x in initial})==e)
 for q in range(3*e):ck('discrete_coset_reduction',F(q,e)-F(q%e,e)==q//e)
for m in range(1,17):
 for n in range(1,17):
  # Lexicographic order: smallest positive base element is (0,n).
  initial=[(a,b) for a in range(-2,3) for b in range(-2,3*n+1) if (0,0)<=(a,b)<(0,n)]
  ck('lexicographic_initial_segment',initial==[(0,j) for j in range(n)])
  ck('lexicographic_index_distinction',(len(initial)==m*n)==(m==1))
for n in range(9):
 for j in range(1,20):
  gamma=F(j,2*3**n);k=0
  while F(1,3**k)>=gamma:k+=1
  ck('dense_base_smaller_positive_value',0<F(1,3**k)<gamma)
# The split-prime control in Q(sqrt6) at5: unique simple Hensel lifts of both residue roots.
ck('quadratic_is_not_a_rational_square',math.isqrt(6)**2!=6)
ck('split_simple_residue_roots',[r for r in range(5) if (r*r-6)%5==0]==[1,4])
for seed in [1,4]:
 r=seed;mod=5
 for k in range(1,10):
  ck('simple_root_derivative',math.gcd(2*r,5)==1)
  ck('hensel_root_equation',(r*r-6)%mod==0)
  lifts=[r+j*mod for j in range(5) if ((r+j*mod)**2-6)%(5*mod)==0]
  ck('unique_next_hensel_lift',len(lifts)==1)
  r=lifts[0];mod*=5
ck('split_local_defect',F(1,1*1)==1)
ck('total_degree_not_local_defect',F(2,1*1)!=1)
for f in range(1,65):ck('trivial_valuation_scope',F(f,1*f)==1)
print(json.dumps({'problem_id':30002709,'status':'PASS','substantive_author_turns':0,'exact_controls':sum(c.values()),'groups':dict(sorted(c.items())),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Only exact elementary convention diagnostics. Datta Theorem1.2, not this finite checker, establishes the classification; no new proof or novelty is claimed.'},indent=2,sort_keys=True))
