#!/usr/bin/env python3
"""Independent exact checks for a bounded audit, never a PDE proof certificate."""
import argparse
import json
import os
import sys
import sympy as S

MUTANTS = (
    'cutoff_annulus', 'thickness_radius', 'spike_height', 'spike_support',
    'form_margin', 'mass_baseline', 'curvature_ratio', 'oscillatory_coefficient',
    'entire_rhs', 'entire_potential', 'hardy_threshold', 'normalize_amplitude',
    'normalize_radius', 'blowup_lambda', 'cylinder_drift', 'cylinder_hardy',
    'angular_sign', 'chain_rule_sign', 'compatibility_sign',
)

def need(value, message):
    if not value:
        raise RuntimeError(message)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mutant', choices=MUTANTS)
    p.add_argument('--inject-failure', action='store_true')
    a=p.parse_args()
    rows=[]
    def eq(name, left, right):
        residue=S.simplify(left-right)
        need(residue == 0, name + ': residual ' + str(residue))
        rows.append({'name': name, 'arithmetic': 'exact_symbolic', 'status':'pass'})
    def check(name, cond):
        need(cond, name)
        rows.append({'name':name, 'arithmetic':'exact_rational_or_symbolic_sign', 'status':'pass'})
    def pick(name, good, bad):
        return bad if a.mutant==name else good
    n=S.symbols('n', integer=True, positive=True)
    k=S.symbols('k', integer=True, positive=True)
    r=S.symbols('r', positive=True)
    t=S.symbols('t', real=True)
    eta_energy=(2*r)**n/r**2-r**n/r**2
    eq('cutoff_energy_without_ball_volume',eta_energy,pick('cutoff_annulus',2**n-1,2**n+1)*r**(n-2))
    eq('annular_average',eta_energy/(r**n-(r/2)**n),2**n/r**2)
    R=r/4
    eq('thickness_ratio',eta_energy.subs(r,R)/R**n,pick('thickness_radius',16,8)*(2**n-1)/r**2)
    rk,rhok,ak=2**(-k),2**(-3*k-4),2**(-k)
    eq('spike_height',rk**2*ak/rhok**2,2**(3*k+pick('spike_height',8,7)))
    eq('relative_radius',rhok/rk,2**(-2*k-4))
    eq('adjacent_separation',(rhok+rhok.subs(k,k+1))/(rk-rk.subs(k,k+1)),pick('spike_support',9,8)*2**(-2*k-6))
    check('support_separation_maximum',S.Rational(9,256)<1)
    check('relative_radius_maximum',S.Rational(1,64)<1)
    q=S.symbols('q', positive=True)
    eq('spike_Lq_scaling',(ak*rhok**(-2))**q*rhok**n,ak**q*rhok**(n-2*q))
    eq('critical_norm_scaling',S.simplify((rhok**(-2))**(n/2)*rhok**n),1)
    eq('sum_spike_weights',S.summation(ak,(k,1,S.oo)),1)
    eq('strict_form_margin',S.Rational(1,2)+S.Rational(1,4),pick('form_margin',S.Rational(3,4),S.Rational(2,3)))
    H=(n-2)**2/4
    eq('baseline_mass',H*n/(2*(n-2)),pick('mass_baseline',1,2)*n*(n-2)/8)
    exponent=k*k-k+4+k-(2*k+2)
    eq('curvature_ratio_exponent',exponent,k*k-2*k+pick('curvature_ratio',2,1))
    osc=S.exp(t)*(1+pick('oscillatory_coefficient',S.Rational(2,5),S.Rational(1,5))*S.sin(t))
    eq('osc_first',S.diff(osc,t),S.exp(t)*(1+S.Rational(2,5)*(S.sin(t)+S.cos(t))))
    eq('osc_second',S.diff(osc,t,2),S.exp(t)*(1+S.Rational(4,5)*S.cos(t)))
    eq('osc_third',S.diff(osc,t,3),S.exp(t)*(1+S.Rational(4,5)*(S.cos(t)-S.sin(t))))
    check('osc_positive_lower',1-S.Rational(2,5)>0)
    check('osc_first_positive',1-S.Rational(2,5)*S.sqrt(2)>0)
    check('osc_second_positive',1-S.Rational(4,5)>0)
    check('osc_third_negative',(S.diff(osc,t,3)/S.exp(t)).subs(t,3*S.pi/4)<0)
    # Derive the entire PDE directly by differentiating the profile.
    w=-S.log(1+r*r)
    lap=lambda h:S.diff(h,r,2)+(n-1)*S.diff(h,r)/r
    G=2*(n-2)*S.exp(t)+pick('entire_rhs',4,5)*S.exp(2*t)
    eq('entire_equation',-lap(w),G.subs(t,w))
    V=S.diff(G,t).subs(t,w)
    eq('entire_linearization',V,2*(n-2)/(1+r*r)+pick('entire_potential',8,4)/(1+r*r)**2)
    eq('hardy_comparison',2*(n-2)-r*r*V,(2*(n-2)+2*(n-6)*r*r)/(1+r*r)**2)
    eq('dimension_threshold',H-2*(n-2),(n-2)*(n-pick('hardy_threshold',10,9))/4)
    check('threshold_n10',S.simplify((H-2*(n-2)).subs(n,10))==0)
    check('threshold_n9_fails',S.simplify((H-2*(n-2)).subs(n,9))<0)
    ell=S.symbols('ell',integer=True,nonnegative=True)
    check('comparison_nge10_coefficients',S.Poly((2*(n-2)+2*(n-6)*r*r).subs(n,ell+10),r).all_coeffs()[0]>0)
    amp=pick('normalize_amplitude',n/(n+2),(n+2)/n)
    rho2=pick('normalize_radius',1/(2*n+4),1/(2*n))
    g=G.subs(t,amp*t)/G.subs(t,0)
    v=-S.log(1+rho2*r*r)/amp
    eq('normalized_value',g.subs(t,0),1)
    eq('normalized_derivative',S.diff(g,t).subs(t,0),1)
    eq('normalized_equation',-lap(v),g.subs(t,v))
    # Symbolic positive source jets check the original blow-up factors.
    lam,f0,fp,fj=S.symbols('lam f0 fp fj',positive=True)
    a0=f0/fp
    rho20=pick('blowup_lambda',1/(lam*fp),1/fp)
    eq('blowup_PDE_factor',rho20*lam*fj/a0,fj/f0)
    eq('blowup_derivative_at_zero',a0*fp/f0,1)
    eq('blowup_stability_coefficient',rho20*lam*fj,fj/fp)
    wt,wtt=S.symbols('wt wtt')
    ur=-(2+wt)/r
    urr=(2+wt+wtt)/r**2
    eq('cylinder_equation_radial',-r*r*(urr+(n-1)*ur/r),-wtt+pick('cylinder_drift',n-2,n+2)*wt+2*(n-2))
    beta=(n-2)/2
    z,zt=S.symbols('z zt')
    eq('cylinder_radial_weight',n-1-2*beta-2,-1)
    eq('cylinder_energy_expansion',(zt+beta*z)**2,zt**2+2*beta*z*zt+pick('cylinder_hardy',H,(n+2)**2/4)*z*z)
    ds,psi=S.symbols('ds psi')
    eq('angular_equation',2*(n-2)-ds,2*(n-2)+pick('angular_sign',-1,1)*ds)
    F,Fp,Fpp,Fppp,ux,uxx=S.symbols('F Fp Fpp Fppp ux uxx')
    # d^2(F'(u))/dx^2 = F'''(u) u_x^2 + F''(u) u_xx.
    eq('potential_chain_rule',-(Fppp*ux**2+Fpp*(-F)),Fpp*F+pick('chain_rule_sign',-1,1)*Fppp*ux**2)
    eq('gradient_compatibility',Fp*ux,pick('compatibility_sign',1,-1)*Fp*ux)
    eq('log_gradient_segment_constant',S.Rational(1,4)/S.Rational(3,4),S.Rational(1,3))
    if a.inject_failure:
        need(False,'intentional explicit failure')
    print(json.dumps({'status':'pass','uid':os.getuid(),'euid':os.geteuid(),
        'count':len(rows),'checks':rows,'full_target_proved':False,
        'scope':'Exact algebra and rational checks; no compactness, extremality or full-target certificate.'},indent=2))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'status':'fail','error':str(exc),'uid':os.getuid(),'euid':os.geteuid()}),file=sys.stderr)
        sys.exit(1)
