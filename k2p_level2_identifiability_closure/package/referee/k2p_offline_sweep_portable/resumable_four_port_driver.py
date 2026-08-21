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
import gc
import hashlib
import importlib.metadata
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
DIAGNOSTIC_FIELDS = frozenset({
    "runtime_seconds",
    "peak_rss_bytes",
    "runtime_platform",
    "generated_at_utc",
    "record_payload_sha256",
    "semantic_record_sha256",
})
VALID_STATUSES = frozenset({
    "separated", "isomorphic", "triangle", "restoration_parent", "unresolved", "error"
})


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


def semantic_payload_hash(payload: dict) -> str:
    """Hash the mathematical record independently of platform/run diagnostics."""
    body = {key: value for key, value in payload.items() if key not in DIAGNOSTIC_FIELDS}
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
        for name in (
            "mixed_incidence_graph", "mixed_exact_isomorphic", "mixed_relation_exact",
            "_mixed_triangle_edges", "prepare_mixed_source", "mixed_relation_exact_prepared",
        )
    )
    return compiler, sha_bytes(canonicalizer_source.encode())


def validate_input_lock(package_root: Path, lock: dict) -> dict[str, str]:
    if lock.get("schema") != "k2p-offline-four-port-input-lock-v1":
        raise SystemExit("unsupported INPUT_LOCK schema")
    for distribution, expected in lock.get("dependency_versions", {}).items():
        try:
            observed_version = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            raise SystemExit(f"missing locked dependency: {distribution}")
        if observed_version != expected:
            raise SystemExit(
                f"locked dependency version mismatch: {distribution}: {observed_version} != {expected}"
            )
    observed_hashes = {}
    for relative, expected in lock["files"].items():
        path = package_root / relative
        if not path.is_file():
            raise SystemExit(f"missing locked input: {relative}")
        observed = sha_file(path)
        if observed != expected:
            raise SystemExit(f"locked input hash mismatch: {relative}: {observed}")
        observed_hashes[relative] = observed
    return observed_hashes


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


def compact_rank_map(source_descriptors, cache, loaded_ranks):
    """Retain only integer ranks keyed by descriptor objects already in the main input."""
    compact = {}
    for collection in (source_descriptors, cache.values()):
        for descriptor in collection:
            if descriptor not in compact:
                compact[descriptor] = {"rank": int(loaded_ranks[descriptor]["rank"])}
    return compact


def validate_hard_case_bindings(
    hard_path: Path,
    sources,
    targets,
    rows,
    source_descriptors,
    cache,
    ranks,
) -> None:
    """Bind the four shipped algebraic cases to their exact finite-atlas classes."""
    payload = json.loads(hard_path.read_text())
    cases = payload.get("cases")
    if not isinstance(cases, list) or {case.get("class_id") for case in cases} != {206, 207, 208, 209}:
        raise SystemExit("invalid direct hard-case class census")
    source_descriptor, classes, members = class_universe(
        0, sources, rows, source_descriptors, cache, ranks
    )
    for case in cases:
        class_id = case["class_id"]
        if case.get("source_rank") != ranks[source_descriptor]["rank"]:
            raise SystemExit(f"hard-case source-rank mismatch: {class_id}")
        if case.get("target_rank") != ranks[classes[class_id]]["rank"]:
            raise SystemExit(f"hard-case target-rank mismatch: {class_id}")
        binding = (case.get("target_index"), tuple(case.get("relative_permutation", ())))
        if binding not in {(target_index, tuple(permutation)) for target_index, permutation in members[class_id]}:
            raise SystemExit(f"hard-case target/permutation mismatch: {class_id}")
        if targets[binding[0]].dummy_labels:
            raise SystemExit(f"hard-case target is not direct: {class_id}")


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
    prepared_mixed_source,
    source_insertions,
):
    started = time.perf_counter()
    relations, member_rows, omitted, direct_flags = set(), [], set(), []
    source_graph = sources[source_index].graph
    for target_index, permutation in members:
        relabelled = atlas.relabel_record(targets[target_index], permutation)
        selected = atlas.selected_graph_from_completion(relabelled)
        relation = atlas.mixed_relation_exact_prepared(prepared_mixed_source, selected)
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

    status, certificate = "unresolved", None
    # The four exact F2/F3/F4 certificates are already independently bound and
    # do not need the generic separator search.  All other certificate
    # precedence remains identical to the frozen driver.
    if source_index == 0 and class_id in (206, 207, 208, 209):
        if hard_certificate_hash is None:
            raise RuntimeError("direct hard-case certificate is missing")
        status = "separated"
        certificate = {
            "type": "direct_hard_case_F2_F3_F4",
            "certificate_sha256": hard_certificate_hash,
            "class_id": class_id,
        }
    else:
        separator = atlas.quadratic_separator_fast(source_descriptor, target_descriptor, max_block_size=16)
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
                "source_insertion_edge_candidates": source_insertions,
                "target_dummy_attachments": attachments,
                "require_direct_marginal": True,
            })
    elapsed = time.perf_counter() - started
    return status, certificate, stratum, member_rows, child_requests, elapsed


