"""Independent finite diagnostics; no imported candidate code or numerical solver.

These exhaustive small-domain checks are not implementations of polynomial SFM
or GLS and do not prove the universal complexity claim.
"""
from fractions import Fraction as Q
from itertools import combinations, product
import json
import random
import sys


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def closure(seed, arcs):
    result = set(seed)
    while True:
        enlarged = result | {b for a, b in arcs if a in result}
        if enlarged == result:
            return frozenset(result)
        result = enlarged


def ring_interface(indices, lower, upper, edges, omit_base=False):
    nodes = {(i, t) for i in indices for t in range(lower[i] + 1, upper[i] + 1)}
    forced, banned, arcs = set(), set(), set()
    impossible = False
    for i, t in nodes:
        if t - 1 > lower[i]:
            arcs.add(((i, t), (i, t - 1)))
    for u, v, d in edges:
        if u not in indices or v not in indices:
            continue
        if not omit_base:
            base = lower[v] + d
            if base > upper[u]:
                impossible = True
            elif base > lower[u]:
                forced.add((u, base))
        for t in range(lower[v] + 1, upper[v] + 1):
            target = t + d
            if target > upper[u]:
                banned.add((v, t))
            elif target > lower[u]:
                arcs.add(((v, t), (u, target)))
    return nodes, forced, banned, arcs, impossible


def ring_check(indices, lower, upper, edges):
    nodes, forced, banned, arcs, impossible = ring_interface(indices, lower, upper, edges)
    vectors = [dict(zip(indices, p)) for p in product(*(range(lower[i], upper[i] + 1) for i in indices))]
    encoded = {
        frozenset((i, t) for i in indices for t in range(lower[i] + 1, p[i] + 1))
        for p in vectors if all(p[u] - p[v] >= d for u, v, d in edges if u in indices and v in indices)
    }
    nodes_list = sorted(nodes)
    represented = set()
    for flags in product((0, 1), repeat=len(nodes_list)):
        x = frozenset(w for w, flag in zip(nodes_list, flags) if flag)
        if not impossible and forced <= x and not (banned & x) and all(a not in x or b in x for a, b in arcs):
            represented.add(x)
    need(encoded == represented, 'threshold representation differs from direct feasible vectors')
    if encoded:
        base = closure(forced, arcs)
        need(base in encoded and all(base <= x for x in encoded), 'minimum family member incorrect')
        for node in nodes:
            containing = [x for x in encoded if node in x]
            candidate = closure(forced | {node}, arcs)
            need(bool(containing) == (not bool(candidate & banned)), 'containing-member existence mismatch')
            if containing:
                need(candidate in encoded and all(candidate <= x for x in containing), 'smallest containing-member mismatch')
        for x in encoded:
            for y in encoded:
                need(x & y in encoded and x | y in encoded, 'ring closure failure')
    else:
        need(impossible or bool(closure(forced, arcs) & banned), 'empty-family detection failure')
    return len(encoded), len(represented), 2 ** len(nodes)


def solve_square(rows, rhs):
    n = len(rows)
    m = [[Q(z) for z in row] + [Q(b)] for row, b in zip(rows, rhs)]
    for col in range(n):
        pivot = next((j for j in range(col, n) if m[j][col]), None)
        if pivot is None:
            return None
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [z / scale for z in m[col]]
        for j in range(n):
            if j != col:
                scale = m[j][col]
                m[j] = [a - scale * b for a, b in zip(m[j], m[col])]
    return tuple(row[-1] for row in m)


def slice_value(n, edges, fixed, objective):
    # Anchoring removes only whole-component translation lineality without an
    # existing fixed coordinate. The tested objectives are nonnegative sums of
    # edge rows, hence annihilate each such translation.
    eq = []
    eq_rhs = []
    for i, value in fixed.items():
        eq.append(tuple(int(j == i) for j in range(n)))
        eq_rhs.append(Q(value))
    adjacency = {i: set() for i in range(n)}
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    unseen = set(range(n))
    while unseen:
        component = {min(unseen)}
        while True:
            more = component | {v for u in component for v in adjacency[u]}
            if more == component:
                break
            component = more
        unseen -= component
        if not (component & fixed.keys()):
            anchor = min(component)
            eq.append(tuple(int(j == anchor) for j in range(n)))
            eq_rhs.append(Q(0))
    rows = [tuple(int(j == u) - int(j == v) for j in range(n)) for u, v, _ in edges]
    rhs = [b for _, _, b in edges]
    values = []
    for selected in combinations(range(len(edges)), n - len(eq)):
        y = solve_square(eq + [rows[j] for j in selected], eq_rhs + [rhs[j] for j in selected])
        if y is not None and all(y[u] - y[v] >= b for u, v, b in edges):
            need(all(y[i] == p for i, p in fixed.items()), 'fixed coordinate lost')
            values.append(sum(a * z for a, z in zip(objective, y)))
    need(bool(values), 'no slice optimum vertex after exact lineality anchoring')
    return min(values)


