#!/usr/bin/env python3
"""Finite support for the separately written geometric predecessor bridge.

No network, third-party libraries, source cache, or assert statements are used.
This is not a formal proof of the geometric theorems cited in the report.
"""
from fractions import Fraction
from itertools import combinations, permutations, product
import json


def require(value, message):
    if not value:
        raise RuntimeError(message)


def value(coeff, x, p=None):
    result = sum(a * x ** i for i, a in enumerate(coeff))
    return result if p is None else result % p


def multiply(a, b, p):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = (out[i + j] + x * y) % p
    return out


def remainder(a, b, p):
    out = [x % p for x in a]
    while len(out) >= len(b):
        factor = out[-1] * pow(b[-1], -1, p) % p
        offset = len(out) - len(b)
        for i, x in enumerate(b):
            out[i + offset] = (out[i + offset] - factor * x) % p
        while out and out[-1] == 0:
            out.pop()
    return out


def rank(rows):
    a = [[Fraction(x) for x in row] for row in rows]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        divisor = a[row][col]
        a[row] = [x / divisor for x in a[row]]
        for i in range(len(a)):
            if i != row and a[i][col]:
                multiplier = a[i][col]
                a[i] = [x - multiplier * y for x, y in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def generated(generators):
    identity = tuple(range(len(generators[0])))
    seen = {identity}
    todo = [identity]
    while todo:
        x = todo.pop()
        for g in generators:
            y = compose(g, x)
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def permute(vector, p):
    out = [0] * len(vector)
    for i, j in enumerate(p):
        out[j] = vector[i]
    return tuple(out)


def main():
    fpoly = [2, 5, -10, 0, 1]
    values = [value(fpoly, x) for x in [-4, -1, 0, 1, 4]]
    require(values == [78, -12, 2, -2, 118], "real-root sign data")
    require(all(value(fpoly, x, 5) != 0 for x in range(5)), "linear factor mod5")
    factors = [q for q in product(range(5), repeat=2)
               if not remainder(fpoly, [q[0], q[1], 1], 5)]
    require(factors == [], "quadratic factor mod5")
    require(pow(3, 2, 5) == 4, "imaginary quadratic inertness")
    cubic = [7, 6, 9, 1]
    cubic_values = [value(cubic, x, 13) for x in range(13)]
    require(0 not in cubic_values, "cubic mod13 is reducible")
    require(multiply([-9, 1], cubic, 13) == [x % 13 for x in fpoly], "factorization mod13")
    require(value(cubic, 9, 13) != 0, "squarefree mod13")
    s4 = list(permutations(range(4)))
    four_cycle = (1, 2, 3, 0)
    three_cycles = [p for p in s4 if p != (0, 1, 2, 3)
                    and compose(compose(p, p), p) == (0, 1, 2, 3)]
    require(len(three_cycles) == 8, "3-cycle inventory")
    require(all(len(generated([four_cycle, p])) == 24 for p in three_cycles),
            "4-cycle and 3-cycle group generation")

    # The local embedding fiber under (c,(1234)) has signs +,-,+,-.
    local = (1, -1, 1, -1)
    types = [f for f in product([-1, 1], repeat=4)
             if sum(f[i] == local[i] for i in range(4)) == 1]
    require(len(types) == 4, "CM types with one local selection")
    require(all(abs(sum(f)) == 2 for f in types), "Q0 sign imbalance")
    require(all(rank([permute(f, p) for p in s4]) == 4 for f in types), "full Hodge rank")
    slope = (1, -1, 1, -1)  # harmless nonzero scalar/sign from centered slopes
    slope_orbit = [permute(slope, p) for p in s4]
    require(rank(slope_orbit) == 3, "special-fiber centered rank")
    require(rank([list(row) + [1] for row in slope_orbit]) == 4, "special weight-inclusive rank")
    require(rank([list(row) + [1] for row in [permute(types[0], p) for p in s4]] +
                 [[-x for x in row] + [1] for row in [permute(types[0], p) for p in s4]]) == 5,
            "Hodge weight-inclusive rank")

    tate = []
    divisors = []
    for subset in combinations(range(8), 4):
        d = tuple(int(i in subset) - int(i + 4 in subset) for i in range(4))
        if all(x == 0 for x in d):
            divisors.append(subset)
        if all(sum(x * y for x, y in zip(d, row)) == 0 for row in slope_orbit):
            tate.append(subset)
    extras = sorted(set(tate) - set(divisors))
    require(len(tate) == 8 and len(divisors) == 6, "codimension-two dimensions")
    require(extras == [(0, 1, 2, 3), (4, 5, 6, 7)], "exceptional wedges")
    return {
        "status": "PASS",
        "polynomial": "X^4-10X^2+5X+2",
        "imaginary_quadratic": "Q(sqrt(-2))",
        "prime": 5,
        "real_sign_values": values,
        "cubic_mod13_values": cubic_values,
        "checked_CM_types": len(types),
        "Hodge_centered_rank": 4,
        "reduction_centered_rank": 3,
        "Tate_H4_dimension": len(tate),
        "divisor_product_H4_dimension": len(divisors),
        "limitation": "Finite support only; cited primary geometry and all-powers argument are written separately."
    }


if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True))
