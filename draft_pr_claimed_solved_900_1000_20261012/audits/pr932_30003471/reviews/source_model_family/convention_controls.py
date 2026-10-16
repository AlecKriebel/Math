#!/usr/bin/env python3
"""Exact finite controls for coefficient transpose and Clifford/index signs.

This is a convention diagnostic, not a proof of Fredholm theory or rigidity.
Only Python's standard library is required.
"""
import json, math
from pathlib import Path

def add(a,b): return [[a[i][j]+b[i][j] for j in range(2)] for i in range(2)]
def scale(t,a): return [[t*z for z in row] for row in a]
def mul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def transpose(a): return [list(row) for row in zip(*a)]
def adjoint(a): return [[a[j][i].conjugate() for j in range(2)] for i in range(2)]
def flat(a): return sum(a,[])
def rank(rows):
 rows=[list(map(complex,r)) for r in rows]; pivot=0
 for col in range(len(rows[0])):
  selected=next((k for k in range(pivot,len(rows)) if rows[k][col]!=0),None)
  if selected is None: continue
  rows[pivot],rows[selected]=rows[selected],rows[pivot]
  z=rows[pivot][col]; rows[pivot]=[x/z for x in rows[pivot]]
  for k in range(len(rows)):
   if k!=pivot:
    z=rows[k][col]; rows[k]=[x-z*y for x,y in zip(rows[k],rows[pivot])]
  pivot+=1
  if pivot==len(rows): break
 return pivot

I=[[1+0j,0j],[0j,1+0j]]; Z=scale(0,I)
sigma=[[[0j,1+0j],[1+0j,0j]],[[0j,-1j],[1j,0j]],[[1+0j,0j],[0j,-1+0j]]]
c=[scale(-1j,s) for s in sigma]
omega=[transpose(g) for g in c]
basis=[]
for r in range(2):
 for col in range(2):
  a=[[0j,0j],[0j,0j]];a[r][col]=1+0j;basis.append(a)

def chi_from_indices(n,e,A):
 # A's columns are spinors, omega[e][alpha][beta] is the coefficient
 # of spinor basis beta in c[e] acting on spinor basis alpha.
 return [[-sum(c[n][r][s]*A[s][beta]*omega[e][alpha][beta]
               for s in range(2) for beta in range(2))
          for alpha in range(2)] for r in range(2)]

def chi_matrix(n,e,A): return scale(-1,mul(mul(c[n],A),c[e]))

def null_dimension(sign):
 rows=[]
 for g in c:
  columns=[flat(add(mul(g,A),scale(sign,mul(A,g)))) for A in basis]
  rows.extend(zip(*columns))
 return 4-rank(rows)

checks={
 'pauli_skew_adjoint':all(adjoint(g)==scale(-1,g) for g in c),
 'clifford_all_coordinate_pairs':all(add(mul(c[i],c[j]),mul(c[j],c[i]))==scale(-2*(i==j),I) for i in range(3) for j in range(3)),
 'source_column_volume_minus_identity':mul(mul(c[0],c[1]),c[2])==scale(-1,I),
 'row_coefficients_volume_plus_identity':mul(mul(omega[0],omega[1]),omega[2])==I,
 'coefficient_to_column_matrix_translation_36_cases':all(chi_from_indices(n,e,A)==chi_matrix(n,e,A) for n in range(3) for e in range(3) for A in basis),
 'chi_involution_36_cases':all(chi_matrix(n,e,chi_matrix(n,e,A))==A for n in range(3) for e in range(3) for A in basis),
 'gauss_identity_kernel_3_axes':all(chi_matrix(i,i,I)==I for i in range(3)),
 'naive_untransposed_target_fails_y_axis_identity':scale(-1,mul(mul(c[1],I),omega[1]))==scale(-1,I),
 'commuting_space_dimension_one':null_dimension(-1)==1,
 'anticommuting_space_dimension_zero':null_dimension(1)==0,
}
assert all(checks.values()),checks
pyramid=[]
for h in [1e-6,1.0,1e6]:
 margin=1/math.sqrt(h*h+1)
 # At the four-valent apex all four side-facet normals have z-component margin.
 adjacent_exterior=math.acos(1/(1+h*h))
 pyramid.append(dict(height=h,apex_incident_facets=4,target_radial_dot_each_side_normal=margin,adjacent_side_interior_angle=math.pi-adjacent_exterior))
result=dict(purpose='Exact convention controls only; no numerical proof of universal rigidity.',checks=checks,coefficient_cases=36,commuting_space_dimension=null_dimension(-1),anticommuting_space_dimension=null_dimension(1),nonsimple_apex_controls=pyramid,limits='Finite checks do not certify elliptic Fredholm theory, compactness or universal geometry.')
Path('CONVENTION_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
