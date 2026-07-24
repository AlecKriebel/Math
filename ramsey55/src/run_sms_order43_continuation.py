#!/usr/bin/env python3
"""Run one preregistered long SMS process on the audited order-43 CNF."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from graph_io import encode_graph6
from run_sms_global_pilot import (
    ROOT,
    inspect_graph,
    parse_edge_list,
    resolve,
    run,
    sha256,
    write_json,
)

sys.path.insert(0, str(ROOT / "verify"))
from sms_symmetry_clauses_check import check as check_symmetry  # noqa: E402


def verifier_accepts(run_result: dict[str, object]) -> bool:
    if run_result["returncode"] != 0 or run_result["outer_timeout"]:
        return False
    try:
        document = json.loads(str(run_result["stdout"]))
    except json.JSONDecodeError:
        return False
    return document.get("valid") is True


def audit_symmetry(
    transcript: Path,
    *,
    order: int,
    checker_source: Path,
    output: Path,
) -> dict[str, object]:
    started = time.monotonic()
    try:
        result = check_symmetry(transcript, order)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        result = {
            "schema": "ramsey55.sms_symmetry_check.v1",
            "checker": "independent_sms_row_lex_witness_checker_v1",
            "valid": False,
            "error": str(error),
        }
    result["runtime_seconds"] = time.monotonic() - started
    result["checker_source_sha256"] = sha256(checker_source)
    write_json(output, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan["status"] != "PREREGISTERED_BEFORE_ORDER43_900S_RUN":
        raise SystemExit("plan status does not authorize the long run")

    for record in plan["pinned_files"]:
        path = resolve(record["path"])
        if sha256(path) != record["sha256"]:
            raise SystemExit(f"pinned hash mismatch: {path}")

    experiment = plan["experiment"]
    encoding_check_path = resolve(plan["encoding"]["independent_check"])
    encoding_check = json.loads(encoding_check_path.read_text(encoding="utf-8"))
    cnf = resolve(experiment["cnf"])
    if (
        encoding_check.get("valid") is not True
        or encoding_check.get("cnf_sha256") != sha256(cnf)
        or encoding_check.get("cnf_sha256") != plan["encoding"]["cnf_sha256"]
    ):
        raise SystemExit("the CNF does not match its valid independent audit")

    symmetry_policy = plan["symmetry_policy"]
    if (
        symmetry_policy["label_fixing_units"] != []
        or symmetry_policy["color_partition"] is not None
        or symmetry_policy["initial_partition_argument"] is not None
    ):
        raise SystemExit("unsafe label fixing or partition requested")

    output = plan["output"]
    result_path = resolve(output["result"])
    transcript = resolve(output["symmetry_transcript"])
    audit_path = resolve(output["symmetry_audit"])
    candidate_path = resolve(output["candidate_graph6"])
    for path in (result_path, transcript, audit_path, candidate_path):
        if path.exists():
            raise SystemExit(f"refusing to overwrite preregistered output: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)

    binary = str(resolve(plan["solver"]["binary"]))
    command = [
        binary,
        "-v",
        str(experiment["order"]),
        "--dimacs",
        str(cnf),
        "--cutoff",
        str(experiment["minimality_cutoff"]),
        "--frequency",
        str(experiment["minimality_frequency"]),
        "--timeout",
        str(experiment["internal_timeout_seconds"]),
        "--sym-break-clauses",
        str(transcript),
    ]
    forbidden_options = {
        "--initial-partition",
        "--initial-partition-file",
        "--assumptions",
    }
    if any(option in command for option in forbidden_options):
        raise SystemExit("command unexpectedly requests label fixing or a partition")

    environment = os.environ.copy()
    environment["DYLD_LIBRARY_PATH"] = plan["solver"]["dyld_library_path"]
    solver_started_utc = datetime.now(timezone.utc).isoformat()
    solver_run = run(
        command,
        environment=environment,
        timeout=float(experiment["outer_timeout_seconds"]),
    )
    solver_finished_utc = datetime.now(timezone.utc).isoformat()

    returncode = solver_run["returncode"]
    if solver_run["outer_timeout"]:
        status = "EXTERNAL_TIMEOUT_UNKNOWN"
    elif returncode == 0:
        status = "INTERNAL_TIMEOUT_UNKNOWN"
    elif returncode == 10:
        status = "SAT"
    elif returncode == 20:
        status = "UNVERIFIED_SOLVER_UNSAT"
    else:
        status = "ERROR"

    candidate: dict[str, object] | None = None
    certified = False
    if status == "SAT":
        try:
            edges = parse_edge_list(str(solver_run["stdout"]))
            direct_check, adjacency = inspect_graph(
                edges,
                order=int(experiment["order"]),
                forbidden_size=int(experiment["forbidden_size"]),
                degree_lower=int(experiment["degree_lower"]),
                degree_upper=int(experiment["degree_upper"]),
            )
            # Preserve the construction before doing any transcript work, then
            # immediately run the two independent graph verifiers.
            candidate_path.write_text(
                encode_graph6(adjacency) + "\n", encoding="ascii"
            )
            python_verify = run(
                [
                    sys.executable,
                    "verify/exhaustive_verify.py",
                    str(candidate_path),
                ],
                environment=environment,
                timeout=120,
            )
            cpp_verify = run(
                [
                    str(resolve(plan["verification"]["bitset_binary"])),
                    str(candidate_path),
                ],
                environment=environment,
                timeout=120,
            )
            certified = (
                direct_check["valid"] is True
                and verifier_accepts(python_verify)
                and verifier_accepts(cpp_verify)
            )
            candidate = {
                "graph6_path": str(candidate_path.relative_to(ROOT)),
                "graph6_sha256": sha256(candidate_path),
                "direct_model_check": direct_check,
                "python_verifier": python_verify,
                "cpp_verifier": cpp_verify,
                "dual_verification_accepted": certified,
            }
        except (SyntaxError, TypeError, ValueError) as error:
            candidate = {
                "model_preservation_or_verification_error": str(error),
                "raw_model_retained_in_solver_stdout": True,
                "dual_verification_accepted": False,
            }

    audit = audit_symmetry(
        transcript,
        order=int(experiment["order"]),
        checker_source=resolve(plan["symmetry_policy"]["checker_source"]),
        output=audit_path,
    )
    match = re.search(
        r"Added clauses:\s*([0-9]+)", str(solver_run["stdout"])
    )
    solver_reported_clause_count = int(match.group(1)) if match else None
    audited_clause_count = audit.get("symmetry_clause_count")
    transcript_complete_and_audited = (
        not solver_run["outer_timeout"]
        and audit.get("valid") is True
        and solver_reported_clause_count is not None
        and solver_reported_clause_count == audited_clause_count
    )

    result = {
        "schema": "ramsey55.sms_order43_continuation_result.v1",
        "status": status,
        "evidence_label": (
            "CERTIFIED"
            if certified
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "claim_boundary": (
            "Only a returned graph accepted by direct enumeration and both "
            "independent graph verifiers is a certified construction. A raw "
            "UNSAT result has no mathematical force without a complete "
            "independently checked proof covering symmetry reasoning. "
            "Timeout/unknown is neither SAT nor UNSAT."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "solver_started_utc": solver_started_utc,
        "solver_finished_utc": solver_finished_utc,
        "solver_process_count": 1,
        "label_fixing_units_added": [],
        "color_partition_supplied": None,
        "initial_partition_argument_supplied": None,
        "solver_run": solver_run,
        "symmetry_audit": audit,
        "solver_reported_symmetry_clause_count": solver_reported_clause_count,
        "transcript_complete_and_audited": transcript_complete_and_audited,
        "candidate": candidate,
        "certified_construction": certified,
    }
    write_json(result_path, result)
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
