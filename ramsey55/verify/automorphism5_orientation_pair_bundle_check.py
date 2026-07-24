#!/usr/bin/env python3
"""Independently reconstruct and verify the 40 order-5 orientation pairs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verify"))

import automorphism5_selector_cover_check as structural  # noqa: E402
from automorphism_orbit_cnf_check import independently_build  # noqa: E402


CHECKER_ID = "ramsey55_order5_orientation_pair40_independent_checker_v1"
EXPECTED_PLAN_ID = "ramsey55_order5_orientation_pair40_plan_v1"
EXPECTED_RESULT_ID = "ramsey55_order5_orientation_pair_result_v1"
DEFAULT_PLAN = (
    ROOT
    / "results"
    / "benchmark_plans"
    / "automorphism5_orientation_pair40_v1.json"
)
DEFAULT_BUNDLE = (
    ROOT
    / "certificates"
    / "order43_automorphism5_orientation_pairs40"
)
DEFAULT_SUMMARY = (
    ROOT
    / "results"
    / "global_exact"
    / "automorphism5_orientation_pair40_v1.json"
)
DEFAULT_RESULT = (
    ROOT
    / "results"
    / "verification"
    / "automorphism5_orientation_pair40_check.json"
)


class CheckError(RuntimeError):
    """A cover or certificate invariant failed."""


def sha256_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            state.update(block)
    return state.hexdigest()


def atomic_json(path: Path, value: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as stream:
            temporary = stream.name
            json.dump(value, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


def says_verified(output: str) -> bool:
    return any(
        "VERIFIED" in line and "NOT VERIFIED" not in line
        for line in output.splitlines()
    )


def write_dimacs(
    path: Path, variables: int, clauses: Sequence[Sequence[int]]
) -> None:
    with path.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def decompress(
    archive: Path, target: Path, zstd: Path
) -> tuple[str, int]:
    with target.open("wb") as stream:
        completed = subprocess.run(
            (str(zstd), "-d", "-c", "-q", str(archive)),
            stdout=stream,
            stderr=subprocess.PIPE,
            check=False,
        )
    if completed.returncode != 0:
        raise CheckError(completed.stderr.decode(errors="replace"))
    return sha256_file(target), target.stat().st_size


def validate_pins(plan: Mapping[str, object]) -> dict[str, Path]:
    tools = plan.get("tools")
    sources = plan.get("sources")
    if not isinstance(tools, dict) or not isinstance(sources, dict):
        raise CheckError("plan pins are missing")
    paths: dict[str, Path] = {}
    for collection, label in ((tools, "tool"), (sources, "source")):
        for name, raw in collection.items():
            if not isinstance(raw, dict):
                raise CheckError(f"malformed {label} pin: {name}")
            path = Path(str(raw.get("path")))
            if (
                not path.is_file()
                or raw.get("sha256") != sha256_file(path)
                or raw.get("bytes") != path.stat().st_size
            ):
                raise CheckError(f"{label} pin changed: {name}")
            if collection is tools:
                paths[name] = path
    return paths


def check(
    plan_path: Path, bundle: Path, summary_path: Path
) -> dict[str, object]:
    started = time.monotonic()
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if plan.get("plan") != EXPECTED_PLAN_ID:
        raise CheckError("unexpected plan identifier")
    tools = validate_pins(plan)
    zstd = tools["zstd"]
    drat_trim = tools["drat_trim"]
    lrat_check = tools["lrat_check"]
    batches = plan.get("batches")
    if not isinstance(batches, list) or len(batches) != 40:
        raise CheckError("plan must contain exactly 40 batches")
    scheduled_indices = [
        int(index)
        for batch in batches
        for index in batch["orientation_indices"]
    ]
    if scheduled_indices != list(range(80)):
        raise CheckError("plan schedule is not an exact ordered cover")
    if (
        summary.get("status") != "CERTIFIED_UNSAT"
        or summary.get("all_orientations_certified_unsat") is not True
        or summary.get("certified_orientation_indices") != list(range(80))
        or summary.get("plan_sha256") != sha256_file(plan_path)
    ):
        raise CheckError("production summary is not a complete certificate")

    _, orbits, base_clauses = independently_build(5, 8)
    orientations = structural.independent_orientations()
    if len(orientations) != 80:
        raise CheckError("independent orientation cover is not size 80")
    records = []
    with tempfile.TemporaryDirectory(prefix="r55-aut5-pair-check-") as raw:
        temporary = Path(raw)
        for position, expected in enumerate(batches):
            identifier = str(expected["id"])
            metadata_path = bundle / f"{identifier}.metadata.json"
            result_path = bundle / f"{identifier}.result.json"
            drat_archive = bundle / f"{identifier}.drat.zst"
            lrat_archive = bundle / f"{identifier}.lrat.zst"
            for path in (
                metadata_path,
                result_path,
                drat_archive,
                lrat_archive,
            ):
                if not path.is_file():
                    raise CheckError(f"missing batch artifact: {path}")
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            result = json.loads(result_path.read_text(encoding="utf-8"))
            clauses = structural.expected_orientation_formula(
                metadata,
                independent_orbits=orbits,
                independent_base_clauses=base_clauses,
            )
            variables = 183 + int(expected["count"])
            cnf = temporary / f"{identifier}.cnf"
            write_dimacs(cnf, variables, clauses)
            cnf_hash = sha256_file(cnf)
            if (
                metadata.get("cnf_sha256") != cnf_hash
                or metadata.get("cnf_bytes") != cnf.stat().st_size
                or metadata.get("clause_count") != len(clauses)
                or metadata.get("variable_count") != variables
                or result.get("result") != EXPECTED_RESULT_ID
                or result.get("status") != "CERTIFIED_UNSAT"
                or result.get("formula_sha256") != cnf_hash
                or result.get("formula_bytes") != cnf.stat().st_size
                or result.get("orientation_indices")
                != expected["orientation_indices"]
                or result.get("orientations") != expected["orientations"]
                or result.get("drat_core_check_valid") is not True
                or result.get("lrat_check_valid") is not True
            ):
                raise CheckError(f"batch metadata/result mismatch: {identifier}")

            drat_record = result.get("drat_zstd")
            lrat_record = result.get("lrat_zstd")
            if not isinstance(drat_record, dict) or not isinstance(
                lrat_record, dict
            ):
                raise CheckError("compressed proof metadata is missing")
            if (
                drat_record.get("sha256") != sha256_file(drat_archive)
                or drat_record.get("bytes") != drat_archive.stat().st_size
                or lrat_record.get("sha256") != sha256_file(lrat_archive)
                or lrat_record.get("bytes") != lrat_archive.stat().st_size
            ):
                raise CheckError("compressed proof hash mismatch")
            drat = temporary / f"{identifier}.drat"
            lrat = temporary / f"{identifier}.lrat"
            drat_hash, drat_bytes = decompress(drat_archive, drat, zstd)
            lrat_hash, lrat_bytes = decompress(lrat_archive, lrat, zstd)
            if (
                result.get("drat_uncompressed")
                != {"sha256": drat_hash, "bytes": drat_bytes}
                or result.get("lrat_uncompressed")
                != {"sha256": lrat_hash, "bytes": lrat_bytes}
            ):
                raise CheckError("uncompressed proof hash mismatch")
            checked_drat = subprocess.run(
                (str(drat_trim), str(cnf), str(drat), "-I"),
                text=True,
                capture_output=True,
                check=False,
            )
            checked_lrat = subprocess.run(
                (str(lrat_check), str(cnf), str(lrat)),
                text=True,
                capture_output=True,
                check=False,
            )
            drat_valid = (
                checked_drat.returncode == 0
                and says_verified(checked_drat.stdout + checked_drat.stderr)
            )
            lrat_valid = (
                checked_lrat.returncode == 0
                and says_verified(checked_lrat.stdout + checked_lrat.stderr)
            )
            if not drat_valid or not lrat_valid:
                raise CheckError(f"proof checker rejected {identifier}")
            records.append(
                {
                    "id": identifier,
                    "orientation_indices": expected["orientation_indices"],
                    "formula_sha256": cnf_hash,
                    "drat_valid": drat_valid,
                    "lrat_valid": lrat_valid,
                    "drat_zstd_sha256": sha256_file(drat_archive),
                    "lrat_zstd_sha256": sha256_file(lrat_archive),
                }
            )
            cnf.unlink()
            drat.unlink()
            lrat.unlink()
            print(
                json.dumps(
                    {
                        "event": "batch_checked",
                        "id": identifier,
                        "completed": position + 1,
                        "scheduled": 40,
                    },
                    sort_keys=True,
                ),
                file=sys.stderr,
                flush=True,
            )
    fixed_cover = structural.normalized_fixed_graph_cover()
    degree = structural.degree_normalization()
    valid = (
        len(records) == 40
        and fixed_cover["valid"] is True
        and degree["valid"] is True
    )
    return {
        "checker": CHECKER_ID,
        "valid": valid,
        "plan_sha256": sha256_file(plan_path),
        "summary_sha256": sha256_file(summary_path),
        "batch_count": len(records),
        "certified_orientation_indices": list(range(80)),
        "all_orientations_certified_unsat": True,
        "fixed_graph_normalization_valid": fixed_cover["valid"],
        "degree_normalization_valid": degree["valid"],
        "claim_boundary": (
            "This checks only the 80-orbit internal-orientation cover of the "
            "one-edge all-ones normalized type. The other 58 structural "
            "types require their separate selector-union certificate."
        ),
        "full_cycle_type_covered": False,
        "records": records,
        "runtime_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    args = parser.parse_args()
    result = check(args.plan, args.bundle, args.summary)
    atomic_json(args.result, result)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
