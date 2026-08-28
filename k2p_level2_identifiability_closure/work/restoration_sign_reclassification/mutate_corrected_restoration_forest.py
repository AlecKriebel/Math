#!/usr/bin/env python3
"""Fail-closed mutations for the clean corrected restoration release."""

from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import json
import os
import resource
import secrets
import subprocess
import sys
import tempfile
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
CERTIFICATE = HERE / "corrected_restoration_forest.json"
CROSSWALK = HERE / "corrected_restoration_historical_crosswalk.json"
VERIFIER = HERE / "verify_corrected_restoration_forest.py"
OUTPUT = HERE / "corrected_restoration_mutation_certificate.json"
AUTHORITATIVE_OUTPUT = OUTPUT
MUTATION_DIAGNOSTICS = {
    "omitted_clean_first_edge": "CORRECTED_RESTORATION_REPLAY_FAIL:first coverage length",
    "omitted_provenance_raw_record": "CORRECTED_RESTORATION_REPLAY_FAIL:crosswalk first coverage length",
    "wrong_first_parent_transport": "CORRECTED_RESTORATION_REPLAY_FAIL:source parent transport row binding:0",
    "broken_target_transport_payload": "CORRECTED_RESTORATION_REPLAY_FAIL:target parent transport registry replay:(91, (0, 1, 3, 2), 'D_REPAIR_0_2')",
    "reassigned_quartet_certificate": "CORRECTED_RESTORATION_REPLAY_FAIL:quartet replay:0",
    "reassigned_Ti_presentation": "CORRECTED_RESTORATION_REPLAY_FAIL:T target hash",
    "altered_Bernstein_coefficient": "CORRECTED_RESTORATION_REPLAY_FAIL:Bernstein record at first use:52d67c40fb7867cb1fe9fe10fefb54043be08ef072f1ffbeb3159fd3ec312d75",
    "invalid_D_plus_parameter_witness": "CORRECTED_RESTORATION_REPLAY_FAIL:witness s outside D_plus",
    "reassigned_F_2_112_quartic": "CORRECTED_RESTORATION_REPLAY_FAIL:algebra target pullback nonzero",
    "omitted_second_child": "CORRECTED_RESTORATION_REPLAY_FAIL:second coverage length",
    "wrong_second_parent": "CORRECTED_RESTORATION_REPLAY_FAIL:abstract complete acyclic parent forest",
    "nonforest_depth_cycle_attempt": "CORRECTED_RESTORATION_REPLAY_FAIL:abstract second parent",
    "optimized_mode": "CORRECTED_RESTORATION_REPLAY_FAIL:CORRECTED_RESTORATION_REPLAY_OPTIMIZED_MODE_FORBIDDEN",
}
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
)
LEGACY_WORKER_ENV = "K2P_RESTORATION_MUTATION_WORKER"
INTERNAL_NONCE_ENV = "K2P_RESTORATION_INTERNAL_NONCE"
CLEAN_BASELINE_TIMEOUT_SECONDS = 900


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


def atomic_write_bytes(path, payload):
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise Failure(
                "RESTORATION_MUTATION_OUTPUT_POLICY_FAIL: authoritative override "
                "licenses only the corrected restoration mutation certificate"
            )
        return normalized
    project_root = PROJECT.resolve()
    for candidate in (normalized, resolved):
        try:
            candidate.relative_to(project_root)
        except ValueError:
            continue
        break
    else:
        return normalized
    raise Failure(
        "RESTORATION_MUTATION_OUTPUT_POLICY_FAIL: routine mutation output must "
        "be outside project source tree"
    )


def prepare_public_run(output):
    # Remove any previous success report before validating the public process
    # environment.  A rejected invocation therefore cannot leave stale PASS
    # bytes that a caller could mistake for evidence from the failed run.
    output.unlink(missing_ok=True)
    require(os.environ.get(LEGACY_WORKER_ENV) is None, "legacy ambient worker selector forbidden")
    require(os.environ.get(INTERNAL_NONCE_ENV) is None, "ambient internal nonce forbidden")


