#!/usr/bin/env python3
"""Verify the physical obstruction to the trivial zero phase-cone branch.

For one binary channel of length 333 and sum one, let ``m_r`` be the number
of plus entries in CRT row ``r``.  The recombined trivial coordinate is

    c = sum_{r=0}^8 m_r alpha^r

in ``F_167(alpha)``, where ``Phi_9(alpha)=alpha^6+alpha^3+1=0``.  Reduction
in this basis shows that ``c=0`` forces

    m_s = m_{s+3} = m_{s+6} (mod 167),  s=0,1,2.

Since every margin is in ``[0,37]``, these are integer equalities, which
would make their total divisible by three.  The physical total is 167.

The second part of the verifier maps the complete pinned 1,756-word
row-margin catalog into the nonzero trivial cone and certifies its exact
1,411-point image.  Only Python's standard library is used.
"""

from __future__ import annotations

import csv
from collections import Counter
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from typing import Sequence


P = 167
ROWS = 9
COLUMNS = 37
CHANNEL_PLUS_COUNT = 167

# Low-to-high coefficients of Phi_9=x^6+x^3+1.
PHI9 = (1, 0, 0, 1, 0, 0, 1)
FIELD_DEGREE = 6
Field = tuple[int, int, int, int, int, int]
F_ZERO: Field = (0, 0, 0, 0, 0, 0)
F_ONE: Field = (1, 0, 0, 0, 0, 0)
F_ALPHA: Field = (0, 1, 0, 0, 0, 0)

CATALOG_RELATIVE_PATH = Path("output") / "lp333_order3_row_sum_catalog.csv"
CATALOG_SHA256 = (
    "e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea"
)
CATALOG_ROWS = 1756
CATALOG_HEADER = tuple(
    f"s{row}_{coordinate}"
    for row in range(ROWS)
    for coordinate in ("real", "imag")
)

CANONICAL_ZERO_EXPONENTS = (0, 0, 0, 1, 2, 3, 1, 3, 2)
SIGN_PAIRS = ((1, 1), (-1, 1), (-1, -1), (1, -1))
ZERO_A_PLUS = tuple(
    int(SIGN_PAIRS[value][0] == 1)
    for value in CANONICAL_ZERO_EXPONENTS
)
ZERO_B_PLUS = tuple(
    int(SIGN_PAIRS[value][1] == 1)
    for value in CANONICAL_ZERO_EXPONENTS
)

EXPECTED_CATALOG_IMAGE_SHA256 = (
    "50f3d0f090187ded04c9bce52cfb6900c451dd005d48e4db965046c8d71edb26"
)


def compact_hash(value: object) -> str:
    payload = json.dumps(value, separators=(",", ":"), sort_keys=False)
    return sha256(payload.encode("ascii")).hexdigest()


def f_add(left: Field, right: Field) -> Field:
    return tuple((a + b) % P for a, b in zip(left, right))  # type: ignore[return-value]


def f_neg(value: Field) -> Field:
    return tuple((-entry) % P for entry in value)  # type: ignore[return-value]


