#!/usr/bin/env python3
"""Independent exact derivations; no imports from the audited checker."""
from collections import Counter
from fractions import Fraction
from itertools import permutations, product
import json


def need(value, why):
    if not value:
        raise RuntimeError(why)


def compose(p, q):
    return tuple(p[x] for x in q)


def inverse(p):
    return tuple(p.index(x) for x in range(len(p)))


def wreath():
    s3 = list(permutations(range(3)))
    group = []
    coordinates = {}
    for a, b, swap in product(s3, s3, range(2)):
        perm = tuple(3 + b[i] for i in range(3)) + a if swap else a + tuple(3 + b[i] for i in range(3))
        coordinates[perm] = (a, b, swap)
        group.append(perm)
    group.sort()
    index = {p: i for i, p in enumerate(group)}
    unit = index[tuple(range(6))]
    table = [[index[compose(p, q)] for q in group] for p in group]
    inverses = [index[inverse(p)] for p in group]

    def extend(subgroup, extra):
        generators = tuple(subgroup) + (extra, inverses[extra])
        closure = set(subgroup)
        pending = list(subgroup)
        while pending:
            element = pending.pop()
            for gen in generators:
                value = table[gen][element]
                if value not in closure:
                    closure.add(value)
                    pending.append(value)
        return frozenset(closure)

    all_groups = {frozenset([unit])}
    pending = list(all_groups)
    while pending:
        subgroup = pending.pop()
        for extra in range(len(group)):
            if extra not in subgroup:
                generated = extend(subgroup, extra)
                if generated not in all_groups:
                    all_groups.add(generated)
                    pending.append(generated)
    choices = 0
    swap_subgroups = 0
    for subgroup in all_groups:
        unswapped = [coordinates[group[i]] for i in subgroup if not coordinates[group[i]][2]]
        swapped = [i for i in subgroup if coordinates[group[i]][2]]
        b1 = {a for a, _, _ in unswapped}
        if swapped:
            swap_subgroups += 1
        for t in swapped:
            choices += 1
            a, b, _ = coordinates[group[t]]
            c = tuple(range(3)) + tuple(3 + a[i] for i in range(3))
            conjugates = [compose(compose(c, group[i]), inverse(c)) for i in subgroup]
            need(all(coordinates[p][0] in b1 and coordinates[p][1] in b1 for p in conjugates), 'Wreath containment')
            need(coordinates[compose(compose(c, group[t]), inverse(c))] == (tuple(range(3)), compose(a, b), 1), 'Wreath conjugator')
    need(len(all_groups) == 112 and swap_subgroups == 52, 'Subgroup counts')
    return {'representation': 'Permutations of six points preserving or interchanging two three-point blocks',
            'all_subgroups': len(all_groups), 'subgroups_with_swap': swap_subgroups,
            'all_swap_representative_choices_checked': choices,
            'subgroup_order_distribution': dict(sorted(Counter(len(h) for h in all_groups).items()))}


def matrix():
    a = [[0, 0, 0, -1], [1, 0, 0, -1], [0, 1, 0, -1], [0, 0, 1, -1]]
    def act(v):
        return tuple(sum(x * y for x, y in zip(row, v)) for row in a)
    basis = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    images = [basis]
    for _ in range(5):
        images.append([act(v) for v in images[-1]])
    need(images[5] == basis and len({tuple(x) for x in images[:5]}) == 5, 'Order five')
    gram = [[sum(sum(x * y for x, y in zip(power[i], power[j])) for power in images[:5]) for j in range(4)] for i in range(4)]
    def determinant(m):
        return sum((-1) ** sum(p[i] > p[j] for i in range(len(m)) for j in range(i+1, len(m)))
                   * __import__('math').prod(m[i][p[i]] for i in range(len(m))) for p in permutations(range(len(m))))
    need(determinant(a) == 1, 'Determinant')
    need(gram == [[8 if i == j else -2 for j in range(4)] for i in range(4)], 'Gram matrix')
    need(determinant(gram) == 2000, 'Gram determinant')
    # Q=10I-2J, so the all-ones vector has eigenvalue 2 and its orthogonal complement eigenvalue 10.
    need(all(sum(row) == 2 for row in gram), 'Positive eigenvalue on invariant line')
    return {'method': 'Column-vector iteration and Leibniz determinant', 'gram': gram,
            'gram_determinant': determinant(gram), 'exact_eigenvalues': [2, 10, 10, 10]}


