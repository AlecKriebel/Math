#!/usr/bin/env python3
"""Exact CP-SAT search for circulant good matrices of order 167.

The model uses one Boolean for each independent entry of a normalized skew
sequence ``A`` and three normalized symmetric sequences ``B,C,D``.  It
imposes all 83 independent periodic-autocorrelation equations, the exact row
sums, and the order-independent good-matrix product theorem.

This is a feasibility search, not an exhaustive nonexistence certificate.
``UNKNOWN`` means only that the time limit expired.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from good_167 import GOOD_167_ROW_SUM_PROFILES, ORDER, validate_good_quadruple


def _full_literals(
    model: cp_model.CpModel,
    half_bits: list[cp_model.IntVar],
    *,
    skew: bool,
) -> list[cp_model.IntVar]:
    """Expand negative-entry bits to a full normalized odd sequence."""

    n = 2 * len(half_bits) + 1
    zero = model.new_constant(0)  # negative-entry bit for the fixed +1 at index zero
    result: list[cp_model.IntVar] = [zero, *half_bits]
    for index in range(len(half_bits), 0, -1):
        bit = half_bits[index - 1]
        result.append(bit.negated() if skew else bit)
    if len(result) != n:
        raise AssertionError("literal expansion length mismatch")
    return result


def _xor_bit(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    """Return the Boolean ``left XOR right``."""

    difference = model.new_bool_var(name)
    # XOR(left, right, NOT difference) must be true, hence
    # difference = left XOR right.
    model.add_bool_xor((left, right, difference.negated()))
    return difference


def _edge_orbit_representatives(
    n: int, lag: int, *, skew: bool
) -> tuple[int, ...]:
    """Represent directed edges under ``i -> -i-lag``.

    For a symmetric sequence the reflection-fixed edge has difference zero,
    leaving ``(n-1)/2`` doubled representatives.  For a normalized skew
    sequence the fixed edge contributes one and the pair containing the two
    edges incident with zero contributes one; the remaining
    ``(n-3)/2`` representatives are doubled.
    """

    if n <= 1 or n % 2 != 1 or not 1 <= lag <= (n - 1) // 2:
        raise ValueError("edge-orbit arguments are out of range")
    inverse_two = pow(2, -1, n)
    fixed = (-lag * inverse_two) % n
    special = {0, (-lag) % n} if skew else set()
    excluded = {fixed, *special}
    representatives: list[int] = []
    seen = set(excluded)
    for index in range(n):
        if index in seen:
            continue
        mate = (-index - lag) % n
        if mate == index or mate in seen:
            raise AssertionError("edge reflection orbit mismatch")
        seen.add(index)
        seen.add(mate)
        representatives.append(min(index, mate))
    expected = (n - 3) // 2 if skew else (n - 1) // 2
    if len(representatives) != expected or len(seen) != n:
        raise AssertionError("edge reflection did not partition the indices")
    return tuple(representatives)


def _add_lexicographic_greater_or_equal(
    model: cp_model.CpModel,
    left: list[cp_model.IntVar],
    right: list[cp_model.IntVar],
    name: str,
) -> None:
    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    prefix: cp_model.IntVar | None = None
    for index, (lhs, rhs) in enumerate(zip(left, right, strict=True)):
        lex_clause = [lhs, rhs.negated()]
        if prefix is not None:
            lex_clause.append(prefix.negated())
        model.add_bool_or(lex_clause)
        if index + 1 == len(left):
            break
        next_prefix = model.new_bool_var(f"{name}_prefix_{index + 1}")
        # next_prefix iff prefix is still active and lhs == rhs.  The first
        # position has an implicit true prefix.
        if prefix is not None:
            model.add_bool_or((next_prefix.negated(), prefix))
        model.add_bool_or((next_prefix.negated(), lhs.negated(), rhs))
        model.add_bool_or((next_prefix.negated(), rhs.negated(), lhs))
        both_one = [lhs.negated(), rhs.negated(), next_prefix]
        both_zero = [lhs, rhs, next_prefix]
        if prefix is not None:
            both_one.append(prefix.negated())
            both_zero.append(prefix.negated())
        model.add_bool_or(both_one)
        model.add_bool_or(both_zero)
        prefix = next_prefix


def _doubling_cycle_variable_order(n: int) -> tuple[int, ...] | None:
    """Return the half-variable cycle induced by multiplication by two."""

    half = (n - 1) // 2
    result: list[int] = []
    value = 1
    for _ in range(half):
        representative = min(value, n - value)
        index = representative - 1
        if index in result:
            return None
        result.append(index)
        value = 2 * value % n
    if value not in (1, n - 1) or set(result) != set(range(half)):
        return None
    return tuple(result)


def _add_common_decimation_necklace(
    model: cp_model.CpModel,
    half_bits: list[cp_model.IntVar],
    name: str,
) -> bool:
    """Make a symmetric half-word maximal under the doubling-cycle action."""

    n = 2 * len(half_bits) + 1
    order = _doubling_cycle_variable_order(n)
    if order is None:
        return False
    word = [half_bits[index] for index in order]
    for shift in range(1, len(word)):
        rotated = word[shift:] + word[:shift]
        _add_lexicographic_greater_or_equal(
            model, word, rotated, f"{name}_rotation_{shift}"
        )
    return True


def build_model(
    n: int,
    row_sums: tuple[int, int, int],
    *,
    fix_a1: bool = True,
    half_edges: bool = True,
    common_decimation_necklace: bool = True,
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    """Build the exact normalized good-matrix model at odd order ``n``."""

    if n <= 1 or n % 2 != 1:
        raise ValueError("n must be an odd integer greater than one")
    if tuple(sorted(row_sums)) != row_sums:
        raise ValueError("row sums must be in canonical sorted order")
    if sum(value * value for value in row_sums) != 4 * n - 1:
        raise ValueError("row sums do not satisfy the trivial-character equation")
    if any(value % 4 != n % 4 for value in row_sums):
        raise ValueError("a normalized symmetric row sum must be n modulo four")

    model = cp_model.CpModel()
    half = (n - 1) // 2
    halves = tuple(
        [model.new_bool_var(f"{label}_{index}") for index in range(1, half + 1)]
        for label in "abcd"
    )
    a_half, b_half, c_half, d_half = halves
    full = (
        _full_literals(model, a_half, skew=True),
        _full_literals(model, b_half, skew=False),
        _full_literals(model, c_half, skew=False),
        _full_literals(model, d_half, skew=False),
    )

    # Reindexing every sequence by i -> -i negates all independent entries of
    # A and fixes B,C,D.  Therefore a_1=+1 is safe symmetry breaking.
    if fix_a1:
        model.add(a_half[0] == 0)

    # For a normalized symmetric sequence X, sum(X)=n-4m where m is the
    # number of negative entries among its independent half.
    for bits, target in zip((b_half, c_half, d_half), row_sums, strict=True):
        model.add(sum(bits) == (n - target) // 4)

    if common_decimation_necklace and n == ORDER and row_sums.count(15) != 1:
        raise ValueError("order-167 necklace requires a unique row-sum-15 anchor")
    anchor_index = row_sums.index(15) if 15 in row_sums else 0
    if common_decimation_necklace:
        necklace_applied = _add_common_decimation_necklace(
            model,
            (b_half, c_half, d_half)[anchor_index],
            "common_decimation",
        )
        if n == ORDER and not necklace_applied:
            raise AssertionError("doubling should generate the order-167 quotient")

    # Product theorem in negative-entry bits:
    #   bar(a_k)+bar(a_2k)+bar(b_k)+bar(c_k)+bar(d_k) = 1 (mod 2).
    for k in range(1, half + 1):
        model.add_bool_xor(
            (full[0][k], full[0][2 * k % n], full[1][k], full[2][k], full[3][k])
        )

    # PAF_X(k)=n-2*d_X(k), so complementarity is sum_X d_X(k)=2n.
    # Pair directed edges under i -> -i-k.  A symmetric sequence has one
    # fixed zero edge and 83 doubled representatives at n=167.  The skew
    # sequence has a fixed one edge plus a special two-edge orbit totaling
    # one, and 82 doubled representatives.  Dividing the resulting equation
    # by two leaves exactly sum(representative XORs)=n-1.
    for lag in range(1, half + 1):
        differences = []
        if half_edges:
            for sequence_index, bits in enumerate(full):
                representatives = _edge_orbit_representatives(
                    n, lag, skew=sequence_index == 0
                )
                differences.extend(
                    _xor_bit(
                        model,
                        bits[index],
                        bits[(index + lag) % n],
                        f"half_diff_{lag}_{sequence_index}_{index}",
                    )
                    for index in representatives
                )
            model.add(sum(differences) == n - 1)
        else:
            for sequence_index, bits in enumerate(full):
                differences.extend(
                    _xor_bit(
                        model,
                        bits[index],
                        bits[(index + lag) % n],
                        f"diff_{lag}_{sequence_index}_{index}",
                    )
                    for index in range(n)
                )
            model.add(sum(differences) == 2 * n)

    # When FIXED_SEARCH is requested, branch only on the genuine sequence
    # entries.  Put B,C,D first: the product-cycle XORs and a_1=+1 then force
    # all of A.  Auxiliary Hamming-difference bits are consequences, not
    # search choices.
    symmetric_halves = (b_half, c_half, d_half)
    ordered_symmetric = (
        symmetric_halves[anchor_index],
        *(symmetric_halves[index]
          for index in range(3) if index != anchor_index),
    )
    model.add_decision_strategy(
        [*(bit for bits in ordered_symmetric for bit in bits), *a_half],
        cp_model.CHOOSE_FIRST,
        cp_model.SELECT_MIN_VALUE,
    )

    return model, halves


def _decode(
    solver: cp_model.CpSolver,
    halves: tuple[list[cp_model.IntVar], ...],
) -> tuple[tuple[int, ...], ...]:
    result = []
    for sequence_index, half_bits in enumerate(halves):
        half_signs = tuple(-1 if solver.value(bit) else 1 for bit in half_bits)
        reflected = tuple(reversed(half_signs))
        if sequence_index == 0:
            reflected = tuple(-value for value in reflected)
        result.append((1, *half_signs, *reflected))
    return tuple(result)


def solve(
    n: int,
    row_sums: tuple[int, int, int],
    *,
    time_limit: float,
    workers: int,
    random_seed: int,
    fixed_search: bool = False,
    max_memory_mb: int = 2048,
    half_edges: bool = True,
    common_decimation_necklace: bool = True,
) -> tuple[str, tuple[tuple[int, ...], ...] | None, cp_model.CpSolver]:
    if time_limit <= 0 or workers <= 0 or max_memory_mb <= 0:
        raise ValueError("time limit, workers, and memory cap must be positive")
    model, halves = build_model(
        n,
        row_sums,
        half_edges=half_edges,
        common_decimation_necklace=common_decimation_necklace,
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.max_memory_in_mb = max_memory_mb
    solver.parameters.random_seed = random_seed
    if fixed_search:
        solver.parameters.search_branching = cp_model.FIXED_SEARCH
    status = solver.solve(model)
    name = solver.status_name(status)
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return name, None, solver
    sequences = _decode(solver, halves)
    validate_good_quadruple(sequences, n)
    return name, sequences, solver


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", type=int, default=ORDER)
    parser.add_argument("--profile", type=int, default=0)
    parser.add_argument("--time-limit", type=float, default=60.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=2048,
        help="CP-SAT memory cap in MiB (conservative default for a 16 GiB host)",
    )
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument(
        "--fixed-search",
        action="store_true",
        help="branch on B,C,D,A primaries in that order instead of automatic search",
    )
    parser.add_argument(
        "--full-directed-edges",
        action="store_true",
        help="use the redundant full directed-edge PAF encoding",
    )
    parser.add_argument(
        "--no-common-decimation-necklace",
        action="store_true",
        help="disable the exact common-decimation necklace symmetry break",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="build and validate the model without launching search",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    from good_167 import good_row_sum_profiles

    if args.time_limit <= 0 or args.workers <= 0 or args.max_memory_mb <= 0:
        parser.error("--time-limit, --workers, and --max-memory-mb must be positive")
    profiles = good_row_sum_profiles(args.order)
    if not 0 <= args.profile < len(profiles):
        parser.error(f"--profile must be in 0..{len(profiles)-1}; profiles={profiles}")
    profile = profiles[args.profile]
    print(f"order={args.order} profile={args.profile}/{len(profiles)} row_sums={profile}")
    print(f"workers={args.workers} max_memory_mb={args.max_memory_mb}")
    if args.build_only:
        model, _ = build_model(
            args.order,
            profile,
            half_edges=not args.full_directed_edges,
            common_decimation_necklace=not args.no_common_decimation_necklace,
        )
        proto = model.proto
        print(f"variables={len(proto.variables)} constraints={len(proto.constraints)}")
        print(
            f"half_edges={not args.full_directed_edges} "
            f"common_decimation_necklace="
            f"{not args.no_common_decimation_necklace}"
        )
        return 0
    status, sequences, solver = solve(
        args.order,
        profile,
        time_limit=args.time_limit,
        workers=args.workers,
        random_seed=args.random_seed,
        fixed_search=args.fixed_search,
        max_memory_mb=args.max_memory_mb,
        half_edges=not args.full_directed_edges,
        common_decimation_necklace=not args.no_common_decimation_necklace,
    )
    print(f"status={status}")
    print(f"wall_time={solver.wall_time:.3f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    if sequences is None:
        return 0

    payload = {
        "kind": "circulant_good_matrices",
        "order": args.order,
        "hadamard_order": 4 * args.order,
        "row_sums": list(profile),
        "sequences": [list(sequence) for sequence in sequences],
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
        print(f"wrote={args.output}")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
