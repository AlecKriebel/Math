#!/usr/bin/env python3
"""Adversarial mutations for the independent K3P infrastructure verifier."""

from __future__ import annotations

from hashlib import sha256
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
