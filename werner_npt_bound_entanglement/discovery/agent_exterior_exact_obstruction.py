"""Exact integer check of the sparse W_3 cross-term obstruction.

This is a verification-layer-sized calculation: no floating point and no
third-party packages.
"""

from itertools import product


def digits(index: int) -> tuple[int, int, int]:
    return ((index >> 2) & 1, (index >> 1) & 1, index & 1)


def index(bits: tuple[int, int, int]) -> int:
    return (bits[0] << 2) | (bits[1] << 1) | bits[2]


def swap_expectation(x: list[int], y: list[int], mask: int) -> int:
    value = 0
    for a, b in product(range(8), repeat=2):
        aa = list(digits(a))
        bb = list(digits(b))
        for site in range(3):
            if mask & (1 << site):
                aa[site], bb[site] = bb[site], aa[site]
        value += x[a] * y[b] * x[index(tuple(aa))] * y[index(tuple(bb))]
    return value


def w_expectation(x: list[int], y: list[int]) -> int:
    product_term = sum(
        2 ** mask.bit_count()
        * (-1) ** (3 - mask.bit_count())
        * swap_expectation(x, y, mask)
        for mask in range(8)
    )
    norm_x = sum(value * value for value in x)
    norm_y = sum(value * value for value in y)
    inner = sum(a * b for a, b in zip(x, y))
    return product_term + norm_x * norm_y - 2 * inner * inner


u = [-1, 0, 1, 0, 0, 1, 0, 1]
v = [1, 0, -1, 0, 0, 1, 0, 1]

assert sum(a * b for a, b in zip(u, v)) == 0
assert sum(a * a for a in u) == 4
assert sum(a * a for a in v) == 4
assert [swap_expectation(u, v, mask) for mask in range(8)] == [
    16,
    8,
    8,
    8,
    8,
    8,
    8,
    0,
]
assert w_expectation(u, v) == -48
assert w_expectation(u, u) == 48
assert w_expectation(v, v) == 48

print("exact sparse W_3 obstruction verified")
