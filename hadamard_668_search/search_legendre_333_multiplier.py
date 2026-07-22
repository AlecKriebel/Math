#!/usr/bin/env python3
"""Exact search for order-3 multiplier-invariant fixed-compression LP(333).

This is a strict sublane of ``search_legendre_333_cp_sat.py``.  If both
sequences are invariant under multiplication by a unit ``m`` of order three
modulo 333, only one Boolean variable per multiplier orbit is needed.  The
periodic correlation at lag ``s`` then equals that at ``m*s``, reducing the
166 independent lags to one representative per multiplier orbit.

Failure for every multiplier accepted here does not rule out the prescribed
compression and certainly does not rule out a general LP(333).
"""

from __future__ import annotations

import argparse
from collections import Counter
from collections.abc import Sequence
from math import gcd
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from legendre_333 import (
    FIXED_PLUS_COUNTS_A,
    FIXED_PLUS_COUNTS_B,
    N,
    save_verified_candidate,
    verify_legendre_pair,
)
from search_legendre_333_cp_sat import (
    add_fixed_column_margins,
    add_lexicographic_greater_or_equal,
    add_mod3_compression_table,
    add_mod9_compression_equations,
    fixed_compression_distance_bounds,
    inverted_image,
    shifted_image,
)


ORDER_THREE_MULTIPLIER_REPRESENTATIVES = (10, 112, 121, 211)


def validate_multiplier(multiplier: int) -> None:
    if not 1 < multiplier < N:
        raise ValueError(f"multiplier must be in [2,{N - 1}]")
    if gcd(multiplier, N) != 1:
        raise ValueError("multiplier must be a unit modulo 333")
    if pow(multiplier, 3, N) != 1 or multiplier == 1:
        raise ValueError("multiplier must have exact order three modulo 333")
    # The fixed length-37 compression is preserved only by quadratic
    # residues.  Every order-three residue modulo 37 satisfies this, but keep
    # the condition explicit for defensive validation.
    if pow(multiplier % 37, 18, 37) != 1:
        raise ValueError("multiplier does not preserve the fixed compression")


def multiplier_orbits(multiplier: int) -> tuple[tuple[int, ...], ...]:
    validate_multiplier(multiplier)
    unseen = set(range(N))
    result: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        orbit: list[int] = []
        value = start
        while value not in orbit:
            orbit.append(value)
            value = multiplier * value % N
        if value != start or len(orbit) not in (1, 3):
            raise AssertionError("unexpected order-three orbit")
        unseen.difference_update(orbit)
        result.append(tuple(orbit))
    return tuple(result)


def orbit_index_table(orbits: Sequence[Sequence[int]]) -> tuple[int, ...]:
    result = [-1] * N
    for orbit_index, orbit in enumerate(orbits):
        for value in orbit:
            if not 0 <= value < N or result[value] != -1:
                raise ValueError("orbits are not a partition of Z/333")
            result[value] = orbit_index
    if any(value == -1 for value in result):
        raise ValueError("orbits do not cover Z/333")
    return tuple(result)


def canonical_lag(lag: int, multiplier: int) -> int:
    if not 1 <= lag <= (N - 1) // 2:
        raise ValueError("lag is outside the independent range")
    images: set[int] = set()
    value = lag
    for _ in range(3):
        images.add(min(value, N - value))
        value = multiplier * value % N
    return min(images)


