#!/usr/bin/env python3
"""Exhaustive search for the static inactive-bipartite gluing obstruction.

The program streams canonical unlabeled graphs from nauty ``geng`` and
enumerates every active/inactive marking satisfying the C-108 ridge
covariance equations.  It uses only the Python standard library.

This is a discovery/coverage program, not a certificate-producing program.
Its JSON output deliberately labels bounded negative results OBSERVED.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_GENG = (
    HERE.parents[2] / "tools" / "nauty2_9_3" / "geng"
)


def decode_graph6(record: str) -> tuple[int, ...]:
    """Decode a short graph6 record (orders at most 62) into bit rows."""

    record = record.strip()
    if not record or record.startswith(">>"):
        raise ValueError("not a short graph6 record")
    n = ord(record[0]) - 63
    if not 0 <= n <= 62:
        raise ValueError("only short graph6 records are supported")
    bits: list[int] = []
    for char in record[1:]:
        value = ord(char) - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def every_pair_has_common_neighbor(adjacency: tuple[int, ...]) -> bool:
    return all(
        adjacency[u] & adjacency[v]
        for u, v in itertools.combinations(range(len(adjacency)), 2)
    )


def triangles(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    answer: list[int] = []
    for u in range(len(adjacency)):
        later_u = adjacency[u] & ~((1 << (u + 1)) - 1)
        for v in vertices(later_u):
            common = adjacency[u] & adjacency[v] & ~((1 << (v + 1)) - 1)
            for w in vertices(common):
                answer.append((1 << u) | (1 << v) | (1 << w))
    return tuple(answer)


def is_bipartite_induced(adjacency: tuple[int, ...], allowed: int) -> bool:
    side: dict[int, int] = {}
    for root in vertices(allowed):
        if root in side:
            continue
        side[root] = 0
        stack = [root]
        while stack:
            u = stack.pop()
            for v in vertices(adjacency[u] & allowed):
                if v not in side:
                    side[v] = side[u] ^ 1
                    stack.append(v)
                elif side[v] == side[u]:
                    return False
    return True


def colorings(
    adjacency: tuple[int, ...],
    number_of_colors: int = 3,
    stop_after: int | None = None,
) -> list[tuple[int, ...]]:
    """Enumerate proper colorings, fixing vertex 0 to color 0."""

    n = len(adjacency)
    assignment = [-1] * n
    if n:
        assignment[0] = 0
    answer: list[tuple[int, ...]] = []

    def choose() -> int | None:
        uncolored = [v for v in range(n) if assignment[v] < 0]
        if not uncolored:
            return None
        return max(
            uncolored,
            key=lambda v: (
                len(
                    {
                        assignment[u]
                        for u in vertices(adjacency[v])
                        if assignment[u] >= 0
                    }
                ),
                (adjacency[v] & sum(1 << u for u in uncolored)).bit_count(),
                adjacency[v].bit_count(),
                -v,
            ),
        )

    def visit() -> bool:
        v = choose()
        if v is None:
            answer.append(tuple(assignment))
            return stop_after is not None and len(answer) >= stop_after
        forbidden = {
            assignment[u]
            for u in vertices(adjacency[v])
            if assignment[u] >= 0
        }
        for shade in range(number_of_colors):
            if shade in forbidden:
                continue
            assignment[v] = shade
            if visit():
                assignment[v] = -1
                return True
            assignment[v] = -1
        return False

    visit()
    return answer


def is_three_colorable(adjacency: tuple[int, ...]) -> bool:
    return bool(colorings(adjacency, stop_after=1))


def apex_join(adjacency: tuple[int, ...], neighborhood: int) -> tuple[int, ...]:
    n = len(adjacency)
    rows = list(adjacency) + [neighborhood]
    for v in vertices(neighborhood):
        rows[v] |= 1 << n
    return tuple(rows)


class DisjointSet:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, vertex: int) -> int:
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, left: int, right: int) -> None:
        left = self.find(left)
        right = self.find(right)
        if left != right:
            self.parent[right] = left


def covariance_classes(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    """Return vertex masks forced to have a common C-108 status."""

    n = len(adjacency)
    partition = DisjointSet(n)
    for u in range(n):
        for v in vertices(adjacency[u] & ~((1 << (u + 1)) - 1)):
            opposite = adjacency[u] & adjacency[v]
            if opposite:
                first = next(vertices(opposite))
                for other in vertices(opposite ^ (1 << first)):
                    partition.union(first, other)
    classes: dict[int, int] = {}
    for vertex in range(n):
        root = partition.find(vertex)
        classes[root] = classes.get(root, 0) | (1 << vertex)
    return tuple(sorted(classes.values(), key=lambda mask: next(vertices(mask))))


def proper_three_coloring_partitions(
    adjacency: tuple[int, ...],
) -> list[list[list[int]]]:
    """List proper 3-color partitions modulo permutations of colors."""

    normalized: set[tuple[tuple[int, ...], ...]] = set()
    for coloring in colorings(adjacency):
        parts = [tuple(v for v, shade in enumerate(coloring) if shade == c)
                 for c in range(3)]
        normalized.add(tuple(sorted(parts)))
    return [[list(part) for part in partition] for partition in sorted(normalized)]


def analyze_graph(
    record: str,
    adjacency: tuple[int, ...],
    statistics: dict[str, int],
) -> dict[str, object] | None:
    statistics["canonical_graphs"] += 1
    if not every_pair_has_common_neighbor(adjacency):
        return None
    statistics["common_neighbor_graphs"] += 1
    facets = triangles(adjacency)
    if not facets:
        return None
    if not is_three_colorable(adjacency):
        return None
    statistics["static_equality_graphs"] += 1

    n = len(adjacency)
    all_vertices = (1 << n) - 1
    classes = covariance_classes(adjacency)
    statistics["covariance_class_sets"] += 1
    # Status is constant on each class.  Enumerating all unions gives complete
    # marking coverage, though automorphic markings may occur more than once.
    for class_selection in range(1 << len(classes)):
        inactive = 0
        for index, block in enumerate(classes):
            if class_selection & (1 << index):
                inactive |= block
        active = all_vertices ^ inactive
        statistics["covariant_markings"] += 1
        if inactive.bit_count() < 3 or active.bit_count() < 3:
            continue
        if not is_bipartite_induced(adjacency, inactive):
            continue
        statistics["bipartite_inactive_markings"] += 1
        full_facets = [facet for facet in facets if facet & ~active == 0]
        if not full_facets:
            continue
        statistics["full_active_markings"] += 1
        # A 3-coloring using at most two colors on R is exactly a 3-coloring
        # after adjoining an apex adjacent precisely to R.
        if is_three_colorable(apex_join(adjacency, inactive)):
            continue
        statistics["obstructions"] += 1
        partitions = proper_three_coloring_partitions(adjacency)
        if not partitions:
            raise AssertionError("three-colorability changed during analysis")
        if any(
            len(
                {
                    shade
                    for shade, part in enumerate(partition)
                    if set(part) & set(vertices(inactive))
                }
            )
            < 3
            for partition in partitions
        ):
            # The set expression above is intentionally only a safety check;
            # verify directly to avoid depending on part ordering.
            raise AssertionError("apex equivalence check failed")
        return {
            "status": "OBSERVED_EXACT_COUNTERMODEL",
            "order": n,
            "H_prime_graph6_canonical": record,
            "H_prime_edges": [
                [u, v]
                for u in range(n)
                for v in range(u + 1, n)
                if adjacency[u] & (1 << v)
            ],
            "active_A": list(vertices(active)),
            "inactive_R": list(vertices(inactive)),
            "covariance_classes": [list(vertices(block)) for block in classes],
            "full_active_root_facet": list(vertices(full_facets[0])),
            "all_three_coloring_partitions": partitions,
            "number_of_colorings_modulo_color_permutation": len(partitions),
            "inactive_edges": [
                [u, v]
                for u, v in itertools.combinations(vertices(inactive), 2)
                if adjacency[u] & (1 << v)
            ],
        }
    return None


def run_order(
    geng: Path,
    order: int,
    residue: int,
    modulus: int,
) -> tuple[dict[str, int], dict[str, object] | None, str]:
    max_edges = order * order // 3
    command = [
        str(geng),
        "-q",
        "-c",
        "-k",
        "-d2",
        str(order),
        f"0:{max_edges}",
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
        "covariance_class_sets": 0,
        "covariant_markings": 0,
        "bipartite_inactive_markings": 0,
        "full_active_markings": 0,
        "obstructions": 0,
    }
    witness = None
    for line in process.stdout:
        record = line.strip()
        if not record or record.startswith(">>"):
            continue
        witness = analyze_graph(record, decode_graph6(record), statistics)
        if witness is not None:
            process.terminate()
            break
    _stdout, stderr = process.communicate()
    if witness is None and process.returncode != 0:
        raise RuntimeError(
            f"geng failed with status {process.returncode}: {stderr.strip()}"
        )
    return statistics, witness, " ".join(command)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-order", type=int, default=6)
    parser.add_argument("--max-order", type=int, default=10)
    parser.add_argument("--residue", type=int, default=0)
    parser.add_argument("--modulus", type=int, default=1)
    parser.add_argument("--geng", type=Path, default=DEFAULT_GENG)
    parser.add_argument("--output", type=Path, default=HERE / "search_result.json")
    args = parser.parse_args()
    if not (0 <= args.residue < args.modulus):
        raise SystemExit("require 0 <= residue < modulus")
    if not args.geng.is_file():
        raise SystemExit(f"missing geng executable: {args.geng}")

    started = time.time()
    orders: list[dict[str, object]] = []
    witness = None
    for order in range(args.min_order, args.max_order + 1):
        statistics, witness, command = run_order(
            args.geng, order, args.residue, args.modulus
        )
        orders.append(
            {
                "order": order,
                "statistics": statistics,
                "generator_command": command,
            }
        )
        print(
            f"n={order} canonical={statistics['canonical_graphs']} "
            f"common={statistics['common_neighbor_graphs']} "
            f"static={statistics['static_equality_graphs']} "
            f"markings={statistics['covariant_markings']} "
            f"obstructions={statistics['obstructions']}",
            file=sys.stderr,
            flush=True,
        )
        if witness is not None:
            break

    payload = {
        "schema": "inactive-bipartite-gluing-static-search-v1",
        "result_label": (
            "OBSERVED_EXACT_COUNTERMODEL"
            if witness is not None
            else "OBSERVED_BOUNDED_ABSENCE"
        ),
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
