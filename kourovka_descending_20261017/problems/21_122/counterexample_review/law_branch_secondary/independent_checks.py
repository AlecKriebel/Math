#!/usr/bin/env python3
"""Independent, bounded controls for the law and disjoint-support arguments.

These controls do not prove the infinite-group assertions. The unbounded
normal-form and rigid-support proofs are in AUDIT.md. No author checker is
imported or read.
"""
from collections import deque
from datetime import datetime, timezone
from itertools import permutations, product
from pathlib import Path
import hashlib
import json


def reduce_word(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def inverse_word(word):
    return tuple(-x for x in reversed(word))


def reduced_words(rank, maximum_length):
    layer = [()]
    alphabet = tuple(range(1, rank + 1)) + tuple(range(-rank, 0))
    for _ in range(maximum_length):
        layer = [w + (x,) for w in layer for x in alphabet
                 if not w or w[-1] != -x]
        yield from layer


def substitute(word, images):
    return reduce_word(x for letter in word
                       for x in (images[letter - 1] if letter > 0
                                 else inverse_word(images[-letter - 1])))


def compose(p, q):
    """Permutation p after q."""
    return tuple(p[q[i]] for i in range(len(p)))


def invert(p):
    result = [0] * len(p)
    for i, j in enumerate(p):
        result[j] = i
    return tuple(result)


def generated(generators, degree):
    one = tuple(range(degree))
    gens = list(generators) + [invert(g) for g in generators]
    result, queue = {one}, deque([one])
    while queue:
        g = queue.popleft()
        for h in gens:
            gh = compose(g, h)
            if gh not in result:
                result.add(gh)
                queue.append(gh)
    return sorted(result)


def evaluate(word, values):
    result = tuple(range(len(values[0])))
    for letter in word:
        value = values[abs(letter) - 1]
        result = compose(result, value if letter > 0 else invert(value))
    return result


def power(g, n):
    result = tuple(range(len(g)))
    for _ in range(n):
        result = compose(result, g)
    return result


def order(g):
    one = tuple(range(len(g)))
    result, n = g, 1
    while result != one:
        result = compose(result, g)
        n += 1
    return n


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def image(word, rank, group):
    return {evaluate(word, values) for values in product(group, repeat=rank)}


def full_binary_automorphisms(depth):
    if depth == 0:
        return [(0,)]
    below = full_binary_automorphisms(depth - 1)
    half = 2 ** (depth - 1)
    return [tuple(j + flip * half for j in left)
            + tuple(j + (1 - flip) * half for j in right)
            for left in below for right in below for flip in (0, 1)]


def main():
    formal_cases = formal_power_checks = 0
    lengths = {}
    for rank, maximum_length in ((1, 12), (2, 7), (3, 5)):
        count = 0
        for word in reduced_words(rank, maximum_length):
            blocks = [tuple((abs(x) + i * rank) * (1 if x > 0 else -1)
                            for x in word) for i in range(rank)]
            nested = substitute(word, blocks)
            assert nested
            for e in (1, 2, 3):
                assert reduce_word(nested * e)
                formal_power_checks += 1
            # Every unused generator still receives a nontrivial block image.
            assert all(blocks)
            count += 1
        lengths[str(rank)] = {"maximum_length": maximum_length, "words": count}
        formal_cases += count

    # Identity-word boundary and conjugate-word cancellation controls.
    assert substitute((), [(1,)]) == ()
    conjugated = (1, 2, -1)
    assert len(reduce_word(conjugated * 4)) == 6
    assert substitute((1,), [(1,)]) == (1,)
    assert substitute((-1,), [(-1,)]) == (1,)

    finite_cases = finite_outer_values = 0
    s3 = list(permutations(range(3)))
    d8 = generated([(1, 2, 3, 0), (0, 3, 2, 1)], 4)
    assert len(s3) == 6 and len(d8) == 8
    for group in (s3, d8):
        degree = len(group[0])
        one = tuple(range(degree))
        for rank in (1, 2):
            for word in reduced_words(rank, 4):
                values = image(word, rank, group)
                k_group = generated(values, degree)
                f_group = generated(image(word, rank, k_group), degree)
                exponent = 1
                for g in f_group:
                    exponent = lcm(exponent, order(g))
                for outer in product(values, repeat=rank):
                    assert power(evaluate(word, outer), exponent) == one
                    finite_outer_values += 1
                finite_cases += 1

    # Independently test the exact support lemma, not the author's wreath counts.
    tree = full_binary_automorphisms(3)
    assert len(tree) == len(set(tree)) == 128
    one = tuple(range(8))
    support_checks = conjugation_checks = 0
    for level in (1, 2):
        width = 2 ** (3 - level)
        for vertex in range(2 ** level):
            leaves = set(range(vertex * width, (vertex + 1) * width))
            rigid = [r for r in tree if all(r[x] == x for x in range(8)
                                           if x not in leaves)]
            for g in tree:
                moved_leaves = {g[x] for x in leaves}
                if moved_leaves == leaves:
                    continue
                assert not moved_leaves.intersection(leaves)
                centralizer = [r for r in rigid if compose(r, g) == compose(g, r)]
                assert centralizer == [one]
                conjugates = {compose(compose(invert(r), g), r) for r in rigid}
                assert len(conjugates) == len(rigid)
                support_checks += 1
                conjugation_checks += len(rigid)

    base = Path(__file__).resolve().parent
    target = base.parent.parent / "counterexample/LAW_AND_BRANCH_REDUCTIONS.md"
    result = {"utc": datetime.now(timezone.utc).isoformat(), "status": "PASS",
              "target_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
              "formal_substitution_words": formal_cases,
              "formal_positive_power_checks": formal_power_checks,
              "formal_ranges": lengths,
              "finite_law_cases": finite_cases,
              "finite_outer_value_checks": finite_outer_values,
              "disjoint_support_cases": support_checks,
              "injective_conjugation_checks": conjugation_checks,
              "limitations": "Bounded controls only; general proofs are mathematical, not inferred from these checks."}
    (base / "independent_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
