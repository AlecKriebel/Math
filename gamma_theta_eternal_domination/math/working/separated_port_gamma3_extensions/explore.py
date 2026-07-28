#!/usr/bin/env python3
"""Exact one-vertex-extension scan of the separated-port lollipop control.

The base graph is the nine-vertex graph ``HFzvvn{`` from
``full_list_odd_lollipop_integration``.  We enumerate all 2^9 labeled
neighborhoods of a tenth vertex.  Extension masks describe adjacency in the
*complement* H; the evaluated eternal-domination graph is G = complement(H).

Besides the four exact parameters, the scan tests the following precise
family predicate.  There must be an eternal family F of triples such that:

* S={0,1,2} is in F;
* the response lists at S for old targets 3,...,8 are exactly the lists in
  the nine-vertex control;
* target 3 is the unique full-list target (so the new target has a nonempty
  proper list); and
* the full list-coloring instance without target 3 is satisfiable, while
  fixing target 3 to color 0 makes it unsatisfiable.

The existential quantifier over F is exact.  For every possible nonempty
proper response list of the new vertex, we ban precisely the excluded direct
swaps, compute the greatest eternal kernel of the remaining dominating
triples, and require S and every included direct swap to survive.  Any
admissible proper subfamily lies in that greatest kernel, and the greatest
kernel itself is then a witness.
"""

from __future__ import annotations

import csv
import hashlib
import itertools
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


BASE_N = 9
N = 10
S_MASK = (1 << 0) | (1 << 1) | (1 << 2)
X = 3
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
HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[2]
LABELG = CAMPAIGN / "tools" / "nauty2_9_3" / "labelg"


def pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def make_h_edges(extension_mask: int) -> frozenset[tuple[int, int]]:
    return BASE_H_EDGES | {
        (old, 9) for old in range(BASE_N) if extension_mask & (1 << old)
    }


def adjacency_masks(
    n: int, edges: frozenset[tuple[int, int]]
) -> tuple[int, ...]:
    masks = [0] * n
    for u, v in edges:
        masks[u] |= 1 << v
        masks[v] |= 1 << u
    return tuple(masks)


def complement_masks(n: int, h_adj: tuple[int, ...]) -> tuple[int, ...]:
    all_mask = (1 << n) - 1
    return tuple(all_mask & ~(1 << v) & ~h_adj[v] for v in range(n))


def graph6(n: int, edges: frozenset[tuple[int, int]]) -> str:
    assert n <= 62
    bits = [
        int(pair(i, j) in edges)
        for j in range(1, n)
        for i in range(j)
    ]
    bits.extend([0] * ((-len(bits)) % 6))
    body = "".join(
        chr(63 + sum(bits[start + bit] << (5 - bit) for bit in range(6)))
        for start in range(0, len(bits), 6)
    )
    return chr(63 + n) + body


def graph_edges_from_adj(
    n: int, adj: tuple[int, ...]
) -> frozenset[tuple[int, int]]:
    return frozenset(
        (u, v)
        for u in range(n)
        for v in range(u + 1, n)
        if adj[u] & (1 << v)
    )


def dominates(state: int, closed_g: tuple[int, ...], all_mask: int) -> bool:
    covered = 0
    scan = state
    while scan:
        bit = scan & -scan
        covered |= closed_g[bit.bit_length() - 1]
        scan ^= bit
    return covered == all_mask


def combinations_masks(n: int, size: int):
    for vertices in itertools.combinations(range(n), size):
        yield sum(1 << vertex for vertex in vertices)


def dominating_states(
    n: int, size: int, g_adj: tuple[int, ...]
) -> set[int]:
    all_mask = (1 << n) - 1
    closed_g = tuple(g_adj[v] | (1 << v) for v in range(n))
    return {
        state
        for state in combinations_masks(n, size)
        if dominates(state, closed_g, all_mask)
    }


