#!/usr/bin/env python3
"""Run, validate, and freeze the exact PARI pair-norm slice audit.

The GP program enumerates 3^9 physical placements in each of fifteen
channel alphabets: canonical A/B and A-star A for each of the five
shell-two representatives.  This wrapper treats only completed exact
records as mathematics, validates the expected scope, and stores a
runtime-independent semantic certificate.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import resource
import subprocess
import time


HERE = Path(__file__).resolve().parent
GP_SCRIPT = HERE / "audit_pair_norm_slices.gp"
GP_BINARY = Path("/opt/homebrew/bin/gp")

P = 167
FACTORS = (2, 83, 28057)
SLICE_ASSIGNMENTS = 3**9
SLICE_PAIR_ASSIGNMENTS = SLICE_ASSIGNMENTS**2
PROFILE_LABELS = (
    "h2-222222-0",
    "h2-422220-0",
    "h2-422220-1",
    "h2-422220-2",
    "h2-422220-3",
)
CHANNEL_KINDS = ("A", "B", "Astar-A")
PAIR_KINDS = ("canonical-A-vs-B", "Astar-A-vs-B")


def compact_hash(value: object) -> str:
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()


def file_hash(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=HERE / "pair_norm_nine_trit_slice_certificate.json",
    )
    return parser.parse_args()


def validate_channel(record: list[object]) -> None:
    if len(record) != 7:
        raise AssertionError("a channel record has the wrong length")
    label, kind, selected, assignments, support2, support83, support28057 = record
    if label not in PROFILE_LABELS or kind not in CHANNEL_KINDS:
        raise AssertionError("an unknown channel record was emitted")
    if (
        not isinstance(selected, list)
        or len(selected) != 3
        or len(set(map(int, selected))) != 3
        or not all(0 <= int(value) < 12 for value in selected)
    ):
        raise AssertionError("a channel slice has invalid selected classes")
    if int(assignments) != SLICE_ASSIGNMENTS:
        raise AssertionError("a channel slice has the wrong assignment count")
    for support in (support2, support83, support28057):
        if (
            not isinstance(support, list)
            or len(support) != 2
            or not isinstance(support[0], list)
            or len(support[0]) != 3
        ):
            raise AssertionError("a character support summary is malformed")
    if support2 != [[2, 2, 2], 8]:
        raise AssertionError("an order-two triple image is not complete")
    if support83[0] != [83, 83, 83]:
        raise AssertionError("an order-83 marginal image is not complete")
    if not all(int(value) > 13_000 for value in support28057[0]):
        raise AssertionError("an order-28057 marginal slice unexpectedly collapsed")
    if not 0 < int(support28057[1]) <= SLICE_ASSIGNMENTS:
        raise AssertionError("an order-28057 joint support has invalid size")


def validate_pair(record: list[object]) -> None:
    if len(record) != 6:
        raise AssertionError("a pair record has the wrong length")
    label, kind, assignments, match2, match83, match28057 = record
    if label not in PROFILE_LABELS or kind not in PAIR_KINDS:
        raise AssertionError("an unknown pair record was emitted")
    if int(assignments) != SLICE_PAIR_ASSIGNMENTS:
        raise AssertionError("a pair slice has the wrong Cartesian size")
    for match in (match2, match83, match28057):
        if (
            not isinstance(match, list)
            or len(match) != 2
            or not isinstance(match[0], list)
            or len(match[0]) != 3
        ):
            raise AssertionError("a character match summary is malformed")
        if not all(0 < int(value) < SLICE_PAIR_ASSIGNMENTS for value in match[0]):
            raise AssertionError("a scalar pair-character gate became tautological or empty")
    if not 0 < int(match2[1]) < SLICE_PAIR_ASSIGNMENTS:
        raise AssertionError("the joint order-two gate became tautological or empty")
    if not 0 < int(match83[1]) < SLICE_PAIR_ASSIGNMENTS:
        raise AssertionError("the joint order-83 gate became tautological or empty")
    if int(match28057[1]) != 0:
        raise AssertionError("the pinned order-28057 nine-trit slices gained a joint hit")


def main() -> None:
    args = parse_args()
    if not GP_BINARY.exists():
        raise SystemExit(f"PARI/GP not found at {GP_BINARY}")

    started = time.monotonic()
    completed = subprocess.run(
        (str(GP_BINARY), "-q", str(GP_SCRIPT)),
        check=True,
        capture_output=True,
        text=True,
    )
    elapsed = time.monotonic() - started

    channels: list[list[object]] = []
    pairs: list[list[object]] = []
    gp_elapsed_milliseconds: int | None = None
    for line in completed.stdout.splitlines():
        if line.startswith("CHANNEL|"):
            record = json.loads(line.removeprefix("CHANNEL|"))
            validate_channel(record)
            channels.append(record)
        elif line.startswith("PAIR|"):
            record = json.loads(line.removeprefix("PAIR|"))
            validate_pair(record)
            pairs.append(record)
        elif line.startswith("SUMMARY|"):
            summary = json.loads(line.removeprefix("SUMMARY|"))
            if summary[0] != "elapsed_milliseconds":
                raise AssertionError("the GP summary changed")
            gp_elapsed_milliseconds = int(summary[1])

    expected_channels = {
        (label, kind) for label in PROFILE_LABELS for kind in CHANNEL_KINDS
    }
    expected_pairs = {
        (label, kind) for label in PROFILE_LABELS for kind in PAIR_KINDS
    }
    if {(str(row[0]), str(row[1])) for row in channels} != expected_channels:
        raise AssertionError("the GP output did not contain all fifteen channels")
    if {(str(row[0]), str(row[1])) for row in pairs} != expected_pairs:
        raise AssertionError("the GP output did not contain all ten profile pairs")
    if gp_elapsed_milliseconds is None:
        raise AssertionError("the GP run did not finish with a summary")

    field_order = P**3 - 1
    if field_order != 2 * 83 * 28057:
        raise AssertionError("the F_(167^3) character factorization changed")
    norm_exponent = (P**12 - 1) // (P**3 - 1)
    if norm_exponent != 1 + P**3 + P**6 + P**9:
        raise AssertionError("the E/F_(167^3) norm exponent changed")

    semantic = {
        "schema": "lp333-shell-two-pair-resultant-nine-trit-slices-v1",
        "prime": P,
        "pair_invariants": [
            "nu_X,r=Norm_F_(167^12)/F_(167^3)(w_X,r*w_X,r+3)"
            for _ in range(3)
        ],
        "pair_indices": [0, 1, 2],
        "necessary_equalities": [
            "nu_A,0=nu_B,0",
            "nu_A,1=nu_B,1",
            "nu_A,2=nu_B,2",
        ],
        "norm_exponent": norm_exponent,
        "base_field_unit_order": field_order,
        "coprime_character_factors": list(FACTORS),
        "slice": {
            "active_trits": 9,
            "varied_complete_classes": 3,
            "assignments_per_channel": SLICE_ASSIGNMENTS,
            "ordered_pairs_per_profile_seed": SLICE_PAIR_ASSIGNMENTS,
            "fixed_local_option": 0,
            "scope": (
                "exact finite physical subfamilies only; a zero joint slice "
                "count is not a profile exclusion"
            ),
        },
        "channels": channels,
        "profile_pairs": pairs,
        "gp_script_sha256": file_hash(GP_SCRIPT),
    }
    result = {
        "semantic": semantic,
        "semantic_sha256": compact_hash(semantic),
        "runtime": {
            "wrapper_elapsed_seconds": round(elapsed, 3),
            "gp_elapsed_milliseconds": gp_elapsed_milliseconds,
            "child_peak_rss_bytes": resource.getrusage(
                resource.RUSAGE_CHILDREN
            ).ru_maxrss,
        },
    }
    args.output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(
        json.dumps(
            {
                "channels": len(channels),
                "profile_pairs": len(pairs),
                "order2_joint_images_full": all(
                    row[4][1] == 8 for row in channels
                ),
                "order83_marginal_images_full": all(
                    row[5][0] == [83, 83, 83] for row in channels
                ),
                "order28057_scalar_gates_all_survive": all(
                    all(int(value) > 0 for value in row[5][0])
                    for row in pairs
                ),
                "order28057_joint_slice_hits": sum(
                    int(row[5][1]) for row in pairs
                ),
                "semantic_sha256": result["semantic_sha256"],
                **result["runtime"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
