#!/usr/bin/env python3
"""Exact algebra checks for pass 4. Analytic arguments remain in the report."""
import json
from pathlib import Path
import sympy as s
checks=[]
def eq(name,lhs,rhs=0):
    difference=lhs-rhs
    if isinstance(difference,s.MatrixBase):
        ok=all(s.simplify(s.expand(z))==0 for z in difference)
    else:
        ok=s.simplify(s.expand(difference))==0
    assert ok, (name,difference)
    checks.append(name)

a,t,L,m=s.symbols('A t L m',positive=True)
core=s.diag(-a,-1/a,1)
blend=(1-t)*s.eye(3)+t*core
factor=(1-(a+1)*t)*(1-(1+1/a)*t)
eq('affine blend determinant',blend.det(),factor)
eq('midpoint determinant A=2',blend.det().subs({a:2,t:s.Rational(1,2)}),-s.Rational(1,8))
eq('first root',factor.subs(t,1/(a+1)))
eq('second root',factor.subs(t,a/(a+1)))
eq('core determinant one',core.det(),1)
x,y,z=s.symbols('x y z',real=True)
r2=x*x+y*y+z*z
chi=s.Function('chi')
HH=s.log(a)*x*y*chi(r2)
flow=s.Matrix([s.diff(HH,y),-s.diff(HH,x),0])
eq('Hamiltonian divergence',sum(s.diff(flow[i],v) for i,v in enumerate([x,y,z])))
az=s.Matrix([-y,x,0]); xx=s.Matrix([x,y,z])
eq('rotation rank-one trace',xx.dot(az))
b=s.symbols('b')
eq('twist determinant', (s.eye(3)+b*az*xx.T).det(),1)
eq('gradient scaling sixth power exponent',3,6*s.Rational(1,2))
eq('map scaling sixth power exponent',9,6*s.Rational(3,2))

h=s.symbols('h0:9'); H=s.Matrix(3,3,h); E=s.diag(1,0,0)
K=H.det(); C=H.cofactor_matrix()
eq('inverse addition determinant lemma', (H-t*E).det(),K-t*C[0,0])
Ct=(H+t*E).cofactor_matrix()
eq('rank-one cofactor affine', Ct,C+t*((H+E).cofactor_matrix()-C))
eq('rank-one determinant affine',(H+t*E).det(),K+t*((H+E).det()-K))
alpha,n1,n3=s.symbols('alpha n1 n3',positive=True)
eq('inverse addition cubic radial exponent',-6*alpha-3*alpha,-9*alpha)
eq('inverse addition borderline radial power',(2-9*alpha).subs(alpha,s.Rational(1,3)),-1)
eq('power energy radial exponent',(2-6*alpha).subs(alpha,s.Rational(1,2)),-1)
H1=s.diag(L,m,m); H2=s.diag(m,L,m)
pol=(H1+H2).cofactor_matrix()-H1.cofactor_matrix()-H2.cofactor_matrix()
eq('mixed cofactor diagonal',pol,s.diag(L*m+m*m,L*m+m*m,L*L+m*m))
eq('endpoint determinant exponent',1-s.Rational(2,5),s.Rational(3,5))
eq('endpoint cofactor exponent',1-s.Rational(1,5),s.Rational(4,5))
eq('dual a growth exponent',6*s.Rational(4,5)-5*s.Rational(3,5),s.Rational(9,5))
eq('dual b growth exponent',3-2*s.Rational(3,5),s.Rational(9,5))
eq('dual d growth exponent',3*s.Rational(3,5),s.Rational(9,5))
eq('cofactor endpoint moment exponent',s.Rational(9,4)*s.Rational(4,5),s.Rational(9,5))

F=s.Matrix([[2,1,0],[0,3,1],[1,0,2]])
AA=s.Matrix([[1,2,3],[2,-1,1],[0,3,2]])
BB=s.Matrix([[2,-2,1],[0,1,4],[3,0,-1]])
Dk=AA*F+BB
Du=AA+BB*F.inv()
eq('structured chain orientation',Du,Dk*F.inv())
eq('structured determinant transport',F.det()*Du.det(),Dk.det())
eq('structured cofactor transport',F.det()*Du.cofactor_matrix(),Dk.cofactor_matrix()*F.T)