def representative_lags(multiplier: int) -> tuple[int, ...]:
    validate_multiplier(multiplier)
    return tuple(
        sorted(
            {
                canonical_lag(lag, multiplier)
                for lag in range(1, (N - 1) // 2 + 1)
            }
        )
    )


def invariant_translation_offsets(multiplier: int) -> tuple[int, ...]:
    """Translations preserving the multiplier subspace and fixed compression."""

    validate_multiplier(multiplier)
    return tuple(
        offset
        for offset in range(0, N, 37)
        if (multiplier - 1) * offset % N == 0
    )


def invariant_distance_edge_upper_bound(multiplier: int, lag: int) -> int:
    """Upper-bound a cyclic distance by counting orbit-distinct shift edges."""

    if not 1 <= lag < N:
        raise ValueError(f"lag must be in [1,{N})")
    orbit_indices = orbit_index_table(multiplier_orbits(multiplier))
    return sum(
        orbit_indices[index] != orbit_indices[(index + lag) % N]
        for index in range(N)
    )


def add_invariant_dihedral_symmetry(
    model: cp_model.CpModel,
    variables: Sequence[cp_model.IntVar],
    multiplier: int,
    prefix: str,
) -> None:
    """Choose a maximum under translations that retain multiplier invariance."""

    original = list(variables)
    offsets = invariant_translation_offsets(multiplier)
    for offset in offsets[1:]:
        add_lexicographic_greater_or_equal(
            model,
            original,
            shifted_image(variables, offset),
            f"{prefix}_invariant_shift_{offset}",
        )
    inverted = inverted_image(variables)
    for offset in offsets:
        add_lexicographic_greater_or_equal(
            model,
            original,
            shifted_image(inverted, offset),
            f"{prefix}_invariant_reflection_{offset}",
        )


def build_multiplier_model(multiplier: int, *, symmetry: bool = True) -> tuple[
    cp_model.CpModel,
    list[cp_model.IntVar],
    list[cp_model.IntVar],
    tuple[tuple[int, ...], ...],
]:
    orbits = multiplier_orbits(multiplier)
    orbit_indices = orbit_index_table(orbits)
    model = cp_model.CpModel()
    orbit_a = [model.new_bool_var(f"a_orbit_{index}") for index in range(len(orbits))]
    orbit_b = [model.new_bool_var(f"b_orbit_{index}") for index in range(len(orbits))]
    expanded_a = [orbit_a[orbit_indices[index]] for index in range(N)]
    expanded_b = [orbit_b[orbit_indices[index]] for index in range(N)]

    add_fixed_column_margins(model, expanded_a, FIXED_PLUS_COUNTS_A, "a")
    add_fixed_column_margins(model, expanded_b, FIXED_PLUS_COUNTS_B, "b")
    add_mod3_compression_table(model, expanded_a, expanded_b)
    add_mod9_compression_equations(model, expanded_a, expanded_b)
    if symmetry:
        add_invariant_dihedral_symmetry(model, expanded_a, multiplier, "a")
        add_invariant_dihedral_symmetry(model, expanded_b, multiplier, "b")

    # Resolve each orbit id to one expanded position once.  The compact
    # representative arrays make the XOR cache independent of length 333.
    representatives = [orbit[0] for orbit in orbits]
    compact_a = [expanded_a[index] for index in representatives]
    compact_b = [expanded_b[index] for index in representatives]
    caches: tuple[dict[tuple[int, int], cp_model.IntVar], ...] = ({}, {})
    for lag in representative_lags(multiplier):
        sequence_terms: list[list[cp_model.LinearExpr]] = []
        for prefix, compact, cache in (
            ("a", compact_a, caches[0]),
            ("b", compact_b, caches[1]),
        ):
            weighted_terms: list[cp_model.LinearExpr] = []
            multiplicities: Counter[tuple[int, int]] = Counter()
            for index in range(N):
                left_orbit = orbit_indices[index]
                right_orbit = orbit_indices[(index + lag) % N]
                if left_orbit != right_orbit:
                    multiplicities[tuple(sorted((left_orbit, right_orbit)))] += 1
            for key, coefficient in multiplicities.items():
                difference = cache.get(key)
                if difference is None:
                    difference = model.new_bool_var(
                        f"{prefix}_orbit_xor_{key[0]}_{key[1]}"
                    )
                    model.add_bool_xor(
                        [compact[key[0]], compact[key[1]], difference.negated()]
                    )
                    cache[key] = difference
                weighted_terms.append(coefficient * difference)
            sequence_terms.append(weighted_terms)

        (a_lower, a_upper), (b_lower, b_upper) = fixed_compression_distance_bounds(
            lag
        )
        a_half = model.new_int_var(
            a_lower // 2, a_upper // 2, f"a_half_distance_{lag}"
        )
        b_half = model.new_int_var(
            b_lower // 2, b_upper // 2, f"b_half_distance_{lag}"
        )
        model.add(sum(sequence_terms[0]) == 2 * a_half).with_name(
            f"a_distance_{lag}"
        )
        model.add(sum(sequence_terms[1]) == 2 * b_half).with_name(
            f"b_distance_{lag}"
        )
        model.add(a_half + b_half == (N + 1) // 2).with_name(f"lp_lag_{lag}")

    return model, expanded_a, expanded_b, orbits


def signs(
    solver: cp_model.CpSolver, variables: Sequence[cp_model.IntVar]
) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--multiplier",
        type=int,
        default=121,
        help=(
            "order-three unit modulo 333; subgroup representatives are "
            f"{ORDER_THREE_MULTIPLIER_REPRESENTATIVES} (default: 121)"
        ),
    )
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=2048,
        help="CP-SAT memory cap in MiB (conservative default for a 16 GiB host)",
    )
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument("--log-search-progress", action="store_true")
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument(
        "--symmetry",
        choices=("none", "dihedral"),
        default="dihedral",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/legendre_pair_333_multiplier.json"),
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
        model, expanded_a, expanded_b, orbits = build_multiplier_model(
            args.multiplier, symmetry=args.symmetry == "dihedral"
        )
    except ValueError as error:
        print(f"error={error}", file=sys.stderr)
        return 2

    validation_error = model.validate()
    print(f"multiplier={args.multiplier}")
    print(f"orbit_count={len(orbits)}")
    print(f"representative_lag_count={len(representative_lags(args.multiplier))}")
    print(model.model_stats())
    print(f"model_validation={'passed' if not validation_error else 'failed'}")
    if validation_error:
        print(validation_error, file=sys.stderr)
        return 2
    if args.build_only:
        return 0

    print(f"workers={args.workers} max_memory_mb={args.max_memory_mb}")
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = args.time_limit
    solver.parameters.num_search_workers = args.workers
    solver.parameters.max_memory_in_mb = args.max_memory_mb
    solver.parameters.random_seed = args.random_seed
    solver.parameters.log_search_progress = args.log_search_progress
    status = solver.solve(model)
    print(f"status={solver.status_name(status)}")
    print(f"wall_time={solver.wall_time:.3f}")
    print(f"conflicts={solver.num_conflicts}")
    print(f"branches={solver.num_branches}")
    if status not in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        return 2

    a = signs(solver, expanded_a)
    b = signs(solver, expanded_b)
    report = verify_legendre_pair(a, b)
    if not report.valid:
        print("error=solver candidate failed exact verification", file=sys.stderr)
        return 3
    save_verified_candidate(args.output, a, b)
    print(f"solution={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
