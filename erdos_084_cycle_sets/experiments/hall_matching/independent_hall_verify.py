#!/usr/bin/env python3
"""Independent verifier for the bounded Hall-transport experiment.

This implementation deliberately differs from ``hall_transport.cpp``:

* signature families and all terms in the deletion--contraction identity are
  formed with direct Python set semantics;
* transportation is solved by a FIFO push--relabel algorithm, not Dinic;
* a failed flow is checked again as an explicit Hall inequality.

Only m=6 and m=7 are accepted.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Profile:
    safe: int
    safe_images: int
    boundary0: int
    boundary1: int

    @property
    def deficit(self) -> int:
        return self.safe - self.safe_images

    @property
    def capacity(self) -> int:
        return self.boundary0 + self.boundary1

    @property
    def g(self) -> int:
        return self.capacity - self.deficit


@dataclass
class Edge:
    to: int
    reverse: int
    capacity: int


class PushRelabel:
    """Small, deterministic FIFO push--relabel implementation."""

    def __init__(self, node_count: int) -> None:
        self.graph: list[list[Edge]] = [[] for _ in range(node_count)]

    def add_edge(self, source: int, target: int, capacity: int) -> None:
        forward = Edge(target, len(self.graph[target]), capacity)
        reverse = Edge(source, len(self.graph[source]), 0)
        self.graph[source].append(forward)
        self.graph[target].append(reverse)

    def max_flow(self, source: int, sink: int) -> int:
        node_count = len(self.graph)
        height = [0] * node_count
        excess = [0] * node_count
        current = [0] * node_count
        active = [False] * node_count
        queue: deque[int] = deque()

        def enqueue(node: int) -> None:
            if (
                node != source
                and node != sink
                and excess[node] > 0
                and not active[node]
            ):
                active[node] = True
                queue.append(node)

        def push(node: int, edge: Edge) -> None:
            amount = min(excess[node], edge.capacity)
            if amount == 0:
                return
            edge.capacity -= amount
            self.graph[edge.to][edge.reverse].capacity += amount
            excess[node] -= amount
            excess[edge.to] += amount
            enqueue(edge.to)

        height[source] = node_count
        for edge in self.graph[source]:
            amount = edge.capacity
            if amount == 0:
                continue
            edge.capacity = 0
            self.graph[edge.to][edge.reverse].capacity += amount
            excess[edge.to] += amount
            excess[source] -= amount
            enqueue(edge.to)

        while queue:
            node = queue.popleft()
            active[node] = False
            while excess[node] > 0:
                if current[node] == len(self.graph[node]):
                    residual_heights = [
                        height[edge.to]
                        for edge in self.graph[node]
                        if edge.capacity > 0
                    ]
                    if not residual_heights:
                        raise AssertionError("active node has no residual edge")
                    height[node] = min(residual_heights) + 1
                    current[node] = 0
                    continue

                edge = self.graph[node][current[node]]
                if edge.capacity > 0 and height[node] == height[edge.to] + 1:
                    push(node, edge)
                else:
                    current[node] += 1
            enqueue(node)

        return excess[sink]

    def reachable(self, source: int) -> set[int]:
        reached = {source}
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for edge in self.graph[node]:
                if edge.capacity > 0 and edge.to not in reached:
                    reached.add(edge.to)
                    queue.append(edge.to)
        return reached


def bits(mask: int) -> Iterable[int]:
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def coordinate_bit(m: int, value: int) -> int:
    return 1 << (value + m)


def generator(m: int, p_mask: int, b: int) -> int:
    values = {b, -b}
    values.update(
        b - (index + 1)
        for index in bits(p_mask)
        if -m <= b - (index + 1) <= m
    )
    result = 0
    for value in values:
        result |= coordinate_bit(m, value)
    return result


def union_family(generators: Iterable[int]) -> set[int]:
    family = {0}
    for row in generators:
        family |= {signature | row for signature in tuple(family)}
    return family


def shadow_mask(m: int, p_mask: int) -> int:
    result = 0
    for index in bits(p_mask):
        p = index + 1
        result |= coordinate_bit(m, m + 1 - p)
    return result


def compute_profile(m: int, optional_mask: int) -> Profile:
    p_mask = (optional_mask << 1) | 1
    family = union_family(
        generator(m, p_mask, b)
        for b in range(-m, m + 1)
        if b != 0
    )

    bottom = coordinate_bit(m, -m)
    safe = {signature for signature in family if signature & bottom == 0}
    unsafe = {
        signature & ~bottom for signature in family if signature & bottom
    }
    u_mask = shadow_mask(m, p_mask)

    safe_images = {signature | u_mask for signature in safe}
    unsafe_images = {signature | u_mask for signature in unsafe}
    boundary0 = unsafe_images - unsafe
    boundary1 = (safe_images | unsafe_images) - unsafe

    direct0 = {signature | u_mask for signature in family} - family
    direct1 = {signature | u_mask | bottom for signature in family} - family

    profile = Profile(
        safe=len(safe),
        safe_images=len(safe_images),
        boundary0=len(boundary0),
        boundary1=len(boundary1),
    )
    if len(direct0) != profile.safe_images + profile.boundary0:
        raise AssertionError(f"e0 identity failed at m={m}, P={p_mask}")
    if len(direct1) != profile.boundary1:
        raise AssertionError(f"e1 identity failed at m={m}, P={p_mask}")
    if len(direct0) + len(direct1) - profile.safe != profile.g:
        raise AssertionError(f"DC identity failed at m={m}, P={p_mask}")
    if profile.deficit < 0:
        raise AssertionError(f"negative deficit at m={m}, P={p_mask}")
    return profile


def locality_targets(optional_mask: int, radius: int) -> list[int]:
    targets = [optional_mask]
    present = list(bits(optional_mask))
    if radius >= 1:
        targets.extend(optional_mask ^ (1 << first) for first in present)
    if radius >= 2:
        targets.extend(
            optional_mask ^ (1 << present[first]) ^ (1 << present[second])
            for first in range(len(present))
            for second in range(first + 1, len(present))
        )
    return targets


def fnv_masks(masks: Iterable[int]) -> int:
    value = 1469598103934665603
    for mask in masks:
        for byte in range(8):
            value ^= (mask >> (8 * byte)) & 255
            value = (value * 1099511628211) & ((1 << 64) - 1)
    return value


def solve_transport(
    profiles: list[Profile], radius: int, net: bool
) -> dict[str, int | str]:
    supplies = [
        max(0, -profile.g) if net else profile.deficit
        for profile in profiles
    ]
    capacities = [
        max(0, profile.g) if net else profile.capacity
        for profile in profiles
    ]
    left_masks = [mask for mask, value in enumerate(supplies) if value]
    right_masks = [mask for mask, value in enumerate(capacities) if value]
    right_index = {mask: index for index, mask in enumerate(right_masks)}

    source = 0
    left_offset = 1
    right_offset = left_offset + len(left_masks)
    sink = right_offset + len(right_masks)
    network = PushRelabel(sink + 1)

    total_supply = sum(supplies)
    total_capacity = sum(capacities)
    infinity = total_supply + 1
    for index, mask in enumerate(left_masks):
        network.add_edge(source, left_offset + index, supplies[mask])
    for index, mask in enumerate(right_masks):
        network.add_edge(right_offset + index, sink, capacities[mask])

    transport_edges = 0
    for left_index, p_mask in enumerate(left_masks):
        left_node = left_offset + left_index
        for q_mask in locality_targets(p_mask, radius):
            q_index = right_index.get(q_mask)
            if q_index is not None:
                network.add_edge(left_node, right_offset + q_index, infinity)
                transport_edges += 1

    maximum = network.max_flow(source, sink)
    reached = network.reachable(source)
    hall_left = sorted(
        mask
        for index, mask in enumerate(left_masks)
        if left_offset + index in reached
    )
    # Include zero-capacity target profiles in the exact Hall neighborhood,
    # as the mathematical neighborhood is determined by locality alone.
    hall_neighbors = sorted(
        {
            q_mask
            for p_mask in hall_left
            for q_mask in locality_targets(p_mask, radius)
        }
    )
    hall_supply = sum(supplies[mask] for mask in hall_left)
    hall_capacity = sum(capacities[mask] for mask in hall_neighbors)
    deficiency = hall_supply - hall_capacity

    if maximum < total_supply:
        if deficiency != total_supply - maximum or deficiency <= 0:
            raise AssertionError(
                "min-cut and max-flow deficiencies do not agree"
            )
    elif deficiency > 0:
        raise AssertionError("full flow has a positive Hall deficiency")

    return {
        "supply": total_supply,
        "capacity": total_capacity,
        "transport_edges": transport_edges,
        "flow": maximum,
        "unmatched": total_supply - maximum,
        "status": "FULL" if maximum == total_supply else "HALL_FAILURE",
        "hall_left_count": len(hall_left),
        "hall_left_supply": hall_supply,
        "hall_neighbor_count": len(hall_neighbors),
        "hall_neighbor_capacity": hall_capacity,
        "hall_deficiency": max(0, deficiency),
        "hall_left_hash": f"0x{fnv_masks(hall_left):016x}",
        "hall_neighbor_hash": f"0x{fnv_masks(hall_neighbors):016x}",
    }


EXPECTED = {
    6: {
        "totals": (35594, 24439, 11155, 27462, 27462, 43769),
        "raw1": (11155, 11155, 0),
        "net1": (704, 697, 7),
        "net2": (704, 704, 0),
        "cut1": (2, 24, 15, 17, 7),
        "cut_hashes": (
            "0x89e3b6901036955f",
            "0x81f34ce2fb88521e",
        ),
    },
    7: {
        "totals": (254496, 152873, 101623, 192036, 192036, 282449),
        "raw1": (101623, 101623, 0),
        "net1": (4857, 4699, 158),
        "net2": (4857, 4857, 0),
        "cut1": (21, 371, 166, 213, 158),
        "cut_hashes": (
            "0xb5e30b823ec0eade",
            "0x366cd4a12d77bfd1",
        ),
    },
}


def verify_m(m: int) -> None:
    optional_count = 1 << (2 * m - 1)
    profiles = [compute_profile(m, mask) for mask in range(optional_count)]

    safe = sum(profile.safe for profile in profiles)
    safe_images = sum(profile.safe_images for profile in profiles)
    deficit = sum(profile.deficit for profile in profiles)
    boundary0 = sum(profile.boundary0 for profile in profiles)
    boundary1 = sum(profile.boundary1 for profile in profiles)
    g_total = sum(profile.g for profile in profiles)
    totals = (safe, safe_images, deficit, boundary0, boundary1, g_total)
    if totals != EXPECTED[m]["totals"]:
        raise AssertionError(
            f"m={m} profile totals {totals} != {EXPECTED[m]['totals']}"
        )
    print(
        f"m={m} profiles={optional_count} safe={safe} "
        f"safe_images={safe_images} deficit={deficit} "
        f"boundary0={boundary0} boundary1={boundary1} g={g_total}"
    )

    results = {
        "raw1": solve_transport(profiles, radius=1, net=False),
        "net1": solve_transport(profiles, radius=1, net=True),
        "net2": solve_transport(profiles, radius=2, net=True),
    }
    for label, result in results.items():
        expected = EXPECTED[m][label]
        actual = (
            result["supply"],
            result["flow"],
            result["unmatched"],
        )
        if actual != expected:
            raise AssertionError(
                f"m={m} {label} {actual} != expected {expected}"
            )
        print(
            f"m={m} {label} supply={result['supply']} "
            f"capacity={result['capacity']} flow={result['flow']} "
            f"unmatched={result['unmatched']} status={result['status']} "
            f"compressed_edges={result['transport_edges']}"
        )

    net1 = results["net1"]
    cut = (
        net1["hall_left_count"],
        net1["hall_left_supply"],
        net1["hall_neighbor_count"],
        net1["hall_neighbor_capacity"],
        net1["hall_deficiency"],
    )
    if cut != EXPECTED[m]["cut1"]:
        raise AssertionError(
            f"m={m} net1 Hall witness {cut} != {EXPECTED[m]['cut1']}"
        )
    hashes = (
        net1["hall_left_hash"],
        net1["hall_neighbor_hash"],
    )
    if hashes != EXPECTED[m]["cut_hashes"]:
        raise AssertionError(
            f"m={m} net1 Hall hashes {hashes} "
            f"!= {EXPECTED[m]['cut_hashes']}"
        )
    print(
        f"m={m} net1_cut left={cut[0]} supply={cut[1]} "
        f"neighbors={cut[2]} capacity={cut[3]} deficiency={cut[4]} "
        f"left_hash={net1['hall_left_hash']} "
        f"neighbor_hash={net1['hall_neighbor_hash']}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--m",
        choices=("6", "7", "all"),
        default="all",
        help="bounded case to verify",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    values = (6, 7) if args.m == "all" else (int(args.m),)
    for m in values:
        verify_m(m)
    print("independent Hall verification passed")


if __name__ == "__main__":
    main()
