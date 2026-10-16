#!/usr/bin/env python3
"""Independently authored exact checks for the geometric audit; stdlib only.

No candidate code is imported or executed. This checks arithmetic obligations,
not smoothness, form theory, or heat asymptotics. All acceptance uses fractions.
"""
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path
import hashlib
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def atan_partial(x, count):
    term = x
    total = Q(0)
    for index in range(count):
        total += term / (2 * index + 1)
        term *= -x * x
    return total


def exp_partial(x, degree):
    total = term = Q(1)
    for index in range(1, degree + 1):
        term *= x / index
        total += term
    return total


def enclosure(value, digits=12):
    scale = 10 ** digits
    low = value.numerator * scale // value.denominator
    return [f'{low}/{scale}', f'{low + 1}/{scale}']


def sqrt_upper(value):
    scale = 10 ** 9
    floor = isqrt(value.numerator * scale * scale // value.denominator)
    upper = Q(floor + 1, scale)
    require(Q(floor, scale) ** 2 <= value < upper ** 2,
            'integer square-root enclosure failed')
    return upper


def main():
    tan_alpha = Q(1, 5)
    tan_twice = 2 * tan_alpha / (1 - tan_alpha ** 2)
    tan_four = 2 * tan_twice / (1 - tan_twice ** 2)
    tan_difference = (tan_four - Q(1, 239)) / (1 + tan_four / 239)
    require(tan_difference == 1, 'Machin tangent identity failed')
    # Alternating sums with an even number of terms lie below atan(x),
    # while an odd number lies above it, for x in (0,1).
    pi_low = 16 * atan_partial(Q(1, 5), 12) - 4 * atan_partial(Q(1, 239), 13)
    pi_high = 16 * atan_partial(Q(1, 5), 13) - 4 * atan_partial(Q(1, 239), 12)
    require(Q(1772, 1000) ** 2 < pi_low < pi_high < Q(1773, 1000) ** 2,
            'sqrt(pi) enclosure failed')
    # Tail begins at 1/11!, with later term ratios at most 1/12.
    e_low = exp_partial(Q(1), 10)
    factorial_11 = 1
    for index in range(1, 12):
        factorial_11 *= index
    e_high = e_low + Q(1, factorial_11) / (1 - Q(1, 12))
    require(2 < e_low < e_high < Q(2719, 1000), 'e enclosure failed')

    # Cap volume inequality follows already from e>2.
    cap_upper = 1 + Q(8, 3) / e_low ** 3
    require(cap_upper < 2, 'cap volume upper bound failed')
    L = 10000
    geometric_lower = Q(1772, 2719) * Q(1000 * L - 7092, 1000 * (L + 4))
    require(geometric_lower == Q(1106714561, 1700054750), 'lower-bound reconstruction failed')
    require(geometric_lower > Q(13, 20), 'counterexample threshold failed')
    require(Q(13, 20) - Q(129, 200) == Q(1, 200), 'separation failed')

    # Independent rational replay of the 100 all-time round intervals.
    interval_records = []
    maximum_bound = Q(0)
    maximum_k = None
    for k in range(100, 200):
        a, b = Q(k, 100), Q(k + 1, 100)
        upper = b * sqrt_upper(b) * (
            sum(Q(j * j) / exp_partial(a * (Q(j * j) - Q(1, 4)), 64)
                for j in range(1, 4))
            + Q(32) / exp_partial(Q(63, 4) * a, 64)
        )
        require(upper < Q(129, 200), f'round interval {k} failed')
        if upper > maximum_bound:
            maximum_bound, maximum_k = upper, k
        interval_records.append({'k': k, 'upper_enclosure': enclosure(upper)})
    require(maximum_k == 189, 'unexpected maximum interval')
    require(Q(1773, 3000) < Q(129, 200), 'small-time round bound failed')
    require(Q(25, 16) / (1 + Q(9)) < Q(1, 2), 'round tail ratio bound failed')

    # First round mode at t=2 exceeds normalized zero-time coefficient.
    require(pi_high * e_high ** 3 < 128, 'round maximum attainment witness failed')
    require(Q(1773, 4000) < Q(13, 20), 'weighted maximum attainment witness failed')

    # Exact controls for wrong power/time alternatives.
    require(Q(3, 4) - Q(5, 4) == -Q(1, 2), 'left unitary power failed')
    require(Q(1, 4) - Q(3, 4) == -Q(1, 2), 'right unitary power failed')
    wrong_unitary = [Q(1, 2) - Q(5, 4), Q(1, 4) - Q(1, 2)]
    require(wrong_unitary != [-Q(1, 2), -Q(1, 2)], 'wrong-unitary control not rejected')
    require(Q(3, 2) * Q(2, 3) == 1, 'volume normalization power failed')
    require(Q(L) > pi_high / 2, 'a<1 control failed')
    require(Q(1772, 2719) * Q(1000 - 7092, 5000) < Q(13, 20),
            'short-cylinder control not rejected')

    output = {
        'status': 'PASS',
        'acceptance_arithmetic': 'fractions_and_integers_only',
        'candidate_code_executed': False,
        'pi_enclosure': [enclosure(pi_low)[0], enclosure(pi_high)[1]],
        'e_enclosure': [enclosure(e_low)[0], enclosure(e_high)[1]],
        'cap_integral_upper_enclosure': enclosure(cap_upper),
        'geometric_lower': str(geometric_lower),
        'geometric_lower_enclosure': enclosure(geometric_lower),
        'round_interval_count': len(interval_records),
        'maximum_round_interval': [str(Q(maximum_k, 100)), str(Q(maximum_k + 1, 100))],
        'maximum_round_bound_enclosure': enclosure(maximum_bound),
        'minimum_round_margin_enclosure': enclosure(Q(129, 200) - maximum_bound),
        'counterexample_lower_margin_enclosure': enclosure(geometric_lower - Q(13, 20)),
        'controls': {
            'wrong_unitary_rejected': True,
            'unnormalized_metric_rejected': True,
            'fixed_time_four_not_equal_normalized_time': True,
            'short_cylinder_bound_does_not_prove_target': True,
            'round_and_weighted_maximum_attainment_witnesses': True,
        },
        'obligations_not_certified_by_code': [
            'smooth_chart_extension', 'positive_laplacian_conformal_identity',
            'zero_extension_H1', 'elliptic_form_minmax', 'Poisson_summation',
            'local_heat_trace_coefficient',
        ],
        'round_intervals': interval_records,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out_path = Path(__file__).with_name('GEOMETRY_ARITHMETIC_RESULTS.json')
    out_path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: value for key, value in output.items()
                      if key != 'round_intervals'}, indent=2))


if __name__ == '__main__':
    main()
