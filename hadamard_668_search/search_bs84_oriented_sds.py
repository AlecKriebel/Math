#!/usr/bin/env python3
"""Resumable Stage-A constructor for the prime-83 endpoint fold.

This searches the 45 anchored size profiles from ``NOVEL_BS84_THEORY.md``.
It is not the old 334-sign aperiodic search.  The model uses:

* one eight-valued state on each inverse pair ``{g,-g}``, enforcing the
  oriented parity condition at variable-definition time;
* each unordered residue-pair product exactly once, assigned to its unique
  distance class among the 41 periodic equations;
* the fixed row-sum profile and valid multiplier/phase normalizations.

Every Stage-A solution is written as a standalone JSON certificate and
independently verified.  Its complete ``82 * 83^2`` common-multiplier and
independent ``C,D`` phase portfolio is then hash-joined against the modulo-84
fold.  Any lift is expanded and strictly verified as an order-668 Hadamard
matrix before it is reported.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import random
import resource
import sys
import time
from typing import Any

from ortools.sat.python import cp_model

from verify_bs84_oriented_sds import (
    ENERGY,
    FORMAT,
    HALF,
    PRIME,
    canonical_profiles,
    folded_sequences,
    reconstruct_lift,
    verify_payload,
)


CHECKPOINT_FORMAT = "h668-oriented-sds-search-v1"
MODEL_VERSION = "osds41-pair-products-v1"
BASE_DIRECTORY = Path(__file__).resolve().parent
ALLOWED_PAIR_STATES = tuple(
    (state, *bits)
    for state, bits in enumerate(
        tuple(
            bits
            for bits in itertools.product((0, 1), repeat=4)
            if (bits[0] + bits[1] - bits[2] - bits[3]) % 2 == 0
        )
    )
)
if len(ALLOWED_PAIR_STATES) != 8:
    raise AssertionError("the oriented inverse-pair table must have 8 states")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def peak_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return value / (1024.0 * 1024.0)
    return value / 1024.0


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def equality_product(
    model: cp_model.CpModel,
    left: cp_model.IntVar,
    right: cp_model.IntVar,
    name: str,
) -> cp_model.IntVar:
    """Return the Boolean AND of two incidence variables."""

    product = model.new_bool_var(name)
    model.add(product <= left)
    model.add(product <= right)
    model.add(product >= left + right - 1)
    return product


def build_model(
    profile_index: int,
    hint_sets: tuple[frozenset[int], ...] | None = None,
    *,
    minimize_hint_distance: bool = False,
    max_hint_distance: int | None = None,
) -> tuple[
    cp_model.CpModel,
    tuple[list[cp_model.IntVar], ...],
    list[cp_model.IntVar],
]:
    profiles = canonical_profiles()
    if not 0 <= profile_index < len(profiles):
        raise ValueError("profile index must lie in 0..44")
    sizes = profiles[profile_index]
    model = cp_model.CpModel()
    blocks = tuple(
        [model.new_bool_var(f"{label}_{index}") for index in range(PRIME)]
        for label in "xyzw"
    )
    x_bits, y_bits, z_bits, w_bits = blocks
    model.add(x_bits[0] == 0)
    model.add(y_bits[0] == 0)
    for bits, size in zip(blocks, sizes):
        model.add(sum(bits) == size)

    # Equation (7) is not left to propagation through the quadratic counts:
    # each inverse pair is one eight-valued oriented state.
    pair_states = []
    for lag in range(1, HALF + 1):
        inverse = PRIME - lag
        state = model.new_int_var(0, 7, f"pair_state_{lag}")
        model.add_allowed_assignments(
            [state, x_bits[lag], x_bits[inverse], y_bits[lag], y_bits[inverse]],
            ALLOWED_PAIR_STATES,
        )
        pair_states.append(state)

    # Valid group-action normalizations.  X is nonempty in every profile, so
    # a common multiplier can put one member at residue 1.  Z and W are both
    # nonempty, and their independent translations can put a member at zero.
    model.add(x_bits[1] == 1)
    model.add(z_bits[0] == 1)
    model.add(w_bits[0] == 1)

    # Each unordered residue pair has one distance in 1..41.  Consequently
    # every product below occurs in exactly one equation, with no redundant
    # directed-lag copy.
    difference_terms: list[list[list[cp_model.IntVar]]] = [
        [[] for _lag in range(HALF + 1)] for _block in range(4)
    ]
    product_count = 0
    for block_index, bits in enumerate(blocks):
        for left in range(PRIME):
            for right in range(left + 1, PRIME):
                if block_index < 2 and left == 0:
                    # X,Y omit zero, so this product is identically zero.
                    continue
                difference = right - left
                lag = min(difference, PRIME - difference)
                product = equality_product(
                    model,
                    bits[left],
                    bits[right],
                    f"p_{block_index}_{left}_{right}",
                )
                difference_terms[block_index][lag].append(product)
                product_count += 1
    if product_count != 2 * (82 * 81 // 2) + 2 * (83 * 82 // 2):
        raise AssertionError(f"unexpected pair-product count {product_count}")

    total_size = sum(sizes)
    target = total_size - PRIME
    for lag in range(1, HALF + 1):
        inverse = PRIME - lag
        charge = model.new_int_var(-1, 1, f"charge_{lag}")
        model.add(
            2 * charge
            == x_bits[lag]
            + x_bits[inverse]
            - y_bits[lag]
            - y_bits[inverse]
        )
        counts = [
            term
            for block_terms in difference_terms
            for term in block_terms[lag]
        ]
        model.add(sum(counts) + charge == target)

    if hint_sets is not None:
        if len(hint_sets) != 4:
            raise ValueError("a Stage-A hint must contain four sets")
        distance_terms = []
        for bits, hint in zip(blocks, hint_sets):
            for index, variable in enumerate(bits):
                value = int(index in hint)
                model.add_hint(variable, value)
                distance_terms.append(variable.negated() if value else variable)
        if max_hint_distance is not None:
            model.add(sum(distance_terms) <= max_hint_distance)
        if minimize_hint_distance:
            model.minimize(sum(distance_terms))

    return model, blocks, pair_states


def profile_priority(index: int) -> tuple[int, ...]:
    """Theory-directed order: small orientation charge, then balanced blocks."""

    x_size, y_size, z_size, w_size = canonical_profiles()[index]
    row_sums = (
        82 - 2 * x_size,
        84 - 2 * y_size,
        83 - 2 * z_size,
        83 - 2 * w_size,
    )
    return (
        abs(x_size - y_size),
        abs(z_size - w_size),
        max(abs(value) for value in row_sums),
        sum(abs(value) for value in row_sums),
        index,
    )


def candidate_payload(
    profile_index: int,
    blocks: tuple[list[cp_model.IntVar], ...],
    solver: cp_model.CpSolver,
    *,
    seed: int,
    round_index: int,
) -> dict[str, Any]:
    sets = tuple(
        frozenset(
            index for index, variable in enumerate(bits)
            if solver.boolean_value(variable)
        )
        for bits in blocks
    )
    folded = folded_sequences(*sets)
    paf = tuple(
        sum(
            sum(
                sequence[index] * sequence[(index + lag) % PRIME]
                for index in range(PRIME)
            )
            for sequence in folded
        )
        for lag in range(PRIME)
    )
    sizes = tuple(len(block) for block in sets)
    return {
        "format": FORMAT,
        "modulus": PRIME,
        "model_version": MODEL_VERSION,
        "profile_index": profile_index,
        "profile": dict(zip(("x", "y", "z", "w"), sizes)),
        "search": {
            "random_seed": seed,
            "round_index": round_index,
            "solver_status": "FEASIBLE",
        },
        "x": sorted(sets[0]),
        "y": sorted(sets[1]),
        "z": sorted(sets[2]),
        "w": sorted(sets[3]),
        "fold_u": list(folded[0]),
        "fold_v": list(folded[1]),
        "fold_c": list(folded[2]),
        "fold_d": list(folded[3]),
        "periodic_paf_sum": list(paf),
        "lift": None,
    }


def padded_half_paf(sequence: tuple[int, ...]) -> tuple[int, ...]:
    if len(sequence) != PRIME:
        raise ValueError("expected a length-83 short sequence")
    padded = (*sequence, 0)
    return tuple(
        sum(
            padded[index] * padded[(index + lag) % (PRIME + 1)]
            for index in range(PRIME + 1)
        )
        for lag in range(1, (PRIME + 1) // 2 + 1)
    )


def long_half_paf(sequence: tuple[int, ...]) -> tuple[int, ...]:
    if len(sequence) != PRIME + 1:
        raise ValueError("expected a length-84 long sequence")
    return tuple(
        sum(
            sequence[index] * sequence[(index + lag) % (PRIME + 1)]
            for index in range(PRIME + 1)
        )
        for lag in range(1, (PRIME + 1) // 2 + 1)
    )


def add_exhaustive_lift(
    payload: dict[str, Any],
) -> tuple[int, list[tuple[int, int, int]]]:
    """Hash-join all 564,898 basic lifts and attach the first exact one."""

    sets = tuple(frozenset(payload[label]) for label in "xyzw")
    folded = folded_sequences(*sets)
    u, v, c, d = folded
    hits: list[tuple[int, int, int]] = []
    tested = 0
    first_base: tuple[tuple[int, ...], ...] | None = None
    for multiplier in range(1, PRIME):
        transformed_u = tuple(u[(multiplier * index) % PRIME] for index in range(PRIME))
        transformed_v = tuple(v[(multiplier * index) % PRIME] for index in range(PRIME))
        a = (1, *transformed_u[1:], -1)
        b = (1, *transformed_v[1:], 1)
        ab = tuple(
            left + right
            for left, right in zip(long_half_paf(a), long_half_paf(b))
        )
        c_signatures = []
        d_signature_to_shifts: dict[tuple[int, ...], list[int]] = {}
        for shift in range(PRIME):
            transformed_c = tuple(
                c[(multiplier * index + shift) % PRIME]
                for index in range(PRIME)
            )
            transformed_d = tuple(
                d[(multiplier * index + shift) % PRIME]
                for index in range(PRIME)
            )
            c_signatures.append(padded_half_paf(transformed_c))
            d_signature_to_shifts.setdefault(
                padded_half_paf(transformed_d), []
            ).append(shift)
        for shift_c, c_signature in enumerate(c_signatures):
            needed = tuple(
                -ab[index] - c_signature[index]
                for index in range(len(ab))
            )
            matching_d = d_signature_to_shifts.get(needed, ())
            for shift_d in matching_d:
                base = reconstruct_lift(folded, multiplier, shift_c, shift_d)
                # Directly check all 83 aperiodic equations, independently of
                # the hash condition and the adjacent-fold theorem.
                correlations = tuple(
                    sum(
                        sum(
                            sequence[index] * sequence[index + lag]
                            for index in range(len(sequence) - lag)
                        )
                        for sequence in base
                        if lag < len(sequence)
                    )
                    for lag in range(PRIME + 1)
                )
                if correlations != (ENERGY,) + (0,) * PRIME:
                    raise AssertionError("hash lift failed direct BS verification")
                hits.append((multiplier, shift_c, shift_d))
                if first_base is None:
                    first_base = base
            tested += len(d_signature_to_shifts.get(needed, ()))

    # ``tested`` above counts hash hits; the portfolio size is fixed and all
    # phase pairs were represented in the signature lookup.
    payload["lift_search"] = {
        "portfolio_size": (PRIME - 1) * PRIME * PRIME,
        "hash_matches": len(hits),
        "all_phase_pairs_tested": True,
    }
    if first_base is not None:
        multiplier, shift_c, shift_d = hits[0]
        payload["lift"] = {
            "common_multiplier": multiplier,
            "shift_c": shift_c,
            "shift_d": shift_d,
            "a": list(first_base[0]),
            "b": list(first_base[1]),
            "c": list(first_base[2]),
            "d": list(first_base[3]),
            "all_matching_parameters": [list(hit) for hit in hits],
        }
    return (PRIME - 1) * PRIME * PRIME, hits


def new_checkpoint() -> dict[str, Any]:
    profiles = canonical_profiles()
    return {
        "format": CHECKPOINT_FORMAT,
        "model_version": MODEL_VERSION,
        "created_utc": utc_now(),
        "updated_utc": utc_now(),
        "profile_count": len(profiles),
        "profiles": [
            {
                "index": index,
                "sizes": list(profile),
                "priority": list(profile_priority(index)),
            }
            for index, profile in enumerate(profiles)
        ],
        "attempts": [],
        "candidate_files": [],
        "exact_hadamard_files": [],
    }


def load_checkpoint(path: Path) -> dict[str, Any]:
    if not path.exists():
        return new_checkpoint()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if (
        not isinstance(payload, dict)
        or payload.get("format") != CHECKPOINT_FORMAT
        or payload.get("model_version") != MODEL_VERSION
    ):
        raise ValueError("checkpoint has the wrong format or model version")
    if payload.get("profile_count") != len(canonical_profiles()):
        raise ValueError("checkpoint profile count is inconsistent")
    if not isinstance(payload.get("attempts"), list):
        raise ValueError("checkpoint attempts must be a list")
    return payload


def load_hint(path: Path) -> tuple[int, tuple[frozenset[int], ...]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("hint must contain a JSON object")
    profile_index = payload.get("profile_index")
    if type(profile_index) is not int or not 0 <= profile_index < 45:
        raise ValueError("hint profile_index must lie in 0..44")
    sets = []
    for label in "xyzw":
        value = payload.get(label)
        if (
            not isinstance(value, list)
            or any(type(entry) is not int or not 0 <= entry < PRIME for entry in value)
            or len(set(value)) != len(value)
        ):
            raise ValueError(f"hint {label} must be a distinct residue list")
        sets.append(frozenset(value))
    if tuple(len(block) for block in sets) != canonical_profiles()[profile_index]:
        raise ValueError("hint set sizes disagree with its profile")
    return profile_index, tuple(sets)


def parse_profile_specification(value: str) -> tuple[int, ...]:
    if value == "all":
        return tuple(sorted(range(45), key=profile_priority))
    result = []
    for item in value.split(","):
        index = int(item)
        if not 0 <= index < 45:
            raise ValueError("profile indices must lie in 0..44")
        if index not in result:
            result.append(index)
    if not result:
        raise ValueError("at least one profile is required")
    return tuple(result)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkpoint",
        type=Path,
        default=BASE_DIRECTORY / "output/bs84_oriented_sds_stage_a.json",
    )
    parser.add_argument(
        "--candidate-directory",
        type=Path,
        default=BASE_DIRECTORY / "output/bs84_oriented_sds_candidates",
    )
    parser.add_argument("--profiles", default="all")
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--seconds-per-profile", type=float, default=10.0)
    parser.add_argument("--seed-base", type=int, default=668083)
    parser.add_argument("--max-memory-mb", type=int, default=3072)
    parser.add_argument("--hint", type=Path)
    parser.add_argument("--minimize-hint-distance", action="store_true")
    parser.add_argument("--max-hint-distance", type=int)
    parser.add_argument("--hint-search", action="store_true")
    parser.add_argument(
        "--lift-candidate",
        type=Path,
        help="skip Stage A and exhaustively lift an existing exact prime fold",
    )
    parser.add_argument(
        "--lift-output",
        type=Path,
        help="output path for --lift-candidate (defaults to *.lifted.json)",
    )
    parser.add_argument("--log-search-progress", action="store_true")
    parser.add_argument("--model-stats", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.lift_candidate is not None:
        payload = json.loads(args.lift_candidate.read_text(encoding="utf-8"))
        verify_payload(payload)
        portfolio_size, hits = add_exhaustive_lift(payload)
        verify_payload(payload)
        output = args.lift_output
        if output is None:
            output = args.lift_candidate.with_name(
                f"{args.lift_candidate.stem}.lifted.json"
            )
        if output.resolve() == args.lift_candidate.resolve():
            raise ValueError("--lift-output must not overwrite the input certificate")
        atomic_json(output, payload)
        print(f"candidate={args.lift_candidate}")
        print(f"portfolio_size={portfolio_size}")
        print(f"lift_matches={len(hits)}")
        print(f"output={output}")
        print(f"hadamard_verified={str(bool(hits)).lower()}")
        return 0
    if args.rounds <= 0:
        raise ValueError("--rounds must be positive")
    if args.seconds_per_profile <= 0:
        raise ValueError("--seconds-per-profile must be positive")
    if not 64 <= args.max_memory_mb <= 4096:
        raise ValueError("--max-memory-mb must lie in 64..4096")
    selected_profiles = parse_profile_specification(args.profiles)
    hint_profile = None
    hint_sets = None
    if args.hint is not None:
        hint_profile, hint_sets = load_hint(args.hint)
        if hint_profile not in selected_profiles:
            raise ValueError("--hint profile is not among --profiles")
    if (args.minimize_hint_distance or args.max_hint_distance is not None) and (
        hint_sets is None
    ):
        raise ValueError("hint-distance options require --hint")
    if args.max_hint_distance is not None and args.max_hint_distance < 0:
        raise ValueError("--max-hint-distance must be nonnegative")
    checkpoint = load_checkpoint(args.checkpoint)
    completed = {
        (attempt["profile_index"], attempt["round_index"])
        for attempt in checkpoint["attempts"]
        if isinstance(attempt, dict)
        and type(attempt.get("profile_index")) is int
        and type(attempt.get("round_index")) is int
    }
    candidate_hashes = set()
    for candidate_path in checkpoint.get("candidate_files", []):
        try:
            candidate_hashes.add(
                hashlib.sha256(Path(candidate_path).read_bytes()).hexdigest()
            )
        except OSError:
            pass

    print(f"profile_count={len(canonical_profiles())}")
    print(f"selected_profiles={','.join(str(value) for value in selected_profiles)}")
    print(f"rounds={args.rounds}")
    print(f"seconds_per_profile={args.seconds_per_profile}")
    print(f"max_memory_mb={args.max_memory_mb}")
    found_hadamard = False
    for round_index in range(args.rounds):
        for profile_index in selected_profiles:
            if (profile_index, round_index) in completed:
                continue
            seed = (
                args.seed_base + 1_000_003 * round_index + 10_007 * profile_index
            ) % 2_147_483_647
            active_hint = hint_sets if profile_index == hint_profile else None
            model, blocks, _pair_states = build_model(
                profile_index,
                active_hint,
                minimize_hint_distance=(
                    args.minimize_hint_distance and active_hint is not None
                ),
                max_hint_distance=(
                    args.max_hint_distance if active_hint is not None else None
                ),
            )
            if args.model_stats:
                print(model.model_stats())
            solver = cp_model.CpSolver()
            solver.parameters.max_time_in_seconds = args.seconds_per_profile
            solver.parameters.num_search_workers = 1
            solver.parameters.random_seed = seed
            solver.parameters.randomize_search = True
            if args.hint_search and active_hint is not None:
                solver.parameters.search_branching = cp_model.HINT_SEARCH
            solver.parameters.max_memory_in_mb = args.max_memory_mb
            solver.parameters.log_search_progress = args.log_search_progress
            started = time.monotonic()
            status = solver.solve(model)
            wall_seconds = time.monotonic() - started
            status_name = solver.status_name(status)
            attempt: dict[str, Any] = {
                "profile_index": profile_index,
                "profile": list(canonical_profiles()[profile_index]),
                "round_index": round_index,
                "random_seed": seed,
                "status": status_name,
                "wall_seconds": wall_seconds,
                "solver_wall_seconds": solver.wall_time,
                "branches": solver.num_branches,
                "conflicts": solver.num_conflicts,
                "peak_process_rss_mb": peak_rss_mb(),
            }
            print(
                f"profile={profile_index} round={round_index} "
                f"status={status_name} wall={wall_seconds:.3f}s "
                f"rss={attempt['peak_process_rss_mb']:.1f}MB"
            )
            if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
                payload = candidate_payload(
                    profile_index,
                    blocks,
                    solver,
                    seed=seed,
                    round_index=round_index,
                )
                verify_payload(payload)
                portfolio_size, hits = add_exhaustive_lift(payload)
                verify_payload(payload)
                digest = hashlib.sha256(
                    json.dumps(payload, sort_keys=True).encode("utf-8")
                ).hexdigest()
                candidate_path = args.candidate_directory / (
                    f"profile{profile_index:02d}_round{round_index:03d}_"
                    f"{digest[:12]}.json"
                )
                atomic_json(candidate_path, payload)
                file_digest = hashlib.sha256(candidate_path.read_bytes()).hexdigest()
                attempt["candidate"] = str(candidate_path)
                attempt["candidate_sha256"] = file_digest
                attempt["lift_portfolio_size"] = portfolio_size
                attempt["lift_match_count"] = len(hits)
                if file_digest not in candidate_hashes:
                    checkpoint.setdefault("candidate_files", []).append(
                        str(candidate_path)
                    )
                    candidate_hashes.add(file_digest)
                print(f"prime_fold={candidate_path}")
                print(f"lift_matches={len(hits)}")
                if hits:
                    checkpoint.setdefault("exact_hadamard_files", []).append(
                        str(candidate_path)
                    )
                    found_hadamard = True
                    print("hadamard_verified=true")
            checkpoint["attempts"].append(attempt)
            checkpoint["updated_utc"] = utc_now()
            checkpoint["last_peak_process_rss_mb"] = peak_rss_mb()
            atomic_json(args.checkpoint, checkpoint)
            completed.add((profile_index, round_index))

    print(f"checkpoint={args.checkpoint}")
    print(f"peak_process_rss_mb={peak_rss_mb():.1f}")
    print(f"hadamard_verified={str(found_hadamard).lower()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
