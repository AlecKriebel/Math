"""Independent exact identities plus labeled high-precision falsification tests.

No author checker is imported. Neither the numeric tests nor the exact finite
identities replace the accompanying analytic proof audit.
"""
import argparse
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import hashlib
import json
import math
import random
import sympy as s
import mpmath as mp

exact = Counter()
diagnostics = Counter()


def identity(expr, label):
    assert s.simplify(expr) == 0, label
    exact[label] += 1


def rational_check(condition, label):
    assert condition, label
    exact[label] += 1


a, x, y, r = s.symbols('a x y r', real=True)
c = x + s.I * y
u = x * x + y * y
norm = lambda z: s.expand(z * s.conjugate(z))
num = a + 2 * c + a * c * c
identity(norm(num) - ((1 + u + 2 * a * x) ** 2 - (1 - a * a) * (1 - u) ** 2),
         'raw_complex_jet_squared_modulus')
den = norm(1 + a * c) - r * r * norm(a + c)
identity(den - ((1 - r * r) * (1 + u + 2 * a * x) + (1 - a * a) * (r * r - u)),
         'raw_complex_hyperbolic_denominator')
identity((a + c) / (1 + a * c) + (1 - a * a) * c / (1 + a * c) ** 2
         - num / (1 + a * c) ** 2, 'schur_jet_center_direct_chain_rule')

B, D, k, k0 = s.symbols('B D k k0', positive=True)
T = s.sqrt(D * D - B * k * k)
b = B * (k / k0 - 1) / 2
q = (T + b) / (D + b)
identity(s.diff(q, k) - B / (D + b) ** 2 * ((D - T) / (2 * k0) - k * (D + b) / T),
         'direct_radical_defect_derivative')
rho = 3 - 2 * s.sqrt(2)
K0 = 2 * s.sqrt(2) / 3
identity((1 - rho * rho) / (1 + rho * rho) - K0, 'critical_derivative_normalization')
identity(s.Rational(4, 3) / (2 * K0) - K0 + s.sqrt(2) / 6,
         'strict_defect_derivative_margin')

v, delta = s.symbols('v delta', real=True)
Dv = 1 + a * v
E = Dv * Dv - s.Rational(8, 9) * (1 - a * a)
log_derivative = 8 * a * (1 - a * a) / (9 * Dv * E) - 2 * delta * (1 + a) / (Dv * (1 - v))
identity(log_derivative * 9 * Dv * E * (1 - v) / (2 * (1 + a))
         - (4 * a * (1 - a) * (1 - v) - 9 * delta * E),
         'angular_log_derivative_sign_equivalence')
P = 16 * a * a * (1 - v) * (32 * Dv + (1 - a) ** 2 * (1 - v)) - 81 * E * E
identity(s.diff(P, v, 2) + 4 * a * a * (243 * a * a * v * v + 64 * a * a + 486 * a * v + 272 * a + 163),
         'angular_concavity_polynomial')
identity(P.subs(v, s.Rational(1, 3)) + (19 * a * a - 38 * a + 3) * (35 * a * a + 74 * a + 3) / 9,
         'angular_positive_endpoint_factorization')
identity(P.subs(v, -s.Rational(1, 3)) + (43 * a * a - 98 * a + 3) * (11 * a * a + 62 * a + 3) / 9,
         'angular_negative_endpoint_factorization')
identity((a + 3) ** 3 - 16 * (3 * a + 1) - (1 - a) ** 2 * (a + 11),
         'derivative_final_endpoint_gap')
identity(4 * (a + 3) - (3 * a + 1) * (3 - a) ** 2 - (1 - a) * (3 * a * a - 14 * a + 3),
         'small_a_comparison_gap')

ss, yy = s.symbols('ss yy', positive=True)
X02 = (ss * ss - r ** 4) * (1 - ss * ss) / (1 - r * r) ** 2
identity(ss * ss - X02 - (r * r - ss * ss) ** 2 / (1 - r * r) ** 2,
         'value_region_imaginary_bound')
identity((ss + r * r) * (1 - ss * ss) - (ss - r * r) * (1 + r) ** 2
         - (r - ss) * (r ** 3 + r * r * ss + 2 * r * r + r * ss + 2 * r + ss * ss),
         'phase_first_positive_factorization')
identity(2 * (yy - r) - (1 - r) * yy * ((1 + yy) ** 2 - 2)
         - (1 - yy) * ((1 - r) * yy * yy + 3 * (1 - r) * yy - 2 * r),
         'phase_second_positive_factorization')
R = (3 - s.sqrt(5)) / 2
identity((1 - R * R) / (2 * R) - s.sqrt(5) / 2, 'modulus_phase_constant')
identity((1 + R) / (1 - R) - s.sqrt(5), 'modulus_log_constant')
rational_check(Q(31, 40) + Q(1, 21) - Q(1, 3 * 21 ** 3) > Q(81, 100),
               'strict_rational_arctan_margin')
rational_check(sum(Q(81, 50) ** j / math.factorial(j) for j in range(8)) > 5,
               'strict_rational_exponential_margin')

