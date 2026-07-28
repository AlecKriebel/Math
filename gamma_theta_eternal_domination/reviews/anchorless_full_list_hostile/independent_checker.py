#!/usr/bin/env python3
"""Clean-room checks for the anchorless full-list structural note.

This file deliberately imports no campaign or candidate evaluator.  Graphs
are integer adjacency masks, configurations are integer masks, and the
one-guard greatest fixed point is reconstructed directly from the definition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CANDIDATE = CAMPAIGN / "math/working/anchorless_full_list_structure"
CANDIDATE_MANIFEST_SHA = (
    "d8f26d91e58f28289c4b38aafe6ca6f0a543b127822991a403ffdd2ae36a7033"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def masks_of_size(n: int, size: int):
    for selection in itertools.combinations(range(n), size):
        mask = 0
        for vertex in selection:
            mask |= 1 << vertex
        yield mask


def decode_graph6(record: str) -> tuple[int, ...]:
    """Decode the short graph6 form without using a graph library."""

    payload = record.encode("ascii")
    assert payload and payload[0] != 126
    n = payload[0] - 63
    needed = n * (n - 1) // 2
    assert len(payload) == 1 + (needed + 5) // 6
    stream: list[int] = []
    for byte in payload[1:]:
        value = byte - 63
        assert 0 <= value < 64
        stream.extend((value >> shift) & 1 for shift in (5, 4, 3, 2, 1, 0))
    assert not any(stream[needed:])
    rows = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if stream[cursor]:
                rows[high] |= 1 << low
                rows[low] |= 1 << high
            cursor += 1
    return tuple(rows)


def complement(graph: tuple[int, ...]) -> tuple[int, ...]:
    universe = (1 << len(graph)) - 1
    return tuple(
        universe & ~(graph[vertex] | (1 << vertex))
        for vertex in range(len(graph))
    )


def independent(graph: tuple[int, ...], state: int) -> bool:
    return all(not (graph[v] & (state ^ (1 << v))) for v in bits(state))


def dominates(graph: tuple[int, ...], state: int) -> bool:
    covered = state
    for guard in bits(state):
        covered |= graph[guard]
    return covered == (1 << len(graph)) - 1


def domination_number(graph: tuple[int, ...]) -> int:
    for size in range(1, len(graph) + 1):
        if any(dominates(graph, state) for state in masks_of_size(len(graph), size)):
            return size
    raise AssertionError


def independence_number(graph: tuple[int, ...]) -> int:
    for size in range(len(graph), 0, -1):
        if any(
            independent(graph, state)
            for state in masks_of_size(len(graph), size)
        ):
            return size
    return 0


def independent_domination_number(graph: tuple[int, ...]) -> int:
    for size in range(1, len(graph) + 1):
        if any(
            independent(graph, state) and dominates(graph, state)
            for state in masks_of_size(len(graph), size)
        ):
            return size
    raise AssertionError


def colorable(graph: tuple[int, ...], color_count: int) -> bool:
    assigned = [-1] * len(graph)
    degrees = [row.bit_count() for row in graph]

    def visit(done: int) -> bool:
        if done == len(graph):
            return True
        candidates = []
        for vertex in range(len(graph)):
            if assigned[vertex] >= 0:
                continue
            forbidden = {
                assigned[other]
                for other in bits(graph[vertex])
                if assigned[other] >= 0
            }
            candidates.append(
                (len(forbidden), degrees[vertex], vertex, forbidden)
            )
        _, _, vertex, forbidden = max(candidates)
        for color in range(color_count):
            if color in forbidden:
                continue
            assigned[vertex] = color
            if visit(done + 1):
                return True
            assigned[vertex] = -1
        return False

    return visit(0)


def chromatic_number(graph: tuple[int, ...]) -> int:
    for count in range(1, len(graph) + 1):
        if colorable(graph, count):
            return count
    raise AssertionError


def greatest_kernel(graph: tuple[int, ...], size: int) -> set[int]:
    """Synchronous greatest-fixed-point deletion in the one-guard model."""

    family = {
        state
        for state in masks_of_size(len(graph), size)
        if dominates(graph, state)
    }
    while True:
        doomed = set()
        for state in family:
            for attack in range(len(graph)):
                attack_bit = 1 << attack
                if state & attack_bit:
                    continue
                if not any(
                    graph[guard] & attack_bit
                    and ((state ^ (1 << guard)) | attack_bit) in family
                    for guard in bits(state)
                ):
                    doomed.add(state)
                    break
        if not doomed:
            return family
        family -= doomed


def eternal_number(graph: tuple[int, ...]) -> int:
    for size in range(1, len(graph) + 1):
        if greatest_kernel(graph, size):
            return size
    raise AssertionError


def delete_vertex(graph: tuple[int, ...], deleted: int) -> tuple[int, ...]:
    keep = [v for v in range(len(graph)) if v != deleted]
    new_index = {old: new for new, old in enumerate(keep)}
    rows = []
    for old in keep:
        row = 0
        for neighbor in bits(graph[old]):
            if neighbor in new_index:
                row |= 1 << new_index[neighbor]
        rows.append(row)
    return tuple(rows)


def link_components(
    link: tuple[int, ...], subset: set[int]
) -> list[tuple[list[int], list[int]]]:
    unseen = set(subset)
    answer = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        parity = {start: 0}
        while queue:
            vertex = queue.popleft()
            for neighbor in bits(link[vertex]):
                if neighbor not in subset:
                    continue
                if neighbor in parity:
                    assert parity[neighbor] != parity[vertex]
                    continue
                parity[neighbor] = 1 - parity[vertex]
                unseen.remove(neighbor)
                queue.append(neighbor)
        answer.append(
            (
                sorted(v for v, side in parity.items() if side == 0),
                sorted(v for v, side in parity.items() if side == 1),
            )
        )
    return sorted(answer)


def mask(vertices: tuple[int, ...] | list[int] | set[int]) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


def response_guards(
    graph: tuple[int, ...], family: set[int], state: int, attack: int
) -> list[int]:
    assert not (state & (1 << attack))
    return [
        guard
        for guard in bits(state)
        if graph[guard] & (1 << attack)
        and ((state ^ (1 << guard)) | (1 << attack)) in family
    ]


def parameters(graph: tuple[int, ...]) -> list[int]:
    return [
        domination_number(graph),
        independent_domination_number(graph),
        independence_number(graph),
        eternal_number(graph),
        chromatic_number(complement(graph)),
    ]


def inspect_full_root(
    graph6: str, root: tuple[int, int, int], target: int
) -> dict[str, object]:
    graph = decode_graph6(graph6)
    link = complement(graph)
    family = greatest_kernel(graph, 3)
    root_mask = mask(root)
    assert independent(graph, root_mask)
    assert root_mask in family
    assert target not in root
    assert all(graph[target] & (1 << anchor) for anchor in root)
    assert all(
        (root_mask ^ (1 << anchor)) | (1 << target) in family
        for anchor in root
    )

    physical = set(bits(link[target]))
    spokes = {
        anchor: {b for b in physical if link[anchor] & (1 << b)}
        for anchor in root
    }
    palettes = {
        b: {
            anchor
            for anchor in root
            if mask((target, anchor, b)) in family
        }
        for b in physical
    }
    anchorless = sorted(
        b for b in physical if not any(b in spokes[a] for a in root)
    )

    component_records = []
    for side_zero, side_one in link_components(link, physical):
        sides = (side_zero, side_one)
        assert all(
            any(link[v] & (1 << w) for w in physical)
            for side in sides
            for v in side
        )
        side_palettes = []
        side_spokes = []
        for side in sides:
            palette_values = {tuple(sorted(palettes[v])) for v in side}
            assert len(palette_values) == 1
            palette = next(iter(palette_values))
            assert len(palette) >= 2
            side_palettes.append(list(palette))
            met = sorted(a for a in root if any(v in spokes[a] for v in side))
            assert len(met) <= 1
            side_spokes.append(met)

        # Reconstruct the exact palette identities in Corollary 2.2.
        for side_index, met in enumerate(side_spokes):
            if not met:
                continue
            anchor = met[0]
            assert anchor in side_palettes[side_index]
            assert set(side_palettes[1 - side_index]) == set(root) - {anchor}
        if side_spokes[0] and side_spokes[1]:
            assert side_spokes[0][0] != side_spokes[1][0]
            assert set(side_palettes[0]) == set(root) - {side_spokes[1][0]}
            assert set(side_palettes[1]) == set(root) - {side_spokes[0][0]}

        edge_count = 0
        reverse_checks = 0
        role_signatures = {anchor: set() for anchor in root}
        for b in side_zero:
            for c in side_one:
                if not (link[b] & (1 << c)):
                    continue
                edge_count += 1
                triple = mask((target, b, c))
                assert independent(graph, triple)
                assert triple in family
                for anchor in root:
                    responders = set(
                        response_guards(graph, family, triple, anchor)
                    )
                    # This is the exact bridge between C-073 roles and P.
                    assert (c in responders) == (anchor in palettes[b])
                    assert (b in responders) == (anchor in palettes[c])
                    roles = (
                        target in responders,
                        b in responders,
                        c in responders,
                    )
                    role_signatures[anchor].add(roles)
                    if anchor not in palettes[b] and anchor not in palettes[c]:
                        assert responders == {target}
                        assert mask((anchor, b, c)) in family
                        reverse_checks += 1
        assert edge_count
        # Constancy is read with the fixed X/U/V side roles.
        assert all(len(signatures) == 1 for signatures in role_signatures.values())
        component_records.append(
            {
                "sides": [side_zero, side_one],
                "side_palettes": side_palettes,
                "side_spokes": side_spokes,
                "edges": edge_count,
                "forced_reverse_checks": reverse_checks,
            }
        )

    obligations = len(family) * (len(graph) - 3)
    for state in family:
        for attack in range(len(graph)):
            if state & (1 << attack):
                continue
            assert response_guards(graph, family, state, attack)

    return {
        "graph6": graph6,
        "root": list(root),
        "target": target,
        "parameters": parameters(graph),
        "greatest_family_size": len(family),
        "attack_obligations": obligations,
        "physical_link": sorted(physical),
        "spokes": {str(a): sorted(spokes[a]) for a in root},
        "anchorless": anchorless,
        "palettes": {str(b): sorted(palettes[b]) for b in sorted(physical)},
        "components": component_records,
        "deletion_gamma": domination_number(delete_vertex(graph, target)),
    }


def symbolic_component_audit() -> dict[str, object]:
    """Exhaust the palette/spoke combinatorics used after uniformity."""

    palettes = [p for p in range(8) if p.bit_count() >= 2]
    legal_patterns = 0
    for palette_u in palettes:
        for palette_v in palettes:
            for spoke_u in range(8):
                for spoke_v in range(8):
                    constraints = all(
                        palette_u & (1 << q) and not (palette_v & (1 << q))
                        for q in bits(spoke_u)
                    ) and all(
                        palette_v & (1 << q) and not (palette_u & (1 << q))
                        for q in bits(spoke_v)
                    )
                    if not constraints:
                        continue
                    legal_patterns += 1
                    assert spoke_u.bit_count() <= 1
                    assert spoke_v.bit_count() <= 1
                    if spoke_u and spoke_v:
                        q = next(bits(spoke_u))
                        r = next(bits(spoke_v))
                        assert q != r
                        assert palette_u == (0b111 ^ (1 << r))
                        assert palette_v == (0b111 ^ (1 << q))
                    if spoke_u:
                        q = next(bits(spoke_u))
                        assert palette_v == (0b111 ^ (1 << q))
                    if spoke_v:
                        r = next(bits(spoke_v))
                        assert palette_u == (0b111 ^ (1 << r))

    # A layer vertex can cover at most two palette indices.  Exhaust all
    # finite covers by at most three abstract layer vertices.
    minimum_union = {}
    allowed_memberships = [m for m in range(1, 8) if m != 0b111]
    for palette_size, target in ((2, 0b011), (3, 0b111)):
        best = None
        for count in range(1, 4):
            if any(
                target
                == (lambda chosen: chosen[0] | chosen[1] | chosen[2])(
                    tuple(list(choice) + [0] * (3 - len(choice)))
                )
                for choice in itertools.product(allowed_memberships, repeat=count)
                if all(member & ~target == 0 for member in choice)
            ):
                best = count
                break
        assert best == (1 if palette_size == 2 else 2)
        minimum_union[str(palette_size)] = best

    return {
        "palette_masks_checked": len(palettes),
        "legal_side_spoke_patterns": legal_patterns,
        "maximum_shared_omissions": 1,
        "minimum_external_union_by_palette_size": minimum_union,
    }


def inspect_external_scope_control() -> dict[str, object]:
    """Check the third-attack mechanism on a sharp gamma-two scope control."""

    graph6 = "GCXfVg"
    root = (0, 1, 2)
    target = 7
    anchorless = 6
    graph = decode_graph6(graph6)
    link = complement(graph)
    family = greatest_kernel(graph, 3)
    root_mask = mask(root)
    assert root_mask in family and independent(graph, root_mask)
    assert all(
        (root_mask ^ (1 << anchor)) | (1 << target) in family
        for anchor in root
    )
    assert domination_number(delete_vertex(graph, target)) == 3
    assert link[target] & (1 << anchorless)
    assert all(graph[anchorless] & (1 << anchor) for anchor in root)
    palette = [
        anchor
        for anchor in root
        if mask((target, anchor, anchorless)) in family
    ]
    assert palette == [0, 1, 2]

    layers = {}
    for anchor in palette:
        layer = [
            y
            for y in range(len(graph))
            if y != target
            and link[anchorless] & (1 << y)
            and link[anchor] & (1 << y)
        ]
        assert layer
        assert all(y not in bits(link[target]) for y in layer)
        assert all(graph[target] & (1 << y) for y in layer)
        assert all(mask((anchorless, anchor, y)) in family for y in layer)
        assert all(
            not (link[y] & (1 << z))
            for y, z in itertools.combinations(layer, 2)
        )
        for y in layer:
            source = mask((target, anchor, anchorless))
            assert response_guards(graph, family, source, y) == [target]
        layers[str(anchor)] = layer

    membership = {
        y: sum(y in values for values in layers.values())
        for y in set().union(*(set(values) for values in layers.values()))
    }
    assert max(membership.values()) <= 2
    assert len(membership) == 2

    # This graph deliberately fails gamma(G)>=3 and H[B] no-isolates.  It
    # confirms that neither C-089's count nor C-073's component conclusion
    # may be imported after dropping their hypotheses.
    physical = set(bits(link[target]))
    isolated = [
        b for b in physical if not any(link[b] & (1 << c) for c in physical)
    ]
    assert parameters(graph) == [2, 2, 3, 3, 3]
    assert isolated == [4, 6]
    return {
        "graph6": graph6,
        "root": list(root),
        "target": target,
        "anchorless_vertex": anchorless,
        "parameters": parameters(graph),
        "deletion_gamma": 3,
        "palette": palette,
        "layers": layers,
        "layer_membership_multiplicity": {
            str(y): membership[y] for y in sorted(membership)
        },
        "physical_link_isolates": isolated,
        "scope_warning": (
            "gamma(G)=2, so this checks the literal third-attack mechanism "
            "but not the equality theorem or the C-089 order count"
        ),
    }


def main() -> None:
    assert sha256(CANDIDATE / "MANIFEST.json") == CANDIDATE_MANIFEST_SHA
    candidate_manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    for item in candidate_manifest["files"]:
        assert sha256(CAMPAIGN / item["path"]) == item["sha256"]

    equality = inspect_full_root(r"Ksv`f\knJVis", (1, 2, 3), 0)
    one_spoke = inspect_full_root("EEz_", (0, 1, 2), 4)
    anchorless_only = inspect_full_root("EFz_", (0, 1, 2), 3)

    assert equality["parameters"] == [3, 3, 3, 3, 3]
    assert equality["greatest_family_size"] == 127
    assert equality["physical_link"] == [6, 8, 10, 11]
    assert equality["anchorless"] == []
    assert one_spoke["parameters"] == [2, 2, 3, 3, 3]
    assert one_spoke["greatest_family_size"] == 18
    assert one_spoke["anchorless"] == [5]
    assert anchorless_only["parameters"] == [2, 3, 3, 3, 3]
    assert anchorless_only["greatest_family_size"] == 20
    assert anchorless_only["anchorless"] == [4, 5]

    result = {
        "schema": "anchorless-full-list-hostile-result-v1",
        "candidate_manifest": {
            "sha256": CANDIDATE_MANIFEST_SHA,
            "all_listed_hashes_match": True,
        },
        "model": {
            "attacks_only_unoccupied": True,
            "exactly_one_guard_moves": True,
            "moves_use_G_edges": True,
            "every_successor_is_in_the_same_family": True,
            "H_is_complement_of_G": True,
        },
        "symbolic_audit": symbolic_component_audit(),
        "controls": [equality, one_spoke, anchorless_only],
        "third_attack_scope_control": inspect_external_scope_control(),
        "claim_status": {
            "component_side_palette_uniformity": "PASS",
            "zero_one_two_spoke_classification": "PASS",
            "shared_omission_reverse_state": "PASS",
            "deletion_critical_external_clique_layer": "PASS",
            "external_layer_multiplicity": "PASS",
            "conditional_n_at_least_anchorless_plus_10": "PASS",
            "order10_census": "OBSERVED_ONLY_NOT_REPLAYED",
            "toggle_probe": "OBSERVED_ONLY_NOT_REPLAYED",
            "anchorless_vertices_eliminated": False,
            "full_list_branch_closed": False,
            "complete_k3": False,
            "universal_conjecture_resolved": False,
        },
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = HERE / "result.json"
    path.write_text(encoded)
    print(encoded, end="")
    print(f"sha256 {hashlib.sha256(encoded.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
