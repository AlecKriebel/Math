#!/usr/bin/env python3
"""Independent symbolic and numerical checks of authored E-6322 examples."""
from pathlib import Path
import json
import math
import platform
import sympy as S
import scipy
from scipy.integrate import quad

out = {'scope': 'E-6322 pass 1 exact examples; no minimizer counterexample claimed',
       'software': {'python': platform.python_version(), 'sympy': S.__version__, 'scipy': scipy.__version__},
       'symbolic': {}, 'numerical': []}

def certify(name, expression):
    reduced = S.factor(S.simplify(expression))
    assert reduced == 0, (name, reduced)
    out['symbolic'][name] = {'passed': True, 'difference': str(reduced)}

alpha = S.symbols('alpha', positive=True)
a,b,c,d = S.symbols('a b c d', positive=True)
s,t = S.symbols('s t', positive=True)
q = 1+alpha
P = a*(s*s+2*t*t)**3+b*(2*s*s*t*t+t**4)**S.Rational(3,2)+c*s*s*t**4
Ps = S.diff(P,s).subs({s:q,t:1})
Pt = S.diff(P,t).subs({s:q,t:1})
claimed_positive_residual = alpha*(6*a*(q*q+2)**2*(7+5*alpha)+6*b*S.sqrt(2*q*q+1)*(5+4*alpha)+6*c*q)
certify('radial_positive_residual', (2+5*alpha)*Ps-Pt-claimed_positive_residual)
H=d*s**(-2)*t**(-4)
Hs=S.diff(H,s).subs({s:q,t:1})
Ht=S.diff(H,t).subs({s:q,t:1})
certify('radial_barrier_residual', (2-7*alpha)*Hs-Ht-18*d*alpha*q**(-3))
K=a*(q*q+2)**3+b*(2*q*q+1)**S.Rational(3,2)+c*q*q
E=4*S.pi*(K/(3+6*alpha)+d*q**(-2)/(3-6*alpha))
E0=4*S.pi/S.Integer(3)*(27*a+3*S.sqrt(3)*b+c+d)
certify('radial_energy_at_zero', E.subs(alpha,0)-E0)
certify('radial_energy_first_derivative_zero', S.diff(E,alpha).subs(alpha,0))
certify('radial_energy_quadratic_coefficient', S.diff(E,alpha,2).subs(alpha,0)/2-4*S.pi/3*(63*a+5*S.sqrt(3)*b+c+3*d))

p,v,h = S.symbols('p v h', real=True)
F=S.Matrix([[1,0,0],[0,1,0],[p,v,h]])
certify('triangular_determinant', F.det()-h)
certify('triangular_cofactor_norm', sum(z*z for z in F.cofactor_matrix())-(1+p*p+v*v+2*h*h))
beta,mu,r=S.symbols('beta mu r', positive=True)
hb=r**beta*(1+beta*mu**2)
pq2=beta**2*r**(2*beta)*mu**2*(1-mu**2)
certify('rank_two_gradient_norm', 2+pq2+hb**2-(2+r**(2*beta)*(1+beta*(beta+2)*mu**2)))
certify('rank_two_cofactor_norm', 1+pq2+2*hb**2-(1+r**(2*beta)*(2+(beta**2+4*beta)*mu**2+beta**2*mu**4)))

x,y,z,k=S.symbols('x y z k', real=True)
Qdist=S.symbols('Qdist', positive=True)
inside=1-x*x-y*y-z*z
Y3=z+inside*(1-Qdist**k/4)/2
claimed_J=1-z+z*Qdist**k/4+k*inside*(1-z)*Qdist**(k-2)/8
# Chain rule for Qdist=|x-e3| gives dQdist/dz=(z-1)/Qdist.
certify('boundary_determinant', S.diff(Y3,z)+S.diff(Y3,Qdist)*(z-1)/Qdist-claimed_J)

kk=S.symbols('kk', positive=True)
certify('cone_factor_derivative', S.diff(kk**2*(3-2*kk),kk)-6*kk*(1-kk))
certify('cone_gain_factorization', 1-kk**2*(3-2*kk)-(kk-1)**2*(2*kk+1))

