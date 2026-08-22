#!/usr/bin/env python3
"""Fail-closed mutations for the corrected raw-four terminal overlay."""

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
CERTIFICATE = HERE / "raw4_corrected_terminal_ledger.json"
VERIFIER = HERE / "verify_raw4_corrected_terminal_ledger.py"
OUTPUT = HERE / "raw4_mutation_certificate.json"


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def rehash(document):
    document["coverage_row_hashes"] = [sha(row) for row in document["coverage"]]
    document["coverage_hash_root"] = sha(document["coverage_row_hashes"])
    document.pop("payload_sha256", None)
    document["payload_sha256"] = sha(document)
    return document


def mutate_omitted_raw(document):
    removed = document["coverage"].pop(0)
    document["corrected_rows"] -= 1
    document["raw_id_unique"] -= 1
    document["corrected_category_census"]["exact_exclusion"] -= 1
    document["corrected_reason_census"]["full_map_Ti_strict_sign"] -= 1
    class_id = removed["descriptor_pair_class_id"]
    document["descriptor_pair_classes"][class_id]["raw_multiplicity"] -= 1
    key = f"{removed['source_pullback_sha256']}:{removed['target_pullback_sha256']}"
    document["canonical_relation_class_multiplicities"][key] -= 1


def mutate_reassigned_raw(document):
    document["coverage"][0]["raw_id"] = document["coverage"][1]["raw_id"]


def mutate_wrong_transport(document):
    row = document["coverage"][0]
    row["port_permutation"][0], row["port_permutation"][1] = (
        row["port_permutation"][1], row["port_permutation"][0]
    )


def mutate_reassigned_polynomial(document):
    row = document["coverage"][0]
    alternatives = sorted(set(document["sign_certificates"]) - {row["source_pullback_sha256"]})
    old_key = f"{row['source_pullback_sha256']}:{row['target_pullback_sha256']}"
    new_hash = alternatives[0]
    new_key = f"{new_hash}:{row['target_pullback_sha256']}"
    document["canonical_relation_class_multiplicities"][old_key] -= 1
    document["canonical_relation_class_multiplicities"][new_key] = (
        document["canonical_relation_class_multiplicities"].get(new_key, 0) + 1
    )
    row["source_pullback_sha256"] = new_hash
    row["source_pullback_term_count"] = document["sign_certificates"][new_hash]["source_pullback_term_count"]


def mutate_bernstein_coefficient(document):
    key = sorted(document["sign_certificates"])[0]
    sign = document["sign_certificates"][key]["sign_certificate"]
    sign["minimum_coefficient"] = "-999999"
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_bernstein_tensor_count(document):
    key = sorted(document["sign_certificates"])[0]
    sign = document["sign_certificates"][key]["sign_certificate"]
    sign["negative_coefficients"] += 1
    sign["zero_coefficients"] -= 1
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_reversed_sign(document):
    key = sorted(document["sign_certificates"])[0]
    sign = document["sign_certificates"][key]["sign_certificate"]
    sign["conclusion"] = "strictly_positive"
    sign.pop("certificate_sha256", None)
    sign["certificate_sha256"] = sha(sign)


def mutate_descriptor_reassignment(document):
    document["coverage"][0]["descriptor_pair_class_id"] = 1


def run_verifier(certificate_path, report_path, optimized=False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(VERIFIER),
        "--certificate", str(certificate_path),
        "--report", str(report_path),
    ])
    environment = dict(os.environ)
    environment["PYTHONHASHSEED"] = "17"
    return subprocess.run(command, text=True, capture_output=True, env=environment)


def main():
    original = json.loads(CERTIFICATE.read_text())
    mutations = [
        ("omitted_raw_record", mutate_omitted_raw),
        ("reassigned_raw_record", mutate_reassigned_raw),
        ("wrong_port_transport", mutate_wrong_transport),
        ("reassigned_polynomial_certificate", mutate_reassigned_polynomial),
        ("mutated_Bernstein_coefficient", mutate_bernstein_coefficient),
        ("mutated_Bernstein_tensor_entry_count", mutate_bernstein_tensor_count),
        ("reversed_sign_conclusion", mutate_reversed_sign),
        ("reassigned_descriptor_class", mutate_descriptor_reassignment),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix="raw4_mutations_") as temporary:
        temporary = Path(temporary)
        for name, mutation in mutations:
            candidate = copy.deepcopy(original)
            mutation(candidate)
            rehash(candidate)
            candidate_path = temporary / f"{name}.json"
            candidate_path.write_text(json.dumps(candidate, sort_keys=True) + "\n")
            completed = run_verifier(candidate_path, temporary / f"{name}.report.json")
            if completed.returncode == 0:
                raise SystemExit(f"RAW4_MUTATION_SURVIVED:{name}")
            diagnostic = (completed.stderr + completed.stdout).strip().splitlines()
            if not diagnostic or "RAW4_CORRECTED_REPLAY_FAIL:" not in diagnostic[-1]:
                raise SystemExit(f"RAW4_MUTATION_BAD_DIAGNOSTIC:{name}:{diagnostic[-3:]}")
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
        if optimized.returncode == 0:
            raise SystemExit("RAW4_MUTATION_SURVIVED:optimized_mode")
        diagnostic = (optimized.stderr + optimized.stdout).strip().splitlines()
        if not diagnostic or "RAW4_CORRECTED_REPLAY_OPTIMIZED_MODE_FORBIDDEN" not in diagnostic[-1]:
            raise SystemExit(f"RAW4_OPTIMIZED_BAD_DIAGNOSTIC:{diagnostic[-3:]}")
        results.append({
            "mutation": "python_optimized_mode",
            "rejected": True,
            "return_code": optimized.returncode,
            "diagnostic": diagnostic[-1],
        })

    report = {
        "schema": "k2p-raw4-corrected-mutations-v1",
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
