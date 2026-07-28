#!/usr/bin/env python3
"""Standalone verifier for the free-singleton polarization control."""

from __future__ import annotations

import argparse
from collections import deque
import hashlib
import itertools
import json
from pathlib import Path


def decode_graph6(record: str) -> tuple[int, list[int]]:
    data = record.encode("ascii")
    if not data or not 63 <= data[0] <= 125:
        raise ValueError("only short graph6 records are supported")
    n = data[0] - 63
    bits: list[int] = []
    for byte in data[1:]:
        value = byte - 63
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * n
    position = 0
    for high in range(1, n):
        for low in range(high):
            if bits[position]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            position += 1
    return n, adjacency


def vertices(mask: int) -> list[int]:
    result = []
    while mask:
        bit = mask & -mask
        mask ^= bit
        result.append(bit.bit_length() - 1)
    return result


def masks_of_size(n: int, size: int):
    for subset in itertools.combinations(range(n), size):
        yield sum(1 << vertex for vertex in subset)


def dominates(state: int, adjacency: list[int], full: int) -> bool:
    covered = state
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        covered |= adjacency[bit.bit_length() - 1]
    return covered == full


def independent(state: int, adjacency: list[int]) -> bool:
    scan = state
    while scan:
        bit = scan & -scan
        scan ^= bit
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & scan:
            return False
    return True


def domination_number(n: int, adjacency: list[int]) -> int:
    full = (1 << n) - 1
    for size in range(1, n + 1):
        if any(
            dominates(state, adjacency, full)
            for state in masks_of_size(n, size)
        ):
            return size
    raise AssertionError("no dominating set")


def independence_number(n: int, adjacency: list[int]) -> int:
    for size in range(n, 0, -1):
        if any(
            independent(state, adjacency)
            for state in masks_of_size(n, size)
        ):
            return size
    return 0


def independent_domination_number(n: int, adjacency: list[int]) -> int:
    full = (1 << n) - 1
    for size in range(1, n + 1):
        for state in masks_of_size(n, size):
            if independent(state, adjacency) and dominates(
                state, adjacency, full
            ):
                return size
    raise AssertionError("no maximal independent set")


def greatest_family(
    n: int, adjacency: list[int], size: int
) -> tuple[set[int], int]:
    full = (1 << n) - 1
    family = {
        state
        for state in masks_of_size(n, size)
        if dominates(state, adjacency, full)
    }
    rounds = 0
    while True:
        bad = set()
        for state in family:
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                scan = state & adjacency[attacked]
                if not any(
                    ((state ^ bit) | attacked_bit) in family
                    for bit in (
                        1 << guard
                        for guard in range(n)
                        if scan & (1 << guard)
                    )
                ):
                    bad.add(state)
                    break
        if not bad:
            return family, rounds
        family -= bad
        rounds += 1


def eternal_domination_number(n: int, adjacency: list[int]) -> int:
    for size in range(1, n + 1):
        family, _ = greatest_family(n, adjacency, size)
        if family:
            return size
    raise AssertionError("no eternal family")


