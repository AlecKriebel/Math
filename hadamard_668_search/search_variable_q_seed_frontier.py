#!/usr/bin/env python3
"""Filter the first margin-plus-quad seed frontier with spectral identities.

The dependency-free seed-radius verifier enumerates every raw labelled margin
target near Eliahou's published seed and computes its exact minimum distance
subject to the mandatory endpoint-quad products.  This script builds one
small CP-SAT model for each surviving target, fixes its ordinary and
alternating margins, retains the raw Hamming ball, and adds the primitive
3rd-, 4th-, and 6th-root norm identities.  Optional primitive-7/14 or full
correlation layers can be enabled without changing the decomposition.

All models run sequentially with one worker and an explicit memory cap.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import gc
import json
from pathlib import Path
import sys

from ortools.sat.python import cp_model

from construction import goethals_seidel, verify_hadamard
from search_variable_q_cp_sat import equality_literal, residue_sign_sums
from seed import special_quadruple, summed_aperiodic_correlations
from variable_q_base import LONG, base_correlations, base_to_special
from variable_q_seed_distance import SEED, build_model as build_relaxation, verify_witness
from verify_variable_q_seed_quad_radius import (
    MarginTarget,
    check_radius,
    coordinate_class_sums,
)
from verify_variable_q_seed_radius import distance_to_margins


ENERGY = 334
SHARD_287_MINIMUM_TARGET: MarginTarget = (
    (-18, 18),
    (0, 0),
    (3, 1),
    (-1, -3),
)


@lru_cache(maxsize=None)
def _quadratic_norm_rows(
    bound: int, cross_sign: int
) -> tuple[tuple[int, int, int], ...]:
    """Return ``(a,b,norm)`` rows with norm at most the global energy."""

    if bound < 0 or cross_sign not in (-1, 0, 1):
        raise ValueError("invalid quadratic norm table parameters")
    rows = []
    for first in range(-bound, bound + 1):
        for second in range(-bound, bound + 1):
            norm = (
                first * first
                + cross_sign * first * second
                + second * second
            )
            if norm <= ENERGY:
                rows.append((first, second, norm))
    return tuple(rows)


def add_small_root_table_invariants(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
) -> None:
    """Add the primitive 3rd/4th/6th-root norms using exact tables.

    This is equivalent to ``add_small_root_spectral_invariants`` but avoids
    general multiplication constraints.  Since all four nonnegative norm
    contributions sum to 334, rows above 334 can be removed a priori.
    """

    totals: dict[int, list[cp_model.IntVar]] = {3: [], 4: [], 6: []}
    for label, bits in zip("abcd", sequences, strict=True):
        bound = len(bits)

        residues_3 = residue_sign_sums(model, bits, 3, f"{label}_table_mod3")
        z3_a = model.new_int_var(-bound, bound, f"{label}_table_z3_a")
        z3_b = model.new_int_var(-bound, bound, f"{label}_table_z3_b")
        z3_norm = model.new_int_var(0, ENERGY, f"{label}_table_z3_norm")
        model.add(z3_a == residues_3[0] - residues_3[2])
        model.add(z3_b == residues_3[1] - residues_3[2])
        model.add_allowed_assignments(
            (z3_a, z3_b, z3_norm), _quadratic_norm_rows(bound, -1)
        )
        totals[3].append(z3_norm)

        residues_4 = residue_sign_sums(model, bits, 4, f"{label}_table_mod4")
        z4_real = model.new_int_var(-bound, bound, f"{label}_table_z4_real")
        z4_imag = model.new_int_var(-bound, bound, f"{label}_table_z4_imag")
        z4_norm = model.new_int_var(0, ENERGY, f"{label}_table_z4_norm")
        model.add(z4_real == residues_4[0] - residues_4[2])
        model.add(z4_imag == residues_4[1] - residues_4[3])
        model.add_allowed_assignments(
            (z4_real, z4_imag, z4_norm), _quadratic_norm_rows(bound, 0)
        )
        totals[4].append(z4_norm)

        residues_6 = residue_sign_sums(model, bits, 6, f"{label}_table_mod6")
        z6_a = model.new_int_var(-bound, bound, f"{label}_table_z6_a")
        z6_b = model.new_int_var(-bound, bound, f"{label}_table_z6_b")
        z6_norm = model.new_int_var(0, ENERGY, f"{label}_table_z6_norm")
        model.add(
            z6_a
            == residues_6[0] - residues_6[2] - residues_6[3] + residues_6[5]
        )
        model.add(
            z6_b
            == residues_6[1] + residues_6[2] - residues_6[4] - residues_6[5]
        )
        model.add_allowed_assignments(
            (z6_a, z6_b, z6_norm), _quadratic_norm_rows(bound, 1)
        )
        totals[6].append(z6_norm)

    for modulus in (3, 4, 6):
        model.add(sum(totals[modulus]) == ENERGY)


def add_flip_direction_budget(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
    target: MarginTarget,
    radius: int,
) -> None:
    """Expose the exact classwise flip counts implied by fixed margins.

    In one coordinate class, let ``delta`` be half the desired change in its
    sign sum.  If ``delta > 0``, at least ``delta`` seed-minus signs must flip
    and every seed-plus flip requires one additional compensating seed-minus
    flip.  The other signs are symmetric.  Thus the total number of
    opposite-direction flips over all eight classes is exactly half the
    excess over the unconstrained margin distance.  Stating these redundant
    cardinalities explicitly gives CP-SAT much stronger propagation.
    """

    minimum = distance_to_margins(target)
    if minimum > radius:
        raise ValueError("fixed target lies outside the requested seed ball")
    extra_pairs = (radius - minimum) // 2
    wrong_direction_counts = []
    for sequence_index, (bits, margins, seed) in enumerate(
        zip(sequences, target, SEED, strict=True)
    ):
        ordinary, alternating = margins
        desired = (
            (ordinary + alternating) // 2,
            (ordinary - alternating) // 2,
        )
        current = coordinate_class_sums(seed)
        for parity in (0, 1):
            class_change = desired[parity] - current[parity]
            if class_change % 2:
                raise ValueError("fixed target has unreachable class parity")
            delta = class_change // 2
            plus_seed_flips = [
                bits[index].negated()
                for index in range(parity, len(bits), 2)
                if seed[index] == 1
            ]
            minus_seed_flips = [
                bits[index]
                for index in range(parity, len(bits), 2)
                if seed[index] == -1
            ]
            wrong = model.new_int_var(
                0,
                extra_pairs,
                f"wrong_direction_{sequence_index}_{parity}",
            )
            if delta >= 0:
                model.add(sum(plus_seed_flips) == wrong)
                model.add(sum(minus_seed_flips) == delta + wrong)
            else:
                model.add(sum(minus_seed_flips) == wrong)
                model.add(sum(plus_seed_flips) == -delta + wrong)
            wrong_direction_counts.append(wrong)
    model.add(sum(wrong_direction_counts) <= extra_pairs)


def add_radius_sixteen_shard_287_structure(
    model: cp_model.CpModel,
    sequences: tuple[list[cp_model.IntVar], ...],
    target: MarginTarget,
    radius: int,
) -> bool:
    """Expose the rigid flip structure of the sole hard radius-16 target.

    The target changes only A's odd-coordinate class and requires eight
    positive-to-negative flips there.  Those coordinates occupy distinct
    long endpoint quads.  Preserving quad products needs at least one partner
    flip in each selected quad.  At radius 16 equality is forced: exactly
    eight such A coordinates flip, exactly one of the other three cells in
    each selected quad flips, and every other sign is unchanged.
    """

    if radius != 16 or target != SHARD_287_MINIMUM_TARGET:
        return False
    flips = tuple(
        tuple(
            bit.negated() if seed_value == 1 else bit
            for bit, seed_value in zip(bits, seed, strict=True)
        )
        for bits, seed in zip(sequences, SEED, strict=True)
    )
    selected = []
    for left in range(LONG // 2):
        right = LONG - 1 - left
        odd = left if left % 2 else right
        even = right if left % 2 else left
        a_odd_flip = flips[0][odd]
        partners = (flips[0][even], flips[1][left], flips[1][right])
        if SEED[0][odd] == 1:
            model.add(sum(partners) == a_odd_flip)
            selected.append(a_odd_flip)
        else:
            model.add(a_odd_flip == 0)
            model.add(sum(partners) == 0)
    model.add(sum(selected) == 8)
    for group in flips[2:]:
        for flip in group:
            model.add(flip == 0)
    return True


def build_target_model(
    target: MarginTarget,
    radius: int,
    *,
    minimum_distance: int = 0,
    compression_7: bool = False,
    compression_7_alternating: bool = False,
    full_correlations: bool = False,
    small_root_encoding: str = "table",
) -> tuple[cp_model.CpModel, tuple[list[cp_model.IntVar], ...]]:
    """Build one fixed-margin seed-ball model at the selected proof layer."""

    if radius < 0 or not 0 <= minimum_distance <= radius:
        raise ValueError("distance interval must satisfy 0 <= minimum <= radius")
    if small_root_encoding not in ("table", "multiplication"):
        raise ValueError("small_root_encoding must be table or multiplication")
    model, sequences = build_relaxation(
        small_roots=small_root_encoding == "multiplication",
        compression_7=compression_7,
        compression_7_alternating=compression_7_alternating,
    )
    if small_root_encoding == "table":
        add_small_root_table_invariants(model, sequences)
    model.clear_objective()
    for bits, (ordinary, alternating) in zip(sequences, target, strict=True):
        model.add(2 * sum(bits) - len(bits) == ordinary)
        model.add(
            sum(
                (1 if index % 2 == 0 else -1) * (2 * bit - 1)
                for index, bit in enumerate(bits)
            )
            == alternating
        )

    differences = [
        bit.negated() if seed_value == 1 else bit
        for bits, seed in zip(sequences, SEED, strict=True)
        for bit, seed_value in zip(bits, seed, strict=True)
    ]
    model.add(sum(differences) <= radius)
    model.add(sum(differences) >= minimum_distance)
    add_flip_direction_budget(model, sequences, target, radius)
    add_radius_sixteen_shard_287_structure(model, sequences, target, radius)

    if full_correlations:
        for lag in range(1, LONG):
            terms = []
            for label, bits in zip("abcd", sequences, strict=True):
                terms.extend(
                    equality_literal(
                        model,
                        bits[index],
                        bits[index + lag],
                        f"{label}{label}_frontier_{lag}_{index}",
                    )
                    for index in range(len(bits) - lag)
                )
            model.add(sum(terms) == len(terms) // 2)
    return model, sequences


def _signs(
    solver: cp_model.CpSolver, variables: list[cp_model.IntVar]
) -> tuple[int, ...]:
    return tuple(1 if solver.value(variable) else -1 for variable in variables)


def _verify_exact(sequences: tuple[tuple[int, ...], ...]) -> None:
    if base_correlations(*sequences) != (334,) + (0,) * 83:
        raise AssertionError("frontier candidate failed exact base correlations")
    s, q = base_to_special(*sequences)
    if any(summed_aperiodic_correlations(special_quadruple(s, q))[1:]):
        raise AssertionError("frontier candidate failed exact special correlations")
    verify_hadamard(goethals_seidel(special_quadruple(s, q)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--radius", type=int, default=14)
    parser.add_argument("--minimum-distance", type=int, default=0)
    parser.add_argument("--compression-7", action="store_true")
    parser.add_argument("--compression-7-alternating", action="store_true")
    parser.add_argument("--full-correlations", action="store_true")
    parser.add_argument(
        "--small-root-encoding",
        choices=("table", "multiplication"),
        default="table",
    )
    parser.add_argument("--time-limit-per-target", type=float, default=30.0)
    parser.add_argument("--max-memory-mb", type=int, default=256)
    parser.add_argument("--random-seed", type=int, default=668)
    parser.add_argument(
        "--resume-from",
        type=Path,
        help="reuse INFEASIBLE records from a compatible earlier JSON run",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/variable_q_seed_frontier_root_filter.json"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if (
        args.radius < 0
        or not 0 <= args.minimum_distance <= args.radius
        or args.time_limit_per_target <= 0
        or args.max_memory_mb <= 0
    ):
        print(
            "error=distance interval must be valid and limits positive",
            file=sys.stderr,
        )
        return 2

    radius_check = check_radius(args.radius)
    frontier_records = []
    parity_skipped = 0
    for record in radius_check.targets:
        if record.quad_distance is None or record.quad_distance > args.radius:
            continue
        first_possible = max(args.minimum_distance, record.quad_distance)
        if (first_possible - record.margin_distance) % 2:
            first_possible += 1
        if first_possible > args.radius:
            parity_skipped += 1
            continue
        frontier_records.append(record)
    frontier = tuple(frontier_records)
    print(f"distance_interval=[{args.minimum_distance},{args.radius}]")
    print(f"margin_plus_quad_frontier={len(frontier)}")
    print(f"parity_skipped={parity_skipped}")
    print(f"workers=1 max_memory_mb={args.max_memory_mb}")

    reused_results = {}
    if args.resume_from:
        previous = json.loads(args.resume_from.read_text(encoding="utf-8"))
        previous_layers = previous.get("layers", {})
        expected_layers = {
            "small_roots": True,
            "small_root_encoding": args.small_root_encoding,
            "compression_7": args.compression_7,
            "compression_7_alternating": args.compression_7_alternating,
            "full_correlations": args.full_correlations,
            "radius_16_shard_287_structure": args.radius == 16,
        }
        if (
            previous.get("kind") != "variable-q-seed-frontier-filter"
            or previous.get("radius") != args.radius
            or previous.get("minimum_distance", 0) != args.minimum_distance
            or previous.get("frontier_size") != len(frontier)
            or previous_layers != expected_layers
        ):
            print("error=incompatible resume certificate", file=sys.stderr)
            return 2
        for result in previous.get("results", ()):
            if result.get("status") == "INFEASIBLE":
                key = (
                    int(result["shard"]),
                    tuple(tuple(pair) for pair in result["target"]),
                )
                reused_results[key] = result
        print(f"reused_infeasible={len(reused_results)}")

    results = []
    for attempt, record in enumerate(frontier, start=1):
        record_key = (record.shard, record.target)
        if record_key in reused_results:
            result = dict(reused_results[record_key])
            result["reused"] = True
            results.append(result)
            continue
        model, variables = build_target_model(
            record.target,
            args.radius,
            minimum_distance=args.minimum_distance,
            compression_7=args.compression_7,
            compression_7_alternating=args.compression_7_alternating,
            full_correlations=args.full_correlations,
            small_root_encoding=args.small_root_encoding,
        )
        validation = model.validate()
        if validation:
            print(f"error=invalid model: {validation}", file=sys.stderr)
            return 2
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = args.time_limit_per_target
        solver.parameters.num_search_workers = 1
        solver.parameters.max_memory_in_mb = args.max_memory_mb
        solver.parameters.random_seed = args.random_seed
        status = solver.solve(model)
        status_name = solver.status_name(status)
        result = {
            "shard": record.shard,
            "margin_distance": record.margin_distance,
            "quad_distance": record.quad_distance,
            "target": [list(pair) for pair in record.target],
            "status": status_name,
            "wall_time": solver.wall_time,
            "conflicts": solver.num_conflicts,
            "branches": solver.num_branches,
        }
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            sequences = tuple(_signs(solver, group) for group in variables)
            witness = verify_witness(
                sequences,
                small_roots=True,
                compression_7=args.compression_7,
                compression_7_alternating=args.compression_7_alternating,
            )
            if tuple(
                (witness.ordinary[index], witness.alternating[index])
                for index in range(4)
            ) != record.target:
                raise AssertionError("decoded witness has the wrong fixed margins")
            if witness.distance > args.radius:
                raise AssertionError("decoded witness lies outside the seed ball")
            if args.full_correlations:
                _verify_exact(sequences)
            result["distance"] = witness.distance
            result["sequences"] = {
                label: list(sequence)
                for label, sequence in zip("abcd", sequences, strict=True)
            }
        results.append(result)
        print(
            f"attempt={attempt}/{len(frontier)} shard={record.shard} "
            f"status={status_name} wall_time={solver.wall_time:.3f} "
            f"branches={solver.num_branches}"
        )
        del solver, model, variables
        gc.collect()

    payload = {
        "kind": "variable-q-seed-frontier-filter",
        "radius": args.radius,
        "minimum_distance": args.minimum_distance,
        "parity_skipped": parity_skipped,
        "frontier_size": len(frontier),
        "layers": {
            "small_roots": True,
            "small_root_encoding": args.small_root_encoding,
            "compression_7": args.compression_7,
            "compression_7_alternating": args.compression_7_alternating,
            "full_correlations": args.full_correlations,
            "radius_16_shard_287_structure": args.radius == 16,
        },
        "workers": 1,
        "max_memory_mb": args.max_memory_mb,
        "time_limit_per_target": args.time_limit_per_target,
        "resume_from": str(args.resume_from) if args.resume_from else None,
        "reused_infeasible": len(reused_results),
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote={args.output}")

    counts = {
        name: sum(result["status"] == name for result in results)
        for name in ("INFEASIBLE", "FEASIBLE", "OPTIMAL", "UNKNOWN")
    }
    print(f"status_counts={counts}")
    if results and counts["INFEASIBLE"] == len(results):
        print(
            "PASS: the selected spectral layer excludes the complete "
            f"margin-plus-quad frontier at radius {args.radius}"
        )
        return 0
    if counts["UNKNOWN"]:
        print("INCOMPLETE: at least one frontier model timed out")
        return 1
    print("SURVIVORS: at least one necessary-condition model is feasible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
