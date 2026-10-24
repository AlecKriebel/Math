#!/usr/bin/env python3
"""Exact consistency check of antichain-supported odometers in W_p.

No external packages. Finite permutations are constructed on words of length m.
The general continuum argument is in ../approach_constructions.md.
"""
import collections
import itertools
import json
from pathlib import Path


def digits(number, p, length):
    result = []
    for _ in range(length):
        result.append(number % p)
        number //= p
    return tuple(reversed(result))


def encode(word, p):
    number = 0
    for digit in word:
        number = p * number + digit
    return number


def permutation(p, m, support):
    result = []
    for number in range(p ** m):
        word = digits(number, p, m)
        image = word
        for n in support:
            prefix = (1,) * n + (0,)
            if len(prefix) < m and word[:len(prefix)] == prefix:
                # Root-first digits are least significant for the odometer.
                suffix = list(word[len(prefix):])
                carry = 1
                for j in range(len(suffix)):
                    suffix[j], carry = (suffix[j] + carry) % p, (suffix[j] + carry) // p
                image = prefix + tuple(suffix)
                break
        result.append(encode(image, p))
    assert sorted(result) == list(range(p ** m))
    return result


def histogram(perm):
    seen = set()
    result = collections.Counter()
    for start in range(len(perm)):
        if start in seen:
            continue
        current, length = start, 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = perm[current]
        assert current == start
        result[length] += 1
    return dict(sorted(result.items()))


def predicted(p, m, support):
    result = collections.Counter()
    fixed = p ** m
    for n in support:
        if n <= m - 2:
            length = p ** (m - n - 1)
            result[length] += 1
            fixed -= length
    if fixed:
        result[1] = fixed
    return dict(sorted(result.items()))


def main():
    records = []
    cases = 0
    for p, maximum_r in [(2, 6), (3, 4), (5, 3)]:
        for r in range(1, maximum_r + 1):
            m = r + 1
            signatures = set()
            for bits in itertools.product((0, 1), repeat=r):
                support = tuple(n for n, bit in enumerate(bits) if bit)
                actual = histogram(permutation(p, m, support))
                expected = predicted(p, m, support)
                assert actual == expected, (p, m, support, actual, expected)
                signatures.add(tuple(actual.items()))
                cases += 1
            assert len(signatures) == 2 ** r
            records.append({"p": p, "support_slots": r, "tree_level": m,
                            "distinct_histograms": len(signatures),
                            "all_histograms_match_formula": True})
    result = {"scope": "finite consistency checks only; not a complete proof of 21.136",
              "permutations_checked": cases, "records": records, "all_passed": True}
    output = Path(__file__).with_name("tree_support_checks.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(output.resolve()), "permutations_checked": cases,
                      "all_passed": True}))


if __name__ == "__main__":
    main()
