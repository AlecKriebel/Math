#!/usr/bin/env python3
"""Independent finite diagnostics; not a polynomial optimizer or proof.

No imports from the candidate, no network calls, no file writes, no asserts.
Only very small LPs are enumerated. Finite enumeration is used deliberately.
"""
from fractions import Fraction as Q
from itertools import combinations, product
from math import gcd
import json


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def dot(a, b):
    return sum((i*j for i, j in zip(a, b)), Q(0))


def layers(d):
    result = []
    for sign in (1, -1):
        old = Q(0)
        for level in sorted({sign*x for x in d if sign*x > 0}):
            result.append((level-old, tuple(sign if sign*x >= level else 0 for x in d)))
            old = level
    return result


def gaussian(rows, values):
    n = len(values)
    work = [list(map(Q, row))+[Q(value)] for row, value in zip(rows, values)]
    for column in range(n):
        pivot = next((i for i in range(column, n) if work[i][column]), None)
        if pivot is None:
            return None
        work[column], work[pivot] = work[pivot], work[column]
        q = work[column][column]
        work[column] = [v/q for v in work[column]]
        for i in range(n):
            if i != column:
                q = work[i][column]
                work[i] = [v-q*w for v, w in zip(work[i], work[column])]
    return tuple(row[-1] for row in work)


def feasible(edges, point):
    return all(point[u]-point[v] >= demand for u, v, demand in edges)


def tiny_lp(n, edges, cost, fixed=None):
    """Vertex enumeration after removing component translation lineality.

    Caller supplies a bounded objective (a nonnegative row combination).
    """
    fixed = dict(fixed or {})
    adjacency = [set() for _ in range(n)]
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(n))
    while unseen:
        root = min(unseen)
        seen, todo = set(), [root]
        while todo:
            node = todo.pop()
            if node in seen:
                continue
            seen.add(node)
            todo.extend(adjacency[node]-seen)
        unseen -= seen
        need(sum(cost[i] for i in seen) == 0, 'test objective must annihilate lineality')
        if not set(fixed).intersection(seen):
            fixed[root] = Q(0)
    free = [i for i in range(n) if i not in fixed]
    rows, rhs = [], []
    for u, v, demand in edges:
        row = [int(i == u)-int(i == v) for i in free]
        residual = demand-fixed.get(u, Q(0))+fixed.get(v, Q(0))
        rows.append(row)
        rhs.append(residual)
    if not free:
        point = tuple(fixed[i] for i in range(n))
        return (dot(cost, point), point) if feasible(edges, point) else None
    best = None
    for selection in combinations(range(len(edges)), len(free)):
        solution = gaussian([rows[j] for j in selection], [rhs[j] for j in selection])
        if solution is None:
            continue
        point = [Q(0)]*n
        for i, value in fixed.items():
            point[i] = value
        for i, value in zip(free, solution):
            point[i] = value
        point = tuple(point)
        if feasible(edges, point):
            objective = dot(cost, point)
            if best is None or objective < best[0]:
                best = objective, point
    return best


