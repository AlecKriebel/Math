#!/usr/bin/env python3
"""Low-storage search for the order-5, cycle-type 5^8 1^3 Ramsey branch.

The search normalizes the graph induced by the three fixed vertices up to
global complementation, then quotients the three four-subsets of moved cycles
seen by the fixed vertices under the remaining exact relabeling symmetries.
Negative solver outcomes are observations only: this program emits no proof
certificate.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import itertools
import json
import math
import random
import resource
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Iterable

from graph_io import encode_graph6


SEARCH_ID = "ramsey55_order5_fixed_split_search_v1"
ORDER = 43
PRIME = 5
CYCLE_COUNT = 8
FIXED_VERTICES = (40, 41, 42)
EXPECTED_VARIABLES = 183
EXPECTED_SIGNATURES = 192_054
EXPECTED_CLAUSES = 384_108
EXPECTED_DIMACS_SHA256 = (
    "8abb891e769995940c06f403bb261b8d4e4c7c5d03749b7a13ca445182c4b7c6"
)


def permutation() -> tuple[int, ...]:
    """Return the canonical permutation (0 1 2 3 4)...(35 36 37 38 39)."""
    image = list(range(ORDER))
    for block in range(CYCLE_COUNT):
        base = PRIME * block
        for offset in range(PRIME):
            image[base + offset] = base + (offset + 1) % PRIME
    return tuple(image)


def edge_orbits() -> tuple[
    dict[tuple[int, int], int], tuple[tuple[tuple[int, int], ...], ...]
]:
    """Independently construct the edge-orbit partition."""
    image = permutation()
    remaining = set(itertools.combinations(range(ORDER), 2))
    parts: list[tuple[tuple[int, int], ...]] = []
    while remaining:
        initial = min(remaining)
        current = initial
        part: set[tuple[int, int]] = set()
        for _ in range(PRIME):
            part.add(current)
            current = tuple(sorted((image[current[0]], image[current[1]])))
        canonical = tuple(sorted(part))
        remaining.difference_update(canonical)
        parts.append(canonical)
    parts.sort(key=lambda part: part[0])
    edge_variable = {
        edge: variable
        for variable, part in enumerate(parts, start=1)
        for edge in part
    }
    if len(edge_variable) != math.comb(ORDER, 2):
        raise AssertionError("edge orbits do not partition K_43")
    return edge_variable, tuple(parts)


def ramsey_signatures(
    edge_variable: dict[tuple[int, int], int],
) -> tuple[tuple[int, ...], ...]:
    """Deduplicate the exact edge-orbit signatures of all five-sets."""
    signatures = {
        tuple(
            sorted(
                {
                    edge_variable[edge]
                    for edge in itertools.combinations(vertices, 2)
                }
            )
        )
        for vertices in itertools.combinations(range(ORDER), 5)
    }
    return tuple(sorted(signatures))


def clauses_from_signatures(
    signatures: Iterable[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for signature in signatures:
        clauses.append(signature)
        clauses.append(tuple(-variable for variable in signature))
    return clauses


def dimacs_sha256(
    variable_count: int, signatures: Iterable[tuple[int, ...]]
) -> str:
    """Hash the DIMACS that the generic writer would produce, without writing it."""
    signatures = tuple(signatures)
    state = hashlib.sha256()
    state.update(f"p cnf {variable_count} {2 * len(signatures)}\n".encode("ascii"))
    for signature in signatures:
        state.update((" ".join(map(str, signature)) + " 0\n").encode("ascii"))
        state.update(
            (
                " ".join(str(-variable) for variable in signature) + " 0\n"
            ).encode("ascii")
        )
    return state.hexdigest()


def membership_counts(subsets: tuple[frozenset[int], ...]) -> tuple[int, ...]:
    counts = [0] * (1 << len(subsets))
    for cycle in range(CYCLE_COUNT):
        mask = sum(
            (cycle in subset) << coordinate
            for coordinate, subset in enumerate(subsets)
        )
        counts[mask] += 1
    return tuple(counts)


def permute_count_coordinates(
    counts: tuple[int, ...], coordinate_order: tuple[int, int, int]
) -> tuple[int, ...]:
    transformed = [0] * 8
    for old_mask, count in enumerate(counts):
        new_mask = sum(
            ((old_mask >> coordinate_order[new_coordinate]) & 1)
            << new_coordinate
            for new_coordinate in range(3)
        )
        transformed[new_mask] = count
    return tuple(transformed)


def canonical_counts(
    counts: tuple[int, ...], fixed_vertex_group: tuple[tuple[int, int, int], ...]
) -> tuple[int, ...]:
    return min(
        permute_count_coordinates(counts, coordinate_order)
        for coordinate_order in fixed_vertex_group
    )


def fixed_split_types(
    fixed_pattern: str,
) -> tuple[tuple[int, ...], ...]:
    """Return exact S8/fixed-vertex orbit representatives.

    ``edgeless`` has the full S3 action on fixed vertices. ``one_edge`` has
    only the swap of the two endpoints of the normalized unique edge.
    """
    if fixed_pattern == "edgeless":
        group = tuple(itertools.permutations(range(3)))
    elif fixed_pattern == "one_edge":
        group = ((0, 1, 2), (1, 0, 2))
    else:
        raise ValueError(f"unknown fixed pattern: {fixed_pattern}")
    first = frozenset(range(4))
    four_subsets = tuple(
        frozenset(subset) for subset in itertools.combinations(range(8), 4)
    )
    representatives = {
        canonical_counts(membership_counts((first, second, third)), group)
        for second in four_subsets
        for third in four_subsets
    }
    return tuple(sorted(representatives))


def subsets_from_counts(
    counts: tuple[int, ...],
) -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
    """Realize a count vector, choosing cycles 0..3 in the first subset."""
    if len(counts) != 8 or sum(counts) != CYCLE_COUNT:
        raise ValueError("invalid membership count vector")
    masks = [
        mask
        for wanted_first_bit in (1, 0)
        for mask, count in enumerate(counts)
        if bool(mask & 1) == bool(wanted_first_bit)
        for _ in range(count)
    ]
    subsets = tuple(
        frozenset(
            cycle for cycle, mask in enumerate(masks) if (mask >> coordinate) & 1
        )
        for coordinate in range(3)
    )
    if tuple(map(len, subsets)) != (4, 4, 4):
        raise AssertionError("membership vector does not have 4/4/4 marginals")
    if subsets[0] != frozenset(range(4)):
        raise AssertionError("first fixed vertex was not normalized")
    if membership_counts(subsets) != counts:
        raise AssertionError("membership count realization failed")
    return subsets  # type: ignore[return-value]


def assumptions_for_split(
    fixed_pattern: str,
    counts: tuple[int, ...],
    edge_variable: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    subsets = subsets_from_counts(counts)
    fixed_edges = {
        (40, 41): fixed_pattern == "one_edge",
        (40, 42): False,
        (41, 42): False,
    }
    assignments: dict[int, bool] = {}
    for edge, value in fixed_edges.items():
        assignments[edge_variable[edge]] = value
    for fixed_index, fixed_vertex in enumerate(FIXED_VERTICES):
        for cycle in range(CYCLE_COUNT):
            variable = edge_variable[(PRIME * cycle, fixed_vertex)]
            assignments[variable] = cycle in subsets[fixed_index]
    if len(assignments) != 27:
        raise AssertionError("fixed split must assign 27 distinct edge orbits")
    return tuple(
        variable if value else -variable
        for variable, value in sorted(assignments.items())
    )


def internal_orientation_types(
    counts: tuple[int, ...],
) -> tuple[tuple[bool, ...], ...]:
    """Quotient internal C5 orientations by exact residual symmetries.

    For the all-ones membership type, every fixed-adjacency mask labels one
    cycle uniquely. The residual actions used here are exchange of the two
    endpoints of the unique fixed edge and the global multiplier x -> 2x,
    which exchanges the two undirected nonzero-distance classes in every
    moved 5-cycle.
    """
    if counts != (1,) * 8:
        raise ValueError("internal refinement is defined for the all-ones type")
    subsets = subsets_from_counts(counts)
    masks = [
        sum(
            (cycle in subset) << coordinate
            for coordinate, subset in enumerate(subsets)
        )
        for cycle in range(CYCLE_COUNT)
    ]
    cycle_of_mask = {mask: cycle for cycle, mask in enumerate(masks)}
    if len(cycle_of_mask) != 8:
        raise AssertionError("all-ones type did not label cycles uniquely")

    def endpoint_swap(bits: tuple[bool, ...]) -> tuple[bool, ...]:
        transformed = [False] * CYCLE_COUNT
        for old_cycle, old_mask in enumerate(masks):
            new_mask = (
                (old_mask & ~3)
                | ((old_mask & 1) << 1)
                | ((old_mask & 2) >> 1)
            )
            transformed[cycle_of_mask[new_mask]] = bits[old_cycle]
        return tuple(transformed)

    representatives: set[tuple[bool, ...]] = set()
    for bits in itertools.product((False, True), repeat=CYCLE_COUNT):
        swapped = endpoint_swap(bits)
        orbit = (
            bits,
            swapped,
            tuple(not value for value in bits),
            tuple(not value for value in swapped),
        )
        representatives.add(min(orbit))
    return tuple(sorted(representatives))


def internal_orientation_assumptions(
    orientation: tuple[bool, ...],
    edge_variable: dict[tuple[int, int], int],
) -> tuple[int, ...]:
    if len(orientation) != CYCLE_COUNT:
        raise ValueError("internal orientation must have eight bits")
    literals: list[int] = []
    for cycle, second_distance in enumerate(orientation):
        base = PRIME * cycle
        distance_one = edge_variable[(base, base + 1)]
        distance_two = edge_variable[(base, base + 2)]
        literals.extend(
            (
                -distance_one if second_distance else distance_one,
                distance_two if second_distance else -distance_two,
            )
        )
    if len(set(map(abs, literals))) != 16:
        raise AssertionError("internal orientation does not assign 16 variables")
    return tuple(literals)


def decode_model(
    model: list[int], edge_variable: dict[tuple[int, int], int]
) -> list[int]:
    truth = {abs(literal): literal > 0 for literal in model}
    if any(variable not in truth for variable in range(1, EXPECTED_VARIABLES + 1)):
        raise AssertionError("SAT model is incomplete")
    adjacency = [0] * ORDER
    for (left, right), variable in edge_variable.items():
        if truth[variable]:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return adjacency


def forbidden_counts(adjacency: list[int]) -> tuple[int, int]:
    clique_count = 0
    independent_count = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        edge_count = sum(
            (adjacency[left] >> right) & 1
            for left, right in itertools.combinations(vertices, 2)
        )
        clique_count += edge_count == 10
        independent_count += edge_count == 0
    return clique_count, independent_count


def automorphism_valid(adjacency: list[int]) -> bool:
    image = permutation()
    for left, right in itertools.combinations(range(ORDER), 2):
        transformed = tuple(sorted((image[left], image[right])))
        if ((adjacency[left] >> right) & 1) != (
            (adjacency[transformed[0]] >> transformed[1]) & 1
        ):
            return False
    return True


def run_search(
    conflict_budget: int,
    seed: int,
    fixed_pattern_choice: str,
    maximum_types: int | None,
    membership_counts_filter: tuple[int, ...] | None,
    solver_name: str,
    split_internal_orientations: bool,
) -> dict[str, object]:
    try:
        import pysat
        from pysat import solvers as pysat_solvers
    except ImportError as error:
        raise RuntimeError(
            "python-sat is required for search; set the pinned PYTHONPATH"
        ) from error

    started = time.monotonic()
    edge_variable, orbits = edge_orbits()
    signatures = ramsey_signatures(edge_variable)
    orbit_histogram = Counter(map(len, orbits))
    signature_histogram = Counter(map(len, signatures))
    formula_hash = dimacs_sha256(len(orbits), signatures)
    if (
        len(orbits) != EXPECTED_VARIABLES
        or len(signatures) != EXPECTED_SIGNATURES
        or 2 * len(signatures) != EXPECTED_CLAUSES
        or formula_hash != EXPECTED_DIMACS_SHA256
        or orbit_histogram != Counter({5: 180, 1: 3})
    ):
        raise AssertionError("order-5 formula fingerprint mismatch")
    clauses = clauses_from_signatures(signatures)
    del signatures

    patterns = (
        ("edgeless", "one_edge")
        if fixed_pattern_choice == "all"
        else (fixed_pattern_choice,)
    )
    base_schedule = [
        (fixed_pattern, counts)
        for fixed_pattern in patterns
        for counts in fixed_split_types(fixed_pattern)
    ]
    if membership_counts_filter is not None:
        base_schedule = [
            item for item in base_schedule if item[1] == membership_counts_filter
        ]
        if not base_schedule:
            raise ValueError(
                "membership-count filter is not a canonical type in the "
                "selected fixed pattern"
            )
    schedule: list[
        tuple[str, tuple[int, ...], tuple[bool, ...] | None]
    ] = []
    for fixed_pattern, counts in base_schedule:
        orientations: tuple[tuple[bool, ...] | None, ...]
        if split_internal_orientations:
            orientations = internal_orientation_types(counts)
        else:
            orientations = (None,)
        schedule.extend(
            (fixed_pattern, counts, orientation)
            for orientation in orientations
        )
    rng = random.Random(seed)
    rng.shuffle(schedule)
    if maximum_types is not None:
        schedule = schedule[:maximum_types]

    records: list[dict[str, object]] = []
    construction: dict[str, object] | None = None
    solver_class = getattr(pysat_solvers, solver_name)
    with solver_class(bootstrap_with=clauses, use_timer=True) as solver:
        del clauses
        gc.collect()
        for split_index, (fixed_pattern, counts, orientation) in enumerate(schedule):
            assumptions = list(
                assumptions_for_split(fixed_pattern, counts, edge_variable)
            )
            if orientation is not None:
                assumptions.extend(
                    internal_orientation_assumptions(
                        orientation, edge_variable
                    )
                )
            if len(assumptions) != len(set(map(abs, assumptions))):
                raise AssertionError("split assumptions overlap")
            phase_literals = [
                variable if rng.getrandbits(1) else -variable
                for variable in range(1, EXPECTED_VARIABLES + 1)
            ]
            rng.shuffle(phase_literals)
            solver.set_phases(phase_literals)
            before = solver.accum_stats()
            split_started = time.monotonic()
            solver.conf_budget(conflict_budget)
            outcome = solver.solve_limited(assumptions=assumptions)
            after = solver.accum_stats()
            record = {
                "split_index": split_index,
                "fixed_pattern": fixed_pattern,
                "membership_counts": list(counts),
                "internal_orientation": (
                    [int(value) for value in orientation]
                    if orientation is not None
                    else None
                ),
                "status": (
                    "SAT"
                    if outcome is True
                    else "OBSERVED_UNSAT_UNCHECKED"
                    if outcome is False
                    else "BUDGET_EXHAUSTED"
                ),
                "negative_certified": False,
                "wall_seconds": time.monotonic() - split_started,
                "conflicts": after.get("conflicts", 0)
                - before.get("conflicts", 0),
                "decisions": after.get("decisions", 0)
                - before.get("decisions", 0),
                "propagations": after.get("propagations", 0)
                - before.get("propagations", 0),
            }
            records.append(record)
            print(
                json.dumps(
                    {
                        "event": "split_complete",
                        **record,
                        "completed": len(records),
                        "scheduled": len(schedule),
                    },
                    sort_keys=True,
                ),
                flush=True,
            )
            if outcome is True:
                model = solver.get_model()
                if model is None:
                    raise AssertionError("SAT outcome has no model")
                truth = {abs(literal): literal > 0 for literal in model}
                if any(
                    truth[abs(literal)] != (literal > 0)
                    for literal in assumptions
                ):
                    raise AssertionError("SAT model violates split assumptions")
                adjacency = decode_model(model, edge_variable)
                counts_found = forbidden_counts(adjacency)
                if counts_found != (0, 0) or not automorphism_valid(adjacency):
                    raise AssertionError("SAT model failed independent graph replay")
                graph6 = encode_graph6(adjacency)
                construction = {
                    "split_index": split_index,
                    "fixed_pattern": fixed_pattern,
                    "membership_counts": list(counts),
                    "internal_orientation": (
                        [int(value) for value in orientation]
                        if orientation is not None
                        else None
                    ),
                    "graph6": graph6,
                    "graph6_line_sha256": hashlib.sha256(
                        (graph6 + "\n").encode("ascii")
                    ).hexdigest(),
                    "true_variables": sorted(
                        variable
                        for variable in range(1, EXPECTED_VARIABLES + 1)
                        if truth[variable]
                    ),
                    "forbidden_counts": {
                        "clique_5": counts_found[0],
                        "independent_5": counts_found[1],
                    },
                    "automorphism_replay": True,
                }
                break

    status_counts = Counter(str(record["status"]) for record in records)
    return {
        "search": SEARCH_ID,
        "evidence_label": (
            "CERTIFIED_CONSTRUCTION"
            if construction is not None
            else "REPRODUCIBLE_COMPUTATIONAL_OBSERVATION"
        ),
        "claim_boundary": (
            "A returned SAT model is independently replayed over all 962,598 "
            "five-sets. Negative outcomes have no proof certificates and do not "
            "certify nonexistence, even when every normalized split was visited."
        ),
        "cycle_type": "5^8 1^3",
        "formula": {
            "variable_count": len(orbits),
            "edge_orbit_size_histogram": dict(sorted(orbit_histogram.items())),
            "unique_signature_count": EXPECTED_SIGNATURES,
            "signature_size_histogram": dict(
                sorted(signature_histogram.items())
            ),
            "clause_count": EXPECTED_CLAUSES,
            "dimacs_sha256_without_materialization": formula_hash,
        },
        "normalization": {
            "degree_bound": [18, 24],
            "moved_cycle_neighbors_per_fixed_vertex": 4,
            "edgeless_type_count": len(fixed_split_types("edgeless")),
            "one_edge_type_count": len(fixed_split_types("one_edge")),
            "complete_type_count": 59,
            "fixed_pattern_choice": fixed_pattern_choice,
            "internal_orientation_refinement": split_internal_orientations,
            "all_ones_internal_orientation_type_count": len(
                internal_orientation_types((1,) * 8)
            ),
        },
        "solver": {
            "name": solver_name,
            "pysat_version": pysat.__version__,
            "conflict_budget_per_split": conflict_budget,
            "seed": seed,
        },
        "scheduled_type_count": len(schedule),
        "visited_type_count": len(records),
        "status_counts": dict(sorted(status_counts.items())),
        "construction": construction,
        "records": records,
        "runtime_seconds": time.monotonic() - started,
        "maximum_resident_set_bytes": resource.getrusage(
            resource.RUSAGE_SELF
        ).ru_maxrss,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--conflict-budget", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=20_261_301)
    parser.add_argument(
        "--fixed-pattern",
        choices=("all", "edgeless", "one_edge"),
        default="all",
    )
    parser.add_argument("--maximum-types", type=int)
    parser.add_argument(
        "--membership-counts",
        help="optional comma-separated canonical n_000,...,n_111 vector",
    )
    parser.add_argument(
        "--solver",
        choices=("Cadical195", "Glucose4", "MapleChrono"),
        default="Cadical195",
    )
    parser.add_argument(
        "--split-internal-orientations",
        action="store_true",
        help=(
            "refine the all-ones membership type by its 80 exact residual "
            "internal-C5 orientation orbits"
        ),
    )
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    if args.conflict_budget <= 0:
        parser.error("--conflict-budget must be positive")
    if args.maximum_types is not None and args.maximum_types <= 0:
        parser.error("--maximum-types must be positive")
    membership_counts_filter = None
    if args.membership_counts is not None:
        try:
            membership_counts_filter = tuple(
                int(field) for field in args.membership_counts.split(",")
            )
        except ValueError:
            parser.error("--membership-counts must contain integers")
        if len(membership_counts_filter) != 8:
            parser.error("--membership-counts must have exactly eight entries")
    result = run_search(
        args.conflict_budget,
        args.seed,
        args.fixed_pattern,
        args.maximum_types,
        membership_counts_filter,
        args.solver,
        args.split_internal_orientations,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.result is not None:
        args.result.parent.mkdir(parents=True, exist_ok=True)
        args.result.write_text(payload, encoding="utf-8")
    print(json.dumps({"event": "final", **result}, sort_keys=True), flush=True)
    return 10 if result["construction"] is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
