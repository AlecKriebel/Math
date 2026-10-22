#!/usr/bin/env python3
"""Independent finite controls for the quadrature audit; not a universal proof.

Uses Green's formula on explicit circles and an independently specified oval.
All checks use explicit exceptions, including when Python runs with -O.
No copied source text, private source body, or third-party Python dependency.
"""
import argparse
import cmath
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
TAU = 2 * math.pi


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def csum(values):
    values = list(values)
    return complex(math.fsum(v.real for v in values),
                   math.fsum(v.imag for v in values))


def encoded(value):
    return [value.real, value.imag]


def circle(center, radius):
    def curve(theta):
        radial = radius * cmath.exp(1j * theta)
        return center + radial, 1j * radial
    return curve


def oval(theta):
    # (x^2+y^2)^2 - (x^2+y^2) - (x^2-y^2)/2 = 0.
    radius = math.sqrt(1 + 0.5 * math.cos(2 * theta))
    derivative = -0.5 * math.sin(2 * theta) / radius
    phase = cmath.exp(1j * theta)
    return radius * phase, (derivative + 1j * radius) * phase


def integral(curve, z, samples=8192):
    """Green formula integral of (w-z)^(-2), or area for z=None."""
    def term(k):
        w, dw = curve(TAU * k / samples)
        field = 1 if z is None else 1 / (w - z) ** 2
        return w.conjugate() * field * dw / (2j)
    return TAU / samples * csum(term(k) for k in range(samples))


def union_integral(z, samples=8192):
    """Boundary of union of radius sqrt(1/2) disks centered at +/-1/2."""
    radius = math.sqrt(0.5)
    arcs = [(0.5, -3 * math.pi / 4, 3 * math.pi / 4),
            (-0.5, math.pi / 4, 7 * math.pi / 4)]
    answer = 0j
    for center, lo, hi in arcs:
        def term(k):
            theta = lo + (hi - lo) * (k + 0.5) / samples
            radial = radius * cmath.exp(1j * theta)
            w, dw = center + radial, 1j * radial
            return w.conjugate() * dw / ((w - z) ** 2 * 2j)
        answer += (hi - lo) / samples * csum(term(k) for k in range(samples))
    return answer


