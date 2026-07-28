#!/usr/bin/env python3
"""Exploratory scan for exact cross-ban rank boundary controls.

This script searches the fixed MMV 2022 near-miss catalog.  It deliberately
imports only the frozen, independently reviewed bit-mask implementation used
for C-157.  Its output is discovery evidence until a selected control is
replayed by a standalone strict verifier.
"""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
CORE_PATH = (
    HERE.parent
    / "full_list_nonsingleton_terminal"
    / "verify_cyclic_corridor_control.py"
)
SPEC = importlib.util.spec_from_file_location("c157_core", CORE_PATH)
if SPEC is None or SPEC.loader is None:
    raise AssertionError("could not load frozen C-157 control core")
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


def palette(rows, greatest, root, vertex):
    return CORE.terminal_root_palette(rows, greatest, root, vertex)


def main() -> None:
    with (CAMPAIGN / "instances" / "mmv2022_table9.csv").open() as stream:
        catalog = list(csv.DictReader(stream))
    catalog.extend(
        (
            {
                "catalog_id": "EQUALITY-12",
                "graph6": "Ksv`f\\knJVis",
                "source": "accepted equality control",
            },
            {
                "catalog_id": "EQUALITY-16",
                "graph6": "OYifur}UO]}iTij]tpo]v",
                "source": "accepted equality control",
            },
        )
    )

    records = []
    totals = {
        "graphs": 0,
        "full_incidences": 0,
        "rank_zero_corridors": 0,
        "secondary_rows": 0,
        "witness_transfers": 0,
        "witness_transfers_inside_B": 0,
        "recipient_rank_zero": 0,
        "recipient_rank_positive": 0,
        "recipient_kernel": 0,
        "recipient_banned": 0,
    }

    for catalog_row in catalog:
        rows = CORE.decode_short_graph6(catalog_row["graph6"])
        if CORE.exact_alpha(rows) != 3:
            continue
        greatest, _, _ = CORE.greatest_kernel(rows, 3)
        totals["graphs"] += 1
        order = len(rows)
        for root in CORE.masks_of_size(order, 3):
            if not CORE.independent(rows, root) or root not in greatest:
                continue
            root_vertices = CORE.vertices(root)
            for target in range(order):
                if root >> target & 1:
                    continue
                if palette(rows, greatest, root, target) != root_vertices:
                    continue
                totals["full_incidences"] += 1
                B = frozenset(CORE.complement_neighbors(rows, target))
                for color in root_vertices:
                    ban = CORE.color_ban(rows, root, target, color)
                    kernel, ranks, _ = CORE.greatest_kernel(rows, 3, ban)
                    if kernel:
                        continue
                    fixed = root ^ (1 << color)
                    for mover in range(order):
                        if (
                            fixed >> mover & 1
                            or mover in B
                            or mover == target
                        ):
                            continue
                        predecessor = fixed | (1 << mover)
                        if (
                            predecessor not in greatest
                            or ranks.get(predecessor) != 0
                        ):
                            continue
                        for terminal in B:
                            if predecessor >> terminal & 1:
                                continue
                            successor = fixed | (1 << terminal)
                            if (
                                not (rows[mover] >> terminal & 1)
                                or successor not in greatest
                                or terminal
                                not in CORE.deletion_witness_attacks(
                                    rows, predecessor, ban, ranks
                                )
                            ):
                                continue
                            totals["rank_zero_corridors"] += 1
                            terminal_palette = palette(
                                rows, greatest, root, terminal
                            )
                            for secondary in terminal_palette:
                                if secondary == color:
                                    continue
                                third = next(
                                    vertex
                                    for vertex in root_vertices
                                    if vertex not in (color, secondary)
                                )
                                alternate = (
                                    predecessor
                                    ^ (1 << secondary)
                                    ^ (1 << terminal)
                                )
                                if CORE.dominates(rows, alternate):
                                    raise AssertionError(
                                        (
                                            "C-157 alternate unexpectedly dominates",
                                            catalog_row["catalog_id"],
                                            CORE.vertices(alternate),
                                        )
                                    )
                                totals["secondary_rows"] += 1
                                for witness in CORE.missed_vertices(
                                    rows, alternate
                                ):
                                    q_palette = palette(
                                        rows, greatest, root, mover
                                    )
                                    w_palette = palette(
                                        rows, greatest, root, witness
                                    )
                                    if secondary in q_palette:
                                        endpoint_vertex = mover
                                        endpoint_kind = "mover"
                                    elif secondary in w_palette:
                                        endpoint_vertex = witness
                                        endpoint_kind = "witness"
                                        totals["witness_transfers"] += 1
                                    else:
                                        raise AssertionError(
                                            (
                                                "C-167 transfer failure",
                                                catalog_row["catalog_id"],
                                                color,
                                                secondary,
                                            )
                                        )
                                    recipient_ban = CORE.color_ban(
                                        rows, root, target, secondary
                                    )
                                    recipient_kernel, recipient_ranks, _ = (
                                        CORE.greatest_kernel(
                                            rows, 3, recipient_ban
                                        )
                                    )
                                    recipient_endpoint = (
                                        root
                                        ^ (1 << secondary)
                                        ^ (1 << endpoint_vertex)
                                    )
                                    if recipient_endpoint in recipient_ban:
                                        recipient_status = "banned"
                                        totals["recipient_banned"] += 1
                                    elif recipient_endpoint in recipient_kernel:
                                        recipient_status = "kernel"
                                        totals["recipient_kernel"] += 1
                                    else:
                                        recipient_rank = recipient_ranks.get(
                                            recipient_endpoint
                                        )
                                        if recipient_rank == 0:
                                            recipient_status = "rank_zero"
                                            totals["recipient_rank_zero"] += 1
                                        elif recipient_rank is not None:
                                            recipient_status = (
                                                f"rank_{recipient_rank}"
                                            )
                                            totals[
                                                "recipient_rank_positive"
                                            ] += 1
                                        else:
                                            raise AssertionError(
                                                (
                                                    "unclassified recipient",
                                                    catalog_row["catalog_id"],
                                                )
                                            )
                                    if (
                                        endpoint_kind == "witness"
                                        and witness in B
                                    ):
                                        totals[
                                            "witness_transfers_inside_B"
                                        ] += 1
                                    if (
                                        endpoint_kind == "witness"
                                        and (
                                            witness in B
                                            or recipient_status
                                            not in ("rank_zero",)
                                        )
                                    ):
                                        records.append(
                                            {
                                                "catalog_id": catalog_row[
                                                    "catalog_id"
                                                ],
                                                "graph6": catalog_row["graph6"],
                                                "gamma": CORE.exact_gamma(rows),
                                                "root": list(root_vertices),
                                                "target": target,
                                                "B": sorted(B),
                                                "source_color": color,
                                                "secondary_color": secondary,
                                                "third_color": third,
                                                "mover": mover,
                                                "terminal": terminal,
                                                "witness": witness,
                                                "source_rank": 0,
                                                "palette_mover": list(q_palette),
                                                "palette_terminal": list(
                                                    terminal_palette
                                                ),
                                                "palette_witness": list(
                                                    w_palette
                                                ),
                                                "witness_in_B": witness in B,
                                                "recipient_status": (
                                                    recipient_status
                                                ),
                                                "recipient_endpoint": list(
                                                    CORE.vertices(
                                                        recipient_endpoint
                                                    )
                                                ),
                                            }
                                        )

    inside_B_records = [
        record for record in records if record["witness_in_B"]
    ]
    equality_records = [
        record for record in records if record["gamma"] == 3
    ]
    rank_examples = {}
    for record in records:
        rank_examples.setdefault(record["recipient_status"], record)

    output = {
        "schema": "cross-ban-catalog-scan-v1",
        "status": "OBSERVED",
        "scope": "fixed MMV 2022 Table 9 catalog; discovery only",
        "totals": totals,
        "inside_B_records": inside_B_records,
        "equality_records": equality_records,
        "first_record_by_recipient_status": rank_examples,
        "selected_record_count": len(records),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
