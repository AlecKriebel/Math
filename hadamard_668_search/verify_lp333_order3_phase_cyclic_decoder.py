#!/usr/bin/env python3
"""Audit a mod-7 cyclic decoder for the LP(333) order-three phase shell.

The ninth-root recombination lives in ``Z[zeta_9][C_37]^H``.  Modulo 7,

    Phi_9(X) = (X^3-2)(X^3-4),

and each cubic residue field is ``K=F_(7^3)``.  Since

    7^3 = 10 (mod 37),        H=<10>,

the H-invariant column algebra splits completely into thirteen scalar
K-factors in each conjugate coefficient component.  An exact phase frame
therefore satisfies thirteen affine bilinear equations

    x_A y_A + x_B y_B = 167 = 6 (mod 7)

over K.  This module verifies that split, enumerates the exact local
coefficient alphabets, certifies the affine compatibility-cone count, and
quantifies why the obvious factorwise trellis and balanced MITM are still
too large.

This is a necessary modular sieve and an architecture audit.  It is not a
phase survivor, an LP(333), or an H(668).
"""

from __future__ import annotations

from hashlib import sha256
from itertools import product
import json
from math import ceil, log2
from typing import Iterable, Sequence


P = 7
N = 37
H = (1, 10, 26)
ENERGY = 167
TARGET_SCALAR = ENERGY % P

# Work in F_(7^9)=F_7[t]/(t^9+t+1).  This field contains both the
# coefficient subfield F_(7^3) and the 37th roots needed to evaluate the
# invariant period transform.
FIELD_DEGREE = 9
FIELD_SIZE = P**FIELD_DEGREE
MODULUS = (1, 1, 0, 0, 0, 0, 0, 0, 0, 1)

F = tuple[int, ...]
F_ZERO: F = (0,) * FIELD_DEGREE
F_ONE: F = (1,) + (0,) * (FIELD_DEGREE - 1)

# Pinned roots in the field above.  ALPHA has order nine and ALPHA^3=2.
# ZETA has order 37.
ALPHA: F = (5, 2, 3, 6, 2, 6, 2, 5, 3)
ZETA: F = (4, 2, 0, 5, 5, 6, 1, 4, 1)

PROFILES = tuple(
    (first, second, 3 - first - second)
    for first in range(4)
    for second in range(4 - first)
)

KNOWN_PROFILE_SIGNATURE_FALLBACK = 6_338_555_429

