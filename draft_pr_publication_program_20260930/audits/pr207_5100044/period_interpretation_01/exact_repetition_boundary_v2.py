"""Exact nonprimitive boundary for the displayed-N reading of arXiv k804,a."""
import sys
from pathlib import Path
import datetime,hashlib,json,os
import sympy as s
R=s.Rational
root=Path(__file__).resolve().parent
def need(x,message):
 if x is not True:raise RuntimeError(message)
def zero(x,message):need(s.simplify(x)==0,message)
def dot(p,q):return sum(x*y for x,y in zip(p,q))
def det(p,q):return p[0]*q[1]-p[1]*q[0]
def minus(p,q):return tuple(x-y for x,y in zip(p,q))
def area(p):return s.simplify(sum(det(p[i],p[(i+1)%len(p)]) for i in range(len(p)))/2)
def unit(v):
 n=s.sqrt(dot(v,v));return tuple(s.simplify(x/n) for x in v)
focus=(s.sqrt(3),s.Integer(0))
P=[(2*s.sqrt(2),s.Integer(0)),(-4*s.sqrt(2)/3,R(5,3)),(-4*s.sqrt(2)/3,-R(5,3))]
M=[tuple(-x for x in p) for p in P]
alpha2=R(32,9);beta2=R(5,9);A=s.Integer(8);B=s.Integer(5)
zero(alpha2-beta2-(A-B),'Confocality')
need(bool(0<beta2<B and 0<alpha2<A),'Strictly nested nondegenerate elliptical caustic')
for p in P:zero(p[0]**2/A+p[1]**2/B-1,'Outer ellipse')
for i,p in enumerate(P):
 prev=P[(i-1)%3];nxt=P[(i+1)%3]
 incoming=unit(minus(p,prev));outgoing=unit(minus(nxt,p));normal=(p[0]/A,p[1]/B)
 reflected=tuple(s.simplify(incoming[j]-2*dot(incoming,normal)*normal[j]/dot(normal,normal)) for j in range(2))
 for x,y in zip(reflected,outgoing):zero(x-y,'Exact specular reflection')
 edge=minus(nxt,p);line=(-edge[1],edge[0]);constant=dot(line,p)
 zero(alpha2*line[0]**2+beta2*line[1]**2-constant**2,'Each side tangent to same caustic')
need(len(set(P))==3,'Least vertex period3')
def invert(poly):
 out=[]
 for p in poly:
  v=minus(p,focus);d=dot(v,v);need(s.simplify(d).is_positive is True,'Positive Euclidean inversion denominator')
  out.append(tuple(s.simplify(x/d) for x in v))
 return out
ap=area(P);am=area(M);ip=area(invert(P));im=area(invert(M))
zero(am-ap,'Central reflection preserves signed orbit area')
productP=s.radsimp(ap*ip);productM=s.radsimp(am*im)
difference=s.radsimp(productP-productM)
need(difference.is_zero is False,'Distinct exact three-period area products')
repeatP=P*4;repeatM=M*4
zero(area(repeatP)-4*ap,'Four traversals scale area by4')
zero(area(invert(repeatP))-4*ip,'Four traversals scale inverse area by4')
zero(area(repeatM)*area(invert(repeatM))-16*productM,'Negative triangle traversal scaling')
zero(area(repeatP)*area(invert(repeatP))-16*productP,'Triangle traversal scaling')
r={'schema':'pr207-exact-repetition-boundary-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_pin':{'bytes':len(Path(__file__).read_bytes()),'sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'outer_ellipse':'x^2/8+y^2/5=1','caustic':'x^2/(32/9)+y^2/(5/9)=1','focus_plus':'(sqrt(3),0)','oriented_triangle':[list(map(str,p)) for p in P],'second_triangle':'Central reflection -P in the same forward3-periodic confocal family','exact_specular_and_tangency_identities_verified':True,'least_period':3,'signed_triangle_area':str(ap),'inverse_area_P':str(s.radsimp(ip)),'inverse_area_minusP':str(s.radsimp(im)),'three_period_product_P':str(productP),'three_period_product_minusP':str(productM),'three_period_product_difference':str(difference),'traversals':4,'displayed_length':12,'displayed_length_mod4':0,'twelve_vertex_product_P':str(s.radsimp(16*productP)),'twelve_vertex_product_minusP':str(s.radsimp(16*productM)),'twelve_vertex_product_difference':str(s.radsimp(16*difference)),'evidence_limit':'Exact counterexample only to the reading allowing repeated shorter cycles to count as displayedN-periodic polygons. Does not contradict the separately verified theorem requiring least period divisible4. Periodic orbits are in one connected forward confocal family by the standard caustic parametrization; central reflection is its real phase shift.','SymPy':s.__version__}
raw=(json.dumps(r,sort_keys=True,indent=2)+'\n').encode()
with (root/'EXACT_BOUNDARY_RESULT.json').open('xb') as f:f.write(raw);f.flush();os.fchmod(f.fileno(),0o444);os.fsync(f.fileno())
print(json.dumps({k:r[k] for k in ('status','three_period_product_P','three_period_product_minusP','three_period_product_difference','twelve_vertex_product_difference','least_period','displayed_length')},sort_keys=True))

