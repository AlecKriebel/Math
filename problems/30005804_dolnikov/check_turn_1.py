from exact_geometry import *
import json
c=0;instances=0;max_tau=0
shapes=[[(0,0),(2,0),(0,2)],[(0,0),(3,0),(2,2),(0,1)],[(0,0),(2,0),(3,1),(1,3),(0,2)],[(0,0),(2,0),(2,2),(0,2)]]
centers=[(x,y) for x in (0,2,4) for y in (0,2,4)]
for K in shapes:
 polys=[[(F(a+x),F(b+y)) for a,b in K] for x,y in centers];cv=masks(polys)
 for S in range(1,1<<len(polys)):
  a=min_cover(S,cv);b=hypergraph_chromatic(S,cv);assert a==b;c+=1;instances+=1;max_tau=max(max_tau,a)
 for i,P in enumerate(polys):
  for p in P:assert inside(p,P);c+=1
 # Every candidate is rational, and each coverage bit is checked directly.
 for m,p in cv.items():
  for i,P in enumerate(polys):assert bool(m>>i&1)==inside(p,P);c+=1
K=[(0,0),(2,0),(0,2)];ps=[[(F(a+x),F(b+y)) for a,b in K] for x,y in [(0,0),(2,0),(0,2)]];cv=masks(ps)
assert all(any(m&e==e for m in cv) for e in [3,5,6]);c+=1
assert not any(m==7 for m in cv);c+=1
assert min_cover(7,cv)==hypergraph_chromatic(7,cv)==2;c+=1
# Thickening/perturbation slack constants, exact rational arithmetic.
assert F(3,8)-F(1,16)>F(1,4) and F(3,8)+F(1,16)<F(1,2);c+=1
assert F(1,4)-F(1,8)==F(1,8) and F(1,2)+F(1,8)==F(5,8)<1;c+=1
print(json.dumps({'assertions':c,'rational_family_instances':instances,'fixed_grid_centers':9,'fixed_polygons':4,'largest_piercing_number_seen':max_tau,'scope':'Exact instance algorithms and Helly equivalence only; no exhaustive colorful conjecture claim'},indent=2,sort_keys=True))
