#!/usr/bin/env python3
"""Radius-one complement-edge additions around all one-vertex extensions.

We keep every complement edge of the separated-port lollipop core and add
one formerly absent H-edge among the nine old vertices.  Edges incident with
the new vertex are already exhausted by ``explore.py``.  Thus this is the
27 * 2^9 local search that can strengthen G by deleting one G-edge without
destroying any literal edge of the original lollipop core.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict

import explore as core


OLD_PAIRS = tuple(
    (u, v)
    for u in range(core.BASE_N)
    for v in range(u + 1, core.BASE_N)
)
ADDED_H_EDGES = tuple(
    edge for edge in OLD_PAIRS if edge not in core.BASE_H_EDGES
)


def main() -> None:
    assert len(ADDED_H_EDGES) == 27
    rows = []
    raw_records = []
    for added_h_edge in ADDED_H_EDGES:
        for extension_mask in range(1 << core.BASE_N):
            h_edges = core.make_h_edges(extension_mask) | {added_h_edge}
            h_adj = core.adjacency_masks(core.N, h_edges)
            g_adj = core.complement_masks(core.N, h_adj)
            g_edges = core.graph_edges_from_adj(core.N, g_adj)
            raw_g6 = core.graph6(core.N, g_edges)
            raw_records.append(raw_g6)

            gamma = core.gamma_exact(core.N, g_adj)
            alpha = core.alpha_exact(core.N, g_adj)
            gamma_inf, kernel_states = core.gamma_infinity_exact(
                core.N, g_adj, gamma
            )
            theta = core.theta_exact(core.N, h_adj, alpha)
            witnesses = core.exact_family_predicate(
                core.N, g_adj, h_adj
            )
            rows.append(
                {
                    "added_h_edge": list(added_h_edge),
                    "extension_h_mask": extension_mask,
                    "extension_h_neighbors": [
                        vertex
                        for vertex in range(core.BASE_N)
                        if extension_mask & (1 << vertex)
                    ],
                    "labeled_graph6": raw_g6,
                    "gamma": gamma,
                    "alpha": alpha,
                    "gamma_infinity": gamma_inf,
                    "theta": theta,
                    "unrestricted_optimal_kernel_states": kernel_states,
                    "family_witness_count": len(witnesses),
                    "augmentation_sensitive_witness_count": sum(
                        witness["augmentation_sensitive"]
                        for witness in witnesses
                    ),
                    "family_witnesses": witnesses,
                }
            )

    canonical_records = core.canonicalize(raw_records)
    for row, canonical in zip(rows, canonical_records):
        row["canonical_graph6"] = canonical

    csv_path = core.HERE / "edge_additions.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        fieldnames = [
            "added_h_edge",
            "extension_h_mask",
            "extension_h_neighbors",
            "labeled_graph6",
            "canonical_graph6",
            "gamma",
            "alpha",
            "gamma_infinity",
            "theta",
            "unrestricted_optimal_kernel_states",
            "family_witness_count",
            "augmentation_sensitive_witness_count",
            "family_witnesses",
        ]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            encoded = dict(row)
            for key in (
                "added_h_edge",
                "extension_h_neighbors",
                "family_witnesses",
            ):
                encoded[key] = json.dumps(
                    encoded[key], separators=(",", ":")
                )
            writer.writerow(encoded)

    canonical_to_rows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        canonical_to_rows[row["canonical_graph6"]].append(row)
    assert all(
        len(
            {
                (
                    member["gamma"],
                    member["alpha"],
                    member["gamma_infinity"],
                    member["theta"],
                )
                for member in members
            }
        )
        == 1
        for members in canonical_to_rows.values()
    )
    property_rows = [
        row for row in rows if row["augmentation_sensitive_witness_count"]
    ]
    equality_rows = [
        row
        for row in property_rows
        if row["gamma"]
        == row["alpha"]
        == row["gamma_infinity"]
        == 3
    ]
    summary = {
        "status": "PASS",
        "scope": {
            "operation": (
                "add one non-core H-edge among old vertices, after arbitrary "
                "one-vertex H-neighborhood extension"
            ),
            "old_edge_choices": len(ADDED_H_EDGES),
            "extension_choices_per_edge": 1 << core.BASE_N,
            "labeled_cases": len(rows),
            "canonical_unlabeled_graphs": len(canonical_to_rows),
        },
        "labeled_parameter_counts": {
            ",".join(map(str, key)): value
            for key, value in sorted(
                Counter(
                    (
                        row["gamma"],
                        row["alpha"],
                        row["gamma_infinity"],
                        row["theta"],
                    )
                    for row in rows
                ).items()
            )
        },
        "property_labeled_cases": len(property_rows),
        "property_canonical_graphs": len(
            {row["canonical_graph6"] for row in property_rows}
        ),
        "gamma3_equality_property_labeled_cases": len(equality_rows),
        "gamma3_equality_property_canonical_graphs": len(
            {row["canonical_graph6"] for row in equality_rows}
        ),
        "gamma3_equality_property_canonical_graph6": sorted(
            {row["canonical_graph6"] for row in equality_rows}
        ),
        "gamma3_equality_witness_rows": equality_rows,
        "edge_additions_csv_sha256": hashlib.sha256(
            csv_path.read_bytes()
        ).hexdigest(),
    }
    (core.HERE / "edge_additions_summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
