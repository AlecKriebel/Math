"""Independent exact lifted-cover cochains and finite-observation controls.

No imports from the author packet. All matrices are derived from lifted cells.
Finite controls support the separately written proofs; they do not prove
recognizability, Cech continuity, or the infinite obstruction by enumeration.
"""
from fractions import Fraction
from math import gcd
import hashlib
import json

assertions = 0
categories = {}


def check(ok, category):
    global assertions
    if not ok:
        raise AssertionError(category)
    assertions += 1
    categories[category] = categories.get(category, 0) + 1


def zero(m, n):
    return [[0 for _ in range(n)] for _ in range(m)]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(col) for col in zip(*a)]


def multiply(a, b):
    cols = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in cols] for row in a]


def reduced(a):
    a = [list(map(Fraction, row)) for row in a]
    pivots = []
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                value = a[i][col]
                a[i] = [x - value * y for x, y in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a, pivots


def rank(a):
    return len(reduced(a)[1])


def kernel(a):
    rref, pivots = reduced(a)
    vectors = []
    for j in range(len(a[0])):
        if j not in pivots:
            vector = [Fraction(0) for _ in range(len(a[0]))]
            vector[j] = 1
            for i, p in enumerate(pivots):
                vector[p] = -rref[i][j]
            vectors.append(vector)
    return transpose(vectors)


def joined_rank(a, b):
    return rank([x + y for x, y in zip(a, b)])


def cells(q, u, v):
    """Chain boundary from oriented lifted edges and square boundary paths."""
    inc = (u, v, u, v)
    edge = lambda g, label: 4 * (g % q) + label
    b1, b2 = zero(q, 4 * q), zero(4 * q, 4 * q)
    for g in range(q):
        for label in range(4):
            b1[g][edge(g, label)] -= 1
            b1[(g + inc[label]) % q][edge(g, label)] += 1
        for x in range(2):
            for y in range(2):
                face = 4 * g + 2 * x + y
                path = ((g, x, 1), (g + inc[x], y + 2, 1),
                        (g + inc[y + 2], x, -1), (g, y + 2, -1))
                for state, label, sign in path:
                    b2[edge(state, label)][face] += sign
    return b1, b2


def betti(q, b1, b2):
    r1, r2 = rank(b1), rank(b2)
    return [q - r1, 4 * q - r1 - r2, 4 * q - r2]


WORDS = ((0, 0, 1), (0, 1))


def lifted_substitution(q, u, v):
    """Actual cellular lift from monodromy (2u+v,u+v) to (u,v).

    A target path starts at the source sheet g. A square maps to the
    tau(x) by tau(y) rectangular grid, with each tile sheet obtained by
    both prefix transports. This tests the model beyond a fixed cover.
    """
    inc = (u, v)
    f1, f2 = zero(4 * q, 4 * q), zero(4 * q, 4 * q)
    for g in range(q):
        for direction in range(2):
            for label in range(2):
                sheet = g
                for letter in WORDS[label]:
                    f1[4 * (sheet % q) + 2 * direction + letter][4 * g + 2 * direction + label] += 1
                    sheet += inc[letter]
        for x in range(2):
            for y in range(2):
                sx = 0
                for letter_x in WORDS[x]:
                    sy = 0
                    for letter_y in WORDS[y]:
                        target = 4 * ((g + sx + sy) % q) + 2 * letter_x + letter_y
                        f2[target][4 * g + 2 * x + y] += 1
                        sy += inc[letter_y]
                    sx += inc[letter_x]
    return identity(q), f1, f2


def projection(q, Q):
    answer = []
    for n in (1, 4, 4):
        p = zero(n * q, n * Q)
        for g in range(Q):
            for c in range(n):
                p[n * (g % q) + c][n * g + c] = 1
        answer.append(p)
    return answer


cover_records = []
for q in range(1, 25):
    for u, v in ((1, 0), (2, 1), (5, 3), (0, 0), (2, 0)):
        b1, b2 = cells(q, u, v)
        h = gcd(gcd(q, u), v)
        check(multiply(b1, b2) == zero(q, 4 * q), "lifted_boundary_squared")
        bs = betti(q, b1, b2)
        check(bs == [h, 4 * h, q + 3 * h], "actual_cover_betti")
        cover_records.append({"q": q, "monodromy": [u, v], "components": h, "betti": bs})

substitution_records = []
for q in (1, 2, 3, 4, 5, 6, 8, 12):
    u, v = 1, 0
    for level in range(4):
        next_u, next_v = 2 * u + v, u + v
        a1, a2 = cells(q, u, v)
        b1, b2 = cells(q, next_u, next_v)
        f0, f1, f2 = lifted_substitution(q, u, v)
        check(multiply(a1, f1) == multiply(f0, b1), "substitution_chain_degree1")
        check(multiply(a2, f2) == multiply(f1, b2), "substitution_chain_degree2")
        check(gcd(gcd(q, next_u), next_v) == 1, "substitution_surjective_monodromy")
        image_h1 = joined_rank(a2, multiply(f1, kernel(b1))) - rank(a2)
        image_h2 = rank(multiply(f2, kernel(b2)))
        check(image_h1 == 4, "actual_lifted_H1_isomorphism")
        check(image_h2 == q + 3, "actual_lifted_H2_isomorphism")
        substitution_records.append({"q": q, "level": level, "target_monodromy": [u, v],
                                     "source_monodromy": [next_u, next_v],
                                     "homology_image_ranks": [1, image_h1, image_h2]})
        u, v = next_u, next_v

transfer_records = []
for q in (1, 2, 3, 4, 5, 6, 8, 12):
    for u, v in ((1, 0), (2, 1), (13, 8)):
        a1, a2 = cells(q, u, v)
        b1, b2 = cells(2 * q, u, v)
        p0, p1, p2 = projection(q, 2 * q)
        check(multiply(a1, p1) == multiply(p0, b1), "reduction_chain_degree1")
        check(multiply(a2, p2) == multiply(p1, b2), "reduction_chain_degree2")
        check(multiply(p1, transpose(b1)) == multiply(transpose(a1), p0), "transfer_is_cochain_degree0")
        check(multiply(p2, transpose(b2)) == multiply(transpose(a2), p1), "transfer_is_cochain_degree1")
        for p in (p0, p1, p2):
            check(multiply(p, transpose(p)) == [[2 * z for z in row] for row in identity(len(p))],
                  "transfer_pullback_twice_identity")
        cochain_image = joined_rank(transpose(b2), transpose(p2)) - rank(b2)
        check(cochain_image == q + 3, "actual_cover_H2_pullback_injective")
        transfer_records.append({"q": q, "monodromy": [u, v], "H2_image_rank": cochain_image})


def tau(word):
    return "".join("aab" if letter == "a" else "ab" for letter in word)


word = "a"
for _ in range(8):
    word = tau(word)


def signed_transport(word, start, end):
    if end >= start:
        return word[start:end].count("a")
    return -word[end:start].count("a")


def shift(point, n, m, modulus):
    i, j, g = point
    step = signed_transport(word, i, i + n) + signed_transport(word, j, j + m)
    return i + n, j + m, (g + step) % modulus


def observation(point, k):
    i, j, g = point
    return word[i - 1:i + 2], word[j - 1:j + 2], g % (2 ** k)


generator_records = []
for k in range(1, 9):
    modulus = 2 ** (k + 3)
    h = 2 ** k
    for g in range(8):
        p, r = (100, 120, g), (100, 120, g + h)
        for n in range(-7, 8):
            for m in range(-7, 8):
                p1, r1 = shift(p, n, m, modulus), shift(r, n, m, modulus)
                check(p1[:2] == r1[:2] and (r1[2] - p1[2]) % modulus == h, "actual_action_tail_difference")
                check(observation(p1, k) == observation(r1, k), "actual_finite_observation_not_generator")
                check(shift(p1, -n, -m, modulus) == p, "actual_signed_action_inverse")
                reduced_point = (p[0], p[1], p[2] % (2 ** k))
                check(tuple((*p1[:2], p1[2] % (2 ** k))) == shift(reduced_point, n, m, 2 ** k),
                      "actual_action_quotient_compatibility")
        check(shift(shift(p, 3, -2, modulus), -5, 6, modulus) == shift(p, -2, 4, modulus),
              "actual_action_cocycle_law")
    generator_records.append({"observation_level": k, "distinct_pair_difference": h,
                              "modulus": modulus, "tested_shift_box": [-7, 7]})

# Boundary-condition controls that defeat unsafe generalizations.
check(betti(4, *cells(4, 0, 0)) == [4, 16, 16], "minimal_base_does_not_make_zero_extension_minimal")
check(betti(4, *cells(4, 2, 0)) == [2, 8, 10], "surjectivity_needed_for_connected_Betti_tuple")

result = {"assertions": assertions, "categories": categories, "cover_records": cover_records,
          "lifted_substitution_records": substitution_records, "transfer_records": transfer_records,
          "finite_observation_records": generator_records,
          "scope": "Independent exact actual lifted cells, changing substitution monodromy, cohomology transfer, and signed actions; no author imports and no novelty or full target certification."}
print(json.dumps(result, sort_keys=True, indent=2))
