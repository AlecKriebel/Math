"""Independent exact controls; authored before access to any candidate checker.

No input files are read. All samples are generated here using the standard
library. Small-case computations supplement the mathematical audit.
"""
from collections import deque
from fractions import Fraction as Q
from itertools import combinations, product
import json
import random


def bit(x, i):
    return (x >> i) & 1


def projection(x, axes):
    return tuple(bit(x, i) for i in axes)


def lattice(states):
    return all((a & b) in states and (a | b) in states
               for a in states for b in states)


def mtp2(p, n):
    return all(p[a & b] * p[a | b] >= p[a] * p[b]
               for a in range(1 << n) for b in range(1 << n))


def marginal(p, axes):
    values = {z: Q(0) for z in product((0, 1), repeat=len(axes))}
    for x, value in enumerate(p):
        values[projection(x, axes)] += value
    return values


def ci(p, a, b, c):
    a, b, c = tuple(a), tuple(b), tuple(c)
    abc, ac, bc, cc = (marginal(p, axes) for axes in
                       (a + b + c, a + c, b + c, c))
    for av, bv, cv in product(product((0, 1), repeat=len(a)),
                              product((0, 1), repeat=len(b)),
                              product((0, 1), repeat=len(c))):
        if abc[av + bv + cv] * cc[cv] != ac[av + cv] * bc[bv + cv]:
            return False
    return True


def separates(n, edges, a, b, c):
    reached, frontier = set(a), list(a)
    while frontier:
        u = frontier.pop()
        for i, j in edges:
            v = j if u == i else i if u == j else None
            if v is not None and v not in c and v not in reached:
                reached.add(v)
                frontier.append(v)
    return not (reached & set(b))


def globally_markov(p, n, edges):
    checked = 0
    for labels in product(range(4), repeat=n):
        a, b, c = (tuple(i for i, label in enumerate(labels) if label == k)
                   for k in (1, 2, 3))
        if a and b and separates(n, edges, a, b, c):
            checked += 1
            if not ci(p, a, b, c):
                return False, checked
    return True, checked


def support_local_recovery(states, n, edges):
    unary = [set(bit(x, i) for x in states) for i in range(n)]
    edge = [set(projection(x, e) for x in states) for e in edges]
    return {x for x in range(1 << n)
            if all(bit(x, i) in unary[i] for i in range(n))
            and all(projection(x, e) in allowed
                    for e, allowed in zip(edges, edge))}


def implications_recovery(states, n, edges):
    fixed = {i: bit(next(iter(states)), i) for i in range(n)
             if len({bit(x, i) for x in states}) == 1}
    active = set(range(n)) - fixed.keys()
    arrows = []
    for i, j in edges:
        if i in active and j in active:
            allowed = {projection(x, (i, j)) for x in states}
            if (1, 0) not in allowed:
                arrows.append((i, j))
            if (0, 1) not in allowed:
                arrows.append((j, i))
    return {x for x in range(1 << n)
            if all(bit(x, i) == value for i, value in fixed.items())
            and all(bit(x, i) <= bit(x, j) for i, j in arrows)}


def exhaustive_support_controls():
    counts = {}
    for n in range(5):
        all_edges = list(combinations(range(n), 2))
        sublattices, represented = 0, 0
        for mask in range(1, 1 << (1 << n)):
            states = {x for x in range(1 << n) if (mask >> x) & 1}
            if not lattice(states):
                continue
            sublattices += 1
            for edge_mask in range(1 << len(all_edges)):
                edges = [e for k, e in enumerate(all_edges)
                         if (edge_mask >> k) & 1]
                if support_local_recovery(states, n, edges) == states:
                    represented += 1
                    assert implications_recovery(states, n, edges) == states
        counts[str(n)] = {"nonempty_sublattices": sublattices,
                          "graph_support_representations": represented}
    return counts


def residual_network(capacity, s, t):
    residual = [row[:] for row in capacity]
    value = 0
    while True:
        predecessor = {s: None}
        pending = deque([s])
        while pending and t not in predecessor:
            u = pending.popleft()
            for v, room in enumerate(residual[u]):
                if room > 0 and v not in predecessor:
                    predecessor[v] = u
                    pending.append(v)
        if t not in predecessor:
            return value, residual
        path, v = [], t
        while v != s:
            u = predecessor[v]
            path.append((u, v))
            v = u
        amount = min(residual[u][v] for u, v in path)
        for u, v in path:
            residual[u][v] -= amount
            residual[v][u] += amount
        value += amount


