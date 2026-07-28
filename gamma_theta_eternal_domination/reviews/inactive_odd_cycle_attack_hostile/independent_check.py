#!/usr/bin/env python3
"""Hostile clean-room audit for the inactive induced-C5 certificate.

This file intentionally imports neither the candidate generator nor any
campaign evaluator.  It:

* freezes the candidate note and manifest by SHA-256;
* independently enumerates the 52 equality patterns of five witnesses;
* independently reconstructs every DIMACS byte from the stated mathematics;
* checks every manifest artifact and pinned executable hash;
* replays every DRAT proof with the pinned drat-trim binary; and
* independently verifies the 16-vertex equality/C4 boundary graph.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path
from typing import Iterable, Iterator


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "inactive_odd_cycle_attack"
BUNDLE = CANDIDATE / "certificates"

FROZEN_NOTE_SHA256 = (
    "5ccd88e833db4794a834000a3f72e8ca32efbb339559800728ab0ef196861393"
)
FROZEN_MANIFEST_SHA256 = (
    "3260bd78dd4a8726b2b16f92fcc3dfafc8309531133c3ae34f0f0d3ba24193d7"
)
FROZEN_CONTROL_SHA256 = (
    "a4c9197db6add4d817ff4118d9af07672ca1284bbcb07d4aef6cbe1ec76d55e1"
)
FROZEN_DRAT_TRIM_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)
EXPECTED_CONTROL_G6 = "OQifur}UO]}iTij]tpo}v"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def canonical_word(word: tuple[int, ...]) -> bool:
    """Recognize first-occurrence-normalized set-partition words."""

    if not word or word[0] != 0:
        return False
    seen_maximum = 0
    for value in word[1:]:
        if value > seen_maximum + 1:
            return False
        seen_maximum = max(seen_maximum, value)
    return True


def equality_patterns() -> tuple[str, ...]:
    """Enumerate all equality relations on five ordered objects.

    This deliberately uses an exhaustive scan of all 5^5 words rather than
    the recursive routine in the candidate generator.
    """

    return tuple(
        "".join(map(str, word))
        for word in itertools.product(range(5), repeat=5)
        if canonical_word(word)
    )


def ordered_pairs(order: int) -> Iterator[tuple[int, int]]:
    for first in range(order):
        for second in range(first + 1, order):
            yield first, second


def ordered_triples(order: int) -> Iterator[tuple[int, int, int]]:
    for first in range(order):
        for second in range(first + 1, order):
            for third in range(second + 1, order):
                yield first, second, third


def reconstruct_dimacs(pattern: str) -> tuple[bytes, dict[str, object]]:
    """Reconstruct the candidate formula without importing its code."""

    require(len(pattern) == 5, "witness pattern must have length five")
    labels = tuple(int(character) for character in pattern)
    require(canonical_word(labels), f"noncanonical witness pattern {pattern}")
    block_count = max(labels) + 1
    order = 6 + block_count
    target = order - 1
    states = tuple(ordered_triples(order))

    variable = 1
    h_edge: dict[tuple[int, int], int] = {}
    for pair in ordered_pairs(order):
        h_edge[pair] = variable
        variable += 1

    retained: dict[tuple[int, int, int], int] = {}
    for state in states:
        retained[state] = variable
        variable += 1

    response: dict[tuple[tuple[int, int, int], int, int], int] = {}
    for state in states:
        for attacked in range(order):
            if attacked in state:
                continue
            for guard in state:
                response[(state, attacked, guard)] = variable
                variable += 1

    def h(first: int, second: int) -> int:
        return h_edge[tuple(sorted((first, second)))]

    clauses: list[tuple[int, ...]] = []
    group_counts: dict[str, int] = {}

    start = len(clauses)
    for state in states:
        for attacked in range(order):
            if attacked in state:
                continue
            clauses.append(
                (
                    -retained[state],
                    -h(attacked, state[0]),
                    -h(attacked, state[1]),
                    -h(attacked, state[2]),
                )
            )
    group_counts["retained_state_domination"] = len(clauses) - start

    start = len(clauses)
    for state in states:
        for attacked in range(order):
            if attacked in state:
                continue
            legal_choices: list[int] = []
            for guard in state:
                marker = response[(state, attacked, guard)]
                successor = tuple(
                    sorted(
                        [attacked]
                        + [occupant for occupant in state if occupant != guard]
                    )
                )
                require(len(successor) == 3, "one-swap successor is not a triple")
                legal_choices.append(marker)
                # A selected response is one current guard moving on one G-edge.
                clauses.append((-marker, -h(guard, attacked)))
                # That exact one-swap successor must be retained.
                clauses.append((-marker, retained[successor]))
            # Only unoccupied attacks are visited.  Retention forces at least
            # one individually legal one-guard response.
            clauses.append((-retained[state], *legal_choices))
    group_counts["one_guard_closure"] = len(clauses) - start

    start = len(clauses)
    rim_edges = {
        tuple(sorted((index, (index + 1) % 5)))
        for index in range(5)
    }
    for pair in ordered_pairs(5):
        clauses.append((h(*pair) if pair in rim_edges else -h(*pair),))
    group_counts["induced_c5"] = len(clauses) - start

    start = len(clauses)
    witness_vertices: list[int] = []
    for index, label in enumerate(labels):
        following = (index + 1) % 5
        witness = 5 + label
        witness_vertices.append(witness)
        witness_state = tuple(sorted((index, following, witness)))
        absent_if_first_moves = tuple(sorted((following, witness, target)))
        absent_if_second_moves = tuple(sorted((index, witness, target)))
        clauses.extend(
            (
                (h(index, witness),),
                (h(following, witness),),
                (retained[witness_state],),
                (-retained[absent_if_first_moves],),
                (-retained[absent_if_second_moves],),
            )
        )
    group_counts["witness_and_inactivity"] = len(clauses) - start

    variable_count = variable - 1
    rows = [f"p cnf {variable_count} {len(clauses)}"]
    rows.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    dimacs = ("\n".join(rows) + "\n").encode("ascii")

    state_attack_count = len(states) * (order - 3)
    require(
        group_counts["retained_state_domination"] == state_attack_count,
        "wrong domination-clause count",
    )
    require(
        group_counts["one_guard_closure"] == 7 * state_attack_count,
        "wrong closure-clause count",
    )
    require(group_counts["induced_c5"] == 10, "rim is not fully specified")
    require(
        group_counts["witness_and_inactivity"] == 25,
        "wrong witness/inactivity-clause count",
    )

    return dimacs, {
        "partition": pattern,
        "block_count": block_count,
        "order": order,
        "target": target,
        "witness_vertices": witness_vertices,
        "variables": variable_count,
        "clauses": len(clauses),
        "literal_count": sum(len(clause) for clause in clauses),
        "group_counts": group_counts,
    }


Graph = tuple[frozenset[int], ...]
State = frozenset[int]


def graph_from_edges(order: int, edges: Iterable[tuple[int, int]]) -> Graph:
    rows: list[set[int]] = [set() for _ in range(order)]
    for first, second in edges:
        require(0 <= first < second < order, "malformed edge")
        rows[first].add(second)
        rows[second].add(first)
    return tuple(frozenset(row) for row in rows)


def complement(graph: Graph) -> Graph:
    all_vertices = set(range(len(graph)))
    return tuple(
        frozenset(all_vertices - {vertex} - set(graph[vertex]))
        for vertex in range(len(graph))
    )


def decode_graph6(encoded: str) -> Graph:
    require(encoded and encoded[-1] != "\n", "graph6 must not include newline")
    order = ord(encoded[0]) - 63
    require(0 <= order <= 62, "only short graph6 headers are accepted")
    bits: list[int] = []
    for character in encoded[1:]:
        value = ord(character) - 63
        require(0 <= value < 64, "invalid graph6 payload character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    require(len(bits) >= needed, "truncated graph6 payload")
    require(all(bit == 0 for bit in bits[needed:]), "nonzero graph6 padding")
    edges: list[tuple[int, int]] = []
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.append((low, high))
            cursor += 1
    return graph_from_edges(order, edges)


def encode_graph6(graph: Graph) -> str:
    order = len(graph)
    require(order <= 62, "only short graph6 headers are accepted")
    bits = [
        int(high in graph[low])
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload: list[str] = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def states_of_size(order: int, size: int) -> Iterator[State]:
    for state in itertools.combinations(range(order), size):
        yield frozenset(state)


def dominates(graph: Graph, state: State) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def independent(graph: Graph, state: State) -> bool:
    return all(not (graph[vertex] & state) for vertex in state)


def domination_number(graph: Graph) -> tuple[int, State]:
    for size in range(1, len(graph) + 1):
        for state in states_of_size(len(graph), size):
            if dominates(graph, state):
                return size, state
    raise AssertionError("finite graph has no dominating set")


def independence_number(graph: Graph) -> tuple[int, State]:
    for size in range(len(graph), -1, -1):
        for state in states_of_size(len(graph), size):
            if independent(graph, state):
                return size, state
    raise AssertionError("empty set should be independent")


def independent_domination_number(graph: Graph) -> tuple[int, State]:
    for size in range(1, len(graph) + 1):
        for state in states_of_size(len(graph), size):
            if independent(graph, state) and dominates(graph, state):
                return size, state
    raise AssertionError("a maximal independent set must exist")


def greatest_eternal_family(graph: Graph, guard_count: int) -> frozenset[State]:
    family = {
        state
        for state in states_of_size(len(graph), guard_count)
        if dominates(graph, state)
    }
    while True:
        rejected: set[State] = set()
        for state in family:
            for attacked in range(len(graph)):
                if attacked in state:
                    continue
                if not any(
                    attacked in graph[guard]
                    and frozenset((state - {guard}) | {attacked}) in family
                    for guard in state
                ):
                    rejected.add(state)
                    break
        if not rejected:
            return frozenset(family)
        family.difference_update(rejected)


def eternal_number(
    graph: Graph, gamma_lower_bound: int
) -> tuple[int, frozenset[State]]:
    for size in range(gamma_lower_bound, len(graph) + 1):
        kernel = greatest_eternal_family(graph, size)
        if kernel:
            return size, kernel
    raise AssertionError("all guards form an eternal family")


def coloring_with_at_most(graph: Graph, color_count: int) -> tuple[int, ...] | None:
    colors = [-1] * len(graph)

    def search(remaining: set[int]) -> bool:
        if not remaining:
            return True
        vertex = max(
            remaining,
            key=lambda candidate: (
                len(
                    {
                        colors[neighbor]
                        for neighbor in graph[candidate]
                        if colors[neighbor] >= 0
                    }
                ),
                len(graph[candidate] & remaining),
                len(graph[candidate]),
                -candidate,
            ),
        )
        forbidden = {
            colors[neighbor]
            for neighbor in graph[vertex]
            if colors[neighbor] >= 0
        }
        # Trying only a single representative unused color is a sound color
        # permutation reduction.
        used = set(colors) - {-1}
        choices = [color for color in range(color_count) if color not in forbidden]
        unused_seen = False
        for color in choices:
            if color not in used:
                if unused_seen:
                    continue
                unused_seen = True
            colors[vertex] = color
            if search(remaining - {vertex}):
                return True
            colors[vertex] = -1
        return False

    if search(set(range(len(graph)))):
        return tuple(colors)
    return None


def chromatic_number(graph: Graph) -> tuple[int, tuple[int, ...]]:
    for count in range(1, len(graph) + 1):
        coloring = coloring_with_at_most(graph, count)
        if coloring is not None:
            return count, coloring
    raise AssertionError("assigning a distinct color to every vertex must work")


def exact_parameters(graph: Graph) -> tuple[dict[str, int], dict[str, object]]:
    gamma, dominating_witness = domination_number(graph)
    ind_dom, independent_dominating_witness = independent_domination_number(graph)
    alpha, independent_witness = independence_number(graph)
    gamma_infinity, kernel = eternal_number(graph, gamma)
    theta, clique_partition_coloring = chromatic_number(complement(graph))
    return (
        {
            "gamma": gamma,
            "i": ind_dom,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        {
            "dominating_witness": sorted(dominating_witness),
            "independent_dominating_witness": sorted(
                independent_dominating_witness
            ),
            "maximum_independent_witness": sorted(independent_witness),
            "eternal_kernel": kernel,
            "theta_coloring": list(clique_partition_coloring),
        },
    )


def audit_c4_control() -> dict[str, object]:
    control_path = CANDIDATE / "c4_control.json"
    require(sha256(control_path) == FROZEN_CONTROL_SHA256, "C4 control changed")
    claimed = json.loads(control_path.read_text(encoding="utf-8"))
    require(
        claimed.get("schema") == "inactive-c4-parity-control-v1",
        "wrong C4-control schema",
    )
    require(claimed.get("graph6_G") == EXPECTED_CONTROL_G6, "wrong graph6 graph")

    g_graph = decode_graph6(EXPECTED_CONTROL_G6)
    require(encode_graph6(g_graph) == EXPECTED_CONTROL_G6, "graph6 round trip failed")
    h_graph = complement(g_graph)
    h_edges = [
        [first, second]
        for first, second in ordered_pairs(len(h_graph))
        if second in h_graph[first]
    ]
    require(h_edges == claimed["H_edges"], "graph6 and stated H edge list disagree")

    target = claimed["target"]
    require(target == 15, "unexpected target")
    deletion_g = graph_from_edges(
        target,
        (
            (first, second)
            for first, second in ordered_pairs(target)
            if second in g_graph[first]
        ),
    )

    full_parameters, full_data = exact_parameters(g_graph)
    deletion_parameters, deletion_data = exact_parameters(deletion_g)
    require(
        full_parameters == claimed["full_parameters"] == {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "full control parameters are not all three",
    )
    require(
        deletion_parameters == claimed["deletion_parameters"] == {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 3,
        },
        "deletion control parameters are not all three",
    )

    full_kernel = full_data["eternal_kernel"]
    deletion_kernel = deletion_data["eternal_kernel"]
    require(isinstance(full_kernel, frozenset), "full kernel has wrong type")
    require(isinstance(deletion_kernel, frozenset), "deletion kernel has wrong type")
    require(
        len(full_kernel) == claimed["greatest_triple_kernel_size"] == 304,
        "wrong full greatest-kernel size",
    )

    deletion_triangles = tuple(
        frozenset(state)
        for state in ordered_triples(target)
        if all(second in h_graph[first] for first, second in itertools.combinations(state, 2))
    )
    require(
        len(deletion_triangles) == claimed["deletion_triangle_count"] == 18,
        "wrong deletion triangle count",
    )
    require(
        set(deletion_triangles) <= set(full_kernel),
        "a full-graph maximum independent triple is missing from the full kernel",
    )
    require(
        set(deletion_triangles) <= set(deletion_kernel),
        "a deletion maximum independent triple is missing from its kernel",
    )

    active: set[int] = set()
    inactive: set[int] = set()
    incidence_count = 0
    for vertex in range(target):
        containing = [
            state for state in deletion_triangles if vertex in state
        ]
        require(bool(containing), f"deletion vertex {vertex} has no triangle")
        statuses: set[bool] = set()
        for state in containing:
            incidence_count += 1
            successor = frozenset((state - {vertex}) | {target})
            statuses.add(
                target in g_graph[vertex] and successor in full_kernel
            )
        require(
            len(statuses) == 1,
            f"target-response status fails to propagate at vertex {vertex}",
        )
        if next(iter(statuses)):
            active.add(vertex)
        else:
            inactive.add(vertex)

    require(sorted(active) == claimed["active_set"], "wrong active set")
    require(sorted(inactive) == claimed["inactive_set"], "wrong inactive set")

    inactive_edges = [
        [first, second]
        for first, second in ordered_pairs(target)
        if first in inactive and second in inactive and second in h_graph[first]
    ]
    require(
        inactive_edges == claimed["inactive_induced_edges"],
        "wrong inactive induced edge set",
    )

    cycle = claimed["named_inactive_induced_C4"]
    require(cycle == [0, 1, 2, 3, 0], "unexpected named C4")
    rim = cycle[:-1]
    require(len(set(rim)) == 4 and set(rim) <= inactive, "C4 vertices invalid")
    expected_cycle_edges = {
        tuple(sorted((rim[index], rim[(index + 1) % 4])))
        for index in range(4)
    }
    actual_cycle_edges = {
        (first, second)
        for first, second in ordered_pairs(target)
        if first in rim and second in rim and second in h_graph[first]
    }
    require(
        actual_cycle_edges == expected_cycle_edges,
        "named inactive C4 is not induced",
    )

    root = frozenset(claimed["root"])
    require(root == frozenset((5, 6, 7)), "unexpected root")
    require(root in deletion_triangles, "root is not an H triangle")
    require(root in full_kernel, "root is not retained")
    root_responses: dict[str, list[int]] = {}
    for guard in sorted(root):
        require(target in g_graph[guard], f"root guard {guard} cannot move to target")
        successor = frozenset((root - {guard}) | {target})
        require(successor in full_kernel, f"root guard {guard} response is not retained")
        require(dominates(g_graph, successor), "root successor does not dominate")
        root_responses[str(guard)] = sorted(successor)
    require(
        claimed["root_full_in_greatest_kernel"] is True,
        "control does not claim a full root",
    )

    return {
        "control_sha256": FROZEN_CONTROL_SHA256,
        "graph6_G": EXPECTED_CONTROL_G6,
        "full_parameters": full_parameters,
        "deletion_parameters": deletion_parameters,
        "full_kernel_size": len(full_kernel),
        "deletion_kernel_size": len(deletion_kernel),
        "deletion_triangle_count": len(deletion_triangles),
        "triangle_vertex_incidences_checked": incidence_count,
        "active_set": sorted(active),
        "inactive_set": sorted(inactive),
        "inactive_induced_edges": inactive_edges,
        "named_inactive_induced_C4": cycle,
        "root": sorted(root),
        "root_responses": root_responses,
        "full_theta_coloring": full_data["theta_coloring"],
        "deletion_theta_coloring": deletion_data["theta_coloring"],
    }


def safe_case_path(relative: str, expected: str) -> Path:
    require(relative == expected, f"unexpected artifact path {relative!r}")
    path = (BUNDLE / relative).resolve()
    require(path.is_relative_to(BUNDLE.resolve()), "artifact escapes bundle")
    return path


def audit_certificate_bundle() -> dict[str, object]:
    note_path = CANDIDATE / "NOTE.md"
    manifest_path = BUNDLE / "manifest.json"
    require(sha256(note_path) == FROZEN_NOTE_SHA256, "candidate note changed")
    require(
        sha256(manifest_path) == FROZEN_MANIFEST_SHA256,
        "candidate manifest changed",
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    patterns = equality_patterns()
    require(len(patterns) == 52, "Bell-number coverage is not 52")
    require(len(set(patterns)) == 52, "duplicate equality pattern")
    require(
        manifest.get("schema") == "inactive-c5-local-certificates-v1",
        "wrong certificate schema",
    )
    require(
        manifest.get("model") == "one-guard-moves; unoccupied attacks only",
        "wrong model ledger",
    )
    require(manifest.get("partition_count") == 52, "wrong partition count")
    require(tuple(manifest.get("partitions", ())) == patterns, "wrong RGS manifest")
    records = manifest.get("cases")
    require(isinstance(records, list) and len(records) == 52, "wrong case list")
    require(
        tuple(record.get("partition") for record in records) == patterns,
        "case order/coverage mismatch",
    )

    checker = Path(manifest["checker"]["path"]).resolve()
    solver = Path(manifest["solver"]["path"]).resolve()
    expected_checker = (
        CAMPAIGN / "tools" / "drat_trim_2023_05_22" / "drat-trim"
    ).resolve()
    expected_solver = (
        CAMPAIGN / "tools" / "cadical_3_0_1" / "build" / "cadical"
    ).resolve()
    require(checker == expected_checker, "manifest points at an unexpected checker")
    require(solver == expected_solver, "manifest points at an unexpected solver")
    require(checker.is_file(), "pinned checker is missing")
    require(solver.is_file(), "pinned solver is missing")
    require(
        sha256(checker) == manifest["checker"]["sha256"]
        == FROZEN_DRAT_TRIM_SHA256,
        "pinned checker hash mismatch",
    )
    require(
        sha256(solver) == manifest["solver"]["sha256"],
        "pinned solver hash mismatch",
    )

    all_paths: set[Path] = set()
    total_clauses = 0
    total_literals = 0
    total_proof_bytes = 0
    order_histogram: dict[int, int] = {}
    group_totals = {
        "retained_state_domination": 0,
        "one_guard_closure": 0,
        "induced_c5": 0,
        "witness_and_inactivity": 0,
    }
    for record, pattern in zip(records, patterns, strict=True):
        suffixes = (
            ("instance", "instance_sha256", f"cases/{pattern}.cnf"),
            ("proof", "proof_sha256", f"cases/{pattern}.drat"),
            ("solver_log", "solver_log_sha256", f"cases/{pattern}.solver.txt"),
            ("checker_log", "checker_log_sha256", f"cases/{pattern}.checker.txt"),
        )
        artifacts: dict[str, Path] = {}
        for field, hash_field, expected_relative in suffixes:
            path = safe_case_path(record[field], expected_relative)
            require(path not in all_paths, f"duplicate artifact {path}")
            all_paths.add(path)
            require(path.is_file(), f"missing artifact {path}")
            require(sha256(path) == record[hash_field], f"hash mismatch for {path}")
            artifacts[field] = path

        expected_bytes, statistics = reconstruct_dimacs(pattern)
        require(
            artifacts["instance"].read_bytes() == expected_bytes,
            f"DIMACS byte mismatch for {pattern}",
        )
        for field in (
            "partition",
            "block_count",
            "order",
            "target",
            "witness_vertices",
            "variables",
            "clauses",
            "literal_count",
        ):
            require(
                record[field] == statistics[field],
                f"manifest {field} mismatch for {pattern}",
            )
        require(record["solver_returncode"] == 20, "wrong solver return code")
        require(record["checker_returncode"] == 0, "wrong checker return code")
        require(record["checker_verified"] is True, "checker flag is false")
        require(
            "s UNSATISFIABLE"
            in artifacts["solver_log"].read_text(encoding="utf-8"),
            f"solver log lacks UNSAT for {pattern}",
        )
        require(
            "s VERIFIED" in artifacts["checker_log"].read_text(encoding="utf-8"),
            f"checker log lacks VERIFIED for {pattern}",
        )

        replay = subprocess.run(
            [str(checker), str(artifacts["instance"]), str(artifacts["proof"])],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        require(replay.returncode == 0, f"DRAT replay failed for {pattern}")
        require(
            "s VERIFIED" in replay.stdout + replay.stderr,
            f"DRAT replay did not report VERIFIED for {pattern}",
        )

        total_clauses += int(statistics["clauses"])
        total_literals += int(statistics["literal_count"])
        proof_size = artifacts["proof"].stat().st_size
        require(
            proof_size == record["proof_size_bytes"],
            f"proof-size mismatch for {pattern}",
        )
        total_proof_bytes += proof_size
        order = int(statistics["order"])
        order_histogram[order] = order_histogram.get(order, 0) + 1
        group_counts = statistics["group_counts"]
        require(isinstance(group_counts, dict), "group counts malformed")
        for name in group_totals:
            group_totals[name] += int(group_counts[name])

    require(
        order_histogram == {7: 1, 8: 15, 9: 25, 10: 10, 11: 1},
        "Stirling-number order histogram mismatch",
    )
    disk_case_files = {
        path.resolve()
        for path in (BUNDLE / "cases").iterdir()
        if path.is_file()
    }
    require(
        disk_case_files == all_paths,
        "case directory contains an unmanifested or omitted artifact",
    )
    require(total_clauses == 215_100, "unexpected total clause count")
    require(total_proof_bytes == 276_375, "unexpected total proof bytes")

    return {
        "note_sha256": FROZEN_NOTE_SHA256,
        "manifest_sha256": FROZEN_MANIFEST_SHA256,
        "checker_sha256": sha256(checker),
        "solver_sha256": sha256(solver),
        "partition_count": len(patterns),
        "partitions": list(patterns),
        "order_histogram": {
            str(order): count for order, count in sorted(order_histogram.items())
        },
        "clause_group_totals": group_totals,
        "total_clauses": total_clauses,
        "total_literals": total_literals,
        "total_proof_bytes": total_proof_bytes,
        "case_artifact_count": len(all_paths),
        "case_directory_exactly_matches_manifest": True,
        "all_artifact_hashes_match": True,
        "all_instance_bytes_match": True,
        "all_52_drat_proofs_replayed": True,
        "semantic_audit": {
            "attacks_are_only_on_unoccupied_template_vertices": True,
            "each_response_moves_exactly_one_current_guard": True,
            "each_move_requires_one_G_edge": True,
            "each_successor_is_the_exact_one_swap_state": True,
            "each_successor_is_retained": True,
            "every_retained_state_dominates_every_template_vertex": True,
            "multiple_true_response_markers_mean_multiple_legal_choices_not_simultaneous_moves": True,
        },
    }


def main() -> None:
    bundle_result = audit_certificate_bundle()
    control_result = audit_c4_control()
    payload = {
        "schema": "inactive-c5-hostile-review-v1",
        "verdict": "UNCONDITIONAL PASS",
        "scope": (
            "local inactive induced C5 exclusion and its stated equality "
            "corollary only; no claim of inactive bipartiteness or full k=3"
        ),
        "bundle": bundle_result,
        "c4_control": control_result,
        "mathematical_coverage": {
            "five_witness_equality_patterns_are_exactly_all_52_set_partitions": True,
            "alpha_equals_gamma_infinity_equals_3_forces_every_H_triangle_into_every_optimal_family": True,
            "gamma_of_G_minus_x_at_least_3_supplies_a_common_H_neighbor_for_each_C5_rim_edge": True,
            "an_induced_C5_forces_each_witness_off_the_rim": True,
            "C108_inactivity_supplies_all_ten_absent_endpoint_successors": True,
            "restriction_to_template_vertices_is_a_sound_relaxation": True,
            "extra_vertices_or_edges_cannot_rescue_a_template_attack": True,
        },
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    output = HERE / "evidence.json"
    output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    print("evidence_sha256", hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == "__main__":
    main()
