#!/usr/bin/env python3
"""Independent one-variable exact trigonometric integration of periodic witness.

This does not import the Laurent engine. It uses explicit six-dimensional
Schouten diagonal formulas and integrates the two pairings by parts separately.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

x, E = s.symbols('x epsilon', real=True)
si, co = s.sin(x), s.cos(x)
fp = -E*si
C = E**2*co**2+E**3*co*si**2+s.Rational(3, 2)*E**4*si**4
Cp = s.diff(C, x)


def pairing_after_y_average(a, c):
    # psi=cos(a*x+y), phi=cos(c*x+y); normalizing y integral to mean.
    A = 2*E*a*a*co+E**2*(a*a-1)*si**2
    B = 2*a*E**2*si*co+6*a*E**3*si**3
    diff = (a-c)*x
    return (-(c*c+1)*A*s.cos(diff)+4*c*fp*A*s.sin(diff)
            -(c*c+1)*B*s.sin(diff)-4*c*fp*B*s.cos(diff))/2+2*a*Cp*s.sin(diff) \
        + 2*(a*a+1)*C*s.cos(diff)


expr = s.expand(pairing_after_y_average(1, 2)-pairing_after_y_average(2, 1))
integrated = s.simplify(s.integrate(expr, (x, 0, 2*s.pi))/(2*s.pi))
expected = s.Rational(3, 2)*E+s.Rational(99, 8)*E**3
assert s.expand(integrated-expected) == 0
assert integrated.subs(E, s.Rational(1, 10)) == s.Rational(1299, 8000)
# The exact density integral is zero independently of periodic pairing: C''
# minus 4(f'C)' is a periodic total derivative.
S = s.diff(C, x, 2)-4*s.diff(fp*C, x)
assert s.simplify(s.integrate(S, (x, 0, 2*s.pi))) == 0
receipt = {'status': 'PASS', 'exact_assertions': 3, 'sympy_version': s.__version__,
           'global_metric': 'g=exp(2*epsilon*cos(x1))*g_flat on (R/2*pi*Z)^6',
           'psi': 'cos(x1+x2)', 'phi': 'cos(2*x1+x2)',
           'exact_normalized_pairing': str(integrated),
           'at_epsilon_1_over_10': '1299/8000',
           'source': 'independent analytic Schouten diagonal and integration by parts; no Laurent engine import',
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('PERIODIC_ANALYTIC_RESULTS.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
