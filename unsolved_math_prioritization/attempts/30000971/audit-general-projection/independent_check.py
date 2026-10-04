#!/usr/bin/env python3
"""Independent exact controls. Does not import or modify the frozen packet.

Builds Hessians from polynomial terms, the full conormal constraints including
the eliminated source variables, jet evaluation matrices, and interpolation
spans by finite-algebra multiplication. Geometry is checked in AUDIT.md.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement
import json


def sparse_rank(rows):
    pivots = {}
    for row in rows:
        row = {j: Fraction(v) for j, v in row.items() if v}
        while row:
            j = min(row)
            if j not in pivots:
                lead = row[j]
                pivots[j] = {k: v / lead for k, v in row.items()}
                break
            mul = row[j]
            for k, v in pivots[j].items():
                row[k] = row.get(k, 0) - mul * v
                if not row[k]:
                    del row[k]
    return len(pivots)


def bareiss(a):
    a = [list(row) for row in a]
    previous, sign, size = 1, 1, len(a)
    for k in range(size - 1):
        pivot = next((j for j in range(k, size) if a[j][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        for i in range(k + 1, size):
            for j in range(k + 1, size):
                numerator = a[k][k] * a[i][j] - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = a[k][k]
    return sign * a[-1][-1]


def derivative_at_zero(monomial, directions):
    coeff, terms = 1, list(monomial)
    for direction in directions:
        coeff *= terms.count(direction)
        if not coeff:
            return 0
        terms.remove(direction)
    return coeff if not terms else 0


def monomial_value(monomial, e):
    """A-basis index for a monomial; None means zero in A."""
    if len(monomial) > 1 or any(i >= e for i in monomial):
        return None
    return 0 if not monomial else monomial[0] + 1


def pair_relation(left, right):
    a, b = Counter(left), Counter(right)
    lcm = a | b
    return tuple((lcm - a).elements()), tuple((lcm - b).elements())


def jet_controls(n):
    """Quadrics at p=[1:0:...] and q=[0:1:0:...]."""
    mons = list(combinations_with_replacement(range(n + 1), 2))
    columns = {mon: i for i, mon in enumerate(mons)}
    # In the chart X_a=1: value is X_a^2, derivative b is X_a X_b.
    jet_p = [{columns[(0, 0)]: 1}]
    jet_p += [{columns[(0, b)]: 1} for b in range(1, n + 1)]
    value_q = {columns[(1, 1)]: 1}
    jet_q = [value_q]
    jet_q += [{columns[tuple(sorted((1, b)))]: 1}
              for b in range(n + 1) if b != 1]
    one_jet_value = sparse_rank(jet_p + [value_q])
    two_jets = sparse_rank(jet_p + jet_q)
    assert one_jet_value == n + 2
    assert two_jets == 2 * (n + 1) - 1
    return one_jet_value, two_jets


def test(e):
    quadrics = list(combinations_with_replacement(range(e), 2))
    g = len(quadrics)
    n, c = e * g, g - e
    m, d = n + c, e + 1
    excluded = [((a, a), a) for a in range(e)]
    other = [(alpha, b) for alpha in quadrics for b in range(e)
             if (alpha, b) not in excluded]
    w_index = {pair: e + i for i, pair in enumerate(other)}
    polynomials = {alpha: [alpha] + [(w_index[(alpha, b)], b)
                   for b in range(e) if (alpha, b) in w_index]
                   for alpha in quadrics}
    normal = [[sum(derivative_at_zero(term, (v, b))
                   for term in polynomials[alpha]) for v in range(n)]
              for alpha, b in excluded + other]
    det = bareiss(normal)
    normal_rank = sparse_rank([{j: val for j, val in enumerate(row) if val}
                              for row in normal])
    failed = [{v: derivative_at_zero(alpha, (v, b)) for v in range(e)
               if derivative_at_zero(alpha, (v, b))}
              for alpha, b in excluded + other]
    failed_rank = sparse_rank(failed)
    assert (det, normal_rank, failed_rank) == (2 ** e, n, e)

    # All generators, with every pair-lcm relation, in the n-variable source.
    generators = [(i,) for i in range(e, n)] + quadrics
    assert len(generators) == m
    rows = []
    for left, right in combinations(range(m), 2):
        ca, cb = pair_relation(generators[left], generators[right])
        output = [{} for _ in range(d)]
        for generator, multiplier, sign in ((left, ca, 1), (right, cb, -1)):
            for basis in range(d):
                mon = multiplier + (() if basis == 0 else (basis - 1,))
                target = monomial_value(mon, e)
                if target is not None:
                    col = generator * d + basis
                    output[target][col] = output[target].get(col, 0) + sign
        rows.extend(row for row in output if row)
    relation_rank = sparse_rank(rows)
    quadratic_constant_rows = [{i * d: 1} for i in range(n - e, m)]
    assert relation_rank == g
    assert sparse_rank(rows + quadratic_constant_rows) == g
    tangent_dim = m * d - relation_rank
    qlength = m * d - tangent_dim
    q = Fraction(qlength, c)

    # Derivation equations applied to each z_i z_j=0 in A.
    derivation_rows = []
    for i, j in quadrics:
        row_by_output = [{} for _ in range(d)]
        for variable, multiplier in ((i, j), (j, i)):
            for basis in range(d):
                mon = (multiplier,) + (() if basis == 0 else (basis - 1,))
                target = monomial_value(mon, e)
                if target is not None:
                    col = variable * d + basis
                    row_by_output[target][col] = row_by_output[target].get(col, 0) + 1
        derivation_rows.extend(row for row in row_by_output if row)
    derivation_dim = e * d - sparse_rank(derivation_rows)
    assert derivation_dim == e * e

    # Actual images of the homogeneous quadratic Veronese sections, with X_0=1.
    ambient_images = set()
    for i, j in combinations_with_replacement(range(n + 1), 2):
        mon = tuple(a - 1 for a in (i, j) if a != 0)
        ambient_images.add(monomial_value(mon, e))
    ambient_images.discard(None)
    reachable = {0}
    hilbert = [len(reachable)]
    for degree in range(1, 4):
        reached = set()
        for a in reachable:
            for b in ambient_images:
                mon = (() if a == 0 else (a - 1,)) + (() if b == 0 else (b - 1,))
                target = monomial_value(mon, e)
                if target is not None:
                    reached.add(target)
        reachable = reached
        hilbert.append(len(reachable))
    reg = next(i for i, h in enumerate(hilbert) if h == d) + 1
    jet_value, two_jets = jet_controls(n)
    assert qlength == g and reg == 2
    assert d + Fraction(derivation_dim, c) == Fraction(n, c) + 1
    return dict(e=e, n=n, c=c, target=m, g=g, length=d,
                jacobian_determinant=det, jacobian_rank=normal_rank,
                no_cross_terms_rank=failed_rank,
                full_conormal_unknowns=m*d, full_conormal_relation_rank=relation_rank,
                full_conormal_hom_dimension=tangent_dim, Q_length=qlength,
                Q_annihilated_by_maximal_ideal=True, q=str(q),
                interpolation_ranks=hilbert, ideal_sheaf_regularity=reg,
                derivation_dimension=derivation_dim,
                first_jet_and_value_rank=jet_value,
                two_first_jets_rank=two_jets,
                two_first_jets_target_dimension=2*(n+1),
                strong_comparison_fails=(reg > q),
                weak_bound=str(Fraction(n,c)+1))


if __name__ == '__main__':
    print(json.dumps({'result': 'PASS', 'exact_arithmetic': True,
                      'geometry_is_proved_separately': True,
                      'cases': [test(e) for e in range(2,7)]}, indent=2))
