#!/usr/bin/env python3
"""Fail-closed mutations for the clean corrected restoration release."""

from __future__ import annotations

import copy
import gc
import hashlib
import json
import os
import resource
import subprocess
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "corrected_restoration_forest.json"
CROSSWALK = HERE / "corrected_restoration_historical_crosswalk.json"
VERIFIER = HERE / "verify_corrected_restoration_forest.py"
OUTPUT = HERE / "corrected_restoration_mutation_certificate.json"


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def sha_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rehash_clean(certificate):
    for row in certificate["first_coverage"]:
        row.pop("row_sha256", None)
        row["row_sha256"] = sha(row)
    for row in certificate["second_coverage"]:
        parent = certificate["first_coverage"][row["parent_first_coverage_index"]]
        row["parent_first_row_sha256"] = parent["row_sha256"]
        row.pop("row_sha256", None)
        row["row_sha256"] = sha(row)
    first_hashes = [row["row_sha256"] for row in certificate["first_coverage"]]
    second_hashes = [row["row_sha256"] for row in certificate["second_coverage"]]
    certificate["first_row_hashes"] = first_hashes
    certificate["first_hash_root"] = sha(first_hashes)
    certificate["second_row_hashes"] = second_hashes
    certificate["second_hash_root"] = sha(second_hashes)


def sync_crosswalk(certificate, crosswalk):
    require(
        len(certificate["first_coverage"]) == len(crosswalk["first_coverage"]),
        "sync first length",
    )
    require(
        len(certificate["second_coverage"]) == len(crosswalk["second_coverage"]),
        "sync second length",
    )
    for clean, provenance in zip(certificate["first_coverage"], crosswalk["first_coverage"]):
        provenance["clean_row_sha256"] = clean["row_sha256"]
        provenance["source_parent_transport_id"] = clean["source_parent_transport_id"]
        provenance["target_parent_transport_id"] = clean["target_parent_transport_id"]
        provenance["corrected_status"] = clean["status"]
        provenance["corrected_proof"] = clean["proof"]
        for field in ("certificate", "certificate_sha256"):
            if field in clean:
                provenance[field] = copy.deepcopy(clean[field])
            else:
                provenance.pop(field, None)
        provenance.pop("corrected_row_sha256", None)
        clean_hash = provenance.pop("clean_row_sha256")
        provenance["corrected_row_sha256"] = sha(provenance)
        provenance["clean_row_sha256"] = clean_hash
    for clean, provenance in zip(certificate["second_coverage"], crosswalk["second_coverage"]):
        provenance["clean_row_sha256"] = clean["row_sha256"]
        for field in (
            "status",
            "proof",
            "certificate",
            "certificate_sha256",
            "source_parent_mixed_graph_sha256",
            "target_parent_mixed_graph_sha256",
        ):
            if field in clean:
                provenance[field] = copy.deepcopy(clean[field])
            else:
                provenance.pop(field, None)
        provenance.pop("row_sha256", None)
        clean_hash = provenance.pop("clean_row_sha256")
        provenance["row_sha256"] = sha(provenance)
        provenance["clean_row_sha256"] = clean_hash
    old_first = [row["corrected_row_sha256"] for row in crosswalk["first_coverage"]]
    old_second = [row["row_sha256"] for row in crosswalk["second_coverage"]]
    clean_first = [row["row_sha256"] for row in certificate["first_coverage"]]
    clean_second = [row["row_sha256"] for row in certificate["second_coverage"]]
    crosswalk["first_row_hashes"] = old_first
    crosswalk["first_hash_root"] = sha(old_first)
    crosswalk["second_row_hashes"] = old_second
    crosswalk["second_hash_root"] = sha(old_second)
    crosswalk["clean_first_row_hashes"] = clean_first
    crosswalk["clean_first_hash_root"] = sha(clean_first)
    crosswalk["clean_second_row_hashes"] = clean_second
    crosswalk["clean_second_hash_root"] = sha(clean_second)


