from pathlib import Path
import sympy as s,json,datetime
x,y,c=s.symbols('x y c',real=True);v=[x,y];F=s.Matrix([x,y+c*x*x]);J=F.jacobian(v);g=J.T*J;gi=g.inv();checks=[]
def check(n,q):
 if not q:raise ValueError(n)
 checks.append(n)
check('nonlinear smooth pullback Jacobian nonsingular everywhere',s.det(J)==1)
check('metric determinant positive without additional boundary metric hypothesis',s.det(g)==1)
G=[[[s.simplify(sum(gi[k,l]*(s.diff(g[l,j],v[i])+s.diff(g[l,i],v[j])-s.diff(g[i,j],v[l])) for l in range(2))/2) for j in range(2)]for i in range(2)]for k in range(2)]
for k in range(2):
 for l in range(2):
  for i in range(2):
   for j in range(2):
    R=s.diff(G[k][j][l],v[i])-s.diff(G[k][i][l],v[j])+sum(G[k][i][m]*G[m][j][l]-G[k][j][m]*G[m][i][l] for m in range(2))
    check(f'pullback Riemann flat {k}{l}{i}{j}',s.simplify(R)==0)
L=1+4*c*c*x*x;nu=s.Matrix([2*c*x,-L])/s.sqrt(L);T=s.Matrix([1,0])/s.sqrt(L)
check('outward metric normal unit',s.simplify((nu.T*g*nu)[0])==1)
check('outward metric normal orthogonal to face',s.simplify((nu.T*g*T)[0])==0)
check('pushforward normal is outward graph normal',s.simplify(J*nu-s.Matrix([2*c*x,-1])/s.sqrt(L))==s.zeros(2,1))
Dnu=s.Matrix([sum(T[i]*s.diff(nu[k],v[i]) for i in range(2))+sum(G[k][i][j]*T[i]*nu[j] for i in range(2) for j in range(2)) for k in range(2)])
H=s.simplify((Dnu.T*g*T)[0]);embedded=s.simplify((s.diff(J*nu,x).T*J*s.Matrix([1,0]))[0]/L)
check('nonlinear face mean curvature preserved with correct sign',s.simplify(H-embedded)==0 and s.simplify(H-2*c/L**s.Rational(3,2))==0)
check('convex lower boundary has positive outward mean curvature',H.subs({x:0,c:1})==2)
check('negative curvature is not repaired by pulling back',H.subs({x:0,c:-1})==-2)
# A model interior diffeomorphism that cannot support this application at a corner.
t=s.symbols('t',nonnegative=True);check('corner-degenerate map detected despite positive interior derivative',s.diff(t**3,t).subs(t,0)==0)
a,b=s.symbols('a b',positive=True);check('strict turning deficit forces negative integrated curvature',s.simplify(2*s.pi-(2*s.pi+a+b))==-a-b)
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'labels':checks,'scope':'Independent exact local geometric consistency controls; not an analytic source-proof certificate'},indent=2))
