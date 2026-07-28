#!/usr/bin/env python3
"""Clean-room audit of the rank-one QQ1/AQ1 normalization.

This file deliberately imports neither the candidate checker nor either
campaign verifier.  It has two independent jobs:

1. enumerate every optional named incidence in the QQ1 and AQ1 cores and
   replay the proof's collision, attack-tree, ridge-permutation, activity,
   and completion implications with ordinary Python sets; and
2. decode and exactly evaluate the fixed Graph6 boundary control Hslaghb.

The accepted theorems C-010, C-064, C-108, and C-150 remain mathematical
dependencies.  Their consequences are instantiated explicitly below.
"""

from __future__ import annotations

import functools
import hashlib
import itertools
import json


GRAPH6 = "Hslaghb"


def pair(left: str, right: str) -> frozenset[str]:
    assert left != right
    return frozenset((left, right))


def has(edges: set[frozenset[str]], left: str, right: str) -> bool:
    return left != right and pair(left, right) in edges


def movers(
    edges: set[frozenset[str]], state: frozenset[str], target: str
) -> tuple[str, ...]:
    assert target not in state
    return tuple(
        sorted(guard for guard in state if has(edges, guard, target))
    )


def move(
    state: frozenset[str], guard: str, target: str
) -> frozenset[str]:
    assert guard in state and target not in state
    return (state - {guard}) | {target}


def misses(
    edges: set[frozenset[str]], state: frozenset[str], vertex: str
) -> bool:
    assert vertex not in state
    return all(not has(edges, guard, vertex) for guard in state)


def independent(
    edges: set[frozenset[str]], state: frozenset[str]
) -> bool:
    return all(
        not has(edges, left, right)
        for left, right in itertools.combinations(state, 2)
    )


def canonical_permutation(
    path: tuple[frozenset[str], ...]
) -> dict[str, str]:
    """Return the C-064 product from the first state to the last."""

    mapping: dict[str, str] = {}

    def image(vertex: str) -> str:
        return mapping.get(vertex, vertex)

    for source, target in zip(path, path[1:]):
        departing = tuple(source - target)
        entering = tuple(target - source)
        assert len(departing) == len(entering) == 1
        old, new = departing[0], entering[0]
        universe = set(mapping) | set(mapping.values()) | {old, new}
        step = {old: new, new: old}
        mapping = {
            vertex: step.get(image(vertex), image(vertex))
            for vertex in universe
            if step.get(image(vertex), image(vertex)) != vertex
        }
    return mapping


def image(permutation: dict[str, str], vertex: str) -> str:
    return permutation.get(vertex, vertex)


def base_edges(case: str) -> tuple[
    tuple[str, ...],
    set[frozenset[str]],
    set[frozenset[str]],
    tuple[frozenset[str], ...],
]:
    if case == "AQ1":
        vertices = ("u", "x", "p", "q", "r", "a", "b", "c")
        present = {
            pair("u", "x"),
            pair("u", "r"),
            pair("p", "r"),
            pair("q", "r"),
            pair("x", "r"),
            pair("a", "u"),
            pair("a", "x"),
            pair("b", "p"),
            pair("c", "q"),
        }
        absent = {
            pair("x", "p"),
            pair("x", "q"),
            pair("p", "q"),
            pair("a", "r"),
            pair("a", "p"),
            pair("a", "q"),
            pair("b", "u"),
            pair("b", "r"),
            pair("b", "q"),
            pair("c", "u"),
            pair("c", "r"),
            pair("c", "p"),
        }
        optional = tuple(
            pair(*edge)
            for edge in (
                ("a", "b"),
                ("a", "c"),
                ("b", "c"),
                ("x", "b"),
                ("x", "c"),
                ("u", "p"),
                ("u", "q"),
            )
        )
    elif case == "QQ1":
        # The collision a=x is represented literally: there is no a label.
        vertices = ("u", "x", "p", "q", "r", "b", "c")
        present = {
            pair("u", "x"),
            pair("u", "r"),
            pair("p", "r"),
            pair("q", "r"),
            pair("b", "p"),
            pair("c", "q"),
        }
        absent = {
            pair("x", "p"),
            pair("x", "q"),
            pair("p", "q"),
            pair("x", "r"),
            pair("b", "u"),
            pair("b", "r"),
            pair("b", "q"),
            pair("c", "u"),
            pair("c", "r"),
            pair("c", "p"),
        }
        optional = tuple(
            pair(*edge)
            for edge in (
                ("x", "b"),
                ("x", "c"),
                ("b", "c"),
                ("u", "p"),
                ("u", "q"),
            )
        )
    else:
        raise ValueError(case)
    assert not (present & absent)
    all_pairs = {
        pair(left, right)
        for left, right in itertools.combinations(vertices, 2)
    }
    assert all_pairs == present | absent | set(optional)
    return vertices, present, absent, optional


