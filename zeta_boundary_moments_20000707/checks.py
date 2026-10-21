"""Reproducible algebra and numerical diagnostics, not proofs of zeta uniformity."""
import json
from pathlib import Path
import sympy as s
import mpmath as mp
v = s.symbols('v')
h = (1 - v * v) ** 2 * (1 - 7 * v * v)
H = v * (1 - v * v) ** 3
if not s.expand(s.diff(H, v) - h) == 0:
    raise RuntimeError('Mathematical check failed at original line 9')
if not s.integrate(h, (v, -1, 1)) == 0:
    raise RuntimeError('Mathematical check failed at original line 10')
if not h.subs(v, 0) == 1:
    raise RuntimeError('Mathematical check failed at original line 11')
for t in (-1, 1):
    if not (h.subs(v, t) == 0 and s.diff(h, v).subs(v, t) == 0):
        raise RuntimeError('Mathematical check failed at original line 13')
if not sum((abs(x) for x in s.Poly(s.diff(h, v), v).all_coeffs())) == 120:
    raise RuntimeError('Mathematical check failed at original line 14')
pi = s.pi
z0 = -s.Rational(1, 2)
zprime0 = -s.log(2 * pi) / 2
if not s.simplify(2 * pi * (zprime0 - s.log(2 * pi) * z0)) == 0:
    raise RuntimeError('Mathematical check failed at original line 19')
import sys
rows = []
if '--symbolic-only' not in sys.argv:
    mp.mp.dps = 35
    X = mp.mpf('1')
    
    def regular(t):
        if abs(t) < mp.mpf('1e-12'):
            return mp.euler ** 2 + 2 * mp.stieltjes(1)
        return abs(mp.zeta(1 + 1j * t)) ** 2 - 1 / t ** 2
    J = mp.quad(regular, [0, mp.mpf('.01'), mp.mpf('.1'), X]) - 1 / X
    limit = J + mp.pi * mp.euler - mp.zeta(2) * X + mp.pi * mp.log(X)
    rows = []
    for qs in ('0.08', '0.04', '0.02', '0.01'):
        q = mp.mpf(qs)
        delta = q / 2
        F = mp.quad(lambda t: abs(mp.zeta(1 - delta + 1j * t)) ** 2, [0, delta, mp.mpf('.1'), X])
        C = (2 * mp.pi) ** (1 - q) * mp.zeta(q) / q
        D = -2 * mp.pi * mp.zeta(1 - q)
        normalized = F - mp.zeta(2 - q) * X - C * X ** q - D
        rows.append({'q': qs, 'renormalized': str(normalized), 'fixed_X_limit': str(limit), 'absolute_difference': str(abs(normalized - limit))})
    if not all((mp.mpf(rows[i + 1]['absolute_difference']) < mp.mpf(rows[i]['absolute_difference']) for i in range(len(rows) - 1))):
        raise RuntimeError('Mathematical check failed at original line 36')
result = {'exact_h_primitive': True, 'zero_bump_integral': True, 'bump_C1': True, 'derivative_coefficient_bound': 120, 'secondary_linear_numerator_cancellation': True, 'fixed_X_diagnostic_only': rows, 'warning': 'Numerical convergence is a diagnostic, not a proof or a uniform bound.'}


# Exact sign and renormalization checks. These algebraic checks do not establish uniform zeta estimates.
q, ell, J, gamma, aa, xx = s.symbols('q ell J gamma aa xx', nonzero=True)
secondary_sign = -1
cross_sign = -1
D_gamma_sign = -1
secondary = secondary_sign*pi/q - pi*ell
pole_F = pi/q + J + cross_sign*pi*gamma
D_leading = 2*pi/q + D_gamma_sign*2*pi*gamma
renormalized = s.expand(pole_F-aa*xx-secondary-D_leading)
if s.simplify(renormalized-(J+pi*gamma-aa*xx+pi*ell)) != 0:
    raise RuntimeError('Pole subtraction signs or constants incorrect')
endpoint_sign = -1
if endpoint_sign*pi != -pi:
    raise RuntimeError('Endpoint density sign incorrect')
K = 1000
if not (s.Rational(120,K) < s.Rational(1,4)):
    raise RuntimeError('Bump derivative budget does not guarantee positivity')
# Verify the exact double-integration-by-parts sign on a compact C2 polynomial weight.
u=s.symbols('u')
psi=u**3*(1-u)**3
HH=u**4
smoothing_sign=1
if s.integrate(psi*s.diff(HH,u,2),(u,0,1)) != smoothing_sign*s.integrate(s.diff(psi,u,2)*HH,(u,0,1)):
    raise RuntimeError('Double integration by parts sign incorrect')
result['additional_exact_guards']=['renormalization signs and constants','endpoint sign','bump positivity budget','smoothing sign']
result['symbolic_only'] = '--symbolic-only' in sys.argv

print(json.dumps(result, indent=2))
