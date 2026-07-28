#!/usr/bin/env python3
"""Clean-room audit for the global-witness-cascade candidate.

This file imports neither the campaign evaluator nor any search or verifier
from the candidate directory.  It checks the frozen source manifest, replays
the local physical-witness attack certificate symbolically, and independently
reconstructs the 21-vertex graph, parameters, eternal family, response data,
canonical gates, critical witnesses, and greatest triple kernel.
"""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


CAMPAIGN = Path(__file__).resolve().parents[2]
CANDIDATE = CAMPAIGN / "math/working/global_witness_cascade"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def decode_graph6(record: str) -> tuple[int, list[int]]:
    raw = record.encode("ascii")
    if not raw or raw[0] < 63 or raw[0] > 125:
        raise AssertionError("malformed graph6 header")
    if raw[0] == 126:
        raise AssertionError("long graph6 header not needed by this control")
    n = raw[0] - 63
    payload = []
    for char in raw[1:]:
        value = char - 63
        assert 0 <= value < 64
        payload.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    pairs = [(u, v) for v in range(1, n) for u in range(v)]
    assert len(payload) >= len(pairs)
    assert not any(payload[len(pairs) :])
    adjacency = [0] * n
    for present, (u, v) in zip(payload, pairs):
        if present:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return n, adjacency


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def state_mask(state) -> int:
    value = 0
    for vertex in state:
        bit = 1 << int(vertex)
        assert not (value & bit)
        value |= bit
    return value


def adjacent(adjacency: list[int], u: int, v: int) -> bool:
    return bool(adjacency[u] & (1 << v))


def dominates(adjacency: list[int], state: int) -> bool:
    covered = state
    for guard in vertices(state):
        covered |= adjacency[guard]
    return covered == (1 << len(adjacency)) - 1


def independent(adjacency: list[int], state: int) -> bool:
    return all(not (adjacency[u] & state) for u in vertices(state))


def successor(state: int, mover: int, attacked: int) -> int:
    assert state & (1 << mover)
    assert not (state & (1 << attacked))
    return (state ^ (1 << mover)) | (1 << attacked)


def greatest_kernel(adjacency: list[int], k: int) -> tuple[set[int], int]:
    n = len(adjacency)
    alive = {
        state_mask(state)
        for state in combinations(range(n), k)
        if dominates(adjacency, state_mask(state))
    }
    rounds = 0
    while True:
        remove = set()
        for state in alive:
            for attacked in range(n):
                if state & (1 << attacked):
                    continue
                if not any(
                    adjacent(adjacency, mover, attacked)
                    and successor(state, mover, attacked) in alive
                    for mover in vertices(state)
                ):
                    remove.add(state)
                    break
        if not remove:
            return alive, rounds
        alive.difference_update(remove)
        rounds += 1


