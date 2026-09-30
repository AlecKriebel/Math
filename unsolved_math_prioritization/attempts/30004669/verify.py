#!/usr/bin/env python3
"""Finite algebra/logic controls; never estimates genuine Kolmogorov complexity."""
from pathlib import Path
from collections import Counter
from itertools import product,combinations
from fractions import Fraction
import hashlib,json
counts=Counter()
def check(x,label):
 assert x,label
 counts[label]+=1
# Bounded change-record encoding: blocks contain a unary record of changes.
# The final bit is the initial bit xor the parity of the occupied block.
h=(2,3,4);starts=(0,2,5)
for initial in product((0,1),repeat=3):
 for changes in product(*(range(x+1) for x in h)):
  D={starts[j]+i for j in range(3) for i in range(changes[j])}
  final=tuple(initial[j]^(changes[j]%2) for j in range(3))
  recovered=[]
  for j in range(3):
   present=[i for i in range(h[j]) if starts[j]+i in D]
   bit=1-initial[j] if present and max(present)%2==0 else initial[j]
   recovered.append(bit)
   check(bit==final[j],'finite_change_record_parity')
  check(tuple(recovered)==final,'finite_truth_table_cover')
# The parity functional is total even on answers that are not valid change records.
for Dbits in product((0,1),repeat=sum(h)):
 vals=[]
 for start,size in zip(starts,h):
  hits=[j for j in range(size) if Dbits[start+j]]
  vals.append(int(bool(hits) and max(hits)%2==0))
 check(all(v in (0,1) for v in vals),'totality_on_arbitrary_oracle_answers')
# Compose arbitrary Boolean functions on two bits with a two-bit oracle map.
for tables in product(range(16),repeat=2):
 for B in range(4):
  A=((tables[0]>>B)&1)+2*((tables[1]>>B)&1)
  for query in (0,1):
   check(((A>>query)&1)==((tables[query]>>B)&1),'truth_table_query_simulation')
# Exhaust the inclusion pattern D^B subset D^A subset D on a three-point universe.
sets=[{i for i in range(3) if mask>>i&1} for mask in range(8)]
for D,A,B in product(sets,repeat=3):
 if B<=A<=D:
  check(not(B==D) or A==D,'equality_transfers_downward')
  check(not(A!=D) or B!=D,'strictness_transfers_upward')
  check(D-A<=D-B,'same_witness_transfers_upward')
# Exact arithmetic of a shallowness transfer. Values are abstract integers,
# not asserted to be Kolmogorov complexities of actual strings.
for ka,kb,b,c,d in product(range(4),repeat=5):
 if ka<=kb+d:
  kat=ka+b; kbs=kat+c
  check(kbs<=kb+b+c+d,'additive_gap_transfer')
# Prefix-free unary input family and its finite Kraft sum.
codes=['1'*n+'0' for n in range(41)]
check(all(not b.startswith(a) and not a.startswith(b) for a,b in combinations(codes,2)),'unary_family_prefix_free')
check(sum((Fraction(1,2**len(p)) for p in codes),Fraction())==1-Fraction(1,2**41),'unary_family_Kraft_sum')
for word in product((0,1),repeat=7):
 for n in range(1,8):
  check(tuple(word[j] for j in range(n))==word[:n],'oracle_prefix_print_control')
# A computable unbounded use need not be monotone; search still finds a prefix.
u=lambda n:n//2 if n%2==0 else 0
for j in range(100):
 n=next(n for n in range(1000) if u(n)>j)
 check(n==2*(j+1),'unbounded_use_prefix_search')
base=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(counts.values()),'categories':dict(counts),'artifact_sha256':hashlib.sha256((base/'PARTIAL.md').read_bytes()).hexdigest(),'limits':'Finite change records, truth tables, set inclusions and abstract inequalities only. No actual Kolmogorov complexity, infinite-depth decision, noncomputable oracle construction or proof of the imported cost-function theorem.'}
(base/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
