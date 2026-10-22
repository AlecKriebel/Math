"""Root fresh direct line certificate using previously disclosed exact vertices, no reviewer helper code."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"reproduction_source_adversary/vendor"))
import sympy as s,json,datetime,hashlib
HERE=Path(__file__).resolve().parent
R=s.Rational
a=R(3,2); b=s.Integer(1); lam=R(9,25);F=s.Matrix([s.sqrt(5)/2,0]); count=0

def check(x):
 global count
 assert s.simplify(x)==0,x
 count+=1

def det(x,y):return x[0]*y[1]-x[1]*y[0]
def area(v):return s.simplify(sum(det(v[i],v[(i+1)%len(v)]) for i in range(len(v)))/2)
rows=[]
phases=[('major',[(a,0),(R(9,10),R(4,5)),(-R(9,10),R(4,5)),(-a,0),(-R(9,10),-R(4,5)),(R(9,10),-R(4,5))]),('minor',[(0,1),(-3*s.sqrt(21)/10,R(2,5)),(-3*s.sqrt(21)/10,-R(2,5)),(0,-1),(3*s.sqrt(21)/10,-R(2,5)),(3*s.sqrt(21)/10,R(2,5))])]
for name,coords in phases:
 v=[s.Matrix(p) for p in coords];pedal=[];anti=[]
 assert len(set(tuple(p) for p in v))==6
 for i,p in enumerate(v):
  q=v[(i+1)%6];d=q-p;prev=v[(i-1)%6]
  check(p[0]**2/a**2+p[1]**2/b**2-1)
  A=d[0]**2/(a**2-lam)+d[1]**2/(b**2-lam)
  B=2*(p[0]*d[0]/(a**2-lam)+p[1]*d[1]/(b**2-lam))
  C=p[0]**2/(a**2-lam)+p[1]**2/(b**2-lam)-1
  check(B**2-4*A*C);t=s.simplify(-B/(2*A));assert t>0 and t<1
  u=p-prev;u=u/s.sqrt(u.dot(u));w=d/s.sqrt(d.dot(d));n=s.Matrix([p[0]/a**2,p[1]/b**2])
  reflected=u-2*n*(u.dot(n))/n.dot(n)
  check(det(reflected,w));check(reflected.dot(w)-1)
  pp=p-F;qq=q-F;K=det(pp,qq);assert K!=0
  foot=pp-d*pp.dot(d)/d.dot(d);check(foot.dot(d))
  # Perpendicular foot lies on original side: normal projection formula above gives foot-pp parallel to d.
  check(det(foot-pp,d))
  vertex=s.Matrix([(pp.dot(pp)*qq[1]-qq.dot(qq)*pp[1])/K,(pp[0]*qq.dot(qq)-qq[0]*pp.dot(pp))/K])
  check(pp.dot(vertex)-pp.dot(pp));check(qq.dot(vertex)-qq.dot(qq))
  pedal.append(foot);anti.append(vertex)
 Ap=area(pedal);Aq=area(anti);product=s.simplify(Ap*Aq)
 repeated=s.simplify(area(pedal*2)*area(anti*2));check(repeated-4*product)
 rows.append({'phase':name,'pedal':str(Ap),'antipedal':str(Aq),'primitive_product':str(product),'listed12_product':str(repeated)})
assert rows[0]['listed12_product']=='27648/625' and rows[1]['listed12_product']=='27783/625'
diff=s.simplify(s.sympify(rows[0]['listed12_product'])-s.sympify(rows[1]['listed12_product']));assert diff==-R(27,125)
x={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','assertions':count,'source':'Root independent direct line/reflection/tangency implementation; exact disclosed vertices from reproduction family, no reused helper/source code.','rows':rows,'exact_listed12_difference':str(diff),'interpretation':'Unrestricted traversal-count claim false; primitive N0mod4 theorem unaffected.','sympy_version':s.__version__}
(HERE/'ROOT_EXACT_DOMAIN_CERTIFICATE.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print(json.dumps(x,indent=2))
