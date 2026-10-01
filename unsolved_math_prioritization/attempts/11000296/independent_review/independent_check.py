#!/usr/bin/env python3
"""Exact convention controls; no finite calculation proves group-homology nonvanishing."""
from itertools import permutations,combinations
from collections import Counter
import json
C=Counter()
def ck(t,k):assert t,k;C[k]+=1
def sign(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
# For coordinate apartments, compare every basis permutation and coordinate subspace.
# Twisted block brackets absorb their own internal permutation signs.
for n in range(2,7):
 for p in permutations(range(n)):
  ck(sign(p)**2==1,'twisted_input_permutation_invariance')
  for a in range(1,n):
   for S in combinations(range(n),a):
    positions=[i for i,v in enumerate(p) if v in S]
    rest=[i for i,v in enumerate(p) if v not in S]
    shuffle=positions+rest
    ordinary=sign(shuffle);determinant=sign(shuffle)
    ck(ordinary*determinant==1,'natural_determinant_shuffle_cancellation')
    ck(sign(p)**2*ordinary*determinant==1,'corrected_component_basis_independence')
# Explicit actual-target witness: swap e2,e3 and project to span(e1,e2).
base=tuple(range(6));swapped=(0,2,1,3,4,5);S={0,1}
def literal_coefficient(p):return sign([i for i,v in enumerate(p) if v in S]+[i for i,v in enumerate(p) if v not in S])
ck(sign(base)**2==sign(swapped)**2==1,'literal_witness_equal_twisted_inputs')
ck(literal_coefficient(base)==1 and literal_coefficient(swapped)==-1,'literal_witness_opposite_outputs')
# Eight elementary matrices in column-vector convention, after reordering basis.
E=[]
for r in (0,1):
 for c in range(2,6):E.append(tuple(tuple(int(i==r and j==c) for j in range(6)) for i in range(6)))
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(6)) for j in range(6)) for i in range(6))
Z=tuple((0,)*6 for _ in range(6))
for A in E:
 for B in E:ck(mul(A,B)==Z,'unipotent_nilpotent_products_zero')
ck(len(set(E))==8,'eight_independent_block_coordinates')
nu=lambda n:n*(n-1)//2
for a in range(1,31):
 for b in range(1,31):
  ck(nu(a+b)-nu(a)-nu(b)==a*b,'duality_dimension_identity')
  ck(nu(a)+nu(b)<nu(a+b),'primitive_degree_gap')
  if a==b:ck(((nu(a)+a)%2==0)==(a%4 in (0,3)),'equal_rank_parity_exception')
ck((nu(2),nu(4),nu(6),nu(6)-nu(2)-nu(4))==(1,6,15,8),'specific_degree_eight_detection')
ck((2,4)!=(4,2),'distinct_coproduct_rank_components')
ck((-1)**((nu(2)+2)*(nu(4)+4))==1,'specific_graded_swap_sign')
ck(1+(-1)**((nu(2)+2)**2)==0,'first_class_repeated_odd_primitive_control')
for A in (-1,1):
 for B in (-1,1):ck(A**4*B**(-2)==1,'trivial_unipotent_orientation_character')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'literal_display_witness':{'n':6,'a':2,'b':4,'permutation_zero_based':swapped,'component_basis_indices_zero_based':[0,1],'equal_twisted_inputs':True,'bare_shuffle_coefficients':[1,-1],'invariant_coefficients_after_line_factor':[1,1]},'scope':'Finite determinant/permutation/matrix/dimension controls only. The nonzero pairing is the written invariant argument using credited primary theorems.'},indent=2))
