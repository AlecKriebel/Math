#!/usr/bin/env python3
"""Portable atomic, hash-bound, resumable K2P four-port classifier.

The distribution directory is self-contained:

    package_root/
      atlas/k2p_atlas_core.py
      atlas/descriptors_4.pkl
      atlas/rank_certs_4.pkl
      certificates/direct_hard_cases.json
      schemas/four_port_record_v3.schema.json
      INPUT_LOCK.json
      resumable_four_port_driver.py

One JSON file is committed atomically per canonical descriptor class. Existing
records are reused only after every immutable input binding and the record's
self-hash are verified. The implementation is POSIX-portable (Linux/macOS).
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import fcntl
import hashlib
import importlib.util
import inspect
import json
import os
import pickle
import platform
import resource
import sys
import time
from pathlib import Path
from typing import Any

SCHEMA = "k2p-four-port-record-v3"
MANIFEST_SCHEMA = "k2p-four-port-residual-manifest-v2"


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def canonical_data(value: Any):
    if dataclasses.is_dataclass(value):
        return {field.name: canonical_data(getattr(value, field.name)) for field in dataclasses.fields(value)}
    if isinstance(value, dict):
        return {str(key): canonical_data(item) for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))}
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def sha_object(value: Any) -> str:
    raw = json.dumps(canonical_data(value), sort_keys=True, separators=(",", ":")).encode()
    return sha_bytes(raw)


def payload_hash(payload: dict) -> str:
    body = {key: value for key, value in payload.items() if key != "record_payload_sha256"}
    return sha_bytes(json.dumps(body, sort_keys=True, separators=(",", ":"), default=str).encode())


def fsync_directory(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True, indent=2, default=str)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    fsync_directory(path.parent)


def load_module(module_path: Path):
    module_name = "k2p_atlas_core"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def graph_payload(graph):
    nodes = []
    for node, data in sorted(graph.nodes(data=True), key=lambda pair: repr(pair[0])):
        nodes.append([repr(node), {str(key): repr(value) for key, value in sorted(data.items())}])
    edges = []
    for tail, head, data in sorted(graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))):
        edges.append([repr(tail), repr(head), {str(key): repr(value) for key, value in sorted(data.items())}])
    return {
        "nodes": nodes,
        "edges": edges,
        "graph": {str(key): repr(value) for key, value in sorted(graph.graph.items())},
    }


def source_insertion_candidates(graph):
    answer = []
    for tail, head, data in sorted(graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        answer.append({"tail": repr(tail), "head": repr(head), "edge_role": data.get("edge_role")})
    return answer


def target_dummy_attachments(graph):
    answer = {}
    for node, data in graph.nodes(data=True):
        role = data.get("dummy_name")
        if data.get("role") == "leaf" and role:
            parents = list(graph.predecessors(node))
            if len(parents) != 1:
                raise AssertionError((node, parents))
            parent = parents[0]
            answer[str(role)] = {
                "parent": repr(parent),
                "leaf_node": repr(node),
                "edge_role": graph.edges[parent, node].get("edge_role"),
            }
    return answer


def current_hashes(atlas_root: Path, atlas):
    compiler = sha_file(atlas_root / "k2p_atlas_core.py")
    canonicalizer_source = "\n".join(
        inspect.getsource(getattr(atlas, name))
        for name in ("mixed_incidence_graph", "mixed_exact_isomorphic", "mixed_relation_exact")
    )
    return compiler, sha_bytes(canonicalizer_source.encode())


def validate_input_lock(package_root: Path, lock: dict) -> None:
    if lock.get("schema") != "k2p-offline-four-port-input-lock-v1":
        raise SystemExit("unsupported INPUT_LOCK schema")
    for relative, expected in lock["files"].items():
        path = package_root / relative
        if not path.is_file():
            raise SystemExit(f"missing locked input: {relative}")
        observed = sha_file(path)
        if observed != expected:
            raise SystemExit(f"locked input hash mismatch: {relative}: {observed}")


def class_universe(source_index, sources, rows, source_descriptors, cache, ranks):
    source_descriptor = source_descriptors[source_index]
    source_rank = ranks[source_descriptor]["rank"]
    seen, classes, members = {}, [], []
    for raw in rows[source_index]:
        descriptor = cache[raw]
        if ranks[descriptor]["rank"] < source_rank:
            continue
        if descriptor not in seen:
            seen[descriptor] = len(classes)
            classes.append(descriptor)
            members.append([])
        members[seen[descriptor]].append(raw)
    return source_descriptor, classes, members


def peak_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def classify_one(
    atlas,
    source_index,
    class_id,
    source_descriptor,
    target_descriptor,
    members,
    sources,
    targets,
    hard_certificate_hash,
):
    started = time.perf_counter()
    relations, member_rows, omitted, direct_flags = set(), [], set(), []
    source_graph = sources[source_index].graph
    for target_index, permutation in members:
        relabelled = atlas.relabel_record(targets[target_index], permutation)
        selected = atlas.selected_graph_from_completion(relabelled)
        relation = atlas.mixed_relation_exact(source_graph, selected)
        relations.add(relation)
        omitted.update(targets[target_index].dummy_labels)
        direct_flags.append(not targets[target_index].dummy_labels)
        member_rows.append({
            "target_index": target_index,
            "port_match": list(permutation),
            "target_core": targets[target_index].core_id,
            "target_repair_index": targets[target_index].repair_index,
            "incoming_selected": targets[target_index].incoming_selected,
            "dummy_roles": list(targets[target_index].dummy_labels),
            "graph_relation": relation,
            "target_selected_graph_sha256": sha_object(graph_payload(selected)),
            "target_dummy_attachments": target_dummy_attachments(relabelled.graph),
        })

    separator = atlas.quadratic_separator_fast(source_descriptor, target_descriptor, max_block_size=16)
    status, certificate = "unresolved", None
    if separator:
        status = "separated"
        certificate = {
            "type": "exact_multihomogeneous_quadratic",
            "degree": 2,
            "weight": separator["weight"],
            "coordinate_pairs": separator["coordinate_pairs"],
            "coefficients": separator["coefficients"],
            "source_nonzero_terms": separator["source_nonzero_terms"],
        }
    elif relations == {"isomorphic"}:
        status = "isomorphic"
        certificate = {"type": "exact_mixed_graph_isomorphism"}
    elif relations <= {"isomorphic", "triangle"} and "triangle" in relations:
        status = "triangle"
        certificate = {"type": "ordinary_triangle_quotient"}
    elif source_index == 0 and class_id in (206, 207, 208, 209):
        if hard_certificate_hash is None:
            raise RuntimeError("direct hard-case certificate is missing")
        status = "separated"
        certificate = {
            "type": "direct_hard_case_F2_F3_F4",
            "certificate_sha256": hard_certificate_hash,
            "class_id": class_id,
        }
    elif omitted:
        status = "restoration_parent"
        certificate = {"type": "requires_direct_child_restoration"}

    if any(direct_flags) and not all(direct_flags):
        raise AssertionError("descriptor class mixes direct and dummy presentations")
    stratum = "direct_no_dummy" if all(direct_flags) else "restoration_candidate"
    if stratum == "direct_no_dummy" and omitted:
        raise AssertionError("direct descriptor unexpectedly has omitted roles")

    child_requests = []
    if omitted:
        insertions = source_insertion_candidates(source_graph)
        for role in sorted(omitted):
            attachments = []
            for member in member_rows:
                if role in member["dummy_roles"]:
                    if role not in member["target_dummy_attachments"]:
                        raise AssertionError((role, member))
                    attachments.append({
                        "target_index": member["target_index"],
                        "port_match": member["port_match"],
                        **member["target_dummy_attachments"][role],
                    })
            child_requests.append({
                "omitted_role": role,
                "selected_total": source_descriptor.k + 1,
                "source_insertion_edge_candidates": insertions,
                "target_dummy_attachments": attachments,
                "require_direct_marginal": True,
            })
    elapsed = time.perf_counter() - started
    return status, certificate, stratum, member_rows, child_requests, elapsed


def validate_record(row: dict, common: dict, path: Path) -> None:
    for key in (
        "schema", "canonicalizer_sha256", "compiler_sha256", "source_index",
        "canonical_class_id", "descriptor_sha256", "source_graph_sha256",
        "descriptor_pickle_sha256", "rank_pickle_sha256", "output_schema_sha256",
        "input_lock_sha256",
    ):
        if row.get(key) != common[key]:
            raise SystemExit(f"stale/corrupt record {path}: {key}")
    if row.get("record_payload_sha256") != payload_hash(row):
        raise SystemExit(f"stale/corrupt record {path}: record_payload_sha256")
    if row.get("status") not in {
        "separated", "isomorphic", "triangle", "restoration_parent", "unresolved", "error"
    }:
        raise SystemExit(f"stale/corrupt record {path}: status")


def build_manifest(
    run_dir: Path,
    records_dir: Path,
    source_index: int,
    class_count: int,
    immutable: dict,
) -> dict:
    records = []
    class_ids = set()
    for path in sorted(records_dir.glob("class_*.json")):
        row = json.loads(path.read_text())
        for key, value in immutable.items():
            if row.get(key) != value:
                raise SystemExit(f"old-input record rejected: {path}: {key}")
        if row.get("record_payload_sha256") != payload_hash(row):
            raise SystemExit(f"corrupt record rejected while building manifest: {path}")
        class_id = row["canonical_class_id"]
        if class_id in class_ids:
            raise SystemExit(f"duplicate canonical class record: {class_id}")
        class_ids.add(class_id)
        records.append({
            "canonical_class_id": class_id,
            "status": row["status"],
            "stratum": row["stratum"],
            "descriptor_sha256": row["descriptor_sha256"],
            "record_sha256": sha_file(path),
            "omitted_roles": row["omitted_roles"],
            "child_requests": row["child_requests"],
        })
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "source_index": source_index,
        **immutable,
        "canonical_class_count": class_count,
        "record_count": len(records),
        "complete": len(records) == class_count and class_ids == set(range(class_count)),
        "records": records,
        "unresolved": [row["canonical_class_id"] for row in records if row["status"] == "unresolved"],
        "restoration_candidates": [
            row["canonical_class_id"] for row in records if row["status"] == "restoration_parent"
        ],
    }
    atomic_json(run_dir / "residual_manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-index", type=int, required=True)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-root", type=Path, default=Path.cwd() / "k2p_four_port_run")
    parser.add_argument("--expected-compiler-sha256")
    parser.add_argument("--expected-canonicalizer-sha256")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--manifest-every", type=int, default=1)
    parser.add_argument("--list-sources", action="store_true")
    args = parser.parse_args()

    package_root = args.package_root.resolve()
    atlas_root = package_root / "atlas"
    input_lock_path = package_root / "INPUT_LOCK.json"
    input_lock = json.loads(input_lock_path.read_text())
    validate_input_lock(package_root, input_lock)
    input_lock_sha = sha_file(input_lock_path)

    atlas = load_module(atlas_root / "k2p_atlas_core.py")
    compiler_sha, canonicalizer_sha = current_hashes(atlas_root, atlas)
    if args.expected_compiler_sha256 and args.expected_compiler_sha256 != compiler_sha:
        raise SystemExit(f"compiler hash mismatch: {compiler_sha}")
    if args.expected_canonicalizer_sha256 and args.expected_canonicalizer_sha256 != canonicalizer_sha:
        raise SystemExit(f"canonicalizer hash mismatch: {canonicalizer_sha}")

    descriptor_path = atlas_root / "descriptors_4.pkl"
    rank_path = atlas_root / "rank_certs_4.pkl"
    with descriptor_path.open("rb") as handle:
        sources, targets, rows, source_descriptors, cache = pickle.load(handle)
    with rank_path.open("rb") as handle:
        ranks = pickle.load(handle)

    if args.list_sources:
        result = []
        for source_index in range(len(source_descriptors)):
            source_descriptor, classes, _members = class_universe(
                source_index, sources, rows, source_descriptors, cache, ranks
            )
            result.append({
                "source_index": source_index,
                "core": sources[source_index].core_id,
                "repair_index": sources[source_index].repair_index,
                "source_rank": ranks[source_descriptor]["rank"],
                "canonical_class_count": len(classes),
            })
        print(json.dumps(result, sort_keys=True, indent=2))
        return

    if not 0 <= args.source_index < len(source_descriptors):
        raise SystemExit(f"source index out of range: {args.source_index}")

    descriptor_pickle_sha = sha_file(descriptor_path)
    rank_pickle_sha = sha_file(rank_path)
    schema_path = package_root / "schemas" / "four_port_record_v3.schema.json"
    schema_sha = sha_file(schema_path)
    hard_path = package_root / "certificates" / "direct_hard_cases.json"
    hard_hash = sha_file(hard_path)

    source_descriptor, classes, members = class_universe(
        args.source_index, sources, rows, source_descriptors, cache, ranks
    )
    end = len(classes) if args.end is None else min(args.end, len(classes))
    if not 0 <= args.start <= end:
        raise SystemExit((args.start, end))

    output_root = args.output_root.resolve()
    run_dir = output_root / f"source_{args.source_index}"
    records_dir = run_dir / "records"
    records_dir.mkdir(parents=True, exist_ok=True)

    lock_path = run_dir / "source.lock"
    lock_handle = lock_path.open("a+")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f"another process holds {lock_path}")

    immutable = {
        "schema": SCHEMA,
        "canonicalizer_sha256": canonicalizer_sha,
        "compiler_sha256": compiler_sha,
        "descriptor_pickle_sha256": descriptor_pickle_sha,
        "rank_pickle_sha256": rank_pickle_sha,
        "output_schema_sha256": schema_sha,
        "input_lock_sha256": input_lock_sha,
    }
    processed, reused, counts = 0, 0, {}
    source_graph_sha = sha_object(graph_payload(sources[args.source_index].graph))

    try:
        for class_id in range(args.start, end):
            descriptor = classes[class_id]
            output = records_dir / f"class_{class_id:06d}.json"
            common = {
                **immutable,
                "source_index": args.source_index,
                "canonical_class_id": class_id,
                "descriptor_sha256": sha_object(descriptor),
                "source_graph_sha256": source_graph_sha,
                "direction": "source_to_target",
                "source_rank": ranks[source_descriptor]["rank"],
                "target_rank": ranks[descriptor]["rank"],
            }
            if output.exists() and not args.force:
                old = json.loads(output.read_text())
                validate_record(old, common, output)
                reused += 1
                counts[old["status"]] = counts.get(old["status"], 0) + 1
                continue

            status, certificate, stratum, member_rows, child_requests, elapsed = classify_one(
                atlas,
                args.source_index,
                class_id,
                source_descriptor,
                descriptor,
                members[class_id],
                sources,
                targets,
                hard_hash,
            )
            target_graph_hash = sha_object(sorted(row["target_selected_graph_sha256"] for row in member_rows))
            all_port_matches = sorted({tuple(row["port_match"]) for row in member_rows})
            payload = {
                **common,
                "target_graph_sha256": target_graph_hash,
                "incoming_roles": {
                    "source_selected": sources[args.source_index].incoming_selected,
                    "targets": sorted(set(row["incoming_selected"] for row in member_rows)),
                },
                "port_match": member_rows[0]["port_match"],
                "port_matches": [list(match) for match in all_port_matches],
                "omitted_roles": sorted({role for row in member_rows for role in row["dummy_roles"]}),
                "stratum": stratum,
                "status": status,
                "certificate": certificate,
                "certificate_payload_sha256": None if certificate is None else sha_object(certificate),
                "restoration_parent_id": None,
                "child_requests": child_requests,
                "members": member_rows,
                "runtime_seconds": elapsed,
                "peak_rss_bytes": peak_rss_bytes(),
                "runtime_platform": {
                    "python": sys.version,
                    "platform": platform.platform(),
                    "machine": platform.machine(),
                },
                "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            }
            payload["record_payload_sha256"] = payload_hash(payload)
            atomic_json(output, payload)
            processed += 1
            counts[status] = counts.get(status, 0) + 1
            atomic_json(run_dir / "progress.json", {
                "source_index": args.source_index,
                "next_class_id": class_id + 1,
                "end": end,
                "processed_this_invocation": processed,
                "reused": reused,
                "counts": counts,
                **immutable,
            })
            if args.manifest_every > 0 and processed % args.manifest_every == 0:
                build_manifest(run_dir, records_dir, args.source_index, len(classes), immutable)
            print(json.dumps({"class_id": class_id, "status": status, "seconds": elapsed}), flush=True)

        manifest = build_manifest(run_dir, records_dir, args.source_index, len(classes), immutable)
        print(json.dumps({
            "DONE": True,
            "source_index": args.source_index,
            "range": [args.start, end],
            "processed": processed,
            "reused": reused,
            "counts": counts,
            "manifest_complete": manifest["complete"],
            "compiler_sha256": compiler_sha,
            "canonicalizer_sha256": canonicalizer_sha,
        }), flush=True)
    finally:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
        lock_handle.close()


if __name__ == "__main__":
    main()
