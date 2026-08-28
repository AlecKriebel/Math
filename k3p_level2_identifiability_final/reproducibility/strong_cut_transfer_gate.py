#!/usr/bin/env python3
"""Fail-closed active gate for the strong-class K3P cut-transfer theorem.

This verifier does not import either global-transfer implementation.  It
invokes the sealed release verifier in ordinary and optimized Python, checks
the theorem manifest and every bound file, and enforces the corrected claim
boundary.  In particular, it rejects substitution of the withdrawn universal
pointwise cut-rank equivalence for the directional strong-class theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
DEFAULT_PROJECT = HERE.parent
TRANSFER_RELATIVE = Path("cut_recovery/strong_crossbridge/global_transfer")
DEFAULT_REPORT = HERE / "strong_class_cut_transfer_gate_report.json"
EXPECTED_THEOREM_SHA256 = "b5163a9840e7ceaa0bdbe9a5730b6a65109fcedc28ac8e39e1af81083c25c77a"

EXPECTED_CLAIM = (
    "For binary standard semi-directed strongly tree-child level-2 networks "
    "under source-relative regular full-dimensional containment on strict D3,+, "
    "Cut(N)=Cut(Nprime)."
)
EXPECTED_CLAIM_BOUNDARY = {
    "conclusion": "Cut(N)=Cut(Nprime)_under_source_relative_containment_in_the_strong_class",
    "strong_class_cut_transfer": "PROVED",
    "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
}
EXPECTED_NONCIRCULARITY = {
    "bridge_tree_equality_assumed": False,
    "common_bridge_tree_assumed": False,
    "fourteen_orbit_classification_imported": False,
    "only_preexisting_cut_direction_used": "Cut(Nprime) subset Cut(N)",
    "reverse_direction_proved_here": "Cut(N) subset Cut(Nprime)",
    "target_open_marginal_assumed": False,
    "target_regular_point_assumed": False,
}
EXPECTED_THEOREM_FILES = {
    "GLOBAL_TRANSFER_AUDIT.md",
    "GLOBAL_TRANSFER_CERTIFICATE.json",
    "GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json",
    "OPTIMIZED_VERIFICATION_REPORT.json",
    "README.md",
    "RELEASE_OPTIMIZED_VERIFICATION_REPORT.json",
    "RELEASE_VERIFICATION_REPORT.json",
    "VERIFICATION_REPORT.json",
    "WORK_LOG.md",
    "adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
    "adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.md",
    "adversarial/MANIFEST.sha256",
    "adversarial/MUTATION_RESULTS.json",
    "adversarial/VERIFICATION_REPORT.json",
    "adversarial/WORK_LOG.md",
    "adversarial/test_global_transfer_adversarial_mutations.py",
    "adversarial/verify_global_transfer_adversarial.py",
    "build_global_transfer.py",
    "build_manifest.py",
    "verify_global_transfer.py",
    "verify_release.py",
}
EXPECTED_LOAD_BEARING_PATHS = {
    "directed_cut_inclusion_audit": "cut_recovery/global_logic/CUT_GLOBAL_LOGIC_REPORT.json",
    "frozen_strong_topology": "cut_recovery/upstream_frozen/corrected_jc_cut_certificate.json",
    "pointwise_204_adversarial_mutations": "cut_recovery/strong_crossbridge/final_certificate/ADVERSARIAL_MUTATION_REPORT.json",
    "pointwise_204_certificate": "cut_recovery/strong_crossbridge/final_certificate/STRONG_CROSSBRIDGE_FINAL_CERTIFICATE.json",
    "pointwise_204_independent_verification": "cut_recovery/strong_crossbridge/final_certificate/VERIFICATION_REPORT.json",
    "pointwise_204_universe": "cut_recovery/strong_crossbridge/final_certificate/UNIVERSE_CERTIFICATE.json",
    "recompiled_direction_universe": "cut_recovery/strong_crossbridge/global_transfer/GLOBAL_TRANSFER_DIRECTION_UNIVERSE.json",
    "selected_marginal": "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json",
}
EXPECTED_AUDIT_PATHS = {
    "audit": "cut_recovery/strong_crossbridge/global_transfer/adversarial/ADVERSARIAL_GLOBAL_TRANSFER_AUDIT.json",
    "manifest": "cut_recovery/strong_crossbridge/global_transfer/adversarial/MANIFEST.sha256",
    "mutation_report": "cut_recovery/strong_crossbridge/global_transfer/adversarial/MUTATION_RESULTS.json",
    "verification_report": "cut_recovery/strong_crossbridge/global_transfer/adversarial/VERIFICATION_REPORT.json",
    "release_verifier": "cut_recovery/strong_crossbridge/global_transfer/verify_release.py",
    "release_report": "cut_recovery/strong_crossbridge/global_transfer/RELEASE_VERIFICATION_REPORT.json",
    "release_optimized_report": "cut_recovery/strong_crossbridge/global_transfer/RELEASE_OPTIMIZED_VERIFICATION_REPORT.json",
}


class GateError(RuntimeError):
    pass


def require(condition: bool, label: object) -> None:
    if not condition:
        raise GateError(str(label))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict:
    require(path.is_file(), ("missing JSON", str(path)))
    value = json.loads(path.read_text())
    require(isinstance(value, dict), ("JSON object required", str(path)))
    return value


def project_binding(project: Path, record: dict, expected_path: str | None = None) -> dict:
    require(set(record) == {"path", "sha256"}, ("malformed binding", record))
    if expected_path is not None:
        require(record["path"] == expected_path, ("bound path", expected_path))
    path = (project / record["path"]).resolve()
    try:
        path.relative_to(project.resolve())
    except ValueError as error:
        raise GateError(("bound path resolves outside project", record["path"])) from error
    require(path.is_file(), ("missing bound file", record["path"]))
    require(sha256(path) == record["sha256"], ("bound file hash", record["path"]))
    return {"path": record["path"], "sha256": record["sha256"]}


def parse_summary(stdout: str) -> dict:
    for line in reversed(stdout.splitlines()):
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    raise GateError("release verifier emitted no JSON summary")


def invoke_release(transfer: Path, optimized: bool) -> dict:
    verifier = transfer / "verify_release.py"
    require(verifier.is_file(), "release verifier is absent")
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(verifier), "--no-write-report"])
    result = subprocess.run(
        command,
        cwd=transfer,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    summary = parse_summary(result.stdout)
    expected = {
        "status": "PASS",
        "directions": 204,
        "tree_colorings": 19270,
        "adversarial_mutations": 32,
        "python_optimized": optimized,
    }
    require(result.returncode == 0, ("release verifier exit", optimized, result.stdout))
    require(summary == expected, ("release verifier summary", optimized, summary))
    return {
        "mode": "optimized" if optimized else "ordinary",
        "exit_code": result.returncode,
        "summary": summary,
        "transcript": result.stdout,
    }


def validate_release_report(path: Path, optimized: bool, release_sha: str) -> dict:
    report = load(path)
    require(
        report.get("schema") == "k3p-lost-bridge-global-transfer-release-verification-v1",
        ("release report schema", path.name),
    )
    require(report.get("status") == "PASS" and report.get("remaining_gaps") == [],
            ("release report status", path.name))
    require(report.get("python_optimized") is optimized, ("release report mode", path.name))
    require(report.get("release_verifier_sha256") == release_sha,
            ("release verifier binding", path.name))
    require(report.get("circular_hash_dependency") is False,
            ("circular hash dependency", path.name))
    require(report.get("producer_imported") is False,
            ("producer imported into release gate", path.name))
    require(report.get("adversarial_verifier_imported") is False,
            ("adversarial verifier imported into release gate", path.name))
    require(report.get("producer") == {
        "direction_count": 204,
        "mutation_count": 30,
        "proof_step_count": 14,
        "two_terminal_mixture_components_checked": 7,
    }, ("producer release summary", path.name))
    require(report.get("adversarial") == {
        "direction_count": 204,
        "manifest_rows_checked": 7,
        "mutation_count": 32,
        "side_blob_switching_components": 7,
        "tree_colorings_checked": 19270,
        "tree_counterexamples": 0,
    }, ("adversarial release summary", path.name))
    return report


def verify_gate(project: Path, transfer: Path) -> dict:
    project = project.resolve()
    transfer = transfer.resolve()
    require(transfer.is_dir(), "global-transfer package is absent")
    try:
        transfer.relative_to(project)
    except ValueError as error:
        raise GateError("global-transfer package resolves outside the project root") from error

    theorem_path = transfer / "THEOREM_MANIFEST.json"
    theorem = load(theorem_path)
    release_path = transfer / "verify_release.py"
    release_sha = sha256(release_path)

    require(theorem.get("schema") == "k3p-lost-bridge-global-transfer-theorem-manifest-v1",
            "cut-transfer theorem manifest schema")
    require(theorem.get("status") == "PASS", "cut-transfer theorem manifest status")
    require(theorem.get("certified_claim") == EXPECTED_CLAIM,
            "universal pointwise recovery substituted for directional strong-class theorem")
    require(theorem.get("independent_adversarial_audit", {}).get("claim_boundary") ==
            EXPECTED_CLAIM_BOUNDARY,
            "withdrawn universal pointwise claim boundary")
    require(theorem.get("noncircularity") == EXPECTED_NONCIRCULARITY,
            "cut-transfer noncircularity contract")
    require(theorem.get("independent_adversarial_audit", {}).get("status") == "PASS",
            "independent cut-transfer audit status")
    require(theorem.get("independent_adversarial_audit", {}).get("remaining_gaps") == [],
            "independent cut-transfer audit gaps")

    files = theorem.get("files", {})
    require(set(files) == EXPECTED_THEOREM_FILES, "cut-transfer theorem file set")
    for relative, expected in sorted(files.items()):
        path = transfer / relative
        require(path.is_file() and sha256(path) == expected,
                ("cut-transfer theorem file hash", relative))

    load_bearing = theorem.get("load_bearing_inputs", {})
    require(set(load_bearing) == set(EXPECTED_LOAD_BEARING_PATHS),
            "cut-transfer load-bearing input set")
    for name, record in sorted(load_bearing.items()):
        project_binding(project, record, EXPECTED_LOAD_BEARING_PATHS[name])

    audit = theorem["independent_adversarial_audit"]
    project_binding(project, audit["audit"], EXPECTED_AUDIT_PATHS["audit"])
    project_binding(project, audit["manifest"], EXPECTED_AUDIT_PATHS["manifest"])
    project_binding(project, audit["mutation_report"], EXPECTED_AUDIT_PATHS["mutation_report"])
    project_binding(project, audit["verification_report"], EXPECTED_AUDIT_PATHS["verification_report"])
    require(project_binding(
        project, audit["release_verifier"], EXPECTED_AUDIT_PATHS["release_verifier"]
    )["sha256"] == release_sha,
            "theorem release verifier binding")

    ordinary_path = transfer / "RELEASE_VERIFICATION_REPORT.json"
    optimized_path = transfer / "RELEASE_OPTIMIZED_VERIFICATION_REPORT.json"
    ordinary = validate_release_report(ordinary_path, False, release_sha)
    optimized = validate_release_report(optimized_path, True, release_sha)
    require(project_binding(
        project, audit["release_report"], EXPECTED_AUDIT_PATHS["release_report"]
    )["sha256"] == sha256(ordinary_path),
            "theorem ordinary release binding")
    require(project_binding(
        project, audit["release_optimized_report"], EXPECTED_AUDIT_PATHS["release_optimized_report"]
    )["sha256"] ==
            sha256(optimized_path), "theorem optimized release binding")

    validation = theorem.get("validation", {})
    require(validation.get("topology_directions_rebuilt") == 204,
            "cut-transfer direction coverage")
    require(validation.get("local_pointwise_targets_bound") == 204,
            "local pointwise handoff coverage")
    require(validation.get("proof_DAG_steps") == 14,
            "cut-transfer proof DAG")
    require(validation.get("ordinary_replay") == validation.get("optimized_replay") == "PASS",
            "producer ordinary/optimized replay")
    require(validation.get("release_ordinary_replay") ==
            validation.get("release_optimized_replay") == "PASS",
            "release ordinary/optimized replay")
    require(validation.get("adversarial_tree_counterexamples") == 0,
            "crossing-quartet topology counterexample")
    require(validation.get("global_transfer_mutations_rejected") == 30 and
            validation.get("adversarial_mutations_rejected") == 32,
            "cut-transfer mutation coverage")
    require(sha256(theorem_path) == EXPECTED_THEOREM_SHA256,
            "sealed cut-transfer theorem manifest hash")

    ordinary_replay = invoke_release(transfer, False)
    optimized_replay = invoke_release(transfer, True)
    return {
        "schema": "k3p-strong-class-cut-transfer-active-gate-v1",
        "status": "PASS",
        "certified_claim": EXPECTED_CLAIM,
        "claim_boundary": EXPECTED_CLAIM_BOUNDARY,
        "noncircularity": EXPECTED_NONCIRCULARITY,
        "universal_pointwise_K3P_cut_recovery_used": False,
        "theorem_manifest": {
            "path": str(theorem_path.relative_to(project)),
            "sha256": sha256(theorem_path),
        },
        "release_verifier": {
            "path": str(release_path.relative_to(project)),
            "sha256": release_sha,
        },
        "stored_release_reports": {
            "ordinary": {"path": str(ordinary_path.relative_to(project)), "sha256": sha256(ordinary_path)},
            "optimized": {"path": str(optimized_path.relative_to(project)), "sha256": sha256(optimized_path)},
        },
        "fresh_release_replays": {
            "ordinary": ordinary_replay,
            "optimized": optimized_replay,
        },
        "producer_summary": ordinary["producer"],
        "adversarial_summary": ordinary["adversarial"],
        "remaining_gaps": [],
    }


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(value, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=path.name + ".", delete=False
    ) as handle:
        handle.write(encoded)
        temporary = Path(handle.name)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, default=DEFAULT_PROJECT)
    parser.add_argument("--transfer-root", type=Path)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args()
    project = args.project_root.resolve()
    transfer = (args.transfer_root or (project / TRANSFER_RELATIVE)).resolve()
    try:
        report = verify_gate(project, transfer)
    except (GateError, KeyError, ValueError, TypeError, OSError, json.JSONDecodeError) as error:
        print(f"STRONG_CLASS_CUT_TRANSFER_GATE_FAIL: {error}", file=sys.stderr)
        return 1
    if not args.no_write_report:
        atomic_json(args.report, report)
    print("STRONG_CLASS_CUT_TRANSFER_GATE_PASS")
    print(json.dumps({
        "status": report["status"],
        "theorem_manifest_sha256": report["theorem_manifest"]["sha256"],
        "ordinary_release": report["fresh_release_replays"]["ordinary"]["summary"],
        "optimized_release": report["fresh_release_replays"]["optimized"]["summary"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
