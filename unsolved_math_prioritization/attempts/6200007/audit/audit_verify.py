#!/usr/bin/env python3
"""Read-only frozen-packet replay and independent finite audit controls.

Usage: python3 audit_verify.py AUTHOR_PACKET_DIRECTORY
These controls do not replace the infinite or topological proofs.
"""
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys


MANIFEST_HASH = '5f02f43dd7fad57a3bfb65205a7d53be2d9d0e42896870c8bc3aa77f72bc63b7'
PROOF_HASH = '648d14899fc0f26848a59019328179cff8ab2658bbbe866a87c541b637dc34f2'
COUNTS = {}


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def check(condition, label):
    require(condition, label)
    COUNTS[label] = COUNTS.get(label, 0) + 1


def digest(data):
    return hashlib.sha256(data).hexdigest()


def distance(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]:
        k += 1
    return len(a) + len(b) - 2 * k


def main():
    require(len(sys.argv) == 2, 'one author-packet directory argument required')
    root = Path(sys.argv[1]).resolve()
    manifest_data = (root / 'SHA256SUMS.json').read_bytes()
    require(digest(manifest_data) == MANIFEST_HASH, 'frozen manifest identity')
    require(digest((root / 'TURN_4.md').read_bytes()) == PROOF_HASH, 'frozen main proof identity')
    manifest = json.loads(manifest_data)
    listed = set()
    for entry in manifest['files']:
        path = Path(entry['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'relative manifest path')
        data = (root / path).read_bytes()
        require(len(data) == entry['bytes'], 'author file byte length')
        require(digest(data) == entry['sha256'], 'author file SHA-256')
        listed.add(str(path))
    require(len(listed) == 14, 'fourteen author manifest entries')
    require({p.name for p in root.iterdir() if p.is_file()} == listed | {'SHA256SUMS.json'},
            'exact fifteen-file author inventory')
    replay = subprocess.run([sys.executable, str(root / 'verify.py')], cwd=root,
                            check=True, capture_output=True).stdout
    require(replay == (root / 'CHECKS.json').read_bytes(), 'exact author replay bytes')
    report = json.loads(replay)
    require(report['status'] == 'PASS' and report['total_assertions'] == 59002,
            'author assertion count and status')

    # Exhaustive bounded determinant-one enumeration, independent of generator words.
    matrix_count = 0
    for a, b, c, d in itertools.product(range(-8, 9), repeat=4):
        if a * d - b * c != 1:
            continue
        matrix_count += 1
        u2, v2, dot = a * a + c * c, b * b + d * d, a * b + c * d
        check(u2 >= 1 and v2 >= 1, 'nonzero_integer_column_norms')
        check(u2 * v2 - dot * dot == 1, 'lagrange_angle_identity')
        check(Fraction(1, u2 * v2) <= Fraction(1, v2), 'column_angle_bound')

    # Exact chordal squared distances on RP^1 for the parabolic witnesses.
    previous = Fraction(1, 1)
    for n in range(1, 4097):
        gap = Fraction(1, (n * n + 1) * ((n + 1) ** 2 + 1))
        infinity_gap = Fraction(1, n * n + 1)
        check(gap < previous, 'parabolic_pair_distance_decreases')
        check(gap <= Fraction(1, n ** 4), 'parabolic_pair_distance_bound')
        check(infinity_gap <= Fraction(1, n * n), 'parabolic_infinity_distance_bound')
        previous = gap

    # Base-point product inequality on every quadruple in a depth-three binary tree.
    nodes = [''] + [''.join(w) for length in range(1, 4)
                    for w in itertools.product('01', repeat=length)]
    distances = {(a, b): distance(a, b) for a in nodes for b in nodes}
    for x, y, o, p in itertools.product(nodes, repeat=4):
        twice_o = distances[x, o] + distances[y, o] - distances[x, y]
        twice_p = distances[x, p] + distances[y, p] - distances[x, y]
        check(abs(twice_o - twice_p) <= 2 * distances[o, p], 'basepoint_product_inequality')

    for a, b, p, t in itertools.permutations(range(4)):
        terms = [(set(u), set(v))
                 for u in itertools.combinations((a, b, p), 2)
                 for v in itertools.combinations((a, t, p), 2)]
        survivors = [(u, v) for u, v in terms if not u.intersection(v)]
        check(len(terms) == 9 and len(survivors) == 2,
              'nine_terms_seven_intersections')
        check({(frozenset(u), frozenset(v)) for u, v in survivors} ==
              {(frozenset((a, b)), frozenset((t, p))),
               (frozenset((b, p)), frozenset((a, t)))},
              'two_surviving_crossratios')

    result = {
        'problem_id': 6200007,
        'status': 'PASS',
        'author_manifest_sha256': MANIFEST_HASH,
        'author_main_proof_sha256': PROOF_HASH,
        'verified_author_files_including_manifest': 15,
        'author_replay_assertions': 59002,
        'author_replay_byte_identical': True,
        'author_replay_sha256': digest(replay),
        'additional_matrix_representatives': matrix_count,
        'additional_checks': dict(sorted(COUNTS.items())),
        'additional_total_assertions': sum(COUNTS.values()),
        'arithmetic': 'integers_and_exact_rationals',
        'limits': [
            'Finite controls do not prove compactness, nonconicality, or a boundary theorem.',
            'The general prescribed-boundary realization problem is not solved by this audit.',
            'Additional assertion counts are separate from the frozen author count.'
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
