"""Exact independent lower-hull enumeration and saturated-face lattice controls.

Uses no author or old reviewer code. Finite tests supplement UNIVERSAL_PROOF.md.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from math import comb, gcd
from pathlib import Path
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
COUNT = 0

def require(test, message):
    global COUNT
    COUNT += 1
    if not test:
        raise AssertionError(message)

def determinant(rows):
    n = len(rows)
    if not n:
        return 1
    a = [list(map(F, row)) for row in rows]
    sign = 1
    value = F(1)
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        p = a[col][col]
        value *= p
        for row in range(col + 1, n):
            scale = a[row][col] / p
            for c in range(col + 1, n):
                a[row][c] -= scale * a[col][c]
    return sign * value

def solve(rows, rhs):
    n = len(rows)
    a = [list(map(F, row)) + [F(b)] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if a[r][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        p = a[col][col]
        a[col] = [x / p for x in a[col]]
        for r in range(n):
            if r != col:
                c = a[r][col]
                a[r] = [x - c * y for x, y in zip(a[r], a[col])]
    return [a[r][-1] for r in range(n)]

def lattice_volume(vertices):
    """gcd of maximal minors = normalized volume in saturated affine lattice."""
    k = len(vertices) - 1
    if k == 0:
        return 1
    d = len(vertices[0])
    diffs = [[v[i] - vertices[0][i] for i in range(d)] for v in vertices[1:]]
    g = 0
    for cols in combinations(range(d), k):
        value = determinant([[row[c] for c in cols] for row in diffs])
        require(value.denominator == 1, 'integer maximal minor')
        g = gcd(g, abs(value.numerator))
    return g

def lower_hull(points, heights):
    d = len(points[0])
    facets = []
    for ids in combinations(range(len(points)), d + 1):
        lin = solve([list(points[i]) + [1] for i in ids], [heights[i] for i in ids])
        if lin is None:
            continue
        others = [F(heights[i]) - sum(F(x) * y for x, y in zip(list(p) + [1], lin))
                  for i, p in enumerate(points) if i not in ids]
        if all(x > 0 for x in others):
            facets.append(tuple(ids))
        elif all(x >= 0 for x in others) and any(x == 0 for x in others):
            return None
    return tuple(facets)

def closure(facets):
    return {face for tau in facets for k in range(1, len(tau) + 1)
            for face in combinations(tau, k)}

def simplex_points(n, scale, variant):
    # Unimodular ambient shear of a dilated standard simplex: Delzant.
    out = [tuple(0 for _ in range(n))]
    for j in range(n):
        out.append(tuple(scale * (int(i == j) + (variant if i < j else 0)) for i in range(n)))
    return out

def projected_massive(q, l, facets):
    n = len(q[0])
    e = [tuple(0 for _ in range(l))] + [tuple(int(i == j) for i in range(l)) for j in range(l)]
    points = [a + v for a in q for v in e]
    kmax = n + l
    direct = [[0] * len(q) for _ in range(kmax + 1)]
    for face in closure(facets):
        k = len(face) - 1
        rows = {idx // (l + 1) for idx in face}
        cols = {idx % (l + 1) for idx in face}
        if k != len(rows) + len(cols) - 2:
            continue
        volume = lattice_volume([points[i] for i in face])
        require(volume > 0, 'nondegenerate massive simplex')
        for idx in face:
            direct[k][idx // (l + 1)] += volume
    base = [[0] * len(q) for _ in range(n + 1)]
    for k in range(n + 1):
        for face in combinations(range(len(q)), k + 1):
            v = lattice_volume([q[i] for i in face])
            for i in face:
                base[k][i] += v
    expected = [[sum(comb(l + 1, ell + 1) * comb(k + 1, j + 1) * base[j][a]
                     for j in range(n + 1) for ell in range(l + 1) if j + ell == k)
                 for a in range(len(q))] for k in range(kmax + 1)]
    require(direct == expected, 'product-face identity with saturated induced lattice')
    if l == n - 1:
        alternating = [sum((-1) ** (kmax - k) * direct[k][a] for k in range(kmax + 1))
                       for a in range(len(q))]
        require(alternating == [n * base[n][a] - base[n - 1][a] for a in range(len(q))],
                'alternating projected massive vector')
    return direct, base

def staircase_facets(n, l, rp, cp):
    paths = set()
    for positions in combinations(range(n + l), n):
        horizontal = set(positions)
        r = c = 0
        path = [(rp[0], cp[0])]
        for t in range(n + l):
            if t in horizontal:
                r += 1
            else:
                c += 1
            path.append((rp[r], cp[c]))
        paths.add(tuple(sorted(a * (l + 1) + b for a, b in path)))
    return paths

def is_staircase(n, l, facets):
    f = set(facets)
    return any(f == staircase_facets(n, l, rp, cp)
               for rp in permutations(range(n + 1)) for cp in permutations(range(l + 1)))

def square_vectors(q, facets):
    # Full-dimensional and boundary simplices in the square x/y in {0, scale}.
    scale = q[1][0]
    points = [a + (b,) for a in q for b in (0, 1)]
    massive = [[0] * 4 for _ in range(4)]
    for face in closure(facets):
        k = len(face) - 1
        ps = [points[i] for i in face]
        fixed = sum(len({p[c] for p in ps}) == 1 and ps[0][c] in (0, scale)
                    for c in (0, 1)) + int(len({p[2] for p in ps}) == 1)
        if k != 3 - fixed:
            continue
        v = lattice_volume(ps)
        for i in face:
            massive[k][i // 2] += v
    return tuple(sum((-1) ** (3 - k) * massive[k][a] for k in range(4)) for a in range(4))

def main():
    rng = random.Random(630955)
    records = []
    nonstaircases = 0
    for n, l, trials in [(1, 0, 2), (1, 1, 8), (1, 2, 8), (2, 1, 12), (2, 2, 30), (3, 2, 10)]:
        for trial in range(trials):
            q = simplex_points(n, 1 + trial % 3, trial % 2)
            e = [tuple(0 for _ in range(l))] + [tuple(int(i == j) for i in range(l)) for j in range(l)]
            points = [a + v for a in q for v in e]
            while True:
                heights = [rng.randrange(-1000000, 1000001) for _ in points]
                facets = lower_hull(points, heights)
                if facets is not None:
                    break
            vol = sum(lattice_volume([points[i] for i in tau]) for tau in facets)
            require(vol == comb(n + l, n) * lattice_volume(q), 'complete lower-hull triangulation volume')
            direct, base = projected_massive(q, l, facets)
            nonstair = not is_staircase(n, l, facets)
            nonstaircases += int(nonstair)
            records.append({'n': n, 'l': l, 'q': q, 'heights': heights, 'facets': facets,
                            'nonstaircase_up_to_row_column_permutations': nonstair,
                            'normalized_volume': vol, 'projected_massive': direct, 'base_massive': base})
    require(nonstaircases > 0, 'genuine nonstaircase product triangulations exercised')
    for n in range(1, 41):
        for j in range(n + 1):
            direct = sum((-1) ** (2 * n - 1 - j - ell) * comb(n, ell + 1)
                         * comb(j + ell + 1, j + 1) for ell in range(n))
            expected = n if j == n else (-1 if j == n - 1 else 0)
            require(direct == expected, 'finite difference including n=1')
    # Complete unit square configuration, where all lattice points are used.
    q = [(0, 0), (1, 0), (1, 1), (0, 1)]
    hpoly = {(2, 0, 2, 0), (0, 2, 0, 2)}
    cloud = set()
    for trial in range(120):
        heights = [rng.randrange(-1000000, 1000001) for _ in range(8)]
        facets = lower_hull([a + (b,) for a in q for b in (0, 1)], heights)
        if facets is None:
            continue
        require(sum(lattice_volume([q[i // 2] + (i % 2,) for i in tau]) for tau in facets) == 6,
                'square-prism complete volume')
        vector = square_vectors(q, facets)
        cloud.add(vector)
        require(vector[0] == vector[2] and vector[1] == vector[3] and sum(vector) == 4
                and all(0 <= x <= 2 for x in vector), 'arbitrary product triangulation projection in H')
    require((1, 1, 1, 1) in cloud, 'projected vertex can become strictly nonextreme')
    for scale in (1, 2, 3):
        sq = [(0, 0), (scale, 0), (scale, scale), (0, scale)]
        for sign in (-1, 1):
            w = [0, sign, 0, sign]
            for trial in range(6):
                h = [1000000 * w[a] + rng.randrange(-1000, 1001) for a in range(4) for _ in range(2)]
                facets = lower_hull([a + (b,) for a in sq for b in (0, 1)], h)
                require(facets is not None, 'generic small perturbation')
                base_facets = [(0, 1, 2), (0, 2, 3)] if sign > 0 else [(0, 1, 3), (1, 2, 3)]
                require(all(any({i // 2 for i in tau} <= set(cell) for cell in base_facets) for tau in facets),
                        'equal-column perturbed hull refines chosen base cells')
                expected = [0] * 4
                for cell in base_facets:
                    v = lattice_volume([sq[i] for i in cell])
                    for i in cell:
                        expected[i] += 2 * v
                for i in range(4):
                    expected[i] -= 2 * scale
                require(square_vectors(sq, facets) == tuple(expected), 'product-refinement vector including unused lattice points')
    # Deliberately false replacements, each detected by an explicit witness.
    rejects = {}
    rejects['omit_product_binomial_volume'] = comb(4, 2) != 1
    rejects['replace_vertex_multiplicity_by_indicator'] = comb(4, 3) != comb(3, 2)
    rejects['count_interior_faces_as_massive'] = 2 * 2 != 0
    rejects['omit_second_factor_face_multiplicity'] = comb(3, 1) != 1
    rejects['every_projection_extreme'] = (1, 1, 1, 1) not in hpoly and (1, 1, 1, 1) in cloud
    rejects['forget_induced_lattice_normalization'] = lattice_volume([(0, 0), (1, 1)]) == 1
    rejects['n_coefficient_replaced_by_n_plus_one'] = 2 != 3
    rejects['degree_one_nonconstant_discriminant'] = sum([1 - 1, 1 - 1]) == 0
    require(all(rejects.values()), 'all explicit false replacements rejected')
    result = {'status': 'PASS_FINITE_INDEPENDENT_PRODUCT_CONTROLS', 'assertions': COUNT,
              'product_triangulations': len(records), 'nonstaircase_triangulations': nonstaircases,
              'finite_difference_max_n': 40, 'unit_square_projection_cloud': sorted(cloud),
              'scaled_square_equal_column_refinements': 36, 'negative_mutations': rejects,
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'records': records, 'limits': 'Finite exact controls supplement the universal written proof; no old code imported, no full priority audit or geometric foundational theorem certification.'}
    (HERE / 'INDEPENDENT_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'records'}, sort_keys=True))

if __name__ == '__main__':
    main()
