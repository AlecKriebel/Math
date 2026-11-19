#!/usr/bin/env python3
"""Finite local-exchange regression, not a proof of an infinite theorem."""
import json
from itertools import combinations
from pathlib import Path

# Assertions are explicit runtime checks, including under optimized Python.


def union(family):
    result = 0
    for edge in family:
        result |= edge
    return result


def check(n):
    full = (1 << n) - 1
    edges = list(range(1 << n))  # includes the empty edge
    counts = dict(vertices=n, families=0, covers=0, deletion_witnesses=0,
                  union_witnesses=0, finite_singleton_exceptions=0)
    for bits in range(1 << len(edges)):
        counts['families'] += 1
        c = {e for e in edges if bits & (1 << e)}
        if union(c) != full:
            continue
        counts['covers'] += 1
        deletable = next((e for e in sorted(c) if union(c - {e}) == full), None)
        if deletable is not None:
            d = c - {deletable}
            if not (len(c - d) == 1 and len(d - c) == 0):
                raise AssertionError("regression check 3 failed")
            counts['deletion_witnesses'] += 1
        elif len(c) >= 2:
            # Every pair must work, not just one favorably selected pair.
            for a, b in combinations(sorted(c), 2):
                u = a | b
                if not (u not in c and u != a and (u != b)):
                    raise AssertionError("regression check 5 failed")
                d = (c - {a, b}) | {u}
                if not (union(d) == full):
                    raise AssertionError("regression check 6 failed")
                if not (len(c - d) == 2 and len(d - c) == 1):
                    raise AssertionError("regression check 7 failed")
            counts['union_witnesses'] += 1
        else:
            if not (c == {full}):
                raise AssertionError("regression check 4 failed")
            # {full} is strongly minimal on a finite nonempty ground set:
            # any competing cover either contains full or adds another edge.
            counts['finite_singleton_exceptions'] += 1
    if not (counts['finite_singleton_exceptions'] == 1):
        raise AssertionError("regression check 1 failed")
    if not (counts['covers'] == sum((counts[k] for k in ('deletion_witnesses', 'union_witnesses', 'finite_singleton_exceptions')))):
        raise AssertionError("regression check 2 failed")
    return counts


if __name__ == '__main__':
    result = {'purpose': 'Exhaustive finite tests of the local exchanges; not infinite verification',
              'cases': [check(n) for n in range(1, 5)]}
    target = Path(__file__).with_name('REGRESSION_RESULTS.json')
    target.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