def named_assignments(case: str):
    _, present, _, optional = base_edges(case)
    for bits in itertools.product((False, True), repeat=len(optional)):
        edges = set(present)
        edges.update(
            edge for bit, edge in zip(bits, optional) if bit
        )
        yield edges


def audit_private_ledger(case: str, edges: set[frozenset[str]]) -> None:
    """Reconstruct the C-150 private-witness incidences."""

    root = "x" if case == "QQ1" else "a"
    assert has(edges, root, "u")
    for missed in ("r", "p", "q"):
        assert not has(edges, root, missed)
    assert has(edges, "b", "p")
    for missed in ("u", "r", "q"):
        assert not has(edges, "b", missed)
    assert has(edges, "c", "q")
    for missed in ("u", "r", "p"):
        assert not has(edges, "c", missed)


def audit_forced_chain(case: str, edges: set[frozenset[str]]) -> None:
    """Check completeness of the M_q -> U -> R -> S forcing."""

    mq = frozenset(("x", "p", "c"))
    w = frozenset(("x", "b", "c"))
    u_state = frozenset(("u", "b", "c"))
    r_state = frozenset(("r", "b", "c"))

    # Every possible b-responder from M_q is either immediately
    # non-dominating or, if retained, forces U at the next attack on u.
    for guard in movers(edges, mq, "b"):
        successor = move(mq, guard, "b")
        if guard == "c":
            assert successor == frozenset(("x", "p", "b"))
            assert misses(edges, successor, "q")
        elif guard == "p":
            assert successor == w
            assert movers(edges, successor, "u") == ("x",)
            assert move(successor, "x", "u") == u_state
        elif guard == "x":
            assert successor == frozenset(("b", "p", "c"))
            if has(edges, "p", "u"):
                assert movers(edges, successor, "u") == ("p",)
                assert move(successor, "p", "u") == u_state
            else:
                assert misses(edges, successor, "u")
        else:
            raise AssertionError(guard)
    assert "p" in movers(edges, mq, "b")

    # Once U is forced, r has exactly one responder.
    assert movers(edges, u_state, "r") == ("u",)
    assert move(u_state, "u", "r") == r_state

    if case == "AQ1":
        # Any retained a-response from R forces S along one of two complete
        # unique-response paths.  R's retention also forces at least one of
        # b,c to be eligible.
        response_guards = movers(edges, r_state, "a")
        for guard in response_guards:
            assert guard in ("b", "c")
            first = move(r_state, guard, "a")
            if guard == "b":
                assert movers(edges, first, "p") == ("r",)
                second = move(first, "r", "p")
                assert movers(edges, second, "q") == ("c",)
                terminal = move(second, "c", "q")
            else:
                assert movers(edges, first, "q") == ("r",)
                second = move(first, "r", "q")
                assert movers(edges, second, "p") == ("b",)
                terminal = move(second, "b", "p")
            assert terminal == frozenset(("a", "p", "q"))
        if response_guards:
            s_state = frozenset(("a", "p", "q"))
            assert independent(edges, s_state)
            assert movers(edges, s_state, "x") == ("a",)
            assert move(s_state, "a", "x") == frozenset(("x", "p", "q"))


