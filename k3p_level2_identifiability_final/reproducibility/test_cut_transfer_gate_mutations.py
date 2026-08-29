#!/usr/bin/env python3
"""Targeted semantic mutations for the active strong-class cut-transfer gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "reproducibility" / "strong_cut_transfer_gate.py"
TRANSFER_RELATIVE = Path("cut_recovery/strong_crossbridge/global_transfer")
THEOREM_RELATIVE = TRANSFER_RELATIVE / "THEOREM_MANIFEST.json"
OUTPUT = ROOT / "reproducibility" / "CUT_TRANSFER_GATE_MUTATION_REPORT.json"


def clone_project() -> tuple[tempfile.TemporaryDirectory, Path]:
    temporary = tempfile.TemporaryDirectory(prefix="k3p-cut-transfer-gate-")
    project = Path(temporary.name) / "project"
    source_transfer = ROOT / TRANSFER_RELATIVE
    shutil.copytree(source_transfer, project / TRANSFER_RELATIVE)
    theorem = json.loads((ROOT / THEOREM_RELATIVE).read_text())
    for record in theorem["load_bearing_inputs"].values():
        relative = Path(record["path"])
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return temporary, project


def run(
    project: Path,
    optimized: bool = False,
    gate: Path = GATE,
) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(gate),
        "--project-root", str(project),
        "--transfer-root", str(project / TRANSFER_RELATIVE),
        "--no-write-report",
    ])
    return subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def clean_case(name: str, optimized: bool) -> dict:
    temporary, project = clone_project()
    try:
        result = run(project, optimized=optimized)
        sentinel = "STRONG_CLASS_CUT_TRANSFER_GATE_PASS"
        passed = result.returncode == 0 and sentinel in result.stdout
        return {
            "name": name,
            "result": "PASS" if passed else "FAIL",
            "exit_code": result.returncode,
            "sentinel_seen": sentinel in result.stdout,
        }
    finally:
        temporary.cleanup()


def mutation_case(name: str, mutate, expected: str, optimized: bool = False) -> dict:
    temporary, project = clone_project()
    try:
        theorem_path = project / THEOREM_RELATIVE
        theorem = json.loads(theorem_path.read_text())
        mutate(theorem)
        theorem_path.write_text(json.dumps(theorem, indent=2, sort_keys=True) + "\n")
        result = run(project, optimized=optimized)
        rejected = result.returncode != 0 and expected in result.stdout
        return {
            "name": name,
            "result": "REJECTED" if rejected else "SURVIVED",
            "exit_code": result.returncode,
            "expected_diagnostic": expected,
            "diagnostic_seen": expected in result.stdout,
            "optimized_gate": optimized,
        }
    finally:
        temporary.cleanup()


def canonical_payload_sha256(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def coherent_legacy_provenance_case() -> dict:
    """Reseal every affected hash after admitting the retired legacy premise."""
    temporary, project = clone_project()
    try:
        evidence_relative = TRANSFER_RELATIVE / "K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"
        evidence_path = project / evidence_relative
        evidence = json.loads(evidence_path.read_text())
        evidence["provenance_policy"][
            "legacy_global_logic_report_is_load_bearing"
        ] = True
        evidence["payload_sha256"] = canonical_payload_sha256(evidence)
        evidence_path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")

        theorem_path = project / THEOREM_RELATIVE
        theorem = json.loads(theorem_path.read_text())
        evidence_sha = file_sha256(evidence_path)
        theorem["load_bearing_inputs"]["k3p_directed_cut_inclusion_evidence"][
            "sha256"
        ] = evidence_sha
        theorem["files"]["K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json"] = evidence_sha
        theorem_path.write_text(json.dumps(theorem, indent=2, sort_keys=True) + "\n")

        copied_gate = project / "reproducibility" / "strong_cut_transfer_gate.py"
        copied_gate.parent.mkdir(parents=True, exist_ok=True)
        source = GATE.read_text()
        replacement = f'EXPECTED_THEOREM_SHA256 = "{file_sha256(theorem_path)}"'
        source, substitutions = re.subn(
            r'^EXPECTED_THEOREM_SHA256\s*=.*$', replacement, source,
            count=1, flags=re.MULTILINE,
        )
        if substitutions != 1:
            raise RuntimeError("could not reseal copied gate")
        copied_gate.write_text(source)

        result = run(project, gate=copied_gate)
        expected = "active K3P cut-inclusion evidence provenance"
        rejected = result.returncode != 0 and expected in result.stdout
        return {
            "name": "coherently_reseal_legacy_global_logic_provenance",
            "result": "REJECTED" if rejected else "SURVIVED",
            "exit_code": result.returncode,
            "expected_diagnostic": expected,
            "diagnostic_seen": expected in result.stdout,
            "optimized_gate": False,
            "all_affected_hashes_resealed": True,
        }
    finally:
        temporary.cleanup()


def main() -> int:
    cases = [
        coherent_legacy_provenance_case(),
        mutation_case(
            "substitute_universal_pointwise_iff_for_directional_theorem",
            lambda x: x.__setitem__(
                "certified_claim",
                "For every strict K3P tensor, rank Flat<=4 iff the split is a bridge.",
            ),
            "universal pointwise recovery substituted",
        ),
        mutation_case(
            "promote_withdrawn_universal_pointwise_claim",
            lambda x: x["independent_adversarial_audit"]["claim_boundary"].__setitem__(
                "universal_pointwise_K3P_cut_recovery", "PROVED"
            ),
            "withdrawn universal pointwise claim boundary",
        ),
        mutation_case(
            "replace_strong_class_scope_by_universal_scope",
            lambda x: x["independent_adversarial_audit"]["claim_boundary"].__setitem__(
                "conclusion", "universal_pointwise_cut_rank_equivalence"
            ),
            "withdrawn universal pointwise claim boundary",
            optimized=True,
        ),
        mutation_case(
            "assume_bridge_tree_equality_circularly",
            lambda x: x["noncircularity"].__setitem__("bridge_tree_equality_assumed", True),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "assume_common_bridge_tree_circularly",
            lambda x: x["noncircularity"].__setitem__("common_bridge_tree_assumed", True),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "import_fourteen_orbit_before_localization",
            lambda x: x["noncircularity"].__setitem__("fourteen_orbit_classification_imported", True),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "assume_target_regular_point",
            lambda x: x["noncircularity"].__setitem__("target_regular_point_assumed", True),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "replace_proved_directed_inclusion_by_cut_equality",
            lambda x: x["noncircularity"].__setitem__(
                "directed_cut_inclusion_proved_here", "Cut(Nprime)=Cut(N)"
            ),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "claim_legacy_global_logic_is_active",
            lambda x: x["noncircularity"].__setitem__(
                "legacy_global_logic_report_used", True
            ),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "claim_jc_cut_theorem_is_active",
            lambda x: x["noncircularity"].__setitem__(
                "jc_model_cut_theorem_used", True
            ),
            "cut-transfer noncircularity contract",
        ),
        mutation_case(
            "drop_load_bearing_204_universe",
            lambda x: x["load_bearing_inputs"].pop("pointwise_204_universe"),
            "cut-transfer load-bearing input set",
        ),
        mutation_case(
            "drop_load_bearing_k3p_cut_evidence",
            lambda x: x["load_bearing_inputs"].pop(
                "k3p_directed_cut_inclusion_evidence"
            ),
            "cut-transfer load-bearing input set",
        ),
        mutation_case(
            "drop_producer_verifier_from_theorem_file_set",
            lambda x: x["files"].pop("verify_global_transfer.py"),
            "cut-transfer theorem file set",
        ),
        mutation_case(
            "add_unrecognized_field_to_sealed_theorem",
            lambda x: x.__setitem__("unrecognized_claim_extension", True),
            "sealed cut-transfer theorem manifest hash",
        ),
        mutation_case(
            "redirect_load_bearing_input_outside_locked_path",
            lambda x: x["load_bearing_inputs"]["selected_marginal"].__setitem__(
                "path", "cut_recovery/verification_report.json"
            ),
            "bound path",
        ),
    ]
    clean = [
        clean_case("clean_ordinary_gate", optimized=False),
        clean_case("clean_optimized_gate", optimized=True),
    ]
    rejected = sum(case["result"] == "REJECTED" for case in cases)
    report = {
        "schema": "k3p-strong-class-cut-transfer-gate-mutations-v2",
        "status": "PASS" if rejected == len(cases) and all(
            case["result"] == "PASS" for case in clean
        ) else "FAIL",
        "claim_boundary_tested": {
            "strong_class_directional_cut_equality": "ACTIVE",
            "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
        },
        "clean_replays": clean,
        "mutations": cases,
        "mutation_count": len(cases),
        "rejected_count": rejected,
        "survived_count": len(cases) - rejected,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if report["status"] == "PASS":
        print("STRONG_CLASS_CUT_TRANSFER_GATE_MUTATIONS_PASS")
    print(json.dumps({
        "status": report["status"],
        "clean_replays": len(clean),
        "mutations": len(cases),
        "rejected": rejected,
    }, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
