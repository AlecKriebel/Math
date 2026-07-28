#!/usr/bin/env python3
"""Clean-room audit of the exact-static mixed-P4 local exclusion.

This checker does not import candidate code or campaign evaluators.  It
derives the eight-vertex pair ledger from the mathematical hypotheses,
constructs a configuration/attack incidence table, and computes the
greatest locally closed set by synchronous deletion.  It also reconstructs
the two graph6 boundary controls.
"""

from __future__ import annotations

from itertools import combinations
import hashlib
import json
from pathlib import Path


NAMES = ("a", "b", "c", "x0", "x1", "x2", "x3", "d")
ANCHORS = frozenset(("a", "b", "c"))
PATH = ("x0", "x1", "x2", "x3")
ROOT = tuple(sorted(ANCHORS))
STATIC_LISTS = {
    "x0": frozenset(("a",)),
    "x1": frozenset(("a", "c")),
    "x2": frozenset(("b", "c")),
    "x3": frozenset(("b",)),
}
FAMILY_LISTS = {
    **STATIC_LISTS,
    "d": frozenset(("c",)),
}


def pair(first: str, second: str) -> tuple[str, str]:
    if first == second:
        raise AssertionError("loop")
    return tuple(sorted((first, second)))


def derive_pair_ledger() -> tuple[
    frozenset[tuple[str, str]],
    frozenset[tuple[str, str]],
    tuple[tuple[str, str], ...],
]:
    """Derive, rather than transcribe, the 14/9/5 partition."""
    edges: set[tuple[str, str]] = set()
    nonedges: set[tuple[str, str]] = set()

    # The independent retained root.
    nonedges.update(pair(u, v) for u, v in combinations(sorted(ANCHORS), 2))

    # Positive static roles supply graph edges.
    for target, roles in STATIC_LISTS.items():
        edges.update(pair(target, role) for role in roles)

    # The displayed path is induced in H=complement(G).
    for left_index, right_index in combinations(range(4), 2):
        target_pair = pair(PATH[left_index], PATH[right_index])
        if right_index == left_index + 1:
            nonedges.add(target_pair)
        else:
            edges.add(target_pair)

    # Accepted endpoint saturation from C-070.
    edges.update((pair("c", "x0"), pair("c", "x3")))

    # One failed c-swap at x0 has a missed vertex d.
    nonedges.update((pair("d", "a"), pair("d", "b"), pair("d", "x0")))

    # S dominates d, so c is the only possible anchor neighbor.
    edges.add(pair("d", "c"))

    # The retained c-swaps at x1 and x2 dominate d.
    edges.update((pair("d", "x1"), pair("d", "x2")))

    universe = {
        pair(first, second)
        for first, second in combinations(NAMES, 2)
    }
    if edges & nonedges:
        raise AssertionError(("contradictory ledger", sorted(edges & nonedges)))
    optional = tuple(sorted(universe - edges - nonedges))
    expected_optional = tuple(
        sorted(
            (
                pair("b", "x0"),
                pair("b", "x1"),
                pair("a", "x2"),
                pair("a", "x3"),
                pair("d", "x3"),
            )
        )
    )
    if optional != expected_optional:
        raise AssertionError(("unexpected optional pairs", optional))
    if (len(edges), len(nonedges), len(optional), len(universe)) != (14, 9, 5, 28):
        raise AssertionError("pair coverage is not 14+9+5=28")
    return frozenset(edges), frozenset(nonedges), optional


def matrix_for(
    fixed_edges: frozenset[tuple[str, str]],
    optional: tuple[tuple[str, str], ...],
    mask: int,
) -> dict[str, dict[str, bool]]:
    present = set(fixed_edges)
    present.update(
        edge for bit, edge in enumerate(optional) if mask & (1 << bit)
    )
    return {
        first: {
            second: first != second and pair(first, second) in present
            for second in NAMES
        }
        for first in NAMES
    }


