#!/usr/bin/env python3
"""Independent, offline controls; stdout JSON, no input-file modifications.

Default: exact rational/integer checks using only the Python standard library.
--numeric: additionally use mpmath for non-certified complex-Gaussian and
direct modular-form quadrature diagnostics. Neither mode is a formal proof.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument('--public', type=Path, default=Path(__file__).resolve().parent.parent / 'public')
parser.add_argument('--numeric', action='store_true')
args = parser.parse_args()
checks = 0

def check(condition):
    global checks
    checks += 1
    if not condition:
        raise AssertionError('Independent control failed at check %d' % checks)

manifest = json.loads((Path(__file__).resolve().parent / 'FROZEN_INPUTS.json').read_text())
check(json.loads((args.public / 'FROZEN_AUTHOR_MANIFEST.json').read_text()) == manifest)
frozen = {}
for name, info in manifest['files'].items():
    raw = (args.public / name).read_bytes()
    ok = hashlib.sha256(raw).hexdigest() == info['sha256'] and len(raw) == info['bytes']
    check(ok)
    frozen[name] = ok
check(manifest['files']['PROOF.md']['sha256'] ==
      '405a9f91ea3cc437e55e55e63bdcf7151b8b8187f2659394f1ea3d0a07a1440f')

def sigma(n, k):
    return sum(j**k for j in range(1, n + 1) if n % j == 0)

def multiply(a, b, n):
    return [sum(a[j] * b[k-j] for j in range(k+1)) for k in range(n+1)]

N = 80
e2 = [1] + [-24*sigma(n, 1) for n in range(1, N+1)]
e4 = [1] + [240*sigma(n, 3) for n in range(1, N+1)]
e6 = [1] + [-504*sigma(n, 5) for n in range(1, N+1)]
a = multiply(e2, e2, N)
b = multiply(a, e2, N)
h = multiply(e4, e4, N)
A = multiply(h, a, N)
B = multiply(h, b, N)
for n in range(1, N+1):
    # Separate divisor identities, rather than another convolution routine.
    check(a[n] == 240*sigma(n, 3) - 288*n*sigma(n, 1))
    check(b[n] == -504*sigma(n, 5) + 2160*n*sigma(n, 3) - 1728*n*n*sigma(n, 1))
    check(h[n] == 480*sigma(n, 7))
check(a[:2] == [1, -48])
check(b[:2] == [1, -72])
check(A[:2] == [1, 432])
check(B[:3] == [1, 408, 28872])

# Coefficients of X^(2-j)*y^j in the Gaussian response, with y=c/tau.
response = [F((2 if j == 0 else comb(2, j)), 24) - F(comb(3, j+1), 36)
            for j in range(3)]
check(response == [0, 0, F(1, 72)])

# Reconstruct normalized Taylor and root data from the *unnormalized* source.
v8 = F(-8640, -8640)
d80 = 2*F(18144, -8640)
d81 = F(72, -8640)
check((v8, d80, d81) == (1, F(-21, 5), F(-1, 120)))
e8 = F(v8, 12) + (d80 - 72*d81)/216
check(e8 == F(1, 15))

v240 = F(113218560, 113218560)
v241 = F(725760, 113218560)
d240 = 2*F(-223140096, 113218560)
d241 = F(-4437504, 113218560)
d242 = F(-3456, 2*113218560)
check((v240, v241, d240, d241, d242) ==
      (1, F(1, 156), F(-3587, 910), F(-107, 2730), F(-1, 65520)))
j24 = (v240 + A[1]*v241)/12 + (d240 + B[1]*d241 + B[2]*d242)/216
check(j24 == F(20, 91))

# Higher-depth obstruction, all coefficients, including canceled terms.
residual = {j: 7*(2 if j == 0 else comb(6, j))-2*comb(7, j+1)
            for j in range(7)}
check(residual == {0: 0, 1: 0, 2: 35, 3: 70, 4: 63, 5: 28, 6: 5})
# If A=6B', the coefficient of y^j for j>=1 is 6(j-1)/(j+1)! B^(j+1).
check(F(6*(2-1), factorial(3)) == 1)
for degree in range(3):
    for x in [F(-3), F(0), F(2, 5), F(8)]:
        for y in [F(-2), F(1, 3), F(4)]:
            bv = lambda t: t**degree
            av = lambda t: 6*degree*t**(degree-1) if degree else F(0)
            check(av(x)+av(x+y)-12*(bv(x+y)-bv(x))/y == 0)

# Jacobians and orientation-independent algebra for each contour substitution.
for p in (2, 6):
    for w in [F(1, 3), F(2), F(-3, 2), F(7, 5)]:
        z1, z2, z3 = -1-1/w, 1-1/w, -1/w
        check((z1+1)**(2*p-2)*z1**(-p)/w**2 == 1/(w**p*(w+1)**p))
        check((z2-1)**(2*p-2)*z2**(-p)/w**2 == 1/(w**p*(w-1)**p))
        check(z3**(p-2)/w**2 == w**(-p))
    # Half Gamma(p) and (-i)^(-p); the normalization supplies one extra i.
    check(F(factorial(p-1), 2)*((-1)**(p//2)) == (-F(1, 2) if p == 2 else -60))

mutations = {
    'omit_origin_derivative': F(1, 12) - 72*d81/216 != e8,
    'use_quadratic_coefficient_as_second_derivative': F(1, 12)+(d80/2-72*d81)/216 != e8,
    'double_derivative_weight': F(1, 12)+(d80-72*d81)/108 != e8,
    'omit_first_root_derivative': F(1, 12)+d80/216 != e8,
    'wrong_E2_anomaly_sign': F(2, 24)+F(3, 36) != 0,
    'omit_leech_derivative_division_by_radius':
        (v240+A[1]*v241)/12+(d240+B[1]*d241+B[2]*2*d242)/216 != j24,
    'identify_weighted_tail_with_midpoint_kernel': F(1, 2)**3 != F(1, 2)**11,
    'delete_lower_terms_from_depth_six_response': residual[2] != 0,
}
for ok in mutations.values():
    check(ok)

numeric = None
if args.numeric:
    import mpmath as m
    m.mp.dps = 120
    NN = 220
    aa = [1] + [240*sigma(n,3)-288*n*sigma(n,1) for n in range(1, NN+1)]
    bb = [1] + [-504*sigma(n,5)+2160*n*sigma(n,3)-1728*n*n*sigma(n,1)
                for n in range(1, NN+1)]
    hh = [1] + [480*sigma(n,7) for n in range(1, NN+1)]
    AAA, BBB = multiply(hh, aa, NN), multiply(hh, bb, NN)
    taus = [m.mpc('0.13', '0.37'), m.mpc('-0.61', '0.9'),
            m.mpc('0.8', '1.4'), m.mpc('0.2', '2.7'), m.j]
    gaussian_rows = []
    for d, va, vb in ((8, aa, bb), (24, AAA, BBB)):
        for tau in taus:
            q = m.exp(2*m.pi*m.j*tau)
            qt = m.exp(-2*m.pi*m.j/tau)
            v = m.mpc(0)
            for n in range(NN+1):
                f, ft = q**n, tau**(-d//2)*qt**n
                v += va[n]*(f+ft)/24 + vb[n]*(2*m.pi*m.j)*(tau*f-ft/tau)/432
            H = m.mpc(1) if d == 8 else m.polyval(hh[::-1], q)
            target = -H/(2*m.pi**2*tau**2)
            err = abs(v-target)
            check(err < m.mpf('1e-90'))
            gaussian_rows.append({'dimension': d, 'tau': str(tau), 'absolute_error': str(err)})

    # The author integrates a divided q-series. This diagnostic instead uses
    # direct Eisenstein evaluations and the product formula for Delta.
    def phi(t, sign, d):
        q = sign*m.exp(-2*m.pi*t)
        E2 = m.polyval(e2[::-1], q)
        E4 = m.polyval(e4[::-1], q)
        E6 = m.polyval(e6[::-1], q)
        delta = q*m.fprod((1-q**n)**24 for n in range(1, N+1))
        if d == 8:
            return (E2*E4-E6)**2/delta
        return (25*E4**4-49*E6**2*E4+48*E6*E4**2*E2
                +(-49*E4**3+25*E6**2)*E2**2)/delta**2

    period_rows = []
    for d in (8, 24):
        p = d//4
        ii = m.quad(lambda t: phi(t,-1,d)/(t*t+m.mpf('0.25'))**p,
                    [m.mpf('0.5'), 1, 2, 4, 8, 12, 16])
        kk = m.quad(lambda t: phi(t,1,d)/t**p, [1, 2, 4, 8, 12, 16])
        value = (-2*ii-4*kk)/(17280*m.pi) if d == 8 else (120*ii+240*kk)/(113218560*m.pi**5)
        target = m.mpf(1)/15 if d == 8 else m.mpf('0.177860964729650276645646126241')
        check(abs(value-target) < (m.mpf('1e-38') if d == 8 else m.mpf('1e-30')))
        if d == 8:
            mutations['reverse_first_contour_orientation'] = abs((2*ii-4*kk)/(17280*m.pi)-target) > m.mpf('0.001')
            check(mutations['reverse_first_contour_orientation'])
        period_rows.append({'dimension': d, 'I': str(ii), 'K': str(kk), 'midpoint': str(value)})
    numeric = {'working_decimal_digits': m.mp.dps, 'gaussian_truncation': NN,
               'modular_truncation': N, 'quadrature_upper_endpoint': 16,
               'complex_gaussians': gaussian_rows, 'direct_modular_quadrature': period_rows,
               'caveat': 'Non-interval diagnostics; truncation and rounding are not certified.'}

out = {'result': 'PASS', 'assertions': checks, 'frozen_inputs': frozen,
       'exact_e8_midpoint': str(e8), 'exact_leech_weighted_tail': str(j24),
       'coefficient_comparison_through_n': N,
       'gaussian_response_X2_Xy_y2': [str(v) for v in response],
       'depth_six_residual_coefficients': residual,
       'rejected_mutations': mutations, 'numeric': numeric,
       'scope': 'Controls support, but do not replace, the analytic audit; the Leech midpoint is unresolved.'}
print(json.dumps(out, indent=2, sort_keys=True))
