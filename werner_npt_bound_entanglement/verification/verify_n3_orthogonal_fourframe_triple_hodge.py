#!/usr/bin/env python3
"""Exact checker for the orthogonal four-frame triple-Hodge example.

The normalized Hodge coefficients have common factor 1/(3 sqrt(8)).
The script keeps only their integer numerators, so all checks reduce
to integer arithmetic.
"""

from itertools import product

Word = tuple[int, int, int]
Tensor = dict[Word, int]


def epsilon(a: int, b: int, c: int) -> int:
    if len({a, b, c}) < 3:
        return 0
    if (a, b, c) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)):
        return 1
    return -1


def hodge_numerator(left: Tensor, right: Tensor) -> Tensor:
    out: Tensor = {}
    for p, q, r in product(range(3), repeat=3):
        value = 0
        for (a, b, c), left_value in left.items():
            for (d, e, f), right_value in right.items():
                value += (
                    left_value
                    * right_value
                    * epsilon(p, a, d)
                    * epsilon(q, b, e)
                    * epsilon(r, c, f)
                )
        if value:
            out[(p, q, r)] = value
    return out


# Unnormalized Phi_0|0>, Phi_0|2>, Phi_1|0>, Phi_1|2>.
u0: Tensor = {(0, 0, 0): 1, (1, 1, 0): 1, (2, 2, 0): 1}
w1: Tensor = {(0, 0, 2): 1, (1, 1, 2): 1, (2, 2, 2): 1}
u1: Tensor = {(0, 1, 0): 1, (1, 2, 0): 1, (2, 0, 0): 1}
w0: Tensor = {(0, 1, 2): 1, (1, 2, 2): 1, (2, 0, 2): 1}

z01 = hodge_numerator(u0, w1)
z10 = hodge_numerator(u1, w0)

assert z01 == {(0, 0, 1): -2, (1, 1, 1): -2, (2, 2, 1): -2}
assert z10 == {(0, 1, 1): -2, (1, 2, 1): -2, (2, 0, 1): -2}

norm01_numerator = sum(value * value for value in z01.values())
norm10_numerator = sum(value * value for value in z10.values())
cross_numerator = sum(z01.get(word, 0) * value for word, value in z10.items())

assert norm01_numerator == norm10_numerator == 12
assert cross_numerator == 0

# Each normalized squared norm is numerator/(3^2 * 8).
assert norm01_numerator * 6 == 9 * 8
assert norm10_numerator * 6 == 9 * 8

print("verified exact orthogonal four-frame triple-Hodge counterexample")
print("||z01||^2 = ||z10||^2 = 1/6")
print("opposite-energy sum = 1/3 > 1/4")
print("<z01,z10> = 0")
