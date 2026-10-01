#!/usr/bin/env python3
"""Exact signature-defect gauge, Kirby and lens-space controls."""
import sympy as S
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
C=Counter()
def ck(v,n):
 assert v,n
 C[n]+=1
def quad(B,x):return (x.T*B*x)[0]
def dot(x,y):return (x.T*y)[0]
matrices=[S.Matrix([[b]]) for b in [-5,-4,-2,-1,1,2,3,4,8]]
matrices += [S.Matrix(B) for B in [[[0,4],[4,0]],[[2,1],[1,4]],[[1,2],[2,-3]],[[4,2],[2,4]],[[2,1,0],[1,2,1],[0,1,2]],[[0,2,1],[2,4,0],[1,0,-2]]]]
for B in matrices:
 n=B.rows;ck(B.det()!=0,'nonsingular_test_lattice');diag=S.Matrix([B[i,i] for i in range(n)])
 wus=[S.Matrix(x) for x in product([0,1],repeat=n) if all(y%2==0 for y in B*S.Matrix(x)-diag)]
 ck(bool(wus),'integral_Wu_vector_exists_control');w=wus[0]
 for a in product([-1,0,1],repeat=n):
  c=diag+2*S.Matrix(a);z0=(c-B*w)/2;ck(all(x.q==1 for x in z0),'characteristic_Wu_difference_even')
  expanded=-quad(B,w)-4*quad(B.inv(),z0)+4*dot(w,z0)
  ck(S.simplify(expanded+quad(B.inv(),c)-8*dot(w,z0))==0,'generalized_Brown_defect_identity')
  for zz in product([-1,0,1],repeat=n):
   z=S.Matrix(zz);cp=c+2*B*z;rho=(dot(c,z)+quad(B,z))/2
   ck(rho.q==1,'representative_parity_integral')
   ck(S.simplify(-quad(B.inv(),cp)+quad(B.inv(),c)+8*rho)==0,'exact_defect_change')
   for ww in [S.zeros(n,1),S.ones(n,1),-S.ones(n,1)]:
    lhs=(dot(c,z+ww)+quad(B,z+ww))/2
    rhs=rho+(dot(cp,ww)+quad(B,ww))/2
    ck(lhs==rhs,'exact_representative_cocycle')
  P=S.eye(n)
  if n>1:P[0,1]=1
  BP=P.T*B*P;cc=P.T*c
  ck(quad(BP.inv(),cc)==quad(B.inv(),c),'handle_slide_defect_invariant')
 for w in wus:
  for zz in product([-1,0,1],repeat=n):
   z=S.Matrix(zz);ww=w+2*z
   correction=(quad(B,ww)-quad(B,w))/8
   ck(correction.q==1,'nonbinary_spin_Arf_correction_integral')
   ck((-quad(B,ww)+8*correction+quad(B,w))%16==0,'nonbinary_spin_correction_repairs_defect')
for e in [-1,1]:
 for k in range(-15,16,2):
  correction=S.Rational(e*(k*k-1),8)
  ck(correction.q==1,'odd_stabilization_correction_integral')
  ck((e*(1-k*k)+8*correction)%16==0,'odd_stabilization_repaired')
# Fixed L4 Spin^c class and both reference-spin calculations.
q=lambda c,j:F(j*j-c*j,8)%1
for j in range(-10,11):ck(q(2,j)==q(10,j),'same_L4_quadratic_after_gauge')
ck((F(1)-F(2*2,4))%16==0,'L4_first_raw_defect')
ck((F(1)-F(10*10,4))%16==8,'L4_second_raw_defect')
zeta=S.symbols('zeta');poly=sum(zeta**int(8*q(2,j)) for j in range(4))
ck(S.rem(poly,zeta**4+1,zeta)==2,'exact_L4_Gauss_sum_two')
ck(q(0,-1)==F(1,8) and q(4,1)==F(5,8),'two_spin_origin_corrections')
ck((1-8*q(0,-1))%16==0,'first_origin_value_zero')
ck((-3-8*q(4,1))%16==8,'second_origin_value_eight')
# Four-term condition for any rational defect lifts with one fixed Brown class.
for k in product([-1,0,1],repeat=4):
 D=[F(2,3)+8*x for x in k];dd=D[0]-D[1]-D[2]+D[3];ck((dd/8).denominator==1,'surgery_cube_defect_integral_after_eighth')
 for eps in product([0,1],repeat=4):
  ee=eps[0]-eps[1]-eps[2]+eps[3]
  ck(((dd+8*ee)%16==0)==((F(ee)+dd/8)%2==0),'surgery_cube_parity_criterion')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'categories':dict(C),'scope':'Exact characteristic-vector, gauge-cocycle, Kirby-label and fixed-lens-space controls. The general invariant correction and original target are not solved.'},indent=2))
