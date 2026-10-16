from pathlib import Path
import json,hashlib,ast,dis,types,sys
from datetime import datetime,timezone
import sympy as s
HERE=Path(__file__).resolve().parent;P=HERE.parent/'publication_package_v1';M=P/'materials';checks=[]
def need(b,name):
 if b is not True and b is not s.true:raise RuntimeError(name+': '+str(b))
 checks.append(name)
def eq(a,b,n):need(s.simplify(a-b)==0,n)
def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def area(P):return s.simplify(sum(cross(a,b) for a,b in zip(P,P[1:]+P[:1]))/2)
def feet(P,m):
 q=[]
 for a,b in zip(P,P[1:]+P[:1]):
  d=b-a;q.append(a+d*((m-a).dot(d)/d.dot(d)))
 return q
# Homogeneous endpoint formula: enforce only cover and dual-caustic relations.
a,b,u,v,w,l,e=s.symbols('a b u v w l e',nonzero=True)
H=a*a*u*u+b*b*v*v;D=u*u+v*v
X=-a*a*u*w-v*e;Y=-b*b*v*w+u*e
subs={e*e:a*a*b*b*l*D,w*w:H-l*D}
eq(u*X+v*Y+w*H,0,'homogeneous incidence')
eq(s.expand(X*X/a**2+Y*Y/b**2-H*H).subs(subs),0,'cover on outer conic')
# Independent direct side-vector projections for the three published controls.
R=s.Rational
H6=list(map(s.Matrix,[(2,0),(R(4,3),s.sqrt(5)/3),(-R(4,3),s.sqrt(5)/3),(-2,0),(-R(4,3),-s.sqrt(5)/3),(R(4,3),-s.sqrt(5)/3)]))
J6=list(map(s.Matrix,[(0,1),(-4*s.sqrt(2)/3,R(1,3)),(-4*s.sqrt(2)/3,-R(1,3)),(0,-1),(4*s.sqrt(2)/3,-R(1,3)),(4*s.sqrt(2)/3,R(1,3))]))
products=[]
for label,P6 in [('H',H6),('J',J6)]:
 q=feet(P6,s.zeros(2,1));products.append(area(P6)*area(q))
 eq(area(P6*2)*area(feet(P6*2,s.zeros(2,1))),4*area(P6)*area(q),label+' doubled lists scale by four')
 for k,(p,q) in enumerate(zip(P6,P6[1:]+P6[:1])):
  n=s.Matrix([p[1]-q[1],q[0]-p[0]]);h=-n.dot(p)
  eq(h*h-R(32,9)*n[0]**2-R(5,9)*n[1]**2,0,label+' tangent '+str(k))
eq(products[0],R(14000,729),'H6 exact product');eq(products[1],R(14336,729),'J6 exact product')
eq(4*(products[1]-products[0]),R(448,243),'nominal twelve counterexample')
a8=4*s.sqrt(2);b8=3*s.sqrt(3)
W=list(map(s.Matrix,[(a8,0),(4*a8/5,3*b8/5),(0,b8),(-4*a8/5,3*b8/5),(-a8,0),(-4*a8/5,-3*b8/5),(0,-b8),(4*a8/5,-3*b8/5)]))
Z=[W[(3*j)%8] for j in range(8)]
xx,yy=s.symbols('x y',real=True)
B=area(feet(Z,s.Matrix([xx,yy])))
eq(area(Z),168*s.sqrt(6)/5,'star original area')
eq(B,96*s.sqrt(6)/245*(13-xx*xx-yy*yy),'star all-M polynomial')
eq(B.subs({xx:s.sqrt(13),yy:0}),0,'star zero signed area')
need(B.subs({xx:4,yy:0}).is_negative is True,'star negative signed area')
# Branch grouping is a formal order calculation, including N4 shared neighbors.
t=s.symbols('t');A=s.Matrix(s.symbols('A:2'));C=s.Matrix(s.symbols('C:2'));V=s.Matrix(s.symbols('V:2'));F=s.Matrix(s.symbols('F:2'))
expr=s.expand(cross(A/t**2+C,t*V+t**3*F))
for k in [-4,-3,-2]:eq(expr.coeff(t,k),0,'even-double/odd cancellation '+str(k))
for n in range(4,101,4):
 m=n//2
 need([j for j in range(n) if (2*j)%n==0]==[0,m],'singular indices '+str(n))
 need({n-1,0}.isdisjoint({m-1,m}),'grouped edges disjoint '+str(n))
 need(all((2*j-m+1)%n for j in range(n)),'S/R separated '+str(n))
for n in range(6,101,4):
 m=n//2;need(any((2*j-m+1)%n==0 for j in range(n)),'S/R intersects outside parity '+str(n))
# Compile original complete scripts at both optimization levels; all assertion
# opcodes are counted recursively, and their actual unchanged check wrappers
# are exercised on a false mathematical identity. This does not replay broad diagnostics.
legacy=[]
def ops(c):
 return sum(i.opname=='LOAD_ASSERTION_ERROR' or (i.opname=='LOAD_COMMON_CONSTANT' and i.argrepr=='AssertionError') for i in dis.get_instructions(c))+sum(ops(x) for x in c.co_consts if isinstance(x,types.CodeType))
for rel,name in [('verify.py','ck'),('independent_review/independent_checks.py','check')]:
 p=M/'audit/original_submitted_head'/rel;raw=p.read_text();tree=ast.parse(raw)
 wrapper=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name==name)
 outcomes=[]
 for opt in [0,1]:
  c=compile(raw,str(p),'exec',optimize=opt);sites=ops(c)
  ns={'C':__import__('collections').Counter()}
  exec(compile(ast.Module(body=[wrapper],type_ignores=[]),str(p),'exec',optimize=opt),ns)
  try:ns[name]('actual false area identity',R(128,25)==R(129,25));rejected=False
  except AssertionError:rejected=True
  need(rejected==(opt==0),'legacy wrapper actual false rejection '+rel+' '+str(opt))
  need((sites>0)==(opt==0),'all assertion opcode removal '+rel+' '+str(opt))
  outcomes.append({'optimization':opt,'recursive_assertion_opcode_sites':sites,'actual_false_identity_rejected':rejected,'advertised_count_after_false_call':sum(ns['C'].values())})
 legacy.append({'path':rel,'sha256':hashlib.sha256(raw.encode()).hexdigest(),'outcomes':outcomes})
report={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','optimization':sys.flags.optimize,'exact_checks':len(checks),'labels':checks,'legacy_enforcement_scope':'complete-source recursive bytecode inventory plus unchanged check wrapper on exact false 128/25=129/25; broad legacy replay not repeated','legacy':legacy}
(HERE/('INDEPENDENT_EXACT_OPT.json' if sys.flags.optimize else 'INDEPENDENT_EXACT.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['labels','legacy']}))
