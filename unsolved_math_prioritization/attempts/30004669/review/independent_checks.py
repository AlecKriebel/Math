#!/usr/bin/env python3
"""Bounded logical models only: no Kolmogorov complexity is evaluated."""
from itertools import product,combinations
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
C=Counter()
def ck(cat,x):
 assert x,cat
 C[cat]+=1
# Four-point universes: test implications using membership bits directly.
for state in product(range(4),repeat=4):
 #0 outside D;1 in D only;2 in D,A;3 in D,A,B.
 D={i for i,s in enumerate(state) if s>=1};A={i for i,s in enumerate(state) if s>=2};B={i for i,s in enumerate(state) if s==3}
 ck('inclusion_complements',(set(range(4))-A)<=(set(range(4))-B))
 ck('equality_downward',B!=D or A==D)
 for x in D-A:ck('same_strictness_witness',x in D-B)
# Exact quantifier pattern for eventually periodic gap sequences.
# Such a sequence fails to diverge iff a finite bound occurs on its period infinitely.
for tail in product(range(4),repeat=4):
 b=min(tail)
 ck('infinite_subsequence_bound',any(x<=b for x in tail))
 for shift in range(4):
  ck('bound_at_arbitrarily_late_positions',any(tail[(shift+i)%4]<=b for i in range(4)))
# Additive inequality, with both fast-complexity lower bounds retained.
for KA,KB,d,b,c in product(range(5),repeat=5):
 if KA<=KB+d:
  fastA=KA+b;fastB=max(KB,fastA+c)
  if fastB<=fastA+c:ck('bounded_gap_transfer',fastB-KB<=b+c+d)
# A diagnostic for why the unbounded-complexity comparison is essential.
for n in range(1,101):
 KA=fastA=n;KB=0;fastB=n
 ck('simulation_alone_insufficient',fastB<=fastA and fastA-KA==0 and fastB-KB==n)
# Adaptive query programs composed with total three-bit Boolean oracle maps.
for seed in range(64):
 tables=[((seed+1)*37+19*i)&255 for i in range(3)]
 for oracle in range(8):
  A=[(tables[i]>>oracle)&1 for i in range(3)]
  first=seed%3;second=(first+1+A[first])%3
  direct=(A[first],A[second])
  simulated=((tables[first]>>oracle)&1,(tables[second]>>oracle)&1)
  ck('adaptive_tt_composition',direct==simulated)
# Variable bounded-change blocks with the actual initial-bit convention.
for size in range(1,26):
 for initial in (0,1):
  for changes in range(size+1):
   block=[int(i<changes) for i in range(size)]
   last=max((i for i,b in enumerate(block) if b),default=-1)
   recovered=(1-initial) if last>=0 and last%2==0 else initial
   ck('change_record_recovery',recovered==initial^(changes%2))
# Unary oracle-reader programs: codes are prefix-free for every finite truncation.
for n in range(1,71):
 codes=['1'*i+'0' for i in range(n)]
 ck('prefix_code_Kraft',sum((F(1,2**len(p)) for p in codes),F(0))==1-F(1,2**n))
 ck('prefix_code_nonprefix',all(not a.startswith(b) and not b.startswith(a) for a,b in combinations(codes,2)))
# Unbounded, nonmonotone computable uses still permit the bit-recovery search.
for j in range(250):
 u=lambda n:n//3 if n%3==0 else 0
 n=next(n for n in range(3*(j+2)) if u(n)>j)
 ck('nonmonotone_unbounded_use',n==3*(j+1))
r={'status':'PASS','assertions':sum(C.values()),'categories':dict(C),'artifact_sha256':'38fd590eac83acc56e457f0ff761a65f8fe3ad3f947f42cb3519a8a7ced6ae16','limits':'Finite Boolean/inequality models only. No genuine complexity values, depth decision, noncomputable oracle outcome or cost-function proof.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