def rational_averaging():
    def r(v):
        return (-v[1], v[0] - v[1])
    def add(v, w):
        return tuple(x+y for x, y in zip(v, w))
    checked = 0
    for z1 in product(range(-3, 4), repeat=2):
        z = [(0, 0), z1, add(z1, r(z1))]
        v = tuple(Fraction(sum(x[j] for x in z), 3) for j in range(2))
        for i, j in product(range(3), repeat=2):
            acted = z[j]
            for _ in range(i):
                acted = r(acted)
            need(z[(i+j) % 3] == add(z[i], acted), 'Cocycle identity')
        acted = v
        for i in range(3):
            need(z[i] == tuple(x-y for x, y in zip(v, acted)), 'Averaging coboundary identity')
            acted = r(acted)
        checked += 1
    return {'C3_rational_plane_cocycles': checked, 'division_by_group_order_used': True}


def countermodel():
    # Construct multiplication from the independently checked involutory automorphism.
    def alpha(n, z):
        return -n, (z+n) % 2
    points = list(product(range(-5, 6), range(2)))
    for n, z in points:
        need(alpha(*alpha(n, z)) == (n, z), 'Order-two automorphism')
        for m, w in points:
            need(alpha(n+m, (z+w)%2) == ((-n-m), ((z+n)+(w+m))%2), 'Additive automorphism')
    def multiply(x, y):
        n, z, e = x
        m, w, d = y
        if e:
            m, w = alpha(m, w)
        return n+m, (z+w)%2, (e+d)%2
    parity_checks = 0
    for n, z in product(range(-10, 11), range(2)):
        square = multiply((n, z, 1), (n, z, 1))
        need(square == (0, n%2, 0), 'Reflection square')
        parity_checks += 1
    return {'automorphism_samples': len(points), 'reflection_square_checks': parity_checks,
            'odd_reflections_no_order_two_lift': True, 'even_reflections_lift': True}


def character_ranks():
    def rank(rows, prime):
        span = {tuple(0 for _ in rows[0])}
        for v in rows:
            span = {tuple((x + k*y) % prime for x, y in zip(w, v)) for w in span for k in range(prime)}
        size = len(span)
        dimension = 0
        while size > 1:
            need(size % prime == 0, 'Prime-power span size')
            size //= prime
            dimension += 1
        return dimension
    binary = list(product(range(2), repeat=4))
    maxima = set()
    for a, b, c in product(binary, repeat=3):
        d = tuple((x+y+z) % 2 for x, y, z in zip(a, b, c))
        maxima.add(rank([a, b, c, d], 2))
    need(max(maxima) == 3, 'SO4 binary bound')
    odd = {}
    for p in (3, 5):
        vectors = list(product(range(p), repeat=3))
        maximum = max(rank([a, b], p) for a, b in product(vectors, repeat=2))
        need(maximum == 2, 'Two rotation planes cannot be faithful at rank three')
        odd[str(p)] = {'systems': len(vectors)**2, 'maximum_character_rank': maximum}
    return {'binary_systems': 4096, 'binary_max_rank': 3, 'odd_prime_pair_checks': odd,
            'scope': 'Finite examples corroborate the all-prime representation-theoretic proof.'}


if __name__ == '__main__':
    result = {'status': 'PASS', 'torus': matrix(), 'rational_averaging': rational_averaging(),
              'countermodel': countermodel(), 'wreath': wreath(), 'character_ranks': character_ranks()}
    print(json.dumps(result, indent=2))
