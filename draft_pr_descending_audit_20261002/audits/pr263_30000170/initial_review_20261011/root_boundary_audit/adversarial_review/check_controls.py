#!/usr/bin/env python3
"""Deterministic high-precision controls for the exact derivation in AUDIT_REPORT.md.

Only Python's standard library is needed. These finite checks do not replace the proof.
Run: python3 check_controls.py
"""
from decimal import Decimal as D, getcontext
from random import Random
import json

getcontext().prec = 90
ZERO, ONE, TWO, FOUR = D(0), D(1), D(2), D(4)
RNG = Random(26330000170)


def add(z, w):
    return z[0] + w[0], z[1] + w[1]


def sub(z, w):
    return z[0] - w[0], z[1] - w[1]


def scale(c, z):
    return c * z[0], c * z[1]


def multiply(z, w):
    return z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0]


def conjugate(z):
    return z[0], -z[1]


def dot(z, w):
    return z[0] * w[0] + z[1] * w[1]


def norm2(z):
    return dot(z, z)


def norm(z):
    return norm2(z).sqrt()


def phi(z):
    r = norm(z)
    if z[0] < ZERO:
        # Stable rationalization near the negative ray.
        return abs(z[1]) / (TWO * (r - z[0])).sqrt()
    return ((r + z[0]) / TWO).sqrt()


def distance_ray(z):
    return abs(z[1]) if z[0] < ZERO else norm(z)


def gradient(z):
    p, r = phi(z), norm(z)
    assert p > ZERO
    return p / (TWO * r), z[1] / (FOUR * r * p)


def sample(scale_value):
    return scale_value * D(RNG.randint(-1000000, 1000000)) / D(1000000)


def coefficient_point(a, disc):
    return a, scale(D('0.25'), sub(multiply(a, a), disc))


def alpha(point):
    a, b = point
    return -a[0] / TWO + phi(sub(multiply(a, a), scale(FOUR, b))) / TWO


def vector_subgradient(a, q):
    return add((D('-0.5'), ZERO), multiply(conjugate(a), q)), scale(-TWO, q)


# Distance-bound and gradient identities, including approaches to both ray sides.
min_distance_ratio = None
max_gradient_error = ZERO
boundary_count = 0
for m in (D(1), D(10), D(10000)):
    delta = ONE / (D(16) * m * m)
    cases = [(ZERO, ZERO), (-delta, ZERO), (delta, ZERO), (ZERO, delta), (ZERO, -delta)]
    for power in (1, 3, 8, 20, 35):
        imag = delta / (D(10) ** power)
        # Radius strictly less than delta, with both imaginary signs.
        cases += [(-delta / TWO, imag), (-delta / TWO, -imag)]
    for z in cases:
        assert norm(z) <= delta
        p, d = phi(z), distance_ray(z)
        assert p >= d / (TWO * delta.sqrt())
        if d:
            ratio = p * TWO * delta.sqrt() / d
            min_distance_ratio = ratio if min_distance_ratio is None else min(min_distance_ratio, ratio)
        if p:
            q = gradient(z)
            error = abs(FOUR * norm(z) * norm2(q) - ONE)
            max_gradient_error = max(max_gradient_error, error)
            assert error < D('1e-80')
        boundary_count += 1

