#!/usr/bin/env python3
"""Independent recursive-word audit of the antichain odometer construction.

The author's implementation locates a selected prefix by looping over support
and performs digit arithmetic. This implementation locates the first digit
different from 1 and uses wreath recursion for the subtree odometer. It also
checks restriction to the preceding tree level, including inactive slots.
"""
import hashlib
import importlib.util
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "construction_artifacts" / "verify_tree_support.py"


def odometer(word, p):
    if not word:
        return ()
    first, tail = word[0], word[1:]
    return ((first + 1) % p,) + (odometer(tail, p) if first == p - 1 else tail)


def image(word, p, support):
    n = 0
    while n < len(word) and word[n] == 1:
        n += 1
    if n == len(word) or word[n] != 0 or n not in support:
        return word
    return word[: n + 1] + odometer(word[n + 1 :], p)


def cycle_counts(mapping):
    remaining = set(mapping)
    counts = Counter()
    while remaining:
        start = next(iter(remaining))
        point = start
        length = 0
        while point in remaining:
            remaining.remove(point)
            point = mapping[point]
            length += 1
        assert point == start
        counts[length] += 1
    return counts


def main():
    spec = importlib.util.spec_from_file_location("author_tree_support", AUTHOR)
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    cases = 0
    point_checks = 0
    records = []
    for p, maximum_m in [(2, 7), (3, 5), (5, 4)]:
        for m in range(maximum_m + 1):
            words = tuple(itertools.product(range(p), repeat=m))
            signatures = set()
            # Include two slots inactive at this level, testing the cutoff.
            for bits in itertools.product((0, 1), repeat=m + 2):
                support = frozenset(n for n, bit in enumerate(bits) if bit)
                mapping = {word: image(word, p, support) for word in words}
                assert len(set(mapping.values())) == p**m
                actual = cycle_counts(mapping)
                expected = Counter()
                moved = 0
                for n in support:
                    if n + 1 < m:
                        length = p ** (m - n - 1)
                        expected[length] += 1
                        moved += length
                if p**m - moved:
                    expected[1] = p**m - moved
                assert actual == expected, (p, m, support, actual, expected)
                author_permutation = author.permutation(p, m, support)
                for index, word in enumerate(words):
                    assert author.digits(author_permutation[index], p, m) == mapping[word]
                    if m:
                        assert mapping[word][:-1] == image(word[:-1], p, support)
                    point_checks += 1
                signatures.add(tuple(sorted(actual.items())))
                cases += 1
            assert len(signatures) == 2 ** max(0, m - 1)
            records.append({"p": p, "level": m,
                            "supports_checked": 2 ** (m + 2),
                            "distinct_cycle_histograms": len(signatures)})
    result = {
        "scope": "independent finite consistency checks, not a solution of 21.136",
        "author_script_sha256": hashlib.sha256(AUTHOR.read_bytes()).hexdigest(),
        "supports_checked": cases,
        "word_images_checked": point_checks,
        "checks": ["independent wreath-recursive permutation",
                   "complete cycle histogram formula", "bijection",
                   "agreement with author permutation", "tree-level restriction",
                   "boundary levels 0 and 1", "inactive deep support slots"],
        "records": records,
        "all_passed": True,
    }
    destination = HERE / "tree_support_independent_checks.json"
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(destination), "supports_checked": cases,
                      "word_images_checked": point_checks, "all_passed": True}))


if __name__ == "__main__":
    main()