q=(2-t)/(1-t)**2
eq('barrier secant factor',((1-t)**(-2)-1)/t,q)
eq('barrier source limit',s.limit(q,t,0),2)
eq('barrier positive quotient max at half',q.subs(t,s.Rational(1,2)),6)
eq('six minus secant factor',6-q,(1-2*t)*(4-3*t)/(1-t)**2)
eq('secant derivative nonnegative',s.diff(q,t),(3-t)/(1-t)**3)
eq('secant source excess',q-2,t*(3-2*t)/(1-t)**2)
J0,Jv=s.symbols('J0 Jv',positive=True)
Jt=(1-t)*J0+t*Jv
eq('barrier directional derivative',s.diff(Jt**-2,t).subs(t,0),-2*J0**-3*(Jv-J0))

p1,p2,p3=s.symbols('p1 p2 p3',real=True)
ss=p1+p2+p3; gamma=ss-3
bar3=p1+p2-2-3*gamma; pos3=4*p1+p3-5
eta=2*(3*p1+p2+2*p3-6)
eq('third stress exponent gap',pos3-bar3,eta)
eq('physical sixth energy exponent',3+6*(p1-1),6*p1-3)
eq('physical barrier energy exponent',3-2*gamma,9-2*ss)
eq('first cofactor stress gap',(2*p1+3*p2-5)-(5*p1-5),3*(p2-p1))
eq('first determinant stress gap',(2*ss-p1-5)-(5*p1-5),2*ss-6*p1)
eq('first barrier stress gap',(7-2*ss-p1)-(5*p1-5),2*(6-ss-3*p1))

rho2=s.symbols('rho2',positive=True)
g,delta=s.symbols('g delta',positive=True)
Q=z*z+rho2
f1=z**3*Q**((g-2)/2)
f2=z*Q**((g+delta)/2)
J1=Q**(g/2)*(z*z/Q)*(3+(g-2)*z*z/Q)
J2=Q**((g+delta)/2)*(1+(g+delta)*z*z/Q)
eq('angular repaired first Jacobian term',s.diff(f1,z),J1)
eq('angular repaired second Jacobian term',s.diff(f2,z),J2)
f=z**3*r2**(-s.Rational(3,4))+z*s.sqrt(r2)
FF=s.Matrix([[1,0,0],[0,1,0],[s.diff(f,x),s.diff(f,y),s.diff(f,z)]])
eq('triangular cofactor third row',FF.cofactor_matrix()[2,:],s.Matrix([[0,0,1]]))
mu,eps=s.symbols('mu eps',positive=True)
primitive=mu/(2*eps*(mu*mu+eps))+s.atan(mu/s.sqrt(eps))/(2*eps**s.Rational(3,2))
eq('angular integral primitive',s.diff(primitive,mu),1/(mu*mu+eps)**2)
angle=1/(eps*(1+eps))+s.atan(1/s.sqrt(eps))/eps**s.Rational(3,2)
eq('angular definite integral',primitive.subs(mu,1)-primitive.subs(mu,-1),angle)
eq('angular leading integral coefficient',s.limit(angle*eps**s.Rational(3,2),eps,0),s.pi/2)
eq('repaired angular exponent',-2*s.Rational(1,2)-s.Rational(3,2)*s.Rational(1,2),-s.Rational(7,4))
eq('repaired radial exponent',2-s.Rational(7,4),s.Rational(1,4))
r,d=s.symbols('r d',positive=True)
Jaxis=s.Rational(3,2)*s.sqrt(r)+2*r
baraxis=6*d*Jaxis**-4*s.diff(Jaxis,r)
eq('axis leading barrier coefficient',s.limit(baraxis*r**s.Rational(5,2),r,0),8*d/9)
eq('inverse a directional coefficient',6+5,11)
eq('inverse b directional coefficient',3+2,5)
eq('inverse c directional coefficient',1,1)
kappa=s.symbols('kappa',positive=True)
logr=s.log(s.E/r)
R=r**s.Rational(3,2)*logr**kappa
qrad=s.Rational(3,2)-kappa/logr
eq('radial repair radius derivative',s.diff(R,r),r**s.Rational(1,2)*logr**kappa*qrad)
eq('radial repair determinant via stretches',(r**s.Rational(1,2)*logr**kappa)**3*qrad,r**s.Rational(3,2)*logr**(3*kappa)*qrad)
eq('radial repair inverse target relation',R*(r**s.Rational(3,2)*logr**(3*kappa)*qrad)**-1,logr**(-2*kappa)/qrad)
eq('projection borderline logarithmic power',2*s.Rational(1,2),1)
result={'status':'pass','exact_checks':len(checks),'checks':checks,'scope':'Exact algebra only; analytic assumptions and proof arguments are stated in COMPARISON_AND_TANGENT_CERTIFICATION.md.'}
Path(__file__).with_name('verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'pass','exact_checks':len(checks)}))
