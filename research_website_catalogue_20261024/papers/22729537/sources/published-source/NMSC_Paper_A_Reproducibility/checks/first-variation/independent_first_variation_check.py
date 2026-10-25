#!/usr/bin/env python3
"""Exact independent regression for Paper A's first-variation jet recurrence.

Nodes: NMSA-002 and the local parameter-fiber consequence.
All inputs are the small integer matrices below. No project implementation,
generated outputs, external packages, numerical tolerances, or file inputs are
used. This finite check supplements the universal proof; it does not replace it.
"""

if not __debug__:
    raise SystemExit("Independent recurrence check requires assertions: do not use python -O")


def add(a, b):
    return [[x + y for x, y in zip(row_a, row_b)]
            for row_a, row_b in zip(a, b)]


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def power_variations(a, da, maximum):
    power = [[1, 0], [0, 1]]
    variation = [[0, 0], [0, 0]]
    result = []
    for _ in range(maximum + 1):
        result.append((power, variation))
        # Differentiate A^(k+1) = A^k A, retaining noncommuting order.
        power, variation = mul(power, a), add(mul(variation, a), mul(power, da))
    return result


def polynomial_product(a, b):
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i + j] += x * y
    return result


def main():
    x, dx = [[-1, 0], [0, -3]], [[1, 2], [3, 4]]
    y, dy = [[-2, 0], [0, -5]], [[2, 1], [-1, 3]]
    middle, dmiddle = [[1, 3], [2, 4]], [[0, 1], [1, 0]]
    row, drow = [[1, 2]], [[3, -1]]
    column, dcolumn = [[1], [2]], [[0], [1]]
    x_jets, y_jets = power_variations(x, dx, 15), power_variations(y, dy, 15)

    # Mixed derivatives at x=y=0 of the parameter derivative of
    # row exp(x X) middle exp(y Y) column. Differentiate all five factors.
    mixed = []
    for p, dp in x_jets:
        jet_row = []
        for q, dq in y_jets:
            terms = [(drow, p, middle, q, column),
                     (row, dp, middle, q, column),
                     (row, p, dmiddle, q, column),
                     (row, p, middle, dq, column),
                     (row, p, middle, q, dcolumn)]
            value = 0
            for term in terms:
                product = term[0]
                for factor in term[1:]:
                    product = mul(product, factor)
                value += product[0][0]
            jet_row.append(value)
        mixed.append(jet_row)

    # Ascending coefficients of (D+1)^2(D+3)^2 and (D+2)^2(D+5)^2.
    px = polynomial_product([3, 4, 1], [3, 4, 1])
    py = polynomial_product([10, 7, 1], [10, 7, 1])
    checks = 0
    for k in range(12):
        for ell in range(16):
            assert sum(px[j] * mixed[k + j][ell] for j in range(5)) == 0
            checks += 1
    for ell in range(12):
        for k in range(16):
            assert sum(py[j] * mixed[k][ell + j] for j in range(5)) == 0
            checks += 1

    # Negative control: base (undoubled) characteristic recurrence fails.
    assert any(sum([3, 4, 1][j] * mixed[k + j][ell] for j in range(3)) != 0
               for k in range(14) for ell in range(16))
    assert checks == 384
    print(f"PASS: {checks} exact mixed first-variation recurrences; "
          "undoubled recurrence rejected.")


if __name__ == "__main__":
    main()
