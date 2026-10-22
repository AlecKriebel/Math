"""Finite checks for tree_language_audit.md; proofs, not these bounds, are decisive.

Run: python3 tree_language_verify.py
No third-party packages, network calls, or group-automaticity assumptions.
"""

from functools import lru_cache
from itertools import product
import json
import re


@lru_cache(None)
def trees(n):
    if n == 0:
        return (None,)
    return tuple(
        (left, right)
        for k in range(n)
        for left in trees(k)
        for right in trees(n - 1 - k)
    )


def preorder(tree):
    return "0" if tree is None else "1" + preorder(tree[0]) + preorder(tree[1])


def exposed(tree, start=0):
    """Return exposed-caret first-leaf indices and total number of leaves."""
    if tree is None:
        return frozenset(), 1
    left, left_count = exposed(tree[0], start)
    right, right_count = exposed(tree[1], start + left_count)
    own = {start} if tree == (None, None) else set()
    return left | right | own, left_count + right_count


def reduced(left, right):
    return not (exposed(left)[0] & exposed(right)[0])


def left_comb(n):
    return None if n == 0 else (left_comb(n - 1), None)


def right_comb(n):
    return None if n == 0 else (None, right_comb(n - 1))


COLUMNS = {("1", "1"): "A", ("1", "0"): "B", ("0", "1"): "C", ("0", "0"): "D"}


def convolution(left, right):
    assert len(left) == len(right)
    return "".join(COLUMNS[pair] for pair in zip(left, right))


def bubbled_index(negative_exponents):
    """Bubble the appended index 1 using i^-1 j^-1 -> (j+1)^-1 i^-1."""
    current = 1
    for index, exponent in enumerate(negative_exponents):
        if index >= current:
            return current
        for _ in range(exponent):
            assert index < current
            current += 1
    return current


def frontier_return(negative_exponents):
    height = 1
    for index in range(sum(negative_exponents) + 1):
        exponent = negative_exponents[index] if index < len(negative_exponents) else 0
        height += exponent - 1
        if height == 0:
            return index + 1
        assert height > 0
    raise AssertionError("finite negative data must give a return")


def main():
    examined = 0
    matched_serial = []
    matched_convolution = []
    for n in range(8):
        for left, right in product(trees(n), repeat=2):
            examined += 1
            if not reduced(left, right):
                continue
            u, v = preorder(left), preorder(right)
            serial = u + "#" + v
            if re.fullmatch(r"1{2,}0{3,}#(?:10){2,}0", serial):
                assert n >= 2 and left == left_comb(n) and right == right_comb(n)
                matched_serial.append(n)
            conv = convolution(u, v)
            if re.fullmatch(r"(?:AB)+(?:CD)+D", conv):
                assert n >= 2 and n % 2 == 0
                assert left == left_comb(n) and right == right_comb(n)
                assert conv == "AB" * (n // 2) + "CD" * (n // 2) + "D"
                matched_convolution.append(n)
    assert matched_serial == list(range(2, 8))
    assert matched_convolution == [2, 4, 6]
    for n in range(2, 101):
        left, right = left_comb(n), right_comb(n)
        assert preorder(left) == "1" * n + "0" * (n + 1)
        assert preorder(right) == "10" * n + "0"
        assert reduced(left, right)
    exponent_vectors = 0
    for length in range(7):
        for exponents in product(range(4), repeat=length):
            assert bubbled_index(exponents) == frontier_return(exponents)
            exponent_vectors += 1
    result = {
        "all_equal_caret_tree_pairs_checked_through_n": 7,
        "pair_count": examined,
        "serial_filter_matches_caret_counts": matched_serial,
        "convolution_filter_matches_caret_counts": matched_convolution,
        "opposite_combs_checked_through_n": 100,
        "negative_exponent_vectors_checked": exponent_vectors,
        "negative_exponent_vector_max_length": 6,
        "negative_exponent_entry_maximum": 3,
        "status": "all assertions passed; finite corroboration only",
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
