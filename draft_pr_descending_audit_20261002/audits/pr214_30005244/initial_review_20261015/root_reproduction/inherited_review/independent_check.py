"""Independent review controls, written without importing the author checker.
These check exact identities and finite-dimensional analogues, not infinite limits.
"""
from itertools import permutations,product
from fractions import Fraction
import json
import sympy as s
import numpy as np
exact=0
x,y,z,k,r=s.symbols('x y z k r',real=True,nonzero=True)
rho=s.sqrt(x*x+y*y+z*z)
g=s.exp(s.I*k*rho)/(4*s.pi*rho)
# Differentiate in Cartesian coordinates, then restrict to a positive x-axis.
# At the axis the radial and transverse eigenvalues recover the full tensor.
for i,q in enumerate((x,y,z)):
 val=s.diff(g,q,2).subs({x:r,y:0,z:0}).subs(s.Abs(r),r)
 if i==0: target=s.exp(s.I*k*r)*(2-2*s.I*k*r-k*k*r*r)/(4*s.pi*r**3)
 else: target=s.exp(s.I*k*r)*(s.I*k*r-1)/(4*s.pi*r**3)
 # Sympy differentiates assuming positive r for the square root restriction.
 assert s.simplify(val-target)==0,(val,target);exact+=1
# Radial and transverse dynamic corrections after subtracting the static part.
t=s.symbols('t')
radial=2*s.exp(s.I*t)*(s.I*t-1)+2
transverse=s.exp(s.I*t)*(1-s.I*t-t*t)-1
assert s.series(radial,t,0,4).removeO()==-t*t-2*s.I*t**3/3;exact+=1
assert s.series(transverse,t,0,4).removeO()==-t*t/2-2*s.I*t**3/3;exact+=1
# Distributional delta coefficient: isotropy plus trace fixes I/3.
d=s.symbols('d');assert s.solve(3*d-1,d)==[s.Rational(1,3)];exact+=1
# Fourier symbol projection minus I/3 at several exact rational directions.
for v in ((1,0,0),(1,1,0),(1,2,3),(-2,3,7),(0,5,-1)):
 u=s.Matrix(v);P=u*u.T/(u.dot(u));B=P-s.eye(3)/3
 assert P*P==P;exact+=9
 assert s.simplify(B.charpoly().as_expr()-(s.Symbol('lambda')-s.Rational(2,3))*(s.Symbol('lambda')+s.Rational(1,3))**2)==0;exact+=1
# Cancellation on complete cubic group orbits, using rational numerator matrices.
for v in product(range(4),repeat=3):
 if v==(0,0,0):continue
 orb={tuple(e[j]*p[j] for j in range(3)) for p in permutations(v) for e in product((-1,1),repeat=3)}
 ans=[[Fraction(0) for _ in range(3)] for _ in range(3)]
 for w in orb:
  r2=sum(t*t for t in w)
  for i in range(3):
   for j in range(3):ans[i][j]+=Fraction((r2 if i==j else 0)-3*w[i]*w[j],r2)
 assert all(entry==0 for row in ans for entry in row);exact+=9
# Radial integrability exponents: near static subtraction is O(delta),
# square dynamic correction is also O(delta), far static square O(R^-3).
q=s.symbols('q',positive=True)
for power,primitive in ((0,q),(-4,-1/(3*q**3))):
 assert s.simplify(s.diff(primitive,q)-q**power)==0;exact+=1
# Nonnormal compact perturbation control: defective eigenvalue, moving projection,
# static spike with nonvanishing norm and strong limit zero in increasing spaces.
controls=[]
for n in (8,16,32,64):
 size=n+3;theta=1/n;U=np.eye(size);a=0;b=size-1
 U[a,a]=U[b,b]=np.cos(theta);U[a,b]=-np.sin(theta);U[b,a]=np.sin(theta)
 C=np.zeros((size,size),dtype=complex);lam=2+1j
 C[0,0]=C[1,1]=lam;C[0,1]=1
 B=np.zeros_like(C);B[-1,-1]=.5
 Sh=U@(B+C)@U.T
 Ph=U@np.diag([1,1]+[0]*(size-2))@U.T
 P=np.diag([1,1]+[0]*(size-2))
 assert np.linalg.norm(Ph@Ph-Ph)<1e-13
 assert np.linalg.norm(Sh@Ph-Ph@Sh)<1e-13
 vals=np.linalg.eigvals(Sh)
 assert sum(abs(z-lam)<1e-7 for z in vals)==2
 err=np.linalg.norm(Ph-P,2)
 assert abs(err-np.sin(theta))<1e-13
 assert abs(np.trace(Ph)-2)<1e-13
 # The invariant two-dimensional restriction is a genuine Jordan block.
 Q=U[:,:2];small=Q.T@Sh@Q
 assert np.linalg.norm(small-C[:2,:2])<1e-13
 controls.append({'dimension':size,'static_norm':float(np.linalg.norm(B,2)),'projection_error':float(err),'algebraic_multiplicity':2})
print(json.dumps({'status':'PASS','exact_assertions':exact,'defective_eigenvalue_controls':controls,'limitations':'Independent algebra, summation symmetry, integrability exponents, and finite-dimensional defective-eigenvalue controls; the infinite-dimensional convergence assertions require the reviewed analytical proof.'},indent=2))
