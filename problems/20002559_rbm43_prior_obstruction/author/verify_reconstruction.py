#!/usr/bin/env python3
"""Independent, solver-free reconstruction of the cited RBM(4,3) certificate.

Inputs are external published files, deliberately excluded from this package.
No producer executable is loaded or run. All 8**8 selectors are covered without
hidden-state normalization. Python 3.10+; standard library only.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import permutations, product
import json
from pathlib import Path
import re
import sys

SUPPORT = (0, 1, 2, 4, 7, 9, 10, 12)
EXPECTED_CERTIFICATE = '451797a35b04ef35c603b872cc965fc6adebaf43da49dc4b1ac3a6e32b34f1e7'
EXPECTED_APPENDIX = '7e4ac6e492f2e1278f82b4c91dddd15de8f7e014beb3c2d62a63a6f3fe04e3f0'

def need(condition, message):
    if not condition:
        raise ValueError(message)

def bits(n, length):
    return tuple((n >> (length - 1 - i)) & 1 for i in range(length))

def features(joint):
    v, h = divmod(joint, 8)
    x, y = bits(v, 4), bits(h, 3)
    return (1,) + x + y + tuple(a*b for a in x for b in y)

FEATURES = tuple(features(j) for j in range(128))

def cube_maps(d):
    for order in permutations(range(d)):
        for flip in range(1 << d):
            yield tuple(sum(bits(v, d)[order[i]] << (d-1-i) for i in range(d)) ^ flip for v in range(1 << d))

def validate_identity(left, right):
    need(left and len(left) == len(right), 'unequal or empty degrees')
    need(all(type(j) is int and 0 <= j < 128 for j in left + right), 'invalid joint index')
    need(all(j//8 in SUPPORT for j in right), 'right state outside support')
    for k in range(20):
        need(sum(FEATURES[j][k] for j in left) == sum(FEATURES[j][k] for j in right), 'feature imbalance')
    outside = sum(j//8 not in SUPPORT for j in left)
    need(outside > 0 and len(left) <= 4*outside, 'missing leakage or ratio bound')
    return len(left), outside

def from_printed_appendix(text):
    rows = []
    for line in text.splitlines():
        if not re.match(r'^\|\s*\d+\s*\|', line):
            continue
        cells = [x.strip() for x in line.split('|')[1:-1]]
        need(len(cells) == 5, 'malformed printable row')
        number, left, right, degree, outside = cells
        need(int(number) == len(rows)+1, 'nonconsecutive printable row')
        left = [int(v) for v in left.split(',')]
        right = [int(v) for v in right.split(',')]
        need(validate_identity(left, right) == (int(degree), int(outside)), 'incorrect printable degree metadata')
        rows.append((left, right))
    need(len(rows) == 42, 'missing printable rows')
    return rows

def compare_json(data, rows):
    need(data['support'] == list(SUPPORT), 'incorrect target')
    need(len(data['cuts']) == len(rows), 'JSON row count')
    for cut, (left, right) in zip(data['cuts'], rows):
        jl, jr = [], []
        for joint, exponent in cut['left']:
            need(type(exponent) is int and exponent > 0, 'bad left multiplicity')
            jl += [joint]*exponent
        for index, hidden, exponent in cut['right']:
            need(type(index) is int and 0 <= index < 8, 'bad support index')
            need(type(hidden) is int and 0 <= hidden < 8, 'bad hidden index')
            need(type(exponent) is int and exponent > 0, 'bad right multiplicity')
            jr += [8*SUPPORT[index]+hidden]*exponent
        need(sorted(jl) == sorted(left) and sorted(jr) == sorted(right), 'printed/JSON disagreement')

def reconstruct(rows):
    visible = [p for p in cube_maps(4) if {p[x] for x in SUPPORT} == set(SUPPORT)]
    hidden = list(cube_maps(3))
    need(len(visible) == 6 and len(hidden) == 48, 'cube symmetry census')
    position = {s: i for i, s in enumerate(SUPPORT)}
    patterns = set()
    transformed = 0
    max_degree, max_ratio = 0, Fraction(0)
    for left, right in rows:
        for vm in visible:
            for hm in hidden:
                def transform(j):
                    return 8*vm[j//8]+hm[j%8]
                ll, rr = list(map(transform, left)), list(map(transform, right))
                degree, outside = validate_identity(ll, rr)
                transformed += 1
                max_degree = max(max_degree, degree)
                max_ratio = max(max_ratio, Fraction(degree, outside))
                assignment = {}
                for j in rr:
                    i, h = position[j//8], j%8
                    need(i not in assignment or assignment[i] == h, 'right side conflicts as selector')
                    assignment[i] = h
                patterns.add(tuple(sorted(assignment.items())))

    # Index an unrestricted selector by its eight base-eight digits. Each
    # pattern fixes some digits. Enumerating the complement digits gives its
    # exact cylinder; there is no symmetry quotient in this enumeration.
    count = 8**8
    covered = bytearray(count)
    markings = 0
    for pattern in sorted(patterns):
        fixed = dict(pattern)
        origin = sum(h << (3*i) for i,h in pattern)
        free = [i for i in range(8) if i not in fixed]
        if not free:
            covered[origin] = 1
            markings += 1
            continue
        last = free.pop()
        stride = 1 << (3*last)
        for values in product(range(8), repeat=len(free)):
            start = origin + sum(h << (3*i) for i,h in zip(free, values))
            covered[start:start+8*stride:stride] = b'\1'*8
            markings += 8
    total = covered.count(1)
    need(total == count, 'uncovered selector, first index '+str(covered.find(0)))
    return {
        'visible_symmetries': len(visible), 'hidden_symmetries': len(hidden),
        'base_identities': len(rows), 'transformed_identities_checked': transformed,
        'unnormalized_partial_assignments': len(patterns),
        'unnormalized_selectors': count, 'covered_selectors': total,
        'markings_with_overlap': markings, 'maximum_degree': max_degree,
        'maximum_degree_over_outside': str(max_ratio),
        'coverage_sha256': hashlib.sha256(covered).hexdigest(),
    }

def exact_controls():
    eps = Fraction(1, 2**25)
    qplus_inside, qplus_outside = Fraction(1,8)*(1-eps)+eps/16, eps/16
    need(8*(qplus_inside+qplus_outside) == 1, 'qplus normalization')
    need(qplus_inside > 0 and qplus_outside > 0, 'qplus positivity')
    need(8*qplus_outside < (qplus_inside/8)**4, 'positive exclusion inequality')
    need(Fraction(15,1024)**4 > eps, 'TV rational bound')
    need(eps/2 == Fraction(1,2**26), 'TV transfer')
    return {'positive_target_normalized': True, 'positive_target_violates_inequality': True,
            'uniform_support_tv_bound': str(eps), 'positive_target_tv_bound': str(eps/2)}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificate', type=Path)
    ap.add_argument('appendix', type=Path)
    args = ap.parse_args()
    certificate, appendix = args.certificate.read_bytes(), args.appendix.read_bytes()
    # Digests are reported, not used as a substitute for semantic validation.
    rows = from_printed_appendix(appendix.decode('utf-8'))
    compare_json(json.loads(certificate), rows)
    result = reconstruct(rows)
    result.update(exact_controls())
    result.update({'status': 'PASS_INDEPENDENT_FULL_SELECTOR_RECONSTRUCTION',
                   'certificate_sha256': hashlib.sha256(certificate).hexdigest(),
                   'appendix_sha256': hashlib.sha256(appendix).hexdigest(),
                   'certificate_expected_hash_match': hashlib.sha256(certificate).hexdigest() == EXPECTED_CERTIFICATE,
                   'appendix_expected_hash_match': hashlib.sha256(appendix).hexdigest() == EXPECTED_APPENDIX,
                   'implementation': 'new standard-library implementation; no producer code executed',
                   'python_optimized': sys.flags.optimize})
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
