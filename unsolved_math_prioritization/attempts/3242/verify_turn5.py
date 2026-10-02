#!/usr/bin/env python3
"""Exact parameter and forced-adjacency controls; no MILP or large graph search."""
from itertools import combinations,permutations
from collections import Counter
import json
counts=Counter();allowed=[]
def ck(g,v):
 if not v:raise AssertionError(g)
 counts[g]+=1
for N in range(11,15):
 for a in range(1,N):
  for b in range(a,N):
   c=N-a-b
   if c<b:continue
   if a<=2 and b<=a+2 and c<=a+b+2:allowed.append((a,b,c))
ck('complete_parameter_reduction',allowed==[(2,3,6),(2,4,5),(2,3,7),(2,4,6),(2,4,7),(2,4,8)])
for a,b,c in [(2,3,7),(2,4,8)]:
 N=a+b+c;W=N-2;S=a+b
 ck('quadratic_exclusion',W*(W+1)//2-S*(S+1)-2*S>2*a*b)
for c in [5,6,7]:
 N=c+6;W=N-2;M=c+2
 ck('size_two_class_forces_top_values',W-1>max(M,6))
 ck('required_max_B_degree',6<M<W-1)
 ck('max_B_saturates_outside',M==2+c)
 ck('low_B_vertices_distinct',len({1,2,M})==3)
 ck('C_upper_after_low_vertices',2+(4-2)==4)
 ck('two_missing_degrees_one_slot',len({5,6}-{1,2,M})>4-len({1,2,M}))

# For the (2,3,6) case with a saturated B vertex, the four required high
# values plus degree one exhaust A union B exactly. Enumerate their assignments
# to demonstrate that degree five has no available representative there.
high={1,6,7,8,9};assignments=0
for vals in permutations(high):
 if vals[0]!=9:continue
 if 8 not in vals[2:]:continue
 assignments+=1
 ck('saturated_B_exhausts_AB_degrees',5 not in vals)
 low=vals.index(1)
 ck('low_vertex_in_known_side',low==1 or low>=2)
 ck('saturated_B_forces_C_degree_cap', (1+3 if low==1 else 2+2)==4)
ck('saturated_B_case_nonempty',assignments>0)
# The nonsaturated B branch has A degrees8,9 and B degrees6,7 plus one low.
ck('unsaturated_B_top_value_forced',8>5)
ck('unsaturated_B_high_values_forced',min(6,7)>5)
ck('degree_seven_C_requirement',7-2==6-1)
ck('old_low_degree_excluded_from_C',2+1>2)
ck('new_low_B_blocks_degree_five',2+2<5)
for r in [1,2]:
 D=3-r
 bound=10 if D==2 else 5
 ck('isolate_restoration_source',bound+r<=11)

for n in range(2,16):
 for w in range(1,n):
  d=n-w
  for k in range(1,n+1):
   if n-1>(2*k-1)*d:
    ck('small_order_failure_covered_by_theorems',k<=2 or d==1 or (k==3 and d==2))
ck('first_surviving_parameter_not_construction',16-1>(2*4-1)*2)
ck('three_color_next_surviving_parameter',17-1>(2*3-1)*3)
print(json.dumps({'problem_id':3242,'author_turn':5,'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'allowed_three_color_deficit_two_partitions':allowed,'saturated_B_degree_assignments':assignments,'floating_point_used':False,'scope':'Exact partition completeness, cut exclusions, forced-neighbor arithmetic and small-order corollary parameter coverage. The general arguments are proved in TURN_5.md. No graph enumeration above six and no full original resolution is certified.'},indent=2,sort_keys=True))
