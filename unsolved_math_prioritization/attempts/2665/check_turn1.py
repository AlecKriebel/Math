"""Exact controls for integral singular-core reduction. No knot geometry is inferred from tests."""
from collections import Counter
from math import gcd,lcm
from functools import reduce
import json
import sympy as s
from sympy.matrices.normalforms import hermite_normal_form
C=Counter()
def ck(x,label):
 assert x,label
 C[label]+=1
def enlarged(A,alpha):
 n=A.rows;V=s.zeros(n+2);V[0,1]=1
 if n:
  V[2:,2:]=A;V[1,2:]=s.Matrix(alpha).T;V[2:,1]=s.Matrix(alpha)
 return V
def skewdet(A):return (A-A.T).det() if A.rows else s.Integer(1)
def ap(A,t):return (t*A-A.T).det() if A.rows else s.Integer(1)
def congruence(n,seed):
 P=s.eye(n)
 for j in range(2*n+1):
  a=(j+seed)%n;b=(2*j+seed+1)%n
  if a==b:b=(b+1)%n
  Q=s.eye(n);Q[a,b]=(-1 if (j+seed)%2 else 1)
  P=P*Q
 return P
def reduce_once(V):
 n=V.rows;J=V-V.T
 v=V.nullspace()[0];D=lcm(*[int(x.q) for x in v]);v=v*D
 g=reduce(gcd,[abs(int(x)) for x in v]);v=v/g
 ck(V*v==s.zeros(n,1),'primitive_right_kernel')
 ck(reduce(gcd,[abs(int(x)) for x in v])==1,'kernel_is_primitive')
 row=(v.T*J);w=s.zeros(n,1);g=s.Integer(0)
 for i in range(n):
  a=row[i]
  if g==0 and a==0:continue
  u,z,h=s.gcdex(g,a);w=u*w;w[i]+=z;g=h
 ck(g==1 and (v.T*J*w)[0]==1,'integral_symplectic_partner')
 projection=s.eye(n)+v*(w.T*J)-w*(v.T*J)
 ck(projection*projection==projection,'integral_complement_projection')
 ck(all(x.q==1 for x in projection),'projection_integral_entries')
 E=hermite_normal_form(s.Matrix(n,n,[int(x) for x in projection]))
 ck(E.shape==(n,n-2),'complement_rank')
 ck(v.T*J*E==s.zeros(1,n-2) and w.T*J*E==s.zeros(1,n-2),'complement_orthogonal')
 w=w-(w.T*V*w)[0]*v
 P=s.Matrix.hstack(v,w,E)
 ck(abs(P.det())==1,'basis_unimodular')
 B=P.T*V*P;A=B[2:,2:];alpha=list(B[2:,1])
 ck(B==enlarged(A,alpha),'exact_symmetric_enlargement_shape')
 ck(skewdet(A)==1,'reduced_skew_unimodular')
 # n+1 distinct integer evaluations certify equality of degree-at-most-n polynomials.
 for t in range(n+1):ck(ap(V,t)==t*ap(A,t),'alexander_polynomial_reduction_identity')
 return A
cores=[s.zeros(0)]+[s.Matrix([[1,0],[1,d]]) for d in [-6,-4,-2,-1,1,2,3,4,5,6]]
for A in cores:
 for seed in range(1,5):
  for steps in range(1,4):
   V=A
   for step in range(steps):
    alpha=[((i+1)*(seed+step))%5-2 for i in range(V.rows)]
    V=enlarged(V,alpha);P=congruence(V.rows,seed+step);V=P.T*V*P
   ck(skewdet(V)==1,'generated_form_admissible')
   original=V;rounds=0
   while V.rows and V.det()==0:
    V=reduce_once(V);rounds+=1
   ck(rounds==steps,'terminates_at_expected_rank')
   ck(V.rows==A.rows,'core_dimension')
   ck(V.det()==A.det() if A.rows else V.rows==0,'core_determinant')
   for t in range(original.rows+1):ck(ap(original,t)==t**rounds*ap(V,t),'full_reduction_polynomial_identity')
   if not A.rows:ck(V.rows==0,'alexander_one_reduces_to_empty')
# General symbolic determinant identity for a 2x2 old block with arbitrary entries.
t,a,b,c,d,x,y=s.symbols('t a b c d x y');A=s.Matrix([[a,b],[c,d]]);V=enlarged(A,[x,y])
ck(s.expand((t*V-V.T).det()-t*(t*A-A.T).det())==0,'symbolic_block_determinant')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'sympy_version':s.__version__,'scope':'Exact integral lattice reduction and polynomial controls only. Trotter congruence and boundary-preserving geometric realization are cited analytic inputs; composite-leading classes remain unresolved.'},indent=2,sort_keys=True))
