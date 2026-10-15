#!/usr/bin/env python3
"""Independent exact geometry diagnostics. These do not certify Bi's analytic theorem."""
import json
import sympy as s
checks=[]
def require(name,condition):
    if condition is not True and condition != s.true:
        raise RuntimeError(f'failed: {name}: {condition!r}')
    checks.append(name)
def zeq(a,b):
    return s.simplify(a-b)==0
x,y,c=s.symbols('x y c',real=True)
F=s.Matrix([x,y+c*x*x]); J=F.jacobian((x,y)); g=s.simplify(J.T*J); gi=g.inv(); D=1+4*c*c*x*x
require('nonlinear shear pullback determinant is one',zeq(g.det(),1))
coords=(x,y)
Gamma=[[[s.simplify(sum(gi[k,l]*(s.diff(g[l,j],coords[i])+s.diff(g[l,i],coords[j])-s.diff(g[i,j],coords[l])) for l in range(2))/2) for j in range(2)] for i in range(2)] for k in range(2)]
require('sole nonzero Christoffel coefficient',all(zeq(Gamma[k][i][j],2*c if (k,i,j)==(1,0,0) else 0) for k in range(2) for i in range(2) for j in range(2)))
R=[]
for k in range(2):
 for l in range(2):
  for i in range(2):
   for j in range(2):
    q=s.diff(Gamma[k][j][l],coords[i])-s.diff(Gamma[k][i][l],coords[j])+sum(Gamma[k][i][m]*Gamma[m][j][l]-Gamma[k][j][m]*Gamma[m][i][l] for m in range(2))
    R.append(s.simplify(q))
require('all nonlinear pullback Riemann components vanish',all(q==0 for q in R))
for sign,label in [(-1,'bottom'),(1,'top')]:
 cov=s.Matrix([0,sign]); nu=s.simplify(gi*cov/s.sqrt((cov.T*gi*cov)[0])); pushed=s.simplify(J*nu)
 expected=s.Matrix([-sign*2*c*x,sign])/s.sqrt(D)
 require(label+' outward normal pushes correctly',all(zeq(a,b) for a,b in zip(pushed,expected)))
 dnu=s.Matrix([s.diff(nu[k],x)+sum(Gamma[k][0][j]*nu[j] for j in range(2)) for k in range(2)])
 H=s.simplify((s.Matrix([1,0]).T*g*dnu)[0]/g[0,0])
 require(label+' curvature pullback has correct sign',zeq(H,-sign*2*c/D**s.Rational(3,2)))
 require(label+' curvature sign at c=x=1',s.sign(H.subs({c:1,x:1}))==-sign)
require('nonlinear flatness alone does not imply all faces mean convex',(-2*c/D**s.Rational(3,2)).subs({c:1,x:1})<0)
# Reflection, shear, anisotropic scale: no ambient orientation assumption is used.
As=[s.Matrix([[2,1,0],[0,3,1],[0,0,4]]),s.Matrix([[-2,1,0],[0,3,1],[0,0,4]]),s.Matrix([[1,1,0],[0,1,1],[1,0,2]])]
Ns=[s.Matrix([1,0,0]),s.Matrix([0,-1,0]),s.Matrix([1,2,-1])]
for ai,A in enumerate(As):
 G=A.T*A; Gi=G.inv()
 require(f'affine {ai} nonsingular',A.det()!=0)
 for ni,N in enumerate(Ns):
  require(f'affine {ai} normal {ni} covector push',A*Gi*N==A.inv().T*N)
  require(f'affine {ai} normal {ni} squared norm',(N.T*Gi*N)[0]==(A.inv().T*N).dot(A.inv().T*N))
  for mi,M in enumerate(Ns):
   require(f'affine {ai} normal Gram {ni},{mi}',zeq((N.T*Gi*M)[0],(A.inv().T*N).dot(A.inv().T*M)))
# Interior/exterior angle comparison and nonacute convention.
ths=[s.pi/3,s.pi/2,2*s.pi/3]
for i,t in enumerate(ths):
 require(f'angle supplementary identity {i}',zeq(s.cos(s.pi-t),-s.cos(t)))
 for j,u in enumerate(ths):
  require(f'angle weak order reversal {i},{j}',bool(t<=u)==bool(s.pi-t>=s.pi-u))
  require(f'angle normal inner product order {i},{j}',bool(t<=u)==bool(s.cos(s.pi-t)<=s.cos(s.pi-u)))
