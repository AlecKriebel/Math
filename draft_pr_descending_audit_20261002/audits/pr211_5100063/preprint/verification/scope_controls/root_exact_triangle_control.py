"""Actual outer tangent geometry in two exact triangular phases.

The two original phases are also used in Ferudun2026, DOI23096994, Section6,
for the different ORIGINAL-vertex product. This control derives the OUTER
vertices by solving boundary tangent equations and uses no Jacobi formulas.
It is finite exact evidence, not the all-period proof or priority clearance.
"""
from pathlib import Path
import json,hashlib
import sympy as s
def clean(x):return s.simplify(s.radsimp(x))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def area(p):return clean(sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2)
def inv(p,f):
 x,y=p[0]-f,p[1];d=clean(x*x+y*y);assert d>0
 return (clean(x/d),clean(y/d))
aa,bb=s.Integer(21),s.Integer(16);lam=s.Rational(336,25);c=s.sqrt(aa-bb)
H=[(s.sqrt(21),0),(-3*s.sqrt(21)/5,s.Rational(16,5)),(-3*s.sqrt(21)/5,-s.Rational(16,5))]
V=[(0,s.Integer(4)),(-s.Rational(21,5),-s.Rational(8,5)),(s.Rational(21,5),-s.Rational(8,5))]
rows=[]
for label,points in [('H',H),('V',V)]:
 outer=[]
 for j,p in enumerate(points):
  q=points[(j+1)%3];assert clean(p[0]**2/aa+p[1]**2/bb-1)==0
  nx,ny=q[1]-p[1],p[0]-q[0];ell=nx*p[0]+ny*p[1]
  assert clean(ell*ell-(aa-lam)*nx*nx-(bb-lam)*ny*ny)==0
  ap,bp=p[0]/aa,p[1]/bb;aq,bq=q[0]/aa,q[1]/bb;dd=clean(ap*bq-aq*bp);assert dd!=0
  Q=(clean((bq-bp)/dd),clean((ap-aq)/dd));outer.append(Q)
  assert clean(ap*Q[0]+bp*Q[1]-1)==0 and clean(aq*Q[0]+bq*Q[1]-1)==0
  assert clean(Q[0]**2/aa+Q[1]**2/bb-1)>0
 areas=[area([inv(p,f) for p in outer]) for f in [c,-c]]
 original=[area([inv(p,f) for p in points]) for f in [c,-c]]
 product=clean(areas[0]*areas[1]);original_product=clean(original[0]*original[1]);assert all(a>0 for a in areas)
 for r in [3,5,7]:
  repeated=[area([inv(p,f) for p in outer]*r) for f in [c,-c]]
  assert clean(repeated[0]*repeated[1]-r*r*product)==0
 rows.append(dict(phase=label,outer_vertices=[[str(x) for x in p] for p in outer],outer_inverse_areas=[str(x) for x in areas],outer_product=str(product),original_inverse_areas=[str(x) for x in original],original_product=str(original_product)))
assert rows[0]['outer_product']==rows[1]['outer_product']
assert rows[0]['outer_product']!=rows[0]['original_product']
out=dict(status='PASS finite exact actual-geometry controls',sympy=s.__version__,ellipse_squared_axes=[str(aa),str(bb)],caustic_parameter=str(lam),phases=rows,repetition_factors=[3,5,7],limits='No general-period or novelty conclusion. Distinguishes original-vertex and outer-vertex products in the same billiard family.')
Path(__file__).with_name('ROOT_EXACT_TRIANGLE_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
