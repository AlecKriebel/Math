#!/usr/bin/env python3
"""Independent hostile checker for the three-gate witness package.

This file deliberately imports no campaign evaluator, search code, or source
verifier.  The graph game is represented by integer masks, and its greatest
families are computed with a reverse-obligation queue rather than the source
verifier's repeated simultaneous-deletion loop.
"""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


N = 12
GRAPH6 = "KBn]r]vj]lnZ"
ANCHORS = (0, 1, 2)
H_EDGE_LIST = (
    (0, 1), (0, 2), (0, 3), (0, 7), (0, 11),
    (1, 2), (1, 4), (1, 8), (1, 9),
    (2, 5), (2, 6), (2, 10),
    (3, 7), (3, 9),
    (4, 8), (4, 10),
    (5, 6), (5, 11),
    (6, 9), (7, 10), (8, 11),
)
EXPECTED_LISTS = {
    3: (1, 2),
    4: (0, 2),
    5: (0, 1),
    6: (0, 1),
    7: (1, 2),
    8: (0, 2),
    9: (0, 2),
    10: (0, 1),
    11: (1, 2),
}
GATES = (
    (6, 3, 9, 1),
    (7, 4, 10, 2),
    (8, 5, 11, 0),
)
CONNECTORS = ((3, 7, 0), (4, 8, 1), (5, 6, 2))
CRITICAL_PAIRS = ((4, 6), (5, 7), (3, 8))


def edge(u: int, v: int) -> tuple[int, int]:
    assert u != v
    return (u, v) if u < v else (v, u)


H_EDGES = frozenset(edge(u, v) for u, v in H_EDGE_LIST)
ALL_EDGES = frozenset(combinations(range(N), 2))
G_EDGES = ALL_EDGES - H_EDGES


def masks_from_edges(edges: frozenset[tuple[int, int]]) -> tuple[int, ...]:
    rows = [0] * N
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


G_ADJ = masks_from_edges(G_EDGES)
H_ADJ = masks_from_edges(H_EDGES)
FULL = (1 << N) - 1


def vertices(mask: int) -> tuple[int, ...]:
    return tuple(v for v in range(N) if mask >> v & 1)


def subset_masks(size: int) -> tuple[int, ...]:
    return tuple(sum(1 << v for v in choice) for choice in combinations(range(N), size))


def dominates(mask: int) -> bool:
    covered = mask
    for v in vertices(mask):
        covered |= G_ADJ[v]
    return covered == FULL


def independent(mask: int) -> bool:
    rest = mask
    while rest:
        bit = rest & -rest
        rest ^= bit
        v = bit.bit_length() - 1
        if G_ADJ[v] & rest:
            return False
    return True


def connected() -> bool:
    reached = 1
    while True:
        expanded = reached
        for v in vertices(reached):
            expanded |= G_ADJ[v]
        if expanded == reached:
            return reached == FULL
        reached = expanded


def greatest_family_queue(size: int) -> frozenset[int]:
    """Compute the greatest eternal family by reverse obligation counts."""

    states = frozenset(mask for mask in subset_masks(size) if dominates(mask))
    alive = set(states)
    counts: dict[tuple[int, int], int] = {}
    reverse: dict[int, list[tuple[int, int]]] = defaultdict(list)

    for state in states:
        for attacked in range(N):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            successors = []
            for guard in vertices(state):
                if G_ADJ[guard] & attacked_bit:
                    successor = (state ^ (1 << guard)) | attacked_bit
                    if successor in states:
                        successors.append(successor)
            key = (state, attacked)
            counts[key] = len(successors)
            for successor in successors:
                reverse[successor].append(key)

    losing_count = defaultdict(int)
    queue: deque[int] = deque()
    queued: set[int] = set()
    for (state, _attacked), count in counts.items():
        if count == 0:
            losing_count[state] += 1
            if state not in queued:
                queue.append(state)
                queued.add(state)

    while queue:
        doomed = queue.popleft()
        if doomed not in alive:
            continue
        alive.remove(doomed)
        for key in reverse.get(doomed, ()):
            origin, _attacked = key
            if origin not in alive:
                continue
            counts[key] -= 1
            assert counts[key] >= 0
            if counts[key] == 0:
                losing_count[origin] += 1
                if origin not in queued:
                    queue.append(origin)
                    queued.add(origin)
    return frozenset(alive)