def eternal_kernel(
    n: int,
    size: int,
    g_adj: tuple[int, ...],
    *,
    banned: frozenset[int] = frozenset(),
) -> tuple[frozenset[int], tuple[int, ...]]:
    all_mask = (1 << n) - 1
    family = dominating_states(n, size, g_adj) - set(banned)
    rounds: list[int] = []
    while True:
        dead = set()
        for state in family:
            attacks = all_mask ^ state
            while attacks:
                attack_bit = attacks & -attacks
                attack = attack_bit.bit_length() - 1
                guards = state & g_adj[attack]
                legal = False
                while guards:
                    guard_bit = guards & -guards
                    if (state ^ guard_bit) | attack_bit in family:
                        legal = True
                        break
                    guards ^= guard_bit
                if not legal:
                    dead.add(state)
                    break
                attacks ^= attack_bit
        if not dead:
            return frozenset(family), tuple(rounds)
        rounds.append(len(dead))
        family.difference_update(dead)


def gamma_exact(n: int, g_adj: tuple[int, ...]) -> int:
    for size in range(1, n + 1):
        if dominating_states(n, size, g_adj):
            return size
    raise AssertionError("unreachable")


def alpha_exact(n: int, g_adj: tuple[int, ...]) -> int:
    for size in range(n, 0, -1):
        for state in combinations_masks(n, size):
            scan = state
            independent = True
            while scan:
                bit = scan & -scan
                vertex = bit.bit_length() - 1
                if g_adj[vertex] & (state ^ bit):
                    independent = False
                    break
                scan ^= bit
            if independent:
                return size
    return 0


def k_colorable(n: int, adj: tuple[int, ...], colors: int) -> bool:
    assigned = [-1] * n
    saturation = [0] * n
    degrees = [adj[v].bit_count() for v in range(n)]

    def visit(colored: int) -> bool:
        if colored == n:
            return True
        candidates = [v for v in range(n) if assigned[v] < 0]
        vertex = max(
            candidates,
            key=lambda v: (saturation[v].bit_count(), degrees[v], -v),
        )
        forbidden = saturation[vertex]
        for color in range(colors):
            bit = 1 << color
            if forbidden & bit:
                continue
            assigned[vertex] = color
            changed: list[tuple[int, int]] = []
            neighbors = adj[vertex]
            while neighbors:
                neighbor_bit = neighbors & -neighbors
                neighbor = neighbor_bit.bit_length() - 1
                if assigned[neighbor] < 0:
                    old = saturation[neighbor]
                    saturation[neighbor] |= bit
                    if saturation[neighbor] != old:
                        changed.append((neighbor, old))
                neighbors ^= neighbor_bit
            if visit(colored + 1):
                return True
            for neighbor, old in changed:
                saturation[neighbor] = old
            assigned[vertex] = -1
        return False

    return visit(0)


def theta_exact(n: int, h_adj: tuple[int, ...], lower: int) -> int:
    for colors in range(max(1, lower), n + 1):
        if k_colorable(n, h_adj, colors):
            return colors
    raise AssertionError("unreachable")


def gamma_infinity_exact(
    n: int, g_adj: tuple[int, ...], lower: int
) -> tuple[int, int]:
    for size in range(lower, n + 1):
        kernel, _ = eternal_kernel(n, size, g_adj)
        if kernel:
            return size, len(kernel)
    raise AssertionError("unreachable")


def direct_swap(guard: int, target: int) -> int:
    return (S_MASK ^ (1 << guard)) | (1 << target)


def list_coloring_exists(
    n: int,
    h_adj: tuple[int, ...],
    lists: dict[int, frozenset[int]],
    *,
    include_x: bool,
    x_fixed: int = 0,
) -> bool:
    assigned = [-1] * n
    assigned[0], assigned[1], assigned[2] = 0, 1, 2
    vertices = [
        vertex
        for vertex in range(3, n)
        if include_x or vertex != X
    ]
    effective = dict(lists)
    if include_x:
        effective[X] = frozenset((x_fixed,))

    def visit(remaining: tuple[int, ...]) -> bool:
        if not remaining:
            return True
        best_vertex = -1
        best_colors: tuple[int, ...] | None = None
        for vertex in remaining:
            colors = tuple(
                color
                for color in effective[vertex]
                if all(
                    assigned[neighbor] != color
                    for neighbor in range(n)
                    if assigned[neighbor] >= 0
                    and h_adj[vertex] & (1 << neighbor)
                )
            )
            if not colors:
                return False
            if best_colors is None or len(colors) < len(best_colors):
                best_vertex, best_colors = vertex, colors
        assert best_colors is not None
        rest = tuple(v for v in remaining if v != best_vertex)
        for color in best_colors:
            assigned[best_vertex] = color
            if visit(rest):
                assigned[best_vertex] = -1
                return True
            assigned[best_vertex] = -1
        return False

    return visit(tuple(vertices))


