#!/usr/bin/env python3
"""Fail-closed mutations for the theta2 full-map truth certificate."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CERTIFICATE = PROJECT / "work/adversarial_proof_review/theta2_tree_sunlet_full_map_certificate.json"
VERIFIER = HERE / "verify_theta2_full_map_independent.py"
OUTPUT = HERE / "theta2_mutation_certificate.json"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def rehash(document):
    document["ordered_truth_row_hash_root"] = sha(document["ordered_truth_row_hashes"])
    document.pop("payload_sha256", None)
    document["payload_sha256"] = sha(document)


def mutate_omitted_row(document):
    document["ordered_truth_row_hashes"].pop(0)
    document["claimed_rows"] -= 1
    document["full_map_source_zero_rows"] -= 1
    document["full_map_strict_target_sign_rows"] -= 1


def mutate_reassigned_row(document):
    document["ordered_truth_row_hashes"][0] = document["ordered_truth_row_hashes"][1]


def first_sign(document):
    key = sorted(document["sign_certificates"])[0]
    return key, document["sign_certificates"][key]


def mutate_missing_target_presentation(document):
    _, record = first_sign(document)
    record["target_presentations"].pop(0)


def mutate_wrong_target_orientation(document):
    _, record = first_sign(document)
    presentation = record["target_presentations"][0]
    presentation[2] = next(label for label in presentation[1] if label != presentation[2])


def mutate_bernstein_coefficient(document):
    _, record = first_sign(document)
    sign = record["sign"]
    sign["minimum_coefficient"] = "-123456789"
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_bernstein_tensor_count(document):
    _, record = first_sign(document)
    sign = record["sign"]
    sign["negative_coefficients"] += 1
    sign["zero_coefficients"] -= 1
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_relation_multiplicity(document):
    key = sorted(document["canonical_relation_class_multiplicities"])[0]
    document["canonical_relation_class_multiplicities"][key] += 1


def mutate_source_zero_count(document):
    document["full_map_source_zero_rows"] -= 1


def mutate_graph_relation_count(document):
    document["exact_full_graph_relation_census"] = {"none": 2527, "isomorphic": 1}
    document["false_iso_or_triangle_conflicts"] = 1


def run_verifier(certificate, report, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([str(VERIFIER), "--certificate", str(certificate), "--report", str(report)])
    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = "29"
    return subprocess.run(command, capture_output=True, text=True, env=environment)


def main():
    original = json.loads(CERTIFICATE.read_text())
    mutations = [
        ("omitted_truth_row", mutate_omitted_row),
        ("reassigned_truth_row", mutate_reassigned_row),
        ("missing_target_presentation", mutate_missing_target_presentation),
        ("wrong_target_orientation", mutate_wrong_target_orientation),
        ("mutated_Bernstein_coefficient", mutate_bernstein_coefficient),
        ("mutated_Bernstein_tensor_entry_count", mutate_bernstein_tensor_count),
        ("reassigned_relation_multiplicity", mutate_relation_multiplicity),
        ("wrong_source_zero_count", mutate_source_zero_count),
        ("wrong_graph_relation_count", mutate_graph_relation_count),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="theta2_sign_mutations_") as temporary:
        temporary = Path(temporary)
        for name, mutation in mutations:
            candidate = copy.deepcopy(original)
            mutation(candidate)
            rehash(candidate)
            candidate_path = temporary / f"{name}.json"
            candidate_path.write_text(json.dumps(candidate, sort_keys=True) + "\n")
            completed = run_verifier(candidate_path, temporary / f"{name}.report.json")
            diagnostic = (completed.stderr + completed.stdout).strip().splitlines()
            if completed.returncode == 0:
                raise SystemExit(f"THETA2_MUTATION_SURVIVED:{name}")
            if not diagnostic or "THETA2_FULL_MAP_REPLAY_FAIL:" not in diagnostic[-1]:
                raise SystemExit(f"THETA2_MUTATION_BAD_DIAGNOSTIC:{name}:{diagnostic[-3:]}")
            results.append({
                "mutation": name,
                "rejected": True,
                "return_code": completed.returncode,
                "diagnostic": diagnostic[-1],
            })

        optimized = run_verifier(
            CERTIFICATE,
            temporary / "optimized.report.json",
            optimized=True,
        )
        diagnostic = (optimized.stderr + optimized.stdout).strip().splitlines()
        if optimized.returncode == 0:
            raise SystemExit("THETA2_MUTATION_SURVIVED:optimized_mode")
        if not diagnostic or "THETA2_FULL_MAP_REPLAY_OPTIMIZED_MODE_FORBIDDEN" not in diagnostic[-1]:
            raise SystemExit(f"THETA2_OPTIMIZED_BAD_DIAGNOSTIC:{diagnostic[-3:]}")
        results.append({
            "mutation": "python_optimized_mode",
            "rejected": True,
            "return_code": optimized.returncode,
            "diagnostic": diagnostic[-1],
        })

    report = {
        "schema": "k2p-theta2-full-map-mutations-v1",
        "status": "PASS",
        "source_certificate_sha256": hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "mutation_count": len(results),
        "survived": 0,
        "results": results,
    }
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": report["status"],
        "mutations": report["mutation_count"],
        "survived": report["survived"],
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
