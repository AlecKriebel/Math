"""Independent exact audit. No assertions: checks remain enabled under python -O.
Usage: python3 independent_audit.py PATH_TO_FROZEN_PUBLIC_DIRECTORY
Produces JSON on stdout only and never modifies the supplied directory.
"""
import hashlib
import heapq
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

EXPECTED_MANIFEST = 'd7e9b428572aa3864071d8e9bba50732afa6606586a4f1aa5250ada59ea24736'
EXPECTED_CANDIDATE = '9db9ae5f8cfc0d05239e117c813a05ad6806c322f30b57637b8ed408fc906afd'


def need(value, reason):
    if not value:
        raise ValueError(reason)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def geometry(tiles, width, height, tiling=True, no_four=False):
    need(len(tiles) > 0, 'empty tiling')
    for x, y, s in tiles:
        need(s > 0, 'nonpositive tile')
        need(0 <= x and 0 <= y and x+s <= width and y+s <= height, 'outside box')
    corners = set()
    contact, side = [], []
    for i, (x, y, s) in enumerate(tiles):
        corners.update((x+a*s, y+b*s) for a in (0, 1) for b in (0, 1))
        for j in range(i):
            a, b, t = tiles[j]
            dx, dy = min(x+s, a+t)-max(x, a), min(y+s, b+t)-max(y, b)
            need(not (dx > 0 and dy > 0), 'interior overlap')
            if dx >= 0 and dy >= 0:
                contact.append((i, j))
                if dx > 0 or dy > 0:
                    side.append((i, j))
    incident = max(sum(x <= a <= x+s and y <= b <= y+s for x, y, s in tiles) for a, b in corners)
    if no_four:
        need(incident <= 3, 'fourfold meeting')
    if tiling:
        xs = sorted({0, width} | {v for x, y, s in tiles for v in (x, x+s)})
        ys = sorted({0, height} | {v for x, y, s in tiles for v in (y, y+s)})
        for a, b in zip(xs, xs[1:]):
            for c, d in zip(ys, ys[1:]):
                u, v = F(a+b, 2), F(c+d, 2)
                need(sum(x < u < x+s and y < v < y+s for x, y, s in tiles) == 1, 'uncovered cell')
        need(sum(s*s for x, y, s in tiles) == width*height, 'area mismatch')
    return contact, side, incident