def symbolic_physical_witness_certificate() -> dict[str, int]:
    """Validate every state/attack branch in Theorem 2.1."""
    names = ("a", "b", "c", "x", "u", "v", "y", "s", "t", "o", "m", "q")
    assert len(set(names)) == len(names)

    def st(*items: str) -> frozenset[str]:
        assert len(set(items)) == len(items)
        return frozenset(items)

    h_edges = {
        frozenset(edge)
        for edge in (
            ("a", "b"),
            ("a", "c"),
            ("b", "s"),
            ("x", "s"),
            ("u", "s"),
            ("a", "v"),
            ("u", "v"),
            ("v", "t"),
            ("y", "t"),
            ("v", "o"),
            ("o", "m"),
            ("m", "y"),
            ("a", "q"),
            ("x", "q"),
            ("y", "q"),
        )
    }

    absent = {
        st("a", "b", "x"),  # c not in L(x)
        st("a", "b", "t"),  # c not in L(t)
        st("a", "c", "y"),  # b not in L(y)
        st("a", "c", "o"),  # b not in L(o)
        st("a", "c", "m"),  # b not in L(m)
    }
    present = {st("a", "b", "u")}  # c in L(u)
    dead_attacks = 0
    nondomination_checks = 0
    forcing_attacks = 0

    def edge_h(u: str, v: str) -> bool:
        return frozenset((u, v)) in h_edges

    def add_nondominating(state: frozenset[str], missed: str) -> None:
        nonlocal nondomination_checks
        assert missed not in state
        assert all(edge_h(guard, missed) for guard in state)
        absent.add(state)
        nondomination_checks += 1

    def prove_dead(state: frozenset[str], attacked: str) -> None:
        nonlocal dead_attacks
        assert attacked not in state
        for mover in state:
            if edge_h(mover, attacked):
                continue
            nxt = (state - {mover}) | {attacked}
            assert nxt in absent, (state, attacked, mover, nxt)
        absent.add(state)
        dead_attacks += 1

    def force(state: frozenset[str], attacked: str, expected: frozenset[str]):
        nonlocal forcing_attacks
        assert state in present
        assert attacked not in state
        possible_shapes = []
        for mover in state:
            nxt = (state - {mover}) | {attacked}
            if edge_h(mover, attacked) or nxt in absent:
                continue
            possible_shapes.append(nxt)
        assert possible_shapes == [expected] or set(possible_shapes) == {expected}
        present.add(expected)
        forcing_attacks += 1

    # Immediate nondominating shapes.
    add_nondominating(st("b", "u", "x"), "s")
    add_nondominating(st("a", "u", "t"), "v")
    add_nondominating(st("u", "t", "o"), "v")
    add_nondominating(st("a", "t", "o"), "v")
    add_nondominating(st("a", "x", "y"), "q")

    # Dead-state ladder, in dependency order.
    prove_dead(st("a", "x", "t"), "b")
    prove_dead(st("c", "y", "o"), "a")
    prove_dead(st("c", "y", "m"), "a")
    prove_dead(st("c", "o", "m"), "a")
    prove_dead(st("y", "o", "m"), "c")
    prove_dead(st("y", "t", "o"), "m")
    prove_dead(st("u", "y", "o"), "m")
    prove_dead(st("u", "y", "t"), "o")
    prove_dead(st("a", "y", "o"), "c")
    prove_dead(st("a", "y", "t"), "o")

    # The three forced retained states.
    force(st("a", "b", "u"), "x", st("a", "u", "x"))
    force(st("a", "u", "x"), "t", st("u", "x", "t"))
    force(st("u", "x", "t"), "y", st("x", "y", "t"))

    # Every possible response to the final attack is excluded.
    final_state = st("x", "y", "t")
    assert final_state in present
    prove_dead(final_state, "a")

    return {
        "dead_state_attacks": dead_attacks,
        "nondomination_checks": nondomination_checks,
        "forcing_attacks": forcing_attacks,
        "known_absent_states": len(absent),
    }


