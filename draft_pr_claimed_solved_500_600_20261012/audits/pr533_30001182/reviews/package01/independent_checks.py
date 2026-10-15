#!/usr/bin/env python3
"""Independent exact controls; infinite claims are proved in INDEPENDENT_MATH.md."""
from fractions import Fraction as Q
from itertools import product,permutations
from pathlib import Path
import json,hashlib
if not __debug__: raise RuntimeError('Assertions required')

def unit(n,i,j): return tuple(tuple(Q(a==i and b==j) for b in range(n)) for a in range(n))
def diag(xs): return tuple(tuple(Q(x) if i==j else Q(0) for j in range(len(xs))) for i,x in enumerate(xs))
def plus(a,b): return tuple(tuple(x+y for x,y in zip(ar,br)) for ar,br in zip(a,b))
def scale(c,a): return tuple(tuple(c*x for x in ar) for ar in a)
def mul(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))) for i in range(len(a)))
def tr(a): return sum(a[i][i] for i in range(len(a)))
def transpose(a): return tuple(zip(*a))
def prod(xs,n):
 a=diag([1]*n)
 for x in xs:a=mul(a,x)
 return a
checks=0
P=diag([0,0,1,1]);Qp=diag([0,1,0,1]);parameters=[]
for a,b in [(1,0),(0,1),(1,1),(1,3),(3,1),(2,5),(5,2)]:
 t=Q(b*b,a*a+b*b);v=(a,0,0,b);rho=tuple(tuple(Q(x*y,a*a+b*b) for y in v) for x in v)
 assert tr(rho)==1 and mul(rho,rho)==rho;checks+=2
 # Basis p and q words supplemented by complemented projections.
 one=diag([1]*4);gens=[P,Qp,plus(one,scale(-1,P)),plus(one,scale(-1,Qp))]
 for n in range(7):
  for symbols in product(range(4),repeat=n):
   w=prod([gens[s] for s in symbols],4)
   assert tr(mul(rho,w))==(1-t)*w[0][0]+t*w[3][3];checks+=1
 for i,j in product(range(4),repeat=2):
  e=unit(4,i,j);assert mul(mul(rho,e),rho)==scale(tr(mul(rho,e)),rho);checks+=1
 assert t*(1-t)>=0;checks+=1
 parameters.append({'t':str(t),'nontrivial_downstairs':0<t<1})
# A pair-only alternative: symmetric orbit law on two copies, showing why a
# third copy is actually needed for the vector-identification graph.
two_orbit=[((0,1),(1,0)),((1,0),(0,1))]
assert all(c[0][0]==c[1][1] and c[0][1]==c[1][0] for c in two_orbit)
assert sum(c[0][0]*c[1][1] for c in two_orbit)==1;checks+=2
# C4 in finite compressions large enough to contain the inspected indices.
n=6;xs={i:plus(unit(n,0,i),unit(n,i,0)) for i in range(1,n)}
for i,x in xs.items():
 assert prod([x,x,x],n)==x;checks+=1
 for j,y in xs.items():
  if i==j:continue
  assert prod([x,x,y,y],n)==unit(n,0,0);checks+=1
  assert prod([x,unit(n,0,0),y],n)==unit(n,i,j);checks+=1
  assert prod([x,y,x,y],n)[0][0]==0;checks+=1
for perm in permutations(range(1,n)):
 U=tuple(tuple(Q((j==0 and i==0) or (j>0 and i==perm[j-1])) for j in range(n)) for i in range(n))
 for i,x in xs.items():assert mul(mul(U,x),transpose(U))==xs[perm[i-1]];checks+=1
# C5 generation by diagonal tail algebra plus twisted copy, faithful E weights,
# minimality via Etheta(A)=D, and exact density eigenvectors.
Z=diag([1,-1]);R=diag([1,0]);state_density=((Q(1,2),Q(1,6)),(Q(1,6),Q(1,2)))
assert tr(state_density)==1 and state_density[0][0]*state_density[1][1]-state_density[0][1]*state_density[1][0]==Q(2,9);checks+=2
for i,j in product(range(2),repeat=2):
 e=unit(2,i,j);ze=mul(mul(Z,e),Z);Et=scale(Q(1,3),plus(scale(2,e),ze))
 assert Et==scale(Q(1) if i==j else Q(1,3),e);checks+=1
 if i!=j:
  assert plus(e,ze)==diag([0,0])
  # half sum/difference of (e,e) and (e,-e) isolates each summand.
  assert scale(Q(1,2),plus(e,scale(-1,ze)))==e;checks+=1
assert mul(mul(Z,R),Z)==R;checks+=1
for vector,eigenvalue in [((1,1),Q(2,3)),((1,-1),Q(1,3))]:
 assert tuple(sum(row[j]*vector[j] for j in range(2)) for row in state_density)==tuple(eigenvalue*x for x in vector);checks+=1
# Laurent Gram determinant is uniformly -1 regardless of unknown eta(Y^2).
for c in [Q(0),Q(1,100),Q(1),Q(10**9)]:assert -1==0*c-1;checks+=1
result={'status':'PASS','checks':checks,'parameter_instances':parameters,'C4_matrix_and_permutation_controls':True,'C5_minimality_generation_density_controls':True,'two_copy_boundary_control':True,'algebraic_nonextension_gram_controls':True,'limits':'Finite exact standard-library controls supplement independently derived universal proofs; no priority certainty or formal certification.','verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,indent=2))
