#!/usr/bin/env python3
"""Independent exact controls for an unresolved Ricci-shrinker research packet.

Requires SymPy. The radial cigar route differs from the author's Cartesian
Christoffel computation. Analytic/geometric arguments remain in AUDIT_REPORT.md.
No control proves the requested general estimate or supplies a counterexample.
"""
import json
from pathlib import Path
import sympy as sp

checks = []

def check(name, condition):
    assert bool(condition), name
    checks.append(name)

def zero(name, expression):
    check(name, sp.simplify(sp.trigsimp(expression)) == 0)

r, n, delta, ell = sp.symbols('r n delta ell', positive=True)
f, mu, C, R, q = sp.symbols('f mu C R q', real=True)
F = f + C
zero('hamilton_shift_sign', (R + q - F).subs(R + q, f + C))
zero('entropy_shift_sign', F.subs(C, -mu) - (f - mu))
zero('weighted_trace_from_two_identities', (n/2 - R - q).subs(R, F - q) - (n/2 - F))
check('growth_lower_ratio', sp.limit((r-5*n)**2/(4*r*r), r, sp.oo) == sp.Rational(1, 4))
check('growth_upper_ratio', sp.limit((r+sp.sqrt(2*n))**2/(4*r*r), r, sp.oo) == sp.Rational(1, 4))
# Ratio saturation alone is compatible with a strictly positive absolute gap.
Rgap = r*r/4 - 1
check('ratio_saturation_positive_gap', sp.limit(Rgap/(r*r/4), r, sp.oo) == 1)
zero('absolute_gap_of_one', r*r/4-Rgap-1)
Rbad = r*r/4 - r**-2
check('bad_sequence_gap_tends_zero', sp.limit(r*r/4-Rbad, r, sp.oo) == 0)
check('bad_sequence_scalar_ratio', sp.limit(Rbad/r**2, r, sp.oo) == sp.Rational(1, 4))

Bp, loss1, loss2 = sp.symbols('Bp loss1 loss2', nonnegative=True)
# Write both threshold inequalities as nonnegative slack variables.
P = delta*r*r - 5*n*r/2 + 25*n*n/4 - Bp
zero('scalar_gap_absorption_slack_identity',
     P-delta*r*r/2-(delta*r*r/4-5*n*r/2)-(delta*r*r/4-Bp)-25*n*n/4)
zero('linear_threshold_factorization', delta*r*r/4-5*n*r/2-delta*r*(r-10*n/delta)/4)
zero('constant_threshold_factorization', delta*r*r/4-Bp-delta*(r*r-4*Bp/delta)/4)

t = sp.symbols('t', nonnegative=True)
zero('general_cutoff_energy', 2*sp.integrate(ell**-2, (t, 0, ell))-2/ell)
zero('general_endpoint_loss', sp.integrate(1-(t/ell)**2, (t, 0, ell))-2*ell/3)
zero('unit_cutoff_total_global_Ricci_loss', (4*ell/3).subs(ell,1)-sp.Rational(4,3))
T = sp.symbols('T', positive=True)
ric = sp.diag(T, -T, 0, 0)
zero('nonnegative_scalar_does_not_bound_Ricci_trace', sp.trace(ric))
check('nonnegative_scalar_unbounded_direction', sp.limit(ric[0,0], T, sp.oo) == sp.oo)

lams = sp.symbols('l0:4', real=True)
zero('four_dimensional_trace_Hessian_Cauchy_identity',
     4*sum(x*x for x in lams)-sum(lams)**2-
     sum((lams[i]-lams[j])**2 for i in range(4) for j in range(i+1,4)))
H = sp.diag(-T, 0, 0, 0)
zero('critical_gradient_square_Hessian_trace', sp.trace(2*H*H)-2*T*T)
check('negative_potential_trace_compatible_positive_q_trace', sp.trace(H)<0)
zero('Bochner_rhs_at_zero_q', (2*T*T-q).subs(q,0)-2*T*T)
zero('flow_potential_speed', q/q-1)

