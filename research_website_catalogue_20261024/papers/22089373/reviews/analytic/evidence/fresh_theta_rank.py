from fresh_graph_fourier import *
from datetime import datetime,timezone
import sympy as sp
from sympy.polys.matrices import DomainMatrix
P,s,Q,t,R,u,v,S=sp.symbols('P s Q t R u v S');h=sp.Rational(1,2)
# Effective root edge AC is the product of the two root arcs; choose the algebraic split 1*1/2.
xs=[1,h,v,h,u,s,h,t,S,P,R,Q]
qt=[sp.expand(coordinate(theta,labels,tuple(map(int,g)),xs,[h,h])) for g in orbits[:8]]
D=DomainMatrix.from_Matrix(sp.Matrix(qt).jacobian([P,s,Q,t,R,u,v,S])).det().as_expr()
expected=-P**3*s**3*Q**4*t*R**4*u**3*v*S**3*(s-1)**2*(v-1)*(v+1)**2/16384
assert sp.expand(D-expected)==0
print('source generic 8-minor exact',flush=True)
x,y,z,w=sp.symbols('x y z w');xt=[1,h,z,h,w,x,y,h,Q,P,R,S];pm={f'L{i}':j for i,j in enumerate([3,1,2,0])}
qt2=[sp.expand(coordinate(theta,pm,tuple(map(int,g)),xt,[h,h])) for g in orbits[:8]]
D2=DomainMatrix.from_Matrix(sp.Matrix(qt2).jacobian([P,x,y,z,R,w,S,Q])).det().as_expr()
expected2=-P**3*x**2*y**2*z*R**4*w**4*S**3*Q**4*(x-1)**2*(z-1)*(z+1)**3/32768
assert sp.expand(D2-expected2)==0
print('target generic 8-minor exact',flush=True)
# Cherry inverse evaluated at a distinct positive point, without submitted helper functions.
u0=F(2,7);v0=F(4,9)
def old(g):return coordinate(omega,labels,g,src[:12],src[12:])
def cherry(gx,a,b):return old(tuple(gx)+(a^b,))*(u0 if a else 1)*(v0 if b else 1)
uv=cherry((0,0,0),1,1);ratio=cherry((1,0,0),1,0)/cherry((1,0,0),0,1)
assert uv*ratio==u0*u0 and uv/ratio==v0*v0
for gx in product(range(4),repeat=3):
 for a,b in product(range(4),repeat=2):
  assert cherry(gx,a,b)/(u0 if a else 1)/(v0 if b else 1)==old(tuple(gx)+(a^b,))
assert sp.expand(expected.subs(v,1))==0 and sp.expand(expected2.subs(x,1))==0
Path(__file__).with_name('fresh-theta-rank.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','source_generic_rank8_minor':str(sp.factor(D)),'target_generic_rank8_minor':str(sp.factor(D2)),'cherry_forward_inverse_assignments':1024,'boundary_zero_minors':2,'gauge_note':'An effective root-edge product is used for symbolic determinants; 1*1/2 is an algebraic split, not a claimed strict physical witness.'},indent=2)+'\n')