def audit_ridge_directions() -> dict[str, object]:
    """Independently check every C-064 permutation direction."""

    aq_b_edges = next(
        edges
        for edges in named_assignments("AQ1")
        if has(edges, "a", "b") and not has(edges, "a", "c")
    )
    aq_c_edges = next(
        edges
        for edges in named_assignments("AQ1")
        if has(edges, "a", "c") and not has(edges, "a", "b")
    )
    qq_b_edges = next(
        edges
        for edges in named_assignments("QQ1")
        if not has(edges, "x", "b") and has(edges, "x", "c")
    )
    qq_c_edges = next(
        edges
        for edges in named_assignments("QQ1")
        if has(edges, "x", "b") and not has(edges, "x", "c")
    )

    aq_b_path = tuple(
        map(
            frozenset,
            (
                ("r", "a", "c"),
                ("p", "a", "c"),
                ("p", "a", "q"),
                ("p", "x", "q"),
            ),
        )
    )
    aq_c_path = tuple(
        map(
            frozenset,
            (
                ("r", "a", "b"),
                ("q", "a", "b"),
                ("q", "a", "p"),
                ("q", "x", "p"),
            ),
        )
    )
    qq_b_path = tuple(
        map(
            frozenset,
            (
                ("r", "b", "x"),
                ("q", "b", "x"),
                ("q", "p", "x"),
            ),
        )
    )
    qq_c_path = tuple(
        map(
            frozenset,
            (
                ("r", "c", "x"),
                ("p", "c", "x"),
                ("p", "q", "x"),
            ),
        )
    )

    for edges, path in (
        (aq_b_edges, aq_b_path),
        (aq_c_edges, aq_c_path),
        (qq_b_edges, qq_b_path),
        (qq_c_edges, qq_c_path),
    ):
        assert all(independent(edges, state) for state in path)

    aq_b = canonical_permutation(aq_b_path)
    aq_c = canonical_permutation(aq_c_path)
    qq_b = canonical_permutation(qq_b_path)
    qq_c = canonical_permutation(qq_c_path)

    # C-064 says rho(L_start(t)) = L_end(rho(t)).  The displayed end
    # markers therefore pull back to r at the start, not conversely.
    assert image(aq_b, "r") == "p" and image(aq_b, "b") == "b"
    assert image(aq_c, "r") == "q" and image(aq_c, "c") == "c"
    assert image(qq_b, "r") == "q" and image(qq_b, "c") == "c"
    assert image(qq_c, "r") == "p" and image(qq_c, "b") == "b"

    # T -> S transports the p-at-b and q-at-c markers without changing
    # either guard or target.
    ts_path = (
        frozenset(("x", "p", "q")),
        frozenset(("a", "p", "q")),
    )
    aq_saturated_edges = next(
        edges
        for edges in named_assignments("AQ1")
        if first_obstruction("AQ1", edges) == "normalized_survivor"
    )
    assert all(independent(aq_saturated_edges, state) for state in ts_path)
    ts = canonical_permutation(ts_path)
    assert image(ts, "p") == "p" and image(ts, "b") == "b"
    assert image(ts, "q") == "q" and image(ts, "c") == "c"

    return {
        "AQ1_b_branch": aq_b,
        "AQ1_c_branch": aq_c,
        "QQ1_xb_counterassumption": qq_b,
        "QQ1_xc_counterassumption": qq_c,
        "AQ1_T_to_S": ts,
    }


