#!/usr/bin/env python3
"""Independent exact algebra and quantitative checks for the tangent-locus audit.
Not a test of the whole geometric proof. Requires SymPy (tested 1.14.0).
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import sympy as s

checks=[]
def check(name,statement):
    assert statement,name
    checks.append(name)

z,z1,z2,z3=s.symbols('z z1 z2 z3')
a,b,c,d,e,f,g,h=s.symbols('a b c d e f g h')
A=s.Matrix([[a,b],[c,d]]);B=s.Matrix([[e,f],[g,h]])
poly=s.expand((A+z*B).det())
check('rank_pencil_is_quadratic',s.Poly(poly,z).degree()<=2)
V=s.Matrix([[1,z1,z1*z1],[1,z2,z2*z2],[1,z3,z3*z3]])
check('distinct_contact_vandermonde',s.simplify(V.det()-(z2-z1)*(z3-z1)*(z3-z2))==0)
v1,v2=s.symbols('v1 v2')
DG=s.Matrix([[a+z*e,b+z*f,v1],[c+z*g,d+z*h,v2],[0,0,1]])
check('swept_jacobian',s.expand(DG.det()-poly)==0)

# Two contacts do not force a null sweep. This catches an invalid degree-one shortcut.
AA=s.diag(1,0);BB=s.diag(-1,1)
p=s.expand((AA+z*BB).det())
check('two_contact_negative_control',p.subs(z,0)==0 and p.subs(z,1)==0 and p.subs(z,2)!=0)

# Check the moving line / fixed plane derivative without invoking the candidate's formula.
t=s.symbols('t');Nx,Ny,Nz,s0=s.symbols('Nx Ny Nz s0',nonzero=True)
U1,U2,V1,V2=s.symbols('U1 U2 V1 V2')
height=(Nz*s0-t*(Nx*U1+Ny*U2))/(Nz+t*(Nx*V1+Ny*V2))
der=s.diff(height,t).subs(t,0)
check('plane_intersection_derivative',s.simplify(der+(Nx*(U1+s0*V1)+Ny*(U2+s0*V2))/Nz)==0)

# Exact cap margins for narrow as well as wide normal cones.
alphas=[F(1),F(1,2),F(1,7),F(1,100),F(1,10000)]
for aa,bb in product(alphas,repeat=2):
    eps=min(F(1,8),aa/32,bb/32)
    check(f'cap_margins_{aa}_{bb}',(1-eps)*aa/2>=aa/4 and (1-eps)*bb/2>=bb/4 and eps/(aa/4)<F(1,4) and eps/(bb/4)<F(1,4))

# Independently verify the max-support increment bound for nonsmooth polyhedral sets.
normals=[(F(1),F(0)),(F(-1),F(0)),(F(0),F(1)),(F(0),F(-1)),(F(3,5),F(4,5)),(F(-3,5),F(4,5))]
C=[(F(0),F(0),F(0)),(F(-1),F(0),F(1,10)),(F(0),F(-2),F(-1,10)),(F(-1),F(-1),F(1,20))]
u=(F(1,7),F(-1,9));v=(F(-1,11),F(1,13))
du=(F(1,5),F(-1,6));dv=(F(-1,8),F(1,12))
def psi(n,u,v):
    return sum(n[i]*u[i] for i in (0,1))-max(n[0]*x+n[1]*y-zz*sum(n[i]*v[i] for i in (0,1)) for x,y,zz in C)
for i,n in enumerate(normals):
    change=psi(n,tuple(u[j]+du[j] for j in (0,1)),tuple(v[j]+dv[j] for j in (0,1)))-psi(n,u,v)
    bounds=[sum(n[j]*(du[j]+zz*dv[j]) for j in (0,1)) for x,y,zz in C]
    check(f'polyhedral_support_increment_{i}',min(bounds)<=change<=max(bounds))

result={'passed':len(checks),'failed':0,'checks':checks,'scope':'Exact checks of algebra, support increments, and margins only; analytic coverage and area formula are reviewed in REVIEW.md.'}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(f'PASS {len(checks)} independent exact diagnostics')
