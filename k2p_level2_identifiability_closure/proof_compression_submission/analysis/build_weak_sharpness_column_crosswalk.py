#!/usr/bin/env python3
"""Derive and seal the named weak-sharpness Jacobian column crosswalk.

This producer reconstructs the two primitive rooted graphs literally, asks the
frozen atlas for its canonical polynomial descriptors, recovers the physical
edge belonging to every descriptor class, and replays the stored exact minors.
It does not import the weak-sharpness producer.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

import networkx as nx


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
OUTPUT = HERE / "WEAK_SHARPNESS_COLUMN_CROSSWALK.json"
FROZEN = PROJECT / "work/weak_sharpness_closure/weak_sharpness_certificate.json"
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas"
sys.path.insert(0, str(ATLAS_PATH))

import k2p_atlas_core as atlas  # noqa: E402


FROZEN_SHA256 = "e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd"
ATLAS_SHA256 = "5b9e03653cc6960bf341fcbe7e63ffd10226d0f6a56441012212c6e3b2a26483"
EXPECTED_ORDERS = {
    "W": ["ZX", "SV", "rS", "SU", "UV", "VZ", "UX"],
    "W_prime": ["VX1", "VX0", "UV", "rS", "SX0", "SU", "UX1"],
}


def require(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise RuntimeError(code if detail is None else f"{code}:{detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def node_payload(graph: nx.DiGraph) -> dict[str, Any]:
    key = repr
    return {
        "nodes": [
            {"id": key(node), "role": data.get("role"), "label": data.get("label")}
            for node, data in sorted(graph.nodes(data=True), key=lambda row: key(row[0]))
        ],
        "edges": [
            [key(tail), key(head)]
            for tail, head in sorted(graph.edges(), key=lambda edge: (key(edge[0]), key(edge[1])))
        ],
    }


def descriptor_payload(descriptor: atlas.MapDescriptor) -> dict[str, Any]:
    return {
        "k": descriptor.k,
        "retic_count": descriptor.retic_count,
        "edge_class_count": descriptor.edge_class_count,
        "outputs": descriptor.outputs,
        "edge_signatures": descriptor.edge_signatures,
    }


def add_node(graph: nx.DiGraph, node: object, role: str, label: int | None = None) -> None:
    graph.add_node(node, role=role, label=label, dummy=False)


def primitive_graphs() -> dict[str, tuple[nx.DiGraph, dict[tuple[object, object], str]]]:
    """Literal encodings equivalent to, but independent of, the frozen builder."""
    core = lambda name: ("core", name)

    first = nx.DiGraph(core_id="theta0_segment3")
    for name, role in (("S", "tree"), ("U", "tree"), ("V", "retic"), ("X", "retic")):
        add_node(first, core(name), role)
    root, z = ("root",), ("sub", 3, 0)
    l0, l1, l2 = ("leaf", "INCOMING"), ("leaf", "seg", 3, 0), ("leaf", "sink", 0)
    add_node(first, root, "root")
    add_node(first, z, "tree")
    add_node(first, l0, "leaf", 0)
    add_node(first, l1, "leaf", 1)
    add_node(first, l2, "leaf", 2)
    first_edges = (
        (root, core("S")), (root, l0), (core("S"), core("U")),
        (core("S"), core("V")), (core("U"), core("X")),
        (core("U"), core("V")), (core("V"), z), (z, core("X")),
        (z, l1), (core("X"), l2),
    )
    first.add_edges_from(first_edges)
    first_names = {
        (z, core("X")): "ZX", (core("S"), core("V")): "SV",
        (root, core("S")): "rS", (core("S"), core("U")): "SU",
        (core("U"), core("V")): "UV", (core("V"), z): "VZ",
        (core("U"), core("X")): "UX",
    }

    second = nx.DiGraph(core_id="theta3_bare")
    for name, role in (
        ("S", "tree"), ("U", "tree"), ("V", "tree"),
        ("X0", "retic"), ("X1", "retic"),
    ):
        add_node(second, core(name), role)
    r2 = ("root",)
    a0, a1, a2 = ("leaf", "INCOMING"), ("leaf", "sink", 0), ("leaf", "sink", 1)
    add_node(second, r2, "root")
    add_node(second, a0, "leaf", 0)
    add_node(second, a1, "leaf", 1)
    add_node(second, a2, "leaf", 2)
    second_edges = (
        (r2, core("S")), (r2, a0), (core("S"), core("U")),
        (core("S"), core("X0")), (core("V"), core("X0")),
        (core("U"), core("X1")), (core("V"), core("X1")),
        (core("U"), core("V")), (core("X0"), a1), (core("X1"), a2),
    )
    second.add_edges_from(second_edges)
    second_names = {
        (core("V"), core("X1")): "VX1", (core("V"), core("X0")): "VX0",
        (core("U"), core("V")): "UV", (r2, core("S")): "rS",
        (core("S"), core("X0")): "SX0", (core("S"), core("U")): "SU",
        (core("U"), core("X1")): "UX1",
    }
    return {"W": (first, first_names), "W_prime": (second, second_names)}


def signature_class_map(
    graph: nx.DiGraph,
    reticulation_order: tuple[object, ...],
    parent_orders: tuple[tuple[object, object], ...],
) -> dict[tuple[object, object], int]:
    coordinates = atlas.orbit_assignments(3)
    edges = tuple(graph.edges())
    arms = atlas.selected_arm_edges(graph)
    switches: list[tuple[tuple[object, object], ...]] = []
    masks: list[dict[tuple[object, object], int]] = []
    for bits in itertools.product((0, 1), repeat=len(reticulation_order)):
        removed: set[tuple[object, object]] = set()
        for index, reticulation in enumerate(reticulation_order):
            kept_parent = parent_orders[index][bits[index]]
            removed.update(
                (parent, reticulation)
                for parent in graph.predecessors(reticulation)
                if parent != kept_parent
            )
        kept = tuple(edge for edge in edges if edge not in removed)
        switches.append(kept)
        masks.append(atlas.descendant_masks_for_switch(graph, kept))

    by_edge: dict[tuple[object, object], tuple[int, ...]] = {}
    for edge in edges:
        if edge in arms:
            continue
        signature: list[int] = []
        for kept, descendant in zip(switches, masks):
            if edge not in kept:
                signature.extend((0,) * len(coordinates))
            else:
                signature.extend(atlas.sector_for_mask(descendant[edge], chars) for chars in coordinates)
        if any(signature):
            by_edge[edge] = tuple(signature)
    active = tuple(sorted(set(by_edge.values())))
    return {edge: active.index(signature) for edge, signature in by_edge.items()}


def canonical_edge_classes(
    graph: nx.DiGraph, descriptor: atlas.MapDescriptor
) -> tuple[dict[tuple[object, object], int], tuple[object, ...], tuple[tuple[object, object], ...]]:
    matches = []
    for order, parents in atlas.retic_variants(graph):
        if atlas.descriptor_variant(graph, order, parents) == descriptor:
            matches.append((signature_class_map(graph, order, parents), order, parents))
    require(len(matches) == 1, "CANONICAL_DESCRIPTOR_ACTION_NOT_UNIQUE", len(matches))
    return matches[0]


def column_record(index: int, plain: str, tex: str, kind: str, **extra: Any) -> dict[str, Any]:
    return {"index": index, "plain": plain, "tex": tex, "kind": kind, **extra}


def display_node(node: object) -> str:
    if node == ("root",):
        return "r"
    if isinstance(node, tuple) and node[:1] == ("core",):
        return str(node[1])
    if node == ("sub", 3, 0):
        return "Z"
    return repr(node)


def build_case(
    key: str,
    graph: nx.DiGraph,
    edge_names: dict[tuple[object, object], str],
    frozen_case: dict[str, Any],
    coordinate_order: list[list[int]],
) -> dict[str, Any]:
    descriptor = atlas.model_descriptor(graph)
    require(descriptor == atlas.model_descriptor_fast2(graph), "ATLAS_CANONICALIZERS_DISAGREE", key)
    graph_sha = object_sha(node_payload(graph))
    descriptor_sha = object_sha(descriptor_payload(descriptor))
    require(graph_sha == frozen_case["graph_sha256"], "GRAPH_HASH_MISMATCH", key)
    require(descriptor_sha == frozen_case["descriptor_sha256"], "DESCRIPTOR_HASH_MISMATCH", key)

    edge_classes, reticulation_order, parent_orders = canonical_edge_classes(graph, descriptor)
    require(set(edge_classes) == set(edge_names), "VISIBLE_EDGE_NAME_DOMAIN", key)
    by_index = {class_index: edge_names[edge] for edge, class_index in edge_classes.items()}
    require(set(by_index) == set(range(7)), "EDGE_CLASS_INDEX_DOMAIN", key)
    order = [by_index[index] for index in range(7)]
    require(order == EXPECTED_ORDERS[key], "EDGE_CLASS_ORDER", (key, order))

    columns: list[dict[str, Any]] = []
    for class_index, edge_name in enumerate(order):
        columns.append(column_record(2 * class_index, f"s_{edge_name}", f"s_{{{edge_name}}}", "edge_s", edge_class=class_index, edge=edge_name))
        columns.append(column_record(2 * class_index + 1, f"g_{edge_name}", f"g_{{{edge_name}}}", "edge_g", edge_class=class_index, edge=edge_name))
    for lambda_index, reticulation in enumerate(reticulation_order):
        label = display_node(reticulation)
        columns.append(column_record(14 + lambda_index, f"lambda_{label}", f"\\lambda_{{{label}}}", "inheritance", reticulation_index=lambda_index, reticulation=label))
    require([column["index"] for column in columns] == list(range(16)), "COLUMN_INDEX_DOMAIN", key)

    rows = frozen_case["minor_rows"]
    minor_columns = frozen_case["minor_columns"]
    require(minor_columns == list(range(9)), "FROZEN_MINOR_COLUMNS", key)
    edge_value = F(frozen_case["internal_edge_pair"][0])
    require(frozen_case["internal_edge_pair"] == [str(edge_value), str(edge_value)], "INTERNAL_PAIR", key)
    pairs = tuple((edge_value, edge_value) for _ in range(7))
    lambdas = tuple(F(value) for value in frozen_case["lambdas"])
    jacobian = atlas.descriptor_jacobian(descriptor, pairs, lambdas)
    determinant = atlas.determinant_square(
        [[jacobian[row][column] for column in minor_columns] for row in rows]
    )
    determinant_text = str(determinant.numerator) if determinant.denominator == 1 else f"{determinant.numerator}/{determinant.denominator}"
    require(determinant_text == frozen_case["minor_determinant"], "MINOR_DETERMINANT", key)
    named_rows = [f"q_{''.join(map(str, coordinate_order[row]))}" for row in rows]
    named_minor_columns = [columns[index] for index in minor_columns]

    return {
        "graph_sha256": graph_sha,
        "descriptor_sha256": descriptor_sha,
        "canonical_reticulation_order": [display_node(node) for node in reticulation_order],
        "canonical_parent_orders": [
            [display_node(parent) for parent in pair]
            for pair in parent_orders
        ],
        "edge_class_order": order,
        "full_parameter_columns": columns,
        "frozen_minor": {
            "row_indices": rows,
            "row_coordinates": named_rows,
            "column_indices": minor_columns,
            "named_columns": named_minor_columns,
            "determinant": determinant_text,
        },
    }


def main() -> None:
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_COLUMN_BUILDER_OPTIMIZED_MODE_FORBIDDEN")
    require(file_sha(FROZEN) == FROZEN_SHA256, "FROZEN_CERTIFICATE_FILE_HASH")
    atlas_file = ATLAS_PATH / "k2p_atlas_core.py"
    require(file_sha(atlas_file) == ATLAS_SHA256, "FROZEN_ATLAS_FILE_HASH")
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    payload = dict(frozen)
    stated_payload_sha = payload.pop("payload_sha256")
    require(object_sha(payload) == stated_payload_sha, "FROZEN_CERTIFICATE_SEAL")
    require(stated_payload_sha == "dfecd30ea217810a902add48350025e5f00dfa1255718783df790a9c7e1a5182", "FROZEN_PAYLOAD_HASH")

    graphs = primitive_graphs()
    cases = {
        "W": build_case("W", *graphs["W"], frozen["first"]["parameter_certificate"], frozen["coordinate_order"]),
        "W_prime": build_case("W_prime", *graphs["W_prime"], frozen["second"]["parameter_certificate"], frozen["coordinate_order"]),
    }
    result: dict[str, Any] = {
        "schema": "k2p-weak-sharpness-column-crosswalk-v1",
        "producer_command": ".venv/bin/python -B proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py",
        "replay_command": ".venv/bin/python -B proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py",
        "mutation_command": ".venv/bin/python -B proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py",
        "bindings": {
            "frozen_certificate": "work/weak_sharpness_closure/weak_sharpness_certificate.json",
            "frozen_certificate_sha256": FROZEN_SHA256,
            "frozen_certificate_payload_sha256": stated_payload_sha,
            "atlas": "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py",
            "atlas_sha256": ATLAS_SHA256,
        },
        "coordinate_order": frozen["coordinate_order"],
        "parameter_convention": "columns 2i and 2i+1 are s and g for canonical edge class i; columns 14 and 15 are inheritance variables in the canonical reticulation order",
        "networks": cases,
        "conclusion": "The anonymous frozen columns 0,...,8 have the exact graph-derived names recorded for W and W_prime.",
    }
    result["payload_sha256"] = object_sha(result)
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("K2P_WEAK_SHARPNESS_COLUMN_CROSSWALK_BUILT")
    print(json.dumps({"output": str(OUTPUT.relative_to(PROJECT)), "sha256": file_sha(OUTPUT), "payload_sha256": result["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
