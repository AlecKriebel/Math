#!/usr/bin/env python3
"""Exact verifier for a balanced-code Hodge determinant counterexample.

This refutes the proposed identity

    sum_k |det(U^T (L_{k1} tensor ... tensor L_{k4}) U)| = 1

under complement balance.  Only integer arithmetic in Z[zeta] is used,
where zeta^2 + zeta + 1 = 0.
"""

from __future__ import annotations

import itertools
from fractions import Fraction


Eis = tuple[int, int]  # a + b*zeta
ONE: Eis = (1, 0)
ZETA_POWERS: tuple[Eis, Eis, Eis] = ((1, 0), (0, 1), (-1, -1))


def add(x: Eis, y: Eis) -> Eis:
    return x[0] + y[0], x[1] + y[1]


def neg(x: Eis) -> Eis:
    return -x[0], -x[1]


def mul(x: Eis, y: Eis) -> Eis:
    # zeta^2 = -1-zeta
    return (
        x[0] * y[0] - x[1] * y[1],
        x[0] * y[1] + x[1] * y[0] - x[1] * y[1],
    )


def conjugate(x: Eis) -> Eis:
    # conjugate(zeta)=zeta^2=-1-zeta
    return x[0] - x[1], -x[1]


def norm(x: Eis) -> int:
    product = mul(x, conjugate(x))
    assert product[1] == 0
    return product[0]


def epsilon(k: int, a: int, b: int) -> int:
    if len({k, a, b}) < 3:
        return 0
    permutation = (k, a, b)
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions & 1 else 1


def words(length: int) -> list[tuple[int, ...]]:
    return list(itertools.product(range(3), repeat=length))


WORDS = words(4)
INDEX = {word: index for index, word in enumerate(WORDS)}

# Edge order: 01,02,03,12,13,23.
ADJACENCY = (
    (0, 2, 2, 1),
    (2, 0, 2, 1),
    (2, 2, 0, 1),
    (1, 1, 1, 0),
)
SYNDROME = (2, 2, 2, 1)


def phases() -> tuple[list[int], list[int]]:
    phase_u: list[int] = []
    phase_v: list[int] = []
    for word in WORDS:
        q = sum(
            ADJACENCY[i][j] * word[i] * word[j]
            for i in range(4)
            for j in range(i + 1, 4)
        ) % 3
        shift = sum(SYNDROME[i] * word[i] for i in range(4)) % 3
        phase_u.append(q)
        phase_v.append((q + shift) % 3)
    return phase_u, phase_v


def check_orthonormal(phase_u: list[int], phase_v: list[int]) -> None:
    # Both columns have 81 coefficients of modulus 1/9.
    assert Fraction(81, 81) == 1
    overlap: Eis = (0, 0)
    for pu, pv in zip(phase_u, phase_v):
        overlap = add(overlap, ZETA_POWERS[(pv - pu) % 3])
    assert overlap == (0, 0)


def reduced_projector_moment(
    phase_u: list[int], phase_v: list[int], retained: tuple[int, ...]
) -> Fraction:
    """Return ||Tr_(retained complement) P||_2^2 exactly."""
    erased = tuple(site for site in range(4) if site not in retained)
    numerator = 0
    for left in words(len(retained)):
        for right in words(len(retained)):
            entry: Eis = (0, 0)
            for rest in words(len(erased)):
                x = [0] * 4
                y = [0] * 4
                for position, site in enumerate(retained):
                    x[site] = left[position]
                    y[site] = right[position]
                for position, site in enumerate(erased):
                    x[site] = y[site] = rest[position]
                ix = INDEX[tuple(x)]
                iy = INDEX[tuple(y)]
                for phase in (phase_u, phase_v):
                    entry = add(
                        entry,
                        ZETA_POWERS[(phase[ix] - phase[iy]) % 3],
                    )
            numerator += norm(entry)
    # Each entry of the reduced projector has denominator 81.
    return Fraction(numerator, 81**2)


def hodge_determinants(
    phase_u: list[int], phase_v: list[int]
) -> tuple[list[Eis], int]:
    """Return the 81 determinant numerators and their common denominator."""
    phase = (phase_u, phase_v)
    determinants: list[Eis] = []
    for labels in words(4):
        entries = [[(0, 0) for _ in range(2)] for _ in range(2)]
        for input_word in WORDS:
            output = [0] * 4
            coefficient = 1
            for site in range(4):
                candidates = [
                    value
                    for value in range(3)
                    if epsilon(labels[site], value, input_word[site])
                ]
                if not candidates:
                    coefficient = 0
                    break
                output[site] = candidates[0]
                coefficient *= epsilon(
                    labels[site], output[site], input_word[site]
                )
            if coefficient == 0:
                continue
            input_index = INDEX[input_word]
            output_index = INDEX[tuple(output)]
            for p in range(2):
                for q in range(2):
                    term = ZETA_POWERS[
                        (phase[p][output_index] + phase[q][input_index]) % 3
                    ]
                    entries[p][q] = add(
                        entries[p][q],
                        term if coefficient > 0 else neg(term),
                    )
        determinant = add(
            mul(entries[0][0], entries[1][1]),
            neg(mul(entries[0][1], entries[1][0])),
        )
        determinants.append(determinant)
    # Each S entry has denominator 81, hence each determinant has 81^2.
    return determinants, 81**2


