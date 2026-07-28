#!/usr/bin/env python3
"""Clean-room audit of the separated-port bounded extension search.

This checker imports no campaign search module.  It reconstructs the
one-guard game from ordinary tuples and sets, enumerates both labeled scopes,
and independently tests the exact response-list/list-coloring predicate.
For every positive case it also computes gamma, alpha, gamma-infinity, and
theta directly.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path


N = 10
OLD_N = 9
VERTICES = tuple(range(N))
ANCHORS = (0, 1, 2)
ANCHOR_SET = frozenset(ANCHORS)
FULL_VERTEX = 3
BASE_H_EDGES = frozenset(
    {
        (0, 1),
        (0, 2),
        (1, 2),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 8),
        (7, 8),
        (4, 7),
    }
)
OLD_LISTS = {
    3: frozenset((0, 1, 2)),
    4: frozenset((0, 1)),
    5: frozenset((0, 1)),
    6: frozenset((0, 1)),
    7: frozenset((1, 2)),
    8: frozenset((1, 2)),
}
REVIEW_DIR = Path(__file__).resolve().parent
CAMPAIGN_DIR = REVIEW_DIR.parents[1]
SOURCE_DIR = (
    CAMPAIGN_DIR / "math" / "working" / "separated_port_gamma3_extensions"
)
LABELG = CAMPAIGN_DIR / "tools" / "nauty2_9_3" / "labelg"


def edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


ALL_OLD_PAIRS = frozenset(
    edge(u, v) for u in range(OLD_N) for v in range(u + 1, OLD_N)
)
ADDABLE_OLD_H_EDGES = tuple(sorted(ALL_OLD_PAIRS - BASE_H_EDGES))


def make_h_edges(
    extension_mask: int, added_h_edge: tuple[int, int] | None
) -> frozenset[tuple[int, int]]:
    result = set(BASE_H_EDGES)
    result.update(
        edge(old, 9)
        for old in range(OLD_N)
        if extension_mask & (1 << old)
    )
    if added_h_edge is not None:
        result.add(added_h_edge)
    return frozenset(result)


def adjacency(
    h_edges: frozenset[tuple[int, int]],
) -> tuple[tuple[frozenset[int], ...], tuple[frozenset[int], ...]]:
    h = []
    g = []
    for u in VERTICES:
        h_neighbors = frozenset(
            v for v in VERTICES if v != u and edge(u, v) in h_edges
        )
        h.append(h_neighbors)
        g.append(frozenset(VERTICES) - {u} - h_neighbors)
    return tuple(h), tuple(g)


def dominates(state: tuple[int, ...], g: tuple[frozenset[int], ...]) -> bool:
    covered = set(state)
    for guard in state:
        covered.update(g[guard])
    return len(covered) == N


def dominating_states(
    size: int, g: tuple[frozenset[int], ...]
) -> frozenset[tuple[int, ...]]:
    return frozenset(
        state
        for state in itertools.combinations(VERTICES, size)
        if dominates(state, g)
    )


def transition_table(
    states: frozenset[tuple[int, ...]],
    g: tuple[frozenset[int], ...],
) -> dict[tuple[int, ...], dict[int, frozenset[tuple[int, ...]]]]:
    table = {}
    for state in states:
        state_set = set(state)
        by_attack = {}
        for attack in set(VERTICES) - state_set:
            successors = set()
            for guard in state:
                if attack in g[guard]:
                    successors.add(
                        tuple(sorted((state_set - {guard}) | {attack}))
                    )
            by_attack[attack] = frozenset(successors)
        table[state] = by_attack
    return table


def greatest_kernel(
    states: frozenset[tuple[int, ...]],
    transitions: dict[
        tuple[int, ...], dict[int, frozenset[tuple[int, ...]]]
    ],
    banned: frozenset[tuple[int, ...]] = frozenset(),
) -> frozenset[tuple[int, ...]]:
    active = set(states - banned)
    while True:
        dead = {
            state
            for state in active
            if any(
                not (successors & active)
                for successors in transitions[state].values()
            )
        }
        if not dead:
            return frozenset(active)
        active.difference_update(dead)


def direct_swap(guard: int, target: int) -> tuple[int, ...]:
    return tuple(sorted((ANCHOR_SET - {guard}) | {target}))


def list_colorable(
    h: tuple[frozenset[int], ...],
    response_lists: dict[int, frozenset[int]],
    *,
    include_full_vertex: bool,
) -> bool:
    colors = {0: 0, 1: 1, 2: 2}
    domains = dict(response_lists)
    if include_full_vertex:
        domains[FULL_VERTEX] = frozenset((0,))
    remaining = frozenset(
        vertex
        for vertex in range(3, N)
        if include_full_vertex or vertex != FULL_VERTEX
    )

    def search(todo: frozenset[int]) -> bool:
        if not todo:
            return True
        feasible = {}
        for vertex in todo:
            choices = tuple(
                color
                for color in domains[vertex]
                if all(
                    other_color != color
                    for other, other_color in colors.items()
                    if other in h[vertex]
                )
            )
            if not choices:
                return False
            feasible[vertex] = choices
        vertex = min(feasible, key=lambda v: (len(feasible[v]), v))
        for color in feasible[vertex]:
            colors[vertex] = color
            if search(todo - {vertex}):
                del colors[vertex]
                return True
            del colors[vertex]
        return False

    return search(remaining)


def exact_predicate(
    h: tuple[frozenset[int], ...],
    g: tuple[frozenset[int], ...],
    triples: frozenset[tuple[int, ...]],
    transitions: dict[
        tuple[int, ...], dict[int, frozenset[tuple[int, ...]]]
    ],
) -> tuple[bool, int]:
    positive_witnesses = 0
    for subset_bits in range(1, 7):
        new_list = frozenset(
            guard for guard in ANCHORS if subset_bits & (1 << guard)
        )
        response_lists = dict(OLD_LISTS)
        response_lists[9] = new_list
        banned = frozenset(
            direct_swap(guard, target)
            for target, allowed in response_lists.items()
            for guard in ANCHORS
            if guard not in allowed
        )
        required = frozenset({ANCHORS}) | frozenset(
            direct_swap(guard, target)
            for target, allowed in response_lists.items()
            for guard in allowed
        )
        kernel = greatest_kernel(triples, transitions, banned)
        if not required <= kernel:
            continue

        # This semantic check also audits the subtle case where the added
        # H-edge is incident with an anchor.  A direct-swap family state
        # cannot dominate its removed anchor unless the swap is a G-edge.
        actual_lists = {
            target: frozenset(
                guard
                for guard in ANCHORS
                if target in g[guard]
                and direct_swap(guard, target) in kernel
            )
            for target in range(3, N)
        }
        assert actual_lists == response_lists

        base_sat = list_colorable(
            h, response_lists, include_full_vertex=False
        )
        augmented_sat = list_colorable(
            h, response_lists, include_full_vertex=True
        )
        if base_sat and not augmented_sat:
            positive_witnesses += 1
    return positive_witnesses > 0, positive_witnesses


def exact_gamma(g: tuple[frozenset[int], ...]) -> int:
    for size in range(1, N + 1):
        if dominating_states(size, g):
            return size
    raise AssertionError("gamma")


def exact_alpha(g: tuple[frozenset[int], ...]) -> int:
    for size in range(N, 0, -1):
        for state in itertools.combinations(VERTICES, size):
            if all(v not in g[u] for u, v in itertools.combinations(state, 2)):
                return size
    raise AssertionError("alpha")


def exact_gamma_infinity(g: tuple[frozenset[int], ...]) -> int:
    for size in range(1, N + 1):
        states = dominating_states(size, g)
        if states and greatest_kernel(
            states, transition_table(states, g)
        ):
            return size
    raise AssertionError("gamma infinity")


def colorable(
    h: tuple[frozenset[int], ...], number_of_colors: int
) -> bool:
    assigned: dict[int, int] = {}

    def search() -> bool:
        if len(assigned) == N:
            return True
        uncolored = set(VERTICES) - assigned.keys()
        feasible = {}
        for vertex in uncolored:
            choices = tuple(
                color
                for color in range(number_of_colors)
                if all(
                    assigned[neighbor] != color
                    for neighbor in h[vertex]
                    if neighbor in assigned
                )
            )
            if not choices:
                return False
            feasible[vertex] = choices
        vertex = min(
            feasible,
            key=lambda v: (
                len(feasible[v]),
                -len(h[v]),
                v,
            ),
        )
        for color in feasible[vertex]:
            assigned[vertex] = color
            if search():
                del assigned[vertex]
                return True
            del assigned[vertex]
        return False

    return search()


def exact_theta(h: tuple[frozenset[int], ...]) -> int:
    for number_of_colors in range(1, N + 1):
        if colorable(h, number_of_colors):
            return number_of_colors
    raise AssertionError("theta")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_csv_index(
    filename: str, *, with_added_edge: bool
) -> tuple[dict[tuple, dict[str, str]], list[str], list[str]]:
    path = SOURCE_DIR / filename
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    index = {}
    labeled = []
    reported_canonical = []
    for row in rows:
        mask = int(row["extension_h_mask"])
        if with_added_edge:
            key = (tuple(json.loads(row["added_h_edge"])), mask)
        else:
            key = (mask,)
        assert key not in index
        index[key] = row
        labeled.append(row["labeled_graph6"])
        reported_canonical.append(row["canonical_graph6"])
    return index, labeled, reported_canonical


def replay_canonicalization(
    labeled: list[str], reported: list[str]
) -> int:
    completed = subprocess.run(
        [str(LABELG), "-q"],
        input=("\n".join(labeled) + "\n").encode("ascii"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    recomputed = completed.stdout.decode("ascii").splitlines()
    assert recomputed == reported
    return len(set(recomputed))


def audit_scope(
    extras: tuple[tuple[int, int] | None, ...],
    csv_index: dict[tuple, dict[str, str]],
) -> dict:
    cases = 0
    positives = 0
    witness_total = 0
    parameters: Counter[tuple[int, int, int, int]] = Counter()
    positive_by_extra: Counter[str] = Counter()
    keys_seen = set()

    for extra in extras:
        for extension_mask in range(1 << OLD_N):
            key = (
                (extension_mask,)
                if extra is None
                else (extra, extension_mask)
            )
            assert key in csv_index
            keys_seen.add(key)
            cases += 1
            h_edges = make_h_edges(extension_mask, extra)
            h, g = adjacency(h_edges)
            triples = dominating_states(3, g)
            transitions = transition_table(triples, g)
            positive, witnesses = exact_predicate(h, g, triples, transitions)

            row = csv_index[key]
            reported_witnesses = int(
                row["augmentation_sensitive_witness_count"]
            )
            reported_positive = reported_witnesses > 0
            assert witnesses == reported_witnesses
            assert positive == reported_positive
            if not positive:
                continue

            positives += 1
            witness_total += witnesses
            positive_by_extra[
                "none" if extra is None else f"{extra[0]}-{extra[1]}"
            ] += 1
            parameter_tuple = (
                exact_gamma(g),
                exact_alpha(g),
                exact_gamma_infinity(g),
                exact_theta(h),
            )
            parameters[parameter_tuple] += 1
            assert parameter_tuple == (
                int(row["gamma"]),
                int(row["alpha"]),
                int(row["gamma_infinity"]),
                int(row["theta"]),
            )

    assert keys_seen == set(csv_index)
    return {
        "cases": cases,
        "predicate_positive": positives,
        "positive_witness_count": witness_total,
        "positive_parameter_counts": {
            ",".join(map(str, key)): count
            for key, count in sorted(parameters.items())
        },
        "positive_by_added_h_edge": dict(sorted(positive_by_extra.items())),
    }


def main() -> None:
    assert len(BASE_H_EDGES) == 9
    assert len(ALL_OLD_PAIRS) == 36
    assert len(ADDABLE_OLD_H_EDGES) == 27

    extension_index, extension_g6, extension_canonical = load_csv_index(
        "extensions.csv", with_added_edge=False
    )
    edge_index, edge_g6, edge_canonical = load_csv_index(
        "edge_additions.csv", with_added_edge=True
    )
    assert len(extension_index) == 512
    assert len(edge_index) == 27 * 512

    extensions = audit_scope((None,), extension_index)
    edge_additions = audit_scope(ADDABLE_OLD_H_EDGES, edge_index)

    assert extensions["predicate_positive"] == 99
    assert extensions["positive_parameter_counts"] == {
        "1,3,3,3": 1,
        "2,3,3,3": 98,
    }
    assert edge_additions["predicate_positive"] == 718
    assert edge_additions["positive_parameter_counts"] == {
        "1,3,3,3": 8,
        "2,3,3,3": 710,
    }

    # Positive anchor-target H-edge additions are exactly omissions already
    # present in the prescribed response lists.  Therefore no positive case
    # silently destroys a required one-guard move.
    allowed_anchor_target_h_edges = {
        edge(guard, target)
        for target, allowed in OLD_LISTS.items()
        for guard in allowed
    }
    positive_added_edges = {
        tuple(map(int, label.split("-")))
        for label in edge_additions["positive_by_added_h_edge"]
    }
    assert not (positive_added_edges & allowed_anchor_target_h_edges)

    extension_canonical_count = replay_canonicalization(
        extension_g6, extension_canonical
    )
    edge_canonical_count = replay_canonicalization(
        edge_g6, edge_canonical
    )
    assert extension_canonical_count == 160
    assert edge_canonical_count == 2099
    assert len(
        {
            row["canonical_graph6"]
            for row in extension_index.values()
            if int(row["augmentation_sensitive_witness_count"]) > 0
        }
    ) == 42
    assert len(
        {
            row["canonical_graph6"]
            for row in edge_index.values()
            if int(row["augmentation_sensitive_witness_count"]) > 0
        }
    ) == 275

    result = {
        "status": "PASS",
        "implementation": (
            "clean-room tuple/set one-guard kernel and coloring replay"
        ),
        "scope": {
            "one_vertex_extensions": extensions,
            "one_added_old_h_edge_extensions": edge_additions,
            "old_h_edge_choices": len(ADDABLE_OLD_H_EDGES),
            "extension_masks_per_choice": 1 << OLD_N,
        },
        "canonicalization_replay": {
            "one_vertex_extension_classes": extension_canonical_count,
            "one_added_old_h_edge_classes": edge_canonical_count,
            "positive_one_vertex_extension_classes": 42,
            "positive_one_added_old_h_edge_classes": 275,
        },
        "source_data_sha256": {
            "extensions.csv": sha256(SOURCE_DIR / "extensions.csv"),
            "edge_additions.csv": sha256(
                SOURCE_DIR / "edge_additions.csv"
            ),
        },
        "conclusion": (
            "Every predicate-positive labeled graph in both stated finite "
            "scopes has gamma at most two; no gamma-three equality control "
            "occurs."
        ),
    }
    output = REVIEW_DIR / "independent_result.json"
    output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