# Third-row Euler-Lagrange divergence on the positive vertical axis.
# At that axis p=v=0, d_x p=d_y v=beta*z**(beta-1),
# d_z h=beta*(1+beta)*z**(beta-1); other first derivatives vanish.
pp,vv,hh=S.symbols('pp vv hh', real=True)
W=a*(2+pp*pp+vv*vv+hh*hh)**3+b*(1+pp*pp+vv*vv+2*hh*hh)**S.Rational(3,2)+c*hh*hh+d*hh**(-2)
axis_dpp=S.diff(W,pp,2).subs({pp:0,vv:0})
axis_dvv=S.diff(W,vv,2).subs({pp:0,vv:0})
axis_dhh=S.diff(W,hh,2).subs({pp:0,vv:0})
Q=1+beta
claimed_axis_normalized=(6*a*(2*(2+hh*hh)**2+Q*(2+hh*hh)*(2+5*hh*hh))
+6*b*(S.sqrt(1+2*hh*hh)+Q*(1+4*hh*hh)/S.sqrt(1+2*hh*hh))
+2*c*Q+6*d*Q*hh**(-4))
certify('rank_two_axis_stationarity_defect',axis_dpp+axis_dvv+Q*axis_dhh-claimed_axis_normalized)

# Coefficients fixed only for numerical tests; symbolic assertions held for all positive coefficients.
coeffs=(1.3,0.7,2.1,0.9)
for al in [0.1,0.25,0.45]:
    aa,bb,cc,dd=coeffs
    qq=1+al
    coef=aa*(qq*qq+2)**3+bb*(2*qq*qq+1)**1.5+cc*qq*qq
    analytic=4*math.pi*(coef/(3+6*al)+dd/(qq*qq*(3-6*al)))
    numerical,err=quad(lambda rr:4*math.pi*(coef*rr**(2+6*al)+dd/qq**2*rr**(2-6*al)),0,1,epsabs=1e-10,epsrel=1e-12)
    assert math.isclose(analytic,numerical,rel_tol=2e-11,abs_tol=1e-9)
    out['numerical'].append({'test':'radial_energy','alpha':al,'analytic':analytic,'quadrature':numerical,'reported_quadrature_error':err,'passed':True})
for be in [0.2,1.0,1.25,1.45]:
    angular,angerr=quad(lambda mm:(1+be*mm*mm)**(-2),-1,1,epsabs=1e-12)
    radial,raderr=quad(lambda rr:rr**(2-2*be),0,1,epsabs=1e-10,epsrel=1e-12)
    numerical=2*math.pi*angular*radial
    analytic=2*math.pi/(3-2*be)*(1/(1+be)+math.atan(math.sqrt(be))/math.sqrt(be))
    assert math.isclose(analytic,numerical,rel_tol=2e-11,abs_tol=1e-9)
    out['numerical'].append({'test':'rank_two_barrier','beta':be,'analytic':analytic,'quadrature':numerical,'passed':True})
    K=be*(be+2)
    analyticF=4*math.pi*(8/3+12*(1+K/3)/(3+2*be)+6*(1+2*K/3+K*K/5)/(3+4*be)+(1+K+3*K*K/5+K**3/7)/(3+6*be))
    numericalF=2*math.pi*quad(lambda rr:quad(lambda mm:(2+rr**(2*be)*(1+K*mm*mm))**3,-1,1)[0]*rr*rr,0,1,epsabs=1e-10,epsrel=1e-12)[0]
    assert math.isclose(analyticF,numericalF,rel_tol=2e-11,abs_tol=1e-8)
    out['numerical'].append({'test':'rank_two_sixth_gradient','beta':be,'analytic':analyticF,'quadrature':numericalF,'passed':True})

# Deterministic interior sampling is a smoke test only; the report gives the proof of positivity.
mins={}
for kval in [1.25,1.5,1.75]:
    min_j=float('inf')
    min_point=None
    for zz in [-0.999,-0.9,-0.5,0,0.5,0.9,0.99,0.999,0.9999]:
        for fraction in [0,0.1,0.5,0.9,0.999]:
            rh2=(1-zz*zz)*fraction
            q2=rh2+(1-zz)**2
            j=1-zz+zz*q2**(kval/2)/4+kval*(1-rh2-zz*zz)*(1-zz)*q2**(kval/2-1)/8
            assert j>0
            if j<min_j: min_j,min_point=j,[math.sqrt(rh2),zz]
    mins[str(kval)]={'minimum_sampled_J':min_j,'rho_z':min_point}
out['boundary_sampling']={'passed':True,'warning':'sampling is not a proof; analytic positivity and integrability estimates are in EXACT_EXAMPLES.md','exponents':mins}
out['all_checks_passed']=True
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'symbolic_checks':len(out['symbolic']),'quadrature_checks':len(out['numerical'])},indent=2))
