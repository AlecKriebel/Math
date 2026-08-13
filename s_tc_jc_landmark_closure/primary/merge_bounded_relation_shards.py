#!/usr/bin/env python3
"""Fail-closed merge of source-core shards for the bounded directed atlas."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SUPPORT = ROOT / "primary/certificates/support_universe.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_hash(value: object) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def resolve(path: str | Path) -> Path:
    answer = Path(path)
    if not answer.is_absolute():
        answer = ROOT / answer
    if not answer.is_file():
        raise AssertionError(("missing artifact", answer))
    return answer


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


def write_jsonl(path: Path, rows: dict[str, dict]) -> str:
    digest = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            for identifier in sorted(rows):
                line = (json.dumps(rows[identifier], sort_keys=True, separators=(",", ":")) + "\n").encode()
                out.write(line)
                digest.update(line)
    return digest.hexdigest()


def expected_cores(outgoing: int) -> set[str]:
    payload = json.loads(SUPPORT.read_text())
    return {
        str(row["core_id"])
        for row in payload["records"]
        if int(row["outgoing_count"]) == outgoing
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, action="append", required=True)
    parser.add_argument("--outgoing", type=int, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    common_top = None
    seen_cores: set[str] = set()
    shard_manifest = []
    relations: dict[str, dict] = {}
    graphs: dict[str, dict] = {}
    polynomials: dict[str, dict] = {}
    signs: dict[str, dict] = {}
    raw_presentations = 0

    def merge_library(destination: dict, incoming: dict, kind: str) -> None:
        for identifier, row in incoming.items():
            prior = destination.setdefault(identifier, row)
            if prior != row:
                raise AssertionError((kind, "content-address disagreement", identifier))

    for summary_arg in args.summary:
        path = resolve(summary_arg)
        payload = json.loads(path.read_text())
        if len(payload.get("runs", ())) != 1:
            raise AssertionError((path, "expected one run"))
        top = {
            key: payload[key]
            for key in (
                "schema",
                "template_path",
                "template_sha256",
                "seventh_template_path",
                "seventh_template_sha256",
                "invariant_orbit_size",
            )
        }
        if common_top is None:
            common_top = top
        elif common_top != top:
            raise AssertionError((path, "invariant/template mismatch"))
        run = payload["runs"][0]
        if int(run["outgoing"]) != args.outgoing:
            raise AssertionError((path, "outgoing size"))
        if run.get("descriptor_mask_convention") != (
            "rooted_selected_side_masks_before_zero_sum_complement_zip"
        ):
            raise AssertionError((path, "descriptor convention"))
        if run.get("target_signature_retention_rule") != (
            "exists source s with s & ~target == 0"
        ):
            raise AssertionError((path, "target prefilter not certified"))
        core_filter = run.get("source_core_filter")
        if not isinstance(core_filter, list) or len(core_filter) != 1:
            raise AssertionError((path, "one source core per shard"))
        core = str(core_filter[0])
        if core in seen_cores:
            raise AssertionError(("duplicate source-core shard", core))
        seen_cores.add(core)
        cert = run.get("bounded_relation_certificate")
        if not cert or cert.get("failure_count") or cert.get("failures"):
            raise AssertionError((path, "failed relation shard"))

        relation_path = resolve(cert["relation_path"])
        graph_path = resolve(cert["graph_library_path"])
        polynomial_path = resolve(cert["polynomial_library_path"])
        sign_path = resolve(cert["sign_library_path"])
        shard_relations, relation_digest = load_jsonl(relation_path, "relation_id")
        shard_graphs, graph_digest = load_jsonl(graph_path, "graph_id")
        shard_polynomials, polynomial_digest = load_jsonl(
            polynomial_path, "polynomial_id"
        )
        shard_signs = json.loads(sign_path.read_text())
        if relation_digest != cert["relation_stream_sha256"]:
            raise AssertionError((path, "relation digest"))
        if graph_digest != cert["graph_library_stream_sha256"]:
            raise AssertionError((path, "graph digest"))
        if polynomial_digest != cert["polynomial_library_stream_sha256"]:
            raise AssertionError((path, "polynomial digest"))
        if sha256(sign_path) != cert["sign_library_sha256"]:
            raise AssertionError((path, "sign digest"))

        for relation_id, row in shard_relations.items():
            binding = row.get("binding_sha256")
            body = {key: value for key, value in row.items() if key != "binding_sha256"}
            if stable_hash(body) != binding:
                raise AssertionError((relation_id, "binding"))
            if relation_id not in relations:
                relations[relation_id] = row
                continue
            prior = relations[relation_id]
            comparable = lambda value: {
                key: item for key, item in value.items()
                if key not in {"raw_coverage", "binding_sha256"}
            }
            if comparable(prior) != comparable(row):
                raise AssertionError((relation_id, "cross-shard relation body"))
            coverage = {
                stable_hash(item): item
                for item in (*prior["raw_coverage"], *row["raw_coverage"])
            }
            prior["raw_coverage"] = [coverage[key] for key in sorted(coverage)]
            prior_without_binding = {
                key: value for key, value in prior.items() if key != "binding_sha256"
            }
            prior["binding_sha256"] = stable_hash(prior_without_binding)

        merge_library(graphs, shard_graphs, "graph")
        merge_library(polynomials, shard_polynomials, "polynomial")
        merge_library(signs, shard_signs, "sign")
        raw_presentations += int(cert["raw_presentations_examined"])
        shard_manifest.append({
            "core": core,
            "summary_path": str(path.relative_to(ROOT)),
            "summary_sha256": sha256(path),
            "relations": len(shard_relations),
            "relation_stream_sha256": relation_digest,
            "graphs": len(shard_graphs),
            "polynomials": len(shard_polynomials),
            "strict_signs": len(shard_signs),
        })

    expected = expected_cores(args.outgoing)
    if seen_cores != expected:
        raise AssertionError({
            "missing_source_cores": sorted(expected - seen_cores),
            "unexpected_source_cores": sorted(seen_cores - expected),
        })

    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    base = out.parent / f"bounded_relation_n{args.outgoing}_{args.tag}"
    relation_path = base.with_name(base.name + "_relations.jsonl.gz")
    graph_path = base.with_name(base.name + "_graphs.jsonl.gz")
    polynomial_path = base.with_name(base.name + "_polynomials.jsonl.gz")
    sign_path = base.with_name(base.name + "_signs.json")
    relation_digest = write_jsonl(relation_path, relations)
    graph_digest = write_jsonl(graph_path, graphs)
    polynomial_digest = write_jsonl(polynomial_path, polynomials)
    sign_path.write_text(json.dumps(signs, sort_keys=True, indent=2) + "\n")

    counts = Counter()
    for row in relations.values():
        counts[row["classification"]] += 1
        counts[
            f"{row['source_kind']}_to_{row['target_kind']}_"
            f"{row['classification']}"
        ] += 1
    cert = {
        "relation_tag": args.tag,
        "relation_path": str(relation_path.relative_to(ROOT)),
        "relation_stream_sha256": relation_digest,
        "sign_library_path": str(sign_path.relative_to(ROOT)),
        "sign_library_sha256": sha256(sign_path),
        "graph_library_path": str(graph_path.relative_to(ROOT)),
        "graph_library_records": len(graphs),
        "graph_library_stream_sha256": graph_digest,
        "polynomial_library_path": str(polynomial_path.relative_to(ROOT)),
        "polynomial_library_records": len(polynomials),
        "polynomial_library_stream_sha256": polynomial_digest,
        "canonical_decorated_relations": len(relations),
        "raw_presentations_examined": raw_presentations,
        "counts": dict(sorted(counts.items())),
        "distinct_strict_polynomials": len(signs),
        "failure_count": 0,
        "failures": [],
    }
    assert common_top is not None
    result = {
        **common_top,
        "merge_schema": "bounded-relation-source-core-partition-v1",
        "support_universe_path": str(SUPPORT.relative_to(ROOT)),
        "support_universe_sha256": sha256(SUPPORT),
        "source_core_partition": sorted(seen_cores),
        "shards": sorted(shard_manifest, key=lambda row: row["core"]),
        "runs": [{
            "outgoing": args.outgoing,
            "descriptor_mask_convention": (
                "rooted_selected_side_masks_before_zero_sum_complement_zip"
            ),
            "target_signature_retention_rule": (
                "exists source s with s & ~target == 0"
            ),
            "source_core_filter": sorted(seen_cores),
            "bounded_relation_certificate": cert,
        }],
    }
    out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": "EXACTLY_MERGED",
        "output": str(out),
        "output_sha256": sha256(out),
        "source_cores": sorted(seen_cores),
        "relations": len(relations),
        "counts": dict(sorted(counts.items())),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