def f_multiply(left: Field, right: Field) -> Field:
    work = [0] * (2 * FIELD_DEGREE - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            work[left_index + right_index] = (
                work[left_index + right_index]
                + left_value * right_value
            ) % P
    # alpha^k=-alpha^(k-3)-alpha^(k-6), k>=6.
    for degree in range(len(work) - 1, FIELD_DEGREE - 1, -1):
        value = work[degree] % P
        work[degree] = 0
        work[degree - 3] = (work[degree - 3] - value) % P
        work[degree - 6] = (work[degree - 6] - value) % P
    return tuple(work[:FIELD_DEGREE])  # type: ignore[return-value]


def f_power(value: Field, exponent: int) -> Field:
    if exponent < 0:
        raise ValueError("field exponents must be nonnegative")
    result = F_ONE
    base = value
    while exponent:
        if exponent & 1:
            result = f_multiply(result, base)
        base = f_multiply(base, base)
        exponent //= 2
    return result


def f_inverse(value: Field) -> Field:
    if value == F_ZERO:
        raise ZeroDivisionError("zero has no field inverse")
    return f_power(value, P**FIELD_DEGREE - 2)


def f_scale(scalar: int, value: Field) -> Field:
    return tuple((scalar * entry) % P for entry in value)  # type: ignore[return-value]


def margin_coordinate(margins: Sequence[int]) -> Field:
    """Evaluate ``sum m_r alpha^r`` using ``Phi_9(alpha)=0``."""

    if len(margins) != ROWS:
        raise ValueError("a channel needs nine row margins")
    if any(type(value) is not int for value in margins):
        raise ValueError("row margins must be integers")
    return (
        (margins[0] - margins[6]) % P,
        (margins[1] - margins[7]) % P,
        (margins[2] - margins[8]) % P,
        (margins[3] - margins[6]) % P,
        (margins[4] - margins[7]) % P,
        (margins[5] - margins[8]) % P,
    )


def polynomial_coordinate(margins: Sequence[int]) -> Field:
    """Independently evaluate the margin polynomial by field arithmetic."""

    if len(margins) != ROWS:
        raise ValueError("a channel needs nine row margins")
    result = F_ZERO
    power = F_ONE
    for margin in margins:
        result = f_add(result, f_scale(int(margin), power))
        power = f_multiply(power, F_ALPHA)
    return result


def matrix_rank_mod_p(matrix: Sequence[Sequence[int]]) -> int:
    work = [[int(value) % P for value in row] for row in matrix]
    if not work:
        return 0
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (
                row
                for row in range(rank, len(work))
                if work[row][column] % P
            ),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], P - 2, P)
        work[rank] = [
            value * inverse % P for value in work[rank]
        ]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % P
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def verify_phi9_margin_kernel() -> dict[str, object]:
    """Certify the displayed kernel and the integer lifting argument."""

    order = next(
        exponent
        for exponent in range(1, 10)
        if pow(P, exponent, 9) == 1
    )
    if order != 6:
        raise AssertionError("Phi_9 is no longer irreducible modulo 167")
    if f_power(F_ALPHA, 6) != f_neg(
        f_add(f_power(F_ALPHA, 3), F_ONE)
    ):
        raise AssertionError("the Phi_9 reduction relation changed")
    if f_power(F_ALPHA, 9) != F_ONE:
        raise AssertionError("alpha is not a ninth root")
    if any(f_power(F_ALPHA, divisor) == F_ONE for divisor in (1, 3)):
        raise AssertionError("alpha is not primitive of order nine")

    columns = tuple(
        polynomial_coordinate(
            tuple(int(index == row) for index in range(ROWS))
        )
        for row in range(ROWS)
    )
    reduction_matrix = tuple(
        tuple(columns[column][row] for column in range(ROWS))
        for row in range(FIELD_DEGREE)
    )
    rank = matrix_rank_mod_p(reduction_matrix)
    kernel_basis = tuple(
        tuple(
            int(row in (residue, residue + 3, residue + 6))
            for row in range(ROWS)
        )
        for residue in range(3)
    )
    if rank != FIELD_DEGREE:
        raise AssertionError("the margin evaluation map lost rank six")
    if any(margin_coordinate(vector) != F_ZERO for vector in kernel_basis):
        raise AssertionError("the claimed three kernel vectors no longer vanish")
    if matrix_rank_mod_p(kernel_basis) != 3:
        raise AssertionError("the claimed kernel vectors lost independence")
    if ROWS - rank != len(kernel_basis):
        raise AssertionError("the displayed vectors no longer span the kernel")

    # The coordinate formula and the independent polynomial evaluator agree
    # on a deterministic collection that includes all basis vectors.
    fixtures = tuple(
        tuple((11 * fixture + 7 * row + row * row) % 38 for row in range(ROWS))
        for fixture in range(19)
    )
    for margins in (
        *(
            tuple(int(index == row) for index in range(ROWS))
            for row in range(ROWS)
        ),
        *fixtures,
    ):
        if margin_coordinate(margins) != polynomial_coordinate(margins):
            raise AssertionError("the two margin evaluators disagree")

    if not COLUMNS < P:
        raise AssertionError("the [0,37] congruence lift is no longer valid")
    if CHANNEL_PLUS_COUNT % 3 == 0:
        raise AssertionError("the physical channel support became divisible by three")

    # If c=0, the six displayed coordinates give congruences between
    # margins whose differences lie in [-37,37].  The only multiple of 167
    # in that interval is zero, so the congruences are integer equalities.
    lifted_difference_interval = (-COLUMNS, COLUMNS)
    multiples_in_interval = tuple(
        value
        for value in range(lifted_difference_interval[0],
                           lifted_difference_interval[1] + 1)
        if value % P == 0
    )
    if multiples_in_interval != (0,):
        raise AssertionError("the margin congruences no longer lift uniquely")

    return {
        "ord_9_167": order,
        "phi9_degree": FIELD_DEGREE,
        "evaluation_rank": rank,
        "kernel_dimension": ROWS - rank,
        "kernel_basis": kernel_basis,
        "margin_interval": (0, COLUMNS),
        "difference_interval": lifted_difference_interval,
        "multiples_of_167_in_difference_interval": multiples_in_interval,
        "per_channel_plus_count": CHANNEL_PLUS_COUNT,
        "per_channel_plus_count_mod_3": CHANNEL_PLUS_COUNT % 3,
        "individual_zero_coordinate_impossible": True,
        "joint_trivial_zero_branch_impossible": True,
    }