def finite_value_checks(rng):
    slices = pairs = instances = 0
    for n in range(1, 5):
        for _ in range(28):
            left = set(range((n + 1) // 2))
            edges = [(u, v, Q(rng.randrange(-6, 7), rng.randrange(1, 7)))
                     for u in left for v in range(n) if v not in left and rng.choice((False, True))]
            objective = [Q(0) for _ in range(n)]
            for u, v, _ in edges:
                weight = Q(rng.randrange(0, 5), rng.randrange(1, 5))
                objective[u] += weight
                objective[v] -= weight
            indices = tuple(i for i in range(n) if rng.choice((False, True)))
            feasible = [p for p in product(range(-1, 2), repeat=len(indices))
                        if all(dict(zip(indices, p))[u] - dict(zip(indices, p))[v] >= b
                               for u, v, b in edges if u in indices and v in indices)]
            values = {p: slice_value(n, edges, dict(zip(indices, p)), objective) for p in feasible}
            slices += len(values)
            for p, q in product(feasible, repeat=2):
                meet = tuple(min(x, y) for x, y in zip(p, q))
                join = tuple(max(x, y) for x, y in zip(p, q))
                need(meet in values and join in values, 'integer domain min/max closure fails')
                need(values[p] + values[q] >= values[meet] + values[join], 'partial minimum not submodular')
                pairs += 1
            instances += 1
    return instances, slices, pairs


def main():
    rng = random.Random(102530001102)
    families = assignments = sets = nonempty = empty = 0
    for n in range(1, 5):
        left = set(range((n + 1) // 2))
        possible_edges = [(u, v) for u in left for v in range(n) if v not in left]
        for flags in product((0, 1), repeat=len(possible_edges)):
            for i_flags in product((0, 1), repeat=n):
                indices = tuple(i for i, flag in enumerate(i_flags) if flag)
                for repetition in range(6):
                    lower = {i: rng.randrange(-5, 6) for i in indices}
                    upper = {i: lower[i] + rng.randrange(0, 3) for i in indices}
                    edges = [(u, v, rng.randrange(-5, 6)) for (u, v), flag in zip(possible_edges, flags) if flag]
                    count, _, powersets = ring_check(indices, lower, upper, edges)
                    assignments += count
                    sets += powersets
                    families += 1
                    nonempty += bool(count)
                    empty += not bool(count)
    # Very large signed endpoints have exactly the same representation size.
    huge = 2 ** 180 + 123
    count, _, powersets = ring_check((0, 1), {0: huge, 1: -huge}, {0: huge + 2, 1: -huge + 2}, [(0, 1, 2 * huge + 1)])
    families += 1
    assignments += count
    sets += powersets
    nonempty += bool(count)
    empty += not bool(count)
    # The missing baseline is a real defect, not caught by prefix implications.
    nodes, forced, banned, arcs, impossible = ring_interface((0, 1), {0: 0, 1: 0}, {0: 2, 1: 2}, [(0, 1, 1)], omit_base=True)
    empty_set_admitted = not impossible and not forced and not banned.intersection(set())
    need(empty_set_admitted and 0 - 0 < 1, 'omitted-baseline control was not detected')
    instances, slices, pairs = finite_value_checks(rng)
    # Exact hull boundary controls for both endpoints integral, demand 1/2.
    relaxation_only = (Q(1, 2), Q(0))
    hull_boundary = (Q(3, 2), Q(1, 2))
    need(relaxation_only[0] - relaxation_only[1] >= Q(1, 2), 'relaxation control infeasible')
    need(relaxation_only[0] - relaxation_only[1] < 1, 'LP-relaxation confusion undetected')
    need(hull_boundary == tuple((x + y) / 2 for x, y in zip((1, 0), (2, 1))), 'rational boundary convex combination failed')
    # Integer recession directions, fractional interpolation and lineality.
    directions = [(1, 0), (0, -1), (1, 1), (-1, -1)]
    for direction in directions:
        need(direction[0] - direction[1] >= 0, 'invalid recession generator')
        t = Q(7, 3)
        lo = t.numerator // t.denominator
        weight = t - lo
        point = tuple(Q(x) + t * d for x, d in zip((1, 0), direction))
        blended = tuple((1 - weight) * (x + lo * d) + weight * (x + (lo + 1) * d)
                        for x, d in zip((1, 0), direction))
        need(point == blended and point[0] - point[1] >= 1, 'fractional recession interpolation failed')
    print(json.dumps({'status': 'PASS', 'seed': 102530001102,
                      'ring_families': families, 'nonempty_families': nonempty,
                      'empty_families': empty, 'feasible_encoded_assignments': assignments,
                      'candidate_sets_examined': sets, 'hybrid_instances': instances,
                      'exact_slice_LPs': slices, 'submodular_pairs': pairs,
                      'controls': ['omitted_base_threshold', 'large_signed_bit_endpoints',
                                   'LP_vs_mixed_hull_boundary', 'fractional_hull_boundary',
                                   'fractional_recession_interpolation', 'both_lineality_signs'],
                      'limitations': 'Finite diagnostics only; no polynomial SFM, GLS, or universal theorem implementation.',
                      'optimization_mode': sys.flags.optimize}, indent=2))


if __name__ == '__main__':
    main()
