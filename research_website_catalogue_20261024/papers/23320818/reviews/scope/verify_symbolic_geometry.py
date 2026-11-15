#!/usr/bin/env python3
"""Independent exact symbolic metric and harmonic-Hessian scope controls.
Read-only: imports no deposited code, performs no file/network writes.
"""
import json
import sympy as s
checks=[]
def zero(expr,label):
 value=s.factor(s.trigsimp(s.cancel(expr)))
 if value!=0:raise RuntimeError(label+': '+str(value))
 checks.append(label)
t,rho,theta,az=s.symbols('t rho theta az',real=True)
a=s.symbols('a',positive=True);A,B=s.symbols('A B',nonnegative=True)
phi=1-a/rho;q=(rho+a)/(rho-a);N=A+B*q
coords=[t,rho,theta,az]
metric=[-N**2,phi**4,phi**4*rho**2,phi**4*rho**2*s.sin(theta)**2]
# Entire 4D Levi-Civita connection from the displayed metric, generic theta.
Gamma=[[[s.factor(sum((s.diff(metric[k],coords[i]) if j==k else 0)+(s.diff(metric[k],coords[j]) if i==k else 0)-(s.diff(metric[i],coords[k]) if i==j else 0) for unused in [0])/(2*metric[k])) for j in range(4)] for i in range(4)] for k in range(4)]
Ric=[]
for i in range(4):
 row=[]
 for j in range(4):
  value=sum(s.diff(Gamma[k][i][j],coords[k])-s.diff(Gamma[k][i][k],coords[j]) for k in range(4))
  value+=sum(Gamma[k][i][j]*Gamma[l][k][l]-Gamma[l][i][k]*Gamma[k][j][l] for k in range(4) for l in range(4))
  row.append(s.factor(s.trigsimp(value)))
 Ric.append(row)
scalar=s.factor(sum(Ric[i][i]/metric[i] for i in range(4)))
zero(scalar,'full four-dimensional scalar curvature vanishes')
expected=[s.Integer(0),4*A*a/(N*rho**3*phi**6),-2*A*a/(N*rho**3*phi**6),-2*A*a/(N*rho**3*phi**6)]
for i in range(4):
 for j in range(4):zero(Ric[i][j]/metric[i]-(scalar/2 if i==j else 0)-(expected[i] if i==j else 0),f'full mixed Einstein entry {i},{j}')
zero(sum((Ric[i][i]/metric[i])**2 for i in range(4))-24*a*a*A*A/(N*N*rho**6*phi**12),'family Ricci norm from full metric')
main=[s.factor(s.sympify(e).subs({A:s.Rational(1,2),B:s.Rational(1,2)})) for e in expected]
zero(main[1]-2*a/(rho**3*phi**5),'main radial curvature')
zero(main[2]+a/(rho**3*phi**5),'main angular curvature')
zero(sum(e*e for e in main)-6*a*a/(rho**6*phi**10),'main singular invariant')
zero(s.limit((rho-a)**5*main[1],rho,a,dir='+')-2*a**3,'exact borderline fifth-power limit')
for i in range(4):zero(s.factor(expected[i].subs(A,0)),'vacuum A=0 entry '+str(i))

# Independent harmonic-Hessian representation of the density, Cartesian and
# generic in all three coordinates. This mechanism proves the all-test estimate.
x,y,z=s.symbols('x y z',real=True);u=[x,y,z];R=s.sqrt(x*x+y*y+z*z)
D=[[2*A*a*s.diff(1/R,u[i],u[j]) for j in range(3)] for i in range(3)]
for i in range(3):
 for j in range(3):zero(D[i][j]-A*a/R**3*(6*u[i]*u[j]/R**2-2*int(i==j)),f'harmonic Hessian density {i},{j}')
zero(sum(D[i][i] for i in range(3)),'density trace zero')
for j in range(3):
 zero(sum(s.diff(D[i][j],u[i]) for i in range(3)),'Cartesian divergence '+str(j))
 zero(sum(D[i][j]*u[i]/R for i in range(3))-4*A*a*u[j]/R**4,'boundary traction '+str(j))
Phi=1-a/R;grad=[s.diff(Phi,v) for v in u]
for k in range(3):
 term=sum(D[i][j]*2/Phi*(int(j==i)*grad[k]+int(j==k)*grad[i]-int(i==k)*grad[j]) for i in range(3) for j in range(3))
 zero(term,'complete conformal connection contraction '+str(k))
# Surface area and normalized time integral reduce the exact boundary value.
zero((-4*A/a**2)*(4*s.pi*a**2)+16*s.pi*A,'negative sign and sphere-area normalization')
zero((-16*s.pi*A).subs(A,s.Rational(1,2))+8*s.pi,'main normalized defect is minus eight pi')
zero(s.limit(phi/(rho-a),rho,a,dir='+')-1/a,'simple defining function and positive normal derivative')
zero(s.diff(rho**2*s.diff(phi,rho),rho),'Euclidean harmonicity')
zero(-s.Rational(1,4)*(4*a**s.Rational(2,3))**s.Rational(3,2)+2*a,'regular ZAS mass')
c=s.symbols('c',positive=True)
zero(-s.Rational(1,4)*(4*a**s.Rational(2,3)*c**(-s.Rational(2,3)))**s.Rational(3,2)+2*a/c,'uniform tilt regular mass')
zero(phi**4-phi**(-2)*(phi**3)**2*(1-phi**2)-phi**6,'nearly-null tilt radial degeneration')
affine=rho-a-a*s.log(rho/a)
zero(s.diff(affine,rho)-phi,'exact null affine primitive')
zero(s.limit(affine/(rho-a)**2,rho,a,dir='+')-1/(2*a),'finite affine-length leading coefficient')
radial_s=rho-a-3*a*s.log(rho/a)-3*a*a*(1/rho-1/a)+a**3*s.Rational(1,2)*(1/rho**2-1/a**2)
zero(s.diff(radial_s,rho)-phi**3,'exact radial conformal primitive')
zero(s.limit(radial_s/(rho-a)**4,rho,a,dir='+')-1/(4*a**3),'radial conformal leading coefficient')
print(json.dumps({'status':'PASS','symbolic_identities':len(checks),'checks':checks,'method':'full generic-theta 4D connection/Ricci plus independent Cartesian harmonic Hessian density','sympy_version':s.__version__,'deposited_program_imports':False,'sampling_used_as_universal_proof':False},indent=2))
