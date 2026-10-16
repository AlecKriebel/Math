"""Fresh exact controls for the specific earlier-combination and isotropic gaps."""
from pathlib import Path
import sympy as s,json,hashlib
HERE=Path(__file__).resolve().parent
M=lambda x,y:s.Matrix([x,y])
def det(p,q):return s.det(s.Matrix.hstack(p,q))
def area(poly):return s.simplify(sum(det(p,poly[(i+1)%len(poly)]) for i,p in enumerate(poly))/2)
def anti(poly):return [s.simplify(s.Matrix.vstack(p.T,poly[(i+1)%len(poly)].T).inv()*M(p.dot(p),poly[(i+1)%len(poly)].dot(poly[(i+1)%len(poly)]))) for i,p in enumerate(poly)]
def f(p,q):return s.simplify((p.dot(p)*q.dot(q)-(p.dot(p)+q.dot(q))*p.dot(q)/2)/det(p,q))
triangle=[M(0,s.sqrt(5)),M(-s.Rational(8,3),-s.sqrt(5)/3),M(s.Rational(8,3),-s.sqrt(5)/3)]
assert all(any(p == -q for q in triangle) is False for p in triangle)
for i,p in enumerate(triangle):
 q=triangle[(i+1)%3];prev=triangle[(i-1)%3];edge=q-p;normal=M(-edge[1],edge[0]);h=normal.dot(p)
 assert s.simplify(p[0]**2/8+p[1]**2/5-1)==0
 assert s.simplify(normal[0]**2*s.Rational(32,9)+normal[1]**2*s.Rational(5,9)-h**2)==0
 incoming=p-prev;nu=M(p[0]/8,p[1]/5);reflected=s.simplify(incoming-2*incoming.dot(nu)/nu.dot(nu)*nu)
 assert s.simplify(det(reflected,edge))==0 and s.simplify(reflected.dot(edge)).is_positive
assert area(triangle)!=0
A=area(triangle);U=area(anti(triangle));actual=s.simplify(U/A)
aa,bb,lam=s.Integer(8),s.Integer(5),s.Rational(40,9);d=aa-bb;D=aa*bb
focal_R=s.simplify((D*(3*bb-aa)+lam*d**2)/(2*D*(bb-lam)))
assert focal_R==s.Rational(36,5) and actual!=focal_R
focus=s.sqrt(3); p=triangle[0]
assert s.simplify((p-M(focus,0)).dot(p-M(focus,0))-(s.sqrt(8)-focus*(p[0]/s.sqrt(8)))**2)==0
origin_formula_residual=s.simplify(p.dot(p)-aa);assert origin_formula_residual==-3
# A finite antipedal whose first complex vertex is isotropic.
poly=[M(1,s.I),M(0,1),M(2,0)]
assert poly[0].dot(poly[0])==0
for p,q in zip(poly,poly[1:]+poly[:1]):assert det(p,q)!=0
rs=anti(poly)
assert s.simplify(area(rs)-sum(f(p,poly[(i+1)%3]) for i,p in enumerate(poly)))==0
for i,r in enumerate(rs):
 for p in (poly[i],poly[(i+1)%3]):assert s.simplify(p.dot(r)-p.dot(p))==0
z=s.symbols('z');P=M(1,s.I);Q=M(1+z,s.I)
num=s.expand(P.dot(P)*Q.dot(Q)-(P.dot(P)+Q.dot(Q))*P.dot(Q)/2)
assert s.expand(num/z**2+1+z/2)==0
assert s.limit(f(P,Q),z,0)==0
# Same-caustic N4 direct line construction independently rebuilt.
def pedal(poly):
 out=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  edge=q-p;normal=M(-edge[1],edge[0]);out.append(s.simplify(normal*normal.dot(p)/normal.dot(normal)))
 return out
ps=[M(s.sqrt(5),0),M(0,s.sqrt(3)),M(-s.sqrt(5),0),M(0,-s.sqrt(3))]
al=s.sqrt(s.Rational(25,8));be=s.sqrt(s.Rational(9,8));rect=[M(al,be),M(-al,be),M(-al,-be),M(al,-be)]
even=[]
for points in (ps,rect):
 for i,p in enumerate(points):
  q=points[(i+1)%4];prev=points[(i-1)%4];edge=q-p;normal=M(-edge[1],edge[0]);h=normal.dot(p)
  assert s.simplify(normal[0]**2*al**2+normal[1]**2*be**2-h**2)==0
  incoming=p-prev;nu=M(p[0]/5,p[1]/3);reflected=s.simplify(incoming-2*incoming.dot(nu)/nu.dot(nu)*nu)
  assert s.simplify(det(reflected,edge))==0 and s.simplify(reflected.dot(edge)).is_positive
 even.append(str(s.simplify(area(pedal(points))*area(anti(points)))))
assert even==['225/4','289/4']
result={'status':'PASS','central_pair_failure':{'strict_reflected_odd_triangle_vertices':[[str(c) for c in p] for p in triangle],'exact_outer_membership_caustic_tangency_and_forward_reflection':True,'least_period_3_by_three_distinct_noncollinear_vertices':True,'no_negated_partner_for_any_vertex':True,'original_area':str(A),'origin_antipedal_area':str(U),'actual_origin_ratio':str(actual),'prior_focal_R':str(focal_R),'invalid_origin_specialization_residual':str(origin_formula_residual),'mechanism':'An odd nonzero vertex set cannot have an involutive opposite pairing. Focal norm identities impose c^2=a^2-b^2; choosing F=O in a noncircular ellipse breaks them.'},'isotropic_control':{'vertices':[[str(c) for c in p] for p in poly],'finite_named_intersections':[[str(c) for c in p] for p in rs],'actual_signed_area':str(area(rs)),'F_equals_actual_signed_area':True,'coincident_isotropic_numerator':str(num),'coincident_isotropic_second_order_and_removable':True},'same_caustic_N4':{'exact_reflection_and_tangency':True,'products':even},'sympy':s.__version__}
(HERE/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
