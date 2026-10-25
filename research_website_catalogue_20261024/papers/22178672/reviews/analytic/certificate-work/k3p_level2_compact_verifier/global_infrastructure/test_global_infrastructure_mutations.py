#!/usr/bin/env python3
"""Adversarial mutations for the independent K3P infrastructure verifier."""

from __future__ import annotations

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "global_infrastructure" / "verify_global_infrastructure.py"
FILES = [
    "bridge_fibre/K3P_BRIDGE_FIBRE_CERTIFICATE.json",
    "marginals/K3P_MARGINAL_SUBMERSION_CERTIFICATE.json",
    "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json",
    "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
    "global_infrastructure/GLOBAL_INFRASTRUCTURE_MANIFEST.json",
]


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def payload_hash(value: dict) -> str:
    body = dict(value)
    body.pop("payload_sha256", None)
    return sha256(canonical(body)).hexdigest()


def file_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def rebind(bundle: Path, relative: str, value: dict) -> None:
    value["payload_sha256"] = payload_hash(value)
    path = bundle / relative
    write(path, value)
    manifest_path = bundle / "global_infrastructure" / "GLOBAL_INFRASTRUCTURE_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["artifacts"][relative]["sha256"] = file_hash(path)
    manifest["artifacts"][relative]["payload_sha256"] = value["payload_sha256"]
    manifest["artifacts"][relative]["schema"] = value["schema"]
    manifest["payload_sha256"] = payload_hash(manifest)
    write(manifest_path, manifest)


def clone() -> tuple[tempfile.TemporaryDirectory, Path]:
    temporary = tempfile.TemporaryDirectory(prefix="k3p-global-mutation-")
    bundle = Path(temporary.name)
    for relative in FILES:
        target = bundle / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    return temporary, bundle


def run(bundle: Path, optimized: bool = False) -> subprocess.CompletedProcess[str]:
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command += [str(VERIFIER), "--project-root", str(ROOT), "--certificate-root", str(bundle)]
    return subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def mutation_case(name: str, relative: str, mutate, expected: str) -> dict:
    temporary, bundle = clone()
    try:
        path = bundle / relative
        value = json.loads(path.read_text())
        mutate(value)
        rebind(bundle, relative, value)
        result = run(bundle)
        combined = result.stdout + result.stderr
        passed = result.returncode != 0 and expected in combined
        return {
            "name": name,
            "status": "REJECTED" if passed else "SURVIVED",
            "exit_code": result.returncode,
            "expected_diagnostic": expected,
            "diagnostic_observed": expected in combined,
        }
    finally:
        temporary.cleanup()


