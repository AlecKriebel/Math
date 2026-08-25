#!/usr/bin/env python3
"""Adversarial mutation suite for the independent signed-pair verifier."""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "SIGNED_PAIR_CERTIFICATES.json"
VERIFIER = HERE / "verify_signed_pair_certificates.py"
REPORT = HERE / "ADVERSARIAL_MUTATION_REPORT.json"


def digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def rebind_records(manifest):
    manifest["records_sha256"] = digest(manifest["records"])


def run_verifier(path):
    return subprocess.run(
        [
            sys.executable,
            str(VERIFIER),
            "--manifest",
            str(path),
            "--no-report",
        ],
        cwd=HERE,
        text=True,
        capture_output=True,
        check=False,
    )


def changed_hex(value):
    return ("0" if value[0] != "0" else "1") + value[1:]


def mutation_cases(base):
    cases = []
    for position, record in enumerate(base["records"]):
        def flip_operator(manifest, position=position):
            coefficient = manifest["records"][position]["selection"][
                "combination_coefficients"
            ][1]
            manifest["records"][position]["selection"]["combination_coefficients"][1] = -coefficient
            rebind_records(manifest)

        cases.append(
            (
                f"operator_flip_target_{record['target_index']}",
                "flip the signed-minor operator while rebinding the aggregate record hash",
                flip_operator,
            )
        )

    def target_index(manifest):
        manifest["records"][0]["target_index"] += 1
        rebind_records(manifest)

    def record_id(manifest):
        manifest["records"][1]["record_id"] += 1000
        rebind_records(manifest)

    def old_order(manifest):
        order = manifest["records"][2]["old_order"]
        order[0], order[1] = order[1], order[0]
        rebind_records(manifest)

    def descriptor_hash(manifest):
        record = manifest["records"][3]
        record["descriptor_sha256"] = changed_hex(record["descriptor_sha256"])
        rebind_records(manifest)

    def output_hash(manifest):
        record = manifest["records"][4]
        record["output_polynomial_family_sha256"] = changed_hex(
            record["output_polynomial_family_sha256"]
        )
        rebind_records(manifest)

    def left_minor_hash(manifest):
        polynomial = manifest["records"][5]["polynomials"]
        polynomial["left_minor_sha256"] = changed_hex(polynomial["left_minor_sha256"])
        rebind_records(manifest)

    def reduced_coefficient(manifest):
        polynomial = manifest["records"][6]["polynomials"]["reduced_polynomial"]
        polynomial[0][1] = str(int(polynomial[0][1]) + 1)
        rebind_records(manifest)

    def numerator_hash(manifest):
        bernstein = manifest["records"][7]["bernstein"]
        bernstein["ordered_numerators_sha256"] = changed_hex(
            bernstein["ordered_numerators_sha256"]
        )
        rebind_records(manifest)

    def nonzero_numerator(manifest):
        bernstein = manifest["records"][8]["bernstein"]
        bernstein["nonzero_coefficients"][0]["numerator"] += 1
        rebind_records(manifest)

    def common_monomial(manifest):
        polynomial = manifest["records"][9]["polynomials"]
        polynomial["positive_monomial_exponent"][0] += 1
        rebind_records(manifest)

    def candidates_tested(manifest):
        manifest["records"][10]["selection"]["candidates_tested"] += 1
        rebind_records(manifest)

    def character_sum(manifest):
        manifest["records"][11]["selection"]["character_sums"][1] = 2
        rebind_records(manifest)

    def rows(manifest):
        manifest["records"][0]["selection"]["rows"] = [0, 2]
        rebind_records(manifest)

    def coordinate(manifest):
        manifest["records"][1]["selection"]["left_coordinate_indices"][0] += 1
        rebind_records(manifest)

    def degree(manifest):
        manifest["records"][2]["bernstein"]["degrees"][0] += 1
        rebind_records(manifest)

    def positivity_count(manifest):
        manifest["records"][3]["bernstein"]["negative"] = 1
        rebind_records(manifest)

    def delete_record(manifest):
        del manifest["records"][4]
        rebind_records(manifest)

    def swap_records(manifest):
        manifest["records"][5], manifest["records"][6] = (
            manifest["records"][6],
            manifest["records"][5],
        )
        rebind_records(manifest)

    def frozen_hash(manifest):
        value = manifest["inputs"]["primitive_certificate_sha256"]
        manifest["inputs"]["primitive_certificate_sha256"] = changed_hex(value)

    def producer_hash(manifest):
        value = manifest["inputs"]["producer_sha256"]
        manifest["inputs"]["producer_sha256"] = changed_hex(value)

    def aggregate_hash(manifest):
        manifest["records_sha256"] = changed_hex(manifest["records_sha256"])

    cases.extend(
        (
            ("target_index", "change a target index", target_index),
            ("record_id", "change a frozen primitive record id", record_id),
            ("old_order", "transpose two normalized port labels", old_order),
            ("descriptor_hash", "change the exact descriptor hash", descriptor_hash),
            ("output_family_hash", "change the output-polynomial family hash", output_hash),
            ("left_minor_hash", "change a selected minor hash", left_minor_hash),
            ("reduced_coefficient", "change an explicit reduced-polynomial coefficient", reduced_coefficient),
            ("bernstein_hash", "change the ordered Bernstein-numerator hash", numerator_hash),
            ("bernstein_nonzero", "change a nonzero Bernstein numerator", nonzero_numerator),
            ("common_monomial", "change the factored positive monomial", common_monomial),
            ("candidate_ordinal", "change the deterministic-search ordinal", candidates_tested),
            ("character_sum", "change a selected character block", character_sum),
            ("row_pair", "change a selected row pair", rows),
            ("coordinate_index", "change a selected Fourier coordinate", coordinate),
            ("bernstein_degree", "change a tensor Bernstein degree", degree),
            ("positivity_count", "assert a spurious negative coefficient", positivity_count),
            ("record_deletion", "delete one theorem record and rebind", delete_record),
            ("record_permutation", "swap two theorem records and rebind", swap_records),
            ("frozen_input_hash", "change the frozen input binding", frozen_hash),
            ("producer_hash", "change the producer source binding", producer_hash),
            ("aggregate_hash", "change only the aggregate record hash", aggregate_hash),
        )
    )
    return cases


