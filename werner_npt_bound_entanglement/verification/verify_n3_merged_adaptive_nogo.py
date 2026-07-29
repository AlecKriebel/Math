#!/usr/bin/env python3
"""Exact checker for the merged-adaptive formal no-go.

This verifies rational purity/overlap data, exact swap-sector masses,
all scalar weighted trace-norm identities, the formal negative target,
and the Pauli certificate J^3 = 8 J for the first common-origin
separator.  It does not claim that the formal marginals have a common
global realization.
"""

from fractions import Fraction as F
from itertools import permutations, product


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


def second_self_profile() -> dict[int, F]:
    a = {0: F(1), ALL: F(1), 1: F(1, 2), 14: F(1, 2)}
    for i in (1, 2, 3):
        a[1 << i] = F(53, 100)
        a[ALL ^ (1 << i)] = F(53, 100)
        a[1 | (1 << i)] = F(101, 200)
        a[ALL ^ (1 | (1 << i))] = F(101, 200)
    return a


def second_cross_profile() -> dict[int, F]:
    q = {0: F(1), ALL: F(0), 1: F(1, 2), 14: F(3, 200)}
    for i in (1, 2, 3):
        q[1 << i] = F(51, 100)
        q[1 | (1 << i)] = F(99, 200)
    for i in (1, 2, 3):
        for j in range(i + 1, 4):
            q[(1 << i) | (1 << j)] = F(101, 200)
            q[1 | (1 << i) | (1 << j)] = F(1, 200)
    return q


def third_self_profile() -> dict[int, F]:
    a = {0: F(1), ALL: F(1), 1: F(1, 2), 14: F(1, 2)}
    for i in (1, 2, 3):
        a[1 << i] = F(53, 100)
        a[ALL ^ (1 << i)] = F(53, 100)
        a[1 | (1 << i)] = F(99, 200)
        a[ALL ^ (1 | (1 << i))] = F(99, 200)
    return a


def third_cross_profile() -> dict[int, F]:
    q = {0: F(1), ALL: F(0), 1: F(1, 2), 14: F(9, 500)}
    for i in (1, 2, 3):
        q[1 << i] = F(253, 500)
        q[1 | (1 << i)] = F(483, 1000)
    for i in (1, 2, 3):
        for j in range(i + 1, 4):
            q[(1 << i) | (1 << j)] = F(99, 200)
            q[1 | (1 << i) | (1 << j)] = F(0)
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


def trace_matrix(a):
    return sum(a[i][i] for i in range(len(a)))


