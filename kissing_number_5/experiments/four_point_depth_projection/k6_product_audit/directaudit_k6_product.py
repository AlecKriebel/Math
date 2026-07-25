#!/usr/bin/env python3
"""Exact product-row audit of the stored 51-atom direct K6 extension."""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from experiments.four_point_depth_projection.k5_product_audit import (
    verify_product_extension_independent as direction_source,
)
from experiments.four_point_depth_projection.k6_product_audit.productpool_verify import (
    PAIRS,
    assert_rank_five_psd,
    edge_color,
    k6_state_slack_twice,
    triangle_indices,
)


ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "certificates" / "centered_quarter_bv_pseudodistribution.json"
DIRECT = (
    ROOT
    / "experiments"
    / "centered_quarter_k6_rank"
    / "direct_k6_triangle_extension.json"
)
SOURCE_SHA256 = (
    "112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550"
)
DIRECT_SHA256 = (
    "32e629ab5df91cf6e616aa1f7a61af22f853b78ccff50947738b5cab1394d0ba"
)
EXPECTED_WORST = Q(
    -34774569534004858111024638332474125643044200329,
    356018544845649389857262695513200000000000000,
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(
    source_path: Path = SOURCE,
    direct_path: Path = DIRECT,
) -> dict[str, object]:
    assert digest(source_path) == SOURCE_SHA256
    assert digest(direct_path) == DIRECT_SHA256
    source = json.loads(source_path.read_text())
    direct = json.loads(direct_path.read_text())
    assert direct["schema"] == (
        "kissing5.centered_quarter_direct_k6_triangle_extension.v1"
    )
    assert direct["source_sha256"] == SOURCE_SHA256

    grid = tuple(Q(value) for value in source["grid"])
    scaled_values = tuple(int(4 * value) for value in grid)
    alpha = tuple(Q(value) for value in source["alpha"])
    nu = tuple(Q(value) for value in source["nu"])
    triples = tuple(tuple(item) for item in source["triple_orbits"])
    triple_index = {triple: index for index, triple in enumerate(triples)}

    atoms = direct["atoms"]
    weights = tuple(Q(atom["weight"]) for atom in atoms)
    assert len(atoms) == 51 and all(weight > 0 for weight in weights)
    assert sum(weights) == 1
    parsed = []
    edge_marginal = [Q(0)] * 7
    triangle_marginal = [Q(0)] * 51
    for atom, weight in zip(atoms, weights):
        edges = tuple(
            atom[
                "edge_color_indices_"
                "01_02_03_04_05_12_13_14_15_23_24_25_34_35_45"
            ]
        )
        assert_rank_five_psd(edges, scaled_values)
        faces = triangle_indices(edges, triple_index)
        assert faces == tuple(atom["triangle_orbit_indices"])
        parsed.append(edges)
        for color in edges:
            edge_marginal[color] += weight
        for face in faces:
            triangle_marginal[face] += weight
    assert edge_marginal == [3 * value / 8 for value in alpha]
    assert triangle_marginal == [value / 78 for value in nu]

    violations = []
    family_reports = []
    all_slacks = []
    for family_index, (
        base_index,
        threshold_index,
        capacity,
    ) in enumerate(direction_source.capacity_families(grid)):
        states, coverage, _feasible = direction_source.direction_states(
            base_index, grid, triples
        )
        family_violations = 0
        family_minimum = None
        for state_index, (required, table) in enumerate(states):
            slack = sum(
                weight
                * k6_state_slack_twice(
                    edges,
                    base_index,
                    threshold_index,
                    capacity,
                    required,
                    table,
                )
                for edges, weight in zip(parsed, weights)
            )
            all_slacks.append(slack)
            family_minimum = (
                slack
                if family_minimum is None or slack < family_minimum
                else family_minimum
            )
            if slack < 0:
                family_violations += 1
                violations.append(
                    {
                        "family_index": family_index,
                        "state_index": state_index,
                        "required_depth_count": required,
                        "base_inner_product": str(grid[base_index]),
                        "high_threshold": str(grid[threshold_index]),
                        "capacity": capacity,
                        "twice_symmetrized_slack": str(slack),
                    }
                )
        family_reports.append(
            {
                "base_inner_product": str(grid[base_index]),
                "high_threshold": str(grid[threshold_index]),
                "capacity": capacity,
                "direction_states": coverage["distinct_states"],
                "negative_rows": family_violations,
                "minimum_twice_symmetrized_slack": str(family_minimum),
            }
        )

    assert len(all_slacks) == 560
    assert len(violations) == 41
    assert all(
        item["base_inner_product"] == "-1/4"
        and item["high_threshold"] == "1/2"
        and item["capacity"] == 3
        for item in violations
    )
    assert min(all_slacks) == EXPECTED_WORST

    # The worst row is the original symmetric negative-sum direction.
    base_index = grid.index(Q(-1, 4))
    threshold_index = grid.index(Q(1, 2))
    table = tuple(
        int(
            direction_source.direction_audit.direction_qualifies(
                first,
                second,
                grid[base_index],
                (Q(-1), Q(-1)),
            )
        )
        for first in grid
        for second in grid
    )
    symmetric_slack = sum(
        weight
        * k6_state_slack_twice(
            edges,
            base_index,
            threshold_index,
            3,
            7,
            table,
        )
        for edges, weight in zip(parsed, weights)
    )
    assert symmetric_slack == EXPECTED_WORST

    return {
        "status": "PASS",
        "audit_conclusion": (
            "the stored 51-atom direct K6 extension violates 41 product "
            "states, all at q=-1/4, b=1/2, M=3"
        ),
        "source_sha256": SOURCE_SHA256,
        "direct_extension_sha256": DIRECT_SHA256,
        "positive_atoms": len(atoms),
        "product_rows_checked": len(all_slacks),
        "negative_product_rows": len(violations),
        "worst_twice_symmetrized_slack": EXPECTED_WORST,
        "worst_row_is_symmetric_negative_sum": True,
        "product_families": family_reports,
    }


if __name__ == "__main__":
    report = audit()
    print(
        json.dumps(
            {
                key: str(value) if isinstance(value, Q) else value
                for key, value in report.items()
            },
            indent=2,
            sort_keys=True,
        )
    )
