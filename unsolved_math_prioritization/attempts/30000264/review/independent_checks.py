#!/usr/bin/env python3
"""Independent Schur-complement, configuration and cone controls."""
from fractions import Fraction as F
from math import isqrt
from itertools import product
from pathlib import Path
from hashlib import sha256
from collections import Counter
import json
C=Counter()
def ck(g,v):
 assert v,g
 C[g]+=1
def dot(v,w):return sum(a*b for a,b in zip(v,w))
def transpose(A):return list(map(list,zip(*A)))
def mm(A,B):return [[dot(r,c) for c in zip(*B)] for r in A]
def ident(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def square_root(x):
 a=isqrt(x.numerator);b=isqrt(x.denominator)
 ck('exact_distance_root',a*a==x.numerator and b*b==x.denominator)
 return F(a,b)

# Reconstruct reciprocal distances, then eliminate the first two coordinates.
witnesses=[]
for t in dict.fromkeys([F(1,5),F(1,3)]+[F(j,80) for j in range(9,33)]):
 c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
 points=[(c,s,F(0)),(c,-s,F(0)),(-c,s,F(0)),(-c,-s,F(0))]
 A=[[F(0) if i==j else 1/square_root(sum((a-b)**2 for a,b in zip(points[i],points[j]))) for j in range(4)] for i in range(4)]
 a=A[0][1];b=A[0][2];d=A[0][3]
 ck('distance_matrix_form',A==[[0,a,b,d],[a,0,d,b],[b,d,0,a],[d,b,a,0]])
 B=[[0,a],[a,0]];X=[[b,d],[d,b]];Bi=[[0,1/a],[1/a,0]]
 Xi=mm(Bi,X)
 T=ident(4)
 for i in range(2):
  for j in range(2):T[i][j+2]=-Xi[i][j]
 D=mm(mm(transpose(T),A),T)
 schur=[[ -2*b*d/a,a-(b*b+d*d)/a ],[a-(b*b+d*d)/a,-2*b*d/a]]
 ck('Schur_congruence',D==[B[0]+[0,0],B[1]+[0,0],[0,0]+schur[0],[0,0]+schur[1]])
 plus=schur[0][0]+schur[0][1];minus=schur[0][0]-schur[0][1]
 ck('Schur_positive_branch',plus==(a*a-(b+d)**2)/a)
 ck('Schur_negative_branch',minus==((b-d)**2-a*a)/a<0)
 negative=1+int(plus<0)+int(minus<0)
 positive=1+int(plus>0)+int(minus>0)
 ck('Schur_trace_control',sum(A[i][i] for i in range(4))==0)
 if t in (F(1,5),F(1,3)):
  witnesses.append({'half_angle':str(t),'negative':negative,'positive':positive,'sphere_dimension':negative-1})
 numerator=1-4*t-t**4
 ck('crossing_sign',((plus>0)-(plus<0))==((numerator>0)-(numerator<0)))
 ck('crossing_derivative',-4-4*t**3<0)
ck('different_homology_dimensions',[w['sphere_dimension'] for w in witnesses]==[1,2])

# Global configuration-factor coordinates, using rational unit quaternions.
def conj(q):return(q[0],-q[1],-q[2],-q[3])
def qm(q,r):
 a,b,c,d=q;e,f,g,h=r
 return(a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)
def inv_stereo(x):
 norm=dot(x,x)
 return ((norm-1)/(norm+1),)+tuple(2*t/(norm+1) for t in x)
def stereo(q):return tuple(t/(1-q[0]) for t in q[1:])
base=[(F(i),F(j),F(k)) for i,j,k in product((-1,0,1),repeat=3)]
for seed in base[::3]:
 a1=inv_stereo(seed)
 for x in base[::4]:
  for y in base[1::5]:
   if x==y:continue
   a2=qm(a1,inv_stereo(x));a3=qm(a1,inv_stereo(y))
   ck('quaternion_unit',dot(a1,a1)==dot(a2,a2)==dot(a3,a3)==1)
   ck('labelled_configuration_distinct',len({a1,a2,a3})==3)
   xx=stereo(qm(conj(a1),a2));yy=stereo(qm(conj(a1),a3))
   ck('configuration_product_inverse',xx==x and yy==y)
   midpoint=tuple((xx[i]+yy[i])/2 for i in range(3));difference=tuple(yy[i]-xx[i] for i in range(3))
   ck('Euclidean_pair_inverse',tuple(midpoint[i]-difference[i]/2 for i in range(3))==x and tuple(midpoint[i]+difference[i]/2 for i in range(3))==y and any(difference))

# Nonorthogonal three-point coordinates explicitly verify the global congruence.
V=[[F(1),F(1),F(1)],[F(-1),F(1),F(1)],[F(0),F(-2),F(1)]]
C3=[[F(i!=j) for j in range(3)] for i in range(3)]
ck('fixed_C3_normal_form',mm(mm(transpose(V),C3),V)==[[-2,0,0],[0,-6,0],[0,0,6]])
for diag in product((F(1,3),F(1),F(5,2)),repeat=3):
 A=[[F(0) if i==j else diag[i]*diag[j] for j in range(3)] for i in range(3)]
 a,b,c=A[0][1],A[0][2],A[1][2]
 ck('positive_diagonal_recovery',(a*b/c,a*c/b,b*c/a)==tuple(z*z for z in diag))
 for x in [tuple(map(F,z)) for z in [(1,2,3),(1,-1,0),(0,1,-1),(1,0,0)]]:
  dx=tuple(diag[i]*x[i] for i in range(3))
  ck('total_congruence',dot(x,tuple(dot(row,x) for row in A))==sum(dx)**2-dot(dx,dx))

# Null directions are retained in the weak cone, removed only in the strict cone.
for rm,rz,rp in [(0,1,2),(1,1,1),(2,0,1),(1,0,2),(0,0,3),(0,3,0)]:
 n=rm+rz+rp
 for v in product((F(-2),F(0),F(1)),repeat=n):
  if not any(v):continue
  value=-2*sum(z*z for z in v[:rm])+3*sum(z*z for z in v[rm+rz:])
  if value<=0:
   ck('weak_target_nonzero',any(v[:rm+rz]))
   for t in (F(0),F(1,4),F(3,4),F(1)):
    w=v[:rm+rz]+tuple((1-t)*z for z in v[rm+rz:])
    ck('weak_cone_deformation',any(w) and -2*sum(z*z for z in w[:rm])+3*sum(z*z for z in w[rm+rz:])<=0)
  if value<0:
   ck('strict_negative_nonzero',any(v[:rm]))
   for t in (F(0),F(1,4),F(3,4),F(1)):
    w=v[:rm]+tuple((1-t)*z for z in v[rm:])
    ck('strict_cone_deformation',any(w) and -2*sum(z*z for z in w[:rm])+3*sum(z*z for z in w[rm+rz:])<0)

root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(C.values()),'categories':dict(C),'independent_Schur_witnesses':witnesses,'artifact_sha256':sha256((root/'author_replay/PARTIAL.md').read_bytes()).hexdigest(),'scope':'Exact Schur-complement, global-coordinate and cone-deformation diagnostics only; no determination of the general total topology.'}
(root/'independent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
