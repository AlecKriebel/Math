"""Exact algebra checks supporting the research note; not a global proof checker."""
import json
import sympy as s
checks = {}
# Attempt 2: derivative of the square of the canonical nilpotent block.
N=s.Matrix([[0,1,0],[0,0,1],[0,0,0]])
G=s.Matrix([[0,0,1],[0,1,0],[1,0,0]])
a,b,c,f=s.symbols('a b c f')
X=s.Matrix([a,b,c]); e1=s.Matrix([1,0,0]); e2=s.Matrix([0,1,0])
dl=s.Matrix([[0,0,f]])
dN=s.Rational(3,2)*(X*dl+f*e1*(X.T*G))-f*c*s.eye(3)
expected=3*f*b*(e1*e1.T*G)-f*c*s.Rational(1,2)*(e2*e1.T*G+e1*e2.T*G)
assert s.simplify(dN*N+N*dN-expected)==s.zeros(3)
checks['jordan_square_derivative']=True
# Uniqueness of simultaneous canonical frames: P commutes with N and is an isometry.
p0,p1,p2=s.symbols('p0 p1 p2')
P=p0*s.eye(3)+p1*N+p2*N**2
assert P.T*G==G*P
assert s.expand(P**2)==p0**2*s.eye(3)+2*p0*p1*N+(p1**2+2*p0*p2)*N**2
checks['canonical_frame_centralizer']=True
# Attempt 5: round-metric flip and its angular determinant.
u,k,z=s.symbols('u k z', real=True)
D=s.diag(u,1-u);v=s.Matrix([u,1-u]);O=D-2*k**2*(v*v.T)
assert s.factor(O.det()-u*(1-u)*(1-2*k**2))==0
H=s.diag(1,u,1-u);Tflat=s.Matrix([z,k*u,k*(1-u)])
full=H-2*Tflat*Tflat.T
assert s.factor(full.det()-u*(1-u)*(1-2*(z**2+k**2)))==0
checks['torus_and_ambient_determinants']=True
# The unit relation z^2+k^2=1 gives det(full)=-det(H).
# Local compatible pair, including nilpotent collisions.
t,x,y=s.symbols('t x y');coords=[t,x,y];eta=s.diag(-1,1,1)
p=s.Matrix(coords);pf=p.T*eta;q=(pf*p)[0]
A=p*pf;L=s.eye(3)+A
assert s.simplify(A*A-q*A)==s.zeros(3)
assert s.factor(L.det()-(1+q))==0
for i,xi in enumerate(coords):
 e=s.eye(3)[:,i]
 assert s.simplify(L.diff(xi)-(e*pf+p*(e.T*eta)))==s.zeros(3)
bar=(eta-(eta*p)*(pf)/(1+q))/(1+q)
assert s.simplify(bar-eta*L.inv()/(1+q))==s.zeros(3)
checks['local_transition_compatibility']=True
print(json.dumps({'all_passed':all(checks.values()),'checks':checks},indent=2))
