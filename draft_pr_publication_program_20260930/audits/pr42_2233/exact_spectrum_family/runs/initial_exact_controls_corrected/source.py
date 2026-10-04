#!/usr/bin/env python3
"""Private audit controls; exact finite sets, never a solution of EP653."""
from collections import Counter
from fractions import Fraction as Q
import json
import os


def spectrum(points):
    points = tuple((Q(x), Q(y)) for x, y in points)
    if len(set(points)) != len(points):
        raise ValueError("duplicate coordinates: requested finite-set cardinality fails")
    local = tuple(frozenset((x-u)**2 + (y-v)**2 for j, (u, v) in enumerate(points)
                            if j != i) for i, (x, y) in enumerate(points))
    counts = tuple(map(len, local))
    values = frozenset(counts)
    return {"n": len(points), "counts": counts, "values": sorted(values),
            "M": len(values), "distance_sum": sum(counts),
            "multiplicity_histogram": dict(sorted(Counter(counts).items()))}


def verify(points, expected):
    result = spectrum(points)
    for key, value in expected.items():
        assert result[key] == value, (key, result[key], value)
    return result


def must_reject(name, fn, error):
    try:
        fn()
    except error:
        return {"mutation": name, "rejected": True}
    raise AssertionError("adversarial mutation was accepted: " + name)


def run():
    results = []
    examples = [
        ("singleton", [(0, 0)], {"counts": (0,), "M": 1}),
        ("pair", [(0, 0), (1, 0)], {"counts": (1, 1), "M": 1}),
        ("three-term progression", [(i, 0) for i in range(3)],
         {"counts": (2, 1, 2), "M": 2}),
        ("scalene triangle", [(0, 0), (3, 0), (0, 4)],
         {"counts": (2, 2, 2), "M": 1}),
        ("unit square", [(0, 0), (1, 0), (1, 1), (0, 1)],
         {"counts": (2, 2, 2, 2), "M": 1}),
        ("centered four-point circle", [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)],
         {"counts": (1, 3, 3, 3, 3), "M": 2}),
    ]
    for name, points, expected in examples:
        results.append({"control": name, **verify(points, expected)})
    for n in range(1, 33):
        expected_counts = tuple(max(i, n-1-i) for i in range(n))
        results.append({"control": "arithmetic progression", **verify(
            [(i, 0) for i in range(n)], {"counts": expected_counts,
                "M": (n+1)//2})})
        for q in (2, 3, 6):
            results.append({"control": f"powers q={q}", **verify(
                [(q**i, 0) for i in range(n)], {"counts": (n-1,)*n, "M": 1})})
    for n in range(2, 17):
        points = [(Q(1-t*t, 1+t*t), Q(2*t, 1+t*t)) for t in range(n)]
        results.append({"control": "rational unit circle", **spectrum(points)})
        results.append({"control": "parabola", **spectrum([(t, t*t) for t in range(n)])})
    results.extend([
        must_reject("wrong progression M", lambda: verify([(i,0) for i in range(5)], {"M": 5}), AssertionError),
        must_reject("wrong pair multiplicity", lambda: verify([(0,0),(1,0)], {"counts": (1,0)}), AssertionError),
        must_reject("duplicate cardinality", lambda: spectrum([(0,0),(0,0),(1,0)]), ValueError),
        must_reject("degree substituted for local distinct distances", lambda: verify(
            [(0,0),(1,0),(1,1),(0,1)], {"counts": (3,3,3,3)}), AssertionError),
    ])
    print(json.dumps({"pid": os.getpid(), "arithmetic": "Fraction squared distances; no float equality",
                      "finite_controls_only": True, "results": results}, indent=2))


if __name__ == "__main__":
    run()