def theta_number(n: int, adjacency: list[int]) -> int:
    full = (1 << n) - 1
    h_neighbors = [
        full ^ adjacency[vertex] ^ (1 << vertex) for vertex in range(n)
    ]

    def colorable(color_count: int) -> bool:
        colors = [-1] * n

        def visit() -> bool:
            if all(color >= 0 for color in colors):
                return True
            uncolored = [v for v in range(n) if colors[v] < 0]
            vertex = max(
                uncolored,
                key=lambda v: (
                    len(
                        {
                            colors[w]
                            for w in vertices(h_neighbors[v])
                            if colors[w] >= 0
                        }
                    ),
                    h_neighbors[v].bit_count(),
                    -v,
                ),
            )
            forbidden = {
                colors[w]
                for w in vertices(h_neighbors[vertex])
                if colors[w] >= 0
            }
            for color in range(color_count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                if visit():
                    return True
                colors[vertex] = -1
            return False

        return visit()

    for count in range(1, n + 1):
        if colorable(count):
            return count
    raise AssertionError("coloring failure")


def verify_family(
    n: int, adjacency: list[int], family: set[int]
) -> tuple[int, str]:
    full = (1 << n) - 1
    obligations = 0
    rows = []
    for state in sorted(family):
        if not dominates(state, adjacency, full):
            raise AssertionError("retained state is nondominating")
        for attacked in range(n):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            legal = []
            scan = state & adjacency[attacked]
            while scan:
                guard_bit = scan & -scan
                scan ^= guard_bit
                successor = (state ^ guard_bit) | attacked_bit
                if successor in family:
                    legal.append(guard_bit.bit_length() - 1)
            if not legal:
                raise AssertionError("unanswered attack")
            obligations += 1
            rows.append([state, attacked, legal])
    digest = hashlib.sha256(
        json.dumps(rows, separators=(",", ":")).encode()
    ).hexdigest()
    return obligations, digest


def response_lists(
    n: int, family: set[int], reference: int
) -> dict[int, list[int]]:
    anchors = vertices(reference)
    result = {}
    for outside in range(n):
        if reference & (1 << outside):
            continue
        response = []
        for anchor in anchors:
            successor = (reference ^ (1 << anchor)) | (1 << outside)
            if successor in family:
                response.append(anchor)
        if not response:
            raise AssertionError("empty response list")
        result[outside] = response
    return result


def projection(
    n: int,
    adjacency: list[int],
    reference: int,
    lists: dict[int, list[int]],
    frozen: int,
) -> dict[str, object]:
    full = (1 << n) - 1
    remaining = [v for v in vertices(reference) if v != frozen]
    projected = set(remaining)
    projected.update(v for v, response in lists.items() if frozen not in response)
    projected_mask = sum(1 << v for v in projected)
    side: dict[int, int] = {}
    component: dict[int, int] = {}
    components: list[list[int]] = []
    for root in sorted(projected):
        if root in side:
            continue
        index = len(components)
        side[root] = 0
        component[root] = index
        queue = deque([root])
        members = []
        while queue:
            vertex = queue.popleft()
            members.append(vertex)
            h_scan = (
                full ^ adjacency[vertex] ^ (1 << vertex)
            ) & projected_mask
            while h_scan:
                bit = h_scan & -h_scan
                h_scan ^= bit
                neighbor = bit.bit_length() - 1
                if neighbor not in side:
                    side[neighbor] = side[vertex] ^ 1
                    component[neighbor] = index
                    queue.append(neighbor)
                elif side[neighbor] == side[vertex]:
                    raise AssertionError("projection complement is not bipartite")
        components.append(sorted(members))
    anchor_component = component[remaining[0]]
    if component[remaining[1]] != anchor_component:
        raise AssertionError("anchor edge split")
    return {
        "remaining": remaining,
        "side": side,
        "component": component,
        "components": components,
        "anchor_component": anchor_component,
    }


def audit(data: dict[str, object]) -> dict[str, object]:
    n, adjacency = decode_graph6(str(data["graph6"]))
    edge_count = sum(mask.bit_count() for mask in adjacency) // 2
    if n != data["expected_order"] or edge_count != data["expected_size"]:
        raise AssertionError("order/size mismatch")
    family, rounds = greatest_family(n, adjacency, 3)
    obligations, response_hash = verify_family(n, adjacency, family)
    reference = sum(1 << v for v in data["reference"])
    if reference not in family or not independent(reference, adjacency):
        raise AssertionError("reference mismatch")
    lists = response_lists(n, family, reference)
    expected_lists = {
        int(v): response for v, response in data["expected_lists"].items()
    }
    if lists != expected_lists:
        raise AssertionError(f"list mismatch: {lists}")
    parameters = {
        "gamma": domination_number(n, adjacency),
        "i": independent_domination_number(n, adjacency),
        "alpha": independence_number(n, adjacency),
        "gamma_infinity": eternal_domination_number(n, adjacency),
        "theta": theta_number(n, adjacency),
    }
    if parameters != data["expected_parameters"]:
        raise AssertionError(f"parameter mismatch: {parameters}")
    if len(family) != data["expected_family_size"]:
        raise AssertionError("family-size mismatch")
    if obligations != data["expected_obligations"]:
        raise AssertionError("obligation mismatch")

    projections = {
        frozen: projection(n, adjacency, reference, lists, frozen)
        for frozen in vertices(reference)
    }
    found = []
    lifted = set()
    full = (1 << n) - 1
    for singleton, response in sorted(lists.items()):
        if len(response) != 1:
            continue
        demanded = response[0]
        for frozen in sorted(set(vertices(reference)) - {demanded}):
            info = projections[frozen]
            component_index = info["component"][singleton]
            if component_index == info["anchor_component"]:
                continue
            other_anchor = next(
                anchor
                for anchor in vertices(reference)
                if anchor not in (frozen, demanded)
            )
            members = info["components"][component_index]
            singleton_side = info["side"][singleton]
            for vertex in members:
                required = (
                    demanded
                    if info["side"][vertex] == singleton_side
                    else other_anchor
                )
                if required not in lists.get(vertex, []):
                    raise AssertionError("polarization conclusion failed")
            for left, right in itertools.combinations(members, 2):
                if adjacency[left] >> right & 1:
                    continue
                triple = tuple(sorted((frozen, left, right)))
                state = sum(1 << vertex for vertex in triple)
                if state not in family:
                    raise AssertionError("component edge did not lift")
                lifted.add(triple)
            found.append(
                {
                    "singleton": singleton,
                    "frozen": frozen,
                    "demanded": demanded,
                    "other_anchor": other_anchor,
                    "component": members,
                }
            )
    if found != data["expected_free_incidences"]:
        raise AssertionError(f"free-incidence mismatch: {found}")
    expected_lifted = {
        tuple(row) for row in data["expected_lifted_component_edges"]
    }
    if lifted != expected_lifted:
        raise AssertionError(f"lifted-edge mismatch: {lifted}")
    family_hash = hashlib.sha256(
        json.dumps(
            [vertices(state) for state in sorted(family)],
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    return {
        "graph6": data["graph6"],
        "order": n,
        "size": edge_count,
        "parameters": parameters,
        "family_size": len(family),
        "deletion_rounds": rounds,
        "obligations": obligations,
        "family_sha256": family_hash,
        "response_certificate_sha256": response_hash,
        "lists": {str(v): response for v, response in lists.items()},
        "free_incidences": found,
        "lifted_component_edges": [list(row) for row in sorted(lifted)],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", required=True, type=Path)
    args = parser.parse_args()
    controls = json.loads(args.check.read_text())
    result = {
        "schema": "free-unit-chain-attack-verification-v1",
        "model": controls["standard_model"],
        "case": audit(controls["free_singleton_component"]),
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
