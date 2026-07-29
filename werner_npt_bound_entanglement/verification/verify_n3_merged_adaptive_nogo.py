#!/usr/bin/env python3
"""Exact checker for the merged-adaptive formal no-go.

This verifies rational purity/overlap data, exact swap-sector masses,
all scalar weighted trace-norm identities, the formal negative target,
and the Pauli certificate J^3 = 8 J for the first common-origin
separator.  It does not claim that the formal marginals have a common
global realization.
"""

from fractions import Fraction as F
from itertools import product


PARTIES = 4
K = 1
ALL = (1 << PARTIES) - 1


def walsh_sector(moment: dict[int, F], sector: int) -> F:
    return sum(
        (-1) ** bin(sector & subset).count("1") * moment[subset]
        for subset in range(1 << PARTIES)
    ) / (1 << PARTIES)


def self_profile() -> dict[int, F]:
    return {
        subset: F(1) if subset in (0, ALL) else F(1, 2)
        for subset in range(1 << PARTIES)
    }


def cross_profile() -> dict[int, F]:
    q = {subset: F(1, 2) for subset in range(1 << PARTIES)}
    q[0] = F(1)
    q[ALL] = F(0)
    # K plus two physical sites, and the physical triple.
    q[(1 << 0) | (1 << 1) | (1 << 2)] = F(0)
    q[(1 << 0) | (1 << 1) | (1 << 3)] = F(0)
    q[(1 << 0) | (1 << 2) | (1 << 3)] = F(0)
    q[(1 << 1) | (1 << 2) | (1 << 3)] = F(0)
    return q


# Gaussian-integer matrices, represented by Python complex numbers whose
# real and imaginary parts remain exact small integers in every operation.
I2 = ((1, 0), (0, 1))
X = ((0, 1), (1, 0))
Y = ((0, -1j), (1j, 0))
Z = ((1, 0), (0, -1))
PAULI = (I2, X, Y, Z)


def kron(a, b):
    ar, ac = len(a), len(a[0])
    br, bc = len(b), len(b[0])
    return tuple(
        tuple(a[i // br][j // bc] * b[i % br][j % bc]
              for j in range(ac * bc))
        for i in range(ar * br)
    )


def pauli_string(labels):
    out = ((1,),)
    for label in labels:
        out = kron(out, PAULI[label])
    return out


def zero(n=16):
    return tuple(tuple(0 for _ in range(n)) for _ in range(n))


def add(*matrices):
    n = len(matrices[0])
    return tuple(
        tuple(sum(matrix[i][j] for matrix in matrices)
              for j in range(n))
        for i in range(n)
    )


def scale(c, matrix):
    return tuple(tuple(c * value for value in row) for row in matrix)


def multiply(a, b):
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n))
              for j in range(n))
        for i in range(n)
    )


def main() -> None:
    a = self_profile()
    b = self_profile()
    q = cross_profile()

    assert all(a[s] == a[ALL ^ s] for s in range(16))
    assert all(b[s] == b[ALL ^ s] for s in range(16))
    assert all(q[s] * q[s] <= a[s] * b[s] for s in range(16))

    self_sector = {r: walsh_sector(a, r) for r in range(16)}
    cross_sector = {r: walsh_sector(q, r) for r in range(16)}
    assert all(value >= 0 for value in self_sector.values())
    assert all(value >= 0 for value in cross_sector.values())
    assert self_sector[0] == F(9, 16)
    assert all(
        self_sector[r] == (F(1, 16)
                           if bin(r).count("1") in (2, 4) else F(0))
        for r in range(1, 16)
    )
    expected_cross_support = {0, 1, 2, 4, 8, 15}
    assert cross_sector[0] == F(3, 8)
    assert all(
        cross_sector[r] == (
            F(1, 8) if r in expected_cross_support - {0} else F(0)
        )
        for r in range(1, 16)
    )

    # Original adaptive frames: HS^2=1/6, trace norm^2=1/3.
    p = F(1, 2)
    original_delta = p - 3 * F(1, 6)
    original_alpha = F(1) - 3 * F(1, 3)
    original_beta = F(1, 3) - 2 * F(1, 6)
    assert (original_delta, original_alpha, original_beta) == (0, 0, 0)

    # The formal exterior target.
    sum_q_ki = sum(q[1 | (1 << i)] for i in (1, 2, 3))
    sum_q_i = sum(q[1 << i] for i in (1, 2, 3))
    sum_q_kij = sum(
        q[1 | (1 << i) | (1 << j)]
        for i in (1, 2, 3)
        for j in range(i + 1, 4)
    )
    d0 = 3 * q[1] - 2 * sum_q_ki + sum_q_i
    exterior = sum_q_kij - sum_q_i + F(1, 2)
    sharp_defect = d0 + exterior
    formal_q3 = (
        q[1] - F(1, 2) * sum_q_ki
        + F(1, 4) * sum_q_kij - F(1, 8) * q[ALL]
    )
    assert d0 == 0
    assert exterior == -1
    assert sharp_defect == -1
    assert formal_q3 == F(-1, 4)

    # Weighted merged trace-norm identities, checked as polynomial
    # coefficients at several exact x,y values.  Since every expression is
    # quadratic, these checks also independently catch coefficient errors.
    for x, y in product((F(0), F(1), F(2), F(3)), repeat=2):
        if x == y == 0:
            continue
        # Branch Z assigned to the merged block.
        delta_z = (x + y) ** 2 / 2
        alpha_z = 4 * x * y
        beta_z = (x - y) ** 2
        assert 2 * delta_z == alpha_z + beta_z
        assert min(delta_z, alpha_z, beta_z) >= 0

        # Branch X or Y assigned to the merged block.
        delta_xy = (x * x + y * y) / 2
        alpha_xy = 2 * x * y
        beta_xy = (x - y) ** 2
        assert 2 * delta_xy == alpha_xy + beta_xy
        assert min(delta_xy, alpha_xy, beta_xy) >= 0

    # Exact Pauli certificate for the first violated common-origin
    # constraint.  Mhat and Nhat are sqrt(3) M and sqrt(3) N.
    def term(k_axis, site, site_axis):
        labels = [0, 0, 0, 0]
        labels[0] = k_axis
        labels[site] = site_axis
        return pauli_string(labels)

    mhat = scale(-1, add(
        term(1, 1, 1), term(2, 2, 2), term(3, 3, 3)
    ))
    nhat = scale(-1, add(
        term(2, 1, 2), term(3, 2, 3), term(1, 3, 1)
    ))
    identity = pauli_string((0, 0, 0, 0))
    assert multiply(mhat, mhat) == scale(3, identity)
    assert multiply(nhat, nhat) == scale(3, identity)

    anticommutator_numerator = add(
        multiply(mhat, nhat), multiply(nhat, mhat)
    )
    # {M,N}=anticommutator_numerator/3=2J/3.
    assert all(value.real % 2 == 0 and value.imag % 2 == 0
               for row in anticommutator_numerator
               for value in row)
    j_matrix = scale(F(1, 2), anticommutator_numerator)
    assert multiply(multiply(j_matrix, j_matrix), j_matrix) == scale(
        8, j_matrix
    )

    print("verified exact merged-adaptive formal no-go")
    print("D0 =", d0, "E =", exterior, "D =", sharp_defect,
          "formal Q3 =", formal_q3)
    print("verified J^3 = 8 J, hence ||{M,N}|| <= 4 sqrt(2) / 3 < 2")


if __name__ == "__main__":
    main()
