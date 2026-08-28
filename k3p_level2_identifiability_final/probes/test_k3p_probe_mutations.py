#!/usr/bin/env python3
"""Fail-closed mutation suite for the exact K3P probe-coherence release."""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
VERIFIER = HERE / "verify_k3p_probes.py"
OUTPUT = HERE / "K3P_PROBE_MUTATION_CERTIFICATE.json"
FILES = (
    "K3P_PROBE_COHERENCE_CERTIFICATE.json",
    "one_port_ledger.jsonl.gz",
    "two_port_parent_inventory.jsonl.gz",
    "two_port_ledger.jsonl.gz",
    "exact_transport_ledger.jsonl.gz",
    "parent_restriction_ledger.jsonl.gz",
    "separation_proof_registry.json.gz",
)


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
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class Ordered:
    def __init__(self):
        self.rows = 0
        self.root = sha([])

    def add(self, row):
        self.root = sha({"previous": self.root, "row_sha256": sha(row)})
        self.rows += 1

    def public(self):
        return {
            "algorithm": "root_0=sha256(canonical([])); root_n=sha256(canonical({previous:root_(n-1),row_sha256:h_n}))",
            "rows": self.rows,
            "ordered_hash_root": self.root,
        }


def write_gzip_json(path, value):
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as handle:
            handle.write(canonical_bytes(value) + b"\n")


def rewrite_jsonl(path, transform):
    source = path.with_suffix(path.suffix + ".source")
    path.rename(source)
    ordered = Ordered()
    counts = collections.Counter()
    rows = 0
    with gzip.open(source, "rt") as incoming, path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as compressed:
            for number, line in enumerate(incoming):
                row = transform(json.loads(line), number)
                if row is None:
                    continue
                compressed.write(canonical_bytes(row) + b"\n")
                ordered.add(row)
                rows += 1
                if "status" in row:
                    counts[row["status"]] += 1
    source.unlink()
    return ordered.public(), counts, rows


def load_certificate(root):
    return json.loads((root / "K3P_PROBE_COHERENCE_CERTIFICATE.json").read_text())


def seal_certificate(root, certificate):
    certificate.pop("payload_sha256", None)
    logical = dict(certificate)
    logical.pop("operational", None)
    certificate["payload_sha256"] = sha(logical)
    (root / "K3P_PROBE_COHERENCE_CERTIFICATE.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )


def update_one(root, transform):
    path = root / "one_port_ledger.jsonl.gz"
    ordered, counts, rows = rewrite_jsonl(path, transform)
    certificate = load_certificate(root)
    certificate["one_port"]["ledger_sha256"] = sha_file(path)
    certificate["one_port"]["ordered_ledger"] = ordered
    certificate["one_port"]["counts"] = dict(sorted(counts.items()))
    certificate["one_port"]["raw_pairs"] = rows
    certificate["one_port"]["equality_survivors"] = counts["isomorphic"] + counts["triangle"]
    seal_certificate(root, certificate)


def update_two(root, transform):
    path = root / "two_port_ledger.jsonl.gz"
    ordered, counts, rows = rewrite_jsonl(path, transform)
    reverse = collections.Counter()
    with gzip.open(path, "rt") as handle:
        for line in handle:
            row = json.loads(line)
            if "reverse_order_certificate" in row:
                reverse[row["reverse_order_certificate"]["reverse_parent_relation"]] += 1
    certificate = load_certificate(root)
    certificate["two_port"]["ledger_sha256"] = sha_file(path)
    certificate["two_port"]["ordered_ledger"] = ordered
    certificate["two_port"]["counts"] = dict(sorted(counts.items()))
    certificate["two_port"]["raw_pairs"] = rows
    certificate["two_port"]["equality_survivors"] = counts["isomorphic"] + counts["triangle"]
    certificate["two_port"]["reverse_order_parent_relation_counts"] = dict(sorted(reverse.items()))
    seal_certificate(root, certificate)


def update_parent_inventory(root, transform):
    path = root / "two_port_parent_inventory.jsonl.gz"
    ordered, _, rows = rewrite_jsonl(path, transform)
    certificate = load_certificate(root)
    certificate["two_port"]["parent_inventory_sha256"] = sha_file(path)
    certificate["two_port"]["ordered_parent_inventory"] = ordered
    certificate["two_port"]["parents"] = rows
    seal_certificate(root, certificate)


def update_streaming_store(root, filename, field, transform):
    path = root / filename
    ordered, _, rows = rewrite_jsonl(path, transform)
    certificate = load_certificate(root)
    certificate["registries"][field].update({
        "sha256": sha_file(path),
        "unique_records": rows,
        "ordered_records": ordered,
    })
    seal_certificate(root, certificate)


def update_proof_registry(root, transform):
    path = root / "separation_proof_registry.json.gz"
    with gzip.open(path, "rt") as handle:
        proof = json.load(handle)
    proof.pop("payload_sha256")
    transform(proof)
    proof["payload_sha256"] = sha(proof)
    write_gzip_json(path, proof)
    certificate = load_certificate(root)
    certificate["registries"]["separation"]["sha256"] = sha_file(path)
    certificate["registries"]["separation"]["payload_sha256"] = proof["payload_sha256"]
    seal_certificate(root, certificate)


def link_case(root):
    for filename in FILES:
        if filename == "K3P_PROBE_COHERENCE_CERTIFICATE.json":
            # Every mutation reseals the summary, so it must be a private copy.
            # Mutating through a symlink would corrupt the frozen source.
            shutil.copy2(HERE / filename, root / filename)
        else:
            os.symlink(HERE / filename, root / filename)


def make_writable(root, filename):
    path = root / filename
    source = path.resolve()
    path.unlink()
    shutil.copy2(source, path)


def run_verifier(root, optimized=False, hash_seed="37"):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(VERIFIER), "--package-dir", str(root), "--output", str(root / "verification.json")])
    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = hash_seed
    started = time.monotonic()
    result = subprocess.run(command, text=True, capture_output=True, env=environment)
    return {
        "returncode": result.returncode,
        "runtime_seconds": time.monotonic() - started,
        "output_tail": (result.stdout + result.stderr)[-600:],
    }


