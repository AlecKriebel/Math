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
from collections.abc import Sequence
import json
from math import gcd
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from good_167 import (
    GOOD_167_ROW_SUM_PROFILES,
    ORDER,
    is_skew,
    is_symmetric,
    product_theorem_holds,
    validate_good_quadruple,
)
from good_167_linear import skew_from_negative_mask, symmetric_from_negative_mask
from verify_good_167_local import verify_local_checkpoint


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


def _half_literal_descriptor(
    n: int,
    index: int,
    *,
    skew: bool,
) -> tuple[int | None, bool]:
    """Describe a full negative-entry literal by half index and complement.

    The normalized entry at zero is the constant false bit.  Reflection reuses
    a half variable for a symmetric sequence and complements it for a skew
    sequence.
    """

    if n <= 1 or n % 2 != 1:
        raise ValueError("n must be odd and greater than one")
    index %= n
    if index == 0:
        return None, False
    half = (n - 1) // 2
    if index <= half:
        return index - 1, False
    return n - index - 1, skew


def _cached_edge_difference(
    model: cp_model.CpModel,
    half_bits: list[cp_model.IntVar],
    left: int,
    right: int,
    *,
    skew: bool,
    sequence_index: int,
    cache: dict[tuple[int, int, int], cp_model.IntVar],
) -> cp_model.LinearExpr | int:
    """Return one full-edge XOR, sharing its unordered half-variable pair."""

    n = 2 * len(half_bits) + 1
    left_base, left_complement = _half_literal_descriptor(n, left, skew=skew)
    right_base, right_complement = _half_literal_descriptor(n, right, skew=skew)
    complement = left_complement != right_complement
    if left_base is None and right_base is None:
        return int(complement)
    if left_base is None or right_base is None:
        base = right_base if left_base is None else left_base
        assert base is not None
        literal = half_bits[base]
        return literal.negated() if complement else literal
    if left_base == right_base:
        return int(complement)
    first, second = sorted((left_base, right_base))
    key = (sequence_index, first, second)
    difference = cache.get(key)
    if difference is None:
        difference = _xor_bit(
            model,
            half_bits[first],
            half_bits[second],
            f"pair_diff_{sequence_index}_{first + 1}_{second + 1}",
        )
        cache[key] = difference
    return difference.negated() if complement else difference


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


def _decimate_sequence(sequence: Sequence[int], multiplier: int) -> tuple[int, ...]:
    """Apply the index automorphism ``i -> multiplier*i``."""

    n = len(sequence)
    multiplier %= n
    if n <= 1 or gcd(multiplier, n) != 1:
        raise ValueError("decimation multiplier must be a unit")
    return tuple(sequence[multiplier * index % n] for index in range(n))


def _necklace_word(sequence: Sequence[int]) -> tuple[int, ...] | None:
    """Return negative-entry bits in doubling-cycle order."""

    order = _doubling_cycle_variable_order(len(sequence))
    if order is None:
        return None
    return tuple(1 if sequence[index + 1] == -1 else 0 for index in order)


def _canonicalize_common_decimation(
    sequences: Sequence[Sequence[int]],
    row_sums: tuple[int, int, int],
) -> tuple[tuple[tuple[int, ...], ...], int, int]:
    """Choose the necklace-maximal doubling decimation and normalize ``A[1]``.

    At order 167, multiplication by two is transitive on nonzero indices
    modulo sign.  The unique symmetric sequence of row sum 15 anchors that
    common-decimation orbit.  Replacing a chosen multiplier by its negative
    leaves all symmetric sequences unchanged and makes the skew sequence have
    ``A[1]=+1``.
    """

    immutable = tuple(tuple(sequence) for sequence in sequences)
    if len(immutable) != 4:
        raise ValueError("a good-matrix hint must contain four sequences")
    n = len(immutable[0])
    if row_sums.count(15) != 1:
        raise ValueError("common-decimation canonicalization needs a unique row-sum-15 anchor")
    anchor = immutable[1 + row_sums.index(15)]
    word = _necklace_word(anchor)
    if word is None:
        raise ValueError("doubling does not generate the half-index cycle")
    shift = max(
        range(len(word)),
        key=lambda amount: word[amount:] + word[:amount],
    )
    multiplier = pow(2, shift, n)
    if immutable[0][multiplier] == -1:
        multiplier = (-multiplier) % n
    transformed = tuple(
        _decimate_sequence(sequence, multiplier) for sequence in immutable
    )
    if transformed[0][1] != 1:
        raise AssertionError("signed decimation did not normalize A[1]")
    transformed_word = _necklace_word(transformed[1 + row_sums.index(15)])
    if transformed_word != max(
        word[amount:] + word[:amount] for amount in range(len(word))
    ):
        raise AssertionError("decimation did not select the maximal necklace rotation")
    return transformed, shift, multiplier


