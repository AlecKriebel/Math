#!/usr/bin/env python3
"""Independently reconstruct and replay one selector-lifted C7 shard."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
for directory in (ROOT / "src", ROOT / "verify"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

import automorphism7_pair_lifted_blocker_sample_check as sample_check  # noqa: E402
import automorphism7_side_orbit_cover as one_side  # noqa: E402


CHECKER_ID = "ramsey55_automorphism7_pair_lifted_shard_checker_v1"
BASE_VARIABLE_COUNT = 129
EXPECTED_SCHEDULE_SHA256 = (
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


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or Path(str(record.get("path", ""))).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch: {label}")


def certified_models(path: Path) -> set[int]:
    models = {
        int(line, 2)
        for line in path.read_text(encoding="ascii").splitlines()
    }
    if len(models) != 191394:
        raise ValueError("bad certified side-model list")
    return models


def schedule_from_certified_models(
    models: set[int],
) -> tuple[
    tuple[tuple[tuple[int, int], ...], ...],
    list[int],
    list[tuple[int, int]],
]:
    edge_orbits, side_table = one_side.side_edge_orbits()
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
    multiplier_actions = tuple(
        one_side.edge_variable_permutation(
            edge_orbits,
            side_table,
            (0, 1, 2),
            (0, 0, 0),
            multiplier,
        )
        for multiplier in range(1, 7)
    )
    side_class: dict[int, int] = {}
    representatives: list[int] = []
    for model in sorted(models):
        if model in side_class:
            continue
        orbit = {
            one_side.transform_bits(model, action) for action in h_actions
        }
        if not orbit <= models or orbit & side_class.keys():
            raise AssertionError("certified H orbit cover failed")
        index = len(representatives)
        for image in orbit:
            side_class[image] = index
        representatives.append(min(orbit))
    class_actions = [
        tuple(
            side_class[one_side.transform_bits(model, action)]
            for model in representatives
        )
        for action in multiplier_actions
    ]
    schedule: list[tuple[int, int]] = []
    covered: set[tuple[int, int]] = set()
    for left in range(len(representatives)):
        for right in range(left, len(representatives)):
            pair = (left, right)
            if pair in covered:
                continue
            orbit = {
                tuple(sorted((action[left], action[right])))
                for action in class_actions
            }
            if pair != min(orbit):
                raise AssertionError("noncanonical pair traversal")
            schedule.append(pair)
            covered.update(orbit)
    lines = [f"{left},{right}" for left, right in schedule]
    if (
        len(representatives) != 664
        or len(covered) != 220780
        or len(schedule) != 37194
        or sha256_lines(lines) != EXPECTED_SCHEDULE_SHA256
    ):
        raise AssertionError("certified pair schedule mismatch")
    return edge_orbits, representatives, schedule


def side_cube(
    left_model: int,
    right_model: int,
    map_a: list[int],
    map_b: list[int],
) -> tuple[int, ...]:
    units = [
        variable if left_model >> index & 1 else -variable
        for index, variable in enumerate(map_a)
    ]
    units.extend(
        -variable if right_model >> index & 1 else variable
        for index, variable in enumerate(map_b)
    )
    return tuple(units)


def wrapper_bytes(
    base_clauses: tuple[tuple[int, ...], ...],
    fixed_units: list[int],
    cubes: list[dict[str, Any]],
) -> bytes:
    clauses = list(base_clauses)
    clauses.extend((unit,) for unit in fixed_units)
    selectors: list[int] = []
    for record in cubes:
        selector = int(record["selector"])
        cube = tuple(int(literal) for literal in record["side_units"])
        blocker = tuple(-literal for literal in cube)
        selectors.append(selector)
        clauses.extend((-selector, literal) for literal in cube)
        clauses.append((selector, *blocker))
    clauses.append(tuple(selectors))
    return sample_check.dimacs_bytes(
        BASE_VARIABLE_COUNT + 37194, tuple(clauses)
    )


def verified(output: str) -> bool:
    return "VERIFIED" in output and "NOT VERIFIED" not in output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--shard-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    result = json.loads(args.shard_result.read_text(encoding="utf-8"))
    if (
        plan.get("schema")
        != "ramsey55.automorphism7_pair_lifted_shard_pilot_plan.v1"
        or result.get("pipeline")
        != "ramsey55_automorphism7_pair_lifted_shard_v1"
    ):
        raise SystemExit("bad plan/result")
    paths = {
        label: (
            Path(record["path"])
            if Path(record["path"]).is_absolute()
            else ROOT / record["path"]
        )
        for label, record in plan["pins"].items()
    }
    paths["runner"] = ROOT / plan["runner"]["path"]
    paths["checker"] = Path(__file__).resolve()
    paths["tests"] = ROOT / plan["tests"]["path"]
    for label, path in paths.items():
        record = (
            plan[label]
            if label in {"runner", "checker", "tests"}
            else plan["pins"][label]
        )
        validate_pin(record, path, label)
    outputs = {
        name: ROOT / relative for name, relative in plan["outputs"].items()
    }
    if outputs["result"].resolve() != args.shard_result.resolve():
        raise SystemExit("shard result mismatch")
    if outputs["independent_check"].resolve() != args.output.resolve():
        raise SystemExit("independent-check output mismatch")
    if any(
        not path.is_file()
        for name, path in outputs.items()
        if name != "independent_check"
    ):
        raise FileNotFoundError("planned artifact missing")
    side_bundle = json.loads(
        paths["side_exhaustion_bundle"].read_text(encoding="utf-8")
    )
    if side_bundle.get("valid") is not True:
        raise AssertionError("side bundle invalid")

    edge_orbits, representatives, schedule = schedule_from_certified_models(
        certified_models(paths["side_models"])
    )
    shard_index = int(plan["shard"]["index"])
    shard_count = int(plan["shard"]["count"])
    pair_indices = [
        index for index in range(len(schedule)) if index % shard_count == shard_index
    ]
    base_variables, base_clauses = sample_check.parse_dimacs(paths["cnf"])
    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    table = sample_check.edge_table(metadata)
    fixed_units, map_a, map_b = sample_check.fixed_and_side_maps(table)
    if base_variables != BASE_VARIABLE_COUNT:
        raise AssertionError("bad base formula")
    expected_records: list[dict[str, Any]] = []
    for pair_index in pair_indices:
        left, right = schedule[pair_index]
        cube = side_cube(
            representatives[left], representatives[right], map_a, map_b
        )
        expected_records.append(
            {
                "pair_index": pair_index,
                "pair": [left, right],
                "selector": BASE_VARIABLE_COUNT + pair_index + 1,
                "side_units": list(cube),
                "blocker": [-literal for literal in cube],
            }
        )
    expected_wrapper = wrapper_bytes(
        base_clauses, fixed_units, expected_records
    )
    wrapper_exact = outputs["wrapper_cnf"].read_bytes() == expected_wrapper

    proof = outputs["lifted_drat"].read_bytes()
    observed_records = result["records"]
    if len(observed_records) != len(expected_records):
        raise AssertionError("record count mismatch")
    offset = 0
    segment_audits: list[dict[str, object]] = []
    for expected, observed in zip(expected_records, observed_records):
        for key in ("pair_index", "pair", "selector", "side_units", "blocker"):
            if observed[key] != expected[key]:
                raise AssertionError(f"record mismatch: {key}")
        if int(observed["segment_offset"]) != offset:
            raise AssertionError("segment offset gap")
        size = int(observed["segment_bytes"])
        segment_audits.append(
            sample_check.audit_segment(
                proof[offset : offset + size], expected, observed
            )
        )
        offset += size
    if proof[offset:] != b"0\n":
        raise AssertionError("proof stream has wrong terminator")

    compressed_checks: dict[str, bool] = {}
    for raw_name, compressed_name in (
        ("lifted_drat", "lifted_drat_zstd"),
        ("lifted_lrat", "lifted_lrat_zstd"),
    ):
        decompressed = subprocess.run(
            [
                str(paths["zstd"]),
                "-d",
                "-q",
                "-c",
                str(outputs[compressed_name]),
            ],
            capture_output=True,
            check=False,
            timeout=600,
        )
        matches = (
            decompressed.returncode == 0
            and decompressed.stdout == outputs[raw_name].read_bytes()
        )
        compressed_checks[raw_name] = matches
        if not matches:
            raise AssertionError("compressed artifact mismatch")

    caps = plan["hard_caps"]
    if shutil.disk_usage(args.output.parent).free < (
        int(caps["minimum_free_bytes_after_completion"])
        + int(caps["raw_lrat_bytes"])
    ):
        raise RuntimeError("independent replay storage gate failed")
    with tempfile.TemporaryDirectory(
        prefix="automorphism7-shard-independent-replay-",
        dir=args.output.parent,
    ) as temporary_directory:
        regenerated = Path(temporary_directory) / "regenerated.lrat"
        drat = subprocess.run(
            [
                str(paths["drat_trim"]),
                str(outputs["wrapper_cnf"]),
                str(outputs["lifted_drat"]),
                "-I",
                "-L",
                str(regenerated),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=int(plan["proof_check_timeout_seconds"]),
        )
        drat_valid = (
            drat.returncode == 0
            and verified(drat.stdout + drat.stderr)
            and regenerated.is_file()
            and regenerated.stat().st_size <= int(caps["raw_lrat_bytes"])
        )
        regenerated_sha = (
            sha256_file(regenerated) if regenerated.is_file() else None
        )
        lrat_exact = (
            drat_valid
            and regenerated.read_bytes() == outputs["lifted_lrat"].read_bytes()
        )
    lrat = subprocess.run(
        [
            str(paths["lrat_check"]),
            str(outputs["wrapper_cnf"]),
            str(outputs["lifted_lrat"]),
        ],
        capture_output=True,
        text=True,
        check=False,
        timeout=int(plan["proof_check_timeout_seconds"]),
    )
    lrat_valid = lrat.returncode == 0 and verified(lrat.stdout + lrat.stderr)
    cap_checks = {
        "wrapper": outputs["wrapper_cnf"].stat().st_size
        <= int(caps["wrapper_bytes"]),
        "raw_drat": outputs["lifted_drat"].stat().st_size
        <= int(caps["raw_drat_bytes"]),
        "raw_lrat": outputs["lifted_lrat"].stat().st_size
        <= int(caps["raw_lrat_bytes"]),
        "compressed_drat": outputs["lifted_drat_zstd"].stat().st_size
        <= int(caps["compressed_drat_bytes"]),
        "compressed_lrat": outputs["lifted_lrat_zstd"].stat().st_size
        <= int(caps["compressed_lrat_bytes"]),
    }
    valid = (
        wrapper_exact
        and len(segment_audits) == len(pair_indices)
        and drat_valid
        and lrat_valid
        and lrat_exact
        and all(compressed_checks.values())
        and all(cap_checks.values())
        and result.get("status") == "CERTIFIED_UNSAT_SHARD"
        and result.get("all_pairs_unsat_within_budget") is True
    )
    check_result = {
        "checker": CHECKER_ID,
        "valid": valid,
        "evidence_label": "INDEPENDENT CERTIFIED-MODEL SHARD REPLAY",
        "claim_boundary": (
            "This independently certifies one shard only. No conclusion "
            "about the other 127 shards is made."
        ),
        "shard_index": shard_index,
        "shard_count": shard_count,
        "pair_count": len(pair_indices),
        "first_pair_index": pair_indices[0],
        "last_pair_index": pair_indices[-1],
        "pair_schedule_sha256": EXPECTED_SCHEDULE_SHA256,
        "certified_side_model_count": 191394,
        "certified_schedule_reconstruction": True,
        "wrapper_exact": wrapper_exact,
        "wrapper_sha256": sha256_file(outputs["wrapper_cnf"]),
        "segment_count": len(segment_audits),
        "all_segments_exact": True,
        "drat_sha256": sha256_file(outputs["lifted_drat"]),
        "drat_trim_valid": drat_valid,
        "lrat_sha256": sha256_file(outputs["lifted_lrat"]),
        "regenerated_lrat_sha256": regenerated_sha,
        "regenerated_lrat_exact": lrat_exact,
        "lrat_check_valid": lrat_valid,
        "compressed_checks": compressed_checks,
        "cap_checks": cap_checks,
        "shard_result_sha256": sha256_file(args.shard_result),
        "plan_sha256": sha256_file(args.plan),
        "runtime_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(check_result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(check_result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