def close_control(name, actual, expected, tolerance, extra=None):
    error = abs(actual - expected)
    require(math.isfinite(error), name + ': non-finite error')
    require(error <= tolerance,
            f'{name}: absolute error {error:.17g} > {tolerance:.17g}')
    row = {'name': name, 'actual': encoded(complex(actual)),
           'expected': encoded(complex(expected)),
           'absolute_error': error, 'tolerance': tolerance, 'passed': True}
    if extra:
        row.update(extra)
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--perturb-oracle', action='store_true')
    args = parser.parse_args()
    positive = []
    negative = []

    # Arbitrary, non-normalized mass; distant translate avoids origin specialness.
    mass, center, z = 0.37, 10 + 3j, 12 + 2j
    actual = integral(circle(center, math.sqrt(mass / math.pi)), z)
    expected = mass / (center - z) ** 2
    if args.perturb_oracle:
        expected += 1
    positive.append(close_control('arbitrary_mass_and_translate', actual,
                                  expected, 1e-11))

    # Merge repeated nodes with unequal positive coefficients.
    weights, center, z = [0.1, 0.2, 0.7], 2 + 3j, 5 + 2j
    expected = math.pi * csum(w / (center - z) ** 2 for w in weights)
    actual = integral(circle(center, 1), z)
    positive.append(close_control('repeated_centers_merge', actual, expected,
                                  1e-11))

    # A very small mass and a unit-order mass, disjoint and not rational radii.
    weights, centers, z = [1e-8, 1 - 1e-8], [-3 + 1j, 3 - 2j], 0.2 + 0.1j
    actual = csum(integral(circle(c, math.sqrt(w)), z)
                  for c, w in zip(centers, weights))
    expected = math.pi * csum(w / (c - z) ** 2
                             for c, w in zip(centers, weights))
    positive.append(close_control('disjoint_extreme_mass_ratio', actual,
                                  expected, 1e-11))

    # Three tangent closed disks surround a bounded complementary component.
    centers = [(2 / 3) * cmath.exp(1j * TAU * j / 3) for j in range(3)]
    radius, z = 1 / math.sqrt(3), 0.02 + 0.01j
    gap = min(abs(c - z) - radius for c in centers)
    require(gap > 0.05, 'hole test point not positively separated from disks')
    actual = csum(integral(circle(c, radius), z) for c in centers)
    expected = math.pi / 3 * csum(1 / (c - z) ** 2 for c in centers)
    closed_form = math.pi * z * (z ** 3 + 2 * (2 / 3) ** 3) / (z ** 3 - (2 / 3) ** 3) ** 2
    positive.append(close_control('tangent_ring_bounded_hole', actual, expected,
                                  1e-10, {'point': encoded(z),
                                          'minimum_disk_gap': gap}))
    positive.append(close_control('ring_rational_closed_form', expected,
                                  closed_form, 1e-12))
    area = csum(integral(circle(c, radius), None) for c in centers)
    positive.append(close_control('ring_exact_total_area', area, math.pi, 1e-11))

    # Smooth genuinely overlapping two-node oval, area pi, node weights 1/2.
    positive.append(close_control('overlapping_oval_area', integral(oval, None),
                                  math.pi, 1e-11))
    for name, z, samples, tolerance in [
        ('overlapping_oval_exterior', 2 + 0.3j, 8192, 1e-11),
        ('overlapping_oval_near_boundary', 1.23 + 0j, 32768, 1e-8),
    ]:
        actual = integral(oval, z, samples)
        expected = math.pi / 2 * (1 / (z - 0.5) ** 2 + 1 / (z + 0.5) ** 2)
        positive.append(close_control(name, actual, expected, tolerance,
                                      {'samples': samples, 'point': encoded(z)}))
        positive.append(close_control(name + '_beurling_sign', -actual / math.pi,
                                      -expected / math.pi, tolerance))

    # Negative control: replacing smash sum by ordinary union loses overlap mass.
    overlap = math.pi / 4 - 0.5
    union_area = math.pi - overlap
    require(math.pi - union_area > 0.28, 'union area-loss control did not reject')
    z = 2 + 0.3j
    field = union_integral(z)
    refined = union_integral(z, 16384)
    oracle = math.pi / 2 * (1 / (z - 0.5) ** 2 + 1 / (z + 0.5) ** 2)
    require(abs(field - refined) < 1e-7, 'union diagnostic failed refinement')
    require(abs(field - oracle) > 0.05, 'ordinary union falsely accepted')
    negative.append({'name': 'ordinary_union_is_not_smash_sum',
                     'exact_area_loss': overlap, 'field_discrepancy': abs(field - oracle),
                     'refinement_difference': abs(field - refined), 'rejected': True})

    # Negative control: all entire harmonic moments and exterior field are
    # insufficient. Annulus 1<|w|<sqrt(2), area pi, has the moments of pi*delta_0.
    # The same inverse-square identity fails at z=1/2 in its bounded hole.
    outer, inner = circle(0, math.sqrt(2)), circle(0, 1)
    z = 2 + 0.3j
    actual = integral(outer, z) - integral(inner, z)
    positive.append(close_control('annulus_unbounded_component_only', actual,
                                  math.pi / z ** 2, 1e-11))
    z = 0.5 + 0j
    actual = integral(outer, z) - integral(inner, z)
    positive.append(close_control('annulus_hole_actual_zero', actual, 0j, 1e-11))
    discrepancy = abs(actual - math.pi / z ** 2)
    require(discrepancy > 12, 'entire-moments-only model falsely accepted in hole')
    negative.append({'name': 'entire_harmonic_moments_do_not_control_holes',
                     'hole_point': encoded(z), 'field_discrepancy': discrepancy,
                     'rejected': True})

    require(len(positive) == 13, 'positive control count changed unexpectedly')
    require(len(negative) == 2, 'negative control count changed unexpectedly')
    payload = {'status': 'passed', 'python_optimization': sys.flags.optimize,
               'python_version': sys.version, 'positive': positive,
               'adverse': negative,
               'limitations': 'Floating-point diagnostics on explicit examples; universal claims are proved in REPORT.md.'}
    payload['artifact_pins'] = {}
    for name in ['check_quadrature.py', 'INPUT_PINS.json', 'SOURCE_PINS.json']:
        payload['artifact_pins'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        print(json.dumps({'status': 'failed', 'error': str(error),
                          'python_optimization': sys.flags.optimize}), file=sys.stderr)
        sys.exit(2)
