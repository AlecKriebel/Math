"""Exact controls for the already sealed analytic proof; not a proof by sampling."""
import json
import sympy as S

r, R, m, lam, t = S.symbols('r R m lam t', real=True)
x = S.symbols('x', real=True)
u, f = S.Function('u')(x), S.Function('f')(x)
chi = S.Function('chi')(r)
checks = {}
def exact(name, expression):
    reduced = S.simplify(expression)
    assert reduced == 0, (name, reduced)
    checks[name] = True

exact('conformal_divergence_per_coordinate', S.diff(u*u*S.diff(f/u,x),x)-u*S.diff(f,x,2)+f*S.diff(u,x,2))
radial_u = 1-chi/r
exact('cutoff_radial_laplacian', S.diff(radial_u,r,2)+2*S.diff(radial_u,r)/r+S.diff(chi,r,2)/r)
end_u = 1+m/(2*r)
assert S.limit(-2*r*r*end_u**3*S.diff(end_u,r), r, S.oo) == m
checks['ADM_flux_arbitrary_mass'] = True
exact('capacity_quotient_flux', S.expand(S.series((1-R*t)/(1+m*t/2),t,0,2).removeO()).coeff(t,1)+R+m/2)
d, rho = S.symbols('d rho', positive=True)
I = 4*S.pi*(S.integrate(rho**2/d,(rho,0,d))+S.integrate(rho,(rho,d,R)))
exact('Newton_interior_solid_ball', I-2*S.pi*(R**2-d**2/3))
deltaV = 3*m*I.subs(d,lam*R)
shift = deltaV/(4*S.pi*R**2)
exact('volume_radius_shift_arbitrary_mass_center', shift-m*(3-lam**2)/2)
exact('deficit_arbitrary_mass_center', shift-m/2-m*(1-lam**2/2))
assert (shift-m/2).subs({m:-2,lam:S.Rational(1,2)}) == -S.Rational(7,4)
checks['explicit_deficit_minus_seven_quarters'] = True
q = S.symbols('q', nonnegative=True)
remainder = S.expand((1-q)**6-1+6*q)
# For 0 <= q <= 1/3, each q^k <= q^2 for k >= 2, giving 57 q^2.
assert sum(abs(remainder.coeff(q,k)) for k in range(2,7)) == 57
checks['universal_binomial_remainder_coefficients'] = True
A = S.symbols('A', positive=True)
exact('finite_core_radius_error_order', S.diff((3*A/(4*S.pi))**S.Rational(1,3),A)*A**S.Rational(2,3)-(3/(4*S.pi))**S.Rational(1,3)/3)
result = {'status':'PASS','exact_identities':len(checks),'checks':checks,
          'scope':'Symbolic identities for all admissible parameters; the sealed analytic proof supplies domains, completeness, boundary values, uniqueness, uniform estimates and exhaustion quantifiers.'}
print(json.dumps(result,indent=2,sort_keys=True))
