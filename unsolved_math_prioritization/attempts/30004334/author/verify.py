#!/usr/bin/env python3
"""Portable exact checks for the authored root-of-unity blowup packet.

The geometric proofs are in PROOFS.md. This script checks only the explicitly
stated arithmetic certificates. It performs no network access or remote writes.
Checks use explicit exceptions and remain active under python -O.
"""
import argparse
import copy
from fractions import Fraction
import hashlib
import itertools
import json
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def neg(a):
    return -a[0], -a[1]


def mul(a, b):
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def div(a, b):
    den = b[0] ** 2 + b[1] ** 2
    require(den != 0, "Gaussian division by zero")
    return Fraction(a[0] * b[0] + a[1] * b[1], den), Fraction(a[1] * b[0] - a[0] * b[1], den)


ZERO = (0, 0)
ONE = (1, 0)
I_POWERS = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def dot(a, b):
    out = ZERO
    for x, y in zip(a, b):
        out = add(out, mul(x, y))
    return out


def cross(a, b):
    return tuple(add(mul(a[(j + 1) % 3], b[(j + 2) % 3]),
                     neg(mul(a[(j + 2) % 3], b[(j + 1) % 3]))) for j in range(3))


def normalized(a):
    scale = next(x for x in a if x != ZERO)
    return tuple(div(x, scale) for x in a)


def exact_grid_lines():
    indices = list(itertools.product(range(4), repeat=2))
    points = [(ONE, I_POWERS[a], I_POWERS[b]) for a, b in indices]
    lines = {normalized(cross(p, q)) for p, q in itertools.combinations(points, 2)}
    incidences = []
    for line in sorted(lines):
        incidences.append([indices[j] for j, p in enumerate(points) if dot(line, p) == ZERO])
    return incidences


def v_matrix(cert):
    require(cert['grid_order'] == 4, 'Wrong grid order')
    v = [[0] * 4 for _ in range(4)]
    seen = set()
    for a, b, value in cert['v_nonzero']:
        require(0 <= a < 4 and 0 <= b < 4 and (a, b) not in seen, 'Invalid v entry')
        seen.add((a, b))
        require(value in (-1, 1), 'Invalid v coefficient')
        v[a][b] = value
    require(sum(x * x for row in v for x in row) == 6, 'Wrong v norm')
    for t in range(4):
        require(sum(v[t]) == 0, 'Nonzero row sum')
        require(sum(v[a][t] for a in range(4)) == 0, 'Nonzero column sum')
        require(sum(v[a][(a + t) % 4] for a in range(4)) == 0, 'Nonzero diagonal sum')
    return v


def multiplicities(k, v):
    return [[2 * k * k + 2 * k * v[a][b] for b in range(4)] for a in range(4)]


def jet_matrix(k, v, prime=101, root=10):
    require(prime == 101 and root == 10, 'Certificate residue field changed')
    require((root * root + 1) % prime == 0, 'Invalid image of i')
    d = 8 * k * k + 1
    monomials = [(u, w) for u in range(d + 1) for w in range(d + 1 - u)]
    a = multiplicities(k, v)
    rows = []
    for j in range(4):
        for ell in range(4):
            x, y = pow(root, j, prime), pow(root, ell, prime)
            for r in range(a[j][ell]):
                for s in range(a[j][ell] - r):
                    rows.append([(comb(u, r) * comb(w, s) * pow(x, u - r, prime) * pow(y, w - s, prime)) % prime
                                 if u >= r and w >= s else 0 for u, w in monomials])
    return rows, monomials


def det_mod(matrix, p):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), 'Minor is not square')
    a = [row[:] for row in matrix]
    det = 1
    for c in range(n):
        pivot = next((r for r in range(c, n) if a[r][c] % p), None)
        if pivot is None:
            return 0
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            det = -det
        val = a[c][c] % p
        det = (det * val) % p
        inv = pow(val, -1, p)
        tail = [(x * inv) % p for x in a[c][c + 1:]]
        for r in range(c + 1, n):
            coefficient = a[r][c] % p
            if coefficient:
                a[r][c + 1:] = [(x - coefficient * y) % p for x, y in zip(a[r][c + 1:], tail)]
            a[r][c] = 0
    return det % p


