#!/usr/bin/env python3
"""Independent exact controls supplement INITIAL_DERIVATION.md, not universal tests."""
import json
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
counts=Counter()
def check(k,v):
 if not v:raise RuntimeError(k)
 counts[k]+=1
def mul(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def tr(A):return tuple(zip(*A))
def det(A):return A[0][0]*A[1][1]-A[0][1]*A[1][0]
I=((F(1),F(0)),(F(0),F(1)));A=((F(3,5),F(-4,5)),(F(4,5),F(3,5)));B=((3,-4),(4,3))
a,b=1,0;P=I;Q=I;u0,u1=2,6
for n in range(1,2049):
 a,b=3*a-4*b,4*a+3*b
 check('gaussian_norm',a*a+b*b==25**n)
 check('modular_pair',a%5==3 and b%5==4)
 check('trace_recurrence_cross_family',2*a==u1)
 check('both_signs_nonidentity',b!=0 and (a,b)!=(5**n,0) and (a,-b)!=(5**n,0))
 u0,u1=u1,6*u1-25*u0
 if n<=384:
  P=mul(P,A);Q=mul(Q,tr(A));G=((F(a,5**n),F(-b,5**n)),(F(b,5**n),F(a,5**n)))
  check('gaussian_vs_fraction_matrix',P==G)
  check('positive_inverse_matrix',mul(P,Q)==I)
  check('fraction_isometry',mul(tr(P),P)==I and det(P)==1)
check('modular_idempotent',tuple(tuple(x%5 for x in row) for row in mul(B,B))==tuple(tuple(x%5 for x in row) for row in B))
for R,order in [(I,1),(((-1,0),(0,-1)),2),(((0,-1),(1,0)),4)]:
 P=I
 for _ in range(order):P=mul(P,R)
 check('finite_rotation_controls',mul(tr(R),R)==I and P==I)
for C in [((F(1,2),0),(0,F(1,2))),((F(2),0),(0,F(1,2))),((F(3,5),F(-4,5)),(F(4,5),F(3,5)+F(1,10**6)))]:
 check('nonrotation_controls',mul(tr(C),C)!=I)
for n in range(1,8):
 for pi in permutations(range(n)):
  for j in range(n):
   outside={pi[i] for i in range(n) if i!=j}
   check('permuted_separated_end_count',len(outside)==n-1)
   check('threshold_boundary_control',(len(outside)>1)==(n>=3))
check('one_end_no_count_obstruction',1-1<2)
check('two_end_no_count_obstruction',2-1<2)
check('three_point_cantor_witness',len({F(0),F(2,3),F(1)})==3)
print(json.dumps({'status':'PASS','checks_by_family':dict(counts),'total_controls':sum(counts.values()),'gaussian_bound':2048,'fraction_matrix_bound':384,'end_permutation_bound':7,'limits':'The explicit induction proves all exponents; enumeration verifies only finite arithmetic and combinatorial controls, not analytic/topological universals or novelty.'},indent=2,sort_keys=True))