def crossings(tiles, width, height, edges, mask):
    # Union-find rather than the candidate's breadth-first bit-frontier algorithm.
    n = len(tiles)
    parent = list(range(n))
    def root(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for i, j in edges:
        if mask & (1 << i) and mask & (1 << j):
            parent[root(i)] = root(j)
    boundary = [set() for _ in range(4)]
    for i, (x, y, s) in enumerate(tiles):
        if mask & (1 << i):
            for k, condition in enumerate((x == 0, x+s == width, y == 0, y+s == height)):
                if condition:
                    boundary[k].add(root(i))
    return bool(boundary[0] & boundary[1]), bool(boundary[2] & boundary[3])


def evaluate(tiles, width, height, dual=True):
    contact, side, incident = geometry(tiles, width, height, no_four=dual)
    if dual:
        need(contact == side, 'corner-only adjacency in admissible finite tiling')
    n = len(tiles)
    truth = [crossings(tiles, width, height, contact, m) for m in range(1 << n)]
    if dual:
        need(all(truth[m][0] != truth[((1 << n)-1) ^ m][1] for m in range(1 << n)), 'Hex alternative')
    return {
        'tiles': n,
        'H': str(F(sum(h for h, v in truth), 1 << n)),
        'V': str(F(sum(v for h, v in truth), 1 << n)),
        'H_by_black_count': [sum(h for m, (h, v) in enumerate(truth) if m.bit_count() == k) for k in range(n+1)],
        'V_by_black_count': [sum(v for m, (h, v) in enumerate(truth) if m.bit_count() == k) for k in range(n+1)],
        'influences': [str(F(sum(truth[m][0] != truth[m | (1 << i)][0] for m in range(1 << n) if not m & (1 << i)), 1 << (n-1))) for i in range(n)],
        'maximum_incidence': incident,
    }, truth


def line_certificate(tiles, width, height):
    edges, _, _ = geometry(tiles, width, height)
    result = []
    for axis, span, transverse in [(0, width, height), (1, height, width)]:
        heights = sorted({0, transverse} | {v for t in tiles for v in (t[1-axis], t[1-axis]+t[2])})
        occupation = [F(0) for _ in tiles]
        for low, high in zip(heights, heights[1:]):
            mid = F(low+high, 2)
            path = [i for i, t in enumerate(tiles) if t[1-axis] < mid < t[1-axis]+t[2]]
            path.sort(key=lambda i: tiles[i][axis])
            need(sum(tiles[i][2] for i in path) == span, 'line does not span')
            for i in path:
                occupation[i] += F(high-low, transverse)
        need(occupation == [F(t[2], transverse) for t in tiles], 'occupation certificate')
        distance = [None] * len(tiles)
        queue = []
        for i, t in enumerate(tiles):
            if t[axis] == 0:
                distance[i] = t[2]
                heapq.heappush(queue, (t[2], i))
        while queue:
            d, i = heapq.heappop(queue)
            if d != distance[i]:
                continue
            for a, b in edges:
                j = b if a == i else a if b == i else None
                if j is not None:
                    alt = d + tiles[j][2]
                    if distance[j] is None or alt < distance[j]:
                        distance[j] = alt
                        heapq.heappush(queue, (alt, j))
        least = min(distance[i] for i, t in enumerate(tiles) if t[axis]+t[2] == span)
        need(least == span, 'side-length shortest path')
        result.append(str(F(span, transverse)))
    return result


def power_coefficients(counts):
    n = len(counts)-1
    c = [0] * (n+1)
    for k, count in enumerate(counts):
        for j in range(n-k+1):
            c[k+j] += count * math.comb(n-k, j) * (-1)**j
    return c


def all_integral_tilings(n):
    def extend(occupied, tiles):
        empty = next((i for i in range(n*n) if not occupied & (1 << i)), None)
        if empty is None:
            yield tiles
            return
        x, y = empty % n, empty // n
        for s in range(1, min(n-x, n-y)+1):
            cells = sum(1 << (n*b+a) for a in range(x, x+s) for b in range(y, y+s))
            if not cells & occupied:
                yield from extend(occupied | cells, tiles+[(x, y, s)])
    yield from extend(0, [])


def main():
    public = Path(sys.argv[1])
    manifest = (public/'FROZEN_MANIFEST.json').read_bytes()
    need(sha(manifest) == EXPECTED_MANIFEST, 'frozen manifest mismatch')
    entries = json.loads(manifest)['files']
    for e in entries:
        b = (public/e['path']).read_bytes()
        need(len(b) == e['bytes'] and sha(b) == e['sha256'], 'frozen file mismatch: '+e['path'])
    need(sha((public/'CANDIDATE.md').read_bytes()) == EXPECTED_CANDIDATE, 'candidate mismatch')
    need({str(p.relative_to(public)) for p in public.rglob('*') if p.is_file()} == {e['path'] for e in entries} | {'FROZEN_MANIFEST.json'}, 'unmanifested public file')
    tiles = [(0, 0, 2), (2, 0, 2), (0, 2, 1), (1, 2, 2), (3, 2, 1), (0, 3, 1), (3, 3, 1)]
    result, truth = evaluate(tiles, 4, 4)
    stored = json.loads((public/'checks/exact_crossings_results.json').read_text())
    for k in ['H_by_black_count', 'V_by_black_count', 'influences']:
        need(result[k] == stored[k], 'stored result mismatch: '+k)
    need(result['H'] == '65/128' and result['V'] == '63/128', 'wrong exact probabilities')
    coefficients = power_coefficients(result['H_by_black_count'])
    need(coefficients == [0, 0, 1, 8, -18, 15, -6, 1], 'polynomial identity')
    for m, (h, v) in enumerate(truth):
        black = lambda i: bool(m & (1 << i))
        formula = (black(3) and any(black(i) for i in (0, 2, 5)) and any(black(i) for i in (1, 4, 6))) or (not black(3) and black(0) and black(1))
        need(h == formula, 'direct formula')
    need(sum(F(x) for x in result['influences']) == F(107, 64), 'influence sum')
    variants = []
    for swap, flipx, flipy in itertools.product((False, True), repeat=3):
        tt = []
        for x, y, s in tiles:
            if swap:
                x, y = y, x
            tt.append((4-x-s if flipx else x, 4-y-s if flipy else y, s))
        r, _ = evaluate(tt, 4, 4)
        need(r['H'] == ('63/128' if swap else '65/128'), 'orientation control')
        need(line_certificate(tt, 4, 4) == ['1', '1'], 'VEL certificate')
        variants.append({'transpose': swap, 'flip_x': flipx, 'flip_y': flipy, 'H': r['H']})
    refined = tiles[1:] + [(F(x, 2), F(y, 2), F(s, 2)) for x, y, s in tiles]
    refine_result, _ = evaluate(refined, 4, 4)
    need(line_certificate(refined, 4, 4) == ['1', '1'], 'refinement VEL')
    control, _ = evaluate([(0, 0, 1)], 1, 1)
    need(control['H'] == control['V'] == '1/2', 'single-square control')
    grid = [(x, y, 1) for y in range(2) for x in range(2)]
    edges, side, _ = geometry(grid, 2, 2)
    black = (1 << 0) | (1 << 3)
    white = 15 ^ black
    need(crossings(grid, 2, 2, edges, black)[0] and crossings(grid, 2, 2, edges, white)[1], 'corner checkerboard control')
    need(not crossings(grid, 2, 2, side, black)[0] and not crossings(grid, 2, 2, side, white)[1], 'edge checkerboard control')
    need(line_certificate(grid, 2, 2) == ['1', '1'], 'fourfold VEL control')
    need(line_certificate([(0, 0, 1), (1, 0, 1)], 2, 1) == ['2', '1/2'], 'rectangle normalization')
    rejected = []
    for name, bad, w, h in [('zero_side', [(0, 0, 0)], 1, 1), ('overlap', [(0, 0, 1), (0, 0, 1)], 1, 1), ('gap', [(0, 0, 1)], 2, 2), ('outside', [(-1, 0, 1)], 1, 1), ('fourfold', grid, 2, 2)]:
        try:
            geometry(bad, w, h, no_four=True)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('failed adversarial rejection: '+name)
    census = []
    for n in range(1, 5):
        total = admissible = configs = 0
        for tt in all_integral_tilings(n):
            total += 1
            _, _, incidence = geometry(tt, n, n)
            need(line_certificate(tt, n, n) == ['1', '1'], 'census VEL')
            if incidence <= 3:
                evaluate(tt, n, n)
                admissible += 1
                configs += 1 << len(tt)
        census.append({'box_side': n, 'all_integral_tilings': total, 'admissible': admissible, 'colorings_checked': configs})
    dyadic = {}
    for K in range(6, 11):
        z = 2**(K-2)
        R = F(4**(K+1), 2**z-4)
        need(R > 0, 'positive tail')
        dyadic[str(K)] = {'numerator': str(R.numerator), 'denominator': str(R.denominator)}
        old = json.loads((public/'checks/dyadic_exact_bounds.json').read_text())[str(K)]
        need(dyadic[str(K)]['numerator'] == old['numerator'] and dyadic[str(K)]['denominator'] == old['denominator'], 'dyadic mismatch')
    need(F(4096, 16383) < F(1, 3), 'tail below one third')
    # Exact lower-bound endpoint algebra, including worst placement and s=D.
    need((1-3*F(1, 64))/2 > F(1, 4), 'endpoint separation')
    print(json.dumps({'status': 'PASS', 'assertions_used': False, 'manifest_files_verified': len(entries), 'seven_square': result, 'power_coefficients': coefficients, 'orientation_controls': variants, 'refined_thirteen_square': refine_result, 'integral_tiling_census': census, 'invalid_geometries_rejected': rejected, 'corner_checkerboard_both_cross': True, 'edge_checkerboard_neither_cross': True, 'rectangle_VEL': ['2', '1/2'], 'dyadic': dyadic}, indent=2))


if __name__ == '__main__':
    main()
