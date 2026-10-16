#!/usr/bin/env python3
"""Exact checks of pass-2 endpoint and stationarity identities; not a minimizer proof."""
from pathlib import Path
import json
import platform
import sympy as S
import scipy
from scipy.integrate import quad

out={'scope':'E-6322 pass2 auxiliary endpoint certification; no minimizer counterexample',
     'software':{'python':platform.python_version(),'sympy':S.__version__,'scipy':scipy.__version__},
     'symbolic':{},'quadrature':[]}
def ck(name,expr):
    d=S.factor(S.simplify(expr))
    assert d==0,(name,d)
    out['symbolic'][name]={'passed':True,'difference':str(d)}

r,kappa=S.symbols('r kappa',positive=True)
LL=r**S.Rational(-1,2)*S.log(S.E/r)**(-kappa)
be=-S.Rational(1,2)+kappa/S.log(S.E/r)
ck('endpoint_logarithmic_derivative',r*S.diff(LL,r)/LL-be)
n1,n2,n3,be0=S.symbols('n1 n2 n3 beta',real=True)
n=S.Matrix([n1,n2,n3]);w=be0*S.Matrix([n1,n2,-5*n3])
M=S.eye(3)+w*n.T
Delta=1+be0*(1-6*n3*n3)
ck('anisotropic_determinant_on_unit_sphere',M.det()-Delta-be0*(n1*n1+n2*n2+n3*n3-1))
Dgeneric=1+(n.T*w)[0]
ck('rank_one_inverse',sum(z*z for z in (M*(S.eye(3)-w*n.T/Dgeneric)-S.eye(3))))
L=S.symbols('L',positive=True)
D=S.diag(L,L,L**(-5))
ck('scale_determinant',D.det()-L**(-3))
ck('scale_cofactor',sum(z*z for z in (D.cofactor_matrix()-S.diag(L**(-4),L**(-4),L**2))))

p,s,t,m=S.symbols('p s t m',real=True)
ck('inverse_gradient_endpoint', (5*S.Rational(9,5)-3)-6)
ck('inverse_cofactor_endpoint', (4*S.Rational(9,4)-3)-6)
ck('inverse_determinant_endpoint', (3*3-3)-6)
ck('energy_log_integral', S.integrate(S.Symbol('u',positive=True)**(-S.Rational(3,2)),(S.Symbol('u',positive=True),1,S.oo))-2)

alpha=S.symbols('alpha',positive=True)
ck('power_gradient_inverse_threshold', 2+3*alpha-5*alpha*(S.Rational(3,5)+3/(5*alpha))+1)
ck('power_cofactor_inverse_threshold', 2+3*alpha-4*alpha*(S.Rational(3,4)+3/(4*alpha))+1)
ck('power_determinant_inverse_threshold', 2+3*alpha-3*alpha*(1+1/alpha)+1)

P,B,J,d,kk,eps=S.symbols('P B J d kk eps',positive=True)
# Degree-six positive density under F -> k^(-1/3) F.
ck('material_positive_homogeneity',kk*P*kk**(-2)-P/kk)
ck('material_barrier_homogeneity',kk*d*(J/kk)**(-2)-d*kk**3*J**(-2))
ck('hard_truncation_positive_term',(P/kk).subs(kk,J/eps)-eps*P/J)

rho,a0=S.symbols('rho a0',positive=True)
logrho=S.log(S.E/rho)
u=rho**S.Rational(2,3)*logrho**(-a0)
ck('log_shear_derivative',S.diff(u,rho)-rho**S.Rational(-1,3)*logrho**(-a0)*(S.Rational(2,3)+a0/logrho))

ss=S.symbols('ss',positive=True)
L0=S.log(S.exp(2)/r)
press=S.log(L0)
qq=r**(-2)*S.Integral(ss/S.log(S.exp(2)/ss),(ss,0,r))
ck('abstract_pressure_derivative',S.diff(press,r)+1/(r*L0))
ck('abstract_tensor_radial_ode',S.diff(qq,r)+2*qq/r-1/(r*L0))

