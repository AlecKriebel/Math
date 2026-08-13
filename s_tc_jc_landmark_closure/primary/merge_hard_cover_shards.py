#!/usr/bin/env python3
"""Deterministically merge disjoint schema-3 hard-cover root shards."""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path

from atlas_compiler import stable_hash


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_stream(path: Path, key: str) -> dict[str, dict]:
    rows = {}
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            identifier = row[key]
            prior = rows.setdefault(identifier, row)
            if prior != row:
                raise AssertionError((path, "content conflict", identifier))
    return rows


def union_rows(target: dict[str, dict], source: dict[str, dict], label: str):
    for identifier, row in source.items():
        prior = target.setdefault(identifier, row)
        if prior != row:
            raise AssertionError((label, "content conflict", identifier))


def normalized_bounded(row: dict) -> dict:
    return {key: value for key, value in row.items() if key != "elapsed_seconds"}


def write_stream(path: Path, rows: dict[str, dict]) -> str:
    digest = hashlib.sha256()
    with path.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as out:
            for identifier in sorted(rows):
                line = (
                    json.dumps(rows[identifier], sort_keys=True, separators=(",", ":"))
                    + "\n"
                ).encode()
                out.write(line)
                digest.update(line)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", action="append", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    states = {}
    graphs = {}
    polynomials = {}
    roots = {}
    ranges = []
    input_hashes = {}
    bounded = None
    first_cover = None
    all_root_cases = None
    selected_outgoing = None
    source_core_filter = None
    source_extra_count_filter = None
    descriptor_cache_scope = None
    descriptor_mask_normalization = None
    state_rows_total = 0
    root_rows_total = 0

    for summary_path in args.summary:
        payload = json.loads(summary_path.read_text())
        if len(payload["runs"]) != 1:
            raise AssertionError((summary_path, "expected one run"))
        run = payload["runs"][0]
        cover = run["hard_cover"]
        input_hashes[str(summary_path)] = sha256(summary_path)
        if bounded is None:
            bounded = normalized_bounded(run["bounded_summary"])
            first_cover = cover
            all_root_cases = int(cover["all_root_cases"])
            selected_outgoing = int(cover["selected_outgoing"])
            source_core_filter = payload.get("source_core_filter")
            source_extra_count_filter = payload.get("source_extra_count_filter")
            descriptor_cache_scope = cover.get("descriptor_cache_scope")
            descriptor_mask_normalization = cover.get(
                "descriptor_mask_normalization"
            )
        else:
            if normalized_bounded(run["bounded_summary"]) != bounded:
                raise AssertionError("bounded summaries differ across shards")
            if int(cover["all_root_cases"]) != all_root_cases:
                raise AssertionError("all-root count differs across shards")
            if int(cover["selected_outgoing"]) != selected_outgoing:
                raise AssertionError("outgoing size differs across shards")
            if payload.get("source_core_filter") != source_core_filter:
                raise AssertionError("source-core filters differ across shards")
            if payload.get("source_extra_count_filter") != source_extra_count_filter:
                raise AssertionError("source-extra filters differ across shards")
            if cover.get("descriptor_cache_scope") != descriptor_cache_scope:
                raise AssertionError("descriptor-cache scopes differ across shards")
            if cover.get("descriptor_mask_normalization") != descriptor_mask_normalization:
                raise AssertionError("descriptor-mask normalizations differ across shards")
        start, stop = cover["selected_root_range"]
        if start is None or stop is None:
            raise AssertionError((summary_path, "not a range shard"))
        ranges.append((int(start), int(stop)))
        streams = (
            (states, cover["relation_path"], "state_id", "states"),
            (graphs, cover["graph_library_path"], "graph_id", "graphs"),
            (
                polynomials,
                cover["polynomial_library_path"],
                "polynomial_id",
                "polynomials",
            ),
            (roots, cover["root_case_path"], "root_case_id", "roots"),
        )
        for destination, relative, key, label in streams:
            path = PROJECT / relative
            input_hashes[str(path)] = sha256(path)
            incoming = read_stream(path, key)
            if label == "states":
                state_rows_total += len(incoming)
            elif label == "roots":
                root_rows_total += len(incoming)
                shard_indices = {
                    int(row["global_root_case_index"])
                    for row in incoming.values()
                }
                if shard_indices != set(range(int(start), int(stop))):
                    raise AssertionError((
                        summary_path,
                        "root rows do not equal declared shard range",
                    ))
            union_rows(destination, incoming, label)

    assert first_cover is not None and bounded is not None
    if descriptor_cache_scope != "selected_port_count_and_exact_rooted_graph_id":
        raise AssertionError(("unsafe descriptor-cache scope", descriptor_cache_scope))
    if descriptor_mask_normalization != (
        "minimum_of_quartet_side_and_complement_on_zero_sum_characters"
    ):
        raise AssertionError((
            "unsafe descriptor-mask normalization",
            descriptor_mask_normalization,
        ))
    ordered_ranges = sorted(ranges)
    cursor = 0
    for start, stop in ordered_ranges:
        if start != cursor or stop <= start:
            raise AssertionError(("root shard gap or overlap", cursor, start, stop))
        cursor = stop
    if cursor != all_root_cases:
        raise AssertionError(("root shard cover incomplete", cursor, all_root_cases))
    global_indices = {int(row["global_root_case_index"]) for row in roots.values()}
    if global_indices != set(range(all_root_cases)):
        raise AssertionError("root library global indices are not complete")
    if len(states) != state_rows_total:
        raise AssertionError(("duplicate state across disjoint root shards", state_rows_total, len(states)))
    if len(roots) != root_rows_total:
        raise AssertionError(("duplicate root across disjoint root shards", root_rows_total, len(roots)))
    if any(int(row.get("schema", -1)) != 3 for row in states.values()):
        raise AssertionError("non-schema-3 state in shard merge")

    terminal_counts = Counter(
        row["terminal_classification"] for row in states.values()
    )
    unresolved = sum(
        count for key, count in terminal_counts.items()
        if key.startswith("unresolved") or "non_T" in key
    )
    cert = HERE / "certificates"
    state_path = cert / f"hard_cover_n{selected_outgoing}_{args.tag}.jsonl.gz"
    graph_path = cert / f"hard_cover_graphs_n{selected_outgoing}_{args.tag}.jsonl.gz"
    polynomial_path = cert / f"hard_cover_polynomials_n{selected_outgoing}_{args.tag}.jsonl.gz"
    root_path = cert / f"hard_cover_root_cases_n{selected_outgoing}_{args.tag}.jsonl.gz"
    cover = {
        **{
            key: value for key, value in first_cover.items()
            if key not in {
                "selected_root_range", "selected_root_case_indices",
                "root_case_commitment", "canonical_restored_relations",
                "counts", "unresolved", "relation_path",
                "relation_stream_sha256", "descriptor_cache_size",
                "sign_cache_size", "graph_library_records",
                "graph_library_path", "graph_library_stream_sha256",
                "polynomial_library_records", "polynomial_library_path",
                "polynomial_library_stream_sha256", "root_case_records",
                "root_case_path", "root_case_stream_sha256",
            }
        },
        "selected_root_range": [0, all_root_cases],
        "selected_root_case_indices": None,
        "selected_root_cases": all_root_cases,
        "root_case_commitment": stable_hash([
            (identifier, roots[identifier]["root_case"])
            for identifier in sorted(roots)
        ]),
        "canonical_restored_relations": len(states),
        "counts": dict(sorted(terminal_counts.items())),
        "unresolved": unresolved,
        "relation_path": str(state_path.relative_to(PROJECT)),
        "relation_stream_sha256": write_stream(state_path, states),
        "descriptor_cache_size": None,
        "sign_cache_size": None,
        "graph_library_records": len(graphs),
        "graph_library_path": str(graph_path.relative_to(PROJECT)),
        "graph_library_stream_sha256": write_stream(graph_path, graphs),
        "polynomial_library_records": len(polynomials),
        "polynomial_library_path": str(polynomial_path.relative_to(PROJECT)),
        "polynomial_library_stream_sha256": write_stream(
            polynomial_path, polynomials
        ),
        "root_case_records": len(roots),
        "root_case_path": str(root_path.relative_to(PROJECT)),
        "root_case_stream_sha256": write_stream(root_path, roots),
        "merged_root_ranges": ordered_ranges,
    }
    output = {
        "schema": 1,
        "relation_action": "anchor every source boundary; full target S_p",
        "source_core_filter": source_core_filter,
        "source_extra_count_filter": source_extra_count_filter,
        "merged_shard_inputs": input_hashes,
        "runs": [{"bounded_summary": bounded, "hard_cover": cover}],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": "UNRESOLVED" if unresolved else "EXACTLY COMPUTED",
        "states": len(states),
        "roots": len(roots),
        "graphs": len(graphs),
        "polynomials": len(polynomials),
        "counts": cover["counts"],
        "output": str(args.output),
        "sha256": sha256(args.output),
    }, sort_keys=True))
    if unresolved:
        raise SystemExit("merged hard cover has unresolved terminals")


if __name__ == "__main__":
    main()