def check_control(data: dict) -> dict:
    n, g_adj = decode_graph6(str(data["graph6"]))
    assert n == int(data["order"]) == 21
    all_mask = (1 << n) - 1
    h_adj = [
        (all_mask ^ (1 << u) ^ g_adj[u])
        for u in range(n)
    ]
    declared_h = {
        tuple(sorted(map(int, edge))) for edge in data["h_edges"]
    }
    decoded_h = {
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if adjacent(h_adj, u, v)
    }
    assert declared_h == decoded_h
    g_size = sum(mask.bit_count() for mask in g_adj) // 2
    assert g_size == int(data["size"]) == 174

    raw_family = [tuple(map(int, state)) for state in data["selected_family"]]
    assert all(tuple(sorted(state)) == state and len(state) == 3 for state in raw_family)
    assert len(raw_family) == len(set(raw_family)) == int(data["selected_family_size"])
    serialization = "\n".join(",".join(map(str, s)) for s in sorted(raw_family))
    assert sha256(serialization.encode("ascii")).hexdigest() == data[
        "selected_family_sha256"
    ]
    family = {state_mask(state) for state in raw_family}
    assert all(dominates(g_adj, state) for state in family)

    obligations = 0
    legal_responses = 0
    for state in family:
        for attacked in range(n):
            if state & (1 << attacked):
                continue
            obligations += 1
            count = sum(
                adjacent(g_adj, mover, attacked)
                and successor(state, mover, attacked) in family
                for mover in vertices(state)
            )
            assert count >= 1
            legal_responses += count
    assert obligations == 15_174

    # Exact domination and independent-domination parameters.
    dominating_singletons = [
        (u,) for u in range(n) if dominates(g_adj, 1 << u)
    ]
    dominating_pairs = [
        pair
        for pair in combinations(range(n), 2)
        if dominates(g_adj, state_mask(pair))
    ]
    independent_dominating_pairs = [
        pair for pair in dominating_pairs if independent(g_adj, state_mask(pair))
    ]
    assert not dominating_singletons
    assert len(dominating_pairs) == int(data["dominating_pair_count"]) == 114
    assert independent_dominating_pairs
    gamma = 2
    independent_domination = 2

    anchor = state_mask((0, 1, 2))
    assert independent(g_adj, anchor)
    assert not any(
        independent(g_adj, state_mask(state))
        for state in combinations(range(n), 4)
    )
    alpha = 3

    # A supplied proper 3-coloring of H plus the anchor H-triangle proves
    # theta=chi(H)=3 without importing a coloring solver.
    coloring = list(map(int, data["h_coloring"]))
    assert len(coloring) == n
    assert set(coloring) <= {0, 1, 2}
    assert all(coloring[u] != coloring[v] for u, v in decoded_h)
    assert all(adjacent(h_adj, u, v) for u, v in combinations((0, 1, 2), 2))
    theta = 3

    kernel_one, rounds_one = greatest_kernel(g_adj, 1)
    kernel_two, rounds_two = greatest_kernel(g_adj, 2)
    kernel, kernel_rounds = greatest_kernel(g_adj, 3)
    assert not kernel_one
    assert not kernel_two
    assert len(kernel) == int(data["greatest_triple_family_size"]) == 1_237
    assert family <= kernel
    gamma_infinity = 3

    lists = {}
    for outside in range(3, n):
        responders = []
        for omitted in range(3):
            direct = (anchor ^ (1 << omitted)) | (1 << outside)
            if direct in family:
                responders.append(omitted)
        lists[outside] = responders
    expected_lists = {
        int(vertex): list(map(int, responders))
        for vertex, responders in data["direct_lists"].items()
    }
    assert lists == expected_lists
    assert all(len(response_list) == 2 for response_list in lists.values())

    # Canonical complete gates, reconstructed directly from the notation.
    gates = (
        # left, right, cap, original, middle, left anchor, right anchor,
        # cap anchor
        (6, 3, 9, 12, 15, 2, 0, 1),
        (7, 4, 10, 13, 16, 0, 1, 2),
        (8, 5, 11, 14, 17, 1, 2, 0),
    )
    for left, right, cap, original, middle, la, ra, ca in gates:
        required_h = (
            (la, left),
            (ra, right),
            (ca, cap),
            (left, cap),
            (right, cap),
            (left, original),
            (original, middle),
            (middle, right),
        )
        assert all(adjacent(h_adj, u, v) for u, v in required_h)
        assert adjacent(g_adj, left, right)  # failed direct incidence
    for u, v in ((3, 7), (4, 8), (5, 6)):
        assert adjacent(h_adj, u, v)

    critical = (
        # anchor, endpoint 1, endpoint 2, dynamic witness, exact list
        (0, 4, 6, 18, [1, 2]),
        (1, 5, 7, 19, [0, 2]),
        (2, 3, 8, 20, [0, 1]),
    )
    critical_checks = []
    for anchor_vertex, u, v, witness, response_list in critical:
        common_h = [
            w
            for w in range(n)
            if w not in (u, v)
            and adjacent(h_adj, u, w)
            and adjacent(h_adj, v, w)
        ]
        assert common_h == [witness]
        assert adjacent(g_adj, anchor_vertex, witness)
        assert lists[witness] == response_list
        anchor_pair_common_h = [
            w
            for w in range(n)
            if w not in (anchor_vertex, witness)
            and adjacent(h_adj, anchor_vertex, w)
            and adjacent(h_adj, witness, w)
        ]
        assert not anchor_pair_common_h
        assert dominates(g_adj, state_mask((anchor_vertex, witness)))
        critical_checks.append(
            {
                "pair": [u, v],
                "witness": witness,
                "dynamic_anchor": anchor_vertex,
            }
        )

    assert data["parameters"] == {
        "alpha": alpha,
        "gamma": gamma,
        "gamma_infinity": gamma_infinity,
        "i": independent_domination,
        "theta": theta,
    }

    return {
        "order": n,
        "size": g_size,
        "parameters": data["parameters"],
        "selected_family_size": len(family),
        "attack_obligations": obligations,
        "legal_retained_responses": legal_responses,
        "dominating_pair_count": len(dominating_pairs),
        "independent_dominating_pair_count": len(independent_dominating_pairs),
        "greatest_triple_kernel_size": len(kernel),
        "greatest_kernel_deletion_rounds": kernel_rounds,
        "one_guard_kernel_size": len(kernel_one),
        "one_guard_kernel_deletion_rounds": rounds_one,
        "two_guard_kernel_size": len(kernel_two),
        "two_guard_kernel_deletion_rounds": rounds_two,
        "critical_witnesses": critical_checks,
    }


def main() -> None:
    manifest = json.loads((CANDIDATE / "MANIFEST.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        assert digest(CANDIDATE / name) == expected
    note_hash = digest(CANDIDATE / "NOTE.md")
    assert note_hash == "1f0e2b5fce583dbc5a485ec7aa767204cd1c581a737cd6256e77224d4cdb2a32"

    data = json.loads(
        (CANDIDATE / "dynamic_three_witness_control.json").read_text()
    )
    result = {
        "verdict": "PASS",
        "candidate_note_sha256": note_hash,
        "manifest_sha256": digest(CANDIDATE / "MANIFEST.json"),
        "symbolic_physical_witness_certificate": (
            symbolic_physical_witness_certificate()
        ),
        "control": check_control(data),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