def invoke_verifier(command, report_path, timeout):
    started = time.monotonic()
    try:
        run = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        def decoded(value):
            if value is None:
                return ""
            if isinstance(value, bytes):
                return value.decode("utf-8", errors="replace")
            return value

        output = decoded(error.stdout) + decoded(error.stderr)
        return {
            "returncode": None,
            "runtime_seconds": time.monotonic() - started,
            "diagnostic": str(output).strip(),
            "success_artifact_present": report_path.exists(),
            "timeout": True,
            "signal": False,
        }
    return {
        "returncode": run.returncode,
        "runtime_seconds": time.monotonic() - started,
        "diagnostic": run.stdout.strip(),
        "success_artifact_present": report_path.exists(),
        "timeout": False,
        "signal": run.returncode < 0,
    }


def qualify_mutation_failure(name, result):
    expected = MUTATION_DIAGNOSTICS[name]
    require(result.get("timeout") is False, f"mutation timeout:{name}")
    require(result.get("signal") is False, f"mutation signal:{name}:{result}")
    require(result.get("returncode") == 1, f"mutation exit:{name}:{result}")
    require(
        not any(marker in result.get("diagnostic", "") for marker in FORBIDDEN_FAILURE_MARKERS),
        f"mutation unrelated crash:{name}:{result}",
    )
    require(
        result.get("success_artifact_present") is False,
        f"mutation success artifact:{name}",
    )
    require(result.get("diagnostic") == expected, f"mutation diagnostic:{name}:{result}")
    return {
        "mutation": name,
        "rejected": True,
        "returncode": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": expected,
        "success_artifact_absent": True,
        "timeout": False,
        "signal": False,
    }


