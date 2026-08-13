#!/usr/bin/env python3
"""Exact regression for the certified-sign cache shortcut."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def resolve(path: str | Path) -> Path:
    answer = Path(path)
    if not answer.is_absolute():
        answer = ROOT / answer
    if not answer.is_file():
        raise AssertionError(("missing artifact", answer))
    return answer


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_stream(path: Path, key: str) -> tuple[dict[str, dict], str]:
    rows: dict[str, dict] = {}
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line in handle:
            digest.update(line)
            row = json.loads(line)
            identifier = str(row[key])
            if identifier in rows:
                raise AssertionError((path, "duplicate", identifier))
            rows[identifier] = row
    return rows, digest.hexdigest()


def one_run(path: Path) -> tuple[dict, dict, dict]:
    payload = json.loads(path.read_text())
    if len(payload.get("runs", ())) != 1:
        raise AssertionError((path, "expected one run"))
    run = payload["runs"][0]
    cert = run.get("bounded_relation_certificate")
    if not cert or cert.get("failure_count") or cert.get("failures"):
        raise AssertionError((path, "failed relation certificate"))
    return payload, run, cert


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("optimized", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    baseline_path = resolve(args.baseline)
    optimized_path = resolve(args.optimized)
    baseline_payload, baseline_run, baseline_cert = one_run(baseline_path)
    optimized_payload, optimized_run, optimized_cert = one_run(optimized_path)

    for key in baseline_payload:
        if key in {"runs", "descriptor_bit_cache"}:
            continue
        if baseline_payload[key] != optimized_payload.get(key):
            raise AssertionError(("top-level field", key))
    for key in baseline_run:
        if key in {"elapsed_seconds", "bounded_relation_certificate"}:
            continue
        if baseline_run[key] != optimized_run.get(key):
            raise AssertionError(("run field", key))

    stream_specs = (
        ("relation_path", "relation_id", "relation_stream_sha256"),
        ("graph_library_path", "graph_id", "graph_library_stream_sha256"),
        ("polynomial_library_path", "polynomial_id", "polynomial_library_stream_sha256"),
    )
    streams = {}
    for path_key, id_key, digest_key in stream_specs:
        left, left_digest = load_stream(resolve(baseline_cert[path_key]), id_key)
        right, right_digest = load_stream(resolve(optimized_cert[path_key]), id_key)
        if left_digest != baseline_cert[digest_key]:
            raise AssertionError((path_key, "baseline declared digest"))
        if right_digest != optimized_cert[digest_key]:
            raise AssertionError((path_key, "optimized declared digest"))
        if left != right or left_digest != right_digest:
            raise AssertionError((path_key, "normalized stream disagreement"))
        streams[path_key] = {"records": len(left), "logical_sha256": left_digest}

    left_sign_path = resolve(baseline_cert["sign_library_path"])
    right_sign_path = resolve(optimized_cert["sign_library_path"])
    left_signs = json.loads(left_sign_path.read_text())
    right_signs = json.loads(right_sign_path.read_text())
    if left_signs != right_signs:
        raise AssertionError("sign library disagreement")

    for key in baseline_cert:
        if key in {
            "relation_tag", "relation_path", "sign_library_path",
            "graph_library_path", "polynomial_library_path",
        }:
            continue
        if baseline_cert[key] != optimized_cert.get(key):
            raise AssertionError(("certificate field", key))

    result = {
        "schema": "relation-certified-cache-shortcut-equivalence-v1",
        "status": "EXACTLY_VERIFIED",
        "baseline_summary": str(baseline_path.relative_to(ROOT)),
        "baseline_summary_sha256": sha256(baseline_path),
        "optimized_summary": str(optimized_path.relative_to(ROOT)),
        "optimized_summary_sha256": sha256(optimized_path),
        "streams": streams,
        "sign_records": len(left_signs),
        "reason": (
            "A previously certified cached candidate has deterministic order "
            "priority over every uncached candidate. Selecting the least such "
            "candidate before expanding unused pullbacks preserves the exact "
            "historical witness and every normalized output body."
        ),
    }
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
