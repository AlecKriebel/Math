#!/usr/bin/env python3
"""Exact mathematical gate orchestration used inside an isolated copy."""

from __future__ import annotations

import argparse
import gzip
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import hashlib
import shutil


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
COMMITMENTS: dict[str, object] = {}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def logical_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(*command: str, cwd: Path = ROOT) -> None:
    print("\n==> " + " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=os.environ.copy(), check=True)


def compare(generated: Path, expected: Path) -> None:
    if generated.read_bytes() != expected.read_bytes():
        raise AssertionError(f"replay differs from frozen certificate: {expected.relative_to(ROOT)}")


def compare_logical_gzip(generated: Path, expected: Path) -> None:
    with gzip.open(generated, "rb") as left, gzip.open(expected, "rb") as right:
        if left.read() != right.read():
            raise AssertionError(
                f"logical replay differs from frozen certificate: {expected.relative_to(ROOT)}"
            )


def convention_gate() -> None:
    # Exercise the exact finite fixtures without importing literature files or
    # audit prose, which are not mathematical inputs.
    import importlib.util
    module_path = ROOT / "reviews/final_standard_convention/verify_conventions.py"
    spec = importlib.util.spec_from_file_location("fixed_convention", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory(prefix="convention-") as raw:
        module.OUT = Path(raw) / "certificate.json"
        module.source_hashes = lambda: {}
        module.main()
        payload = json.loads(module.OUT.read_text())
        assert payload["verdict"] == "VERIFIED_AFTER_CORRECTION"
        assert payload["mutations"]["unexpected_survivors"] == []


def triangle_gate() -> None:
    here = ROOT / "reviews/triangle_redirection_cleanroom"
    with tempfile.TemporaryDirectory(prefix="triangle-") as raw:
        out = Path(raw)
        run(PYTHON, str(here / "cleanroom_verify.py"),
            "--claim", str(ROOT / "primary/certificates/jc_triangle_redirection_active.json"),
            "--certificate", str(out / "certificate.json"),
            "--mutations", str(out / "mutations.json"))
        compare(out / "certificate.json", here / "certificate.json")
        compare(out / "mutations.json", here / "mutation_results.json")


def base_gate(n3: bool) -> None:
    name = "base_gate_adversarial_referee_n3" if n3 else "base_gate_adversarial_referee"
    script = "referee_n3.py" if n3 else "referee.py"
    here = ROOT / "reviews" / name
    with tempfile.TemporaryDirectory(prefix=name + "-") as raw:
        out = Path(raw)
        run(PYTHON, str(here / script), "--certificate", str(out / "certificate.json"),
            "--mutations", str(out / "mutations.json"))
        compare(out / "certificate.json", here / "certificate.json")
        compare(out / "mutations.json", here / "mutation_results.json")
        COMMITMENTS[f"base_gate_{'n3' if n3 else 'n4'}"] = {
            "certificate_sha256": sha256(out / "certificate.json"),
            "mutations_sha256": sha256(out / "mutations.json"),
        }


def full_n4_exact_audit() -> None:
    here = ROOT / "reviews/final_hard_cover_cleanroom"
    summary = ROOT / "primary/certificates/hard_cover_schema3_theta2_full_summary.json"
    with tempfile.TemporaryDirectory(prefix="n4-full-exact-") as raw:
        out = Path(raw)
        run(
            PYTHON, str(here / "audit_candidate_stream.py"),
            "--relations", "primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz",
            "--graphs", "primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz",
            "--roots", "primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz",
            "--polynomials", "primary/certificates/hard_cover_polynomials_n4_schema3_theta2_full.jsonl.gz",
            "--summary", str(summary.relative_to(ROOT)),
            "--expected-summary-sha256", sha256(summary),
            "--invariant-metadata", "primary/certificates/invariant_multihomogeneity.json",
            "--family-tag", "n4_minimum",
            "--output", str(out / "audit.json"),
            "--terminal-records-output", str(out / "terminals.jsonl.gz"),
        )
        compare(
            out / "audit.json",
            here / "certificates/schema3_n4_theta2_full_audit.json",
        )
        compare_logical_gzip(
            out / "terminals.jsonl.gz",
            here / "certificates/schema3_n4_theta2_terminal_records.jsonl.gz",
        )
        COMMITMENTS["n4_all_record_exact_audit"] = {
            "audit_sha256": sha256(out / "audit.json"),
            "terminal_stream_logical_sha256": logical_sha256(
                out / "terminals.jsonl.gz"
            ),
        }
    run(PYTHON, str(here / "mutation_schema3_stream.py"))
    run(PYTHON, str(here / "verify_schema3_n4_certificates.py"))


def omega_gate(full: bool) -> None:
    if full:
        run(PYTHON, "omega_audit/runtime_compat/verify_orbit_constant.py")
        run(PYTHON, "omega_audit/runtime_compat/run_historical_omega.py")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "omega_audit/frozen_input/historical/src")
        print("\n==> historical standard-library Omega replay", flush=True)
        subprocess.run([PYTHON, "omega_audit/frozen_input/historical/src/verify_jc_omega_move_stdlib.py"],
                       cwd=ROOT, env=env, check=True)
    run(PYTHON, "omega_audit/independent/verify_omega_release.py")
    run(PYTHON, "omega_audit/independent/verify_omega_rank_readability.py")
    generated = ROOT / "omega_audit/independent/output"
    if generated.is_dir():
        COMMITMENTS["omega"] = {
            path.name: sha256(path) for path in sorted(generated.glob("*.json"))
        }
        shutil.rmtree(generated)


def quick() -> None:
    run(PYTHON, "verifiers/package_mutation_tests.py")
    run(PYTHON, "reviews/root_probe/verify_active_structural.py")
    run(PYTHON, "reviews/global_bridge/exact_audit.py",
        "--output", "reviews/global_bridge/exact_audit_certificate.json")
    run(PYTHON, "reviews/global_bridge/mutation_tests.py",
        "--output", "reviews/global_bridge/mutation_certificate.json")
    run(PYTHON, "reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py")
    run(PYTHON, "reviews/direct_anchor_probe_closure/mutation_tests.py")
    run(PYTHON, "reviews/compact_probe_clean_clone_gate/verify_tracked_inputs.py")
    triangle_gate()
    run(PYTHON, "s_tc_jc_sharp_boundary/reproducibility/verify_math.py")
    omega_gate(False)


def full(regenerate: bool) -> None:
    run(PYTHON, "verifiers/package_mutation_tests.py")
    convention_gate()
    run(PYTHON, "reviews/root_probe/verify_active_structural.py")
    run(PYTHON, "reviews/global_bridge/exact_audit.py",
        "--output", "reviews/global_bridge/exact_audit_certificate.json")
    run(PYTHON, "reviews/global_bridge/mutation_tests.py",
        "--output", "reviews/global_bridge/mutation_certificate.json")
    run(PYTHON, "independent/bridge_cut/verify_bridge.py",
        "--output", "reviews/global_bridge/upstream_bridge_replay.json")
    run(PYTHON, "independent/bridge_cut/verify_cut.py",
        "--output", "reviews/global_bridge/upstream_cut_replay.json")
    run(PYTHON, "independent/bridge_cut/verify_mutations.py",
        "--output", "reviews/global_bridge/upstream_mutation_replay.json")
    run(PYTHON, "reviews/n3_universe_generator/generate_universe.py")
    with tempfile.TemporaryDirectory(prefix="bounded-cleanroom-") as raw:
        out = Path(raw)
        run(PYTHON, "reviews/bounded_directed_relation_cleanroom/cleanroom_verify.py",
            "--repo", str(ROOT), "--family", "n3", "--omit-history-regressions",
            "--output", str(out / "n3_full_replay.json"),
            "--mutation-output", str(out / "n3_mutation_replay.json"),
            "--manifest-output", str(out / "n3_manifest.json"))
        replay = json.loads((out / "n3_full_replay.json").read_text())
        mutations = json.loads((out / "n3_mutation_replay.json").read_text())
        assert replay["status"] == "VERIFIED"
        assert mutations["n3"]["all_required_mutations_rejected"]
        COMMITMENTS["bounded_n3_cleanroom"] = {
            "replay_sha256": sha256(out / "n3_full_replay.json"),
            "mutations_sha256": sha256(out / "n3_mutation_replay.json"),
        }
    run(PYTHON, "reviews/theta2_signature_gate/verify_gate.py")
    run(PYTHON, "reviews/theta2_signature_gate/canonicalize_relations.py")
    base_gate(True)
    full_n4_exact_audit()
    base_gate(False)
    run(PYTHON, "reviews/final_hard_cover_cleanroom/verify_schema3_n4_certificates.py")
    if regenerate:
        run(PYTHON, "reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py")
    run(PYTHON, "reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py")
    run(PYTHON, "reviews/direct_anchor_probe_closure/mutation_tests.py")
    run(PYTHON, "reviews/compact_probe_clean_clone_gate/semantic_gate.py",
        "--family", "all", "--output",
        "reviews/compact_probe_clean_clone_gate/certificates/compact_only_semantic_replay.json")
    run(PYTHON, "reviews/compact_probe_clean_clone_gate/mutation_tests.py")
    run(PYTHON, "reviews/compact_probe_clean_clone_gate/verify_tracked_inputs.py")
    triangle_gate()
    run(PYTHON, "s_tc_jc_sharp_boundary/reproducibility/verify_math.py")
    omega_gate(True)

    if regenerate:
        with tempfile.TemporaryDirectory(prefix="complete-regeneration-output-") as raw:
            regenerated = Path(raw) / "regeneration_commitment.json"
            run(
                PYTHON,
                "verifiers/regenerate_load_bearing.py",
                "--output",
                str(regenerated),
            )
            COMMITMENTS["primitive_regeneration"] = json.loads(
                regenerated.read_text(encoding="utf-8")
            )

    for relative in (
        "reviews/n3_universe_generator/n3_universe_certificate.json",
        "reviews/n3_universe_generator/n3_normalized_raw_relations.jsonl.gz",
        "reviews/n3_universe_generator/n3_normalized_merged_relations.jsonl.gz",
        "reviews/theta2_signature_gate/signature_certificate.json",
        "reviews/theta2_signature_gate/canonical_quotient_certificate.json",
        "reviews/theta2_signature_gate/presentation_crosswalk.jsonl",
        "reviews/direct_anchor_probe_closure/certificates/summary.json",
        "reviews/compact_probe_clean_clone_gate/certificates/compact_only_semantic_replay.json",
        "reviews/compact_probe_clean_clone_gate/certificates/mutation_tests.json",
    ):
        COMMITMENTS[relative] = sha256(ROOT / relative)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("quick", "full", "regenerate-all"))
    args = parser.parse_args()
    if args.mode == "quick":
        quick()
    else:
        full(args.mode == "regenerate-all")
    output = os.environ.get("STC_JC_COMMITMENT_OUTPUT")
    if output:
        Path(output).write_text(json.dumps(COMMITMENTS, sort_keys=True, indent=2) + "\n")
    print(f"VERIFIED: all exact mathematical gates ({args.mode})")


if __name__ == "__main__":
    main()
