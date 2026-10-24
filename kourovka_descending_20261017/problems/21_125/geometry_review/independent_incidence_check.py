#!/usr/bin/env python3
"""Independent Hydra cube incidence audit, standard library only.

No imports from the author's checker. Hyperplanes are components of an
explicit graph obtained by walking square boundaries, rather than a DSU
using precomputed parallelism formulae. Wreath actions use coordinate
updates instead of the author's multiplication law.
"""
from collections import Counter, deque
from itertools import combinations, permutations
from pathlib import Path
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'hydra_geometry'


def reverse(p):
    return tuple(p.index(i) for i in range(len(p)))


def generators(s, top, rank):
    out = [s] + [None] * rank
    out[-1] = top
    for i in range(rank - 1, 0, -1):
        a = out[i + 1]
        ai = reverse(a)
        out[i] = tuple(a[s[ai[x]]] for x in range(len(s)))
    if any(out[1][s[x]] != s[out[1][x]] for x in range(len(s))):
        return None
    return out


def orbit(gens, start=0):
    known, pending = {start}, [start]
    for x in pending:
        for g in gens:
            y = g[x]
            if y not in known:
                known.add(y)
                pending.append(y)
    return known


def square_data(gens):
    """Return all squares as four (edge id, boundary sign, start, end)."""
    n, m = len(gens[0]), len(gens) - 1
    backward = [reverse(g) for g in gens]
    squares = []
    for i in range(1, m + 1):
        labels = [1, i + 1, -(i if i > 1 else 1), -(i + 1)]
        for initial in range(n):
            current = initial
            perimeter = []
            for token in labels:
                label, sign = abs(token) - 1, 1 if token > 0 else -1
                nxt = (gens if sign > 0 else backward)[label][current]
                origin = current if sign > 0 else nxt
                perimeter.append((label * n + origin, sign, current, nxt))
                current = nxt
            assert current == initial, (i, initial)
            squares.append((i, initial, perimeter))
    return squares


def geometry(gens, full=False):
    n, m = len(gens[0]), len(gens) - 1
    squares = square_data(gens)
    adjacent = [set() for _ in range(n * (m + 1))]
    for _, _, boundary in squares:
        for j in (0, 1):
            a, b = boundary[j][0], boundary[j + 2][0]
            adjacent[a].add(b)
            adjacent[b].add(a)
            # Positive transverse orientations must agree across a square.
            assert boundary[j][1] == -boundary[j + 2][1]
    component = [-1] * len(adjacent)
    for e in range(len(adjacent)):
        if component[e] >= 0:
            continue
        component[e] = e
        pending = [e]
        for x in pending:
            for y in adjacent[x]:
                if component[y] < 0:
                    component[y] = e
                    pending.append(y)
    crossings = Counter()
    for level, _, boundary in squares:
        if component[boundary[0][0]] == component[boundary[1][0]]:
            crossings[level] += 1
    out = {'hyperplanes': len(set(component)),
           'self_crossing_square_count': sum(crossings.values()),
           'crossing_by_level': dict(crossings)}
    if not full:
        return out

    # A germ consists of an actual geometric edge id and a sign. Build each
    # vertex link directly from the incident corners of the lifted squares.
    germs, links = [set() for _ in range(n)], [set() for _ in range(n)]
    for label, g in enumerate(gens):
        for v, w in enumerate(g):
            edge = label * n + v
            germs[v].add((edge, 1))
            germs[w].add((edge, -1))
    crossing_hyperplanes = set()
    for _, _, boundary in squares:
        for j, (edge, sign, v, _) in enumerate(boundary):
            prev = boundary[(j - 1) % 4]
            incoming, outgoing = (prev[0], -prev[1]), (edge, sign)
            assert prev[3] == v
            links[v].add(frozenset((incoming, outgoing)))
            hs = frozenset((component[incoming[0]], component[outgoing[0]]))
            if len(hs) == 2:
                crossing_hyperplanes.add(hs)

    direct, indirect, inter = [], [], []
    for v in range(n):
        for a, b in combinations(sorted(germs[v]), 2):
            pair = frozenset((a, b))
            if pair in links[v]:
                continue
            ha, hb = component[a[0]], component[b[0]]
            if ha == hb:
                (direct if a[1] == b[1] else indirect).append((v, a, b))
            elif frozenset((ha, hb)) in crossing_hyperplanes:
                inter.append((v, a, b))
    out.update(direct_self_osculation_count=len(direct),
               indirect_self_osculation_count=len(indirect),
               inter_osculation_count=len(inter),
               A_special=not(crossings or direct or inter))
    return out


def partitions(n, prefix=()):
    if n == 0:
        yield prefix
    else:
        for k in range(prefix[-1] if prefix else 1, n + 1):
            yield from partitions(n - k, prefix + (k,))


def canonical_permutation(part):
    p = []
    start = 0
    for size in part:
        p.extend(range(start + 1, start + size))
        p.append(start)
        start += size
    return tuple(p)


