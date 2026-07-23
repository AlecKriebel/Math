#!/usr/bin/env python3
"""Exact CP-SAT search in the sextic-cyclotomic LP(333) quotient.

The quotient has nine CRT rows and seven column parts

    {0}, C_0, ..., C_5

over F_37.  Its zero-part QPSK word is fixed to the canonical perfect word

    (0,0,0,1,2,3,1,3,2)

of exponents of ``i``.  Every nonzero quotient cell is represented by the two
binary signs (A,B) in the convention

    1 -> (+,+), i -> (-,+), -1 -> (-,-), -i -> (+,-).

Thus there are exactly ``9 * 6 * 2 = 108`` primary Boolean variables.
For every two phases ``z,w``,

    Re(z conjugate(w)) = 1 - (A_z XOR A_w) - (B_z XOR B_w).

The six audited transition matrices therefore turn each quotient correlation
target ``-1`` into a weighted XOR cardinality target ``333 - (-1) = 334``.
There are exactly 34 reversal-inequivalent equations: six at row lag zero,
and seven at each row lag 1 through 4.  Pair XOR variables are cached globally
and reused between equations.

For propagation, each length-nine class word is also channeled to its
canonical four-coordinate real-PAF signature.  The audited target-sum catalog
has 7,056 words and 28 signatures for each of ``-3i`` and ``+3i``.  The three
even classes and three odd classes are channeled through the exact 298
opposite aggregate vectors, representing all 1,658,700 compatible ordered
signature sextuples.  This layer is logically redundant with the pure-column
lag equations and can be disabled to reproduce the original model exactly.

The full sixfold class rotation does not survive both alternating compression
and canonical zero-word normalization.  A rigorously audited residual C3
action does survive: decimation by 226 fixes CRT rows and rotates the class
pairs ``((0,1),(2,3),(4,5))``.  By default the model selects the lexicographically
least of those three pair rotations with a two-Boolean exact tie encoding.
This symmetry channel can be disabled independently.

A solver assignment is never written directly.  It is expanded through the
audited CRT quotient, converted into two length-333 sign sequences, checked by
an independent full 333-lag correlation replay, checked by the repository's
Legendre-pair verifier, expanded to the bordered two-circulant matrix of order
668, and checked for exact Hadamard orthogonality.  Only then is the canonical
candidate JSON saved.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from pathlib import Path
import sys
from typing import Sequence

from ortools.sat.python import cp_model

from check_lp333_sextic_quotient import (
    CLASSES,
    N,
    ROOTS,
    ROWS,
    TRANSITION_MATRICES,
    ZERO_COLUMN_MATRIX,
    crt_correlation_real,
    expand_crt_array,
    expand_length333,
    phase_sum,
    qpsk_to_sign_pair,
    real_paf_exponents,
    quotient_correlation_real,
    quotient_phase_table,
)
from construction import two_circulant_legendre, verify_hadamard
from legendre_333 import save_verified_candidate, verify_legendre_pair


CANONICAL_ZERO_EXPONENTS: tuple[int, ...] = (0, 0, 0, 1, 2, 3, 1, 3, 2)
TARGET_XOR_COUNT = N + 1
PRIMARY_SIGN_BITS = ROWS * len(CLASSES) * 2
SIGNATURE_LAGS = tuple(range(1, (ROWS - 1) // 2 + 1))
C3_DECIMATION = 226

# (A,B) signs to the exponent e in i**e.
SIGN_PAIR_TO_EXPONENT = {
    (1, 1): 0,
    (-1, 1): 1,
    (-1, -1): 2,
    (1, -1): 3,
}

BitNode = int | cp_model.IntVar
Matrix = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class QuotientEquation:
    """One reversal-inequivalent quotient correlation equation."""

    name: str
    row_lag: int
    column_lag: int
    matrix: Matrix


@dataclass
class SexticModel:
    """The model and the metadata required to decode and audit it."""

    model: cp_model.CpModel
    a_nodes: tuple[tuple[BitNode, ...], ...]
    b_nodes: tuple[tuple[BitNode, ...], ...]
    primary_variables: tuple[cp_model.IntVar, ...]
    xor_variables: tuple[cp_model.IntVar, ...]
    signature_variables: tuple[cp_model.IntVar, ...]
    signature_shard_variable: cp_model.IntVar | None
    c3_variables: tuple[cp_model.IntVar, ...]
    equations: tuple[QuotientEquation, ...]
    compression_constraints: int
    signature_constraints: int
    c3_constraints: int

    def exact_counts(self) -> dict[str, int]:
        """Return exact model-size counts from the serialized CP-SAT model."""

        proto = self.model.proto
        return {
            "primary_sign_bits": len(self.primary_variables),
            "cached_xor_variables": len(self.xor_variables),
            "signature_variables": len(self.signature_variables),
            "signature_shard_variables": int(
                self.signature_shard_variable is not None
            ),
            "c3_variables": len(self.c3_variables),
            "total_variables": len(proto.variables),
            "compression_constraints": self.compression_constraints,
            "quotient_lag_constraints": len(self.equations),
            "signature_constraints": self.signature_constraints,
            "c3_constraints": self.c3_constraints,
            "total_constraints": len(proto.constraints),
        }


def quotient_equations() -> tuple[QuotientEquation, ...]:
    """Return the exact 34-equation reversal quotient."""

    equations: list[QuotientEquation] = []
    for class_index, matrix in enumerate(TRANSITION_MATRICES):
        equations.append(
            QuotientEquation(
                name=f"row_0_class_{class_index}",
                row_lag=0,
                column_lag=CLASSES[class_index][0],
                matrix=matrix,
            )
        )
    for row_lag in range(1, (ROWS - 1) // 2 + 1):
        equations.append(
            QuotientEquation(
                name=f"row_{row_lag}_zero_column",
                row_lag=row_lag,
                column_lag=0,
                matrix=ZERO_COLUMN_MATRIX,
            )
        )
        for class_index, matrix in enumerate(TRANSITION_MATRICES):
            equations.append(
                QuotientEquation(
                    name=f"row_{row_lag}_class_{class_index}",
                    row_lag=row_lag,
                    column_lag=CLASSES[class_index][0],
                    matrix=matrix,
                )
            )
    if len(equations) != 34:
        raise AssertionError("the sextic reversal quotient must have 34 equations")
    return tuple(equations)


QUOTIENT_EQUATIONS = quotient_equations()


def real_paf_signature(exponents: Sequence[int]) -> tuple[int, ...]:
    """Return the four reversal-independent real PAF coefficients."""

    if len(exponents) != ROWS:
        raise ValueError("a quotient class word must have length nine")
    return tuple(real_paf_exponents(exponents, lag) for lag in SIGNATURE_LAGS)


@lru_cache(maxsize=2)
def target_phase_word_records(
    imaginary_sum: int,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Enumerate target-sum words and their exact real-PAF signatures."""

    if imaginary_sum not in (-3, 3):
        raise ValueError("target imaginary phase sum must be -3 or +3")
    target = (0, imaginary_sum)
    return tuple(
        (word, real_paf_signature(word))
        for word in product(range(4), repeat=ROWS)
        if phase_sum(word) == target
    )