def graph6_decode(record: str) -> frozenset[tuple[int, int]]:
    assert ord(record[0]) - 63 == N
    bits = []
    for char in record[1:]:
        value = ord(char) - 63
        assert 0 <= value < 64
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    required = N * (N - 1) // 2
    assert len(bits) >= required
    decoded = []
    cursor = 0
    for high in range(1, N):
        for low in range(high):
            if bits[cursor]:
                decoded.append((low, high))
            cursor += 1
    assert all(bit == 0 for bit in bits[required:])
    return frozenset(decoded)


def graph6_encode(edges: frozenset[tuple[int, int]]) -> str:
    bits = [
        int((low, high) in edges)
        for high in range(1, N)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    chars = [chr(N + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = 2 * value + bit
        chars.append(chr(value + 63))
    return "".join(chars)


def family_bytes(family: frozenset[int]) -> bytes:
    rows = [
        ",".join(str(v) for v in vertices(mask))
        for mask in sorted(family, key=vertices)
    ]
    return "\n".join(rows).encode("ascii")


def family_obligations(
    family: frozenset[int],
) -> tuple[int, int, bytes]:
    obligations = 0
    legal_moves = 0
    rows = []
    for state in sorted(family, key=vertices):
        state_vertices = vertices(state)
        for attacked in range(N):
            attacked_bit = 1 << attacked
            if state & attacked_bit:
                continue
            legal = []
            for guard in state_vertices:
                if G_ADJ[guard] & attacked_bit:
                    successor = (state ^ (1 << guard)) | attacked_bit
                    if successor in family:
                        legal.append((guard, successor))
            assert legal
            obligations += 1
            legal_moves += len(legal)
            rows.append(
                f"{','.join(map(str, state_vertices))}|{attacked}|"
                + ";".join(
                    f"{guard}>{','.join(map(str, vertices(successor)))}"
                    for guard, successor in legal
                )
            )
    return obligations, legal_moves, "\n".join(rows).encode("ascii")


def exact_parameters(
    families: dict[int, frozenset[int]],
) -> dict[str, int]:
    gamma = next(
        size
        for size in range(1, N + 1)
        if any(dominates(mask) for mask in subset_masks(size))
    )
    alpha = next(
        size
        for size in range(N, 0, -1)
        if any(independent(mask) for mask in subset_masks(size))
    )
    i_number = next(
        size
        for size in range(1, N + 1)
        if any(
            independent(mask) and dominates(mask)
            for mask in subset_masks(size)
        )
    )
    gamma_infinity = min(size for size, family in families.items() if family)

    # A proper 3-coloring of H gives theta <= 3, while the anchor triangle
    # 0-1-2 in H gives theta >= 3.
    h_coloring = (0, 1, 2, 1, 0, 0, 1, 2, 2, 0, 1, 1)
    assert all(h_coloring[u] != h_coloring[v] for u, v in H_EDGES)
    assert all(edge(u, v) in H_EDGES for u, v in combinations(ANCHORS, 2))
    theta = 3
    return {
        "gamma": gamma,
        "i": i_number,
        "alpha": alpha,
        "gamma_infinity": gamma_infinity,
        "theta": theta,
    }


def direct_lists(family: frozenset[int]) -> dict[int, tuple[int, ...]]:
    anchor_mask = sum(1 << v for v in ANCHORS)
    result = {}
    for outside in range(3, N):
        result[outside] = tuple(
            omitted
            for omitted in ANCHORS
            if ((anchor_mask ^ (1 << omitted)) | (1 << outside)) in family
        )
    return result


def missing_vertices(mask: int) -> tuple[int, ...]:
    covered = mask
    for v in vertices(mask):
        covered |= G_ADJ[v]
    return vertices(FULL ^ covered)


# Symbolic audit of the two finite attack trees.  Only explicitly supplied
# H-edges can make a move illegal.  List omissions enter solely as absent
# family states, never as graph incidences.
Names = frozenset[str]


def named_state(*items: str) -> Names:
    return frozenset(items)


def named_edge(u: str, v: str) -> frozenset[str]:
    assert u != v
    return frozenset((u, v))


NAMED_H = {
    named_edge("a", "b"), named_edge("a", "c"), named_edge("b", "c"),
    named_edge("a", "a0"), named_edge("a", "a1"),
    named_edge("b", "b0"), named_edge("b", "b1"),
    named_edge("c", "c0"), named_edge("c", "c1"),
    named_edge("a0", "a1"), named_edge("b0", "b1"),
    named_edge("c0", "c1"),
    named_edge("b*", "b"), named_edge("b*", "a0"),
    named_edge("b*", "c1"),
    named_edge("c*", "c"), named_edge("c*", "a1"),
    named_edge("c*", "b0"),
    named_edge("a*", "a"), named_edge("a*", "b1"),
    named_edge("a*", "c0"),
    named_edge("q", "b0"), named_edge("q", "c1"),
}


class AttackAudit:
    def __init__(
        self,
        absent: set[Names],
        retained: set[Names],
        extra_h: tuple[frozenset[str], ...] = (),
    ) -> None:
        self.absent = absent
        self.retained = retained
        self.named_h = NAMED_H | set(extra_h)
        self.attacks = 0
        self.candidate_shapes = 0
        self.illegal_by_physical_h = 0
        self.killed_by_absence = 0
        self.nondomination_checks = 0

    def h_edge(self, u: str, v: str) -> bool:
        return named_edge(u, v) in self.named_h

    def nondominating(self, state: Names, witness: str) -> None:
        assert witness not in state
        assert all(self.h_edge(guard, witness) for guard in state)
        self.nondomination_checks += 1
        self.absent.add(state)

    def dead(self, state: Names, attacked: str) -> None:
        assert attacked not in state
        self.attacks += 1
        for guard in state:
            self.candidate_shapes += 1
            if self.h_edge(guard, attacked):
                self.illegal_by_physical_h += 1
                continue
            successor = (state - {guard}) | {attacked}
            assert successor in self.absent
            self.killed_by_absence += 1
        self.absent.add(state)

    def force_only(
        self,
        state: Names,
        attacked: str,
        target: Names,
    ) -> None:
        assert state in self.retained
        assert attacked not in state
        self.attacks += 1
        uneliminated = []
        for guard in state:
            self.candidate_shapes += 1
            successor = (state - {guard}) | {attacked}
            if self.h_edge(guard, attacked):
                self.illegal_by_physical_h += 1
            elif successor in self.absent:
                self.killed_by_absence += 1
            else:
                uneliminated.append(successor)
        assert uneliminated == [target]
        self.retained.add(target)


def audit_b_inclusion() -> dict[str, int]:
    # Contradict b not in L(q).  Type-b direct swaps omitting b are absent.
    assumed = named_state("a", "c", "q")
    absent = {
        assumed,
        named_state("a", "c", "b0"),
        named_state("a", "c", "b1"),
    }
    retained = {named_state("a", "c", "c0")}
    audit = AttackAudit(absent, retained)

    audit.nondominating(named_state("c", "c0", "q"), "c1")
    audit.force_only(
        named_state("a", "c", "c0"),
        "q",
        named_state("a", "c0", "q"),
    )

    audit.nondominating(named_state("a", "c0", "b1"), "a*")
    audit.dead(named_state("a", "b1", "q"), "c")

    audit.dead(named_state("c", "b1", "q"), "a")
    audit.dead(named_state("c", "b0", "q"), "a")
    audit.dead(named_state("c", "b0", "b1"), "a")
    audit.dead(named_state("b0", "b1", "q"), "c")
    audit.dead(named_state("c0", "b1", "q"), "b0")

    forced = named_state("a", "c0", "q")
    audit.dead(forced, "b1")
    assert forced in audit.retained and forced in audit.absent
    return {
        "attacks_checked": audit.attacks,
        "candidate_shapes_checked": audit.candidate_shapes,
        "illegal_by_explicit_H_edge": audit.illegal_by_physical_h,
        "killed_by_absent_successor": audit.killed_by_absence,
        "nondomination_checks": audit.nondomination_checks,
    }


def audit_c_inclusion() -> dict[str, int]:
    # Contradict c not in L(q).  Type-c direct swaps omitting c are absent.
    assumed = named_state("a", "b", "q")
    absent = {
        assumed,
        named_state("a", "b", "c0"),
        named_state("a", "b", "c1"),
    }
    retained = {named_state("a", "b", "b1")}
    audit = AttackAudit(absent, retained)

    audit.nondominating(named_state("b", "b1", "q"), "b0")
    audit.force_only(
        named_state("a", "b", "b1"),
        "q",
        named_state("a", "b1", "q"),
    )

    audit.nondominating(named_state("a", "b1", "c0"), "a*")
    audit.dead(named_state("a", "c0", "q"), "b")

    audit.dead(named_state("b", "c1", "q"), "a")
    audit.dead(named_state("b", "c0", "q"), "a")
    audit.dead(named_state("b", "c0", "c1"), "a")
    audit.dead(named_state("c0", "c1", "q"), "b")
    audit.dead(named_state("b1", "c0", "q"), "c1")

    forced = named_state("a", "b1", "q")
    audit.dead(forced, "c0")
    assert forced in audit.retained and forced in audit.absent
    return {
        "attacks_checked": audit.attacks,
        "candidate_shapes_checked": audit.candidate_shapes,
        "illegal_by_explicit_H_edge": audit.illegal_by_physical_h,
        "killed_by_absent_successor": audit.killed_by_absence,
        "nondomination_checks": audit.nondomination_checks,
    }


def audit_b1_collision() -> dict[str, int]:
    """Rule out b1 as a common H-neighbor of P_a."""

    absent = {
        named_state("a", "c", "b*"),
        named_state("a", "c", "b1"),
    }
    retained = {named_state("a", "c", "c0")}
    audit = AttackAudit(
        absent,
        retained,
        extra_h=(named_edge("b1", "c1"),),
    )
    audit.nondominating(named_state("c", "c0", "b*"), "c1")
    audit.force_only(
        named_state("a", "c", "c0"),
        "b*",
        named_state("a", "c0", "b*"),
    )
    audit.nondominating(named_state("a", "c0", "b1"), "a*")
    audit.dead(named_state("a", "b1", "b*"), "c")
    audit.nondominating(named_state("c0", "b1", "b*"), "c1")
    forced = named_state("a", "c0", "b*")
    audit.dead(forced, "b1")
    assert forced in audit.retained and forced in audit.absent
    return {
        "attacks_checked": audit.attacks,
        "candidate_shapes_checked": audit.candidate_shapes,
        "illegal_by_explicit_H_edge": audit.illegal_by_physical_h,
        "killed_by_absent_successor": audit.killed_by_absence,
        "nondomination_checks": audit.nondomination_checks,
    }


def audit_c0_collision() -> dict[str, int]:
    """Rule out c0 as a common H-neighbor of P_a."""

    absent = {
        named_state("a", "b", "c*"),
        named_state("a", "b", "c0"),
    }
    retained = {named_state("a", "b", "b1")}
    audit = AttackAudit(
        absent,
        retained,
        extra_h=(named_edge("c0", "b0"),),
    )
    audit.nondominating(named_state("b", "b1", "c*"), "b0")
    audit.force_only(
        named_state("a", "b", "b1"),
        "c*",
        named_state("a", "b1", "c*"),
    )
    audit.nondominating(named_state("a", "b1", "c0"), "a*")
    audit.dead(named_state("a", "c0", "c*"), "b")
    audit.nondominating(named_state("b1", "c0", "c*"), "b0")
    forced = named_state("a", "b1", "c*")
    audit.dead(forced, "c0")
    assert forced in audit.retained and forced in audit.absent
    return {
        "attacks_checked": audit.attacks,
        "candidate_shapes_checked": audit.candidate_shapes,
        "illegal_by_explicit_H_edge": audit.illegal_by_physical_h,
        "killed_by_absent_successor": audit.killed_by_absence,
        "nondomination_checks": audit.nondomination_checks,
    }


def cyclic_symmetry_check() -> bool:
    cycle = {
        "a": "b", "b": "c", "c": "a",
        "a0": "b0", "b0": "c0", "c0": "a0",
        "a1": "b1", "b1": "c1", "c1": "a1",
        "a*": "b*", "b*": "c*", "c*": "a*",
    }
    geometric_h = {item for item in NAMED_H if "q" not in item}
    mapped_h = {
        frozenset(cycle[vertex] for vertex in item)
        for item in geometric_h
    }
    assert mapped_h == geometric_h
    critical = (
        named_state("b0", "c1"),
        named_state("c0", "a1"),
        named_state("a0", "b1"),
    )
    assert tuple(
        frozenset(cycle[vertex] for vertex in item)
        for item in critical
    ) == critical[1:] + critical[:1]
    return True


def source_hashes(campaign: Path) -> dict[str, str]:
    source = campaign / "math" / "working" / "three_gate_odd_holonomy"
    result = {}
    for name in ("NOTE.md", "verify.py", "result.json", "RESEARCH_LOG.md"):
        result[name] = sha256((source / name).read_bytes()).hexdigest()
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    campaign = (
        args.campaign.resolve()
        if args.campaign is not None
        else Path(__file__).resolve().parents[2]
    )

    assert graph6_decode(GRAPH6) == G_EDGES
    assert graph6_encode(G_EDGES) == GRAPH6
    assert connected()

    families = {size: greatest_family_queue(size) for size in (1, 2, 3)}
    family = families[3]
    obligations, legal_moves, response_bytes = family_obligations(family)
    lists = direct_lists(family)
    assert lists == EXPECTED_LISTS

    boundary_evidence = []
    for left, right, cap, cap_type in GATES:
        boundary = (1 << left) | (1 << right) | (1 << cap_type)
        missing = missing_vertices(boundary)
        assert cap in missing
        assert not dominates(boundary)
        assert boundary not in family
        boundary_evidence.append(
            {
                "boundary": list(vertices(boundary)),
                "cap_witness": cap,
                "all_undominated_vertices": list(missing),
            }
        )

    for start, end, connector_type in CONNECTORS:
        assert edge(start, end) in H_EDGES
        assert connector_type not in lists[start]
        assert connector_type not in lists[end]

    pair_evidence = []
    for u, v in CRITICAL_PAIRS:
        mask = (1 << u) | (1 << v)
        common_h_neighbors = tuple(
            w
            for w in range(N)
            if w not in (u, v)
            and H_ADJ[u] >> w & 1
            and H_ADJ[v] >> w & 1
        )
        assert dominates(mask)
        assert common_h_neighbors == ()
        pair_evidence.append(
            {
                "pair": [u, v],
                "dominates_G": True,
                "common_H_neighbors": [],
            }
        )

    result = {
        "schema": "three-gate-odd-holonomy-hostile-review-v1",
        "verdict": "PASS",
        "source_sha256": source_hashes(campaign),
        "graph": {
            "graph6": GRAPH6,
            "order": N,
            "size": len(G_EDGES),
            "connected": True,
            "graph6_round_trip": True,
        },
        "parameters": exact_parameters(families),
        "greatest_family_sizes": {
            str(size): len(family_at_size)
            for size, family_at_size in families.items()
        },
        "greatest_triple_family_sha256": sha256(
            family_bytes(family)
        ).hexdigest(),
        "obligations": obligations,
        "legal_moves": legal_moves,
        "response_table_sha256": sha256(response_bytes).hexdigest(),
        "lists": {str(v): list(value) for v, value in lists.items()},
        "dead_boundaries": boundary_evidence,
        "critical_pair_sharpness": pair_evidence,
        "theorem_attack_tree_audits": {
            "b_in_Lq": audit_b_inclusion(),
            "c_in_Lq": audit_c_inclusion(),
        },
        "displayed_collision_audits": {
            "b1_cannot_witness_Pa": audit_b1_collision(),
            "c0_cannot_witness_Pa": audit_c0_collision(),
        },
        "cyclic_geometry_invariant": cyclic_symmetry_check(),
        "scope_checks": {
            "attacks_only_unoccupied": True,
            "exactly_one_guard_replaced_per_candidate": True,
            "list_omission_used_only_as_state_absence": True,
            "no_missing_response_as_nonedge_inference": True,
            "outside_q_distinctness_required": True,
            "control_is_boundary_only_not_complete_C098_gates": True,
            "no_universal_k3_claim": True,
        },
    }

    if args.check is not None:
        expected = json.loads(args.check.read_text(encoding="utf-8"))
        assert result == expected, "independent evidence mismatch"
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    print("PASS")


if __name__ == "__main__":
    main()
