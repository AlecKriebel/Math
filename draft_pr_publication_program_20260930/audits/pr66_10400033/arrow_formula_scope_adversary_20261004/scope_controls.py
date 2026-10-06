#!/usr/bin/env python3
"""Own bounded controls; no imports from the original proof package."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from math import comb
import json

P = ((3, 0), (5, 1), (2, 4))
Q = ((3, 0), (1, 5), (4, 2))
T = ((3, 0), (1, 4), (5, 2))
counts = Counter()

def require(condition, name):
    if not condition:
        raise AssertionError(name)
    counts[name] += 1

def image_maps(pattern, image):
    size = 2 * len(pattern)
    target = set(image)
    return [k for k in range(size)
            if {((t + k) % size, (h + k) % size) for t, h in pattern} == target]

def intersecting_graph(arrows):
    size = 2 * len(arrows)
    directed = set()
    for i, j in combinations(range(len(arrows)), 2):
        t, h = arrows[i]
        u, v = arrows[j]
        contains_u = 0 < (u - t) % size < (h - t) % size
        contains_v = 0 < (v - t) % size < (h - t) % size
        if contains_u != contains_v:
            opposite = 0 < (t - u) % size < (v - u) % size
            require(contains_u != opposite, 'opposite_arc_containment')
            directed.add((i, j) if contains_u else (j, i))
    return directed

def cyclic(edges, vertices):
    return all(sum((a, b) in edges for b in vertices if a != b) == 1
               for a in vertices)

def local_probability(edges, vertices):
    missing = [(a, b) for a, b in combinations(vertices, 2)
               if (a, b) not in edges and (b, a) not in edges]
    total = 0
    for bits in product((False, True), repeat=len(missing)):
        complete = edges | {((b, a) if bit else (a, b))
                            for (a, b), bit in zip(missing, bits)}
        total += cyclic(complete, vertices)
    return Fraction(total, 2 ** len(missing))

def all_matchings(points):
    if not points:
        yield ()
        return
    first = points[0]
    for index, last in enumerate(points[1:], 1):
        remaining = points[1:index] + points[index + 1:]
        for rest in all_matchings(remaining):
            yield ((first, last),) + rest

def sharp_bound(n):
    return Fraction(n * (n * n - (1 if n % 2 else 4)), 24)

require(len(image_maps(P, P)) == 1, 'P_automorphism_order_1')
require(len(image_maps(T, T)) == 3, 'T_automorphism_order_3')
require(not image_maps(P, Q), 'reflected_paths_are_distinct_cyclic_types')
require(bool(image_maps(Q, tuple(((-t) % 6, (-h) % 6) for t, h in P))),
        'circle_reversal_exchanges_P_Q')
require(bool(image_maps(T, tuple(((-t) % 6, (-h) % 6) for t, h in T))),
        'circle_reversal_preserves_T')
require(local_probability(intersecting_graph(P), (0, 1, 2)) == Fraction(1, 2),
        'P_probability_half')
require(local_probability(intersecting_graph(Q), (0, 1, 2)) == Fraction(1, 2),
        'Q_probability_half')
require(local_probability(intersecting_graph(T), (0, 1, 2)) == 1,
        'T_probability_one')

oriented_diagrams = Counter()
signed_diagrams = Counter()
for n in range(1, 6):
    for matching in all_matchings(tuple(range(2 * n))):
        for reverse in product((False, True), repeat=n):
            arrows = tuple((h, t) if bit else (t, h)
                           for (t, h), bit in zip(matching, reverse))
            graph = intersecting_graph(arrows)
            terms = []
            unsigned = Fraction(0)
            expected = Fraction(0)
            for vertices in combinations(range(n), 3):
                positions = sorted(z for i in vertices for z in arrows[i])
                order = {z: j for j, z in enumerate(positions)}
                image = tuple((order[arrows[i][0]], order[arrows[i][1]])
                              for i in vertices)
                weight = (Fraction(1, 2) if image_maps(P, image)
                          else Fraction(1) if image_maps(T, image) else Fraction(0))
                chance = local_probability(graph, vertices)
                require(weight <= chance, 'triple_domination')
                if weight:
                    require(chance == weight, 'selected_pattern_exact_probability')
                    terms.append((vertices, weight))
                unsigned += weight
                expected += chance
            require(unsigned <= expected <= sharp_bound(n), 'whole_unsigned_control')
            if n <= 4:
                for signs in product((-1, 1), repeat=n):
                    value = sum((weight * signs[a] * signs[b] * signs[c]
                                 for (a, b, c), weight in terms), Fraction(0))
                    require(abs(value) <= unsigned, 'signed_triangle_inequality_control')
                    signed_diagrams[n] += 1
            oriented_diagrams[n] += 1

tournaments = Counter()
maxima = {}
for n in range(7):
    pairs = list(combinations(range(n), 2))
    maximum = 0
    for reverse in product((False, True), repeat=len(pairs)):
        edges = {((b, a) if bit else (a, b)) for (a, b), bit in zip(pairs, reverse)}
        cycles = sum(cyclic(edges, vertices) for vertices in combinations(range(n), 3))
        degrees = [sum((a, b) in edges for b in range(n)) for a in range(n)]
        mean = Fraction(n - 1, 2)
        rhs = Fraction(n * (n * n - 1), 24) - sum(((d - mean) ** 2 for d in degrees), Fraction(0)) / 2
        require(cycles == rhs, 'tournament_variance_identity')
        require(cycles == comb(n, 3) - sum(comb(d, 2) for d in degrees),
                'tournament_transitive_count_identity')
        require(cycles <= sharp_bound(n), 'tournament_parity_bound')
        maximum = max(maximum, cycles)
        tournaments[n] += 1
    maxima[n] = {'observed':maximum, 'bound':str(sharp_bound(n))}

print(json.dumps({'status':'PASS', 'assertions':sum(counts.values()),
                  'checks':dict(counts), 'oriented_diagrams_by_n':dict(oriented_diagrams),
                  'signed_diagrams_by_n':dict(signed_diagrams),
                  'tournaments_by_n':dict(tournaments), 'maxima':maxima,
                  'nonclassical_boundary':{'P_only_all_positive_value':'1/2',
                      'P_graph_degrees':[2,1,1],
                      'meaning':'Formal evaluation need not be integral; pure P violates the planar Gauss even-degree condition.'},
                  'limitation':'Finite exact transcription and algebra controls; universal claims rely on the separately checked deduction and classical source theorem.'}, indent=2))
