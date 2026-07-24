#!/usr/bin/env python3
"""Verify the factorwise trace/Parseval sieve for the H(668) phase cone.

The prime-167 ninth-root split stores one trivial coordinate in F_(167^6)
and six primitive coordinates in F_(167^12) for each of the two channels.
This module proves that a three-by-three row-Galois transform recovers the
original six Eisenstein fiber words from those four cone blocks.  It then
checks two exact identities for every H-invariant Eisenstein word U:

    37 U(0) = c + 3 Tr(x) + 3 Tr(y),

    37 sum_j U_j conjugate(V_j)
      = c_U conjugate(c_V)
        + 3 Tr(x_U y_V^(167^5) + y_U x_V^(167^7)).

The first identity fixes the six normalized zero-column fiber values.  The
diagonal specialization of the second fixes the six profile-resolved support
counts.  All arithmetic is exact and uses the repository's finite-field
implementation.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from typing import Optional, Sequence

from verify_lp333_order3_labeled_jet import ZERO_A_PLUS, ZERO_B_PLUS
from verify_lp333_order3_phase_factor import fiber_phase
import verify_lp333_order3_prime167_split as split


P = 167
N = 37
Q = P * P

K = split.K
L = split.L
K6Word = tuple[L, ...]
FiberWord = tuple[K, ...]
FiberCRT = tuple[K, L, L]

K_THREE: K = (3, 0)
K_37: K = (37, 0)
L_MINUS_ONE: L = split.l_embed((-1, 0))

EXPECTED_LOCAL_ALPHABET_SHA256 = (
    "111b47b011ff267769cb6af618baf048284fc6db8a5bc69e02c40be156a04277"
)
EXPECTED_FULL_ALGEBRA_SHA256 = (
    "2978c247c1ac8ae68d876420d2521bfbaa1c7708a956d322e09af2b14204db26"
)
EXPECTED_PHYSICAL_FIXTURE_SHA256 = (
    "dbf9f30d023049d99d3fc3f038b7fc99124d535a83022fd3d825da9c581d6437"
)
EXPECTED_NEGATIVE_CONE_SHA256 = (
    "98add67fffdbe386b2caabc1e679352e9d76f9f51a56e663ad8eb59cd830e6fe"
)
EXPECTED_COMPOSITE_SHA256 = (
    "8253d73531cfbf4d5111c211b75da5abfdd8abeb11efc47973e49daedcc9b1e1"
)
EXPECTED_BIT_DECODER_SHA256 = (
    "7bf5e08aca41bb4822472c4f8ed08fd7271429d823dff132589c7521c569169a"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def l_sum(values: Sequence[L]) -> L:
    result = split.L_ZERO
    for value in values:
        result = split.l_add(result, value)
    return result


def l_polynomial_evaluate(coefficients: Sequence[L], point: L) -> L:
    result = split.L_ZERO
    for coefficient in reversed(coefficients):
        result = split.l_add(
            split.l_multiply(result, point),
            coefficient,
        )
    return result


def trace_e_to_k(value: L) -> K:
    """Trace F_(167^12) to F_(167^2)."""

    result = split.L_ZERO
    current = value
    for _ in range(6):
        result = split.l_add(result, current)
        current = split.l_power(current, Q)
    if current != value:
        raise AssertionError("the E/k trace orbit failed to close")
    return split.l_constant(result)


def trace_e_to_k6(value: L) -> L:
    """Trace F_(167^12) to F_(167^6)."""

    result = split.l_add(value, split.l_power(value, P**6))
    if split.l_power(result, P**6) != result:
        raise AssertionError("an E/K trace left F_(167^6)")
    return result


def trace_k3_to_f(value: L) -> int:
    """Trace F_(167^3) to F_167, represented inside the large field."""

    if split.l_power(value, P**3) != value:
        raise ValueError("the input is not in F_(167^3)")
    result = split.L_ZERO
    current = value
    for _ in range(3):
        result = split.l_add(result, current)
        current = split.l_power(current, P)
    constant = split.l_constant(result)
    if constant[1] != 0:
        raise AssertionError("an F_(167^3)/F_167 trace left the prime field")
    return constant[0]


def ninth_root() -> L:
    candidate = split.l_power(
        split.field_fixture(2),
        (split.E_SIZE - 1) // 9,
    )
    omega = split.l_embed((0, 1))
    omega2 = split.l_multiply(omega, omega)
    if split.l_power(candidate, 3) == omega2:
        candidate = split.l_inverse(candidate)
    if (
        split.l_power(candidate, 3) != omega
        or split.l_power(candidate, 9) != split.L_ONE
        or split.l_power(candidate, P**6) != candidate
    ):
        raise AssertionError("the pinned ninth root changed")
    return candidate


def l_matrix_rank(rows: Sequence[Sequence[L]]) -> int:
    work = [list(row) for row in rows]
    if not work:
        return 0
    rank = 0
    column_count = len(work[0])
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] != split.L_ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = split.l_inverse(work[rank][column])
        work[rank] = [
            split.l_multiply(value, inverse) for value in work[rank]
        ]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            if factor != split.L_ZERO:
                work[row] = [
                    split.l_subtract(
                        left,
                        split.l_multiply(factor, right),
                    )
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def f_matrix_rank(rows: Sequence[Sequence[int]]) -> int:
    work = [[value % P for value in row] for row in rows]
    if not work:
        return 0
    rank = 0
    column_count = len(work[0])
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, P)
        work[rank] = [value * inverse % P for value in work[rank]]
        for row in range(len(work)):
            if row == rank:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % P
                    for left, right in zip(work[row], work[rank])
                ]
        rank += 1
        if rank == len(work):
            break
    return rank


def solve_l_matrix(
    rows: Sequence[Sequence[L]],
    values: Sequence[L],
) -> tuple[L, ...]:
    if len(rows) != len(values) or any(len(row) != len(rows) for row in rows):
        raise ValueError("expected a square linear system")
    work = [list(row) + [value] for row, value in zip(rows, values)]
    size = len(work)
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if work[row][column] != split.L_ZERO
            ),
            None,
        )
        if pivot is None:
            raise ValueError("the row-Galois matrix is singular")
        work[column], work[pivot] = work[pivot], work[column]
        inverse = split.l_inverse(work[column][column])
        work[column] = [
            split.l_multiply(value, inverse) for value in work[column]
        ]
        for row in range(size):
            if row == column:
                continue
            factor = work[row][column]
            if factor != split.L_ZERO:
                work[row] = [
                    split.l_subtract(
                        left,
                        split.l_multiply(factor, right),
                    )
                    for left, right in zip(work[row], work[column])
                ]
    return tuple(row[-1] for row in work)


def vandermonde_row(alpha: L, frobenius_exponent: int) -> tuple[L, ...]:
    conjugate = split.l_power(alpha, P**frobenius_exponent)
    return (
        split.L_ONE,
        conjugate,
        split.l_multiply(conjugate, conjugate),
    )


def decode_trivial(origin: L, alpha: L) -> tuple[K, K, K]:
    """Recover the three k-valued augmentations from one K6 origin."""

    if split.l_power(origin, P**6) != origin:
        raise ValueError("the trivial coordinate is not in F_(167^6)")
    exponents = (0, 2, 4)
    matrix = tuple(vandermonde_row(alpha, exponent) for exponent in exponents)
    values = tuple(
        origin if exponent == 0 else split.l_power(origin, P**exponent)
        for exponent in exponents
    )
    decoded = solve_l_matrix(matrix, values)
    return tuple(split.l_constant(value) for value in decoded)  # type: ignore[return-value]


def decode_primitive_half(
    values: Sequence[L],
    alpha: L,
) -> tuple[L, L, L]:
    """Recover x_0,x_1,x_2 from factors r=0,2,4 (or y from 1,3,5)."""

    if len(values) != 3:
        raise ValueError("one primitive parity needs three factors")
    inverse_exponents = (0, 10, 8)
    aligned = tuple(
        value
        if exponent == 0
        else split.l_power(value, P**exponent)
        for value, exponent in zip(values, inverse_exponents)
    )
    matrix = tuple(
        vandermonde_row(alpha, exponent)
        for exponent in inverse_exponents
    )
    decoded = solve_l_matrix(matrix, aligned)
    if any(split.l_power(value, P**12) != value for value in decoded):
        raise AssertionError("a decoded primitive coordinate left E")
    return decoded  # type: ignore[return-value]


def decode_cone_coordinates(
    origin: L,
    primitive: Sequence[L],
    alpha: L,
) -> tuple[FiberCRT, FiberCRT, FiberCRT]:
    """Invert the row direction in one channel's seven cone coordinates."""

    if len(primitive) != 6:
        raise ValueError("expected six primitive factors")
    first = decode_trivial(origin, alpha)
    plus = decode_primitive_half(primitive[0::2], alpha)
    minus = decode_primitive_half(primitive[1::2], alpha)
    return tuple(
        (first[index], plus[index], minus[index])
        for index in range(3)
    )  # type: ignore[return-value]


