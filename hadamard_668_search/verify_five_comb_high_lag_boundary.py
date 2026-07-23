#!/usr/bin/env python3
"""Dependency-free generator and verifier for the five-comb high-lag table.

The unrestricted projective common-type packing has twelve normalized
projective parameters.  After lags 83 and 82, its six outer hole signs are
one balanced projective direction, its orientation, and one long-tail sign.
The latter two signs gauge out of lags 81 through 78.  This module generates
the resulting exact allowed table and its two useful projections.

Everything here uses the Python standard library.  The public generators
are suitable for import by a CP model.  A full row consists of twelve
Boolean projective parameters, ``e_index`` in ``0..2``, and seven Boolean
negativity indicators, with ``1`` denoting a negative scalar sign.
The independently verified full physical hole fiber fixes
``e_direction=2``; ``e2_boundary_rows()`` removes that now-constant column.
"""

from __future__ import annotations

from functools import lru_cache
import hashlib
from itertools import combinations_with_replacement, product
import random
from typing import Iterable, Sequence


PARAMETER_NAMES = (
    "alpha",
    "beta",
    "u5",
    "u6",
    "u7",
    "y1",
    "y2",
    "y3",
    "y4",
    "y5",
    "y6",
    "y7",
)
GAUGE_SIGN_NAMES = (
    "sigma1_prime",
    "sigma2_prime",
    "sigma3_prime",
    "tau4_prime",
    "tau5_prime",
    "tau6_prime",
    "tau7_prime",
)

LENGTHS = (84, 84, 83, 83)
SHIFTS = (0, 1, 2, 3, 20, 21, 22, 23)
PARAMETER_COUNT = 12
GAUGE_SIGN_COUNT = 7
BOUNDARY_ROW_WIDTH = PARAMETER_COUNT + 1 + GAUGE_SIGN_COUNT
E2_BOUNDARY_ROW_WIDTH = PARAMETER_COUNT + GAUGE_SIGN_COUNT
BOUNDARY_COLUMN_NAMES = PARAMETER_NAMES + ("e_index",) + GAUGE_SIGN_NAMES
BOUNDARY_COLUMN_DOMAINS = (
    *((0, 1),) * PARAMETER_COUNT,
    (0, 1, 2),
    *((0, 1),) * GAUGE_SIGN_COUNT,
)
PARAMETER_E_COLUMN_NAMES = PARAMETER_NAMES + ("e_index",)
PARAMETER_COLUMN_NAMES = PARAMETER_NAMES
E2_BOUNDARY_COLUMN_NAMES = PARAMETER_NAMES + GAUGE_SIGN_NAMES
E2_BOUNDARY_COLUMN_DOMAINS = (
    *((0, 1),) * PARAMETER_COUNT,
    *((0, 1),) * GAUGE_SIGN_COUNT,
)
E2_PARAMETER_COLUMN_NAMES = PARAMETER_NAMES
PHYSICAL_E_DIRECTION = 2
PHYSICAL_E_INDEX = PHYSICAL_E_DIRECTION - 1

EXPECTED_FULL_ROW_COUNT = 33_718
EXPECTED_PARAMETER_E_ROW_COUNT = 7_454
EXPECTED_PARAMETER_ROW_COUNT = 2_967
EXPECTED_E2_FULL_ROW_COUNT = 10_934
EXPECTED_E2_PARAMETER_ROW_COUNT = 2_434
EXPECTED_FULL_SHA256 = (
    "4297e9d0d543ab8264eac5296b883554a97a8e1ad7c2b9bf8ac03a6bee8dd697"
)
EXPECTED_PARAMETER_E_SHA256 = (
    "d7305acac88b62f35c6031d237f53656aafbd13712fcdaa0d192c5e7b4bd0b73"
)
EXPECTED_PARAMETER_SHA256 = (
    "d49447cb39472e6d894a57a4c842e1eab8df6a99183ad8259dc62ae27f5c93fb"
)
EXPECTED_E2_FULL_SHA256 = (
    "441c25786c4a0bc56f9e86c84bf9c8c8252595a9f75298aad960c31320aeb6b4"
)
EXPECTED_E2_PARAMETER_SHA256 = (
    "85972db2c71b3e1415705017b0f3f1e57aab3f7cba880104c8f60d83c687d2c0"
)