def _validate_structural_hint(
    sequences: Sequence[Sequence[int]],
    n: int,
    row_sums: tuple[int, int, int],
    *,
    fix_a1: bool,
    common_decimation_necklace: bool,
) -> tuple[tuple[int, ...], ...]:
    """Validate every exact constraint except PAF complementarity."""

    if len(sequences) != 4:
        raise ValueError("a good-matrix hint must contain four sequences")
    immutable = tuple(tuple(sequence) for sequence in sequences)
    if any(
        len(sequence) != n
        or any(type(value) is not int or value not in (-1, 1) for value in sequence)
        for sequence in immutable
    ):
        raise ValueError("hint sequences must be length-n sign sequences")
    a, b, c, d = immutable
    if not is_skew(a) or not all(is_symmetric(sequence) for sequence in (b, c, d)):
        raise ValueError("hint does not have normalized skew/symmetric structure")
    if tuple(sum(sequence) for sequence in (b, c, d)) != row_sums:
        raise ValueError("hint symmetric row sums do not match the model")
    if fix_a1 and a[1] != 1:
        raise ValueError("hint violates the A[1]=+1 symmetry break")
    if not product_theorem_holds(a, b, c, d):
        raise ValueError("hint violates the good-matrix product theorem")
    if common_decimation_necklace:
        anchor = (b, c, d)[row_sums.index(15) if 15 in row_sums else 0]
        word = _necklace_word(anchor)
        if word is not None and word != max(
            word[amount:] + word[:amount] for amount in range(len(word))
        ):
            raise ValueError("hint violates the common-decimation necklace")
    return immutable


def _local_checkpoint_hint(
    payload: object,
    row_sums: tuple[int, int, int],
    *,
    common_decimation_necklace: bool,
) -> tuple[tuple[tuple[int, ...], ...], dict[str, int]]:
    """Verify, reorder, and canonicalize an order-167 local checkpoint."""

    diagnostics = verify_local_checkpoint(payload)
    assert isinstance(payload, dict)  # established by the strict verifier
    try:
        profile = GOOD_167_ROW_SUM_PROFILES.index(row_sums)
    except ValueError as error:
        raise ValueError("local hints are supported only for an order-167 row-sum profile") from error
    if payload["profile"] != profile:
        raise ValueError("local checkpoint profile does not match the requested model")

    a = skew_from_negative_mask(int(payload["a_mask"], 16))
    oriented_symmetric = tuple(
        symmetric_from_negative_mask(int(payload[f"{name}_mask"], 16))
        for name in ("b", "c", "d")
    )
    by_sum = {sum(sequence): sequence for sequence in oriented_symmetric}
    if len(by_sum) != 3 or set(by_sum) != set(row_sums):
        raise ValueError("local checkpoint symmetric sequences cannot be canonically reordered")
    sequences = (a, *(by_sum[target] for target in row_sums))
    shift = 0
    multiplier = 1
    if common_decimation_necklace:
        sequences, shift, multiplier = _canonicalize_common_decimation(
            sequences, row_sums
        )
    sequences = _validate_structural_hint(
        sequences,
        ORDER,
        row_sums,
        fix_a1=True,
        common_decimation_necklace=common_decimation_necklace,
    )
    return sequences, {
        **diagnostics,
        "profile": profile,
        "decimation_shift": shift,
        "decimation_multiplier": multiplier,
    }


