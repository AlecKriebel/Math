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
    by_distance = {}
    for i, distances in enumerate(local):
        for d in distances:
            by_distance.setdefault(d, set()).add(i)
    assert sum(counts) == sum(map(len, by_distance.values()))
    assert sum(counts) >= 2 * len(by_distance)
    assert sum(counts) <= len(points) * (len(points)-1)
    if len(points) > 1:
        assert 1 <= min(counts) <= max(counts) <= len(points)-1
        assert len(values) <= len(points)-1
    return {"n": len(points), "counts": counts, "values": sorted(values),
            "M": len(values), "distance_sum": sum(counts),
            "global_squared_distance_count": len(by_distance),
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
        ("two separated progressions", [(i,0) for i in (0,1,2,10,11,12)],
         {"n": 6, "counts": (5,4,5,5,4,5), "values": [4,5], "M": 2}),
        ("overlapping progressions as set union", sorted(set([(i,0) for i in (0,1,2,2,3,4)])),
         {"n": 5, "counts": (4,3,2,3,4), "values": [2,3,4], "M": 3}),
        ("near-coincident rational triple", [(0,0),(1,0),(1+Q(1,10**30),0)],
         {"n": 3, "counts": (2,2,2), "M": 1}),
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
        must_reject("sum of component spectrum sizes", lambda: verify(
            [(i,0) for i in (0,1,2,10,11,12)], {"M": 4}), AssertionError),
        must_reject("union of old component count spectra", lambda: verify(
            [(i,0) for i in (0,1,2,10,11,12)], {"values": [1,2]}), AssertionError),
        must_reject("overlapping cardinalities added", lambda: verify(
            sorted(set([(i,0) for i in (0,1,2,2,3,4)])), {"n": 6}), AssertionError),
        must_reject("degenerate powers q=1", lambda: spectrum([(1**i,0) for i in range(4)]), ValueError),
    ])
    print(json.dumps({"pid": os.getpid(), "arithmetic": "Fraction squared distances; no float equality",
                      "finite_controls_only": True, "results": results}, indent=2))


if __name__ == "__main__":
    run()