H4 = (
    (1, 1, 1, 1),
    (1, -1, 1, -1),
    (1, 1, -1, -1),
    (1, -1, -1, 1),
)
MUB_TWIST = (1, 1, 1, -1)
VECTORS = tuple(
    tuple(
        H4[row][column] * (MUB_TWIST[row] if basis else 1)
        for row in range(4)
    )
    for basis in range(2)
    for column in range(4)
)
PHI = tuple(sum(vector) for vector in VECTORS)


def word_signature(word: Sequence[int]) -> tuple[int, ...]:
    """Return the four positive aperiodic correlations of a length-five word."""

    return tuple(
        sum(word[index] * word[index + lag] for index in range(5 - lag))
        for lag in range(1, 5)
    )


WORDS = tuple((1,) + tail for tail in product((-1, 1), repeat=4))
WORD_SIGNATURES = tuple(word_signature(word) for word in WORDS)
QUARTETS = tuple(
    indices
    for indices in combinations_with_replacement(range(len(WORDS)), 4)
    if all(
        sum(WORD_SIGNATURES[index][lag] for index in indices) == 0
        for lag in range(4)
    )
)


def _require_bits(values: Sequence[int], size: int, label: str) -> tuple[int, ...]:
    result = tuple(values)
    if len(result) != size or any(value not in (0, 1) for value in result):
        raise ValueError(f"{label} must contain exactly {size} Boolean values")
    return result


def _require_signs(
    values: Sequence[int], size: int, label: str
) -> tuple[int, ...]:
    result = tuple(values)
    if len(result) != size or any(value not in (-1, 1) for value in result):
        raise ValueError(f"{label} must contain exactly {size} signs")
    return result


def normalized_projective_labels(
    parameters: Sequence[int],
) -> tuple[int, ...]:
    """Evaluate the twelve-bit normalized projective parametrization."""

    (
        alpha,
        beta,
        u5,
        u6,
        u7,
        y1,
        y2,
        y3,
        y4,
        y5,
        y6,
        y7,
    ) = _require_bits(parameters, PARAMETER_COUNT, "parameters")
    low = (0, 0, beta, alpha, 0, 0, alpha, beta)
    middle = (0, y1, y2, y3, y4, y5, y6, y7)
    high = (
        0,
        beta ^ u7,
        alpha ^ beta ^ u6,
        alpha ^ u5,
        0,
        u5,
        u6,
        u7,
    )
    return tuple(
        low[slot] + 2 * middle[slot] + 4 * high[slot]
        for slot in range(8)
    )


def projective_character(label: int) -> int:
    """Return the four-row character sum ``Phi(label)``."""

    if not 0 <= label < 8:
        raise ValueError("a projective label must lie in 0..7")
    return PHI[label]


def signs_from_negative_bits(bits: Sequence[int]) -> tuple[int, ...]:
    """Decode Boolean negativity indicators as ``+1,-1`` signs."""

    return tuple(
        -1 if bit else 1
        for bit in _require_bits(bits, GAUGE_SIGN_COUNT, "sign bits")
    )


def negative_bits_from_signs(signs: Sequence[int]) -> tuple[int, ...]:
    """Encode ``+1,-1`` signs as Boolean negativity indicators."""

    return tuple(
        int(sign < 0)
        for sign in _require_signs(signs, GAUGE_SIGN_COUNT, "signs")
    )


def decode_boundary_row(
    row: Sequence[int],
) -> tuple[tuple[int, ...], int, tuple[int, ...]]:
    """Decode one CP row as ``(parameters, e_direction, gauge_signs)``."""

    values = tuple(row)
    if len(values) != BOUNDARY_ROW_WIDTH:
        raise ValueError(
            f"a boundary row must have width {BOUNDARY_ROW_WIDTH}"
        )
    parameters = _require_bits(
        values[:PARAMETER_COUNT], PARAMETER_COUNT, "row parameters"
    )
    e_index = values[PARAMETER_COUNT]
    if type(e_index) is not int or e_index not in (0, 1, 2):
        raise ValueError("row e_index must lie in 0..2")
    signs = signs_from_negative_bits(values[PARAMETER_COUNT + 1 :])
    return parameters, e_index + 1, signs


