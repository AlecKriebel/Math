#!/usr/bin/env python3
"""Exact finite geometry controls. Requires SymPy; no group/E-infinity lift certified."""
import sympy as s
from itertools import combinations,permutations
from collections import Counter
from pathlib import Path
import json,hashlib
a=(1+s.sqrt(5))/2
ap=1-a
sp=lambda z:s.simplify(s.expand(z))
checks=Counter()
def ck(k,v):
    assert bool(v),k
    checks[k]+=1
def eq(A,B):
    return all(sp(z)==0 for z in A-B)
verts=[s.Matrix(z) for z in [(0,0),(1,0),(a,1),(1,a),(0,1)]]
lines=[s.Matrix(z) for z in [(0,1,0),(0,1,-1),(1,-a,0),(1,-a,a),(a,-1,0),(a,-1,-a),(1,0,0),(1,0,-1),(0,0,1)]]
sigma=[2,3,6,7,0,1,4,5,8]
sv=[0,2,4,1,3]
Q=s.Matrix([[1,(1-s.sqrt(5))/4],[(1-s.sqrt(5))/4,1]])
ck('pentagon_metric_positive',Q.det()>0)
for i,j in combinations(range(5),2):
    d=verts[i]-verts[j]
    expected=1 if ((i-j)%5 in [1,4]) else a*a
    ck('regular_pentagon_distances',sp((d.T*Q*d)[0]-expected)==0)
ck('golden_identity',sp(a*a-a-1)==0)
ck('galois_sum_product',sp(a+ap-1)==0 and sp(a*ap+1)==0)
def flats(L):
    out=set()
    for i,j in combinations(range(len(L)),2):
        p=L[i].cross(L[j]);ck('distinct_lines',any(sp(z)!=0 for z in p))
        out.add(tuple(k for k,l in enumerate(L) if sp(l.dot(p))==0))
    return sorted(out)
F=flats(lines)
expected=[(0,1,8),(0,2,4,6),(0,3),(0,5,7),(1,2,5),(1,3,6),(1,4),(1,7),(2,3,8),(2,7),(3,4,7),(3,5),(4,5,8),(5,6),(6,7,8)]
ck('all_intersection_flats',F==expected)
for f in F:
    ck('sigma_preserves_flats',tuple(sorted(sigma[i] for i in f)) in F)
for i in range(9):
    ck('sigma_order_four',sigma[sigma[sigma[sigma[i]]]]==i)
R=s.Matrix([[0,1,0],[1,0,0],[0,0,1]])
T=s.Matrix([[a,1],[1,a]])
ck('candidate_affine_invertible',sp(T.det()-a)==0)
for i in [0,1,4]:
    ck('forced_affine_vertex_images',eq(T*verts[i],verts[sv[i]]))
ck('forced_affine_fails_C',not eq(T*verts[2],verts[sv[2]]))
for i in range(8):
    k=sigma[sigma[i]]
    ck('square_geometric_line_map',eq((R.T*lines[k]).cross(lines[i]),s.zeros(3,1)))
for l in lines[:8]:
    ck('fixed_basepoint_outside_arrangement',sp(l.dot(s.Matrix([2,2,1])))!=0)
conjugated=[v.applyfunc(lambda x:sp(x.subs(s.sqrt(5),-s.sqrt(5)))) for v in verts]
for i in range(5):
    ck('cross_realization_vertex_map',eq(T*conjugated[i],verts[sv[i]]))
# Explicit identification with the published Nazir-Yoshinaga equations.
N=[s.Matrix(v) for v in [(1,0,0),(1,-a,a),(0,1,-1),(1,1,-1),(1,0,-1),(1,-a,0),(0,1,0),(1,1,-a-1),(0,0,1)]]
U=s.Matrix([[0,1,0],[-1,a-1,1],[0,0,1]])
d=[0,4,3,7,2,6,1,5,8]
ck('FS_identification_invertible',U.det()==1)
for i in range(9):
    ck('FS_identification_line_equations',eq((U.T*N[d[i]]).cross(lines[i]),s.zeros(3,1)))
# All combinatorial automorphisms: the unique quadruple point determines four
# incident lines; their parallel partners are then forced by the fixed infinity line.
auts=[]
for perm in permutations([0,2,4,6]):
    h={8:8}
    for old,new in zip([0,2,4,6],perm):h[old]=new;h[old+1]=new+1
    if sorted(tuple(sorted(h[i] for i in f)) for f in F)==F:auts.append([h[i] for i in range(9)])
powers=[];cur=list(range(9))
for k in range(4):
    powers.append(cur);cur=[sigma[i] for i in cur]
ck('affine_combinatorial_group_C4',sorted(auts)==sorted(powers))
p=Path(__file__)
receipt={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
'artifact_sha256':hashlib.sha256(p.with_name('OBSTRUCTION.md').read_bytes()).hexdigest(),
'checker_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sympy_version':s.__version__,
'line_permutation':sigma,'flats':F,'affine_combinatorial_automorphisms':auts,
'limitation':'Finite incidence, affine identities and normalization only. No sigma lift to the full fundamental group or integral E-infinity coalgebra is certified.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
