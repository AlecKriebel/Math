#!/usr/bin/env python3
"""Tests and tamper checks for the block-reinsertion artifacts."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import random
import tempfile


HERE = Path(__file__).resolve().parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


verifier = load_module(
    "block_reinsertion_verifier_tests",
    HERE / "verify_block_reinsertion.py",
)
topology_tool = load_module(
    "block_topology_tests", HERE / "block_topology.py"
)


def adjacency(cardinality: int, edges: list[tuple[int, int]]) -> list[int]:
    answer = [0] * cardinality
    for first, second in edges:
        answer[first] |= 1 << second
        answer[second] |= 1 << first
    return answer


def brute_independent_size(graph: list[int]) -> int:
    best = 0
    for mask in range(1 << len(graph)):
        if mask.bit_count() <= best:
            continue
        valid = True
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            vertex = bit.bit_length() - 1
            if graph[vertex] & mask:
                valid = False
                break
            remaining ^= bit
        if valid:
            best = mask.bit_count()
    return best


def test_independent_set_search() -> None:
    rng = random.Random(2026072800)
    for cardinality in range(1, 10):
        for _ in range(30):
            probability = rng.uniform(0.05, 0.95)
            edges = [
                (first, second)
                for first in range(cardinality)
                for second in range(first + 1, cardinality)
                if rng.random() < probability
            ]
            graph = adjacency(cardinality, edges)
            computed, visited = verifier.maximum_independent_size(
                graph
            )
            assert visited > 0
            assert computed == brute_independent_size(graph)


def test_graph_isomorphism() -> None:
    first = adjacency(
        8,
        [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
        ],
    )
    permutation = [4, 1, 7, 0, 6, 2, 5, 3]
    permuted_edges = []
    for left in range(8):
        for right in range(left + 1, 8):
            if (first[left] >> right) & 1:
                permuted_edges.append(
                    (permutation[left], permutation[right])
                )
    second = adjacency(8, permuted_edges)
    mapping, visited = topology_tool.isomorphism(first, second)
    assert mapping is not None and visited > 0
    verifier.verify_mapping(first, second, mapping)

    cycle_six = adjacency(
        6,
        [(index, (index + 1) % 6) for index in range(6)],
    )
    two_triangles = adjacency(
        6,
        [
            (0, 1),
            (1, 2),
            (2, 0),
            (3, 4),
            (4, 5),
            (5, 3),
        ],
    )
    mapping, _visited = topology_tool.isomorphism(
        cycle_six, two_triangles
    )
    assert mapping is None


def mutated_verification(
    source_mutation=None,
    topology_mutation=None,
):
    source = json.loads(verifier.SOURCE.read_bytes())
    topology = json.loads(verifier.TOPOLOGY.read_bytes())
    if source_mutation is not None:
        source_mutation(source)
    source_bytes = (json.dumps(source, indent=2) + "\n").encode()
    topology["source_sha256"] = hashlib.sha256(
        source_bytes
    ).hexdigest()
    if topology_mutation is not None:
        topology_mutation(topology)
    with tempfile.TemporaryDirectory() as directory:
        source_path = Path(directory) / "source.json"
        topology_path = Path(directory) / "topology.json"
        source_path.write_bytes(source_bytes)
        topology_path.write_text(
            json.dumps(topology, indent=2) + "\n"
        )
        return verifier.verify(
            source_path,
            topology_path,
            enforce_pinned_hashes=False,
        )


def must_reject(source_mutation=None, topology_mutation=None) -> None:
    try:
        mutated_verification(source_mutation, topology_mutation)
    except (
        AssertionError,
        KeyError,
        TypeError,
        ValueError,
        verifier.VerificationError,
    ):
        return
    raise AssertionError("tampered artifact was accepted")


def test_tamper_detection() -> None:
    must_reject(
        source_mutation=lambda source: source.update(
            {"evidence_status": "EXACT"}
        )
    )

    def damage_cover(source):
        analysis = source["analyses"][0]
        analysis["minimum_vertex_cover"][0] = analysis[
            "maximum_independent_set"
        ][0]

    must_reject(source_mutation=damage_cover)

    def damage_stress(source):
        source["analyses"][2]["stress"]["weights"][0] += 0.01

    must_reject(source_mutation=damage_stress)

    def damage_coordinate(source):
        source["analyses"][1]["source"][
            "coordinates_float64"
        ][0][0] += 0.001

    must_reject(source_mutation=damage_coordinate)

    def damage_mapping(topology):
        report = next(
            item
            for item in topology["reports"]
            if item["cardinality"] == 44
            and item["restart"] == 0
        )
        mapping = report["source_to_retained_isomorphism"]
        mapping[0], mapping[1] = mapping[1], mapping[0]

    must_reject(topology_mutation=damage_mapping)

    # Solver status is deliberately not a premise of verification.
    def damage_solver_status(source):
        source["runs"][0]["epigraph_solver"]["success"] = False
        source["runs"][0]["epigraph_solver"]["message"] = (
            "ignored by independent checker"
        )

    report = mutated_verification(
        source_mutation=damage_solver_status
    )
    assert report["status"].endswith("independently verified")


def main() -> None:
    report = verifier.verify()
    assert report["strict_improvement_count"] == 0
    assert report["nonisomorphic_restart_count"] == 14
    test_independent_set_search()
    test_graph_isomorphism()
    test_tamper_detection()
    print("block-reinsertion verifier tests passed")


if __name__ == "__main__":
    main()
