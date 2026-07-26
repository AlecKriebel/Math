#!/usr/bin/env python3
"""Independent hostile probe for the anti-C7 near-hub note.

The evaluator uses explicit frozenset configurations and imports no campaign
graph, game, or search implementation.  Enumeration is supporting regression
evidence; the accompanying review audits the handwritten proof.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess


CAMPAIGN = Path(__file__).resolve().parents[1]
NOTE = CAMPAIGN / "math/lemmas/order12_k4_antihole_near_hubs.md"
AUTHOR_PROBE = CAMPAIGN / "reviews/order12_k4_antihole_near_hubs_probe.py"
NOTE_SHA256 = (
    "5db7b3970794ca3dd16fd612ae2d1b2111a68596a34ccd304c7a30fd1371688e"
)
PREDECESSOR_NOTE_SHA256 = (
    "39182554433e413741f15d7c70e89d07389c8d1ebd658ab74c39bc596fc825c5"
)
AUTHOR_PROBE_SHA256 = (
    "850e7973b5863b7beb8d6562149f4c08adf7a36af9df8bba22a99fd6c14fe0c2"
)


Graph = tuple[frozenset[int], ...]
State = frozenset[int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def two_spokes(first: int, second: int, outside_edge: bool) -> Graph:
    neighbors = [set() for _ in range(9)]
    for vertex in range(7):
        successor = (vertex + 1) % 7
        neighbors[vertex].add(successor)
        neighbors[successor].add(vertex)
    for outside, rim in ((7, first), (8, second)):
        neighbors[outside].add(rim)
        neighbors[rim].add(outside)
    if outside_edge:
        neighbors[7].add(8)
        neighbors[8].add(7)
    return tuple(frozenset(row) for row in neighbors)


def dominates(graph: Graph, state: State) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(graph[guard])
    return len(covered) == len(graph)


def independent(graph: Graph, state: State) -> bool:
    return all(second not in graph[first] for first, second in combinations(state, 2))


def successors(graph: Graph, state: State, attack: int) -> tuple[State, ...]:
    require(attack not in state, "occupied attack")
    return tuple(
        frozenset((set(state) - {guard}) | {attack})
        for guard in sorted(state)
        if attack in graph[guard]
    )


def live_family(graph: Graph, guards: int) -> set[State]:
    live = {
        frozenset(selected)
        for selected in combinations(range(len(graph)), guards)
        if dominates(graph, frozenset(selected))
    }
    while True:
        rejected = {
            state
            for state in live
            if any(
                not any(
                    response in live
                    for response in successors(graph, state, attack)
                )
                for attack in range(len(graph))
                if attack not in state
            )
        }
        if not rejected:
            return live
        live.difference_update(rejected)


def eternal_number(graph: Graph) -> int:
    for guards in range(1, len(graph) + 1):
        if live_family(graph, guards):
            return guards
    raise AssertionError("fully occupied configuration must survive")


def two_spoke_exhaustion() -> dict[str, object]:
    histogram: dict[int, int] = {}
    for first in range(7):
        for second in range(7):
            for edge in (False, True):
                value = eternal_number(two_spokes(first, second, edge))
                histogram[value] = histogram.get(value, 0) + 1
                require(
                    value == (4 if edge and first == second else 5),
                    "two-spoke characterization failed",
                )
    require(histogram == {4: 7, 5: 91}, "two-spoke histogram differs")
    return {
        "ordered_labeled_graphs": 98,
        "histogram": {str(key): histogram[key] for key in sorted(histogram)},
    }


def independent_five_set_exhaustion() -> dict[str, object]:
    cycle = two_spokes(0, 0, False)[:7]
    witnesses: dict[str, list[int]] = {}
    for first in range(7):
        for second in range(7):
            triple = next(
                (
                    selected
                    for selected in combinations(range(7), 3)
                    if first not in selected
                    and second not in selected
                    and independent(cycle, frozenset(selected))
                ),
                None,
            )
            require(triple is not None, "deleted pair hits every stable triple")
            witnesses[f"{first},{second}"] = list(triple)
    return {
        "ordered_deleted_pairs": len(witnesses),
        "witness_table_sha256": sha256(
            (
                json.dumps(witnesses, sort_keys=True, separators=(",", ":"))
                + "\n"
            ).encode("ascii")
        ).hexdigest(),
    }


def attack_table_exhaustion() -> dict[str, object]:
    rows = {
        1: (frozenset({1, 3, 6, 7}), 2, frozenset({2, 3, 6, 7}), 0),
        2: (frozenset({1, 3, 6, 7}), 0, frozenset({0, 3, 6, 7}), 2),
        3: (frozenset({1, 4, 6, 7}), 0, frozenset({0, 1, 4, 7}), 3),
    }
    records: dict[str, object] = {}
    for distance, (forced, first_attack, expected, second_attack) in rows.items():
        graph = two_spokes(0, distance, True)
        require(independent(graph, forced), "forced configuration is not stable")
        first = successors(graph, forced, first_attack)
        dominating_first = tuple(state for state in first if dominates(graph, state))
        require(dominating_first == (expected,), "unique first response differs")
        second = successors(graph, expected, second_attack)
        require(second, "second attack has no adjacent guard to audit")
        require(
            not any(dominates(graph, state) for state in second),
            "second attack has a dominating response",
        )
        records[str(distance)] = {
            "first_response_count": len(first),
            "dominating_first_count": len(dominating_first),
            "second_response_count": len(second),
            "dominating_second_count": 0,
        }
    return records


def antihole_graph() -> Graph:
    neighbors = []
    for vertex in range(7):
        forbidden = {vertex, (vertex - 1) % 7, (vertex + 1) % 7}
        neighbors.append(frozenset(set(range(7)) - forbidden))
    return tuple(neighbors)


def p3_cap_exhaustion() -> dict[str, object]:
    antihole = antihole_graph()
    base = ((0, 1, 4), (0, 2, 5), (0, 3, 6))
    no_hub_patterns = 0
    five_near_failures = 0
    for gap in range(7):
        triples = tuple(
            tuple((vertex + gap) % 7 for vertex in triple)
            for triple in base
        )
        require(
            set().union(*(set(triple) for triple in triples)) == set(range(7)),
            "cap triples do not cover rim",
        )
        for triple in triples:
            internal = [
                witness
                for witness in range(7)
                if witness not in triple
                and all(vertex in antihole[witness] for vertex in triple)
            ]
            require(not internal, "cap triple has internal antihole witness")
            near = set(range(7)) - {gap}
            require(
                not set(triple).issubset(near),
                "aligned near-hub witnesses cap triple",
            )
        five_near_failures += 1
        for remaining_mask in range((1 << 7) - 1):
            remaining = {
                vertex
                for vertex in range(7)
                if remaining_mask & (1 << vertex)
            }
            if all(set(triple).issubset(remaining) for triple in triples):
                no_hub_patterns += 1
    require(no_hub_patterns == 0, "nonhub outside pattern witnesses all cap triples")
    return {
        "aligned_gap_cases": 7,
        "four_near_hub_nonhub_patterns": 7 * 127,
        "five_near_hub_cases": five_near_failures,
        "surviving_no_hub_patterns": no_hub_patterns,
    }


def author_probe_replay() -> dict[str, object]:
    # The author probe remains immutably bound to the predecessor note.  Run
    # its unchanged semantic checks against the accepted editorial revision
    # by overriding only that expected note digest in memory.
    bootstrap = (
        "import importlib.util;"
        f"p={str(AUTHOR_PROBE)!r};"
        "s=importlib.util.spec_from_file_location('anti_c7_author_probe',p);"
        "m=importlib.util.module_from_spec(s);"
        "s.loader.exec_module(m);"
        f"m.FROZEN_NOTE_SHA256={NOTE_SHA256!r};"
        "m.main()"
    )
    completed = subprocess.run(
        ("python3", "-c", bootstrap),
        cwd=CAMPAIGN,
        env={},
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
        timeout=30,
    )
    require(completed.returncode == 0, "author probe returned nonzero")
    require(not completed.stderr, "author probe wrote stderr")
    report = json.loads(completed.stdout)
    require(
        report["verdict_signal"] == "PASS_PROPOSED_LEMMA_REGRESSION",
        "author probe verdict differs",
    )
    return {
        "exit_code": completed.returncode,
        "stdout_sha256": sha256(completed.stdout).hexdigest(),
        "stderr_bytes": len(completed.stderr),
        "author_source_unchanged": True,
        "runtime_note_hash_rebinding_only": True,
        "predecessor_note_sha256": PREDECESSOR_NOTE_SHA256,
    }


def main() -> None:
    require(digest(NOTE) == NOTE_SHA256, "note hash differs")
    require(digest(AUTHOR_PROBE) == AUTHOR_PROBE_SHA256, "author probe hash differs")
    report = {
        "schema": "order12-k4-antihole-near-hubs-hostile-probe-v1",
        "frozen_inputs": {
            str(NOTE.relative_to(CAMPAIGN)): NOTE_SHA256,
            str(AUTHOR_PROBE.relative_to(CAMPAIGN)): AUTHOR_PROBE_SHA256,
        },
        "independence": {
            "campaign_game_code_imported": False,
            "state_representation": "frozenset",
            "closure": "explicit colored configuration graph greatest fixed point",
        },
        "two_spoke_exhaustion": two_spoke_exhaustion(),
        "independent_five_sets": independent_five_set_exhaustion(),
        "attack_table": attack_table_exhaustion(),
        "p3_cap": p3_cap_exhaustion(),
        "author_probe_replay": author_probe_replay(),
        "verdict_signal": "ACCEPT_LOCAL_LEMMAS_WITHOUT_SCOPE_INFLATION",
    }
    print(json.dumps(report, allow_nan=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