def rank_check(rc, v):
    k = rc['k']
    require(k in (1, 2), 'Uncertified k')
    matrix, monomials = jet_matrix(k, v, rc['prime'], rc['i_mod_p'])
    require(rc['degree'] == 8 * k * k + 1, 'Wrong interpolation degree')
    require(rc['row_count'] == len(matrix), 'Wrong jet count')
    require(rc['column_count'] == len(monomials) == rc['rank'], 'Wrong claimed full rank')
    selected = rc['pivot_rows']
    require(len(selected) == len(monomials) and len(set(selected)) == len(selected), 'Invalid selected rows')
    require(all(type(t) is int and 0 <= t < len(matrix) for t in selected), 'Invalid row index')
    determinant = det_mod([matrix[t] for t in selected], rc['prime'])
    require(determinant != 0, 'Interpolation minor vanishes')
    return {'k': k, 'degree': rc['degree'], 'rows': len(matrix), 'columns': len(monomials),
            'prime': rc['prime'], 'minor_determinant_mod_prime': determinant, 'full_column_rank': True}


def complex_square(m, d):
    require(m >= 1 and d >= 1, 'Orders must be positive')
    return d * d - (4 if d % 3 == 0 else 2 if m % 3 == 0 else 0)


def mathematical_checks(cert, include_large_rank=True):
    require(cert['schema'] == 'root-unity-negativity-certificates-v1', 'Wrong schema')
    require(cert['problem_id'] == '30004334' and cert['base_field'] == 'C', 'Wrong target')
    require(cert['relaxation_is_not_curve_construction'] is True, 'Numerical classes misidentified as curves')
    v = v_matrix(cert)
    incidences = exact_grid_lines()
    counts = {}
    for line in incidences:
        counts[str(len(line))] = counts.get(str(len(line)), 0) + 1
    require(counts == cert['expected_line_counts'], 'Wrong exact line-incidence census')
    pair_coverage = sum(comb(len(line), 2) for line in incidences)
    require(pair_coverage == comb(16, 2), 'Point pairs not covered exactly')
    tested = 0
    for k in range(1, 101):
        a = multiplicities(k, v)
        d = 8 * k * k + 1
        S, Q = sum(map(sum, a)), sum(x * x for row in a for x in row)
        require(min(x for row in a for x in row) >= 0, 'Negative multiplicity')
        require(S == 32 * k * k and Q == 64 * k ** 4 + 24 * k * k, 'Moment identity failed')
        square, canonical, fiber = d * d - Q, -3 * d + S, 4 * d - S
        require(square == 1 - 8 * k * k and canonical == 8 * k * k - 3 and fiber == 4,
                'Intersection identity failed')
        require(square + canonical == -2, 'Genus identity failed')
        for line in incidences:
            require(sum(a[r][s] for r, s in line) <= d, 'Line-Bezout test failed')
            tested += 1
        if k >= 3:
            require(square < -62, 'Weak-negativity exclusion threshold failed')
    for item in cert['complex_power_examples']:
        require(complex_square(item['m'], item['d']) == item['self_intersection'], 'Wrong complex power-image square')
    power_cases = 0
    for m in range(1, 41):
        for d in range(1, 101):
            value = complex_square(m, d)
            require(value >= 0 or (d == 1 and m % 3 == 0 and value == -1), 'Unexpected negative power-image case')
            power_cases += 1
    require(complex_square(4, 6) == 32 and 6 * (3 - 4) - 1 == -7, 'Characteristic separation failed')
    rank_results = [rank_check(rc, v) for rc in cert['rank_certificates'] if include_large_rank or rc['k'] == 1]
    expected_k = [1, 2] if include_large_rank else [1]
    require([r['k'] for r in rank_results] == expected_k, 'Missing or repeated rank certificate')
    return {'schema': 'root-unity-negativity-checks-v1', 'status': 'pass',
            'scope': 'Exact arithmetic certificates only; general complex problem unresolved',
            'gaussian_rational_grid_points': 16, 'exact_lines_determined_by_pairs': len(incidences),
            'line_size_census': counts, 'pair_coverage': pair_coverage,
            'numerical_family_k_range': [1, 100], 'line_bezout_checks': tested,
            'power_image_formula_cases': power_cases, 'interpolation_certificates': rank_results}


