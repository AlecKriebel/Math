#!/usr/bin/env python3
"""Bounded falsification checks, not substitutes for the general proofs.

Only standard-library exact arithmetic is used. This file does not import an
author's checker or assume that a bounded test proves the theorem.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
from pathlib import Path
import json


def connected(vertices, edges):
    vertices = set(vertices)
    if not vertices:
        return False
    reached = {min(vertices)}
    while True:
        new = reached | {v for u in reached for v in vertices
                         if tuple(sorted((u, v))) in edges}
        if new == reached:
            return reached == vertices
        reached = new


def flag_zero_acyclic(vertices, edges):
    """Reduced H_0 vanishes and H_-1 vanishes, using component merging."""
    parent = {v: v for v in vertices}
    if not parent:
        return False
    def root(v):
        while parent[v] != v:
            v = parent[v]
        return v
    for u, v in edges:
        if u in parent and v in parent:
            parent[root(u)] = root(v)
    return len({root(v) for v in parent}) == 1


def recursive_one_domination(vertices, living, edges):
    """Direct n=1 expansion of the primary source's recursive definition."""
    for v in vertices - living:
        entire_link = {u for u in vertices if tuple(sorted((u, v))) in edges}
        living_link = entire_link & living
        if not flag_zero_acyclic(living_link, edges):
            return False
        # Zero-acyclic domination requires each outside vertex in the full
        # link to have a nonempty restricted link to the living link.
        for u in entire_link - living_link:
            if not any(tuple(sorted((u, x))) in edges for x in living_link):
                return False
    return True


def explicit_bc(vertices, living, edges):
    dead = vertices - living
    if any(not connected({x for x in living if tuple(sorted((x, v))) in edges}, edges)
           for v in dead):
        return False
    return all(any(tuple(sorted((u, x))) in edges and tuple(sorted((v, x))) in edges
                   for x in living)
               for u, v in edges if u in dead and v in dead)


def graph_checks():
    census = []
    totals = Counter()
    for n in range(1, 6):
        vertices = set(range(n))
        possible = list(combinations(range(n), 2))
        counts = Counter()
        for graph_bits in range(1 << len(possible)):
            edges = {e for i, e in enumerate(possible) if graph_bits >> i & 1}
            for live_bits in range(1, 1 << n):
                living = {v for v in vertices if live_bits >> v & 1}
                recursive = recursive_one_domination(vertices, living, edges)
                explicit = explicit_bc(vertices, living, edges)
                assert recursive == explicit, (n, edges, living)
                counts['graph_living_pairs'] += 1
                if not explicit:
                    continue
                counts['passing_BC'] += 1
                for order in permutations(vertices - living):
                    previous = set(living)
                    for z in order:
                        link = {x for x in previous if tuple(sorted((x, z))) in edges}
                        live_link = link & living
                        assert connected(live_link, edges)
                        for y in link - living:
                            assert any(tuple(sorted((y, x))) in edges for x in live_link)
                        previous.add(z)
                        counts['link_induction_steps'] += 1
                    counts['dead_vertex_orders'] += 1
        census.append({'vertices': n, **dict(counts)})
        totals.update(counts)
    return {'census': census, 'totals': dict(totals),
            'scope': 'B,C and their inheritance only; no finite test for arbitrary flag pi_1.'}


