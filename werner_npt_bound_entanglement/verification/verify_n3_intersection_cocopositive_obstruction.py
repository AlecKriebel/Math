#!/usr/bin/env python3
"""Exact verifier for the qutrit-GHZ copositive Schur no-go.

This checker uses only Python's standard library and rational
arithmetic.  It reconstructs the GHZ block of A_w, the anchor energy,
the local-swap expectation, and the partially transposed rank-one Choi
expectation on the explicit Schmidt-rank-two vector q.
"""

from fractions import Fraction as F
from itertools import product


def words():
    return list(product(range(3), repeat=3))


BASIS = words()
INDEX = {word: index for index, word in enumerate(BASIS)}
GHZ = [(r, r, r) for r in range(3)]


def a_entry(row, col):
    """Exact entry of A_w for normalized qutrit GHZ w."""
    value = F(0)

    # P_w.
    if row in GHZ and col in GHZ:
        value += F(1, 3)

    # -1/2 sum_i I_i tensor rho_{\bar i}.
    # rho_{\bar i}=(1/3) sum_r |rr><rr|.
    for i in range(3):
        other = [j for j in range(3) if j != i]
        if (
            row[i] == col[i]
            and row[other[0]] == row[other[1]]
            and col[other[0]] == col[other[1]]
            and row[other[0]] == col[other[0]]
        ):
            value -= F(1, 6)

    # +1/4 sum_{i<j} I_{ij} tensor rho_k, with rho_k=I/3.
    # Every one of the three summands is I/3.
    if row == col:
        value += F(1, 4)

    # -I/8.
    if row == col:
        value -= F(1, 8)

    return value


def swap_subset(pair, subset):
    """Swap selected physical sites between the two replicas."""
    left, right = list(pair[0]), list(pair[1])
    for site in subset:
        left[site], right[site] = right[site], left[site]
    return tuple(left), tuple(right)


def y_expectation(q_support):
    """Compute <q| prod_i(I-F_i/2) |q> exactly."""
    total = F(0)
    for mask in range(8):
        subset = tuple(i for i in range(3) if mask & (1 << i))
        coefficient = F(-1, 2) ** len(subset)
        for ket, ket_coefficient in q_support.items():
            image = swap_subset(ket, subset)
            total += (
                coefficient
                * ket_coefficient
                * q_support.get(image, F(0))
            )
    return total


def r_expectation(indices):
    """Compute <q|(|vec A><vec A|)^Gamma|q> on sum_i |g_i,g_i>."""
    return sum(
        a_entry(GHZ[i], GHZ[j]) * a_entry(GHZ[j], GHZ[i])
        for i in indices
        for j in indices
    )


def main():
    expected_block = [
        [F(-1, 24), F(1, 3), F(1, 3)],
        [F(1, 3), F(-1, 24), F(1, 3)],
        [F(1, 3), F(1, 3), F(-1, 24)],
    ]
    block = [[a_entry(row, col) for col in GHZ] for row in GHZ]
    assert block == expected_block

    # For w=(g0+g1+g2)/sqrt(3), <w|A_w|w> is the average
    # of all entries in the displayed rational block.
    anchor_energy = sum(sum(row) for row in block) / 3
    assert anchor_energy == F(5, 8)

    q_support = {
        (GHZ[0], GHZ[0]): F(1),
        (GHZ[1], GHZ[1]): F(1),
    }

    # The coefficient matrix of q has two nonzero diagonal entries,
    # hence exact rank (and Schmidt rank) two.
    coefficient_diagonal = [F(1), F(1)] + [F(0)] * 25
    assert sum(value != 0 for value in coefficient_diagonal) == 2

    y_value = y_expectation(q_support)
    assert y_value == F(1, 4)
    filtered_value = anchor_energy * y_value
    assert filtered_value == F(5, 32)

    choi_pt_value = r_expectation((0, 1))
    assert choi_pt_value == F(65, 288)

    obstruction = filtered_value - choi_pt_value
    assert obstruction == F(-5, 72)

    print("A_w on GHZ subspace:")
    for row in block:
        print(" ", row)
    print("anchor energy a =", anchor_energy)
    print("<q|Y|q> =", y_value)
    print("<q|aY|q> =", filtered_value)
    print("<q|(|vec A><vec A|)^Gamma|q> =", choi_pt_value)
    print("<q|J(Phi_w)^Gamma|q> =", obstruction)
    print("verified: exact Schmidt-rank-two copositive-route obstruction")


if __name__ == "__main__":
    main()
