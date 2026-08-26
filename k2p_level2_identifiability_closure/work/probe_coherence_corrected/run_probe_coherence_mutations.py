#!/usr/bin/env python3
"""Fail-closed mutation suite for the corrected probe-coherence release."""

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
PROJECT = HERE.parents[1]
VERIFIER = HERE / "verify_probe_coherence_corrected.py"
OUTPUT = HERE / "probe_coherence_mutation_certificate.json"
AUTHORITATIVE_OUTPUT = OUTPUT
FILES = (
    "probe_coherence_certificate.json",
    "one_port_ledger.jsonl.gz",
    "two_port_parent_inventory.jsonl.gz",
    "two_port_ledger.jsonl.gz",
    "exact_transport_ledger.jsonl.gz",
    "parent_restriction_ledger.jsonl.gz",
    "separation_proof_registry.json.gz",
)
MUTATION_DIAGNOSTICS = {
    "omitted_anchor": "CORRECTED_PROBE_REPLAY_FAIL:anchor rows",
    "swapped_classifier_precedence": "CORRECTED_PROBE_REPLAY_FAIL:classifier order",
    "omitted_one_port_probe": "CORRECTED_PROBE_REPLAY_FAIL:one Cartesian/order coverage:0:('four:raw2040', 0, 1)",
    "wrong_one_port_parent": "CORRECTED_PROBE_REPLAY_FAIL:one Cartesian/order coverage:0:('four:raw2042', 0, 0)",
    "reassigned_Ti_certificate": "CORRECTED_PROBE_REPLAY_FAIL:one T_i proof:122",
    "omitted_two_port_parent": "CORRECTED_PROBE_REPLAY_FAIL:two parent ordered equality coverage:0",
    "missing_root_suppressed_site": "CORRECTED_PROBE_REPLAY_FAIL:profile formula:source:P1:four:raw2040:0:0",
    "omitted_two_port_probe": "CORRECTED_PROBE_REPLAY_FAIL:two raw total from parents",
    "wrong_two_port_parent": "CORRECTED_PROBE_REPLAY_FAIL:two Cartesian/order coverage:0:('P1:four:raw2040:1:1', 0, 0)",
    "reversed_order_class": "CORRECTED_PROBE_REPLAY_FAIL:reverse class:0",
    "inconsistent_global_triangle": "CORRECTED_PROBE_REPLAY_FAIL:global triangle hash:two:1887",
    "broken_exact_transport": "CORRECTED_PROBE_REPLAY_FAIL:transport self hash:d36206c63e2262bc13495519b217d2e600b576e64ddcb603c34529dcd4025f8c",
    "omitted_parent_restriction": "CORRECTED_PROBE_REPLAY_FAIL:one source restriction:0",
    "altered_Bernstein_certificate": "CORRECTED_PROBE_REPLAY_FAIL:Bernstein replay:05c1967f1addbbf8854ce12ec25861b3b2793fb2961d77ad892e633e93c3c71f",
    "optimized_mode": "CORRECTED_PROBE_REPLAY_FAIL:CORRECTED_PROBE_REPLAY_OPTIMIZED_MODE_FORBIDDEN",
}
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
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


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise MutationFailure(
                "PROBE_MUTATION_OUTPUT_POLICY_FAIL: authoritative override "
                "licenses only the corrected probe mutation certificate"
            )
        return normalized
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise MutationFailure(
        "PROBE_MUTATION_OUTPUT_POLICY_FAIL: routine mutation output must be "
        "outside project source tree"
    )


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
    return json.loads((root / "probe_coherence_certificate.json").read_text())


