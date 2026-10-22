"""Fresh symbolic/rational corroboration, without importing submitted controls.

These checks do not prove infinite-dimensional limits or historical priority.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
import sympy as s

r = s.symbols('r', positive=True)
k = s.symbols('k')
g = s.exp(s.I*k*r)/(4*s.pi*r)
transverse = -s.diff(g,r)/r-k*k*g
radial_extra = -s.diff(g,r,2)+s.diff(g,r)/r
assert s.simplify(transverse-s.exp(s.I*k*r)*(1-s.I*k*r-k*k*r*r)/(4*s.pi*r**3)) == 0
assert s.simplify(radial_extra-s.exp(s.I*k*r)*(k*k*r*r+3*s.I*k*r-3)/(4*s.pi*r**3)) == 0
assert s.simplify(s.limit(r*(transverse-1/(4*s.pi*r**3)),r,0)+k*k/(8*s.pi)) == 0
assert s.simplify(s.limit(transverse-1/(4*s.pi*r**3)+k*k/(8*s.pi*r),r,0)+s.I*k**3/(6*s.pi)) == 0
n = s.symbols('n', integer=True, positive=True)
assert s.expand(1-n+n*(n-1)-(n-1)**2) == 0
assert s.expand(-n*(n-1)+3*n-3+(n-1)*(n-3)) == 0
l = s.symbols('l', integer=True, positive=True)
assert s.simplify(l/(2*l+1)-s.Rational(1,3)-(l-1)/(3*(2*l+1))) == 0
assert s.simplify((l+1)/(2*l+3)-l/(2*l+1)-1/((2*l+1)*(2*l+3))) == 0
a = 1/(2*l+1)
assert s.simplify(a*l-a*(-l-1)-1) == 0
# Intersection volume of two unit balls separated by r gives exact pair integrals.
overlap = s.pi*(4+r)*(2-r)**2/12
inv_square_pair = s.integrate(4*s.pi*overlap,(r,0,2))
square_pair = s.integrate(4*s.pi*r**4*overlap,(r,0,2))
assert inv_square_pair == 4*s.pi**2
assert square_pair == 32*s.pi**2/15
assert s.simplify(6*inv_square_pair/(64*s.pi**2)) == s.Rational(3,8)
assert s.simplify(9*square_pair/(16*s.pi**2)) == s.Rational(6,5)
frequency = F(1,10000)
epsilon = 2*frequency**2
eta = 120*frequency**2
assert 30*epsilon < F(1,2)
assert eta < F(1,2)
assert eta/(1-eta) <= 240*frequency**2
assert F(1,30)*60*30 == 60
assert 2+2*240 == 482
assert 3*482 == 1446
trace_coefficient = -F(2,3)+1446*frequency
assert trace_coefficient == -F(7831,15000) < 0
j = s.symbols('j', integer=True, positive=True)
assert s.simplify(s.summation(2**(-3*j-3*n-12),(n,1,s.oo))-2**(-3*j-12)/7) == 0
result = dict(all_passed=True, radial_identity=True, all_n_coefficient_algebra=True,
              all_l_harmonic_jump_and_gap=True, exact_C2_HS_squared='3/8',
              exact_remainder_majorant_HS_squared_coefficient='6/5',
              kappa=str(frequency), projection_upper=str(eta),
              imaginary_trace_upper=str(trace_coefficient*frequency**3),
              negative_trace_coefficient=str(trace_coefficient),
              all_j_removed_volume_series=True,
              limitations='Symbolic/rational corroboration only; analytic completeness, limits, Fredholm theory and priority require the written review.')
out = Path(__file__).parent/'INDEPENDENT_CONTROLS_RESULT.json'
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
