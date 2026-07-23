#!/usr/bin/env python3
"""Sample exact length-9 compression profiles for the LP(333) search.

This is a deliberately small outer search.  It does not search the 666 signs
of a Legendre pair.  Instead, for row sums ``a_i = 2*z_i + 1`` and
``b_i = 2*w_i + 1``, it enumerates the exact integer system

    sum(z) = sum(w) = -4,
    sum(z_i**2 + w_i**2) = 152,
    sum(z_i*z_(i+t) + w_i*w_(i+t)) = -15,  t = 1,2,3,4.

These equations are equivalent to combined cyclic PAF
``(594,-74,...,-74)`` for the two length-9 row compressions.  They are
necessary compressed conditions only; an emitted profile is neither an
``LP(333)`` nor a Hadamard-matrix certificate.

CP-SAT is always restricted to one worker.  Solutions are canonicalized
under the complete 1,944-element profile symmetry from
``legendre_333_profile_catalog``.  The callback writes a canonical profile
only on its first occurrence, so the requested count bounds the deduplication
memory and profile objects are never accumulated for output.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
import os
from pathlib import Path
import sys
from typing import Any, TextIO

import ortools
from ortools.sat.python import cp_model

from legendre_333_profile_catalog import (
    EXACT_COMBINED_PAF,
    ROW_SUM_PROFILES,
    canonical_profile,
    combined_paf,
    plus_counts,
    profile_orbit,
)


Z_MIN = -11
Z_MAX = 10
PROFILE_LENGTH = 9
DEFAULT_COUNT = 12
DEFAULT_TIME_LIMIT = 10.0
DEFAULT_MAX_MEMORY_MB = 128
CENTERED_NORM_SHARDS = tuple(range(76, 149, 2))
PROFILE_SYMMETRY_MODES = ("none", "basic")


def validate_centered_norm_shard(value: int | None) -> None:
    """Validate an optional shard of the exact combined norm 152."""

    if value is not None and (
        type(value) is not int or value not in CENTERED_NORM_SHARDS
    ):
        raise ValueError("centered norm shard must be an even integer in [76,148]")


def build_profile_model(
    centered_norm_shard: int | None = None,
    profile_symmetry: str = "none",
) -> tuple[
    cp_model.CpModel, list[cp_model.IntVar], list[cp_model.IntVar]
]:
    """Build the exact 18-coordinate compressed-profile model."""

    validate_centered_norm_shard(centered_norm_shard)
    if profile_symmetry not in PROFILE_SYMMETRY_MODES:
        raise ValueError("profile symmetry must be 'none' or 'basic'")
    model = cp_model.CpModel()
    z = [
        model.new_int_var(Z_MIN, Z_MAX, f"z_{index}")
        for index in range(PROFILE_LENGTH)
    ]
    w = [
        model.new_int_var(Z_MIN, Z_MAX, f"w_{index}")
        for index in range(PROFILE_LENGTH)
    ]
    model.add(sum(z) == -4).with_name("sum_z")
    model.add(sum(w) == -4).with_name("sum_w")

    square_vectors: list[list[cp_model.IntVar]] = []
    for prefix, vector in (("z", z), ("w", w)):
        vector_squares: list[cp_model.IntVar] = []
        for index, value in enumerate(vector):
            square = model.new_int_var(0, 121, f"{prefix}_square_{index}")
            model.add_multiplication_equality(square, [value, value])
            vector_squares.append(square)
        square_vectors.append(vector_squares)
    z_squares, w_squares = square_vectors
    norm_z = model.new_int_var(4, 148, "norm_z")
    norm_w = model.new_int_var(4, 148, "norm_w")
    max_norm = model.new_int_var(76, 148, "max_centered_norm")
    model.add(norm_z == sum(z_squares)).with_name("norm_z_definition")
    model.add(norm_w == sum(w_squares)).with_name("norm_w_definition")
    model.add(norm_z + norm_w == 152).with_name("combined_norm")
    model.add_max_equality(max_norm, [norm_z, norm_w]).with_name(
        "max_centered_norm_definition"
    )
    if centered_norm_shard is not None:
        model.add(max_norm == centered_norm_shard).with_name(
            "centered_norm_shard"
        )

    for lag in range(1, 5):
        products: list[cp_model.IntVar] = []
        for prefix, vector in (("z", z), ("w", w)):
            for index in range(PROFILE_LENGTH):
                product = model.new_int_var(
                    -121, 121, f"{prefix}_product_{lag}_{index}"
                )
                model.add_multiplication_equality(
                    product,
                    [vector[index], vector[(index + lag) % PROFILE_LENGTH]],
                )
                products.append(product)
        model.add(sum(products) == -15).with_name(
            f"combined_correlation_{lag}"
        )
    if profile_symmetry == "basic":
        add_basic_profile_symmetry(model, z, w)
    return model, z, w


def _equality_literal(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    equal = model.new_bool_var(name)
    model.add(left == right).only_enforce_if(equal)
    model.add(left != right).only_enforce_if(equal.negated())
    return equal


def _add_lexicographic_greater_or_equal(
    model: cp_model.CpModel,
    left: Sequence[cp_model.IntVar],
    right: Sequence[cp_model.IntVar],
    name: str,
) -> None:
    """Add the exact integer-vector constraint ``left >=lex right``."""

    if len(left) != len(right):
        raise ValueError("lexicographic vectors must have equal length")
    if not left:
        return
    prefix_equal = model.new_bool_var(f"{name}_prefix_0")
    model.add(prefix_equal == 1)
    for index, (left_value, right_value) in enumerate(
        zip(left, right, strict=True)
    ):
        model.add(left_value >= right_value).only_enforce_if(prefix_equal)
        if index + 1 == len(left):
            break
        equal = _equality_literal(
            model, left_value, right_value, f"{name}_equal_{index}"
        )
        next_prefix = model.new_bool_var(f"{name}_prefix_{index + 1}")
        model.add(next_prefix <= prefix_equal)
        model.add(next_prefix <= equal)
        model.add(next_prefix >= prefix_equal + equal - 1)
        prefix_equal = next_prefix


def _dihedral_variable_image(
    vector: Sequence[cp_model.IntVar], reflection: int, shift: int
) -> tuple[cp_model.IntVar, ...]:
    return tuple(
        vector[(reflection * index + shift) % PROFILE_LENGTH]
        for index in range(PROFILE_LENGTH)
    )


def add_basic_profile_symmetry(
    model: cp_model.CpModel,
    z: Sequence[cp_model.IntVar],
    w: Sequence[cp_model.IntVar],
) -> None:
    """Break the independent dihedral subgroup and sequence interchange."""

    for prefix, vector in (("z", z), ("w", w)):
        for reflection in (-1, 1):
            for shift in range(PROFILE_LENGTH):
                if reflection == 1 and shift == 0:
                    continue
                _add_lexicographic_greater_or_equal(
                    model,
                    vector,
                    _dihedral_variable_image(vector, reflection, shift),
                    f"{prefix}_dihedral_{reflection}_{shift}",
                )
    _add_lexicographic_greater_or_equal(
        model, z, w, "sequence_interchange"
    )


def _z_coordinates(row_sums: Sequence[int]) -> tuple[int, ...]:
    return tuple((value - 1) // 2 for value in row_sums)


def profile_centered_norm_shard(
    a: Sequence[int], b: Sequence[int]
) -> int:
    """Return the swap-invariant maximum centered norm of one profile."""

    z = _z_coordinates(a)
    w = _z_coordinates(b)
    return max(
        sum(value * value for value in z),
        sum(value * value for value in w),
    )


def add_catalog_hint(
    model: cp_model.CpModel,
    z: Sequence[cp_model.IntVar],
    w: Sequence[cp_model.IntVar],
    random_seed: int,
    centered_norm_shard: int | None = None,
) -> int | None:
    """Add one reproducibly selected known profile as a nonbinding hint."""

    validate_centered_norm_shard(centered_norm_shard)
    profile_indices = tuple(
        index
        for index, profile in enumerate(ROW_SUM_PROFILES)
        if centered_norm_shard is None
        or profile_centered_norm_shard(*profile) == centered_norm_shard
    )
    if not profile_indices:
        return None
    profile_index = profile_indices[random_seed % len(profile_indices)]
    hint_a, hint_b = canonical_profile(*ROW_SUM_PROFILES[profile_index])
    for variable, value in zip(z, _z_coordinates(hint_a), strict=True):
        model.add_hint(variable, value)
    for variable, value in zip(w, _z_coordinates(hint_b), strict=True):
        model.add_hint(variable, value)
    return profile_index


def exclude_catalog_orbits(
    model: cp_model.CpModel,
    z: Sequence[cp_model.IntVar],
    w: Sequence[cp_model.IntVar],
    centered_norm_shard: int | None = None,
) -> tuple[int, int]:
    """Forbid every oriented image of each catalog orbit in this shard."""

    validate_centered_norm_shard(centered_norm_shard)
    excluded_profiles = tuple(
        profile
        for profile in ROW_SUM_PROFILES
        if centered_norm_shard is None
        or profile_centered_norm_shard(*profile) == centered_norm_shard
    )
    assignments = {
        _z_coordinates(image_a) + _z_coordinates(image_b)
        for profile in excluded_profiles
        for image_a, image_b in profile_orbit(*profile)
    }
    if assignments:
        model.add_forbidden_assignments(
            tuple(z) + tuple(w), sorted(assignments)
        ).with_name("exclude_catalog_profile_orbits")
    return len(excluded_profiles), len(assignments)


def validate_canonical_profile(
    a: Sequence[int], b: Sequence[int]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Validate one emitted profile using the catalog's exact helpers."""

    immutable_a = tuple(a)
    immutable_b = tuple(b)
    plus_counts(immutable_a)
    plus_counts(immutable_b)
    if sum(immutable_a) != 1 or sum(immutable_b) != 1:
        raise ValueError("compressed row sums must each sum to one")
    if combined_paf((immutable_a, immutable_b)) != EXACT_COMBINED_PAF:
        raise ValueError("profile fails the exact length-9 PAF equations")
    if canonical_profile(immutable_a, immutable_b) != (
        immutable_a,
        immutable_b,
    ):
        raise ValueError("profile is not the canonical orbit representative")

    z = _z_coordinates(immutable_a)
    w = _z_coordinates(immutable_b)
    if any(not Z_MIN <= value <= Z_MAX for value in z + w):
        raise ValueError("profile lies outside the exact z-coordinate bounds")
    if sum(z) != -4 or sum(w) != -4:
        raise ValueError("profile fails the centered sum equations")
    if sum(value * value for value in z + w) != 152:
        raise ValueError("profile fails the centered norm equation")
    return immutable_a, immutable_b


