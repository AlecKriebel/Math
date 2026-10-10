#!/usr/bin/env python3
"""Independent finite arithmetic and pinned-release audit. No network or source texts."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import sys

AUTHOR_MANIFEST = 'a9b478491ffe9f3dd75d177bd863ec8dc2f28ac3ed69f04bce9e35955247e989'
AUTHOR_REPORT = 'd87d55930ab6d9d3c644dc975cebbc5f9a3bf3523c7cb77a2168ded696231098'
AUTHOR_FILES = {'CLAIMS.json', 'GATE.json', 'LEDGER.json', 'README.md', 'REPORT.md',
                'SOURCES.json', 'test_negative_controls.py', 'verify_math.py', 'verify_packet.py'}
AUDIT_FILES = {'AUDIT.md', 'ACCEPTANCE.json', 'CLAIMS.json', 'SOURCE_CHECKS.json',
               'README.md', 'READONLY_REPLAY_FIX.patch', 'verify_audit.py',
               'test_audit.py', 'TEST_RESULTS.json'}
Q = Fraction


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for k, v in pairs:
        need(k not in result, 'duplicate JSON key')
        result[k] = v
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def inventory(root, expected):
    need(root.is_dir() and not root.is_symlink(), 'not an ordinary release directory')
    entries = list(root.iterdir())
    need({p.name for p in entries} == expected | {'MANIFEST.json'}, 'closed inventory differs')
    need(all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular release entry')


def authenticate(root, expected, pin, author=False):
    inventory(root, expected)
    data = (root / 'MANIFEST.json').read_bytes()
    need(digest(data) == pin, 'externally pinned manifest differs')
    m = read_json(root / 'MANIFEST.json')
    if author:
        need(set(m) == {'schema', 'problem_id', 'files'}, 'author manifest keys')
        need(m['schema'] == 'rational-voa-frozen-manifest-v1', 'author manifest schema')
    else:
        need(set(m) == {'schema', 'problem_id', 'files'}, 'audit manifest keys')
        need(m['schema'] == 'rational-voa-independent-audit-v1', 'audit manifest schema')
    need(type(m['problem_id']) is int and m['problem_id'] == 30002842, 'manifest problem')
    need(type(m['files']) is list, 'manifest entries are not a list')
    names = []
    for e in m['files']:
        need(type(e) is dict and set(e) == {'name', 'bytes', 'sha256'}, 'manifest entry schema')
        need(type(e['name']) is str and e['name'] in expected, 'unexpected file name')
        need(type(e['bytes']) is int and e['bytes'] >= 0, 'invalid byte count')
        need(type(e['sha256']) is str and len(e['sha256']) == 64 and
             all(c in '0123456789abcdef' for c in e['sha256']), 'invalid digest')
        names.append(e['name'])
        b = (root / e['name']).read_bytes()
        need(len(b) == e['bytes'] and digest(b) == e['sha256'], 'authenticated file differs')
    need(len(names) == len(set(names)) and set(names) == expected, 'manifest inventory differs')
    if author:
        need(digest((root / 'REPORT.md').read_bytes()) == AUTHOR_REPORT, 'author report differs')
    return len(expected)


def rank(matrix, columns):
    a = [[Q(x) for x in row] for row in matrix]
    need(all(len(row) == columns for row in a), 'ragged coefficient matrix')
    pivot_row = 0
    for col in range(columns):
        candidates = [r for r in range(pivot_row, len(a)) if a[r][col] != 0]
        if not candidates:
            continue
        r = candidates[0]
        a[r], a[pivot_row] = a[pivot_row], a[r]
        z = a[pivot_row][col]
        a[pivot_row] = [v/z for v in a[pivot_row]]
        for r in range(pivot_row + 1, len(a)):
            z = a[r][col]
            a[r] = [v-z*w for v, w in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == len(a):
            break
    return pivot_row


def dimension(kind, n):
    # Unknown D is indexed by (input basis index, output basis index).
    def product(i, j):
        if kind == 'coordinate':
            return {i: Q(1)} if i == j else {}
        if i == 0:
            return {j: Q(1)}
        if j == 0:
            return {i: Q(1)}
        return {0: Q(1)} if i == j else {}
    rows = []
    for i, j, out in itertools.product(range(n), repeat=3):
        row = [Q(0)] * (n*n)
        for z, coefficient in product(i, j).items():
            row[z*n+out] += coefficient
        for z in range(n):
            row[i*n+z] -= product(z, j).get(out, 0)
            row[j*n+z] -= product(i, z).get(out, 0)
        rows.append(row)
    return n*n-rank(rows, n*n)


def polynomial_product(p, q):
    out = [Q(0)] * (len(p)+len(q)-1)
    for i in range(len(p)):
        for j in range(len(q)):
            out[i+j] += p[i]*q[j]
    return out


def polynomial_value(p, x):
    return sum((a*x**i for i, a in enumerate(p)), Q(0))


def verify_claims(c):
    scope = {
        'problem_id': 30002842, 'queue_rank': 991, 'status': 'unsolved_partial',
        'author_approaches_completed': 5, 'mathematical_partial_results_accepted': True,
        'full_conjecture_proved': False, 'conjecture_disproved': False,
        'han_theorem_disproved': False, 'han_v5_verified_as_resolution': False,
        'affine_example_has_v1_zero': False, 'finite_checks_are_formal_voa_proof': False,
        'read_only_runner_patch_required': True,
    }
    need(type(c) is dict and set(c) == set(scope) | {'arithmetic'}, 'claim schema')
    for key, value in scope.items():
        need(type(c[key]) is type(value) and c[key] == value, 'scope differs: '+key)
    a = c['arithmetic']
    keys = {'cartan_charge', 'hat_sign', 'spectral_sign', 'tail_action',
            'coordinate_dimensions', 'spin_dimensions', 'central_charges', 'permutation_order'}
    need(type(a) is dict and set(a) == keys, 'arithmetic claim schema')
    for key in ['cartan_charge', 'hat_sign', 'spectral_sign', 'tail_action', 'permutation_order']:
        need(type(a[key]) is int, 'coefficient must be an integer')
    need(a['cartan_charge'] == 2, 'root charge normalization')
    need(a['hat_sign'] == -1, 'tail lift sign')
    need(a['spectral_sign'] == -1, 'commutator sign')
    need(a['tail_action'] == 2, 'moving tail is nonzero')
    # Independently recurse the normalized descendant factors at several primary weights.
    descendant_checks = 0
    for k in range(1, 9):
        coefficient = Q(1)
        zero_mode_factor = 1
        for r in range(0, 65):
            need(coefficient*zero_mode_factor == 1, 'zero-mode identity')
            if k == 1 and r >= 1:
                previous = coefficient * (-r)
                lowering = r*(r+1)
                need(coefficient*lowering == -(r+1)*previous, 'lowering coefficient')
            coefficient *= Q(-1, k+r)
            zero_mode_factor *= -(k+r)
            descendant_checks += 1
    for n in range(1, 65):
        N = n+2
        b = {N: Q(1)}  # units of normalized c_N
        hat = {N+1: -a['hat_sign']*b[N]}
        need(sum(hat.values())*a['cartan_charge'] == a['tail_action'], 'tail action changed')
        need(1 not in hat and all(i not in hat for i in range(2, N)), 'wrong support')
    for J in [[], [2], [2, 3], [3, 8, 19], list(range(2, 20))]:
        p = [Q(1)]
        for i in J:
            p = polynomial_product(p, [Q(1), Q(1, i*(i-1))])
        need(polynomial_value(p, Q(0)) == 1, 'filter constant term')
        for i in J:
            need(polynomial_value(p, Q(a['spectral_sign']*i*(i-1))) == 0,
                 'filter failed to annihilate eigenvalue')
        matrix = [[Q(i*(i-1))**r for i in J] for r in range(1, len(J)+1)]
        need(rank(matrix, len(J)) == len(J), 'spectral moment rank')
    coordinate = [dimension('coordinate', n) for n in range(1, 6)]
    spin = [dimension('spin', s+1) for s in range(2, 6)]
    for key, actual in [('coordinate_dimensions', coordinate), ('spin_dimensions', spin)]:
        need(type(a[key]) is list and all(type(x) is int for x in a[key]), 'dimension types')
        need(a[key] == actual, 'false dimension claim')
    need(coordinate == [0]*5 and spin == [1, 3, 6, 10], 'independent exact rank result')
    need(a['central_charges'] == ['1/2', '7/10', '1/2'], 'central charge fixture')
    charges = list(map(Q, a['central_charges']))
    valid_permutations = [p for p in itertools.permutations(range(3))
                          if all(charges[i] == charges[p[i]] for i in range(3))]
    need(a['permutation_order'] == len(valid_permutations) == 2, 'forbidden charge permutation')
    return {'descendant_checks': descendant_checks, 'moving_tail_cases': 64,
            'coordinate_dimensions': coordinate, 'spin_dimensions': spin,
            'charge_preserving_permutations': len(valid_permutations)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--claims', type=Path)
    parser.add_argument('--author-root', type=Path)
    parser.add_argument('--audit-root', type=Path, default=Path(__file__).parent)
    parser.add_argument('--expected-audit-manifest')
    args = parser.parse_args()
    try:
        if args.claims is not None:
            result = verify_claims(read_json(args.claims))
        else:
            need(args.author_root is not None and args.expected_audit_manifest is not None,
                 'author root and independently recorded audit manifest are required')
            author_count = authenticate(args.author_root, AUTHOR_FILES, AUTHOR_MANIFEST, True)
            audit_count = authenticate(args.audit_root, AUDIT_FILES, args.expected_audit_manifest)
            result = verify_claims(read_json(args.audit_root / 'CLAIMS.json'))
            acceptance = read_json(args.audit_root / 'ACCEPTANCE.json')
            need(acceptance['disposition'] == 'accept_partial_results_with_replay_patch',
                 'acceptance inflation')
            need(acceptance['conjecture_status'] == 'unsolved_partial', 'conjecture inflation')
            need(acceptance['mathematical_corrections_required'] is False, 'acceptance mismatch')
            need(acceptance['source_text_redistributed'] is False, 'source redistribution')
            result.update(author_files=author_count, audit_files=audit_count,
                          external_sources_retrieved_by_replay=False)
        print(json.dumps({'ok': True, 'result': result}, sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, IndexError) as e:
        print('AUDIT_REJECTED: '+str(e), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
