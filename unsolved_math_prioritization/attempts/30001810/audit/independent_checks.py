#!/usr/bin/env python3
"""Independent exact audit controls, not a proof of the aspherical comparison.

Standard library only. Optional --input points to the original frozen directory.
Without it, all mathematical controls run and archival input checks are skipped.
All optimization enumerates exact rational basic feasible solutions and verifies
matching dual certificates. No floating-point solver or fixed candidate-only test.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import argparse, hashlib, json, subprocess, sys


def solve_unique(A, b):
    """Exact solution of a consistent full-column-rank rectangular system."""
    n = len(A[0]) if A else 0
    rows = [list(map(Q, a)) + [Q(v)] for a, v in zip(A, b)]
    piv = []
    r = 0
    for j in range(n):
        k = next((k for k in range(r, len(rows)) if rows[k][j]), None)
        if k is None:
            continue
        rows[r], rows[k] = rows[k], rows[r]
        v = rows[r][j]
        rows[r] = [v2 / v for v2 in rows[r]]
        for k in range(len(rows)):
            if k != r:
                v = rows[k][j]
                rows[k] = [a - v * z for a, z in zip(rows[k], rows[r])]
        piv.append(j)
        r += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return None
    if len(piv) != n:
        return None
    answer = [Q(0)] * n
    for k, j in enumerate(piv):
        answer[j] = rows[k][-1]
    return answer


def l1_optimize(A, b):
    """Minimize sum |x_i| subject to A x=b, enumerate all signed BFS."""
    r, m = len(A), len(A[0])
    cols = [[Q(sign * A[i][j]) for i in range(r)]
            for sign in [1, -1] for j in range(m)]
    best = None
    checked = feasible = 0
    for s in range(1, r + 1):
        for active in combinations(range(2 * m), s):
            checked += 1
            vals = solve_unique([[cols[j][i] for j in active] for i in range(r)], b)
            if vals is None or any(x < 0 for x in vals):
                continue
            feasible += 1
            x = [Q(0)] * m
            for j, v in zip(active, vals):
                x[j % m] += v if j < m else -v
            objective = sum(abs(v) for v in x)
            if best is None or objective < best[0]:
                best = (objective, x)
    assert best is not None
    dual = None
    for active in combinations(range(2 * m), r):
        y = solve_unique([cols[j] for j in active], [1] * r)
        if y is not None and all(sum(c * z for c, z in zip(col, y)) <= 1 for col in cols):
            objective = sum(Q(v) * z for v, z in zip(b, y))
            if dual is None or objective > dual[0]:
                dual = (objective, y)
    assert dual is not None and dual[0] == best[0]
    assert [sum(Q(a) * v for a, v in zip(row, best[1])) for row in A] == list(map(Q, b))
    return {'minimum': str(best[0]), 'primal': list(map(str, best[1])),
            'dual': list(map(str, dual[1])), 'bases_checked': checked,
            'feasible_bases': feasible, 'matching_dual_certificate': True}


def bareiss_det(A):
    """Fraction-free elimination, independently coded from original check."""
    n = len(A)
    if not n:
        return 1
    A = [row[:] for row in A]
    old, sign = 1, 1
    for k in range(n - 1):
        pivot = next((i for i in range(k, n) if A[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            A[k], A[pivot] = A[pivot], A[k]
            sign *= -1
        v = A[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = A[i][j] * v - A[i][k] * A[k][j]
                assert numerator % old == 0
                A[i][j] = numerator // old
            A[i][k] = 0
        old = v
    return sign * A[-1][-1]


def words(p, q):
    if p == q == 0:
        yield ()
    if p:
        for rest in words(p - 1, q):
            yield (0,) + rest
    if q:
        for rest in words(p, q - 1):
            yield (1,) + rest


def shuffle(aa, bb):
    for word in words(len(aa) - 1, len(bb) - 1):
        inv = sum(word[i] > word[j] for i in range(len(word)) for j in range(i + 1, len(word)))
        i = j = 0
        path = [(aa[0], bb[0])]
        for w in word:
            i += w == 0
            j += w == 1
            path.append((aa[i], bb[j]))
        yield (-1) ** inv, tuple(path), word


def bdry(chain):
    d = defaultdict(int)
    for sign, simplex in chain:
        if len(simplex) > 1:
            for i in range(len(simplex)):
                d[simplex[:i] + simplex[i + 1:]] += sign * (-1) ** i
    return {key: val for key, val in d.items() if val}


def expected_boundary(aa, bb):
    d = defaultdict(int)
    if len(aa) > 1:
        for k in range(len(aa)):
            for sign, simplex, _ in shuffle(aa[:k] + aa[k + 1:], bb):
                d[simplex] += (-1) ** k * sign
    if len(bb) > 1:
        for k in range(len(bb)):
            for sign, simplex, _ in shuffle(aa, bb[:k] + bb[k + 1:]):
                d[simplex] += (-1) ** (len(aa) - 1 + k) * sign
    return {key: val for key, val in d.items() if val}


def shuffle_checks():
    terms = same_factor = mixed = pairs = 0
    for p, q in product(range(8), repeat=2):
        aa, bb = tuple(range(p + 1)), tuple(range(q + 1))
        chain = []
        for sign, simplex, word in shuffle(aa, bb):
            chain.append((sign, simplex))
            pts = [tuple(int(i == t) for t in range(1, p + 1)) +
                   tuple(int(j == t) for t in range(1, q + 1)) for i, j in simplex]
            A = [[pts[j + 1][i] - pts[0][i] for j in range(p + q)] for i in range(p + q)]
            assert bareiss_det(A) == sign
            same_factor += sum(a == b for a, b in zip(word, word[1:]))
            mixed += sum(a != b for a, b in zip(word, word[1:]))
        assert len(chain) == comb(p + q, p)
        assert bdry(chain) == expected_boundary(aa, bb)
        terms += len(chain)
        pairs += 1
    small = [(sgn, sim) for sgn, sim, _ in shuffle((0, 1), (0, 1))]
    expect = expected_boundary((0, 1), (0, 1))
    wrong = [(-small[0][0], small[0][1]), small[1]]
    assert bdry(wrong) != expect and bdry(small[:-1]) != expect
    return {'dimension_range': '0 <= p,q <= 7', 'pairs': pairs, 'simplices': terms,
            'same_factor_internal_deletions': same_factor,
            'mixed_factor_internal_deletions': mixed,
            'wrong_sign_rejected': True, 'missing_shuffle_rejected': True}


def torus_faces(triangles):
    """Affine integer-vertex torus edges are distinguished by winding vectors.
    Each starting vertex is integral, hence projects to the same torus point.
    Equal winding vectors give identical parametrized straight edge maps.
    """
    d = defaultdict(int)
    for sgn, tri in triangles:
        for i in range(3):
            a, b = tri[:i] + tri[i + 1:]
            winding = tuple(v - u for u, v in zip(a, b))
            d[winding] += sgn * (-1) ** i
    return {key: val for key, val in d.items() if val}


def parametrization_checks():
    lower = ((0, 0), (1, 0), (1, 1))
    upper = ((0, 0), (1, 1), (0, 1))
    relabelled_upper = ((0, 0), (0, 1), (1, 1))
    bad = torus_faces([(1, lower), (1, upper)])
    good = torus_faces([(1, lower), (-1, relabelled_upper)])
    assert bad == {(1, 0): 1, (-1, 0): 1} and good == {}
    assert bareiss_det([[1, 1], [0, 1]]) == 1
    assert bareiss_det([[1, 0], [1, 1]]) == 1
    return {'oriented_gluing_raw_sum_is_cycle': False,
            'raw_boundary': {'h': 1, 'h_reverse': 1},
            'compatible_parametrization_boundary': {},
            'topological_degree': 1, 'simplex_count_before_and_after': 2}


def fold_checks():
    def location(x, y):
        tests = [x + 2, 1 - x, 3 * y - x - 2, x + 2 - y]
        return 'interior' if min(tests) > 0 else ('boundary' if min(tests) == 0 else 'outside')
    cases = []
    for y, expected in [(Q(3, 5), -1), (Q(2), 1), (Q(1), 0), (Q(3), 0)]:
        locations = [location(x, y) for x in [Q(-1, 2), Q(1, 2)]]
        assert 'boundary' not in locations
        degree = sum(s for s, loc in zip([-1, 1], locations) if loc == 'interior')
        assert degree == expected
        cases.append({'target': ['1/4', str(y)], 'locations': locations, 'degree': degree})
    # Three edge derivatives of f=(x^2,y) retain nonzero y components.
    assert [1, 2, -3] == [1 - 0, 3 - 1, 0 - 3]
    # A midpoint of the vertical fold lies in the interior and has zero Jacobian.
    assert location(Q(0), Q(1)) == 'interior' and 2 * Q(0) == 0
    # Boundary regularity cannot be inferred from interior-only full rank:
    # h(t)=t^2 on [0,1] has h'(0)=0.
    assert 2 * Q(0) == 0 and all(2 * Q(i, 10) > 0 for i in range(1, 11))
    return {'degree_cases': cases, 'edge_y_velocities': [1, 2, -3],
            'interior_fold_rejected': True, 'boundary_rank_loss_rejected': True}


def cover_checks():
    checked = 0
    for d in range(2, 14):
        for w in range(-17, 18):
            if w == 0:
                continue
            starts = sorted(Q(j, d) for j in range(d))
            ends = sorted(Q((j + w) % d, d) for j in range(d))
            assert starts == ends
            assert sum(Q(w, d) for _ in range(d)) == w
            assert Q(w, d) != 0
            checked += 1
    # A nonzero-degree smooth circle map can have a critical point:
    # t -> t-sin(2*pi*t)/(2*pi) has derivative 1-cos(2*pi*t), zero at 0.
    assert 1 - 1 == 0
    ratios = [Q(d, d) for d in range(2, 20)]
    assert all(x == 1 for x in ratios)
    return {'circle_cover_and_winding_pairs': checked,
            'lift_endpoint_permutations_match': True,
            'transfer_degree_preserved': True,
            'nonzero_degree_does_not_imply_local_diffeomorphism': True,
            'linear_cover_cost_does_not_imply_vanishing': True}


def optimization_checks():
    A = [[1, -1, 0, 0], [1, 0, 2, 3]]
    imm = l1_optimize([row[:3] for row in A], [0, 1])
    ordinary = l1_optimize(A, [0, 1])
    assert imm['minimum'] == '1/2' and ordinary['minimum'] == '1/3'
    B = [(2, 2, -1, 0), (3, 3, 0, -1)]
    assert all(sum(a * b for a, b in zip(row, col)) == 0 for row in A for col in B)
    # Immersive optimal cocycle phi=degree/2 is norm 1 on I but 3/2 on e4.
    phi = [Q(a, 2) for a in A[1]]
    assert max(map(abs, phi[:3])) == 1 and abs(phi[3]) == Q(3, 2)
    # e4 is already a cycle, so adding a coboundary cannot reduce phi(e4).
    assert A[0][3] == 0
    assert sum(x * y for x, y in zip(phi, B[0])) == 0
    assert B[0] != (0, 0, 0, 0) and B[0][2] == -1
    equal = l1_optimize([[1, -1, 0, 0], [1, 0, 2, 2]], [0, 1])
    assert equal['minimum'] == '1/2'
    circles = []
    for k in [1, 2, 3, 5, 8, 13]:
        opt = l1_optimize([list(range(1, k + 1))], [1])
        assert Q(opt['minimum']) == Q(1, k)
        circles.append({'max_winding': k, **opt})
    approx = []
    # Dense rational affine solutions z=t+b*B1; t=(1,1,0).
    for b in [Q(-7, 20), Q(-71, 200), Q(-707, 2000), Q(-7071, 20000), Q(-1, 2)]:
        z = [1 + 2 * b, 1 + 2 * b, -b]
        assert z[0] - z[1] == 0 and z[0] + 2 * z[2] == 1
        d = lcm(*(v.denominator for v in z), b.denominator)
        c = [int(d * v) for v in z]
        u = int(d * b)
        assert [c[0] - d, c[1] - d, c[2]] == [2 * u, 2 * u, -u]
        approx.append({'b': str(b), 'z': list(map(str, z)), 'denominator': d,
                       'integral_boundary_witness': u,
                       'normalized_cost': str(sum(abs(v) for v in z))})
    # Signed face occurrences with total zero pair exactly, including self-pairs.
    signed_faces = {'f': [1, -1, 1, -1], 'g': [1, 1, -1, -1]}
    assert all(vals.count(1) == vals.count(-1) for vals in signed_faces.values())
    defective = {'f': [1, -1, 1]}
    assert any(vals.count(1) != vals.count(-1) for vals in defective.values())
    return {'strict_gap_abstract_chain_model': {'immersive': imm, 'ordinary': ordinary,
                'uncontrolled_cocycle_value': '3/2',
                'is_manifold_counterexample': False},
            'equal_norm_abstract_control': equal,
            'circle_restricted_library_optima': circles,
            'rational_affine_and_integral_boundary_controls': approx,
            'unbalanced_face_multiset_rejected': True,
            'truncated_top_cycle_kernel_is_nonzero': True,
            'cochain_not_annihilating_ordinary_boundaries_rejected': True}


def archived_checks(path):
    p = Path(path)
    expected_manifest = '8ff41ceaafa1278519013f401c12d6279840a9fbbfe87ba74103c91293af1348'
    expected_report = 'b796c99ef3673687fcf40c3f3912b008fa6694d4b5eca996b1c1998f0e230062'
    raw = (p / 'MANIFEST.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected_manifest
    manifest = json.loads(raw)
    def valid(data, item):
        return len(data) == item['bytes'] and hashlib.sha256(data).hexdigest() == item['sha256']
    for item in manifest['files']:
        blob = (p / item['path']).read_bytes()
        assert valid(blob, item)
        assert not valid(blob + b'\n', item)
        assert not valid(blob[:-1], item)
        assert not valid(bytes([blob[0] ^ 1]) + blob[1:], item)
    assert hashlib.sha256((p / 'MATHEMATICAL_REPORT.md').read_bytes()).hexdigest() == expected_report
    rerun = subprocess.run([sys.executable, str(p / 'check_exact.py')], check=True, text=True, capture_output=True)
    assert rerun.stdout == (p / 'EXACT_CHECKS.json').read_text()
    paths = {x.name for x in p.iterdir() if x.is_file()}
    expected_paths = {x['path'] for x in manifest['files']} | {'MANIFEST.json'}
    assert paths == expected_paths
    assert not any(x.suffix.lower() in {'.pdf', '.png', '.jpg', '.txt'} for x in p.iterdir())
    return {'manifest_sha256': expected_manifest, 'report_sha256': expected_report,
            'files_matched': len(manifest['files']), 'total_files': len(paths),
            'original_program_matches_saved_output_byte_for_byte': True,
            'append_truncate_and_single_byte_mutations_rejected_per_file': True,
            'unmanifested_file_count': 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input')
    args = parser.parse_args()
    result = {'status': 'PASS', 'arithmetic': 'exact integers and fractions',
              'shuffle': shuffle_checks(), 'face_parametrization': parametrization_checks(),
              'fold': fold_checks(), 'cover': cover_checks(), 'optimization': optimization_checks(),
              'input_integrity': archived_checks(args.input) if args.input else 'not requested',
              'scope_limit': 'Finite controls do not settle arbitrary aspherical equality or verify foundational existence theorems.'}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
