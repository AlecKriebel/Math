#!/usr/bin/env python3
"""Clean-room hostile checker for the full-star reverse-color package.

This file imports only the Python standard library.  It does not import the
candidate probe, either campaign verifier, NetworkX, or a SAT solver.

It independently:

* decodes the labeled order-12 control;
* computes gamma, i, alpha, one-guard gamma-infinity, and theta;
* computes the literal greatest eternal triple-family;
* reconstructs the physical complement link, palettes, reverse rows, and
  anchored deletion colorings;
* computes the three restricted greatest kernels from the exact online game;
* scans the complete pinned ``geng -cq`` streams through order nine; and
* replays every labeled edge toggle of radius at most two around the control.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "full_star_reverse_color"
GENG = CAMPAIGN / "tools" / "nauty2_9_3" / "geng"
CONTROL_G6 = r"Ksv`f\knJVis"
CONTROL_ROOT = (1, 2, 3)
CONTROL_TARGET = 0
KNOWN_CONNECTED_COUNTS = (0, 1, 1, 2, 6, 21, 112, 853, 11117, 261080)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def decode_graph6(record: str) -> tuple[int, tuple[int, ...]]:
    """Decode a short graph6 record into symmetric open-neighborhood masks."""

    raw = record.encode("ascii")
    if not raw or raw[0] < 63 or raw[0] > 125:
        raise ValueError("not a short graph6 record")
    order = raw[0] - 63
    if order > 62:
        raise ValueError("only short graph6 is needed in this audit")
    payload_bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 payload byte")
        payload_bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = order * (order - 1) // 2
    if len(payload_bits) < required:
        raise ValueError("truncated graph6 payload")
    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if payload_bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return order, tuple(adjacency)


def encode_graph6(adjacency: tuple[int, ...]) -> str:
    order = len(adjacency)
    if order > 62:
        raise ValueError("only short graph6 is needed in this audit")
    bits = [
        (adjacency[left] >> right) & 1
        for right in range(1, order)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def graph_valid(adjacency: tuple[int, ...]) -> bool:
    order = len(adjacency)
    all_vertices = (1 << order) - 1
    return all(
        not (adjacency[vertex] >> vertex & 1)
        and adjacency[vertex] & ~all_vertices == 0
        and all(
            ((adjacency[vertex] >> other) & 1)
            == ((adjacency[other] >> vertex) & 1)
            for other in range(order)
        )
        for vertex in range(order)
    )


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(adjacency)) - 1
    return tuple(
        all_vertices & ~(1 << vertex) & ~neighbors
        for vertex, neighbors in enumerate(adjacency)
    )


def connected(adjacency: tuple[int, ...]) -> bool:
    if not adjacency:
        return False
    reached = 1
    frontier = 1
    while frontier:
        neighbors = 0
        scan = frontier
        while scan:
            bit = scan & -scan
            scan ^= bit
            neighbors |= adjacency[bit.bit_length() - 1]
        frontier = neighbors & ~reached
        reached |= frontier
    return reached == (1 << len(adjacency)) - 1


@lru_cache(maxsize=None)
def masks_of_size(order: int, size: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << vertex for vertex in values)
        for values in itertools.combinations(range(order), size)
    )


def vertices(mask: int) -> Iterator[int]:
    while mask:
        bit = mask & -mask
        mask ^= bit
        yield bit.bit_length() - 1


def as_vertices(mask: int) -> list[int]:
    return list(vertices(mask))


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    remaining = state
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        if adjacency[bit.bit_length() - 1] & remaining:
            return False
    return True


def dominating(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(dominating(adjacency, state) for state in masks_of_size(len(adjacency), size)):
            return size
    raise AssertionError("the whole vertex set must dominate")


def independence_number(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency), -1, -1):
        if any(independent(adjacency, state) for state in masks_of_size(len(adjacency), size)):
            return size
    return 0


def independent_domination_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if any(
            independent(adjacency, state) and dominating(adjacency, state)
            for state in masks_of_size(len(adjacency), size)
        ):
            return size
    raise AssertionError("a maximal independent set exists")


def k_colorings(
    adjacency: tuple[int, ...],
    colors_count: int,
    fixed: dict[int, int] | None = None,
    omitted: int | None = None,
) -> list[tuple[int, ...]]:
    """Enumerate proper colorings, optionally deleting one vertex."""

    order = len(adjacency)
    colors = [-1] * order
    if omitted is not None:
        colors[omitted] = -2
    for vertex, color in (fixed or {}).items():
        if vertex == omitted or not 0 <= color < colors_count:
            return []
        colors[vertex] = color
    for left in range(order):
        if colors[left] < 0:
            continue
        for right in vertices(adjacency[left]):
            if right > left and colors[right] == colors[left]:
                return []
    answers: list[tuple[int, ...]] = []

    def choose_vertex() -> int | None:
        best = None
        best_key = None
        for vertex in range(order):
            if colors[vertex] != -1:
                continue
            used = {
                colors[other]
                for other in vertices(adjacency[vertex])
                if colors[other] >= 0
            }
            key = (len(used), adjacency[vertex].bit_count(), -vertex)
            if best_key is None or key > best_key:
                best_key = key
                best = vertex
        return best

    def search() -> None:
        vertex = choose_vertex()
        if vertex is None:
            answers.append(tuple(colors))
            return
        forbidden = {
            colors[other]
            for other in vertices(adjacency[vertex])
            if colors[other] >= 0
        }
        for color in range(colors_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            search()
        colors[vertex] = -1

    search()
    return answers


def chromatic_number(adjacency: tuple[int, ...]) -> int:
    for count in range(1, len(adjacency) + 1):
        if k_colorings(adjacency, count):
            return count
    raise AssertionError("n colors always suffice")


def response_successors(
    adjacency: tuple[int, ...],
    state: int,
    attack: int,
    active: set[int],
) -> tuple[int, ...]:
    attack_bit = 1 << attack
    if state & attack_bit:
        raise ValueError("attacks must be unoccupied")
    answers = []
    movers = state & adjacency[attack]
    for guard in vertices(movers):
        successor = state ^ (1 << guard) ^ attack_bit
        if successor in active:
            answers.append(successor)
    return tuple(sorted(answers))


def greatest_kernel(
    adjacency: tuple[int, ...],
    size: int,
    banned: set[int] | None = None,
) -> tuple[set[int], list[int], int, int]:
    """Synchronous greatest-fixed-point deletion from the literal definition."""

    banned = banned or set()
    dominating_states = {
        state
        for state in masks_of_size(len(adjacency), size)
        if dominating(adjacency, state)
    }
    banned_dominating = len(dominating_states & banned)
    active = dominating_states - banned
    initial = len(active)
    rounds: list[int] = []
    while True:
        doomed = set()
        for state in active:
            for attack in range(len(adjacency)):
                if state >> attack & 1:
                    continue
                if not response_successors(adjacency, state, attack, active):
                    doomed.add(state)
                    break
        if not doomed:
            break
        rounds.append(len(doomed))
        active -= doomed
    return active, rounds, initial, banned_dominating


def family_is_eternal(
    adjacency: tuple[int, ...],
    family: set[int],
    size: int,
) -> bool:
    if not family or any(state.bit_count() != size for state in family):
        return False
    if any(not dominating(adjacency, state) for state in family):
        return False
    for state in family:
        for attack in range(len(adjacency)):
            if state >> attack & 1:
                continue
            if not response_successors(adjacency, state, attack, family):
                return False
    return True


def eternal_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        family, _rounds, _initial, _banned = greatest_kernel(adjacency, size)
        if family:
            return size
    raise AssertionError("the all-vertex state is eternal")


def edge_list(adjacency: tuple[int, ...]) -> list[list[int]]:
    return [
        [left, right]
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left] >> right & 1
    ]


def response_guards(
    adjacency: tuple[int, ...],
    family: set[int],
    state: int,
    attack: int,
) -> set[int]:
    if state >> attack & 1:
        raise ValueError("attack is occupied")
    result = set()
    for guard in vertices(state & adjacency[attack]):
        if state ^ (1 << guard) ^ (1 << attack) in family:
            result.add(guard)
    return result


def control_audit() -> dict[str, object]:
    order, graph = decode_graph6(CONTROL_G6)
    if not graph_valid(graph) or encode_graph6(graph) != CONTROL_G6:
        raise AssertionError("graph6 decoder/encoder round trip failed")
    opposite = complement(graph)
    root_mask = sum(1 << vertex for vertex in CONTROL_ROOT)
    target_bit = 1 << CONTROL_TARGET
    greatest, greatest_rounds, greatest_initial, _ = greatest_kernel(graph, 3)
    parameters = {
        "gamma": domination_number(graph),
        "i": independent_domination_number(graph),
        "alpha": independence_number(graph),
        "gamma_infinity": eternal_number(graph),
        "theta": chromatic_number(opposite),
    }
    if parameters != {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(parameters)
    if not family_is_eternal(graph, greatest, 3):
        raise AssertionError("computed greatest family is not eternal")
    if len(greatest) != 127:
        raise AssertionError(len(greatest))
    if not independent(graph, root_mask) or root_mask not in greatest:
        raise AssertionError("root is not a retained maximum independent set")

    selected_states: dict[str, list[int]] = {}
    for color, anchor in enumerate(CONTROL_ROOT):
        successor = root_mask ^ (1 << anchor) ^ target_bit
        if not (graph[anchor] & target_bit) or successor not in greatest:
            raise AssertionError("target is not full")
        selected_states[str(color)] = as_vertices(successor)

    physical_mask = opposite[CONTROL_TARGET]
    physical = as_vertices(physical_mask)
    link_edges = [
        (left, right)
        for left, right in itertools.combinations(physical, 2)
        if opposite[left] >> right & 1
    ]
    if physical != [6, 8, 10, 11] or link_edges != [(6, 8), (10, 11)]:
        raise AssertionError((physical, link_edges))

    palettes = {
        str(vertex): [
            color
            for color, anchor in enumerate(CONTROL_ROOT)
            if target_bit | (1 << anchor) | (1 << vertex) in greatest
        ]
        for vertex in physical
    }
    reverse_by_edge: dict[str, list[int]] = {}
    response_rows: dict[str, dict[str, dict[str, list[int]]]] = {}
    hall_unions: dict[str, list[int]] = {}
    for left, right in link_edges:
        edge_key = f"{left}-{right}"
        state = target_bit | (1 << left) | (1 << right)
        if not independent(graph, state) or state not in greatest:
            raise AssertionError("physical-link edge state is not retained")
        reverse_by_edge[edge_key] = [
            color
            for color, anchor in enumerate(CONTROL_ROOT)
            if (1 << anchor) | (1 << left) | (1 << right) in greatest
        ]
        rows = {}
        union = set()
        for color, anchor in enumerate(CONTROL_ROOT):
            actual = response_guards(graph, greatest, state, anchor)
            expected = set()
            if color in reverse_by_edge[edge_key]:
                expected.add(CONTROL_TARGET)
            if color in palettes[str(right)]:
                expected.add(left)
            if color in palettes[str(left)]:
                expected.add(right)
            if actual != expected:
                raise AssertionError((edge_key, color, actual, expected))
            union |= actual
            rows[str(color)] = {
                "actual_guard_positions": sorted(actual),
                "formula_guard_positions": sorted(expected),
            }
        if union != {CONTROL_TARGET, left, right}:
            raise AssertionError(("Hall union misses a guard role", edge_key, union))
        response_rows[edge_key] = rows
        hall_unions[edge_key] = sorted(union)

    reverse_sets = {tuple(value) for value in reverse_by_edge.values()}
    if reverse_sets != {(0, 1, 2)}:
        raise AssertionError(reverse_sets)
    reverse_global = list(next(iter(reverse_sets)))

    fixed = {anchor: color for color, anchor in enumerate(CONTROL_ROOT)}
    deletion_colorings = sorted(
        k_colorings(opposite, 3, fixed=fixed, omitted=CONTROL_TARGET)
    )
    feasible = [
        color
        for color in range(3)
        if any(
            all(coloring[vertex] != color for vertex in physical)
            for coloring in deletion_colorings
        )
    ]
    normalized_colorings = [
        [None if value == -2 else value for value in coloring]
        for coloring in deletion_colorings
    ]
    if normalized_colorings != [
        [None, 0, 1, 2, 0, 1, 2, 0, 1, 1, 0, 2],
        [None, 0, 1, 2, 2, 0, 1, 1, 0, 2, 1, 0],
    ]:
        raise AssertionError(normalized_colorings)
    if feasible != [2]:
        raise AssertionError(feasible)

    restricted: dict[str, object] = {}
    safe_colors = []
    for color, anchor in enumerate(CONTROL_ROOT):
        banned = {
            root_mask ^ (1 << anchor) ^ (1 << vertex)
            for vertex in physical
        }
        kernel, rounds, initial, banned_dominating = greatest_kernel(
            graph, 3, banned
        )
        selected = root_mask ^ (1 << anchor) ^ target_bit
        safe = root_mask in kernel and selected in kernel
        if safe:
            safe_colors.append(color)
        closure = family_is_eternal(graph, kernel, 3) if kernel else True
        if not closure or kernel & banned:
            raise AssertionError("restricted fixed point is invalid")
        restricted[str(color)] = {
            "banned_root_swap_states": [
                as_vertices(state) for state in sorted(banned)
            ],
            "banned_states_count": len(banned),
            "banned_dominating_states": banned_dominating,
            "initial_allowed_dominating_states": initial,
            "deletion_rounds": rounds,
            "kernel_states": len(kernel),
            "root_survives": root_mask in kernel,
            "selected_target_state_survives": selected in kernel,
            "safe": safe,
            "fixed_point_eternal_if_nonempty": closure,
        }
    if safe_colors != [2]:
        raise AssertionError(safe_colors)

    feasible_coloring = next(
        coloring
        for coloring in deletion_colorings
        if all(coloring[vertex] != 2 for vertex in physical)
    )
    extended = list(feasible_coloring)
    extended[CONTROL_TARGET] = 2
    color_classes = [
        [vertex for vertex, color in enumerate(extended) if color == index]
        for index in range(3)
    ]
    fiber_family = {
        sum(1 << vertex for vertex in choice)
        for choice in itertools.product(*color_classes)
    }
    kernel_two, _rounds, _initial, _banned = greatest_kernel(
        graph,
        3,
        {
            root_mask ^ (1 << CONTROL_ROOT[2]) ^ (1 << vertex)
            for vertex in physical
        },
    )
    if not family_is_eternal(graph, fiber_family, 3):
        raise AssertionError("clique-fiber family is not eternal")
    if fiber_family != kernel_two:
        raise AssertionError("safe restricted kernel differs from clique fibers")

    return {
        "graph6_labeled": CONTROL_G6,
        "order": order,
        "size": len(edge_list(graph)),
        "edge_list": edge_list(graph),
        "parameters": parameters,
        "dominating_triples_initial": greatest_initial,
        "greatest_family_deletion_rounds": greatest_rounds,
        "greatest_family_states": len(greatest),
        "root": list(CONTROL_ROOT),
        "target": CONTROL_TARGET,
        "full_target_successors": selected_states,
        "physical_link_vertices": physical,
        "physical_link_edges": [list(edge) for edge in link_edges],
        "palettes": palettes,
        "reverse_colors_by_edge": reverse_by_edge,
        "global_reverse_colors": reverse_global,
        "exact_response_rows": response_rows,
        "family_response_hall_unions": hall_unions,
        "anchored_deletion_colorings": normalized_colorings,
        "feasible_target_colors": feasible,
        "restricted_kernels": restricted,
        "safe_colors": safe_colors,
        "safe_color_clique_fibers": {
            "color": 2,
            "color_classes": color_classes,
            "states": len(fiber_family),
            "equals_restricted_kernel": True,
        },
    }


def alpha_gamma_three(
    adjacency: tuple[int, ...],
) -> tuple[bool, tuple[int, ...]]:
    order = len(adjacency)
    independent_triples = tuple(
        state
        for state in masks_of_size(order, 3)
        if independent(adjacency, state)
    )
    if not independent_triples:
        return False, ()
    if any(
        independent(adjacency, state)
        for state in masks_of_size(order, 4)
    ):
        return False, ()
    if any(
        dominating(adjacency, state)
        for size in (1, 2)
        for state in masks_of_size(order, size)
    ):
        return False, ()
    return True, independent_triples


def full_incidence_count(
    adjacency: tuple[int, ...],
    family: set[int],
    independent_triples: Iterable[int],
) -> int:
    count = 0
    all_vertices = (1 << len(adjacency)) - 1
    for root in independent_triples:
        if root not in family:
            raise AssertionError("maximum independent state missing from family")
        for target in vertices(all_vertices ^ root):
            target_bit = 1 << target
            if all(
                root ^ (1 << anchor) ^ target_bit in family
                for anchor in vertices(root)
            ):
                count += 1
    return count


def connected_records(order: int) -> Iterator[tuple[str, bytes]]:
    process = subprocess.Popen(
        (str(GENG), "-cq", str(order)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    try:
        for raw in process.stdout:
            if not raw.strip():
                continue
            if not raw.endswith(b"\n"):
                raise AssertionError("geng emitted a non-newline-terminated record")
            yield raw.decode("ascii").rstrip("\n"), raw
    finally:
        process.stdout.close()
        stderr = process.stderr.read()
        process.stderr.close()
        code = process.wait()
        if code != 0 or stderr:
            raise AssertionError(
                {"geng_return_code": code, "geng_stderr": stderr.decode()}
            )


def census_through_nine() -> dict[str, object]:
    rows = []
    for order in range(1, 10):
        stream_digest = hashlib.sha256()
        seen: set[str] = set()
        graph_count = 0
        disconnected_outputs = 0
        equality_count = 0
        full_count = 0
        for record, raw in connected_records(order):
            graph_count += 1
            stream_digest.update(raw)
            if record in seen:
                raise AssertionError(("duplicate graph6 record", order, record))
            seen.add(record)
            decoded_order, graph = decode_graph6(record)
            if decoded_order != order or encode_graph6(graph) != record:
                raise AssertionError(("bad graph6 roundtrip", order, record))
            if not graph_valid(graph):
                raise AssertionError(("invalid graph", order, record))
            if not connected(graph):
                disconnected_outputs += 1
            static, independent_triples = alpha_gamma_three(graph)
            if not static:
                continue
            family, _rounds, _initial, _banned = greatest_kernel(graph, 3)
            if not family:
                continue
            equality_count += 1
            full_count += full_incidence_count(
                graph, family, independent_triples
            )
        if disconnected_outputs:
            raise AssertionError(("geng -c emitted disconnected graphs", order))
        if graph_count != KNOWN_CONNECTED_COUNTS[order]:
            raise AssertionError(
                ("connected count mismatch", order, graph_count)
            )
        rows.append(
            {
                "order": order,
                "connected_unlabeled_graphs": graph_count,
                "distinct_graph6_records": len(seen),
                "graph6_stream_sha256": stream_digest.hexdigest(),
                "all_records_connected": True,
                "gamma_alpha_gamma_infinity_three": equality_count,
                "full_incidences": full_count,
            }
        )
    expected_equalities = [0, 0, 0, 0, 0, 2, 16, 140, 1380]
    if [
        row["gamma_alpha_gamma_infinity_three"] for row in rows
    ] != expected_equalities:
        raise AssertionError(rows)
    if any(row["full_incidences"] for row in rows):
        raise AssertionError("unexpected full incidence through order nine")
    return {
        "generator": {
            "path": str(GENG.relative_to(CAMPAIGN)),
            "sha256": sha256_file(GENG),
            "commands": [
                f"tools/nauty2_9_3/geng -cq {order}"
                for order in range(1, 10)
            ],
        },
        "orders": rows,
        "totals": {
            "connected_unlabeled_graphs": sum(
                row["connected_unlabeled_graphs"] for row in rows
            ),
            "distinct_graph6_records": sum(
                row["distinct_graph6_records"] for row in rows
            ),
            "gamma_alpha_gamma_infinity_three": sum(
                row["gamma_alpha_gamma_infinity_three"] for row in rows
            ),
            "full_incidences": sum(row["full_incidences"] for row in rows),
        },
        "coverage_checks": {
            "known_connected_counts_match_every_order": True,
            "record_order_and_graph6_roundtrip_checked": True,
            "every_output_checked_connected": True,
            "no_duplicate_graph6_record_within_each_stream": True,
            "stream_hashes_frozen": True,
            "generator_is_pinned_but_not_formally_verified_in_this_package": True,
        },
    }


def toggle_audit(base: tuple[int, ...]) -> dict[str, object]:
    order = len(base)
    pairs = tuple(itertools.combinations(range(order), 2))
    root_mask = sum(1 << vertex for vertex in CONTROL_ROOT)
    target_bit = 1 << CONTROL_TARGET
    tested = 0
    equality = 0
    full = 0
    full_edit_sets = []
    for radius in range(3):
        for edits in itertools.combinations(pairs, radius):
            tested += 1
            adjacency = list(base)
            for left, right in edits:
                adjacency[left] ^= 1 << right
                adjacency[right] ^= 1 << left
            graph = tuple(adjacency)
            static, independent_triples = alpha_gamma_three(graph)
            if not static:
                continue
            family, _rounds, _initial, _banned = greatest_kernel(graph, 3)
            if not family:
                continue
            equality += 1
            if root_mask not in independent_triples:
                continue
            if all(
                root_mask ^ (1 << anchor) ^ target_bit in family
                for anchor in CONTROL_ROOT
            ):
                full += 1
                full_edit_sets.append([list(edge) for edge in edits])
    expected_tested = sum(math.comb(len(pairs), radius) for radius in range(3))
    if tested != expected_tested or tested != 2212:
        raise AssertionError(tested)
    if equality != 232 or full != 1 or full_edit_sets != [[]]:
        raise AssertionError((equality, full, full_edit_sets))
    return {
        "scope": "all labeled edge-toggle sets of cardinality zero, one, or two",
        "canonicalized": False,
        "labeled_graphs_tested": tested,
        "gamma_alpha_gamma_infinity_three": equality,
        "specified_full_incidences": full,
        "full_incidence_edit_sets": full_edit_sets,
        "classification": "OBSERVED_ONLY",
        "universal_implication": False,
    }


def dependency_hashes() -> dict[str, str]:
    paths = {
        "C-058": "math/working/universal_transition_private_neighborhood_attack.md",
        "C-059": "math/working/universal_complement_local_balance_attack.md",
        "C-064": "math/working/cross_state_response_exchange.md",
        "C-073": "math/working/k3_full_list_slice/NOTE.md",
        "C-108": "math/lemmas/general_target_response_propagation.md",
        "C-132": "math/working/full_list_multistep_bridge/NOTE.md",
        "C-139": "math/working/anchorless_full_list_structure/NOTE.md",
    }
    return {
        label: sha256_file(CAMPAIGN / relative)
        for label, relative in paths.items()
    }


def candidate_hash_audit() -> dict[str, object]:
    manifest_path = CANDIDATE / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    mismatches = {}
    for filename, expected in manifest["files"].items():
        actual = sha256_file(CANDIDATE / filename)
        if actual != expected:
            mismatches[filename] = {"expected": expected, "actual": actual}
    if mismatches:
        raise AssertionError(mismatches)
    return {
        "manifest_sha256": sha256_file(manifest_path),
        "all_listed_file_hashes_match": True,
        "listed_files": len(manifest["files"]),
    }


def main() -> None:
    control = control_audit()
    _order, base = decode_graph6(CONTROL_G6)
    census = census_through_nine()
    toggles = toggle_audit(base)
    result = {
        "schema": "full-star-reverse-color-hostile-audit-v1",
        "status": "PASS",
        "model": {
            "attacks_only_at_unoccupied_vertices": True,
            "exactly_one_guard_moves": True,
            "move_must_follow_graph_edge": True,
            "every_retained_state_dominates": True,
            "greatest_fixed_point_is_synchronous": True,
        },
        "candidate": candidate_hash_audit(),
        "dependencies": dependency_hashes(),
        "control": control,
        "through_order_nine": census,
        "toggle_probe": toggles,
        "classification": {
            "global_reverse_set_nonempty": "PROVED",
            "global_reverse_set_edge_independent": "PROVED",
            "exact_response_row_formula": "PROVED",
            "feasible_colors_subset_reverse_for_greatest_family": "PROVED",
            "feasible_colors_pass_restricted_kernel": "PROVED",
            "control_refutes_reverse_color_sufficiency": "CERTIFIED_CONTROL",
            "control_refutes_reverse_implies_restricted_survival": "CERTIFIED_CONTROL",
            "zero_full_incidences_through_order_nine": "OBSERVED_ONLY",
            "radius_two_toggle_pattern": "OBSERVED_ONLY",
            "full_list_branch_closed": False,
            "complete_parameter_three": False,
            "universal_conjecture_resolved": False,
        },
        "semantic_checks": {
            "restricted_kernel_universe": (
                "all dominating triples except S-s_r+y for y in N_H(x)"
            ),
            "restricted_kernel_meaning": (
                "greatest eternal triple-family avoiding those exact banned "
                "root-swap states"
            ),
            "does_not_supply_persistent_guard_labels_or_a_coloring": True,
        },
    }
    frozen_path = HERE / "result.json"
    if frozen_path.exists():
        frozen = json.loads(frozen_path.read_text())
        if result != frozen:
            raise AssertionError("result.json differs from the clean replay")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