def first_obstruction(case: str, edges: set[frozenset[str]]) -> str:
    """Classify the first proof obstruction for one named assignment."""

    audit_private_ledger(case, edges)
    audit_forced_chain(case, edges)

    if case == "AQ1":
        ab = has(edges, "a", "b")
        ac = has(edges, "a", "c")
        if not ab and not ac:
            return "R_misses_a"
        if ab and not ac:
            return "AQ1_b_marker_covariance"
        if ac and not ab:
            return "AQ1_c_marker_covariance"
        if not has(edges, "x", "b"):
            return "M_q_b_attack_forces_xb"
        if not has(edges, "x", "c"):
            return "M_p_c_attack_forces_xc"
    else:
        xb = has(edges, "x", "b")
        xc = has(edges, "x", "c")
        if not xb and not xc:
            return "R_misses_x"
        if not xb:
            return "QQ1_xb_marker_covariance"
        if not xc:
            return "QQ1_xc_marker_covariance"

    # At this point W is excluded: in QQ1 it misses r; in AQ1 every
    # response to a misses one of r,p,q.
    w = frozenset(("x", "b", "c"))
    if case == "QQ1":
        assert misses(edges, w, "r")
    else:
        assert movers(edges, w, "a") == ("b", "c", "x")
        missed = {"x": "r", "b": "p", "c": "q"}
        for guard, vertex in missed.items():
            assert misses(edges, move(w, guard, "a"), vertex)

    if not has(edges, "b", "c"):
        u_state = frozenset(("u", "b", "c"))
        assert independent(edges, u_state)
        assert move(u_state, "u", "x") == w
        return "C108_forces_excluded_W"

    if not has(edges, "u", "p"):
        root = frozenset(("x", "p", "c"))
        assert movers(edges, root, "b") == ("c", "p", "x")
        assert misses(edges, move(root, "x", "b"), "u")
        assert move(root, "p", "b") == w
        assert misses(edges, move(root, "c", "b"), "q")
        return "M_q_b_attack_forces_up"

    if not has(edges, "u", "q"):
        root = frozenset(("x", "b", "q"))
        assert movers(edges, root, "c") == ("b", "q", "x")
        assert misses(edges, move(root, "x", "c"), "u")
        assert move(root, "q", "c") == w
        assert misses(edges, move(root, "b", "c"), "p")
        return "M_p_c_attack_forces_uq"

    return "normalized_survivor"


def audit_activity_and_reduction() -> dict[str, object]:
    """Audit u▷a, a not▷u, and preservation of the QQ1 blocker."""

    edges = next(
        edges
        for edges in named_assignments("AQ1")
        if first_obstruction("AQ1", edges) == "normalized_survivor"
    )
    results = []
    for sa, sq in itertools.product((False, True), repeat=2):
        extension = set(edges)
        if sa:
            extension.add(pair("s", "a"))
        if sq:
            extension.add(pair("s", "q"))
        # I={u,b,s} is the independent completion.  In particular s misses
        # u,b.  Saturation also prevents s from colliding with every named
        # vertex: ua,ux,up,uq,ur and bc cover the possible identities.
        extension.discard(pair("s", "u"))
        extension.discard(pair("s", "b"))
        i_state = frozenset(("u", "b", "s"))
        j_state = frozenset(("x", "b", "s"))
        assert independent(extension, i_state)
        assert move(i_state, "u", "x") == j_state
        eligible = movers(extension, j_state, "a")
        assert set(("x", "b")) <= set(eligible)
        for guard in eligible:
            successor = move(j_state, guard, "a")
            if guard == "s":
                assert misses(extension, successor, "q")
            elif guard == "b":
                if not sq:
                    assert misses(extension, successor, "q")
                else:
                    assert movers(extension, successor, "q") == ("s",)
                    terminal = move(successor, "s", "q")
                    assert misses(extension, terminal, "p")
            elif guard == "x":
                assert successor == frozenset(("a", "b", "s"))
            else:
                raise AssertionError(guard)
        results.append({"sa": sa, "sq": sq, "eligible": list(eligible)})

    s_state = frozenset(("a", "p", "q"))
    b_state = frozenset(("u", "p", "q"))
    assert independent(edges, s_state)
    assert move(s_state, "a", "u") == b_state
    # C-108 therefore reads the omitted B as a not▷u.  The same B and r
    # have exactly u,p,q as movers and the same private-witness ledger.
    assert movers(edges, b_state, "r") == ("p", "q", "u")
    assert not has(edges, "a", "r")
    assert has(edges, "p", "r") and has(edges, "q", "r")
    return {
        "independent_completion_collision_check": (
            "s is distinct from a,x,p,q,r,c after saturation"
        ),
        "activity_assignments": results,
        "reverse_successor": sorted(b_state),
        "blocker_movers": list(movers(edges, b_state, "r")),
        "reduced_row": "QQ1",
    }