def fourier_rotated_amplitudes(
    phase_u: list[int], phase_v: list[int]
) -> tuple[list[Eis], list[Eis]]:
    """Apply the qutrit Fourier matrix on site zero.

    The returned coefficients have the common scalar denominator
    3*sqrt(3).  Each nonzero Eisenstein numerator is a unit.
    """
    out: list[list[Eis]] = []
    for phase in (phase_u, phase_v):
        column: list[Eis] = []
        for output_word in WORDS:
            value: Eis = (0, 0)
            for input_zero in range(3):
                input_word = list(output_word)
                input_word[0] = input_zero
                exponent = (
                    output_word[0] * input_zero
                    + phase[INDEX[tuple(input_word)]]
                ) % 3
                value = add(value, ZETA_POWERS[exponent])
            # The Fourier sum is either zero or three times a unit.
            assert value == (0, 0) or norm(value) == 9
            if value != (0, 0):
                assert value[0] % 3 == value[1] % 3 == 0
                value = value[0] // 3, value[1] // 3
                assert norm(value) == 1
            column.append(value)
        assert sum(value != (0, 0) for value in column) == 27
        out.append(column)
    return out[0], out[1]


def hodge_determinants_from_amplitudes(
    amplitudes: tuple[list[Eis], list[Eis]]
) -> tuple[dict[tuple[int, ...], Eis], int]:
    """Hodge determinants for columns with denominator 3*sqrt(3)."""
    determinants: dict[tuple[int, ...], Eis] = {}
    for labels in WORDS:
        entries = [[(0, 0) for _ in range(2)] for _ in range(2)]
        for input_word in WORDS:
            output = [0] * 4
            coefficient = 1
            for site in range(4):
                candidates = [
                    value
                    for value in range(3)
                    if epsilon(labels[site], value, input_word[site])
                ]
                if not candidates:
                    coefficient = 0
                    break
                output[site] = candidates[0]
                coefficient *= epsilon(
                    labels[site], output[site], input_word[site]
                )
            if coefficient == 0:
                continue
            input_index = INDEX[input_word]
            output_index = INDEX[tuple(output)]
            for p in range(2):
                for q in range(2):
                    term = mul(
                        amplitudes[p][output_index],
                        amplitudes[q][input_index],
                    )
                    entries[p][q] = add(
                        entries[p][q],
                        term if coefficient > 0 else neg(term),
                    )
        determinants[labels] = add(
            mul(entries[0][0], entries[1][1]),
            neg(mul(entries[0][1], entries[1][0])),
        )
    # Each S entry has denominator (3*sqrt(3))^2=27.
    return determinants, 27**2


def verify_rotated_sector_split(
    amplitudes: tuple[list[Eis], list[Eis]],
    determinants: dict[tuple[int, ...], Eis],
) -> None:
    """Verify d_(R,k)=det(S_k)/8 for all odd R and all k.

    Rather than introduce the 1/16 swap-sector projector explicitly, we
    verify its Walsh transform.  If omega=(u tensor v-v tensor u)/sqrt(2)
    and M_k=B_k tensor B_k, put h_(T,k)=omega^T F_T M_k omega.
    The asserted sector split is equivalent to

        h_empty=det(S_k), h_full=-det(S_k), h_T=0 otherwise.

    The common denominator of h is 2*27^2=1458.
    """
    wedge: dict[tuple[int, int], Eis] = {}
    for left in range(81):
        for right in range(81):
            value = add(
                mul(amplitudes[0][left], amplitudes[1][right]),
                neg(mul(amplitudes[1][left], amplitudes[0][right])),
            )
            if value != (0, 0):
                wedge[left, right] = value

    def hodge_image(
        labels: tuple[int, ...], word: tuple[int, ...]
    ) -> tuple[int, tuple[int, ...]]:
        output = [0] * 4
        coefficient = 1
        for site in range(4):
            candidates = [
                value
                for value in range(3)
                if epsilon(labels[site], value, word[site])
            ]
            if not candidates:
                return 0, tuple(output)
            output[site] = candidates[0]
            coefficient *= epsilon(labels[site], output[site], word[site])
        return coefficient, tuple(output)

    for labels, determinant in determinants.items():
        images = {
            index: hodge_image(labels, word)
            for index, word in enumerate(WORDS)
        }
        walsh_values: list[Eis] = []
        for mask in range(16):
            value: Eis = (0, 0)
            for (left, right), input_amplitude in wedge.items():
                coefficient_left, output_left = images[left]
                coefficient_right, output_right = images[right]
                coefficient = coefficient_left * coefficient_right
                if coefficient == 0:
                    continue
                output_left = list(output_left)
                output_right = list(output_right)
                for site in range(4):
                    if mask >> site & 1:
                        output_left[site], output_right[site] = (
                            output_right[site],
                            output_left[site],
                        )
                output_amplitude = wedge.get(
                    (INDEX[tuple(output_left)], INDEX[tuple(output_right)]),
                    (0, 0),
                )
                term = mul(output_amplitude, input_amplitude)
                value = add(value, term if coefficient > 0 else neg(term))
            walsh_values.append(value)

        # determinant has denominator 729, while h has denominator 1458.
        twice_determinant = add(determinant, determinant)
        assert walsh_values[0] == twice_determinant
        assert walsh_values[15] == neg(twice_determinant)
        assert all(walsh_values[mask] == (0, 0) for mask in range(1, 15))


