#!/usr/bin/env python3
"""Exact diagonal-code census for constant rank-three generators.

The certified default is a symmetry-reduced obstruction test for

    exp(-z A) (N0 + eta*z^18*J + 19*y^36*J) exp(z A)

over F_37[y]/(y^37).  For each projective rational similarity type of a
rank-three matrix A, it constructs

    W_A = F_A + z^18 F_A,

where F_A is the temporal span obtained from unordered pairs of powers of
A using A=A^T and M=M^T.  Every actual diagonal word belongs to W_A after
forgetting that the conjugated matrices are the fixed N0 and J.  The older,
looser entry-product overcode remains available through ``--code universal``.

The rank-three rational types are enumerated by separating the nilpotent
zero-primary part from the invertible part.  This deliberately includes
types that may not occur for a self-adjoint operator, so emptiness remains
a safe obstruction.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from hashlib import sha256
import importlib.util
from itertools import product
from pathlib import Path
from typing import Iterable, Sequence


P = 37
HERE = Path(__file__).resolve().parent
PROMOTED = (
    HERE.parent
    if (HERE.parent / "verify_rank_two_conjugation_obstruction.py").is_file()
    else HERE.parent / "conference_334_z37_lift"
)
EXPECTED_QUOTIENT_SHA256 = (
    "c5d8765da49deb39c2ff3407b9d0f265e3ca56c1015d5b0075355c53ca60fb5b"
)
DIAGONAL_UPPER_INDICES = (0, 9, 17, 24, 30, 35, 39, 42, 44)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


R = load_module(
    "rank_two_code_base",
    PROMOTED / "verify_rank_two_conjugation_obstruction.py",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def direct_sum_with_zero(
    blocks: Sequence[Sequence[Sequence[int]]],
) -> list[list[int]]:
    """Return one scalar zero block direct-summed with ``blocks``."""

    order = 1 + sum(len(block) for block in blocks)
    result = [[0] * order for _ in range(order)]
    offset = 1
    for block in blocks:
        for i, row in enumerate(block):
            require(len(row) == len(block), "a rational block is not square")
            for j, value in enumerate(row):
                result[offset + i][offset + j] = value % P
        offset += len(block)
    return result


def jordan(size: int, eigenvalue: int) -> list[list[int]]:
    result = [[0] * size for _ in range(size)]
    for i in range(size):
        result[i][i] = eigenvalue % P
        if i + 1 < size:
            result[i][i + 1] = 1
    return result


def companion_quadratic(c1: int, c0: int) -> list[list[int]]:
    """Companion of X^2+c1*X+c0."""

    return [[0, -c0 % P], [1, -c1 % P]]


def companion_cubic(c2: int, c1: int, c0: int) -> list[list[int]]:
    """Companion of X^3+c2*X^2+c1*X+c0."""

    return [
        [0, 0, -c0 % P],
        [1, 0, -c1 % P],
        [0, 1, -c2 % P],
    ]


def matrix_rank(matrix: Sequence[Sequence[int]]) -> int:
    work = [[value % P for value in row] for row in matrix]
    rank = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(rank, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, P)
        work[rank] = [value * inverse % P for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % P
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
    return rank


def matrix_multiply(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
) -> list[list[int]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right))) % P
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def solve_columns(
    columns: Sequence[Sequence[int]],
    target: Sequence[int],
) -> list[int] | None:
    """Solve a full-column-rank linear system over F_37."""

    if not columns:
        return [] if not any(value % P for value in target) else None
    rows = [
        [column[index] % P for column in columns] + [target[index] % P]
        for index in range(len(target))
    ]
    pivot_rows: list[int] = []
    current = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(current, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[current], rows[pivot] = rows[pivot], rows[current]
        inverse = pow(rows[current][column], -1, P)
        rows[current] = [value * inverse % P for value in rows[current]]
        for row in range(len(rows)):
            if row == current or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                (left - factor * right) % P
                for left, right in zip(rows[row], rows[current])
            ]
        pivot_rows.append(current)
        current += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return None
    if current != len(columns):
        raise AssertionError("power columns unexpectedly became dependent")
    solution = [0] * len(columns)
    for row in pivot_rows:
        pivot = next(index for index, value in enumerate(rows[row][:-1]) if value)
        solution[pivot] = rows[row][-1]
    return solution


def minimal_polynomial(
    matrix: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """Return coefficients c_0,...,c_d of the monic minimal polynomial."""

    order = len(matrix)
    identity = [
        [int(i == j) for j in range(order)]
        for i in range(order)
    ]
    powers = [identity]
    for degree in range(1, order + 1):
        powers.append(matrix_multiply(powers[-1], matrix))
        columns = [
            [entry for row in power for entry in row]
            for power in powers[:-1]
        ]
        target = [
            -entry % P
            for row in powers[-1]
            for entry in row
        ]
        solution = solve_columns(columns, target)
        if solution is not None:
            result = tuple(solution + [1])
            require(
                len(result) == degree + 1,
                "minimal-polynomial degree changed",
            )
            return result
    raise AssertionError("minimal polynomial was not found")


@dataclass(frozen=True)
class RationalType:
    family: str
    label: str
    matrix: tuple[tuple[int, ...], ...]


def freeze(matrix: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(value % P for value in row) for row in matrix)


def projective_cubic_coefficients() -> list[tuple[int, int, int]]:
    representatives = set()
    for c2 in range(P):
        for c1 in range(P):
            for c0 in range(1, P):
                orbit = {
                    (
                        scalar * c2 % P,
                        scalar * scalar * c1 % P,
                        pow(scalar, 3, P) * c0 % P,
                    )
                    for scalar in range(1, P)
                }
                representatives.add(min(orbit))
    result = sorted(representatives)
    require(len(result) == 1371, "cubic projective class count changed")
    return result


def projective_quadratic_coefficients() -> list[tuple[int, int]]:
    representatives = set()
    for c1 in range(P):
        for c0 in range(1, P):
            orbit = {
                (
                    scalar * c1 % P,
                    scalar * scalar * c0 % P,
                )
                for scalar in range(1, P)
            }
            representatives.add(min(orbit))
    result = sorted(representatives)
    require(len(result) == 38, "quadratic projective class count changed")
    return result


def rational_types() -> list[RationalType]:
    """Enumerate a projectively complete over-list of rank-three types."""

    result: list[RationalType] = []

    # Invertible dimension three: every cyclic class, followed by the
    # noncyclic repeated-eigenvalue classes.
    for c2, c1, c0 in projective_cubic_coefficients():
        matrix = direct_sum_with_zero([companion_cubic(c2, c1, c0)])
        result.append(
            RationalType(
                "invertible3_cyclic",
                f"cubic_{c2}_{c1}_{c0}",
                freeze(matrix),
            )
        )
    for ratio in range(2, P):
        matrix = direct_sum_with_zero(
            [[[1, 0, 0], [0, 1, 0], [0, 0, ratio]]]
        )
        result.append(
            RationalType(
                "invertible3_repeated_semisimple",
                f"diag_1_1_{ratio}",
                freeze(matrix),
            )
        )
    result.append(
        RationalType(
            "invertible3_scalar",
            "scalar_1",
            freeze(
                direct_sum_with_zero(
                    [[[1, 0, 0], [0, 1, 0], [0, 0, 1]]]
                )
            ),
        )
    )
    result.append(
        RationalType(
            "invertible3_J2_plus_line",
            "J2_1_plus_1",
            freeze(direct_sum_with_zero([jordan(2, 1), [[1]]])),
        )
    )

    # One zero J2 block plus an invertible two-dimensional part.
    for c1, c0 in projective_quadratic_coefficients():
        matrix = direct_sum_with_zero(
            [jordan(2, 0), companion_quadratic(c1, c0)]
        )
        result.append(
            RationalType(
                "zero_J2_plus_invertible2_cyclic",
                f"J2zero_quad_{c1}_{c0}",
                freeze(matrix),
            )
        )
    result.append(
        RationalType(
            "zero_J2_plus_invertible2_scalar",
            "J2zero_plus_scalar1",
            freeze(
                direct_sum_with_zero(
                    [jordan(2, 0), [[1, 0], [0, 1]]]
                )
            ),
        )
    )

    # Invertible dimension one plus zero-primary rank two.
    result.extend(
        [
            RationalType(
                "zero_rank2_plus_line",
                "J3zero_plus_1",
                freeze(direct_sum_with_zero([jordan(3, 0), [[1]]])),
            ),
            RationalType(
                "zero_rank2_plus_line",
                "J2zero_J2zero_plus_1",
                freeze(
                    direct_sum_with_zero(
                        [jordan(2, 0), jordan(2, 0), [[1]]]
                    )
                ),
            ),
        ]
    )

    # Pure zero-primary rank three.
    result.extend(
        [
            RationalType(
                "nilpotent_rank3",
                "J4zero",
                freeze(direct_sum_with_zero([jordan(4, 0)])),
            ),
            RationalType(
                "nilpotent_rank3",
                "J3zero_J2zero",
                freeze(
                    direct_sum_with_zero([jordan(3, 0), jordan(2, 0)])
                ),
            ),
            RationalType(
                "nilpotent_rank3",
                "J2zero_J2zero_J2zero",
                freeze(
                    direct_sum_with_zero(
                        [jordan(2, 0), jordan(2, 0), jordan(2, 0)]
                    )
                ),
            ),
        ]
    )

    require(len(result) == 1452, "rank-three rational type count changed")
    require(
        all(matrix_rank(record.matrix) == 3 for record in result),
        "a listed rational type lost rank three",
    )
    return result


@dataclass
class WordCensus:
    count: int
    weights: Counter[int]
    words: list[tuple[int, ...]]


def multiply_by_indeterminate_mod(
    value: Sequence[int],
    modulus: Sequence[int],
) -> list[int]:
    """Multiply by T in F_37[T]/(modulus)."""

    degree = len(modulus) - 1
    require(modulus[-1] == 1, "minimal polynomial is not monic")
    leading = value[-1]
    result = [0] + list(value[:-1])
    if leading:
        result = [
            (entry - leading * modulus[index]) % P
            for index, entry in enumerate(result)
        ]
    require(len(result) == degree, "quotient-algebra dimension changed")
    return result


def exponential_algebra_coefficients(
    modulus: Sequence[int],
    sign: int,
) -> list[list[int]]:
    """Expand exp(sign*z*A) in 1,A,... modulo the minimal polynomial."""

    degree = len(modulus) - 1
    result = [[0] * P for _ in range(degree)]
    result[0] = R.ONE[:]
    matrix_power = [1] + [0] * (degree - 1)
    z_power = R.ONE[:]
    factorial = 1
    for exponent in range(1, P):
        matrix_power = multiply_by_indeterminate_mod(matrix_power, modulus)
        z_power = R.polynomial_multiply(z_power, R.LOGARITHM)
        factorial = factorial * exponent % P
        scalar = pow(factorial, -1, P)
        if sign < 0 and exponent % 2:
            scalar = -scalar % P
        for index, coefficient in enumerate(matrix_power):
            if coefficient:
                result[index] = R.polynomial_add(
                    result[index],
                    R.polynomial_scale(
                        z_power, scalar * coefficient % P
                    ),
                )
    return result


def symmetric_diagonal_code(
    matrix: Sequence[Sequence[int]],
) -> tuple[list[list[int]], list[int]]:
    """Safe code using A=A^T and M=M^T.

    If exp(±zA)=sum_r f_r^± A^r, then transposition identifies the
    diagonal coefficients for (r,s) and (s,r).  Allowing the resulting
    symmetric matrix coefficients to vary independently gives a safe
    overcode with at most twice binomial(m+1,2) generators.
    """

    functions, _ = symmetric_coefficient_functions(matrix)
    generators: list[list[int]] = []
    for value in functions:
        generators.append(R.y_to_x_coefficients(value))
        generators.append(
            R.y_to_x_coefficients(
                R.polynomial_multiply(R.HALF_POWER, value)
            )
        )
    return R.reduced_row_basis(generators)


def symmetric_coefficient_functions(
    matrix: Sequence[Sequence[int]],
) -> tuple[list[list[int]], list[tuple[int, int]]]:
    """Temporal functions indexed by unordered pairs of powers of A."""

    modulus = minimal_polynomial(matrix)
    negative = exponential_algebra_coefficients(modulus, -1)
    positive = exponential_algebra_coefficients(modulus, 1)
    functions = []
    pairs = []
    for first in range(len(modulus) - 1):
        for second in range(first, len(modulus) - 1):
            value = R.polynomial_multiply(
                negative[first], positive[second]
            )
            if first != second:
                value = R.polynomial_add(
                    value,
                    R.polynomial_multiply(
                        negative[second], positive[first]
                    ),
                )
            functions.append(value)
            pairs.append((first, second))
    return functions, pairs


def reduce_by_basis(
    vector: Sequence[int],
    basis: Sequence[Sequence[int]],
    pivots: Sequence[int],
) -> list[int]:
    result = [value % P for value in vector]
    for row, pivot in zip(basis, pivots):
        if result[pivot]:
            factor = result[pivot]
            result = [
                (left - factor * right) % P
                for left, right in zip(result, row)
            ]
    return result


@dataclass
class FixedJResult:
    ordinary_rank: int
    half_quotient_rank: int
    attainable_syndromes_both_orientations: int
    survivor_count: int
    survivor_weights: Counter[int]


def fixed_j_local_closure(
    matrix: Sequence[Sequence[int]],
    words: Sequence[Sequence[int]],
) -> FixedJResult:
    """Restore the fixed rank-one J term, with local powers fully relaxed."""

    functions, pairs = symmetric_coefficient_functions(matrix)
    ordinary_rows = [R.y_to_x_coefficients(value) for value in functions]
    half_rows = [
        R.y_to_x_coefficients(
            R.polynomial_multiply(R.HALF_POWER, value)
        )
        for value in functions
    ]
    ordinary_basis, ordinary_pivots = R.reduced_row_basis(ordinary_rows)
    half_remainders = [
        reduce_by_basis(row, ordinary_basis, ordinary_pivots)
        for row in half_rows
    ]
    half_basis, half_pivots = R.reduced_row_basis(half_remainders)

    generator_information = [
        tuple(row[pivot] for pivot in half_pivots)
        for row in half_remainders
    ]
    target_information = []
    for word in words:
        remainder = reduce_by_basis(word, ordinary_basis, ordinary_pivots)
        information = tuple(remainder[pivot] for pivot in half_pivots)
        require(
            not any(reduce_by_basis(remainder, half_basis, half_pivots)),
            "a combined-code word left the half quotient",
        )
        target_information.append(information)

    algebra_degree = len(minimal_polynomial(matrix)) - 1
    attainable: set[tuple[int, ...]] = set()
    for tail in product(range(P), repeat=algebra_degree - 1):
        values = (1,) + tail
        coefficients = [
            values[first] * values[second] % P
            for first, second in pairs
        ]
        information = tuple(
            sum(
                coefficient * generator[index]
                for coefficient, generator in zip(
                    coefficients, generator_information
                )
            )
            % P
            for index in range(len(half_pivots))
        )
        attainable.add(information)
        attainable.add(tuple(-value % P for value in information))

    survivor_weights: Counter[int] = Counter()
    survivors = 0
    for word, information in zip(words, target_information):
        if information in attainable:
            survivors += 1
            survivor_weights[
                sum(value - 18 for value in word[1:])
            ] += 1

    return FixedJResult(
        ordinary_rank=len(ordinary_basis),
        half_quotient_rank=len(half_basis),
        attainable_syndromes_both_orientations=len(attainable),
        survivor_count=survivors,
        survivor_weights=survivor_weights,
    )


def packed_key(values: Sequence[int]) -> tuple[int, ...]:
    return tuple(values)


def compatible_binary_word_census(
    basis: Sequence[Sequence[int]],
    pivots: Sequence[int],
) -> WordCensus:
    """Meet-in-the-middle intersection with {0} x {18,19}^36."""

    require(pivots and pivots[0] == 0, "constant pivot disappeared")
    is_pivot = set(pivots)
    checks = [coordinate for coordinate in range(P) if coordinate not in is_pivot]
    bit_rows = [list(row) for row in basis[1:]]
    information_bits = len(bit_rows)
    require(information_bits <= 25, "rank-three information set exceeded 25")

    base = [
        sum(18 * row[coordinate] for row in bit_rows) % P
        for coordinate in checks
    ]
    left_bits = information_bits // 2
    right_bits = information_bits - left_bits
    keyed = min(6, len(checks))

    def subset_sums(begin: int, count: int) -> list[list[int]]:
        result = [[0] * len(checks) for _ in range(1 << count)]
        for mask in range(1, 1 << count):
            bit = mask & -mask
            offset = bit.bit_length() - 1
            previous = mask ^ bit
            row = bit_rows[begin + offset]
            result[mask] = [
                (value + row[coordinate]) % P
                for value, coordinate in zip(result[previous], checks)
            ]
        return result

    left_sums = subset_sums(0, left_bits)
    right_sums = subset_sums(left_bits, right_bits)
    buckets: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for mask, values in enumerate(right_sums):
        buckets[packed_key(values[:keyed])].append(mask)

    count = 0
    weights: Counter[int] = Counter()
    words: list[tuple[int, ...]] = []
    for left_mask, left in enumerate(left_sums):
        for target_mask in range(1 << keyed):
            needed = [
                (
                    18
                    + ((target_mask >> index) & 1)
                    - base[index]
                    - left[index]
                )
                % P
                for index in range(keyed)
            ]
            for right_mask in buckets.get(packed_key(needed), ()):
                right = right_sums[right_mask]
                if any(
                    (base[index] + left[index] + right[index]) % P
                    not in (18, 19)
                    for index in range(keyed, len(checks))
                ):
                    continue

                # Pivot values are exactly the selected 18/19 coefficients.
                weight = left_mask.bit_count() + right_mask.bit_count()
                # Nonpivot target bits contribute as well.
                for index in range(len(checks)):
                    value = (base[index] + left[index] + right[index]) % P
                    weight += value - 18
                word = [0] * P
                for row_index, row in enumerate(bit_rows):
                    bit = (
                        (left_mask >> row_index) & 1
                        if row_index < left_bits
                        else (right_mask >> (row_index - left_bits)) & 1
                    )
                    coefficient = 18 + bit
                    if coefficient:
                        word = [
                            (left_value + coefficient * right_value) % P
                            for left_value, right_value in zip(word, row)
                        ]
                require(
                    word[0] == 0
                    and all(value in (18, 19) for value in word[1:]),
                    "MITM reconstructed a nonbinary word",
                )
                count += 1
                weights[weight] += 1
                words.append(tuple(word))
    require(len(set(words)) == count, "MITM emitted a duplicate word")
    return WordCensus(count, weights, words)


def quotient_profiles(path: Path) -> list[tuple[int, tuple[int, ...]]]:
    raw = path.read_bytes()
    require(
        sha256(raw).hexdigest() == EXPECTED_QUOTIENT_SHA256,
        "canonical quotient dump hash changed",
    )
    result = []
    for line in raw.decode().splitlines():
        if not line.startswith("canonical_upper "):
            continue
        fields = line.split()
        index = int(fields[1])
        upper = list(map(int, fields[2:]))
        require(len(upper) == 45, "canonical upper triangle changed")
        profile = tuple(
            sorted((36 - upper[position]) // 2 for position in DIAGONAL_UPPER_INDICES)
        )
        result.append((index, profile))
    require(len(result) == 625, "quotient class count changed")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--quotients",
        type=Path,
        default=Path("/tmp/z37_quotients_canonical.txt"),
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--code",
        choices=("symmetric", "universal"),
        default="symmetric",
        help="Use the self-adjoint/symmetric-M overcode or the looser entry-product code.",
    )
    parser.add_argument(
        "--fixed-j",
        action="store_true",
        help="For quotient-compatible symmetric-code types, restore the local fixed-J Veronese constraint.",
    )
    parser.add_argument("--verbose-survivors", action="store_true")
    args = parser.parse_args()

    types = rational_types()
    if args.limit is not None:
        types = types[: args.limit]

    profiles = quotient_profiles(args.quotients)
    records = []
    dimension_distribution: Counter[int] = Counter()
    word_count_distribution: Counter[int] = Counter()
    family_survivors: Counter[str] = Counter()
    survivor_signatures: Counter[tuple[object, ...]] = Counter()
    signature_examples: dict[tuple[object, ...], str] = {}
    compatible_type_count = 0
    fixed_j_type_survivors = 0
    fixed_j_family_survivors: Counter[str] = Counter()
    fixed_j_signature_distribution: Counter[tuple[object, ...]] = Counter()

    for ordinal, record in enumerate(types, 1):
        if args.code == "symmetric":
            basis, pivots = symmetric_diagonal_code(record.matrix)
        else:
            basis, pivots = R.universal_diagonal_code(record.matrix)
        census = compatible_binary_word_census(basis, pivots)
        weights = set(census.weights)
        compatible_classes = [
            index
            for index, profile in profiles
            if set(profile) <= weights
        ]
        dimension_distribution[len(basis)] += 1
        word_count_distribution[census.count] += 1
        if compatible_classes:
            compatible_type_count += 1
            family_survivors[record.family] += 1
            class_digest = sha256(
                ",".join(map(str, compatible_classes)).encode()
            ).hexdigest()[:16]
            signature = (
                record.family,
                len(basis),
                census.count,
                tuple(sorted(census.weights.items())),
                len(compatible_classes),
                class_digest,
            )
            survivor_signatures[signature] += 1
            signature_examples.setdefault(signature, record.label)
            records.append(
                (
                    ordinal,
                    record.family,
                    record.label,
                    len(basis),
                    census.count,
                    tuple(sorted(census.weights.items())),
                    tuple(compatible_classes),
                )
            )
            if args.fixed_j:
                require(
                    args.code == "symmetric",
                    "fixed-J closure requires the symmetric temporal code",
                )
                closure = fixed_j_local_closure(record.matrix, census.words)
                fixed_j_signature_distribution[
                    (
                        closure.ordinary_rank,
                        closure.half_quotient_rank,
                        closure.attainable_syndromes_both_orientations,
                        closure.survivor_count,
                        tuple(sorted(closure.survivor_weights.items())),
                    )
                ] += 1
                if closure.survivor_count:
                    fixed_j_type_survivors += 1
                    fixed_j_family_survivors[record.family] += 1
        if ordinal % 100 == 0:
            print(f"progress={ordinal}/{len(types)}", flush=True)

    if args.limit is None and args.code == "symmetric":
        require(
            dimension_distribution
            == Counter({14: 1270, 12: 97, 10: 41, 8: 38, 6: 4, 4: 2}),
            "rank-three code-dimension census changed",
        )
        require(
            word_count_distribution
            == Counter(
                {
                    2: 492,
                    4: 673,
                    8: 8,
                    16: 82,
                    32: 19,
                    64: 56,
                    128: 114,
                    256: 8,
                }
            ),
            "rank-three binary-word census changed",
        )
        require(
            compatible_type_count == 960,
            "rank-three quotient-compatible type count changed",
        )
        require(
            family_survivors
            == Counter(
                {
                    "invertible3_cyclic": 901,
                    "invertible3_repeated_semisimple": 35,
                    "invertible3_scalar": 1,
                    "invertible3_J2_plus_line": 1,
                    "zero_J2_plus_invertible2_cyclic": 19,
                    "zero_J2_plus_invertible2_scalar": 1,
                    "zero_rank2_plus_line": 2,
                }
            ),
            "rank-three quotient-compatible family census changed",
        )
        if args.fixed_j:
            require(
                sum(fixed_j_signature_distribution.values()) == 960,
                "fixed-J closure did not cover every residual type",
            )
            require(
                fixed_j_type_survivors == 0
                and not fixed_j_family_survivors,
                "a constant symmetric rank-three type survived fixed J",
            )

    print(f"rational_types_checked={len(types)}")
    print(f"diagonal_code={args.code}")
    print(
        "code_dimension_distribution="
        + ",".join(f"{key}:{value}" for key, value in sorted(dimension_distribution.items()))
    )
    print(
        "compatible_word_count_distribution="
        + ",".join(f"{key}:{value}" for key, value in sorted(word_count_distribution.items()))
    )
    print(f"quotient_compatible_type_count={compatible_type_count}")
    print(
        "quotient_compatible_family_distribution="
        + ",".join(f"{key}:{value}" for key, value in sorted(family_survivors.items()))
    )
    if args.fixed_j:
        print(f"fixed_j_type_survivors={fixed_j_type_survivors}")
        print(
            "fixed_j_family_survivors="
            + ",".join(
                f"{key}:{value}"
                for key, value in sorted(fixed_j_family_survivors.items())
            )
        )
        for signature, multiplicity in sorted(
            fixed_j_signature_distribution.items(), key=lambda item: repr(item[0])
        ):
            ordinary, half_rank, attainable, survivors, weights = signature
            print(
                "fixed_j_signature "
                f"multiplicity={multiplicity} ordinary_rank={ordinary} "
                f"half_quotient_rank={half_rank} "
                f"attainable_syndromes={attainable} "
                f"survivor_words={survivors} weights={weights}"
            )
        if args.limit is None:
            print("constant_symmetric_rank3=IMPOSSIBLE")
            print("certificate=PASS")
    for signature, multiplicity in sorted(
        survivor_signatures.items(), key=lambda item: repr(item[0])
    ):
        family, dimension, count, weights, class_count, class_digest = signature
        print(
            "survivor_signature "
            f"family={family} multiplicity={multiplicity} "
            f"example={signature_examples[signature]} "
            f"dimension={dimension} words={count} "
            f"weights={weights} compatible_classes={class_count} "
            f"class_digest={class_digest}"
        )
    if args.verbose_survivors:
        for item in records:
            ordinal, family, label, dimension, count, weights, classes = item
            print(
                "survivor "
                f"ordinal={ordinal} family={family} label={label} "
                f"dimension={dimension} words={count} "
                f"weights={weights} classes={classes}"
            )


if __name__ == "__main__":
    main()