def audit_completion_quantifier() -> dict[str, object]:
    """Check the arbitrary d quantifier and both singleton-hit branches."""

    results: dict[str, str] = {}
    base = {
        pair("p", "r"),
        pair("q", "r"),
        pair("p", "b"),
        pair("q", "c"),
    }
    for dp, dq in itertools.product((False, True), repeat=2):
        edges = set(base)
        if dp:
            edges.add(pair("d", "p"))
        if dq:
            edges.add(pair("d", "q"))
        s_state = frozenset(("a", "p", "q"))
        i_state = frozenset(("a", "r", "d"))
        key = f"dp={int(dp)},dq={int(dq)}"
        if not dp and not dq:
            results[key] = "excluded: retained S would miss d"
            continue
        if dp and not dq:
            path = (
                s_state,
                frozenset(("a", "d", "q")),
                i_state,
            )
            assert all(independent(edges, state) for state in path)
            permutation = canonical_permutation(path)
            assert image(permutation, "q") == "r"
            assert image(permutation, "c") == "c"
            assert not has(edges, "r", "c")
            results[key] = "excluded: q-at-c marker maps to r-at-c"
        elif dq and not dp:
            path = (
                s_state,
                frozenset(("a", "p", "d")),
                i_state,
            )
            assert all(independent(edges, state) for state in path)
            permutation = canonical_permutation(path)
            assert image(permutation, "p") == "r"
            assert image(permutation, "b") == "b"
            assert not has(edges, "r", "b")
            results[key] = "excluded: p-at-b marker maps to r-at-b"
        else:
            results[key] = "only surviving incidence"
    assert results["dp=1,dq=1"] == "only surviving incidence"
    return {
        "arbitrary_completion_incidence_cases": results,
        "universality_reason": (
            "the audit uses no property of d beyond ad=rd=0; after "
            "normalization such d cannot equal any named core vertex"
        ),
        "clique_reason": (
            "two nonadjacent completions with a,r would form an "
            "independent four-set"
        ),
    }


def audit_named_incidence_space() -> dict[str, object]:
    output: dict[str, object] = {}
    for case in ("QQ1", "AQ1"):
        counts: dict[str, int] = {}
        survivors = []
        total = 0
        for edges in named_assignments(case):
            total += 1
            obstruction = first_obstruction(case, edges)
            counts[obstruction] = counts.get(obstruction, 0) + 1
            if obstruction == "normalized_survivor":
                survivors.append(sorted(sorted(item) for item in edges))
        expected = 32 if case == "QQ1" else 128
        assert total == expected
        assert len(survivors) == 1
        output[case] = {
            "assignments": total,
            "first_obstruction_counts": counts,
            "normalized_survivors": len(survivors),
        }
    return output