def recombine_words(words: Sequence[Sequence[K]], alpha: L) -> K6Word:
    if len(words) != 3 or any(len(word) != N for word in words):
        raise ValueError("expected three length-37 Eisenstein words")
    alpha2 = split.l_multiply(alpha, alpha)
    result = []
    for column in range(N):
        result.append(
            l_sum(
                (
                    split.l_embed(words[0][column]),
                    split.l_multiply(
                        alpha,
                        split.l_embed(words[1][column]),
                    ),
                    split.l_multiply(
                        alpha2,
                        split.l_embed(words[2][column]),
                    ),
                )
            )
        )
    return tuple(result)


def cone_coordinates(word: Sequence[L]) -> tuple[L, tuple[L, ...]]:
    if len(word) != N:
        raise ValueError("expected a length-37 word")
    origin = l_sum(tuple(word))
    primitive = tuple(
        l_polynomial_evaluate(
            word,
            split.l_power(split.ZETA, P**index),
        )
        for index in range(6)
    )
    return origin, primitive


def cone_inverse_coefficient(
    origin: L,
    primitive: Sequence[L],
    column: int,
) -> L:
    """Recover one H-invariant K6 coefficient by factorwise field traces."""

    if len(primitive) != 6 or not 0 <= column < N:
        raise ValueError("expected six factors and one C_37 column")
    value = origin
    for index, coordinate in enumerate(primitive):
        gaussian_period = l_sum(
            tuple(
                split.l_power(
                    split.ZETA,
                    (-column * pow(P, index, N) * h) % N,
                )
                for h in split.H
            )
        )
        value = split.l_add(
            value,
            trace_e_to_k6(
                split.l_multiply(coordinate, gaussian_period)
            ),
        )
    value = split.l_scale(value, (pow(N, -1, P), 0))
    if split.l_power(value, P**6) != value:
        raise AssertionError("an inverse coefficient left F_(167^6)")
    return value


def origin_trace_rhs(crt: FiberCRT) -> K:
    c, x, y = crt
    primitive_trace = split.k_add(trace_e_to_k(x), trace_e_to_k(y))
    return split.k_add(c, split.k_multiply(K_THREE, primitive_trace))