def seal_certificate(root, certificate):
    certificate.pop("payload_sha256", None)
    logical = dict(certificate)
    logical.pop("operational", None)
    certificate["payload_sha256"] = sha(logical)
    (root / "probe_coherence_certificate.json").write_text(
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
        if filename == "probe_coherence_certificate.json":
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
    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            env=environment,
            timeout=180,
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
            "success_artifact_present": (root / "verification.json").exists(),
            "timeout": True,
            "signal": False,
        }
    return {
        "returncode": result.returncode,
        "runtime_seconds": time.monotonic() - started,
        "diagnostic": (result.stdout + result.stderr).strip(),
        "success_artifact_present": (root / "verification.json").exists(),
        "timeout": False,
        "signal": result.returncode < 0,
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


def qualify_clean_baseline(root, result, hash_seed):
    require(result.get("timeout") is False, "clean baseline timeout")
    require(result.get("signal") is False, "clean baseline signal")
    require(result.get("returncode") == 0, f"clean baseline exit:{result}")
    require(
        not any(marker in result.get("diagnostic", "") for marker in FORBIDDEN_FAILURE_MARKERS),
        f"clean baseline crash:{result}",
    )
    require(result.get("success_artifact_present") is True, "clean baseline report absent")
    report = json.loads((root / "verification.json").read_text())
    payload = report.pop("payload_sha256")
    operational = report.pop("operational")
    del operational
    require(payload == sha(report), "clean baseline payload")
    require(
        report.get("schema") == "k2p-corrected-probe-independent-verification-v1"
        and report.get("status") == "PASS"
        and report.get("unresolved") == 0
        and report.get("incoherent") == 0,
        f"clean baseline semantics:{report}",
    )
    return {
        "PYTHONHASHSEED": int(hash_seed),
        "returncode": 0,
        "status": "PASS",
        "report_schema": report["schema"],
        "report_status": report["status"],
        "success_artifact_present": True,
        "unresolved": 0,
        "incoherent": 0,
        "timeout": False,
        "signal": False,
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


def mutate_reassigned_Ti(root):
    make_writable(root, "one_port_ledger.jsonl.gz")
    changed = [False]
    def transform(row, number):
        del number
        if not changed[0] and row["status"] == "full_map_Ti_strict_sign":
            row["proof_id"] = "TI:" + "0" * 64
            changed[0] = True
        return row
    update_one(root, transform)
    require(changed[0], "no T_i row to mutate")


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


def mutate_omitted_restriction(root):
    make_writable(root, "parent_restriction_ledger.jsonl.gz")
    update_streaming_store(
        root, "parent_restriction_ledger.jsonl.gz", "parent_restrictions",
        lambda row, number: None if number == 0 else row,
    )


def mutate_Bernstein(root):
    make_writable(root, "separation_proof_registry.json.gz")
    def transform(proof):
        strict = proof["full_map_Ti_registry"]["strict_polynomial_registry"]
        first = strict[sorted(strict)[0]]["Bernstein_certificate"]
        first["minimum_coefficient"] = "999"
    update_proof_registry(root, transform)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    args = parser.parse_args()
    output_path = validate_output_path(args.output, args.allow_authoritative_output)
    output_path.unlink(missing_ok=True)
    if not __debug__:
        raise MutationFailure("PROBE_MUTATION_DRIVER_OPTIMIZED_MODE_FORBIDDEN")
    require((HERE / "probe_coherence_certificate.json").exists(), "missing source certificate")
    cases = [
        ("omitted_anchor", mutate_omitted_anchor),
        ("swapped_classifier_precedence", mutate_swapped_classifier),
        ("omitted_one_port_probe", mutate_omitted_one),
        ("wrong_one_port_parent", mutate_wrong_one_parent),
        ("reassigned_Ti_certificate", mutate_reassigned_Ti),
        ("omitted_two_port_parent", mutate_omitted_parent),
        ("missing_root_suppressed_site", mutate_missing_root_site),
        ("omitted_two_port_probe", mutate_omitted_two),
        ("wrong_two_port_parent", mutate_wrong_two_parent),
        ("reversed_order_class", mutate_reverse_order),
        ("inconsistent_global_triangle", mutate_inconsistent_triangle),
        ("broken_exact_transport", mutate_broken_transport),
        ("omitted_parent_restriction", mutate_omitted_restriction),
        ("altered_Bernstein_certificate", mutate_Bernstein),
    ]
    results = []
    case_runtimes = {}
    started = time.monotonic()
    for name, mutation in cases:
        with tempfile.TemporaryDirectory(prefix=f"k2p_probe_mutation_{name}_") as directory:
            root = Path(directory)
            link_case(root)
            mutation(root)
            replay = run_verifier(root)
            runtime_seconds = replay.pop("runtime_seconds")
            results.append(qualify_mutation_failure(name, replay))
            case_runtimes[name] = runtime_seconds
            print(json.dumps(results[-1], sort_keys=True), flush=True)
    with tempfile.TemporaryDirectory(prefix="k2p_probe_optimized_") as directory:
        root = Path(directory)
        link_case(root)
        replay = run_verifier(root, optimized=True)
        runtime_seconds = replay.pop("runtime_seconds")
        results.append(qualify_mutation_failure("optimized_mode", replay))
        case_runtimes["optimized_mode"] = runtime_seconds
    with tempfile.TemporaryDirectory(prefix="k2p_probe_hashseed_") as directory:
        root = Path(directory)
        link_case(root)
        replay = run_verifier(root, hash_seed="12345")
        baseline_runtime = replay.pop("runtime_seconds")
        baseline = qualify_clean_baseline(root, replay, "12345")
    require(
        len(results) == 15 and all(row["rejected"] is True for row in results),
        "mutation census",
    )
    report = {
        "schema": "k2p-corrected-probe-mutations-v2",
        "status": "PASS",
        "clean_baseline": baseline,
        "diagnostic_contract": MUTATION_DIAGNOSTICS,
        "source_certificate_sha256": sha_file(HERE / "probe_coherence_certificate.json"),
        "source_verifier_sha256": sha_file(VERIFIER),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
        "mutations_attempted": len(results),
        "mutations_rejected": sum(row["rejected"] for row in results),
        "cases": results,
        "operational": {
            "runtime_seconds": time.monotonic() - started,
            "baseline_runtime_seconds": baseline_runtime,
            "case_runtime_seconds": case_runtimes,
        },
    }
    logical = dict(report)
    logical.pop("operational")
    report["payload_sha256"] = sha(logical)
    atomic_write_bytes(
        output_path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    )
    print(json.dumps({
        "status": "PASS", "mutations": len(results),
        "payload_sha256": report["payload_sha256"],
    }, sort_keys=True))
    print("K2P_CORRECTED_PROBE_MUTATIONS_PASS rejected=15 survived=0")


if __name__ == "__main__":
    try:
        main()
    except (MutationFailure, KeyError, IndexError, OSError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"CORRECTED_PROBE_MUTATION_FAIL:{error}") from error
