#!/usr/bin/env python3
"""Clean-room hostile checks for the inactive odd-cycle induction.

This program deliberately imports no candidate code.  It performs:

1. a direct monotone one-guard deletion audit for every equality pattern
   among the witnesses of odd paths through length seven;
2. distinct-witness even-path controls;
3. an exhaustive small-graph audit of the adjacent-true-twin family lift;
4. frozen-source integrity checks.

The finite checks support, but do not replace, the all-length human proof
audited in REVIEW.md.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "math" / "working" / "inactive_odd_cycle_induction"

EXPECTED_HASHES = {
    "NOTE.md": "ca8f655573575fefc1eb6e343950658c970e638aa66c62015647c784699a8d02",
    "verify_induction.py": "a0bec0c32de355ca7a8cf9dab01d0e2b6c0cb879084bad70f54d0e78884e277e",
    "independent_result.json": "83b81b9bfd94044bc8cd7b0cf8f9fccd613370c760bc91509d755d2b03d8e458",
    "dead_state_saturation.py": "2f34182a0c1219f65459c2e814e27651f0bd5bf1b7da82541b2bae93db70b47d",
    "RESEARCH_LOG.md": "22d146d5836009594b9ecd13a48c11959af186b2b6f6c151581c8acd23c833c0",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def partitions(length: int):
    """Yield all restricted-growth strings of the requested length."""

    if length == 0:
        yield ()
        return

    def extend(prefix: tuple[int, ...]):
        if len(prefix) == length:
            yield prefix
            return
        for label in range(max(prefix) + 2):
            yield from extend(prefix + (label,))

    yield from extend((0,))


def three_sets(order: int) -> tuple[list[int], dict[int, int]]:
    states = [
        (1 << a) | (1 << b) | (1 << c)
        for a, b, c in itertools.combinations(range(order), 3)
    ]
    return states, {mask: index for index, mask in enumerate(states)}


def path_template(
    path_length: int, pattern: tuple[int, ...]
) -> tuple[int, list[int], list[int], int, set[tuple[int, int]]]:
    """Return order, named states, boundary states, endpoint, nonedges."""

    if len(pattern) != path_length:
        raise ValueError("pattern length mismatch")
    block_count = max(pattern) + 1
    witness_start = path_length + 1
    target = witness_start + block_count
    order = target + 1
    named: list[int] = []
    boundary: list[int] = []
    nonedges: set[tuple[int, int]] = set()
    for index, block in enumerate(pattern):
        left = index
        right = index + 1
        witness = witness_start + block
        named.append((1 << left) | (1 << right) | (1 << witness))
        boundary.extend(
            [
                (1 << left) | (1 << witness) | (1 << target),
                (1 << right) | (1 << witness) | (1 << target),
            ]
        )
        for first, second in (
            (left, right),
            (left, witness),
            (right, witness),
        ):
            nonedges.add(tuple(sorted((first, second))))
    endpoint = (1 << 0) | (1 << path_length) | (1 << target)
    return order, named, boundary, endpoint, nonedges


def dead_closure(
    order: int,
    initial_dead_masks: set[int],
    forced_nonedges: set[tuple[int, int]],
) -> set[int]:
    """Greatest-family deletion under local unoccupied one-guard attacks.

    Every unspecified edge is treated optimistically as present.  Thus a
    state deleted here is absent in every completion and every eternal
    subfamily satisfying the initial absences.
    """

    states, index = three_sets(order)
    dead = [False] * len(states)
    queue: deque[int] = deque()
    for mask in initial_dead_masks:
        position = index[mask]
        if not dead[position]:
            dead[position] = True
            queue.append(position)

    sources: list[int] = []
    remaining: list[int] = []
    reverse: list[list[int]] = [[] for _ in states]

    for source_index, current in enumerate(states):
        for attacked in range(order):
            if current & (1 << attacked):
                continue
            successors: list[int] = []
            guards = [
                vertex
                for vertex in range(order)
                if current & (1 << vertex)
            ]
            for guard in guards:
                if tuple(sorted((guard, attacked))) in forced_nonedges:
                    continue
                successor = (current ^ (1 << guard)) | (1 << attacked)
                successors.append(index[successor])
            obligation = len(sources)
            sources.append(source_index)
            live_count = sum(not dead[item] for item in successors)
            remaining.append(live_count)
            for successor_index in successors:
                if not dead[successor_index]:
                    reverse[successor_index].append(obligation)
            if live_count == 0 and not dead[source_index]:
                dead[source_index] = True
                queue.append(source_index)

    # Initial dead states were excluded from reverse lists above.  This is
    # intentional: their contribution was already removed in live_count.
    while queue:
        newly_dead = queue.popleft()
        for obligation in reverse[newly_dead]:
            if remaining[obligation] == 0:
                continue
            remaining[obligation] -= 1
            if remaining[obligation] == 0:
                source = sources[obligation]
                if not dead[source]:
                    dead[source] = True
                    queue.append(source)

    return {states[position] for position, value in enumerate(dead) if value}


def audit_collision_patterns() -> dict[str, object]:
    results: list[dict[str, int]] = []
    total_patterns = 0
    vacuous_patterns = 0
    for length in (1, 3, 5, 7):
        length_patterns = 0
        length_vacuous = 0
        for pattern in partitions(length):
            length_patterns += 1
            (
                order,
                named,
                boundary,
                endpoint,
                nonedges,
            ) = path_template(length, pattern)
            support_dead = dead_closure(order, set(boundary), nonedges)
            if any(item in support_dead for item in named):
                length_vacuous += 1
                continue
            contradiction_dead = dead_closure(
                order, set(boundary) | {endpoint}, nonedges
            )
            if not all(item in contradiction_dead for item in named):
                raise AssertionError(
                    f"odd-path survivor: length={length}, pattern={pattern}"
                )
        total_patterns += length_patterns
        vacuous_patterns += length_vacuous
        results.append(
            {
                "path_length": length,
                "partition_count": length_patterns,
                "boundary_already_deletes_named_count": length_vacuous,
                "boundary_consistent_endpoint_forced_count": (
                    length_patterns - length_vacuous
                ),
            }
        )
    if total_patterns != 1 + 5 + 52 + 877:
        raise AssertionError("unexpected Bell-number total")
    return {
        "odd_path_results": results,
        "total_partitions": total_patterns,
        "boundary_already_deletes_named_count": vacuous_patterns,
        "boundary_consistent_endpoint_forced_count": (
            total_patterns - vacuous_patterns
        ),
    }


def is_dominating(order: int, edges: set[tuple[int, int]], state: int) -> bool:
    for attacked in range(order):
        if state & (1 << attacked):
            continue
        if not any(
            state & (1 << guard)
            and tuple(sorted((guard, attacked))) in edges
            for guard in range(order)
        ):
            return False
    return True


def is_eternal_family(
    order: int, edges: set[tuple[int, int]], family: set[int]
) -> bool:
    if not family:
        return False
    if any(not is_dominating(order, edges, state) for state in family):
        return False
    for state in family:
        for attacked in range(order):
            if state & (1 << attacked):
                continue
            legal = False
            for guard in range(order):
                if not (state & (1 << guard)):
                    continue
                if tuple(sorted((guard, attacked))) not in edges:
                    continue
                successor = (state ^ (1 << guard)) | (1 << attacked)
                if successor in family:
                    legal = True
                    break
            if not legal:
                return False
    return True


def blow_up_once(
    order: int,
    edges: set[tuple[int, int]],
    family: set[int],
    cloned: int,
) -> tuple[int, set[tuple[int, int]], set[int]]:
    """Replace one vertex by two adjacent true twins and lift the family."""

    clone = order
    new_edges = set(edges)
    new_edges.add(tuple(sorted((cloned, clone))))
    for other in range(order):
        if other == cloned:
            continue
        if tuple(sorted((cloned, other))) in edges:
            new_edges.add(tuple(sorted((clone, other))))
    lifted: set[int] = set()
    for state in family:
        lifted.add(state)
        if state & (1 << cloned):
            lifted.add((state ^ (1 << cloned)) | (1 << clone))
    return order + 1, new_edges, lifted


def audit_twin_lift() -> dict[str, int]:
    order = 4
    possible_edges = list(itertools.combinations(range(order), 2))
    states, _ = three_sets(order)
    graph_count = 0
    family_count = 0
    lift_count = 0
    for graph_bits in range(1 << len(possible_edges)):
        graph_count += 1
        edges = {
            possible_edges[index]
            for index in range(len(possible_edges))
            if graph_bits & (1 << index)
        }
        for family_bits in range(1, 1 << len(states)):
            family = {
                states[index]
                for index in range(len(states))
                if family_bits & (1 << index)
            }
            if not is_eternal_family(order, edges, family):
                continue
            family_count += 1
            for cloned in range(order):
                (
                    lifted_order,
                    lifted_edges,
                    lifted_family,
                ) = blow_up_once(order, edges, family, cloned)
                if not is_eternal_family(
                    lifted_order, lifted_edges, lifted_family
                ):
                    raise AssertionError(
                        "adjacent-true-twin lift failed: "
                        f"graph_bits={graph_bits}, family_bits={family_bits}, "
                        f"cloned={cloned}"
                    )
                lift_count += 1
    return {
        "labeled_graph_count": graph_count,
        "eternal_triple_family_count": family_count,
        "verified_single_vertex_lifts": lift_count,
    }


def audit_even_controls() -> list[dict[str, int]]:
    results: list[dict[str, int]] = []
    for length in (2, 4, 6, 8):
        pattern = tuple(range(length))
        order, named, boundary, endpoint, nonedges = path_template(
            length, pattern
        )
        dead = dead_closure(order, set(boundary) | {endpoint}, nonedges)
        if any(item in dead for item in named):
            raise AssertionError(f"even control died at length {length}")
        results.append(
            {
                "path_length": length,
                "order": order,
                "surviving_named_states": len(named),
            }
        )
    return results


def main() -> None:
    integrity = {
        filename: sha256(CANDIDATE / filename)
        for filename in EXPECTED_HASHES
    }
    if integrity != EXPECTED_HASHES:
        raise AssertionError(
            f"candidate integrity mismatch: {integrity!r}"
        )

    payload = {
        "schema": "inactive-odd-cycle-hostile-audit-v1",
        "classification": "UNCONDITIONAL-PASS-SUPPORT",
        "candidate_integrity": integrity,
        "collision_pattern_audit": audit_collision_patterns(),
        "even_controls": audit_even_controls(),
        "true_twin_lift_audit": audit_twin_lift(),
        "semantics": {
            "attacks": "unoccupied vertices only",
            "movement": "exactly one guard along one graph edge",
            "family": "every retained state dominates and is response-closed",
            "unspecified_local_edges": (
                "treated optimistically as present in deletion audit"
            ),
        },
    }
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":")
    ).encode()
    payload["result_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