def egcd(a, b):
    if b == 0:
        return abs(a), (1 if a > 0 else -1), 0
    d, x, y = egcd(b, a % b)
    return d, y, x - (a // b) * y


def bezout(weights):
    coefficients = []
    d = 0
    for w in weights:
        g, x, y = egcd(d, w)
        coefficients = [x*c for c in coefficients] + [y]
        d = g
    assert sum(a*b for a, b in zip(weights, coefficients)) == d
    return d, coefficients


def inverse(word):
    return [(g, -e) for g, e in reversed(word)]


def power(word, exponent):
    return (word if exponent >= 0 else inverse(word)) * abs(exponent)


def coefficient_word(generators, coefficients):
    return [(g, 1 if e > 0 else -1) for g, e in zip(generators, coefficients)
            for _ in range(abs(e))]


def reduces_by_legal_ra_ag_cancellations(word, edges):
    """Every performed cancellation has only commuting letters between it.

    Returning True is therefore an exact identity certificate; the algorithm
    is not used to infer nontriviality from a nonempty remainder.
    """
    retained = []
    for g, e in word:
        for i in range(len(retained)-1, -1, -1):
            h, f = retained[i]
            if g != h and tuple(sorted((g, h))) in edges:
                continue
            if g == h and e == -f:
                del retained[i]
            else:
                retained.append((g, e))
            break
        else:
            retained.append((g, e))
    return not retained


def residue_checks():
    # The live graph is a triangle; dead z=3 commutes precisely with its
    # chosen live link. Nontrivial link gcd and negative weights are included.
    live = [0, 1, 2]
    count = 0
    maximum_word_length = 0
    for weights in [(2,3,5), (2,-3,5), (6,-10,15), (-6,10,-15),
                    (6,-9,15), (-6,9,-15)]:
        scale = gcd(gcd(abs(weights[0]), abs(weights[1])), abs(weights[2]))
        normalized = tuple(w//scale for w in weights)
        d, coefficients = bezout(normalized)
        assert d == 1
        t = coefficient_word(live, coefficients)
        height = lambda w: sum(normalized[g]*e for g, e in w if g != 3)
        assert height(t) == 1
        for live_link_bits in range(1, 8):
            link = [v for v in live if live_link_bits >> v & 1]
            dz, coeff = bezout([normalized[v] for v in link])
            v_word = coefficient_word(link, coeff)
            assert height(v_word) == dz
            edges = set(combinations(live, 2)) | {(x, 3) for x in link}
            for q in range(-8, 9):
                ell, i = divmod(q, dz)
                assert q == i + ell*dz and 0 <= i < dz
                h = power(t, q) + power(v_word, -ell) + power(t, -i)
                assert height(h) == 0
                for epsilon in [-1, 1]:
                    zi = power(t, i) + [(3, epsilon)] + power(t, -i)
                    lhs = h + zi + inverse(h)
                    rhs = power(t, q) + [(3, epsilon)] + power(t, -q)
                    maximum_word_length = max(maximum_word_length, len(lhs)+len(rhs))
                    assert reduces_by_legal_ra_ag_cancellations(lhs+inverse(rhs), edges)
                    count += 1
    # Exact residue/Britton arithmetic, including negative heights. If two
    # residues have difference divisible by dz, they must coincide.
    arithmetic = 0
    for dz in range(1, 25):
        for i, j in product(range(dz), repeat=2):
            assert ((j-i) % dz == 0) == (i == j)
            arithmetic += 1
    return {'identity_cases': count, 'largest_certificate_word_length': maximum_word_length,
            'britton_residue_cases': arithmetic,
            'scope': 'Exact bounded word identities and residue arithmetic; not a proof of general Britton normal form.'}


def geometric_and_exponent_checks():
    # An edge's two endpoint constructions hit the same point in its complete
    # standard line. Exact rational arithmetic avoids rounding assumptions.
    edge_checks = 0
    for weight in range(1, 16):
        for height in range(-50, 51):
            from_left = -Fraction(height, weight)
            from_right = 1-Fraction(height+weight, weight)
            assert from_left == from_right
            edge_checks += 1
    exponents = []
    a = 4
    for d in range(12):
        assert a == (9*3**d-1)//2
        assert a >= 4
        exponents.append(a)
        a = 3*a+1
    return {'weighted_edge_compatibility_cases': edge_checks,
            'first_twelve_induction_exponents': exponents,
            'scope': 'Edge compatibility and recurrence sanity only; topological extension and disk area are audited analytically.'}


if __name__ == '__main__':
    result = {'graphs': graph_checks(), 'residues': residue_checks(),
              'geometry_and_recurrence': geometric_and_exponent_checks(), 'result': 'PASS'}
    destination = Path(__file__).with_name('INDEPENDENT_RESULTS.json')
    destination.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
