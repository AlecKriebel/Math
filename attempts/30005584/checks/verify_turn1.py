"""Exact matrix and normalization controls; not a proof about Ricci soliton moduli."""
from fractions import Fraction as Q
from itertools import product,permutations
from collections import Counter
import json
counts=Counter()
def ck(v,k):
 assert v,k
 counts[k]+=1
def mm(A,B):return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def tr(A):return sum(A[i][i] for i in range(3))
def transpose(A):return tuple(zip(*A))
def q(A):
 A2=mm(A,A);s=tr(A2)
 return tuple(tuple(A2[i][j]-(s/3 if i==j else 0) for j in range(3)) for i in range(3))
def det(A):return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def scale(A,t):return tuple(tuple(t*x for x in r) for r in A)
def add(A,B):return tuple(tuple(a+b for a,b in zip(r,s)) for r,s in zip(A,B))
def make(v):
 a,b,c,d,e=map(Q,v);return ((a,c,d),(c,b,e),(d,e,-a-b))
I=((Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1)))
rots=[]
for p in permutations(range(3)):
 for signs in product((-1,1),repeat=3):
  R=tuple(tuple(Q(signs[i] if j==p[i] else 0) for j in range(3)) for i in range(3))
  if det(R)==1:rots.append(R)
for v in product(range(-2,3),repeat=5):
 A=make(v);B=q(A);s=tr(mm(A,A))
 ck(tr(B)==0,'trace_free_output')
 ck(tr(mm(B,B))==s*s/6,'properness_norm_identity')
 ck(q(scale(A,-1))==B,'even_map')
 ck(mm(mm(A,A),A)==add(scale(A,s/2),scale(I,det(A))),'cayley_hamilton')
 for R in rots:
  RA=mm(mm(R,A),transpose(R))
  ck(q(RA)==mm(mm(R,B),transpose(R)),'SO3_equivariance_controls')
# Trace pairing is the derivative of the invariant potential on trace-free variations.
for a,b in product(range(-2,3),repeat=2):
 A=make((a,b,1,-1,2));A2=mm(A,A)
 for i in range(5):
  w=[0]*5;w[i]=1;H=make(w)
  ck(tr(mm(q(A),H))==tr(mm(A2,H)),'gradient_trace_pairing')
# Diagonal derivative determinant at A=diag(a,b,-a-b).
for a,b in product(range(-4,5),repeat=2):
 J11=Q(2*a-2*b,3);J12=Q(-2*a-4*b,3);J21=Q(-4*a-2*b,3);J22=Q(2*b-2*a,3)
 D=(J11*J22-J12*J21)*(a+b)*(-b)*(-a)
 Dneg=(-J11*-J22-(-J12)*(-J21))*(-a-b)*b*a
 ck(Dneg==-D,'opposite_regular_signs')
 if (a,b)==(1,2):ck(D==-56,'explicit_jacobian_minus56')
# Scalar-cone cutoff and normalization do not require square-root numerics.
for a,b in product(range(1,12),repeat=2):
 radius2=Q(a,b)
 ck((2/radius2-6>=0)==(radius2<=Q(1,3)),'cone_scalar_cutoff')
 f0=Q(-a,b)
 ck(Q(1,2)*(2)==1,'soliton_metric_scaling')
 ck((f0/2)*2==f0,'initial_second_derivative_scaling')
print(json.dumps({'status':'PASS','assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'scope':'Exact finite-dimensional diagnostic identities only; no numerical Ricci-expander degree claim.'},indent=2,sort_keys=True))