def parseval_pair_rhs(left: FiberCRT, right: FiberCRT) -> K:
    c_left, x_left, y_left = left
    c_right, x_right, y_right = right
    trivial = split.k_multiply(c_left, split.k_conjugate(c_right))
    plus = split.l_multiply(
        x_left,
        split.l_power(y_right, P**5),
    )
    minus = split.l_multiply(
        y_left,
        split.l_power(x_right, P**7),
    )
    primitive = split.k_add(
        trace_e_to_k(plus),
        trace_e_to_k(minus),
    )
    return split.k_add(
        trivial,
        split.k_multiply(K_THREE, primitive),
    )


def direct_pair_inner(left: Sequence[K], right: Sequence[K]) -> K:
    if len(left) != N or len(right) != N:
        raise ValueError("expected two length-37 words")
    result = split.K_ZERO
    for first, second in zip(left, right):
        result = split.k_add(
            result,
            split.k_multiply(first, split.k_conjugate(second)),
        )
    return result


def invariant_basis() -> tuple[FiberWord, ...]:
    result = []
    origin = [split.K_ZERO] * N
    origin[0] = split.K_ONE
    result.append(tuple(origin))
    for part in split.CLASSES:
        word = [split.K_ZERO] * N
        for column in part:
            word[column] = split.K_ONE
        result.append(tuple(word))
    return tuple(result)


def verify_full_invariant_algebra() -> dict[str, object]:
    """Certify row inversion and both trace identities on a full basis."""

    alpha = ninth_root()
    trivial_matrix = tuple(
        vandermonde_row(alpha, exponent) for exponent in (0, 2, 4)
    )
    primitive_matrix = tuple(
        vandermonde_row(alpha, exponent) for exponent in (0, 10, 8)
    )
    if l_matrix_rank(trivial_matrix) != 3:
        raise AssertionError("the trivial row-Galois matrix lost rank")
    if l_matrix_rank(primitive_matrix) != 3:
        raise AssertionError("the primitive row-Galois matrix lost rank")

    basis = invariant_basis()
    basis_crt = tuple(split.crt_forward(word) for word in basis)

    coefficient_representatives = (0,) + tuple(
        part[0] for part in split.CLASSES
    )
    coefficient_trace_checks = []
    for basis_index, word in enumerate(basis):
        lifted_word = tuple(split.l_embed(value) for value in word)
        origin, primitive = cone_coordinates(lifted_word)
        for representative_index, column in enumerate(
            coefficient_representatives
        ):
            recovered = cone_inverse_coefficient(
                origin,
                primitive,
                column,
            )
            expected = split.l_embed(word[column])
            if recovered != expected:
                raise AssertionError(
                    "the factorwise coefficient trace inverse failed"
                )
            coefficient_trace_checks.append(
                (
                    basis_index,
                    representative_index,
                    compact_hash(recovered),
                )
            )

    origin_checks = []
    for word, crt in zip(basis, basis_crt):
        lhs = split.k_multiply(K_37, word[0])
        rhs = origin_trace_rhs(crt)
        if lhs != rhs:
            raise AssertionError("the inverse-DFT origin trace identity failed")
        origin_checks.append((lhs, rhs))

    pair_checks = []
    for left_index, left in enumerate(basis):
        for right_index, right in enumerate(basis):
            lhs = split.k_multiply(
                K_37,
                direct_pair_inner(left, right),
            )
            rhs = parseval_pair_rhs(
                basis_crt[left_index],
                basis_crt[right_index],
            )
            if lhs != rhs:
                raise AssertionError("the bilinear Parseval identity failed")
            pair_checks.append((left_index, right_index, lhs))

    # The recombined coordinate map is k-linear.  Checking one invariant
    # basis word in each of the three row slots therefore proves the inverse
    # on the full 39-dimensional k-space.
    inversion_checks = []
    zero_word: FiberWord = (split.K_ZERO,) * N
    for slot in range(3):
        for basis_index, word in enumerate(basis):
            words = [zero_word, zero_word, zero_word]
            words[slot] = word
            recombined = recombine_words(words, alpha)
            origin, primitive = cone_coordinates(recombined)
            decoded = decode_cone_coordinates(origin, primitive, alpha)
            expected = tuple(
                basis_crt[basis_index]
                if index == slot
                else (
                    split.K_ZERO,
                    split.L_ZERO,
                    split.L_ZERO,
                )
                for index in range(3)
            )
            if decoded != expected:
                raise AssertionError("row-Galois inversion failed on a basis")
            inversion_checks.append(
                (slot, basis_index, compact_hash(decoded))
            )

    # Prove the exact scalar cut counts by evaluating the trace formulas on
    # coordinate axes, rather than merely counting their displayed fields.
    inverse_37 = (pow(N, -1, P), 0)
    zero_crt: FiberCRT = (
        split.K_ZERO,
        split.L_ZERO,
        split.L_ZERO,
    )
    origin_axis_words = []
    for scalar in (split.K_ONE, (0, 1)):
        word = [split.K_ZERO] * N
        word[0] = scalar
        origin_axis_words.append(tuple(word))
    origin_axis_crts = tuple(
        split.crt_forward(word) for word in origin_axis_words
    )
    zero_cut_evaluations = []
    for slot in range(6):
        for scalar_index in range(2):
            crts = [zero_crt] * 6
            crts[slot] = origin_axis_crts[scalar_index]
            outputs = tuple(
                split.k_multiply(inverse_37, origin_trace_rhs(crt))
                for crt in crts
            )
            zero_cut_evaluations.append(
                tuple(
                    coordinate
                    for output in outputs
                    for coordinate in output
                )
            )
    if f_matrix_rank(zero_cut_evaluations) != 12:
        raise AssertionError("the twelve fixed-origin cuts lost rank")

    # The six individual Hermitian support forms are independent in the
    # ambient polynomial space: evaluating them on the six unit
    # origin-coordinate axes gives the identity matrix.  The cone supplies
    # their sum, leaving five displayed support-difference equations.  This
    # is an equation-count statement, not a codimension claim on the locus
    # already cut out by the cone and fixed-zero equations.
    support_form_evaluations = []
    for slot in range(6):
        crts = [zero_crt] * 6
        crts[slot] = origin_axis_crts[0]
        row = []
        for crt in crts:
            value = split.k_multiply(
                inverse_37,
                parseval_pair_rhs(crt, crt),
            )
            if value[1] != 0:
                raise AssertionError("a support-axis value left F_167")
            row.append(value[0])
        support_form_evaluations.append(tuple(row))
    support_form_evaluations = tuple(support_form_evaluations)
    if f_matrix_rank(support_form_evaluations) != 6:
        raise AssertionError("the six support forms lost rank")
    difference_rows = tuple(
        tuple(
            (int(column == row) - int(column == 5)) % P
            for column in range(6)
        )
        for row in range(5)
    )
    if split.k_matrix_rank(
        tuple(
            tuple((entry, 0) for entry in row)
            for row in difference_rows
        )
    ) != 5:
        raise AssertionError(
            "the five ambient support-difference forms lost rank"
        )

    certificate = (
        l_matrix_rank(trivial_matrix),
        l_matrix_rank(primitive_matrix),
        len(basis),
        len(origin_checks),
        len(pair_checks),
        len(inversion_checks),
        len(coefficient_trace_checks),
        12,
        6,
        5,
        compact_hash(tuple(origin_checks)),
        compact_hash(tuple(pair_checks)),
        compact_hash(tuple(inversion_checks)),
        compact_hash(tuple(coefficient_trace_checks)),
        compact_hash(tuple(zero_cut_evaluations)),
        compact_hash(support_form_evaluations),
        compact_hash(difference_rows),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_FULL_ALGEBRA_SHA256
        and certificate_hash != EXPECTED_FULL_ALGEBRA_SHA256
    ):
        raise AssertionError("the full-algebra trace certificate changed")
    return {
        "row_galois_ranks": (3, 3),
        "invariant_basis_words": len(basis),
        "origin_basis_checks": len(origin_checks),
        "bilinear_basis_pair_checks": len(pair_checks),
        "row_inversion_basis_checks": len(inversion_checks),
        "coefficient_trace_inverse_checks": len(
            coefficient_trace_checks
        ),
        "fixed_zero_column_scalar_cuts": 12,
        "profile_support_scalar_forms": 6,
        "remaining_support_equations_after_total": 5,
        "certificate_sha256": certificate_hash,
    }