@lru_cache(maxsize=1)
def canonical_signatures() -> tuple[tuple[int, ...], ...]:
    """Return the common lexicographically ordered catalog of 28 signatures."""

    negative = tuple(
        sorted({signature for _, signature in target_phase_word_records(-3)})
    )
    positive = tuple(
        sorted({signature for _, signature in target_phase_word_records(3)})
    )
    if negative != positive:
        raise AssertionError("+/-3i target words have different PAF signatures")
    if len(negative) != 28:
        raise AssertionError("the audited signature catalog must have size 28")
    return negative


SIGNATURES = canonical_signatures()
SIGNATURE_INDEX = {
    signature: index for index, signature in enumerate(SIGNATURES)
}


@lru_cache(maxsize=2)
def signature_word_table(imaginary_sum: int) -> tuple[tuple[int, ...], ...]:
    """Return ``(A[0:9],B[0:9],signature_id)`` rows for one target sum."""

    rows: list[tuple[int, ...]] = []
    for word, signature in target_phase_word_records(imaginary_sum):
        pairs = tuple(exponent_to_sign_pair(exponent) for exponent in word)
        rows.append(
            tuple(int(pair[0] == 1) for pair in pairs)
            + tuple(int(pair[1] == 1) for pair in pairs)
            + (SIGNATURE_INDEX[signature],)
        )
    if len(rows) != 7_056:
        raise AssertionError("each target-sum word table must have 7,056 rows")
    return tuple(rows)