def record_problem(path: Path, field: str) -> None:
    raise SystemExit(f"stale/corrupt record {path}: {field}")


def validate_record_semantics(row: dict, path: Path, hard_certificate_hash: str | None) -> None:
    required = {
        "schema", "canonicalizer_sha256", "compiler_sha256", "descriptor_pickle_sha256",
        "rank_pickle_sha256", "output_schema_sha256", "input_lock_sha256",
        "hard_certificate_sha256", "source_index", "canonical_class_id",
        "descriptor_sha256", "source_graph_sha256", "target_graph_sha256", "direction",
        "incoming_roles", "port_match", "port_matches", "omitted_roles", "source_rank",
        "target_rank", "stratum", "status", "certificate", "certificate_payload_sha256",
        "restoration_parent_id", "child_requests", "members", "runtime_seconds",
        "peak_rss_bytes", "runtime_platform", "generated_at_utc",
        "semantic_record_sha256", "record_payload_sha256",
    }
    missing = sorted(required - set(row))
    if missing:
        record_problem(path, f"missing fields {missing}")
    if row.get("record_payload_sha256") != payload_hash(row):
        record_problem(path, "record_payload_sha256")
    if row.get("semantic_record_sha256") != semantic_payload_hash(row):
        record_problem(path, "semantic_record_sha256")
    if row.get("direction") != "source_to_target":
        record_problem(path, "direction")
    if row.get("status") not in VALID_STATUSES or row.get("status") == "error":
        record_problem(path, "status")

    certificate = row.get("certificate")
    certificate_hash = None if certificate is None else sha_object(certificate)
    if row.get("certificate_payload_sha256") != certificate_hash:
        record_problem(path, "certificate_payload_sha256")
    certificate_type = certificate.get("type") if isinstance(certificate, dict) else None
    expected_types = {
        "isomorphic": "exact_mixed_graph_isomorphism",
        "triangle": "ordinary_triangle_quotient",
        "restoration_parent": "requires_direct_child_restoration",
    }
    status = row["status"]
    if status == "separated":
        if certificate_type not in {"exact_multihomogeneous_quadratic", "direct_hard_case_F2_F3_F4"}:
            record_problem(path, "separated certificate")
        if certificate_type == "exact_multihomogeneous_quadratic":
            if certificate.get("degree") != 2 or not certificate.get("coefficients"):
                record_problem(path, "quadratic certificate")
        else:
            class_id = row.get("canonical_class_id")
            if row.get("source_index") != 0 or class_id not in {206, 207, 208, 209}:
                record_problem(path, "hard-case identity")
            if certificate.get("class_id") != class_id:
                record_problem(path, "hard-case class_id")
            if hard_certificate_hash is None or certificate.get("certificate_sha256") != hard_certificate_hash:
                record_problem(path, "hard-case certificate_sha256")
    elif status == "unresolved":
        if certificate is not None:
            record_problem(path, "unresolved certificate")
    elif certificate_type != expected_types.get(status):
        record_problem(path, f"{status} certificate")

    members = row.get("members")
    if not isinstance(members, list) or not members or not all(isinstance(member, dict) for member in members):
        record_problem(path, "members")
    try:
        member_matches = [tuple(member["port_match"]) for member in members]
        expected_matches = [list(match) for match in sorted(set(member_matches))]
        expected_omitted = sorted({role for member in members for role in member["dummy_roles"]})
        expected_target_hash = sha_object(sorted(member["target_selected_graph_sha256"] for member in members))
        expected_target_roles = sorted(set(member["incoming_selected"] for member in members))
    except (KeyError, TypeError, ValueError):
        record_problem(path, "member shape")
    if row.get("port_match") != members[0].get("port_match"):
        record_problem(path, "port_match")
    if row.get("port_matches") != expected_matches:
        record_problem(path, "port_matches")
    if row.get("omitted_roles") != expected_omitted:
        record_problem(path, "omitted_roles")
    if row.get("target_graph_sha256") != expected_target_hash:
        record_problem(path, "target_graph_sha256")
    incoming_roles = row.get("incoming_roles")
    if not isinstance(incoming_roles, dict) or incoming_roles.get("targets") != expected_target_roles:
        record_problem(path, "incoming_roles")

    expected_stratum = "restoration_candidate" if expected_omitted else "direct_no_dummy"
    if row.get("stratum") != expected_stratum:
        record_problem(path, "stratum")
    child_requests = row.get("child_requests")
    if not isinstance(child_requests, list):
        record_problem(path, "child_requests")
    child_roles = [request.get("omitted_role") for request in child_requests if isinstance(request, dict)]
    if sorted(child_roles) != expected_omitted or len(child_roles) != len(child_requests):
        record_problem(path, "child request roles")
    if any(request.get("require_direct_marginal") is not True for request in child_requests):
        record_problem(path, "child request direct-marginal flag")
    if status == "restoration_parent" and not expected_omitted:
        record_problem(path, "restoration parent stratum")
    relations = {member.get("graph_relation") for member in members}
    if not relations <= {"none", "isomorphic", "triangle"}:
        record_problem(path, "member graph_relation")
    if status == "isomorphic" and relations != {"isomorphic"}:
        record_problem(path, "isomorphic graph relations")
    if status == "triangle" and not (
        relations <= {"isomorphic", "triangle"} and "triangle" in relations
    ):
        record_problem(path, "triangle graph relations")