def local_profile(subset: Sequence[int]) -> tuple[int, int, int]:
    return tuple(
        sum(int(row % 3 == residue) for row in subset)
        for residue in range(3)
    )  # type: ignore[return-value]


def active_fibers(profile: Sequence[int]) -> int:
    return sum(value in (1, 2) for value in profile)


def profile_from_bits(bits: Sequence[int]) -> tuple[int, int, int]:
    if len(bits) != 9 or any(value not in (0, 1) for value in bits):
        raise ValueError("expected a binary nine-row word")
    return tuple(
        sum(bits[row] for row in range(residue, 9, 3))
        for residue in range(3)
    )  # type: ignore[return-value]


def ninth_fourier_value(bits: Sequence[int], alpha: L) -> L:
    if len(bits) != 9:
        raise ValueError("expected a nine-row word")
    return l_sum(
        tuple(
            split.l_scale(split.l_power(alpha, row), (int(value), 0))
            for row, value in enumerate(bits)
            if value
        )
    )


def ninth_dft(bits: Sequence[int], alpha: L) -> tuple[L, ...]:
    if len(bits) != 9:
        raise ValueError("expected nine coefficients")
    return tuple(
        l_sum(
            tuple(
                split.l_scale(
                    split.l_power(alpha, (frequency * row) % 9),
                    (int(value) % P, 0),
                )
                for row, value in enumerate(bits)
                if value % P
            )
        )
        for frequency in range(9)
    )


def inverse_ninth_dft(spectrum: Sequence[L], alpha: L) -> tuple[L, ...]:
    if len(spectrum) != 9:
        raise ValueError("expected nine Fourier values")
    inverse_nine = (pow(9, -1, P), 0)
    return tuple(
        split.l_scale(
            l_sum(
                tuple(
                    split.l_multiply(
                        spectrum[frequency],
                        split.l_power(
                            alpha,
                            (-frequency * row) % 9,
                        ),
                    )
                    for frequency in range(9)
                )
            ),
            inverse_nine,
        )
        for row in range(9)
    )


def inverse_ninth_dft_partial(
    spectrum: Sequence[L],
    frequencies: Sequence[int],
    alpha: L,
) -> tuple[L, ...]:
    if len(spectrum) != 9 or any(
        not 0 <= frequency < 9 for frequency in frequencies
    ):
        raise ValueError("invalid partial ninth-root spectrum")
    inverse_nine = (pow(9, -1, P), 0)
    return tuple(
        split.l_scale(
            l_sum(
                tuple(
                    split.l_multiply(
                        spectrum[frequency],
                        split.l_power(
                            alpha,
                            (-frequency * row) % 9,
                        ),
                    )
                    for frequency in frequencies
                )
            ),
            inverse_nine,
        )
        for row in range(9)
    )


