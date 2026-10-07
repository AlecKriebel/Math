#!/usr/bin/env python3
"""Exact integer illustrations; these computations do not prove EGH or Sperner."""
import itertools
import json
from collections import Counter
from pathlib import Path


def convolution(degrees):
    h = [1]
    for d in degrees:
        if d < 1:
            raise ValueError("degrees must be positive")
        nxt = [0] * (len(h) + d - 1)
        for j, coefficient in enumerate(h):
            for r in range(d):
                nxt[j + r] += coefficient
        h = nxt
    return h


def enumeration(degrees):
    counts = Counter(map(sum, itertools.product(*(range(d) for d in degrees))))
    return [counts[j] for j in range(sum(d - 1 for d in degrees) + 1)]


def main():
    cases = [(), (1, 1, 1), (1, 2, 4), (2, 2, 2), (2, 3, 4),
             (3, 3, 3), (2,) * 8]
    output = []
    for degrees in cases:
        h = convolution(degrees)
        assert h == enumeration(degrees)
        assert h == h[::-1]
        assert sum(h) == __import__("math").prod(degrees)
        output.append({"degrees": list(degrees), "hilbert_function": h,
                       "maximum": max(h),
                       "maximal_layers": [j for j, v in enumerate(h) if v == max(h)]})
    # Independent exact counting over a systematic small family.
    checked = 0
    for n in range(6):
        for degrees in itertools.combinations_with_replacement(range(1, 6), n):
            assert convolution(degrees) == enumeration(degrees)
            checked += 1
    result = {"purpose": "Illustrations only, not empirical proof of the theorem",
              "independent_small_cases_checked": checked, "examples": output}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