def mutate_omitted_anchor(root):
    certificate = load_certificate(root)
    certificate["anchor_inventory"]["public_anchors"].pop(0)
    seal_certificate(root, certificate)


def mutate_swapped_classifier(root):
    certificate = load_certificate(root)
    certificate["classifier_order"][0], certificate["classifier_order"][1] = (
        certificate["classifier_order"][1], certificate["classifier_order"][0]
    )
    seal_certificate(root, certificate)


def mutate_omitted_one(root):
    make_writable(root, "one_port_ledger.jsonl.gz")
    update_one(root, lambda row, number: None if number == 0 else row)


def mutate_wrong_one_parent(root):
    make_writable(root, "one_port_ledger.jsonl.gz")
    certificate = load_certificate(root)
    replacement = certificate["anchor_inventory"]["public_anchors"][1]["anchor_id"]
    def transform(row, number):
        if number == 0:
            row["parent_anchor_id"] = replacement
        return row
    update_one(root, transform)


def mutate_reassigned_k3p_separator(root):
    make_writable(root, "one_port_ledger.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        if not changed[0] and row["status"] == "k3p_tree_sunlet_sos":
            row["proof_id"] = "K3P-TS:" + "0" * 64
            changed[0] = True
        return row
    update_one(root, transform)
    require(changed[0], "no K3P tree-sunlet row to mutate")


def mutate_omitted_parent(root):
    make_writable(root, "two_port_parent_inventory.jsonl.gz")
    update_parent_inventory(root, lambda row, number: None if number == 0 else row)


def mutate_missing_root_site(root):
    make_writable(root, "two_port_parent_inventory.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        if not changed[0]:
            profile = row["source_candidate_profile"]
            index = next(i for i, site in enumerate(profile["sites"]) if site["site_type"] == "root_suppressed_segment")
            profile["sites"].pop(index)
            profile["site_count"] -= 1
            changed[0] = True
        return row
    update_parent_inventory(root, transform)
    require(changed[0], "no root site to mutate")


def mutate_omitted_two(root):
    make_writable(root, "two_port_ledger.jsonl.gz")
    update_two(root, lambda row, number: None if number == 0 else row)


def mutate_wrong_two_parent(root):
    make_writable(root, "two_port_ledger.jsonl.gz")
    with gzip.open(root / "two_port_parent_inventory.jsonl.gz", "rt") as handle:
        parent_ids = [json.loads(next(handle))["one_port_parent_id"] for _ in range(2)]
    def transform(row, number):
        if number == 0:
            row["one_port_parent_id"] = parent_ids[1]
        return row
    update_two(root, transform)


def mutate_reverse_order(root):
    make_writable(root, "two_port_ledger.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        if not changed[0] and "reverse_order_certificate" in row:
            row["reverse_order_certificate"]["reverse_parent_canonical_one_port_class_id"] = -1
            changed[0] = True
        return row
    update_two(root, transform)
    require(changed[0], "no reverse row to mutate")


def mutate_inconsistent_triangle(root):
    make_writable(root, "two_port_ledger.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        if not changed[0] and row.get("global_triangle_sha256") is not None:
            row["global_triangle_sha256"] = "0" * 64
            changed[0] = True
        return row
    update_two(root, transform)
    require(changed[0], "no global triangle row to mutate")


def mutate_broken_transport(root):
    make_writable(root, "exact_transport_ledger.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        if not changed[0]:
            row["record"]["vertex_map"][0][1] += "_corrupt"
            changed[0] = True
        return row
    update_streaming_store(root, "exact_transport_ledger.jsonl.gz", "exact_transports", transform)


def mutate_folded_transport(root):
    """Fold two source vertices onto one target while preserving row syntax."""
    make_writable(root, "exact_transport_ledger.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        vertex_map = row["record"]["vertex_map"]
        if not changed[0] and len(vertex_map) >= 2:
            vertex_map[0][1] = vertex_map[1][1]
            changed[0] = True
        return row
    update_streaming_store(root, "exact_transport_ledger.jsonl.gz", "exact_transports", transform)
    require(changed[0], "no transport available to fold")


def mutate_omitted_restriction(root):
    make_writable(root, "parent_restriction_ledger.jsonl.gz")
    update_streaming_store(
        root, "parent_restriction_ledger.jsonl.gz", "parent_restrictions",
        lambda row, number: None if number == 0 else row,
    )


def mutate_tree_circuit_deck(root):
    make_writable(root, "separation_proof_registry.json.gz")
    def transform(proof):
        certificates = proof["k3p_tree_sunlet_registry"]["certificates"]
        first = certificates[sorted(certificates)[0]]
        first["tree_circuit_pullback_sha256"][0] = "0" * 64
    update_proof_registry(root, transform)


def mutate_k2p_sector_equality(root):
    certificate = load_certificate(root)
    certificate["uses_k2p_sector_equality"] = True
    seal_certificate(root, certificate)


def mutate_separator_reference(root):
    make_writable(root, "separation_proof_registry.json.gz")
    def transform(proof):
        proof["k3p_tree_sunlet_registry"]["separator_certificate_sha256"] = "0" * 64
    update_proof_registry(root, transform)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--no-write-report", action="store_true")
    args = parser.parse_args(argv)
    require((HERE / "K3P_PROBE_COHERENCE_CERTIFICATE.json").exists(), "missing source certificate")
    cases = [
        ("omitted_anchor", mutate_omitted_anchor),
        ("swapped_classifier_precedence", mutate_swapped_classifier),
        ("omitted_one_port_probe", mutate_omitted_one),
        ("wrong_one_port_parent", mutate_wrong_one_parent),
        ("reassigned_K3P_tree_sunlet_certificate", mutate_reassigned_k3p_separator),
        ("omitted_two_port_parent", mutate_omitted_parent),
        ("missing_root_suppressed_site", mutate_missing_root_site),
        ("omitted_two_port_probe", mutate_omitted_two),
        ("wrong_two_port_parent", mutate_wrong_two_parent),
        ("reversed_order_class", mutate_reverse_order),
        ("inconsistent_global_triangle", mutate_inconsistent_triangle),
        ("broken_exact_transport", mutate_broken_transport),
        ("folded_exact_transport", mutate_folded_transport),
        ("omitted_parent_restriction", mutate_omitted_restriction),
        ("altered_tree_zero_circuit_deck", mutate_tree_circuit_deck),
        ("imposed_K2P_sector_equality", mutate_k2p_sector_equality),
        ("corrupted_six_circuit_separator_reference", mutate_separator_reference),
    ]
    results = []
    started = time.monotonic()
    for name, mutation in cases:
        with tempfile.TemporaryDirectory(prefix=f"k3p_probe_mutation_{name}_") as directory:
            root = Path(directory)
            link_case(root)
            mutation(root)
            replay = run_verifier(root)
            require(replay["returncode"] != 0, f"mutation survived:{name}:{replay}")
            results.append({"mutation": name, "rejected": True, **replay})
            print(json.dumps(results[-1], sort_keys=True), flush=True)
    with tempfile.TemporaryDirectory(prefix="k3p_probe_optimized_") as directory:
        root = Path(directory)
        link_case(root)
        replay = run_verifier(root, optimized=True)
        require(replay["returncode"] != 0, f"optimized mode survived:{replay}")
        results.append({"mutation": "optimized_mode", "rejected": True, **replay})
    with tempfile.TemporaryDirectory(prefix="k3p_probe_hashseed_") as directory:
        root = Path(directory)
        link_case(root)
        replay = run_verifier(root, hash_seed="12345")
        require(replay["returncode"] == 0, f"nondefault hash seed failed:{replay}")
        hash_seed_check = {"PYTHONHASHSEED": 12345, "status": "PASS", **replay}
    report = {
        "schema": "k3p-corrected-probe-mutations-v1",
        "status": "PASS",
        "source_certificate_sha256": sha_file(HERE / "K3P_PROBE_COHERENCE_CERTIFICATE.json"),
        "source_verifier_sha256": sha_file(VERIFIER),
        "mutations_attempted": len(results),
        "mutations_rejected": sum(row["rejected"] for row in results),
        "cases": results,
        "nondefault_hash_seed_replay": hash_seed_check,
        "operational": {"runtime_seconds": time.monotonic() - started},
    }
    logical = dict(report)
    logical.pop("operational")
    report["payload_sha256"] = sha(logical)
    require(not (args.no_write_report and args.output != OUTPUT),
            "choose either --output or --no-write-report")
    if not args.no_write_report:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS", "mutations": len(results),
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (MutationFailure, KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_PROBE_MUTATION_FAIL:{error}") from error