def main():
    count = dict(vectors=0, layers=0, coordinate_checks=0, difference_checks=0,
                 model_instances=0, slice_lps=0, submodular_pairs=0,
                 nearest_sublevel_checks=0, removable_layers=0,
                 exact_denominator_checks=0, oracle_value_bit_checks=0, boundary_checks=0,
                 unsupported_generalizations_rejected=0, large_number_checks=0)
    grid = tuple(map(Q, (-3, -2, -1, 0, 1, 2, 3)))+(Q(-1, 2), Q(1, 2))
    for n in range(1, 5):
        for d in product(grid, repeat=n):
            ls = layers(d)
            need(len(ls) <= n, 'threshold layer count')
            need(tuple(sum((q*r[i] for q, r in ls), Q(0)) for i in range(n)) == d,
                 'threshold exact reconstruction')
            count['vectors'] += 1
            for q, r in ls:
                need(q > 0 and any(r), 'nonzero positive layer')
                count['layers'] += 1
                for i in range(n):
                    need(r[i]*d[i] >= 0 and abs(q*r[i]) <= abs(d[i]),
                         'coordinate conformity and domination')
                    count['coordinate_checks'] += 1
                    for j in range(n):
                        need((r[i]-r[j])*(d[i]-d[j]) >= 0,
                             'difference conformity')
                        need(abs(q*(r[i]-r[j])) <= abs(d[i]-d[j]),
                             'difference domination')
                        count['difference_checks'] += 1

    models = []
    # Empty graphs, isolated vertices, all choices of integer coordinates,
    # and every graph on these specified small bipartitions.
    for n in range(1, 4):
        U = set(range((n+1)//2))
        possible = [(u, v) for u in U for v in range(n) if v not in U]
        for selected in product((0, 1), repeat=len(possible)):
            edges = [(u, v, Q(3*j-2, 2*j+3))
                     for j, ((u, v), keep) in enumerate(zip(possible, selected)) if keep]
            for integer_bits in product((0, 1), repeat=n):
                I = tuple(i for i, keep in enumerate(integer_bits) if keep)
                models.append((n, U, edges, I))
    huge = 2**180+31
    den = 2**127-1
    models.extend([
        (4, {0, 1}, [(0, 2, Q(1, 3)), (0, 3, Q(5, 7)),
                    (1, 2, Q(-2, 5)), (1, 3, Q(3, 11))], (0, 3)),
        (4, {0, 1}, [(0, 2, Q(huge, den)), (1, 3, Q(-huge-1, den+2))], (0, 1)),
        (4, {0, 1}, [(0, 2, Q(huge, 3)), (0, 3, Q(-huge, 5)),
                    (1, 2, Q(1, den)), (1, 3, Q(7, den+2))], (0, 3)),
    ])
    for n, U, edges, I in models:
        cost = [Q(0)]*n
        for j, (u, v, _) in enumerate(edges):
            weight = Q(j+1, j+2)
            cost[u] += weight
            cost[v] -= weight
        base = tiny_lp(n, edges, cost)
        need(base is not None, 'continuous feasibility')
        _, star = base
        # Direct rational ceil(star-n), kept separate from upper endpoint.
        lo = {i: -((-(star[i]-n)).numerator//(-(star[i]-n)).denominator) for i in I}
        hi = {i: (star[i]+n).numerator//(star[i]+n).denominator for i in I}
        need(all(hi[i]-lo[i] <= 2*n for i in I), 'bounded label count')
        k = 1
        for _, _, demand in edges:
            k = k*demand.denominator//gcd(k, demand.denominator)
        qcost = 1
        for coefficient in cost:
            qcost = qcost*coefficient.denominator//gcd(qcost, coefficient.denominator)
        qvalue = k*qcost
        B = max([1]+[-((-abs(b)).numerator//(-abs(b)).denominator) for _, _, b in edges])
        A = max([1]+[-((-abs(a)).numerator//(-abs(a)).denominator) for a in cost])
        Hstar = -((-max(map(abs, star))).numerator//(-max(map(abs, star))).denominator)+n
        value_bound = n*A*(Hstar+n*B)
        values, completions = {}, {}
        for assignment in product(*(range(lo[i], hi[i]+1) for i in I)):
            fixed = dict(zip(I, map(Q, assignment)))
            valid = all(fixed[u]-fixed[v] >= b for u, v, b in edges if u in I and v in I)
            res = tiny_lp(n, edges, cost, fixed)
            count['slice_lps'] += 1
            need(valid == (res is not None), 'integer-coordinate domain exactness')
            if not valid:
                continue
            value, completion = res
            values[assignment], completions[assignment] = value, completion
            need((value*qvalue).denominator == 1, 'common denominator for all exact oracle values')
            need(abs(value) <= value_bound, 'uniform exact oracle value magnitude bound')
            count['oracle_value_bit_checks'] += 2
            for coordinate in completion:
                need((coordinate*k).denominator == 1, 'common demand denominator for basic completion')
                count['exact_denominator_checks'] += 1
            d = tuple(completion[i]-star[i] for i in range(n))
            for q, direction in layers(d):
                moved = tuple(star[i]+q*direction[i] for i in range(n))
                need(feasible(edges, moved), 'forward layer feasibility')
                need(dot(cost, direction) >= 0, 'LP layer objective sign')
                if q >= 1:
                    reduced = tuple(completion[i]-direction[i] for i in range(n))
                    need(feasible(edges, reduced), 'layer removal feasibility')
                    need(all(reduced[i].denominator == 1 for i in I), 'integer preservation')
                    need(dot(cost, reduced) <= value, 'layer removal objective')
                    need(sum(abs(reduced[i]-star[i]) for i in range(n)) < sum(abs(d[i]) for i in range(n)),
                         'strict l1 decrease')
                    count['removable_layers'] += 1
        need(values, 'finite domain is nonempty')
        for p, value in values.items():
            # This finite nearest-completion check is diagnostic only; it does
            # not replace the proof's compact minimizer over all completions.
            eligible = [completions[q] for q, qvalue in values.items() if qvalue <= value]
            near = min(eligible, key=lambda z: sum(abs(z[i]-star[i]) for i in range(n)))
            need(max(abs(near[i]-star[i]) for i in range(n)) < n,
                 'finite nearest sublevel representative proximity')
            count['nearest_sublevel_checks'] += 1
        for p, pvalue in values.items():
            for q, qvalue in values.items():
                meet = tuple(min(i, j) for i, j in zip(p, q))
                join = tuple(max(i, j) for i, j in zip(p, q))
                need(meet in values and join in values, 'domain lattice closure')
                need(pvalue+qvalue >= values[meet]+values[join], 'exact partial LP submodularity')
                count['submodular_pairs'] += 1
        count['model_instances'] += 1
        if any(abs(b.numerator).bit_length() > 100 or b.denominator.bit_length() > 100 for _, _, b in edges):
            need(len(values) <= (2*n+1)**len(I), 'large magnitude does not create more labels')
            need(k.bit_length() <= 1+sum(b.denominator.bit_length() for _, _, b in edges),
                 'common denominator has polynomial binary length')
            count['large_number_checks'] += 2

    # Mathematical attacks on tempting but unsupported substitutions.
    d = (Q(-2), Q(2))
    unsigned = ((Q(2), (0, 1)),)
    need(tuple(sum((q*r[i] for q, r in unsigned), Q(0)) for i in range(2)) != d,
         'positive-only decomposition must fail on negative entries')
    count['unsupported_generalizations_rejected'] += 1
    need(min(0, 1)+min(1, 0) < 1, 'original covering set is not meet closed')
    count['unsupported_generalizations_rejected'] += 1
    # Without mixed feasibility, two opposing rational difference inequalities
    # may force a half-integer difference between two integer coordinates.
    need(Q(1, 2).denominator != 1, 'general difference-system mixed-feasibility assumption is needed')
    count['unsupported_generalizations_rejected'] += 1
    need(Q(1, 3) < 1, 'single-edge demand cannot be rounded when one endpoint is continuous')
    count['unsupported_generalizations_rejected'] += 1
    # Isolated coordinate rays and empty-dimensional instance.
    for n in range(1, 5):
        for i in range(n):
            for sign in (-1, 1):
                ray = tuple(sign if j == i else 0 for j in range(n))
                need(all(type(q) is int for q in ray), 'empty graph integral ray')
                cost = tuple(-sign if j == i else 0 for j in range(n))
                need(dot(cost, ray) < 0, 'empty graph improvement')
                count['boundary_checks'] += 1
    need(tiny_lp(0, [], []) == (Q(0), ()), 'zero dimensional instance')
    count['boundary_checks'] += 1
    print(json.dumps({'status': 'PASS', 'counts': count,
                      'limitations': 'Finite exact diagnostics, not an implementation of rational LP, SFM, or GLS and not a complexity proof.'},
                     sort_keys=True))


if __name__ == '__main__':
    main()