def dominates_core(
    state: tuple[str, ...],
    matrix: dict[str, dict[str, bool]],
) -> bool:
    occupied = set(state)
    for vertex in NAMES:
        if vertex in occupied:
            continue
        if not any(matrix[vertex][guard] for guard in state):
            return False
    return True


def restores_root(state: tuple[str, ...]) -> bool:
    occupied = set(state)
    missing = ANCHORS - occupied
    supplied: set[str] = set()
    for vertex in occupied - ANCHORS:
        supplied.update(FAMILY_LISTS[vertex])
    return missing <= supplied


def local_trace(
    matrix: dict[str, dict[str, bool]],
) -> dict[str, object]:
    """Compute closure using an explicit attack/successor incidence table."""
    configurations = tuple(tuple(sorted(state)) for state in combinations(NAMES, 3))
    admissible = tuple(
        state
        for state in configurations
        if dominates_core(state, matrix) and restores_root(state)
    )
    index = {state: position for position, state in enumerate(admissible)}

    obligations: dict[int, dict[str, tuple[int, ...]]] = {}
    for state_index, state in enumerate(admissible):
        occupied = set(state)
        by_attack: dict[str, tuple[int, ...]] = {}
        for attacked in NAMES:
            if attacked in occupied:
                continue
            successors: list[int] = []
            for guard in state:
                if not matrix[guard][attacked]:
                    continue
                successor = tuple(sorted((occupied - {guard}) | {attacked}))
                if successor in index:
                    successors.append(index[successor])
            by_attack[attacked] = tuple(sorted(set(successors)))
        obligations[state_index] = by_attack

    live = set(range(len(admissible)))
    deletion_rows: list[tuple[int, ...]] = []
    fatal_at_root: str | None = None
    root_rank: int | None = None
    root_index = index[ROOT]

    while live:
        doomed: list[int] = []
        first_fatal: dict[int, str] = {}
        for state_index in sorted(live):
            for attacked in NAMES:
                successors = obligations[state_index].get(attacked)
                if successors is None:
                    continue
                if not any(successor in live for successor in successors):
                    doomed.append(state_index)
                    first_fatal[state_index] = attacked
                    break
        if not doomed:
            break
        deletion_rows.append(tuple(doomed))
        if root_index in doomed:
            root_rank = len(deletion_rows)
            fatal_at_root = first_fatal[root_index]
        live.difference_update(doomed)

    if live:
        raise AssertionError(("nonempty terminal local kernel", live))
    if root_rank is None or fatal_at_root is None:
        raise AssertionError("root was not deleted")

    return {
        "initial": len(admissible),
        "round_sizes": [len(row) for row in deletion_rows],
        "root_rank": root_rank,
        "root_fatal_attack": fatal_at_root,
        "terminal": len(live),
    }


def audit_core() -> dict[str, object]:
    fixed_edges, fixed_nonedges, optional = derive_pair_ledger()
    records = []
    for mask in range(32):
        matrix = matrix_for(fixed_edges, optional, mask)

        # Every positive direct family swap must be in the initial
        # overapproximation.  This independently catches an incidence error.
        for target, roles in FAMILY_LISTS.items():
            for role in roles:
                state = tuple(sorted((ANCHORS - {role}) | {target}))
                if not dominates_core(state, matrix) or not restores_root(state):
                    raise AssertionError(("positive direct state missing", mask, state))

        trace = local_trace(matrix)
        records.append({"mask": mask, **trace})

    if any(row["terminal"] != 0 for row in records):
        raise AssertionError("a completion retained a local kernel")
    if min(row["initial"] for row in records) != 28:
        raise AssertionError("unexpected minimum initial size")
    if max(row["initial"] for row in records) != 32:
        raise AssertionError("unexpected maximum initial size")

    encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return {
        "fixed_edges": [list(edge) for edge in sorted(fixed_edges)],
        "fixed_nonedges": [list(edge) for edge in sorted(fixed_nonedges)],
        "optional_pairs_lexical_bit_order": [list(edge) for edge in optional],
        "pair_partition": [len(fixed_edges), len(fixed_nonedges), len(optional), 28],
        "completion_count": len(records),
        "empty_terminal_count": sum(row["terminal"] == 0 for row in records),
        "initial_size_multiset": sorted(row["initial"] for row in records),
        "root_rank_multiset": sorted(row["root_rank"] for row in records),
        "records_sha256": hashlib.sha256(encoded).hexdigest(),
        "records": records,
    }