def decode_small_graph6(record: str) -> tuple[int, ...]:
    raw = record.encode("ascii")
    if not raw or not 63 <= raw[0] <= 125:
        raise ValueError("small Graph6 record required")
    order = raw[0] - 63
    bits = []
    for byte in raw[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid Graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * order
    offset = 0
    for high in range(1, order):
        for low in range(high):
            if bits[offset]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            offset += 1
    return tuple(adjacency)


def popcount(value: int) -> int:
    return value.bit_count()


def dominates_mask(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in range(len(adjacency)):
        if state >> vertex & 1:
            covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def independent_mask(adjacency: tuple[int, ...], state: int) -> bool:
    for vertex in range(len(adjacency)):
        if state >> vertex & 1 and adjacency[vertex] & state:
            return False
    return True


def exact_static_parameters(adjacency: tuple[int, ...]) -> dict[str, int]:
    order = len(adjacency)
    masks = range(1 << order)
    gamma = min(
        popcount(state)
        for state in masks
        if dominates_mask(adjacency, state)
    )
    alpha = max(
        popcount(state)
        for state in masks
        if independent_mask(adjacency, state)
    )
    maximal_independent = []
    for state in masks:
        if not independent_mask(adjacency, state):
            continue
        if all(
            state >> vertex & 1
            or not independent_mask(adjacency, state | 1 << vertex)
            for vertex in range(order)
        ):
            maximal_independent.append(state)
    independent_domination = min(map(popcount, maximal_independent))

    clique = [False] * (1 << order)
    clique[0] = True
    for state in range(1, 1 << order):
        clique[state] = all(
            not (state >> left & 1 and state >> right & 1)
            or adjacency[left] >> right & 1
            for left, right in itertools.combinations(range(order), 2)
        )

    @functools.lru_cache(maxsize=None)
    def cover_number(remaining: int) -> int:
        if remaining == 0:
            return 0
        pivot_bit = remaining & -remaining
        best = order
        subset = remaining
        while subset:
            if subset & pivot_bit and clique[subset]:
                best = min(best, 1 + cover_number(remaining ^ subset))
            subset = (subset - 1) & remaining
        return best

    theta = cover_number((1 << order) - 1)
    return {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "theta": theta,
    }


def greatest_kernel(
    adjacency: tuple[int, ...], guards: int
) -> tuple[int, list[int], set[int]]:
    order = len(adjacency)
    family = {
        state
        for state in range(1 << order)
        if popcount(state) == guards and dominates_mask(adjacency, state)
    }
    initial = len(family)
    rounds: list[int] = []
    while True:
        remove = set()
        for state in family:
            for target in range(order):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                responses = False
                for guard in range(order):
                    guard_bit = 1 << guard
                    if not state & guard_bit:
                        continue
                    if not adjacency[guard] & target_bit:
                        continue
                    successor = state ^ guard_bit | target_bit
                    if successor in family:
                        responses = True
                        break
                if not responses:
                    remove.add(state)
                    break
        if not remove:
            return initial, rounds, family
        family -= remove
        rounds.append(len(remove))


def audit_boundary_control() -> dict[str, object]:
    adjacency = decode_small_graph6(GRAPH6)
    order = len(adjacency)
    size = sum(popcount(row) for row in adjacency) // 2
    static = exact_static_parameters(adjacency)
    kernels = {}
    gamma_infinity = None
    for guards in range(static["gamma"], order + 1):
        initial, rounds, family = greatest_kernel(adjacency, guards)
        kernels[str(guards)] = {
            "initial_dominating_states": initial,
            "deletion_rounds": rounds,
            "final_kernel_size": len(family),
        }
        if family:
            gamma_infinity = guards
            break
    assert (order, size) == (9, 17)
    assert static == {"gamma": 3, "i": 3, "alpha": 3, "theta": 4}
    assert gamma_infinity == 4
    assert kernels["3"] == {
        "initial_dominating_states": 45,
        "deletion_rounds": [24, 21],
        "final_kernel_size": 0,
    }

    labels = {"u": 0, "x": 1, "p": 2, "q": 3, "r": 4, "b": 5, "c": 6}
    core_edges = sorted(
        sorted((left, right))
        for left, right in itertools.combinations(labels, 2)
        if adjacency[labels[left]] >> labels[right] & 1
    )
    expected_core_edges = sorted(
        sorted(edge)
        for edge in (
            ("u", "x"),
            ("u", "p"),
            ("u", "q"),
            ("u", "r"),
            ("p", "r"),
            ("q", "r"),
            ("p", "b"),
            ("q", "c"),
            ("x", "b"),
            ("x", "c"),
            ("b", "c"),
        )
    )
    assert core_edges == expected_core_edges

    return {
        "graph6": GRAPH6,
        "graph6_ascii_sha256": hashlib.sha256(
            GRAPH6.encode("ascii")
        ).hexdigest(),
        "n": order,
        "m": size,
        **static,
        "gamma_infinity_one_guard": gamma_infinity,
        "kernels_until_optimum": kernels,
        "core_labels": labels,
        "core_G_edges": core_edges,
    }


def main() -> None:
    result = {
        "schema": "rank-one-ur1-normalization-hostile-clean-room-v1",
        "accepted_dependencies": ["C-010", "C-064", "C-108", "C-150"],
        "named_incidence_audit": audit_named_incidence_space(),
        "ridge_direction_audit": audit_ridge_directions(),
        "activity_and_AQ1_to_QQ1": audit_activity_and_reduction(),
        "completion_quantifier_audit": audit_completion_quantifier(),
        "boundary_control": audit_boundary_control(),
        "verdict": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