def ninth_spectrum_from_value(
    value: L,
    profile: Sequence[int],
    weight: int,
    alpha: L,
) -> tuple[L, ...]:
    """Complete the ninth-root spectrum from one primitive value."""

    normalized_profile = tuple(int(entry) for entry in profile)
    if (
        weight not in (3, 6)
        or len(normalized_profile) != 3
        or any(not 0 <= entry <= 3 for entry in normalized_profile)
        or sum(normalized_profile) != weight
        or split.l_power(value, P**6) != value
    ):
        raise ValueError("invalid weight, profile, or F_(167^6) value")

    spectrum: list[Optional[L]] = [None] * 9
    spectrum[0] = split.l_embed((weight, 0))
    current = value
    for power in range(6):
        frequency = pow(P, power, 9)
        if spectrum[frequency] is not None:
            raise AssertionError("the primitive ninth frequencies collided")
        spectrum[frequency] = current
        current = split.l_power(current, P)
    if current != value:
        raise AssertionError("the primitive ninth Frobenius orbit did not close")

    omega = split.l_power(alpha, 3)
    omega2 = split.l_multiply(omega, omega)
    profile_value = l_sum(
        (
            split.l_embed((normalized_profile[0], 0)),
            split.l_scale(omega, (normalized_profile[1], 0)),
            split.l_scale(omega2, (normalized_profile[2], 0)),
        )
    )
    spectrum[3] = profile_value
    spectrum[6] = split.l_power(profile_value, P)
    if any(entry is None for entry in spectrum):
        raise AssertionError("the ninth-root spectrum is incomplete")
    return tuple(spectrum)  # type: ignore[arg-type,return-value]


def decode_ninth_bits(
    value: L,
    profile: Sequence[int],
    weight: int,
    alpha: Optional[L] = None,
) -> tuple[L, ...]:
    """Return the nine inverse-DFT values for one proposed physical column."""

    root = ninth_root() if alpha is None else alpha
    return inverse_ninth_dft(
        ninth_spectrum_from_value(value, profile, weight, root),
        root,
    )


def decoded_values_are_bits(values: Sequence[L]) -> bool:
    return all(
        split.l_multiply(value, value) == value
        for value in values
    )


def verify_ninth_bit_decoder() -> dict[str, object]:
    """Prove and exhaust the lookup-free local zero/one decoder."""

    alpha = ninth_root()

    # The forward and inverse DFT maps are inverse on the full nine-dimensional
    # prime-field space, not only on physical words.
    dft_basis_checks = []
    for row in range(9):
        basis = tuple(int(index == row) for index in range(9))
        recovered = inverse_ninth_dft(ninth_dft(basis, alpha), alpha)
        expected = tuple(
            split.L_ONE if value else split.L_ZERO for value in basis
        )
        if recovered != expected:
            raise AssertionError("the complete ninth-root DFT failed to invert")
        dft_basis_checks.append(compact_hash(recovered))

    branch_certificates = []
    for weight in (3, 6):
        physical_words = tuple(
            tuple(int(row in subset) for row in range(9))
            for subset in combinations(range(9), weight)
        )
        profiles = tuple(
            (first, second, weight - first - second)
            for first in range(4)
            for second in range(4)
            if 0 <= weight - first - second <= 3
        )
        if len(profiles) != 10 or len(physical_words) != 84:
            raise AssertionError("the physical row-word census changed")

        values: dict[L, list[tuple[int, ...]]] = {}
        expected_triples = set()
        for bits in physical_words:
            value = ninth_fourier_value(bits, alpha)
            profile = profile_from_bits(bits)
            values.setdefault(value, []).append(bits)
            expected_triples.add((value, profile, bits))

        # Cache the primitive and nonprimitive inverse-DFT contributions
        # separately.  Their sum is exactly decode_ninth_bits, while avoiding
        # repeating large-field multiplications in the 820-pair iff census.
        primitive_decoded = {}
        for value in values:
            spectrum = ninth_spectrum_from_value(
                value,
                profiles[0],
                weight,
                alpha,
            )
            primitive_decoded[value] = inverse_ninth_dft_partial(
                spectrum,
                (1, 2, 4, 5, 7, 8),
                alpha,
            )
        profile_decoded = {}
        for profile in profiles:
            spectrum = ninth_spectrum_from_value(
                next(iter(values)),
                profile,
                weight,
                alpha,
            )
            profile_decoded[profile] = inverse_ninth_dft_partial(
                spectrum,
                (0, 3, 6),
                alpha,
            )
        sample_value, sample_profile, _ = next(iter(expected_triples))
        cached_sample = tuple(
            split.l_add(first, second)
            for first, second in zip(
                primitive_decoded[sample_value],
                profile_decoded[sample_profile],
            )
        )
        if cached_sample != decode_ninth_bits(
            sample_value,
            sample_profile,
            weight,
            alpha,
        ):
            raise AssertionError("the split decoder cache changed the inverse DFT")

        accepted_triples = set()
        pair_checks = 0
        for value in values:
            for profile in profiles:
                pair_checks += 1
                decoded = tuple(
                    split.l_add(first, second)
                    for first, second in zip(
                        primitive_decoded[value],
                        profile_decoded[profile],
                    )
                )
                if not decoded_values_are_bits(decoded):
                    continue
                bits = tuple(int(entry == split.L_ONE) for entry in decoded)
                if (
                    sum(bits) != weight
                    or profile_from_bits(bits) != profile
                    or ninth_fourier_value(bits, alpha) != value
                ):
                    raise AssertionError(
                        "idempotence accepted an inconsistent physical word"
                    )
                accepted_triples.add((value, profile, bits))
        if accepted_triples != expected_triples:
            raise AssertionError("the idempotence iff census changed")
        if pair_checks != 820 or len(accepted_triples) != 84:
            raise AssertionError("the cross-profile decoder census changed")

        branch_certificates.append(
            (
                weight,
                len(physical_words),
                len(values),
                pair_checks,
                len(accepted_triples),
                compact_hash(tuple(sorted(profiles))),
                compact_hash(
                    tuple(
                        sorted(
                            (
                                compact_hash(value),
                                profile,
                                bits,
                            )
                            for value, profile, bits in accepted_triples
                        )
                    )
                ),
            )
        )

    certificate = (
        len(dft_basis_checks),
        tuple(dft_basis_checks),
        tuple(branch_certificates),
        9,
        2 * 12 * 9,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_BIT_DECODER_SHA256
        and certificate_hash != EXPECTED_BIT_DECODER_SHA256
    ):
        raise AssertionError("the ninth-bit decoder certificate changed")
    return {
        "full_dft_basis_checks": len(dft_basis_checks),
        "weights_checked": (3, 6),
        "physical_words_per_weight": 84,
        "distinct_primitive_values_per_weight": 82,
        "value_profile_pairs_per_weight": 820,
        "idempotent_pairs_per_weight": 84,
        "quadratic_bit_equations_per_class": 9,
        "displayed_quadratic_equations_for_24_classes": 2 * 12 * 9,
        "certificate_sha256": certificate_hash,
    }


