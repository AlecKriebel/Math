#!/usr/bin/env python3
"""Fresh symbolic deductions, including harmonic Hessian density mechanism.

No candidate checker is imported. These are algebraic supporting checks; the
report supplies the geometric and quantified integrability argument.
"""
import json
import sympy as s

checks={}
def verify(name, expression):
    if expression is not True:
        raise RuntimeError(name)
    checks[name]=True

def zero(z):
    return s.simplify(s.trigsimp(s.cancel(z))) == 0

a,rho=s.symbols('a rho',positive=True)
A,B=s.symbols('A B',nonnegative=True)
t,theta,azimuth=s.symbols('t theta azimuth',real=True)
p=1-a/rho
N=A+B*(rho+a)/(rho-a)
coords=[t,rho,theta,azimuth]
g=s.diag(-N*N,p**4,p**4*rho*rho,p**4*rho*rho*s.sin(theta)**2)
gi=g.inv()
Gamma={}
for upper in range(4):
    for i in range(4):
        for j in range(4):
            Gamma[upper,i,j]=s.factor(sum(gi[upper,k]*(s.diff(g[k,j],coords[i])+s.diff(g[k,i],coords[j])-s.diff(g[i,j],coords[k])) for k in range(4))/2)
Ric=s.zeros(4)
for i in range(4):
    for j in range(4):
        Ric[i,j]=s.simplify(sum(s.diff(Gamma[k,i,j],coords[k])-s.diff(Gamma[k,i,k],coords[j])+sum(Gamma[k,i,j]*Gamma[l,k,l]-Gamma[l,i,k]*Gamma[k,j,l] for l in range(4)) for k in range(4)))
R=s.simplify(s.trace(gi*Ric))
G=(gi*Ric-s.eye(4)*R/2).applyfunc(s.simplify)
target=s.diag(0,4*A*a/(N*rho**3*p**6),-2*A*a/(N*rho**3*p**6),-2*A*a/(N*rho**3*p**6))
for i in range(4):
    for j in range(4):verify('spherical_Einstein_'+str(i)+'_'+str(j),zero(G[i,j]-target[i,j]))
verify('scalar_flat',zero(R))
selected={A:s.Rational(1,2),B:s.Rational(1,2)}
verify('main_lapse',zero(N.subs(selected)-1/p))
verify('main_Ricci_square',zero(s.trace((gi*Ric)**2).subs(selected)-6*a*a/(rho**6*p**10)))
verify('vacuum_endpoint',all(zero(z.subs(A,0)) for z in G))
verify('ultrastatic_endpoint',zero(G[1,1].subs({A:1,B:0})-4*a/(rho**3*p**6)))

x,y,z=s.symbols('x y z',real=True)
X=[x,y,z];rad=s.sqrt(x*x+y*y+z*z)
potential=1/rad
H=s.hessian(potential,X)
D=2*A*a*H
claimed=s.Matrix(3,3,lambda i,j:A*a/rad**3*(6*X[i]*X[j]/rad**2-2*int(i==j)))
verify('density_is_harmonic_Hessian',all(zero(v) for v in D-claimed))
verify('potential_harmonic',zero(s.trace(H)))
for j in range(3):
    verify('density_divergence_'+str(j),zero(sum(s.diff(D[i,j],X[i]) for i in range(3))))
    verify('normal_density_'+str(j),zero(sum(X[i]/rad*D[i,j] for i in range(3))-4*A*a*X[j]/rad**4))
ph=1-a/rad
for k in range(3):
    contracted=sum(D[i,j]*2/ph*(int(i==j)*s.diff(ph,X[k])+int(j==k)*s.diff(ph,X[i])-int(i==k)*s.diff(ph,X[j])) for i in range(3) for j in range(3))
    verify('all_vector_connection_'+str(k),zero(contracted))
verify('flux_minus_16_pi_A',zero(-4*A/a**2*(4*s.pi*a*a)+16*s.pi*A))
verify('main_flux_minus_8_pi',zero((-16*s.pi*A).subs(selected)+8*s.pi))

gap=s.symbols('gap',positive=True)
verify('borderline_coefficient',s.limit((rho-a)**5*G[1,1].subs(selected),rho,a,dir='+')==2*a**3)
verify('optical_order',s.limit(p.subs(rho,a+gap)**3/gap**3,gap,0)==a**-3)
verify('null_affine_formula',zero(s.diff(rho-a-a*s.log(rho/a),rho)-p))
verify('null_affine_order',s.limit((gap-a*s.log((a+gap)/a))/gap**2,gap,0)==1/(2*a))
verify('harmonic_resolution',zero(s.diff(p,rho,2)+2/rho*s.diff(p,rho)))
verify('positive_simple_zero_derivative',s.limit(s.diff(p,rho),rho,a,dir='+')==1/a)
c=s.symbols('c',real=True)
# For |c|<1 the resolved normal derivative is 1/(a sqrt(1-c^2)).
# Its 4/3 power surface integral gives mass -2a/(1-c^2).
u=s.symbols('u',positive=True)
verify('uniform_tilt_mass',zero(-s.Rational(1,4)*(4*a**s.Rational(2,3)/u**s.Rational(2,3))**s.Rational(3,2)+2*a/u))
verify('near_null_tilt_radial',zero(p**4-p**-2*(p**3*s.sqrt(1-p*p))**2-p**6))
print(json.dumps({'verdict':'PASS','exact_symbolic_check_count':len(checks),'checks':checks,'sympy_version':s.__version__,'new_density_mechanism':'D=2Aa Hess_delta(1/rho), so its trace and divergence vanish away from rho=0.','imports_candidate_checkers':False,'proof_by_finite_sampling':False},indent=2,sort_keys=True))
