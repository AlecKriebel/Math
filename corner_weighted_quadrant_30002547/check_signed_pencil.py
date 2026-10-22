#!/usr/bin/env python3
"""Exact finite-length normalization check for ATTEMPT_2, not a radius proof."""
from collections import defaultdict
from fractions import Fraction


def direct(a, maximum_length):
    layer = {(0, 0, ""): Fraction(1)}
    answer = [Fraction(1)]
    steps = [("N", 0, 1), ("S", 0, -1), ("E", 1, 0), ("W", -1, 0)]
    for length in range(1, maximum_length + 1):
        following = defaultdict(Fraction)
        for (x, y, previous), weight in layer.items():
            for letter, dx, dy in steps:
                if x + dx >= 0 and y + dy >= 0:
                    factor = a if previous + letter in ("NW", "ES") else 1
                    following[x + dx, y + dy, letter] += weight * factor
        layer = following
        if length % 2 == 0:
            answer.append(sum(value for (x, y, _), value in layer.items()
                              if x == y == 0))
    return answer


def contracted(a, maximum_length):
    previous, before_previous = {(0, 0): Fraction(1)}, {}
    answer = [Fraction(1)]
    for length in range(1, maximum_length + 1):
        following = defaultdict(Fraction)
        for (x, y), weight in previous.items():
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if x + dx >= 0 and y + dy >= 0:
                    following[x + dx, y + dy] += weight
        for (x, y), weight in before_previous.items():
            for dx, dy in ((-1, 1), (1, -1)):
                if x + dx >= 0 and y + dy >= 0:
                    following[x + dx, y + dy] += (a - 1) * weight
        previous, before_previous = following, previous
        if length % 2 == 0:
            answer.append(following[0, 0])
    return answer


if __name__ == "__main__":
    for parameter in map(Fraction, ("-1", "-3/4", "-1/2", "-1/4", "0")):
        expected = direct(parameter, 14)
        actual = contracted(parameter, 14)
        assert expected == actual, (parameter, expected, actual)
        print(f"a={parameter}: exact agreement through length 14; "
              + ", ".join(map(str, actual)))
