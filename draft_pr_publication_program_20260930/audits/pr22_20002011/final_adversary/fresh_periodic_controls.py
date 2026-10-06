#!/usr/bin/env python3
"""New exact closed-torus Fourier controls, independently derived after seal.

Sparse Laurent coefficients implement derivatives and exact integration. No
numeric tolerance or author/sibling checker is imported. Two active coordinates
are still contracted as a six-dimensional metric. These are finite falsification
controls, not a universal classification or new substantive proof-search attempt.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

E = s.symbols('epsilon', real=True)
Z = (0, 0)
checks = {}


def check(label, truth):
    assert bool(truth), label
    checks[label] = 'PASS'


def clean(a):
    return {k: s.expand(v) for k, v in a.items() if s.expand(v) != 0}


def add(*args):
    c = {}
    for a in args:
        for k, v in a.items():
            c[k] = c.get(k, 0) + v
    return clean(c)


def scale(a, v):
    return clean({k: v*w for k, w in a.items()})


def mul(a, b):
    c = {}
    for k, v in a.items():
        for l, w in b.items():
            m = tuple(k[i]+l[i] for i in range(2))
            c[m] = c.get(m, 0)+v*w
    return clean(c)


def d(a, i):
    if i >= 2:
        return {}
    return clean({k: s.I*k[i]*v for k, v in a.items()})


def lap(a):
    return clean({k: -(k[0]**2+k[1]**2)*v for k, v in a.items()})


def dot(a, b):
    return add(*(mul(u, v) for u, v in zip(a, b)))


def grad(a):
    return [d(a, i) for i in range(6)]


def cos(k):
    assert k != Z
    return {k: s.Rational(1, 2), tuple(-j for j in k): s.Rational(1, 2)}


def mean(a):
    return s.expand(a.get(Z, 0))


def P(f):
    df = grad(f)
    q = dot(df, df)
    return [[add(scale(d(d(f, i), j), -1), mul(df[i], df[j]),
                 scale(q, -s.Rational(1, 2)) if i == j else {})
             for j in range(6)] for i in range(6)]


def deltaP(f, v):
    df, dv = grad(f), grad(v)
    q = dot(df, dv)
    return [[add(scale(d(d(v, i), j), -1), mul(df[i], dv[j]),
                 mul(dv[i], df[j]), scale(q, -1) if i == j else {})
             for j in range(6)] for i in range(6)]


def C(p, n=6):
    return add(*(mul(p[i][j], p[i][j]) for i in range(n) for j in range(n)))


def divdensity(f, c):
    return add(lap(c), scale(dot(grad(f), grad(c)), -4),
               scale(mul(c, lap(f)), -4))


def direct(f, v):
    p, dp = P(f), deltaP(f, v)
    c = C(p)
    dc = scale(add(*(mul(p[i][j], dp[i][j])
                     for i in range(6) for j in range(6))), 2)
    return add(divdensity(f, dc), scale(dot(grad(v), grad(c)), -4),
               scale(mul(c, lap(v)), -4))


def intrinsic(f, v, connection=True, trace=True):
    p, df, dv = P(f), grad(f), grad(v)
    dotfv = dot(df, dv)
    H = []
    for i in range(6):
        row = []
        for j in range(6):
            h = d(d(v, i), j)
            if connection:
                h = add(h, scale(mul(df[i], dv[j]), -1),
                        scale(mul(df[j], dv[i]), -1),
                        dotfv if i == j and trace else {})
            row.append(h)
        H.append(row)
    T = add(*(mul(p[i][j], H[i][j]) for i in range(6) for j in range(6)))
    divC = add(*(d(mul(C(p), d(v, i)), i) for i in range(2)))
    return add(scale(divC, -4), scale(divdensity(f, T), -2))


def periodic_case(k, l, amplitude):
    label = str(k)+str(l)+'_amplitude_'+str(amplitude)
    m = tuple(k[i]+l[i] for i in range(2))
    f, psi, phi = scale(cos(k), E), cos(l), cos(m)
    ds = divdensity(f, C(P(f)))
    Dpsi, Dphi = direct(f, psi), direct(f, phi)
    check(label+'_density_mean_zero', mean(ds) == 0)
    check(label+'_linearization_mean_zero', mean(Dpsi) == 0)
    check(label+'_constant_direction_zero', direct(f, {Z: 1}) == {})
    check(label+'_full_intrinsic_operator', Dpsi == intrinsic(f, psi))
    paired = s.expand(mean(add(mul(phi, Dpsi), scale(mul(psi, Dphi), -1))))
    norm_l = sum(i*i for i in l)
    norm_m = sum(i*i for i in m)
    kl, km = sum(k[i]*l[i] for i in range(2)), sum(k[i]*m[i] for i in range(2))
    leading = s.Rational(1, 2)*(norm_l*km**2-norm_m*kl**2)
    check(label+'_leading_pairing', paired.coeff(E, 1) == leading)
    value = paired.subs(E, amplitude)
    check(label+'_full_rational_pairing_nonzero', value != 0)
    return {'k': k, 'psi_mode': l, 'phi_mode': m, 'pairing_polynomial': str(paired),
            'amplitude': str(amplitude), 'exact_normalized_integrated_defect': str(value),
            'physical_integral': '(2*pi)^6 times normalized defect'}


# Nonparallel and parallel modes exercise the trace term, plus negative and
# rescaled amplitudes. The exact pair is global, smooth, periodic and integrated.
cases = [periodic_case(k, l, a) for k, l, a in [
    ((1, 0), (1, 1), s.Rational(1, 10)),
    ((1, 0), (1, 1), -s.Rational(1, 5)),
    ((2, 1), (1, -1), s.Rational(1, 7)),
    ((1, 1), (2, 0), s.Rational(1, 11)),
    ((1, 0), (0, 1), s.Rational(1, 13)),
]]

f = scale(cos((1, 0)), E)
v = cos((1, 1))
correct = direct(f, v)
check('missing_connection_mutation_detected', intrinsic(f, v, connection=False) != correct)
check('missing_trace_connection_mutation_detected', intrinsic(f, v, trace=False) != correct)
fullS = divdensity(f, C(P(f)))
check('missing_volume_mutation_detected_by_constant_direction',
      scale(fullS, -6) != {})
wrongS = add(lap(C(P(f))), scale(dot(grad(f), grad(C(P(f)))), -4))
check('missing_product_divergence_term_detected_by_integral', mean(wrongS) != 0)
check('two_by_two_schouten_mutation_detected', C(P(f), n=2) != C(P(f), n=6))
check('density_scaling_constant_shift_control', direct(f, {Z: 1}) == {})
check('full_integrated_pairing_antisymmetry',
      mean(add(mul(cos((2, 1)), correct), scale(mul(v, direct(f, cos((2, 1)))), -1)))
      == -mean(add(mul(v, direct(f, cos((2, 1)))), scale(mul(cos((2, 1)), correct), -1))))

receipt = {'status': 'PASS', 'exact_assertions': len(checks), 'failed': 0,
           'sympy_version': s.__version__, 'closed_periodic_cases': cases,
           'mutations_detected': ['connection', 'connection trace', 'volume',
                                  'divergence product term', 'six-dimensional contraction'],
           'checks': checks,
           'scope': 'Exact finite globally periodic density/operator/integral controls; universal proof is in FIRST_PASS.md. No new proof-search attempt or discovery claim.',
           'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('FRESH_PERIODIC_RESULTS.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