def catalog_path() -> Path:
    return Path(__file__).resolve().parent / CATALOG_RELATIVE_PATH


def parse_catalog() -> tuple[tuple[tuple[int, int], ...], ...]:
    payload = catalog_path().read_bytes()
    actual_hash = sha256(payload).hexdigest()
    if actual_hash != CATALOG_SHA256:
        raise AssertionError(
            f"row-sum catalog hash changed: {actual_hash} != {CATALOG_SHA256}"
        )
    rows = list(csv.reader(StringIO(payload.decode("ascii"), newline="")))
    if not rows or tuple(rows[0]) != CATALOG_HEADER:
        raise AssertionError("the row-sum catalog header changed")
    result = []
    for raw in rows[1:]:
        if len(raw) != 2 * ROWS:
            raise AssertionError("a row-sum catalog entry has the wrong width")
        values = tuple(int(value) for value in raw)
        result.append(
            tuple(
                (values[2 * row], values[2 * row + 1])
                for row in range(ROWS)
            )
        )
    if len(result) != CATALOG_ROWS or len(set(result)) != CATALOG_ROWS:
        raise AssertionError("the row-sum catalog count or uniqueness changed")
    return tuple(result)


def plus_margins(
    row_sum_word: Sequence[tuple[int, int]]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Recover the A/B plus counts from the Gaussian QPSK row sums."""

    if len(row_sum_word) != ROWS:
        raise ValueError("a row-sum word needs nine Gaussian entries")
    a_margins = []
    b_margins = []
    for real, imaginary in row_sum_word:
        # s=(A+B+i(B-A))/2, hence A=Re(s)-Im(s), B=Re(s)+Im(s).
        a_sign_sum = int(real) - int(imaginary)
        b_sign_sum = int(real) + int(imaginary)
        if (COLUMNS + a_sign_sum) % 2:
            raise AssertionError("an A row sign sum has the wrong parity")
        if (COLUMNS + b_sign_sum) % 2:
            raise AssertionError("a B row sign sum has the wrong parity")
        a_margins.append((COLUMNS + a_sign_sum) // 2)
        b_margins.append((COLUMNS + b_sign_sum) // 2)
    return tuple(a_margins), tuple(b_margins)


def verify_catalog_image() -> dict[str, object]:
    """Pin the exact row-margin image inside the nonzero trivial cone."""

    catalog = parse_catalog()
    records = []
    coordinate_pairs = []
    ratios = []
    for index, word in enumerate(catalog):
        if (
            sum(value[0] for value in word),
            sum(value[1] for value in word),
        ) != (1, 0):
            raise AssertionError("a row-sum catalog word lost total one")
        margins_a, margins_b = plus_margins(word)
        for channel, (margins, fixed_zero) in enumerate(
            (
                (margins_a, ZERO_A_PLUS),
                (margins_b, ZERO_B_PLUS),
            )
        ):
            if any(not 0 <= value <= COLUMNS for value in margins):
                raise AssertionError("a physical row margin left [0,37]")
            if sum(margins) != CHANNEL_PLUS_COUNT:
                raise AssertionError(
                    f"channel {channel} lost its exact plus count 167"
                )
            class_margins = tuple(
                (margin - zero) // 3
                for margin, zero in zip(margins, fixed_zero)
            )
            if any(
                (margin - zero) % 3
                for margin, zero in zip(margins, fixed_zero)
            ):
                raise AssertionError(
                    "a margin is incompatible with the fixed zero column"
                )
            if any(not 0 <= value <= 12 for value in class_margins):
                raise AssertionError("a class margin left [0,12]")

        coordinate_a = margin_coordinate(margins_a)
        coordinate_b = margin_coordinate(margins_b)
        if coordinate_a == F_ZERO or coordinate_b == F_ZERO:
            raise AssertionError("the catalog met the impossible zero branch")
        if coordinate_a != polynomial_coordinate(margins_a):
            raise AssertionError("the A margin coordinate changed")
        if coordinate_b != polynomial_coordinate(margins_b):
            raise AssertionError("the B margin coordinate changed")

        conjugate_a = f_power(coordinate_a, P**3)
        conjugate_b = f_power(coordinate_b, P**3)
        norm_residual = f_add(
            f_multiply(coordinate_a, conjugate_a),
            f_multiply(coordinate_b, conjugate_b),
        )
        if norm_residual != F_ZERO:
            raise AssertionError("a row-margin word left the trivial norm cone")

        ratio = f_multiply(coordinate_b, f_inverse(coordinate_a))
        ratio_norm = f_multiply(ratio, f_power(ratio, P**3))
        if ratio_norm != f_neg(F_ONE):
            raise AssertionError("a projective ratio lost norm minus one")

        coordinate_pairs.append((coordinate_a, coordinate_b))
        ratios.append(ratio)
        records.append(
            (
                index,
                margins_a,
                margins_b,
                coordinate_a,
                coordinate_b,
                ratio,
            )
        )

    pair_multiplicities = Counter(coordinate_pairs)
    ratio_multiplicities = Counter(ratios)
    pair_histogram = tuple(sorted(Counter(pair_multiplicities.values()).items()))
    ratio_histogram = tuple(
        sorted(Counter(ratio_multiplicities.values()).items())
    )
    if (
        len(pair_multiplicities) != 1411
        or len(ratio_multiplicities) != 1411
        or pair_histogram != ((1, 1066), (2, 345))
        or ratio_histogram != ((1, 1066), (2, 345))
    ):
        raise AssertionError("the 1,756-to-1,411 cone census changed")

    # Equality of both cardinalities is not enough: check that a ratio
    # identifies a unique ordered coordinate pair on this exact catalog.
    ratio_to_pairs: dict[Field, set[tuple[Field, Field]]] = {}
    for pair, ratio in zip(coordinate_pairs, ratios):
        ratio_to_pairs.setdefault(ratio, set()).add(pair)
    if any(len(pairs) != 1 for pairs in ratio_to_pairs.values()):
        raise AssertionError("one catalog ratio acquired two physical scales")

    abstract_ratio_count = P**3 + 1
    if abstract_ratio_count != 4_657_464:
        raise AssertionError("the norm-minus-one fiber size changed")
    certificate = (
        CATALOG_SHA256,
        ZERO_A_PLUS,
        ZERO_B_PLUS,
        tuple(records),
        tuple(sorted(pair_multiplicities.items())),
        tuple(sorted(ratio_multiplicities.items())),
        abstract_ratio_count,
    )
    certificate_hash = compact_hash(certificate)
    if (
        EXPECTED_CATALOG_IMAGE_SHA256
        and certificate_hash != EXPECTED_CATALOG_IMAGE_SHA256
    ):
        raise AssertionError("the catalog cone-image certificate changed")
    return {
        "catalog_sha256": CATALOG_SHA256,
        "catalog_rows": len(catalog),
        "fixed_zero_a": ZERO_A_PLUS,
        "fixed_zero_b": ZERO_B_PLUS,
        "fixed_zero_plus_counts": (
            sum(ZERO_A_PLUS),
            sum(ZERO_B_PLUS),
        ),
        "per_channel_plus_count": CHANNEL_PLUS_COUNT,
        "distinct_coordinate_pairs": len(pair_multiplicities),
        "distinct_projective_ratios": len(ratio_multiplicities),
        "pair_multiplicity_histogram": pair_histogram,
        "ratio_multiplicity_histogram": ratio_histogram,
        "ratio_determines_unique_catalog_scale": True,
        "abstract_norm_minus_one_ratios": abstract_ratio_count,
        "certificate_sha256": certificate_hash,
    }


def verify() -> dict[str, object]:
    return {
        "margin_kernel": verify_phi9_margin_kernel(),
        "catalog_image": verify_catalog_image(),
    }


def main() -> None:
    print(json.dumps(verify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
