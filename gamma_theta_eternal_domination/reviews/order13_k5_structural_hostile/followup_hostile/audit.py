#!/usr/bin/env python3
"""Independent hostile replay for the order-13 k=5 follow-up note.

This checker freezes the reviewed bytes, recomputes the finite counts with a
fresh implementation, exhausts all five-vertex graphs for Lemma 9, checks the
local nonsimplicial translation, tests the clique-insertion equivalence on
small graphs, and directly simulates the one-guard obstruction in Theorem 10.
It is not a ten-vertex kernel enumeration or an order-13 exclusion
certificate.
"""

from __future__ import annotations

from itertools import combinations, product
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXPECTED = {
    "math/working/order13_k5_structural.md": (
        11274,
        "34c29d4b14e0955bd1ea0968f138a991cdd2a595ff3dd26891b74c1218af0a11",
    ),
    "math/working/order13_k5_followup/RESULT.md": (
        18805,
        "14d44f8b69acdec27783559794f6096c77c9c3f63cc2e219d59728eaf1e4a88b",
    ),
    "math/working/order13_k5_followup/audit.py": (
        6077,
        "b14c0aa6b9ba3ce4c0909ed67931ab5ed4d425f533e11c9640069a83f116dd88",
    ),
    "math/working/order13_k5_followup/evidence.json": (
        447,
        "9b591df7e5905a833bab72084cd8436c3847d5b26e750d005d1bdce99a03ba14",
    ),
    "math/lemmas/simplicial_neighborhood_reduction.md": (
        6559,
        "87cdebc4177bf7703a53892f84d436c0a52eb5444a6b0ac14663284c0351b25a",
    ),
    "math/lemmas/independent_antineighborhood_projection.md": (
        6735,
        "543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620",
    ),
    "math/lemmas/order12_frontier.md": (
        8120,
        "adb27204d33feb47933f2a4b1e381485b2e1b80c22b56a67b18586c4933c2b75",
    ),
}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def freeze_inputs() -> dict[str, dict[str, object]]:
    bindings: dict[str, dict[str, object]] = {}
    for relative, expected in EXPECTED.items():
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"unsafe or missing frozen input: {relative}")
        raw = path.read_bytes()
        actual = (len(raw), digest(raw))
        if actual != expected:
            raise RuntimeError(f"frozen input changed: {relative}: {actual}")
        bindings[relative] = {
            "sha256": actual[1],
            "size_bytes": actual[0],
        }
    return bindings


def graph_from_edge_mask(order: int, mask: int) -> tuple[int, ...]:
    adjacency = [0] * order
    bit_index = 0
    for first in range(order):
        for second in range(first + 1, order):
            if mask & (1 << bit_index):
                adjacency[first] |= 1 << second
                adjacency[second] |= 1 << first
            bit_index += 1
    return tuple(adjacency)


def is_independent(adjacency: tuple[int, ...], chosen: int) -> bool:
    remaining = chosen
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & (chosen ^ bit):
            return False
        remaining ^= bit
    return True


def closed_neighborhood(adjacency: tuple[int, ...], chosen: int) -> int:
    covered = chosen
    remaining = chosen
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        covered |= adjacency[vertex]
        remaining ^= bit
    return covered


def is_dominating(adjacency: tuple[int, ...], chosen: int) -> bool:
    return closed_neighborhood(adjacency, chosen) == (1 << len(adjacency)) - 1


def alpha(adjacency: tuple[int, ...]) -> int:
    return max(
        mask.bit_count()
        for mask in range(1 << len(adjacency))
        if is_independent(adjacency, mask)
    )


def gamma(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency) + 1):
        for vertices in combinations(range(len(adjacency)), size):
            chosen = sum(1 << vertex for vertex in vertices)
            if is_dominating(adjacency, chosen):
                return size
    raise AssertionError("finite graph has no dominating set")


def is_clique(adjacency: tuple[int, ...], chosen: int) -> bool:
    remaining = chosen
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        if (chosen ^ bit) & ~adjacency[vertex]:
            return False
        remaining ^= bit
    return True


