#!/usr/bin/env python3
"""Clean-room audit of the 14-vertex third-color gate-cycle control.

The checker deliberately imports neither the source verifier nor any campaign
graph evaluator.  Its only graph input is the labeled graph6 string printed in
the mathematical note.  All graph parameters, the one-guard greatest fixed
point, response lists, gate incidences, and the even-return witness are rebuilt
with ordinary sets and exhaustive enumeration.
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess


LABELED_G6 = "MEXrtIdmdjLQqztC?"
CANONICAL_G6 = "MGEFK~cfJLBi]f]Z?"
EXPECTED_FAMILY_HASH = (
    "f0c587abd7d7123c822235793049623b02165ae134dd98c22bfa316141b1eaad"
)
N = 14
S = frozenset((0, 1, 2))
A, B, C = 0, 1, 2
X, Q0, T0, Y0, Z1, Q1, T1, Y1, Z0, U, V = range(3, 14)


def decode_graph6(record: str) -> tuple[int, set[frozenset[int]]]:
    raw = record.strip()
    if not raw or raw.startswith(">>"):
        raise ValueError("only a headerless small graph6 record is accepted")
    order = ord(raw[0]) - 63
    if not 0 <= order <= 62:
        raise ValueError("not a small graph6 order")
    bits: list[int] = []
    for character in raw[1:]:
        value = ord(character) - 63
        if not 0 <= value <= 63:
            raise ValueError("bad graph6 payload")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = order * (order - 1) // 2
    if len(bits) < needed:
        raise ValueError("truncated graph6 payload")
    edges: set[frozenset[int]] = set()
    cursor = 0
    for high in range(1, order):
        for low in range(high):
            if bits[cursor]:
                edges.add(frozenset((low, high)))
            cursor += 1
    return order, edges


def encode_graph6(order: int, edges: set[frozenset[int]]) -> str:
    bits = [
        int(frozenset((low, high)) in edges)
        for high in range(1, order)
        for low in range(high)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    payload: list[str] = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


ORDER, G_EDGES = decode_graph6(LABELED_G6)
ALL_PAIRS = {
    frozenset(pair) for pair in combinations(range(ORDER), 2)
}
H_EDGES = ALL_PAIRS - G_EDGES


def adjacent(edges: set[frozenset[int]], u: int, v: int) -> bool:
    return u != v and frozenset((u, v)) in edges


def g_edge(u: int, v: int) -> bool:
    return adjacent(G_EDGES, u, v)


def h_edge(u: int, v: int) -> bool:
    return adjacent(H_EDGES, u, v)


def dominates(vertices: frozenset[int]) -> bool:
    return all(
        vertex in vertices
        or any(g_edge(vertex, guard) for guard in vertices)
        for vertex in range(ORDER)
    )


def independent(vertices: frozenset[int]) -> bool:
    return all(not g_edge(u, v) for u, v in combinations(vertices, 2))


def connected() -> bool:
    reached = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbor in range(ORDER):
            if neighbor not in reached and g_edge(vertex, neighbor):
                reached.add(neighbor)
                queue.append(neighbor)
    return len(reached) == ORDER


def domination_number() -> int:
    for size in range(1, ORDER + 1):
        if any(
            dominates(frozenset(vertices))
            for vertices in combinations(range(ORDER), size)
        ):
            return size
    raise AssertionError("V always dominates")


def independence_number() -> int:
    answer = 0
    for size in range(1, ORDER + 1):
        if any(
            independent(frozenset(vertices))
            for vertices in combinations(range(ORDER), size)
        ):
            answer = size
        else:
            break
    return answer


def independent_domination_number() -> int:
    for size in range(1, ORDER + 1):
        if any(
            independent(frozenset(vertices))
            and dominates(frozenset(vertices))
            for vertices in combinations(range(ORDER), size)
        ):
            return size
    raise AssertionError("a maximal independent set exists")


def color_graph(
    edges: set[frozenset[int]], color_count: int
) -> tuple[int, ...] | None:
    """Independent exhaustive DSATUR, used only for the 14-vertex control."""

    colors = [-1] * ORDER
    degrees = [
        sum(adjacent(edges, vertex, other) for other in range(ORDER))
        for vertex in range(ORDER)
    ]

    def search(colored: int) -> bool:
        if colored == ORDER:
            return True
        remaining = [v for v in range(ORDER) if colors[v] < 0]
        vertex = max(
            remaining,
            key=lambda v: (
                len(
                    {
                        colors[w]
                        for w in range(ORDER)
                        if colors[w] >= 0 and adjacent(edges, v, w)
                    }
                ),
                degrees[v],
                -v,
            ),
        )
        forbidden = {
            colors[w]
            for w in range(ORDER)
            if colors[w] >= 0 and adjacent(edges, vertex, w)
        }
        for color in range(color_count):
            if color in forbidden:
                continue
            colors[vertex] = color
            if search(colored + 1):
                return True
            colors[vertex] = -1
        return False

    return tuple(colors) if search(0) else None


def greatest_triple_kernel() -> tuple[
    set[frozenset[int]], list[int], int, dict[tuple[tuple[int, ...], int], tuple[int, ...]]
]:
    family = {
        frozenset(vertices)
        for vertices in combinations(range(ORDER), 3)
        if dominates(frozenset(vertices))
    }
    initial_size = len(family)
    rounds: list[int] = []
    while True:
        remove: set[frozenset[int]] = set()
        for state in family:
            for attacked in range(ORDER):
                if attacked in state:
                    continue
                legal = False
                for guard in state:
                    successor = (state - {guard}) | {attacked}
                    if g_edge(guard, attacked) and successor in family:
                        legal = True
                        break
                if not legal:
                    remove.add(state)
                    break
        if not remove:
            break
        family -= remove
        rounds.append(len(remove))

    responses: dict[tuple[tuple[int, ...], int], tuple[int, ...]] = {}
    for state in sorted(family, key=lambda item: tuple(sorted(item))):
        for attacked in range(ORDER):
            if attacked in state:
                continue
            moves = tuple(
                sorted(
                    guard
                    for guard in state
                    if g_edge(guard, attacked)
                    and (state - {guard}) | {attacked} in family
                )
            )
            if not moves:
                raise AssertionError("kernel is not eternally closed")
            responses[(tuple(sorted(state)), attacked)] = moves
    return family, rounds, initial_size, responses


def serialized_family_hash(family: set[frozenset[int]]) -> str:
    payload = "".join(
        ",".join(str(v) for v in sorted(state)) + "\n"
        for state in sorted(family, key=lambda item: tuple(sorted(item)))
    ).encode("ascii")
    return sha256(payload).hexdigest()


def response_lists(family: set[frozenset[int]]) -> dict[int, tuple[int, ...]]:
    return {
        outside: tuple(
            anchor
            for anchor in sorted(S)
            if (S - {anchor}) | {outside} in family
        )
        for outside in range(3, ORDER)
    }


def anchored_list_colorings(
    lists: dict[int, tuple[int, ...]]
) -> list[tuple[int, ...]]:
    colors = [-1] * ORDER
    colors[A], colors[B], colors[C] = A, B, C
    answers: list[tuple[int, ...]] = []

    def search(vertex: int) -> None:
        if vertex == ORDER:
            answers.append(tuple(colors))
            return
        forbidden = {
            colors[other]
            for other in range(ORDER)
            if colors[other] >= 0 and h_edge(vertex, other)
        }
        for color in lists[vertex]:
            if color not in forbidden:
                colors[vertex] = color
                search(vertex + 1)
                colors[vertex] = -1

    search(3)
    return answers


def shortest_path_in_projection(
    start: int, target: int, omitted: int, lists: dict[int, tuple[int, ...]]
) -> tuple[int, ...] | None:
    projection = (S - {omitted}) | {
        vertex
        for vertex in range(3, ORDER)
        if omitted not in lists[vertex]
    }
    queue = deque([(start, (start,))])
    reached = {start}
    while queue:
        vertex, path = queue.popleft()
        if vertex == target:
            return path
        for neighbor in sorted(projection):
            if neighbor not in reached and h_edge(vertex, neighbor):
                reached.add(neighbor)
                queue.append((neighbor, path + (neighbor,)))
    return None


def canonicalize_with_labelg() -> tuple[str, str]:
    executable = (
        Path(__file__).resolve().parents[2] / "tools" / "nauty2_9_3" / "labelg"
    )
    run = subprocess.run(
        [str(executable), "-q"],
        input=LABELED_G6 + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    digest = sha256(executable.read_bytes()).hexdigest()
    return run.stdout.strip(), digest


def theorem_even_parity_control(
    lists: dict[int, tuple[int, ...]]
) -> dict[str, object]:
    """Check all hypotheses of Theorem 4.4 except its oddness condition."""

    path = (Y0, T0, Z0)
    assertions = {
        "vertices_distinct_and_outside_S": (
            len({X, Z1, *path}) == 5 and not ({X, Z1, *path} & S)
        ),
        "c_in_L_v0": C in lists[Y0],
        "c_not_in_L_x": C not in lists[X],
        "a_omitted_along_path": all(A not in lists[v] for v in path),
        "first_cap_edges_in_H": all(
            h_edge(u, v) for u, v in ((B, Z1), (X, Z1), (Y0, Z1))
        ),
        "path_edges_in_H": all(
            h_edge(u, v) for u, v in zip(path, path[1:])
        ),
        "return_cap_edges_in_H": h_edge(A, Z0) and h_edge(X, Z0),
        "path_length_even": (len(path) - 1) % 2 == 0,
    }
    if not all(assertions.values()):
        raise AssertionError(assertions)
    return {"vertices": [X, Z1, *path], "checks": assertions}


def broader_wording_countercontrols(
    lists: dict[int, tuple[int, ...]]
) -> dict[str, object]:
    """Witness why three conspicuous hypotheses cannot simply be deleted."""

    def common_prefix(path: tuple[int, ...]) -> dict[str, bool]:
        return {
            "vertices_distinct_and_outside_S": (
                len({X, Z1, *path}) == 2 + len(path)
                and not ({X, Z1, *path} & S)
            ),
            "c_in_L_v0": C in lists[path[0]],
            "c_not_in_L_x": C not in lists[X],
            "first_cap_edges_in_H": all(
                h_edge(u, v)
                for u, v in ((B, Z1), (X, Z1), (path[0], Z1))
            ),
            "path_edges_in_H": all(
                h_edge(u, v) for u, v in zip(path, path[1:])
            ),
        }

    # All Theorem 4.4 hypotheses except oddness hold.  This is the sharp
    # even return highlighted in the source note.
    even_path = (Y0, T0, Z0)
    even = common_prefix(even_path) | {
        "a_omitted_along_path": all(A not in lists[v] for v in even_path),
        "return_a_edge_in_H": h_edge(A, even_path[-1]),
        "return_x_edge_in_H": h_edge(X, even_path[-1]),
        "path_is_even": (len(even_path) - 1) % 2 == 0,
    }
    assert all(even.values())

    # If x--t in H is omitted, the one-edge path 6--5 survives in this
    # equality graph.  Every other displayed condition still holds.
    missing_xt_path = (Y0, T0)
    missing_xt = common_prefix(missing_xt_path) | {
        "a_omitted_along_path": all(
            A not in lists[v] for v in missing_xt_path
        ),
        "return_a_edge_in_H": h_edge(A, missing_xt_path[-1]),
        "return_x_edge_is_in_G": g_edge(X, missing_xt_path[-1]),
        "path_is_odd": (len(missing_xt_path) - 1) % 2 == 1,
    }
    assert all(missing_xt.values())

    # If the whole path need not omit a, 6--10--13--11 is an odd return
    # with both endpoint cap edges, but vertices 10 and 13 admit a.
    mixed_path = (Y0, Y1, V, Z0)
    mixed = common_prefix(mixed_path) | {
        "return_a_edge_in_H": h_edge(A, mixed_path[-1]),
        "return_x_edge_in_H": h_edge(X, mixed_path[-1]),
        "path_is_odd": (len(mixed_path) - 1) % 2 == 1,
        "interior_has_a_in_its_list": any(
            A in lists[v] for v in mixed_path[1:-1]
        ),
    }
    assert all(mixed.values())

    return {
        "drop_oddness": {
            "path": list(even_path),
            "checks": even,
        },
        "drop_return_edge_x_t": {
            "path": list(missing_xt_path),
            "checks": missing_xt,
        },
        "drop_uniform_a_omission": {
            "path": list(mixed_path),
            "checks": mixed,
        },
    }


def audit_chirality_and_type_words() -> dict[str, object]:
    """Exhaust the finite color/type calculations used in Sections 2--3."""

    def allowed(omitted: int) -> tuple[int, int]:
        return tuple(color for color in range(3) if color != omitted)

    def chirality(omitted: int, color: int) -> int:
        assert color in allowed(omitted)
        if color == (omitted - 1) % 3:
            return 0
        assert color == (omitted + 1) % 3
        return 1

    implication_checks = 0
    for left_type, right_type in product(range(3), repeat=2):
        if left_type == right_type:
            continue
        common = set(allowed(left_type)) & set(allowed(right_type))
        assert len(common) == 1
        collision = next(iter(common))
        right_other = next(
            color for color in allowed(right_type) if color != collision
        )
        left_other = next(
            color for color in allowed(left_type) if color != collision
        )
        assert chirality(left_type, collision) == chirality(
            right_type, right_other
        )
        assert chirality(right_type, collision) == chirality(
            left_type, left_other
        )
        implication_checks += 2

    # Lists 01, 12, 02 have omitted types 2, 0, 1 respectively.
    gate_assignments: list[tuple[int, int, int]] = []
    for x_color, y_color, z_color in product((0, 1), (1, 2), (0, 2)):
        if x_color == 1 and y_color == 1:
            continue
        if x_color == 0 and z_color == 0:
            continue
        if y_color == 2 and z_color == 2:
            continue
        gate_assignments.append((x_color, y_color, z_color))
        assert len(
            {
                chirality(2, x_color),
                chirality(0, y_color),
                chirality(1, z_color),
            }
        ) == 1
    assert gate_assignments == [(0, 1, 2), (1, 2, 0)]

    cyclic_words_checked = 0
    for length in range(2, 11):
        for word in product(range(3), repeat=length):
            if any(word[i] == word[(i + 1) % length] for i in range(length)):
                continue
            steps = [
                1 if (word[(i + 1) % length] - word[i]) % 3 == 1 else -1
                for i in range(length)
            ]
            reversals = sum(
                steps[i - 1] != steps[i] for i in range(length)
            )
            assert reversals % 2 == 0
            # A literal-to-complement closure changes exactly the closing
            # connector bit, hence toggles the even cycle xor to one.
            assert (reversals ^ 1) % 2 == 1
            cyclic_words_checked += 1

    return {
        "cross_implications_checked": implication_checks,
        "tight_gate_assignments": [list(item) for item in gate_assignments],
        "cyclic_type_words_checked_lengths_2_through_10": cyclic_words_checked,
    }


def build_evidence() -> dict[str, object]:
    assert ORDER == N
    assert encode_graph6(ORDER, G_EDGES) == LABELED_G6
    assert len(G_EDGES) == 47
    assert connected()

    gamma = domination_number()
    alpha = independence_number()
    ind_dom = independent_domination_number()
    assert (gamma, ind_dom, alpha) == (3, 3, 3)
    assert independent(S) and dominates(S)

    family, deletion_rounds, initial_size, responses = greatest_triple_kernel()
    assert initial_size == 172
    assert len(family) == 172
    assert deletion_rounds == []
    assert S in family
    family_digest = serialized_family_hash(family)
    assert family_digest == EXPECTED_FAMILY_HASH
    assert len(responses) == 172 * (N - 3)
    response_payload = "".join(
        f"{','.join(map(str, state))}|{attacked}:"
        f"{','.join(map(str, responses[(state, attacked)]))}\n"
        for state, attacked in sorted(responses)
    ).encode("ascii")
    response_digest = sha256(response_payload).hexdigest()
    legal_response_moves = sum(len(moves) for moves in responses.values())

    lists = response_lists(family)
    expected_lists = {
        3: (0, 1),
        4: (1, 2),
        5: (1, 2),
        6: (1, 2),
        7: (0, 2),
        8: (0, 2),
        9: (0, 2),
        10: (0, 2),
        11: (1, 2),
        12: (0, 1),
        13: (0, 1),
    }
    assert lists == expected_lists

    # Rebuild both tight gates directly from their exact lists and H/G edges.
    gates = (
        (X, Q0, T0, Y0, Z1, C, B),
        (X, Q1, T1, Y1, Z0, C, A),
    )
    gate_checks: list[dict[str, object]] = []
    for x, q, middle, y, cap, omitted_x, omitted_cap in gates:
        assert len(lists[x]) == len(lists[q]) == len(lists[y]) == 2
        assert len(lists[cap]) == 2
        assert omitted_x not in lists[x]
        assert lists[q] == lists[y]
        assert omitted_cap not in lists[cap]
        assert h_edge(x, q)
        assert h_edge(q, middle) and h_edge(middle, y)
        assert g_edge(x, y)
        assert h_edge(x, cap) and h_edge(y, cap)
        assert h_edge(omitted_cap, cap)
        gate_checks.append(
            {
                "ports": [x, q, y],
                "same_sign_path": [q, middle, y],
                "failed_pair": [x, y],
                "cap": cap,
            }
        )

    # The shared-port gates close by an even path 6-5-11 in B_a.
    even_return = shortest_path_in_projection(Y0, Z0, A, lists)
    assert even_return == (Y0, T0, Z0)
    assert not h_edge(Y0, Z0)
    even_pattern = theorem_even_parity_control(lists)

    colorings = anchored_list_colorings(lists)
    assert len(colorings) == 2
    assert color_graph(H_EDGES, 2) is None
    h_coloring = color_graph(H_EDGES, 3)
    assert h_coloring is not None
    assert all(
        h_coloring[u] != h_coloring[v]
        for u, v in (tuple(edge) for edge in H_EDGES)
    )

    canonical, labelg_hash = canonicalize_with_labelg()
    assert canonical == CANONICAL_G6

    return {
        "schema": "third-color-gate-cycle-hostile-audit-v1",
        "verdict": "PASS",
        "graph": {
            "labeled_graph6": LABELED_G6,
            "canonical_graph6": canonical,
            "order": ORDER,
            "size": len(G_EDGES),
            "connected": True,
            "parameters": {
                "gamma": gamma,
                "i": ind_dom,
                "alpha": alpha,
                "gamma_infinity": 3,
                "theta": 3,
            },
            "one_complement_3_coloring": list(h_coloring),
        },
        "one_guard_kernel": {
            "initial_dominating_triples": initial_size,
            "greatest_family_size": len(family),
            "deletion_rounds": deletion_rounds,
            "obligations": len(responses),
            "legal_response_moves": legal_response_moves,
            "family_sha256": family_digest,
            "response_table_sha256": response_digest,
        },
        "lists_at_S": {str(v): list(value) for v, value in lists.items()},
        "tight_gates": gate_checks,
        "anchored_list_colorings": [list(item) for item in colorings],
        "even_return_path_in_B_a": list(even_return),
        "even_parity_countercontrol_to_broader_odd_return_wording": even_pattern,
        "broader_wording_countercontrols": broader_wording_countercontrols(
            lists
        ),
        "finite_chirality_and_type_word_audit": audit_chirality_and_type_words(),
        "canonicalizer": {
            "path": "tools/nauty2_9_3/labelg",
            "sha256": labelg_hash,
        },
    }


def main() -> None:
    destination = Path(__file__).with_name("evidence.json")
    result = build_evidence()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if destination.exists():
        assert destination.read_text(encoding="utf-8") == encoded
    else:
        destination.write_text(encoded, encoding="utf-8")
    print("PASS")


if __name__ == "__main__":
    main()