def census(rank, n):
    counts = Counter()
    least = None
    level_min = {i: n + 1 for i in range(1, rank + 1)}
    level_clean = Counter()
    for partition in partitions(n):
        s = canonical_permutation(partition)
        for top in permutations(range(n)):
            counts['pairs_mod_S_conjugacy'] += 1
            gens = generators(s, top, rank)
            if gens is None:
                continue
            counts['relator_satisfying'] += 1
            if len(orbit(gens)) != n:
                continue
            counts['connected_covers'] += 1
            g = geometry(gens)
            c = g['self_crossing_square_count']
            counts['self_crossing_covers' if c else 'without_self_crossing'] += 1
            least = c if least is None else min(least, c)
            for i in level_min:
                k = g['crossing_by_level'].get(i, 0)
                level_min[i] = min(level_min[i], k)
                if k == 0:
                    level_clean[i] += 1
    return {'rank': rank, 'cover_degree': n, 'counts': dict(counts),
            'minimum_self_crossing_squares': least,
            'min_selfcross_squares_by_level': {str(k):v for k,v in level_min.items()},
            'number_with_level_clean': {str(k):v for k,v in level_clean.items()}}


def wreath(k, p):
    # Enumerate (base integer, rotation). Right multiplication by the base
    # generator adds 1 at the current rotation coordinate. Multiplication by
    # the top generator increments rotation. This avoids group-product code.
    s, t = [], []
    for b in range(p ** k):
        for r in range(k):
            digit = b // (p ** r) % p
            nextb = b + (p ** r) * (1 if digit < p - 1 else 1 - p)
            s.append(nextb * k + r)
            t.append(b * k + (r + 1) % k)
    return tuple(s), tuple(t)


def subgroup_filter(gens):
    """Regular-cover criterion with q(L_m) computed independently as orbit."""
    s, m, n = gens[0], len(gens) - 1, len(gens[0])
    subgroup_gens = [gens[1]]
    for i in range(2, m + 1):
        a, ai = gens[i], reverse(gens[i])
        subgroup_gens.append(tuple(ai[s[a[x]]] for x in range(n)))
    members = orbit(subgroup_gens)
    misses = [gens[j][0] not in members for j in range(2, m + 1)]
    return {'image_hyperplane_subgroup_order':len(members),
            'alpha_j_missing': misses,
            'predicts_no_self_crossing':all(misses)}


def main():
    started = time.monotonic()
    author_base = json.loads((AUTHOR / 'cover_search_results.json').read_text())['rows']
    author_extended = json.loads((AUTHOR / 'cover_search_extended.json').read_text())['rows']
    rows = []
    for a in author_base + author_extended:
        r = census(a['rank'], a['cover_degree'])
        assert r['counts'] == a['counts'], (r, a)
        assert r['minimum_self_crossing_squares'] == a['least_crossing_example']['self_crossing_squares']
        rows.append(r)
    level_author = json.loads((AUTHOR / 'level_crossing_results.json').read_text())['rows']
    for a in level_author:
        r = next(x for x in rows if (x['rank'],x['cover_degree']) == (a['rank'],a['degree']))
        for key in ('min_selfcross_squares_by_level','number_with_level_clean'):
            assert r[key] == a[key], (key, r, a)
        for lev, witness in a['witnesses'].items():
            g = geometry(generators(tuple(witness['S']),tuple(witness['top']),a['rank']))
            assert {str(k):v for k,v in g['crossing_by_level'].items()} == witness['counts']
    wreath_rows = []
    for a in json.loads((AUTHOR / 'wreath_cover_results.json').read_text())['rows']:
        s,t = wreath(a['wreath_top_order'], a['wreath_base_modulus'])
        gens = generators(s,t,a['rank'])
        assert gens is not None and len(orbit(gens)) == len(s)
        r = geometry(gens,full=True)
        for key in ('hyperplanes','self_crossing_square_count','direct_self_osculation_count',
                    'indirect_self_osculation_count','inter_osculation_count','A_special'):
            assert r[key] == a[key], (key,r,a)
        sf = subgroup_filter(gens)
        assert sf['predicts_no_self_crossing'] == (r['self_crossing_square_count'] == 0)
        r.update(rank=a['rank'],degree=a['degree'],wreath_top_order=a['wreath_top_order'],
                 wreath_base_modulus=a['wreath_base_modulus'],regular_subgroup_filter=sf)
        wreath_rows.append(r)
    inputs = json.loads((HERE / 'INPUT_MANIFEST.json').read_text())['inputs']
    assert all(hashlib.sha256((AUTHOR/n).read_bytes()).hexdigest() == item['sha256'] for n,item in inputs.items())
    output = {'status':'PASS','implementation':'independent square walks, edge adjacency components and actual-edge vertex links; no author checker imported',
              'complete_census_rows':rows,'wreath_rows':wreath_rows,
              'input_hashes_still_match':True,'elapsed_seconds':time.monotonic()-started}
    (HERE / 'INDEPENDENT_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'PASS','census_rows':len(rows),'wreath_rows':len(wreath_rows),
                      'pairs_examined':sum(r['counts']['pairs_mod_S_conjugacy'] for r in rows),
                      'connected_covers':sum(r['counts']['connected_covers'] for r in rows),
                      'elapsed_seconds':output['elapsed_seconds']}))


if __name__ == '__main__':
    main()
