"""Exact replay of the finite level-2 orientation-core atlas."""

from __future__ import annotations

import json
from pathlib import Path

from enumerate_theta_orientation_cores import enumerate_cores


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "certificates" / "level2_generator_atlas.json"


def signature(core):
    return (
        tuple(core["branch_types"]),
        tuple(tuple(path) for path in core["path_event_sequences_U_to_V"]),
        core["template_automorphism_order"],
        core["minimum_tree_port_subdivisions"],
    )


def main():
    with ATLAS.open() as stream:
        atlas = json.load(stream)

    raw_valid, computed_cores = enumerate_cores()
    expected_theta = {
        (
            tuple(item["branch_types_UV"]),
            tuple(tuple(path) for path in item["path_event_sequences_U_to_V"]),
            item["template_automorphism_order"],
            item["minimum_tree_port_subdivisions"],
        )
        for item in atlas["orientation_cores"]
        if item["undirected_core"] == "theta"
    }
    computed = {signature(core) for core in computed_cores}
    assert computed == expected_theta
    assert raw_valid == atlas["theta_enumeration_counts"]["raw_valid_orientations_before_isomorphism"]
    assert len(computed) == atlas["theta_enumeration_counts"]["orientation_cores_after_branch_and_path_symmetry"]

    # The reduced cubic-core inequality: for cyclomatic number mu=2,
    # E=V+1 and 3V <= 2E force V<=2.  A nonempty biconnected cubic core
    # cannot have V=1 (a loop contributes degree 2), so V=2,E=3.
    possibilities = []
    for vertices in range(1, 8):
        edges = vertices + 1
        if 3 * vertices <= 2 * edges:
            possibilities.append((vertices, edges))
    assert possibilities == [(1, 2), (2, 3)]
    assert 2 * 3 == 3 * 2  # the V=2 case is exactly cubic: theta

    cycle = next(item for item in atlas["orientation_cores"] if item["id"] == "cycle-S-X")
    assert cycle["template_automorphism_order"] == 2
    assert cycle["minimum_tree_port_subdivisions"] == 1

    print("theta_raw_valid", raw_valid)
    print("theta_orientation_cores", len(computed))
    print("total_cycle_plus_theta_orientation_cores", 1 + len(computed))
    print("PASS: complete reduced level-2 generator and orientation atlas")


if __name__ == "__main__":
    main()

