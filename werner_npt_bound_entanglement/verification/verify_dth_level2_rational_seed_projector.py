#!/usr/bin/env python3
"""Exact group-algebra audit for rational degree-three DTH source charts.

The three bivector pairs occupy replica slots (0,1), (2,3), and (5,6);
slot 4 is the final z vector.  On the six bivector slots this verifier builds
the wreath projector onto pair-antisymmetric, pair-symmetric tensors and then
the central-character projector onto the S_(3,3) summand.

All arithmetic is in QQ and the script has no third-party dependencies.
"""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product


N = 7
IDENTITY = tuple(range(N))
PAIR_SLOTS = ((0, 1), (2, 3), (5, 6))
W_SLOTS = (0, 1, 2, 3, 5, 6)


def compose(left, right):
    return tuple(left[right[index]] for index in range(N))


def inverse(permutation):
    out = [0] * N
    for source, target in enumerate(permutation):
        out[target] = source
    return tuple(out)


def transposition(first, second):
    out = list(IDENTITY)
    out[first], out[second] = out[second], out[first]
    return tuple(out)


def pair_permutation(permutation):
    out = list(IDENTITY)
    for source, target in enumerate(permutation):
        for bit in (0, 1):
            out[PAIR_SLOTS[source][bit]] = PAIR_SLOTS[target][bit]
    return tuple(out)


def multiply(left, right):
    out = {}
    for first, a in left.items():
        for second, b in right.items():
            key = compose(first, second)
            out[key] = out.get(key, Fraction(0)) + a * b
    return {key: value for key, value in out.items() if value}


def wreath_projector():
    out = {}
    for flips in product((0, 1), repeat=3):
        flip = IDENTITY
        sign = 1
        for pair, selected in zip(PAIR_SLOTS, flips):
            if selected:
                flip = compose(transposition(*pair), flip)
                sign = -sign
        for permutation in permutations(range(3)):
            key = compose(pair_permutation(permutation), flip)
            out[key] = out.get(key, Fraction(0)) + Fraction(sign, 48)
    return out


def grassmann_projector():
    wreath = wreath_projector()
    central = {
        transposition(first, second): Fraction(1)
        for first, second in combinations(W_SLOTS, 2)
    }
    plus_five = dict(central)
    plus_five[IDENTITY] = Fraction(5)
    plus_fifteen = dict(central)
    plus_fifteen[IDENTITY] = Fraction(15)
    return {
        key: value / 144
        for key, value in multiply(
            multiply(wreath, plus_five), plus_fifteen
        ).items()
    }


def main():
    wreath = wreath_projector()
    assert len(wreath) == 48
    assert set(wreath.values()) == {Fraction(-1, 48), Fraction(1, 48)}
    assert multiply(wreath, wreath) == wreath
    assert all(wreath.get(inverse(key), 0) == value
               for key, value in wreath.items())

    projector = grassmann_projector()
    assert len(projector) == 720
    assert multiply(projector, projector) == projector
    assert all(projector.get(inverse(key), 0) == value
               for key, value in projector.items())
    assert sum(projector.values()) == 0
    assert projector[IDENTITY] == Fraction(1, 144)
    assert 720 * projector[IDENTITY] == 5

    multiplicities = Counter(projector.values())
    assert multiplicities == Counter({
        Fraction(1, 576): 192,
        Fraction(-1, 576): 192,
        Fraction(1, 288): 144,
        Fraction(-1, 288): 144,
        Fraction(1, 144): 24,
        Fraction(-1, 144): 24,
    })
    print("exact rational S_(3,3) projector audit passed")
    print("wreath/projector supports:", len(wreath), len(projector))
    print("regular-representation rank:", 720 * projector[IDENTITY])


if __name__ == "__main__":
    main()
