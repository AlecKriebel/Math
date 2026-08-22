#!/usr/bin/env python3
"""Independent replay of the named weak-sharpness column crosswalk.

The checker does not import the crosswalk producer or the primary atlas.  It
uses the independently written weak-sharpness formal-map expansion, derives
edge switching signatures from literal graph encodings, replays both exact
minors, and checks the graph, descriptor, certificate, and payload hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_INPUT = HERE / "WEAK_SHARPNESS_COLUMN_CROSSWALK.json"
FROZEN = PROJECT / "work/weak_sharpness_closure/weak_sharpness_certificate.json"
AUDIT_DIR = PROJECT / "work/weak_sharpness_audit"
sys.path.insert(0, str(AUDIT_DIR))

import audit_weak_sharpness as independent  # noqa: E402


FROZEN_SHA256 = "e66c78a0aeab990b4dc448f4f064b37e1e15ecbff75a5f472bf116d4464378bd"
FROZEN_PAYLOAD_SHA256 = "dfecd30ea217810a902add48350025e5f00dfa1255718783df790a9c7e1a5182"
ATLAS_SHA256 = "5b9e03653cc6960bf341fcbe7e63ffd10226d0f6a56441012212c6e3b2a26483"
EXPECTED = {
    "W": {
        "order": ["ZX", "SV", "rS", "SU", "UV", "VZ", "UX"],
        "reticulations": ["X", "V"],
        "parents": [["U", "Z"], ["U", "S"]],
        "graph_sha256": "5b11a276dad1f6ddd671e2706c31e73ca525e7f6d89aed77bf83151a3ceba374",
        "descriptor_sha256": "a9a046ac8bee060c6548c931b5ae1fb8c7bc60ec36e467bbd6dd884d31630a14",
        "rows": [1, 2, 3, 5, 4, 7, 6, 8, 9],
        "determinant": "10368019213741323/563981315074464023964442388464888915634290688",
        "edge_value": "1/7",
        "lambdas": ["15996/16339", "1/8"],
    },
    "W_prime": {
        "order": ["VX1", "VX0", "UV", "rS", "SX0", "SU", "UX1"],
        "reticulations": ["X1", "X0"],
        "parents": [["U", "V"], ["S", "V"]],
        "graph_sha256": "c0f954ce00e0d09138eb82bdbdbdda68e3ed5e7b156482c1775a3f3795524fb1",
        "descriptor_sha256": "2df6cfa6592d706f243377039778744e0ad80901bd22046cf15181c48a418e48",
        "rows": [1, 2, 3, 5, 4, 6, 7, 8, 9],
        "determinant": "1435825/85002596691653613846528",
        "edge_value": "1/4",
        "lambdas": ["1/2", "1/6"],
    },
}
EDGE_NAMES = {
    "W": {("Z", "X"): "ZX", ("S", "V"): "SV", ("r", "S"): "rS", ("S", "U"): "SU", ("U", "V"): "UV", ("V", "Z"): "VZ", ("U", "X"): "UX"},
    "W_prime": {("V", "X1"): "VX1", ("V", "X0"): "VX0", ("U", "V"): "UV", ("r", "S"): "rS", ("S", "X0"): "SX0", ("S", "U"): "SU", ("U", "X1"): "UX1"},
}


class CrosswalkFailure(RuntimeError):
    pass


def need(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise CrosswalkFailure(code if detail is None else f"{code}:{detail}")


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


def fraction_text(value: F) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def verify_seal(value: dict[str, Any], code: str) -> None:
    stated = value.get("payload_sha256")
    need(isinstance(stated, str), f"{code}_SEAL_MISSING")
    payload = dict(value)
    del payload["payload_sha256"]
    need(object_sha(payload) == stated, f"{code}_SEAL_MISMATCH")


def switching_edge_order(graph, model, names: dict[tuple[str, str], str]) -> list[str]:
    """Derive class order directly from complete visible switching signatures."""
    coordinates = independent.orbit_coordinates()
    all_edges = tuple(sorted(graph.edges()))
    arms = frozenset(
        edge for edge in all_edges
        if graph.nodes[edge[1]]["role"] == "leaf" and isinstance(graph.nodes[edge[1]]["label"], int)
    )
    switches = []
    for bits in itertools.product((0, 1), repeat=len(model.retic_order)):
        removed = set()
        for index, reticulation in enumerate(model.retic_order):
            kept_parent = model.parent_orders[index][bits[index]]
            removed.update(
                (parent, reticulation)
                for parent in graph.predecessors(reticulation)
                if parent != kept_parent
            )
        kept = tuple(edge for edge in all_edges if edge not in removed)
        switches.append((kept, independent.descendant_masks(graph, kept)))

    signatures: dict[tuple[str, str], tuple[int, ...]] = {}
    for edge in all_edges:
        if edge in arms:
            continue
        signature: list[int] = []
        for kept, masks in switches:
            if edge not in kept:
                signature.extend((0,) * len(coordinates))
            else:
                signature.extend(independent.sector(masks[edge], chars) for chars in coordinates)
        if any(signature):
            signatures[edge] = tuple(signature)
    active = tuple(sorted(set(signatures.values())))
    need(active == model.edge_signatures, "INDEPENDENT_SIGNATURE_DESCRIPTOR_MISMATCH")
    classes = {edge: active.index(signature) for edge, signature in signatures.items()}
    need(set(classes) == set(names), "INDEPENDENT_VISIBLE_EDGE_DOMAIN")
    inverse = {index: names[edge] for edge, index in classes.items()}
    need(set(inverse) == set(range(7)), "INDEPENDENT_CLASS_INDEX_DOMAIN")
    return [inverse[index] for index in range(7)]


def graph_payload_from_independent_spec(key: str, spec) -> dict[str, Any]:
    if key == "W":
        ids = {
            "r": ("root",), "S": ("core", "S"), "U": ("core", "U"),
            "V": ("core", "V"), "X": ("core", "X"), "Z": ("sub", 3, 0),
            "L0": ("leaf", "INCOMING"), "L1": ("leaf", "seg", 3, 0),
            "L2": ("leaf", "sink", 0),
        }
    else:
        ids = {
            "r": ("root",), "S": ("core", "S"), "U": ("core", "U"),
            "V": ("core", "V"), "X0": ("core", "X0"), "X1": ("core", "X1"),
            "L0": ("leaf", "INCOMING"), "L1": ("leaf", "sink", 0),
            "L2": ("leaf", "sink", 1),
        }
    nodes = [
        {"id": repr(ids[node]), "role": role, "label": label}
        for node, role, label in spec.nodes
    ]
    edges = [[repr(ids[tail]), repr(ids[head])] for tail, head in spec.arcs]
    return {
        "nodes": sorted(nodes, key=lambda row: row["id"]),
        "edges": sorted(edges, key=lambda edge: (edge[0], edge[1])),
    }


def expected_columns(order: list[str], reticulations: list[str]) -> list[dict[str, Any]]:
    columns: list[dict[str, Any]] = []
    for class_index, edge in enumerate(order):
        columns.extend((
            {"index": 2 * class_index, "plain": f"s_{edge}", "tex": f"s_{{{edge}}}", "kind": "edge_s", "edge_class": class_index, "edge": edge},
            {"index": 2 * class_index + 1, "plain": f"g_{edge}", "tex": f"g_{{{edge}}}", "kind": "edge_g", "edge_class": class_index, "edge": edge},
        ))
    for index, reticulation in enumerate(reticulations):
        columns.append({
            "index": 14 + index, "plain": f"lambda_{reticulation}",
            "tex": f"\\lambda_{{{reticulation}}}", "kind": "inheritance",
            "reticulation_index": index, "reticulation": reticulation,
        })
    return columns


def frozen_binding() -> dict[str, Any]:
    need(file_sha(FROZEN) == FROZEN_SHA256, "FROZEN_CERTIFICATE_FILE_HASH")
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    verify_seal(frozen, "FROZEN_CERTIFICATE")
    need(frozen["payload_sha256"] == FROZEN_PAYLOAD_SHA256, "FROZEN_CERTIFICATE_PAYLOAD_HASH")
    return frozen


def verify_case(
    key: str,
    record: dict[str, Any],
    spec,
    frozen_case: dict[str, Any],
    coordinates: list[list[int]],
) -> None:
    expected = EXPECTED[key]
    graph = independent.rooted_graph(spec)
    model = independent.canonical_formal_map(graph)
    derived_order = switching_edge_order(graph, model, EDGE_NAMES[key])
    need(derived_order == expected["order"], "DERIVED_EDGE_CLASS_ORDER", key)
    need(record["edge_class_order"] == expected["order"], "STORED_EDGE_CLASS_ORDER", key)
    reticulations = list(model.retic_order)
    parents = [list(pair) for pair in model.parent_orders]
    need(reticulations == expected["reticulations"], "DERIVED_RETICULATION_ORDER", key)
    need(parents == expected["parents"], "DERIVED_PARENT_ORDER", key)
    need(record["canonical_reticulation_order"] == reticulations, "STORED_RETICULATION_ORDER", key)
    need(record["canonical_parent_orders"] == parents, "STORED_PARENT_ORDER", key)

    graph_hash = object_sha(graph_payload_from_independent_spec(key, spec))
    descriptor_hash = object_sha({
        "k": 3, "retic_count": 2, "edge_class_count": model.edge_class_count,
        "outputs": model.outputs, "edge_signatures": model.edge_signatures,
    })
    need(graph_hash == expected["graph_sha256"], "DERIVED_GRAPH_HASH", key)
    need(descriptor_hash == expected["descriptor_sha256"], "DERIVED_DESCRIPTOR_HASH", key)
    need(record["graph_sha256"] == graph_hash == frozen_case["graph_sha256"], "STORED_GRAPH_HASH", key)
    need(record["descriptor_sha256"] == descriptor_hash == frozen_case["descriptor_sha256"], "STORED_DESCRIPTOR_HASH", key)

    columns = expected_columns(expected["order"], expected["reticulations"])
    need(record["full_parameter_columns"] == columns, "NAMED_FULL_COLUMN_ORDER", key)
    minor = record["frozen_minor"]
    need(minor["row_indices"] == expected["rows"] == frozen_case["minor_rows"], "MINOR_ROWS", key)
    need(minor["column_indices"] == list(range(9)) == frozen_case["minor_columns"], "MINOR_COLUMNS", key)
    named_rows = [f"q_{''.join(map(str, coordinates[row]))}" for row in expected["rows"]]
    need(minor["row_coordinates"] == named_rows, "NAMED_MINOR_ROWS", key)
    need(minor["named_columns"] == columns[:9], "NAMED_MINOR_COLUMNS", key)

    edge_value = F(expected["edge_value"])
    pairs = tuple((edge_value, edge_value) for _ in range(7))
    lambdas = tuple(F(value) for value in expected["lambdas"])
    derivative = independent.jacobian(model, pairs, lambdas)
    determinant = independent.determinant(
        [[derivative[row][column] for column in range(9)] for row in expected["rows"]]
    )
    determinant_text = fraction_text(determinant)
    need(determinant_text == expected["determinant"], "INDEPENDENT_MINOR_DETERMINANT", key)
    need(minor["determinant"] == determinant_text == frozen_case["minor_determinant"], "STORED_MINOR_DETERMINANT", key)


def verify_artifact(value: dict[str, Any]) -> None:
    verify_seal(value, "CROSSWALK")
    need(value.get("schema") == "k2p-weak-sharpness-column-crosswalk-v1", "SCHEMA")
    need(value.get("producer_command") == ".venv/bin/python -B proof_compression_submission/analysis/build_weak_sharpness_column_crosswalk.py", "PRODUCER_COMMAND")
    need(value.get("replay_command") == ".venv/bin/python -B proof_compression_submission/analysis/verify_weak_sharpness_column_crosswalk.py", "REPLAY_COMMAND")
    need(value.get("mutation_command") == ".venv/bin/python -B proof_compression_submission/analysis/test_weak_sharpness_column_crosswalk_mutations.py", "MUTATION_COMMAND")
    bindings = value.get("bindings")
    need(isinstance(bindings, dict), "BINDINGS")
    need(bindings.get("frozen_certificate_sha256") == FROZEN_SHA256, "BOUND_FROZEN_FILE_HASH")
    need(bindings.get("frozen_certificate_payload_sha256") == FROZEN_PAYLOAD_SHA256, "BOUND_FROZEN_PAYLOAD_HASH")
    need(bindings.get("atlas_sha256") == ATLAS_SHA256, "BOUND_ATLAS_HASH")
    frozen = frozen_binding()
    need(value.get("coordinate_order") == frozen["coordinate_order"] == [list(row) for row in independent.orbit_coordinates()], "COORDINATE_ORDER")
    need(set(value.get("networks", {})) == {"W", "W_prime"}, "NETWORK_KEY_SET")
    first_spec, second_spec = independent.independent_specs()
    verify_case("W", value["networks"]["W"], first_spec, frozen["first"]["parameter_certificate"], value["coordinate_order"])
    verify_case("W_prime", value["networks"]["W_prime"], second_spec, frozen["second"]["parameter_certificate"], value["coordinate_order"])
    need(value.get("conclusion") == "The anonymous frozen columns 0,...,8 have the exact graph-derived names recorded for W and W_prime.", "CONCLUSION")


def main() -> None:
    if not __debug__:
        raise SystemExit("WEAK_SHARPNESS_COLUMN_REPLAY_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    args = parser.parse_args()
    value = json.loads(args.input.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "ARTIFACT_NOT_OBJECT")
    verify_artifact(value)
    print("K2P_WEAK_SHARPNESS_COLUMN_CROSSWALK_PASS")
    print(json.dumps({
        "artifact_sha256": file_sha(args.input),
        "W_columns_0_8": [column["plain"] for column in value["networks"]["W"]["frozen_minor"]["named_columns"]],
        "W_prime_columns_0_8": [column["plain"] for column in value["networks"]["W_prime"]["frozen_minor"]["named_columns"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
