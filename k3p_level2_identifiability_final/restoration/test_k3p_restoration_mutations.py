#!/usr/bin/env python3
"""Adversarial mutation suite for the K3P restoration release."""
from __future__ import annotations

import copy
import gzip
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "K3P_RESTORATION_MUTATION_CERTIFICATE.json"
VERIFIER = HERE / "verify_k3p_restoration.py"


class MutationFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise MutationFailure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def logical_payload(value):
    result = dict(value)
    result.pop("payload_sha256", None)
    return sha(result)


def read_registry():
    with gzip.open(HERE / "restoration_proof_registry.json.gz", "rt") as handle:
        return json.load(handle)


def read_ledger():
    with gzip.open(HERE / "restoration_ledger.jsonl.gz", "rt") as handle:
        return [json.loads(line) for line in handle]


def gzip_bytes(payload):
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buffer, mtime=0) as handle:
        handle.write(payload)
    return buffer.getvalue()


def reseal(root, manifest, registry, records):
    prefixes = {
        "displayed_quartet_mismatch": "Q:",
        "k3p_tree_sunlet_sos": "K3P-TS:",
        "k3p_exact_multihomogeneous_quadratic": "K3P-Q2:",
        "k3p_direct_marginal_quartic": "K3P-M4:",
    }
    # Certificates that were intentionally changed carry a temporary
    # ``__old_id`` marker so references can be transported coherently.
    for kind, certificates in list(registry["proofs"].items()):
        rebuilt = {}
        for old_key, certificate in certificates.items():
            old_id = certificate.pop("__old_id", old_key)
            new_id = prefixes[kind] + sha(certificate)
            rebuilt[new_id] = certificate
            if new_id != old_id:
                for record in records:
                    if record.get("proof_id") == old_id:
                        record["proof_id"] = new_id
        registry["proofs"][kind] = rebuilt
    registry["counts"] = {key: len(value) for key, value in registry["proofs"].items()}
    registry["payload_sha256"] = logical_payload(registry)
    registry_path = root / "restoration_proof_registry.json.gz"
    registry_path.write_bytes(gzip_bytes(
        json.dumps(registry, sort_keys=True, separators=(",", ":")).encode() + b"\n"
    ))
    for index, record in enumerate(records):
        record["edge_index"] = index
        payload = dict(record)
        payload.pop("row_sha256", None)
        record["row_sha256"] = sha(payload)
    ledger_path = root / "restoration_ledger.jsonl.gz"
    ledger_path.write_bytes(gzip_bytes(
        b"".join(canonical_bytes(record) + b"\n" for record in records)
    ))
    manifest["proof_registry"]["sha256"] = sha_file(registry_path)
    manifest["proof_registry"]["payload_sha256"] = registry["payload_sha256"]
    manifest["proof_registry"]["certificate_counts"] = registry["counts"]
    manifest["ledger"]["sha256"] = sha_file(ledger_path)
    manifest["ledger"]["rows"] = len(records)
    manifest["ledger"]["ordered_row_hash_root"] = sha(
        [record["row_sha256"] for record in records]
    )
    manifest["payload_sha256"] = logical_payload(manifest)
    (root / "RESTORATION_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )


def mutate_certificate(registry, kind, mutation):
    old_id = next(iter(registry["proofs"][kind]))
    certificate = registry["proofs"][kind][old_id]
    mutation(certificate)
    certificate["__old_id"] = old_id


def run_case(name, expected, mutation, baseline):
    manifest0, registry0, records0 = baseline
    with tempfile.TemporaryDirectory(prefix="k3p-restoration-mutation-") as temporary:
        root = Path(temporary)
        manifest = copy.deepcopy(manifest0)
        registry = copy.deepcopy(registry0)
        records = copy.deepcopy(records0)
        mutation(manifest, registry, records)
        reseal(root, manifest, registry, records)
        process = subprocess.run(
            [sys.executable, str(VERIFIER), "--artifact-only", "--package-dir", str(root)],
            cwd=HERE,
            text=True,
            capture_output=True,
            timeout=30,
        )
        combined = process.stdout + process.stderr
        require(process.returncode != 0, f"mutation unexpectedly passed:{name}")
        require(expected in combined,
                f"wrong failure class:{name}:expected={expected!r}:output={combined[-1000:]!r}")
        return {
            "mutation": name,
            "expected_failure_class": expected,
            "observed_failure_class": expected,
            "exit_code": process.returncode,
            "rejected": True,
        }


def main():
    require(__debug__ and not sys.flags.optimize, "optimized Python forbidden")
    manifest = json.loads((HERE / "RESTORATION_MANIFEST.json").read_text())
    registry = read_registry()
    records = read_ledger()
    baseline = (manifest, registry, records)

    def delete_row(_m, _p, rows):
        rows.pop(123)

    def duplicate_row(_m, _p, rows):
        rows.append(copy.deepcopy(rows[123]))

    def wrong_proof_reference(_m, _p, rows):
        row = next(item for item in rows if item["proof_kind"] == "k3p_tree_sunlet_sos")
        row["proof_id"] = "K3P-TS:" + "0" * 64

    def omit_registry_certificate(_m, proof, _rows):
        kind = "k3p_exact_multihomogeneous_quadratic"
        proof["proofs"][kind].pop(next(iter(proof["proofs"][kind])))

    def collapse_quartet(_m, proof, _rows):
        def change(cert):
            cert["source_splits"] = copy.deepcopy(cert["target_splits"])
        mutate_certificate(proof, "displayed_quartet_mismatch", change)

    def erase_sunlet_circuit(_m, proof, _rows):
        def change(cert):
            cert["sunlet_circuit_pullback_sha256"] = [sha([])] * 6
        mutate_certificate(proof, "k3p_tree_sunlet_sos", change)

    def impose_k2p_equality(_m, proof, _rows):
        proof["uses_k2p_sector_equality"] = True

    def restore_historical_algebra(_m, proof, _rows):
        proof["uses_historical_k2p_algebra"] = True

    def boundary_quadratic_witness(_m, proof, _rows):
        def change(cert):
            cert["strict_source_witness"]["inheritance"][0] = "0"
        mutate_certificate(proof, "k3p_exact_multihomogeneous_quadratic", change)

    def untransported_sector_swap(_m, proof, _rows):
        def change(cert):
            value = cert["terms"][0]["coordinate_indices"][1]
            cert["terms"][0]["coordinate_indices"][1] = (value + 1) % 64
            cert["terms"][0]["coordinate_indices"].sort()
        mutate_certificate(proof, "k3p_direct_marginal_quartic", change)

    def k2p_quartic_template(_m, proof, _rows):
        def change(cert):
            cert["template_file"] = "historical_F_2_112_k2p.json"
        mutate_certificate(proof, "k3p_direct_marginal_quartic", change)

    def target_openness(_m, proof, _rows):
        def change(cert):
            cert["target_marginal_openness_used"] = True
        mutate_certificate(proof, "k3p_direct_marginal_quartic", change)

    def conflate_minimal_count(m, _p, _r):
        m["census"]["minimal_k3p_terminal_rows"] = 36_792

    def conflate_legacy_count(m, _p, _r):
        m["census"]["legacy_full_forest_leaves"] = 36_568

    def activate_depth2(_m, _p, rows):
        row = next(item for item in rows if item["layer"] == 2)
        row["active_k3p_status"] = "separated"

    def retain_active_continuation(_m, _p, rows):
        row = next(item for item in rows if item.get("legacy_structural_status") == "continuation")
        row["active_k3p_status"] = "continuation"

    def break_parent_transport(_m, _p, rows):
        row = next(item for item in rows if item["layer"] == 1)
        row["source_parent_transport_id"] = "0" * 64

    def omit_second_child_same_count(_m, _p, rows):
        second = [index for index, row in enumerate(rows) if row["layer"] == 2]
        rows[second[1]] = copy.deepcopy(rows[second[0]])

    def active_continuation_count(m, _p, _r):
        m["census"]["active_k3p_continuations"] = 1

    cases = [
        ("delete_one_restoration_edge", "ledger row census", delete_row),
        ("duplicate_one_restoration_edge", "ledger row census", duplicate_row),
        ("reassign_proof_reference", "ledger proof reference", wrong_proof_reference),
        ("omit_quadratic_certificate", "ledger proof reference", omit_registry_certificate),
        ("collapse_quartet_mismatch", "quartet split mismatch", collapse_quartet),
        ("erase_sunlet_nonzero_circuits", "SOS nonzero census", erase_sunlet_circuit),
        ("impose_k2p_C_equals_T", "K2P sector equality forbidden", impose_k2p_equality),
        ("restore_historical_k2p_algebra", "historical K2P algebra forbidden", restore_historical_algebra),
        ("accept_boundary_inheritance", "quadratic witness inheritance", boundary_quadratic_witness),
        ("swap_sector_coordinate_without_transport", "quartic coordinate transport", untransported_sector_swap),
        ("reuse_k2p_quartic_template", "quartic active template whitelist", k2p_quartic_template),
        ("require_target_marginal_openness", "quartic target openness", target_openness),
        ("conflate_minimal_with_legacy_leaves", "minimal K3P terminal count", conflate_minimal_count),
        ("conflate_legacy_with_minimal_leaves", "legacy/full-forest leaf count", conflate_legacy_count),
        ("promote_redundant_depth2_to_active", "redundant depth-two marker", activate_depth2),
        ("retain_k3p_active_continuation", "first active K3P status", retain_active_continuation),
        ("break_first_parent_transport", "first parent transport reference", break_parent_transport),
        ("omit_second_child_replace_with_duplicate", "ledger/frozen structural identity", omit_second_child_same_count),
        ("claim_one_active_continuation", "legacy versus active continuation distinction", active_continuation_count),
    ]
    results = [run_case(name, expected, mutation, baseline)
               for name, expected, mutation in cases]

    optimized = subprocess.run(
        [sys.executable, "-O", str(VERIFIER), "--artifact-only", "--package-dir", str(HERE)],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=30,
    )
    combined = optimized.stdout + optimized.stderr
    require(optimized.returncode != 0 and "optimized Python forbidden" in combined,
            f"optimized-mode mutation not rejected:{combined[-1000:]}")
    results.append({
        "mutation": "optimized_mode_bypass",
        "expected_failure_class": "optimized Python forbidden",
        "observed_failure_class": "optimized Python forbidden",
        "exit_code": optimized.returncode,
        "rejected": True,
    })
    result = {
        "schema": "k3p-restoration-mutation-certificate-v1",
        "status": "PASS",
        "mutations": results,
        "mutation_count": len(results),
        "rejected": sum(row["rejected"] for row in results),
        "accepted": 0,
        "manifest_payload_sha256": manifest["payload_sha256"],
        "verifier_sha256": sha_file(VERIFIER),
    }
    result["payload_sha256"] = logical_payload(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "mutation_count": len(results),
        "rejected": len(results),
        "payload_sha256": result["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (MutationFailure, KeyError, IndexError, ValueError, OSError,
            subprocess.SubprocessError) as error:
        raise SystemExit(f"K3P_RESTORATION_MUTATION_FAIL:{error}") from error