def exact_flow_controls():
    rng = random.Random(30005303)
    case_count, state_count = 0, 0
    for n in range(8):
        for trial in range(75):
            oriented = []
            for i, j in combinations(range(n), 2):
                if rng.randrange(3) != 0:
                    oriented.append((i, j, rng.randrange(7)) if rng.randrange(2)
                                    else (j, i, rng.randrange(7)))
            fields = [rng.randrange(-8, 9) for _ in range(n)]
            energies = [-sum(fields[i] * bit(x, i) for i in range(n))
                        -sum(jj * bit(x, i) * bit(x, j) for i, j, jj in oriented)
                        for x in range(1 << n)]
            minimum = min(energies)
            unary = [-fields[i] - sum(jj for u, _, jj in oriented if u == i)
                     for i in range(n)]
            s, t = n, n + 1
            capacity = [[0] * (n + 2) for _ in range(n + 2)]
            for i, j, jj in oriented:
                capacity[i][j] += jj
            for i, bb in enumerate(unary):
                if bb < 0:
                    capacity[s][i] = -bb
                else:
                    capacity[i][t] = bb
            value, residual = residual_network(capacity, s, t)
            shift = sum(-bb for bb in unary if bb < 0)
            assert value == minimum + shift
            weights = []
            for x, energy in enumerate(energies):
                side = {s} | {i for i in range(n) if bit(x, i)}
                crossing = sum(residual[u][v] for u in side
                               for v in range(n + 2) if v not in side)
                assert crossing == energy - minimum >= 0
                # Construct local edge/unary factors and verify the exact product.
                local = Q(1)
                for i in range(n):
                    local *= Q(1, 2 ** (residual[i][t] if bit(x, i)
                                       else residual[s][i]))
                for i, j in combinations(range(n), 2):
                    if bit(x, i) != bit(x, j):
                        local *= Q(1, 2 ** (residual[i][j] if bit(x, i)
                                           else residual[j][i]))
                assert local == Q(1, 2 ** (energy - minimum))
                weights.append(local)
                state_count += 1
            assert 1 <= sum(weights) <= 1 << n
            assert mtp2([w / sum(weights) for w in weights], n)
            case_count += 1
    return {"networks": case_count, "configurations": state_count}


def named_controls():
    cycle = [(0, 1), (1, 2), (2, 3), (3, 0)]
    p = [Q(0)] * 16
    for x in range(16):
        if bit(x, 0) == bit(x, 1):
            p[x] = Q(2 ** (bit(x, 0) * bit(x, 2) * bit(x, 3)), 9)
    assert sum(p) == 1 and mtp2(p, 4)
    markov, separations = globally_markov(p, 4, cycle)
    assert markov and separations == 4
    # Independent even/odd product check on the quotient's three bits.
    sides = [[], []]
    for a, b, c in product((0, 1), repeat=3):
        x = a + 2 * a + 4 * b + 8 * c
        sides[(a + b + c) % 2].append(x)
    for axes in [()] + [(i,) for i in range(4)] + cycle:
        assert sorted(projection(x, axes) for x in sides[0]) == sorted(
            projection(x, axes) for x in sides[1])
    even, odd = (product_value([p[x] for x in side]) for side in sides)
    assert even == Q(1, 9 ** 4) and odd == Q(2, 9 ** 4)
    equal = [Q(0)] * 8
    equal[0] = equal[7] = Q(1, 2)
    assert mtp2(equal, 3)
    assert globally_markov(equal, 3, [(0, 1), (1, 2)])[0]
    assert all(ci(equal, (i,), (j,), tuple(set(range(3)) - {i, j}))
               for i, j in combinations(range(3), 2))
    assert not globally_markov(equal, 3, [])[0]
    false_local = [Q(0)] * 8
    false_local[1] = false_local[6] = Q(1, 2)
    assert not mtp2(false_local, 3)
    for i, j in combinations(range(3), 2):
        for x in range(8):
            if not bit(x, i) and not bit(x, j):
                assert false_local[x] * false_local[x | (1 << i) | (1 << j)] >= (
                    false_local[x | (1 << i)] * false_local[x | (1 << j)])
    smoothing = [Q(2), Q(1), Q(4), Q(2)]
    assert mtp2(smoothing, 2)
    assert not mtp2([v + Q(1, 17) for v in smoothing], 2)
    # Equality-block aggregate positive despite one negative original coupling.
    aggregate = [Q(0)] * 8
    for x in range(8):
        if bit(x, 0) == bit(x, 1):
            exponent = -3 * bit(x, 0) * bit(x, 2) + 5 * bit(x, 1) * bit(x, 2)
            aggregate[x] = Q(2 ** exponent)
    assert mtp2(aggregate, 3)
    # General (non-attractive) edge models are not closed: antiferromagnetic K3.
    ground = {1, 2, 3, 4, 5, 6}
    triangle = list(combinations(range(3), 2))
    assert support_local_recovery(ground, 3, triangle) != ground
    boundary = [Q(1, 6) if x in ground else Q(0) for x in range(8)]
    assert not mtp2(boundary, 3)
    return {"C4_ordered_separations": separations,
            "C4_even_product": str(even), "C4_odd_product": str(odd),
            "named_controls": 7}


def product_value(values):
    value = Q(1)
    for item in values:
        value *= item
    return value


if __name__ == "__main__":
    report = {"named": named_controls(),
              "supports": exhaustive_support_controls(),
              "flows": exact_flow_controls(),
              "status": "all independently designed exact controls passed"}
    print(json.dumps(report, indent=2, sort_keys=True))
