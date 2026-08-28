#!/usr/bin/env python3
"""Test whether a layer-resealed conflicting JSONL member name is rejected.

This deliberately does not import the submitted verifier.  It makes a disposable
probe-layer clone, injects a conflicting duplicate top-level name in the first
one-port row (the later, authoritative-looking value wins under Python's default
JSON decoder), updates only the layer's advertised file hash and payload seal,
and invokes the published independent verifier on that clone.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def sha_object(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mutate_ledger(source: Path, destination: Path) -> dict[str, object]:
    with gzip.open(source, "rb") as incoming:
        lines = incoming.readlines()
    if not lines or not lines[0].endswith(b"\n") or not lines[0].startswith(b"{"):
        raise SystemExit("unexpected JSONL fixture")
    original = json.loads(lines[0])
    field = "parent_anchor_id"
    if field not in original:
        raise SystemExit("duplicate-name fixture field missing")
    attacker_value = "R4-CONFLICTING-EARLIER-VALUE"
    prefix = json.dumps(field).encode() + b":" + json.dumps(attacker_value).encode() + b","
    mutant_line = b"{" + prefix + lines[0][1:]
    reparsed = json.loads(mutant_line)
    if reparsed != original:
        raise SystemExit("mutation did not preserve Python default-decoder semantics")
    with destination.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=6) as encoded:
            encoded.write(mutant_line)
            for line in lines[1:]:
                encoded.write(line)
    return {
        "mutated_row_number": 0,
        "duplicate_name": field,
        "earlier_conflicting_value": attacker_value,
        "later_effective_value": original[field],
        "default_decoder_semantics_unchanged": reparsed == original,
        "mutant_line_is_noncanonical": mutant_line[:-1] != canonical_bytes(reparsed),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    layer = project / "work/probe_coherence_corrected"
    verifier = layer / "verify_probe_coherence_corrected.py"
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="r4-probe-duplicate-jsonl-") as temporary:
        clone = Path(temporary) / "probe_coherence_corrected"
        clone.mkdir()
        required = (
            "exact_transport_ledger.jsonl.gz",
            "parent_restriction_ledger.jsonl.gz",
            "separation_proof_registry.json.gz",
            "two_port_parent_inventory.jsonl.gz",
            "two_port_ledger.jsonl.gz",
        )
        for name in required:
            os.link(layer / name, clone / name)
        mutation = mutate_ledger(layer / "one_port_ledger.jsonl.gz", clone / "one_port_ledger.jsonl.gz")
        report = json.loads((layer / "probe_coherence_certificate.json").read_text())
        old_hash = report["one_port"]["ledger_sha256"]
        new_hash = sha_file(clone / "one_port_ledger.jsonl.gz")
        if old_hash == new_hash:
            raise SystemExit("mutation did not change compressed file hash")
        report["one_port"]["ledger_sha256"] = new_hash
        report.pop("payload_sha256", None)
        logical = dict(report)
        logical.pop("operational", None)
        report["payload_sha256"] = sha_object(logical)
        (clone / "probe_coherence_certificate.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n"
        )
        command = [
            str(args.python),
            "-B",
            str(verifier),
            "--package-dir",
            str(clone),
            "--output",
            str(clone / "verification.json"),
        ]
        completed = subprocess.run(command, text=True, capture_output=True, check=False, timeout=900)
        result = {
            "schema": "r4-probe-conflicting-duplicate-jsonl-attack-v1",
            "attack": mutation,
            "layer_reseal": {
                "old_one_port_ledger_sha256": old_hash,
                "new_one_port_ledger_sha256": new_hash,
                "certificate_payload_sha256": report["payload_sha256"],
                "certificate_payload_reseal_valid": report["payload_sha256"] == sha_object(logical),
            },
            "production_verifier": {
                "path": str(verifier.relative_to(project)),
                "sha256": sha_file(verifier),
                "command": command,
                "exit_code": completed.returncode,
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "accepted_mutant": completed.returncode == 0,
            },
            "runtime_seconds": time.monotonic() - started,
        }
        result["payload_sha256"] = sha_object(result)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps({
            "accepted_mutant": result["production_verifier"]["accepted_mutant"],
            "exit_code": completed.returncode,
            "payload_sha256": result["payload_sha256"],
        }, sort_keys=True))


if __name__ == "__main__":
    main()
