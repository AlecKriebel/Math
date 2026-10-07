"""Exact entropy-coefficient checks; no floating point or external packages.

These checks certify chain-rule algebra only. They do not certify entropy
inequalities, continuity, the coding model, or infinite-dimensional limits.
"""
from collections import Counter
import json


def h(*labels):
    return Counter({frozenset(labels): 1}) if labels else Counter()


def add(*terms):
    out = Counter()
    for coefficient, term in terms:
        for key, value in term.items():
            out[key] += coefficient * value
    return Counter({key: value for key, value in out.items() if value})


def mi(a, b, c=()):
    return add((1, h(*a, *c)), (1, h(*b, *c)),
               (-1, h(*c)), (-1, h(*a, *b, *c)))


def ch(a, c=()):
    return add((1, h(*a, *c)), (-1, h(*c)))


def check(name, *terms):
    residual = add(*terms)
    assert not residual, (name, residual)
    return {"name": name, "residual_coefficients": 0, "exact": True}


checks = []
# F minus the private-information expression equals the stated remainder.
checks.append(check("second chain identity",
    (1, mi(("W",), ("B", "V"), ("X",))),
    (-1, mi(("W",), ("E",), ("X",))),
    (-1, mi(("W", "V"), ("B",), ("X",))),
    (1, mi(("W", "V"), ("E",), ("X",))),
    (-1, mi(("W",), ("V",), ("X",))),
    (1, mi(("V",), ("B",), ("X",))),
    (-1, mi(("V",), ("E",), ("W", "X")))))
checks.append(check("second classical entropy remainder",
    (1, mi(("W",), ("V",), ("X",))),
    (-1, mi(("V",), ("B",), ("X",))),
    (1, ch(("V",), ("W", "X"))),
    (-1, ch(("V",), ("B", "X")))))
checks.append(check("third chain identity",
    (1, mi(("K", "W"), ("B", "L", "V"))),
    (-1, mi(("W",), ("E",), ("K", "L"))),
    (-1, mi(("K", "L", "W", "V"), ("B",))),
    (1, mi(("W", "V"), ("E",), ("K", "L"))),
    (-1, mi(("K", "W"), ("L", "V"))),
    (1, mi(("L", "V"), ("B",))),
    (-1, mi(("V",), ("E",), ("W", "K", "L")))))
checks.append(check("third classical entropy remainder",
    (1, mi(("K", "W"), ("L", "V"))),
    (1, ch(("V",), ("W", "K", "L"))),
    (-1, mi(("K", "W"), ("L",))),
    (-1, ch(("V",), ("L",)))))
checks.append(check("third reliability/secrecy expression",
    (1, mi(("K", "W"), ("B", "L", "V"))),
    (-1, mi(("W",), ("E",), ("K", "L"))),
    (-1, h("K")),
    (-1, mi(("W",), ("L",), ("K",))),
    (-1, ch(("W",), ("E", "K", "L"))),
    (1, ch(("K", "W"), ("B", "L", "V")))))
print(json.dumps({"checks": checks, "count": len(checks)}, indent=2))
