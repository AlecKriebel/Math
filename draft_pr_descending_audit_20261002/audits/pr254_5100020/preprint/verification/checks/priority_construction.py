"""Exact construction distinctions; these are not new billiard proofs."""
from fractions import Fraction as F
from pathlib import Path
import json

def dot(p,q): return sum(x*y for x,y in zip(p,q))
def det(p,q): return p[0]*q[1]-p[1]*q[0]
def area(ps): return sum(det(p,ps[(i+1)%len(ps)]) for i,p in enumerate(ps))/2
def meet(n,h,m,g):
    d=det(n,m)
    assert d
    return ((h*m[1]-n[1]*g)/d,(n[0]*g-h*m[0])/d)
def pedal(ps):
    qs=[]
    for i,p in enumerate(ps):
        q=ps[(i+1)%len(ps)]; v=(q[0]-p[0],q[1]-p[1])
        n=(-v[1],v[0]); h=dot(n,p); nn=dot(n,n)
        qs.append(tuple(h*x/nn for x in n))
    return qs
def anti(ps): return [meet(p,dot(p,p),ps[(i+1)%len(ps)],dot(ps[(i+1)%len(ps)],ps[(i+1)%len(ps)])) for i,p in enumerate(ps)]

p=(F(6,5),F(4,5)); a,b=F(2),F(1)
assert p[0]**2/a**2+p[1]**2/b**2==1
outer_normal=(p[0]/a**2,p[1]/b**2)
assert det(outer_normal,p)==F(-18,25)
inv=tuple(x/dot(p,p) for x in p)
assert inv[0]**2/a**2+inv[1]**2/b**2==dot(inv,inv)**2
assert dot(inv,p)==1
radial_support_squared=2*a*a*b*b/(a*a+b*b)
elliptic_support_squared=(a*a+b*b)/2
assert radial_support_squared==F(8,5)
assert elliptic_support_squared==F(5,2)
assert elliptic_support_squared-radial_support_squared==F(9,10)
triangle=[(F(2),F(0)),(F(0),F(2)),(F(-1),F(-1))]
aa=area(triangle); ap=area(pedal(triangle)); ant=area(anti(triangle))
assert (aa,ap,ant)==(F(4),F(24,25),F(18))
assert ap*ant==F(432,25)!=aa**2
result={
  'status':'PASS',
  'ellipse_outer_vs_origin_antipedal_normal_determinant':str(det(outer_normal,p)),
  'inversion_quartic_identity':True,
  'circular_polar_of_inverse_vertex_is_antipedal_side':True,
  'antipedal_line_support_squared_at_45_degrees':str(radial_support_squared),
  'outer_ellipse_line_support_squared_at_45_degrees':str(elliptic_support_squared),
  'generic_triangle_original_area':str(aa),
  'generic_triangle_same_origin_pedal_area':str(ap),
  'generic_triangle_same_origin_antipedal_area':str(ant),
  'same_point_generic_product':str(ap*ant),
  'original_area_squared':str(aa**2),
  'scope':'The triangle is an exact negative control on an overly general same-point area-product shortcut, not a billiard counterexample. The normal test distinguishes the actual constructions, not every possible reindexing or transformation.'
}
Path(__file__).with_name('CONSTRUCTION_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