@lru_cache(maxsize=1)
def signature_triples_by_vector() -> dict[
    tuple[int, ...], tuple[tuple[int, int, int], ...]
]:
    """Group all ordered signature triples by coordinatewise aggregate."""

    buckets: defaultdict[tuple[int, ...], list[tuple[int, int, int]]] = (
        defaultdict(list)
    )
    for triple in product(range(len(SIGNATURES)), repeat=3):
        vector = tuple(
            sum(SIGNATURES[index][coordinate] for index in triple)
            for coordinate in range(len(SIGNATURE_LAGS))
        )
        buckets[vector].append(triple)
    return {
        vector: tuple(triples)
        for vector, triples in sorted(buckets.items())
    }


def negate_signature_vector(vector: Sequence[int]) -> tuple[int, ...]:
    """Negate one four-coordinate aggregate vector."""

    if len(vector) != len(SIGNATURE_LAGS):
        raise ValueError("signature aggregate vector must have four coordinates")
    return tuple(-coordinate for coordinate in vector)


@lru_cache(maxsize=1)
def compatible_signature_shards() -> tuple[tuple[int, ...], ...]:
    """Return the 298 aggregates whose negatives are also triple aggregates."""

    triples = signature_triples_by_vector()
    result = tuple(
        vector
        for vector in triples
        if negate_signature_vector(vector) in triples
    )
    if len(result) != 298:
        raise AssertionError("the audited aggregate shard count must be 298")
    return result


SIGNATURE_SHARD_VECTORS = compatible_signature_shards()


def signature_triples_for_shard(
    shard: int, *, odd: bool = False
) -> tuple[tuple[int, int, int], ...]:
    """Return the even or opposite odd ordered triples for one shard."""

    if not 0 <= shard < len(SIGNATURE_SHARD_VECTORS):
        raise ValueError("signature shard must lie in [0,298)")
    vector = SIGNATURE_SHARD_VECTORS[shard]
    if odd:
        vector = negate_signature_vector(vector)
    return signature_triples_by_vector()[vector]


@lru_cache(maxsize=2)
def aggregate_signature_table(odd: bool) -> tuple[tuple[int, ...], ...]:
    """Return unsharded rows ``(shard_id,sig_1,sig_2,sig_3)``."""

    return tuple(
        (shard, *triple)
        for shard in range(len(SIGNATURE_SHARD_VECTORS))
        for triple in signature_triples_for_shard(shard, odd=odd)
    )


@lru_cache(maxsize=1)
def signature_catalog_counts() -> dict[str, int]:
    """Return the deterministic audited cardinalities of every signature table."""

    even_sizes = tuple(
        len(signature_triples_for_shard(shard))
        for shard in range(len(SIGNATURE_SHARD_VECTORS))
    )
    odd_sizes = tuple(
        len(signature_triples_for_shard(shard, odd=True))
        for shard in range(len(SIGNATURE_SHARD_VECTORS))
    )
    return {
        "negative_target_words": len(target_phase_word_records(-3)),
        "positive_target_words": len(target_phase_word_records(3)),
        "signatures": len(SIGNATURES),
        "signature_shards": len(SIGNATURE_SHARD_VECTORS),
        "minimum_triple_table_rows": min((*even_sizes, *odd_sizes)),
        "maximum_triple_table_rows": max((*even_sizes, *odd_sizes)),
        "unsharded_even_table_rows": sum(even_sizes),
        "unsharded_odd_table_rows": sum(odd_sizes),
        "ordered_signature_sextuples": sum(
            even_sizes[shard] * odd_sizes[shard]
            for shard in range(len(SIGNATURE_SHARD_VECTORS))
        ),
    }