def negative_controls(cert):
    tests = []
    def rejected(label, action):
        try:
            action()
        except (ValueError, KeyError, IndexError, TypeError):
            tests.append(label)
            return
        raise ValueError('Negative control was not rejected: ' + label)
    c = copy.deepcopy(cert); c['grid_order'] = 5
    rejected('wrong_grid_order', lambda: v_matrix(c))
    c = copy.deepcopy(cert); c['v_nonzero'][0][2] = -1
    rejected('perturbed_zero_sum_pattern', lambda: v_matrix(c))
    c = copy.deepcopy(cert); c['complex_power_examples'][0]['self_intersection'] = -7
    rejected('characteristic_p_formula_substituted_over_C', lambda: mathematical_checks(c, False))
    c = copy.deepcopy(cert); c['relaxation_is_not_curve_construction'] = False
    rejected('numerical_feasibility_claimed_as_realized_curve', lambda: mathematical_checks(c, False))
    r = copy.deepcopy(cert['rank_certificates'][0]); r['pivot_rows'][0] = r['pivot_rows'][1]
    rejected('duplicated_interpolation_row', lambda: rank_check(r, v_matrix(cert)))
    r = copy.deepcopy(cert['rank_certificates'][0]); r['rank'] -= 1
    rejected('altered_full_rank_claim', lambda: rank_check(r, v_matrix(cert)))
    require(det_mod([[1, 2], [2, 4]], 101) == 0, 'Singular determinant control failed')
    tests.append('singular_minor_recognized')
    return tests


def check_manifest(expected=None):
    path = ROOT / 'AUTHOR_MANIFEST.json'
    require(path.is_file(), 'Author manifest missing')
    raw = path.read_bytes()
    if expected:
        require(sha(raw) == expected.lower(), 'Pinned manifest hash mismatch')
    manifest = json.loads(raw)
    require(manifest['schema'] == 'root-unity-author-manifest-v1', 'Wrong manifest schema')
    files = manifest['files']
    require(len(files) == len({x['path'] for x in files}), 'Duplicate manifest entry')
    actual = {x.relative_to(ROOT).as_posix() for x in ROOT.rglob('*') if x.is_file()}
    listed = {x['path'] for x in files}
    require(actual == listed | {'AUTHOR_MANIFEST.json'}, 'Packet file inventory mismatch')
    for item in files:
        name = item['path']
        require('/' not in name and '\\' not in name and name not in ('.', '..'), 'Unsafe manifest path')
        f = ROOT / name
        require(not f.is_symlink(), 'Packet symlink forbidden')
        data = f.read_bytes()
        require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'File integrity mismatch: ' + name)
    return sha(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--write-checks', action='store_true', help='Authoring only: generate deterministic check record before freeze')
    args = parser.parse_args()
    cert = json.loads((ROOT / 'CERTIFICATES.json').read_text())
    if not args.write_checks:
        digest = check_manifest(args.expected_manifest)
    results = mathematical_checks(cert)
    if args.write_checks:
        require(not (ROOT / 'AUTHOR_MANIFEST.json').exists(), 'Do not overwrite checks in a frozen packet')
        (ROOT / 'CHECK_RESULTS.json').write_text(json.dumps(results, indent=2, sort_keys=True) + '\n')
    else:
        require(results == json.loads((ROOT / 'CHECK_RESULTS.json').read_text()), 'Recorded check results differ from replay')
        results = {'mathematical_checks': results, 'manifest_sha256': digest}
    if args.self_test:
        results['negative_controls_rejected'] = negative_controls(cert)
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
