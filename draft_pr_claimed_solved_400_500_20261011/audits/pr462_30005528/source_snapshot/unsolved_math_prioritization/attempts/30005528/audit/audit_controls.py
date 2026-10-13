#!/usr/bin/env python3
"""Portable, offline, exact controls for the frozen compact-domino packet.

Run: python3 audit_controls.py --release ../release
Prints JSON only; writes solely within disposable temporary directories.
Does not download sources or change the input release. These finite controls
supplement, and do not replace, the all-period proof and source audit.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from math import gcd, isqrt
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile


COUNTS = Counter()


def check(condition, category):
    if not condition:
        raise AssertionError(category)
    COUNTS[category] += 1


# Strict rational bounds, certified by squaring. No decimal floating point.
LO = Q(1414213562373095, 10**15)
HI = Q(1414213562373096, 10**15)


def interval(a, b):
    """Enclose a+b*sqrt(2), independently of the author's sign method."""
    return (a + b*LO, a + b*HI) if b >= 0 else (a + b*HI, a + b*LO)


def independent_sign(a, b):
    if a == b == 0:
        return 0
    low, high = interval(a, b)
    if low > 0:
        return 1
    if high < 0:
        return -1
    raise AssertionError("rational enclosure too coarse for this finite test")


def fingerprint(release, frozen):
    actual = sorted(str(p.relative_to(release)) for p in release.rglob('*') if p.is_file())
    expected = sorted(f['path'] for f in frozen['files'])
    check(actual == expected, 'frozen_file_inventory')
    for item in frozen['files']:
        data = (release / item['path']).read_bytes()
        check(len(data) == item['bytes'], 'frozen_file_byte_lengths')
        check(hashlib.sha256(data).hexdigest() == item['sha256'], 'frozen_file_sha256')


