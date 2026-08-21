"""Floating-point probe for the polarized Hodge moment tensors.

For a four-qutrit code plane with normalized bivector ``omega``, this
computes

    M_S(k,l) = omega^T (B_k tensor B_l) F_S omega,

where B_k is the tensor product of the four local epsilon matrices.  The
Walsh transforms Q_R are also reported.  This is discovery code only.
"""

from __future__ import annotations

import math
import sys


def read_frame(path: str) -> tuple[list[complex], list[complex]]:
    u = [0j] * 81
    v = [0j] * 81
    with open(path, encoding="utf-8") as source:
        for line in source:
            fields = line.split()
            index = int(fields[0])
            u[index] = complex(float(fields[1]), float(fields[2]))
            v[index] = complex(float(fields[3]), float(fields[4]))
    return u, v


def epsilon(k: int, a: int, b: int) -> int:
    if k == a or k == b or a == b:
        return 0
    values = (k, a, b)
    inversions = sum(
        values[i] > values[j] for i in range(3) for j in range(i + 1, 3)
    )
    return -1 if inversions & 1 else 1


def hodge_maps() -> list[list[tuple[int, int, int]]]:
    maps: list[list[tuple[int, int, int]]] = []
    for code in range(81):
        value = code
        labels = []
        for _ in range(4):
            labels.append(value % 3)
            value //= 3
        sparse = []
        for input_index in range(81):
            value = input_index
            inputs = []
            for _ in range(4):
                inputs.append(value % 3)
                value //= 3
            output_index = 0
            place = 1
            sign = 1
            for site in range(4):
                found: tuple[int, int] | None = None
                for output in range(3):
                    coefficient = epsilon(
                        labels[site], output, inputs[site]
                    )
                    if coefficient:
                        found = (output, coefficient)
                        break
                if found is None:
                    sign = 0
                    break
                output_index += found[0] * place
                place *= 3
                sign *= found[1]
            if sign:
                sparse.append((output_index, input_index, sign))
        maps.append(sparse)
    return maps


def swap_table(mask: int) -> list[int]:
    table = []
    for left in range(81):
        for right in range(81):
            swapped_left = left
            swapped_right = right
            for site in range(4):
                if mask >> site & 1:
                    place = 3**site
                    x = (swapped_left // place) % 3
                    y = (swapped_right // place) % 3
                    swapped_left += (y - x) * place
                    swapped_right += (x - y) * place
            table.append(81 * swapped_left + swapped_right)
    return table


def inner(left: list[complex], right: list[complex]) -> complex:
    return sum(x.conjugate() * y for x, y in zip(left, right))


def main() -> None:
    u, v = read_frame(sys.argv[1])
    scale = 1.0 / math.sqrt(2.0)
    omega = [
        scale * (u[a] * v[b] - v[a] * u[b])
        for a in range(81)
        for b in range(81)
    ]
    maps = hodge_maps()
    moments: list[list[complex]] = []
    for mask in range(16):
        swapped = swap_table(mask)
        tensor = [0j] * 6561
        for k, left_map in enumerate(maps):
            for l, right_map in enumerate(maps):
                value = 0j
                for a, c, left_sign in left_map:
                    output_base = 81 * a
                    input_base = 81 * c
                    for b, d, right_sign in right_map:
                        value += (
                            left_sign
                            * right_sign
                            * omega[output_base + b]
                            * omega[swapped[input_base + d]]
                        )
                tensor[81 * k + l] = value
        moments.append(tensor)
        print("M_norm", mask, inner(tensor, tensor).real)

    sectors = []
    for sector in range(16):
        tensor = [
            sum(
                (-1 if (sector & mask).bit_count() & 1 else 1)
                * moments[mask][entry]
                for mask in range(16)
            )
            / 16.0
            for entry in range(6561)
        ]
        sectors.append(tensor)
        print("Q_norm", sector, inner(tensor, tensor).real)

    print("M_gram_with_zero")
    for mask in range(16):
        value = inner(moments[0], moments[mask])
        print(mask, value.real, value.imag)

    print("Q_gram_odd")
    odd = [mask for mask in range(16) if mask.bit_count() & 1]
    for left in odd:
        print(
            left,
            *(inner(sectors[left], sectors[right]).real for right in odd),
        )


if __name__ == "__main__":
    main()