def main() -> int:
    if not __debug__:
        print("optimized mode forbidden", file=sys.stderr)
        return 2
    cases = []
    cases.append(mutation_case(
        "impose_K2P_sector_equality_C_equals_T",
        "bridge_fibre/K3P_BRIDGE_FIBRE_CERTIFICATE.json",
        lambda x: x["incidence_action"].__setitem__("independent_nonzero_sectors", ["C", "G"]),
        "K2P sector equality introduced",
    ))
    cases.append(mutation_case(
        "permute_C_and_T_without_coordinate_transport",
        "bridge_fibre/K3P_BRIDGE_FIBRE_CERTIFICATE.json",
        lambda x: x.__setitem__("character_labels", ["0", "T", "G", "C"]),
        "bridge character labels",
    ))
    cases.append(mutation_case(
        "delete_principal_transition_inequality",
        "bridge_fibre/K3P_BRIDGE_FIBRE_CERTIFICATE.json",
        lambda x: x["physical_local_product"]["principal_domain_inequalities"].remove("1-c-g+t>0"),
        "missing or changed D3+ inequality",
    ))
    cases.append(mutation_case(
        "delete_continuous_time_inequality",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["simultaneous_physical_bridge_gluing"]["continuous_time_inequalities"].remove("t-c*g>0"),
        "global missing CT inequality",
    ))
    cases.append(mutation_case(
        "restore_old_uncapped_bridge_formula",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["simultaneous_physical_bridge_gluing"].update({
            "epsilon_formula": "epsilon=L^2/(4*U)",
            "base_common_effective_isotropic_spectrum": ["L^2/(4*U)"] * 3,
        }),
        "gluing capped epsilon formula",
    ))
    cases.append(mutation_case(
        "replace_total_rank_drop_by_one_selected_minor",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["genericity"].__setitem__(
            "total_source_rank_drop_locus",
            "zero locus of one selected Jacobian minor",
        ),
        "genericity total rank-drop locus",
    ))
    cases.append(mutation_case(
        "promote_triangle_to_ambient_rank_15",
        "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json",
        lambda x: x["orientations"]["1"].__setitem__("rank", 15),
        "H14 rank orientation 1",
    ))
    cases.append(mutation_case(
        "claim_ambient_open_triangle_germ",
        "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json",
        lambda x: x.__setitem__("ambient_open_triangle_germ", True),
        "ambient-open triangle claim",
    ))
    cases.append(mutation_case(
        "use_orientation_specific_context_contraction",
        "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json",
        lambda x: x["orientations"]["2"].__setitem__("context_contraction_id", "wrong-orientation-specific-context"),
        "context id orientation 2",
    ))
    cases.append(mutation_case(
        "collapse_contextual_relative_rank_into_ambient_rank",
        "triangle_h14/K3P_H14_CONTEXT_CERTIFICATE.json",
        lambda x: x["common_relative_germ"].__setitem__("rank_in_ambient_A15", 15),
        "relative contextual rank",
    ))

    # A coherently formed x^3-y^3 coefficient is a binomial with disjoint
    # supports, but its exponent-difference vector has content three.  Exercise
    # the exact helper directly so this hardening cannot pass merely because a
    # different H14 pullback check happens to fail first.
    spec = importlib.util.spec_from_file_location(
        "k3p_global_verifier_primitive_binomial_mutation", VERIFIER
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        module.require_primitive_exponent_difference(("x", "x", "x"),
                                                     ("y", "y", "y"))
    except module.VerificationError as error:
        diagnostic = str(error)
        cases.append({
            "name": "replace_primitive_coefficient_by_x3_minus_y3",
            "status": "REJECTED" if "binomial exponent difference" in diagnostic else "SURVIVED",
            "exit_code": 1,
            "expected_diagnostic": "binomial exponent difference",
            "diagnostic_observed": "binomial exponent difference" in diagnostic,
        })
    else:
        cases.append({
            "name": "replace_primitive_coefficient_by_x3_minus_y3",
            "status": "SURVIVED",
            "exit_code": 0,
            "expected_diagnostic": "binomial exponent difference",
            "diagnostic_observed": False,
        })
    cases.append(mutation_case(
        "restore_obsolete_universal_pointwise_cut_interface",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["dependencies"].__setitem__(
            "pointwise_cut_interface",
            x["dependencies"].pop("strong_class_containment_cut_equality_interface"),
        ),
        "global dependency interface set",
    ))
    cases.append(mutation_case(
        "substitute_universal_pointwise_claim_for_directional_theorem",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["dependencies"]["strong_class_containment_cut_equality_interface"].__setitem__(
            "required_claim", "rank Flat<=4 iff bridge split at every strict K3P point"
        ),
        "directional strong-class cut claim",
    ))
    cases.append(mutation_case(
        "mark_withdrawn_universal_pointwise_theorem_used",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["dependencies"]["strong_class_containment_cut_equality_interface"].__setitem__(
            "universal_pointwise_K3P_cut_recovery_used", True
        ),
        "universal pointwise theorem used",
    ))
    cases.append(mutation_case(
        "assume_common_bridge_tree_inside_cut_transfer",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["dependencies"]["strong_class_containment_cut_equality_interface"]["noncircularity"].__setitem__(
            "common_bridge_tree_assumed", True
        ),
        "cut-transfer interface circularity",
    ))
    cases.append(mutation_case(
        "corrupt_cut_transfer_theorem_manifest_hash",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["dependencies"]["strong_class_containment_cut_equality_interface"]["theorem_manifest"].__setitem__(
            "sha256", "0" * 64
        ),
        "cut-transfer theorem manifest hash",
    ))
    cases.append(mutation_case(
        "promote_generic_noncut_recovery_to_universal_pointwise",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["dependencies"]["generic_cut_rank_recovery"].__setitem__(
            "universal_pointwise_K3P_cut_recovery_claimed", True
        ),
        "generic cut-rank claim boundary",
    ))
    cases.append(mutation_case(
        "restore_pointwise_cut_node_in_dependency_DAG",
        "global_infrastructure/K3P_GLOBAL_GLUE_AND_RECONSTRUCTION_CERTIFICATE.json",
        lambda x: x["logical_dependency_dag"].__setitem__(
            "bridge_tree_recovery", ["pointwise_cut_interface"]
        ),
        "corrected cut transfer missing from reconstruction DAG",
    ))

    temporary, bundle = clone()
    try:
        optimized = run(bundle, optimized=True)
        text = optimized.stdout + optimized.stderr
        cases.append({
            "name": "optimized_assert_bypass",
            "status": "REJECTED" if optimized.returncode != 0 and "optimized mode is forbidden" in text else "SURVIVED",
            "exit_code": optimized.returncode,
            "expected_diagnostic": "optimized mode is forbidden",
            "diagnostic_observed": "optimized mode is forbidden" in text,
        })
    finally:
        temporary.cleanup()

    report = {
        "schema": "k3p-global-infrastructure-mutation-certificate-v1",
        "mutations": cases,
        "rejected": sum(case["status"] == "REJECTED" for case in cases),
        "survived": sum(case["status"] == "SURVIVED" for case in cases),
    }
    report["status"] = "PASS" if report["survived"] == 0 else "FAIL"
    report["payload_sha256"] = payload_hash(report)
    output = ROOT / "global_infrastructure" / "MUTATION_CERTIFICATE.json"
    write(output, report)
    print(json.dumps(report, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
