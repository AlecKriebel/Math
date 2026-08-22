#!/usr/bin/env python3
"""Fail-closed mutations for the independent coherent-probe structural replay."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SOURCE = PROJECT / "work/probe_coherence_closure/probe_certificate.json"
VERIFIER = HERE / "verify_probe_certificate_structure.py"
OUTPUT = HERE / "probe_structural_mutation_certificate.json"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def resign(certificate):
    certificate.pop("payload_sha256", None)
    certificate["payload_sha256"] = sha(certificate)


def mutate_omitted_anchor_coverage(certificate):
    coverage = certificate["anchors"]["canonical_raw_coverage"]
    key = next(key for key, values in coverage.items() if values)
    coverage[key].pop()


def mutate_wrong_parent_transport(certificate):
    certificate["one_port"]["survivors"][0]["parent_transport_sha256"] = "0" * 64


def mutate_wrong_insertion(certificate):
    row = certificate["one_port"]["survivors"][0]
    row["source_insertion_index"] += 1


def mutate_broken_global_triangle(certificate):
    row = next(row for row in certificate["two_port"]["survivors"] if row["global_triangle"] is not None)
    row["global_triangle"]["source_triangle_edges"] = list(reversed(row["global_triangle"]["source_triangle_edges"]))


def mutate_reassigned_quadratic(certificate):
    # Change the row-to-descriptor assignment while consistently updating its
    # local row hash.  The independent census/class binding must still reject it.
    bindings = certificate["cycle_terminal_inventory"]["physical_equal_topology_raw_bindings"]
    hashes = certificate["cycle_terminal_inventory"]["physical_equal_topology_raw_binding_hashes"]
    old = bindings[0]["descriptor_pair_class_id"]
    bindings[0]["descriptor_pair_class_id"] = next(
        row["descriptor_pair_class_id"] for row in bindings if row["descriptor_pair_class_id"] != old
    )
    hashes[0] = sha(bindings[0])


def mutate_unsafe_cache_substitution(certificate):
    certificate["reviewed_39_anchor_regression"]["one_port"] = dict(
        certificate["optimization_adversarial_regression"]["unsafe_reviewed_39_A_plus_p"]
    )


MUTATIONS = {
    "omitted_anchor_coverage": mutate_omitted_anchor_coverage,
    "wrong_parent_transport": mutate_wrong_parent_transport,
    "wrong_insertion": mutate_wrong_insertion,
    "broken_global_triangle": mutate_broken_global_triangle,
    "reassigned_cycle_quadratic": mutate_reassigned_quadratic,
    "unsafe_topology_cache": mutate_unsafe_cache_substitution,
}


def main():
    outcomes = {}
    for name, mutation in MUTATIONS.items():
        certificate = json.loads(SOURCE.read_text())
        mutation(certificate)
        resign(certificate)
        with tempfile.TemporaryDirectory(prefix="k2p_probe_mutation_") as tmp:
            path = Path(tmp) / "mutated.json"
            path.write_text(json.dumps(certificate, sort_keys=True))
            run = subprocess.run(
                [sys.executable, "-B", str(VERIFIER), "--certificate", str(path)],
                cwd=PROJECT,
                capture_output=True,
                text=True,
            )
        if run.returncode == 0:
            raise SystemExit(f"MUTATION_SURVIVED:{name}")
        diagnostic = (run.stderr or run.stdout).strip().splitlines()[-1]
        if not diagnostic.startswith("PROBE_STRUCTURAL_REPLAY_FAIL:"):
            raise SystemExit(f"NON_FAIL_CLOSED_DIAGNOSTIC:{name}:{diagnostic}")
        outcomes[name] = {"status": "REJECTED", "diagnostic": diagnostic}

    report = {
        "schema": "k2p-coherent-probe-structural-mutations-v1",
        "status": "PASS",
        "mutations": outcomes,
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
