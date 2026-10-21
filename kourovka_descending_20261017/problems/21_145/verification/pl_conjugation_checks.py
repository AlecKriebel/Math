#!/usr/bin/env python3
"""Supplementary exact checks of restricted Thompson-F construction failures.

These finite examples do not settle either quasi-isometry question.
All piecewise-linear maps use ordinary function composition on [0,1].
"""
from fractions import Fraction as Q
from bisect import bisect_right
from pathlib import Path
import json

if not __debug__:
    raise RuntimeError("Run without Python optimization: checks use assertions")

IDENTITY = [(Q(0), Q(0)), (Q(1), Q(1))]
X0 = [(Q(0), Q(0)), (Q(1, 2), Q(1, 4)),
      (Q(3, 4), Q(1, 2)), (Q(1), Q(1))]
X1 = [(Q(0), Q(0)), (Q(1, 2), Q(1, 2)),
      (Q(3, 4), Q(5, 8)), (Q(7, 8), Q(3, 4)), (Q(1), Q(1))]


def value(f, t):
    i = min(bisect_right([p[0] for p in f], t) - 1, len(f) - 2)
    a, b = f[i:i + 2]
    return a[1] + (t - a[0]) * (b[1] - a[1]) / (b[0] - a[0])


def inverse(f):
    return [(y, x) for x, y in f]


def reduced(points):
    out = []
    for p in points:
        out.append(p)
        while len(out) >= 3:
            a, b, c = out[-3:]
            if (b[1] - a[1]) * (c[0] - b[0]) != (c[1] - b[1]) * (b[0] - a[0]):
                break
            out.pop(-2)
    return out


def compose(f, g):
    gi = inverse(g)
    xs = sorted({x for x, _ in g} | {value(gi, x) for x, _ in f})
    return reduced([(x, value(f, value(g, x))) for x in xs])


def power(f, n):
    if n < 0:
        return power(inverse(f), -n)
    out = IDENTITY
    for _ in range(n):
        out = compose(f, out)
    return out


def log_two(q):
    a, b = q.numerator, q.denominator
    assert a > 0 and (a & (a - 1)) == 0 and (b & (b - 1)) == 0
    return a.bit_length() - b.bit_length()


def slopes(f):
    return [(b[1] - a[1]) / (b[0] - a[0]) for a, b in zip(f, f[1:])]


def left_clone(f):
    return reduced([(x / 2, y / 2) for x, y in f] + [(Q(1), Q(1))])


def main():
    cases = []
    assert value(X0, Q(1, 2)) == Q(1, 4)
    assert value(X1, Q(1, 2)) == Q(1, 2)
    for m in range(1, 33):
        h = power(X1, m)
        assert compose(inverse(h), h) == IDENTITY
        w = compose(inverse(h), compose(X0, h))
        exponents = list(map(log_two, slopes(w)))
        # Each generator or inverse has slopes between 1/2 and 2.
        # Thus this slope certifies |w| >= 2m+1; the displayed word gives <=.
        assert max(exponents) == 2 * m + 1
        for x, y in w:
            assert x.denominator & (x.denominator - 1) == 0
            assert y.denominator & (y.denominator - 1) == 0
        a = left_clone(power(X0, m))
        assert value(a, Q(1, 2)) == Q(1, 2)
        adjacent = compose(a, X0)
        assert value(adjacent, Q(1, 2)) == Q(1, 2 ** (m + 2))
        cases.append({"m": m, "conjugate_max_log2_slope": max(exponents),
                      "conjugate_word_length": 2 * m + 1,
                      "adjacent_midpoint_depth": m + 2})
    result = {"status": "passed", "arithmetic": "exact Fraction",
              "finite_cases": len(cases), "cases": cases,
              "scope": "Restricted construction counterexamples; no arbitrary-QI conclusion"}
    Path(__file__).with_name("pl_conjugation_result.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "cases"}))


if __name__ == "__main__":
    main()