def profile_payload(
    index: int, a: Sequence[int], b: Sequence[int]
) -> dict[str, Any]:
    """Return a self-checking JSON object for one canonical profile."""

    immutable_a, immutable_b = validate_canonical_profile(a, b)
    z = _z_coordinates(immutable_a)
    w = _z_coordinates(immutable_b)
    return {
        "index": index,
        "row_sums_a": list(immutable_a),
        "row_sums_b": list(immutable_b),
        "row_plus_counts_a": list(plus_counts(immutable_a)),
        "row_plus_counts_b": list(plus_counts(immutable_b)),
        "centered_norms": [
            sum(value * value for value in z),
            sum(value * value for value in w),
        ],
        "combined_cyclic_paf_0_through_8": list(
            combined_paf((immutable_a, immutable_b))
        ),
        "canonicalization": "lp333-fixed-seed-profile-lexmax-v1",
        "compressed_constraints_verified": True,
        "full_legendre_pair_verified": False,
        "hadamard_668_verified": False,
    }


class JsonSampleWriter:
    """Incrementally write one valid JSON document without retaining profiles."""

    def __init__(self, stream: TextIO, metadata: dict[str, Any]) -> None:
        self._stream = stream
        self._first = True
        self._closed = False
        self._stream.write("{\n")
        for key, value in metadata.items():
            self._stream.write(f"  {json.dumps(key)}: ")
            json.dump(value, self._stream, separators=(",", ":"))
            self._stream.write(",\n")
        self._stream.write('  "profiles": [')

    def write_profile(self, payload: dict[str, Any]) -> None:
        if self._closed:
            raise RuntimeError("cannot write to a finished JSON sample")
        self._stream.write("\n    " if self._first else ",\n    ")
        json.dump(payload, self._stream, separators=(",", ":"))
        self._stream.flush()
        self._first = False

    def finish(self, result: dict[str, Any]) -> None:
        if self._closed:
            raise RuntimeError("JSON sample is already finished")
        if not self._first:
            self._stream.write("\n  ")
        self._stream.write("],\n  \"result\": ")
        json.dump(result, self._stream, separators=(",", ":"))
        self._stream.write("\n}\n")
        self._stream.flush()
        self._closed = True