def finalize_case(certificate, crosswalk, directory, *, sync=True, optimized=False):
    certificate.pop("payload_sha256", None)
    crosswalk.pop("payload_sha256", None)
    if sync:
        rehash_clean(certificate)
        sync_crosswalk(certificate, crosswalk)
    crosswalk["payload_sha256"] = sha(crosswalk)
    crosswalk_path = directory / "crosswalk.json"
    crosswalk_bytes = encoded(crosswalk)
    crosswalk_path.write_bytes(crosswalk_bytes)
    certificate["inputs"]["provenance_crosswalk_sha256"] = hashlib.sha256(
        crosswalk_bytes
    ).hexdigest()
    certificate["inputs"]["provenance_crosswalk_payload_sha256"] = crosswalk[
        "payload_sha256"
    ]
    certificate["payload_sha256"] = sha(certificate)
    certificate_path = directory / "certificate.json"
    certificate_path.write_bytes(encoded(certificate))
    # The verifier is intentionally independent.  Release the two large
    # in-memory JSON trees before spawning it so the mutation harness remains
    # comfortably below the referee memory cap.
    certificate.clear()
    crosswalk.clear()
    gc.collect()
    report_path = directory / "report.json"
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend([
        str(VERIFIER),
        "--certificate",
        str(certificate_path),
        "--crosswalk",
        str(crosswalk_path),
        "--report",
        str(report_path),
    ])
    started = time.monotonic()
    try:
        run = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=180,
            check=False,
        )
        output = run.stdout.strip()
        return {
            "returncode": run.returncode,
            "runtime_seconds": time.monotonic() - started,
            "output_tail": output[-800:],
            "rejected": run.returncode != 0,
        }
    except subprocess.TimeoutExpired as error:
        output = (error.stdout or "") + (error.stderr or "")
        return {
            "returncode": None,
            "runtime_seconds": time.monotonic() - started,
            "output_tail": str(output)[-800:],
            "rejected": False,
            "timeout": True,
        }


def first_index(certificate, proof):
    return next(index for index, row in enumerate(certificate["first_coverage"]) if row["proof"] == proof)


def run_case(name, mutate, *, sync=True, optimized=False):
    certificate = json.loads(CERTIFICATE.read_text())
    crosswalk = json.loads(CROSSWALK.read_text())
    mutate(certificate, crosswalk)
    with tempfile.TemporaryDirectory(prefix=f"k2p-restoration-{name}-") as temporary:
        result = finalize_case(
            certificate,
            crosswalk,
            Path(temporary),
            sync=sync,
            optimized=optimized,
        )
    result["mutation"] = name
    require(result["rejected"], f"mutation survived:{name}:{result}")
    print(json.dumps(result, sort_keys=True), flush=True)
    return result