def elementary_symmetric_cubic(orbit: Sequence[L]) -> tuple[int, int, int]:
    if len(orbit) != 3:
        raise ValueError("expected one cubic Frobenius orbit")
    first = l_sum(tuple(orbit))
    second = l_sum(
        tuple(
            split.l_multiply(orbit[left], orbit[right])
            for left in range(3)
            for right in range(left + 1, 3)
        )
    )
    third = split.l_multiply(
        split.l_multiply(orbit[0], orbit[1]),
        orbit[2],
    )
    constants = tuple(
        split.l_constant(value)
        for value in (first, second, third)
    )
    if any(value[1] != 0 for value in constants):
        raise AssertionError("a cubic norm polynomial left F_167")
    return tuple(value[0] for value in constants)  # type: ignore[return-value]


def verify_local_alphabet() -> dict[str, object]:
    """Exhaust the 84 normalized weight-three row words."""

    alpha = ninth_root()
    roots = tuple(split.l_power(alpha, exponent) for exponent in range(9))
    word_values: dict[L, list[tuple[int, ...]]] = {}
    norms_by_active: dict[int, dict[L, int]] = {0: {}, 2: {}, 3: {}}
    trace_histogram: dict[int, int] = {}
    records = []
    for subset in combinations(range(9), 3):
        word = l_sum(tuple(roots[row] for row in subset))
        norm = split.l_multiply(word, split.l_power(word, P**3))
        if split.l_power(norm, P**3) != norm:
            raise AssertionError("a local cyclotomic norm left F_(167^3)")
        profile = local_profile(subset)
        active = active_fibers(profile)
        trace = trace_k3_to_f(norm)
        if trace != 3 * active:
            raise AssertionError("the local norm trace lost the support count")
        word_values.setdefault(word, []).append(subset)
        norms_by_active[active][norm] = (
            norms_by_active[active].get(norm, 0) + 1
        )
        trace_histogram[trace] = trace_histogram.get(trace, 0) + 1
        records.append((subset, profile, active, trace))

    # The repository's alternating normalization also uses the complements
    # of these words.  A weight-six complement negates W because the sum of
    # all nine ninth roots is zero; its norm and active-fiber branch therefore
    # remain unchanged.  Check all 84 complements explicitly.
    complement_records = []
    full_rows = set(range(9))
    for subset in combinations(range(9), 3):
        complement = tuple(sorted(full_rows.difference(subset)))
        word_three = l_sum(tuple(roots[row] for row in subset))
        word_six = l_sum(tuple(roots[row] for row in complement))
        if word_six != split.l_neg(word_three):
            raise AssertionError("a weight-six complement lost its sign")
        norm_three = split.l_multiply(
            word_three,
            split.l_power(word_three, P**3),
        )
        norm_six = split.l_multiply(
            word_six,
            split.l_power(word_six, P**3),
        )
        profile_three = local_profile(subset)
        profile_six = local_profile(complement)
        if profile_six != tuple(3 - value for value in profile_three):
            raise AssertionError("a complemented residue profile changed")
        if (
            norm_six != norm_three
            or active_fibers(profile_six) != active_fibers(profile_three)
            or trace_k3_to_f(norm_six)
            != 3 * active_fibers(profile_six)
        ):
            raise AssertionError("a weight-six norm branch changed")
        complement_records.append(
            (
                subset,
                complement,
                profile_three,
                profile_six,
                active_fibers(profile_six),
                trace_k3_to_f(norm_six),
            )
        )

    if len(word_values) != 82:
        raise AssertionError("the 84 row words no longer give 82 values")
    collision_histogram: dict[int, int] = {}
    for subsets in word_values.values():
        collision_histogram[len(subsets)] = (
            collision_histogram.get(len(subsets), 0) + 1
        )
    expected_norm_histograms = {
        0: (3,),
        2: (18, 18, 18),
        3: (9, 9, 9),
    }
    actual_norm_histograms = {
        active: tuple(sorted(values.values()))
        for active, values in norms_by_active.items()
    }
    if actual_norm_histograms != expected_norm_histograms:
        raise AssertionError("the seven-value local norm alphabet changed")
    if trace_histogram != {0: 3, 6: 54, 9: 27}:
        raise AssertionError("the local norm-trace histogram changed")
    if collision_histogram != {1: 81, 3: 1}:
        raise AssertionError("the local row-word collision histogram changed")

    polynomials = {}
    for active in (2, 3):
        seed = next(iter(norms_by_active[active]))
        orbit = tuple(split.l_power(seed, P**power) for power in range(3))
        if set(orbit) != set(norms_by_active[active]):
            raise AssertionError("a local norm set is not one Frobenius orbit")
        elementary = elementary_symmetric_cubic(orbit)
        polynomials[active] = (
            1,
            (-elementary[0]) % P,
            elementary[1],
            (-elementary[2]) % P,
        )
    if polynomials != {
        2: (1, 161, 9, 164),
        3: (1, 158, 18, 158),
    }:
        raise AssertionError("the two cubic local norm polynomials changed")

    certificate = (
        len(records),
        len(word_values),
        tuple(sorted(collision_histogram.items())),
        tuple(
            (active, tuple(sorted(histogram.items(), key=str)))
            for active, histogram in sorted(norms_by_active.items())
        ),
        tuple(sorted(trace_histogram.items())),
        tuple(sorted(polynomials.items())),
        compact_hash(tuple(records)),
        compact_hash(tuple(complement_records)),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_LOCAL_ALPHABET_SHA256
        and certificate_hash != EXPECTED_LOCAL_ALPHABET_SHA256
    ):
        raise AssertionError("the local-alphabet trace certificate changed")
    return {
        "row_words": len(records),
        "weight_six_complements": len(complement_records),
        "physical_weights_checked": (3, 6),
        "distinct_row_values": len(word_values),
        "distinct_norm_values": sum(
            len(values) for values in norms_by_active.values()
        ),
        "row_value_collision_histogram": collision_histogram,
        "norm_value_multiplicity_by_active_fibers": actual_norm_histograms,
        "norm_trace_histogram": trace_histogram,
        "norm_cubic_polynomials_descending_mod_167": polynomials,
        "certificate_sha256": certificate_hash,
    }