def load_local_hint(
    path: Path,
    row_sums: tuple[int, int, int],
    *,
    common_decimation_necklace: bool,
) -> tuple[tuple[tuple[int, ...], ...], dict[str, int]]:
    """Load a strictly verified nonexact local checkpoint as a CP-SAT hint."""

    return _local_checkpoint_hint(
        json.loads(path.read_text()),
        row_sums,
        common_decimation_necklace=common_decimation_necklace,
    )


def build_model(
    n: int,
    row_sums: tuple[int, int, int],
    *,
    fix_a1: bool = True,
    half_edges: bool = True,
    common_decimation_necklace: bool = True,
    hint_sequences: Sequence[Sequence[int]] | None = None,
    max_symmetric_hint_distance: int | None = None,
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
    if max_symmetric_hint_distance is not None and (
        max_symmetric_hint_distance < 0 or max_symmetric_hint_distance > 3 * ((n - 1) // 2)
    ):
        raise ValueError("symmetric hint distance is out of range")
    if max_symmetric_hint_distance is not None and hint_sequences is None:
        raise ValueError("a symmetric hint-distance bound requires hint sequences")

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
    difference_cache: dict[tuple[int, int, int], cp_model.IntVar] = {}
    for lag in range(1, half + 1):
        differences = []
        if half_edges:
            for sequence_index, bits in enumerate(halves):
                representatives = _edge_orbit_representatives(
                    n, lag, skew=sequence_index == 0
                )
                differences.extend(
                    _cached_edge_difference(
                        model,
                        bits,
                        index,
                        (index + lag) % n,
                        skew=sequence_index == 0,
                        sequence_index=sequence_index,
                        cache=difference_cache,
                    )
                    for index in representatives
                )
            model.add(sum(differences) == n - 1)
        else:
            for sequence_index, bits in enumerate(halves):
                differences.extend(
                    _cached_edge_difference(
                        model,
                        bits,
                        index,
                        (index + lag) % n,
                        skew=sequence_index == 0,
                        sequence_index=sequence_index,
                        cache=difference_cache,
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

    if hint_sequences is not None:
        validated_hint = _validate_structural_hint(
            hint_sequences,
            n,
            row_sums,
            fix_a1=fix_a1,
            common_decimation_necklace=common_decimation_necklace,
        )
        for sequence, bits in zip(validated_hint, halves, strict=True):
            for index, bit in enumerate(bits, start=1):
                model.add_hint(bit, int(sequence[index] == -1))
        if max_symmetric_hint_distance is not None:
            mismatches = []
            for sequence, bits in zip(
                validated_hint[1:], halves[1:], strict=True
            ):
                mismatches.extend(
                    bit.negated() if sequence[index] == -1 else bit
                    for index, bit in enumerate(bits, start=1)
                )
            model.add(sum(mismatches) <= max_symmetric_hint_distance)
        validation_error = model.validate()
        if validation_error:
            raise AssertionError(f"hinted CP-SAT model is invalid: {validation_error}")

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
    max_memory_mb: int = 256,
    half_edges: bool = True,
    common_decimation_necklace: bool = True,
    hint_sequences: Sequence[Sequence[int]] | None = None,
    hint_conflict_limit: int = 1000,
    max_symmetric_hint_distance: int | None = None,
) -> tuple[str, tuple[tuple[int, ...], ...] | None, cp_model.CpSolver]:
    if (
        time_limit <= 0
        or workers <= 0
        or max_memory_mb <= 0
        or hint_conflict_limit <= 0
    ):
        raise ValueError("time limit, workers, memory cap, and hint conflict limit must be positive")
    model, halves = build_model(
        n,
        row_sums,
        half_edges=half_edges,
        common_decimation_necklace=common_decimation_necklace,
        hint_sequences=hint_sequences,
        max_symmetric_hint_distance=max_symmetric_hint_distance,
    )
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = workers
    solver.parameters.max_memory_in_mb = max_memory_mb
    solver.parameters.random_seed = random_seed
    if hint_sequences is not None:
        solver.parameters.repair_hint = max_symmetric_hint_distance is None
        if solver.parameters.repair_hint:
            solver.parameters.hint_conflict_limit = hint_conflict_limit
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
        default=256,
        help="CP-SAT memory cap in MiB (the one-worker default for a 16 GiB host)",
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
        "--hint",
        type=Path,
        help="strictly verified nonexact local checkpoint to repair",
    )
    parser.add_argument(
        "--hint-conflict-limit",
        type=int,
        default=1000,
        help="conflicts spent repairing a supplied hint before normal search",
    )
    parser.add_argument(
        "--max-hint-exchanges",
        type=int,
        help=(
            "exactly search the ball with total B,C,D Hamming distance at "
            "most twice this value; requires --hint and "
            "--no-common-decimation-necklace"
        ),
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="build and validate the model without launching search",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    from good_167 import good_row_sum_profiles

    if (
        args.time_limit <= 0
        or args.workers <= 0
        or args.max_memory_mb <= 0
        or args.hint_conflict_limit <= 0
    ):
        parser.error(
            "--time-limit, --workers, --max-memory-mb, and "
            "--hint-conflict-limit must be positive"
        )
    if args.max_hint_exchanges is not None and args.max_hint_exchanges < 0:
        parser.error("--max-hint-exchanges must be nonnegative")
    if args.max_hint_exchanges is not None and args.hint is None:
        parser.error("--max-hint-exchanges requires --hint")
    if args.max_hint_exchanges is not None and not args.no_common_decimation_necklace:
        parser.error(
            "--max-hint-exchanges requires --no-common-decimation-necklace "
            "so canonicalization cannot clip the local ball"
        )
    profiles = good_row_sum_profiles(args.order)
    if not 0 <= args.profile < len(profiles):
        parser.error(f"--profile must be in 0..{len(profiles)-1}; profiles={profiles}")
    profile = profiles[args.profile]
    common_decimation_necklace = not args.no_common_decimation_necklace
    max_symmetric_hint_distance = (
        None
        if args.max_hint_exchanges is None
        else 2 * args.max_hint_exchanges
    )
    hint_sequences = None
    hint_diagnostics = None
    if args.hint is not None:
        if args.order != ORDER:
            parser.error("--hint currently accepts only order-167 local checkpoints")
        try:
            hint_sequences, hint_diagnostics = load_local_hint(
                args.hint,
                profile,
                common_decimation_necklace=common_decimation_necklace,
            )
        except (OSError, json.JSONDecodeError, ValueError) as error:
            parser.error(f"invalid --hint: {error}")
    print(f"order={args.order} profile={args.profile}/{len(profiles)} row_sums={profile}")
    print(f"workers={args.workers} max_memory_mb={args.max_memory_mb}")
    if hint_diagnostics is not None:
        print(
            f"hint={args.hint} energy={hint_diagnostics['energy']} "
            f"bad_lags={hint_diagnostics['bad_lags']} "
            f"decimation_shift={hint_diagnostics['decimation_shift']} "
            f"decimation_multiplier={hint_diagnostics['decimation_multiplier']}"
        )
        if max_symmetric_hint_distance is not None:
            print(
                "exact_hint_ball=true "
                f"max_symmetric_hamming_distance={max_symmetric_hint_distance} "
                f"max_exchanges={args.max_hint_exchanges}"
            )
        print(
            f"repair_hint={str(max_symmetric_hint_distance is None).lower()} "
            f"hint_conflict_limit={args.hint_conflict_limit} hinted_primaries={4 * ((args.order - 1) // 2)}"
        )
    if args.build_only:
        model, _ = build_model(
            args.order,
            profile,
            half_edges=not args.full_directed_edges,
            common_decimation_necklace=common_decimation_necklace,
            hint_sequences=hint_sequences,
            max_symmetric_hint_distance=max_symmetric_hint_distance,
        )
        proto = model.proto
        print(f"variables={len(proto.variables)} constraints={len(proto.constraints)}")
        print(
            f"half_edges={not args.full_directed_edges} "
            f"common_decimation_necklace="
            f"{common_decimation_necklace}"
        )
        print(f"hinted_variables={len(proto.solution_hint.vars)}")
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
        common_decimation_necklace=common_decimation_necklace,
        hint_sequences=hint_sequences,
        hint_conflict_limit=args.hint_conflict_limit,
        max_symmetric_hint_distance=max_symmetric_hint_distance,
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
