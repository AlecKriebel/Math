#!/usr/bin/env python3
"""Search successive literal one-guard strengthenings of the static model.

The base obstruction is the one in ``search_static.py``.  Optional layers:

``gamma3``
    After adjoining the target x in the complement, every pair still has a
    common neighbor.  Equivalently, the resulting guard graph has gamma=3.

``successors``
    In addition, every response prescribed active by the marking produces a
    dominating triple after the move to x.

``rank1``, ``rank2``, ...
    In addition, every deletion triangle survives that many synchronous
    rounds of the exact greatest-family deletion operator.

``eternal``
    Every deletion triangle survives the stabilized kernel.  In the equality
    setting this is equivalent to an eternal three-guard family.

Outputs are discovery artifacts and are labeled OBSERVED.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_BASE_SPEC = importlib.util.spec_from_file_location(
    "inactive_bipartite_search_static", HERE / "search_static.py"
)
if _BASE_SPEC is None or _BASE_SPEC.loader is None:
    raise RuntimeError("cannot load search_static.py")
base = importlib.util.module_from_spec(_BASE_SPEC)
_BASE_SPEC.loader.exec_module(base)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    universe = (1 << len(adjacency)) - 1
    return tuple(universe ^ (1 << v) ^ adjacency[v] for v in range(len(adjacency)))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in base.vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def masks_of_size(order: int, size: int):
    for subset in itertools.combinations(range(order), size):
        yield sum(1 << vertex for vertex in subset)


def kernel_ranks(
    adjacency: tuple[int, ...], size: int = 3
) -> tuple[frozenset[int], dict[int, int], list[int]]:
    """Exact synchronous greatest-family deletion with removal ranks."""

    order = len(adjacency)
    universe = (1 << order) - 1
    family = {
        state for state in masks_of_size(order, size) if dominates(adjacency, state)
    }
    ranks: dict[int, int] = {}
    removed_per_round: list[int] = []
    round_number = 0
    while True:
        deleted: list[int] = []
        for state in family:
            for attack in base.vertices(universe ^ state):
                if not any(
                    ((state ^ (1 << guard)) | (1 << attack)) in family
                    for guard in base.vertices(state & adjacency[attack])
                ):
                    deleted.append(state)
                    break
        if not deleted:
            return frozenset(family), ranks, removed_per_round
        round_number += 1
        removed_per_round.append(len(deleted))
        for state in deleted:
            family.remove(state)
            ranks[state] = round_number


def target_extension(
    h_prime: tuple[int, ...], inactive: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    h = base.apex_join(h_prime, inactive)
    return h, complement(h)


def static_successors_dominate(
    g: tuple[int, ...],
    deletion_facets: tuple[int, ...],
    active: int,
    target: int,
) -> bool:
    for facet in deletion_facets:
        for guard in base.vertices(facet & active):
            successor = (facet ^ (1 << guard)) | (1 << target)
            if not (g[guard] & (1 << target)):
                return False
            if not dominates(g, successor):
                return False
    return True


def layer_number(label: str) -> int | None:
    if label.startswith("rank"):
        value = int(label[4:])
        if value < 1:
            raise ValueError("rank horizon must be positive")
        return value
    return None


def qualifies(
    label: str,
    h_prime: tuple[int, ...],
    facets: tuple[int, ...],
    active: int,
    inactive: int,
) -> tuple[bool, dict[str, object]]:
    h, g = target_extension(h_prime, inactive)
    target = len(h_prime)
    details: dict[str, object] = {
        "target": target,
        "H_with_target_graph6_labeled": graph6(h),
        "G_with_target_graph6_labeled": graph6(g),
    }
    if label == "static":
        return True, details
    if not base.every_pair_has_common_neighbor(h):
        return False, details
    details["global_gamma_equals_alpha_equals_3"] = True
    if label == "gamma3":
        return True, details
    if not static_successors_dominate(g, facets, active, target):
        return False, details
    details["all_marked_target_successors_dominate"] = True
    if label == "successors":
        return True, details

    family, ranks, removed = kernel_ranks(g)
    required_ranks = {
        tuple(base.vertices(facet)): ranks.get(facet)
        for facet in facets
    }
    details["dominating_triple_kernel_final_size"] = len(family)
    details["kernel_removed_per_round"] = removed
    details["required_facet_deletion_ranks"] = [
        {
            "facet": list(facet),
            "rank": required_ranks[facet],
        }
        for facet in sorted(required_ranks)
    ]
    if label == "eternal":
        return all(facet in family for facet in facets), details
    horizon = layer_number(label)
    assert horizon is not None
    return all(
        ranks.get(facet, horizon + 1) > horizon
        for facet in facets
    ), details


def graph6(adjacency: tuple[int, ...]) -> str:
    bits: list[int] = []
    for high in range(1, len(adjacency)):
        for low in range(high):
            bits.append(1 if adjacency[low] & (1 << high) else 0)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(len(adjacency) + 63) + "".join(payload)


def analyze_graph(
    label: str,
    record: str,
    adjacency: tuple[int, ...],
    statistics: dict[str, int],
) -> dict[str, object] | None:
    statistics["canonical_graphs"] += 1
    if not base.every_pair_has_common_neighbor(adjacency):
        return None
    statistics["common_neighbor_graphs"] += 1
    facets = base.triangles(adjacency)
    if not facets or not base.is_three_colorable(adjacency):
        return None
    statistics["static_equality_graphs"] += 1

    order = len(adjacency)
    universe = (1 << order) - 1
    classes = base.covariance_classes(adjacency)
    for selection in range(1 << len(classes)):
        inactive = 0
        for index, block in enumerate(classes):
            if selection & (1 << index):
                inactive |= block
        active = universe ^ inactive
        statistics["covariant_markings"] += 1
        if inactive.bit_count() < 3 or active.bit_count() < 3:
            continue
        if not base.is_bipartite_induced(adjacency, inactive):
            continue
        full_facets = [facet for facet in facets if facet & ~active == 0]
        if not full_facets:
            continue
        if base.is_three_colorable(base.apex_join(adjacency, inactive)):
            continue
        statistics["base_obstructions"] += 1
        accepted, details = qualifies(
            label, adjacency, facets, active, inactive
        )
        if not accepted:
            continue
        statistics["layer_obstructions"] += 1
        partitions = base.proper_three_coloring_partitions(adjacency)
        return {
            "status": "OBSERVED_EXACT_COUNTERMODEL",
            "required_layer": label,
            "order_of_H_prime": order,
            "H_prime_graph6_canonical": record,
            "H_prime_edges": [
                [u, v]
                for u in range(order)
                for v in range(u + 1, order)
                if adjacency[u] & (1 << v)
            ],
            "active_A": list(base.vertices(active)),
            "inactive_R": list(base.vertices(inactive)),
            "inactive_edges": [
                [u, v]
                for u, v in itertools.combinations(base.vertices(inactive), 2)
                if adjacency[u] & (1 << v)
            ],
            "covariance_classes": [
                list(base.vertices(block)) for block in classes
            ],
            "full_active_root_facet": list(base.vertices(full_facets[0])),
            "all_deletion_coloring_partitions": partitions,
            **details,
        }
    return None


def run_order(
    geng: Path,
    order: int,
    label: str,
    residue: int,
    modulus: int,
) -> tuple[dict[str, int], dict[str, object] | None, str]:
    command = [
        str(geng),
        "-q",
        "-c",
        "-k",
        "-d2",
        str(order),
        f"0:{order * order // 3}",
    ]
    if modulus > 1:
        command.append(f"{residue}/{modulus}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert process.stdout is not None
    statistics = {
        "canonical_graphs": 0,
        "common_neighbor_graphs": 0,
        "static_equality_graphs": 0,
        "covariant_markings": 0,
        "base_obstructions": 0,
        "layer_obstructions": 0,
    }
    witness = None
    for line in process.stdout:
        record = line.strip()
        if not record or record.startswith(">>"):
            continue
        witness = analyze_graph(
            label, record, base.decode_graph6(record), statistics
        )
        if witness is not None:
            process.terminate()
            break
    _stdout, stderr = process.communicate()
    if witness is None and process.returncode:
        raise RuntimeError(stderr.strip())
    return statistics, witness, " ".join(command)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--layer",
        default="gamma3",
        help="static, gamma3, successors, rankN, or eternal",
    )
    parser.add_argument("--min-order", type=int, default=6)
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument("--residue", type=int, default=0)
    parser.add_argument("--modulus", type=int, default=1)
    parser.add_argument("--geng", type=Path, default=base.DEFAULT_GENG)
    parser.add_argument("--output", type=Path, default=HERE / "layer_result.json")
    args = parser.parse_args()
    if args.layer not in {"static", "gamma3", "successors", "eternal"}:
        try:
            layer_number(args.layer)
        except (ValueError, TypeError):
            raise SystemExit("invalid --layer") from None
    if not 0 <= args.residue < args.modulus:
        raise SystemExit("require 0 <= residue < modulus")

    started = time.time()
    orders: list[dict[str, object]] = []
    witness = None
    for order in range(args.min_order, args.max_order + 1):
        stats, witness, command = run_order(
            args.geng, order, args.layer, args.residue, args.modulus
        )
        orders.append(
            {"order": order, "statistics": stats, "generator_command": command}
        )
        print(
            f"layer={args.layer} n={order} "
            f"graphs={stats['canonical_graphs']} "
            f"base={stats['base_obstructions']} "
            f"accepted={stats['layer_obstructions']}",
            file=sys.stderr,
            flush=True,
        )
        if witness is not None:
            break
    payload = {
        "schema": "inactive-bipartite-gluing-layer-search-v1",
        "result_label": (
            "OBSERVED_EXACT_COUNTERMODEL"
            if witness is not None
            else "OBSERVED_BOUNDED_ABSENCE"
        ),
        "required_layer": args.layer,
        "scope": {
            "orders": [args.min_order, orders[-1]["order"]],
            "geng_residue": args.residue,
            "geng_modulus": args.modulus,
            "canonical_unlabeled_graphs": True,
            "all_ridge_covariant_markings_enumerated": True,
            "proof_certificate_claimed": False,
        },
        "orders": orders,
        "witness": witness,
        "wall_seconds": time.time() - started,
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
