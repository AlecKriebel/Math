"""Fresh finite mechanism checks; no earlier audit code is imported.

Central homotopy uses formal noncommuting letters in the two central pieces,
and arbitrary cochain values, rather than a particular cocycle.
Free-word enumeration is a finite check, not an infinite-dimensional proof.
"""
from collections import Counter
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json


def add(out, value, sign=1):
    for term, coefficient in value.items():
        out[term] += sign * coefficient
        if not out[term]:
            del out[term]


def times(a, b):
    if a is None or b is None or a[0] != b[0]:
        return None
    return (a[0], a[1] + b[1])


def cut(a, color):
    return a if a is not None and a[0] == color else None


def left(a, value):
    if a is None or a[0] != "z":
        return Counter()
    return Counter({(a[1] + l, args, r): c for (l, args, r), c in value.items()})


def right(value, a):
    if a is None or a[0] != "z":
        return Counter()
    return Counter({(l, args, r + a[1]): c for (l, args, r), c in value.items()})


def formal(args):
    if any(a is None for a in args):
        return Counter()
    return Counter({((), tuple(args), ()): 1})


def differential(f, degree):
    def result(args):
        if any(a is None for a in args):
            return Counter()
        out = Counter()
        add(out, left(args[0], f(args[1:])))
        for j in range(degree):
            merged = args[:j] + (times(args[j], args[j + 1]),) + args[j + 2:]
            add(out, f(merged), (-1) ** (j + 1))
        add(out, right(f(args[:-1]), args[-1]), (-1) ** (degree + 1))
        return out
    return result


def homotopy(f, degree):
    def result(args):
        if degree <= 1 or any(a is None for a in args):
            return Counter()
        out = Counter()
        for j in range(degree - 1):
            inserted = tuple(cut(a, "z") for a in args[:j])
            inserted += (("q", ()), cut(args[j], "q")) + args[j + 1:]
            add(out, f(inserted), (-1) ** (j + 1))
        return out
    return result


central = []
for n in range(1, 10):
    dj = differential(homotopy(formal, n), n - 1)
    jd = homotopy(differential(formal, n), n + 1)
    count = 0
    for colors in product(("z", "q"), repeat=n):
        args = tuple((color, (f"a{i + 1}",)) for i, color in enumerate(colors))
        lhs = Counter()
        add(lhs, dj(args))
        add(lhs, jd(args))
        rhs = formal(args)
        add(rhs, formal(tuple(cut(a, "z") for a in args)), -1)
        assert lhs == rhs, (n, colors, lhs, rhs)
        count += 1
    central.append({"degree": n, "all_central_color_patterns": count, "passed": True})


def reduce_word(letters):
    result = []
    for label, sign in letters:
        if result and result[-1] == (label, -sign):
            result.pop()
        else:
            result.append((label, sign))
    return tuple(result)


blocks = []
for ds in ((0,), (1,), (2,), (3,), (0, 1), (1, 0), (1, 1), (0, 2, 0)):
    signs = tuple(sign for d in ds for sign in (1, -1) * d + (1,))
    coefficients = Counter()
    for labels in product(range(3), repeat=len(signs)):
        word = reduce_word(zip(labels, signs))
        assert word and word[0][1] == word[-1][1] == 1, (ds, labels, word)
        coefficients[word] += 1
    blocks.append({"ordered_block_degrees": ds, "original_terms": 3 ** len(signs),
                   "reduced_words": len(coefficients), "positive_endpoints": True})

catalan = []
for d in range(1, 6):
    signs = (-1, 1) * d
    leading = 0
    for labels in product(range(d), repeat=2 * d):
        if len(set(labels)) == d and not reduce_word(zip(labels, signs)):
            leading += 1
    expected = comb(2 * d, d) // (d + 1)
    factorial = 1
    for j in range(1, d + 1):
        factorial *= j
    assert leading == expected * factorial, (d, leading, expected)
    catalan.append({"moment_degree": d, "distinct_label_assignments": leading,
                    "Catalan_times_factorial": expected * factorial, "passed": True})

result = {"description": "Fresh symbolic and finite mechanism checks, not a proof of upstream vanishing",
          "central_homotopy": central, "ordered_free_blocks": blocks, "Catalan_leading_terms": catalan,
          "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
