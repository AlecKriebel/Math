#!/usr/bin/env python3
"""Exact independent controls for the finite regular-module equivalence.

This is not an all-finite-group computation or a witness for the Pell candidate.
No author implementation is imported. Uses standard-library integer/rational math.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
from collections import Counter, defaultdict, deque
from itertools import product
from math import gcd, lcm
import json

PELL = ((3, 2), (20, 14), (119, 84))
POSITIVE_CONTROL = ((1, 3), (3, 1), (1, 1))


def mul(p, q):
    return tuple(p[q[j]] for j in range(len(p)))


def inv(p):
    r = [0] * len(p)
    for j, i in enumerate(p):
        r[i] = j
    return tuple(r)


def generated(gens, identity):
    out = {identity}
    todo = [identity]
    while todo:
        p = todo.pop()
        for s in gens:
            q = mul(s, p)
            if q not in out:
                out.add(q)
                todo.append(q)
    return [identity] + sorted(out - {identity})


def primitive(row):
    d = 0
    for z in row:
        d = gcd(d, z)
    return [z // d for z in row] if d else row


def rank(matrix):
    basis = {}
    for original in matrix:
        row = list(original)
        for pivot, old in sorted(basis.items()):
            if row[pivot]:
                r = row[pivot]
                row = primitive([old[pivot] * x - r * y for x, y in zip(row, old)])
        if any(row):
            first = next(i for i, z in enumerate(row) if z)
            basis[first] = primitive(row)
    return len(basis)


def regular_matrix(group, marks, pairs):
    n = len(group)
    index = {g: i for i, g in enumerate(group)}
    rows = []
    for h, (p, q) in zip(marks, pairs):
        h_inv = inv(h)
        for g in group:
            j = index[g]
            source = index[mul(h_inv, g)]
            row = [0] * (3 * n)
            row[source] += p
            row[n + j] -= q
            row[2 * n + source] += 1
            row[2 * n + j] -= 1
            rows.append(row)
    return rows


def dot(row, vector):
    return sum(x * y for x, y in zip(row, vector))


def group_controls():
    specs = {
        'trivial': [(0,)],
        'C2': [(1, 0)],
        'C3': [(1, 2, 0)],
        'C4': [(1, 2, 3, 0)],
        'V4': [(1, 0, 3, 2), (2, 3, 0, 1)],
        'S3': [(1, 2, 0), (1, 0, 2)],
        'D4': [(1, 2, 3, 0), (0, 3, 2, 1)],
    }
    cases = []
    total = 0
    for name, gens in specs.items():
        identity = tuple(range(len(gens[0])))
        group = generated(gens, identity)
        n = len(group)
        counts = Counter()
        for marks in product(group, repeat=3):
            if len(generated(marks, identity)) != n:
                continue
            matrix = regular_matrix(group, marks, PELL)
            r = rank(matrix)
            assert r == 3 * n - 1
            # No nonzero A can occur with B=0, and conversely, using Q-rank.
            no_b = [row[:n] + row[2*n:] for row in matrix]
            no_a = [row[n:] for row in matrix]
            assert rank(no_b) == rank(no_a) == 2 * n - 1
            vertical = [row[2*n:] for row in matrix]
            assert rank(vertical) == n - 1
            counts[r] += 1
            total += 1
        cases.append({'group': name, 'order': n, 'generating_markings': sum(counts.values()),
                      'Pell_ranks': dict(counts), 'vertical_kernel_dimension': 1,
                      'zero_A_iff_zero_B': 'PASS'})
    # Essential-hypothesis falsifier: non-generating marks produce false positives
    # if one incorrectly uses a one-dimensional constant-T baseline.
    group = generated([(1, 0)], (0, 1))
    matrix = regular_matrix(group, [(0, 1)] * 3, PELL)
    assert rank(matrix) == 4
    assert rank([r[4:] for r in matrix]) == 0
    assert rank([r[:2] + r[4:] for r in matrix]) == 2
    return {'cases': cases, 'total_generating_markings': total,
            'scope': 'bounded validation controls only, not a universal negative theorem',
            'non_generating_falsifier': {'group': 'C2', 'marks': 'all identity',
                 'full_kernel_dimension': 2, 'vertical_kernel_dimension': 2,
                 'horizontal_solution': False,
                 'meaning': 'rank<=3N-2 alone fails if generation is dropped'}}


def matched_permutation(left, right):
    assert Counter(left) == Counter(right)
    places = defaultdict(deque)
    for j, value in enumerate(right):
        places[value].append(j)
    return tuple(places[value].popleft() for value in left)


def apply(p, v):
    back = inv(p)
    return tuple(v[back[j]] for j in range(len(p)))


def multiset_controls():
    # Independent positive control, NOT the Pell pairs. A=T=... are rational.
    triples = [(Fraction(1), Fraction(1), Fraction(-2)),
               (Fraction(-1), Fraction(-1), Fraction(2))]
    weights = [Fraction(1, 3), Fraction(1, 3)]
    # Split positive masses over repeated triples to test exact multiplicities.
    weighted_triples = triples + triples
    weights += [Fraction(2, 3), Fraction(2, 3)]
    for p, q in POSITIVE_CONTROL:
        left, right = defaultdict(Fraction), defaultdict(Fraction)
        for (a, b, t), w in zip(weighted_triples, weights):
            left[p*a + t] += w
            right[q*b + t] += w
        assert dict(left) == dict(right)
    den = lcm(*(w.denominator for w in weights))
    counts = [int(w * den) for w in weights]
    expanded = [triple for triple, count in zip(weighted_triples, counts) for _ in range(count)]
    n = len(expanded)
    A = tuple(t[0] for t in expanded)
    B = tuple(t[1] for t in expanded)
    T = tuple(t[2] for t in expanded)
    marks = []
    for p, q in POSITIVE_CONTROL:
        left = tuple(p*a + t for a, t in zip(A, T))
        right = tuple(q*b + t for b, t in zip(B, T))
        h = matched_permutation(left, right)
        assert apply(h, left) == right
        marks.append(h)
    identity = tuple(range(n))
    group = generated(marks, identity)
    # Matrix coefficient map into ONE regular copy, preserving a nonzero A entry.
    coordinate = next(j for j, a in enumerate(A) if a)
    F = lambda v: tuple(v[g[coordinate]] for g in group)
    regular_A, regular_B, regular_T = F(A), F(B), F(T)
    matrix = regular_matrix(group, marks, POSITIVE_CONTROL)
    assert any(regular_A) and any(regular_B)
    assert all(dot(row, regular_A + regular_B + regular_T) == 0 for row in matrix)
    assert rank(matrix) <= 3 * len(group) - 2
    # Additional independent height is the literal last coordinate 1 of t.
    d = lcm(*(x.denominator for v in (regular_A, regular_B, regular_T) for x in v))
    va = tuple(int(d*x) for x in regular_A) + (0,)
    vb = tuple(int(d*x) for x in regular_B) + (0,)
    vt = tuple(int(d*x) for x in regular_T) + (1,)
    assert any(va[:-1]) and any(vb[:-1]) and vt[-1] == 1
    assert rank([list(va), list(vt)]) == rank([list(vb), list(vt)]) == 2
    # Values alone do not suffice: same underlying sets can have wrong masses.
    assert set([0, 0, 1]) == set([0, 1, 1])
    assert Counter([0, 0, 1]) != Counter([0, 1, 1])
    return {'pairs': POSITIVE_CONTROL, 'label': 'positive control, not Pell candidate',
            'rational_weight_denominator': den, 'expanded_multiplicities': counts,
            'coordinate_count': n, 'generated_group_order': len(group),
            'regular_matrix_rank': rank(matrix), 'matrix_size': 3*len(group),
            'regular_horizontal_vector': {'A': list(map(str, regular_A)),
                'B': list(map(str, regular_B)), 'T': list(map(str, regular_T))},
            'integer_height_vertices_real_rank': 2,
            'set_without_multiplicity_falsifier': 'PASS'}


def signed_mass_control():
    """Signed projection cancellation is trivial even for impossible norm data."""
    pairs = ((1, 1), (2, 1), (3, 1))
    directions = [(1, 0, -p) for p, q in pairs] + [(0, 1, -q) for p, q in pairs]
    mass = Counter({(0, 0, 0): 1})
    for delta in directions:
        new = Counter()
        for point, weight in mass.items():
            new[point] += weight
            shifted = tuple(x+y for x, y in zip(point, delta))
            new[shifted] -= weight
        # Counter's unary plus discards negatives, so filter explicitly.
        mass = Counter({point: weight for point, weight in new.items() if weight})
    assert any(a and weight for (a, b, t), weight in mass.items())
    assert any(weight < 0 for weight in mass.values()) and any(weight > 0 for weight in mass.values())
    for p, q in pairs:
        left, right = Counter(), Counter()
        for (a, b, t), weight in mass.items():
            left[p*a+t] += weight
            right[q*b+t] += weight
        assert all(weight == 0 for weight in left.values())
        assert all(weight == 0 for weight in right.values())
    # Yet orthogonal witness equations would give ||pA+T||=||B+T||
    # at p=1,2,3. Subtracting the consecutive squared norm equations yields
    # 3||A||²+2<A,T>=0 and 5||A||²+2<A,T>=0, forcing A=0.
    return {'pairs': pairs, 'signed_atoms': len(mass),
            'all_six_signed_projection_measures_zero': True,
            'has_nonzero_A_support': True,
            'actual_orthogonal_horizontal_solution': False,
            'reason': 'three equal norms at distinct p force ||A||^2=0',
            'meaning': 'positive rational weights may be replicated; signed weights are invalid'}


def main():
    out = {'utc': datetime.now(timezone.utc).isoformat(),
           'arithmetic': 'exact primitive integer elimination and rational multiplicities',
           'author_imports': False, 'regular_rank_controls': group_controls(),
           'multiset_positive_controls': multiset_controls(),
           'signed_weight_falsifier': signed_mass_control(),
           'scope': 'Finite tests supplement the unbounded equivalence proof in AUDIT.md. They do not decide Pell existence or all-finite-group rank.'}
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({'result': 'PASS', 'generating_markings': out['regular_rank_controls']['total_generating_markings'],
                      'positive_control': 'PASS', 'generation_and_multiplicity_falsifiers': 'PASS'}))


if __name__ == '__main__':
    main()
