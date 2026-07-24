#!/usr/bin/env python3
"""Validate and summarize the bounded global exact-track artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SUMMARY_ID = "ramsey55_global_exact_pilot_summary_v1"
DEGREES = (18, 19, 20, 21)
EXPECTED_BASE_SHA256 = (
    "141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while block := source.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} does not contain a JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir", type=Path, default=Path("results/global_exact")
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    audit_path = args.results_dir / "proof_solver_audit.json"
    audit = load(audit_path)
    approved = audit.get("approved_solvers")
    if not isinstance(approved, list) or "MapleChrono" not in approved:
        raise ValueError("MapleChrono did not pass the recorded proof audit")

    branches: list[dict[str, object]] = []
    artifact_paths = [audit_path]
    for degree in DEGREES:
        metadata_path = args.results_dir / f"branch_d{degree}.metadata.json"
        check_path = args.results_dir / f"branch_d{degree}.check.json"
        pilot_path = (
            args.results_dir
            / "pilots"
            / f"d{degree}_maplechrono_200k.json"
        )
        metadata = load(metadata_path)
        check = load(check_path)
        pilot = load(pilot_path)
        artifact_paths.extend((metadata_path, check_path, pilot_path))
        consistency = {
            "metadata_degree": metadata.get("degree") == degree,
            "metadata_base_hash": (
                metadata.get("base_cnf_sha256") == EXPECTED_BASE_SHA256
            ),
            "branch_check_valid": check.get("valid") is True,
            "check_hash_matches_metadata": (
                check.get("branch_cnf_sha256") == metadata.get("cnf_sha256")
            ),
            "pilot_hash_matches_metadata": (
                pilot.get("cnf_sha256") == metadata.get("cnf_sha256")
            ),
            "pilot_solver": pilot.get("solver") == "MapleChrono",
            "pilot_budget": pilot.get("conflict_budget") == 200_000,
            "pilot_status": pilot.get("status") == "BUDGET_EXHAUSTED",
            "pilot_has_no_proof": pilot.get("proof_written") is False,
        }
        if not all(consistency.values()):
            raise ValueError(
                f"inconsistent degree-{degree} artifacts: {consistency}"
            )
        branches.append(
            {
                "degree": degree,
                "branch_cnf_sha256": metadata["cnf_sha256"],
                "branch_cnf_bytes": metadata["cnf_bytes"],
                "variable_count": metadata["variable_count"],
                "clause_count": metadata["clause_count"],
                "status": pilot["status"],
                "conflict_budget": pilot["conflict_budget"],
                "observed_conflicts": pilot["conflicts"],
                "decisions": pilot["decisions"],
                "propagations": pilot["propagations"],
                "restarts": pilot["restarts"],
                "runtime_seconds": pilot["runtime_seconds"],
                "solver_cpu_seconds": pilot["solver_cpu_seconds"],
                "maximum_resident_set_bytes": pilot[
                    "maximum_resident_set_bytes"
                ],
                "consistency": consistency,
            }
        )

    result = {
        "summary": SUMMARY_ID,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_category": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "global_outcome": "UNRESOLVED",
        "global_interpretation": (
            "No branch returned SAT. No branch returned UNSAT, so no DRAT/LRAT "
            "certificate was produced. Budget exhaustion is not evidence of "
            "nonexistence."
        ),
        "branch_cover": [18, 19, 20, 21],
        "branch_cover_scope": (
            "The base formula is SAT iff at least one listed degree branch is "
            "SAT; global UNSAT would require independently checked UNSAT "
            "proofs for all four branches."
        ),
        "base_cnf_sha256": EXPECTED_BASE_SHA256,
        "solver": "MapleChrono",
        "solver_distribution": (
            "python-sat 1.9.dev7, MapleLCMDistChronoBT SAT Competition "
            "2018 version"
        ),
        "proof_audit_sha256": sha256_file(audit_path),
        "approved_proof_solvers": approved,
        "excluded_proof_solvers": audit.get("excluded_solvers"),
        "total_observed_conflicts": sum(
            int(branch["observed_conflicts"]) for branch in branches
        ),
        "total_solver_cpu_seconds": sum(
            float(branch["solver_cpu_seconds"]) for branch in branches
        ),
        "branches": branches,
        "artifact_sha256": {
            str(path): sha256_file(path) for path in artifact_paths
        },
        "summary_source_sha256": sha256_file(Path(__file__)),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
