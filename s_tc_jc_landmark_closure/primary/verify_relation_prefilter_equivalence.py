#!/usr/bin/env python3
"""Prove that the exact target-signature prefilter changes no relation body."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve(path: str) -> Path:
    answer = ROOT / path
    if not answer.is_file():
        raise AssertionError(("missing artifact", answer))
    return answer


def load_stream(path: Path, key: str) -> tuple[dict[str, dict], str]:
    rows: dict[str, dict] = {}
    digest = hashlib.sha256()
    with gzip.open(path, "rb") as handle:
        for line in handle:
            digest.update(line)
            row = json.loads(line)
            identifier = str(row[key])
            if identifier in rows:
                raise AssertionError(("duplicate", path, identifier))
            rows[identifier] = row
    return rows, digest.hexdigest()


def one_run(path: Path) -> tuple[dict, dict]:
    payload = json.loads(path.read_text())
    if len(payload.get("runs", ())) != 1:
        raise AssertionError((path, "expected one run"))
    run = payload["runs"][0]
    cert = run.get("bounded_relation_certificate")
    if not cert or cert.get("failure_count") or cert.get("failures"):
        raise AssertionError((path, "failed or missing relation certificate"))
    return payload, run


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("old_summary", type=Path)
    parser.add_argument("filtered_summary", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    old_payload, old_run = one_run(args.old_summary)
    new_payload, new_run = one_run(args.filtered_summary)
    if new_run.get("target_signature_retention_rule") != (
        "exists source s with s & ~target == 0"
    ):
        raise AssertionError("filtered run does not declare the exact directed-pair predicate")

    equal_fields = (
        "outgoing",
        "descriptor_mask_convention",
        "source_core_filter",
        "source_extra_count_filter",
        "source_bases",
        "source_raw_labelled",
        "source_signatures",
        "target_raw_labelled",
        "common_signatures",
        "necessary_directed_pairs",
        "equal_pairs",
        "strict_pairs",
        "necessary_pairs_by_target_kind_membership",
        "necessary_pair_kind_matrix",
        "topology_audit",
        "signature_pair_commitment",
    )
    for field in equal_fields:
        if old_run.get(field) != new_run.get(field):
            raise AssertionError((field, old_run.get(field), new_run.get(field)))
    if int(new_run["target_signatures"]) > int(old_run["target_signatures"]):
        raise AssertionError("a prefilter cannot create target signatures")

    old_cert = old_run["bounded_relation_certificate"]
    new_cert = new_run["bounded_relation_certificate"]
    stream_specs = (
        ("relation_path", "relation_id", "relation_stream_sha256"),
        ("graph_library_path", "graph_id", "graph_library_stream_sha256"),
        ("polynomial_library_path", "polynomial_id", "polynomial_library_stream_sha256"),
    )
    stream_report = {}
    for path_field, key, digest_field in stream_specs:
        old_rows, old_digest = load_stream(resolve(old_cert[path_field]), key)
        new_rows, new_digest = load_stream(resolve(new_cert[path_field]), key)
        if old_digest != old_cert[digest_field] or new_digest != new_cert[digest_field]:
            raise AssertionError((path_field, "declared stream digest"))
        if old_rows != new_rows:
            raise AssertionError((path_field, "exact normalized bodies differ"))
        stream_report[path_field] = {
            "records": len(old_rows),
            "sha256": old_digest,
        }

    old_sign_path = resolve(old_cert["sign_library_path"])
    new_sign_path = resolve(new_cert["sign_library_path"])
    old_signs = json.loads(old_sign_path.read_text())
    new_signs = json.loads(new_sign_path.read_text())
    if old_signs != new_signs:
        raise AssertionError("strict-sign libraries differ")
    if sha256(old_sign_path) != old_cert["sign_library_sha256"]:
        raise AssertionError("old sign-library hash")
    if sha256(new_sign_path) != new_cert["sign_library_sha256"]:
        raise AssertionError("filtered sign-library hash")

    for field in (
        "canonical_decorated_relations",
        "raw_presentations_examined",
        "counts",
        "distinct_strict_polynomials",
        "failure_count",
        "failures",
    ):
        if old_cert.get(field) != new_cert.get(field):
            raise AssertionError(("certificate field", field))

    result = {
        "schema": "relation-target-prefilter-equivalence-v1",
        "status": "EXACTLY_VERIFIED",
        "old_summary": str(args.old_summary),
        "old_summary_sha256": sha256(args.old_summary),
        "filtered_summary": str(args.filtered_summary),
        "filtered_summary_sha256": sha256(args.filtered_summary),
        "old_target_signatures": int(old_run["target_signatures"]),
        "retained_target_signatures": int(new_run["target_signatures"]),
        "necessary_directed_pairs": int(new_run["necessary_directed_pairs"]),
        "streams": stream_report,
        "strict_sign_records": len(old_signs),
        "mathematical_reason": (
            "A target survives source-relative containment only if every "
            "invariant nonzero on the source is also nonzero on the target; "
            "this is exactly s & ~t == 0."
        ),
    }
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
