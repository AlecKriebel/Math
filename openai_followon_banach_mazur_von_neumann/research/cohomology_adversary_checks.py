"""Exact finite boundary checks for upstream 295; no proof by sampling.

All computations use integers. Run with Python 3. This deliberately tests
the central homotopy on every cochain basis vector, not just cocycles.
"""
from collections import Counter
from itertools import product
from math import comb
import json
from pathlib import Path


def differential(table, n):
    """Hochschild d on A=C e0 + C e1, with coefficient module C e0."""
    out = {}
    for xs in product((0, 1), repeat=n + 1):
        value = (1 if xs[0] == 0 else 0) * table[xs[1:]]
        for j in range(n):
            if xs[j] == xs[j + 1]:
                merged = xs[:j] + (xs[j],) + xs[j + 2:]
                value += (-1) ** (j + 1) * table[merged]
        value += (-1) ** (n + 1) * table[xs[:-1]] * (1 if xs[-1] == 0 else 0)
        out[xs] = value
    return out


def homotopy(table, n):
    if n == 0:
        return None
    if n == 1:
        return {(): 0}
    out = {}
    for xs in product((0, 1), repeat=n - 1):
        value = 0
        for i in range(n - 1):
            # z a_j must survive before i; q a_i must survive at i.
            if all(x == 0 for x in xs[:i]) and xs[i] == 1:
                inserted = xs[:i] + (1, 1) + xs[i + 1:]
                value += (-1) ** (i + 1) * table[inserted]
        out[xs] = value
    return out


central_results = []
for n in range(7):
    tuples = list(product((0, 1), repeat=n))
    checked = 0
    for basis in tuples:
        table = {xs: int(xs == basis) for xs in tuples}
        jdf = homotopy(differential(table, n), n + 1)
        djf = {xs: 0 for xs in tuples} if n == 0 else differential(homotopy(table, n), n - 1)
        for xs in tuples:
            cut = table[xs] if all(x == 0 for x in xs) else 0
            assert djf[xs] + jdf[xs] == table[xs] - cut, (n, basis, xs)
            checked += 1
    central_results.append({"degree": n, "basis_cochains": len(tuples), "equations_checked": checked, "passed": True})


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


moment_results = []
for d in range(1, 5):
    catalan = comb(2 * d, d) // (d + 1)
    for r in range(1, 5):
        identities = 0
        leading = 0
        for labels in product(range(1, r + 1), repeat=2 * d):
            signed = tuple(label if i % 2 else -label for i, label in enumerate(labels))
            if not reduce_word(signed):
                identities += 1
                if len(set(labels)) == d:
                    leading += 1
        falling = 1
        for j in range(d):
            falling *= max(r - j, 0)
        assert leading == catalan * falling, (d, r, leading, catalan * falling)
        moment_results.append({"d": d, "r": r, "identity_assignments": identities,
                               "d_distinct_label_assignments": leading,
                               "catalan_times_falling_factorial": catalan * falling,
                               "passed": True})


block_results = []
for ds in ((0,), (1,), (2,), (0, 1), (1, 0), (1, 1), (0, 1, 0)):
    signs = []
    for d in ds:
        signs += [1 if j % 2 == 0 else -1 for j in range(2 * d + 1)]
    r = 3
    coefficients = Counter()
    for labels in product(range(1, r + 1), repeat=len(signs)):
        word = reduce_word(tuple(label * sign for label, sign in zip(labels, signs)))
        assert word and word[0] > 0 and word[-1] > 0, (ds, labels, word)
        coefficients[word] += 1
    block_results.append({"block_degrees": list(ds), "r": r, "degree": len(signs),
                          "terms_checked": r ** len(signs), "reduced_words": len(coefficients),
                          "no_scalar_and_positive_endpoints": True})


result = {"scope": "Exact finite checks only; not a computational proof of infinite-algebra vanishing.",
          "central_homotopy": central_results, "catalan_leading_counts": moment_results,
          "ordered_block_endpoints": block_results}
target = Path(__file__).with_name("cohomology_adversary_checks.json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"output": str(target), "central_equations": sum(x["equations_checked"] for x in central_results),
                  "moment_cases": len(moment_results), "block_cases": len(block_results), "passed": True}))
