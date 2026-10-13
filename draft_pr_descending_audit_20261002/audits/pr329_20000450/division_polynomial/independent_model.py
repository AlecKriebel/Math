#!/usr/bin/env python3
"""Independent model/isomorphism/chart and all-characteristic-zero fiber checks."""
import json
import sympy as s

r=s.sqrt(5)
lam,x,xi,b=s.symbols('lam x xi b')
checks=[]


def equal(a,z,name):
    difference=s.cancel(a-z,extension=r)
    if difference!=0:
        difference=s.simplify(difference)
    if difference!=0:raise ValueError(name+': '+str(difference))
    checks.append(name)


def main():
    phi=(1+r)/2;c=(11+5*r)/2;d=5+2*r
    alpha=1-r/5;gamma=2*r/5
    beta=(11-5*r)*lam/(2*(lam+5*r));k=4*(lam+5*r)/r;q=d*k*k
    a0=5-2*r;a1=(-26+10*r)*lam-20*r
    a2=(42-86*r/5)*lam**2+(-100+100*r)*lam+500+200*r
    a3=(-112+48*r)*lam**2*(lam+5*r)/5
    T=4*x**3+(b*b-6*b+1)*x*x+2*(b*b-b)*x+b*b
    transported=s.Poly(s.expand(q**3*T.subs({x:xi/q+beta,b:beta})/4),xi)
    expected=[1,a2,a1*a3,a0*a3*a3]
    for power,(actual,wanted) in enumerate(zip(transported.all_coeffs(),expected)):
        equal(actual,wanted,'transported W coefficient xi^'+str(3-power))
    DeltaT=s.factor(16*s.discriminant(T/4,x))
    equal(DeltaT,b**5*(b*b-11*b-1),'Tate discriminant from cubic discriminant')
    DW=16*s.discriminant(xi**3+a2*xi**2+a1*a3*xi+a0*a3*a3,xi)
    factor=2**24*(161-72*r)*lam**5*(lam+5*r)**5*(lam+c)
    equal(DW,factor,'exact W discriminant and all finite nonsingular exceptions')
    equal(DW,q**6*DeltaT.subs(b,beta),'discriminant scaling is q^6')
    equal(beta.subs(lam,-c),c,'finite lambda=-c maps to other Tate cusp')
    equal(s.limit(beta,lam,s.oo),(11-5*r)/2,'lambda infinity maps to Tate cusp')
    for root in (c,(11-5*r)/2):equal(root*root-11*root-1,0,'Tate cusp root')
    # Under xi=q(x-beta), exactly the marked subgroup lies at inverse-map poles.
    z=a3/(q*(x-beta))-alpha*lam
    t=z-5-2*r
    aconic=40+20*r+8*lam
    equal(z+gamma*lam,(gamma-alpha)*lam*x/(x-beta),'Y inverse-map pole only at x=0 or x=beta')
    equal(aconic+4*r*t,4*r*(z+gamma*lam),'X inverse-map pole is the same x=0 chart pole')
    x_vertex=s.cancel(beta+a3/(q*alpha*lam),extension=r)
    node=-(25+10*r)/4
    equal(T.subs({b:beta,x:x_vertex}).subs(lam,node),0,'allowed plane-cusp parameter has two-torsion vertex preimage')
    if s.simplify(factor.subs(lam,node))==0:raise ValueError('Allowed plane-cusp fiber incorrectly excluded')
    c4=(b*b-6*b+1)**2-24*(b*b-b)
    c6=-(b*b-6*b+1)**3+36*(b*b-6*b+1)*(b*b-b)-216*b*b
    if s.degree(s.gcd(s.Poly(c4,b),s.Poly(DeltaT,b)),b)!=0:raise ValueError('j0 hidden singular exclusion')
    if s.degree(s.gcd(s.Poly(c6,b),s.Poly(DeltaT,b)),b)!=0:raise ValueError('j1728 hidden singular exclusion')
    # Elementary modular fractional-linear identities are checked without importing
    # any assertion about the full-level moduli interpretation.
    tau=s.symbols('tau');f=tau**4+3*tau**3+4*tau**2+2*tau+1;g=tau**4-2*tau**3+4*tau**2-3*tau+1
    eps=lambda v:(phi*v+1)/(v-phi);iota=lambda v:(c*v+1)/(v-c)
    equal(eps(eps(tau)),tau,'epsilon is involution')
    equal(iota(iota(tau)),tau,'iota is involution')
    equal(iota(eps(tau)**5),tau*f/g,'exact displayed modular rational identity')
    equal(iota(beta),-1/(lam+c),'exact Kummer parameter specialization')
    # A wrong twist coefficient must fail the complete cubic transport identity.
    wrong_q=(5-2*r)*k*k
    wrong=s.cancel((wrong_q*(x-beta))**3+a2*(wrong_q*(x-beta))**2+a1*a3*wrong_q*(x-beta)+a0*a3*a3-wrong_q**3*T.subs(b,beta)/4,extension=r)
    if wrong==0:raise ValueError('Wrong quadratic-twist mutant was undetected')
    print(json.dumps(dict(status='PASS',exact_checks=checks,all_finite_exceptions=['0','-5sqrt5','-phi^5'],
        inverse_chart_poles='Only Tate x=0 or x=beta, already in the marked subgroup; R roots are never poles.',
        allowed_plane_cusp_parameter=str(node),j0_j1728_no_extra_exclusion=True,
        wrong_quadratic_twist_mutant_rejected=True,
        scope='Exact algebraic model/isomorphism/discriminant/pole checks; plane normalization geometry and full-level moduli interpretation require their separate proofs.'),indent=2))


if __name__=='__main__':main()