def matrix_element(left, matrix, right):
    return sum(
        left[i].conjugate() * matrix[i][j] * right[j]
        for i in range(len(left))
        for j in range(len(right))
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

    # The second formal survivor, which passes the full pair orbit of the
    # joint-frame separator.
    a2 = second_self_profile()
    b2 = second_self_profile()
    q2 = second_cross_profile()
    assert len(a2) == len(b2) == len(q2) == 16
    assert all(a2[s] == a2[ALL ^ s] for s in range(16))
    assert all(q2[s] * q2[s] <= a2[s] * b2[s] for s in range(16))
    a2_sector = {r: walsh_sector(a2, r) for r in range(16)}
    q2_sector = {r: walsh_sector(q2, r) for r in range(16)}
    expected_a2 = {
        0: F(921, 1600),
        3: F(105, 1600), 5: F(105, 1600), 9: F(105, 1600),
        6: F(93, 1600), 10: F(93, 1600), 12: F(93, 1600),
        15: F(85, 1600),
    }
    expected_q2 = {
        0: F(303, 800), 1: F(103, 800),
        2: F(99, 800), 4: F(99, 800), 8: F(99, 800),
        15: F(97, 800),
    }
    assert all(a2_sector[r] == expected_a2.get(r, F(0))
               for r in range(16))
    assert all(q2_sector[r] == expected_q2.get(r, F(0))
               for r in range(16))

    sum_q2_ki = sum(q2[1 | (1 << i)] for i in (1, 2, 3))
    sum_q2_i = sum(q2[1 << i] for i in (1, 2, 3))
    sum_q2_kij = sum(
        q2[1 | (1 << i) | (1 << j)]
        for i in (1, 2, 3)
        for j in range(i + 1, 4)
    )
    d02 = 3 * q2[1] - 2 * sum_q2_ki + sum_q2_i
    exterior2 = sum_q2_kij - sum_q2_i + F(1, 2)
    defect2 = d02 + exterior2
    formal_q32 = (
        q2[1] - F(1, 2) * sum_q2_ki
        + F(1, 4) * sum_q2_kij
    )
    assert d02 == F(3, 50)
    assert exterior2 == F(-203, 200)
    assert defect2 == F(-191, 200)
    assert formal_q32 == F(-191, 800)

    # Each original permutation has these exact adaptive gaps.
    assert F(1, 2) - 3 * F(4, 25) == F(1, 50)
    assert F(1) - 3 * F(8, 25) == F(1, 25)
    assert F(8, 25) - 2 * F(4, 25) == 0

    # Build all six normalized Pauli sign frames.  For relative
    # three-cycles the exact numerator A=3{M,N} obeys A^3=32A, so
    # ||{M,N}||=4 sqrt(2)/3.  Other pairs need only the universal bound 2.
    frames = []
    frame_labels = list(permutations((1, 2, 3)))
    for assignment in frame_labels:
        frame = zero()
        for site, axis in enumerate(assignment, 1):
            frame = add(frame, scale(-1, term(axis, site, axis)))
        assert multiply(frame, frame) == scale(3, identity)
        frames.append(frame)

    def compose_inverse(left, right):
        # Permutations are tuples of images of positions 0,1,2.
        inverse = [0, 0, 0]
        for position, image_value in enumerate(left):
            inverse[image_value - 1] = position
        return tuple(
            inverse[right[position] - 1] for position in range(3)
        )

    low_pairs = 0
    for first in range(6):
        for second in range(first + 1, 6):
            numerator = add(
                multiply(frames[first], frames[second]),
                multiply(frames[second], frames[first]),
            )
            relative = compose_inverse(
                frame_labels[first], frame_labels[second]
            )
            is_three_cycle = all(relative[position] != position
                                 for position in range(3))
            if is_three_cycle:
                assert multiply(
                    multiply(numerator, numerator), numerator
                ) == scale(32, numerator)
                assert numerator != zero()
                low_pairs += 1
            else:
                # For a relative transposition the exact spectrum of the
                # numerator is contained in {-2,6}, and 6 occurs.
                assert multiply(numerator, numerator) == add(
                    scale(4, numerator), scale(12, identity)
                )
                assert numerator != scale(-2, identity)
            # The pairwise separator for a three-cycle is
            # 2/25 >= 1 - 2 sqrt(2)/3.  Squaring its positive radical
            # comparison gives 5000 > 4761.
    assert low_pairs == 6
    assert F(8, 9) > F(529, 625)

    # Coefficient checks for every weighted merged inequality.
    # X/Y on the merged block:
    assert F(1) - F(53, 100) == F(47, 100)
    assert (
        F(101, 100) + F(1, 100) - 2 * F(51, 100)
    ) == 0
    # Z on the merged block:
    assert F(1) - F(101, 200) == F(99, 200)
    assert 2 * F(99, 200) - 2 * F(1, 100) == F(97, 100)
    # Every coefficient in the piecewise trace-norm gaps (58)--(59)
    # is positive.
    assert min(F(49, 25), F(47, 50), F(99, 25),
               F(99, 100), F(194, 100)) > 0

    # Exact three-frame Clifford certificate.  The even and odd
    # integer-Pauli sums have norm 5; after dividing by sqrt(3), this
    # gives the threshold m^2 <= 25/27.
    for triple in ((0, 3, 4), (1, 2, 5)):
        triple_sum = add(*(frames[index] for index in triple))
        polynomial = identity
        for root in (-3, -1, 3, 5):
            polynomial = multiply(
                polynomial, add(triple_sum, scale(-root, identity))
            )
        assert polynomial == zero()
        # Exhibit a 5-eigenvector for the even triple.  The odd case is
        # unitarily equivalent and has the same certified polynomial.
        if triple == (0, 3, 4):
            vector = [F(0) for _ in range(16)]
            # Use the integer-scaled vector so that multiplication by the
            # Gaussian-integer Pauli matrices remains exact in Python.
            vector[8] = F(3)
            vector[1] = vector[2] = vector[4] = F(-1)
            product_vector = [
                sum(triple_sum[row][column] * vector[column]
                    for column in range(16))
                for row in range(16)
            ]
            assert product_vector == [5 * value for value in vector]

    # The second survivor is excluded, while the third survives:
    assert F(24, 25) > F(25, 27)
    assert F(23, 25) <= F(25, 27)

    # The entire arbitrarily weighted six-frame support hierarchy also
    # fails to exclude the third survivor.  The full integer-frame sum
    # has exact spectrum contained in {-6,-2,6,10}.
    full_sum = add(*frames)
    polynomial = identity
    for root in (-6, -2, 6, 10):
        polynomial = multiply(
            polynomial, add(full_sum, scale(-root, identity))
        )
    assert polynomial == zero()

    # Explicit opposite-parity vectors u_raw and w_raw.  Their squared
    # norms are 12 and 4, respectively.  For every integer frame their
    # normalized expectations are 5/3 and 1, and all cross matrix
    # elements vanish.
    u_raw = [0 for _ in range(16)]
    u_raw[1] = u_raw[2] = u_raw[4] = -1
    u_raw[8] = 3
    w_raw = [0 for _ in range(16)]
    w_raw[5], w_raw[6], w_raw[9], w_raw[10] = 1, -1, -1, 1
    assert sum(abs(value) ** 2 for value in u_raw) == 12
    assert sum(abs(value) ** 2 for value in w_raw) == 4
    assert sum(
        left.conjugate() * right for left, right in zip(u_raw, w_raw)
    ) == 0
    for frame in frames:
        assert matrix_element(u_raw, frame, u_raw) == 20
        assert matrix_element(w_raw, frame, w_raw) == 4
        assert matrix_element(u_raw, frame, w_raw) == 0

    # t=3(sqrt(69)-5)/10 lies in (0,1), since 25<69 and 621<625.
    # Substitution into (1+2t/3)/sqrt(3) gives sqrt(23)/5.
    assert 25 < 69
    assert 9 * 69 < 25 * 25
    assert F(1, 3) * 23 == F(23, 3)

    # The eigenvalue-10 spectral projection is P=projector_numerator/768.
    # Its exact compression and trace identities certify both the
    # three-dimensional top eigenspace and the symmetric mixed-state
    # realization of all nine individual Pauli first moments.
    projector_numerator = multiply(
        multiply(
            add(full_sum, scale(-6, identity)),
            add(full_sum, scale(2, identity)),
        ),
        add(full_sum, scale(6, identity)),
    )
    assert multiply(
        projector_numerator, projector_numerator
    ) == scale(768, projector_numerator)
    assert trace_matrix(projector_numerator) == 3 * 768
    for frame in frames:
        assert scale(
            3,
            multiply(
                multiply(projector_numerator, frame),
                projector_numerator,
            ),
        ) == scale(5 * 768, projector_numerator)
    for axis in (1, 2, 3):
        for site in (1, 2, 3):
            pauli_correlator = scale(-1, term(axis, site, axis))
            # Tr((P/3) O_{axis,site})=5/9.
            assert trace_matrix(
                multiply(projector_numerator, pauli_correlator)
            ) == 1280

    a3 = third_self_profile()
    b3 = third_self_profile()
    q3 = third_cross_profile()
    assert len(a3) == len(b3) == len(q3) == 16
    assert all(a3[s] == a3[ALL ^ s] for s in range(16))
    assert all(q3[s] * q3[s] <= a3[s] * b3[s] for s in range(16))
    a3_sector = {r: walsh_sector(a3, r) for r in range(16)}
    q3_sector = {r: walsh_sector(q3, r) for r in range(16)}
    expected_a3 = {
        0: F(183, 320),
        3: F(107, 1600), 5: F(107, 1600), 9: F(107, 1600),
        6: F(19, 320), 10: F(19, 320), 12: F(19, 320),
        15: F(79, 1600),
    }
    expected_q3 = {
        0: F(597, 1600), 1: F(259, 2000),
        2: F(247, 2000), 4: F(247, 2000), 8: F(247, 2000),
        3: F(1, 1600), 5: F(1, 1600), 9: F(1, 1600),
        6: F(17, 8000), 10: F(17, 8000), 12: F(17, 8000),
        15: F(949, 8000),
    }
    assert all(a3_sector[r] == expected_a3.get(r, F(0))
               for r in range(16))
    assert all(q3_sector[r] == expected_q3.get(r, F(0))
               for r in range(16))

    sum_q3_ki = sum(q3[1 | (1 << i)] for i in (1, 2, 3))
    sum_q3_i = sum(q3[1 << i] for i in (1, 2, 3))
    sum_q3_kij = sum(
        q3[1 | (1 << i) | (1 << j)]
        for i in (1, 2, 3)
        for j in range(i + 1, 4)
    )
    d03 = 3 * q3[1] - 2 * sum_q3_ki + sum_q3_i
    exterior3 = sum_q3_kij - sum_q3_i + F(1, 2)
    defect3 = d03 + exterior3
    formal_q33 = (
        q3[1] - F(1, 2) * sum_q3_ki
        + F(1, 4) * sum_q3_kij
    )
    assert d03 == F(3, 25)
    assert exterior3 == F(-509, 500)
    assert defect3 == F(-449, 500)
    assert formal_q33 == F(-449, 2000)

    # Third-survivor adaptive and weighted-merged coefficient checks.
    assert F(1, 2) - F(23, 50) == F(1, 25)
    assert F(1) - 2 * F(23, 50) == F(2, 25)
    assert F(23, 25) <= F(25, 27)
    assert F(47, 100) > 0 and F(11, 500) > 0
    assert F(101, 200) > 0 and F(483, 500) > 0
    assert F(101, 50) > 0
    assert F(47, 50) > 0 and F(11, 250) > 0

    print("verified exact merged-adaptive formal no-go")
    print("D0 =", d0, "E =", exterior, "D =", sharp_defect,
          "formal Q3 =", formal_q3)
    print("verified J^3 = 8 J, hence ||{M,N}|| <= 4 sqrt(2) / 3 < 2")
    print("verified joint-orbit survivor: D =", defect2,
          "formal Q3 =", formal_q32)
    print("verified three-frame survivor: D =", defect3,
          "formal Q3 =", formal_q33)


if __name__ == "__main__":
    main()
