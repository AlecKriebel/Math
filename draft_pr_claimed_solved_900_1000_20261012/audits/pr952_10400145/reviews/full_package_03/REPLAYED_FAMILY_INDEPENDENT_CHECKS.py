"""Independent exact first-jet and normalized type-A adjoint contraction checks.
Pure Python standard library; no candidate checker import or execution.
"""
from fractions import Fraction as F
import json

def zero(n):return [[F(0) for j in range(n)] for i in range(n)]
def e(n,i,j):
 a=zero(n);a[i][j]=F(1);return a
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(c,a):return [[c*x for x in r] for r in a]
def mul(a,b):
 n=len(a);return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
def comm(a,b):return add(mul(a,b),scale(F(-1),mul(b,a)))
def casimir(n,x):
 ans=zero(n)
 # Off diagonal dual pair: E_ij dual E_ji in trace form.
 for i in range(n):
  for j in range(n):
   if i!=j:ans=add(ans,comm(e(n,i,j),comm(e(n,j,i),x)))
 # H_i=E_ii-E_nn, Gram I+J, inverse I-J/n.
 hs=[add(e(n,i,i),scale(F(-1),e(n,n-1,n-1))) for i in range(n-1)]
 for i,a in enumerate(hs):
  for j,b in enumerate(hs):
   ans=add(ans,scale(F(i==j)-F(1,n),comm(a,comm(b,x))))
 return ans

rows=[]
for n in range(2,7):
 basis=[e(n,i,j) for i in range(n) for j in range(n) if i!=j]
 basis += [add(e(n,i,i),scale(F(-1),e(n,n-1,n-1))) for i in range(n-1)]
 assert len(basis)==n*n-1
 for x in basis:assert casimir(n,x)==scale(F(2*n),x)
 rows.append({'matrix_size':n,'lie_rank':n-1,'dimension':len(basis),'casimir_eigenvalue':2*n,'theta_weight':2*n*(n*n-1),'expected_first_coefficient_for_P':-n*(n*n-1)})
# At q=1+x modulo x^2, q^k = 1+kx, hence
# (t-q)(t-q^2)|t=q^n = (n-1)(n-2)x^2 = 0.
# A second-quotient representative 1+b(q)(t-q) therefore gives v_n=(n-1)b(1).
first={'actual_sizes_1_2_3':[0,-6,-24],'required_size_3_given_sizes_1_2':-12,'second_difference':-12,'ratios':{'quantum_3_over_2':4,'interpolation_3_over_2':2}}
assert first['actual_sizes_1_2_3'][2]-2*first['actual_sizes_1_2_3'][1]+first['actual_sizes_1_2_3'][0]==-12
# Poincare k=1 summand q(1+q)(1-q^3); multiply polynomials in x exactly.
def pmul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return c
poincare_k1=pmul(pmul([1,1],[2,1]),[0,-3,-3,-1])
assert poincare_k1[:2]==[0,-6]
# Alternative node choice 2,3,4 excludes a rank-one-only artifact.
other=[-n*(n*n-1) for n in [2,3,4]]
assert other[2]-2*other[1]+other[0]==-18
print(json.dumps({'all_pass':True,'arithmetic':'exact rational matrices, all basis vectors checked','casimir_checks':rows,'first_jet':first,'P_k1_polynomial_in_q_minus_1':poincare_k1,'sizes_2_3_4':other,'second_difference_2_3_4':-18},indent=2))
