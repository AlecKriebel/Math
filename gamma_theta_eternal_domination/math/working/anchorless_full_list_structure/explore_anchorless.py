#!/usr/bin/env python3
"""Exploratory census for anchorless physical-inactive vertices.

This is discovery code, not an independent verifier.  It scans connected
unlabeled graphs produced by the pinned nauty ``geng`` executable, filters
for gamma=alpha=gamma_inf=3, and records greatest-family full roots whose
target deletion has domination number at least three and whose physical
inactive set contains an anchorless vertex.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(CAMPAIGN / "src"))

from verifier_a.core import BitGraph, eternal_fixed_point, theta  # noqa: E402


def masks_of_size(n: int, size: int):
    for vertices in itertools.combinations(range(n), size):
        mask = sum(1 << vertex for vertex in vertices)
        yield vertices, mask


def gamma_alpha_three(graph: BitGraph) -> tuple[bool, list[int]]:
    independent_triples = [
        mask
        for _vertices, mask in masks_of_size(graph.n, 3)
        if graph.is_independent(mask)
    ]
    if not independent_triples:
        return False, []
    if any(
        graph.is_independent(mask)
        for _vertices, mask in masks_of_size(graph.n, 4)
    ):
        return False, []
    if any(
        graph.is_dominating(mask)
        for size in (1, 2)
        for _vertices, mask in masks_of_size(graph.n, size)
    ):
        return False, []
    return True, independent_triples


def alpha_three(graph: BitGraph) -> tuple[bool, list[int]]:
    independent_triples = [
        mask
        for _vertices, mask in masks_of_size(graph.n, 3)
        if graph.is_independent(mask)
    ]
    if not independent_triples:
        return False, []
    if any(
        graph.is_independent(mask)
        for _vertices, mask in masks_of_size(graph.n, 4)
    ):
        return False, []
    return True, independent_triples


def gamma_alpha_three_from_k4free_complement(
    graph: BitGraph, complement: BitGraph
) -> tuple[bool, list[int]]:
    """Fast static equality-three test when ``complement`` is K4-free."""

    for u, v in itertools.combinations(range(graph.n), 2):
        if not (complement.adj[u] & complement.adj[v]):
            return False, []
    independent_triples = []
    for a, b, c in itertools.combinations(range(graph.n), 3):
        if (
            complement.adj[a] >> b & 1
            and complement.adj[a] >> c & 1
            and complement.adj[b] >> c & 1
        ):
            independent_triples.append((1 << a) | (1 << b) | (1 << c))
    return bool(independent_triples), independent_triples


def deletion_has_no_dominating_pair(graph: BitGraph, deleted: int) -> bool:
    remaining = [vertex for vertex in range(graph.n) if vertex != deleted]
    for size in (1, 2):
        for vertices in itertools.combinations(remaining, size):
            mask = sum(1 << vertex for vertex in vertices)
            covered = mask
            for vertex in vertices:
                covered |= graph.adj[vertex]
            if all(covered & (1 << vertex) for vertex in remaining):
                return False
    return True


def vertices(mask: int) -> list[int]:
    return [vertex for vertex in range(mask.bit_length()) if mask >> vertex & 1]


def analyze_root(
    graph: BitGraph,
    family: set[int],
    root: int,
    target: int,
    require_critical_deletion: bool,
) -> dict[str, object] | None:
    root_vertices = vertices(root)
    target_bit = 1 << target
    successors = [root ^ (1 << anchor) ^ target_bit for anchor in root_vertices]
    if not all(successor in family for successor in successors):
        return None
    deletion_critical = deletion_has_no_dominating_pair(graph, target)
    if require_critical_deletion and not deletion_critical:
        return None

    complement = graph.complement()
    physical = complement.adj[target]
    spokes = {
        anchor: physical & complement.adj[anchor] for anchor in root_vertices
    }
    spoke_union = 0
    for spoke in spokes.values():
        spoke_union |= spoke
    anchorless = physical & ~spoke_union
    if not anchorless:
        return None

    palettes: dict[str, list[int]] = {}
    for vertex in vertices(physical):
        palettes[str(vertex)] = [
            anchor
            for anchor in root_vertices
            if target_bit | (1 << anchor) | (1 << vertex) in family
        ]

    return {
        "root": root_vertices,
        "target": target,
        "deletion_has_no_dominating_pair": deletion_critical,
        "physical_inactive": vertices(physical),
        "spokes": {
            str(anchor): vertices(spoke) for anchor, spoke in spokes.items()
        },
        "anchorless": vertices(anchorless),
        "palettes": palettes,
        "h_b_edges": [
            [u, v]
            for u, v in itertools.combinations(vertices(physical), 2)
            if complement.adj[u] >> v & 1
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-order", type=int, default=6)
    parser.add_argument("--max-order", type=int, default=9)
    parser.add_argument("--stop-after", type=int, default=20)
    parser.add_argument("--allow-noncritical-deletion", action="store_true")
    parser.add_argument("--allow-gamma-two", action="store_true")
    parser.add_argument(
        "--complement-k4free",
        action="store_true",
        help="generate all K4-free complements rather than connected G",
    )
    parser.add_argument("--residue", type=int)
    parser.add_argument("--modulus", type=int)
    args = parser.parse_args()

    geng = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
    records: list[dict[str, object]] = []
    counts: dict[str, int] = {}

    for order in range(args.min_order, args.max_order + 1):
        geng_options = "-kq" if args.complement_k4free else "-cq"
        geng_command = [str(geng), geng_options, str(order)]
        if args.modulus is not None:
            if args.residue is None or not 0 <= args.residue < args.modulus:
                raise SystemExit("require 0 <= residue < modulus")
            geng_command.append(f"{args.residue}/{args.modulus}")
        process = subprocess.Popen(
            geng_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        assert process.stdout is not None
        tested = equality = full_critical = 0
        for line in process.stdout:
            record = line.strip()
            if not record:
                continue
            tested += 1
            generated = BitGraph.from_graph6(record)
            graph = generated.complement() if args.complement_k4free else generated
            if args.complement_k4free:
                static_ok, independent_triples = (
                    gamma_alpha_three_from_k4free_complement(graph, generated)
                )
            elif args.allow_gamma_two:
                static_ok, independent_triples = alpha_three(graph)
            else:
                static_ok, independent_triples = gamma_alpha_three(graph)
            if not static_ok:
                continue
            kernel = eternal_fixed_point(graph, 3)
            if not kernel.exists:
                continue
            equality += 1
            family = set(kernel.family)
            for root in independent_triples:
                if root not in family:
                    raise AssertionError("maximum independent state missing")
                for target in range(order):
                    if root >> target & 1:
                        continue
                    analyzed = analyze_root(
                        graph,
                        family,
                        root,
                        target,
                        not args.allow_noncritical_deletion,
                    )
                    if analyzed is None:
                        continue
                    full_critical += 1
                    records.append(
                        {
                            "graph6": graph.to_graph6(),
                            "generated_complement_graph6": (
                                record if args.complement_k4free else None
                            ),
                            "order": order,
                            "theta": theta(graph),
                            "greatest_family_size": len(family),
                            **analyzed,
                        }
                    )
                    if len(records) >= args.stop_after:
                        process.terminate()
                        process.wait()
                        process.stdout.close()
                        print(
                            json.dumps(
                                {"counts": counts, "records": records},
                                indent=2,
                                sort_keys=True,
                            )
                        )
                        return
        return_code = process.wait()
        process.stdout.close()
        if return_code:
            raise SystemExit(f"geng failed at order {order}: {return_code}")
        counts[str(order)] = {
            "generated_graphs": tested,
            "static_and_eternal_three_graphs": equality,
            "anchorless_full_roots_matching_requested_deletion_filter": (
                full_critical
            ),
        }

    print(json.dumps({"counts": counts, "records": records}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
