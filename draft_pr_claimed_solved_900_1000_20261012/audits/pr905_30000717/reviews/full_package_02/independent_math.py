"""Fresh exact review controls, derived directly from the manuscript.

This script imports no distributed checker or result. These finite controls
support the universal written proof; they are not an SOS degree search.
"""
import sympy as s
from itertools import product,permutations
import json,sys
checks=[]
def require(ok,label):
 if not bool(ok): raise RuntimeError(label)
 checks.append(label)
x,y,z,t,a,b,c,delta=s.symbols('x y z t a b c delta',real=True)
vars=(x,y,z)
R=sum(v**6 for v in vars)-sum(u**4*v**2 for u,v in permutations(vars,2))+3*x**2*y**2*z**2
F=sum(v**3 for v in (a,b,c))-sum(u**2*v for u,v in permutations((a,b,c),2))+3*a*b*c
require(s.expand(F-(a-b)**2*(a+b-c)-c*(a-c)*(b-c))==0,'Ordered Schur identity')
require(s.expand(F.subs({a:x*x,b:y*y,c:z*z})-R)==0,'Square specialization')
u,v,w=s.symbols('u v w',nonnegative=True)
ordered=s.Poly(s.expand(F.subs({a:w+v+u,b:w+v,c:w})),u,v,w)
require(all(d>0 for d in ordered.coeffs()),'Nonnegative coefficient expansion after order substitution')
for perm in permutations(vars): require(s.expand(R.xreplace(dict(zip(vars,perm)))-R)==0,'Permutation '+str(perm))
Z=[(1,i,j) for i,j in product((-1,1),repeat=2)]+[(1,i,0) for i in (-1,1)]+[(1,0,j) for j in (-1,1)]+[(0,1,j) for j in (-1,1)]
require(len(Z)==len(set(Z))==10,'Ten distinct representatives')
G=[s.diff(R,q) for q in vars]
J=[vars[j]*G[i]-vars[i]*G[j] for i in range(3) for j in range(i+1,3)]
K=[vars[j]*G[i] for i in range(3) for j in range(3) if i!=j]
def line(p,vec):return s.expand(p.subs(dict(zip(vars,[t*q for q in vec]))))
for vec in Z:
 require(line(R,vec)==0,'Whole zero line '+str(vec))
 require(all(line(g,vec)==0 for g in G),'Gradient on zero line '+str(vec))
 require(all(line(g,vec)==0 for g in J+K),'Both ideals on zero line '+str(vec))
for axis in ((1,0,0),(0,1,0),(0,0,1)):
 require(line(R,axis)==t**6,'Sextic trace '+str(axis))
 require(all(line(g,axis)==0 for g in J+K),'Ideal axis '+str(axis))
require(s.expand(sum(q*g for q,g in zip(vars,G))-6*R)==0,'Euler provides gradient-ideal certificate')
monos=lambda d:[x**i*y**j*z**(d-i-j) for i in range(d,-1,-1) for j in range(d-i,-1,-1)]
def evaluation(d):return s.Matrix([[p.subs(dict(zip(vars,vec))) for p in monos(d)] for vec in Z])
ranks=[]
for d in range(5):
 M=evaluation(d);r=M.rank();n=len(monos(d));ranks.append({'degree':d,'rank':r,'dimension':n})
 require(r==min(n,10),'Degree '+str(d)+' exact rank')
M=evaluation(3);det=M.det();require(abs(det)==128,'Cubic evaluation determinant magnitude')
# Independent coefficient extraction validates the four-dimensional intermediate kernel.
P=[x*(x*x-y*y-z*z),y*(y*y-x*x-z*z),z*(z*z-x*x-y*y),x*y*z]
paired=[vec for vec in Z if 0 in vec];full=[vec for vec in Z if 0 not in vec]
A=s.Matrix([[p.subs(dict(zip(vars,vec))) for p in monos(3)] for vec in paired])
require(A.rank()==6,'Six pair directions impose six independent conditions')
C=s.Matrix([[s.Poly(p,*vars).coeff_monomial(q) for p in P] for q in monos(3)])
require(C.rank()==4 and A*C==s.zeros(6,4),'Displayed four cubics form full paired-direction kernel')
H=s.Matrix([[p.subs(dict(zip(vars,vec))) for p in P] for vec in full])
require(H.det()!=0,'Four full-sign constraints kill the paired-direction kernel')
# Failure controls: point samples, degree truncation and ideal substitution are distinct mechanisms.
quartic=(x*x-y*y)*(x*x+y*y-z*z)
require(all(line(quartic,vec)==0 for vec in Z),'Degree-four counterfactual vanishes on entire zero lines')
require(line(quartic,(1,0,0))==t**4,'Degree-four counterfactual has nonzero axis trace')
finite_only=(x-1)*(y-1)
require(all(finite_only.subs(dict(zip(vars,vec)))==0 for vec in Z),'Nonhomogeneous finite-point shortcut passes the representatives')
require(line(finite_only,(1,1,1))==(t-1)**2 or s.expand(line(finite_only,(1,1,1))-(t-1)**2)==0,'Finite-point shortcut fails whole-line constancy')
deleted=[]
for k in range(10):
 N=M.copy();N.row_del(k);ns=N.nullspace()
 require(len(ns)==1,'Omit one zero constraint loses cubic injectivity '+str(k))
 p=s.expand(sum(q*d for q,d in zip(monos(3),ns[0])))
 deleted.append({'omitted_direction':Z[k],'nonzero_kernel_cubic':str(p),'axis_trace':str(line(p,(1,0,0)))})