class CanonicalProfileCollector(cp_model.CpSolverSolutionCallback):
    """Canonicalize raw solutions and stream orbit-distinct representatives."""

    def __init__(
        self,
        z: Sequence[cp_model.IntVar],
        w: Sequence[cp_model.IntVar],
        writer: JsonSampleWriter,
        count_limit: int,
    ) -> None:
        super().__init__()
        self._z = tuple(z)
        self._w = tuple(w)
        self._writer = writer
        self._count_limit = count_limit
        self._seen: set[tuple[int, ...]] = set()
        self.raw_solution_count = 0
        self.duplicate_orbit_count = 0
        self.profile_count = 0
        self.stopped_after_count = False

    def on_solution_callback(self) -> None:
        self.raw_solution_count += 1
        raw_a = tuple(2 * self.value(variable) + 1 for variable in self._z)
        raw_b = tuple(2 * self.value(variable) + 1 for variable in self._w)
        canonical_a, canonical_b = canonical_profile(raw_a, raw_b)
        key = canonical_a + canonical_b
        if key in self._seen:
            self.duplicate_orbit_count += 1
            return

        # Validate before recording the key or writing any bytes.  A failed
        # arithmetic check therefore cannot appear as a partially trusted
        # profile in an otherwise valid output document.
        payload = profile_payload(self.profile_count, canonical_a, canonical_b)
        self._seen.add(key)
        self._writer.write_profile(payload)
        self.profile_count += 1
        if self.profile_count >= self._count_limit:
            self.stopped_after_count = True
            self.stop_search()