def validate_record(
    row: dict,
    common: dict,
    path: Path,
    hard_certificate_hash: str | None,
) -> None:
    for key, value in common.items():
        if row.get(key) != value:
            record_problem(path, key)
    validate_record_semantics(row, path, hard_certificate_hash)


def semantic_manifest_hash(source_index: int, class_count: int, immutable: dict, records: list) -> str:
    semantic_records = [
        {key: value for key, value in record.items() if key != "record_sha256"}
        for record in records
    ]
    return sha_object({
        "source_index": source_index,
        "canonical_class_count": class_count,
        "immutable": immutable,
        "records": semantic_records,
    })


def build_manifest(
    run_dir: Path,
    records_dir: Path,
    source_index: int,
    class_count: int,
    immutable: dict,
    hard_certificate_hash: str,
) -> dict:
    records = []
    class_ids = set()
    for path in sorted(records_dir.glob("class_*.json")):
        row = json.loads(path.read_text())
        try:
            filename_class_id = int(path.stem.removeprefix("class_"))
        except ValueError:
            raise SystemExit(f"invalid record filename: {path}")
        for key, value in immutable.items():
            if row.get(key) != value:
                raise SystemExit(f"old-input record rejected: {path}: {key}")
        if row.get("source_index") != source_index:
            raise SystemExit(f"cross-source record rejected: {path}")
        if row.get("canonical_class_id") != filename_class_id:
            raise SystemExit(f"filename/class-id disagreement: {path}")
        validate_record_semantics(row, path, hard_certificate_hash)
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
            "semantic_record_sha256": row["semantic_record_sha256"],
            "omitted_roles": row["omitted_roles"],
            "child_requests": row["child_requests"],
        })
    manifest = {
        **immutable,
        "record_schema": immutable["schema"],
        "schema": MANIFEST_SCHEMA,
        "source_index": source_index,
        "canonical_class_count": class_count,
        "record_count": len(records),
        "complete": len(records) == class_count and class_ids == set(range(class_count)),
        "records": records,
        "unresolved": [row["canonical_class_id"] for row in records if row["status"] == "unresolved"],
        "restoration_candidates": [
            row["canonical_class_id"] for row in records if row["status"] == "restoration_parent"
        ],
    }
    manifest["semantic_manifest_sha256"] = semantic_manifest_hash(
        source_index, class_count, immutable, records
    )
    atomic_json(run_dir / "residual_manifest.json", manifest)
    return manifest


