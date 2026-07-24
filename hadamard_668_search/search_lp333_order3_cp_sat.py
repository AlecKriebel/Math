#!/usr/bin/env python3
"""Exact CP-SAT search in the order-three cyclotomic LP(333) quotient.

The quotient is a 9 by 13 QPSK table over

    {0}, C_0, ..., C_11,

where ``C_j=2^j <2^12>`` in ``F_37``.  The canonical zero column is fixed,
leaving exactly ``9*12*2=216`` binary A/B signs.  The 58
reversal-independent quotient correlations are imposed through globally
cached XOR variables and exact cyclotomic transition matrices.

The complete catalog of 1,756 feasible order-three row-sum PAF words is an
exact redundant channel.  It can also be fixed one row at a time to make
future searches resumable.  A residual sixfold class rotation induced by
decimation 226 is broken by selecting the lexicographically least rotation
of six 36-bit adjacent-class blocks.  The commuting B-only involution

    A'(r,C_j)=A(r,C_j),  B'(r,C_j)=B(3-r,C_{j+6})

is the affine map ``B'[n]=B[323*n+111]``.  The default leader compares one
consistent full 216-bit encoding against all eleven nonidentity images of
the complete ``C6 x C2`` action.  The tempting class-fixed multiplier 260 is
not a symmetry in this order-three quotient and is deliberately not used.

No solver assignment is written directly.  It must pass the quotient replay,
all 333 periodic Legendre-pair correlations, and the exact order-668
Hadamard verification before the candidate JSON is saved.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from io import StringIO
from pathlib import Path
import sys
from typing import Sequence, Union

from ortools.sat.python import cp_model

from verify_lp333_order3_quotient import (
    CANONICAL_ZERO_EXPONENTS,
    CLASS_COUNT,
    CLASSES,
    N,
    PAIR_TO_EXPONENT,
    QUOTIENT_EQUATIONS,
    ROOTS,
    ROWS,
    SIGN_PAIRS,
    TARGET_XOR_COUNT,
    QuotientEquation,
    verify_and_save_candidate,
)


PRIMARY_SIGN_BITS = ROWS * CLASS_COUNT * 2
ROW_SUM_CATALOG_PATH = (
    Path(__file__).resolve().parent
    / "output"
    / "lp333_order3_row_sum_catalog.csv"
)
ROW_SUM_CATALOG_SHA256 = (
    "e8631dc0ae2f65c475af1c2e13429778f666a0fa8a13c9f1153d07d7883a98ea"
)
ROW_SUM_CATALOG_SIZE = 1_756
ROW_SUM_HEADER = tuple(
    coordinate
    for row in range(ROWS)
    for coordinate in (f"s{row}_real", f"s{row}_imag")
)

BitNode = Union[int, cp_model.IntVar]


@dataclass
class Order3Model:
    """The model plus every object needed for exact decoding and audits."""

    model: cp_model.CpModel
    a_nodes: tuple[tuple[BitNode, ...], ...]
    b_nodes: tuple[tuple[BitNode, ...], ...]
    primary_variables: tuple[cp_model.IntVar, ...]
    xor_variables: tuple[cp_model.IntVar, ...]
    row_sum_variables: tuple[cp_model.IntVar, ...]
    c6_variables: tuple[cp_model.IntVar, ...]
    c2_variables: tuple[cp_model.IntVar, ...]
    equations: tuple[QuotientEquation, ...]
    compression_constraints: int
    row_sum_constraints: int
    c6_constraints: int
    c2_constraints: int

    def exact_counts(self) -> dict[str, int]:
        proto = self.model.proto
        return {
            "primary_sign_bits": len(self.primary_variables),
            "cached_xor_variables": len(self.xor_variables),
            "row_sum_variables": len(self.row_sum_variables),
            "c6_variables": len(self.c6_variables),
            "c2_variables": len(self.c2_variables),
            "compression_constraints": self.compression_constraints,
            "quotient_lag_constraints": len(self.equations),
            "row_sum_constraints": self.row_sum_constraints,
            "c6_constraints": self.c6_constraints,
            "c2_constraints": self.c2_constraints,
            "total_variables": len(proto.variables),
            "total_constraints": len(proto.constraints),
        }


def _real_paf(sequence: Sequence[tuple[int, int]], lag: int) -> int:
    return sum(
        sequence[index][0] * sequence[(index + lag) % ROWS][0]
        + sequence[index][1] * sequence[(index + lag) % ROWS][1]
        for index in range(ROWS)
    )


@lru_cache(maxsize=1)
def row_sum_catalog() -> tuple[tuple[int, ...], ...]:
    """Load, pin, and convert all 1,756 full row sums to aggregate ``t``."""

    payload = ROW_SUM_CATALOG_PATH.read_bytes()
    actual_hash = sha256(payload).hexdigest()
    if actual_hash != ROW_SUM_CATALOG_SHA256:
        raise AssertionError(
            f"row-sum catalog hash changed: {actual_hash} "
            f"!= {ROW_SUM_CATALOG_SHA256}"
        )
    rows = list(csv.reader(StringIO(payload.decode("ascii"), newline="")))
    if not rows or tuple(rows[0]) != ROW_SUM_HEADER:
        raise AssertionError("row-sum catalog header changed")

    zero = tuple(ROOTS[value] for value in CANONICAL_ZERO_EXPONENTS)
    result: list[tuple[int, ...]] = []
    full_words: set[tuple[tuple[int, int], ...]] = set()
    for raw in rows[1:]:
        if len(raw) != 2 * ROWS:
            raise AssertionError("row-sum catalog row has the wrong width")
        values = tuple(int(value) for value in raw)
        full = tuple(
            (values[2 * row], values[2 * row + 1]) for row in range(ROWS)
        )
        if sum(value[0] for value in full) != 1 or sum(
            value[1] for value in full
        ) != 0:
            raise AssertionError("catalog row has the wrong total")
        if _real_paf(full, 0) != 297 or tuple(
            _real_paf(full, lag) for lag in range(1, 5)
        ) != (-37, -37, -37, -37):
            raise AssertionError("catalog row has the wrong PAF")
        aggregate: list[int] = []
        if len(full) != len(zero):
            raise AssertionError("row-sum and zero words have different lengths")
        for value, core in zip(full, zero):
            difference = value[0] - core[0], value[1] - core[1]
            if difference[0] % 3 or difference[1] % 3:
                raise AssertionError("catalog row is not x+3t")
            aggregate.extend((difference[0] // 3, difference[1] // 3))
        result.append(tuple(aggregate))
        full_words.add(full)
    if len(result) != ROW_SUM_CATALOG_SIZE or len(full_words) != len(result):
        raise AssertionError("row-sum catalog count or uniqueness changed")
    if len(set(result)) != len(result):
        raise AssertionError("aggregate catalog contains duplicates")
    return tuple(result)


def _cached_xor(
    model: cp_model.CpModel,
    left: BitNode,
    right: BitNode,
    cache: dict[tuple[int, int], cp_model.IntVar],
) -> cp_model.LinearExpr | cp_model.IntVar | int:
    """Return ``left XOR right``, sharing every variable-variable pair."""

    if type(left) is int and type(right) is int:
        return int(left) ^ int(right)
    if type(left) is int:
        return right if int(left) == 0 else 1 - right
    if type(right) is int:
        return left if int(right) == 0 else 1 - left
    if left.index == right.index:
        return 0
    key = tuple(sorted((left.index, right.index)))
    difference = cache.get(key)
    if difference is None:
        difference = model.new_bool_var(f"pair_xor_{key[0]}_{key[1]}")
        model.add_bool_xor((left, right, difference.negated())).with_name(
            f"define_pair_xor_{key[0]}_{key[1]}"
        )
        cache[key] = difference
    return difference


def _add_lex_less_or_equal(
    model: cp_model.CpModel,
    left: Sequence[cp_model.IntVar],
    right: Sequence[cp_model.IntVar],
    name: str,
) -> tuple[tuple[cp_model.IntVar, ...], int]:
    """Add an exact integer-vector ``left <=lex right`` constraint."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    if not left:
        return (), 0

    auxiliaries: list[cp_model.IntVar] = []
    model.add(left[0] <= right[0]).with_name(f"{name}_position_0")
    constraint_count = 1
    if len(left) == 1:
        return (), constraint_count

    prefix = model.new_bool_var(f"{name}_equal_through_0")
    auxiliaries.append(prefix)
    model.add(left[0] == right[0]).only_enforce_if(prefix)
    model.add(left[0] != right[0]).only_enforce_if(prefix.negated())
    constraint_count += 2

    for position in range(1, len(left)):
        model.add(left[position] <= right[position]).only_enforce_if(prefix)
        constraint_count += 1
        if position + 1 == len(left):
            break
        next_prefix = model.new_bool_var(
            f"{name}_equal_through_{position}"
        )
        auxiliaries.append(next_prefix)
        model.add_implication(next_prefix, prefix)
        model.add(left[position] == right[position]).only_enforce_if(
            next_prefix
        )
        model.add(left[position] != right[position]).only_enforce_if(
            (prefix, next_prefix.negated())
        )
        constraint_count += 3
        prefix = next_prefix
    return tuple(auxiliaries), constraint_count