def configure_solver(
    *, time_limit: float, random_seed: int, max_memory_mb: int
) -> cp_model.CpSolver:
    """Return the fixed one-worker solver used by the CLI and tests."""

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit
    solver.parameters.num_search_workers = 1
    solver.parameters.max_memory_in_mb = max_memory_mb
    solver.parameters.random_seed = random_seed
    solver.parameters.randomize_search = True
    solver.parameters.enumerate_all_solutions = True
    return solver


def sample_to_stream(
    stream: TextIO,
    *,
    count: int,
    time_limit: float,
    random_seed: int,
    max_memory_mb: int,
    centered_norm_shard: int | None = None,
    exclude_catalog: bool = False,
    profile_symmetry: str = "basic",
) -> dict[str, Any]:
    """Run one bounded search and stream a complete JSON sample document."""

    if count <= 0:
        raise ValueError("count must be positive")
    if time_limit <= 0:
        raise ValueError("time_limit must be positive")
    if max_memory_mb <= 0:
        raise ValueError("max_memory_mb must be positive")
    validate_centered_norm_shard(centered_norm_shard)

    if profile_symmetry not in PROFILE_SYMMETRY_MODES:
        raise ValueError("profile symmetry must be 'none' or 'basic'")
    model, z, w = build_profile_model(centered_norm_shard, profile_symmetry)
    hint_profile = None
    excluded_catalog_orbits = 0
    excluded_catalog_assignments = 0
    if exclude_catalog:
        (
            excluded_catalog_orbits,
            excluded_catalog_assignments,
        ) = exclude_catalog_orbits(model, z, w, centered_norm_shard)
    else:
        hint_profile = add_catalog_hint(
            model, z, w, random_seed, centered_norm_shard
        )
    validation_error = model.validate()
    if validation_error:
        raise RuntimeError(f"invalid CP-SAT model: {validation_error}")

    metadata = {
        "schema": "hadamard668.legendre333-mod9-profile-sample.v1",
        "kind": "legendre333_mod9_compressed_profile_sample",
        "status": "necessary_compressed_conditions_only",
        "length": 333,
        "compression_modulus": 9,
        "block_size": 37,
        "requested_profile_count": count,
        "time_limit_seconds": time_limit,
        "random_seed": random_seed,
        "catalog_hint_profile": hint_profile,
        "catalog_orbits_excluded": excluded_catalog_orbits,
        "catalog_oriented_assignments_excluded": excluded_catalog_assignments,
        "profile_symmetry": profile_symmetry,
        "solver_workers": 1,
        "solver_memory_limit_mib": max_memory_mb,
        "ortools_version": ortools.__version__,
    }
    if centered_norm_shard is not None:
        metadata["centered_norm_shard"] = centered_norm_shard
        metadata["centered_norm_shard_definition"] = (
            "max(sum(z_i^2),sum(w_i^2))"
        )
    writer = JsonSampleWriter(stream, metadata)
    collector = CanonicalProfileCollector(z, w, writer, count)
    solver = configure_solver(
        time_limit=time_limit,
        random_seed=random_seed,
        max_memory_mb=max_memory_mb,
    )
    status = solver.solve(model, collector)
    exhaustive = (
        status in (cp_model.OPTIMAL, cp_model.INFEASIBLE)
        and not collector.stopped_after_count
    )
    result = {
        "solver_status": solver.status_name(status),
        "profile_count": collector.profile_count,
        "raw_solution_count": collector.raw_solution_count,
        "duplicate_orbit_count": collector.duplicate_orbit_count,
        "stopped_after_requested_count": collector.stopped_after_count,
        "exhaustive": exhaustive,
        "solver_wall_time_seconds": solver.wall_time,
        "branches": solver.num_branches,
        "conflicts": solver.num_conflicts,
    }
    if centered_norm_shard is not None:
        result["centered_norm_shard"] = centered_norm_shard
        result["shard_exhaustive"] = exhaustive
    writer.finish(result)
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--time-limit", type=float, default=DEFAULT_TIME_LIMIT)
    parser.add_argument(
        "--seed", "--random-seed", dest="random_seed", type=int, default=668
    )
    parser.add_argument(
        "--max-memory-mb",
        type=int,
        default=DEFAULT_MAX_MEMORY_MB,
        help="CP-SAT memory limit in MiB (default: 128)",
    )
    parser.add_argument(
        "--centered-norm-shard",
        type=int,
        choices=CENTERED_NORM_SHARDS,
        metavar="EVEN_76..148",
        help=(
            "restrict to max(sum(z_i^2),sum(w_i^2)) = M; the 37 even "
            "values 76 through 148 exactly partition the profile model"
        ),
    )
    parser.add_argument(
        "--exclude-catalog",
        action="store_true",
        help=(
            "forbid every oriented image of each already catalogued orbit "
            "in the selected shard"
        ),
    )
    parser.add_argument(
        "--profile-symmetry",
        choices=PROFILE_SYMMETRY_MODES,
        default="basic",
        help=(
            "outer-profile symmetry breaking (default: basic independent "
            "dihedral maxima plus sequence interchange)"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/legendre_333_mod9_profile_sample.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.count <= 0:
        print("error: --count must be positive", file=sys.stderr)
        return 2
    if args.time_limit <= 0:
        print("error: --time-limit must be positive", file=sys.stderr)
        return 2
    if args.max_memory_mb <= 0:
        print("error: --max-memory-mb must be positive", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_name(args.output.name + ".tmp")
    try:
        with temporary.open("w", encoding="utf-8") as stream:
            result = sample_to_stream(
                stream,
                count=args.count,
                time_limit=args.time_limit,
                random_seed=args.random_seed,
                max_memory_mb=args.max_memory_mb,
                centered_norm_shard=args.centered_norm_shard,
                exclude_catalog=args.exclude_catalog,
                profile_symmetry=args.profile_symmetry,
            )
        os.replace(temporary, args.output)
    except (OSError, RuntimeError, ValueError) as error:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(
        f"profiles={result['profile_count']} "
        f"raw_solutions={result['raw_solution_count']} "
        f"status={result['solver_status']} output={args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
