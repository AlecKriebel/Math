#!/usr/bin/env python3
"""Read-only standard-library check of this audit's finite exact arithmetic.

This program neither accesses the network nor proves the calculus/source theorems.
Run a NEW COPY with the externally pinned public manifest SHA-256.
"""
from argparse import ArgumentParser
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial
from pathlib import Path
import json


class VerificationError(Exception):
    pass


def need(condition, message):
    if not condition:
        raise VerificationError(message)


def poly_add(a, b):
    result = [Q(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        result[i] += x
    for i, x in enumerate(b):
        result[i] += x
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def poly_mul(a, b):
    result = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def q2_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def q2_mul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def validate_math(c):
    scope = c['claim_scope']
    need(scope['equal_rates_only'] is True, 'rate scope was broadened')
    need(Q(scope['lower_endpoint']) == Q(17, 4), 'unsupported lower endpoint')
    need(scope['closed_lower_endpoint'] is True, 'closed endpoint missing')
    need(Q(scope['upper_finite_endpoint']) == 7, 'wrong finite endpoint')
    need(Q(scope['infinite_tail_from']) == 7, 'unproved tail start')
    need(scope['positive_integer_initial_counts_as_extension'] is True, 'integer extension missing')
    need(scope['arbitrary_positive_real_initial_counts_proved'] is False, 'unproved real extension')
    need(scope['stable_attainment_extension_by_conditioning'] is False, 'invalid reverse conditioning')
    rows = c['rows']
    need(len(rows) == 5, 'interval count')
    previous = Q(17, 4)
    differences = []
    for row in rows:
        A, B, T, S, f, margin = (Q(row[k]) for k in ['A', 'B', 'T', 'S', 'f', 'margin'])
        need(A == previous and A <= B, 'interval coverage gap/overlap')
        need(A >= Q(17, 4) and 3 <= B <= 7, 'outside analytic monotonicity range')
        need(T > 0 and T ** B.denominator >= Q(3, 2) ** B.numerator, 'power cap false')
        need(S == T / (1 + T), 'cap probability wrong')
        need(Q(3, 4) <= S < 1, 'endpoint monotonicity domain')
        calculated_f = Q(2, 3) * (S ** 2 + (Q(3, 2) - S) ** 2)
        need(f == calculated_f, 'endpoint f wrong')
        need(margin == 1 - 1 / A - calculated_f and margin > 0, 'margin false/nonpositive')
        previous = B
        if B.denominator > 1:
            differences.append(str(T ** B.denominator - Q(3, 2) ** B.numerator))
    need(previous == 7, 'finite coverage ends early')
    need(differences == c['fractional_power_differences'], 'fractional power differences')
    need(differences == ['504313/1024000', '317/512'], 'power exact controls')
    # a^2(2-a)-1=(a-1)(1+a-a^2), as polynomial coefficient vectors.
    need(poly_mul([-1, 1], [1, 1, -1]) == [-1, 0, 2, -1], 'least monotonicity polynomial')
    # R'=2*a^5*(7*a-9), evaluated by exact differentiation and multiplication.
    R = [Q(2), 0, 0, 0, 0, 0, Q(-3), Q(2)]
    derivative = [i * R[i] for i in range(1, len(R))]
    need(derivative == poly_mul([0, 0, 0, 0, 0, 2], [-9, 7]), 'R derivative factorization')
    r_min = 2 * Q(9, 7) ** 7 - 3 * Q(9, 7) ** 6 + 2
    need(r_min == Q(c['R_min']) == Q(52763, 823543) and r_min > 0, 'R minimum value')
    need(1 - 2 * Q(2, 3) ** 2 == Q(1, 9), 'strict derivative lower bound')
    # C=3-sqrt(2), evaluated in Q[sqrt(2)]; these are identities, not samples.
    C = (Q(3), Q(-1))
    C_minus_one = q2_add(C, (Q(-1), Q(0)))
    need(q2_add(q2_mul(C, C), C) == q2_mul((Q(7), Q(0)), C_minus_one), 'tail quadratic-field identity')
    need(Q(7, 5) ** 2 < 2 < Q(2) ** 2, 'sqrt2 strict comparisons')
    # exp(8/5) Taylor partial and geometric tail; monotone ratios are proved in REPORT.
    tail = c['exp_tail']
    x = Q(tail['argument_cap'])
    need(x == Q(8, 5), 'exponential argument cap')
    need(tail['partial_through_degree'] == 4 and tail['tail_first_degree'] == 5, 'Taylor split')
    partial = sum((x ** k / factorial(k) for k in range(5)), Q(0))
    need(partial == Q(tail['partial_sum']) == Q(9067, 1875), 'partial sum')
    ratio = x / 6
    need(ratio == Q(tail['ratio_cap']) == Q(4, 15) and 0 <= ratio < 1, 'tail ratio')
    tail_bound = x ** 5 / factorial(5) / (1 - ratio)
    need(tail_bound == Q(tail['tail_bound']) == Q(4096, 34375), 'geometric tail bound')
    combined = partial + tail_bound
    need(combined == Q(tail['combined_bound']) == Q(510973, 103125), 'combined Taylor bound')
    need(tail['final_integer_cap'] == 6 and combined < 6, 'exponential final strict cap')
    return {'intervals': 5, 'strict_positive_margins': 5, 'fractional_caps': 2,
            'closed_endpoint': '17/4', 'analytic_tail_from': '7'}


def negative_controls(c):
    controls = []
    bad = deepcopy(c); bad['rows'][0]['T'] = '5'; controls.append(('inadequate power cap', bad))
    bad = deepcopy(c); bad['rows'][0]['margin'] = '0'; controls.append(('changed rational margin', bad))
    bad = deepcopy(c); bad['rows'][1]['A'] = '87/20'; controls.append(('interval gap', bad))
    bad = deepcopy(c); bad['rows'].pop(); controls.append(('omitted interval', bad))
    bad = deepcopy(c); bad['claim_scope']['lower_endpoint'] = '4/3'; controls.append(('unsupported lower endpoint', bad))
    bad = deepcopy(c); bad['exp_tail']['tail_bound'] = '0'; controls.append(('bad exponential tail', bad))
    bad = deepcopy(c); bad['claim_scope']['equal_rates_only'] = False; controls.append(('unequal-rate scope claim', bad))
    rejected = []
    for label, bad in controls:
        try:
            validate_math(bad)
        except VerificationError:
            rejected.append(label)
        else:
            raise VerificationError('negative control unexpectedly passed: ' + label)
    return rejected


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', required=True)
    args = parser.parse_args()
    pin = args.manifest_sha256.lower()
    need(len(pin) == 64 and all(ch in '0123456789abcdef' for ch in pin), 'invalid external digest')
    root = Path(__file__).resolve().parent
    members = {'REPORT.md', 'EXACT_CERTIFICATE.json', 'SOURCES.json', 'VERIFY.py', 'MANIFEST.json'}
    need({p.name for p in root.iterdir()} == members, 'public inventory mismatch')
    for p in root.iterdir():
        need(p.is_file() and not p.is_symlink(), 'non-regular public member')
    manifest_bytes = (root / 'MANIFEST.json').read_bytes()
    need(sha256(manifest_bytes).hexdigest() == pin, 'external manifest digest mismatch')
    manifest = json.loads(manifest_bytes)
    need(set(manifest['members']) == members and len(manifest['members']) == 5, 'manifest members')
    entries = manifest['entries']
    need({e['file'] for e in entries} == members - {'MANIFEST.json'} and len(entries) == 4, 'manifest entries')
    for entry in entries:
        data = (root / entry['file']).read_bytes()
        need(len(data) == entry['bytes'] and sha256(data).hexdigest() == entry['sha256'], 'member digest: ' + entry['file'])
    c = json.loads((root / 'EXACT_CERTIFICATE.json').read_bytes())
    need(c['head'] == 'bacae693a1f2a33c89565b0bd716620885831289', 'head identity')
    need(c['base'] == 'f6caddda8f8be2cdb3e91494325d8f7f365bc3fc', 'base identity')
    need(len(c['inputs']) == 8, 'bound input count')
    need(c['inputs']['PROOF.md']['sha256'] == '791ec6c1f849840785afd8ce15e4460b396e108bc2b203d93993cfb0a6103340', 'actual proof identity')
    need(c['inputs']['MATHEMATICAL_AUDIT.md']['sha256'] == '621bded8b4a04118ae17a16930f53e022216ac51223dc5d562c65319826de515', 'actual audit identity')
    result = validate_math(c)
    result['negative_controls_rejected'] = negative_controls(c)
    result['offline'] = True
    result['read_only'] = True
    result['external_manifest_sha256'] = pin
    result['written_proof_and_published_dependency_still_required'] = True
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