def support_167_frame() -> tuple[
    tuple[FiberWord, FiberWord, FiberWord],
    tuple[FiberWord, FiberWord, FiberWord],
]:
    """Build a deterministic physical frame with profile support 167."""

    mutable = [
        [[split.K_ZERO for _ in range(N)] for _ in range(3)]
        for _ in range(2)
    ]
    zero_words = (ZERO_A_PLUS, ZERO_B_PLUS)
    for channel in range(2):
        for residue in range(3):
            phase = fiber_phase(zero_words[channel], residue)
            mutable[channel][residue][0] = (
                phase[0] % P,
                phase[1] % P,
            )

    for channel in range(2):
        for class_index, part in enumerate(split.CLASSES):
            active = channel == 0 or class_index < 6
            if active:
                subset = tuple(
                    residue
                    + 3 * ((2 * class_index + channel + residue) % 3)
                    for residue in range(3)
                )
            else:
                residue = (class_index + channel) % 3
                subset = tuple(residue + 3 * quotient for quotient in range(3))
            word = tuple(int(row in subset) for row in range(9))
            for residue in range(3):
                phase = fiber_phase(word, residue)
                value = phase[0] % P, phase[1] % P
                for column in part:
                    mutable[channel][residue][column] = value

    return tuple(
        tuple(tuple(word) for word in channel)
        for channel in mutable
    )  # type: ignore[return-value]


def fixed_zero_values() -> tuple[K, ...]:
    return tuple(
        (
            fiber_phase(word, residue)[0] % P,
            fiber_phase(word, residue)[1] % P,
        )
        for word in (ZERO_A_PLUS, ZERO_B_PLUS)
        for residue in range(3)
    )


def verify_physical_fixture() -> dict[str, object]:
    """Check all eighteen trace cuts on one support-167 profile frame."""

    alpha = ninth_root()
    frame = support_167_frame()
    expected_zero = fixed_zero_values()
    expected_support = tuple(
        sum(value != split.K_ZERO for value in word)
        for channel in frame
        for word in channel
    )
    if expected_support != (37, 37, 37, 18, 19, 19):
        raise AssertionError("the pinned profile support vector changed")
    if sum(expected_support) != 167:
        raise AssertionError("the pinned physical frame lost support 167")

    decoded_all = []
    zero_residuals = []
    support_residuals = []
    for channel in range(2):
        recombined = recombine_words(frame[channel], alpha)
        origin, primitive = cone_coordinates(recombined)
        decoded = decode_cone_coordinates(origin, primitive, alpha)
        direct = tuple(split.crt_forward(word) for word in frame[channel])
        if decoded != direct:
            raise AssertionError("the physical fixture failed row inversion")
        decoded_all.extend(decoded)

    for index, (word, crt) in enumerate(
        zip(
            tuple(word for channel in frame for word in channel),
            decoded_all,
        )
    ):
        zero_lhs = split.k_multiply(K_37, expected_zero[index])
        zero_rhs = origin_trace_rhs(crt)
        if zero_lhs != zero_rhs:
            raise AssertionError("the fixed-zero trace cut rejected a fixture")
        zero_residuals.append(split.k_sub(zero_rhs, zero_lhs))

        support_lhs = split.k_multiply(
            K_37,
            (expected_support[index], 0),
        )
        support_rhs = parseval_pair_rhs(crt, crt)
        if support_lhs != support_rhs:
            raise AssertionError("the profile support cut rejected a fixture")
        support_residuals.append(split.k_sub(support_rhs, support_lhs))

        if direct_pair_inner(word, word) != (expected_support[index], 0):
            raise AssertionError("a unit/zero word has the wrong direct support")

    certificate = (
        expected_zero,
        expected_support,
        tuple(zero_residuals),
        tuple(support_residuals),
        compact_hash(tuple(decoded_all)),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_PHYSICAL_FIXTURE_SHA256
        and certificate_hash != EXPECTED_PHYSICAL_FIXTURE_SHA256
    ):
        raise AssertionError("the physical trace fixture changed")
    return {
        "fixed_zero_values": expected_zero,
        "profile_support_vector": expected_support,
        "total_support": sum(expected_support),
        "zero_trace_cuts_passed": len(zero_residuals),
        "support_parseval_cuts_passed": len(support_residuals),
        "certificate_sha256": certificate_hash,
    }


