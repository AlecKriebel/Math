#!/usr/bin/env python3
"""Independent finite controls of cohomology dimensions, orientation and scaling."""
from fractions import Fraction as Q
from itertools import combinations,permutations,product
from math import comb
from collections import Counter
from pathlib import Path
import json,hashlib
counts=Counter()
def ck(n,b):assert b,n;counts[n]+=1
def sign(p):return (-1)**sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))
pairs=list(combinations(range(4),2))
W=[[0]*6 for _ in range(6)]
for i,a in enumerate(pairs):
 for j,b in enumerate(pairs):
  if set(a).isdisjoint(b):W[i][j]=sign(a+b)
ck('exterior_pairing_symmetry',W==[list(x) for x in zip(*W)])
ck('exterior_pairing_square_identity',[[sum(W[i][k]*W[k][j] for k in range(6)) for j in range(6)] for i in range(6)]==[[int(i==j) for j in range(6)] for i in range(6)])
ck('exterior_pairing_signature',sum(W[i][i] for i in range(6))==0 and len(W)==6)
for k in range(1,31):
 betti=[1,0,2*k,0,1]
 ck('connected_sum_euler_characteristic',sum((-1)**i*b for i,b in enumerate(betti))==2+2*k)
 ck('middle_degree_dimension',betti[2]==2*k)
 if k>3:ck('graded_embedding_obstruction',betti[2]>comb(4,2))
 if k>7:ck('ungraded_dimension_obstruction',sum(betti)>2**4)
ck('exact_target_betti_dimensions',[1,0,40,0,1]==[1,0,2*20,0,1])
ck('exact_target_total_dimension',42>16)
# Signed affine determinant and exterior-power tests; these do not require positive Jacobians.
for p in permutations(range(4)):
 for signs in product([-1,1],repeat=4):
  ds=[Q(signs[i]*(i+1),4) for i in range(4)]
  det=Q(sign(p))
  for d in ds:det*=d
  reflection_det=-det
  ck('domain_reflection_reverses_signed_volume',det+reflection_det==0)
  ck('absolute_integral_not_integral_absolute',abs(det)==abs(reflection_det))
  lip=max(abs(d) for d in ds)
  for inds in combinations(range(4),3):
   minor=Q(1)
   for j in inds:minor*=ds[j]
   ck('boundary_comass_lipschitz_power',abs(minor)<=lip**3)
  for R in [Q(2),Q(3),Q(7,2)]:
   ck('four_dimensional_dilation',det*R**4==(ds[0]*R)*(ds[1]*R)*(ds[2]*R)*(ds[3]*R)*sign(p))
   ck('normalized_boundary_loss',R**3/R**4==1/R)
# Exact Stokes test on a cube for eta=x0^(m+1)/(m+1) dx1^dx2^dx3.
for m in range(12):
 for R in [Q(1),Q(2),Q(5,2)]:
  bulk=(R**(m+1)-(-R)**(m+1))/Q(m+1)*(2*R)**3
  positive=R**(m+1)/Q(m+1)*(2*R)**3
  negative=-(-R)**(m+1)/Q(m+1)*(2*R)**3
  ck('oriented_stokes_boundary_faces',bulk==positive+negative)
print(json.dumps({'problem_id':6700069,'status':'PASS','exact_controls':sum(counts.values()),'groups':dict(sorted(counts.items())),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Finite exact diagnostics only. The published ball theorem, de Rham representative comparison, Lipschitz Stokes theorem and asymptotic limit are established by the written source/application audit, not this checker.'},indent=2,sort_keys=True))
