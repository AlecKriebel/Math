"""Exact finite checks supporting the proofs in approach_metric_invariants.md.

Trees are complete binary prefix codes. No floating-point arithmetic is used.
This is evidence for the finite combinatorics, not a proof of the cone theorem.
"""

from functools import lru_cache
from itertools import product
import json


@lru_cache(None)
def trees(carets):
    if carets == 0:
        return (("",),)
    return tuple(
        tuple("0" + x for x in left) + tuple("1" + x for x in right)
        for k in range(carets)
        for left in trees(k)
        for right in trees(carets - 1 - k)
    )


def internal(tree):
    return {leaf[:k] for leaf in tree for k in range(len(leaf))}


def from_internal(nodes):
    if "" not in nodes:
        return ("",)
    return tuple(sorted(
        node + bit for node in nodes for bit in "01"
        if node + bit not in nodes
    ))


def reduce_pair(source, target):
    source, target = list(source), list(target)
    while True:
        for j in range(len(source) - 1):
            a, b = source[j:j + 2]
            c, d = target[j:j + 2]
            if (a.endswith("0") and b == a[:-1] + "1"
                    and c.endswith("0") and d == c[:-1] + "1"):
                source[j:j + 2] = [a[:-1]]
                target[j:j + 2] = [c[:-1]]
                break
        else:
            return tuple(source), tuple(target)


def expand(other, old, refined):
    return tuple(
        other[j] + leaf[len(prefix):]
        for j, prefix in enumerate(old)
        for leaf in refined if leaf.startswith(prefix)
    )


def multiply(g, h):
    common = from_internal(internal(g[1]) | internal(h[0]))
    return reduce_pair(expand(g[0], g[1], common),
                       expand(h[1], h[0], common))


def inverse(g):
    return g[1], g[0]


def norm(g):
    return len(g[0]) - 1


IDENTITY = (("",), ("",))
X0 = (("00", "01", "1"), ("0", "10", "11"))


def power(g, k):
    if k < 0:
        return power(inverse(g), -k)
    answer = IDENTITY
    for _ in range(k):
        answer = multiply(answer, g)
    return answer


def blocksum(scaffold, factors):
    return reduce_pair(
        tuple(prefix + leaf for prefix, g in zip(scaffold, factors)
              for leaf in g[0]),
        tuple(prefix + leaf for prefix, g in zip(scaffold, factors)
              for leaf in g[1]),
    )


def main():
    elements = set()
    for k in range(5):
        for a in trees(k):
            for b in trees(k):
                elements.add(reduce_pair(a, b))
    triangle_checks = 0
    for g in elements:
        assert multiply(g, inverse(g)) == IDENTITY
        for h in elements:
            assert norm(multiply(g, h)) <= norm(g) + norm(h)
            triangle_checks += 1

    for k in range(-20, 21):
        assert norm(power(X0, k)) == (abs(k) + 1 if k else 0)

    block_checks = 0
    for n in range(1, 5):
        for scaffold in trees(n - 1):
            for exponents in product(range(-2, 3), repeat=n):
                factors = tuple(power(X0, k) for k in exponents)
                actual = norm(blocksum(scaffold, factors))
                summands = sum(map(norm, factors))
                assert summands <= actual <= summands + n - 1
                assert sum(map(abs, exponents)) <= actual
                assert actual <= sum(map(abs, exponents)) + 2 * n - 1
                block_checks += 1

    # General reduced factors, including source/target shapes beyond powers.
    small = tuple(sorted(g for g in elements if norm(g) <= 3))
    general_block_checks = 0
    scaffold = trees(1)[0]
    for g, h in product(small, repeat=2):
        actual = norm(blocksum(scaffold, (g, h)))
        assert norm(g) + norm(h) <= actual <= norm(g) + norm(h) + 1
        general_block_checks += 1

    print(json.dumps({
        "unique_reduced_elements_through_four_carets": len(elements),
        "triangle_checks": triangle_checks,
        "power_checks": 41,
        "power_block_checks_all_scaffolds_through_four_leaves": block_checks,
        "general_two_block_checks": general_block_checks,
        "result": "all exact assertions passed",
    }, indent=2))


if __name__ == "__main__":
    main()
