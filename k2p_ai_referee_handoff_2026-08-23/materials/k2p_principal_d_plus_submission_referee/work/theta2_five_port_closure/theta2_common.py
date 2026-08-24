#!/usr/bin/env python3
"""Shared exact utilities for the primitive theta2 five-port closure."""

from __future__ import annotations

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
ARTIFACT_ROOT = HERE / "artifacts"

SOURCE_COUNT = 4
TARGET_COUNT = 6138
PERMUTATION_COUNT = 120
RAW_PER_SOURCE = TARGET_COUNT * PERMUTATION_COUNT
RAW_TOTAL = SOURCE_COUNT * RAW_PER_SOURCE


def fail(code: str, detail: object | None = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


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
    return (json.dumps(canonical_data(value), indent=2, sort_keys=True) + "\n").encode()


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


def deterministic_gzip(path: Path, chunks: Iterable[bytes]) -> tuple[str, int]:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    plain_digest = hashlib.sha256()
    plain_bytes = 0
    with temporary.open("wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as encoded:
            for chunk in chunks:
                plain_digest.update(chunk)
                plain_bytes += len(chunk)
                encoded.write(chunk)
        raw.flush()
        os.fsync(raw.fileno())
    os.replace(temporary, path)
    return plain_digest.hexdigest(), plain_bytes


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail("THETA2_JSON_FAIL", f"{path}: {exc}")
    if not isinstance(value, dict):
        fail("THETA2_JSON_OBJECT_FAIL", path)
    return value


def load_atlas(package_root: Path):
    path = package_root / "atlas/k2p_atlas_core.py"
    name = "k2p_theta2_five_port_atlas_core"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail("THETA2_ATLAS_IMPORT_FAIL", path)
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
            "prepare_mixed_source",
            "mixed_relation_exact_prepared",
        )
    )
    return hashlib.sha256(source.encode()).hexdigest()


def descriptor_sha256(descriptor) -> str:
    return sha_object(descriptor)


def split_set_json(split_set) -> list[list[list[int]]]:
    rows = []
    for split in split_set:
        if split == ("star",):
            fail("THETA2_STAR_QUARTET_FORBIDDEN")
        rows.append([list(split[0]), list(split[1])])
    return sorted(rows)


def topology_decision(source_signature, permuted_target_signature):
    """Return an exact pointwise witness, or ``None`` when topology survives."""
    _labels, source_quartets, source_triples = source_signature
    target_quartets, target_triples = permuted_target_signature
    for (quad, source_set), (target_quad, target_set) in zip(
        source_quartets, target_quartets
    ):
        if quad != target_quad:
            fail("THETA2_QUARTET_LABEL_ALIGNMENT_FAIL", (quad, target_quad))
        if source_set == target_set:
            continue
        source_values = set(source_set)
        target_values = set(target_set)
        if not source_values or not target_values:
            fail("THETA2_EMPTY_DISPLAYED_SET", quad)
        if len(source_values) == 1:
            split = next(iter(source_values))
            zero_on, positive_on = "source", "target"
            kind = "I_singleton"
        elif len(target_values) == 1:
            split = next(iter(target_values))
            zero_on, positive_on = "target", "source"
            kind = "I_singleton"
        else:
            target_difference = target_values - source_values
            if target_difference:
                split = min(target_difference, key=repr)
                zero_on, positive_on = "source", "target"
            else:
                split = min(source_values - target_values, key=repr)
                zero_on, positive_on = "target", "source"
            kind = "J_membership"
        content = {
            "reason": "displayed_quartet_mismatch",
            "quartet": list(quad),
            "source_displayed_splits": split_set_json(source_set),
            "target_displayed_splits": split_set_json(target_set),
            "invariant_kind": kind,
            "distinguished_split": [list(split[0]), list(split[1])],
            "zero_on": zero_on,
            "strictly_positive_on": positive_on,
            "theorem": "Englander-et-al-v4-Propositions-2.9-2.10-Theorem-2.11",
        }
        return content
    source_types = dict(source_triples)
    target_types = dict(target_triples)
    for triple in sorted(source_types):
        source_type = source_types[triple]
        target_type = target_types[triple]
        if {source_type, target_type} == {"tree", "sunlet"}:
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
    prefix = "Q" if content["reason"] == "displayed_quartet_mismatch" else "T"
    return f"{prefix}:{sha_object(content)}"


def exact_isomorphism_mapping(atlas, source_graph, target_graph):
    """Return the deterministic vertex map induced by an exact isomorphism.

    Auxiliary incidence-edge nodes carry traversal-order indices, so they are
    intentionally omitted from the serialized witness.  Every candidate is
    still obtained from a full exact incidence-graph isomorphism; the induced
    map on actual mixed-graph vertices is seed-independent and determines the
    edge map uniquely in these simple graphs.
    """
    source = atlas.mixed_incidence_graph(atlas.sd0_mixed(source_graph))
    target = atlas.mixed_incidence_graph(atlas.sd0_mixed(target_graph))
    node_match = (
        lambda left, right: left.get("kind") == right.get("kind")
        and left.get("label") == right.get("label")
    )
    edge_match = lambda left, right: left.get("head") == right.get("head")
    matcher = atlas.nx.algorithms.isomorphism.GraphMatcher(
        source, target, node_match=node_match, edge_match=edge_match
    )
    candidates = []
    for mapping in matcher.isomorphisms_iter():
        vertex_mapping = tuple(
            sorted(
                (repr(left[1]), repr(right[1]))
                for left, right in mapping.items()
                if isinstance(left, tuple)
                and len(left) == 2
                and left[0] == "v"
            )
        )
        if len(vertex_mapping) != sum(
            data.get("kind") == "vertex" for _, data in source.nodes(data=True)
        ):
            fail("THETA2_ISOMORPHISM_VERTEX_MAP_INCOMPLETE")
        candidates.append(vertex_mapping)
    if not candidates:
        return None
    return [list(pair) for pair in min(set(candidates))]


def record_metadata(record) -> dict[str, Any]:
    return {
        "core_id": record.core_id,
        "incoming_selected": record.incoming_selected,
        "repair_index": record.repair_index,
        "selected_sink_mask": record.selected_sink_mask,
        "words": canonical_data(record.words),
        "selected_labels": list(record.selected_labels),
        "dummy_labels": list(record.dummy_labels),
    }
