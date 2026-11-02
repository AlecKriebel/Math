import json, sympy as s
from pathlib import Path
base=Path(__file__).resolve().parents[1]
rows=json.loads((base/'results.json').read_text())
for r in rows:
 d=r['dimension']; cones=r['maximal_cones']; rays=r['rays']; q=len(cones)
 assert all(len(set(c))==d and all(0<=i<len(rays) for i in c) for c in cones)
 assert all(abs(s.det(s.Matrix([rays[i] for i in c])))==1 for c in cones)
 dimensions=[]
 for w in rays:
  equations=[]
  # Unknowns are d slope coordinates for EACH maximal cone, not ray values.
  # All pairs agree on every shared ray, guaranteeing PL continuity.
  for i in range(q):
   for j in range(i):
    for k in set(cones[i]) & set(cones[j]):
     eq=[0]*(d*q)
     for h in range(d): eq[d*i+h]=rays[k][h]; eq[d*j+h]=-rays[k][h]
     equations.append(eq)
   if i:
    eq=[0]*(d*q)
    for h in range(d): eq[d*i+h]=w[h]; eq[h]=-w[h]
    equations.append(eq)
  dimensions.append(d*q-s.Matrix(equations).rank()-d)
 assert dimensions==r['nonlinear_kernel_dimensions'],(r['name'],dimensions)
 print(r['name'], 'smooth cone determinants and slope-coordinate kernel PASS',dimensions)