EXPECTED_CERTIFICATE_SHA256 = (
    "0605563ad589018e39ac73a41ecf880c678f38ad6941730b9dd7fcb2e33e84cf"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


# ---------------------------------------------------------------------------
# Prime-field polynomials and the pinned degree-nine field.


def poly_trim(value: Sequence[int]) -> list[int]:
    result = [int(coefficient) % P for coefficient in value]
    while result and result[-1] == 0:
        result.pop()
    return result


def poly_subtract(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    return poly_trim(
        [
            (
                (left[index] if index < len(left) else 0)
                - (right[index] if index < len(right) else 0)
            )
            % P
            for index in range(max(len(left), len(right)))
        ]
    )


def poly_multiply(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    if not left or not right:
        return []
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            result[left_index + right_index] = (
                result[left_index + right_index]
                + int(left_value) * int(right_value)
            ) % P
    return poly_trim(result)


def poly_mod(
    value: Sequence[int], modulus: Sequence[int]
) -> list[int]:
    result = poly_trim(value)
    divisor = poly_trim(modulus)
    if not divisor:
        raise ZeroDivisionError("polynomial reduction modulo zero")
    inverse_lead = pow(divisor[-1], -1, P)
    while len(result) >= len(divisor):
        offset = len(result) - len(divisor)
        factor = result[-1] * inverse_lead % P
        for index, coefficient in enumerate(divisor):
            result[offset + index] = (
                result[offset + index] - factor * coefficient
            ) % P
        result = poly_trim(result)
    return result


def poly_gcd(
    left: Sequence[int], right: Sequence[int]
) -> list[int]:
    first = poly_trim(left)
    second = poly_trim(right)
    while second:
        first, second = second, poly_mod(first, second)
    if not first:
        return []
    inverse_lead = pow(first[-1], -1, P)
    return [coefficient * inverse_lead % P for coefficient in first]


def poly_power_mod(
    value: Sequence[int], exponent: int, modulus: Sequence[int]
) -> list[int]:
    result = [1]
    base = poly_mod(value, modulus)
    while exponent:
        if exponent & 1:
            result = poly_mod(poly_multiply(result, base), modulus)
        base = poly_mod(poly_multiply(base, base), modulus)
        exponent //= 2
    return result


def verify_modulus_irreducible() -> bool:
    """Apply the exact degree-nine finite-field irreducibility criterion."""

    x = [0, 1]
    # Nine has the single prime divisor three.
    if len(
        poly_gcd(
            MODULUS,
            poly_subtract(
                poly_power_mod(x, P**3, MODULUS),
                x,
            ),
        )
    ) != 1:
        return False
    return not poly_subtract(
        poly_power_mod(x, P**9, MODULUS),
        x,
    )


def f_add(left: F, right: F) -> F:
    return tuple((a + b) % P for a, b in zip(left, right))


def f_neg(value: F) -> F:
    return tuple(-coefficient % P for coefficient in value)


def f_subtract(left: F, right: F) -> F:
    return f_add(left, f_neg(right))


def f_multiply(left: F, right: F) -> F:
    work = [0] * (2 * FIELD_DEGREE - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            work[left_index + right_index] = (
                work[left_index + right_index]
                + left_value * right_value
            ) % P
    # MODULUS is monic and t^9=-(t+1).
    for degree in range(2 * FIELD_DEGREE - 2, FIELD_DEGREE - 1, -1):
        factor = work[degree]
        if factor:
            offset = degree - FIELD_DEGREE
            work[offset] = (work[offset] - factor) % P
            work[offset + 1] = (work[offset + 1] - factor) % P
    return tuple(work[:FIELD_DEGREE])


def f_power(value: F, exponent: int) -> F:
    if exponent < 0:
        return f_power(f_inverse(value), -exponent)
    result = F_ONE
    base = value
    while exponent:
        if exponent & 1:
            result = f_multiply(result, base)
        base = f_multiply(base, base)
        exponent //= 2
    return result


def f_inverse(value: F) -> F:
    if value == F_ZERO:
        raise ZeroDivisionError("zero has no inverse")
    return f_power(value, FIELD_SIZE - 2)


def f_scalar(value: int) -> F:
    return (int(value) % P,) + (0,) * (FIELD_DEGREE - 1)


def f_sum(values: Iterable[F]) -> F:
    result = F_ZERO
    for value in values:
        result = f_add(result, value)
    return result


def subfield_elements() -> tuple[F, ...]:
    """Return F_(7^3) in the basis 1,ALPHA,ALPHA^2."""

    alpha_squared = f_multiply(ALPHA, ALPHA)
    values = []
    for first, second, third in product(range(P), repeat=3):
        values.append(
            f_sum(
                (
                    f_scalar(first),
                    f_multiply(f_scalar(second), ALPHA),
                    f_multiply(f_scalar(third), alpha_squared),
                )
            )
        )
    if len(set(values)) != P**3:
        raise AssertionError("the pinned ninth root lost degree three")
    if any(f_power(value, P**3) != value for value in values):
        raise AssertionError("a coefficient-field value left F_(7^3)")
    return tuple(values)


def k_multiply_coordinates(
    left: tuple[int, int, int],
    right: tuple[int, int, int],
) -> tuple[int, int, int]:
    """Multiply in F_7[a]/(a^3-2), exposing nine scalar products."""

    x0, x1, x2 = left
    y0, y1, y2 = right
    return (
        (x0 * y0 + 2 * x1 * y2 + 2 * x2 * y1) % P,
        (x0 * y1 + x1 * y0 + 2 * x2 * y2) % P,
        (x0 * y2 + x1 * y1 + x2 * y0) % P,
    )


def verify_k_coordinate_multiplication() -> int:
    """Check the coordinate formula on a bilinear basis of K x K."""

    basis_coordinates = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    basis_values = (F_ONE, ALPHA, f_multiply(ALPHA, ALPHA))
    coordinate_of = {
        value: coordinates
        for coordinates, value in zip(basis_coordinates, basis_values)
    }
    # Include the products, which are enough to recover every bilinear
    # product after expanding in the displayed basis.
    checks = 0
    for left_coordinates, left_value in zip(
        basis_coordinates, basis_values
    ):
        for right_coordinates, right_value in zip(
            basis_coordinates, basis_values
        ):
            expected_coordinates = k_multiply_coordinates(
                left_coordinates,
                right_coordinates,
            )
            expected_value = f_sum(
                f_multiply(
                    f_scalar(coefficient),
                    basis_value,
                )
                for coefficient, basis_value in zip(
                    expected_coordinates,
                    basis_values,
                )
            )
            if f_multiply(left_value, right_value) != expected_value:
                raise AssertionError("the F_(7^3) coordinate product changed")
            checks += 1
    if len(coordinate_of) != 3:
        raise AssertionError("the coefficient-field basis collapsed")
    return checks


# ---------------------------------------------------------------------------
# The complete mod-seven invariant split.


def multiplicative_classes() -> tuple[tuple[int, ...], ...]:
    unseen = set(range(1, N))
    classes = []
    while unseen:
        representative = min(unseen)
        orbit = tuple(
            sorted((representative * multiplier) % N for multiplier in H)
        )
        classes.append(orbit)
        unseen.difference_update(orbit)
    if len(classes) != 12 or any(len(orbit) != 3 for orbit in classes):
        raise AssertionError("H no longer gives twelve three-element classes")
    return tuple(classes)


CLASSES = multiplicative_classes()
PARTS = ((0,),) + CLASSES


def period_transform() -> tuple[tuple[F, ...], ...]:
    """Evaluate the thirteen class indicators at the thirteen factors."""

    representatives = (0,) + tuple(orbit[0] for orbit in CLASSES)
    rows = []
    for representative in representatives:
        row = []
        for orbit in PARTS:
            if representative == 0:
                row.append(f_scalar(len(orbit)))
            else:
                row.append(
                    f_sum(
                        f_power(
                            ZETA,
                            representative * exponent % N,
                        )
                        for exponent in orbit
                    )
                )
        rows.append(tuple(row))
    return tuple(rows)


def matrix_rank(matrix: Sequence[Sequence[F]]) -> int:
    if not matrix:
        return 0
    work = [list(row) for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    rank = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(rank, row_count)
                if work[row][column] != F_ZERO
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = f_inverse(work[rank][column])
        work[rank] = [
            f_multiply(inverse, value) for value in work[rank]
        ]
        for row in range(row_count):
            if row == rank or work[row][column] == F_ZERO:
                continue
            factor = work[row][column]
            work[row] = [
                f_subtract(value, f_multiply(factor, pivot_value))
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def verify_complete_split() -> dict[str, object]:
    if not verify_modulus_irreducible():
        raise AssertionError("t^9+t+1 is no longer irreducible modulo seven")
    if f_power(ALPHA, 3) != f_scalar(2):
        raise AssertionError("the pinned ninth root has the wrong cube")
    if f_power(ALPHA, 9) != F_ONE or f_power(ALPHA, 3) == F_ONE:
        raise AssertionError("the pinned ninth root has the wrong order")
    coordinate_product_checks = verify_k_coordinate_multiplication()
    if f_power(ZETA, N) != F_ONE or ZETA == F_ONE:
        raise AssertionError("the pinned column root has the wrong order")

    # Phi_9=(X^3-2)(X^3-4) over F_7.  Neither cubic has a root.
    if any(pow(value, 3, P) in (2, 4) for value in range(P)):
        raise AssertionError("a mod-seven Phi_9 cubic became reducible")
    alpha_inverse = f_inverse(ALPHA)
    if f_power(alpha_inverse, 3) != f_scalar(4):
        raise AssertionError("ninth-root inversion stopped swapping the cubics")

    if P**3 % N != 10 or tuple(
        pow(P**3, exponent, N) for exponent in range(3)
    ) != H:
        raise AssertionError("coefficient Frobenius no longer equals H")

    transform = period_transform()
    if any(
        f_power(value, P**3) != value
        for row in transform
        for value in row
    ):
        raise AssertionError("a Gaussian period left F_(7^3)")
    if matrix_rank(transform) != 13:
        raise AssertionError("the thirteen-factor transform lost rank")
    zero_entries = sum(
        value == F_ZERO for row in transform for value in row
    )
    if zero_entries:
        raise AssertionError("the period transform acquired a zero entry")

    # A single scalar factor gives a length-13, dimension-12 unrestricted
    # linear kernel.  Nonzero entries exclude weight one, while any two
    # columns give an explicit weight-two kernel word.
    row = transform[1]
    weight_two = (row[1], f_neg(row[0]))
    residual = f_add(
        f_multiply(row[0], weight_two[0]),
        f_multiply(row[1], weight_two[1]),
    )
    if residual != F_ZERO:
        raise AssertionError("the explicit weight-two kernel word failed")

    return {
        "phi9_factors": ("X^3-2", "X^3-4"),
        "coefficient_field_size": P**3,
        "coefficient_frobenius_mod_37": P**3 % N,
        "invariant_classes": len(CLASSES),
        "scalar_factors_per_component": len(PARTS),
        "period_transform_rank": matrix_rank(transform),
        "period_transform_zero_entries": zero_entries,
        "single_factor_unrestricted_kernel_distance": 2,
        "coordinate_product_basis_checks": coordinate_product_checks,
        "period_transform_sha256": compact_hash(transform),
    }


# ---------------------------------------------------------------------------
# Exact local coefficient alphabets.


def active_count(profile: Sequence[int]) -> int:
    if (
        len(profile) != 3
        or any(int(value) not in (0, 1, 2, 3) for value in profile)
        or sum(profile) not in (3, 6)
    ):
        raise ValueError(
            "a profile must be a three-fiber count of total three or six"
        )
    return sum(int(value) in (1, 2) for value in profile)


def phase_coefficient_pair(
    profile: Sequence[int], trits: Sequence[int]
) -> tuple[F, F]:
    """Return the plus and conjugate coefficient images in F_(7^3)."""

    if len(trits) != active_count(profile):
        raise ValueError("the trit count does not match the profile")
    plus = F_ZERO
    dagger = F_ZERO
    trit_index = 0
    for residue, count in enumerate(profile):
        if count not in (1, 2):
            continue
        trit = int(trits[trit_index])
        if trit not in (0, 1, 2):
            raise ValueError("phase trits lie in C_3")
        trit_index += 1
        alpha_power = f_power(ALPHA, residue)
        alpha_conjugate_power = f_power(ALPHA, -residue)
        omega = f_power(ALPHA, 3)
        if count == 1:
            phase = f_power(omega, -trit)
            conjugate_phase = f_power(omega, trit)
        else:
            phase = f_neg(f_power(omega, trit))
            conjugate_phase = f_neg(f_power(omega, -trit))
        plus = f_add(plus, f_multiply(alpha_power, phase))
        dagger = f_add(
            dagger,
            f_multiply(alpha_conjugate_power, conjugate_phase),
        )
    return plus, dagger


def coefficient_catalog(
    profile: Sequence[int],
) -> tuple[tuple[F, F], ...]:
    count = active_count(profile)
    return tuple(
        phase_coefficient_pair(profile, trits)
        for trits in product(range(3), repeat=count)
    )


def verify_coefficient_alphabets() -> dict[str, object]:
    profile_rows = []
    for profile in PROFILES:
        catalog = coefficient_catalog(profile)
        expected = 3 ** active_count(profile)
        if len(catalog) != expected or len(set(catalog)) != expected:
            raise AssertionError("a paired coefficient alphabet collided")
        if len({plus for plus, _ in catalog}) != expected:
            raise AssertionError("the plus coefficient stopped decoding trits")

        complement = tuple(3 - value for value in profile)
        complement_catalog = coefficient_catalog(complement)
        if len(set(complement_catalog)) != expected:
            raise AssertionError("a complemented coefficient alphabet collided")
        profile_rows.append((profile, active_count(profile), expected))

    pair_histogram: dict[int, int] = {}
    for left in PROFILES:
        for right in PROFILES:
            size = 3 ** (active_count(left) + active_count(right))
            pair_histogram[size] = pair_histogram.get(size, 0) + 1
    expected_histogram = {
        1: 9,
        9: 36,
        27: 6,
        81: 36,
        243: 12,
        729: 1,
    }
    if pair_histogram != expected_histogram:
        raise AssertionError("the two-channel local alphabet census changed")

    return {
        "profile_alphabets": tuple(profile_rows),
        "one_channel_alphabet_sizes": tuple(
            sorted({row[2] for row in profile_rows})
        ),
        "two_channel_alphabet_histogram": tuple(
            sorted(pair_histogram.items())
        ),
        "maximum_two_channel_local_alphabet": max(pair_histogram),
        "alphabet_sha256": compact_hash(
            (tuple(profile_rows), tuple(sorted(pair_histogram.items())))
        ),
    }


# ---------------------------------------------------------------------------
# Direct factor orientation, affine compatibility, and architecture bounds.


def matrix_vector(
    matrix: Sequence[Sequence[F]], vector: Sequence[F]
) -> tuple[F, ...]:
    return tuple(
        f_sum(
            f_multiply(coefficient, value)
            for coefficient, value in zip(row, vector)
        )
        for row in matrix
    )


def expand_class_word(coefficients: Sequence[F]) -> tuple[F, ...]:
    if len(coefficients) != len(PARTS):
        raise ValueError("expected thirteen invariant class coefficients")
    result = [F_ZERO] * N
    for coefficient, orbit in zip(coefficients, PARTS):
        for exponent in orbit:
            result[exponent] = coefficient
    return tuple(result)


def group_multiply(
    left: Sequence[F], right: Sequence[F]
) -> tuple[F, ...]:
    if len(left) != N or len(right) != N:
        raise ValueError("expected two C_37 words")
    result = [F_ZERO] * N
    for left_index, left_value in enumerate(left):
        if left_value == F_ZERO:
            continue
        for right_index, right_value in enumerate(right):
            if right_value == F_ZERO:
                continue
            target = (left_index + right_index) % N
            result[target] = f_add(
                result[target],
                f_multiply(left_value, right_value),
            )
    return tuple(result)


def evaluate_word(word: Sequence[F], exponent: int) -> F:
    if len(word) != N:
        raise ValueError("expected a C_37 word")
    return f_sum(
        f_multiply(value, f_power(ZETA, exponent * index % N))
        for index, value in enumerate(word)
    )


def verify_factor_orientation() -> dict[str, object]:
    """Match all thirteen scalar products to direct cyclic convolution."""

    transform = period_transform()
    representatives = (0,) + tuple(orbit[0] for orbit in CLASSES)
    row_of_class = {
        frozenset(orbit): index
        for index, orbit in enumerate(PARTS)
    }
    inverse_rows = tuple(
        0
        if representative == 0
        else row_of_class[
            frozenset((-value) % N for value in CLASSES[index - 1])
        ]
        for index, representative in enumerate(representatives)
    )

    plus_channels = []
    dagger_channels = []
    for channel in range(2):
        plus_coefficients = []
        dagger_coefficients = []
        for part_index in range(len(PARTS)):
            profile = PROFILES[(4 * part_index + 3 * channel) % len(PROFILES)]
            count = active_count(profile)
            trits = tuple(
                (part_index + channel + 2 * offset) % 3
                for offset in range(count)
            )
            plus, dagger = phase_coefficient_pair(profile, trits)
            plus_coefficients.append(plus)
            dagger_coefficients.append(dagger)
        plus_channels.append(tuple(plus_coefficients))
        dagger_channels.append(tuple(dagger_coefficients))

    direct_correlation = (F_ZERO,) * N
    coordinate_products = [F_ZERO] * len(PARTS)
    for plus_coefficients, dagger_coefficients in zip(
        plus_channels, dagger_channels
    ):
        plus_word = expand_class_word(plus_coefficients)
        star_word_mutable = [F_ZERO] * N
        for dagger, orbit in zip(dagger_coefficients, PARTS):
            for exponent in orbit:
                star_word_mutable[-exponent % N] = dagger
        star_word = tuple(star_word_mutable)
        direct_correlation = tuple(
            f_add(left, right)
            for left, right in zip(
                direct_correlation,
                group_multiply(plus_word, star_word),
            )
        )

        plus_coordinates = matrix_vector(transform, plus_coefficients)
        dagger_coordinates = matrix_vector(transform, dagger_coefficients)
        for factor_index in range(len(PARTS)):
            coordinate_products[factor_index] = f_add(
                coordinate_products[factor_index],
                f_multiply(
                    plus_coordinates[factor_index],
                    dagger_coordinates[inverse_rows[factor_index]],
                ),
            )

    direct_evaluations = tuple(
        evaluate_word(direct_correlation, representative)
        for representative in representatives
    )
    if tuple(coordinate_products) != direct_evaluations:
        raise AssertionError("the mod-seven factor/star orientation changed")

    # The correlation is H-invariant, and the full-rank period transform
    # makes thirteen scalar target equations equivalent to the complete
    # invariant group-ring target modulo seven.
    class_coefficients = tuple(
        direct_correlation[orbit[0]] for orbit in PARTS
    )
    if any(
        direct_correlation[exponent] != class_coefficients[index]
        for index, orbit in enumerate(PARTS)
        for exponent in orbit
    ):
        raise AssertionError("the direct correlation lost H-invariance")
    if matrix_vector(transform, class_coefficients) != direct_evaluations:
        raise AssertionError("the period transform failed direct replay")

    target_coefficients = (
        (f_scalar(TARGET_SCALAR),)
        + (F_ZERO,) * (len(PARTS) - 1)
    )
    target_evaluations = matrix_vector(transform, target_coefficients)
    if target_evaluations != (f_scalar(TARGET_SCALAR),) * len(PARTS):
        raise AssertionError("the affine factor target is not 167 mod seven")

    certificate = (
        inverse_rows,
        compact_hash(tuple(plus_channels)),
        compact_hash(tuple(dagger_channels)),
        compact_hash(direct_correlation),
        compact_hash(direct_evaluations),
    )
    return {
        "factor_orientation_checks": len(PARTS),
        "inverse_factor_rows": inverse_rows,
        "target_at_every_factor": TARGET_SCALAR,
        "certificate_sha256": compact_hash(certificate),
    }


def dot_pair(
    x: tuple[F, F], y: tuple[F, F]
) -> F:
    return f_add(
        f_multiply(x[0], y[0]),
        f_multiply(x[1], y[1]),
    )


def compatible_y(
    x: tuple[F, F], tau: F
) -> tuple[F, F]:
    """Parameterize x.y=167 mod 7 for nonzero x."""

    target = f_scalar(TARGET_SCALAR)
    first, second = x
    if first != F_ZERO:
        particular = (f_multiply(target, f_inverse(first)), F_ZERO)
    elif second != F_ZERO:
        particular = (F_ZERO, f_multiply(target, f_inverse(second)))
    else:
        raise ValueError("the nonzero affine target has no solution at x=0")
    kernel = (f_neg(second), first)
    return (
        f_add(particular[0], f_multiply(tau, kernel[0])),
        f_add(particular[1], f_multiply(tau, kernel[1])),
    )


def recover_tau(
    x: tuple[F, F], y: tuple[F, F]
) -> F:
    first, second = x
    target = f_scalar(TARGET_SCALAR)
    if dot_pair(x, y) != target:
        raise ValueError("the pair is not factor-compatible")
    if first != F_ZERO:
        return f_multiply(y[1], f_inverse(first))
    if second == F_ZERO:
        raise ValueError("the zero x-vector is never compatible")
    # y_0 = tau*(-x_1).
    return f_neg(f_multiply(y[0], f_inverse(second)))


def verify_affine_compatibility() -> dict[str, object]:
    elements = subfield_elements()
    q = len(elements)
    nonzero = tuple(value for value in elements if value != F_ZERO)
    inverses = {value: f_inverse(value) for value in nonzero}
    probes = (F_ZERO, F_ONE, ALPHA)
    # Exhaust both pivot axes and a deterministic mixed projective slice.
    # The count itself follows from the proved affine-line formula, so there
    # is no value in replaying all q^2-1 projective representatives.
    x_fixtures = (
        tuple((value, F_ZERO) for value in nonzero)
        + tuple((F_ZERO, value) for value in nonzero)
        + tuple(
            (
                value,
                f_add(f_multiply(ALPHA, value), F_ONE),
            )
            for value in elements
        )
    )
    checked = 0
    target = f_scalar(TARGET_SCALAR)
    for first, second in x_fixtures:
        if first != F_ZERO:
            particular = (
                f_multiply(target, inverses[first]),
                F_ZERO,
            )
        elif second != F_ZERO:
            particular = (
                F_ZERO,
                f_multiply(target, inverses[second]),
            )
        else:
            raise AssertionError("a compatibility fixture used x=0")
        kernel = (f_neg(second), first)
        for tau in probes:
            y = (
                f_add(particular[0], f_multiply(tau, kernel[0])),
                f_add(particular[1], f_multiply(tau, kernel[1])),
            )
            if dot_pair((first, second), y) != target:
                raise AssertionError("the affine factor parameterization failed")
            if first != F_ZERO:
                recovered = f_multiply(y[1], inverses[first])
            else:
                recovered = f_neg(f_multiply(y[0], inverses[second]))
            if recovered != tau:
                raise AssertionError("the affine factor parameter is not unique")
            checked += 1

    compatibility_count = (q * q - 1) * q
    if compatibility_count != 40_353_264:
        raise AssertionError("the affine compatibility-cone count changed")

    packed_entry_bytes = ceil(4 * ceil(log2(q)) / 8)
    return {
        "factor_target_mod_7": TARGET_SCALAR,
        "factor_plus_vectors": q * q - 1,
        "compatible_minus_vectors_per_plus": q,
        "compatibility_entries": compatibility_count,
        "projective_x_fixtures": len(x_fixtures),
        "parameter_fixtures_checked": checked,
        "minimum_fixed_width_bytes_per_entry": packed_entry_bytes,
        "packed_table_bytes": compatibility_count * packed_entry_bytes,
        "uint64_table_bytes": compatibility_count * 8,
    }


def quadratic_value(state: tuple[F, F, F, F]) -> F:
    return dot_pair((state[0], state[1]), (state[2], state[3]))


def state_add(
    left: tuple[F, F, F, F],
    right: tuple[F, F, F, F],
) -> tuple[F, F, F, F]:
    return tuple(
        f_add(first, second) for first, second in zip(left, right)
    )  # type: ignore[return-value]


def verify_nonadditivity() -> dict[str, object]:
    """Exhibit the polar term that invalidates an additive Wagner join."""

    zero = F_ZERO
    one = F_ONE
    first = (one, zero, zero, one)
    second = (zero, one, one, zero)
    separate = f_add(quadratic_value(first), quadratic_value(second))
    joined = quadratic_value(state_add(first, second))
    polar = f_subtract(joined, separate)
    if polar == F_ZERO:
        raise AssertionError("the factor quadric accidentally became additive")
    return {
        "quadratic_block_signature_additive": False,
        "polar_fixture": polar,
    }


def architecture_bounds() -> dict[str, object]:
    q = P**3
    raw_one_factor_states = q**4
    if raw_one_factor_states != P**12:
        raise AssertionError("the one-factor state dimension changed")
    if raw_one_factor_states <= KNOWN_PROFILE_SIGNATURE_FALLBACK:
        raise AssertionError("the raw factor trellis unexpectedly beat the fallback")

    # The complete canonical zero-column words remove the tempting
    # per-channel phase gauges.  The certified labelled transport group has
    # no row translation and does not uniformly delete a placement trit.
    # A lossless generic phase architecture must therefore retain all 54.
    raw_phase_trits = 54
    balanced_half_trits = raw_phase_trits // 2
    balanced_half_entries = 3**balanced_half_trits
    identifier_bits = ceil(balanced_half_trits * log2(3))
    information_bytes = (
        balanced_half_entries * balanced_half_trits * log2(3) / 8
    )
    factor_field_products = 2 * len(PARTS)
    scalar_products_per_field_product = 9
    scalar_product_tables = (
        factor_field_products * scalar_products_per_field_product
    )
    scalar_table_rows = P * P

    return {
        "raw_one_factor_states": raw_one_factor_states,
        "raw_state_bitset_bytes": ceil(raw_one_factor_states / 8),
        "raw_state_uint32_predecessor_bytes": raw_one_factor_states * 4,
        "raw_states_over_profile_fallback": (
            raw_one_factor_states / KNOWN_PROFILE_SIGNATURE_FALLBACK
        ),
        "raw_phase_trits": raw_phase_trits,
        "uniform_phase_gauge_trits": 0,
        "balanced_half_trits": balanced_half_trits,
        "balanced_half_entries": balanced_half_entries,
        "minimum_identifier_bits": identifier_bits,
        "identifier_information_bytes": ceil(information_bytes),
        "three_block_trits": (18, 18, 18),
        "largest_three_block_list": 3**18,
        "smallest_three_block_pair_join": 3**36,
        "four_block_trits": (14, 14, 13, 13),
        "largest_four_block_list": 3**14,
        "smallest_four_block_pair_join": 3**26,
        "largest_four_block_pair_join": 3**28,
        "balanced_four_block_pair_join": 3**27,
        "known_profile_signature_fallback": KNOWN_PROFILE_SIGNATURE_FALLBACK,
        "factor_field_products": factor_field_products,
        "scalar_products_per_field_product": (
            scalar_products_per_field_product
        ),
        "scalar_product_tables": scalar_product_tables,
        "rows_per_scalar_product_table": scalar_table_rows,
        "total_scalar_product_table_rows": (
            scalar_product_tables * scalar_table_rows
        ),
    }


def verify() -> dict[str, object]:
    split = verify_complete_split()
    alphabets = verify_coefficient_alphabets()
    orientation = verify_factor_orientation()
    compatibility = verify_affine_compatibility()
    polar = verify_nonadditivity()
    bounds = architecture_bounds()
    certificate = (
        split,
        alphabets,
        orientation,
        compatibility,
        polar,
        bounds,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_CERTIFICATE_SHA256
        and certificate_hash != EXPECTED_CERTIFICATE_SHA256
    ):
        raise AssertionError("the mod-seven cyclic-decoder audit changed")
    return {
        "complete_split": split,
        "coefficient_alphabets": alphabets,
        "factor_orientation": orientation,
        "affine_compatibility": compatibility,
        "nonadditivity": polar,
        "architecture_bounds": bounds,
        "certificate_sha256": certificate_hash,
    }


def main() -> None:
    result = verify()
    split = result["complete_split"]
    alphabets = result["coefficient_alphabets"]
    compatibility = result["affine_compatibility"]
    bounds = result["architecture_bounds"]
    print("coefficient_field=F_(7^3)")
    print(
        "scalar_factors_per_component="
        f"{split['scalar_factors_per_component']}"
    )
    print(
        "period_transform_rank="
        f"{split['period_transform_rank']}"
    )
    print(
        "two_channel_local_alphabet_max="
        f"{alphabets['maximum_two_channel_local_alphabet']}"
    )
    print(
        "affine_compatibility_entries="
        f"{compatibility['compatibility_entries']}"
    )
    print(f"raw_one_factor_states={bounds['raw_one_factor_states']}")
    print(
        "balanced_half_entries="
        f"{bounds['balanced_half_entries']}"
    )
    print(f"certificate_sha256={result['certificate_sha256']}")
    print("PASS: exact mod-seven split and decoder barrier verified")


if __name__ == "__main__":
    main()
