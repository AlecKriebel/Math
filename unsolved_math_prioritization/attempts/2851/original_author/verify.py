#!/usr/bin/env python3
"""Exact finite diagnostic for KP-3.53; not a solver for the open problem.
Python 3 standard library only. All acceptance checks remain active under -O.
"""
import argparse
from collections import Counter
from fractions import Fraction
from itertools import permutations
import json
from pathlib import Path
import sys

class Rejected(ValueError):
    pass

def require(condition, message):
    if not condition:
        raise Rejected(message)

def matrix():
    return [[int((j-i) % 7 in (0, 1, 3)) for j in range(7)] for i in range(7)]

def cycles(p):
    n = len(p)
    require(all(type(x) is int for x in p), 'permutation must have integer entries')
    require(sorted(p) == list(range(n)), 'invalid permutation')
    seen = [False] * n
    total = 0
    for x in range(n):
        if not seen[x]:
            total += 1
            while not seen[x]:
                seen[x] = True
                x = p[x]
    return total

def determinant(a):
    a = [list(map(Fraction, row)) for row in a]
    answer = Fraction(1)
    for i in range(len(a)):
        pivot = next((r for r in range(i, len(a)) if a[r][i]), None)
        if pivot is None:
            return 0
        if pivot != i:
            a[i], a[pivot] = a[pivot], a[i]
            answer = -answer
        v = a[i][i]
        answer *= v
        for j in range(i, len(a)):
            a[i][j] /= v
        for r in range(i+1, len(a)):
            v = a[r][i]
            for j in range(i, len(a)):
                a[r][j] -= v*a[i][j]
    require(answer.denominator == 1, 'nonintegral determinant')
    return answer.numerator

def algebra(a):
    positive = negative = 0
    edge_uses = Counter()
    for p in permutations(range(7)):
        if all(a[i][p[i]] for i in range(7)):
            odd = sum(p[i] > p[j] for i in range(7) for j in range(i+1, 7)) % 2
            positive += not odd
            negative += odd
            edge_uses.update(enumerate(p))
    require(positive == 24 and negative == 0, 'matching-sign check failed')
    det = determinant(a)
    require(det == positive-negative == 24, 'determinant disagrees')
    require(len(edge_uses) == 21 and set(edge_uses.values()) == {8}, 'edge extendibility failed')
    for i in range(7):
        for k in range(7):
            require(sum(a[i][j]*a[k][j] for j in range(7)) == (3 if i == k else 1),
                    'Fano incidence identity failed')
    # Connected and without bridges; supports the planar girth inequality in the report.
    edges = [(i, 7+j) for i in range(7) for j in range(7) if a[i][j]]
    for omitted in [None] + edges:
        adj = [[] for _ in range(14)]
        for u, v in edges:
            if (u, v) != omitted:
                adj[u].append(v)
                adj[v].append(u)
        seen = {0}
        todo = [0]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        require(len(seen) == 14, 'support is disconnected or has a bridge')
    require(2*len(edges) > 3*(14-2), 'nonplanar girth-bound test failed')
    return {'determinant': det, 'permanent': positive+negative,
            'positive_terms': positive, 'negative_terms': negative,
            'support_vertices': 14, 'support_edges': len(edges),
            'matching_uses_per_edge': 8, 'nonplanarity_by_girth_bound': True}