def decode_graph6(record: str) -> list[list[bool]]:
    raw = [ord(character) - 63 for character in record.strip()]
    if not raw or not 0 <= raw[0] <= 62:
        raise ValueError("unsupported graph6 header")
    order = raw[0]
    bits: list[int] = []
    for value in raw[1:]:
        if not 0 <= value <= 63:
            raise ValueError("invalid graph6 character")
        for shift in (5, 4, 3, 2, 1, 0):
            bits.append((value >> shift) & 1)
    required = order * (order - 1) // 2
    if len(bits) < required:
        raise ValueError("short graph6 payload")
    matrix = [[False] * order for _ in range(order)]
    cursor = 0
    for higher in range(1, order):
        for lower in range(higher):
            if bits[cursor]:
                matrix[lower][higher] = matrix[higher][lower] = True
            cursor += 1
    return matrix


def subsets(order: int, size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(combinations(range(order), size))


def graph_dominates(state: tuple[int, ...], matrix: list[list[bool]]) -> bool:
    occupied = set(state)
    return all(
        vertex in occupied or any(matrix[vertex][guard] for guard in state)
        for vertex in range(len(matrix))
    )


def graph_independent(state: tuple[int, ...], matrix: list[list[bool]]) -> bool:
    return not any(matrix[first][second] for first, second in combinations(state, 2))


def greatest_kernel(
    matrix: list[list[bool]],
    size: int,
    forbidden: frozenset[tuple[int, ...]] = frozenset(),
) -> frozenset[tuple[int, ...]]:
    live = {
        state
        for state in subsets(len(matrix), size)
        if state not in forbidden and graph_dominates(state, matrix)
    }
    while True:
        doomed = set()
        for state in live:
            occupied = set(state)
            for attacked in range(len(matrix)):
                if attacked in occupied:
                    continue
                legal = False
                for guard in state:
                    if not matrix[guard][attacked]:
                        continue
                    successor = tuple(sorted((occupied - {guard}) | {attacked}))
                    if successor in live:
                        legal = True
                        break
                if not legal:
                    doomed.add(state)
                    break
        if not doomed:
            return frozenset(live)
        live.difference_update(doomed)


def graph_parameters(matrix: list[list[bool]]) -> dict[str, int]:
    order = len(matrix)
    gamma = next(
        size
        for size in range(order + 1)
        if any(graph_dominates(state, matrix) for state in subsets(order, size))
    )
    indep_dom = next(
        size
        for size in range(order + 1)
        if any(
            graph_dominates(state, matrix) and graph_independent(state, matrix)
            for state in subsets(order, size)
        )
    )
    alpha = next(
        size
        for size in range(order, -1, -1)
        if any(graph_independent(state, matrix) for state in subsets(order, size))
    )
    eternal = next(
        size
        for size in range(1, order + 1)
        if greatest_kernel(matrix, size)
    )

    clique_masks = []
    for size in range(1, order + 1):
        for clique in subsets(order, size):
            if all(matrix[u][v] for u, v in combinations(clique, 2)):
                mask = sum(1 << vertex for vertex in clique)
                clique_masks.append(mask)
    full = (1 << order) - 1
    best = {0: 0}
    for occupied_mask in range(1, full + 1):
        pivot = (occupied_mask & -occupied_mask).bit_length() - 1
        best[occupied_mask] = min(
            1 + best[occupied_mask ^ clique_mask]
            for clique_mask in clique_masks
            if clique_mask & (1 << pivot)
            and clique_mask & occupied_mask == clique_mask
        )
    return {
        "gamma": gamma,
        "i": indep_dom,
        "alpha": alpha,
        "gamma_infinity": eternal,
        "theta": best[full],
    }


def lists_at_root(
    matrix: list[list[bool]],
    family: frozenset[tuple[int, ...]],
    root: tuple[int, ...],
) -> dict[int, list[int]]:
    root_set = set(root)
    return {
        target: [
            role
            for role in root
            if matrix[role][target]
            and tuple(sorted((root_set - {role}) | {target})) in family
        ]
        for target in range(len(matrix))
        if target not in root_set
    }


def static_lists_at_root(
    matrix: list[list[bool]],
    root: tuple[int, ...],
) -> dict[int, list[int]]:
    root_set = set(root)
    return {
        target: [
            role
            for role in root
            if matrix[role][target]
            and graph_dominates(
                tuple(sorted((root_set - {role}) | {target})),
                matrix,
            )
        ]
        for target in range(len(matrix))
        if target not in root_set
    }


def audit_controls() -> dict[str, object]:
    root = (0, 1, 2)

    fdzro_matrix = decode_graph6("FDzro")
    desired = {3: [0], 4: [0, 2], 5: [1, 2], 6: [1]}
    forbidden = frozenset(
        tuple(sorted((set(root) - {role}) | {target}))
        for target, roles in desired.items()
        for role in set(root) - set(roles)
    )
    fdzro_family = greatest_kernel(fdzro_matrix, 3, forbidden)
    if root not in fdzro_family:
        raise AssertionError("FDzro reference state is not retained")
    if not graph_independent(root, fdzro_matrix):
        raise AssertionError("FDzro reference state is not independent")
    fdzro_lists = lists_at_root(fdzro_matrix, fdzro_family, root)
    fdzro_static = static_lists_at_root(fdzro_matrix, root)
    fdzro_params = graph_parameters(fdzro_matrix)
    if len(fdzro_family) != 21:
        raise AssertionError(("FDzro family size", len(fdzro_family)))
    if fdzro_lists != desired:
        raise AssertionError(("FDzro family lists", fdzro_lists))
    if fdzro_static != {
        3: [0, 2],
        4: [0, 1, 2],
        5: [0, 1, 2],
        6: [1, 2],
    }:
        raise AssertionError(("FDzro static lists", fdzro_static))
    if fdzro_params != {
        "gamma": 2,
        "i": 2,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(("FDzro parameters", fdzro_params))

    # Count each unoccupied attack; greatest_kernel already checks that each
    # has a same-family one-edge successor.
    fdzro_obligations = len(fdzro_family) * (len(fdzro_matrix) - 3)
    if fdzro_obligations != 84:
        raise AssertionError(fdzro_obligations)

    hco_matrix = decode_graph6("HCOceRy")
    hco_family = greatest_kernel(hco_matrix, 3)
    if root not in hco_family:
        raise AssertionError("HCOceRy reference state is not retained")
    if not graph_independent(root, hco_matrix):
        raise AssertionError("HCOceRy reference state is not independent")
    hco_lists = lists_at_root(hco_matrix, hco_family, root)
    hco_params = graph_parameters(hco_matrix)
    if hco_params != {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(("HCOceRy parameters", hco_params))
    if len(hco_family) != 24:
        raise AssertionError(("HCOceRy family size", len(hco_family)))
    if hco_lists[3] != [0] or hco_lists[6] != [0]:
        raise AssertionError(("HCOceRy singleton lists", hco_lists))
    if not hco_matrix[3][6]:
        raise AssertionError("HCOceRy singleton controls are not adjacent in G")
    for defect in (3, 6):
        missed = [anchor for anchor in root if not hco_matrix[defect][anchor]]
        if missed != [1, 2]:
            raise AssertionError(("HCOceRy missed anchors", defect, missed))

    return {
        "FDzro": {
            "parameters": fdzro_params,
            "constrained_family_size": len(fdzro_family),
            "unoccupied_attack_obligations": fdzro_obligations,
            "family_lists": fdzro_lists,
            "static_lists": fdzro_static,
        },
        "HCOceRy": {
            "parameters": hco_params,
            "greatest_family_size": len(hco_family),
            "lists_at_3_and_6": [hco_lists[3], hco_lists[6]],
            "missed_anchor_sets": [
                [anchor for anchor in root if not hco_matrix[defect][anchor]]
                for defect in (3, 6)
            ],
            "singletons_adjacent_in_G": hco_matrix[3][6],
        },
    }


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_hashes() -> dict[str, str]:
    campaign = Path(__file__).resolve().parents[2]
    pinned = {
        "candidate_NOTE.md": (
            campaign / "math/working/mixed_p4_infinite_descent/NOTE.md",
            "c58271538d6253ec4ac56d8df7edb7a067d67453dcf8393352a5bf394ed71d34",
        ),
        "candidate_verify.py": (
            campaign / "math/working/mixed_p4_infinite_descent/verify.py",
            "527b15ce630e9466acd8241f0edbb3f74a25f67a4cdf9985ff8f88871346a4de",
        ),
        "candidate_verify_bitset.py": (
            campaign / "math/working/mixed_p4_infinite_descent/verify_bitset.py",
            "b428401b7f48bd7027b1054c37748bbca779f445389aa6d4b80138264ce28692",
        ),
        "candidate_MANIFEST.json": (
            campaign / "math/working/mixed_p4_infinite_descent/MANIFEST.json",
            "7729b8f1e1d41e58f45a13f68e126d8427d082d902687e7ad203be47bd51438d",
        ),
        "candidate_RESEARCH_LOG.md": (
            campaign / "math/working/mixed_p4_infinite_descent/RESEARCH_LOG.md",
            "dff14dc1990b67a542a2eb8550dffded4d12af102b01c8489469aa1e31dd2047",
        ),
        "candidate_RESULT_SUMMARY.json": (
            campaign / "math/working/mixed_p4_infinite_descent/RESULT_SUMMARY.json",
            "2af0b6048347f8dcb612c1256081a5a4c3ec667f4ac543eced18646d76c13ea3",
        ),
        "candidate_probe_static_gamma_core.py": (
            campaign / "math/working/mixed_p4_infinite_descent/probe_static_gamma_core.py",
            "1dbfa8fde2bf072a4938c1406f073a55c56bca4bbdef48b63ca43f51fe640a8c",
        ),
        "C121_NOTE.md": (
            campaign / "math/working/dynamic_gluing_y3/NOTE.md",
            "ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9",
        ),
        "C070_NOTE.md": (
            campaign / "math/working/k3_mixed_witness_followup.md",
            "079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04",
        ),
    }
    observed = {name: hash_file(path) for name, (path, _) in pinned.items()}
    for name, (_, expected) in pinned.items():
        if observed[name] != expected:
            raise AssertionError(("dependency hash changed", name, observed[name], expected))
    return observed


def main() -> None:
    core = audit_core()
    controls = audit_controls()
    hashes = audit_hashes()
    result = {
        "schema": "mixed-p4-one-defect-hostile-clean-room-v1",
        "model": {
            "attacks": "unoccupied displayed vertices only",
            "move": "one occupied guard traverses one G-edge to the attack",
            "successor": "same three-set family",
        },
        "core": core,
        "controls": controls,
        "dependency_hashes": hashes,
        "collision_exclusions": {
            "d_not_in_failed_state": ["a", "b", "x0"],
            "d_not_c": "c-x0 is a G-edge",
            "d_not_x1": "a-x1 is a G-edge",
            "d_not_x2": "b-x2 is a G-edge",
            "d_not_x3": "b-x3 is a G-edge",
        },
        "scope": (
            "exact static lists at one independent retained root only; "
            "no claim for family-only lists, longer chains, or complete k=3"
        ),
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
