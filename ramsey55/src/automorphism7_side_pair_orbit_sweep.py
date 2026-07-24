#!/usr/bin/env python3
"""Proof-free in-memory sweep of the audited order-7 side-pair quotient."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import random
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

from pysat.solvers import Cadical195


ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / "verify"
if str(VERIFY) not in sys.path:
    sys.path.insert(0, str(VERIFY))

import automorphism7_side_orbit_cover as one_side  # noqa: E402
import automorphism7_side_gluing_pilot as pilot  # noqa: E402
from residual_completion_glucose import model_satisfies  # noqa: E402


EXPECTED_CNF_SHA256 = (
    "8045d463f68d78a745e18bb02ccc7d49fa02b47176a7282b1ef6f436fb109eb1"
)
EXPECTED_METADATA_SHA256 = (
    "04f18fdcf4d50bda27580e1653f99f423d9799ba1ddbf0e95b1683542e6b7a56"
)
EXPECTED_ONE_SIDE_CHECKER_SHA256 = (
    "b4531da9785fb98a668b3ea9876660f46500c47115f9aa582d19455081071543"
)
EXPECTED_PAIR_CHECKER_SHA256 = (
    "ebd5c3c02ac642e702d45d3f58b23aac97fbc93ad8792e0c877591b4809c3b37"
)
EXPECTED_CLASS_REPRESENTATIVE_SHA256 = (
    "bb60ab5feb5417ef3dfa46a0a9dd9886d612baf56c9ea985be7f89b955cd76ce"
)
EXPECTED_PAIR_SCHEDULE_SHA256 = (
    "cbcb78bd7c2b58669d2241eb109a0cfb9c5b61bb916a151d953ffdacf03cc1ae"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_lines(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("ascii")).hexdigest()


def build_pair_schedule() -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    list[int],
    list[tuple[int, int]],
]:
    edge_orbits, side_table = one_side.side_edge_orbits()
    side_clauses = one_side.side_formula(side_table)
    side_models = one_side.enumerate_models(side_clauses)
    h_actions = {
        one_side.edge_variable_permutation(
            edge_orbits,
            side_table,
            block_permutation,
            (0, shift_1, shift_2),
        )
        for block_permutation in itertools.permutations(range(3))
        for shift_1 in range(7)
        for shift_2 in range(7)
    }
    k_actions = tuple(
        one_side.edge_variable_permutation(
            edge_orbits, side_table, (0, 1, 2), (0, 0, 0), multiplier
        )
        for multiplier in range(1, 7)
    )
    side_class: dict[int, int] = {}
    class_representatives: list[int] = []
    for model in sorted(side_models):
        if model in side_class:
            continue
        orbit = {
            one_side.transform_bits(model, action) for action in h_actions
        }
        if not orbit <= side_models or orbit & side_class.keys():
            raise AssertionError("side H-orbit coverage failed")
        class_index = len(class_representatives)
        for image in orbit:
            side_class[image] = class_index
        class_representatives.append(min(orbit))
    class_multiplier_actions = [
        tuple(
            side_class[one_side.transform_bits(model, action)]
            for model in class_representatives
        )
        for action in k_actions
    ]
    pair_schedule: list[tuple[int, int]] = []
    covered: set[tuple[int, int]] = set()
    for left_class in range(664):
        for right_class in range(left_class, 664):
            pair = (left_class, right_class)
            if pair in covered:
                continue
            orbit = {
                tuple(sorted((action[left_class], action[right_class])))
                for action in class_multiplier_actions
            }
            if pair != min(orbit):
                raise AssertionError("pair traversal is not canonical")
            pair_schedule.append(pair)
            covered.update(orbit)
    class_lines = [format(model, "030b") for model in class_representatives]
    pair_lines = [f"{left},{right}" for left, right in pair_schedule]
    if (
        len(side_models) != 191394
        or len(h_actions) != 294
        or len(class_representatives) != 664
        or len(covered) != 220780
        or len(pair_schedule) != 37194
        or sha256_lines(class_lines) != EXPECTED_CLASS_REPRESENTATIVE_SHA256
        or sha256_lines(pair_lines) != EXPECTED_PAIR_SCHEDULE_SHA256
    ):
        raise AssertionError("audited pair schedule pin mismatch")
    return edge_orbits, class_representatives, pair_schedule


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--shard-index", type=int, required=True)
    parser.add_argument("--shard-count", type=int, required=True)
    parser.add_argument("--conflict-budget", type=int, default=200000)
    parser.add_argument("--seed", type=int, default=20261211)
    args = parser.parse_args()
    if (
        args.shard_count < 1
        or not 0 <= args.shard_index < args.shard_count
        or args.conflict_budget < 1
    ):
        raise SystemExit("invalid shard or budget")
    pinned = {
        args.cnf: EXPECTED_CNF_SHA256,
        args.metadata: EXPECTED_METADATA_SHA256,
        Path(one_side.__file__): EXPECTED_ONE_SIDE_CHECKER_SHA256,
        VERIFY / "automorphism7_side_pair_orbit_cover.py": (
            EXPECTED_PAIR_CHECKER_SHA256
        ),
    }
    for path, expected in pinned.items():
        if sha256_file(path) != expected:
            raise SystemExit(f"pin mismatch: {path}")

    setup_started = time.monotonic()
    edge_orbits, class_representatives, pair_schedule = build_pair_schedule()
    shard_schedule = [
        (global_index, pair)
        for global_index, pair in enumerate(pair_schedule)
        if global_index % args.shard_count == args.shard_index
    ]
    variable_count, clauses = one_side.parse_dimacs(args.cnf)
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    if variable_count != 129 or not isinstance(metadata, dict):
        raise ValueError("unexpected global formula")
    edge_table = one_side.global_edge_table(metadata)
    map_a = [edge_table[orbit[0]] for orbit in edge_orbits]
    map_b = [
        edge_table[(orbit[0][0] + 21, orbit[0][1] + 21)]
        for orbit in edge_orbits
    ]
    fixed_orbits = sorted(
        {
            variable
            for (left, right), variable in edge_table.items()
            if right == 42
        },
        key=lambda variable: min(
            left
            for (left, right), observed in edge_table.items()
            if right == 42 and observed == variable
        ),
    )
    fixed_units = fixed_orbits[:3] + [
        -variable for variable in fixed_orbits[3:]
    ]
    assigned = set(fixed_orbits + map_a + map_b)
    cross_variables = sorted(set(range(1, 130)) - assigned)
    if len(assigned) != 66 or len(cross_variables) != 63:
        raise AssertionError("unexpected 66/63 variable partition")

    print(
        json.dumps(
            {
                "event": "start",
                "evidence_label": "PROOF-FREE CONSTRUCTION SEARCH",
                "claim_boundary": (
                    "SAT is replayed and dual-verified. Negative solver "
                    "outcomes are observations only; no proof is emitted."
                ),
                "pair_schedule_count": len(pair_schedule),
                "pair_schedule_sha256": EXPECTED_PAIR_SCHEDULE_SHA256,
                "shard_index": args.shard_index,
                "shard_count": args.shard_count,
                "shard_pair_count": len(shard_schedule),
                "conflict_budget_per_pair": args.conflict_budget,
                "seed": args.seed,
                "setup_seconds": time.monotonic() - setup_started,
            },
            sort_keys=True,
        ),
        flush=True,
    )

    rng = random.Random(args.seed + 1000003 * args.shard_index)
    statuses: Counter[str] = Counter()
    total_conflicts = 0
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses, use_timer=True) as solver:
        for shard_position, (global_index, pair) in enumerate(
            shard_schedule, start=1
        ):
            left_class, right_class = pair
            left_model = class_representatives[left_class]
            right_model = class_representatives[right_class]
            units = list(fixed_units)
            units.extend(
                variable if left_model >> index & 1 else -variable
                for index, variable in enumerate(map_a)
            )
            units.extend(
                -variable if right_model >> index & 1 else variable
                for index, variable in enumerate(map_b)
            )
            if len(units) != 66 or len({abs(unit) for unit in units}) != 66:
                raise AssertionError("pair does not fix 66 variables")
            solver.set_phases(
                [
                    *units,
                    *(
                        variable if rng.getrandbits(1) else -variable
                        for variable in cross_variables
                    ),
                ]
            )
            before = solver.accum_stats().get("conflicts", 0)
            pair_started = time.monotonic()
            solver.conf_budget(args.conflict_budget)
            outcome = solver.solve_limited(assumptions=units)
            pair_seconds = time.monotonic() - pair_started
            conflicts = solver.accum_stats().get("conflicts", 0) - before
            total_conflicts += conflicts
            status = (
                "SAT"
                if outcome is True
                else "OBSERVED_UNSAT_UNCHECKED"
                if outcome is False
                else "BUDGET_EXHAUSTED"
            )
            statuses[status] += 1
            if outcome is True:
                raw_model = solver.get_model()
                truth = pilot.complete_model_truth(raw_model, variable_count)
                if not model_satisfies(raw_model, clauses):
                    raise AssertionError("SAT model failed direct CNF replay")
                adjacency = pilot.decode_global_graph(truth, edge_table)
                graph6 = pilot.encode_graph6(adjacency) + "\n"
                graph_sha256 = hashlib.sha256(
                    graph6.encode("ascii")
                ).hexdigest()
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".g6",
                    encoding="ascii",
                    delete=False,
                ) as stream:
                    stream.write(graph6)
                    temporary = Path(stream.name)
                try:
                    python_check = subprocess.run(
                        [
                            sys.executable,
                            str(VERIFY / "exhaustive_verify.py"),
                            str(temporary),
                        ],
                        capture_output=True,
                        text=True,
                        timeout=120,
                        check=False,
                    )
                    cpp_check = subprocess.run(
                        [str(ROOT / "build" / "bitset_verify"), str(temporary)],
                        capture_output=True,
                        text=True,
                        timeout=120,
                        check=False,
                    )
                finally:
                    os.unlink(temporary)
                print(
                    json.dumps(
                        {
                            "event": "SAT",
                            "global_pair_index": global_index,
                            "pair": pair,
                            "graph6": graph6.strip(),
                            "graph6_sha256": graph_sha256,
                            "cnf_replay": True,
                            "python_returncode": python_check.returncode,
                            "python_stdout": python_check.stdout.strip(),
                            "cpp_returncode": cpp_check.returncode,
                            "cpp_stdout": cpp_check.stdout.strip(),
                            "pair_seconds": pair_seconds,
                            "conflicts": conflicts,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
                return 10
            if shard_position % 128 == 0 or shard_position == len(shard_schedule):
                print(
                    json.dumps(
                        {
                            "event": "progress",
                            "shard_index": args.shard_index,
                            "shard_position": shard_position,
                            "shard_pair_count": len(shard_schedule),
                            "last_global_pair_index": global_index,
                            "last_pair": pair,
                            "last_status": status,
                            "last_conflicts": conflicts,
                            "last_pair_seconds": pair_seconds,
                            "status_counts": dict(sorted(statuses.items())),
                            "total_conflicts": total_conflicts,
                            "elapsed_seconds": time.monotonic() - started,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
    print(
        json.dumps(
            {
                "event": "complete",
                "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
                "claim_boundary": (
                    "No proof artifacts were produced. All negative outcomes "
                    "remain uncertified solver observations."
                ),
                "shard_index": args.shard_index,
                "shard_count": args.shard_count,
                "shard_pair_count": len(shard_schedule),
                "status_counts": dict(sorted(statuses.items())),
                "total_conflicts": total_conflicts,
                "runtime_seconds": time.monotonic() - started,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