def exponent_to_sign_pair(exponent: int) -> tuple[int, int]:
    """Return the binary sign pair for one exponent of ``i``."""

    if type(exponent) is not int or not 0 <= exponent < 4:
        raise ValueError("QPSK exponent must lie in {0,1,2,3}")
    return qpsk_to_sign_pair(ROOTS[exponent])


def sign_pair_to_exponent(a_sign: int, b_sign: int) -> int:
    """Invert :func:`exponent_to_sign_pair` exactly."""

    try:
        return SIGN_PAIR_TO_EXPONENT[(a_sign, b_sign)]
    except KeyError as error:
        raise ValueError("A and B entries must both be signs") from error


def expected_class_phase_sum(class_index: int) -> tuple[int, int]:
    """Return ``-3i`` on even classes and ``+3i`` on odd classes."""

    if not 0 <= class_index < len(CLASSES):
        raise ValueError("sextic class index must lie in [0,6)")
    return (0, -3 if class_index % 2 == 0 else 3)


def validate_quotient_exponents(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Validate dimensions, canonical zero word, and all seven phase sums."""

    normalized = tuple(tuple(row) for row in exponents)
    if len(normalized) != ROWS or any(len(row) != 7 for row in normalized):
        raise ValueError("expected a 9 by 7 quotient exponent table")
    if any(
        type(exponent) is not int or not 0 <= exponent < 4
        for row in normalized
        for exponent in row
    ):
        raise ValueError("quotient exponents must lie in {0,1,2,3}")
    if tuple(row[0] for row in normalized) != CANONICAL_ZERO_EXPONENTS:
        raise ValueError("quotient zero column is not the fixed canonical word")
    if phase_sum(CANONICAL_ZERO_EXPONENTS) != (1, 0):
        raise AssertionError("canonical zero word no longer sums to one")
    for class_index in range(len(CLASSES)):
        actual = phase_sum(
            tuple(row[class_index + 1] for row in normalized)
        )
        expected = expected_class_phase_sum(class_index)
        if actual != expected:
            raise ValueError(
                f"class {class_index} phase sum is {actual}, expected {expected}"
            )
    return normalized


def expand_sign_sequences(
    exponents: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Expand a validated quotient into its two length-333 sign sequences."""

    normalized = validate_quotient_exponents(exponents)
    qpsk_sequence = expand_length333(expand_crt_array(normalized))
    pairs = tuple(qpsk_to_sign_pair(value) for value in qpsk_sequence)
    return (
        tuple(pair[0] for pair in pairs),
        tuple(pair[1] for pair in pairs),
    )


def weighted_xor_count(
    exponents: Sequence[Sequence[int]],
    row_lag: int,
    matrix: Sequence[Sequence[int]],
) -> int:
    """Evaluate one quotient equation directly as a weighted XOR count."""

    quotient = quotient_phase_table(exponents)
    sign_pairs = tuple(
        tuple(qpsk_to_sign_pair(value) for value in row) for row in quotient
    )
    return sum(
        matrix[left][right]
        * (
            (sign_pairs[row][left][0] != sign_pairs[(row + row_lag) % ROWS][right][0])
            + (sign_pairs[row][left][1] != sign_pairs[(row + row_lag) % ROWS][right][1])
        )
        for row in range(ROWS)
        for left in range(7)
        for right in range(7)
    )


def _cached_xor(
    model: cp_model.CpModel,
    left: BitNode,
    right: BitNode,
    cache: dict[tuple[int, int], cp_model.IntVar],
) -> cp_model.LinearExpr | cp_model.IntVar | int:
    """Return ``left XOR right``, introducing one globally cached variable."""

    left_fixed = type(left) is int
    right_fixed = type(right) is int
    if left_fixed and right_fixed:
        return int(left) ^ int(right)
    if left_fixed:
        variable = right
        if int(left) == 0:
            return variable
        return 1 - variable
    if right_fixed:
        variable = left
        if int(right) == 0:
            return variable
        return 1 - variable

    if left.index == right.index:
        return 0
    key = tuple(sorted((left.index, right.index)))
    difference = cache.get(key)
    if difference is None:
        difference = model.new_bool_var(f"pair_xor_{key[0]}_{key[1]}")
        # left XOR right XOR (NOT difference) must have odd parity, which is
        # exactly equivalent to difference == left XOR right.
        model.add_bool_xor([left, right, difference.negated()]).with_name(
            f"define_pair_xor_{key[0]}_{key[1]}"
        )
        cache[key] = difference
    return difference


def _add_signature_channel(
    model: cp_model.CpModel,
    a_rows: Sequence[Sequence[BitNode]],
    b_rows: Sequence[Sequence[BitNode]],
    signature_shard: int | None,
) -> tuple[
    tuple[cp_model.IntVar, ...],
    cp_model.IntVar | None,
    int,
]:
    """Channel all six class words and their complementary triple aggregate."""

    if signature_shard is not None and not (
        0 <= signature_shard < len(SIGNATURE_SHARD_VECTORS)
    ):
        raise ValueError("signature shard must lie in [0,298)")

    signature_variables = tuple(
        model.new_int_var(
            0, len(SIGNATURES) - 1, f"class_{class_index}_signature"
        )
        for class_index in range(len(CLASSES))
    )
    constraint_count = 0
    for class_index, signature_variable in enumerate(signature_variables):
        imaginary_sum = -3 if class_index % 2 == 0 else 3
        variables = (
            tuple(a_rows[row][class_index + 1] for row in range(ROWS))
            + tuple(b_rows[row][class_index + 1] for row in range(ROWS))
            + (signature_variable,)
        )
        model.add_allowed_assignments(
            variables, signature_word_table(imaginary_sum)
        ).with_name(f"class_{class_index}_word_signature")
        constraint_count += 1

    even_variables = tuple(signature_variables[index] for index in (0, 2, 4))
    odd_variables = tuple(signature_variables[index] for index in (1, 3, 5))
    shard_variable: cp_model.IntVar | None = None
    if signature_shard is None:
        shard_variable = model.new_int_var(
            0, len(SIGNATURE_SHARD_VECTORS) - 1, "signature_shard"
        )
        model.add_allowed_assignments(
            (shard_variable, *even_variables),
            aggregate_signature_table(False),
        ).with_name("even_signature_triple")
        model.add_allowed_assignments(
            (shard_variable, *odd_variables),
            aggregate_signature_table(True),
        ).with_name("odd_signature_triple")
    else:
        model.add_allowed_assignments(
            even_variables,
            signature_triples_for_shard(signature_shard),
        ).with_name(f"even_signature_triple_shard_{signature_shard}")
        model.add_allowed_assignments(
            odd_variables,
            signature_triples_for_shard(signature_shard, odd=True),
        ).with_name(f"odd_signature_triple_shard_{signature_shard}")
    constraint_count += 2
    return signature_variables, shard_variable, constraint_count


def _add_c3_signature_lex_leader(
    model: cp_model.CpModel,
    signature_variables: Sequence[cp_model.IntVar],
) -> tuple[tuple[cp_model.IntVar, ...], int]:
    """Choose the exact least cyclic rotation of three adjacent class pairs.

    Encoding a pair ``(s_even,s_odd)`` as ``28*s_even+s_odd`` preserves its
    lexicographic order.  For three pair codes ``p0,p1,p2``, the word is the
    least cyclic rotation exactly when

        p0 <= p1, p0 <= p2, and p0 == p2 implies p0 == p1.

    The implication is the tie case missed by merely requiring ``p0`` to be
    a minimum.  Two fully reified equality literals give a seven-constraint
    encoding with no large table.
    """

    if len(signature_variables) != len(CLASSES):
        raise ValueError("C3 symmetry requires all six signature variables")
    pair_codes = tuple(
        len(SIGNATURES) * signature_variables[even]
        + signature_variables[even + 1]
        for even in (0, 2, 4)
    )
    model.add(pair_codes[0] <= pair_codes[1]).with_name("c3_pair_0_le_pair_1")
    model.add(pair_codes[0] <= pair_codes[2]).with_name("c3_pair_0_le_pair_2")

    equal_01 = model.new_bool_var("c3_pair_0_eq_pair_1")
    equal_02 = model.new_bool_var("c3_pair_0_eq_pair_2")
    model.add(pair_codes[0] == pair_codes[1]).only_enforce_if(equal_01)
    model.add(pair_codes[0] != pair_codes[1]).only_enforce_if(
        equal_01.negated()
    )
    model.add(pair_codes[0] == pair_codes[2]).only_enforce_if(equal_02)
    model.add(pair_codes[0] != pair_codes[2]).only_enforce_if(
        equal_02.negated()
    )
    model.add_implication(equal_02, equal_01).with_name(
        "c3_last_tie_requires_first_tie"
    )
    return (equal_01, equal_02), 7


def build_model(
    *,
    signature_channel: bool = True,
    signature_shard: int | None = None,
    c3_symmetry: bool = True,
) -> SexticModel:
    """Build the complete exact sextic quotient model."""

    if not signature_channel and signature_shard is not None:
        raise ValueError("a signature shard requires the signature channel")
    model = cp_model.CpModel()
    zero_pairs = tuple(
        exponent_to_sign_pair(exponent) for exponent in CANONICAL_ZERO_EXPONENTS
    )
    a_rows: list[tuple[BitNode, ...]] = []
    b_rows: list[tuple[BitNode, ...]] = []
    primary: list[cp_model.IntVar] = []
    for row in range(ROWS):
        a_row: list[BitNode] = [int(zero_pairs[row][0] == 1)]
        b_row: list[BitNode] = [int(zero_pairs[row][1] == 1)]
        for class_index in range(len(CLASSES)):
            a_variable = model.new_bool_var(f"a_r{row}_c{class_index}")
            b_variable = model.new_bool_var(f"b_r{row}_c{class_index}")
            a_row.append(a_variable)
            b_row.append(b_variable)
            primary.extend((a_variable, b_variable))
        a_rows.append(tuple(a_row))
        b_rows.append(tuple(b_row))

    if len(primary) != PRIMARY_SIGN_BITS:
        raise AssertionError("sextic model must have exactly 108 primary bits")

    compression_constraints = 0
    for class_index in range(len(CLASSES)):
        # sum phase = -3i on even classes gives (sum A,sum B)=(3,-3);
        # +3i on odd classes gives (-3,3).  Nine signs with sum +/-3
        # have respectively six or three positive entries.
        a_plus = 6 if class_index % 2 == 0 else 3
        b_plus = 3 if class_index % 2 == 0 else 6
        model.add(
            sum(a_rows[row][class_index + 1] for row in range(ROWS)) == a_plus
        ).with_name(f"a_class_{class_index}_compression")
        model.add(
            sum(b_rows[row][class_index + 1] for row in range(ROWS)) == b_plus
        ).with_name(f"b_class_{class_index}_compression")
        compression_constraints += 2

    cache: dict[tuple[int, int], cp_model.IntVar] = {}
    for equation in QUOTIENT_EQUATIONS:
        expression: cp_model.LinearExpr | int = 0
        for row in range(ROWS):
            shifted_row = (row + equation.row_lag) % ROWS
            for left in range(7):
                for right in range(7):
                    weight = equation.matrix[left][right]
                    if not weight:
                        continue
                    expression += weight * _cached_xor(
                        model,
                        a_rows[row][left],
                        a_rows[shifted_row][right],
                        cache,
                    )
                    expression += weight * _cached_xor(
                        model,
                        b_rows[row][left],
                        b_rows[shifted_row][right],
                        cache,
                    )
        model.add(expression == TARGET_XOR_COUNT).with_name(
            f"lp333_{equation.name}"
        )

    signature_variables: tuple[cp_model.IntVar, ...] = ()
    signature_shard_variable: cp_model.IntVar | None = None
    signature_constraints = 0
    if signature_channel:
        (
            signature_variables,
            signature_shard_variable,
            signature_constraints,
        ) = _add_signature_channel(
            model, a_rows, b_rows, signature_shard
        )

    c3_variables: tuple[cp_model.IntVar, ...] = ()
    c3_constraints = 0
    if signature_channel and c3_symmetry:
        c3_variables, c3_constraints = _add_c3_signature_lex_leader(
            model, signature_variables
        )

    bundle = SexticModel(
        model=model,
        a_nodes=tuple(a_rows),
        b_nodes=tuple(b_rows),
        primary_variables=tuple(primary),
        xor_variables=tuple(cache.values()),
        signature_variables=signature_variables,
        signature_shard_variable=signature_shard_variable,
        c3_variables=c3_variables,
        equations=QUOTIENT_EQUATIONS,
        compression_constraints=compression_constraints,
        signature_constraints=signature_constraints,
        c3_constraints=c3_constraints,
    )
    counts = bundle.exact_counts()
    if counts["primary_sign_bits"] != PRIMARY_SIGN_BITS:
        raise AssertionError("primary variable count changed")
    if counts["quotient_lag_constraints"] != 34:
        raise AssertionError("quotient equation count changed")
    if counts["total_variables"] != (
        counts["primary_sign_bits"]
        + counts["cached_xor_variables"]
        + counts["signature_variables"]
        + counts["signature_shard_variables"]
        + counts["c3_variables"]
    ):
        raise AssertionError("unexpected variables entered the model")
    if counts["total_constraints"] != (
        counts["cached_xor_variables"]
        + counts["compression_constraints"]
        + counts["quotient_lag_constraints"]
        + counts["signature_constraints"]
        + counts["c3_constraints"]
    ):
        raise AssertionError("unexpected constraints entered the model")
    return bundle


def quotient_exponents_from_solver(
    solver: cp_model.CpSolver, bundle: SexticModel
) -> tuple[tuple[int, ...], ...]:
    """Decode the solver's A/B bits back into the 9 by 7 exponent table."""

    def sign(node: BitNode) -> int:
        value = int(node) if type(node) is int else solver.value(node)
        return 1 if value else -1

    result: list[tuple[int, ...]] = []
    for row in range(ROWS):
        result.append(
            tuple(
                sign_pair_to_exponent(
                    sign(bundle.a_nodes[row][column]),
                    sign(bundle.b_nodes[row][column]),
                )
                for column in range(7)
            )
        )
    normalized = tuple(result)
    validate_quotient_exponents(normalized)
    return normalized


def full_periodic_correlation_replay(
    a: Sequence[int], b: Sequence[int]
) -> tuple[int, ...]:
    """Independently compute and verify all 333 combined periodic PAFs."""

    if len(a) != N or len(b) != N:
        raise ValueError("candidate sequences must both have length 333")
    if any(type(value) is not int or value not in (-1, 1) for value in (*a, *b)):
        raise ValueError("candidate sequences must contain only signs")
    correlations = tuple(
        sum(
            a[index] * a[(index + lag) % N]
            + b[index] * b[(index + lag) % N]
            for index in range(N)
        )
        for lag in range(N)
    )
    if correlations[0] != 2 * N:
        raise ValueError("candidate has the wrong zero-lag norm")
    bad = tuple(
        (lag, value)
        for lag, value in enumerate(correlations[1:], start=1)
        if value != -2
    )
    if bad:
        lag, value = bad[0]
        raise ValueError(
            f"full periodic replay failed at lag {lag}: "
            f"correlation sum {value}; {len(bad)} bad nonzero lags"
        )
    return correlations


def verify_and_save_candidate(
    path: Path, exponents: Sequence[Sequence[int]]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Replay every exact layer, verify H(668), and only then save."""

    normalized = validate_quotient_exponents(exponents)
    quotient = quotient_phase_table(normalized)
    array = expand_crt_array(normalized)
    for equation in QUOTIENT_EQUATIONS:
        distance = weighted_xor_count(
            normalized, equation.row_lag, equation.matrix
        )
        quotient_value = quotient_correlation_real(
            quotient, equation.row_lag, equation.matrix
        )
        direct_value = crt_correlation_real(
            array, equation.row_lag, equation.column_lag
        )
        if distance != N - quotient_value or direct_value != quotient_value:
            raise ValueError(f"quotient replay disagrees for {equation.name}")
        if distance != TARGET_XOR_COUNT:
            raise ValueError(
                f"quotient equation {equation.name} has XOR count {distance}, "
                f"expected {TARGET_XOR_COUNT}"
            )

    a, b = expand_sign_sequences(normalized)
    report = verify_legendre_pair(a, b)
    if not report.valid:
        raise ValueError("expanded assignment failed the exact Legendre-pair verifier")
    full_periodic_correlation_replay(a, b)
    hadamard = two_circulant_legendre(a, b)
    verify_hadamard(hadamard)
    save_verified_candidate(path, a, b)
    return a, b


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=4096,
        help="CP-SAT memory cap in MiB (default: 4096)",
    )
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--log-search-progress", action="store_true")
    parser.add_argument(
        "--signature-shard",
        type=int,
        choices=range(len(SIGNATURE_SHARD_VECTORS)),
        metavar=f"0..{len(SIGNATURE_SHARD_VECTORS) - 1}",
        help=(
            "restrict the exact signature channel to one of the 298 "
            "complementary aggregate vectors"
        ),
    )
    parser.add_argument(
        "--no-signature-channel",
        action="store_true",
        help=(
            "disable the redundant 28-signature/298-shard channel and "
            "reproduce the original 2,970-variable quotient model"
        ),
    )
    parser.add_argument(
        "--no-c3-symmetry",
        action="store_true",
        help=(
            "disable the exact residual C3 lex leader while retaining the "
            "signature channel"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/lp333_sextic_candidate.json"),
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="build and validate the complete model without solving",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.time_limit <= 0:
        print("error: --time-limit must be positive", file=sys.stderr)
        return 2
    if args.workers <= 0:
        print("error: --workers must be positive", file=sys.stderr)
        return 2
    if args.max_memory_mb <= 0:
        print("error: --max-memory-mb must be positive", file=sys.stderr)
        return 2
    if args.no_signature_channel and args.signature_shard is not None:
        print(
            "error: --signature-shard cannot be combined with "
            "--no-signature-channel",
            file=sys.stderr,
        )
        return 2

    bundle = build_model(
        signature_channel=not args.no_signature_channel,
        signature_shard=args.signature_shard,
        c3_symmetry=not args.no_c3_symmetry,
    )
    validation_error = bundle.model.validate()
    counts = bundle.exact_counts()
    for name, value in counts.items():
        print(f"{name}={value}")
    print(f"model_validation={'passed' if not validation_error else 'failed'}")
    if validation_error:
        print(validation_error, file=sys.stderr)
        return 2
    if args.no_signature_channel:
        print("signature_channel=disabled")
    elif args.signature_shard is None:
        print("signature_channel=enabled signature_shards=all")
    else:
        print(
            f"signature_channel=enabled signature_shard={args.signature_shard} "
            f"aggregate={SIGNATURE_SHARD_VECTORS[args.signature_shard]}"
        )
    print(
        "c3_symmetry="
        f"{'enabled' if not args.no_signature_channel and not args.no_c3_symmetry else 'disabled'}"
    )
    if args.build_only:
        return 0

    print(
        f"workers={args.workers} max_memory_mb={args.max_memory_mb} "
        f"time_limit={args.time_limit}"
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    solver.parameters.log_search_progress = args.log_search_progress
    status = solver.solve(bundle.model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.6f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    print(f"solver_booleans={solver.num_booleans}")

    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 1
    try:
        exponents = quotient_exponents_from_solver(solver, bundle)
        verify_and_save_candidate(args.output, exponents)
    except ValueError as error:
        print(f"error=solver assignment failed exact replay: {error}", file=sys.stderr)
        return 3
    print(f"solution={args.output}")
    print("hadamard_order=668")
    print("hadamard_verified=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
