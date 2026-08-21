#!/usr/bin/env python3
"""Adversarial mutations for the restoration certificate and verifier."""
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "five_port_certificate.json"
VERIFIER = HERE / "verify_restoration_forest.py"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def rehash_row_and_certificate(payload, row_index):
    row = payload["algebra_rows"][row_index]
    old_hash = row["row_sha256"]
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    new_hash = digest(body)
    row["row_sha256"] = new_hash
    matches = [index for index, value in enumerate(payload["ordered_raw_child_hashes"]) if value == old_hash]
    if len(matches) != 1:
        raise RuntimeError(("row hash multiplicity", old_hash, matches))
    payload["ordered_raw_child_hashes"][matches[0]] = new_hash
    payload["ordered_raw_child_hash_root"] = digest(payload["ordered_raw_child_hashes"])
    payload["certificate_payload_sha256"] = digest({
        key: value for key, value in payload.items() if key != "certificate_payload_sha256"
    })


def run_mutation(name, payload, *, full=False, optimized=False):
    with tempfile.TemporaryDirectory(prefix=f"k2p-restoration-{name}-") as directory:
        path = Path(directory) / "certificate.json"
        path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
        command = [sys.executable]
        if optimized:
            command.append("-O")
        command.extend([str(VERIFIER), "--certificate", str(path)])
        if not full:
            command.append("--skip-regeneration")
        completed = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed.returncode == 0:
            raise RuntimeError(f"mutation survived: {name}: {completed.stdout}")
        return {
            "name": name,
            "rejected": True,
            "returncode": completed.returncode,
            "diagnostic": completed.stderr.strip().splitlines()[-1],
        }


def main():
    original = json.loads(CERTIFICATE.read_text())
    results = []

    quadratic = copy.deepcopy(original)
    q_index = next(
        index for index, row in enumerate(quadratic["algebra_rows"])
        if row["proof"] == "exact_multihomogeneous_quadratic"
    )
    quadratic["algebra_rows"][q_index]["coefficients"][0] += 1
    rehash_row_and_certificate(quadratic, q_index)
    results.append(run_mutation("quadratic_coefficient_outer_hashes_recomputed", quadratic))

    quartic = copy.deepcopy(original)
    f_index = next(
        index for index, row in enumerate(quartic["algebra_rows"])
        if row["proof"] == "inherited_exact_F_2_112_quartic"
    )
    quartic["algebra_rows"][f_index]["lifted_coordinate_monomials"][0][1] += 1
    rehash_row_and_certificate(quartic, f_index)
    results.append(run_mutation("quartic_coefficient_outer_hashes_recomputed", quartic))

    transport = copy.deepcopy(original)
    t_index = next(
        index for index, row in enumerate(transport["algebra_rows"])
        if row["remaining_roles"]
    )
    transport["algebra_rows"][t_index]["remaining_roles"] = []
    rehash_row_and_certificate(transport, t_index)
    results.append(run_mutation("remaining_role_transport_outer_hashes_recomputed", transport))

    optimized = copy.deepcopy(original)
    results.append(run_mutation("python_optimized_mode", optimized, optimized=True))

    raw_hash = copy.deepcopy(original)
    raw_hash["ordered_raw_child_hashes"][0] = "0" * 64
    raw_hash["ordered_raw_child_hash_root"] = digest(raw_hash["ordered_raw_child_hashes"])
    raw_hash["certificate_payload_sha256"] = digest({
        key: value for key, value in raw_hash.items() if key != "certificate_payload_sha256"
    })
    # Only a complete deterministic regeneration can detect a coherently
    # rehashed mutation of a topology-only child row.
    results.append(run_mutation("topology_child_hash_outer_hashes_recomputed", raw_hash, full=True))

    report = {"schema": "k2p-restoration-mutation-report-v1", "tests": results, "passed": len(results)}
    output = HERE / "mutation_report.json"
    output.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
