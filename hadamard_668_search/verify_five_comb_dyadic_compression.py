#!/usr/bin/env python3
"""Dependency-free verifier for the order-16 dyadic compression theorem.

For four sign rows, compress each row by residue class modulo 16.  The
result is a 4-by-16 integer array ``u``.  This verifier checks, entirely
with integer arithmetic, that the following descriptions are equivalent:

* flat summed spectra at roots of orders 1, 2, 4, 8, and 16;
* the nine symmetric residue-bucket equations for the positive-lag
  aperiodic correlations;
* the flat periodic-autocorrelation identity for the compressed array;
* vanishing of the nine-component quadratic signature ``q(u)``.

It also verifies the associated polarization identity, the physical
84,84,83,83 compression-cell parity shell, its 1,589 magnitude patterns,
and the determinant of the nine spectral bucket equations.  No solver or
third-party package is used.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
from itertools import product
import random
import struct
from typing import Iterable, Sequence


MODULUS = 16
ROW_LENGTHS = (84, 84, 83, 83)
ROOT_ORDERS = (1, 2, 4, 8, 16)

# The coordinates are the symmetric positive-lag residue buckets
# (b_0,b_1,...,b_8).  For 1 <= t <= 7, b_t contains both residues +/-t.
BUCKET_TRANSFORM = (
    (1, 1, 1, 1, 1, 1, 1, 1, 1),       # L1
    (1, -1, 1, -1, 1, -1, 1, -1, 1),   # L2
    (1, 0, -1, 0, 1, 0, -1, 0, 1),     # L4
    (1, 0, 0, 0, -1, 0, 0, 0, 1),      # L8a
    (0, 1, 0, -1, 0, -1, 0, 1, 0),     # L8b
    (1, 0, 0, 0, 0, 0, 0, 0, -1),      # P0
    (0, 1, 0, 0, 0, 0, 0, -1, 0),      # P1
    (0, 0, 1, 0, 0, 0, -1, 0, 0),      # P2
    (0, 0, 0, 1, 0, -1, 0, 0, 0),      # P3
)


Rows = tuple[tuple[int, ...], ...]
Compressed = tuple[tuple[int, ...], ...]
Signature = tuple[int, ...]


def _check_sign_rows(rows: Sequence[Sequence[int]]) -> None:
    if len(rows) > 4:
        raise ValueError("at most four rows are allowed")
    if any(value not in (-1, 1) for row in rows for value in row):
        raise ValueError("source rows must contain only signs")


def compress_mod_16(rows: Sequence[Sequence[int]]) -> Compressed:
    """Return the four-row periodic compression modulo 16."""

    _check_sign_rows(rows)
    result = [[0] * MODULUS for _ in range(4)]
    for row_index, row in enumerate(rows):
        for position, value in enumerate(row):
            result[row_index][position % MODULUS] += value
    return tuple(tuple(row) for row in result)


def aperiodic_correlations(rows: Sequence[Sequence[int]]) -> Signature:
    """Return the summed positive-lag aperiodic correlations."""

    _check_sign_rows(rows)
    maximum = max((len(row) for row in rows), default=0)
    return tuple(
        sum(
            row[position] * row[position + lag]
            for row in rows
            for position in range(len(row) - lag)
        )
        for lag in range(1, maximum)
    )


def correlation_buckets(correlations: Sequence[int]) -> Signature:
    """Compress positive-lag correlations into b_0,...,b_8."""

    buckets = [0] * 9
    for lag, value in enumerate(correlations, start=1):
        residue = lag % MODULUS
        coordinate = min(residue, MODULUS - residue)
        buckets[coordinate] += value
    return tuple(buckets)


def _check_compressed(vector: Sequence[Sequence[int]]) -> None:
    if len(vector) != 4 or any(len(row) != MODULUS for row in vector):
        raise ValueError("a compressed vector must have shape 4 by 16")


def quadratic_signature(
    vector: Sequence[Sequence[int]],
    support_count: int,
) -> Signature:
    """Return q_0,...,q_8 for a compressed vector.

    ``support_count`` is the number of underlying disjoint sign positions.
    In particular, it is additive when two compressed vectors are added.
    """

    _check_compressed(vector)
    norm_excess = (
        sum(value * value for row in vector for value in row)
        - support_count
    )
    if norm_excess % 2:
        raise ValueError("norm and support count have incompatible parity")
    result = [norm_excess // 2]
    for lag in range(1, 8):
        result.append(
            sum(
                row[residue] * row[(residue + lag) % MODULUS]
                for row in vector
                for residue in range(MODULUS)
            )
        )
    lag_eight = sum(
        row[residue] * row[(residue + 8) % MODULUS]
        for row in vector
        for residue in range(MODULUS)
    )
    if lag_eight % 2:
        raise AssertionError("lag-eight cyclic autocorrelation is not even")
    result.append(lag_eight // 2)
    return tuple(result)


def bilinear_signature(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
) -> Signature:
    """Return the polarization B_0,...,B_8 of ``quadratic_signature``."""

    _check_compressed(left)
    _check_compressed(right)
    result = [
        sum(
            left[row][residue] * right[row][residue]
            for row in range(4)
            for residue in range(MODULUS)
        )
    ]
    for lag in range(1, 8):
        result.append(
            sum(
                left[row][residue]
                * right[row][(residue + lag) % MODULUS]
                + right[row][residue]
                * left[row][(residue + lag) % MODULUS]
                for row in range(4)
                for residue in range(MODULUS)
            )
        )
    result.append(
        sum(
            left[row][residue] * right[row][(residue + 8) % MODULUS]
            for row in range(4)
            for residue in range(MODULUS)
        )
    )
    return tuple(result)


def add_compressed(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
) -> Compressed:
    _check_compressed(left)
    _check_compressed(right)
    return tuple(
        tuple(left[row][residue] + right[row][residue] for residue in range(16))
        for row in range(4)
    )


def periodic_autocorrelation(
    vector: Sequence[Sequence[int]],
) -> tuple[int, ...]:
    """Return the summed cyclic autocorrelation on Z/16Z."""

    _check_compressed(vector)
    return tuple(
        sum(
            row[residue] * row[(residue + lag) % MODULUS]
            for row in vector
            for residue in range(MODULUS)
        )
        for lag in range(MODULUS)
    )


def transform_buckets(buckets: Sequence[int]) -> Signature:
    if len(buckets) != 9:
        raise ValueError("there must be nine symmetric residue buckets")
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, buckets))
        for row in BUCKET_TRANSFORM
    )


def _reduce_power(order: int, exponent: int) -> tuple[int, int]:
    """Reduce zeta_order**exponent in the power-of-two cyclotomic basis."""

    if order == 1:
        return 1, 0
    if order == 2:
        return ((1, 0) if exponent % 2 == 0 else (-1, 0))
    degree = order // 2
    exponent %= order
    if exponent >= degree:
        return -1, exponent - degree
    return 1, exponent


def exact_spectral_residual(
    rows: Sequence[Sequence[int]],
    order: int,
) -> Signature:
    """Return exact coefficients of sum |X(zeta_order)|^2 - N.

    The calculation evaluates the source rows directly in
    ``Z[zeta_order]``.  It does not use correlations or residue buckets.
    """

    if order not in ROOT_ORDERS:
        raise ValueError("root order must be one of 1,2,4,8,16")
    _check_sign_rows(rows)
    degree = 1 if order <= 2 else order // 2
    result = [0] * degree
    for row in rows:
        value = [0] * degree
        for position, coefficient in enumerate(row):
            sign, coordinate = _reduce_power(order, position)
            value[coordinate] += sign * coefficient
        for left in range(degree):
            for right in range(degree):
                sign, coordinate = _reduce_power(order, left - right)
                result[coordinate] += (
                    sign * value[left] * value[right]
                )
    result[0] -= sum(len(row) for row in rows)
    return tuple(result)


def predicted_spectral_residuals(
    transformed: Sequence[int],
) -> tuple[Signature, ...]:
    """Translate L1,...,P3 into exact cyclotomic-basis coefficients."""

    if len(transformed) != 9:
        raise ValueError("the transformed bucket vector must have length nine")
    l1, l2, l4, l8a, l8b, p0, p1, p2, p3 = transformed
    return (
        (2 * l1,),
        (2 * l2,),
        (2 * l4, 0),
        (2 * l8a, l8b, 0, -l8b),
        (2 * p0, p1, p2, p3, 0, -p3, -p2, -p1),
    )


def expected_periodic_paf(
    buckets: Sequence[int],
    support_count: int,
) -> Signature:
    if len(buckets) != 9:
        raise ValueError("there must be nine buckets")
    result = [0] * MODULUS
    result[0] = support_count + 2 * buckets[0]
    for lag in range(1, 8):
        result[lag] = buckets[lag]
        result[MODULUS - lag] = buckets[lag]
    result[8] = 2 * buckets[8]
    return tuple(result)


def _pack_ints(values: Iterable[int]) -> bytes:
    values = tuple(values)
    return struct.pack(f"<{len(values)}i", *values)


def verify_sequence_fixture(
    rows: Rows,
    digest: "hashlib._Hash",
) -> bool:
    """Verify every dyadic identity for one source-row fixture."""

    correlations = aperiodic_correlations(rows)
    buckets = correlation_buckets(correlations)
    compressed = compress_mod_16(rows)
    support_count = sum(len(row) for row in rows)
    quadratic = quadratic_signature(compressed, support_count)
    if quadratic != buckets:
        raise AssertionError("quadratic signature does not equal lag buckets")

    observed_paf = periodic_autocorrelation(compressed)
    predicted_paf = expected_periodic_paf(buckets, support_count)
    if observed_paf != predicted_paf:
        raise AssertionError("Z16 compression PAF identity failed")

    transformed = transform_buckets(buckets)
    observed_roots = tuple(
        exact_spectral_residual(rows, order) for order in ROOT_ORDERS
    )
    predicted_roots = predicted_spectral_residuals(transformed)
    if observed_roots != predicted_roots:
        raise AssertionError("exact root/bucket identity failed")

    roots_are_flat = all(
        coefficient == 0
        for residual in observed_roots
        for coefficient in residual
    )
    bucket_equations_hold = all(value == 0 for value in transformed)
    buckets_vanish = all(value == 0 for value in buckets)
    paf_is_flat = observed_paf == (support_count,) + (0,) * 15
    q_vanishes = all(value == 0 for value in quadratic)
    if len(
        {
            roots_are_flat,
            bucket_equations_hold,
            buckets_vanish,
            paf_is_flat,
            q_vanishes,
        }
    ) != 1:
        raise AssertionError("the four dyadic formulations disagree")

    lengths = tuple(len(row) for row in rows) + (0,) * (4 - len(rows))
    digest.update(struct.pack("<4H", *lengths))
    for row in rows:
        digest.update(bytes(1 if value > 0 else 0 for value in row))
    digest.update(_pack_ints(buckets))
    digest.update(_pack_ints(transformed))
    for residual in observed_roots:
        digest.update(_pack_ints(residual))
    return roots_are_flat


def exhaustive_and_random_sequence_checks() -> tuple[int, int, int, int, str]:
    """Run exhaustive short fixtures and deterministic full-size fixtures."""

    digest = hashlib.sha256(b"five-comb-dyadic-sequences-v1\0")
    exhaustive_count = 0
    flat_count = 0
    # Every sign sequence of every length through 13 is checked.
    for length in range(14):
        for mask in range(1 << length):
            row = tuple(
                1 if (mask >> position) & 1 else -1
                for position in range(length)
            )
            flat_count += verify_sequence_fixture((row,), digest)
            exhaustive_count += 1

    special_rows: list[Rows] = []
    for lengths in (
        (15, 16, 17, 18),
        (31, 32, 33, 34),
        ROW_LENGTHS,
    ):
        special_rows.extend(
            (
                tuple(tuple(1 for _ in range(length)) for length in lengths),
                tuple(
                    tuple(1 if position % 2 == 0 else -1 for position in range(length))
                    for length in lengths
                ),
                tuple(
                    tuple(
                        1 if (position + row_index) % 3 else -1
                        for position in range(length)
                    )
                    for row_index, length in enumerate(lengths)
                ),
            )
        )
    for rows in special_rows:
        flat_count += verify_sequence_fixture(rows, digest)

    generator = random.Random(0x668D1A)
    random_count = 768
    for fixture in range(random_count):
        if fixture % 4 == 0:
            lengths = ROW_LENGTHS
        elif fixture % 4 == 1:
            lengths = (17, 16, 15, 14)
        elif fixture % 4 == 2:
            lengths = tuple(generator.randrange(0, 85) for _ in range(4))
        else:
            lengths = (33, 32, 31, 30)
        rows = tuple(
            tuple(
                1 if generator.getrandbits(1) else -1
                for _ in range(length)
            )
            for length in lengths
        )
        flat_count += verify_sequence_fixture(rows, digest)

    if exhaustive_count != (1 << 14) - 1:
        raise AssertionError("exhaustive fixture count changed")
    if flat_count < 3:
        raise AssertionError("expected empty and singleton flat fixtures")
    return (
        exhaustive_count,
        len(special_rows),
        random_count,
        flat_count,
        digest.hexdigest(),
    )


def _compressed_from_state(
    coordinates: Sequence[tuple[int, int]],
    state: Sequence[int],
) -> Compressed:
    result = [[0] * MODULUS for _ in range(4)]
    for (row, residue), value in zip(coordinates, state):
        result[row][residue] = value
    return tuple(tuple(row) for row in result)


def verify_polarization_fixture(
    left: Compressed,
    left_support: int,
    right: Compressed,
    right_support: int,
    digest: "hashlib._Hash",
) -> None:
    combined = add_compressed(left, right)
    observed = quadratic_signature(
        combined, left_support + right_support
    )
    expected = tuple(
        a + b + cross
        for a, b, cross in zip(
            quadratic_signature(left, left_support),
            quadratic_signature(right, right_support),
            bilinear_signature(left, right),
        )
    )
    if observed != expected:
        raise AssertionError("q(u+v)=q(u)+q(v)+B(u,v) failed")
    digest.update(_pack_ints(value for row in left for value in row))
    digest.update(_pack_ints(value for row in right for value in row))
    digest.update(_pack_ints(observed))


def exhaustive_and_random_polarization_checks() -> tuple[int, int, str]:
    """Verify polarization exhaustively on sparse states and randomly."""

    digest = hashlib.sha256(b"five-comb-dyadic-polarization-v1\0")
    exhaustive_count = 0
    states = tuple(product((-1, 0, 1), repeat=3))
    # These eight layouts force every cyclic offset 1,...,8 to occur in
    # an exhaustive fixture, while keeping the Cartesian product small.
    for lag in range(1, 9):
        coordinates = ((0, 0), (0, lag), (1, (3 * lag + 1) % 16))
        for left_state in states:
            left = _compressed_from_state(coordinates, left_state)
            left_support = sum(value != 0 for value in left_state)
            for right_state in states:
                right = _compressed_from_state(coordinates, right_state)
                right_support = sum(value != 0 for value in right_state)
                verify_polarization_fixture(
                    left,
                    left_support,
                    right,
                    right_support,
                    digest,
                )
                exhaustive_count += 1

    generator = random.Random(0x668B11)
    random_count = 768
    for _ in range(random_count):
        vectors = []
        supports = []
        for _side in range(2):
            vector = [[0] * MODULUS for _ in range(4)]
            support = 0
            for row in range(4):
                for residue in range(MODULUS):
                    count = generator.randrange(7)
                    support += count
                    vector[row][residue] = sum(
                        1 if generator.getrandbits(1) else -1
                        for _ in range(count)
                    )
            vectors.append(tuple(tuple(row) for row in vector))
            supports.append(support)
        verify_polarization_fixture(
            vectors[0],
            supports[0],
            vectors[1],
            supports[1],
            digest,
        )
    if exhaustive_count != 8 * 27 * 27:
        raise AssertionError("polarization fixture count changed")
    return exhaustive_count, random_count, digest.hexdigest()


def physical_cell_parities() -> tuple[int, int]:
    """Return the counts of even and odd compression cells."""

    cell_sizes = []
    for length in ROW_LENGTHS:
        sizes = [0] * MODULUS
        for position in range(length):
            sizes[position % MODULUS] += 1
        cell_sizes.extend(sizes)
    even = sum(size % 2 == 0 for size in cell_sizes)
    odd = len(cell_sizes) - even
    if sorted(set(cell_sizes)) != [5, 6]:
        raise AssertionError("physical compression cell sizes changed")

    for size, expected in (
        (5, (-5, -3, -1, 1, 3, 5)),
        (6, (-6, -4, -2, 0, 2, 4, 6)),
    ):
        observed = sorted(
            {
                sum(signs)
                for signs in product((-1, 1), repeat=size)
            }
        )
        if tuple(observed) != expected:
            raise AssertionError("compression-cell alphabet check failed")
    return even, odd


def enumerate_shell_patterns() -> tuple[tuple[int, int, int, int, int], ...]:
    """Enumerate the physical zero-lag shell magnitude patterns.

    ``e_j`` counts even cells of magnitude ``2j`` and ``o_j`` counts odd
    cells of magnitude ``2j+1``.  The returned coordinate order is
    ``(e1,e2,e3,o1,o2)``; the zero-category counts are determined by 14
    and 50.
    """

    patterns = []
    for e1 in range(15):
        for e2 in range(15 - e1):
            for e3 in range(15 - e1 - e2):
                for o1 in range(51):
                    for o2 in range(51 - o1):
                        if (
                            e1
                            + 4 * e2
                            + 9 * e3
                            + 2 * o1
                            + 6 * o2
                            == 71
                        ):
                            patterns.append((e1, e2, e3, o1, o2))
    return tuple(patterns)


def verify_shell_patterns() -> tuple[int, str]:
    patterns = enumerate_shell_patterns()
    if len(patterns) != 1_589:
        raise AssertionError(
            f"expected 1,589 shell patterns, found {len(patterns)}"
        )
    if any((e1 + e3) % 2 != 1 for e1, _e2, e3, _o1, _o2 in patterns):
        raise AssertionError("shell parity e1+e3 odd failed")

    # Independently enumerate all count compositions and use the original
    # squared magnitudes, rather than the reduced shell equation.
    direct = set()
    for e0 in range(15):
        for e1 in range(15 - e0):
            for e2 in range(15 - e0 - e1):
                e3 = 14 - e0 - e1 - e2
                for o0 in range(51):
                    for o1 in range(51 - o0):
                        o2 = 50 - o0 - o1
                        energy = (
                            4 * e1
                            + 16 * e2
                            + 36 * e3
                            + o0
                            + 9 * o1
                            + 25 * o2
                        )
                        if energy == 334:
                            direct.add((e1, e2, e3, o1, o2))
    if direct != set(patterns):
        raise AssertionError("independent shell enumeration disagrees")

    digest = hashlib.sha256(b"five-comb-dyadic-shell-v1\0")
    for pattern in patterns:
        digest.update(bytes(pattern))
    return len(patterns), digest.hexdigest()


def determinant_bareiss(matrix: Sequence[Sequence[int]]) -> int:
    """Compute an exact determinant using fraction-free elimination."""

    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a nonempty square matrix")
    work = [list(row) for row in matrix]
    sign = 1
    denominator = 1
    for column in range(size - 1):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for index in range(column + 1, size):
                numerator = (
                    work[row][index] * pivot
                    - work[row][column] * work[column][index]
                )
                if numerator % denominator:
                    raise AssertionError("Bareiss division was not exact")
                work[row][index] = numerator // denominator
            work[row][column] = 0
        denominator = pivot
    return sign * work[-1][-1]


def determinant_fraction(matrix: Sequence[Sequence[int]]) -> int:
    """Independent exact determinant using rational row elimination."""

    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("determinant requires a nonempty square matrix")
    work = [[Fraction(value) for value in row] for row in matrix]
    determinant = Fraction(1)
    for column in range(size):
        pivot_row = next(
            (row for row in range(column, size) if work[row][column]),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            determinant = -determinant
        pivot = work[column][column]
        determinant *= pivot
        for index in range(column, size):
            work[column][index] /= pivot
        for row in range(column + 1, size):
            multiplier = work[row][column]
            for index in range(column, size):
                work[row][index] -= multiplier * work[column][index]
    if determinant.denominator != 1:
        raise AssertionError("integer matrix acquired noninteger determinant")
    return determinant.numerator


def verify_bucket_basis() -> tuple[int, str]:
    first = determinant_bareiss(BUCKET_TRANSFORM)
    second = determinant_fraction(BUCKET_TRANSFORM)
    if first != second or first != -256:
        raise AssertionError(
            f"bucket transform determinant is {first}, expected -256"
        )
    digest = hashlib.sha256(b"five-comb-dyadic-basis-v1\0")
    for row in BUCKET_TRANSFORM:
        digest.update(_pack_ints(row))
    digest.update(_pack_ints((first,)))
    return first, digest.hexdigest()


def self_validation_checks() -> int:
    """Exercise rejection paths so a vacuous checker cannot report PASS."""

    checks = 0
    nonflat = ((1, 1),)
    correlations = aperiodic_correlations(nonflat)
    buckets = correlation_buckets(correlations)
    if buckets == (0,) * 9:
        raise AssertionError("known nonflat fixture was accepted")
    checks += 1

    compressed = compress_mod_16(nonflat)
    if periodic_autocorrelation(compressed) == (2,) + (0,) * 15:
        raise AssertionError("known nonflat PAF was accepted")
    checks += 1

    corrupted = list(quadratic_signature(compressed, 2))
    corrupted[1] += 1
    if tuple(corrupted) == buckets:
        raise AssertionError("corrupted quadratic signature was accepted")
    checks += 1

    try:
        quadratic_signature(compressed, 1)
    except ValueError:
        checks += 1
    else:
        raise AssertionError("invalid support parity was accepted")

    singular = tuple(BUCKET_TRANSFORM[:-1]) + (BUCKET_TRANSFORM[0],)
    if determinant_bareiss(singular) != 0 or determinant_fraction(singular) != 0:
        raise AssertionError("singular determinant fixture was accepted")
    checks += 1

    if (0, 0, 0, 0, 0) in set(enumerate_shell_patterns()):
        raise AssertionError("invalid zero shell pattern was accepted")
    checks += 1
    return checks


def main() -> None:
    sequence = exhaustive_and_random_sequence_checks()
    polarization = exhaustive_and_random_polarization_checks()
    even_cells, odd_cells = physical_cell_parities()
    shell_count, shell_hash = verify_shell_patterns()
    determinant, basis_hash = verify_bucket_basis()
    rejection_checks = self_validation_checks()

    combined = hashlib.sha256(b"five-comb-dyadic-verifier-v1\0")
    for value in (
        sequence[4],
        polarization[2],
        shell_hash,
        basis_hash,
    ):
        combined.update(bytes.fromhex(value))

    print(
        "PASS roots_Z16_PAF_buckets_q "
        f"exhaustive={sequence[0]} special={sequence[1]} "
        f"random={sequence[2]} flat={sequence[3]} sha256={sequence[4]}"
    )
    print(
        "PASS q_B_polarization "
        f"exhaustive={polarization[0]} random={polarization[1]} "
        f"sha256={polarization[2]}"
    )
    print(
        "PASS physical_parity_shell "
        f"even_cells={even_cells} odd_cells={odd_cells} "
        f"patterns={shell_count} e1_plus_e3=odd sha256={shell_hash}"
    )
    print(
        "PASS integer_bucket_basis "
        f"determinant={determinant} sha256={basis_hash}"
    )
    print(
        "PASS self_validation "
        f"rejection_checks={rejection_checks} "
        f"combined_sha256={combined.hexdigest()}"
    )


if __name__ == "__main__":
    main()