# Full coefficient supports, with zero and negative-ray-interior base points.
min_scaled_support_slack = None
support_count = 0
for m in (D(1), D(10), D(10000)):
    delta = ONE / (D(16) * m * m)
    for base_zero in (True, False):
        for _ in range(200):
            a_x = (sample(delta / D(16)), sample(delta / D(16)))
            a_y = (sample(delta / D(16)), sample(delta / D(16)))
            disc_x = (ZERO, ZERO) if base_zero else (-delta * D(RNG.randint(1, 1000000)) / D(2000000), ZERO)
            disc_y = (sample(delta / TWO), sample(delta / TWO))
            assert norm(disc_x) < delta and norm(disc_y) < delta
            if base_zero:
                qraw = (abs(sample(m)), sample(m))
                q = scale(m / max(m, norm(qraw)), qraw)
            else:
                q = (ZERO, sample(m))
                assert abs(q[1]) <= ONE / (TWO * abs(disc_x[0]).sqrt())
            assert norm(q) <= m
            x, y = coefficient_point(a_x, disc_x), coefficient_point(a_y, disc_y)
            da, db = sub(y[0], x[0]), sub(y[1], x[1])
            va, vb = vector_subgradient(a_x, q)
            d2 = norm2(da) + norm2(db)
            slack = alpha(y) - alpha(x) - dot(va, da) - dot(vb, db) + m * d2 / TWO
            exact_form = (phi(disc_y) - dot(q, sub(disc_y, disc_x))) / TWO + dot(q, multiply(da, da)) / TWO + m * d2 / TWO
            assert abs(slack - exact_form) < D('1e-75')
            assert slack >= ZERO
            scaled_slack = slack / d2
            min_scaled_support_slack = scaled_slack if min_scaled_support_slack is None else min(min_scaled_support_slack, scaled_slack)
            support_count += 1

# Adverse-curvature controls on the zero set, where no positive Phi slack masks errors.
sharp_rows = []
for m in (D(1), D(10), D(10000)):
    for tau in (D('0.01'), D('0.000001')):
        a_x, disc = (ZERO, ZERO), (ZERO, ZERO)
        a_y, q = (ZERO, tau), (m, ZERO)
        x, y = coefficient_point(a_x, disc), coefficient_point(a_y, disc)
        da, db = sub(y[0], x[0]), sub(y[1], x[1])
        va, vb = vector_subgradient(a_x, q)
        d2 = norm2(da) + norm2(db)
        signed_deficit = alpha(y) - alpha(x) - dot(va, da) - dot(vb, db)
        assert signed_deficit == -m * tau*tau / TWO
        slack = signed_deficit + m*d2/TWO
        assert slack == m*tau**4 / D(32)
        sharp_rows.append({'M': str(m), 'tau': str(tau), 'needed_curvature_coefficient': str(-TWO*signed_deficit/d2), 'slack': str(slack)})

# Exact horizontal-normal witness and its asymptotic ratio, without cancellation.
horizontal_rows = []
for exponent in range(1, 9):
    sigma = D(10) ** (-exponent)
    t, s, h, k = sigma**3, sigma, sigma**4, sigma**3 / TWO
    rho2 = t*t + s*s
    raw_pairing = t*(h*h-k*k) + TWO*s*h*k
    exact_polynomial = sigma**8 - sigma**9 / FOUR + sigma**11
    assert raw_pairing == exact_polynomial
    disc_delta = sub(multiply((t+h, s+k), (t+h, s+k)), multiply((t, s), (t, s)))
    dist2 = norm2(disc_delta) / D(16) + h*h / FOUR
    normal_norm = FOUR * rho2.sqrt() * (ONE + D('1.25') * rho2).sqrt()
    support_ratio = raw_pairing / normal_norm / dist2
    horizontal_rows.append({
        'sigma': str(sigma),
        'support_ratio': str(support_ratio),
        'sigma_times_ratio': str(sigma * support_ratio),
        'negative_Im_b_normal_component': str(-FOUR*s / normal_norm),
    })
    assert support_ratio > ZERO
assert abs(D(horizontal_rows[-1]['sigma_times_ratio']) - D('0.8')) < D('1e-8')
assert abs(D(horizontal_rows[-1]['negative_Im_b_normal_component']) + ONE) < D('1e-14')

print(json.dumps({
    'status': 'PASS',
    'decimal_precision': getcontext().prec,
    'random_seed': 26330000170,
    'boundary_cases': boundary_count,
    'coefficient_support_cases': support_count,
    'minimum_distance_bound_ratio': str(min_distance_ratio),
    'maximum_gradient_norm_identity_error': str(max_gradient_error),
    'minimum_support_slack_divided_by_squared_distance': str(min_scaled_support_slack),
    'sharp_zero_set_curvature': sharp_rows,
    'horizontal_witness': horizontal_rows,
    'interpretation': 'Finite controls support reproducibility; exact proof and asymptotic counterexample are in AUDIT_REPORT.md.'
}, indent=2))