def exact_family_predicate(
    n: int, g_adj: tuple[int, ...], h_adj: tuple[int, ...]
) -> list[dict]:
    eligible_new = frozenset(
        guard for guard in range(3) if g_adj[guard] & (1 << 9)
    )
    witnesses = []
    for subset_bits in range(1, 1 << 3):
        new_list = frozenset(
            guard for guard in range(3) if subset_bits & (1 << guard)
        )
        if len(new_list) == 3 or not new_list <= eligible_new:
            continue
        lists = dict(OLD_LISTS)
        lists[9] = new_list
        banned = frozenset(
            direct_swap(guard, target)
            for target, allowed in lists.items()
            for guard in range(3)
            if guard not in allowed
        )
        family, rounds = eternal_kernel(n, 3, g_adj, banned=banned)
        required = {S_MASK} | {
            direct_swap(guard, target)
            for target, allowed in lists.items()
            for guard in allowed
        }
        if not required <= family:
            continue
        base_sat = list_coloring_exists(
            n, h_adj, lists, include_x=False
        )
        augmented_sat = list_coloring_exists(
            n, h_adj, lists, include_x=True, x_fixed=0
        )
        witnesses.append(
            {
                "new_list": sorted(new_list),
                "family_states": len(family),
                "deletion_rounds": list(rounds),
                "base_list_coloring_sat": base_sat,
                "augmented_x0_list_coloring_sat": augmented_sat,
                "augmentation_sensitive": base_sat and not augmented_sat,
            }
        )
    return witnesses