require(any(rec['axis_trace']!='0' for rec in deleted),'Omitted-line failure can create nonzero axis cubic')
# Constants remain allowed on zero lines; leading coefficient cancellation cannot occur over R.
for D in (1,3,4,17,100):
 q1=3*t**D+2; q2=-4*t**D+5
 require(s.Poly(s.expand(q1*q1+q2*q2),t).LC()==25,'Positive real leading coefficient control '+str(D))
require(s.expand(((R+1)/2)**2+(s.I*(R-1)/2)**2-R)==0,'Complex-square boundary has an explicit counterexample')
# Q's real variety elimination is independent of its tangency-minor reading.
Q=(1-x*y)**2+y*y-s.Rational(1,2); qx=s.diff(Q,x);qy=s.diff(Q,y)
A=y*qx;B=x*qy
require(s.expand(A-2*y*y*(x*y-1))==0,'Q literal first generator')
require(s.expand(B-2*x*(x*(x*y-1)+y))==0,'Q literal second generator')
require(s.expand(B.subs(y,0))==-2*x*x,'Q y=0 branch')
require(s.simplify(B.subs(x,1/y))==2,'Q xy=1 branch impossible')
require(Q.subs({x:0,y:0})==s.Rational(1,2),'Q origin nonnegative')
require(Q.subs({x:2,y:s.Rational(1,2)})==-s.Rational(1,4),'Q global negativity')
require(s.simplify(Q.subs({x:1/t,y:t}))==t*t-s.Rational(1,2),'Q infimum path')
require(s.expand(Q+s.Rational(1,2)-(1-x*y)**2-y*y)==0,'Q global lower bound with incompatible equality constraints')
Qminor=s.expand(y*qx-x*qy)
# An exact algebraic tangency witness: y=x/4, x^2=44/15.
require(s.rem(Qminor.subs(y,x/4),x*x-s.Rational(44,15),x)==0,'Q has negative point on minor variety')
require(s.rem(Q.subs(y,x/4),x*x-s.Rational(44,15),x)==-s.Rational(221,900),'Q minor negative value')
# Semantics mutation controls: coefficient 3->4, missing line, missing minus sign, and wrong ideal all trigger a concrete failed hypothesis.
R4=s.expand(R+x*x*y*y*z*z)
mutations=[{'case':'Robinson coefficient 3 changed to 4','rejected_by':'zero-line identity','witness':str(line(R4,(1,1,1)))},
{'case':'quartic injection silently substituted for cubic injection','rejected_by':'rank 10 versus dimension 15','witness':str(quartic)},
{'case':'finite points silently substituted for whole zero lines','rejected_by':'nonconstant restriction','witness':str(line(finite_only,(1,1,1)))},
{'case':'replace tangency ideal by gradient ideal','rejected_by':'axis no longer lies in variety; certificate R in gradient ideal exists','witness':str(line(G[0],(1,0,0)))},
{'case':'allow complex rather than real square coefficients','rejected_by':'leading-term positivity fails','witness':'((R+1)/2)^2+(i(R-1)/2)^2=R'}]
require(line(R4,(1,1,1))==t**6,'Changed-coefficient mutation detected')
# The axis failure remains exact for all constant epsilon; eps<0 would already fail at origin.
result={'verdict':'PASS_FRESH_EXACT_CONTROLS','sympy':s.__version__,'check_count':len(checks),'checks':checks,'degree_ranks':ranks,'review_ordered_cubic_determinant':str(det),'ordered_nonnegative_expansion':str(ordered.as_expr()),'omitted_direction_controls':deleted,'semantic_mutations':mutations,'scope':'Finite controls support the separately reconstructed universal real-polynomial proof; no global degree cutoff or numerical optimization is used.'}
print(json.dumps(result,indent=2))