def main() -> None:
    phase_u, phase_v = phases()
    check_orthonormal(phase_u, phase_v)

    moments: dict[int, Fraction] = {}
    for mask in range(16):
        retained = tuple(site for site in range(4) if mask >> site & 1)
        moments[mask] = reduced_projector_moment(
            phase_u, phase_v, retained
        )
    assert moments[0] == 4
    assert moments[15] == 2
    assert all(moments[mask] == Fraction(4, 3) for mask in range(1, 15))
    assert all(moments[mask] == moments[15 ^ mask] for mask in range(1, 15))

    # Walsh inversion gives the all-antisymmetric sector mass.
    alternating_moment_sum = sum(
        (-1) ** sum(mask >> site & 1 for site in range(4)) * moments[mask]
        for mask in range(16)
    )
    assert alternating_moment_sum == Fraction(10, 3)
    p_all = alternating_moment_sum / 16
    assert p_all == Fraction(5, 24)

    determinants, denominator = hodge_determinants(phase_u, phase_v)
    determinant_norms = [norm(value) for value in determinants]
    assert len(determinants) == 81
    assert set(determinant_norms) == {15309}
    assert 15309 == 3**7 * 7
    assert denominator == 3**8

    # Every absolute determinant is
    # sqrt(3^7*7)/3^8 = sqrt(21)/243.  Therefore the sum is
    # 81*sqrt(21)/243 = sqrt(21)/3, whose square is 7/3, not 1.
    squared_absolute_sum = Fraction(81**2 * 15309, denominator**2)
    assert squared_absolute_sum == Fraction(7, 3)
    assert squared_absolute_sum != 1

    # Now rotate only site zero by the unitary qutrit Fourier transform.
    # Every A_T, and hence complement balance and p_all, is preserved by
    # this local unitary.  Its sparse amplitudes are computed exactly above.
    rotated = fourier_rotated_amplitudes(phase_u, phase_v)
    assert all(sum(norm(value) for value in column) == 27 for column in rotated)
    rotated_overlap: Eis = (0, 0)
    for x, y in zip(*rotated):
        rotated_overlap = add(rotated_overlap, mul(conjugate(x), y))
    assert rotated_overlap == (0, 0)
    rotated_determinants, rotated_denominator = (
        hodge_determinants_from_amplitudes(rotated)
    )
    nonzero = {
        labels: value
        for labels, value in rotated_determinants.items()
        if value != (0, 0)
    }
    assert len(nonzero) == 27
    assert set(norm(value) for value in nonzero.values()) == {81}
    assert rotated_denominator == 729
    rotated_value_counts: dict[Eis, int] = {}
    for value in rotated_determinants.values():
        rotated_value_counts[value] = rotated_value_counts.get(value, 0) + 1
    assert rotated_value_counts == {
        (0, 0): 54,
        (0, -9): 12,
        (-9, 0): 9,
        (9, 9): 6,
    }
    # There are 27 nonzero determinants, each of modulus 9/729=1/81.
    rotated_absolute_sum = Fraction(27 * 9, rotated_denominator)
    assert rotated_absolute_sum == Fraction(1, 3)
    verify_rotated_sector_split(rotated, rotated_determinants)

    print("orthonormal frame: exact")
    print("proper nonempty moments: 4/3 (complement-balanced)")
    print("p_[4] = 5/24")
    print("81 determinant norms: 15309 / 6561^2")
    print("sum |det S_k| = sqrt(21)/3 > 1")
    print("after one local Fourier transform: sum |det S_k| = 1/3 < 1")
    print("each odd swap sector contributes exactly one eighth pointwise")


if __name__ == "__main__":
    main()
