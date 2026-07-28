#!/usr/bin/env python3
"""Generate DRAT certificates for all dihedral C7 witness-partition orbits."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path


PROBE_PATH = Path(__file__).with_name("probe.py")
PROBE_SPEC = importlib.util.spec_from_file_location("inactive_rim_probe", PROBE_PATH)
if PROBE_SPEC is None or PROBE_SPEC.loader is None:
    raise RuntimeError("cannot load probe.py")
PROBE = importlib.util.module_from_spec(PROBE_SPEC)
PROBE_SPEC.loader.exec_module(PROBE)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            value.update(block)
    return value.hexdigest()


def normalize(values: tuple[int, ...]) -> str:
    labels: dict[int, int] = {}
    result: list[str] = []
    for value in values:
        if value not in labels:
            labels[value] = len(labels)
        result.append(str(labels[value]))
    return "".join(result)


def dihedral_images(partition: str) -> tuple[str, ...]:
    values = tuple(map(int, partition))
    images: set[str] = set()
    for reflected in (False, True):
        row = values[::-1] if reflected else values
        for shift in range(7):
            images.add(normalize(row[shift:] + row[:shift]))
    return tuple(sorted(images))


def canonical(partition: str) -> str:
    return min(dihedral_images(partition))


def run(command: list[str], log: Path) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    log.write_text(completed.stdout + completed.stderr, encoding="utf-8")
    return completed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()

    solver = arguments.solver.resolve()
    checker = arguments.checker.resolve()
    output = arguments.output.resolve()
    cases = output / "cases"
    cases.mkdir(parents=True, exist_ok=True)

    all_partitions = tuple(PROBE.restricted_growth_strings(7))
    orbit_map = {
        partition: canonical(partition) for partition in all_partitions
    }
    representatives = tuple(sorted(set(orbit_map.values())))
    if len(all_partitions) != 877 or len(representatives) != 93:
        raise AssertionError("unexpected Bell or dihedral-orbit count")

    records: list[dict[str, object]] = []
    for position, partition in enumerate(representatives, 1):
        cnf, metadata = PROBE.build(7, partition, False)
        stem = cases / partition
        instance = stem.with_suffix(".cnf")
        proof = stem.with_suffix(".drat")
        solver_log = stem.with_suffix(".solver.txt")
        checker_log = stem.with_suffix(".checker.txt")
        instance.write_text(cnf.dimacs(), encoding="ascii")

        solved = run([str(solver), str(instance), str(proof)], solver_log)
        if solved.returncode != 20 or "s UNSATISFIABLE" not in solved.stdout:
            raise RuntimeError(f"solver failed on {partition}")
        checked = run([str(checker), str(instance), str(proof)], checker_log)
        checker_text = checked.stdout + checked.stderr
        if checked.returncode != 0 or "s VERIFIED" not in checker_text:
            raise RuntimeError(f"checker rejected {partition}")

        record = {
            **metadata,
            "instance": instance.relative_to(output).as_posix(),
            "instance_sha256": digest(instance),
            "proof": proof.relative_to(output).as_posix(),
            "proof_sha256": digest(proof),
            "proof_size_bytes": proof.stat().st_size,
            "solver_log": solver_log.relative_to(output).as_posix(),
            "solver_log_sha256": digest(solver_log),
            "checker_log": checker_log.relative_to(output).as_posix(),
            "checker_log_sha256": digest(checker_log),
            "solver_returncode": solved.returncode,
            "checker_returncode": checked.returncode,
            "checker_verified": True,
            "orbit_size": sum(
                representative == partition
                for representative in orbit_map.values()
            ),
        }
        records.append(record)
        print(
            json.dumps(
                {
                    "case": position,
                    "of": len(representatives),
                    "partition": partition,
                    "order": metadata["order"],
                    "proof_bytes": proof.stat().st_size,
                },
                sort_keys=True,
            ),
            flush=True,
        )

    manifest = {
        "schema": "inactive-c7-dihedral-certificates-v1",
        "model": "one-guard-moves; unoccupied attacks only",
        "scope": (
            "all 877 equality patterns of seven rim-edge witnesses, "
            "reduced to 93 orbits under the dihedral action on C7"
        ),
        "coverage": {
            "partition_count": len(all_partitions),
            "representative_count": len(representatives),
            "partitions": list(all_partitions),
            "representatives": list(representatives),
            "orbit_map": orbit_map,
            "group": "D_7 generated by cyclic shift and reversal",
        },
        "solver": {"path": str(solver), "sha256": digest(solver)},
        "checker": {"path": str(checker), "sha256": digest(checker)},
        "cases": records,
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "manifest": str(manifest_path),
                "manifest_sha256": digest(manifest_path),
                "partition_count": len(all_partitions),
                "representative_count": len(representatives),
                "total_proof_bytes": sum(
                    int(record["proof_size_bytes"]) for record in records
                ),
                "all_verified": True,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
