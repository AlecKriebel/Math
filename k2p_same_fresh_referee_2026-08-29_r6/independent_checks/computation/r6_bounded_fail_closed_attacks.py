#!/usr/bin/env python3
"""Bounded reviewer attacks for exact failures and mutation qualification."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any


class Failure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise Failure(code if detail is None else f"{code}:{detail}")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "NOT_OBJECT", path)
    if "payload_sha256" in value:
        body = dict(value)
        claimed = body.pop("payload_sha256")
        if claimed != sha_object(body) and "operational" in body:
            body.pop("operational")
        require(claimed == sha_object(body), "PAYLOAD_HASH", path)
    return value


ATLAS_PROBE = r'''
import importlib.util
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("r6_atlas_probe", path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
constant = (((), ((0, 1),)),)
outputs = tuple(constant for _ in module.orbit_assignments(4))
descriptor = module.MapDescriptor(4, 0, 0, outputs, ())
unit = lambda columns: ((1,) + (0,) * (len(columns) - 1),)
tests = (
    ("reference", "ATLAS_TARGET_PULLBACK_NONZERO degree=2 engine=reference", "exact_kernel_sparse_columns", lambda: module.quadratic_separator(descriptor, descriptor)),
    ("fast", "ATLAS_TARGET_PULLBACK_NONZERO degree=2 engine=fast", "kernel_sparse_columns_fast", lambda: module.quadratic_separator_fast(descriptor, descriptor)),
    ("cubic", "ATLAS_TARGET_PULLBACK_NONZERO degree=3 engine=fast", "kernel_sparse_columns_fast", lambda: module.cubic_separator_fast(descriptor, descriptor)),
    ("homogeneous", "ATLAS_TARGET_PULLBACK_NONZERO degree=4 engine=homogeneous", "kernel_sparse_columns_fast", lambda: module.homogeneous_separator_fast(descriptor, descriptor, 4, 1000)),
    ("subset", "ATLAS_TARGET_PULLBACK_NONZERO degree=3 engine=subset", "kernel_sparse_columns_fast", lambda: module.homogeneous_separator_subset(descriptor, descriptor, 3, tuple(range(len(outputs))))),
    ("positive_target", "ATLAS_SOURCE_PULLBACK_NONZERO degree=2 engine=positive_target", "kernel_sparse_columns_fast", lambda: module.source_invariant_positive_target(descriptor, descriptor)),
)
observed = []
for name, expected, kernel_name, operation in tests:
    original = getattr(module, kernel_name)
    setattr(module, kernel_name, unit)
    try:
        operation()
    except module.AtlasInvariantError as error:
        if str(error) != expected:
            raise
        observed.append(name)
    else:
        raise SystemExit("FALSE_CERTIFICATE_ACCEPTED:" + name)
    finally:
        setattr(module, kernel_name, original)
print(",".join(observed))
'''


def atlas_attacks(project: Path, python: Path) -> dict[str, Any]:
    atlas = project / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
    expected = "reference,fast,cubic,homogeneous,subset,positive_target"
    rows = []
    for mode in ("normal", "dash_O", "environment"):
        environment = dict(os.environ)
        environment.pop("PYTHONOPTIMIZE", None)
        command = [str(python), "-B", "-c", ATLAS_PROBE, str(atlas)]
        if mode == "dash_O":
            command.insert(1, "-O")
        elif mode == "environment":
            environment["PYTHONOPTIMIZE"] = "1"
        completed = subprocess.run(
            command,
            cwd=project,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
            check=False,
        )
        require(completed.returncode == 0 and completed.stdout.strip() == expected, "ATLAS_ATTACK", f"{mode}:{completed.returncode}:{completed.stdout}")
        rows.append({"mode": mode, "rejected_false_certificate_families": expected.split(",")})
    return {"atlas_sha256": sha_file(atlas), "modes": rows, "attacks_per_mode": 6}


def ambient_optimized_guards(project: Path, python: Path) -> dict[str, Any]:
    cases = (
        ("composite_verifier", "work/corrected_composite_ledgers/verify_corrected_composites_independent.py", ("--family", "raw4", "--report", "OUT")),
        ("composite_mutations", "work/corrected_composite_ledgers/run_composite_mutations.py", ("--family", "raw4", "--output", "OUT")),
        ("static_article_audit", "proof_compression_submission/adversarial_review/audit_article_sources.py", ()),
        ("printed_anchor_mutations", "proof_compression_submission/adversarial_review/test_printed_authority_hash_gate.py", ()),
        ("raw4_generator", "work/raw_ledger_audit/generate_raw_ledger.py", ("--output-root", "OUTDIR")),
        ("raw4_verifier", "work/raw_ledger_audit/verify_raw_ledger.py", ()),
        ("theta2_generator", "work/theta2_five_port_closure/generate_theta2_ledger.py", ("--output-root", "OUTDIR")),
        ("theta2_verifier", "work/theta2_five_port_closure/verify_theta2_ledger.py", ("--quick",)),
        ("canonicalizer", "work/canonicalizer_completeness/canonicalizer_audit.py", ("--semantic-only",)),
        ("parameter_transport", "work/canonicalizer_completeness/inheritance_transport/verify_parameter_transport_certificate.py", ("--structural-only",)),
        ("rank_upper", "work/rank_upper_certificates/verify_rank_upper_certificates.py", ("--output", "OUT")),
        ("final_release", "work/final_theorem_release/verify_final_theorem_release.py", ("--quick", "--output", "OUT")),
    )
    rows = []
    for name, relative, raw_arguments in cases:
        with tempfile.TemporaryDirectory(prefix="r6-ambient-opt-") as directory:
            scratch = Path(directory)
            stale = scratch / "stale.json"
            stale.write_text('{"status":"PASS"}\n', encoding="utf-8")
            arguments = tuple(
                str(stale) if item == "OUT" else str(scratch / "out") if item == "OUTDIR" else item
                for item in raw_arguments
            )
            environment = dict(os.environ)
            environment["PYTHONOPTIMIZE"] = "1"
            completed = subprocess.run(
                [str(python), "-B", str(project / relative), *arguments],
                cwd=scratch,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=30,
                check=False,
            )
            observed = completed.stdout.strip()
            require(completed.returncode != 0 and "OPTIMIZED" in observed.upper(), "AMBIENT_OPTIMIZED", f"{name}:{completed.returncode}:{observed[:500]}")
            rows.append({"entry_point": name, "exit_code": completed.returncode, "diagnostic": observed})
    return {"mode": "PYTHONOPTIMIZE=1", "entry_point_count": len(rows), "rows": rows}


def rank_upper_audit(project: Path) -> dict[str, Any]:
    root = project / "work/rank_upper_certificates"
    report_path = root / "mutation_report.json"
    report = load(report_path)
    require(report["schema"] == "k2p-rank-upper-adversarial-mutations-v2" and report["status"] == "pass" and report["survivors"] == 0, "RANK_MUTATION_STATUS")
    sampled = next(row for row in report["results"] if row["mutation"] == "sampled_rank_substituted_for_symbolic_upper")
    require(
        sampled["complete_mutant_package_created"] is True
        and sampled["production_verifier_invoked"] is True
        and sampled["verifier_exit_code"] == 1
        and sampled["semantic_diagnostic_matched"] is True
        and sampled["success_artifact_created"] is False
        and sampled["sampled_evidence_cannot_prove_global_upper_bound"] is True,
        "RANK_SAMPLED_ATTACK",
    )
    verifier = root / "verify_rank_upper_certificates.py"
    syzygy = root / "syzygy_upper.py"
    source = syzygy.read_text(encoding="utf-8")
    require("coefficient_system" in source and "exact_integer_rank" in source and "rank_stacked - rank_system" in source, "RANK_SYMBOLIC_CODE")
    require(
        source.lower().count("sample") == 1
        and "No sampled Jacobian is used for the upper bound." in source,
        "RANK_UPPER_SAMPLED_CODE",
    )
    coverage = load(root / "rank_upper_coverage.json")
    mechanisms = collections.Counter(row["upper_mechanism"] for row in coverage["descriptors"])
    require(
        mechanisms
        == {
            "multilinear_lambda_polynomial_vector_fields": 3515,
            "base_fields_plus_primitive_log_field_port_transport": 864,
        },
        "RANK_MECHANISMS",
        mechanisms,
    )
    return {
        "coverage_sha256": sha_file(root / "rank_upper_coverage.json"),
        "descriptor_count": coverage["descriptor_count"],
        "mechanism_counts": dict(mechanisms),
        "mutation_report_sha256": sha_file(report_path),
        "mutation_payload_sha256": report["payload_sha256"],
        "sampled_rank_attack_observed_diagnostic": sampled["observed_semantic_diagnostic"],
        "sampled_rank_attack_rejected": True,
        "verifier_sha256": sha_file(verifier),
        "symbolic_upper_engine_sha256": sha_file(syzygy),
    }


def other_mutation_reports(project: Path) -> dict[str, Any]:
    specifications = (
        ("canonicalizer", "work/canonicalizer_completeness/canonicalizer_completeness_mutation_certificate.json", "k2p-canonicalizer-completeness-mutations-v2", "survived"),
        ("parameter_transport", "work/canonicalizer_completeness/inheritance_transport/parameter_transport_mutation_report.json", "k2p_parameter_transport_mutations_v2", "survived"),
        ("restoration", "work/restoration_sign_reclassification/corrected_restoration_mutation_certificate.json", "k2p-corrected-restoration-mutations-v2", None),
        ("probe", "work/probe_coherence_corrected/probe_coherence_mutation_certificate.json", "k2p-corrected-probe-mutations-v2", None),
        ("independent_probe", "work/global_proof_adversary/probe_full_audit/independent_probe_mutation_report.json", "k2p-corrected-probe-independent-mutations-v2", "mutations_survived"),
        ("direct_closure", "package/referee/k2p_offline_sweep_portable/direct_closure_mutation_report.json", "k2p-four-port-direct-closure-mutations-v2", "mutations_survived"),
    )
    rows = {}
    for name, relative, schema, survivor_field in specifications:
        path = project / relative
        report = load(path)
        no_survivors = (
            report.get(survivor_field) == 0
            if survivor_field is not None
            else report.get("mutations_attempted")
            == report.get("mutations_rejected")
        )
        require(report["schema"] == schema and no_survivors, "MUTATION_REPORT", name)
        complete = report.get("complete_production_verifier_attacks")
        rows[name] = {
            "path": relative,
            "sha256": sha_file(path),
            "payload_sha256": report.get("payload_sha256"),
            "schema": schema,
            "survivors": 0,
            "complete_production_verifier_attacks": complete,
        }
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    python = args.python.absolute()
    require(project.is_dir() and python.is_file(), "INPUT")
    result = {
        "schema": "r6-reviewer-bounded-fail-closed-attacks-v1",
        "status": "PASS",
        "atlas_false_certificate_attacks": atlas_attacks(project, python),
        "ambient_optimized_entrypoints": ambient_optimized_guards(project, python),
        "rank_upper": rank_upper_audit(project),
        "other_mutation_reports": other_mutation_reports(project),
        "unresolved": 0,
    }
    result["payload_sha256"] = sha_object(result)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "payload_sha256": result["payload_sha256"], "atlas_attacks": 18, "optimized_guards": result["ambient_optimized_entrypoints"]["entry_point_count"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Failure as error:
        raise SystemExit(f"R6_BOUNDED_ATTACK_FAIL:{error}")
