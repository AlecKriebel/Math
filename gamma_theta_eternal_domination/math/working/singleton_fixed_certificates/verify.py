#!/usr/bin/env python3
"""Independent verifier for the anchor-fixed response controls.

The implementation uses only the Python standard library and does not
import campaign search or evaluator code.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
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
    if position > len(bits):
        raise ValueError("truncated graph6 record")
    return n, adjacency


def vertices(mask: int) -> list[int]:
    result = []
    scan = mask
    while scan:
        bit = scan & -scan
        scan ^= bit
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
        if any(dominates(state, adjacency, full) for state in masks_of_size(n, size)):
            return size
    raise AssertionError("finite graph has no dominating set")


def independence_number(n: int, adjacency: list[int]) -> int:
    for size in range(n, 0, -1):
        if any(independent(state, adjacency) for state in masks_of_size(n, size)):
            return size
    return 0


def independent_domination_number(n: int, adjacency: list[int]) -> int:
    full = (1 << n) - 1
    for size in range(1, n + 1):
        for state in masks_of_size(n, size):
            if independent(state, adjacency) and dominates(state, adjacency, full):
                return size
    raise AssertionError("every maximal independent set dominates")


def greatest_family(n: int, adjacency: list[int], size: int) -> tuple[set[int], int]:
    full = (1 << n) - 1
    family = {
        state
        for state in masks_of_size(n, size)
        if dominates(state, adjacency, full)
    }
    rounds = 0
    while True:
        bad: set[int] = set()
        for state in family:
            for attacked in range(n):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                responders = state & adjacency[attacked]
                legal = False
                scan = responders
                while scan:
                    guard_bit = scan & -scan
                    scan ^= guard_bit
                    successor = (state ^ guard_bit) | attacked_bit
                    if successor in family:
                        legal = True
                        break
                if not legal:
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
    raise AssertionError("finite graph has an eternal family")


def theta_number(n: int, adjacency: list[int]) -> int:
    full = (1 << n) - 1
    h_neighbors = [
        full ^ adjacency[vertex] ^ (1 << vertex) for vertex in range(n)
    ]

    def colorable(color_count: int) -> bool:
        colors = [-1] * n
        saturation = [set() for _ in range(n)]

        def visit(colored: int) -> bool:
            if colored == n:
                return True
            uncolored = [v for v in range(n) if colors[v] < 0]
            vertex = max(
                uncolored,
                key=lambda v: (len(saturation[v]), h_neighbors[v].bit_count(), -v),
            )
            forbidden = {
                colors[u]
                for u in vertices(h_neighbors[vertex])
                if colors[u] >= 0
            }
            for color in range(color_count):
                if color in forbidden:
                    continue
                colors[vertex] = color
                changed = []
                for neighbor in vertices(h_neighbors[vertex]):
                    if colors[neighbor] < 0 and color not in saturation[neighbor]:
                        saturation[neighbor].add(color)
                        changed.append(neighbor)
                if visit(colored + 1):
                    return True
                for neighbor in changed:
                    saturation[neighbor].remove(color)
                colors[vertex] = -1
            return False

        return visit(0)

    for count in range(1, n + 1):
        if colorable(count):
            return count
    raise AssertionError("unreachable")


def verify_family(
    n: int, adjacency: list[int], family: set[int]
) -> tuple[int, str]:
    full = (1 << n) - 1
    obligations = 0
    responses = []
    for state in sorted(family):
        if not dominates(state, adjacency, full):
            raise AssertionError("retained state does not dominate")
        for attacked in range(n):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            obligations += 1
            legal = []
            scan = state & adjacency[attacked]
            while scan:
                guard_bit = scan & -scan
                scan ^= guard_bit
                successor = (state ^ guard_bit) | attacked_bit
                if successor in family:
                    legal.append(guard_bit.bit_length() - 1)
            if not legal:
                raise AssertionError("one-guard obligation has no response")
            responses.append([state, attacked, legal])
    payload = json.dumps(responses, separators=(",", ":")).encode()
    return obligations, hashlib.sha256(payload).hexdigest()


def response_lists(
    n: int, adjacency: list[int], family: set[int], reference: int
) -> dict[int, list[int]]:
    result = {}
    reference_vertices = vertices(reference)
    for outside in range(n):
        outside_bit = 1 << outside
        if reference & outside_bit:
            continue
        response = []
        for anchor in reference_vertices:
            successor = (reference ^ (1 << anchor)) | outside_bit
            if (adjacency[anchor] & outside_bit) and successor in family:
                response.append(anchor)
        if not response:
            raise AssertionError("reference attack has no response")
        result[outside] = response
    return result


def frozen_projections(
    n: int,
    adjacency: list[int],
    reference: int,
    lists: dict[int, list[int]],
) -> dict[int, dict[str, object]]:
    full = (1 << n) - 1
    anchors = vertices(reference)
    result = {}
    for frozen in anchors:
        remaining = [anchor for anchor in anchors if anchor != frozen]
        projected = set(remaining)
        projected.update(
            outside for outside, response in lists.items() if frozen not in response
        )
        parity: dict[int, int] = {}
        component: dict[int, int] = {}
        components: list[list[int]] = []
        for root in sorted(projected):
            if root in parity:
                continue
            index = len(components)
            parity[root] = 0
            component[root] = index
            queue = deque([root])
            members = []
            while queue:
                vertex = queue.popleft()
                members.append(vertex)
                h_scan = (
                    full ^ adjacency[vertex] ^ (1 << vertex)
                ) & sum(1 << item for item in projected)
                while h_scan:
                    bit = h_scan & -h_scan
                    h_scan ^= bit
                    neighbor = bit.bit_length() - 1
                    if neighbor not in parity:
                        parity[neighbor] = parity[vertex] ^ 1
                        component[neighbor] = index
                        queue.append(neighbor)
                    elif parity[neighbor] == parity[vertex]:
                        raise AssertionError("frozen projection is not bipartite")
            components.append(sorted(members))
        anchor_component = component[remaining[0]]
        if component[remaining[1]] != anchor_component:
            raise AssertionError("anchor edge was split across components")
        if parity[remaining[0]] != 0:
            for vertex in components[anchor_component]:
                parity[vertex] ^= 1
        if parity[remaining[0]] != 0 or parity[remaining[1]] != 1:
            raise AssertionError("anchor orientation failed")
        result[frozen] = {
            "remaining": remaining,
            "components": components,
            "component": component,
            "parity": parity,
            "anchor_component": anchor_component,
        }
    return result


def classify_fixed_incidents(
    n: int,
    adjacency: list[int],
    reference: int,
    lists: dict[int, list[int]],
    projections: dict[int, dict[str, object]],
) -> dict[str, object]:
    anchors = set(vertices(reference))
    anchor_singletons = []
    free_singletons = []
    exact_two_rows = []
    for outside, response in sorted(lists.items()):
        if len(response) == 1:
            demanded = response[0]
            for frozen in sorted(anchors - {demanded}):
                data = projections[frozen]
                is_anchor = (
                    data["component"][outside] == data["anchor_component"]
                )
                if is_anchor:
                    aligned = (
                        data["parity"][outside] == data["parity"][demanded]
                    )
                    if not aligned:
                        raise AssertionError("anchor-fixed singleton is misaligned")
                    anchor_singletons.append([outside, frozen, demanded])
                else:
                    free_singletons.append([outside, frozen, demanded])
        elif len(response) == 2:
            omitted = next(iter(anchors - set(response)))
            data = projections[omitted]
            is_anchor = data["component"][outside] == data["anchor_component"]
            if is_anchor:
                raise AssertionError("exact-two vertex lies in anchor component")
            exact_two_rows.append(
                [
                    outside,
                    omitted,
                    data["component"][outside],
                    data["components"][data["component"][outside]],
                ]
            )
        else:
            raise AssertionError("control unexpectedly has a full list")

    full = (1 << n) - 1
    cross_edges = []
    outside_vertices = sorted(lists)
    for left, right in itertools.combinations(outside_vertices, 2):
        if adjacency[left] >> right & 1:
            continue
        if len(lists[left]) != 2 or len(lists[right]) != 2:
            continue
        omitted_left = next(iter(anchors - set(lists[left])))
        omitted_right = next(iter(anchors - set(lists[right])))
        if omitted_left == omitted_right:
            continue
        shared = next(iter(set(lists[left]) & set(lists[right])))
        left_data = projections[omitted_left]
        right_data = projections[omitted_right]
        if (
            left_data["component"][left] == left_data["anchor_component"]
            or right_data["component"][right] == right_data["anchor_component"]
        ):
            raise AssertionError("cross clause has a fixed endpoint")
        cross_edges.append([left, right, shared])

    return {
        "anchor_fixed_singletons": anchor_singletons,
        "free_singletons": free_singletons,
        "exact_two_free_components": exact_two_rows,
        "cross_type_edges": cross_edges,
    }


def response_coloring_count(
    n: int,
    adjacency: list[int],
    reference: int,
    lists: dict[int, list[int]],
) -> int:
    anchors = vertices(reference)
    coloring = {anchor: anchor for anchor in anchors}
    outside = sorted(lists, key=lambda v: (len(lists[v]), v))
    count = 0

    def visit(index: int) -> None:
        nonlocal count
        if index == len(outside):
            count += 1
            return
        vertex = outside[index]
        for color in lists[vertex]:
            conflict = False
            for other, other_color in coloring.items():
                if other_color != color:
                    continue
                if not (adjacency[vertex] >> other) & 1:
                    conflict = True
                    break
            if conflict:
                continue
            coloring[vertex] = color
            visit(index + 1)
            del coloring[vertex]

    visit(0)
    return count


def connected(n: int, adjacency: list[int]) -> bool:
    seen = 1
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        scan = adjacency[vertex] & ~seen
        while scan:
            bit = scan & -scan
            scan ^= bit
            seen |= bit
            queue.append(bit.bit_length() - 1)
    return seen == (1 << n) - 1


def audit_case(name: str, data: dict[str, object]) -> dict[str, object]:
    n, adjacency = decode_graph6(str(data["graph6"]))
    edge_count = sum(mask.bit_count() for mask in adjacency) // 2
    if n != data["expected_order"] or edge_count != data["expected_size"]:
        raise AssertionError(f"{name}: graph order/size mismatch")

    family, deletion_rounds = greatest_family(n, adjacency, 3)
    obligations, response_hash = verify_family(n, adjacency, family)
    reference = sum(1 << vertex for vertex in data["reference"])
    if reference not in family or not independent(reference, adjacency):
        raise AssertionError(f"{name}: reference is not an independent family state")
    lists = response_lists(n, adjacency, family, reference)
    expected_lists = {
        int(vertex): response
        for vertex, response in data["expected_lists"].items()
    }
    if lists != expected_lists:
        raise AssertionError(f"{name}: response lists differ")

    parameters = {
        "gamma": domination_number(n, adjacency),
        "i": independent_domination_number(n, adjacency),
        "alpha": independence_number(n, adjacency),
        "gamma_infinity": eternal_domination_number(n, adjacency),
        "theta": theta_number(n, adjacency),
    }
    if parameters != data["expected_parameters"]:
        raise AssertionError(f"{name}: parameter mismatch {parameters}")
    if len(family) != data["expected_family_size"]:
        raise AssertionError(f"{name}: family size mismatch")
    if obligations != data["expected_obligations"]:
        raise AssertionError(f"{name}: obligation count mismatch")

    projections = frozen_projections(n, adjacency, reference, lists)
    classification = classify_fixed_incidents(
        n, adjacency, reference, lists, projections
    )
    if "expected_anchor_fixed_singleton_incidences" in data:
        if (
            len(classification["anchor_fixed_singletons"])
            != data["expected_anchor_fixed_singleton_incidences"]
        ):
            raise AssertionError(f"{name}: anchor incidence count mismatch")
    if name == "free_exact_two_cross_clauses":
        if not classification["cross_type_edges"]:
            raise AssertionError("cross-clause control has no cross-type edge")

    coloring_count = response_coloring_count(n, adjacency, reference, lists)
    if coloring_count != data["expected_response_coloring_count"]:
        raise AssertionError(f"{name}: response coloring count mismatch")

    family_payload = json.dumps(
        [vertices(state) for state in sorted(family)], separators=(",", ":")
    ).encode()
    return {
        "graph6": data["graph6"],
        "order": n,
        "size": edge_count,
        "connected": connected(n, adjacency),
        "parameters": parameters,
        "family_size": len(family),
        "deletion_rounds": deletion_rounds,
        "obligations": obligations,
        "family_sha256": hashlib.sha256(family_payload).hexdigest(),
        "response_certificate_sha256": response_hash,
        "lists": {str(vertex): response for vertex, response in lists.items()},
        "anchor_fixed_singleton_incidences": len(
            classification["anchor_fixed_singletons"]
        ),
        "free_singleton_incidences": len(classification["free_singletons"]),
        "exact_two_free_vertices": len(
            classification["exact_two_free_components"]
        ),
        "cross_type_edges": classification["cross_type_edges"],
        "response_coloring_count": coloring_count,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", required=True, type=Path)
    args = parser.parse_args()
    controls = json.loads(args.check.read_text())
    result = {
        "schema": "singleton-fixed-certificates-verification-v1",
        "model": controls["standard_model"],
        "cases": {},
    }
    for name in ("anchor_fixed_singletons", "free_exact_two_cross_clauses"):
        result["cases"][name] = audit_case(name, controls[name])
    result["verdict"] = "PASS"
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
