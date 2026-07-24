#!/usr/bin/env python3
"""Independent exact audit of the E=2 neutral-cycle corpus geometry.

This checker does not use the constructive C++ search.  It independently
enumerates all monochromatic 5-cliques with recursive adjacency bitsets,
recomputes every one-edge shared-core outcome, and follows the two neutral
transitions until the labeled graph state repeats.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import encode_graph6, read_graph, validate_simple  # noqa: E402


CHECKER_ID = "ramsey55_e2_neutral_cycle_independent_audit_v1"
LINE_PATTERN = re.compile(r"line_(\d{3})")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def enumerate_cliques(
    adjacency: tuple[int, ...], size: int, complement: bool
) -> tuple[tuple[int, ...], ...]:
    """Enumerate each clique once, using increasing-vertex recursion."""

    order = len(adjacency)
    mask = (1 << order) - 1
    neighborhoods = (
        tuple(
            mask & ~(adjacency[vertex] | (1 << vertex))
            for vertex in range(order)
        )
        if complement
        else adjacency
    )
    found: list[tuple[int, ...]] = []

    def visit(candidates: int, selected: tuple[int, ...]) -> None:
        needed = size - len(selected)
        if needed == 0:
            found.append(selected)
            return
        if candidates.bit_count() < needed:
            return
        while candidates:
            if candidates.bit_count() < needed:
                return
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            visit(
                candidates & neighborhoods[vertex],
                (*selected, vertex),
            )

    visit(mask, ())
    return tuple(found)


def all_conflicts(
    adjacency: tuple[int, ...] | list[int],
) -> tuple[tuple[str, tuple[int, ...]], ...]:
    graph = tuple(adjacency)
    validate_simple(list(graph))
    result = [
        ("C5", vertices)
        for vertices in enumerate_cliques(graph, size=5, complement=False)
    ]
    result.extend(
        ("I5", vertices)
        for vertices in enumerate_cliques(graph, size=5, complement=True)
    )
    return tuple(sorted(result))


def toggle_edge(
    adjacency: tuple[int, ...] | list[int], edge: tuple[int, int]
) -> tuple[int, ...]:
    left, right = edge
    if not 0 <= left < right < len(adjacency):
        raise ValueError("edge is not normalized")
    changed = list(adjacency)
    changed[left] ^= 1 << right
    changed[right] ^= 1 << left
    validate_simple(changed)
    return tuple(changed)


def edge_hamming(
    left: tuple[int, ...] | list[int],
    right: tuple[int, ...] | list[int],
) -> int:
    if len(left) != len(right):
        raise ValueError("graph orders differ")
    return sum(
        ((left[a] >> b) & 1) != ((right[a] >> b) & 1)
        for a, b in combinations(range(len(left)), 2)
    )


def conflict_core(
    conflicts: tuple[tuple[str, tuple[int, ...]], ...],
) -> tuple[int, int, int, int]:
    if len(conflicts) != 2:
        raise ValueError("state does not have exactly two conflicts")
    if conflicts[0][0] != conflicts[1][0]:
        raise ValueError("conflict colors differ")
    core = tuple(sorted(set(conflicts[0][1]) & set(conflicts[1][1])))
    if len(core) != 4:
        raise ValueError("conflicts do not intersect in four vertices")
    return core  # type: ignore[return-value]


@dataclass(frozen=True)
class Outcome:
    edge: tuple[int, int]
    graph: tuple[int, ...]
    conflicts: tuple[tuple[str, tuple[int, ...]], ...]

    @property
    def objective(self) -> int:
        return len(self.conflicts)


@dataclass(frozen=True)
class StateInspection:
    graph: tuple[int, ...]
    conflicts: tuple[tuple[str, tuple[int, ...]], ...]
    core: tuple[int, int, int, int]
    neutral: tuple[Outcome, ...]
    barriers: tuple[Outcome, ...]


def inspect_state(
    adjacency: tuple[int, ...] | list[int],
) -> StateInspection:
    graph = tuple(adjacency)
    conflicts = all_conflicts(graph)
    core = conflict_core(conflicts)
    outcomes = tuple(
        Outcome(
            edge=edge,
            graph=(changed := toggle_edge(graph, edge)),
            conflicts=all_conflicts(changed),
        )
        for edge in combinations(core, 2)
    )
    neutral = tuple(item for item in outcomes if item.objective == 2)
    barriers = tuple(item for item in outcomes if item.objective > 2)
    if any(item.objective < 2 for item in outcomes):
        raise ValueError("shared-core edge reaches E<2")
    if len(neutral) != 2 or len(barriers) != 4:
        raise ValueError("state does not have two neutral and four barrier edges")
    for item in neutral:
        conflict_core(item.conflicts)
        if item.conflicts[0][0] == conflicts[0][0]:
            raise ValueError("neutral transition did not change conflict color")
    return StateInspection(
        graph=graph,
        conflicts=conflicts,
        core=core,
        neutral=neutral,
        barriers=barriers,
    )


@dataclass(frozen=True)
class NeutralCycle:
    graphs: tuple[tuple[int, ...], ...]
    graph6: tuple[str, ...]
    transition_edges: tuple[tuple[int, int], ...]
    barrier_profiles: tuple[tuple[int, ...], ...]
    colors: tuple[str, ...]


def build_neutral_cycle(
    adjacency: tuple[int, ...] | list[int],
) -> NeutralCycle:
    start = tuple(adjacency)
    start_code = encode_graph6(list(start))
    current = start
    previous: tuple[int, int] | None = None
    seen: dict[str, int] = {}
    graphs: list[tuple[int, ...]] = []
    codes: list[str] = []
    transitions: list[tuple[int, int]] = []
    barrier_profiles: list[tuple[int, ...]] = []
    colors: list[str] = []

    while True:
        code = encode_graph6(list(current))
        if code in seen:
            if code != start_code or seen[code] != 0:
                raise ValueError("neutral walk entered a noninitial cycle")
            break
        if len(graphs) >= 10_000:
            raise ValueError("neutral walk exceeded 10,000 states")
        seen[code] = len(graphs)
        inspection = inspect_state(current)
        graphs.append(current)
        codes.append(code)
        barrier_profiles.append(
            tuple(sorted(item.objective for item in inspection.barriers))
        )
        colors.append(inspection.conflicts[0][0])

        neutral_by_edge = {item.edge: item for item in inspection.neutral}
        if previous is None:
            edge = min(neutral_by_edge)
        else:
            if previous not in neutral_by_edge:
                raise ValueError("neutral walk lost its reverse edge")
            forward = sorted(set(neutral_by_edge) - {previous})
            if len(forward) != 1:
                raise ValueError("neutral walk is not locally degree two")
            edge = forward[0]
        transitions.append(edge)
        current = neutral_by_edge[edge].graph
        previous = edge

    return NeutralCycle(
        graphs=tuple(graphs),
        graph6=tuple(codes),
        transition_edges=tuple(transitions),
        barrier_profiles=tuple(barrier_profiles),
        colors=tuple(colors),
    )


def line_number(path: str) -> int:
    match = LINE_PATTERN.search(path)
    if match is None:
        raise ValueError(f"path has no line label: {path}")
    return int(match.group(1))


def audit(output: Path) -> dict[str, object]:
    corpus_path = (
        ROOT / "results/verification/e2_overlap_topology_corpus_v1.json"
    )
    followup_path = (
        ROOT
        / "results/verification/conflict_block_catalog22_followup_summary.json"
    )
    search_source = ROOT / "src/search43_e2_barrier_escape.cpp"
    test_source = ROOT / "tests/e2_neutral_cycle_audit_tests.py"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
    followup = json.loads(followup_path.read_text(encoding="utf-8"))

    catalog_records = corpus["corpora"]["catalog_seed_starts"]
    final_records = corpus["corpora"]["conflict_block_finals"]
    if len(catalog_records) != 22 or len(final_records) != 22:
        raise ValueError("expected 22 catalog and 22 final records")
    final_by_line = {line_number(item["path"]): item for item in final_records}
    run_by_line = {int(item["catalog_line"]): item for item in followup["runs"]}
    if len(final_by_line) != 22 or len(run_by_line) != 22:
        raise ValueError("line labels are not one-to-one")

    # Recheck all 44 retained graph hashes and conflict sets independently.
    for record in [*catalog_records, *final_records]:
        path = ROOT / record["path"]
        if sha256(path) != record["sha256"]:
            raise ValueError(f"graph hash mismatch: {path}")
        observed = all_conflicts(tuple(read_graph(path)))
        expected = tuple(
            sorted(
                (
                    str(item["color"]),
                    tuple(int(vertex) for vertex in item["vertices"]),
                )
                for item in record["conflicts"]
            )
        )
        if observed != expected:
            raise ValueError(f"conflict mismatch: {path}")

    cycle_records: list[dict[str, object]] = []
    global_states: set[str] = set()
    global_barriers: collections.Counter[tuple[int, ...]] = (
        collections.Counter()
    )
    edge_multiplicity_distribution: collections.Counter[int] = (
        collections.Counter()
    )
    final_position_distribution: collections.Counter[int] = (
        collections.Counter()
    )

    for seed_record in catalog_records:
        line = line_number(seed_record["path"])
        final_record = final_by_line[line]
        run_record = run_by_line[line]
        seed_path = ROOT / seed_record["path"]
        final_path = ROOT / final_record["path"]
        seed = tuple(read_graph(seed_path))
        final = tuple(read_graph(final_path))
        cycle = build_neutral_cycle(seed)
        if len(cycle.graphs) != 86:
            raise ValueError(f"line {line}: cycle length is not 86")
        if len(set(cycle.graph6)) != 86:
            raise ValueError(f"line {line}: cycle states are not distinct")
        overlap = global_states & set(cycle.graph6)
        if overlap:
            raise ValueError(f"line {line}: cycle overlaps an earlier cycle")
        global_states.update(cycle.graph6)

        transition_counts = collections.Counter(cycle.transition_edges)
        if len(transition_counts) != 43 or set(transition_counts.values()) != {2}:
            raise ValueError(
                f"line {line}: transition edges are not 43 edges twice"
            )
        edge_multiplicity_distribution.update(transition_counts.values())
        global_barriers.update(cycle.barrier_profiles)
        if set(cycle.barrier_profiles) != {
            (9, 9, 9, 38),
            (10, 10, 12, 15),
        }:
            raise ValueError(f"line {line}: unexpected barrier profile")
        if any(
            cycle.colors[(index + 1) % 86] == color
            for index, color in enumerate(cycle.colors)
        ):
            raise ValueError(f"line {line}: colors do not alternate")

        final_code = encode_graph6(list(final))
        if final_code not in cycle.graph6:
            raise ValueError(f"line {line}: final is not on seed cycle")
        final_position = cycle.graph6.index(final_code)
        final_position_distribution[final_position] += 1
        hamming = edge_hamming(seed, final)
        if hamming != int(run_record["edge_hamming_distance"]):
            raise ValueError(f"line {line}: retained Hamming mismatch")
        maximum_hamming = max(
            edge_hamming(seed, graph) for graph in cycle.graphs
        )
        canonical_digest = hashlib.sha256(
            ("\n".join(sorted(cycle.graph6)) + "\n").encode("ascii")
        ).hexdigest()
        cycle_records.append(
            {
                "catalog_line": line,
                "seed_path": seed_record["path"],
                "seed_sha256": seed_record["sha256"],
                "final_path": final_record["path"],
                "final_sha256": final_record["sha256"],
                "cycle_length": len(cycle.graphs),
                "canonical_cycle_digest_sha256": canonical_digest,
                "final_oriented_position": final_position,
                "final_undirected_cycle_distance": min(
                    final_position, 86 - final_position
                ),
                "seed_final_edge_hamming": hamming,
                "recorded_search_edge_hamming": int(
                    run_record["edge_hamming_distance"]
                ),
                "maximum_seed_hamming_on_cycle": maximum_hamming,
                "distinct_transition_edges": len(transition_counts),
                "transition_edge_multiplicities": {
                    str(value): sum(
                        count == value for count in transition_counts.values()
                    )
                    for value in sorted(set(transition_counts.values()))
                },
                "barrier_profile_counts": {
                    ",".join(map(str, profile)): count
                    for profile, count in sorted(
                        collections.Counter(cycle.barrier_profiles).items()
                    )
                },
                "color_counts": dict(
                    sorted(collections.Counter(cycle.colors).items())
                ),
            }
        )

    if len(global_states) != 22 * 86:
        raise ValueError("global neutral-state count is not 1,892")
    expected_barriers = {
        (9, 9, 9, 38): 946,
        (10, 10, 12, 15): 946,
    }
    if dict(global_barriers) != expected_barriers:
        raise ValueError("global barrier-profile counts disagree")

    result: dict[str, object] = {
        "checker": CHECKER_ID,
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "evidence_label": "REPRODUCIBLE COMPUTATIONAL OBSERVATION",
        "input_bindings": {
            "topology_corpus": str(corpus_path.relative_to(ROOT)),
            "topology_corpus_sha256": sha256(corpus_path),
            "followup_summary": str(followup_path.relative_to(ROOT)),
            "followup_summary_sha256": sha256(followup_path),
            "search_source": str(search_source.relative_to(ROOT)),
            "search_source_sha256": sha256(search_source),
            "checker_source": str(Path(__file__).resolve().relative_to(ROOT)),
            "checker_source_sha256": sha256(Path(__file__).resolve()),
            "test_source": str(test_source.relative_to(ROOT)),
            "test_source_sha256": sha256(test_source),
        },
        "corpus_graphs_replayed": 44,
        "seed_cycle_count": len(cycle_records),
        "cycle_length_distribution": {"86": len(cycle_records)},
        "total_distinct_labeled_neutral_states": len(global_states),
        "cycles_pairwise_disjoint": True,
        "neutral_degree_at_every_state": 2,
        "barrier_edges_at_every_state": 4,
        "shared_core_edge_E0_or_E1_outcomes": 0,
        "neutral_transition_changes_conflict_color": True,
        "barrier_profile_counts": {
            ",".join(map(str, profile)): count
            for profile, count in sorted(global_barriers.items())
        },
        "transition_edge_multiplicity_distribution": {
            str(value): count
            for value, count in sorted(edge_multiplicity_distribution.items())
        },
        "all_cycles_use_43_distinct_edges_twice": True,
        "all_22_conflict_block_finals_on_matching_seed_cycle": True,
        "final_oriented_position_distribution": {
            str(position): count
            for position, count in sorted(final_position_distribution.items())
        },
        "cycles": cycle_records,
        "claim_boundary": (
            "This exact computation covers only the 22 labeled neutral "
            "components generated by the 22 retained catalog starts and "
            "binds the 22 retained conflict-block finals to those components. "
            "It is not a theorem about all E=2 order-43 graphs, is not a "
            "construction, and is not a global nonexistence result."
        ),
        "valid": True,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("refusing to overwrite output")
    result = audit(args.output)
    print(
        json.dumps(
            {
                key: value
                for key, value in result.items()
                if key != "cycles"
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
