"""Independent algebra controls; not a proof of the geometric lemmas.

Initial degrees are computed by full coefficient linear algebra after an
invertible coordinate change at every line. Squared-line membership uses
normal monomial order, so characteristic-two derivative pitfalls are avoided.
"""
from itertools import combinations, permutations
from functools import lru_cache
from collections import Counter
from pathlib import Path
import hashlib
import argparse
import json

counts = Counter()


def ck(x, label):
    assert x, label
    counts[label] += 1


@lru_cache(None)
def monomials(n, degree):
    if n == 1:
        return ((degree,),)
    return tuple((j,) + rest for j in range(degree + 1)
                 for rest in monomials(n - 1, degree - j))


def rref(rows, p):
    a = [[x % p for x in row] for row in rows]
    if not a:
        return []
    k = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(k, len(a)) if a[j][col]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        inv = pow(a[k][col], -1, p)
        a[k] = [(x * inv) % p for x in a[k]]
        for j in range(len(a)):
            if j != k and a[j][col]:
                factor = a[j][col]
                a[j] = [(x - factor * y) % p for x, y in zip(a[j], a[k])]
        k += 1
        if k == len(a):
            break
    return [row for row in a if any(row)]


def rank(rows, p):
    return len(rref(rows, p))


def canonical_line(a, b, p):
    rows = rref([a, b], p)
    ck(len(rows) == 2, 'line_defining_forms_independent')
    return tuple(map(tuple, rows))


def inverse(matrix, p):
    n = len(matrix)
    rows = [list(row) + [int(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    rr = rref(rows, p)
    ck([row[:n] for row in rr] == [[int(i == j) for j in range(n)] for i in range(n)],
       'normal_coordinate_change_invertible')
    return [row[n:] for row in rr]


def multiply(a, b, p):
    out = {}
    for ex, x in a.items():
        for ey, y in b.items():
            e = tuple(i + j for i, j in zip(ex, ey))
            out[e] = (out.get(e, 0) + x * y) % p
    return {e: c for e, c in out.items() if c}


@lru_cache(None)
def substitutions(line, degree, p):
    mat = [list(row) for row in line]
    for i in range(4):
        row = [int(i == j) for j in range(4)]
        if rank(mat + [row], p) > len(mat):
            mat.append(row)
        if len(mat) == 4:
            break
    inv = inverse(mat, p)
    basis = [tuple(int(i == j) for j in range(4)) for i in range(4)]
    powers = []
    for row in inv:
        linear = {e: c for e, c in zip(basis, row) if c}
        xs = [{(0, 0, 0, 0): 1}]
        for k in range(degree):
            xs.append(multiply(xs[-1], linear, p))
        powers.append(xs)
    expansions = []
    for ex in monomials(4, degree):
        poly = {(0, 0, 0, 0): 1}
        for j in range(4):
            poly = multiply(poly, powers[j][ex[j]], p)
        expansions.append(poly)
    return expansions


def initial_degree(lines, multiplicity, p):
    for degree in range(1, 7):
        mons = monomials(4, degree)
        conditions = []
        for line in lines:
            expansions = substitutions(line, degree, p)
            for target in mons:
                if target[0] + target[1] < multiplicity:
                    conditions.append([f.get(target, 0) for f in expansions])
        if rank(conditions, p) < len(mons):
            return degree
    raise AssertionError('Control cutoff was insufficient')


def arrangement(forms, p):
    return sorted({canonical_line(a, b, p) for a, b in combinations(forms, 2)})


def determinant(matrix, p):
    n = len(matrix)
    result = {}
    for perm in permutations(range(n)):
        sign = (-1) ** sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = {(0,) * (n + 1): sign % p}
        for row in range(n):
            term = multiply(term, matrix[row][perm[row]], p)
        for ex, c in term.items():
            result[ex] = (result.get(ex, 0) + c) % p
    return {ex: c for ex, c in result.items() if c}


def run(proof):
    results = []
    basis = [tuple(int(i == j) for j in range(4)) for i in range(4)]
    for p in (2, 3, 5):
        tetra = arrangement(basis, p)
        missing = canonical_line(basis[0], basis[1], p)
        configs = [
            ('single_line', [missing], (1, 2)),
            ('three_coplanar', [canonical_line(basis[0], b, p) for b in
                               (basis[1], basis[2], (0, 1, 1, 0))], (1, 2)),
            ('two_skew', [missing, canonical_line(basis[2], basis[3], p)], (2, 4)),
            ('three_plane_pseudostar', arrangement(basis[:3], p), (2, 3)),
            ('tetrahedron', tetra, (3, 4)),
            ('four_plane_cone', arrangement(basis[:3] + [(1, 1, 1, 0)], p), (3, 4)),
            ('five_plane_star', arrangement(basis + [(1, 1, 1, 1)], p), (4, 5)),
            ('tetrahedron_missing_edge', [l for l in tetra if l != missing], (2, 4)),
        ]
        for name, lines, expected in configs:
            got = tuple(initial_degree(lines, m, p) for m in (1, 2))
            ck(got == expected, 'exact_line_and_symbolic_square_initial_degrees')
            results.append({'characteristic': p, 'configuration': name,
                            'lines': len(lines), 'alpha': got[0], 'alpha_symbolic_square': got[1]})
        for d in range(2, 7):
            symbols = [{tuple(int(i == j) for j in range(d)): 1} for i in range(d)]
            matrix = [[{} for j in range(d - 1)] for i in range(d)]
            for j in range(d - 1):
                matrix[j][j] = symbols[j]
                matrix[d - 1][j] = {e: (-c) % p for e, c in symbols[d - 1].items()}
            for i in range(d):
                minor = determinant([row for k, row in enumerate(matrix) if k != i], p)
                expected = {tuple(int(j != i) for j in range(d)): (-1) ** (d - 1 + i) % p}
                ck(minor == expected, 'hilbert_burch_maximal_minors')
        for degree in range(1, 8):
            for ex in monomials(4, degree):
                all_partials_zero = all(n % p == 0 for n in ex)
                is_pth_power_monomial = all(n == p * (n // p) for n in ex)
                ck(all_partials_zero == is_pth_power_monomial, 'characteristic_p_derivative_kernel_monomials')
    for e in range(2, 13):
        for ga in range(21):
            kh = 2 * ga - 2 - e
            for q in range(ga + 1):
                chi = 1 - q + kh + 2 * e
                ck(chi == e + 2 * ga - 1 - q and chi >= e + ga - 1 >= 1,
                   'riemann_roch_integer_sign_controls')
    return {'status': 'PASS_SUPPLEMENTARY_SMALL_CHARACTERISTIC_CONTROLS',
            'proof_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(),
            'assertions': sum(counts.values()), 'counts': dict(sorted(counts.items())),
            'line_examples': results,
            'qualification': 'Finite algebra examples and numeric identities only. Resolution, Picard/Albanese, Hodge index and duality are reviewed analytically, not certified by these computations.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--proof', required=True, type=Path, help='Path to the frozen public proof')
    args = parser.parse_args()
    print(json.dumps(run(args.proof), indent=2, sort_keys=True))