def run_source(
    args,
    source_index,
    atlas,
    sources,
    targets,
    rows,
    source_descriptors,
    cache,
    ranks,
    compiler_sha,
    canonicalizer_sha,
    descriptor_pickle_sha,
    rank_pickle_sha,
    schema_sha,
    input_lock_sha,
    hard_hash,
) -> None:
    if not 0 <= source_index < len(source_descriptors):
        raise SystemExit(f"source index out of range: {source_index}")
    source_descriptor, classes, members = class_universe(
        source_index, sources, rows, source_descriptors, cache, ranks
    )
    end = len(classes) if args.end is None else min(args.end, len(classes))
    if not 0 <= args.start <= end:
        raise SystemExit((args.start, end))

    output_root = args.output_root.resolve()
    run_dir = output_root / f"source_{source_index}"
    records_dir = run_dir / "records"
    records_dir.mkdir(parents=True, exist_ok=True)
    lock_path = run_dir / "source.lock"
    lock_handle = lock_path.open("a+")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_handle.close()
        raise SystemExit(f"another process holds {lock_path}")

    immutable = {
        "schema": SCHEMA,
        "canonicalizer_sha256": canonicalizer_sha,
        "compiler_sha256": compiler_sha,
        "descriptor_pickle_sha256": descriptor_pickle_sha,
        "rank_pickle_sha256": rank_pickle_sha,
        "output_schema_sha256": schema_sha,
        "input_lock_sha256": input_lock_sha,
        "hard_certificate_sha256": hard_hash,
    }
    processed, reused, counts = 0, 0, {}
    source_graph = sources[source_index].graph
    source_graph_sha = sha_object(graph_payload(source_graph))
    prepared_mixed_source = atlas.prepare_mixed_source(source_graph)
    source_insertions = source_insertion_candidates(source_graph)

    try:
        for class_id in range(args.start, end):
            descriptor = classes[class_id]
            output = records_dir / f"class_{class_id:06d}.json"
            common = {
                **immutable,
                "source_index": source_index,
                "canonical_class_id": class_id,
                "descriptor_sha256": sha_object(descriptor),
                "source_graph_sha256": source_graph_sha,
                "direction": "source_to_target",
                "source_rank": ranks[source_descriptor]["rank"],
                "target_rank": ranks[descriptor]["rank"],
            }
            if output.exists() and not args.force:
                old = json.loads(output.read_text())
                validate_record(old, common, output, hard_hash)
                reused += 1
                counts[old["status"]] = counts.get(old["status"], 0) + 1
                continue

            status, certificate, stratum, member_rows, child_requests, elapsed = classify_one(
                atlas, source_index, class_id, source_descriptor, descriptor,
                members[class_id], sources, targets, hard_hash,
                prepared_mixed_source, source_insertions,
            )
            target_graph_hash = sha_object(sorted(row["target_selected_graph_sha256"] for row in member_rows))
            all_port_matches = sorted({tuple(row["port_match"]) for row in member_rows})
            payload = {
                **common,
                "target_graph_sha256": target_graph_hash,
                "incoming_roles": {
                    "source_selected": sources[source_index].incoming_selected,
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
            payload["semantic_record_sha256"] = semantic_payload_hash(payload)
            payload["record_payload_sha256"] = payload_hash(payload)
            atomic_json(output, payload)
            processed += 1
            counts[status] = counts.get(status, 0) + 1
            atomic_json(run_dir / "progress.json", {
                "source_index": source_index,
                "next_class_id": class_id + 1,
                "end": end,
                "processed_this_invocation": processed,
                "reused": reused,
                "counts": counts,
                **immutable,
            })
            if args.manifest_every > 0 and processed % args.manifest_every == 0:
                build_manifest(run_dir, records_dir, source_index, len(classes), immutable, hard_hash)
            print(json.dumps({
                "source_index": source_index, "class_id": class_id,
                "status": status, "seconds": elapsed,
            }), flush=True)

        manifest = build_manifest(
            run_dir, records_dir, source_index, len(classes), immutable, hard_hash
        )
        print(json.dumps({
            "DONE": True,
            "source_index": source_index,
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
        atlas._OUTPUT_POLY_CACHE.clear()
        atlas._QUADRATIC_SOURCE_PRODUCT_CACHE.clear()
        gc.collect()


def audit_prepared_relations(atlas, sources, targets, rows, source_descriptors, cache, ranks) -> dict:
    """Exhaustively compare prepared and frozen relation paths on eligible presentations."""
    checked, census, source_ranks = 0, [], []
    for source_index in range(len(source_descriptors)):
        source_descriptor, classes, members = class_universe(
            source_index, sources, rows, source_descriptors, cache, ranks
        )
        source_graph = sources[source_index].graph
        prepared = atlas.prepare_mixed_source(source_graph)
        for class_members in members:
            for target_index, permutation in class_members:
                relabelled = atlas.relabel_record(targets[target_index], permutation)
                selected = atlas.selected_graph_from_completion(relabelled)
                frozen = atlas.mixed_relation_exact(source_graph, selected)
                optimized = atlas.mixed_relation_exact_prepared(prepared, selected)
                if frozen != optimized:
                    raise SystemExit(
                        f"prepared relation mismatch: source={source_index} "
                        f"target={target_index} permutation={permutation}: {frozen} != {optimized}"
                    )
                checked += 1
        census.append(len(classes))
        source_ranks.append(ranks[source_descriptor]["rank"])
    return {
        "prepared_relation_presentations_checked": checked,
        "source_class_counts": census,
        "source_ranks": source_ranks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-index", type=int, action="append")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--end", type=int)
    parser.add_argument("--package-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-root", type=Path, default=Path.cwd() / "k2p_four_port_run")
    parser.add_argument("--expected-compiler-sha256")
    parser.add_argument("--expected-canonicalizer-sha256")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--manifest-every", type=int, default=25)
    parser.add_argument("--list-sources", action="store_true")
    parser.add_argument("--audit-prepared-relations", action="store_true")
    args = parser.parse_args()

    if args.manifest_every < 0:
        raise SystemExit("--manifest-every must be nonnegative")
    source_indices = args.source_index or []
    if not (args.list_sources or args.audit_prepared_relations) and not source_indices:
        parser.error("at least one --source-index is required unless --list-sources is used")
    if len(source_indices) != len(set(source_indices)):
        parser.error("duplicate --source-index")
    if len(source_indices) > 1 and (args.start != 0 or args.end is not None):
        parser.error("--start/--end may be used only with one --source-index")

    package_root = args.package_root.resolve()
    atlas_root = package_root / "atlas"
    input_lock_path = package_root / "INPUT_LOCK.json"
    input_lock = json.loads(input_lock_path.read_text())
    observed_hashes = validate_input_lock(package_root, input_lock)
    input_lock_sha = sha_file(input_lock_path)

    atlas = load_module(atlas_root / "k2p_atlas_core.py")
    compiler_sha, canonicalizer_sha = current_hashes(atlas_root, atlas)
    if input_lock.get("compiler_sha256") != compiler_sha:
        raise SystemExit(f"INPUT_LOCK compiler hash mismatch: {compiler_sha}")
    if input_lock.get("canonicalizer_sha256") != canonicalizer_sha:
        raise SystemExit(f"INPUT_LOCK canonicalizer hash mismatch: {canonicalizer_sha}")
    if args.expected_compiler_sha256 and args.expected_compiler_sha256 != compiler_sha:
        raise SystemExit(f"compiler hash mismatch: {compiler_sha}")
    if args.expected_canonicalizer_sha256 and args.expected_canonicalizer_sha256 != canonicalizer_sha:
        raise SystemExit(f"canonicalizer hash mismatch: {canonicalizer_sha}")

    descriptor_path = atlas_root / "descriptors_4.pkl"
    rank_path = atlas_root / "rank_certs_4.pkl"
    with descriptor_path.open("rb") as handle:
        sources, targets, rows, source_descriptors, cache = pickle.load(handle)
    with rank_path.open("rb") as handle:
        loaded_ranks = pickle.load(handle)
    ranks = compact_rank_map(source_descriptors, cache, loaded_ranks)
    del loaded_ranks
    gc.collect()
    validate_hard_case_bindings(
        package_root / "certificates" / "direct_hard_cases.json",
        sources, targets, rows, source_descriptors, cache, ranks,
    )

    if args.audit_prepared_relations:
        print(json.dumps(
            audit_prepared_relations(
                atlas, sources, targets, rows, source_descriptors, cache, ranks
            ),
            sort_keys=True,
            indent=2,
        ))
        return

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

    descriptor_pickle_sha = observed_hashes["atlas/descriptors_4.pkl"]
    rank_pickle_sha = observed_hashes["atlas/rank_certs_4.pkl"]
    schema_sha = observed_hashes["schemas/four_port_record_v3.schema.json"]
    hard_hash = observed_hashes["certificates/direct_hard_cases.json"]
    for source_index in source_indices:
        run_source(
            args, source_index, atlas, sources, targets, rows, source_descriptors, cache, ranks,
            compiler_sha, canonicalizer_sha, descriptor_pickle_sha, rank_pickle_sha,
            schema_sha, input_lock_sha, hard_hash,
        )


if __name__ == "__main__":
    main()