def run(release):
    frozen = json.loads(Path(__file__).with_name('FROZEN_INPUTS.json').read_text())
    fingerprint(release, frozen)
    source = (release/'checks/verify_rotation_family.py').read_text()
    recorded_bytes = (release/'checks/verification_results.json').read_bytes()
    recorded = json.loads(recorded_bytes)

    with tempfile.TemporaryDirectory(prefix='compact-domino-audit-') as tmp:
        author = Path(tmp)/'verify_rotation_family.py'
        author.write_text(source)
        result = subprocess.run([sys.executable, '-B', str(author)], check=True,
                                capture_output=True)
        check(result.stdout == recorded_bytes, 'author_stdout_byte_replay')
        check(author.with_name('verification_results.json').read_bytes() == recorded_bytes,
              'author_output_file_byte_replay')
        namespace = runpy.run_path(str(author), run_name='audited_author_module')
        Field = namespace['Qsqrt2']

        check(LO > 0 and LO*LO < 2 < HI*HI, 'sqrt2_rational_bracket')
        for d in range(1, 10):
            for a in range(-12, 13):
                for b in range(-12, 13):
                    aa, bb = Q(a, d), Q(b, 10-d)
                    check(Field(aa, bb).sign() == independent_sign(aa, bb),
                          'independent_field_signs')

        heights = smaller = prefixes = 0
        for n in range(1, 257):
            # Derive floor(n*sqrt(2)) independently from its rational enclosure.
            floor_low, floor_high = (n*LO).__floor__(), (n*HI).__floor__()
            check(floor_low == floor_high, 'independent_floor_brackets')
            m = floor_low + 1
            check(m == isqrt(2*n*n)+1, 'independent_floor_crosscheck')
            angle = Q(m, n)
            low, high = interval(angle, -Q(1))
            check(0 < low < high < Q(1, n), 'periodic_competitor_domain')
            q = angle.denominator
            check(q == n//gcd(m, n), 'least_period_reduction')
            check((q*m) % n == 0, 'claimed_period_returns')
            for p in range(1, q):
                check((p*m) % n != 0, 'smaller_periods_excluded')
                smaller += 1
            for N in (1, 2, 7, 32, 101):
                # Sum coefficient pairs, rather than using the author's field.
                prefix_a = sum([1+angle]*(N+1), Q(0))/N
                prefix_b = sum([-Q(1)]*(N+1), Q(0))/N
                check((prefix_a-(1+angle), prefix_b+1) ==
                      ((1+angle)/N, -Q(1, N)), 'source_N_plus_one_normalization')
                prefixes += 1
            heights += 1

        angles = 0
        totient_sum = 0
        for q in range(1, 129):
            bottom = (q*LO).__floor__()
            check(bottom == (q*HI).__floor__(), 'angle_interval_floor_brackets')
            # A unit interval of angles supplies q consecutive numerators.
            reduced_count = 0
            for p in range(bottom+1, bottom+q+1):
                if gcd(p, q) != 1:
                    continue
                r = Q(p, q)
                low, high = interval(r, -Q(1))
                check(0 < low < high < 1, 'reduced_angle_domain')
                check(p*p-2*q*q >= 1, 'positive_integer_rationalization_numerator')
                # t*(2*sqrt(2)+1)*q^2 - 1 >= 0, equivalent to the gap.
                gap_a = q*q*(r-4)-1
                gap_b = q*q*(2*r-1)
                check(independent_sign(gap_a, gap_b) > 0,
                      'independent_bounded_period_gap')
                reduced_count += 1
            phi = sum(gcd(j, q) == 1 for j in range(1, q+1))
            check(reduced_count == phi, 'rational_angle_count_by_totient')
            angles += reduced_count
            totient_sum += phi

        expected_counts = {
            'explicit_periodic_competitors': heights,
            'least_period_smaller_candidate_checks': smaller,
            'source_normalization_prefix_checks': prefixes,
            'reduced_rational_angle_instances_denominator_at_most_128': angles,
            'bounded_period_gap_checks': angles,
        }
        for key, value in expected_counts.items():
            check(recorded[key] == value, 'reported_count_crosscheck')
        check((heights, smaller, prefixes, angles, totient_sum) ==
              (256, 23955, 1280, 5022, 5022), 'required_coverage_counts')

        mutations = {
            'unreduced_claimed_period': ('q = n // gcd(m, n)', 'q = n'),
            'approximation_from_below': ('m = isqrt(2 * n * n) + 1',
                                       'm = isqrt(2 * n * n)'),
            'omit_initial_symbol_cost': ('range(N + 1)', 'range(N)'),
            'wrong_height_sign': ('t = Qsqrt2(angle, Q(-1))',
                                  't = Qsqrt2(angle, Q(1))'),
            'wrong_rationalization_identity': ('Q(p*p - 2*q*q, q*q)',
                                               'Q(p*p + 2*q*q, q*q)'),
            'invert_exact_sign_comparison': ('delta = a * a - 2 * b * b',
                                             'delta = 2 * b * b - a * a'),
        }
        for name, (old, new) in mutations.items():
            check(source.count(old) == 1, 'mutation_target_unique')
            mutated = Path(tmp)/(name+'.py')
            mutated.write_text(source.replace(old, new))
            result = subprocess.run([sys.executable, '-B', str(mutated)], capture_output=True)
            check(result.returncode != 0 and b'AssertionError' in result.stderr,
                  'invalid_mutations_rejected')

        # Concrete boundary controls for common invalid changes of hypotheses.
        check((2*Q(3, 2)).denominator == 1, 'rational_alpha_has_periodic_minimizer')
        check(Q(6, 4).denominator == 2, 'period_n_need_not_be_least')
        fixed_height = interval(Q(2), -Q(1))
        check(0 < fixed_height[0] < fixed_height[1] < 1,
              'constant_cost_would_allow_fixed_point_minimizer')
        # Pairing a forward edge with its reverse creates a legal length-two cycle.
        edges = {('x', 'Fx'), ('Fx', 'x')}
        cycle = ['x', 'Fx', 'x']
        check(all((cycle[i], cycle[i+1]) in edges for i in range(2)),
              'symmetrizing_tiles_would_create_two_cycle')

    fingerprint(release, frozen)
    return {
        'status': 'passed',
        'arithmetic': 'exact rational brackets and integer arithmetic; no floating point',
        'author_replay': 'byte-for-byte match, executed only in a temporary copy',
        'reproduced_author_counts': expected_counts,
        'independent_check_counts': dict(sorted(COUNTS.items())),
        'independent_checks_total': sum(COUNTS.values()),
        'negative_mutations_rejected': len(mutations),
        'frozen_input_files_unchanged': True,
        'limitations': [
            'Finite controls do not prove all-period irrationality or topological density.',
            'Source matching, theorem scope, and the infinite argument are separately audited.',
            'These checks establish no historical priority or packing realization.'
        ]
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--release', type=Path, default=Path(__file__).parent.parent/'release')
    args = parser.parse_args()
    print(json.dumps(run(args.release), indent=2, sort_keys=True))