def ribbon_counts(a):
    pairs = [(i, j) for i in range(7) for j in range(7) if a[i][j]]
    rows = [[k for k, (i, j) in enumerate(pairs) if i == r] for r in range(7)]
    cols = [[k for k, (i, j) in enumerate(pairs) if j == c] for c in range(7)]
    require(len(pairs) == 21 and all(len(c) == 3 for c in rows+cols), 'wrong curve valences')
    histogram = Counter()
    witness = {}
    for mask in range(1 << 14):
        tau = [-1] * 84
        an = [-1] * 21
        bn = [-1] * 21
        for r, curve in enumerate(rows+cols):
            order = curve[::-1] if (mask >> r) & 1 else curve
            outgoing, incoming = (0, 2) if r < 7 else (1, 3)
            nxt = an if r < 7 else bn
            for k in range(3):
                x, y = order[k], order[(k+1) % 3]
                nxt[x] = y
                u, v = 4*x+outgoing, 4*y+incoming
                require(tau[u] == tau[v] == -1, 'duplicate ribbon edge')
                tau[u], tau[v] = v, u
        require(all(tau[x] != x and tau[tau[x]] == x for x in range(84)), 'not an edge involution')
        # At each positive crossing, rotation is alpha+, beta+, alpha-, beta-.
        boundary = [4*(t//4)+(t+1) % 4 for t in tau]
        count = cycles(boundary)
        # Independent boundary tracing on the 21 alpha-outgoing halfedges:
        # after four steps the map is bn * an^-1 * bn^-1 * an.
        ai, bi = [-1]*21, [-1]*21
        for x in range(21):
            ai[an[x]], bi[bn[x]] = x, x
        commutator = [bn[ai[bi[an[x]]]] for x in range(21)]
        require(count == cycles(commutator), 'independent face tracers disagree')
        require((23-count) % 2 == 0, 'invalid orientable Euler characteristic')
        histogram[count] += 1
        witness.setdefault(count, mask)
    require(sum(histogram.values()) == 16384, 'incomplete cyclic-order enumeration')
    require(dict(histogram) == {1:2688, 3:11680, 5:2016}, 'unexpected boundary histogram')
    return {'cyclic_orders_checked': 16384,
            'boundary_histogram': {str(k):histogram[k] for k in sorted(histogram)},
            'neighborhood_genus_histogram': {str((23-k)//2):histogram[k] for k in sorted(histogram, reverse=True)},
            'minimum_neighborhood_genus': (23-max(histogram))//2,
            'first_minimum_witness_mask': witness[max(histogram)],
            'independent_tracers_agree_for_every_case': True}

def validate_fixture(data):
    expected_keys = {'problem_id', 'problem_number', 'matrix', 'expected_determinant',
                     'expected_boundary_histogram', 'minimum_neighborhood_genus', 'claim_scope'}
    require(type(data) is dict and set(data) == expected_keys, 'unexpected fixture schema')
    require(type(data['problem_id']) is int and data['problem_id'] == 2851, 'wrong problem ID')
    require(data['problem_number'] == 'KP-3.53', 'wrong problem number')
    a = data['matrix']
    require(type(a) is list and len(a) == 7, 'matrix must have seven rows')
    require(all(type(row) is list and len(row) == 7 for row in a), 'matrix must be square')
    require(all(type(x) is int and x in (0, 1) for row in a for x in row), 'matrix must contain integer zeroes and ones')
    require(a == matrix(), 'fixture is not the specified positive Fano matrix')
    require(type(data['expected_determinant']) is int and data['expected_determinant'] == 24,
            'wrong expected determinant')
    h = data['expected_boundary_histogram']
    require(type(h) is dict and all(type(v) is int for v in h.values()) and h == {'1':2688, '3':11680, '5':2016},
            'wrong expected boundary histogram')
    require(type(data['minimum_neighborhood_genus']) is int and data['minimum_neighborhood_genus'] == 9,
            'wrong expected minimum genus')
    require(data['claim_scope'] == 'positive unweighted Fano matrix only; KP-3.53 unresolved', 'overstated scope')
    return a

def negative_tests(data):
    # These are input-rejection tests, not a second proof of the mathematics.
    cases = []
    for name, change in [
        ('wrong_matrix', lambda d: d['matrix'][0].__setitem__(0,0)),
        ('boolean_matrix_entry', lambda d: d['matrix'][0].__setitem__(0,True)),
        ('wrong_histogram', lambda d: d['expected_boundary_histogram'].__setitem__('5',2015)),
        ('wrong_determinant', lambda d: d.__setitem__('expected_determinant',25)),
        ('overstated_scope', lambda d: d.__setitem__('claim_scope','KP-3.53 solved')),
        ('missing_field', lambda d: d.pop('matrix')),
        ('extra_field', lambda d: d.__setitem__('trust_me',True))]:
        d = json.loads(json.dumps(data))
        change(d)
        try:
            validate_fixture(d)
        except Rejected:
            cases.append(name)
        else:
            raise Rejected('negative fixture accepted: '+name)
    try:
        cycles([0,0])
    except Rejected:
        cases.append('nonpermutation')
    else:
        raise Rejected('nonpermutation accepted')
    return cases

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fixture', type=Path, default=Path(__file__).with_name('claims.json'))
    args = p.parse_args()
    data = json.loads(args.fixture.read_text(encoding='utf-8'))
    a = validate_fixture(data)
    result = {'problem_id':2851, 'status':'PASS_RESTRICTED_DIAGNOSTIC',
              'full_problem_solved':False, 'algebra':algebra(a), 'ribbon':ribbon_counts(a),
              'negative_tests_rejected':negative_tests(data),
              'optimization_safe':True, 'third_party_dependencies':[]}
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (Rejected, OSError, ValueError, TypeError, KeyError, IndexError) as exc:
        print('REJECT: '+str(exc), file=sys.stderr)
        sys.exit(1)