def _class_pair_blocks(
    a_rows: Sequence[Sequence[BitNode]],
    b_rows: Sequence[Sequence[BitNode]],
) -> tuple[tuple[cp_model.IntVar, ...], ...]:
    """Return six 36-bit blocks in one fixed full-assignment order."""

    blocks: list[tuple[cp_model.IntVar, ...]] = []
    for pair_index in range(CLASS_COUNT // 2):
        bits: list[cp_model.IntVar] = []
        for class_index in (2 * pair_index, 2 * pair_index + 1):
            for row in range(ROWS):
                a_node = a_rows[row][class_index + 1]
                b_node = b_rows[row][class_index + 1]
                if type(a_node) is int or type(b_node) is int:
                    raise ValueError("nonzero quotient cells must be variables")
                bits.extend((a_node, b_node))
        if len(bits) != 36:
            raise AssertionError("a class-pair block must contain 36 bits")
        blocks.append(tuple(bits))
    return tuple(blocks)


def _reflected_class_pair_blocks(
    a_rows: Sequence[Sequence[BitNode]],
    b_rows: Sequence[Sequence[BitNode]],
) -> tuple[tuple[cp_model.IntVar, ...], ...]:
    """Return blocks for ``A'(r,j)=A(r,j), B'(r,j)=B(3-r,j+6)``."""

    blocks: list[tuple[cp_model.IntVar, ...]] = []
    for pair_index in range(CLASS_COUNT // 2):
        bits: list[cp_model.IntVar] = []
        for class_index in (2 * pair_index, 2 * pair_index + 1):
            opposite = (class_index + 6) % CLASS_COUNT
            for row in range(ROWS):
                a_node = a_rows[row][class_index + 1]
                b_node = b_rows[(3 - row) % ROWS][opposite + 1]
                if type(a_node) is int or type(b_node) is int:
                    raise ValueError("nonzero quotient cells must be variables")
                bits.extend((a_node, b_node))
        if len(bits) != 36:
            raise AssertionError("a reflected class-pair block must have 36 bits")
        blocks.append(tuple(bits))
    return tuple(blocks)


def _encode_blocks(
    model: cp_model.CpModel,
    blocks: Sequence[Sequence[cp_model.IntVar]],
    prefix: str,
) -> tuple[tuple[cp_model.IntVar, ...], int]:
    """Encode lexicographically ordered bit blocks as exact integers."""

    codes: list[cp_model.IntVar] = []
    for block_index, bits in enumerate(blocks):
        code = model.new_int_var(
            0, (1 << len(bits)) - 1, f"{prefix}_block_code_{block_index}"
        )
        model.add(
            code
            == sum(
                (1 << (len(bits) - position - 1)) * bit
                for position, bit in enumerate(bits)
            )
        ).with_name(f"define_{prefix}_block_code_{block_index}")
        codes.append(code)
    return tuple(codes), len(codes)


def _add_c6_lex_leader(
    model: cp_model.CpModel,
    a_rows: Sequence[Sequence[BitNode]],
    b_rows: Sequence[Sequence[BitNode]],
) -> tuple[
    tuple[cp_model.IntVar, ...],
    int,
    tuple[cp_model.IntVar, ...],
]:
    """Select the least of all six residual class-pair rotations."""

    blocks = _class_pair_blocks(a_rows, b_rows)
    codes, constraint_count = _encode_blocks(model, blocks, "c6")

    auxiliaries: list[cp_model.IntVar] = []
    for shift in range(1, len(codes)):
        rotated = tuple(codes[(index + shift) % len(codes)] for index in range(6))
        variables, constraints = _add_lex_less_or_equal(
            model, tuple(codes), rotated, f"c6_rotation_{shift}"
        )
        auxiliaries.extend(variables)
        constraint_count += constraints
    if len(auxiliaries) != 25 or constraint_count != 106:
        raise AssertionError("C6 lex-leader encoding size changed")
    return tuple((*codes, *auxiliaries)), constraint_count, codes


def _add_c2_coset_lex_leaders(
    model: cp_model.CpModel,
    a_rows: Sequence[Sequence[BitNode]],
    b_rows: Sequence[Sequence[BitNode]],
    original_codes: Sequence[cp_model.IntVar],
) -> tuple[tuple[cp_model.IntVar, ...], int]:
    """Compare the original against all six images in the corrected C2 coset."""

    reflected_blocks = _reflected_class_pair_blocks(a_rows, b_rows)
    reflected_codes, constraint_count = _encode_blocks(
        model, reflected_blocks, "c2"
    )
    auxiliaries: list[cp_model.IntVar] = []
    for shift in range(6):
        image = tuple(
            reflected_codes[(index + shift) % 6] for index in range(6)
        )
        variables, constraints = _add_lex_less_or_equal(
            model,
            tuple(original_codes),
            image,
            f"c2_coset_rotation_{shift}",
        )
        auxiliaries.extend(variables)
        constraint_count += constraints
    if len(auxiliaries) != 30 or constraint_count != 126:
        raise AssertionError("C2-coset lex-leader encoding size changed")
    return tuple((*reflected_codes, *auxiliaries)), constraint_count


def build_model(
    *,
    row_sum_index: int | None = None,
    c6_symmetry: bool = True,
    c2_symmetry: bool = True,
) -> Order3Model:
    """Build the exact order-three quotient model."""

    catalog = row_sum_catalog()
    if row_sum_index is not None and not 0 <= row_sum_index < len(catalog):
        raise ValueError(
            f"row-sum index must lie in [0,{len(catalog)})"
        )

    model = cp_model.CpModel()
    zero_pairs = tuple(
        SIGN_PAIRS[exponent] for exponent in CANONICAL_ZERO_EXPONENTS
    )
    a_rows: list[tuple[BitNode, ...]] = []
    b_rows: list[tuple[BitNode, ...]] = []
    primary: list[cp_model.IntVar] = []
    for row in range(ROWS):
        a_row: list[BitNode] = [int(zero_pairs[row][0] == 1)]
        b_row: list[BitNode] = [int(zero_pairs[row][1] == 1)]
        for class_index in range(CLASS_COUNT):
            a_variable = model.new_bool_var(f"a_r{row}_c{class_index}")
            b_variable = model.new_bool_var(f"b_r{row}_c{class_index}")
            a_row.append(a_variable)
            b_row.append(b_variable)
            primary.extend((a_variable, b_variable))
        a_rows.append(tuple(a_row))
        b_rows.append(tuple(b_row))
    if len(primary) != PRIMARY_SIGN_BITS:
        raise AssertionError("order-three model must have 216 primary bits")

    compression_constraints = 0
    for class_index in range(CLASS_COUNT):
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
            for left in range(CLASS_COUNT + 1):
                for right in range(CLASS_COUNT + 1):
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

    row_sum_variables: list[cp_model.IntVar] = []
    for row in range(ROWS):
        row_sum_variables.extend(
            (
                model.new_int_var(-12, 12, f"t_r{row}_real"),
                model.new_int_var(-12, 12, f"t_r{row}_imag"),
            )
        )
    selected_rows = (
        catalog
        if row_sum_index is None
        else (catalog[row_sum_index],)
    )
    model.add_allowed_assignments(
        tuple(row_sum_variables), selected_rows
    ).with_name("exact_order3_row_sum_catalog")
    row_sum_constraints = 1
    for row in range(ROWS):
        real = row_sum_variables[2 * row]
        imag = row_sum_variables[2 * row + 1]
        model.add(
            sum(
                a_rows[row][class_index + 1]
                + b_rows[row][class_index + 1]
                for class_index in range(CLASS_COUNT)
            )
            == real + CLASS_COUNT
        ).with_name(f"define_t_r{row}_real")
        model.add(
            sum(
                b_rows[row][class_index + 1]
                - a_rows[row][class_index + 1]
                for class_index in range(CLASS_COUNT)
            )
            == imag
        ).with_name(f"define_t_r{row}_imag")
        row_sum_constraints += 2

    c6_variables: tuple[cp_model.IntVar, ...] = ()
    c6_constraints = 0
    c2_variables: tuple[cp_model.IntVar, ...] = ()
    c2_constraints = 0
    if c6_symmetry:
        c6_variables, c6_constraints, original_codes = _add_c6_lex_leader(
            model, a_rows, b_rows
        )
        if c2_symmetry:
            c2_variables, c2_constraints = _add_c2_coset_lex_leaders(
                model, a_rows, b_rows, original_codes
            )

    bundle = Order3Model(
        model=model,
        a_nodes=tuple(a_rows),
        b_nodes=tuple(b_rows),
        primary_variables=tuple(primary),
        xor_variables=tuple(cache.values()),
        row_sum_variables=tuple(row_sum_variables),
        c6_variables=c6_variables,
        c2_variables=c2_variables,
        equations=QUOTIENT_EQUATIONS,
        compression_constraints=compression_constraints,
        row_sum_constraints=row_sum_constraints,
        c6_constraints=c6_constraints,
        c2_constraints=c2_constraints,
    )
    counts = bundle.exact_counts()
    expected_variables = (
        counts["primary_sign_bits"]
        + counts["cached_xor_variables"]
        + counts["row_sum_variables"]
        + counts["c6_variables"]
        + counts["c2_variables"]
    )
    expected_constraints = (
        counts["cached_xor_variables"]
        + counts["compression_constraints"]
        + counts["quotient_lag_constraints"]
        + counts["row_sum_constraints"]
        + counts["c6_constraints"]
        + counts["c2_constraints"]
    )
    if counts["total_variables"] != expected_variables:
        raise AssertionError("unexpected variables entered the order-three model")
    if counts["total_constraints"] != expected_constraints:
        raise AssertionError("unexpected constraints entered the order-three model")
    return bundle


def quotient_exponents_from_solver(
    solver: cp_model.CpSolver, bundle: Order3Model
) -> tuple[tuple[int, ...], ...]:
    """Decode all quotient A/B bits to exponents of ``i``."""

    def sign(node: BitNode) -> int:
        value = int(node) if type(node) is int else solver.value(node)
        return 1 if value else -1

    return tuple(
        tuple(
            PAIR_TO_EXPONENT[
                (
                    sign(bundle.a_nodes[row][column]),
                    sign(bundle.b_nodes[row][column]),
                )
            ]
            for column in range(CLASS_COUNT + 1)
        )
        for row in range(ROWS)
    )


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
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument(
        "--row-sum-index",
        type=int,
        help="fix one of the 1,756 exact aggregate rows (zero based)",
    )
    parser.add_argument(
        "--no-c6-symmetry",
        action="store_true",
        help="disable all residual C6 x C2 symmetry breaking",
    )
    parser.add_argument(
        "--no-c2-symmetry",
        action="store_true",
        help="retain C6 but disable the corrected B-reflection coset leaders",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/legendre_pair_333_order3.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.time_limit <= 0 or args.workers <= 0 or args.max_memory_mb <= 0:
        print(
            "error=time limit, worker count, and memory cap must be positive",
            file=sys.stderr,
        )
        return 2
    try:
        bundle = build_model(
            row_sum_index=args.row_sum_index,
            c6_symmetry=not args.no_c6_symmetry,
            c2_symmetry=not args.no_c2_symmetry,
        )
    except (AssertionError, OSError, ValueError) as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    validation_error = bundle.model.validate()
    print(f"row_sum_catalog_size={len(row_sum_catalog())}")
    print(
        "row_sum_index="
        + ("all" if args.row_sum_index is None else str(args.row_sum_index))
    )
    print(f"c6_symmetry={str(not args.no_c6_symmetry).lower()}")
    print(
        "c2_symmetry="
        f"{str(not args.no_c6_symmetry and not args.no_c2_symmetry).lower()}"
    )
    for name, value in bundle.exact_counts().items():
        print(f"{name}={value}")
    print(bundle.model.model_stats())
    print(f"model_validation={'passed' if not validation_error else 'failed'}")
    if validation_error:
        print(validation_error, file=sys.stderr)
        return 2
    if args.build_only:
        return 0

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    solver.parameters.log_search_progress = args.log_search_progress
    status = solver.solve(bundle.model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.3f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2

    exponents = quotient_exponents_from_solver(solver, bundle)
    verify_and_save_candidate(args.output, exponents)
    print(f"candidate={args.output}")
    print("hadamard_order=668")
    print("hadamard_verified=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
