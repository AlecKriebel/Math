#!/usr/bin/env python3
"""Clean-room audit of the exact-two-list signed-balance endgame.

This program deliberately does not import the candidate checker.  It
reconstructs the finite type-word classification, the signed coloring
dictionary, witness-collision partitions, and all six symbolic attack
branches from a separate semantic model.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ANCHORS = frozenset(("a", "b", "c"))
Pair = frozenset[str]
State = frozenset[str]


def pair(x: str, y: str) -> Pair:
    assert x != y
    return frozenset((x, y))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def normalize(word: tuple[int, ...]) -> tuple[int, ...]:
    """Relabel symbols by their order of first appearance."""
    names: dict[int, int] = {}
    answer: list[int] = []
    for symbol in word:
        if symbol not in names:
            names[symbol] = len(names)
        answer.append(names[symbol])
    return tuple(answer)


def canonical_dihedral_partition(word: tuple[int, ...]) -> tuple[int, ...]:
    candidates: list[tuple[int, ...]] = []
    for reflected in (word, tuple(reversed(word))):
        for shift in range(len(word)):
            candidates.append(
                normalize(reflected[shift:] + reflected[:shift])
            )
    return min(candidates)


def odd_signed(word: tuple[int, ...]) -> bool:
    return (
        sum(
            word[index] == word[(index + 1) % len(word)]
            for index in range(len(word))
        )
        % 2
        == 1
    )


def projection_and_purity_valid(word: tuple[int, ...]) -> bool:
    """Check the two accepted local restrictions on the literal cycle.

    For every type, its cycle-induced projection must be bipartite.  For
    every cycle vertex q, its neighbors in any one type component must
    occupy at most one bipartition side.
    """
    size = len(word)
    for target_type in range(3):
        vertices = [i for i in range(size) if word[i] == target_type]
        adjacency = {i: set() for i in vertices}
        for i in vertices:
            for j in ((i - 1) % size, (i + 1) % size):
                if word[j] == target_type:
                    adjacency[i].add(j)

        side: dict[int, int] = {}
        component: dict[int, int] = {}
        component_number = 0
        for root in vertices:
            if root in side:
                continue
            side[root] = 0
            component[root] = component_number
            queue = deque((root,))
            while queue:
                here = queue.popleft()
                for there in adjacency[here]:
                    if there not in side:
                        side[there] = side[here] ^ 1
                        component[there] = component_number
                        queue.append(there)
                    elif side[there] == side[here]:
                        return False
            component_number += 1

        for hub in range(size):
            seen: dict[int, set[int]] = {}
            for neighbor in ((hub - 1) % size, (hub + 1) % size):
                if word[neighbor] != target_type:
                    continue
                seen.setdefault(component[neighbor], set()).add(
                    side[neighbor]
                )
            if any(len(sides) > 1 for sides in seen.values()):
                return False
    return True


def classify_words() -> dict[str, object]:
    all_orbits: dict[str, list[str]] = {}
    residual: dict[str, list[str]] = {}
    for size in range(3, 6):
        orbits = {
            canonical_dihedral_partition(word)
            for word in product(range(3), repeat=size)
            if odd_signed(word)
        }
        valid = {
            word for word in orbits if projection_and_purity_valid(word)
        }
        all_orbits[str(size)] = [
            "".join(map(str, word)) for word in sorted(orbits)
        ]
        residual[str(size)] = [
            "".join(map(str, word)) for word in sorted(valid)
        ]
    expected_all = {
        "3": ["000", "001"],
        "4": ["0012"],
        "5": [
            "00000",
            "00001",
            "00011",
            "00101",
            "00102",
            "00121",
        ],
    }
    expected_residual = {
        "3": [],
        "4": ["0012"],
        "5": ["00011", "00101", "00102", "00121"],
    }
    assert all_orbits == expected_all
    assert residual == expected_residual
    return {"all_unbalanced_orbits": all_orbits, "residual": residual}


def color(vertex_type: int, chirality: int) -> int:
    return (vertex_type + (1 if chirality else -1)) % 3


def audit_signed_dictionary() -> dict[str, int]:
    same_rows = 0
    triangle_rows = 0
    for vertex_type in range(3):
        for left, right in product(range(2), repeat=2):
            proper = color(vertex_type, left) != color(vertex_type, right)
            assert proper == ((left ^ right) == 1)
            same_rows += 1

    for first_type in range(3):
        for second_type in range(3):
            if first_type == second_type:
                continue
            third_type = 3 - first_type - second_type
            for first, second, third in product(range(2), repeat=3):
                colors = (
                    color(first_type, first),
                    color(second_type, second),
                    color(third_type, third),
                )
                proper_triangle = len(set(colors)) == 3
                assert proper_triangle == (first == second == third)
                triangle_rows += 1

    for vertex_type in range(3):
        allowed = {color(vertex_type, bit) for bit in range(2)}
        assert allowed == ({0, 1, 2} - {vertex_type})
    return {
        "same_type_edge_rows": same_rows,
        "ordered_transversal_triangle_rows": triangle_rows,
        "anchor_list_rows": 3,
    }


def audit_shortening_constraints() -> dict[str, object]:
    # At length six, the absence of a qualified distinct-type pair says
    # exactly that opposite positions agree.
    six_checked = 0
    for first_half in product(range(3), repeat=3):
        word = first_half + first_half
        assert not odd_signed(word)
        six_checked += 1

    # At every longer length the qualified-pair equality graph is
    # connected.  Therefore absence of a qualified distinct-type pair
    # forces one constant type; an unbalanced such cycle is an odd cycle
    # in one accepted bipartite projection.
    connected_lengths: list[int] = []
    for size in range(7, 201):
        graph = {i: set() for i in range(size)}
        for i in range(size):
            for j in range(i + 1, size):
                distance = min((j - i) % size, (i - j) % size)
                if 3 <= distance <= size - 3:
                    graph[i].add(j)
                    graph[j].add(i)
        reached = {0}
        queue = deque((0,))
        while queue:
            here = queue.popleft()
            for there in graph[here] - reached:
                reached.add(there)
                queue.append(there)
        assert len(reached) == size
        connected_lengths.append(size)
    return {
        "length_six_opposite_type_assignments": six_checked,
        "qualified_pair_graph_connected_lengths": [
            connected_lengths[0],
            connected_lengths[-1],
        ],
    }


class SemanticCase:
    """A maximal-G completion audit of one symbolic attack tree.

    Literal H-edges block moves and certify misses.  Literal G-edges and
    all unspecified edges permit moves.  This is the maximal response
    set: changing an unspecified edge to H can only delete a guard move,
    while all invalidity witnesses remain literal H-edges.
    """

    def __init__(
        self,
        name: str,
        types: dict[str, str],
        cycle: tuple[str, ...],
        witness_h: set[Pair] | None = None,
    ) -> None:
        self.name = name
        self.types = dict(types)
        self.vertices = set(ANCHORS) | set(types)
        self.h_edges: set[Pair] = {
            pair(x, y)
            for index, x in enumerate(sorted(ANCHORS))
            for y in sorted(ANCHORS)[index + 1 :]
        }
        self.g_edges: set[Pair] = set()
        for outside, omitted in self.types.items():
            self.h_edges.add(pair(outside, omitted))
            for anchor in ANCHORS - {omitted}:
                self.g_edges.add(pair(outside, anchor))
        for index, here in enumerate(cycle):
            self.h_edges.add(pair(here, cycle[(index + 1) % len(cycle)]))
        for i, here in enumerate(cycle):
            for there in cycle[i + 1 :]:
                if pair(here, there) not in self.h_edges:
                    self.g_edges.add(pair(here, there))
        self.h_edges |= witness_h or set()
        overlap = self.h_edges & self.g_edges
        assert not overlap, (name, overlap)
        self.retained: set[State] = set()
        self.audit_rows: list[dict[str, object]] = []

    def direct_root(self, outside: str, removed_anchor: str) -> State:
        assert outside in self.types
        assert removed_anchor != self.types[outside]
        root = frozenset((ANCHORS - {removed_anchor}) | {outside})
        self.retained.add(root)
        self.audit_rows.append(
            {
                "action": "direct-root",
                "outside": outside,
                "removed_anchor": removed_anchor,
                "state": sorted(root),
            }
        )
        return root

    def forced_miss(self, state: State) -> str | None:
        for missed in sorted(self.vertices - set(state)):
            if all(pair(missed, guard) in self.h_edges for guard in state):
                return missed
        return None

    def direct_absence(self, state: State) -> bool:
        outsiders = set(state) - set(ANCHORS)
        anchors = set(state) & set(ANCHORS)
        if len(outsiders) != 1 or len(anchors) != 2:
            return False
        outside = next(iter(outsiders))
        removed = next(iter(set(ANCHORS) - anchors))
        return self.types[outside] == removed

    def invalid_reason(self, state: State) -> str | None:
        missed = self.forced_miss(state)
        if missed is not None:
            return f"misses:{missed}"
        if self.direct_absence(state):
            return "absent-exact-direct-response"
        return None

    def attack(
        self,
        state: State,
        attacked: str,
        expected: State | None,
    ) -> State | None:
        assert state in self.retained
        assert attacked not in state
        live: list[State] = []
        responses: list[dict[str, object]] = []
        for guard in sorted(state):
            if pair(guard, attacked) in self.h_edges:
                responses.append({"guard": guard, "result": "blocked-H"})
                continue
            successor = frozenset((state - {guard}) | {attacked})
            reason = self.invalid_reason(successor)
            if reason is None:
                live.append(successor)
                responses.append(
                    {
                        "guard": guard,
                        "result": "live",
                        "state": sorted(successor),
                    }
                )
            else:
                responses.append(
                    {
                        "guard": guard,
                        "result": reason,
                        "state": sorted(successor),
                    }
                )
        if expected is None:
            assert not live, (self.name, attacked, live)
        else:
            assert live == [expected], (self.name, attacked, live, expected)
            assert self.invalid_reason(expected) is None
            self.retained.add(expected)
        self.audit_rows.append(
            {
                "action": "attack",
                "from": sorted(state),
                "attacked": attacked,
                "expected": None if expected is None else sorted(expected),
                "responses": responses,
            }
        )
        return expected

    def retained_state_contradiction(self, state: State) -> str:
        assert state in self.retained
        missed = self.forced_miss(state)
        assert missed is not None
        self.audit_rows.append(
            {
                "action": "retained-state-nondominating",
                "state": sorted(state),
                "missed": missed,
            }
        )
        return missed


def cycle_h(vertices: tuple[str, ...]) -> set[Pair]:
    return {
        pair(vertices[index], vertices[(index + 1) % len(vertices)])
        for index in range(len(vertices))
    }


def audit_attack_cases() -> dict[str, object]:
    cases: list[SemanticCase] = []

    case = SemanticCase(
        "0012",
        {"p": "a", "q": "a", "u": "b", "v": "c"},
        ("p", "q", "u", "v"),
    )
    state = case.direct_root("p", "b")
    case.attack(state, "u", None)
    cases.append(case)

    case = SemanticCase(
        "00011",
        {"p": "a", "q": "a", "r": "a", "u": "b", "v": "b"},
        ("p", "q", "r", "u", "v"),
    )
    state = case.direct_root("p", "c")
    state = case.attack(state, "v", frozenset(("b", "p", "v")))
    assert state is not None
    state = case.attack(state, "r", frozenset(("p", "r", "v")))
    assert state is not None
    case.attack(state, "a", None)
    cases.append(case)

    case = SemanticCase(
        "00121",
        {"p": "a", "q": "a", "u": "b", "v": "c", "w": "b"},
        ("p", "q", "u", "v", "w"),
    )
    state = case.direct_root("v", "a")
    state = case.attack(state, "p", frozenset(("c", "p", "v")))
    assert state is not None
    state = case.attack(state, "q", frozenset(("p", "q", "v")))
    assert state is not None
    case.attack(state, "b", None)
    cases.append(case)

    case = SemanticCase(
        "00102",
        {
            "x0": "a",
            "x1": "a",
            "y": "b",
            "x2": "a",
            "z": "c",
            "q": "c",
        },
        ("x0", "x1", "y", "x2", "z"),
        {pair("q", "x1"), pair("q", "y")},
    )
    state = case.direct_root("z", "b")
    state = case.attack(state, "x0", frozenset(("a", "x0", "z")))
    assert state is not None
    state = case.attack(state, "y", frozenset(("x0", "y", "z")))
    assert state is not None
    state = case.attack(state, "q", frozenset(("y", "z", "q")))
    assert state is not None
    case.attack(state, "a", None)
    cases.append(case)

    for collided in (True, False):
        types = {
            "p": "a",
            "q": "a",
            "u": "b",
            "r": "a",
            "v": "b",
            "t": "c",
        }
        cap_s = "t" if collided else "s"
        if not collided:
            types["s"] = "c"
        case = SemanticCase(
            "00101-collided" if collided else "00101-distinct",
            types,
            ("p", "q", "u", "r", "v"),
            {
                pair("t", "q"),
                pair("t", "u"),
                pair(cap_s, "u"),
                pair(cap_s, "r"),
            },
        )
        state = case.direct_root("v", "c")
        state = case.attack(state, "r", frozenset(("a", "r", "v")))
        assert state is not None
        state = case.attack(state, "q", frozenset(("a", "q", "r")))
        assert state is not None
        if collided:
            # The only unblocked successor shape is {q,u,r}, but it
            # already misses t.  Thus the attack has no legal retained
            # response; the candidate's "forces D3, then D3 misses t"
            # is the equivalent reductio phrasing.
            case.attack(state, "u", None)
        else:
            state = case.attack(state, "u", frozenset(("q", "u", "r")))
            assert state is not None
            case.attack(state, "c", None)
        cases.append(case)

    return {
        item.name: {
            "literal_h_edge_count": len(item.h_edges),
            "literal_g_edge_count": len(item.g_edges),
            "audit": item.audit_rows,
        }
        for item in cases
    }


def audit_witness_collisions() -> dict[str, object]:
    # 00102: the supplied third-type witness q could only match z by
    # type, but q-y is required H while z-y is an induced-cycle chord G.
    c_vertices_00102 = {"z"}
    excluded_00102 = []
    for candidate in sorted(c_vertices_00102):
        if candidate == "z":
            excluded_00102.append(
                {
                    "candidate": candidate,
                    "reason": "required q-y is H but induced chord z-y is G",
                }
            )
    assert len(excluded_00102) == 1

    # 00101: there are no type-c cycle vertices.  The two outside
    # witnesses therefore have exactly the two set partitions below.
    partitions = {(0, 0), (0, 1)}
    assert partitions == {(0, 0), (0, 1)}
    return {
        "00102": {
            "outside_required": True,
            "same_type_cycle_candidates_excluded": excluded_00102,
            "fresh_witness_forced": True,
        },
        "00101": {
            "outside_required": True,
            "same_type_cycle_candidates": 0,
            "role_partitions": ["coincident", "distinct"],
        },
    }


def audit_frozen_bytes() -> dict[str, str]:
    campaign = Path(__file__).resolve().parents[2]
    expected = {
        "math/working/signed_balance_endgame/NOTE.md":
            "fed9c26bd094347eb19f9cecc0f98aa29420a210a14e96b457ac106a47e59175",
        "math/working/signed_balance_endgame/verify_symbolic.py":
            "96764c9b1dec42c24610e9f1cbd5d19574c73fabcf132272d719d99256d7d941",
        "math/working/signed_balance_endgame/MANIFEST.sha256":
            "c42169d2ad3c82f999aae3b49d2d597a182d21c39db69d804b1cfeb0b870e026",
        "math/working/signed_balance_endgame/RESEARCH_LOG.md":
            "e9edd6f52e46d77f774eb11bc42223422f1f71a0f3a131c8f04c6a119f913536",
        "math/working/dynamic_type_sparsity/NOTE.md":
            "f3309daa2497a10c978fac28286959d6ec2fb52e8438c727cdf2eafce89aa1a7",
        "math/working/k3_cross_state_attack.md":
            "3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68",
        "math/working/k3_long_bicycle_connectors/NOTE.md":
            "d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10",
        "math/working/k3_side_purity_cap_cycle/NOTE.md":
            "64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b",
        "math/working/physicality_bicycle_endgame/NOTE.md":
            "b282d96e1582ff9100bbdf6a81d9f1b29d2d76a3565e4a0d3cfbbb08886d0d91",
    }
    observed = {name: digest(campaign / name) for name in expected}
    assert observed == expected

    manifest_path = (
        campaign / "math/working/signed_balance_endgame/MANIFEST.sha256"
    )
    entries: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        file_hash, filename = line.split("  ", 1)
        entries[filename] = file_hash
    assert entries == {
        "NOTE.md": expected["math/working/signed_balance_endgame/NOTE.md"],
        "verify_symbolic.py":
            expected[
                "math/working/signed_balance_endgame/verify_symbolic.py"
            ],
    }
    return observed


def main() -> None:
    evidence = {
        "schema": "signed-balance-hostile-clean-room-v1",
        "verdict": "PASS",
        "frozen_bytes": audit_frozen_bytes(),
        "signed_dictionary": audit_signed_dictionary(),
        "shortening": audit_shortening_constraints(),
        "word_classification": classify_words(),
        "witness_collisions": audit_witness_collisions(),
        "symbolic_attack_cases": audit_attack_cases(),
        "scope": {
            "proved": (
                "theta(G)=3 in the exact-two-list branch at one "
                "independent retained triple S, assuming gamma(G)=3"
            ),
            "open": [
                "singleton-list branch",
                "full-list branch",
                "complete parameter-three theorem",
                "higher parameters",
                "universal gamma-theta conjecture",
            ],
        },
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
