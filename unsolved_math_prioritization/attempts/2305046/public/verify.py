#!/usr/bin/env python3
"""Bounded, deterministic controls for the partial MacLane investigation.

This is not a proof checker, zero search, or boundary membership test.
Only the Python standard library is used. Optional source checks require
separately obtained private PDFs and do not fetch any network content.
"""
import argparse
import cmath
from fractions import Fraction as Q
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def add(a, b):
    n = max(len(a), len(b))
    return [(a[k] if k < len(a) else Q(0)) +
            (b[k] if k < len(b) else Q(0)) for k in range(n)]


def neg(a):
    return [-x for x in a]


def mul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def der(a):
    return [(i+1)*a[i+1] for i in range(len(a)-1)] or [Q(0)]


def integ01(a):
    return sum((x/Q(i+1) for i, x in enumerate(a)), Q(0))


def value(a, t):
    out = Q(0)
    for x in reversed(a):
        out = out*t+x
    return out


def exp_series(g, degree):
    """Formal recurrence n a_n = sum_{k=1}^n k g_k a_{n-k}; g_0=0."""
    assert not g or g[0] == 0
    a = [Q(1)]
    for n in range(1, degree+1):
        a.append(sum((k*g[k]*a[n-k] for k in range(1, min(n, len(g)-1)+1)), Q(0))/n)
    return a


def checks():
    # Exact primitive/derivative consistency for three formal test functions.
    formal_count = 0
    for g in [[Q(0), Q(1)], [Q(0), Q(2), Q(-3), Q(1)],
              [Q(0), Q(0), Q(0), Q(7, 3), Q(-1, 5)]]:
        a = exp_series(g, 32)
        F = [Q(0)] + [a[n]/(n+1) for n in range(len(a))]
        assert der(F) == a
        formal_count += len(a)
    a = exp_series([Q(0), Q(1)], 32)
    assert a == [Q(1, math.factorial(n)) for n in range(33)]

    # The Cauchy growth proof uses an exact elementary product inequality.
    growth_count = 0
    for i in range(41):
        for j in range(41):
            x, y = Q(i, 7), Q(j, 11)
            assert 1+x+y <= (1+x)*(1+y)
            assert (1+x)*(1+y)-(1+x+y) == x*y
            growth_count += 1

    # Exact horodisk expansion. l denotes log(R); treat it as any positive
    # rational. No logarithm approximation is needed for this algebra.
    horodisk_count = 0
    for l in [Q(1, 8), Q(1, 2), Q(1), Q(2), Q(8), Q(32)]:
        center, radius = l/(l+1), 1/(l+1)
        for i in range(-12, 13):
            for j in range(-12, 13):
                x, y = Q(i, 13), Q(j, 13)
                if x*x+y*y >= 1:
                    continue
                denominator = (1-x)**2+y*y
                lhs = 1-x*x-y*y-l*denominator
                rhs = (l+1)*(radius*radius-(x-center)**2-y*y)
                assert lhs == rhs
                assert (lhs > 0) == ((x-center)**2+y*y < radius*radius)
                horodisk_count += 1

    # Floating-point diagnostics for the explicit near-miss, not certification
    # of any global analytic assertion. Keep modest radii to avoid overflow.
    max_relative_derivative_error = 0.0
    samples = 0
    for radius in [0.0, 0.2, 0.5, 0.8]:
        for k in range(32):
            z = radius*cmath.exp(2j*math.pi*k/32)
            c = (1+z)/(1-z)
            e = cmath.exp(c)
            exact_d = 2*e/(1-z)**2
            step = 1e-6
            def fun(w):
                return cmath.exp((1+w)/(1-w))
            diagnostic_d = (fun(z+step)-fun(z-step))/(2*step)
            err = abs(diagnostic_d-exact_d)/max(1.0, abs(exact_d))
            max_relative_derivative_error = max(max_relative_derivative_error, err)
            assert abs(e) > 1.0
            assert abs(exact_d) > 0.0
            assert err < 1e-6
            samples += 1

    # Integration-by-parts control for f(z)=z+z^2/4 and a polynomial path
    # gamma(t)=t/2+t^2/4. Identity is exact over the rationals.
    gamma = [Q(0), Q(1, 2), Q(1, 4)]
    h = add([Q(1)], [x/2 for x in gamma])
    fg = add(gamma, [x/4 for x in mul(gamma, gamma)])
    chain_integral = integ01(mul(h, der(gamma)))
    boundary = value(mul(gamma, h), Q(1))-value(mul(gamma, h), Q(0))
    byparts = boundary-integ01(mul(gamma, der(h)))
    increment = value(fg, Q(1))-value(fg, Q(0))
    assert chain_integral == byparts == increment == Q(57, 64)
    assert mul(h, der(gamma)) == der(fg)

    # Exact convergent/divergent controls for integral_0^{1-1/N^2}
    # (1-r)^(-alpha) dr. alpha=1 is reported by its exact log expression.
    thresholds = []
    for N in [2, 4, 16, 256]:
        sub = 2*(1-Q(1, N))
        sup = Q(N*N-1)
        assert sub < 2 and sup >= 3
        thresholds.append({'N': N, 'alpha_half': str(sub),
                           'alpha_one': f'2 log({N})', 'alpha_two': str(sup)})

    status = json.loads((HERE/'STATUS.json').read_text())
    assert status['status'] == 'unsolved'
    assert status['turns_used'] == status['turn_budget'] == 5
    assert not status['full_target_proved']
    assert not status['novelty_claim']
    assert status['independent_audit'] == 'pending'
    return {
        'result': 'passed',
        'formal_series_coefficient_checks': formal_count,
        'growth_inequality_exact_cases': growth_count,
        'horodisk_exact_cases': horodisk_count,
        'exponential_cayley_numeric_samples': samples,
        'exponential_cayley_relative_error_below': '1e-6',
        'integration_by_parts_exact_value': str(increment),
        'threshold_controls': thresholds,
        'source_hash_check': 'not_requested',
        'limits': [
            'No formal proof verification.',
            'No test of MacLane membership or asymptotic boundary limits.',
            'No exhaustive function search or novel existence certificate.',
            'Imported results require the identified scholarly sources.',
            'Finite algebra and floating-point controls do not settle the target.'
        ]
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--source-dir', type=Path)
    args = p.parse_args()
    out = checks()
    if args.source_dir is not None:
        manifest = json.loads((HERE/'SOURCE_MANIFEST.json').read_text())
        matched = []
        for source in manifest['downloaded_sources']:
            path = args.source_dir/source['filename']
            raw = path.read_bytes()
            assert len(raw) == source['bytes'], source['filename']
            assert hashlib.sha256(raw).hexdigest() == source['sha256'], source['filename']
            matched.append(source['filename'])
        out['source_hash_check'] = {'result':'passed', 'files':matched}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
