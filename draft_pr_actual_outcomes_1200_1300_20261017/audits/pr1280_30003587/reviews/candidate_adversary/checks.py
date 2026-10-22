#!/usr/bin/env python3
"""Independent finite falsification checks; no candidate code is imported.

Every validation uses an explicit exception, and therefore survives -O/-OO.
This is finite combinatorics, not a verification of C*-algebra assertions.
"""
import hashlib
import itertools as it
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def reachability(a):
    n = len(a)
    r = [[i == j or a[i][j] > 0 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = r[i][j] or (r[i][k] and r[k][j])
    return r


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def paths(n, edges, start, length):
    current = [(start, ())]
    for _ in range(length):
        current = [(v, word + (e,)) for u, word in current
                   for e, (s, v) in enumerate(edges) if s == u]
    return current


def simple_cycles(n, edges):
    # Enumerates cycles by their smallest vertex, preserving parallel-edge IDs.
    result = []
    for base in range(n):
        def walk(u, seen, word):
            for e, (s, v) in enumerate(edges):
                if s != u:
                    continue
                if v == base:
                    result.append(word + (e,))
                elif v > base and v not in seen:
                    walk(v, seen | {v}, word + (e,))
        walk(base, {base}, ())
    return result


def base_paths(n, edges):
    found = {0: ()}
    queue = [0]
    for u in queue:
        for e, (s, v) in enumerate(edges):
            if s == u and v not in found:
                found[v] = found[u] + (e,)
                queue.append(v)
    require(len(found) == n, 'base paths fail')
    return found


def period_and_class(n, edges):
    bp = base_paths(n, edges)
    dist = [len(bp[v]) for v in range(n)]
    d = 0
    for s, v in edges:
        d = math.gcd(d, dist[s] + 1 - dist[v])
    d = abs(d)
    require(d > 0, 'period zero in a cyclic strong graph')
    cycle_d = math.gcd(*(len(c) for c in simple_cycles(n, edges)))
    require(d == cycle_d, 'two independently defined graph periods differ')
    require(all((dist[v] - dist[s] - 1) % d == 0 for s, v in edges),
            'cyclic-class edge rule fails')
    return d, [v for v in range(n) if dist[v] % d == 0]


def graph_checks():
    counts = dict(matrices=0, essential=0, strong_noncycle=0,
                  reducible_ideal=0, periodic_noncycle=0, return_paths=0)
    witness = None
    for n in range(1, 4):
        for entries in it.product(range(3), repeat=n*n):
            counts['matrices'] += 1
            a = [list(entries[i*n:(i+1)*n]) for i in range(n)]
            if not (all(any(row) for row in a) and
                    all(any(a[i][j] for i in range(n)) for j in range(n))):
                continue
            counts['essential'] += 1
            r = reachability(a)
            if not all(all(row) for row in r):
                components = {frozenset(j for j in range(n) if r[i][j] and r[j][i])
                              for i in range(n)}
                terminal = next(c for c in components
                                if all(not a[i][j] for i in c
                                       for j in range(n) if j not in c))
                h = set(terminal)
                while True:
                    h2 = h | {i for i in range(n)
                              if all(not a[i][j] or j in h for j in range(n))}
                    if h2 == h:
                        break
                    h = h2
                require(0 < len(h) < n, 'terminal hereditary saturation not proper')
                counts['reducible_ideal'] += 1
                continue
            if all(sum(row) == 1 for row in a):
                continue
            counts['strong_noncycle'] += 1
            edges = [(i, j) for i in range(n) for j in range(n)
                     for _ in range(a[i][j])]
            d, cls = period_and_class(n, edges)
            counts['periodic_noncycle'] += d > 1
            f = [[0 for _ in cls] for _ in cls]
            for i, s in enumerate(cls):
                ps = paths(n, edges, s, d)
                counts['return_paths'] += len(ps)
                for v, _ in ps:
                    require(v in cls, 'return endpoint outside class')
                    f[i][cls.index(v)] += 1
            ad = a
            for _ in range(d-1):
                ad = multiply(ad, a)
            require(f == [[ad[i][j] for j in cls] for i in cls],
                    'return-path matrix disagrees with matrix power')
            require(sum(map(sum, f)) >= 2, 'return graph has fewer than two edges')
            b = [[x > 0 for x in row] for row in f]
            power = b
            primitive = False
            for _ in range(max(1, (len(cls)-1)**2+1)):
                if all(all(row) for row in power):
                    primitive = True
                    break
                power = [[bool(x) for x in row] for row in multiply(power, b)]
            require(primitive, 'return graph not primitive within Wielandt bound')
            if d > 1 and witness is None:
                witness = dict(adjacency=a, period=d, cyclic_class=cls, return_matrix=f)
    return counts, witness


def group_elements(moduli):
    return list(it.product(*(range(m) for m in moduli)))


def add(x, y, moduli):
    return tuple((a+b) % m for a, b, m in zip(x, y, moduli))


def pairing(label, g, moduli):
    common = math.lcm(*moduli)
    return sum(a*b*(common//m) for a, b, m in zip(label, g, moduli)) % common


def phase_checks():
    graphs = [
        (1, [(0, 0), (0, 0)]),
        (2, [(0, 0), (0, 1), (1, 0), (1, 1)]),
        (2, [(0, 1), (0, 1), (1, 0), (1, 0)]),
        (3, [(0, 1), (0, 2), (1, 0), (2, 0)]),
    ]
    groups = [(2,), (3,), (4,), (2, 2), (2, 3), (2, 4)]
    counts = dict(labelings=0, element_checks=0, independent_potential_checks=0,
                  quotient_checks=0, noncyclic_labelings=0)
    nontrivial_kernel_witness = None
    for n, edges in graphs:
        cycles = simple_cycles(n, edges)
        bp = base_paths(n, edges)
        for moduli in groups:
            gs = group_elements(moduli)
            q = math.lcm(*moduli)
            # Independent scalar coboundary set, not built from selected paths.
            coboundaries = {tuple((t[s]-t[v]) % q for s, v in edges)
                             for tail in it.product(range(q), repeat=n-1)
                             for t in [(0,) + tail]}
            for labels in it.product(gs, repeat=len(edges)):
                counts['labelings'] += 1
                counts['noncyclic_labelings'] += len(moduli) > 1
                chars = [tuple(pairing(label, g, moduli) for label in labels) for g in gs]
                k = set()
                untwisted = {}
                for g, phases in zip(gs, chars):
                    counts['element_checks'] += 1
                    closed = all(sum(phases[e] for e in c) % q == 0 for c in cycles)
                    direct = phases in coboundaries
                    counts['independent_potential_checks'] += 1
                    require(closed == direct, 'cycle criterion and potential enumeration differ')
                    potential = [(-sum(phases[e] for e in bp[v])) % q for v in range(n)]
                    b = tuple((phases[e]-potential[s]+potential[v]) % q
                              for e, (s, v) in enumerate(edges))
                    untwisted[g] = b
                    require(closed == all(x == 0 for x in b), 'fixed-path kernel mismatch')
                    require(closed == (b in coboundaries), 'untwisted action remains inner outside K')
                    if closed:
                        k.add(g)
                require(all(add(g, h, moduli) in k for g in k for h in k), 'K not subgroup')
                for g in gs:
                    for h in k:
                        counts['quotient_checks'] += 1
                        require(untwisted[add(g, h, moduli)] == untwisted[g],
                                'untwisting fails to descend exactly to quotient')
                if (1 < len(k) < len(gs) and nontrivial_kernel_witness is None
                        and any(any(phases) for g, phases in zip(gs, chars) if g in k)):
                    nontrivial_kernel_witness = dict(vertices=n, edges=edges,
                        moduli=moduli, labels=labels, inner_kernel=sorted(k))
    return counts, nontrivial_kernel_witness


def corner_word_checks():
    cases = [(3, [(0, 1), (0, 2), (1, 0), (2, 0)]),
             (4, [(0, 1), (1, 2), (1, 3), (2, 0), (3, 0)]),
             (2, [(0, 1), (0, 1), (1, 0)])]
    counts = dict(cases=0, spanning_pairs=0, common_extensions=0)
    for n, edges in cases:
        d, cls = period_and_class(n, edges)
        words = [(s, v, word) for s in cls for length in range(2*d+1)
                 for v, word in paths(n, edges, s, length)]
        for s, v, mu in words:
            for t, w, nu in words:
                if v != w:
                    continue
                counts['spanning_pairs'] += 1
                require((len(mu)-len(nu)) % d == 0, 'corner length congruence fails')
                extra = (-len(mu)) % d
                extensions = paths(n, edges, v, extra)
                require(bool(extensions), 'no common extension')
                require(len({word for _, word in extensions}) == len(extensions),
                        'duplicate extension words')
                for r, tau in extensions:
                    counts['common_extensions'] += 1
                    for origin, word in [(s, mu+tau), (t, nu+tau)]:
                        require(len(word) % d == 0 and r in cls, 'nonreturn extension')
                        vertex = origin
                        for k in range(0, len(word), d):
                            require(vertex in cls, 'return block starts outside class')
                            for e in word[k:k+d]:
                                require(edges[e][0] == vertex, 'invalid edge concatenation')
                                vertex = edges[e][1]
                            require(vertex in cls, 'return block ends outside class')
        counts['cases'] += 1
    return counts


def validator_selftest():
    caught = False
    try:
        require(False, 'deliberate sentinel')
    except RuntimeError as e:
        caught = str(e) == 'deliberate sentinel'
    require(caught, 'validation disabled under interpreter optimization')


def main():
    validator_selftest()
    g, gw = graph_checks()
    p, pw = phase_checks()
    result = dict(status='PASS', validation='explicit require raises RuntimeError; no assert',
                  graph_counts=g, phase_counts=p, corner_counts=corner_word_checks(),
                  periodic_graph_witness=gw, mixed_inner_outer_witness=pw,
                  limits='Finite combinatorics only; no C*-algebra assertion is numerically proved.',
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
