#!/usr/bin/env python3
"""Bind every pending bounded relation to one fixed-full hard-cover root."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_hash(value: object) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def resolve(path: str | Path) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    if not candidate.is_file():
        raise AssertionError(("missing input", candidate))
    return candidate


def load_jsonl(path: Path, key: str) -> tuple[dict[str, dict], str]:
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


def relation_key(coverage: dict) -> tuple:
    return (
        str(coverage["source_primitive_id"]),
        str(coverage["target_primitive_id"]),
        tuple(int(value) for value in coverage["source_position_to_label"]),
        tuple(int(value) for value in coverage["target_position_to_label"]),
    )


def root_key(row: dict) -> tuple:
    case = row["root_case"]
    return (
        str(case["source_primitive_id"]),
        str(case["target_primitive_id"]),
        tuple(int(value) for value in case["source_position_to_label"]),
        tuple(int(value) for value in case["target_position_to_label"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--relation-summary", type=Path, action="append", required=True)
    parser.add_argument("--root-stream", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output = args.output.resolve()

    root_path = resolve(args.root_stream)
    roots, root_digest = load_jsonl(root_path, "root_case_id")
    roots_by_key: dict[tuple, str] = {}
    for root_id, row in roots.items():
        key = root_key(row)
        if key in roots_by_key:
            raise AssertionError(("duplicate fixed-full root relation", root_id))
        roots_by_key[key] = root_id

    relation_bodies: dict[str, dict] = {}
    coverage_by_key: dict[tuple, dict] = {}
    shard_rows = []
    classifications = Counter()
    for summary_arg in args.relation_summary:
        summary_path = resolve(summary_arg)
        payload = json.loads(summary_path.read_text())
        if len(payload.get("runs", ())) != 1:
            raise AssertionError((summary_path, "expected one relation run"))
        run = payload["runs"][0]
        cert = run.get("bounded_relation_certificate")
        if not cert or cert.get("failure_count") or cert.get("failures"):
            raise AssertionError((summary_path, "failed relation certificate"))
        relation_path = resolve(cert["relation_path"])
        relations, relation_digest = load_jsonl(relation_path, "relation_id")
        if relation_digest != cert["relation_stream_sha256"]:
            raise AssertionError((relation_path, "logical stream digest"))
        for relation_id, relation in relations.items():
            comparable = {
                key: value for key, value in relation.items()
                if key not in {"raw_coverage", "binding_sha256"}
            }
            if relation_id not in relation_bodies:
                relation_bodies[relation_id] = comparable
                classifications[relation["classification"]] += 1
            elif relation_bodies[relation_id] != comparable:
                raise AssertionError(("cross-shard relation disagreement", relation_id))
            if relation["classification"] != "pending_support_completion":
                continue
            for ordinal, coverage in enumerate(relation["raw_coverage"]):
                key = relation_key(coverage)
                row = {
                    "relation_id": relation_id,
                    "raw_coverage_ordinal": ordinal,
                    "raw_coverage_sha256": stable_hash(coverage),
                    "source_graph_id": coverage["source_graph_id"],
                    "target_completion_graph_id": coverage[
                        "target_completion_graph_id"
                    ],
                }
                if key in coverage_by_key:
                    raise AssertionError(("duplicate pending raw relation", key))
                coverage_by_key[key] = row
        shard_rows.append({
            "summary_path": str(summary_path.relative_to(ROOT)),
            "summary_sha256": sha256(summary_path),
            "relation_path": str(relation_path.relative_to(ROOT)),
            "relation_stream_sha256": relation_digest,
            "source_core_filter": run.get("source_core_filter"),
            "relations": len(relations),
        })

    missing_roots = set(roots_by_key) - set(coverage_by_key)
    extra_relations = set(coverage_by_key) - set(roots_by_key)
    if missing_roots or extra_relations:
        raise AssertionError({
            "missing_fixed_roots": len(missing_roots),
            "unbound_pending_relations": len(extra_relations),
        })

    crosswalk = []
    for key in sorted(roots_by_key, key=repr):
        relation = coverage_by_key[key]
        crosswalk.append({
            **relation,
            "root_case_id": roots_by_key[key],
        })
    args.output.parent.mkdir(parents=True, exist_ok=True)
    logical_digest = hashlib.sha256()
    with args.output.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            for row in crosswalk:
                line = (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()
                out.write(line)
                logical_digest.update(line)

    report = {
        "schema": "bounded-relation-hard-cover-crosswalk-v1",
        "status": "EXACTLY_VERIFIED",
        "root_stream": str(root_path.relative_to(ROOT)),
        "root_stream_file_sha256": sha256(root_path),
        "root_stream_logical_sha256": root_digest,
        "fixed_full_roots": len(roots),
        "pending_raw_relations": len(coverage_by_key),
        "all_roots_bound_bijectively": True,
        "relation_shards": shard_rows,
        "relation_classifications": dict(sorted(classifications.items())),
        "crosswalk_path": str(args.output.relative_to(ROOT)),
        "crosswalk_file_sha256": sha256(args.output),
        "crosswalk_logical_sha256": logical_digest.hexdigest(),
    }
    report_path = args.output.with_suffix("").with_suffix(".summary.json")
    report_path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