def decode_e2_boundary_row(
    row: Sequence[int],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Decode one fixed-physical-fiber row as parameters and gauge signs."""

    values = tuple(row)
    if len(values) != E2_BOUNDARY_ROW_WIDTH:
        raise ValueError(
            f"an e=2 boundary row must have width {E2_BOUNDARY_ROW_WIDTH}"
        )
    parameters = _require_bits(
        values[:PARAMETER_COUNT], PARAMETER_COUNT, "row parameters"
    )
    signs = signs_from_negative_bits(values[PARAMETER_COUNT:])
    return parameters, signs


def gauge_normalize_signs(
    sigma: Sequence[int],
    tau: Sequence[int],
    eta: int,
    tail_sign: int,
) -> tuple[int, ...]:
    """Remove the two outer-hole signs from lags 81 through 78."""

    sigma_values = _require_signs(sigma, 3, "sigma")
    tau_values = _require_signs(tau, 4, "tau")
    if eta not in (-1, 1) or tail_sign not in (-1, 1):
        raise ValueError("eta and tail_sign must be signs")
    sigma1, sigma2, sigma3 = sigma_values
    tau4, tau5, tau6, tau7 = tau_values
    return (
        sigma1 * eta * tail_sign,
        sigma2,
        sigma3 * eta * tail_sign,
        tau4 * eta,
        tau5 * tail_sign,
        tau6 * eta,
        tau7 * tail_sign,
    )


def boundary_equations(
    parameters: Sequence[int],
    e_direction: int,
    gauge_signs: Sequence[int],
) -> tuple[int, int, int, int]:
    """Return ``(R81/f, R80/eta, R79/f, R78/eta)`` exactly."""

    parameter_bits = _require_bits(parameters, PARAMETER_COUNT, "parameters")
    if e_direction not in (1, 2, 3):
        raise ValueError("the balanced direction must be 1, 2, or 3")
    labels = normalized_projective_labels(parameter_bits)
    alpha, beta = parameter_bits[:2]
    (
        sigma1,
        sigma2,
        sigma3,
        tau4,
        tau5,
        tau6,
        tau7,
    ) = _require_signs(gauge_signs, GAUGE_SIGN_COUNT, "gauge_signs")

    return (
        tau7 * PHI[labels[7]]
        + sigma1 * PHI[labels[1] ^ e_direction]
        + 2 * beta * sigma2,
        tau6 * PHI[labels[6]]
        + sigma1 * tau7 * PHI[labels[1] ^ labels[7]]
        + sigma2 * PHI[labels[2] ^ e_direction]
        + 2 * alpha * sigma3,
        tau5 * PHI[labels[5]]
        + sigma1 * tau6 * PHI[labels[1] ^ labels[6]]
        + sigma2 * tau7 * PHI[labels[2] ^ labels[7]]
        + sigma3 * PHI[labels[3] ^ e_direction],
        tau4 * PHI[labels[4]]
        + sigma1 * tau5 * PHI[labels[1] ^ labels[5]]
        + sigma2 * tau6 * PHI[labels[2] ^ labels[6]]
        + sigma3 * tau7 * PHI[labels[3] ^ labels[7]],
    )


@lru_cache(maxsize=1)
def boundary_rows() -> tuple[tuple[int, ...], ...]:
    """Generate the 33,718 CP-ready rows for lags 81 through 78."""

    result = []
    for parameters in product((0, 1), repeat=PARAMETER_COUNT):
        for e_index in range(3):
            e_direction = e_index + 1
            for sign_bits in product((0, 1), repeat=GAUGE_SIGN_COUNT):
                signs = signs_from_negative_bits(sign_bits)
                if boundary_equations(parameters, e_direction, signs) == (
                    0,
                    0,
                    0,
                    0,
                ):
                    result.append(parameters + (e_index,) + sign_bits)
    rows = tuple(result)
    if rows != tuple(sorted(rows)):
        raise AssertionError("boundary rows are not canonically ordered")
    return rows


@lru_cache(maxsize=1)
def parameter_e_rows() -> tuple[tuple[int, ...], ...]:
    """Project the full table onto the twelve parameters and ``e-1``."""

    return tuple(sorted({row[: PARAMETER_COUNT + 1] for row in boundary_rows()}))


@lru_cache(maxsize=1)
def parameter_rows() -> tuple[tuple[int, ...], ...]:
    """Project the full table onto the twelve projective parameters."""

    return tuple(sorted({row[:PARAMETER_COUNT] for row in boundary_rows()}))


@lru_cache(maxsize=1)
def e2_boundary_rows() -> tuple[tuple[int, ...], ...]:
    """Return the physical-fiber table with fixed ``e_index=1`` removed."""

    return tuple(
        row[:PARAMETER_COUNT] + row[PARAMETER_COUNT + 1 :]
        for row in boundary_rows()
        if row[PARAMETER_COUNT] == PHYSICAL_E_INDEX
    )


@lru_cache(maxsize=1)
def e2_parameter_rows() -> tuple[tuple[int, ...], ...]:
    """Project the fixed physical-fiber table onto its twelve parameters."""

    return tuple(
        sorted({row[:PARAMETER_COUNT] for row in e2_boundary_rows()})
    )


def canonical_rows_sha256(
    rows: Iterable[Sequence[int]],
    expected_width: int | None = None,
) -> str:
    """Hash uniformly sized, sorted byte rows.

    The unframed byte serialization intentionally preserves the three
    published digests.  A digest is therefore an attestation only together
    with its exported schema width and expected row count; ``verify()``
    checks all three.
    """

    canonical = tuple(sorted(tuple(row) for row in rows))
    if not canonical:
        raise ValueError("at least one canonical row is required")
    width = len(canonical[0])
    if expected_width is not None and width != expected_width:
        raise ValueError(
            f"canonical row width {width} differs from {expected_width}"
        )
    if any(len(row) != width for row in canonical):
        raise ValueError("canonical rows must have one uniform width")
    if any(
        any(type(value) is not int or not 0 <= value <= 255 for value in row)
        for row in canonical
    ):
        raise ValueError("canonical rows must consist of bytes")
    return hashlib.sha256(
        b"".join(bytes(row) for row in canonical)
    ).hexdigest()


def _validate_type_assignment(types: Sequence[int]) -> tuple[int, ...]:
    result = tuple(types)
    if len(result) != 8 or sorted(result) != list(range(8)):
        raise ValueError("types must be a permutation of 0..7")
    return result


def _word_for_type(quartet: Sequence[int], carrier_type: int) -> tuple[int, ...]:
    return WORDS[quartet[carrier_type // 2]]


def _polarization(carrier_type: int) -> int:
    return -1 if carrier_type % 2 == 0 else 1


def high_lag_formula(
    lag: int,
    quartet: Sequence[int],
    parameters: Sequence[int],
    types: Sequence[int],
    orientations: Sequence[int],
    e_direction: int,
    eta: int,
    tail_sign: int,
) -> int:
    """Evaluate the closed formula for one lag from 64 through 81."""

    if not 64 <= lag <= 81:
        raise ValueError("the closed high-lag formula covers lags 64..81")
    quartet_indices = tuple(quartet)
    if len(quartet_indices) != 4 or any(
        not 0 <= index < len(WORDS) for index in quartet_indices
    ):
        raise ValueError("quartet must contain four normalized-word indices")
    type_values = _validate_type_assignment(types)
    orientation_values = _require_signs(orientations, 8, "orientations")
    if orientation_values[0] != 1:
        raise ValueError("slot-zero orientation must be normalized positive")
    if e_direction not in (1, 2, 3):
        raise ValueError("the balanced direction must be 1, 2, or 3")
    if eta not in (-1, 1) or tail_sign not in (-1, 1):
        raise ValueError("eta and tail_sign must be signs")

    labels = normalized_projective_labels(parameters)

    def first(slot: int, tooth: int) -> int:
        carrier_type = type_values[slot]
        return (
            orientation_values[slot]
            * _word_for_type(quartet_indices, carrier_type)[tooth]
        )

    def second(slot: int, tooth: int) -> int:
        carrier_type = type_values[slot]
        return first(slot, tooth) * _polarization(carrier_type)

    d = 82 - lag
    result = 0
    for position in range(d):
        prefix_slot = position % 4
        prefix_tooth = position // 4
        suffix_position = lag + position
        suffix_residue = (suffix_position - 62) % 4
        suffix_slot = 4 + suffix_residue
        suffix_tooth = (suffix_position - 62 - suffix_residue) // 4
        result += (
            first(prefix_slot, prefix_tooth)
            * second(suffix_slot, suffix_tooth)
            * PHI[labels[prefix_slot] ^ labels[suffix_slot]]
        )

    e_slot = d % 4
    e_tooth = d // 4
    result += (
        first(e_slot, e_tooth)
        * eta
        * PHI[labels[e_slot] ^ e_direction]
    )

    tail_slot = (d + 1) % 4
    tail_tooth = (d + 1) // 4
    result += (
        2
        * tail_sign
        * first(tail_slot, tail_tooth)
        * (labels[tail_slot] & 1)
    )
    return result


def reconstruct_sequences(
    quartet: Sequence[int],
    parameters: Sequence[int],
    types: Sequence[int],
    orientations: Sequence[int],
    e_direction: int,
    eta: int,
    tail_sign: int,
    inner_holes: Sequence[Sequence[int]] | None = None,
) -> tuple[tuple[int, ...], ...]:
    """Reconstruct all four binary target sequences from packed components."""

    quartet_indices = tuple(quartet)
    type_values = _validate_type_assignment(types)
    orientation_values = _require_signs(orientations, 8, "orientations")
    labels = normalized_projective_labels(parameters)
    if orientation_values[0] != 1:
        raise ValueError("slot-zero orientation must be normalized positive")
    if e_direction not in (1, 2, 3):
        raise ValueError("the balanced direction must be 1, 2, or 3")
    if eta not in (-1, 1) or tail_sign not in (-1, 1):
        raise ValueError("eta and tail_sign must be signs")
    if inner_holes is None:
        inner_hole_values = ((1, 1),) * 4
    else:
        inner_hole_values = tuple(
            _require_signs(values, 2, "one row's inner holes")
            for values in inner_holes
        )
        if len(inner_hole_values) != 4:
            raise ValueError("inner_holes must have four rows")

    sequences = [[0] * length for length in LENGTHS]
    for slot, carrier_type in enumerate(type_values):
        word = _word_for_type(quartet_indices, carrier_type)
        epsilon = _polarization(carrier_type)
        for tooth, word_sign in enumerate(word):
            for row in range(4):
                value = (
                    orientation_values[slot]
                    * VECTORS[labels[slot]][row]
                    * word_sign
                )
                first_position = SHIFTS[slot] + 4 * tooth
                second_position = first_position + 42
                if (
                    sequences[row][first_position]
                    or sequences[row][second_position]
                ):
                    raise AssertionError("carrier supports overlap")
                sequences[row][first_position] = value
                sequences[row][second_position] = epsilon * value

    e_vector = tuple(eta * value for value in VECTORS[e_direction])
    for row in range(4):
        sequences[row][40], sequences[row][41] = inner_hole_values[row]
        sequences[row][82] = e_vector[row]
    sequences[0][83] = tail_sign
    sequences[1][83] = -tail_sign

    result = tuple(tuple(sequence) for sequence in sequences)
    if any(value not in (-1, 1) for sequence in result for value in sequence):
        raise AssertionError("the reconstructed packing is not binary")
    return result


def direct_correlation(sequences: Sequence[Sequence[int]], lag: int) -> int:
    """Return the summed aperiodic correlation at one positive lag."""

    if lag <= 0:
        raise ValueError("a positive lag is required")
    return sum(
        sum(
            sequence[index] * sequence[index + lag]
            for index in range(len(sequence) - lag)
        )
        for sequence in sequences
        if lag < len(sequence)
    )


def _orientations_realizing_row(
    row: Sequence[int],
    quartet: Sequence[int],
    types: Sequence[int],
) -> tuple[int, ...]:
    """Choose orientations realizing a table row with ``eta=f=+1``."""

    _parameters, _e_direction, gauge_signs = decode_boundary_row(row)
    sigma1, sigma2, sigma3, tau4, tau5, tau6, tau7 = gauge_signs
    result = [1, sigma1, sigma2, sigma3]
    for slot, tau in zip(range(4, 8), (tau4, tau5, tau6, tau7)):
        carrier_type = types[slot]
        rho = (
            _polarization(carrier_type)
            * _word_for_type(quartet, carrier_type)[4]
        )
        result.append(tau * rho)
    return tuple(result)


def validate_every_boundary_row_directly() -> int:
    """Replay every table row through actual sequences at lags 81..78."""

    quartet = QUARTETS[0]
    types = tuple(range(8))
    checks = 0
    for row in boundary_rows():
        parameters = row[:PARAMETER_COUNT]
        e_direction = row[PARAMETER_COUNT] + 1
        orientations = _orientations_realizing_row(row, quartet, types)
        sequences = reconstruct_sequences(
            quartet,
            parameters,
            types,
            orientations,
            e_direction,
            1,
            1,
        )
        for lag in range(78, 82):
            if direct_correlation(sequences, lag) != 0:
                raise AssertionError(
                    f"a boundary row failed direct reconstruction at lag {lag}"
                )
            checks += 1
    return checks


def validate_general_formula(
    samples_per_quartet: int = 16,
    seed: int = 668,
) -> tuple[int, int, int]:
    """Compare the formula with reconstructed correlations for all quartets."""

    if samples_per_quartet < 1:
        raise ValueError("samples_per_quartet must be positive")
    generator = random.Random(seed)
    formula_checks = 0
    gauge_checks = 0
    normalized_tail_checks = 0
    for quartet in QUARTETS:
        for _sample in range(samples_per_quartet):
            parameters = tuple(
                generator.randrange(2) for _ in range(PARAMETER_COUNT)
            )
            types_list = list(range(8))
            generator.shuffle(types_list)
            types = tuple(types_list)
            orientations = (1,) + tuple(
                generator.choice((-1, 1)) for _ in range(7)
            )
            e_direction = generator.choice((1, 2, 3))
            eta = generator.choice((-1, 1))
            tail_sign = generator.choice((-1, 1))
            inner_holes = tuple(
                tuple(generator.choice((-1, 1)) for _ in range(2))
                for _row in range(4)
            )
            sequences = reconstruct_sequences(
                quartet,
                parameters,
                types,
                orientations,
                e_direction,
                eta,
                tail_sign,
                inner_holes,
            )

            for lag in range(64, 82):
                expected = high_lag_formula(
                    lag,
                    quartet,
                    parameters,
                    types,
                    orientations,
                    e_direction,
                    eta,
                    tail_sign,
                )
                actual = direct_correlation(sequences, lag)
                if actual != expected:
                    raise AssertionError(
                        f"closed formula failed at lag {lag}: "
                        f"{actual} != {expected}"
                    )
                formula_checks += 1

            for lag in (82, 83):
                if direct_correlation(sequences, lag) != 0:
                    raise AssertionError(
                        f"normalized outer holes failed at lag {lag}"
                    )
                normalized_tail_checks += 1

            sigma = orientations[1:4]
            tau = tuple(
                orientations[slot]
                * _polarization(types[slot])
                * _word_for_type(quartet, types[slot])[4]
                for slot in range(4, 8)
            )
            gauge_signs = gauge_normalize_signs(
                sigma, tau, eta, tail_sign
            )
            normalized_equations = boundary_equations(
                parameters, e_direction, gauge_signs
            )
            actual_equations = tuple(
                direct_correlation(sequences, lag)
                for lag in (81, 80, 79, 78)
            )
            expected_equations = (
                tail_sign * normalized_equations[0],
                eta * normalized_equations[1],
                tail_sign * normalized_equations[2],
                eta * normalized_equations[3],
            )
            if actual_equations != expected_equations:
                raise AssertionError("the outer-sign gauge identity failed")
            gauge_checks += 4
    return formula_checks, gauge_checks, normalized_tail_checks


def verify() -> tuple[int, int, int, int]:
    if len(VECTORS) != 8 or PHI != (4, 0, 0, 0, 2, 2, 2, -2):
        raise AssertionError("the projective character table changed")
    for left in range(8):
        for right in range(8):
            inner_product = sum(
                VECTORS[left][row] * VECTORS[right][row]
                for row in range(4)
            )
            if inner_product != PHI[left ^ right]:
                raise AssertionError("the projective XOR character law failed")
    if len(WORDS) != 16 or len(QUARTETS) != 48:
        raise AssertionError("the normalized word or quartet catalog changed")

    full = boundary_rows()
    parameter_e = parameter_e_rows()
    parameters = parameter_rows()
    physical = e2_boundary_rows()
    physical_parameters = e2_parameter_rows()
    if len(full) != EXPECTED_FULL_ROW_COUNT:
        raise AssertionError("the full boundary-row count changed")
    if len(parameter_e) != EXPECTED_PARAMETER_E_ROW_COUNT:
        raise AssertionError("the parameter-plus-e projection changed")
    if len(parameters) != EXPECTED_PARAMETER_ROW_COUNT:
        raise AssertionError("the parameter projection changed")
    if len(physical) != EXPECTED_E2_FULL_ROW_COUNT:
        raise AssertionError("the e=2 physical boundary table changed")
    if len(physical_parameters) != EXPECTED_E2_PARAMETER_ROW_COUNT:
        raise AssertionError("the e=2 parameter projection changed")
    if (
        canonical_rows_sha256(full, BOUNDARY_ROW_WIDTH)
        != EXPECTED_FULL_SHA256
    ):
        raise AssertionError("the full boundary-table hash changed")
    if (
        canonical_rows_sha256(parameter_e, PARAMETER_COUNT + 1)
        != EXPECTED_PARAMETER_E_SHA256
    ):
        raise AssertionError("the parameter-plus-e hash changed")
    if (
        canonical_rows_sha256(parameters, PARAMETER_COUNT)
        != EXPECTED_PARAMETER_SHA256
    ):
        raise AssertionError("the parameter hash changed")
    if (
        canonical_rows_sha256(physical, E2_BOUNDARY_ROW_WIDTH)
        != EXPECTED_E2_FULL_SHA256
    ):
        raise AssertionError("the e=2 physical boundary-table hash changed")
    if (
        canonical_rows_sha256(physical_parameters, PARAMETER_COUNT)
        != EXPECTED_E2_PARAMETER_SHA256
    ):
        raise AssertionError("the e=2 parameter hash changed")

    direct_boundary_checks = validate_every_boundary_row_directly()
    formula_checks, gauge_checks, normalized_tail_checks = (
        validate_general_formula()
    )
    return (
        direct_boundary_checks,
        formula_checks,
        gauge_checks,
        normalized_tail_checks,
    )


def main() -> int:
    (
        direct_boundary_checks,
        formula_checks,
        gauge_checks,
        normalized_tail_checks,
    ) = verify()
    print(f"PASS complementary_quartets={len(QUARTETS)}")
    print(f"PASS full_boundary_rows={len(boundary_rows())}")
    print(f"PASS parameter_e_rows={len(parameter_e_rows())}")
    print(f"PASS parameter_rows={len(parameter_rows())}")
    print(f"PASS e2_boundary_rows={len(e2_boundary_rows())}")
    print(f"PASS e2_parameter_rows={len(e2_parameter_rows())}")
    print(f"full_sha256={canonical_rows_sha256(boundary_rows())}")
    print(f"parameter_e_sha256={canonical_rows_sha256(parameter_e_rows())}")
    print(f"parameter_sha256={canonical_rows_sha256(parameter_rows())}")
    print(f"e2_full_sha256={canonical_rows_sha256(e2_boundary_rows())}")
    print(
        "e2_parameter_sha256="
        f"{canonical_rows_sha256(e2_parameter_rows())}"
    )
    print(f"direct_boundary_checks={direct_boundary_checks}")
    print(f"general_formula_checks={formula_checks}")
    print(f"outer_sign_gauge_checks={gauge_checks}")
    print(f"normalized_tail_checks={normalized_tail_checks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
