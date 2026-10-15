#!/usr/bin/env python3
"""Compare independently generated proof data with author data; never exec it."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json

BASE = Path(__file__).resolve().parent
ORIGINAL = BASE.parent / 'original_submission/files/unsolved_math_prioritization/attempts/30004563'


def rational(x):
    return F(int(x['n']), int(x['d']))


def independent_interval(x):
    return rational(x['lo']), rational(x['hi'])


def author_interval(x):
    return F(x['lower']), F(x['upper'])


def contained(own, author):
    lower, upper = independent_interval(own)
    a, b = author_interval(author)
    if not a <= lower <= upper <= b:
        raise ArithmeticError('independent enclosure is not contained in author enclosure')


def main():
    own = json.loads((BASE / 'independent_certificate.json').read_text())
    author_raw = (ORIGINAL / 'turn2_exact_certificate.json').read_bytes()
    replay_raw = (BASE / 'submitted_replay/turn2_exact_certificate.json').read_bytes()
    if author_raw != replay_raw:
        raise ArithmeticError('replay differs from original certificate bytes')
    author = json.loads(author_raw)
    totals = {}
    for a, b in zip(own['G_samples'], author['scalar_sign_certificates'], strict=True):
        if rational(a['s']) != F(b['s']) or a['sign'] != b['sign']:
            raise ArithmeticError('sample mismatch')
        contained(a['G'], b['G_interval'])
    totals['outgoing_residual_enclosures_contained'] = 6
    for label, entry in zip(['A1', 'A3', 'A5'], own['boundary_parameters'], strict=True):
        a, b = independent_interval(entry['t'])
        c, d = map(F, author['boundary_definitions'][label]['t_interval'])
        if not c <= a < b <= d:
            raise ArithmeticError('boundary isolation mismatch')
    totals['algebraic_root_brackets_contained'] = 3
    for a, b in zip(own['boundary_boxes'], author['boundary_boxes'], strict=True):
        for x, y in zip(a, b, strict=True):
            contained(x, y)
    totals['boundary_coordinate_enclosures_contained'] = 12
    for a, b in zip(own['outgoing_root_brackets'], author['outgoing_center_boxes'], strict=True):
        left, right = independent_interval(a['s'])
        c, d = map(F, b['s_interval'])
        if not c <= left < right <= d:
            raise ArithmeticError('center bracket mismatch')
        for x, y in zip(a['xy'], b['box'], strict=True):
            contained(x, y)
    totals['outgoing_retained_brackets_contained'] = 5
    totals['outgoing_coordinate_enclosures_contained'] = 10
    contained(own['even_determinant'], author['even_determinant'])
    contained(own['odd_determinant'], author['odd_determinant'])
    contained(own['A3_outgoing_residual'], author['A3_not_center_residual'])
    for a, b in zip(own['incoming_samples'], [author['incoming_certificate']['G_at_left'],
                                           author['incoming_certificate']['G_at_right']], strict=True):
        contained(a['H'], b)
    for a, b in zip(own['incoming_Z'], author['incoming_certificate']['coordinate_box'], strict=True):
        contained(a, b)
    for a, b in zip([own['incoming_L'], own['incoming_M']], author['incoming_certificate']['levels'], strict=True):
        contained(a, b)
    totals['incoming_residual_enclosures_contained'] = 2
    totals['incoming_coordinate_enclosures_contained'] = 2
    totals['incoming_level_enclosures_contained'] = 2
    large = own['G_samples'][-1]['G']
    width = rational(large['hi']) - rational(large['lo'])
    if not width < F(1, 10 ** 58):
        raise ArithmeticError('large-s cancellation precision below declared bound')
    result = {
        'status': 'PASS', 'original_and_replay_certificate_byte_identical': True,
        'original_certificate_sha256': hashlib.sha256(author_raw).hexdigest(),
        'submitted_verify_success_calls': author['checks'],
        'comparison_counts': totals,
        'large_s': '100000000000000000',
        'large_s_G_width_lt': '1/10^58',
        'comparison_meaning': 'Every compared independent enclosure is contained in the author enclosure; this comparison follows independent certificate completion and is corroborative data, not an oracle.',
    }
    (BASE / 'comparison_results.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