def atomic_write(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def main():
    base = json.loads(MANIFEST.read_text())
    baseline = run_verifier(MANIFEST)
    if baseline.returncode != 0:
        raise RuntimeError(f"baseline verifier failed: {baseline.stdout}{baseline.stderr}")
    results = []
    with tempfile.TemporaryDirectory(prefix="mutation-", dir=HERE) as temporary_directory:
        temporary_path = Path(temporary_directory)
        for index, (identifier, description, mutate) in enumerate(mutation_cases(base)):
            candidate = copy.deepcopy(base)
            mutate(candidate)
            path = temporary_path / f"{index:03d}.json"
            path.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n")
            completed = run_verifier(path)
            rejected = completed.returncode != 0
            if not rejected:
                raise AssertionError(f"mutation escaped verification: {identifier}")
            error_record = None
            if completed.stdout.strip():
                try:
                    error_record = json.loads(completed.stdout.strip().splitlines()[-1]).get("error")
                except json.JSONDecodeError:
                    error_record = completed.stdout.strip()[-500:]
            results.append(
                {
                    "id": identifier,
                    "description": description,
                    "rejected": True,
                    "verifier_error": error_record,
                }
            )
    report = {
        "schema": "k3p-signed-pair-adversarial-mutations-v1",
        "status": "PASS",
        "baseline_passed": True,
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "mutation_count": len(results),
        "rejected_count": sum(row["rejected"] for row in results),
        "all_mutations_rejected": all(row["rejected"] for row in results),
        "mutations": results,
    }
    atomic_write(REPORT, report)
    print(
        json.dumps(
            {
                "status": report["status"],
                "mutation_count": report["mutation_count"],
                "rejected_count": report["rejected_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
