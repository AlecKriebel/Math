"""Supplementary finite falsification checks; these do not prove the Borel theorem."""
from collections import Counter, deque
from itertools import product
from math import factorial
import json


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def lamp(x, index, amount, q):
    f, h = x
    out = list(f)
    out[index % len(f)] = (out[index % len(f)] + amount) % q
    return tuple(out), h


def shift(x, amount, height_period):
    f, h = x
    return tuple(f[(i - amount) % len(f)] for i in range(len(f))), (h + amount) % height_period


def coord(x, m, height_period):
    r = x[1] % m
    return shift(x, -r, height_period), r


def adjacent(x, m, q, height_period):
    r = x[1] % m
    values = {lamp(x, 0, a, q) for a in [-1, 1]}
    if r < m - 1:
        values.add(shift(x, 1, height_period))
    if r > 0:
        values.add(shift(x, -1, height_period))
    values.discard(x)
    return values


def reachable(seed, neighbors):
    found = {seed}
    pending = [seed]
    while pending:
        for y in neighbors(pending.pop()):
            if y not in found:
                found.add(y)
                pending.append(y)
    return found


def distance_map(seed, neighbors):
    result = {seed: 0}
    pending = deque([seed])
    while pending:
        x = pending.popleft()
        for y in neighbors(x):
            if y not in result:
                result[y] = result[x] + 1
                pending.append(y)
    return result


def compute():
    count = Counter()
    models = []
    wrong_sign = wrap = partial_shift_stabilizer = loops = 0
    # The configuration period and height period are allowed to differ.
    # As W-actions these are nonfree; some t^height_period stabilizers vary by point.
    for configuration_period, height_period, q in [(1, 1, 1), (3, 2, 2), (2, 6, 2), (3, 6, 2), (4, 4, 2)]:
        states = [(f, h) for f in product(range(q), repeat=configuration_period)
                  for h in range(height_period)]
        widths = [m for m in range(1, height_period + 1) if height_period % m == 0]
        fixed = [shift(x, height_period, height_period) == x for x in states]
        if any(fixed) and not all(fixed):
            partial_shift_stabilizer += 1
        for m in widths:
            component_sizes = Counter()
            unseen = set(states)
            for x in states:
                z, r = coord(x, m, height_period)
                need(z[1] % m == 0, 'base residue')
                need(shift(z, r, height_period) == x, 'coordinate inverse')
                need(coord(shift(z, r, height_period), m, height_period) == (z, r), 'two-sided inverse')
                for amount in [-1, 1]:
                    need(coord(lamp(x, 0, amount, q), m, height_period) ==
                         (lamp(z, -r, amount, q), r), 'conjugation sign with nonfree action')
                    if lamp(x, 0, amount, q) == x:
                        loops += 1
                    if lamp(z, -r, amount, q) != lamp(z, r, amount, q):
                        wrong_sign += 1
                if r < m - 1:
                    need(coord(shift(x, 1, height_period), m, height_period) == (z, r + 1), 'vertical edge')
                else:
                    wrapped = coord(shift(x, 1, height_period), m, height_period)
                    need(wrapped[1] == 0, 'wrap residue')
                    if wrapped[0] != z:
                        wrap += 1
                neighbors = lambda y: adjacent(y, m, q, height_period)
                need(len(neighbors(x)) <= 4 and x not in neighbors(x), 'bounded degree and no loops')
                need(all(x in neighbors(y) for y in neighbors(x)), 'edge symmetry')
                base_neighbors = lambda y: {lamp(y, -j, amount, q)
                                            for j in range(m) for amount in [-1, 1]} - {y}
                base_component = reachable(z, base_neighbors)
                predicted = {shift(w, s, height_period) for w in base_component for s in range(m)}
                actual = reachable(x, neighbors)
                need(actual == predicted, 'complete component product with stabilizers')
                # Short slab paths must project to base word balls even if colors of
                # their intermediate points are arbitrary.
                base_distances = distance_map(z, base_neighbors)
                for y, length in distance_map(x, neighbors).items():
                    w, _ = coord(y, m, height_period)
                    need(base_distances[w] <= length, 'short-path projection')
                    count['projected_pairs'] += 1
                count['vertex_checks'] += 1
                if x in unseen:
                    unseen.difference_update(actual)
                    component_sizes[len(actual)] += 1
            for n in widths:
                if n % m == 0:
                    for x in states:
                        need(adjacent(x, m, q, height_period) <= adjacent(x, n, q, height_period), 'divisor inclusion')
                        count['divisor_inclusions'] += 1
            models.append({'configuration_period': configuration_period, 'height_period': height_period,
                           'lamp_modulus': q, 'width': m, 'component_inventory': dict(component_sizes)})
    need(loops > 0, 'trivial-lamp loop model missing')
    need(partial_shift_stabilizer > 0, 'varying point-stabilizer model missing')
    need(wrong_sign > 0 and wrap > 0, 'negative control lacks witnesses')

    # Integer residues use Python's nonnegative remainder, including at negative height.
    for h in range(-40, 41):
        appearances = [h % factorial(n) < factorial(n) - 1 for n in range(1, 9)]
        need(any(appearances) == (h != -1), 'persistent factorial cut at finite tested heights')
        need(appearances == sorted(appearances), 'factorial inclusion at negative heights')
        count['integer_heights'] += 1
    # The noninteger profinite element obtained as a compatible factorial expansion
    # sum_{k>=2} k! has a finite-stage short-path witness for each tested translated edge.
    # This finite residue test is evidence only; nonintegrality is not inferred here.
    residues = {n: sum(factorial(k) for k in range(2, n)) % factorial(n) for n in range(1, 11)}
    for n in range(1, 10):
        need(residues[n + 1] % factorial(n) == residues[n], 'compatible factorial expansion')
        count['compatible_factorial_coordinates'] += 1

    # Finite surrogate of B x Z with merging finite base relations.
    base = list(range(8))
    heights = range(-6, 7)
    space = [(b, h) for b in base for h in heights]
    previous = set()
    for stage in range(7):
        width = 2 ** min(stage, 3)
        relation = {(x, y) for x in space for y in space
                    if x == y or (abs(x[1]) <= stage and abs(y[1]) <= stage
                                  and x[0] // width == y[0] // width)}
        need(previous <= relation, 'finite relation inclusion')
        classes = {x: {y for y in space if (x, y) in relation} for x in space}
        for x in space:
            need(x in classes[x], 'reflexivity')
            need(all(classes[y] == classes[x] for y in classes[x]), 'equivalence classes')
            need(len(classes[x]) <= (2 * stage + 1) * width, 'finite band size')
            count['exceptional_classes'] += 1
        previous = relation
    need(len(previous) == len(space) ** 2, 'full tested exceptional exhaustion')
    return {'schema': 1, 'all_checks_passed': True, 'scope': 'finite diagnostic evidence only',
            'counts': dict(count), 'models': models,
            'controls': {'wrong_sign_witnesses': wrong_sign, 'wrap_witnesses': wrap,
                         'loop_witnesses': loops, 'models_with_varying_shift_stabilizers': partial_shift_stabilizer},
            'infinite_theorem_verified': False}


if __name__ == '__main__':
    print(json.dumps(compute(), indent=2, sort_keys=True))