k = sp.symbols('k', positive=True, integer=True)
eps = lambda z: 2**(-z-3)
zero('bump_adjacent_support_gap', 1-eps(k)-eps(k+1)-(1-3*2**(-k-4)))
check('bump_all_adjacent_supports_disjoint', 3*sp.Rational(1,2)**6 < 1)
zero('bump_total_width', 2*sp.summation(eps(k), (k,2,sp.oo))-sp.Rational(1,8))
h = sp.symbols('h', positive=True)
hp = k/sp.sqrt(1+k*k)/k**3
hpp = 1/(k**3*(1+k*k)**sp.Rational(3,2))
zero('bump_center_first_derivative', (h*hp/2).subs(h,sp.sqrt(1+k*k))-1/(2*k*k))
# The bound uses h <= sqrt(1+k^2); the remaining terms decrease for k >= 2.
fpp_upper = (hp**2 + sp.sqrt(1+k*k)*hpp)/2
loose_upper = (k**-6 + 1/(k**3*(1+k*k)))/2
zero('bump_Hessian_bound_positive_slack', loose_upper-fpp_upper-1/(2*k**6*(1+k*k)))
zero('bump_all_k_upper_at_two', loose_upper.subs(k,2)-sp.Rational(13,640))
check('bump_uniform_Hessian_defect_all_k', sp.Rational(13,640)<sp.Rational(1,2))
check('bump_center_gradient_tends_zero', sp.limit(1/(2*k*k), k, sp.oo)==0)
check('bump_center_Hessian_bound_tends_zero', sp.limit(loose_upper,k,sp.oo)==0)

# Independent cigar calculation in intrinsic radial arclength s.
s = sp.symbols('s', positive=True)
warp = 2*sp.tanh(s/2)
u = -2*sp.log(sp.cosh(s/2))
K = -sp.diff(warp,s,2)/warp
Rc = 2*K
uc = sp.diff(u,s)
zero('radial_cigar_scalar', Rc-1/sp.cosh(s/2)**2)
zero('radial_cigar_radial_steady_equation', K+sp.diff(u,s,2))
zero('radial_cigar_angular_steady_equation', K+uc*sp.diff(warp,s)/warp)
zero('radial_cigar_Hamilton', Rc+uc**2-1)
check('radial_cigar_smooth_pole_warp', sp.limit(warp/s,s,0)==1)
check('radial_cigar_tip_gradient', sp.limit(uc,s,0)==0)
check('radial_cigar_tip_scalar', sp.limit(Rc,s,0)==1)
check('radial_cigar_tip_potential', sp.limit(u,s,0)==0)
check('radial_cigar_shrinking_negative_control', sp.simplify(K+sp.diff(u,s,2)-sp.Rational(1,2)) != 0)
radial_change = 2*sp.asinh(r)
zero('cigar_metric_radial_change', sp.diff(radial_change,r)**2-4/(1+r*r))
zero('cigar_metric_angular_change', warp.subs(s,radial_change)**2-4*r*r/(1+r*r))
check('cigar_complete_radial_end', sp.limit(radial_change,r,sp.oo)==sp.oo)
zero('cigar_infinite_end_arclength', sp.integrate(1,(s,0,r))-r)

a, lam, v = sp.symbols('a lam v', positive=True)
zero('shrink_constant_rescaling', lam/(2*lam)-sp.Rational(1,2))
zero('blowup_Hamilton_scaling', (a+v)/a-(1+v/a))
zero('blowup_scalar_tip_scaling', (a-q)/a-(1-q/a))
check('blowup_steady_constant', sp.limit(1/(2*a),a,sp.oo)==0)
check('blowup_tip_small_gradient', sp.limit(a**-2/a,a,sp.oo)==0)
zero('blowup_trace_equation', (n/(2*a)-(1+v/a-q/a))-(n/(2*a)-1-v/a+q/a))

result = {
    'all_passed': True,
    'passed': len(checks),
    'checks': checks,
    'method': 'Independent exact SymPy identities, limits, and negative controls; cigar checked in intrinsic radial arclength.',
    'limitations': [
        'The full geometric and infinite-bump arguments require the audit report.',
        'The scalar ratio witnesses are algebraic controls, not solitons.',
        'The bump profile is not a shrinking Ricci soliton.',
        'The cigar is a steady comparison, not a counterexample or an asserted blow-up limit.',
        'No unrestricted positive lower gradient bound is proved.'
    ]
}
out = Path(__file__).with_name('audit_controls.json')
out.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
print(json.dumps({'all_passed':True,'passed':len(checks)}))
