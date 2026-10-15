"""Finite diagnostics only; the universal argument is in PRIOR_IMPLICATION.md."""
from fractions import Fraction as F
from itertools import product, combinations
from math import atan2, pi, sqrt
from pathlib import Path
import json, random
HERE=Path(__file__).resolve().parent
V=list(product((-1,1),repeat=3));n=len(V)
E=[(i,j) for i,j in combinations(range(n),2) if sum(a!=b for a,b in zip(V[i],V[j]))==1]
M=[[F(1,16) if (min(i,j),max(i,j)) in E else -F(1,16) if i==j else F(0) for j in range(n)] for i in range(n)]
alpha=[sum(row) for row in M];A=[[alpha[i]*alpha[j]-M[i][j] for j in range(n)] for i in range(n)]
assert alpha==[F(1,8)]*8
mv=lambda a,v:[sum(x*y for x,y in zip(row,v)) for row in a]
spectrum=[]
for size in range(4):
 for subset in combinations(range(3),size):
  char=[F(1) for _ in V]
  for i,v in enumerate(V):
   for j in subset:char[i]*=v[j]
  eig=F(0) if size==0 else F(size-1,8)
  assert mv(A,char)==[eig*x for x in char]
  spectrum.append(str(eig))
def norm2(v):return sum(x*x for x in v)
def var(q):return sum(alpha[i]*norm2(q[i]) for i in range(n))-norm2([sum(alpha[i]*q[i][k] for i in range(n)) for k in range(3)])
def energy(q):return sum(M[i][j]*norm2([a-b for a,b in zip(q[i],q[j])]) for i,j in E)
rng=random.Random(932)
for _ in range(100):
 q=[[F(rng.randrange(-3,4),8) for _ in range(3)] for i in range(n)]
 assert all(norm2([a-b for a,b in zip(q[i],q[j])])<=4 for i,j in E)
 assert var(q)<=energy(q)<=3
# An affine edge-preserving map alone need not be orthogonal: radial data matters.
q=[[F(v[0])+F(3,5)*v[1],F(4,5)*v[1],F(v[2])] for v in V]
assert all(norm2([a-b for a,b in zip(q[i],q[j])])==4 for i,j in E)
assert any(norm2(qi)!=3 for qi in q)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def det(a,b,c):return dot(a,cross(b,c))
def sub(a,b):return [x-y for x,y in zip(a,b)]
def solid(a,b,c):
 na,nb,nc=(sqrt(dot(v,v)) for v in (a,b,c))
 return 2*atan2(det(a,b,c),na*nb*nc+dot(a,b)*nc+dot(b,c)*na+dot(c,a)*nb)
faces=[]
for axis in range(3):
 others=[k for k in range(3) if k!=axis]
 for sign in (-1,1):
  inds=[]
  for u,v in [(1,1),(-1,1),(-1,-1),(1,-1)]:
   x=[0,0,0];x[axis]=sign;x[others[0]]=u;x[others[1]]=v;inds.append(V.index(tuple(x)))
  a,b,c=[V[i] for i in inds[:3]]
  if dot(cross(sub(b,a),sub(c,a)),a)<0:inds.reverse()
  faces.append((axis,sign,inds))
scales=[2**i for i in range(n)];degrees=[]
for t in [0,F(1,7),F(1,2),F(6,7),1]:
 z=[[((1-t)+t*scales[i])*c for c in V[i]] for i in range(n)]
 angle=0
 for axis,sign,inds in faces:
  assert min(sign*z[i][axis] for i in inds)>0
  a,b,c,d=[z[i] for i in inds];angle+=solid(a,b,c)+solid(a,c,d)
 degrees.append(angle/(4*pi));assert abs(degrees[-1]-1)<1e-12
# The positive radial deformation generally destroys quadrilateral planarity.
z=[[scales[i]*c for c in V[i]] for i in range(n)];nonplanar=[]
for _,_,inds in faces:
 a,b,c,d=[z[i] for i in inds];nonplanar.append(det(sub(b,a),sub(c,a),sub(d,a)))
assert any(nonplanar)
# Nonsimple square-pyramid apex: four target-polar vertices in one strict halfspace.
apex=[0,0,1];polar_facet=[[2,0,1],[-2,0,1],[0,2,1],[0,-2,1]]
for positive in [[F(1,1000000),F(1),F(7),F(1000000)],[F(1)]*4]:
 assert all(dot(apex,[r*x for x in v])>0 for r,v in zip(positive,polar_facet))
# Dropping strict positivity creates a literal boundary zero at a vertex.
assert [0*x for x in polar_facet[0]]==[0,0,0]
result={'all_passed':True,'cube_psd_spectrum':spectrum,'exact_edge_contraction_samples':100,'degree_positive_radial_homotopy':degrees,'nonplanar_face_determinants':nonplanar,'affine_without_radial_data_can_fail_orthogonality':True,'nonsimple_four_facet_apex_halfspace':True,'zero_scale_negative_control_detected':True,'limits':'Finite exact algebra and numerical topological diagnostics are not a proof of universal rigidity, Wachspress regularity, or historical public availability.'}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
