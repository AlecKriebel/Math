"""Independent exact local diagnostics; they do not prove ET or Gray stability."""
import sympy as S
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
checks={}
def ck(k,v):
 assert bool(v),k
 checks[k]=checks.get(k,0)+1
x,y,z,s,t,e=S.symbols('x y z s t e',real=True)
coords=(x,y,z)
def curl(v):return S.Matrix([S.diff(v[2],y)-S.diff(v[1],z),S.diff(v[0],z)-S.diff(v[2],x),S.diff(v[1],x)-S.diff(v[0],y)])
def eq(a,b):return all(S.simplify(v)==0 for v in a-b)
# A genuine coordinate solution to d alpha=alpha wedge omega, not a formal coframe.
a=S.exp(-z)*S.Matrix([1,-x*x/2,0]);w=S.Matrix([0,-x,1])
ck('coordinate_connection',eq(curl(a),a.cross(w)))
ck('integrability',S.simplify(a.dot(curl(a)))==0)
ck('differentiated_connection',S.simplify(a.dot(curl(w)))==0)
ck('contact_pencil',S.simplify((w+s*a).dot(curl(w+s*a)))==-1)
ck('normalized_pencil',S.simplify((a+t*w).dot(curl(a+t*w)))==-t*t)
# Arbitrary pointwise jets with the differentiated constraint built in.
a0,a1,a2,w0,w1,w2,g0,g1,g2=S.symbols('a0 a1 a2 w0 w1 w2 g0 g1 g2')
A=S.Matrix([a0,a1,a2]);W=S.Matrix([w0,w1,w2]);G=S.Matrix([g0,g1,g2]);C=A.cross(G)
ck('arbitrary_jets',S.expand((W+s*A).dot(C+s*A.cross(W))-W.dot(C))==0)
# Opposite convention d alpha=omega wedge alpha has the same constant-pencil fact.
ck('opposite_connection_convention',S.expand((W+s*A).dot(C-s*A.cross(W))-W.dot(C))==0)
# Variable shifts have exactly the gradient correction, so constancy matters.
h=x+y*z;beta=w+h*a
ck('variable_shift_remainder',S.simplify(beta.dot(curl(beta))-w.dot(curl(w))-w.dot(S.Matrix([S.diff(h,q) for q in coords]).cross(a)))==0)
# A periodic Legendrian graph in the local solid-torus chart; not a global OT disk.
# theta=dv-u dt; base graph (u,v)=(cos t,sin t).
u,v=S.symbols('u v',real=True)
U=S.cos(t)+e*S.sin(2*t);V=S.sin(t)+e*S.cos(3*t)
eta=S.Matrix([-u+e*(u*v+S.cos(t)),e*(u+S.sin(t)),1+e*(v+S.cos(t))])
pull=lambda form:S.expand(form[0].subs({u:U,v:V},simultaneous=True)+form[1].subs({u:U,v:V},simultaneous=True)*S.diff(U,t)+form[2].subs({u:U,v:V},simultaneous=True)*S.diff(V,t))
q=pull(eta);chi=(1-(u-U)**2-(v-V)**2)**3
corrected=eta-S.Matrix([q*chi,0,0])
ck('moving_graph_annihilation',S.simplify(pull(corrected))==0)
ck('moving_graph_derivative',S.simplify(S.diff(pull(corrected),t))==0)
ck('q_C0_limit',S.simplify(q.subs(e,0))==0)
ck('q_C1_limit',S.simplify(S.diff(q,t).subs(e,0))==0)
base=S.Matrix([-u,0,1])
for i in range(3):
 err=corrected[i]-base[i]
 ck('corrected_C0_limit',S.simplify(err.subs(e,0))==0)
 for c in (t,u,v):ck('corrected_C1_limit',S.simplify(S.diff(err,c).subs(e,0))==0)
ck('boundary_transverse_vector',corrected[2].subs(e,0)==1)
# Uniform contact margin: only a finite closed s-interval is needed.
for B in (F(1,8),F(1),F(4),F(100)):
 for c in (F(1,100),F(1),F(7),F(1000)):
  delta=min(F(1),c/(8*(B+1)))
  ck('uniform_wedge_margin',2*B*delta+delta*delta<c/2)
  for endpoint in (F(0),F(1),F(17)):
   err=delta/(1+endpoint)
   ck('finite_interval_error',err+endpoint*err==delta)
root=Path(__file__).resolve().parent
result={'status':'PASS','assertions':sum(checks.values()),'checks':checks,'candidate_sha256':hashlib.sha256((root/'author_replay/CANDIDATE.md').read_bytes()).hexdigest(),'scope':'Coordinate and general-jet contact pencil; periodic moving-boundary correction and first derivatives; uniform finite-interval margin. These controls do not prove global taut-neighborhood tightness or Gray stability.'}
(root/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
