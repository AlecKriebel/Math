#!/usr/bin/env python3
"""Independent finite controls for KP-4.26. No geometric certification.

This implementation builds SL(2,5) from its action on the 24 nonzero vectors,
rather than enumerating determinant-one matrices. It also constructs the
diagonal quotient directly in a finite cyclic product. Python standard library.
"""
from collections import Counter, deque
from itertools import permutations, product
from fractions import Fraction
import json

checks = 0


def check(value):
    global checks
    checks += 1
    if not value:
        raise AssertionError("Independent control failed")


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def generated_permutations(generators, degree):
    identity = tuple(range(degree))
    found = {identity}
    pending = [identity]
    while pending:
        p = pending.pop()
        for q in generators:
            r = compose(p, q)
            if r not in found:
                found.add(r)
                pending.append(r)
    return sorted(found)


def group_data(elements):
    index = {g: i for i, g in enumerate(elements)}
    one = index[tuple(range(len(elements[0])))]
    table = [[index[compose(a, b)] for b in elements] for a in elements]
    inverse = [next(j for j in range(len(elements)) if table[i][j] == one)
               for i in range(len(elements))]
    return one, table, inverse


def normal_closure(seeds, one, table, inverse):
    conjugates = {table[table[h][s]][inverse[h]]
                  for h in range(len(table)) for s in seeds}
    # Right multiplication by all conjugates enumerates the subgroup. In a
    # finite group the generated monoid equals the generated subgroup.
    found = {one}
    pending = deque([one])
    while pending:
        h = pending.popleft()
        for s in conjugates:
            hs = table[h][s]
            if hs not in found:
                found.add(hs)
                pending.append(hs)
    return found


def analyze(elements, direct_product_check=False):
    one, table, inverse = group_data(elements)
    n = len(elements)

    def commutator(a, b):
        return table[table[table[a][b]][inverse[a]]][inverse[b]]

    derived = normal_closure({commutator(a, b) for a in range(n) for b in range(n)},
                             one, table, inverse)
    unseen = set(range(n))
    rows = []
    while unseen:
        g = min(unseen)
        conjugates = {table[table[h][g]][inverse[h]] for h in range(n)}
        check(conjugates <= unseen)
        unseen -= conjugates
        normal = normal_closure({g}, one, table, inverse)
        centralized = normal_closure({commutator(g, x) for x in range(n)},
                                     one, table, inverse)
        check(centralized <= normal)
        order = 1
        power = g
        while power != one:
            power = table[power][g]
            order += 1
        row = {"class_size": len(conjugates), "element_order": order,
               "normal_closure_order": len(normal),
               "commutator_normal_closure_order": len(centralized),
               "centralizing_quotient_order": n // len(centralized)}
        if direct_product_check:
            # The relation t=g^-1 implies t^order(g)=1, so replacing Z by
            # C_order(g) leaves this quotient unchanged. Compute its normal
            # subgroup directly from conjugates of (1,g).
            generators = {(1 % order, h) for h in conjugates}
            found = {(0, one)}
            pending = deque([(0, one)])
            while pending:
                i, h = pending.popleft()
                for j, s in generators:
                    hs = ((i + j) % order, table[h][s])
                    if hs not in found:
                        found.add(hs)
                        pending.append(hs)
            quotient_order = order * n // len(found)
            check(quotient_order == n // len(centralized))
            row["direct_diagonal_quotient_order"] = quotient_order
        if len(derived) == n:
            check((len(normal) == n) == (len(centralized) == n))
        rows.append(row)
    check(sum(r["class_size"] for r in rows) == n)
    return {"order": n, "derived_order": len(derived),
            "classes": sorted(rows, key=lambda r: (r["element_order"], r["class_size"]))}


vectors = [v for v in product(range(5), repeat=2) if v != (0, 0)]
index = {v: i for i, v in enumerate(vectors)}
upper = tuple(index[((x + y) % 5, y)] for x, y in vectors)
lower = tuple(index[(x, (x + y) % 5)] for x, y in vectors)
binary_icosahedral = analyze(generated_permutations([upper, lower], 24), True)
check(binary_icosahedral["order"] == 120)
check(binary_icosahedral["derived_order"] == 120)
check(len(binary_icosahedral["classes"]) == 9)
check(Counter(r["centralizing_quotient_order"] for r in binary_icosahedral["classes"])
      == Counter({1: 7, 120: 2}))
check(sum(r["class_size"] for r in binary_icosahedral["classes"]
          if r["normal_closure_order"] == 120) == 118)
central_involution = next(r for r in binary_icosahedral["classes"] if r["element_order"] == 2)
check(central_involution["normal_closure_order"] == 2)
check(central_involution["commutator_normal_closure_order"] == 1)

symmetric_three = analyze(list(permutations(range(3))), True)
transposition = next(r for r in symmetric_three["classes"] if r["element_order"] == 2)
check(symmetric_three["derived_order"] == 3)
check(transposition["normal_closure_order"] == 6)
check(transposition["centralizing_quotient_order"] == 2)
cyclic_five = analyze(generated_permutations([tuple((i + 1) % 5 for i in range(5))], 5), True)
check(cyclic_five["derived_order"] == 1)
check(all(r["centralizing_quotient_order"] == 5 for r in cyclic_five["classes"]))


def rank(matrix):
    rows = [[Fraction(a) for a in row] for row in matrix]
    if not rows:
        return 0
    pivot = 0
    for col in range(len(rows[0])):
        chosen = next((i for i in range(pivot, len(rows)) if rows[i][col]), None)
        if chosen is None:
            continue
        rows[pivot], rows[chosen] = rows[chosen], rows[pivot]
        coefficient = rows[pivot][col]
        rows[pivot] = [a / coefficient for a in rows[pivot]]
        for i in range(pivot + 1, len(rows)):
            coefficient = rows[i][col]
            rows[i] = [a - coefficient*b for a, b in zip(rows[i], rows[pivot])]
        pivot += 1
    return pivot


mv_controls = []
for longitude, meridian in product((-1, 1), repeat=2):
    maps = [rank([[1], [-1]]), rank([[longitude]]), rank([[meridian]]), 0, 0]
    source = [1, 1, 1, 1, 0]
    target = [2, 1, 1, 0, 0]
    betti = [target[i] - maps[i] + (source[i-1] - maps[i-1] if i else 0)
             for i in range(5)]
    check(betti == [1, 0, 0, 0, 1])
    check(abs(longitude) == abs(meridian) == 1)
    mv_controls.append({"degree_1_unit": longitude, "degree_2_unit": meridian,
                        "betti": betti})

# Independent signed permutation expansion of the abelianization determinant.
matrix = [[2, -3, 0], [0, 3, -5], [-1, -1, 4]]
determinant = 0
for p in permutations(range(3)):
    sign = (-1)**sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3))
    term = sign
    for i in range(3):
        term *= matrix[i][p[i]]
    determinant += term
check(determinant == -1)

print(json.dumps({"scope": "Finite algebra controls only; no smooth embedding or standardness certificate",
                  "checks": checks, "sl2_f5_permutation_model": binary_icosahedral,
                  "s3_nonperfect_control": symmetric_three,
                  "c5_nonperfect_control": cyclic_five,
                  "primitive_circle_mv_sign_controls": mv_controls,
                  "abelianization_determinant": determinant}, indent=2, sort_keys=True))
