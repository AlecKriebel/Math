#!/usr/bin/env python3
"""Clean-room audit for the physicality-bicycle endgame controls.

This file intentionally imports no campaign evaluator and does not read the
candidate's controls.json.  The two graph6 records, the displayed complement
construction, and the theorem's finite type data are restated below.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "math" / "working" / "physicality_bicycle_endgame"

N = 12
S = (0, 1, 2)
OUTSIDE = tuple(range(3, 12))
TYPES = {
    3: 0,
    4: 1,
    5: 2,
    6: 0,
    7: 1,
    8: 2,
    9: 0,
    10: 1,
    11: 2,
}
GATES = ((3, 4, 5), (6, 7, 8), (9, 10, 11))
RING = ((3, 6), (7, 10), (5, 11))

H_MINUS_EDGES = {
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 6),
    (0, 9),
    (1, 2),
    (1, 4),
    (1, 7),
    (1, 10),
    (2, 5),
    (2, 8),
    (2, 11),
    (3, 4),
    (3, 5),
    (3, 6),
    (4, 5),
    (5, 11),
    (6, 7),
    (6, 8),
    (7, 8),
    (7, 10),
    (9, 10),
    (9, 11),
    (10, 11),
}
H_PLUS_EDGES = H_MINUS_EDGES | {(3, 9), (4, 7), (8, 11)}

RECORDS = {
    "minus": {
        "g6": "KBjB\\z[^||Z[",
        "h6": "K{S{aCb_AAcb",
        "h_edges": H_MINUS_EDGES,
        "expected": {
            "gamma": 2,
            "i": 2,
            "alpha": 3,
            "gamma_infinity": 3,
            "theta": 4,
            "dominating_pairs": 9,
            "dominating_triples": 163,
            "kernel_triples": 163,
            "deletion_rounds": [],
            "attack_obligations": 1467,
            "shortest_unbalanced_length": 6,
        },
        "displayed_cycle": (3, 5, 11, 10, 7, 6),
    },
    "plus": {
        "g6": "KBjB\\j[Z||ZW",
        "h6": "K{S{aSbcAAcf",
        "h_edges": H_PLUS_EDGES,
        "expected": {
            "gamma": 3,
            "i": 3,
            "alpha": 3,
            "gamma_infinity": 4,
            "theta": 4,
            "dominating_pairs": 0,
            "dominating_triples": 136,
            "kernel_triples": 0,
            "deletion_rounds": [34, 56, 46],
            "attack_obligations": None,
            "shortest_unbalanced_length": 5,
        },
        "displayed_cycle": (3, 4, 7, 10, 9),
    },
}

CANDIDATE_HASHES = {
    "NOTE.md": "b282d96e1582ff9100bbdf6a81d9f1b29d2d76a3565e4a0d3cfbbb08886d0d91",
    "MANIFEST.json": "039637c213d3236fa630df0223f3ef320f150b571c4fa15049ee034384317873",
    "RESEARCH_LOG.md": "89d0434a31f23c3dd82efd90797a4101111f604a4ea00b0e03b3a907f5a4c396",
    "controls.json": "f8f2e087b57590fb09fafd679fd75aba8a786fff14fca3729cf9b30f16220489",
    "search_static.py": "f3c95be6ccd830750f29591928e4ad628ee053636637ca276215cb9755d048c3",
    "verify.py": "6dc1d0bd32d601a99b58f1049f4367e3181dbef0f46130c92d683f79111323b3",
}

DEPENDENCY_HASHES = {
    "math/working/dynamic_type_sparsity/NOTE.md": "f3309daa2497a10c978fac28286959d6ec2fb52e8438c727cdf2eafce89aa1a7",
    "math/working/k3_long_bicycle_connectors/NOTE.md": "d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10",
    "math/working/k3_side_purity_cap_cycle/NOTE.md": "64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b",
    "math/working/k3_cross_state_attack.md": "3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68",
    "math/lemmas/maximum_independent_states.md": "08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def graph6_decode(record: str) -> tuple[int, set[tuple[int, int]]]:
    raw = record.encode("ascii")
    require(raw and raw[0] != 126, "only short graph6 headers are expected")
    n = raw[0] - 63
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        require(0 <= value < 64, "invalid graph6 payload byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    needed = n * (n - 1) // 2
    require(len(bits) >= needed, "short graph6 payload")
    edges: set[tuple[int, int]] = set()
    index = 0
    for v in range(1, n):
        for u in range(v):
            if bits[index]:
                edges.add((u, v))
            index += 1
    return n, edges


def graph6_encode(n: int, edges: set[tuple[int, int]]) -> str:
    require(n <= 62, "only short graph6 headers are implemented")
    bits = []
    for v in range(1, n):
        for u in range(v):
            bits.append(1 if (u, v) in edges else 0)
    while len(bits) % 6:
        bits.append(0)
    chars = [chr(n + 63)]
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start : start + 6]:
            value = 2 * value + bit
        chars.append(chr(value + 63))
    return "".join(chars)


def complement_edges(n: int, edges: set[tuple[int, int]]) -> set[tuple[int, int]]:
    all_edges = {(u, v) for v in range(n) for u in range(v)}
    return all_edges - edges


def adjacency(n: int, edges: set[tuple[int, int]]) -> tuple[int, ...]:
    masks = [0] * n
    for u, v in edges:
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return tuple(masks)


def subset_mask(vertices: tuple[int, ...]) -> int:
    answer = 0
    for vertex in vertices:
        answer |= 1 << vertex
    return answer


def dominates(adj: tuple[int, ...], state: int) -> bool:
    covered = state
    probe = state
    while probe:
        low = probe & -probe
        vertex = low.bit_length() - 1
        covered |= adj[vertex]
        probe ^= low
    return covered == (1 << len(adj)) - 1


def independent(adj: tuple[int, ...], state: int) -> bool:
    probe = state
    while probe:
        low = probe & -probe
        vertex = low.bit_length() - 1
        if adj[vertex] & (state ^ low):
            return False
        probe ^= low
    return True


def masks_of_size(n: int, size: int) -> list[int]:
    return [subset_mask(vertices) for vertices in itertools.combinations(range(n), size)]


def minimum_parameter(n: int, predicate) -> int:
    for size in range(1, n + 1):
        if any(predicate(mask) for mask in masks_of_size(n, size)):
            return size
    raise AssertionError("parameter search unexpectedly failed")


def greatest_kernel(
    adj: tuple[int, ...], size: int
) -> tuple[set[int], list[int], list[int], int]:
    states = {state for state in masks_of_size(len(adj), size) if dominates(adj, state)}
    initial = set(states)
    rounds: list[int] = []
    while True:
        doomed: set[int] = set()
        for state in states:
            for attacked in range(len(adj)):
                attacked_bit = 1 << attacked
                if state & attacked_bit:
                    continue
                movable = state & adj[attacked]
                defended = False
                probe = movable
                while probe:
                    guard_bit = probe & -probe
                    successor = (state ^ guard_bit) | attacked_bit
                    if successor in states:
                        defended = True
                        break
                    probe ^= guard_bit
                if not defended:
                    doomed.add(state)
                    break
        if not doomed:
            break
        rounds.append(len(doomed))
        states -= doomed
    obligations = len(states) * (len(adj) - size)
    return states, rounds, sorted(initial), obligations


def gamma_infinity(adj: tuple[int, ...]) -> tuple[int, dict[int, tuple[int, list[int]]]]:
    profile: dict[int, tuple[int, list[int]]] = {}
    for size in range(1, len(adj) + 1):
        kernel, rounds, _, _ = greatest_kernel(adj, size)
        profile[size] = (len(kernel), rounds)
        if kernel:
            return size, profile
    raise AssertionError("full vertex set should be eternal")


def chromatic_number(adj: tuple[int, ...]) -> tuple[int, list[int]]:
    n = len(adj)

    def colorable(k: int) -> list[int] | None:
        colors = [-1] * n

        def search(colored: int) -> bool:
            if colored == n:
                return True
            best = -1
            best_key = (-1, -1)
            for vertex in range(n):
                if colors[vertex] != -1:
                    continue
                neighbor_colors = {
                    colors[neighbor]
                    for neighbor in range(n)
                    if (adj[vertex] >> neighbor) & 1 and colors[neighbor] != -1
                }
                key = (len(neighbor_colors), adj[vertex].bit_count())
                if key > best_key:
                    best_key = key
                    best = vertex
            forbidden = {
                colors[neighbor]
                for neighbor in range(n)
                if (adj[best] >> neighbor) & 1 and colors[neighbor] != -1
            }
            for color in range(k):
                if color in forbidden:
                    continue
                colors[best] = color
                if search(colored + 1):
                    return True
                colors[best] = -1
            return False

        return colors[:] if search(0) else None

    for k in range(1, n + 1):
        coloring = colorable(k)
        if coloring is not None:
            return k, coloring
    raise AssertionError("chromatic search unexpectedly failed")


def components_with_sides(
    vertices: tuple[int, ...], adj: tuple[int, ...]
) -> list[tuple[set[int], dict[int, int]]]:
    remaining = set(vertices)
    result: list[tuple[set[int], dict[int, int]]] = []
    while remaining:
        root = min(remaining)
        sides = {root: 0}
        queue = [root]
        component = {root}
        remaining.remove(root)
        for current in queue:
            for neighbor in vertices:
                if not ((adj[current] >> neighbor) & 1):
                    continue
                if neighbor not in sides:
                    sides[neighbor] = 1 - sides[current]
                    component.add(neighbor)
                    remaining.remove(neighbor)
                    queue.append(neighbor)
                else:
                    require(
                        sides[neighbor] != sides[current],
                        "type projection is not bipartite",
                    )
        result.append((component, sides))
    return result


def direct_swap_lists(adj_g: tuple[int, ...]) -> dict[int, list[int]]:
    lists: dict[int, list[int]] = {}
    root = subset_mask(S)
    for vertex in OUTSIDE:
        allowed = []
        for anchor in S:
            successor = (root ^ (1 << anchor)) | (1 << vertex)
            if ((adj_g[anchor] >> vertex) & 1) and dominates(adj_g, successor):
                allowed.append(anchor)
        lists[vertex] = allowed
    return lists


def family_swap_lists(adj_g: tuple[int, ...], family: set[int]) -> dict[int, list[int]]:
    lists: dict[int, list[int]] = {}
    root = subset_mask(S)
    require(root in family, "reference state missing from eternal family")
    for vertex in OUTSIDE:
        allowed = []
        for anchor in S:
            successor = (root ^ (1 << anchor)) | (1 << vertex)
            if ((adj_g[anchor] >> vertex) & 1) and successor in family:
                allowed.append(anchor)
        lists[vertex] = allowed
    return lists


def signed_parity(cycle: tuple[int, ...]) -> int:
    return sum(
        TYPES[cycle[index]] == TYPES[cycle[(index + 1) % len(cycle)]]
        for index in range(len(cycle))
    ) % 2


def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    rotations = []
    n = len(cycle)
    for orientation in (cycle, tuple(reversed(cycle))):
        rotations.extend(orientation[offset:] + orientation[:offset] for offset in range(n))
    return min(rotations)


def simple_cycles(adj_h: tuple[int, ...], vertices: tuple[int, ...]) -> list[tuple[int, ...]]:
    found: set[tuple[int, ...]] = set()
    vertex_set = set(vertices)
    for start in vertices:
        stack = [(start, (start,), {start})]
        while stack:
            current, path, used = stack.pop()
            for neighbor in vertex_set:
                if not ((adj_h[current] >> neighbor) & 1):
                    continue
                if neighbor == start and len(path) >= 3:
                    found.add(canonical_cycle(path))
                elif neighbor > start and neighbor not in used:
                    stack.append((neighbor, path + (neighbor,), used | {neighbor}))
    return sorted(found, key=lambda cycle: (len(cycle), cycle))


def canonical_word(word: tuple[int, ...]) -> tuple[int, ...]:
    candidates = []
    n = len(word)
    for permutation in itertools.permutations(range(3)):
        relabeled = tuple(permutation[value] for value in word)
        for orientation in (relabeled, tuple(reversed(relabeled))):
            candidates.extend(
                orientation[offset:] + orientation[:offset] for offset in range(n)
            )
    return min(candidates)


def word_classes() -> dict[str, list[list[int]]]:
    result: dict[str, list[list[int]]] = {}
    for length in (3, 4, 5):
        representatives = {
            canonical_word(word)
            for word in itertools.product(range(3), repeat=length)
            if sum(
                word[index] == word[(index + 1) % length]
                for index in range(length)
            )
            % 2
            == 1
        }
        result[str(length)] = [list(word) for word in sorted(representatives)]
    return result


def shortening_word_audit(maximum_length: int = 12) -> dict[str, int]:
    """Falsify the purely typed choice step used in the shortening proof."""
    checked = 0
    unbalanced = 0
    witnesses = 0
    constant_bipartite_exclusions = 0
    for length in range(6, maximum_length + 1):
        for word in itertools.product(range(3), repeat=length):
            checked += 1
            if (
                sum(
                    word[index] == word[(index + 1) % length]
                    for index in range(length)
                )
                % 2
                == 0
            ):
                continue
            unbalanced += 1
            found = False
            for first in range(length):
                for distance in range(3, length - 2):
                    second = (first + distance) % length
                    if word[first] != word[second]:
                        found = True
                        break
                if found:
                    break
            if found:
                witnesses += 1
            else:
                require(
                    len(set(word)) == 1 and length % 2 == 1,
                    f"nonconstant unbalanced length-{length} word has no qualified pair",
                )
                constant_bipartite_exclusions += 1
    return {
        "maximum_length": maximum_length,
        "words_checked": checked,
        "unbalanced_words": unbalanced,
        "qualified_pair_witnesses": witnesses,
        "constant_odd_words_excluded_by_projection_bipartiteness": constant_bipartite_exclusions,
    }


def analyze(name: str, record: dict) -> dict:
    n_g, edges_g = graph6_decode(record["g6"])
    n_h, edges_h = graph6_decode(record["h6"])
    require(n_g == n_h == N, f"{name}: graph6 order mismatch")
    require(edges_h == record["h_edges"], f"{name}: H graph6/construction mismatch")
    require(edges_g == complement_edges(N, edges_h), f"{name}: G and H not complements")
    require(graph6_encode(N, edges_g) == record["g6"], f"{name}: G graph6 reencode")
    require(graph6_encode(N, edges_h) == record["h6"], f"{name}: H graph6 reencode")

    adj_g = adjacency(N, edges_g)
    adj_h = adjacency(N, edges_h)

    gamma = minimum_parameter(N, lambda state: dominates(adj_g, state))
    alpha = max(
        size
        for size in range(N + 1)
        if any(independent(adj_g, state) for state in masks_of_size(N, size))
    )
    independent_domination = minimum_parameter(
        N, lambda state: independent(adj_g, state) and dominates(adj_g, state)
    )
    theta, coloring_h = chromatic_number(adj_h)
    eternal, eternal_profile = gamma_infinity(adj_g)
    kernel3, rounds3, dominating3, obligations3 = greatest_kernel(adj_g, 3)

    dominating_pairs = sum(dominates(adj_g, state) for state in masks_of_size(N, 2))
    require(
        dominating_pairs
        == sum(
            not any(
                ((adj_h[u] >> witness) & 1) and ((adj_h[v] >> witness) & 1)
                for witness in range(N)
                if witness not in (u, v)
            )
            for u, v in itertools.combinations(range(N), 2)
        ),
        f"{name}: pair/common-H-neighbor equivalence failed",
    )

    direct_lists = direct_swap_lists(adj_g)
    expected_lists = {
        vertex: [anchor for anchor in S if anchor != TYPES[vertex]]
        for vertex in OUTSIDE
    }
    require(direct_lists == expected_lists, f"{name}: exact physical direct lists failed")
    for vertex in OUTSIDE:
        for anchor in S:
            in_g = bool((adj_g[vertex] >> anchor) & 1)
            require(
                in_g == (anchor in expected_lists[vertex]),
                f"{name}: physical anchor incidence failed at {anchor},{vertex}",
            )

    response_lists = None
    response_histogram: dict[str, int] | None = None
    if name == "minus":
        response_lists = family_swap_lists(adj_g, kernel3)
        require(response_lists == expected_lists, "minus: eternal-family lists differ")
        require(
            all(mask in kernel3 for mask in dominating3),
            "minus: not every dominating triple survived",
        )
        counts: dict[int, int] = {}
        for state in kernel3:
            for attacked in range(N):
                if (state >> attacked) & 1:
                    continue
                replies = 0
                probe = state & adj_g[attacked]
                while probe:
                    guard = probe & -probe
                    if ((state ^ guard) | (1 << attacked)) in kernel3:
                        replies += 1
                    probe ^= guard
                require(replies > 0, "minus: an eternal obligation has no reply")
                counts[replies] = counts.get(replies, 0) + 1
        response_histogram = {str(key): counts[key] for key in sorted(counts)}

    projection_data = {}
    side_purity = True
    for omitted in S:
        vertices = tuple(v for v in OUTSIDE if TYPES[v] == omitted)
        components = components_with_sides(vertices, adj_h)
        projection_data[str(omitted)] = [
            {
                "vertices": sorted(component),
                "side_0": sorted(v for v in component if sides[v] == 0),
                "side_1": sorted(v for v in component if sides[v] == 1),
            }
            for component, sides in components
        ]
        for q in OUTSIDE:
            for component, sides in components:
                seen_sides = {
                    sides[v]
                    for v in component
                    if (adj_h[q] >> v) & 1
                }
                if len(seen_sides) > 1:
                    side_purity = False
    require(side_purity, f"{name}: universal side purity failed")

    same_type_mates = {
        str(vertex): sorted(
            neighbor
            for neighbor in OUTSIDE
            if neighbor != vertex
            and TYPES[neighbor] == TYPES[vertex]
            and ((adj_h[vertex] >> neighbor) & 1)
        )
        for vertex in OUTSIDE
    }
    if name == "plus":
        require(
            all(same_type_mates[str(vertex)] for vertex in OUTSIDE),
            "plus: a port lacks a same-type complement mate",
        )

    cross_edges = []
    all_common_neighbors_third_type = True
    all_cross_edges_completed = True
    for x, y in itertools.combinations(OUTSIDE, 2):
        if not ((adj_h[x] >> y) & 1) or TYPES[x] == TYPES[y]:
            continue
        third = ({0, 1, 2} - {TYPES[x], TYPES[y]}).pop()
        witnesses = [
            z
            for z in OUTSIDE
            if z not in (x, y)
            and ((adj_h[x] >> z) & 1)
            and ((adj_h[y] >> z) & 1)
        ]
        if not witnesses or not any(TYPES[z] == third for z in witnesses):
            all_cross_edges_completed = False
        if any(TYPES[z] != third for z in witnesses):
            all_common_neighbors_third_type = False
        cross_edges.append(
            {
                "edge": [x, y],
                "third_type": third,
                "witnesses": witnesses,
            }
        )
    require(all_cross_edges_completed, f"{name}: a cross edge has no transversal witness")
    if name == "plus":
        require(
            all_common_neighbors_third_type,
            "plus: a cross edge has a non-third-type outside common neighbor",
        )

    # Check the signed-coloring dictionary assignment by assignment.  Anchors
    # use their names as colors, and the chirality convention is exactly the
    # cyclic one in the theorem.
    dictionary_counts = {"assignments": 0, "proper": 0, "signed": 0}
    for bits in itertools.product((0, 1), repeat=len(OUTSIDE)):
        dictionary_counts["assignments"] += 1
        chirality = dict(zip(OUTSIDE, bits))
        colors = {anchor: anchor for anchor in S}
        for vertex in OUTSIDE:
            omitted = TYPES[vertex]
            colors[vertex] = (omitted - 1) % 3 if chirality[vertex] == 0 else (omitted + 1) % 3
        proper = all(colors[u] != colors[v] for u, v in edges_h)
        signed = all(
            (chirality[u] ^ chirality[v])
            == (1 if TYPES[u] == TYPES[v] else 0)
            for u, v in itertools.combinations(OUTSIDE, 2)
            if (adj_h[u] >> v) & 1
        )
        require(proper == signed, f"{name}: signed/proper dictionary mismatch")
        dictionary_counts["proper"] += int(proper)
        dictionary_counts["signed"] += int(signed)

    cycles = simple_cycles(adj_h, OUTSIDE)
    unbalanced = [cycle for cycle in cycles if signed_parity(cycle)]
    require(unbalanced, f"{name}: expected an unbalanced signed cycle")
    shortest_length = len(unbalanced[0])
    displayed = tuple(record["displayed_cycle"])
    require(
        canonical_cycle(displayed) in set(cycles),
        f"{name}: displayed sequence is not a simple H cycle",
    )
    require(signed_parity(displayed) == 1, f"{name}: displayed cycle is balanced")
    require(
        len(displayed) == shortest_length,
        f"{name}: displayed cycle is not shortest",
    )

    expected = record["expected"]
    actual = {
        "gamma": gamma,
        "i": independent_domination,
        "alpha": alpha,
        "gamma_infinity": eternal,
        "theta": theta,
        "dominating_pairs": dominating_pairs,
        "dominating_triples": len(dominating3),
        "kernel_triples": len(kernel3),
        "deletion_rounds": rounds3,
        "attack_obligations": obligations3 if kernel3 else None,
        "shortest_unbalanced_length": shortest_length,
    }
    require(actual == expected, f"{name}: exact values differ: {actual} != {expected}")

    for gate in GATES:
        require(
            all(pair(u, v) in edges_h for u, v in itertools.combinations(gate, 2)),
            f"{name}: displayed transversal gate missing an edge",
        )
    for edge in RING:
        require(pair(*edge) in edges_h, f"{name}: odd ring edge missing")

    return {
        "g_graph6": record["g6"],
        "h_graph6": record["h6"],
        "g_edges": len(edges_g),
        "h_edges": len(edges_h),
        "parameters": {
            "gamma": gamma,
            "i": independent_domination,
            "alpha": alpha,
            "gamma_infinity": eternal,
            "theta": theta,
        },
        "dominating_pairs": dominating_pairs,
        "dominating_triples": len(dominating3),
        "kernel_triples": len(kernel3),
        "deletion_rounds": rounds3,
        "attack_obligations": obligations3 if kernel3 else None,
        "retained_reply_count_histogram": response_histogram,
        "eternal_profile_through_answer": {
            str(size): {"kernel": value[0], "rounds": value[1]}
            for size, value in eternal_profile.items()
        },
        "direct_lists": {str(key): value for key, value in direct_lists.items()},
        "response_lists": (
            {str(key): value for key, value in response_lists.items()}
            if response_lists is not None
            else None
        ),
        "projection_components": projection_data,
        "same_type_mates": same_type_mates,
        "universal_side_purity": side_purity,
        "cross_edge_count": len(cross_edges),
        "every_cross_edge_has_transversal_witness": all_cross_edges_completed,
        "every_outside_common_witness_has_third_type": all_common_neighbors_third_type,
        "chromatic_coloring_h": coloring_h,
        "signed_coloring_dictionary": dictionary_counts,
        "unbalanced_cycle_count": len(unbalanced),
        "shortest_unbalanced_length": shortest_length,
        "displayed_shortest_unbalanced_cycle": list(displayed),
        "displayed_type_word": [TYPES[v] for v in displayed],
    }


def main() -> None:
    bound_hashes = {}
    for filename, expected in CANDIDATE_HASHES.items():
        digest = hashlib.sha256((CANDIDATE / filename).read_bytes()).hexdigest()
        require(digest == expected, f"candidate byte drift: {filename}")
        bound_hashes[filename] = digest

    bound_dependencies = {}
    for relative, expected in DEPENDENCY_HASHES.items():
        digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        require(digest == expected, f"dependency byte drift: {relative}")
        bound_dependencies[relative] = digest

    classification = word_classes()
    expected_classification = {
        "3": [[0, 0, 0], [0, 0, 1]],
        "4": [[0, 0, 1, 2]],
        "5": [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 0, 1],
            [0, 0, 1, 0, 2],
            [0, 0, 1, 2, 1],
        ],
    }
    require(classification == expected_classification, "type-word classification differs")

    evidence = {
        "schema": "physicality-bicycle-hostile-evidence-v1",
        "verdict": "PASS",
        "candidate_hashes": bound_hashes,
        "dependency_hashes": bound_dependencies,
        "independent_implementation": {
            "campaign_imports": [],
            "candidate_controls_json_read": False,
            "graph6_decoder": "clean-room short-header implementation",
            "game_kernel": "simultaneous greatest-fixed-point deletion from all dominating configurations",
            "coloring": "clean-room exact DSATUR-style backtracking",
        },
        "controls": {
            name: analyze(name, record) for name, record in RECORDS.items()
        },
        "unbalanced_type_word_classes": classification,
        "shortening_word_falsification": shortening_word_audit(),
        "residual_after_bipartite_and_side_purity": [
            "0012",
            "00011",
            "00101",
            "00102",
            "00121",
        ],
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
