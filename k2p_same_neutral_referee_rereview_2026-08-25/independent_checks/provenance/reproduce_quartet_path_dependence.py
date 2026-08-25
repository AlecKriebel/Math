#!/usr/bin/env python3
"""Summarize and directly expose quartet mutation report path dependence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path


INPUTS = (
    "work/quartet_separation_closure/PROOF.md",
    "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json",
    "work/quartet_separation_closure/test_quartet_semantics_mutations.py",
    "work/quartet_separation_closure/verify_quartet_logic.py",
    "proof_compression_submission/article/main.tex",
    "work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md",
    "work/global_theorem_closure/GLOBAL_PROOF.md",
    "work/adversarial_proof_review/TOPOLOGY_DIRECTIONAL_THEOREM.md",
)
CERTIFICATE = "work/quartet_separation_closure/quartet_semantics_mutation_certificate.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_time(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    result: dict[str, object] = {"raw_sha256": sha(text.encode())}
    for key, pattern in (
        ("real_seconds", r"\s*([0-9.]+) real"),
        ("user_seconds", r"\s*([0-9.]+) user"),
        ("system_seconds", r"\s*([0-9.]+) sys"),
        ("maximum_resident_set_size_bytes", r"\s*([0-9]+)\s+maximum resident set size"),
        ("peak_memory_footprint_bytes", r"\s*([0-9]+)\s+peak memory footprint"),
    ):
        match = re.search(pattern, text)
        if match:
            result[key] = float(match.group(1)) if "." in match.group(1) else int(match.group(1))
    return result


def direct_trace(interpreter: Path, project: Path, log: Path) -> dict[str, object]:
    spec_path = project / "work/quartet_separation_closure/QUARTET_SEMANTICS_SPEC.json"
    verifier = project / "work/quartet_separation_closure/verify_quartet_logic.py"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec["edge_spectrum"].update({"G": "s", "T": "g"})
    repro = project / "_path_reproducer"
    repro.mkdir(exist_ok=True)
    mutation = repro / "spectrum_G_T_swap.json"
    output = repro / "should_not_exist.json"
    mutation.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if output.exists():
        output.unlink()
    command = [
        str(interpreter),
        "-B",
        str(verifier),
        "--project",
        str(project),
        "--spec",
        str(mutation),
        "--output",
        str(output),
        "--skip-document-binding",
    ]
    completed = subprocess.run(
        command,
        cwd=project,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    log.write_bytes(completed.stdout)
    normalized = completed.stdout.replace(str(project).encode(), b"<PROJECT>")
    return {
        "command": command,
        "cwd": str(project),
        "returncode": completed.returncode,
        "expected_marker_present": b"EQUAL_SECTOR_SPECTRUM_FAIL" in completed.stdout,
        "failed_mutation_output_exists": output.exists(),
        "stdout_sha256": sha(completed.stdout),
        "stdout_normalized_project_path_sha256": sha(normalized),
        "stdout_contains_absolute_project_path": str(project).encode() in completed.stdout,
        "stdout_log": str(log),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--interpreter", type=Path, required=True)
    parser.add_argument("--project", type=Path, action="append", required=True)
    parser.add_argument("--log-dir", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    if len(args.project) != 2:
        raise SystemExit("exactly two --project arguments required")
    projects = [path.resolve() for path in args.project]
    # Keep the venv entry point rather than resolving its symlink to the base
    # interpreter; resolving it would discard the virtual-environment context.
    interpreter = args.interpreter.absolute()
    args.log_dir.mkdir(parents=True, exist_ok=True)

    input_rows = []
    all_equal = True
    for relative in INPUTS:
        hashes = [sha((project / relative).read_bytes()) for project in projects]
        all_equal &= hashes[0] == hashes[1]
        input_rows.append({"path": relative, "sha256": hashes[0], "identical": hashes[0] == hashes[1]})

    reports = [json.loads((project / CERTIFICATE).read_text(encoding="utf-8")) for project in projects]
    report_hashes = [sha((project / CERTIFICATE).read_bytes()) for project in projects]
    with zipfile.ZipFile(args.archive) as archive:
        sealed = archive.read("k2p_principal_d_plus_submission_referee/" + CERTIFICATE)
    differing_cases = [
        {
            "case": left["case"],
            "first_stdout_sha256": left["stdout_sha256"],
            "second_stdout_sha256": right["stdout_sha256"],
        }
        for left, right in zip(reports[0]["cases"], reports[1]["cases"])
        if left["stdout_sha256"] != right["stdout_sha256"]
    ]

    traces = [
        direct_trace(interpreter, project, args.log_dir / f"quartet_direct_trace_{index + 1}.stdout")
        for index, project in enumerate(projects)
    ]
    normalized_equal = (
        traces[0]["stdout_normalized_project_path_sha256"]
        == traces[1]["stdout_normalized_project_path_sha256"]
    )
    passes = (
        all_equal
        and report_hashes[0] != report_hashes[1]
        and all(value != sha(sealed) for value in report_hashes)
        and len(differing_cases) == 7
        and all(trace["returncode"] != 0 for trace in traces)
        and all(trace["expected_marker_present"] for trace in traces)
        and all(not trace["failed_mutation_output_exists"] for trace in traces)
        and all(trace["stdout_contains_absolute_project_path"] for trace in traces)
        and traces[0]["stdout_sha256"] != traces[1]["stdout_sha256"]
        and normalized_equal
    )
    result = {
        "schema": "independent-quartet-mutation-path-dependence-reproducer-v1",
        "status": "REPRODUCED" if passes else "FAILED_TO_REPRODUCE",
        "interpreter": str(interpreter),
        "projects": [str(path) for path in projects],
        "identical_input_files": input_rows,
        "all_input_bytes_identical": all_equal,
        "sealed_certificate_sha256": sha(sealed),
        "regenerated_certificate_sha256": report_hashes,
        "regenerated_payload_sha256": [report["payload_sha256"] for report in reports],
        "differing_case_count": len(differing_cases),
        "differing_cases": differing_cases,
        "stable_case_names": [
            left["case"]
            for left, right in zip(reports[0]["cases"], reports[1]["cases"])
            if left["stdout_sha256"] == right["stdout_sha256"]
        ],
        "direct_traces": traces,
        "direct_trace_equal_after_project_path_normalization": normalized_equal,
        "prior_suite_runs": [
            {
                "project": str(projects[0]),
                "exit_status": 0,
                "stdout_sha256": sha((args.log_dir / "quartet_path_alpha.stdout").read_bytes()),
                "time": parse_time(args.log_dir / "quartet_path_alpha.time"),
            },
            {
                "project": str(projects[1]),
                "exit_status": 0,
                "stdout_sha256": sha((args.log_dir / "quartet_path_beta.stdout").read_bytes()),
                "time": parse_time(args.log_dir / "quartet_path_beta.time"),
            },
        ],
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "differing_case_count": len(differing_cases), "normalized_equal": normalized_equal}, sort_keys=True))
    return 0 if passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