N1=s.Matrix([0,-1]);N2=s.Matrix([-s.sqrt(3)/2,-s.Rational(1,2)])
require('120-degree wedge exterior normal angle is 60',N1.dot(N2)==s.Rational(1,2))
require('unoriented tangent-line acute angle loses interior convention',2*s.pi/3 != s.pi/3)
# Map smooth on cube, inverse smooth only off x=0: metric degenerates there.
Jbad=s.Matrix([x**3,y]).jacobian((x,y));Gbad=Jbad.T*Jbad
require('singular corner map has degenerate metric',Gbad.subs(x,0).det()==0)
require('singular corner map interior metric positive',Gbad.det()==9*x**4)
require('smooth inverse chain rule would fail at corner',Jbad.subs(x,0).rank()==1)
# Two combinatorially identical pentagonal pyramids have no linear equivalence
# of apex tangent cones, even after any incidence-preserving permutation.
V=[(0,0),(2,0),(3,1),(2,3),(0,2)]
W=[(0,0),(2,0),(3,1),(2,3),(-1,2)]
def cross(a,b,c):
 return (b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
for pts,label in [(V,'reference'),(W,'perturbed')]:
 require(label+' pentagon strictly convex',all(cross(pts[i],pts[(i+1)%5],pts[k])>0 for i in range(5) for k in range(5) if k not in (i,(i+1)%5)))
vs=[s.Matrix([*p,1]) for p in V];ws=[s.Matrix([*p,1]) for p in W]
a=s.symbols('a:9');lam=s.symbols('l:5');A=s.Matrix(3,3,a);cone_ranks=[]
for direction in [1,-1]:
 for shift in range(5):
  perm=[(shift+direction*i)%5 for i in range(5)]
  eq=[e for i in range(5) for e in A*vs[i]-lam[i]*ws[perm[i]]]
  M,_=s.linear_eq_to_matrix(eq,a+lam)
  rank=M.rank();cone_ranks.append(rank)
  require(f'no nonsimple cone equivalence direction={direction} shift={shift}',rank==14)
# Product dimension passage: old normal Gram and new right angles.
A=As[0];G=A.T*A;Gp=s.diag(G,s.ones(1));Gpi=Gp.inv()
require('product leaves old inverse metric block unchanged',Gpi[:3,:3]==G.inv())
for i,N in enumerate(Ns):
 old=s.Matrix([*N,0]);end=s.Matrix([0,0,0,1])
 require(f'product old/end normal orthogonality {i}',(old.T*Gpi*end)[0]==0)
# Planar deficit uses one strict corner anywhere, without requiring uniformity.
angles=[s.pi/6,s.pi/3,s.pi/2]
require('reference irregular triangle exterior turn',s.simplify(sum(s.pi-t for t in angles))==2*s.pi)
for i in range(3):
 delta=s.pi/(20+i)
 changed=angles.copy();changed[i]-=delta
 needed=s.simplify(2*s.pi-sum(s.pi-t for t in changed))
 require(f'one strict angle decrease needs negative integrated curvature {i}',needed==-delta)
# Circle/outward-normal curvature versus CCW boundary turning convention.
t=s.symbols('t',real=True)
T=s.Matrix([-s.sin(t),s.cos(t)]);N=s.Matrix([s.cos(t),s.sin(t)])
require('circle outward mean curvature positive',s.simplify(T.dot(s.diff(N,t)))==1)
require('circle signed CCW turning positive',s.simplify(s.det(s.Matrix.hstack(T,s.diff(T,t))))==1)
print(json.dumps({'schema':'pr672-independent-geometry-controls-v1','checks':len(checks),'passed':True,'groups':['nonlinear pullback geometry and hostile non-mean-convex example','orientation-reversing affine normal identities','interior/exterior dihedral signs','degenerate corner differential exclusion','nonsimple cone restriction under all ten combinatorial maps','product old/new angles','one-point planar strictness and signed curvature'],'nonsimple_system_ranks':cone_ranks,'arithmetic':'SymPy exact symbolic and rational algebra','limits':'Finite identities and countermodels only; not certification of the imported analytic theorem.'},indent=2,sort_keys=True))