def theta(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    full = (1 << order) - 1
    clique = [is_clique(adjacency, mask) for mask in range(1 << order)]
    best = [order + 1] * (1 << order)
    best[0] = 0
    for mask in range(1, 1 << order):
        pivot = mask & -mask
        part = mask
        while part:
            if part & pivot and clique[part]:
                best[mask] = min(best[mask], 1 + best[mask ^ part])
            part = (part - 1) & mask
    return best[full]


def build_attachment_graph(
    q_adjacency: tuple[int, ...],
    attachment_a: int,
    attachment_b: int,
) -> tuple[int, ...]:
    order_q = len(q_adjacency)
    a, b, v = order_q, order_q + 1, order_q + 2
    adjacency = list(q_adjacency) + [0, 0, 0]
    for q in range(order_q):
        if attachment_a & (1 << q):
            adjacency[q] |= 1 << a
            adjacency[a] |= 1 << q
        if attachment_b & (1 << q):
            adjacency[q] |= 1 << b
            adjacency[b] |= 1 << q
    adjacency[a] |= 1 << v
    adjacency[b] |= 1 << v
    adjacency[v] |= (1 << a) | (1 << b)
    return tuple(adjacency)


def check_five_vertex_classification() -> tuple[int, int]:
    qualifying = 0
    one_edge = 0
    for edge_mask in range(1 << 10):
        adjacency = graph_from_edge_mask(5, edge_mask)
        invariant = (gamma(adjacency), alpha(adjacency), theta(adjacency))
        expected = edge_mask.bit_count() == 1
        if expected:
            one_edge += 1
        if invariant == (4, 4, 4):
            qualifying += 1
            if not expected:
                raise AssertionError("Lemma 9 has a non-one-edge qualifier")
        elif expected:
            raise AssertionError("a one-edge graph failed Lemma 9 invariants")
    if (qualifying, one_edge) != (10, 10):
        raise AssertionError("unexpected five-vertex classification count")
    return qualifying, 1 << 10


def check_707_characterization() -> tuple[int, tuple[int, int, int]]:
    counts = []
    for c_size in (1, 2, 3):
        counts.append(
            len(tuple(combinations(range(3), c_size)))
            * sum(
                len(tuple(combinations(range(10), x_size)))
                for x_size in range(5 - c_size)
            )
        )
    if tuple(counts) != (528, 168, 11) or sum(counts) != 707:
        raise AssertionError("707 case split failed")

    # Independently compare (4.2)--(4.4) with direct domination on several
    # ten-vertex kernels and attachment pairs.  The equivalence itself does
    # not need the alpha hypotheses.
    q_graphs = []
    parts = ({0, 1, 2}, {3, 4, 5}, {6, 7}, {8, 9})
    q_edges = 0
    edge_position = {}
    position = 0
    for first in range(10):
        for second in range(first + 1, 10):
            edge_position[first, second] = position
            position += 1
    for part in parts:
        for first, second in combinations(sorted(part), 2):
            q_edges |= 1 << edge_position[first, second]
    q_graphs.append(graph_from_edge_mask(10, q_edges))
    q_graphs.append(graph_from_edge_mask(10, 0))

    mask_pairs = (
        (0b0000000111, 0b0000111000),
        (0b0101010101, 0b1010101010),
        (0b1111000000, 0b0000011111),
        ((1 << 10) - 1, 0),
    )
    full_q = (1 << 10) - 1
    for q_adjacency, (attachment_a, attachment_b) in product(
        q_graphs, mask_pairs
    ):
        graph = build_attachment_graph(
            q_adjacency, attachment_a, attachment_b
        )
        a, b, v = 10, 11, 12
        terminal_vertices = (a, b, v)
        checked = 0
        for c_size in (1, 2, 3):
            for c_vertices in combinations(terminal_vertices, c_size):
                c_mask = sum(1 << vertex for vertex in c_vertices)
                for x_size in range(5 - c_size):
                    for x_vertices in combinations(range(10), x_size):
                        x_mask = sum(1 << vertex for vertex in x_vertices)
                        direct = is_dominating(graph, c_mask | x_mask)
                        q_covered = closed_neighborhood(
                            q_adjacency, x_mask
                        )
                        if a in c_vertices:
                            q_covered |= attachment_a
                        if b in c_vertices:
                            q_covered |= attachment_b
                        condition = (
                            q_covered == full_q
                            and (
                                a in c_vertices
                                or v in c_vertices
                                or bool(x_mask & attachment_a)
                            )
                            and (
                                b in c_vertices
                                or v in c_vertices
                                or bool(x_mask & attachment_b)
                            )
                        )
                        if direct != condition:
                            raise AssertionError(
                                "707 condition is not direct domination"
                            )
                        checked += 1
        if checked != 707:
            raise AssertionError("did not test all 707 pairs")
    return 707, tuple(counts)


def clique_partitions_four(
    adjacency: tuple[int, ...],
) -> list[tuple[int, int, int, int]]:
    order = len(adjacency)
    partitions: set[tuple[int, int, int, int]] = set()
    for assignment in product(range(4), repeat=order):
        parts = tuple(
            sum(1 << vertex for vertex, color in enumerate(assignment)
                if color == part)
            for part in range(4)
        )
        if any(part == 0 for part in parts):
            continue
        if all(is_clique(adjacency, part) for part in parts):
            partitions.add(tuple(sorted(parts)))
    return sorted(partitions)


def check_insertion_criterion() -> int:
    checked = 0
    for order_q in (4, 5):
        edge_count = order_q * (order_q - 1) // 2
        for edge_mask in range(1 << edge_count):
            q_adjacency = graph_from_edge_mask(order_q, edge_mask)
            if theta(q_adjacency) != 4:
                continue
            partitions = clique_partitions_four(q_adjacency)
            if not partitions:
                raise AssertionError("theta four but no four partition")
            if order_q == 4:
                masks = range(1 << order_q)
            else:
                masks = [
                    mask
                    for mask in range(1 << order_q)
                    if mask.bit_count() in (0, 1, 4, 5)
                    or mask in (0b00101, 0b01010, 0b10101, 0b11000)
                ]
            for attachment_a, attachment_b in product(masks, repeat=2):
                insertion = any(
                    any(
                        part & ~attachment_a == 0
                        or part & ~attachment_b == 0
                        for part in partition
                    )
                    for partition in partitions
                )
                graph = build_attachment_graph(
                    q_adjacency, attachment_a, attachment_b
                )
                direct = theta(graph) <= 5
                if insertion != direct:
                    raise AssertionError("Theorem 4 iff failed")
                checked += 1
    if checked < 10000:
        raise AssertionError("insertion synthetic suite unexpectedly small")
    return checked


def is_simplicial(adjacency: tuple[int, ...], vertex: int) -> bool:
    return is_clique(adjacency, adjacency[vertex] | (1 << vertex))


def check_nonsimplicial_translation() -> int:
    checked = 0
    for edge_mask in range(1 << 6):
        q_adjacency = graph_from_edge_mask(4, edge_mask)
        for attachment_a in range(1 << 4):
            for attachment_b in range(1 << 4):
                graph = build_attachment_graph(
                    q_adjacency, attachment_a, attachment_b
                )
                for q in range(4):
                    q_bit = 1 << q
                    closed_q = q_adjacency[q] | q_bit
                    q_closed_clique = is_clique(q_adjacency, closed_q)
                    in_a = bool(attachment_a & q_bit)
                    in_b = bool(attachment_b & q_bit)
                    if in_a and in_b:
                        predicted_simplicial = False
                    elif in_a:
                        predicted_simplicial = (
                            q_closed_clique
                            and closed_q & ~attachment_a == 0
                        )
                    elif in_b:
                        predicted_simplicial = (
                            q_closed_clique
                            and closed_q & ~attachment_b == 0
                        )
                    else:
                        predicted_simplicial = q_closed_clique
                    if is_simplicial(graph, q) != predicted_simplicial:
                        raise AssertionError(
                            "Proposition 7 translation failed"
                        )
                    checked += 1

                # With both masks nonempty, a,b,v require no additional
                # no-simplicial filter.
                if attachment_a and attachment_b:
                    if any(
                        is_simplicial(graph, vertex)
                        for vertex in (4, 5, 6)
                    ):
                        raise AssertionError(
                            "terminal vertex unexpectedly simplicial"
                        )
    return checked


def check_raw_mask_counts() -> tuple[int, int, int]:
    masks = [
        mask
        for mask in range(1, 1 << 10)
        if mask.bit_count() <= 6
    ]
    if len(masks) != 847:
        raise AssertionError("admissible individual-mask count failed")
    ordered = 0
    fixed = 0
    for first in masks:
        for second in masks:
            if (first | second).bit_count() > 7:
                continue
            ordered += 1
            fixed += first == second
    unordered = (ordered + fixed) // 2
    if (ordered, fixed, unordered) != (465157, 847, 233002):
        raise AssertionError("raw mask-pair count failed")
    return ordered, fixed, unordered


def check_forced_state_filters() -> tuple[int, int]:
    parts = ({0, 1, 2}, {3, 4, 5}, {6, 7}, {8, 9})
    adjacency = [0] * 10
    for part in parts:
        for first, second in combinations(sorted(part), 2):
            adjacency[first] |= 1 << second
            adjacency[second] |= 1 << first
    q_adjacency = tuple(adjacency)
    full_q = (1 << 10) - 1
    maximum_q_sets = [
        mask
        for mask in range(1 << 10)
        if mask.bit_count() == 4 and is_independent(q_adjacency, mask)
    ]
    if len(maximum_q_sets) != 36 or alpha(q_adjacency) != 4:
        raise AssertionError("forced-state test kernel changed")

    mask_pairs = (
        (
            sum(1 << q for q in (1, 2, 4, 5)),
            sum(1 << q for q in (7, 8, 9)),
        ),
        (
            sum(1 << q for q in (2, 4, 7)),
            sum(1 << q for q in (5, 8, 9)),
        ),
        (
            sum(1 << q for q in (1, 4, 7, 8)),
            sum(1 << q for q in (2, 5, 9)),
        ),
    )
    independent_state_checks = 0
    residual_state_checks = 0
    for attachment_a, attachment_b in mask_pairs:
        graph = build_attachment_graph(
            q_adjacency, attachment_a, attachment_b
        )
        a, b, v = 10, 11, 12
        for independent_q in maximum_q_sets:
            state = (1 << v) | independent_q
            if not is_independent(graph, state):
                raise AssertionError("maximum-Q forced state is not independent")
            for attacked, own_mask, other_mask in (
                (a, attachment_a, attachment_b),
                (b, attachment_b, attachment_a),
            ):
                responders = state & graph[attacked]
                direct = False
                scan = responders
                while scan:
                    bit = scan & -scan
                    successor = (state ^ bit) | (1 << attacked)
                    direct |= is_dominating(graph, successor)
                    scan ^= bit
                formula = bool(independent_q & other_mask)
                scan = independent_q & own_mask
                while scan:
                    bit = scan & -scan
                    formula |= (
                        own_mask
                        | closed_neighborhood(q_adjacency, independent_q ^ bit)
                    ) == full_q
                    scan ^= bit
                if direct != formula:
                    raise AssertionError("Theorem 8 maximum-Q filter failed")
                independent_state_checks += 1

        residual = full_q & ~(attachment_a | attachment_b)
        residual_independent_sets = [
            mask
            for mask in range(1 << 10)
            if mask & ~residual == 0
            and is_independent(q_adjacency, mask)
        ]
        residual_alpha = max(mask.bit_count() for mask in residual_independent_sets)
        if residual_alpha != 3:
            raise AssertionError("synthetic residual does not have alpha three")
        for independent_r in residual_independent_sets:
            if independent_r.bit_count() != residual_alpha:
                continue
            state = (1 << a) | (1 << b) | independent_r
            if not is_independent(graph, state) or state & (1 << v):
                raise AssertionError("maximum-R forced state shape failed")
            responders = state & graph[v]
            direct = False
            scan = responders
            while scan:
                bit = scan & -scan
                successor = (state ^ bit) | (1 << v)
                direct |= is_dominating(graph, successor)
                scan ^= bit
            q_covered = closed_neighborhood(q_adjacency, independent_r)
            formula = (
                attachment_a | q_covered == full_q
                or attachment_b | q_covered == full_q
            )
            if direct != formula:
                raise AssertionError("Theorem 8 maximum-R filter failed")
            residual_state_checks += 1
    return independent_state_checks, residual_state_checks


def check_attachment_reconstruction() -> int:
    parts = ({0, 1, 2}, {3, 4, 5}, {6, 7}, {8, 9})
    adjacency = [0] * 10
    for part in parts:
        for first, second in combinations(sorted(part), 2):
            adjacency[first] |= 1 << second
            adjacency[second] |= 1 << first
    q_adjacency = tuple(adjacency)
    cases = (
        (0b0000000111, 0b0000111000),
        (0b0101010101, 0b1010101010),
        (0b0010100101, 0b0101000101),
        ((1 << 6) - 1, (1 << 6) - 1),
    )
    checked = 0
    full_graph = (1 << 13) - 1
    full_q = (1 << 10) - 1
    for attachment_a, attachment_b in cases:
        graph = build_attachment_graph(
            q_adjacency, attachment_a, attachment_b
        )
        a, b, v = 10, 11, 12
        if graph[v] != (1 << a) | (1 << b):
            raise AssertionError("distinguished root has wrong neighbors")
        extracted_q = full_graph & ~(
            graph[v] | (1 << v)
        )
        if extracted_q != full_q:
            raise AssertionError("Q is not G minus N[v]")
        extracted_a = graph[a] & full_q
        extracted_b = graph[b] & full_q
        if (extracted_a, extracted_b) != (
            attachment_a,
            attachment_b,
        ):
            raise AssertionError("attachment triple did not reconstruct")
        for q in range(10):
            if graph[q] & full_q != q_adjacency[q]:
                raise AssertionError("kernel edges changed in reconstruction")

        # Swapping a and b maps the ordered reconstruction to the graph built
        # from the swapped masks.
        swapped_graph = build_attachment_graph(
            q_adjacency, attachment_b, attachment_a
        )
        permutation = tuple(range(10)) + (b, a, v)
        for source in range(13):
            mapped_neighbors = sum(
                1 << permutation[target]
                for target in range(13)
                if graph[source] & (1 << target)
            )
            if mapped_neighbors != swapped_graph[permutation[source]]:
                raise AssertionError("a-b swap is not an isomorphism")
        checked += 1
    return checked


def check_six_mask_obstruction() -> tuple[int, int, int]:
    six_masks = [
        sum(1 << vertex for vertex in chosen)
        for chosen in combinations(range(10), 6)
    ]
    full_q = (1 << 10) - 1
    equal = 0
    unequal = 0
    simulated = 0
    for attachment_a in six_masks:
        for attachment_b in six_masks:
            residual = full_q & ~(attachment_a | attachment_b)
            if residual.bit_count() < 3:
                continue
            if attachment_a == attachment_b:
                equal += 1
                if residual.bit_count() != 4:
                    raise AssertionError("bad equal six-mask branch")
                continue
            unequal += 1
            only_b = attachment_b & ~attachment_a
            only_a = attachment_a & ~attachment_b
            if (
                residual.bit_count() != 3
                or only_b.bit_count() != 1
                or only_a.bit_count() != 1
            ):
                raise AssertionError("bad unequal six-mask split")
            x = only_b.bit_length() - 1
            y = only_a.bit_length() - 1

            # Build a synthetic Q satisfying exactly the two residual
            # independence facts used by Theorem 10.  Make A∩B a clique
            # universal to the other five vertices, and add xy.
            common = attachment_a & attachment_b
            q_adjacency = [0] * 10
            common_vertices = [
                q for q in range(10) if common & (1 << q)
            ]
            outside_vertices = [
                q for q in range(10) if not common & (1 << q)
            ]
            for first, second in combinations(common_vertices, 2):
                q_adjacency[first] |= 1 << second
                q_adjacency[second] |= 1 << first
            for first in common_vertices:
                for second in outside_vertices:
                    q_adjacency[first] |= 1 << second
                    q_adjacency[second] |= 1 << first
            q_adjacency[x] |= 1 << y
            q_adjacency[y] |= 1 << x
            q_tuple = tuple(q_adjacency)
            if alpha(q_tuple) != 4 or theta(q_tuple) != 4:
                raise AssertionError("synthetic Theorem 10 kernel failed")
            if not is_independent(q_tuple, residual | (1 << x)):
                raise AssertionError("R union x is not independent")
            if not is_independent(q_tuple, residual | (1 << y)):
                raise AssertionError("R union y is not independent")

            graph = build_attachment_graph(
                q_tuple, attachment_a, attachment_b
            )
            a, b, v = 10, 11, 12
            state = (1 << v) | residual | (1 << x)
            if not is_independent(graph, state) or state.bit_count() != 5:
                raise AssertionError("forced state shape failed")
            if state & (1 << b):
                raise AssertionError("Theorem 10 attack is occupied")
            responders = state & graph[b]
            expected_responders = (1 << v) | (1 << x)
            if responders != expected_responders:
                raise AssertionError("wrong one-guard responder set")
            for responder in (v, x):
                successor = (state ^ (1 << responder)) | (1 << b)
                if is_dominating(graph, successor):
                    raise AssertionError(
                        "Theorem 10 found a dominating successor"
                    )
            simulated += 1
    if (equal, unequal, simulated) != (210, 5040, 5040):
        raise AssertionError("six-mask totals changed")
    return equal, unequal, simulated


def check_claim_boundaries() -> None:
    note = (
        ROOT / "math/working/order13_k5_followup/RESULT.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(note.split())
    required = (
        "not an accepted campaign claim and not an exclusion",
        "No universal or finite-slice resolution is claimed.",
        "attacks only at unoccupied vertices and exactly one guard moving along one edge",
        "These are necessary domination-feasibility tests, not sufficient eternality tests.",
        "a manifest of all kernel and mask orbits plus independently checked coverage and proof artifacts is required",
        "No analytic contradiction is known after Theorem 10.",
    )
    for marker in required:
        if marker not in compact:
            raise AssertionError(f"claim boundary missing: {marker}")
    for theorem in range(1, 11):
        marker = (
            f"Theorem {theorem}"
            if theorem not in (2, 3, 5, 7, 9)
            else None
        )
        if marker is not None and marker not in note:
            raise AssertionError(f"missing theorem marker: {marker}")
    if "N_Q(a)" in note or "N_Q(b)" in note:
        raise AssertionError("follow-up retained undefined attachment notation")

    documentation_sentence = (
        "The remaining vertices \\(v,a,b\\) are automatically nonsimplicial:\n"
        "\\(a,b\\) are nonadjacent neighbors of \\(v\\); since \\(A,B\\) are nonempty,\n"
        "\\(N_G[a]\\) contains the nonadjacent pair consisting of \\(v\\) and any\n"
        "vertex of \\(A\\), and symmetrically for \\(b\\).\n\n"
    )
    if note.count(documentation_sentence) != 1:
        raise AssertionError("terminal nonsimplicial clarification changed")
    former = note.replace(documentation_sentence, "", 1).encode("utf-8")
    if (
        len(former),
        digest(former),
    ) != (
        18551,
        "6f8667776d39c5b2182df30947ed046c5e9072de5ebdfa67973798ffdb544fd9",
    ):
        raise AssertionError(
            "documentation-only reversal did not recover former result"
        )


def main() -> None:
    bindings = freeze_inputs()
    check_claim_boundaries()
    qualifying, graphs_checked = check_five_vertex_classification()
    domination_tests, domination_split = check_707_characterization()
    insertion_cases = check_insertion_criterion()
    nonsimplicial_cases = check_nonsimplicial_translation()
    ordered, fixed, unordered = check_raw_mask_counts()
    forced_q, forced_r = check_forced_state_filters()
    reconstruction_cases = check_attachment_reconstruction()
    equal_six, unequal_six, response_cases = check_six_mask_obstruction()
    print(
        json.dumps(
            {
                "bindings": bindings,
                "claim_boundary": "structural_reduction_not_slice_exclusion",
                "domination_split": domination_split,
                "domination_tests": domination_tests,
                "five_vertex_graphs_checked": graphs_checked,
                "five_vertex_qualifying_one_edge_graphs": qualifying,
                "former_followup_reconstructed": {
                    "sha256": "6f8667776d39c5b2182df30947ed046c5e9072de5ebdfa67973798ffdb544fd9",
                    "size_bytes": 18551,
                },
                "forced_state_filter_cases": {
                    "maximum_Q_states_and_attacks": forced_q,
                    "maximum_R_states_and_attacks": forced_r,
                },
                "insertion_iff_synthetic_cases": insertion_cases,
                "nonsimplicial_translation_cases": nonsimplicial_cases,
                "raw_mask_pairs": {
                    "fixed_under_swap": fixed,
                    "ordered": ordered,
                    "unordered": unordered,
                },
                "reconstruction_and_swap_cases": reconstruction_cases,
                "schema": "gamma-theta-order13-k5-followup-hostile-v1",
                "six_mask_cases": {
                    "equal": equal_six,
                    "unequal": unequal_six,
                    "unequal_one_guard_responses_simulated": response_cases,
                },
                "scope": {
                    "broad_kernel_enumeration_performed": False,
                    "order13_slice_excluded": False,
                },
                "verdict": "ACCEPT_CONDITIONAL_STRUCTURAL_FOLLOWUP",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