def k6_norm_minus_one(alpha: L) -> L:
    """Find a deterministic R in F_(167^6) with R R^(167^3)=-1."""

    for scalar in range(P):
        candidate = split.l_add(alpha, split.l_embed((scalar, 0)))
        if candidate == split.L_ZERO:
            continue
        ratio = split.l_power(candidate, (P**3 - 1) // 2)
        if (
            split.l_power(ratio, P**6) == ratio
            and split.l_multiply(
                ratio,
                split.l_power(ratio, P**3),
            )
            == L_MINUS_ONE
        ):
            return ratio
    raise AssertionError("failed to find the pinned K6 norm-minus-one ratio")


def verify_negative_cone_fixture() -> dict[str, object]:
    """Show the full modular norm cone does not imply profile supports."""

    alpha = ninth_root()
    ratio = k6_norm_minus_one(alpha)
    word_a = (split.L_ONE,) + (split.L_ZERO,) * (N - 1)
    word_b = (ratio,) + (split.L_ZERO,) * (N - 1)
    origins = []
    primitives = []
    decoded = []
    for word in (word_a, word_b):
        origin, primitive = cone_coordinates(word)
        origins.append(origin)
        primitives.append(primitive)
        decoded.extend(decode_cone_coordinates(origin, primitive, alpha))

    # The two group words satisfy W_A W_A^* + W_B W_B^*=0 coefficientwise.
    direct_norm = tuple(
        split.l_add(
            split.l_multiply(
                word_a[column],
                split.l_power(word_a[column], P**3),
            ),
            split.l_multiply(
                word_b[column],
                split.l_power(word_b[column], P**3),
            ),
        )
        for column in range(N)
    )
    if any(value != split.L_ZERO for value in direct_norm):
        raise AssertionError("the negative fixture left the modular norm cone")

    support_forms = tuple(
        parseval_pair_rhs(crt, crt)[0] * pow(N, -1, P) % P
        for crt in decoded
    )
    # parseval_pair_rhs is fixed by coefficient conjugation and must be prime
    # field-valued before division by 37.
    if any(parseval_pair_rhs(crt, crt)[1] != 0 for crt in decoded):
        raise AssertionError("a support form left the prime field")
    if sum(support_forms) % P != 0:
        raise AssertionError("the full cone did not supply total support zero")

    target_support = (37, 37, 37, 18, 19, 19)
    mismatches = tuple(
        index
        for index, (actual, target) in enumerate(
            zip(support_forms, target_support)
        )
        if actual != target
    )
    if not mismatches:
        raise AssertionError("the negative cone fixture passed every profile cut")

    certificate = (
        compact_hash(ratio),
        compact_hash(tuple(origins)),
        compact_hash(tuple(primitives)),
        support_forms,
        target_support,
        mismatches,
        compact_hash(direct_norm),
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_NEGATIVE_CONE_SHA256
        and certificate_hash != EXPECTED_NEGATIVE_CONE_SHA256
    ):
        raise AssertionError("the negative-cone trace fixture changed")
    return {
        "nonzero_full_norm_cone_fixture": True,
        "total_support_form_mod_167": sum(support_forms) % P,
        "individual_support_forms": support_forms,
        "profile_target_supports": target_support,
        "failed_profile_support_indices": mismatches,
        "certificate_sha256": certificate_hash,
    }


def verify() -> dict[str, object]:
    local = verify_local_alphabet()
    decoder = verify_ninth_bit_decoder()
    full = verify_full_invariant_algebra()
    physical = verify_physical_fixture()
    negative = verify_negative_cone_fixture()
    composite = compact_hash(
        (
            local["certificate_sha256"],
            decoder["certificate_sha256"],
            full["certificate_sha256"],
            physical["certificate_sha256"],
            negative["certificate_sha256"],
        )
    )
    if EXPECTED_COMPOSITE_SHA256 and composite != EXPECTED_COMPOSITE_SHA256:
        raise AssertionError("the composite phase-trace certificate changed")
    return {
        "local_alphabet": local,
        "ninth_bit_decoder": decoder,
        "full_invariant_algebra": full,
        "physical_support_167_fixture": physical,
        "negative_cone_fixture": negative,
        "composite_sha256": composite,
        "status": (
            "exact factorwise trace/profile sieve verified; no LP(333) "
            "or H(668) constructed"
        ),
    }


def main() -> None:
    result = verify()
    full = result["full_invariant_algebra"]
    for section in (
        "local_alphabet",
        "ninth_bit_decoder",
        "full_invariant_algebra",
        "physical_support_167_fixture",
        "negative_cone_fixture",
    ):
        print(
            f"{section}_sha256="
            f"{result[section]['certificate_sha256']}"
        )
    print(
        "fixed_zero_column_scalar_cuts="
        f"{full['fixed_zero_column_scalar_cuts']}"
    )
    print(
        "remaining_profile_support_equations="
        f"{full['remaining_support_equations_after_total']}"
    )
    print(f"composite_sha256={result['composite_sha256']}")
    print("PASS: exact row-Galois trace and Parseval sieve verified")
    print("STATUS: new necessary constraints; no LP(333) or H(668)")


if __name__ == "__main__":
    main()