U, V = s.symbols('U V')
h = lambda z: z / (1 - z * z)
kernel = (h(U) - h(V)) / (h(U) + h(V)) * (U + V) / (U - V)
identity(kernel - (1 + U * V) / (1 - U * V), 'odd_grunsky_exact_example_and_factor')
phi = r * (a + r) / (1 + a * r)
phi_prime = (a + 2 * r + a * r * r) / (1 + a * r) ** 2
Fp = lambda z: (1 - z) / (1 + z) ** 3
H = phi_prime * Fp(phi) / Fp(r)
identity(H.subs(a, 1) - 1, 'sharp_derivative_identity_endpoint')
identity(s.diff(H, a).subs(a, 1) - (r * r - 6 * r + 1) / (1 + r) ** 2,
         'sharp_derivative_first_variation')

# High precision diagnostics below are intentionally reported separately.
mp.mp.dps = 90
rr = 3 - 2 * mp.sqrt(2)
RR = (3 - mp.sqrt(5)) / 2
kk0 = 2 * mp.sqrt(2) / 3
rng = random.Random(230503830000048)
tol = mp.mpf('1e-70')
log_ratio = lambda t: mp.log((1 + t) / (1 - t))
for j in range(1200):
    aa = mp.mpf(rng.randrange(1, 10000)) / 10000
    radius = mp.mpf(rng.randrange(0, 10001)) / 10000
    theta = 2 * mp.pi * rng.randrange(10000) / 10000
    cc = rr * radius * mp.e ** (1j * theta)
    ww = rr * (aa + cc) / (1 + aa * cc)
    J = (abs(aa + 2 * cc + aa * cc * cc) + (1 - aa * aa) * (rr * rr - abs(cc) ** 2) / (1 - rr * rr)) / abs(1 + aa * cc) ** 2
    delta0 = abs((rr - ww) / (1 - rr * ww))
    rawQ = (1 - rr * rr) * J / (1 - abs(ww) ** 2)
    kval = (1 - abs(cc) ** 2) / (1 + abs(cc) ** 2)
    vv = 2 * cc.real / (1 + abs(cc) ** 2)
    DD = 1 + aa * vv
    bb = (1 - aa * aa) * (kval / kk0 - 1) / 2
    TT = mp.sqrt(max(mp.mpf(0), DD * DD - (1 - aa * aa) * kval * kval))
    newQ = (TT + bb) / (DD + bb)
    assert abs(rawQ - newQ) < tol
    diagnostics['raw_complex_jet_matches_normalization'] += 1
    interior = newQ * ((1 + delta0) / (1 - delta0)) ** 2
    boundaryQ = mp.sqrt(max(mp.mpf(0), 1 - (mp.mpf(8) / 9) * (1 - aa * aa) / (DD * DD)))
    boundary_delta = mp.sqrt((1 - aa) ** 2 * (1 - vv) / (32 * DD + (1 - aa) ** 2 * (1 - vv)))
    boundary = boundaryQ * ((1 + boundary_delta) / (1 - boundary_delta)) ** 2
    assert interior <= boundary + tol and interior <= 1 + tol
    diagnostics['derivative_interior_to_boundary_and_target'] += 1

    r0 = RR * mp.mpf(rng.randrange(1, 10000)) / 10000
    c0 = r0 * radius * mp.e ** (1j * theta)
    w0 = r0 * (aa + c0) / (1 + aa * c0)
    s0 = abs(w0)
    if r0 * r0 < s0 < r0:
        vv0 = mp.sqrt(w0)
        q0 = (mp.sqrt(r0) - vv0) / (mp.sqrt(r0) + vv0)
        gamma = mp.pi / 2 - abs(mp.arg(q0))
        lower = mp.sqrt(s0 / r0) * mp.atan((1 - r0 * r0) / (2 * r0))
        assert gamma + tol >= lower
        assert gamma > mp.sqrt(log_ratio(r0) * log_ratio(s0))
        diagnostics['outer_region_phase_separation'] += 1

parser = argparse.ArgumentParser()
parser.add_argument('--proof-dir', required=True, type=Path)
args = parser.parse_args()
hashes = {f'TURN_{n}.md': hashlib.sha256((args.proof_dir / f'TURN_{n}.md').read_bytes()).hexdigest() for n in range(1, 5)}
print(json.dumps({'status': 'PASS_INDEPENDENT_CONTROLS',
                  'proof_sha256': hashes,
                  'exact_symbolic_or_rational_checks': sum(exact.values()),
                  'exact_counts': dict(sorted(exact.items())),
                  'high_precision_diagnostic_checks': sum(diagnostics.values()),
                  'diagnostic_counts': dict(sorted(diagnostics.items())),
                  'diagnostic_precision_decimal_digits': mp.mp.dps,
                  'qualification': 'Diagnostics are not universal proof certificates. Analytic branch, domain, interval and historical-scope review is in ADVERSARIAL_REVIEW.md.'}, indent=2, sort_keys=True))