sigma,r3=S.symbols('sigma r3',positive=True)
Pc,Bc,Ps,Bs,Ip,Iu=S.symbols('Pc Bc Ps Bs Ip Iu',real=True)
mm=sigma/(1-sigma); ell=r3/(1-sigma)
raw=Pc-3*Bc+3*mm*Bs-mm*Ps+2*ell*Ip-ell*Iu
prop=Bc-sigma*(Bc+Bs)-(1-sigma)*Pc/3-(2*r3*Ip-sigma*Ps)/3+r3*Iu/3
ck('concentric_material_identity',raw+3*prop/(1-sigma))
rr,m0,ell0=S.symbols('rr m0 ell0',positive=True)
v=(m0*rr-ell0/rr**2)/3
ck('material_shell_divergence',S.diff(v,rr)+2*v/rr-m0)
ck('material_shell_radial_coefficient',S.diff(v,rr)-v/rr-ell0/rr**3)
Bi,Btot,Ptot=S.symbols('Bi Btot Ptot',real=True)
ck('boundary_collar_constants',S.Rational(9,4)*Bi-16*Ptot-S.Rational(15,4)*(Btot-Bi)-6*(Bi-S.Rational(5,8)*Btot-S.Rational(8,3)*Ptot))

l1,l2,l3,b=S.symbols('l1 l2 l3 b',positive=True)
K2=l1*l1*l2*l2+l1*l1*l3*l3+l2*l2*l3*l3
Pb=b*K2**S.Rational(3,2)
for i,(li,cofi) in enumerate([(l1,l2*l3),(l2,l1*l3),(l3,l1*l2)],1):
    ck('positive_cofactor_stress_eigenvalue_'+str(i),li*S.diff(Pb,li)-3*b*S.sqrt(K2)*(K2-cofi**2))

al1,al2,al3=S.symbols('alpha1 alpha2 alpha3',real=True)
gamma=al1+al2+al3-3
bar=al1+al2-3-3*gamma
apos=4*al1+al3-6
bpos=3*al1+al2+al3-6
cpos=2*al1+2*al2+al3-6
eta=2*(3*al1+al2+2*al3-6)
ck('anisotropic_component_exponent_gap',apos-bar-eta)
ck('cofactor_exponent_not_lower',bpos-apos-(al2-al1))
ck('det_square_exponent_not_lower',cpos-apos-2*(al2-al1))
ck('balanced_exponent_gap',(eta-2*(al3-al1)).subs(al2,6-4*al1-al3))
ck('explicit_axis_barrier_exponent',bar.subs({al1:1-alpha,al2:1-alpha,al3:1+5*alpha})-(-11*alpha-1))
ck('explicit_axis_positive_exponent',apos.subs({al1:1-alpha,al2:1-alpha,al3:1+5*alpha})-(alpha-1))

A,LC,z=S.symbols('A LC z',positive=True)
reg=(A-27*LC)*z*z+2*d*eps**(-3)*z+3*d*eps**(-2)
zstar=d*eps**(-3)/(27*LC-A)
ck('regularization_optimal_z',S.diff(reg,z).subs(z,zstar))
ck('regularization_growth_constant',reg.subs(z,zstar)-d*d*eps**(-6)/(27*LC-A)-3*d*eps**(-2))
ck('regularization_barrier_hessian',S.diff(d*J**(-2),J,2).subs(J,eps)-6*d*eps**(-4))

for kv in [0.2,0.25,0.4]:
    value,error=quad(lambda u:u**(-6*kv),1,float('inf'),epsabs=1e-10,epsrel=1e-12)
    exact=1/(6*kv-1)
    assert abs(value-exact)<1e-8
    out['quadrature'].append({'test':'critical_endpoint_energy','kappa':kv,'exact':exact,'quadrature':value,'error_estimate':error,'passed':True})

out['all_checks_passed']=True
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_passed':True,'symbolic_checks':len(out['symbolic']),'quadrature_checks':len(out['quadrature'])},indent=2))
