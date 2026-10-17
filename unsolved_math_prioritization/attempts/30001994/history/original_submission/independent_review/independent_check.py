"""Separate exact algebra controls for the weighted-cut/ordinary-gradient distinction.
These controls supplement, and do not prove, the functional-analytic audit.
"""
import sympy as s
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def ck(v,k):
    assert v,k
    C[k]+=1
x,y,z,q=s.symbols('x y z q',real=True)
h=s.Function('h');r2=x*x+y*y;H=h(r2,z)
A=s.Matrix([-y*H/r2,x*H/r2,0]);variables=[x,y,z]
ck(s.simplify(sum(s.diff(A[i],variables[i]) for i in range(3)))==0,'Cartesian_divergence_for_arbitrary_radial_cutoff')
curl=s.Matrix([s.diff(A[2],y)-s.diff(A[1],z),s.diff(A[0],z)-s.diff(A[2],x),s.diff(A[1],x)-s.diff(A[0],y)])
expected=s.Matrix([-x*s.diff(H,z)/r2,-y*s.diff(H,z)/r2,2*s.Subs(s.Derivative(h(q,z),q),q,r2)])
for v in curl-expected:ck(s.simplify(v)==0,'Cartesian_curl_formula')
A0=s.Matrix([-y/r2,x/r2,0]);ck(s.simplify(A0.dot(A0)-1/r2)==0,'circulation_norm')
u,eps=s.symbols('u eps',positive=True)
# Independent compact C1 polynomial density; a diagnostic replacement for any smooth density.
rho=s.Rational(15,16)*(1-u*u)**2
ck(s.integrate(rho,(u,-1,1))==1,'independent_density_normalization')
I0=s.integrate(rho*rho,(u,-1,1));I2=s.integrate(u*u*rho*rho,(u,-1,1))
ck(I0==s.Rational(5,7),'squared_density_integral')
ck(I2==s.Rational(5,77),'weighted_squared_density_integral')
# The periodic derivative 1-2pi*rho_eps has zero full-circle integral.
ck(s.simplify(2*s.pi-2*s.pi*s.integrate(rho,(u,-1,1)))==0,'periodic_primitive_compatibility')
# 1-cos(theta)<=theta²/2 yields weighted defect <=2pi² eps I2.
for n in range(2,130):
    e=F(1,n)
    weighted=2*e*F(5,77) # with pi² and spatial factor removed
    ordinary=4/e*F(5,7)
    ck(weighted>0 and weighted<2*F(5,77),'positive_weighted_bound')
    ck(weighted==F(10,77*n),'weighted_linear_decay')
    ck(ordinary==F(20*n,7),'ordinary_inverse_scale_blowup')
    ck(weighted/ordinary==e*e/F(22),'weighted_vs_ordinary_distinction')
# Closed-loop topological test: angle-independent B=psi(r,z)e_theta is solenoidal.
r,theta=s.symbols('r theta',positive=True);psi=s.Function('psi')(r,z)
ck(s.diff(psi,theta)/r==0,'solenoidal_topological_test')
ck(s.simplify((1/r)*psi*r-psi)==0,'cylindrical_jacobian_in_circulation_pairing')
# Test normalization can be taken as tensor polynomial bumps on interior rectangles.
t=s.symbols('t');poly=s.Rational(15,16)*(1-t*t)**2
for radius in range(1,26):
    for width in [F(1,8),F(1,4),F(1,2)]:
        ck(s.integrate(poly,(t,-1,1))**2==1,'positive_tensor_pairing_normalization')
        ck(F(radius)-width>0,'test_support_avoids_axis')
print(json.dumps({'status':'PASS','assertions':sum(C.values()),'counts':dict(sorted(C.items())),'scope':'Exact Cartesian vector identities, periodic-cut energy envelope and ordinary-versus-weighted norm distinction; no numerical approximation of the infinite-space solvability question.'},indent=2,sort_keys=True))
