"""Own exact physical verification of disclosed vertices, with direct linear solve."""
from pathlib import Path
from datetime import datetime,timezone
import sympy as sy,json
out=Path(__file__).resolve().parent;Q=sy.Rational
cross=lambda p,q:sy.det(sy.Matrix.hstack(p,q))
def area(v):return sy.simplify(sum(cross(v[i],v[(i+1)%len(v)]) for i in range(len(v)))/2)
cases=[('N6-major',Q(3,2),sy.Integer(1),Q(9,25),[(Q(3,2),0),(Q(9,10),Q(4,5)),(-Q(9,10),Q(4,5)),(-Q(3,2),0),(-Q(9,10),-Q(4,5)),(Q(9,10),-Q(4,5))]),('N6-minor',Q(3,2),sy.Integer(1),Q(9,25),[(0,1),(-3*sy.sqrt(21)/10,Q(2,5)),(-3*sy.sqrt(21)/10,-Q(2,5)),(0,-1),(3*sy.sqrt(21)/10,-Q(2,5)),(3*sy.sqrt(21)/10,Q(2,5))]),('N4-diamond',sy.Integer(2),sy.Integer(1),Q(4,5),[(2,0),(0,1),(-2,0),(0,-1)]),('N4-rectangle',sy.Integer(2),sy.Integer(1),Q(4,5),[(4/sy.sqrt(5),1/sy.sqrt(5)),(-4/sy.sqrt(5),1/sy.sqrt(5)),(-4/sy.sqrt(5),-1/sy.sqrt(5)),(4/sy.sqrt(5),-1/sy.sqrt(5))])]
rows=[];assertions=0
for name,a,b,lam,coords in cases:
 P=[sy.Matrix(v) for v in coords];F=sy.Matrix([sy.sqrt(a*a-b*b),0]);pedal=[];anti=[];N=len(P)
 assert len({tuple(v) for v in P})==N
 residuals=[]
 for i,p in enumerate(P):
  q=P[(i+1)%N];d=q-p;prev=P[(i-1)%N];n=sy.Matrix([p[0]/(a*a),p[1]/(b*b)])
  residuals.append(p[0]**2/(a*a)+p[1]**2/(b*b)-1)
  # Tangency discriminant is exactly zero in the strict caustic equation.
  A=d[0]**2/(a*a-lam)+d[1]**2/(b*b-lam)
  B=2*(p[0]*d[0]/(a*a-lam)+p[1]*d[1]/(b*b-lam))
  C=p[0]**2/(a*a-lam)+p[1]**2/(b*b-lam)-1
  residuals.append(B*B-4*A*C)
  # Reflection computed with independently normalized Cartesian unit vectors.
  incoming=p-prev;incoming=incoming/sy.sqrt(incoming.dot(incoming));outgoing=d/sy.sqrt(d.dot(d))
  reflection=incoming-2*incoming.dot(n)*n/n.dot(n)
  residuals.extend([reflection[j]-outgoing[j] for j in (0,1)])
  foot=p+d*(F-p).dot(d)/d.dot(d);pedal.append(foot)
  residuals.extend([(foot-F).dot(d),cross(foot-p,d)])
  normals=sy.Matrix([(p-F).T,(q-F).T]);rhs=sy.Matrix([(p-F).dot(p),(q-F).dot(q)])
  assert sy.simplify(normals.det())!=0
  vertex=normals.inv()*rhs;anti.append(vertex)
  residuals.extend([(p-F).dot(vertex-p),(q-F).dot(vertex-q)])
 for x in residuals:assert sy.simplify(x)==0
 assertions+=len(residuals)
 pa,aa=area(pedal),area(anti);product=sy.simplify(pa*aa);repeated=sy.simplify(area(pedal*2)*area(anti*2));assert sy.simplify(repeated-4*product)==0
 rows.append({'case':name,'least_period':N,'pedal':str(pa),'antipedal':str(aa),'product':str(product),'listed_twice_product':str(repeated),'exact_residual_count':len(residuals)})
assert rows[0]['product']=='6912/625' and rows[1]['product']=='27783/2500'
assert rows[2]['pedal']=='32/25' and rows[2]['antipedal']=='8' and rows[3]['pedal']=='8/5' and rows[3]['antipedal']=='32/5'
difference=sy.simplify(sy.sympify(rows[0]['listed_twice_product'])-sy.sympify(rows[1]['listed_twice_product']));assert difference==-Q(27,125)
result={'UTC':datetime.now(timezone.utc).isoformat(),'PASS':True,'rows':rows,'exact_residual_count':assertions,'listed12_difference':str(difference),'vertex_source':'Disclosed Root/source-audit coordinates only; no imported checker functions. Own direct inverse normal solve, projection, reflection, tangency-discriminant and shoelace implementation.','limitation':'This independently proves the displayed counterexample and N4 controls; finite controls do not prove the universal theorem.'}
(out/'INDEPENDENT_EXACT_BOUNDARY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
