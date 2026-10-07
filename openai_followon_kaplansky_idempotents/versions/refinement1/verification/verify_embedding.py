#!/usr/bin/env python3
"""Check the written finite-HNN embedding word identities.

Run with Python 3.10 or later; only the standard library is used. Output is
one deterministic compact JSON object. A positive integer labels a generator
and its negative labels the inverse: x=1, t=2, y=3.

The construction writes
    g_i = x^-1 y^i t^-1 x^-i y x^i t y^-i,
then substitutes y=t x t^-1. Its claimed reduced word is
    W_i = x^-1 t x^i t^-2 x^-i t x t^-1 x^i t^2 x^-i t^-1.

These finite checks establish the specified formal free-word identities and
lengths at the stated indices. They do not verify the source group, its
proper one-sided inverse, the HNN base-group embedding, free-basis
injectivity, Britton's lemma, torsion-freeness, or asphericity. Those claims
require the mathematical proofs in EXTENSION_EMBEDDING_AUDIT.md and the
upstream source audits. No source group relation or group-ring coefficient
data is assumed or simulated here.
"""

from __future__ import annotations

import json
from collections.abc import Iterable


Word = tuple[int, ...]
X: Word = (1,)
T: Word = (2,)
Y: Word = (3,)
INDICES = (1, 2, 3, 7, 532, 8260)


def free_reduce(letters: Iterable[int]) -> Word:
    """Cancel adjacent mutually inverse letters with a stack."""
    stack: list[int] = []
    for letter in letters:
        if not isinstance(letter, int) or isinstance(letter, bool) or letter == 0:
            raise ValueError("signed generators must be nonzero integers")
        if stack and stack[-1] == -letter:
            stack.pop()
        else:
            stack.append(letter)
    return tuple(stack)


def inverse(word: Word) -> Word:
    return tuple(-letter for letter in reversed(word))


def power(word: Word, exponent: int) -> Word:
    if exponent >= 0:
        return word * exponent
    return inverse(word) * (-exponent)


def substitute(word: Word, images: dict[int, Word]) -> Word:
    """Extend generator images to words, including inverse letters."""
    expanded: list[int] = []
    for letter in word:
        image = images[abs(letter)]
        expanded.extend(image if letter > 0 else inverse(image))
    return free_reduce(expanded)


def source_generator_expression(index: int) -> Word:
    """The word obtained by solving the i-th HNN relation for g_i."""
    if index < 1:
        raise ValueError("the generator index must be positive")
    return (
        inverse(X)
        + power(Y, index)
        + inverse(T)
        + power(X, -index)
        + Y
        + power(X, index)
        + T
        + power(Y, -index)
    )


def displayed_final_word(index: int) -> Word:
    """Independently encode the displayed W_i, without using substitution."""
    if index < 1:
        raise ValueError("the generator index must be positive")
    return (
        inverse(X)
        + T
        + power(X, index)
        + power(T, -2)
        + power(X, -index)
        + T
        + X
        + inverse(T)
        + power(X, index)
        + power(T, 2)
        + power(X, -index)
        + inverse(T)
    )


def require(condition: bool, message: str) -> None:
    """Use an explicit failure, so checks remain active with python -O."""
    if not condition:
        raise AssertionError(message)


def check() -> dict[str, object]:
    # Boundary checks on the free-word evaluator are separate from the
    # embedding formulas. No presentation-specific word problem is used.
    require(free_reduce((1, 2, -2, -1)) == (), "nested cancellation")
    require(free_reduce((1, 2, -1, -2)) == (1, 2, -1, -2), "noncommutativity")
    require(inverse((1, -2, 3)) == (-3, 2, -1), "word inverse")

    y_image = T + X + inverse(T)
    images = {1: X, 2: T, 3: y_image}
    # The zero-index defining relation t^-1 y t=x.
    zero_left = substitute(inverse(T) + Y + T, images)
    require(zero_left == X, "zero-index HNN relation")
    # Negative letters must map to inverses of their positive images.
    require(substitute(inverse(Y), images) == inverse(y_image), "inverse substitution")

    lengths: list[dict[str, int | bool]] = []
    small_words: list[dict[str, object]] = []
    for index in INDICES:
        gi = source_generator_expression(index)

        # Check the solved formula directly in the free group on x,y,t:
        # t^-1 x^-i y x^i t = y^-i x g_i y^i.
        left = free_reduce(inverse(T) + power(X, -index) + Y + power(X, index) + T)
        right = free_reduce(power(Y, -index) + X + gi + power(Y, index))
        require(left == right, f"solved HNN relation at index {index}")

        computed = substitute(gi, images)
        displayed = displayed_final_word(index)
        require(computed == displayed, f"W_i substitution at index {index}")
        require(free_reduce(displayed) == displayed, f"W_i reducedness at index {index}")
        require(len(displayed) == 4 * index + 10, f"W_i length at index {index}")
        lengths.append({"index": index, "length": len(displayed), "expected": 4 * index + 10,
                        "hnn_relation": True, "substitution": True, "freely_reduced": True})
        if index <= 3:
            small_words.append({"index": index, "signed_word": list(displayed)})

    return {
        "status": "passed",
        "alphabet": {"1": "x", "2": "t", "3": "y", "negative": "inverse"},
        "zero_index_relation": True,
        "small_words": small_words,
        "length_cases": lengths,
        "scope": "Formal free-word identities at the six listed positive indices; no source-group or topology verification.",
    }


if __name__ == "__main__":
    print(json.dumps(check(), separators=(",", ":"), sort_keys=True))
