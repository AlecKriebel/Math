"""Independently verify a priority-family broad-transfer counterexample.

These triangles are in a concentric homothetic Poncelet pair. They do not
constitute the particular confocal-billiard outer family under audit.
"""
from pathlib import Path
import sympy as s,json
rt=s.sqrt(3);f=rt/2
polygons=[[(s.Integer(2),0),(-s.Integer(1),rt/2),(-s.Integer(1),-rt/2)],[(rt,s.Rational(1,2)),(-rt,s.Rational(1,2)),(0,-s.Integer(1))]]
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(poly):return s.simplify(sum(det(poly[i],poly[(i+1)%3]) for i in range(3))/2)
rows=[]
for p in polygons:
 for j,(x,y) in enumerate(p):
  assert s.simplify(x*x/4+y*y-1)==0
  X,Y=p[(j+1)%3];nx,ny=Y-y,x-X;ell=nx*x+ny*y
  assert s.simplify(ell*ell-nx*nx-ny*ny/4)==0
  # Contact point is strictly on the segment, not merely its line.
  T=(s.simplify(nx/ell),s.simplify(ny/(4*ell)))
  parameter=s.simplify(((T[0]-x)*(X-x)+(T[1]-y)*(Y-y))/((X-x)**2+(Y-y)**2))
  assert 0<parameter<1
 areas=[]
 for focus in [f,-f]:
  inverse=[]
  for x,y in p:
   d=s.simplify((x-focus)**2+y*y);assert d>0
   inverse.append((s.simplify((x-focus)/d),s.simplify(y/d)))
  areas.append(area(inverse))
 rows.append(dict(areas=[str(a) for a in areas],product=str(s.simplify(areas[0]*areas[1]))))
assert rows[0]['product']=='27/169' and rows[1]['product']=='27/196'
gap=s.simplify(s.Rational(rows[0]['product'])-s.Rational(rows[1]['product']));assert gap==s.Rational(729,33124)
out=dict(status='PASS exact broad-transfer obstruction',outer_ellipse_axes=['2','1'],inner_ellipse_axes=['1','1/2'],inversion_centers=['sqrt(3)/2','-sqrt(3)/2'],phase_results=rows,nonzero_product_gap=str(gap),boundary_incidence_and_same_inner_tangency_and_internal_contact=True,implication='An all-concentric-Poncelet caustic-focus paired-area product theorem is false. Does not refute the particular confocal-billiard target; any valid transfer needs extra hypotheses.',construction_lead='Independent classical-general priority family; root rederived all geometry and inversion values without importing its checker.')
Path(__file__).with_name('ROOT_GENERIC_TRANSFER_COUNTEREXAMPLE.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