def canonicalize(g6_records: list[str]) -> list[str]:
    proc = subprocess.run(
        [str(LABELG), "-q"],
        input=("\n".join(g6_records) + "\n").encode("ascii"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    records = proc.stdout.decode("ascii").splitlines()
    assert len(records) == len(g6_records)
    return records


def main() -> None:
    base_h_adj = adjacency_masks(BASE_N, BASE_H_EDGES)
    base_g_adj = complement_masks(BASE_N, base_h_adj)
    base_g_edges = graph_edges_from_adj(BASE_N, base_g_adj)
    assert graph6(BASE_N, base_g_edges) == "HFzvvn{"
    base_canonical = canonicalize(["HFzvvn{"])
    assert base_canonical == ["Hvzax|~"]

    raw_records = []
    rows = []
    for extension_mask in range(1 << BASE_N):
        h_edges = make_h_edges(extension_mask)
        h_adj = adjacency_masks(N, h_edges)
        g_adj = complement_masks(N, h_adj)
        g_edges = graph_edges_from_adj(N, g_adj)
        raw_g6 = graph6(N, g_edges)
        raw_records.append(raw_g6)

        gamma = gamma_exact(N, g_adj)
        alpha = alpha_exact(N, g_adj)
        gamma_inf, unrestricted_kernel_states = gamma_infinity_exact(
            N, g_adj, gamma
        )
        theta = theta_exact(N, h_adj, alpha)
        witnesses = exact_family_predicate(N, g_adj, h_adj)
        rows.append(
            {
                "extension_h_mask": extension_mask,
                "extension_h_neighbors": [
                    v for v in range(BASE_N) if extension_mask & (1 << v)
                ],
                "labeled_graph6": raw_g6,
                "gamma": gamma,
                "alpha": alpha,
                "gamma_infinity": gamma_inf,
                "theta": theta,
                "unrestricted_optimal_kernel_states": (
                    unrestricted_kernel_states
                ),
                "family_witness_count": len(witnesses),
                "augmentation_sensitive_witness_count": sum(
                    witness["augmentation_sensitive"]
                    for witness in witnesses
                ),
                "family_witnesses": witnesses,
            }
        )

    canonical_records = canonicalize(raw_records)
    for row, canonical in zip(rows, canonical_records):
        row["canonical_graph6"] = canonical

    parameter_counts = Counter(
        (
            row["gamma"],
            row["alpha"],
            row["gamma_infinity"],
            row["theta"],
        )
        for row in rows
    )
    canonical_to_rows: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        canonical_to_rows[row["canonical_graph6"]].append(row)

    property_rows = [
        row for row in rows if row["augmentation_sensitive_witness_count"]
    ]
    equality_rows = [
        row
        for row in property_rows
        if row["gamma"]
        == row["alpha"]
        == row["gamma_infinity"]
        == 3
    ]
    property_canonical = sorted(
        {row["canonical_graph6"] for row in property_rows}
    )
    equality_canonical = sorted(
        {row["canonical_graph6"] for row in equality_rows}
    )
    canonical_parameter_counts = Counter(
        (
            members[0]["gamma"],
            members[0]["alpha"],
            members[0]["gamma_infinity"],
            members[0]["theta"],
        )
        for members in canonical_to_rows.values()
    )
    assert all(
        len(
            {
                (
                    member["gamma"],
                    member["alpha"],
                    member["gamma_infinity"],
                    member["theta"],
                )
                for member in members
            }
        )
        == 1
        for members in canonical_to_rows.values()
    )

    csv_path = HERE / "extensions.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        fieldnames = [
            "extension_h_mask",
            "extension_h_neighbors",
            "labeled_graph6",
            "canonical_graph6",
            "gamma",
            "alpha",
            "gamma_infinity",
            "theta",
            "unrestricted_optimal_kernel_states",
            "family_witness_count",
            "augmentation_sensitive_witness_count",
            "family_witnesses",
        ]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            csv_row = dict(row)
            for key in (
                "extension_h_neighbors",
                "family_witnesses",
            ):
                csv_row[key] = json.dumps(csv_row[key], separators=(",", ":"))
            writer.writerow(csv_row)

    summary = {
        "status": "PASS",
        "scope": {
            "base_labeled_graph6": "HFzvvn{",
            "base_canonical_graph6": "Hvzax|~",
            "extension_convention": (
                "mask bits are H-neighbors of new vertex 9"
            ),
            "labeled_extensions": len(rows),
            "canonical_unlabeled_graphs": len(canonical_to_rows),
        },
        "predicate": {
            "old_response_lists_exact": {
                str(vertex): sorted(colors)
                for vertex, colors in OLD_LISTS.items()
            },
            "new_response_list": (
                "existentially quantified over nonempty proper subsets of S"
            ),
            "family_quantifier": (
                "exact via greatest safe kernel under direct-swap bans"
            ),
            "unique_full_target": 3,
            "augmentation": "fix target 3 to anchor color 0",
            "augmentation_sensitive_requires": (
                "base list-coloring SAT and augmented list-coloring UNSAT"
            ),
        },
        "labeled_parameter_counts": {
            ",".join(map(str, key)): value
            for key, value in sorted(parameter_counts.items())
        },
        "canonical_parameter_counts": {
            ",".join(map(str, key)): value
            for key, value in sorted(canonical_parameter_counts.items())
        },
        "property_labeled_extensions": len(property_rows),
        "property_canonical_graphs": len(property_canonical),
        "gamma3_equality_property_labeled_extensions": len(equality_rows),
        "gamma3_equality_property_canonical_graphs": len(equality_canonical),
        "property_canonical_graph6": property_canonical,
        "gamma3_equality_property_canonical_graph6": equality_canonical,
        "gamma3_equality_witness_rows": equality_rows,
    }
    csv_sha256 = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    summary["extensions_csv_sha256"] = csv_sha256
    summary_path = HERE / "summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