def run_clean_baseline():
    with tempfile.TemporaryDirectory(prefix="k2p-restoration-baseline-") as temporary:
        report_path = Path(temporary) / "report.json"
        result = invoke_verifier(
            [
                sys.executable,
                str(VERIFIER),
                "--certificate",
                str(CERTIFICATE),
                "--crosswalk",
                str(CROSSWALK),
                "--report",
                str(report_path),
            ],
            report_path,
            CLEAN_BASELINE_TIMEOUT_SECONDS,
        )
        require(result["timeout"] is False, "clean baseline timeout")
        require(result["signal"] is False, "clean baseline signal")
        require(result["returncode"] == 0, f"clean baseline exit:{result}")
        require(
            not any(marker in result["diagnostic"] for marker in FORBIDDEN_FAILURE_MARKERS),
            f"clean baseline crash:{result}",
        )
        require(result["success_artifact_present"] is True, "clean baseline report absent")
        replay = json.loads(report_path.read_text())
        unhashed = dict(replay)
        payload = unhashed.pop("payload_sha256")
        require(payload == sha(unhashed), "clean baseline payload")
        require(
            replay.get("schema") == "k2p-corrected-restoration-independent-replay-v3"
            and replay.get("status") == "PASS"
            and replay.get("unresolved") == 0
            and replay.get("missing_children") == 0
            and replay.get("cycles") == 0,
            f"clean baseline semantics:{replay}",
        )
        return {
            "returncode": 0,
            "status": "PASS",
            "report_schema": replay["schema"],
            "report_status": replay["status"],
            "success_artifact_present": True,
            "unresolved": 0,
            "missing_children": 0,
            "cycles": 0,
            "timeout": False,
            "signal": False,
        }, result["runtime_seconds"]


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
    return invoke_verifier(command, report_path, 180)


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
    runtime_seconds = result.pop("runtime_seconds")
    qualified = qualify_mutation_failure(name, result)
    print(json.dumps(qualified, sort_keys=True), flush=True)
    return {"case": qualified, "runtime_seconds": runtime_seconds}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--internal-worker", choices=tuple(MUTATION_DIAGNOSTICS), help=argparse.SUPPRESS)
    parser.add_argument("--parent-nonce", help=argparse.SUPPRESS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    args = parser.parse_args()
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

    if args.internal_worker is not None:
        if not __debug__:
            raise Failure("MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN")
        require(os.environ.get(LEGACY_WORKER_ENV) is None, "legacy ambient worker selector forbidden")
        inherited_nonce = os.environ.get(INTERNAL_NONCE_ENV)
        require(
            isinstance(args.parent_nonce, str)
            and len(args.parent_nonce) == 64
            and inherited_nonce == args.parent_nonce,
            "internal worker parent nonce",
        )
        matching = [case for case in cases if case[0] == args.internal_worker]
        require(len(matching) == 1, f"unknown mutation worker:{args.internal_worker}")
        name, mutate, sync, optimized = matching[0]
        result = run_case(name, mutate, sync=sync, optimized=optimized)
        result["parent_nonce_sha256"] = hashlib.sha256(args.parent_nonce.encode()).hexdigest()
        print("MUTATION_WORKER_JSON=" + json.dumps(result, sort_keys=True))
        return
    require(args.parent_nonce is None, "parent nonce without internal worker")
    require(args.output is not None, "public --output required")
    output_path = validate_output_path(args.output, args.allow_authoritative_output)
    prepare_public_run(output_path)
    if not __debug__:
        raise Failure("MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN")

    # Run each case in a fresh process.  This prevents Python's allocator from
    # retaining the two large JSON trees across mutations and keeps peak RSS
    # well below the one-GiB referee limit.
    baseline, baseline_runtime = run_clean_baseline()
    results = []
    case_runtimes = {}
    for name, _, _, _ in cases:
        environment = dict(os.environ)
        environment.pop(LEGACY_WORKER_ENV, None)
        nonce = secrets.token_hex(32)
        environment[INTERNAL_NONCE_ENV] = nonce
        run = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--internal-worker",
                name,
                "--parent-nonce",
                nonce,
            ],
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
        require(
            result.pop("parent_nonce_sha256", None)
            == hashlib.sha256(nonce.encode()).hexdigest(),
            f"mutation worker nonce:{name}",
        )
        results.append(result["case"])
        case_runtimes[name] = result["runtime_seconds"]
        print(json.dumps(result["case"], sort_keys=True), flush=True)

    report = {
        "schema": "k2p-corrected-restoration-mutations-v2",
        "status": "PASS",
        "clean_baseline": baseline,
        "diagnostic_contract": MUTATION_DIAGNOSTICS,
        "source_certificate_sha256": sha_file(CERTIFICATE),
        "source_crosswalk_sha256": sha_file(CROSSWALK),
        "verifier_sha256": sha_file(VERIFIER),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "mutations_attempted": len(results),
        "mutations_rejected": sum(result["rejected"] for result in results),
        "cases": results,
        "operational": {
            "runtime_seconds": time.monotonic() - started,
            "baseline_runtime_seconds": baseline_runtime,
            "case_runtime_seconds": case_runtimes,
            "peak_child_rss_bytes": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
        },
    }
    require(report["mutations_attempted"] == report["mutations_rejected"] == 13, "mutation census")
    logical = dict(report)
    logical.pop("operational")
    report["payload_sha256"] = sha(logical)
    atomic_write_bytes(output_path, encoded(report))
    print(json.dumps(report, sort_keys=True))
    print("K2P_CORRECTED_RESTORATION_MUTATIONS_PASS rejected=13 survived=0")


if __name__ == "__main__":
    try:
        main()
    except (
        Failure,
        AssertionError,
        KeyError,
        IndexError,
        OSError,
        ValueError,
        json.JSONDecodeError,
        subprocess.TimeoutExpired,
    ) as error:
        raise SystemExit(f"CORRECTED_RESTORATION_MUTATION_FAIL:{error}") from error
