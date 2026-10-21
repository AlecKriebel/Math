#!/usr/bin/env python3
"""Exact, standard-library checks of the submitted exponent/facet/chamber data.

This does not establish the canonical-potential normalization: independent
mutation reconstruction and primary-source checks are separate requirements.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
WORD = (1, 2, 3, 2, 4, 2, 1, 2, 3, 2, 4, 2)
N = len(WORD)
EDGES = {(1, 2), (2, 3), (2, 4)}


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cartan(i, j):
    return 2 if i == j else -1 if tuple(sorted((i, j))) in EDGES else 0


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def rank(rows):
    m = [[Fraction(v) for v in row] for row in rows]
    r = 0
    for c in range(len(m[0])):
        pivot = next((i for i in range(r, len(m)) if m[i][c]), None)
        if pivot is None:
            continue
        m[r], m[pivot] = m[pivot], m[r]
        scale = m[r][c]
        m[r] = [v / scale for v in m[r]]
        for i in range(len(m)):
            if i != r:
                scale = m[i][c]
                m[i] = [v - scale * w for v, w in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def add(*polynomials):
    out = Counter()
    for p in polynomials:
        out.update(p)
    return out


def mul(*polynomials):
    out = Counter({(0,) * N: 1})
    for p in polynomials:
        product = Counter()
        for a, ca in out.items():
            for b, cb in p.items():
                product[tuple(x + y for x, y in zip(a, b))] += ca * cb
        out = product
    return out


def variable(k):
    a = [0] * N
    a[k - 1] = 1
    return Counter({tuple(a): 1})


def require(check, message):
    if not check:
        raise ValueError(message)


def validate_separators(rows, separators):
    require(len(rows) == len(separators) == 22, "Wrong number of certificates")
    table = [[dot(a, z) for z in separators] for a in rows]
    require(all(table[i][i] == -1 for i in range(22)), "Diagonal is not -1")
    require(all(table[i][j] >= 0 for i in range(22) for j in range(22) if i != j),
            "Negative off-diagonal product")
    return table


def main():
    raw = (HERE / "submitted/PROOF.md").read_bytes()
    text = raw.decode()
    matches = re.findall(r"^\|(\d+)\|([012]{12})\|\(([-\d,]+)\)\|$", text, re.M)
    require([int(m[0]) for m in matches] == list(range(1, 23)), "Nonsequential table")
    rows = [tuple(int(v) for v in m[1]) for m in matches]
    zs = [tuple(int(v) for v in m[2].split(",")) for m in matches]
    require(all(len(z) == N for z in zs), "Wrong vector dimension")
    products = validate_separators(rows, zs)

    one = Counter({(0,) * N: 1})
    y = {k: variable(k) for k in range(1, N + 1)}
    a = add(one, y[3], mul(y[2], y[3]))
    b = mul(y[2], y[3], y[4], y[5])
    f7 = add(one, y[6], mul(y[6], y[8], a),
             mul(y[6], y[8], y[10],
                 add(mul(add(one, y[5]), a),
                     mul(b, add(one, y[6], mul(y[1], y[6]))))))
    f9 = add(one, y[8], mul(y[8], y[10], add(one, y[5], mul(y[4], y[5]))))
    potential = add(mul(y[7], f7), mul(y[9], f9),
                    mul(y[11], add(one, y[10])), y[12])
    require(len(potential) == 22 and set(potential.values()) == {1}, "Support or coefficient")
    require(set(rows) == set(potential), "Expanded formula differs from table")
    require([i + 1 for i, a in enumerate(rows) if max(a) > 1] == [21, 22], "High exponents")
    require(all(a[5] == 2 for a in rows[20:]), "Wrong squared coordinate")
    k_matrix = [[0] * N for _ in range(N)]
    for k in range(N):
        nxt = next((l for l in range(k + 1, N) if WORD[l] == WORD[k]), N)
        k_matrix[k][k] = 1
        if nxt < N:
            k_matrix[k][nxt] = 1
        for l in range(k + 1, nxt):
            k_matrix[k][l] = cartan(WORD[k], WORD[l])
    transformed = multiply(rows, k_matrix)
    require(all(abs(v) <= 1 for a in transformed for v in a), "Pullback exponent bound")
    require(transformed[20] == [0, 1, 0, 1, 0, 1, -1, 0, 0, 0, 0, 0], "Row21 pullback")
    require(transformed[21] == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "Row22 pullback")
    require(all(k_matrix[i][j] == 0 for i in range(N) for j in range(i)), "Not triangular")
    require(all(k_matrix[i][i] == 1 for i in range(N)), "Nonunimodular diagonal")

    product = [[int(i == j) for j in range(4)] for i in range(4)]
    roots = []
    for letter in WORD:
        roots.append(tuple(product[i][letter - 1] for i in range(4)))
        reflection = [[int(i == j) - (cartan(letter, j + 1) if i == letter - 1 else 0)
                       for j in range(4)] for i in range(4)]
        product = multiply(product, reflection)
    require(len(set(roots)) == 12 and all(all(v >= 0 for v in a) and any(a) for a in roots),
            "Root sequence not twelve distinct positives")
    require(product == [[-int(i == j) for j in range(4)] for i in range(4)], "Not w0=-I")
    require(rank(rows) == N, "Cone normals fail full span")
    require(all(sum(a) > 0 for a in rows), "Missing strict interior point")
    facets = []
    for j, (a, z) in enumerate(zip(rows, zs)):
        point = [Fraction(v) + Fraction(1, sum(a)) for v in z]
        require(dot(a, point) == 0, "Facet point not on hyperplane")
        require(all(dot(other, point) > 0 for i, other in enumerate(rows) if i != j),
                "Facet point violates strictness")
        facets.append([str(v) for v in point])

    controls = []
    bad = list(zs)
    bad[0] = (0,) * N
    try:
        validate_separators(rows, bad)
    except ValueError:
        controls.append("zero separating vector rejected")
    altered = list(rows)
    altered[20] = tuple(1 if i == 5 else v for i, v in enumerate(rows[20]))
    require(set(altered) != set(potential), "Exponent-tamper negative control did not differ")
    controls.append("squared-exponent removal rejected by polynomial identity")
    transpose = list(map(list, zip(*k_matrix)))
    require(any(abs(v) > 1 for a in multiply(rows, transpose) for v in a),
            "Transpose control unexpectedly passes bound")
    controls.append("transposed chamber map rejected by exponent bound")
    require(len(controls) == 3, "Negative control failure")
    result = {"proof_sha256": hashlib.sha256(raw).hexdigest(), "terms": len(rows),
              "all_coefficients": 1, "canonical_max_exponent": 2,
              "squared_coordinate_one_based": 6, "separator_products": products,
              "strict_facet_points": facets, "normal_rank": rank(rows),
              "cone_full_dimensional": True, "cone_pointed": True,
              "roots": roots, "w0_product": product, "chamber_K": k_matrix,
              "chamber_K_determinant": 1, "transformed_rows": transformed,
              "transformed_max_abs_exponent": max(abs(v) for a in transformed for v in a),
              "negative_controls": controls,
              "remaining": ["Independent canonical-potential reconstruction",
                            "Primary-source identification of original target", "Priority audit"]}
    (HERE / "ROOT_EXACT_VERIFICATION.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                      {"separator_products", "strict_facet_points", "roots", "w0_product",
                       "chamber_K", "transformed_rows"}}, indent=2))


if __name__ == "__main__":
    main()
