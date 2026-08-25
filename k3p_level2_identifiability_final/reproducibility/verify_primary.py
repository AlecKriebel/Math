#!/usr/bin/env python3
"""Fail-closed orchestrator for the twenty-eight primary K3P proof gates."""

from __future__ import annotations

import hashlib
import json
import os
import platform
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback

from exact_four_port import verify_four_port
from exact_primary import (
    bridge_and_marginal_evidence,
    cherry_evidence,
    collision_evidence,
    model_domain_evidence,
    rooting_census_evidence,
    three_port_evidence,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.resolve()
FROZEN = (ROOT / "input_frozen" / "k3p_cloud_artifacts").resolve()


PRIMARY_ITEMS = {
    1: "K3P inverse-Fourier transition formulas",
    2: "Exact principal stochastic domain",
    3: "Exact continuous-time inequalities",
    4: "Strict isotropic near-identity subdivision",
    5: "Root-movement invariance",
    6: "Strong-class containment cut transfer",
    7: "Tree-ordinary-sunlet separation",
    8: "Rank-14 ordinary-triangle calculation",
    9: "Exact H14 quartic",
    10: "Smoothness of the common triangle point",
    11: "Rank 14 of all three triangle orientations",
    12: "Supplied rank-15 double-theta collision",
    13: "Exact rooting census",
    14: "Complete three-sector bridge action",
    15: "Analytic incidence-normalizer rank",
    16: "Physical local-product lifting",
    17: "Triple-sector marginal products and physical lifts",
    18: "All six four-port source ranks",
    19: "Fourteen-orbit lock",
    20: "All nine polynomial separators",
    21: "All five directed-rank separators",
    22: "Two pre-lock sink-swap quartics",
    23: "Exact 40=38+2 accounting",
    24: "Krawczyk sharpness certificate",
    25: "Rank 15 of both weak-class maps throughout the certified box",
    26: "Stochastic and continuous-time inequalities throughout the box",
    27: "All-n cherry determinant",
    28: "Rooting-class persistence under cherry substitution",
}


def inside_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
        return True
    except ValueError:
        return False


def atomic_json(path: Path, payload):
    assert inside_root(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=path.name + ".", delete=False
    ) as handle:
        handle.write(encoded)
        temporary = Path(handle.name)
    temporary.replace(path)


def sha256_file(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_input_lock():
    path = HERE / "primary_input_lock.json"
    lock = json.loads(path.read_text())
    mismatches = []
    observed = {}
    for relative, expected in sorted(lock["files"].items()):
        candidate = (ROOT / relative).resolve()
        if not inside_root(candidate):
            mismatches.append({"path": relative, "reason": "resolved outside project root"})
            continue
        if not candidate.is_file():
            mismatches.append({"path": relative, "expected_sha256": expected, "observed": "MISSING"})
            continue
        actual = sha256_file(candidate)
        observed[relative] = actual
        if actual != expected:
            mismatches.append({"path": relative, "expected_sha256": expected, "observed_sha256": actual})
    return {
        "schema": lock["schema"],
        "lock_file": str(path.relative_to(ROOT)),
        "lock_sha256": sha256_file(path),
        "file_count": len(lock["files"]),
        "observed_sha256": observed,
        "mismatches": mismatches,
        "status": "PASS" if not mismatches else "FAIL",
    }


def tree_snapshot(directory: Path):
    if not directory.is_dir():
        return {}
    return {
        str(path.relative_to(ROOT)): sha256_file(path)
        for path in sorted(directory.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts
    }


def run_checked_verifier(script: Path, sentinel: str, timeout=1800, preserve_tree=None):
    if not script.is_file():
        return {
            "status": "BLOCKED",
            "script": str(script.relative_to(ROOT)) if inside_root(script) else str(script),
            "gap": "verifier script is absent",
        }
    assert inside_root(script)
    started = time.monotonic()
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    before = tree_snapshot(preserve_tree) if preserve_tree else None
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    elapsed = time.monotonic() - started
    after = tree_snapshot(preserve_tree) if preserve_tree else None
    unchanged = before == after if preserve_tree else True
    return {
        "status": "PASS" if result.returncode == 0 and sentinel in result.stdout and unchanged else "FAIL",
        "script": str(script.relative_to(ROOT)),
        "script_sha256": sha256_file(script),
        "sentinel": sentinel,
        "sentinel_seen": sentinel in result.stdout,
        "exit_code": result.returncode,
        "elapsed_seconds": elapsed,
        "transcript": result.stdout,
        "required_tree_unchanged": str(preserve_tree.relative_to(ROOT)) if preserve_tree else None,
        "tree_unchanged": unchanged,
        "changed_tree_paths": sorted(set(before or {}) ^ set(after or {})) + sorted(
            path for path in set(before or {}) & set(after or {}) if before[path] != after[path]
        ),
    }


def corrected_transport_replay():
    audit_path = ROOT / "clean_room" / "H21_01_TRANSPORT_AUDIT.json"
    hardened_path = ROOT / "clean_room" / "adversarial" / "HARDENED_H21_REAUDIT.json"
    verifier_path = ROOT / "clean_room" / "verify_h21_transport_and_fourteen_orbits.py"
    if not audit_path.is_file() or not hardened_path.is_file():
        return {"status": "BLOCKED", "gap": "corrected transport audit or hardened adversarial re-audit is absent"}
    audit = json.loads(audit_path.read_text())
    hardened = json.loads(hardened_path.read_text())
    replay = run_checked_verifier(
        verifier_path,
        "CLEANROOM_K3P_H21_TRANSPORT_AND_FOURTEEN_ORBITS_PASS",
        preserve_tree=ROOT / "clean_room",
    )
    census = audit.get("census", {})
    verdict = hardened.get("verdict", {})
    required = (
        audit.get("schema") == "k3p-h21-fourteen-orbit-clean-room-audit-v2"
        and audit.get("status") == "PASS"
        and audit.get("exact_remaining_gaps_within_scope") == []
        and census.get("canonical_orbits") == 14
        and census.get("raw_orbit_members") == 38
        and census.get("prelock_sink_swaps") == 2
        and census.get("transported_h14_quartics") == 5
        and census.get("remaining_exact_quartics") == 4
        and census.get("directed_rank_obstructions") == 5
        and hardened.get("schema") == "k3p-hardened-h21-adversarial-reaudit-v1"
        and hardened.get("status") == "PASS_ZERO_REMAINING_HARDENING_GAPS"
        and hardened.get("exact_remaining_gaps") == []
        and verdict.get("H21_mathematical_transport") == "PASS"
        and verdict.get("target_rank_upper_bound_reconstruction") == "PASS_NONCIRCULAR"
        and verdict.get("certificate_skip_control") == "PASS_FAIL_CLOSED"
        and verdict.get("full_fourteen_orbit_and_two_sink_gate") == "PASS"
        and verdict.get("remaining_blockers") == 0
        and replay["status"] == "PASS"
    )
    expected_script_hash = hardened.get("audited_hashes", {}).get("final_hardened_verifier")
    required = required and expected_script_hash == replay.get("script_sha256")
    replay.update(
        {
            "status": "PASS" if required else "FAIL",
            "audit_file": str(audit_path.relative_to(ROOT)),
            "audit_sha256": sha256_file(audit_path),
            "hardened_reaudit_file": str(hardened_path.relative_to(ROOT)),
            "hardened_reaudit_sha256": sha256_file(hardened_path),
            "audit_exact_remaining_gaps": audit.get("exact_remaining_gaps_within_scope"),
            "full_replay": census,
            "hardened_verdict": verdict,
        }
    )
    return replay


def strong_class_cut_transfer_replay():
    """Invoke and bind the corrected directional cut-transfer release gate."""
    transfer = ROOT / "cut_recovery" / "strong_crossbridge" / "global_transfer"
    gate_script = HERE / "strong_cut_transfer_gate.py"
    gate_report_path = HERE / "strong_class_cut_transfer_gate_report.json"
    mutation_script = HERE / "test_cut_transfer_gate_mutations.py"
    mutation_report_path = HERE / "CUT_TRANSFER_GATE_MUTATION_REPORT.json"

    gate_replay = run_checked_verifier(
        gate_script,
        "STRONG_CLASS_CUT_TRANSFER_GATE_PASS",
        timeout=1800,
        preserve_tree=transfer,
    )
    mutation_replay = run_checked_verifier(
        mutation_script,
        "STRONG_CLASS_CUT_TRANSFER_GATE_MUTATIONS_PASS",
        timeout=1800,
        preserve_tree=transfer,
    )
    if not gate_report_path.is_file() or not mutation_report_path.is_file():
        return {
            "status": "FAIL",
            "gap": "active cut-transfer gate did not produce both bound reports",
            "gate_replay": gate_replay,
            "mutation_replay": mutation_replay,
        }

    gate = json.loads(gate_report_path.read_text())
    mutations = json.loads(mutation_report_path.read_text())
    expected_boundary = {
        "conclusion": "Cut(N)=Cut(Nprime)_under_source_relative_containment_in_the_strong_class",
        "strong_class_cut_transfer": "PROVED",
        "universal_pointwise_K3P_cut_recovery": "WITHDRAWN_NOT_USED",
    }
    required = (
        gate_replay["status"] == "PASS"
        and mutation_replay["status"] == "PASS"
        and gate.get("schema") == "k3p-strong-class-cut-transfer-active-gate-v1"
        and gate.get("status") == "PASS"
        and gate.get("claim_boundary") == expected_boundary
        and gate.get("universal_pointwise_K3P_cut_recovery_used") is False
        and gate.get("remaining_gaps") == []
        and gate.get("fresh_release_replays", {}).get("ordinary", {}).get("summary", {}).get("python_optimized") is False
        and gate.get("fresh_release_replays", {}).get("optimized", {}).get("summary", {}).get("python_optimized") is True
        and mutations.get("schema") == "k3p-strong-class-cut-transfer-gate-mutations-v1"
        and mutations.get("status") == "PASS"
        and mutations.get("mutation_count") == mutations.get("rejected_count") == 12
        and mutations.get("survived_count") == 0
        and len(mutations.get("clean_replays", [])) == 2
        and all(row.get("result") == "PASS" for row in mutations.get("clean_replays", []))
    )
    return {
        "schema": "k3p-primary-strong-class-cut-transfer-replay-v1",
        "status": "PASS" if required else "FAIL",
        "gap": None if required else "directional cut-transfer release or its claim-boundary mutations failed",
        "claim_boundary": gate.get("claim_boundary"),
        "universal_pointwise_K3P_cut_recovery_used": gate.get(
            "universal_pointwise_K3P_cut_recovery_used"
        ),
        "gate_report": {
            "path": str(gate_report_path.relative_to(ROOT)),
            "sha256": sha256_file(gate_report_path),
        },
        "mutation_report": {
            "path": str(mutation_report_path.relative_to(ROOT)),
            "sha256": sha256_file(mutation_report_path),
        },
        "theorem_manifest": gate.get("theorem_manifest"),
        "release_verifier": gate.get("release_verifier"),
        "stored_release_reports": gate.get("stored_release_reports"),
        "producer_summary": gate.get("producer_summary"),
        "adversarial_summary": gate.get("adversarial_summary"),
        "gate_replay": gate_replay,
        "mutation_replay": mutation_replay,
    }


def sharpness_replay():
    script = ROOT / "sharpness" / "independent_krawczyk_replay.py"
    certificate_path = ROOT / "sharpness" / "K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json"
    if not script.is_file():
        return {"status": "BLOCKED", "gap": "independent Krawczyk replay script has not landed"}
    replay = run_checked_verifier(
        script,
        "INDEPENDENT_K3P_KRAWCZYK_PASS",
        timeout=3600,
        preserve_tree=ROOT / "sharpness",
    )
    if not certificate_path.is_file():
        replay.update({"status": "FAIL", "gap": "replay did not produce its certificate"})
        return replay
    certificate = json.loads(certificate_path.read_text())
    conclusion = certificate.get("conclusion", {})
    required = {
        "all_checks_pass": True,
        "unique_common_parameter_root_in_box": True,
        "W_rank_15_throughout_box": True,
        "Wprime_rank_15_throughout_box": True,
        "principal_K3P_domain_throughout_box": True,
        "strict_continuous_time_throughout_box": True,
    }
    provenance = certificate.get("provenance", {})
    bound_verifier = provenance.get("independent_verifier", {})
    fields_ok = (
        all(conclusion.get(key) == value for key, value in required.items())
        and bound_verifier.get("sha256") == replay.get("script_sha256")
    )
    replay.update(
        {
            "status": "PASS" if replay["status"] == "PASS" and fields_ok else "FAIL",
            "certificate": str(certificate_path.relative_to(ROOT)),
            "certificate_sha256": sha256_file(certificate_path),
            "conclusion": conclusion,
            "required_conclusion": required,
            "certificate_bound_verifier": bound_verifier,
        }
    )
    return replay


def topology_all_n_replay():
    script = ROOT / "sharpness" / "independent_topology_alln_replay.py"
    certificate_path = ROOT / "sharpness" / "K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json"
    if not script.is_file():
        return {"status": "BLOCKED", "gap": "independent topology/all-n replay script has not landed"}
    replay = run_checked_verifier(
        script,
        "INDEPENDENT_K3P_TOPOLOGY_ALL_N_PASS",
        timeout=1800,
        preserve_tree=ROOT / "sharpness",
    )
    if not certificate_path.is_file():
        replay.update({"status": "FAIL", "gap": "topology replay did not produce its certificate"})
        return replay
    certificate = json.loads(certificate_path.read_text())
    conclusion = certificate.get("conclusion", {})
    required = {
        "all_checks_pass": True,
        "all_n_from": 3,
        "dimension_formula": "6n-3",
        "cherry_determinant_nonzero": True,
        "weak_not_strong_persists": True,
        "nonisomorphism_persists": True,
        "nontriangle_equivalence_persists": True,
        "strict_continuous_time": True,
    }
    bound_verifier = certificate.get("provenance", {}).get("independent_verifier", {})
    fields_ok = (
        all(conclusion.get(key) == value for key, value in required.items())
        and bound_verifier.get("sha256") == replay.get("script_sha256")
    )
    replay.update(
        {
            "status": "PASS" if replay["status"] == "PASS" and fields_ok else "FAIL",
            "certificate": str(certificate_path.relative_to(ROOT)),
            "certificate_sha256": sha256_file(certificate_path),
            "conclusion": conclusion,
            "required_conclusion": required,
            "certificate_bound_verifier": bound_verifier,
        }
    )
    return replay


def make_gate(number, status, evidence, exact_gap=None, qualification=None):
    assert status in {"PASS", "BLOCKED", "FAIL"}
    return {
        "item": number,
        "claim": PRIMARY_ITEMS[number],
        "status": status,
        "evidence": evidence,
        "exact_gap": exact_gap,
        "qualification": qualification,
    }


def stable_replay_record(record):
    """Recursively remove per-run timings from tracked mathematical evidence."""
    if isinstance(record, dict):
        return {
            key: stable_replay_record(value)
            for key, value in record.items()
            if key != "elapsed_seconds"
        }
    if isinstance(record, list):
        return [stable_replay_record(value) for value in record]
    return record


def main():
    report_path = HERE / "primary_gate_report.json"
    input_binding = verify_input_lock()
    gates = []
    family_errors = {}
    evidence_paths = {}

    if input_binding["status"] != "PASS":
        gap = "immutable primary input hash mismatch; no mathematical gate was promoted"
        gates = [make_gate(i, "BLOCKED", ["reproducibility/primary_input_lock.json"], gap) for i in range(1, 29)]
    else:
        def exact_family(name, function, *args):
            try:
                return function(*args)
            except Exception as error:  # fail closed while preserving other independent families
                family_errors[name] = {
                    "exception_type": type(error).__name__,
                    "message": str(error),
                    "traceback": traceback.format_exc(),
                }
                return None

        model = exact_family("model_domain", model_domain_evidence, FROZEN)
        cut_transfer = exact_family("strong_class_cut_transfer", strong_class_cut_transfer_replay)
        three = exact_family("three_port", three_port_evidence, FROZEN)
        collision = exact_family("double_theta", collision_evidence)
        rootings = exact_family("rooting_census", rooting_census_evidence, FROZEN)
        four = exact_family("four_port", verify_four_port, FROZEN)
        cherry = exact_family("cherry", cherry_evidence)
        bridge = marginal = None
        if model is not None:
            combined = exact_family("bridge_marginals", bridge_and_marginal_evidence, model)
            if combined is not None:
                action, normalizer, physical_product, marginal = combined
                bridge = {
                    "schema": "k3p-primary-bridge-fibre-exact-v1",
                    "three_sector_action": action,
                    "incidence_normalizer": normalizer,
                    "physical_local_product": physical_product,
                }

        outputs = [
            ("model_domain/primary_exact_evidence.json", model),
            ("three_port/primary_exact_evidence.json", three),
            ("topology/primary_double_theta_evidence.json", collision),
            ("topology/primary_rooting_census_evidence.json", rootings),
            ("bridge_fibre/primary_exact_evidence.json", bridge),
            ("marginals/primary_exact_evidence.json", marginal),
            ("four_port_atlas/primary_exact_evidence.json", four),
            ("topology/primary_cherry_evidence.json", cherry),
        ]
        for relative, payload in outputs:
            if payload is not None:
                path = ROOT / relative
                atomic_json(path, payload)
                evidence_paths[relative] = sha256_file(path)
        for relative in (
            "reproducibility/strong_class_cut_transfer_gate_report.json",
            "reproducibility/CUT_TRANSFER_GATE_MUTATION_REPORT.json",
        ):
            path = ROOT / relative
            if path.is_file():
                evidence_paths[relative] = sha256_file(path)

        model_path = ["model_domain/primary_exact_evidence.json"]
        for number in range(1, 6):
            gates.append(make_gate(number, "PASS" if model else "FAIL", model_path, family_errors.get("model_domain")))
        cut_evidence = [
            "reproducibility/strong_class_cut_transfer_gate_report.json",
            "reproducibility/CUT_TRANSFER_GATE_MUTATION_REPORT.json",
            "cut_recovery/strong_crossbridge/global_transfer/THEOREM_MANIFEST.json",
            "cut_recovery/strong_crossbridge/global_transfer/RELEASE_VERIFICATION_REPORT.json",
            "cut_recovery/strong_crossbridge/global_transfer/RELEASE_OPTIMIZED_VERIFICATION_REPORT.json",
        ]
        if cut_transfer and cut_transfer["status"] == "PASS":
            gates.append(make_gate(
                6,
                "PASS",
                cut_evidence,
                qualification=(
                    "This is directional cut-set equality under source-relative containment "
                    "inside the strong class. The universal arbitrary-network pointwise "
                    "cut-rank equivalence is withdrawn and not used."
                ),
            ))
        else:
            gates.append(make_gate(
                6,
                "FAIL",
                cut_evidence,
                cut_transfer.get("gap") if cut_transfer else family_errors.get("strong_class_cut_transfer"),
                "No universal pointwise fallback is permitted.",
            ))
        for number in range(7, 12):
            gates.append(make_gate(number, "PASS" if three else "FAIL", ["three_port/primary_exact_evidence.json"], family_errors.get("three_port")))
        gates.append(make_gate(12, "PASS" if collision else "FAIL", ["topology/primary_double_theta_evidence.json"], family_errors.get("double_theta"), "The exact rank-15 collision and 23-dimensional local locus are replayed; no unstored tangent certificate for its separate strict-CT perturbation is asserted here."))
        gates.append(make_gate(13, "PASS" if rootings else "FAIL", ["topology/primary_rooting_census_evidence.json"], family_errors.get("rooting_census")))
        for number in range(14, 17):
            gates.append(make_gate(number, "PASS" if bridge else "FAIL", ["bridge_fibre/primary_exact_evidence.json"], family_errors.get("bridge_marginals")))
        gates.append(make_gate(17, "PASS" if marginal else "FAIL", ["marginals/primary_exact_evidence.json"], family_errors.get("bridge_marginals")))
        gates.append(make_gate(18, "PASS" if four and len(four["source_rank_certificates"]) == 6 else "FAIL", ["four_port_atlas/primary_exact_evidence.json"], family_errors.get("four_port")))

        primary_transport_ok = bool(
            four
            and four.get("raw_transport_gate") == "PASS"
            and four.get("primary_root_suppressed_mixed_transport", {}).get("canonical_orbits") == 14
            and four.get("primary_root_suppressed_mixed_transport", {}).get("raw_orbit_members") == 38
            and four.get("primary_root_suppressed_mixed_transport", {}).get("all_double_cosets_reconstructed") is True
            and four.get("primary_root_suppressed_mixed_transport", {}).get("all_literal_fourier_coordinate_transports_exact") is True
        )
        transport = corrected_transport_replay()
        clean_transport_status = transport["status"]
        transport_status = "PASS" if primary_transport_ok and clean_transport_status == "PASS" else (
            "BLOCKED" if clean_transport_status == "BLOCKED" else "FAIL"
        )
        for number in (19,):
            gates.append(make_gate(number, transport_status, ["four_port_atlas/primary_exact_evidence.json", "clean_room/H21_01_TRANSPORT_AUDIT.json", "clean_room/adversarial/HARDENED_H21_REAUDIT.json"], transport.get("gap") if transport_status != "PASS" else None, "The project-local primary implementation reconstructs all mixed automorphism groups, double cosets, and literal Fourier coordinate actions. The corrected clean-room implementation is an additional cross-check, not a substitute."))
        gates.append(make_gate(20, "PASS" if four and len(four["polynomial_separators"]) == 9 else "FAIL", ["four_port_atlas/primary_exact_evidence.json"], family_errors.get("four_port")))
        gates.append(make_gate(21, "PASS" if four and len(four["directed_rank_separators"]) == 5 else "FAIL", ["four_port_atlas/primary_exact_evidence.json"], family_errors.get("four_port")))
        gates.append(make_gate(22, "PASS" if four and len(four["prelock_sink_swap_separators"]) == 2 else "FAIL", ["four_port_atlas/primary_exact_evidence.json"], family_errors.get("four_port")))
        gates.append(make_gate(23, "PASS" if transport_status == "PASS" and four and four["accounting_numerically_consistent"] and four["accounting_classification_certified_by_this_module"] else ("BLOCKED" if transport_status == "BLOCKED" else "FAIL"), ["four_port_atlas/primary_exact_evidence.json", "clean_room/H21_01_TRANSPORT_AUDIT.json", "clean_room/adversarial/HARDENED_H21_REAUDIT.json"], transport.get("gap") if transport_status != "PASS" else None))

        sharpness = sharpness_replay()
        sharp_status = sharpness["status"]
        sharp_evidence = ["sharpness/K3P_SHARPNESS_KRAWCZYK_CERTIFICATE.json"]
        if sharp_status == "PASS":
            conclusion = sharpness["conclusion"]
            gates.append(make_gate(24, "PASS", sharp_evidence))
            rank_ok = conclusion["W_rank_15_throughout_box"] and conclusion["Wprime_rank_15_throughout_box"]
            gates.append(make_gate(25, "PASS" if rank_ok else "FAIL", sharp_evidence))
            domain_ok = conclusion["principal_K3P_domain_throughout_box"] and conclusion["strict_continuous_time_throughout_box"]
            gates.append(make_gate(26, "PASS" if domain_ok else "FAIL", sharp_evidence))
        else:
            for number in range(24, 27):
                gates.append(make_gate(number, "BLOCKED" if sharp_status == "BLOCKED" else "FAIL", sharp_evidence, sharpness.get("gap") or "independent sharpness replay failed"))
        topology_all_n = topology_all_n_replay()
        topology_status = topology_all_n["status"]
        topology_evidence = [
            "topology/primary_cherry_evidence.json",
            "topology/primary_rooting_census_evidence.json",
            "sharpness/K3P_SHARPNESS_TOPOLOGY_ALL_N_CERTIFICATE.json",
        ]
        gates.append(make_gate(27, "PASS" if cherry and topology_status == "PASS" else ("BLOCKED" if topology_status == "BLOCKED" else "FAIL"), topology_evidence, topology_all_n.get("gap") or family_errors.get("cherry")))
        gates.append(make_gate(28, "PASS" if cherry and rootings and topology_status == "PASS" else ("BLOCKED" if topology_status == "BLOCKED" else "FAIL"), topology_evidence, topology_all_n.get("gap") or family_errors.get("cherry") or family_errors.get("rooting_census")))

    gates.sort(key=lambda record: record["item"])
    assert [record["item"] for record in gates] == list(range(1, 29))
    counts = {status: sum(gate["status"] == status for gate in gates) for status in ("PASS", "BLOCKED", "FAIL")}
    overall = "PASS" if counts == {"PASS": 28, "BLOCKED": 0, "FAIL": 0} else "BLOCKED"
    upstream_audit = {
        "attempted_unchanged_first": True,
        "attempt_date": "2026-08-24T21:41:00-07:00",
        "all_exit_codes": 1,
        "findings": {
            "verify_model_domain_and_bridge.py": "exact assertions reach final write, then fail on hard-coded /mnt/data output",
            "verify_k3p_cut_transfer.py": "absent jc_pointwise_cut_certificate_frozen.json",
            "verify_tree_sunlet_separator.py": "absent k3p_three_port_models module",
            "verify_three_port_geometry.py": "absent k3p_three_port_models module",
            "verify_compiler_specialization.py": "absent cloud k2p atlas/universe path",
            "verify_rooting_censuses.py": "absent k3p_graph_map and rooting_census modules",
            "verify_fourteen_orbits.py": "incorrect package-relative lock path plus absent universe",
            "certify_sharpness_krawczyk.py": "cloud dependency stack and absent sharpness_relative_root.json",
            "verify_sharpness_extension.py": "incorrect package-relative certificate path",
        },
        "policy": "No expected answer was copied to cure these failures; exact primitive replacements or explicit BLOCKED records are used.",
    }
    report = {
        "schema": "k3p-primary-gate-report-v1",
        "project_root": str(ROOT),
        "command": "bash reproducibility/verify_primary.sh",
        "python": {"executable": sys.executable, "version": sys.version, "platform": platform.platform()},
        "input_binding": input_binding,
        "upstream_verifier_audit": upstream_audit,
        "active_verifier_hashes": {
            "reproducibility/verify_primary.sh": sha256_file(HERE / "verify_primary.sh"),
            "reproducibility/exact_primary.py": sha256_file(HERE / "exact_primary.py"),
            "reproducibility/exact_four_port.py": sha256_file(HERE / "exact_four_port.py"),
            "reproducibility/verify_primary.py": sha256_file(Path(__file__).resolve()),
            "reproducibility/strong_cut_transfer_gate.py": sha256_file(HERE / "strong_cut_transfer_gate.py"),
            "reproducibility/test_cut_transfer_gate_mutations.py": sha256_file(HERE / "test_cut_transfer_gate_mutations.py"),
        },
        "generated_evidence_sha256": evidence_paths,
        "auxiliary_replays": {
            "strong_class_cut_transfer": stable_replay_record(locals().get("cut_transfer")),
            "corrected_four_port_transport": stable_replay_record(locals().get("transport")),
            "independent_sharpness": stable_replay_record(locals().get("sharpness")),
            "independent_topology_all_n": stable_replay_record(locals().get("topology_all_n")),
        },
        "gates": gates,
        "counts": counts,
        "completion_estimate_percent": round(100 * counts["PASS"] / 28, 1),
        "overall_status": overall,
        "runtime_logging": {
            "mechanism": "/usr/bin/time -l in the ignored per-run transcript",
            "first_full_run_transcript": "reproducibility/logs/primary_20260825T045030Z.log",
            "first_full_run_elapsed_seconds": 35.16,
            "first_full_run_maximum_resident_set_bytes": 94109696,
            "first_full_run_internal_python_peak_bytes": 70205440
        },
        "family_errors": family_errors,
    }
    atomic_json(report_path, report)
    print(f"PRIMARY_GATE_STATUS {overall}")
    print(f"PRIMARY_GATE_COUNTS pass={counts['PASS']} blocked={counts['BLOCKED']} fail={counts['FAIL']}")
    print(f"PRIMARY_GATE_REPORT {report_path.relative_to(ROOT)}")
    for gate in gates:
        if gate["status"] != "PASS":
            print(f"ITEM_{gate['item']}_{gate['status']} {gate['claim']}: {gate['exact_gap']}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
