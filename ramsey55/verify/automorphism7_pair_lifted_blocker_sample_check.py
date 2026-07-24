#!/usr/bin/env python3
"""Independently audit the selector-guarded C7 proof-lifting sample."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import os
import subprocess
import tempfile
import time
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKER_ID = "ramsey55_automorphism7_pair_lifted_blocker_sample_checker_v1"
ORDER = 43
PRIME = 7
BASE_VARIABLE_COUNT = 129


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_dimacs(path: Path) -> tuple[int, tuple[tuple[int, ...], ...]]:
    variable_count = clause_count = None
    clauses: list[tuple[int, ...]] = []
    for line_number, raw in enumerate(
        path.read_text(encoding="ascii").splitlines(), start=1
    ):
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            fields = line.split()
            if (
                len(fields) != 4
                or fields[:2] != ["p", "cnf"]
                or variable_count is not None
            ):
                raise ValueError(f"bad header at line {line_number}")
            variable_count, clause_count = map(int, fields[2:])
            continue
        if variable_count is None:
            raise ValueError("clause before header")
        fields = tuple(map(int, line.split()))
        if not fields or fields[-1] != 0 or 0 in fields[:-1]:
            raise ValueError(f"bad clause at line {line_number}")
        clause = fields[:-1]
        if any(abs(literal) > variable_count for literal in clause):
            raise ValueError("literal outside declared range")
        clauses.append(clause)
    if variable_count is None or clause_count != len(clauses):
        raise ValueError("DIMACS count mismatch")
    return variable_count, tuple(clauses)


def dimacs_bytes(
    variable_count: int, clauses: tuple[tuple[int, ...], ...]
) -> bytes:
    lines = [f"p cnf {variable_count} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def edge_table(metadata: dict[str, object]) -> dict[tuple[int, int], int]:
    raw_orbits = metadata.get("edge_orbits")
    if not isinstance(raw_orbits, list):
        raise ValueError("missing edge orbits")
    table: dict[tuple[int, int], int] = {}
    for raw_orbit in raw_orbits:
        if not isinstance(raw_orbit, dict):
            raise ValueError("bad orbit record")
        variable = raw_orbit.get("variable")
        edges = raw_orbit.get("edges")
        if type(variable) is not int or not isinstance(edges, list):
            raise ValueError("bad orbit fields")
        for raw_edge in edges:
            if (
                not isinstance(raw_edge, list)
                or len(raw_edge) != 2
                or any(type(vertex) is not int for vertex in raw_edge)
            ):
                raise ValueError("bad edge")
            edge = tuple(raw_edge)
            if not 0 <= edge[0] < edge[1] < ORDER or edge in table:
                raise ValueError("invalid or duplicate edge")
            table[edge] = variable
    multiplicities = Counter(table.values())
    if (
        len(table) != math.comb(ORDER, 2)
        or set(multiplicities) != set(range(1, BASE_VARIABLE_COUNT + 1))
        or set(multiplicities.values()) != {PRIME}
    ):
        raise ValueError("bad global edge partition")
    return table


def side_edge_orbits() -> tuple[tuple[tuple[int, int], ...], ...]:
    rotate = tuple(
        block * PRIME + (offset + 1) % PRIME
        for block in range(3)
        for offset in range(PRIME)
    )
    unseen = set(itertools.combinations(range(21), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        seed = min(unseen)
        edge = seed
        orbit: set[tuple[int, int]] = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((rotate[edge[0]], rotate[edge[1]])))
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    orbits.sort(key=lambda orbit: orbit[0])
    if len(orbits) != 30:
        raise AssertionError("unexpected side orbit count")
    return tuple(orbits)


def fixed_and_side_maps(
    table: dict[tuple[int, int], int],
) -> tuple[list[int], list[int], list[int]]:
    orbits = side_edge_orbits()
    map_a = [table[orbit[0]] for orbit in orbits]
    map_b = [
        table[(orbit[0][0] + 21, orbit[0][1] + 21)] for orbit in orbits
    ]
    fixed_variables = sorted(
        {
            variable
            for (left, right), variable in table.items()
            if right == ORDER - 1
        },
        key=lambda variable: min(
            left
            for (left, right), observed in table.items()
            if right == ORDER - 1 and observed == variable
        ),
    )
    fixed_units = fixed_variables[:3] + [
        -variable for variable in fixed_variables[3:]
    ]
    if len(set(map(abs, fixed_units + map_a + map_b))) != 66:
        raise AssertionError("bad fixed/side variable partition")
    return fixed_units, map_a, map_b


def cube_from_models(
    models: list[str], map_a: list[int], map_b: list[int]
) -> tuple[int, ...]:
    if len(models) != 2 or any(len(model) != 30 for model in models):
        raise ValueError("bad model strings")
    left_model, right_model = map(lambda model: int(model, 2), models)
    units = [
        variable if left_model >> index & 1 else -variable
        for index, variable in enumerate(map_a)
    ]
    units.extend(
        -variable if right_model >> index & 1 else variable
        for index, variable in enumerate(map_b)
    )
    return tuple(units)


def reconstruct_wrapper(
    base_clauses: tuple[tuple[int, ...], ...],
    fixed_units: list[int],
    source_samples: list[dict[str, Any]],
    map_a: list[int],
    map_b: list[int],
) -> tuple[tuple[tuple[int, ...], ...], list[dict[str, Any]]]:
    clauses = list(base_clauses)
    clauses.extend((unit,) for unit in fixed_units)
    samples: list[dict[str, Any]] = []
    selectors: list[int] = []
    for position, source in enumerate(source_samples):
        selector = BASE_VARIABLE_COUNT + position + 1
        cube = cube_from_models(source["models"], map_a, map_b)
        blocker = tuple(-literal for literal in cube)
        selectors.append(selector)
        clauses.extend((-selector, literal) for literal in cube)
        clauses.append((selector, *blocker))
        samples.append(
            {
                "sample_position": position,
                "pair_index": int(source["pair_index"]),
                "pair": source["pair"],
                "models": source["models"],
                "selector": selector,
                "side_units": list(cube),
                "blocker": list(blocker),
            }
        )
    clauses.append(tuple(selectors))
    return tuple(clauses), samples


def parse_drat_line(line: str) -> tuple[bool, tuple[int, ...]]:
    fields = line.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError("bad DRAT line")
    clause = tuple(map(int, fields[:-1]))
    if 0 in clause:
        raise ValueError("internal zero")
    return deletion, clause


def audit_segment(
    payload: bytes,
    expected: dict[str, Any],
    reported: dict[str, Any],
) -> dict[str, object]:
    if sha256_bytes(payload) != reported["segment_sha256"]:
        raise AssertionError("segment hash mismatch")
    if len(payload) != reported["segment_bytes"]:
        raise AssertionError("segment size mismatch")
    lines = payload.decode("ascii").splitlines()
    additions = int(reported["guarded_addition_count"])
    if len(lines) != 2 * additions + 2:
        raise AssertionError("segment record count mismatch")
    selector = int(expected["selector"])
    blocker = tuple(int(literal) for literal in expected["blocker"])

    guarded: list[tuple[int, ...]] = []
    for line in lines[:additions]:
        deletion, clause = parse_drat_line(line)
        if deletion or -selector not in clause:
            raise AssertionError("malformed guarded addition")
        if any(abs(literal) > BASE_VARIABLE_COUNT for literal in clause if literal != -selector):
            raise AssertionError("guarded addition uses an unexpected variable")
        guarded.append(clause)
    if guarded[-1] != (-selector,):
        raise AssertionError("guarded proof does not discharge to -selector")

    deletion, observed_blocker = parse_drat_line(lines[additions])
    if deletion or observed_blocker != blocker:
        raise AssertionError("wrong derived blocker")

    deletion_lines = lines[additions + 1 : additions + 1 + additions]
    observed_deletions: list[tuple[int, ...]] = []
    for line in deletion_lines:
        deletion, clause = parse_drat_line(line)
        if not deletion:
            raise AssertionError("expected guarded-clause deletion")
        observed_deletions.append(clause)
    if observed_deletions != guarded:
        raise AssertionError("guarded deletion list mismatch")

    deletion, final_selector = parse_drat_line(lines[-1])
    if deletion or final_selector != (-selector,):
        raise AssertionError("selector was not rederived after the blocker")
    return {
        "pair_index": expected["pair_index"],
        "selector": selector,
        "segment_sha256": sha256_bytes(payload),
        "segment_bytes": len(payload),
        "guarded_addition_count": additions,
        "blocker_exact": True,
        "temporary_derivation_deleted_exactly": True,
        "selector_rederived_after_blocker": True,
    }


def checker_says_verified(output: str) -> bool:
    return "VERIFIED" in output and "NOT VERIFIED" not in output


def validate_pin(record: object, path: Path, label: str) -> None:
    if (
        not isinstance(record, dict)
        or Path(str(record.get("path", ""))).resolve() != path.resolve()
        or record.get("sha256") != sha256_file(path)
    ):
        raise ValueError(f"pin mismatch: {label}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--sample-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    started = time.monotonic()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    sample_result = json.loads(args.sample_result.read_text(encoding="utf-8"))
    if (
        plan.get("schema")
        != "ramsey55.automorphism7_pair_lifted_blocker_sample_plan.v1"
        or sample_result.get("pipeline")
        != "ramsey55_automorphism7_pair_lifted_blocker_sample_v1"
    ):
        raise SystemExit("wrong plan/result schema")

    paths = {
        "cnf": ROOT / str(plan["cnf"]["path"]),
        "metadata": ROOT / str(plan["metadata"]["path"]),
        "source_sample_plan": ROOT / str(plan["source_sample_plan"]["path"]),
        "source_sample_result": ROOT / str(plan["source_sample_result"]["path"]),
        "pair_audit": ROOT / str(plan["pair_audit"]["path"]),
        "runner": ROOT / str(plan["runner"]["path"]),
        "checker": Path(__file__).resolve(),
        "tests": ROOT / str(plan["tests"]["path"]),
        "drat_trim": Path(str(plan["drat_trim"]["path"])),
        "lrat_check": Path(str(plan["lrat_check"]["path"])),
        "zstd": Path(str(plan["zstd"]["path"])),
        "pysat": Path(str(plan["pysat"]["path"])),
    }
    for label, path in paths.items():
        validate_pin(plan[label], path, label)
    outputs = {
        name: ROOT / str(relative)
        for name, relative in plan["outputs"].items()
    }
    if outputs["result"].resolve() != args.sample_result.resolve():
        raise SystemExit("sample result path mismatch")
    if any(not path.is_file() for path in outputs.values()):
        raise FileNotFoundError("a planned output is missing")

    base_variables, base_clauses = parse_dimacs(paths["cnf"])
    metadata = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    source_plan = json.loads(
        paths["source_sample_plan"].read_text(encoding="utf-8")
    )
    if base_variables != BASE_VARIABLE_COUNT or not isinstance(metadata, dict):
        raise ValueError("unexpected base instance")
    fixed_units, map_a, map_b = fixed_and_side_maps(edge_table(metadata))
    wrapper, expected_samples = reconstruct_wrapper(
        base_clauses,
        fixed_units,
        source_plan["samples"],
        map_a,
        map_b,
    )
    wrapper_payload = dimacs_bytes(
        BASE_VARIABLE_COUNT + len(expected_samples), wrapper
    )
    if outputs["wrapper_cnf"].read_bytes() != wrapper_payload:
        raise AssertionError("wrapper CNF differs from independent reconstruction")
    if sample_result["wrapper"]["sha256"] != sha256_bytes(wrapper_payload):
        raise AssertionError("reported wrapper hash mismatch")

    proof_payload = outputs["lifted_drat"].read_bytes()
    reported_records = sample_result["records"]
    if len(reported_records) != len(expected_samples):
        raise AssertionError("wrong record count")
    segment_audits: list[dict[str, object]] = []
    expected_offset = 0
    for expected, reported in zip(expected_samples, reported_records):
        for key in (
            "sample_position",
            "pair_index",
            "pair",
            "models",
            "selector",
            "side_units",
            "blocker",
        ):
            if reported[key] != expected[key]:
                raise AssertionError(f"record mismatch: {key}")
        if int(reported["segment_offset"]) != expected_offset:
            raise AssertionError("noncontiguous segment offsets")
        length = int(reported["segment_bytes"])
        segment = proof_payload[expected_offset : expected_offset + length]
        segment_audits.append(audit_segment(segment, expected, reported))
        expected_offset += length
    if proof_payload[expected_offset:] != b"0\n":
        raise AssertionError("stream does not end in exactly one empty clause")

    compressed_checks: dict[str, dict[str, object]] = {}
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
            timeout=300,
        )
        if decompressed.returncode != 0:
            raise AssertionError("zstd decompression failed")
        raw = outputs[raw_name].read_bytes()
        compressed_checks[raw_name] = {
            "compressed_sha256": sha256_file(outputs[compressed_name]),
            "compressed_bytes": outputs[compressed_name].stat().st_size,
            "decompressed_sha256": sha256_bytes(decompressed.stdout),
            "matches_raw": decompressed.stdout == raw,
        }
        if decompressed.stdout != raw:
            raise AssertionError("compressed artifact does not match raw")

    with tempfile.TemporaryDirectory(
        prefix="automorphism7-lifted-independent-check-",
        dir=args.output.parent,
    ) as temporary_directory:
        regenerated_lrat = Path(temporary_directory) / "regenerated.lrat"
        drat = subprocess.run(
            [
                str(paths["drat_trim"]),
                str(outputs["wrapper_cnf"]),
                str(outputs["lifted_drat"]),
                "-I",
                "-L",
                str(regenerated_lrat),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=int(plan["proof_check_timeout_seconds"]),
        )
        drat_valid = (
            drat.returncode == 0
            and checker_says_verified(drat.stdout + drat.stderr)
            and regenerated_lrat.is_file()
        )
        regenerated_lrat_sha256 = (
            sha256_file(regenerated_lrat) if regenerated_lrat.is_file() else None
        )
        lrat_reproduced_exactly = (
            drat_valid
            and regenerated_lrat.read_bytes()
            == outputs["lifted_lrat"].read_bytes()
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
    lrat_valid = (
        lrat.returncode == 0
        and checker_says_verified(lrat.stdout + lrat.stderr)
    )
    valid = (
        len(segment_audits) == 12
        and drat_valid
        and lrat_valid
        and lrat_reproduced_exactly
        and all(record["blocker_exact"] for record in segment_audits)
        and all(check["matches_raw"] for check in compressed_checks.values())
    )
    result = {
        "checker": CHECKER_ID,
        "valid": valid,
        "evidence_label": "INDEPENDENT WRAPPER, STREAM, DRAT, AND LRAT REPLAY",
        "claim_boundary": (
            "This validates a proof of the disjunction of the twelve sampled "
            "cubes only.  It does not establish the complete 37,194-cube "
            "cover or certify the order-7 branch."
        ),
        "wrapper": {
            "sha256": sha256_file(outputs["wrapper_cnf"]),
            "bytes": outputs["wrapper_cnf"].stat().st_size,
            "variable_count": BASE_VARIABLE_COUNT + len(expected_samples),
            "clause_count": len(wrapper),
            "independent_reconstruction_exact": True,
        },
        "lifted_drat": {
            "sha256": sha256_file(outputs["lifted_drat"]),
            "bytes": outputs["lifted_drat"].stat().st_size,
            "drat_trim_valid": drat_valid,
        },
        "lifted_lrat": {
            "sha256": sha256_file(outputs["lifted_lrat"]),
            "bytes": outputs["lifted_lrat"].stat().st_size,
            "regenerated_sha256": regenerated_lrat_sha256,
            "regenerated_exactly": lrat_reproduced_exactly,
            "lrat_check_valid": lrat_valid,
        },
        "compressed_checks": compressed_checks,
        "segments": segment_audits,
        "sample_result_sha256": sha256_file(args.sample_result),
        "plan_sha256": sha256_file(args.plan),
        "runtime_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0 if valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
