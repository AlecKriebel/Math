#!/usr/bin/env python3
"""Small exact utilities for the primitive three-port cycle closure."""

from __future__ import annotations

import ast
import dataclasses
import gzip
import hashlib
import importlib.util
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
DEFAULT_PACKAGE_ROOT = PROJECT_ROOT / "package/referee/k2p_offline_sweep_portable"
DEFAULT_ARTIFACT_ROOT = HERE / "artifacts"
STRICT_JSON_DIR = PROJECT_ROOT / "work/final_theorem_release"
if str(STRICT_JSON_DIR) not in sys.path:
    sys.path.insert(0, str(STRICT_JSON_DIR))

from strict_json import StrictJSONError, decode_json_document  # noqa: E402


class ClosureFailure(RuntimeError):
    pass


def fail(code: str, detail: object | None = None) -> "None":
    raise ClosureFailure(code if detail is None else f"{code}: {detail}")


def canonical_data(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: canonical_data(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, dict):
        return {
            str(key): canonical_data(item)
            for key, item in sorted(value.items(), key=lambda pair: repr(pair[0]))
        }
    if isinstance(value, (tuple, list)):
        return [canonical_data(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return sorted((canonical_data(item) for item in value), key=repr)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        canonical_data(value), sort_keys=True, separators=(",", ":")
    ).encode()


def pretty_json_bytes(value: Any) -> bytes:
    return (json.dumps(canonical_data(value), sort_keys=True, indent=2) + "\n").encode()


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    with temporary.open("wb") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_bytes(path, pretty_json_bytes(value))


def deterministic_gzip(path: Path, chunks: Iterable[bytes]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    plain_digest = hashlib.sha256()
    plain_bytes = 0
    rows = 0
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            for chunk in chunks:
                plain_digest.update(chunk)
                plain_bytes += len(chunk)
                rows += 1
                encoded.write(chunk)
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(temporary, path)
    return {
        "sha256": sha_file(path),
        "plain_sha256": plain_digest.hexdigest(),
        "plain_bytes": plain_bytes,
        "rows": rows,
    }


def load_atlas(package_root: Path = DEFAULT_PACKAGE_ROOT):
    path = package_root / "atlas/k2p_atlas_core.py"
    name = f"k2p_cycle_atlas_{hashlib.sha256(str(path).encode()).hexdigest()[:12]}"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail("CYCLE_ATLAS_IMPORT_FAIL", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonicalizer_sha256(atlas) -> str:
    source = "\n".join(
        inspect.getsource(getattr(atlas, name))
        for name in (
            "mixed_incidence_graph",
            "mixed_exact_isomorphic",
            "mixed_relation_exact",
            "_mixed_triangle_edges",
        )
    )
    return hashlib.sha256(source.encode()).hexdigest()


def descriptor_sha256(descriptor) -> str:
    return sha_object(descriptor)


def source_insertion_candidates(graph) -> list[dict[str, object]]:
    rows = []
    for tail, head, data in sorted(
        graph.edges(data=True), key=lambda row: (repr(row[0]), repr(row[1]))
    ):
        if graph.nodes[head].get("role") == "leaf":
            continue
        if graph.nodes[tail].get("role") == "root":
            continue
        rows.append(
            {
                "tail": repr(tail),
                "head": repr(head),
                "edge_role": data.get("edge_role"),
            }
        )
    return rows


def insert_source_leaf(atlas, graph, candidate: dict[str, object], label: int):
    result = graph.copy()
    tail = ast.literal_eval(str(candidate["tail"]))
    head = ast.literal_eval(str(candidate["head"]))
    if not result.has_edge(tail, head):
        fail("CYCLE_INSERTION_EDGE_MISSING", candidate)
    edge_data = dict(result.edges[tail, head])
    result.remove_edge(tail, head)
    subdivision = ("cycle_restoration_subdivision", label, repr(tail), repr(head))
    leaf = ("leaf", "cycle_restoration", label)
    if subdivision in result or leaf in result:
        fail("CYCLE_INSERTION_NODE_COLLISION", (subdivision, leaf))
    result.add_node(subdivision, role="tree", label=None, dummy=False)
    result.add_node(leaf, role="leaf", label=label, dummy=False, dummy_name=None)
    result.add_edge(tail, subdivision, **edge_data)
    result.add_edge(subdivision, head, **edge_data)
    result.add_edge(subdivision, leaf, edge_role="arm")
    atlas.validate_graph(result)
    return result


def relabel_and_promote_all(atlas, record, permutation, roles):
    result = atlas.relabel_record(record, tuple(permutation)).graph
    for offset, role in enumerate(roles):
        nodes = [
            node
            for node, data in result.nodes(data=True)
            if data.get("dummy_name") == role
        ]
        if len(nodes) != 1:
            fail("CYCLE_TARGET_ROLE_FAIL", (role, nodes))
        node = nodes[0]
        result.nodes[node]["label"] = 3 + offset
        result.nodes[node]["dummy"] = False
        result.nodes[node]["dummy_name"] = None
    labels = sorted(
        data["label"]
        for _, data in result.nodes(data=True)
        if isinstance(data.get("label"), int)
    )
    if labels != list(range(3 + len(roles))):
        fail("CYCLE_PROMOTED_LABEL_SET_FAIL", labels)
    atlas.validate_graph(result)
    return result


def split_set_json(split_set) -> list[list[list[int]]]:
    rows = []
    for split in split_set:
        if split == ("star",):
            fail("CYCLE_STAR_QUARTET_FORBIDDEN")
        rows.append([list(split[0]), list(split[1])])
    return sorted(rows)


def topology_decision(source_signature, target_signature):
    source_labels, source_quartets, source_triples = source_signature
    target_labels, target_quartets, target_triples = target_signature
    if source_labels != target_labels:
        fail("CYCLE_TOPOLOGY_LABEL_MISMATCH", (source_labels, target_labels))
    for (quartet, source_set), (other, target_set) in zip(
        source_quartets, target_quartets
    ):
        if quartet != other:
            fail("CYCLE_QUARTET_ORDER_MISMATCH", (quartet, other))
        if source_set == target_set:
            continue
        source_values = set(source_set)
        target_values = set(target_set)
        if not source_values or not target_values:
            fail("CYCLE_EMPTY_DISPLAYED_SET", quartet)
        if len(source_values) == 1:
            split = min(source_values, key=repr)
            zero_on, positive_on, kind = "source", "target", "I_singleton"
        elif len(target_values) == 1:
            split = min(target_values, key=repr)
            zero_on, positive_on, kind = "target", "source", "I_singleton"
        else:
            difference = target_values - source_values
            if difference:
                split = min(difference, key=repr)
                zero_on, positive_on = "source", "target"
            else:
                split = min(source_values - target_values, key=repr)
                zero_on, positive_on = "target", "source"
            kind = "J_membership"
        return {
            "reason": "displayed_quartet_mismatch",
            "quartet": list(quartet),
            "source_displayed_splits": split_set_json(source_values),
            "target_displayed_splits": split_set_json(target_values),
            "invariant_kind": kind,
            "distinguished_split": [list(split[0]), list(split[1])],
            "zero_on": zero_on,
            "strictly_positive_on": positive_on,
            "theorem": "Englander-et-al-v4-Propositions-2.9-2.10-Theorem-2.11",
        }
    source_types = dict(source_triples)
    target_types = dict(target_triples)
    for triple in sorted(source_types):
        if {source_types[triple], target_types[triple]} != {"tree", "sunlet"}:
            continue
        source_type = source_types[triple]
        target_type = target_types[triple]
        return {
            "reason": "tree_sunlet_strict_sign",
            "triple": list(triple),
            "source_type": source_type,
            "target_type": target_type,
            "zero_on": "source" if source_type == "tree" else "target",
            "strictly_negative_on": "source" if source_type == "sunlet" else "target",
            "invariant": "T3=V^2*X_g-X_s^2*Y_g*Z_g",
            "sunlet_pullback": "-a_s^2*b_s^2*a_g*b_g*c_g^2*f_s^2*delta*(1-delta)*d_g*e_g*(1-f_g)^2",
        }
    return None


def witness_id(content: dict[str, Any]) -> str:
    prefix = "QW" if content["reason"] == "displayed_quartet_mismatch" else "TS"
    return f"{prefix}:{sha_object(content)}"


def exact_transport_records(atlas, source_graph, target_graph, relation: str):
    source_mixed = atlas.sd0_mixed(source_graph)
    target_mixed = atlas.sd0_mixed(target_graph)
    if relation == "isomorphic":
        triangle_pairs = ((None, None),)
    elif relation == "triangle":
        triangle_pairs = tuple(
            (source_triangle, target_triangle)
            for source_triangle in atlas._mixed_triangle_edges(source_mixed)
            for target_triangle in atlas._mixed_triangle_edges(target_mixed)
        )
    else:
        fail("CYCLE_TRANSPORT_RELATION_FAIL", relation)
    node_match = (
        lambda left, right: left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    unique = {}
    for source_triangle, target_triangle in triangle_pairs:
        source = atlas.mixed_incidence_graph(source_mixed, source_triangle)
        target = atlas.mixed_incidence_graph(target_mixed, target_triangle)
        matcher = atlas.nx.algorithms.isomorphism.GraphMatcher(
            source, target, node_match=node_match, edge_match=edge_match
        )
        for mapping in matcher.isomorphisms_iter():
            ordered_mapping = sorted(
                mapping.items(), key=lambda pair: canonical_json_bytes(pair[0])
            )
            public_mapping = [
                [canonical_data(left), canonical_data(right)]
                for left, right in ordered_mapping
            ]
            public_source_triangle = None
            public_target_triangle = None
            if source_triangle is not None:
                public_source_triangle = sorted(
                    [
                        sorted(
                            [canonical_data(left), canonical_data(right)],
                            key=lambda item: canonical_json_bytes(item),
                        )
                        for left, right in source_triangle
                    ],
                    key=lambda item: canonical_json_bytes(item),
                )
                public_target_triangle = sorted(
                    [
                        sorted(
                            [canonical_data(left), canonical_data(right)],
                            key=lambda item: canonical_json_bytes(item),
                        )
                        for left, right in target_triangle
                    ],
                    key=lambda item: canonical_json_bytes(item),
                )
            record = {
                "relation": relation,
                "incidence_node_mapping_source_to_target": public_mapping,
                "source_triangle_edges": public_source_triangle,
                "target_triangle_edges": public_target_triangle,
            }
            unique[sha_object(record)] = record
    return [unique[key] for key in sorted(unique)]


def read_json(path: Path):
    try:
        return decode_json_document(
            path.read_bytes(), label=path.name, require_object=True
        )
    except (OSError, StrictJSONError) as exc:
        fail("CYCLE_JSON_READ_FAIL", f"{path}: {exc}")
