#!/usr/bin/env python3
"""Exact finite controls for geometry, normalization and planar combinatorics."""
from fractions import Fraction as F
from itertools import product,combinations
import json
checks=0
def ok(v):
 global checks
 assert v
 checks+=1
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return dot(a,a)
def project(c,u,v):
 w=sub(v,u);t=(norm(v)-norm(u)-2*dot(c,w))/(2*norm(w));return add(c,tuple(t*x for x in w))
def circum(A,B,C):
 u=sub(B,A);v=sub(C,A);x=(norm(B)-norm(A))/2;y=(norm(C)-norm(A))/2;det=u[0]*v[1]-u[1]*v[0]
 return ((x*v[1]-y*u[1])/det,(u[0]*y-v[0]*x)/det)
base=[(F(-1),F(0)),(F(1),F(0)),(F(0),F(1)),(F(0),F(1,4))]
witness=[((0,1),(F(0),F(-3)),F(10)),((0,2),(F(-3),F(3)),F(13)),((1,2),(F(3),F(3)),F(13))]
for (i,j),c,r2 in witness:
 ok(norm(sub(base[i],c))==r2);ok(norm(sub(base[j],c))==r2)
 for k in set(range(4))-{i,j}:ok(norm(sub(base[k],c))>r2)
ok(circum(*base[:3])==(0,0));ok(norm(base[3])<1)
# Finite perturbations supplement continuity; this does not certify a uniform radius.
eta=F(1,1000)
for signs in product((-1,1),repeat=8):
 P=[(base[i][0]+eta*signs[2*i],base[i][1]+eta*signs[2*i+1]) for i in range(4)]
 for (i,j),c,_ in witness:
  z=project(c,P[i],P[j]);r2=norm(sub(z,P[i]));ok(norm(sub(z,P[j]))==r2)
  for k in set(range(4))-{i,j}:ok(norm(sub(z,P[k]))>r2)
 cc=circum(*P[:3]);rr=norm(sub(cc,P[0]));ok(norm(sub(cc,P[3]))<rr)
# Spherical face-stacking triangulations attain the3n-8 clique bound.
E={tuple(sorted(e)) for e in combinations(range(4),2)};faces=[tuple(t) for t in combinations(range(4),3)]
for n in range(4,61):
 triangles=[t for t in combinations(range(n),3) if all(tuple(sorted(e)) in E for e in combinations(t,2))]
 ok(len(triangles)==3*n-8);ok(len(faces)==2*n-4)
 # incidence normalization for simplex counting
 scores=[sum(v in t for t in triangles) for v in range(n)];ok(sum(scores)==3*len(triangles))
 f=faces.pop((n*7)%len(faces));E.update(tuple(sorted((v,n))) for v in f)
 faces +=[(f[0],f[1],n),(f[1],f[2],n),(f[2],f[0],n)]
# Octahedral triangulation: a non-extremal planar control.
O={(i,j) for i,j in combinations(range(6),2) if i//2!=j//2}
tri=sum(all(tuple(sorted(e)) in O for e in combinations(t,2)) for t in combinations(range(6),3));ok(tri==8);ok(tri<3*6-8)
# Positive Stirling-coefficient Poisson moment bounds used analytically.
S=[[0]*12 for _ in range(12)];S[0][0]=1
for q in range(1,11):
 for j in range(1,q+1):S[q][j]=j*S[q-1][j]+S[q-1][j-1]
 bell=sum(S[q])
 for t in range(101):
  mu=F(t,7);moment=sum(S[q][j]*mu**j for j in range(1,q+1));ok(moment<=bell*(1+mu)**q)
# Exact cube-intersection boundary ratio and its elementary union bound.
for d in range(1,5):
 for widths in product(range(1,5),repeat=d):
  for R in (3,10,100):
   ratio=F(1)
   for w in widths:ratio*=max(F(0),1-F(w,2*R))
   ok(0<=ratio<=1);ok(1-ratio<=sum(F(w,2*R) for w in widths))
print(json.dumps(dict(status='PASS',assertions=checks,perturbed_configurations=256,stacked_triangulations=57,scope='finite exact controls; analytic proof supplies Palm integrability, L1 limits and positive-probability robustness'),indent=2,sort_keys=True))
