#!/usr/bin/env python3
"""Bounded digit-3 search on the exact c90c digit-2 manifold.

At each exact quadratic point, proposed moves lie in the kernel of the
digit-2 Jacobian and are biased by the digit-3 carry Jacobian.  The five-form
quadratic retraction is then applied identically, followed by Newton
restoration to all eighteen digit-2 equations.  Only restored exact points
are scored at digit 3.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import sys
import time

import numpy as np


HERE = Path(__file__).resolve().parent
SEARCH = HERE.parent
CARRY = SEARCH / "digit3_carry_algebra"
THEORY = SEARCH / "h0_orbit2_quadric_theory"
sys.path[:0] = [str(HERE), str(CARRY), str(THEORY), str(SEARCH)]

import audit_digit3_carry as carry  # noqa: E402
import search_retracted_newton as lift  # noqa: E402
from verify_quadric_character_compression import (  # noqa: E402
    nullspace_mod3,
)


START = (
    1, 2, 0, 0, 0, 1, 1, 0, 1, 1, 2, 2,
    1, 1, 1, 1, 1, 2, 0, 0, 1, 2, 1, 1,
    1, 2, 0, 2, 1, 2, 0, 1, 0, 1, 2, 2,
)


def compact_hash(value: object) -> str:
    return sha256(
        json.dumps(
            value, separators=(",", ":"), sort_keys=True
        ).encode()
    ).hexdigest()


def effective_rows(profiles, origin, basis):
    rows = []
    for terms, constant_at_zero in lift.second.second_digit_term_data(
        profiles
    ):
        grouped: dict[tuple[int, tuple[int, ...]], int] = defaultdict(int)
        for term in terms:
            constant = (
                term.constant
                + sum(
                    coefficient * origin[variable]
                    for variable, coefficient in term.coefficients
                )
            ) % 3
            slopes = tuple(
                sum(
                    coefficient * basis[column][variable]
                    for variable, coefficient in term.coefficients
                )
                % 3
                for column in range(36)
            )
            grouped[(constant, slopes)] += term.sign
        rows.append(
            (
                constant_at_zero,
                tuple(
                    (form, multiplicity)
                    for form, multiplicity in sorted(grouped.items())
                    if multiplicity
                ),
            )
        )
    return tuple(rows)


def cubic_values(rows, point: np.ndarray) -> np.ndarray:
    return np.array(
        [
            carry.cubic_digit_three(rows[index], point)
            for index in range(1, 20)
        ],
        dtype=np.int16,
    )


def cubic_jacobian(rows, point: np.ndarray) -> np.ndarray:
    values = lambda candidate: tuple(
        map(int, cubic_values(rows, np.array(candidate, dtype=np.int16)))
    )
    return np.array(
        carry.central_jacobian(values, tuple(map(int, point))),
        dtype=np.int16,
    )


def search(
    cpu_seconds: float,
    seed: int,
    restoration_samples: int,
    proposals_per_round: int,
) -> dict[str, object]:
    (
        profiles,
        origin,
        basis,
        q_constants,
        q_linears,
        q_polars,
    ) = lift.exact_forms("c90c")
    g_constants, g_linears, g_polars = lift.structured_forms(
        q_constants, q_linears, q_polars
    )
    subset = tuple(lift.PROFILES["c90c"]["retraction_subset"])
    _, directions = lift.retraction_data(
        subset, g_linears, g_polars
    )
    transform = lift.equation_basis(subset)
    h_constants = transform @ q_constants % 3
    h_linears = transform @ q_linears % 3
    h_polars = np.einsum(
        "ae,eij->aij", transform, q_polars
    ) % 3
    rows = effective_rows(profiles, origin, basis)
    rng = np.random.default_rng(seed)
    started_cpu = time.process_time()
    started_wall = time.monotonic()

    def within_budget() -> bool:
        return time.process_time() - started_cpu < cpu_seconds

    def retract(points: np.ndarray) -> np.ndarray:
        values = lift.evaluate_batch(
            g_constants[list(subset)],
            g_linears[list(subset)],
            g_polars[list(subset)],
            points,
        )
        result = (points - values @ directions.T) % 3
        if np.any(
            lift.evaluate_batch(
                g_constants[list(subset)],
                g_linears[list(subset)],
                g_polars[list(subset)],
                result,
            )
        ):
            raise AssertionError("five-form retraction failed")
        return result

    def q_values(point: np.ndarray) -> np.ndarray:
        return lift.evaluate(
            h_constants, h_linears, h_polars, point
        )

    restoration_attempts = 0
    restoration_successes = 0
    restoration_steps = 0

    def restore(start: np.ndarray) -> np.ndarray | None:
        nonlocal restoration_attempts, restoration_successes
        nonlocal restoration_steps
        restoration_attempts += 1
        point = retract(start.reshape(1, 36))[0]
        seen = set()
        for _ in range(90):
            if not within_budget():
                return None
            key = tuple(map(int, point))
            if key in seen:
                return None
            seen.add(key)
            values = q_values(point)
            defect = int(np.count_nonzero(values))
            if defect == 0:
                restoration_successes += 1
                return point
            jacobian = (
                h_linears
                + np.einsum("eij,j->ei", h_polars, point)
            ) % 3
            solved = lift.affine_solve(jacobian, -values)
            if solved is None:
                return None
            particular, kernel = solved
            sample_count = restoration_samples
            coefficients = rng.integers(
                0,
                3,
                size=(sample_count - 1, len(kernel)),
                dtype=np.int16,
            )
            deltas = np.vstack(
                (
                    particular,
                    (particular + coefficients @ kernel) % 3,
                )
            )
            candidates = retract((point + deltas) % 3)
            residuals = lift.evaluate_batch(
                h_constants, h_linears, h_polars, candidates
            )
            scores = np.count_nonzero(residuals, axis=1)
            minimum = int(scores.min())
            choices = np.flatnonzero(scores == minimum)
            if minimum <= 1 and len(choices) > 1:
                # The carry is used only as a tie break.  A point is not
                # recorded unless all quadratic rows are exactly zero.
                limited = choices[: min(24, len(choices))]
                carry_scores = np.array(
                    [
                        np.count_nonzero(cubic_values(rows, candidates[i]))
                        for i in limited
                    ]
                )
                point = candidates[
                    int(limited[int(np.argmin(carry_scores))])
                ]
            else:
                point = candidates[int(rng.choice(choices))]
            restoration_steps += 1
        return None

    initial = np.array(START, dtype=np.int16)
    if np.any(q_values(initial)):
        raise AssertionError("pinned starting point left digit 2")
    initial_cubic = cubic_values(rows, initial)
    initial_replay = lift.replay("c90c", initial)
    if int(np.count_nonzero(initial_cubic)) != 6:
        raise AssertionError("pinned starting defect changed")
    if initial_replay["nonzero_rows_by_digit"][3] != 6:
        raise AssertionError("carry and direct digit-3 replay disagree")

    pool: list[np.ndarray] = [initial]
    visited = {tuple(map(int, initial))}
    best = initial.copy()
    best_cubic = initial_cubic.copy()
    exact_solutions = 1
    tangent_proposals = 0
    rounds = 0

    while within_budget() and np.count_nonzero(best_cubic):
        base = pool[rounds % len(pool)]
        base_q_jacobian = (
            h_linears
            + np.einsum("eij,j->ei", h_polars, base)
        ) % 3
        tangent = nullspace_mod3(base_q_jacobian)
        if tangent.shape != (18, 36):
            # A rank drop is usable, but retain an exact record of it rather
            # than assuming the generic tangent dimension.
            if not len(tangent):
                break
        cubic = cubic_values(rows, base)
        carry_jacobian = cubic_jacobian(rows, base)
        restricted = carry_jacobian @ tangent.T % 3

        coefficient_candidates: list[np.ndarray] = []
        # First try the full linearized digit-3 target, then each 18-row
        # deletion.  These are the most direct tangent corrections.
        systems = [tuple(range(19))]
        systems.extend(
            tuple(index for index in range(19) if index != omitted)
            for omitted in range(19)
        )
        for selected in systems:
            solved = lift.affine_solve(
                restricted[list(selected)], -cubic[list(selected)]
            )
            if solved is None:
                continue
            particular, kernel = solved
            coefficient_candidates.append(particular)
            for _ in range(min(3, 3 ** min(len(kernel), 2) - 1)):
                weights = rng.integers(
                    0, 3, len(kernel), dtype=np.int16
                )
                coefficient_candidates.append(
                    (particular + weights @ kernel) % 3
                )

        # Add randomized systems containing every currently failed carry row
        # and enough satisfied rows to determine a tangent correction.
        failed = tuple(np.flatnonzero(cubic))
        satisfied = tuple(np.flatnonzero(cubic == 0))
        for _ in range(32):
            need = max(0, min(18, len(tangent)) - len(failed))
            selected_satisfied = (
                tuple(
                    map(
                        int,
                        rng.choice(
                            satisfied,
                            size=min(need, len(satisfied)),
                            replace=False,
                        ),
                    )
                )
                if need
                else ()
            )
            selected = failed + selected_satisfied
            solved = lift.affine_solve(
                restricted[list(selected)], -cubic[list(selected)]
            )
            if solved is not None:
                particular, kernel = solved
                weights = rng.integers(
                    0, 3, len(kernel), dtype=np.int16
                )
                coefficient_candidates.append(
                    (particular + weights @ kernel) % 3
                )

        # Random tangent moves prevent the linearized carry from trapping
        # the search in one local chart.
        coefficient_candidates.extend(
            rng.integers(0, 3, len(tangent), dtype=np.int16)
            for _ in range(48)
        )

        proposals = []
        seen_coefficients = set()
        for coefficients in coefficient_candidates:
            key = tuple(map(int, coefficients))
            if not any(key) or key in seen_coefficients:
                continue
            seen_coefficients.add(key)
            point = (base + coefficients @ tangent) % 3
            point = retract(point.reshape(1, 36))[0]
            residual = q_values(point)
            q_defect = int(np.count_nonzero(residual))
            approximate_cubic = int(
                np.count_nonzero(cubic_values(rows, point))
            )
            proposals.append(
                (
                    q_defect,
                    approximate_cubic,
                    int(np.count_nonzero(point != base)),
                    point,
                )
            )
        proposals.sort(key=lambda item: item[:3])
        tangent_proposals += len(proposals)

        new_points = []
        for _, _, _, proposal in proposals[:proposals_per_round]:
            if not within_budget():
                break
            restored = restore(proposal)
            if restored is None:
                continue
            key = tuple(map(int, restored))
            if key in visited:
                continue
            visited.add(key)
            exact_solutions += 1
            carry_values = cubic_values(rows, restored)
            replayed = lift.replay("c90c", restored)
            defect = int(np.count_nonzero(carry_values))
            if replayed["nonzero_rows_by_digit"][3] != defect:
                raise AssertionError("restored carry/direct replay mismatch")
            new_points.append(restored)
            if defect < int(np.count_nonzero(best_cubic)):
                best = restored.copy()
                best_cubic = carry_values.copy()
                if defect == 0:
                    break
        if new_points:
            pool.extend(new_points)
            pool.sort(
                key=lambda point: int(
                    np.count_nonzero(cubic_values(rows, point))
                )
            )
            pool = pool[:12]
        else:
            # A fresh exact point keeps the manifold walk moving if a local
            # tangent chart restores only to already visited solutions.
            fresh = restore(
                rng.integers(0, 3, 36, dtype=np.int16)
            )
            if fresh is not None:
                key = tuple(map(int, fresh))
                if key not in visited:
                    visited.add(key)
                    exact_solutions += 1
                    pool.append(fresh)
                    pool = pool[-12:]
        rounds += 1

    best_replay = lift.replay("c90c", best)
    best_defect = int(np.count_nonzero(best_cubic))
    result: dict[str, object] = {
        "schema": "h668-c90c-digit3-manifold-search-v1",
        "scope": (
            "Bounded Jacobian-kernel/retraction/Newton search on exact "
            "digit-2 points. UNKNOWN is not an exclusion."
        ),
        "profile_digest": lift.PROFILES["c90c"]["digest"],
        "status": "SAT_DIGIT3" if best_defect == 0 else "UNKNOWN",
        "seed": seed,
        "cpu_seconds_limit": cpu_seconds,
        "cpu_seconds_used": time.process_time() - started_cpu,
        "wall_seconds_used": time.monotonic() - started_wall,
        "restoration_samples": restoration_samples,
        "proposals_per_round": proposals_per_round,
        "rounds": rounds,
        "tangent_proposals": tangent_proposals,
        "restoration_attempts": restoration_attempts,
        "restoration_successes": restoration_successes,
        "restoration_steps": restoration_steps,
        "distinct_exact_digit2_points": exact_solutions,
        "starting_digit3_defect": 6,
        "best_digit3_defect": best_defect,
        "best_digit3_residuals_rows_1_through_19": tuple(
            map(int, best_cubic)
        ),
        "best_affine_coordinates": tuple(map(int, best)),
        "best_replay": {
            "placement_trits": best_replay["placement_trits"],
            "masks_a": best_replay["masks_a"],
            "masks_b": best_replay["masks_b"],
            "displayed_exact_values": best_replay[
                "displayed_exact_values"
            ],
            "nonzero_rows_by_digit": best_replay[
                "nonzero_rows_by_digit"
            ],
            "row_margin_aggregate": best_replay[
                "row_margin_aggregate"
            ],
            "row_margin_catalog_member": best_replay[
                "row_margin_catalog_member"
            ],
        },
    }
    result["semantic_sha256"] = compact_hash(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cpu-seconds", type=float, default=480)
    parser.add_argument("--seed", type=int, default=668_370)
    parser.add_argument("--restoration-samples", type=int, default=256)
    parser.add_argument("--proposals-per-round", type=int, default=8)
    args = parser.parse_args()
    print(
        json.dumps(
            search(
                args.cpu_seconds,
                args.seed,
                args.restoration_samples,
                args.proposals_per_round,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