def main():
    if not __debug__:
        raise Failure("MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN")
    started = time.monotonic()

    def omitted_clean_first(certificate, crosswalk):
        certificate["first_coverage"].pop(0)
        certificate["first_row_hashes"].pop(0)
        certificate["first_hash_root"] = sha(certificate["first_row_hashes"])

    def omitted_provenance(certificate, crosswalk):
        crosswalk["first_coverage"].pop(0)

    def wrong_parent_transport(certificate, crosswalk):
        row = certificate["first_coverage"][0]
        alternatives = sorted(certificate["first_source_transport_certificates"])
        row["source_parent_transport_id"] = next(
            item for item in alternatives if item != row["source_parent_transport_id"]
        )

    def broken_transport_payload(certificate, crosswalk):
        row = certificate["first_coverage"][0]
        old_id = row["target_parent_transport_id"]
        record = certificate["first_target_transport_certificates"].pop(old_id)
        record["parent_mixed_graph_sha256"] = "0" * 64
        record["restricted_child_mixed_graph_sha256"] = "0" * 64
        new_id = sha(record)
        certificate["first_target_transport_certificates"][new_id] = record
        for candidate in certificate["first_coverage"]:
            if candidate["target_parent_transport_id"] == old_id:
                candidate["target_parent_transport_id"] = new_id

    def reassigned_quartet(certificate, crosswalk):
        rows = [row for row in certificate["first_coverage"] if row["proof"] == "displayed_quartet_mismatch"]
        replacement = next(
            row for row in rows[1:]
            if row["certificate_sha256"] != rows[0]["certificate_sha256"]
        )
        rows[0]["certificate_sha256"] = replacement["certificate_sha256"]

    def reassigned_t(certificate, crosswalk):
        rows = [row for row in certificate["first_coverage"] if row["proof"] == "full_map_Ti_zero_strict_sign"]
        replacement = next(row for row in rows[1:] if row["certificate"] != rows[0]["certificate"])
        rows[0]["certificate"] = copy.deepcopy(replacement["certificate"])

    def altered_bernstein(certificate, crosswalk):
        index = first_index(certificate, "full_map_Ti_zero_strict_sign")
        signed_hash = certificate["first_coverage"][index]["certificate"]["signed_pullback_sha256"]
        bernstein = certificate["sign_certificates"][signed_hash]["bernstein"]
        bernstein["minimum_coefficient"] = "0"
        bernstein.pop("certificate_sha256", None)
        bernstein["certificate_sha256"] = sha(bernstein)

    def invalid_physical_witness(certificate, crosswalk):
        index = first_index(certificate, "exact_multihomogeneous_quadratic")
        old_id = certificate["first_coverage"][index]["certificate_sha256"]
        proof = certificate["algebra_certificates"].pop(old_id)
        proof["strict_D_plus_witness"]["edge_pairs"][0][0] = "2"
        new_id = sha(proof)
        certificate["algebra_certificates"][new_id] = proof
        for row in certificate["first_coverage"]:
            if row.get("certificate_sha256") == old_id:
                row["certificate_sha256"] = new_id

    def reassigned_quartic(certificate, crosswalk):
        rows = [row for row in certificate["first_coverage"] if row["proof"] == "inherited_exact_F_2_112_quartic"]
        replacement = next(row for row in rows[1:] if row["certificate_sha256"] != rows[0]["certificate_sha256"])
        rows[0]["certificate_sha256"] = replacement["certificate_sha256"]

    def omitted_second(certificate, crosswalk):
        certificate["second_coverage"].pop(0)
        certificate["second_row_hashes"].pop(0)
        certificate["second_hash_root"] = sha(certificate["second_row_hashes"])

    def wrong_second_parent(certificate, crosswalk):
        continuations = [
            index for index, row in enumerate(certificate["first_coverage"])
            if row["status"] == "continuation"
        ]
        row = certificate["second_coverage"][0]
        replacement = next(index for index in continuations if index != row["parent_first_coverage_index"])
        row["parent_first_coverage_index"] = replacement

    def nonforest_parent(certificate, crosswalk):
        row = certificate["second_coverage"][0]
        row["parent_first_coverage_index"] = 0

    cases = [
        ("omitted_clean_first_edge", omitted_clean_first, False, False),
        ("omitted_provenance_raw_record", omitted_provenance, False, False),
        ("wrong_first_parent_transport", wrong_parent_transport, True, False),
        ("broken_target_transport_payload", broken_transport_payload, True, False),
        ("reassigned_quartet_certificate", reassigned_quartet, True, False),
        ("reassigned_Ti_presentation", reassigned_t, True, False),
        ("altered_Bernstein_coefficient", altered_bernstein, True, False),
        ("invalid_D_plus_parameter_witness", invalid_physical_witness, True, False),
        ("reassigned_F_2_112_quartic", reassigned_quartic, True, False),
        ("omitted_second_child", omitted_second, False, False),
        ("wrong_second_parent", wrong_second_parent, True, False),
        ("nonforest_depth_cycle_attempt", nonforest_parent, True, False),
        ("optimized_mode", lambda certificate, crosswalk: None, True, True),
    ]

    worker_name = os.environ.get("K2P_RESTORATION_MUTATION_WORKER")
    if worker_name is not None:
        matching = [case for case in cases if case[0] == worker_name]
        require(len(matching) == 1, f"unknown mutation worker:{worker_name}")
        name, mutate, sync, optimized = matching[0]
        result = run_case(name, mutate, sync=sync, optimized=optimized)
        print("MUTATION_WORKER_JSON=" + json.dumps(result, sort_keys=True))
        return

    # Run each case in a fresh process.  This prevents Python's allocator from
    # retaining the two large JSON trees across mutations and keeps peak RSS
    # well below the one-GiB referee limit.
    results = []
    for name, _, _, _ in cases:
        environment = dict(os.environ)
        environment["K2P_RESTORATION_MUTATION_WORKER"] = name
        run = subprocess.run(
            [sys.executable, str(Path(__file__).resolve())],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=240,
            check=False,
            env=environment,
        )
        require(run.returncode == 0, f"mutation worker failed:{name}:{run.stdout[-800:]}")
        marker = [
            line.removeprefix("MUTATION_WORKER_JSON=")
            for line in run.stdout.splitlines()
            if line.startswith("MUTATION_WORKER_JSON=")
        ]
        require(len(marker) == 1, f"mutation worker result:{name}:{run.stdout[-800:]}")
        result = json.loads(marker[0])
        results.append(result)
        print(json.dumps(result, sort_keys=True), flush=True)

    report = {
        "schema": "k2p-corrected-restoration-mutations-v1",
        "status": "PASS",
        "source_certificate_sha256": sha_file(CERTIFICATE),
        "source_crosswalk_sha256": sha_file(CROSSWALK),
        "verifier_sha256": sha_file(VERIFIER),
        "mutations_attempted": len(results),
        "mutations_rejected": sum(result["rejected"] for result in results),
        "cases": results,
        "runtime_seconds": time.monotonic() - started,
        "peak_child_rss_bytes": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
    }
    require(report["mutations_attempted"] == report["mutations_rejected"] == 13, "mutation census")
    report["payload_sha256"] = sha(report)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (Failure, AssertionError, KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_RESTORATION_MUTATION_FAIL:{error}") from error
