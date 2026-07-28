#!/usr/bin/env python3
"""Clean-room checks for the full-list terminal-gate candidate.

This file imports no campaign evaluator and no candidate implementation.
It has two independent parts:

1. Exhaust every graph completion on the seven named vertices used by the
   proposed singleton-terminal attack.  For each completion, compute the
   greatest one-guard triple kernel after banning the six root swaps forced
   absent by the three singleton palettes.
2. Decode the named order-12 equality control and recompute its parameters,
   unrestricted/restricted kernels, palettes, and rank-decreasing terminal
   traces directly from the one-guard definition.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def pairs(n: int):
    for j in range(1, n):
        for i in range(j):
            yield i, j


def graph6_decode(record: str) -> tuple[int, tuple[int, ...]]:
    raw = record.encode("ascii")
    if not raw or raw[0] == 126:
        raise ValueError("checker supports only short graph6 records")
    n = raw[0] - 63
    needed = n * (n - 1) // 2
    bits: list[int] = []
    for byte in raw[1:]:
        value = byte - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    if len(bits) < needed:
        raise ValueError("truncated graph6 record")
    adj = [0] * n
    for bit, (i, j) in zip(bits[:needed], pairs(n)):
        if bit:
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    return n, tuple(adj)


def edge_count(adj: tuple[int, ...]) -> int:
    return sum(x.bit_count() for x in adj) // 2


def subset_vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def is_independent(mask: int, adj: tuple[int, ...]) -> bool:
    return all((adj[v] & mask) == 0 for v in subset_vertices(mask))


def dominates(mask: int, adj: tuple[int, ...]) -> bool:
    covered = mask
    for v in subset_vertices(mask):
        covered |= adj[v]
    return covered == (1 << len(adj)) - 1


def configurations(n: int, k: int):
    for vertices in itertools.combinations(range(n), k):
        yield sum(1 << v for v in vertices)


def legal_successors(state: int, attack: int, adj: tuple[int, ...]):
    """One occupied guard moves along one G edge to unoccupied attack."""
    if state & (1 << attack):
        raise ValueError("attacks must be unoccupied")
    for guard in subset_vertices(state & adj[attack]):
        yield (state ^ (1 << guard)) | (1 << attack)


def synchronous_kernel(
    adj: tuple[int, ...],
    k: int,
    banned: set[int] | None = None,
) -> tuple[set[int], dict[int, int], list[int]]:
    banned = banned or set()
    active = {
        state
        for state in configurations(len(adj), k)
        if state not in banned and dominates(state, adj)
    }
    rank: dict[int, int] = {}
    round_sizes: list[int] = []
    round_no = 1
    while True:
        delete: set[int] = set()
        for state in active:
            for attack in range(len(adj)):
                if state & (1 << attack):
                    continue
                if not any(succ in active for succ in legal_successors(state, attack, adj)):
                    delete.add(state)
                    break
        if not delete:
            break
        for state in delete:
            rank[state] = round_no
        active.difference_update(delete)
        round_sizes.append(len(delete))
        round_no += 1
    return active, rank, round_sizes


def parameter_gamma(adj: tuple[int, ...]) -> int:
    n = len(adj)
    for k in range(1, n + 1):
        if any(dominates(state, adj) for state in configurations(n, k)):
            return k
    raise AssertionError


def parameter_alpha(adj: tuple[int, ...]) -> int:
    n = len(adj)
    return max(mask.bit_count() for mask in range(1 << n) if is_independent(mask, adj))


def parameter_i(adj: tuple[int, ...]) -> int:
    n = len(adj)
    return min(
        mask.bit_count()
        for mask in range(1, 1 << n)
        if is_independent(mask, adj) and dominates(mask, adj)
    )


def colorable(adj: tuple[int, ...], colors: int) -> bool:
    n = len(adj)
    assignment = [-1] * n

    def choose_vertex() -> int | None:
        best = None
        best_key = None
        for v in range(n):
            if assignment[v] >= 0:
                continue
            used = {assignment[w] for w in subset_vertices(adj[v]) if assignment[w] >= 0}
            key = (len(used), adj[v].bit_count())
            if best_key is None or key > best_key:
                best = v
                best_key = key
        return best

    def search() -> bool:
        v = choose_vertex()
        if v is None:
            return True
        forbidden = {assignment[w] for w in subset_vertices(adj[v]) if assignment[w] >= 0}
        for color in range(colors):
            if color in forbidden:
                continue
            assignment[v] = color
            if search():
                return True
            assignment[v] = -1
        return False

    return search()


def parameter_theta(adj: tuple[int, ...]) -> int:
    n = len(adj)
    full = (1 << n) - 1
    complement = tuple((full ^ (1 << v) ^ adj[v]) for v in range(n))
    for colors in range(1, n + 1):
        if colorable(complement, colors):
            return colors
    raise AssertionError


def mask(vertices) -> int:
    return sum(1 << v for v in vertices)


def names(state: int, labels: tuple[str, ...]) -> list[str]:
    return [labels[v] for v in subset_vertices(state)]


def local_singleton_exhaustion() -> dict:
    # x,a,b,c,ra,rb,rc
    labels = ("x", "a", "b", "c", "ra", "rb", "rc")
    x, a, b, c, ra, rb, rc = range(7)
    S = (a, b, c)
    terminals = {
        a: mask((ra, b, c)),
        b: mask((a, rb, c)),
        c: mask((a, b, rc)),
    }
    r_for = {a: ra, b: rb, c: rc}

    forced_on = {
        tuple(sorted(edge))
        for edge in (
            (x, a),
            (x, b),
            (x, c),
            (a, ra),
            (b, rb),
            (c, rc),
        )
    }
    forced_off = {
        tuple(sorted(edge))
        for edge in (
            (a, b),
            (a, c),
            (b, c),
            (x, ra),
            (x, rb),
            (x, rc),
        )
    }
    all_pairs = list(pairs(7))
    optional = [edge for edge in all_pairs if edge not in forced_on | forced_off]
    if len(optional) != 9:
        raise AssertionError(optional)

    banned_by_color: dict[int, set[int]] = {}
    for own in S:
        r = r_for[own]
        banned_by_color[own] = {
            mask(tuple(v for v in S if v != omitted) + (r,))
            for omitted in S
            if omitted != own
        }
    all_banned = set().union(*banned_by_color.values())
    if len(all_banned) != 6:
        raise AssertionError(all_banned)

    completions = 0
    locally_dominating_terminals = 0
    countermodels = 0
    branch_absent = 0
    branch_present = 0
    two_color_mutation_models = {labels[own]: 0 for own in S}
    example_mutations: dict[str, dict] = {}

    for optional_bits in range(1 << len(optional)):
        adj = [0] * 7
        edges = set(forced_on)
        for bit, edge in enumerate(optional):
            if optional_bits & (1 << bit):
                edges.add(edge)
        for u, v in edges:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
        adj_t = tuple(adj)
        completions += 1

        required = set(terminals.values())
        if not all(dominates(state, adj_t) for state in required):
            continue
        locally_dominating_terminals += 1
        kernel, _, _ = synchronous_kernel(adj_t, 3, all_banned)
        if required <= kernel:
            countermodels += 1
            dab = mask((ra, rb, c))
            if dab in kernel:
                branch_present += 1
            else:
                branch_absent += 1

        # Remove both singleton bans for one color.  This checks that the
        # three-color quantifier is essential to the local obstruction.
        for relaxed in S:
            relaxed_bans = all_banned - banned_by_color[relaxed]
            relaxed_kernel, _, _ = synchronous_kernel(adj_t, 3, relaxed_bans)
            if required <= relaxed_kernel:
                key = labels[relaxed]
                two_color_mutation_models[key] += 1
                if key not in example_mutations:
                    example_mutations[key] = {
                        "edges": [[labels[u], labels[v]] for u, v in sorted(edges)],
                        "kernel_size": len(relaxed_kernel),
                    }

    return {
        "labels": list(labels),
        "forced_on": [[labels[u], labels[v]] for u, v in sorted(forced_on)],
        "forced_off": [[labels[u], labels[v]] for u, v in sorted(forced_off)],
        "optional_pairs": [[labels[u], labels[v]] for u, v in optional],
        "completion_count": completions,
        "locally_dominating_terminal_count": locally_dominating_terminals,
        "singleton_terminal_countermodels": countermodels,
        "candidate_branch_counts_among_countermodels": {
            "D_ab_absent": branch_absent,
            "D_ab_present": branch_present,
        },
        "relax_one_color_counts": two_color_mutation_models,
        "relax_one_color_examples": example_mutations,
        "gate_label_combinations": 3**3,
    }


def root_palette(
    adj: tuple[int, ...],
    family: set[int],
    root: tuple[int, int, int],
    vertex: int,
) -> list[int]:
    root_mask = mask(root)
    return [
        anchor
        for anchor in root
        if (adj[anchor] & (1 << vertex))
        and ((root_mask ^ (1 << anchor)) | (1 << vertex)) in family
    ]


def deletion_witness_attacks(
    state: int,
    rank: dict[int, int],
    active_kernel: set[int],
    adj: tuple[int, ...],
) -> list[int]:
    current_rank = rank[state]
    threshold = {
        candidate
        for candidate, candidate_rank in rank.items()
        if candidate_rank >= current_rank
    } | active_kernel
    return [
        attack
        for attack in range(len(adj))
        if not state & (1 << attack)
        and not any(succ in threshold for succ in legal_successors(state, attack, adj))
    ]


def reachable_terminals(
    start: int,
    banned: set[int],
    unrestricted_family: set[int],
    restricted_kernel: set[int],
    rank: dict[int, int],
    adj: tuple[int, ...],
) -> set[tuple[int, int]]:
    """Return (predecessor, terminal) pairs over every rank-decreasing trace."""
    todo = [start]
    seen = {start}
    terminals: set[tuple[int, int]] = set()
    while todo:
        state = todo.pop()
        for attack in deletion_witness_attacks(state, rank, restricted_kernel, adj):
            for succ in legal_successors(state, attack, adj):
                if succ not in unrestricted_family:
                    continue
                if succ in banned:
                    terminals.add((state, succ))
                elif succ in rank and rank[succ] < rank[state] and succ not in seen:
                    seen.add(succ)
                    todo.append(succ)
    return terminals


def equality_control() -> dict:
    record = "Ksv`f\\knJVis"
    n, adj = graph6_decode(record)
    if n != 12:
        raise AssertionError(n)

    gamma = parameter_gamma(adj)
    alpha = parameter_alpha(adj)
    indep_dom = parameter_i(adj)
    theta = parameter_theta(adj)
    greatest, _, unrestricted_rounds = synchronous_kernel(adj, 3)
    gamma_infinity = gamma if greatest else None
    if gamma != 3 or not greatest:
        raise AssertionError("control equality failed")

    root = (1, 2, 3)
    root_mask = mask(root)
    target = 0
    full_successors = {
        anchor: (root_mask ^ (1 << anchor)) | (1 << target) for anchor in root
    }
    target_full = all(
        (adj[anchor] & (1 << target)) and successor in greatest
        for anchor, successor in full_successors.items()
    )
    B = [v for v in range(n) if adj[target] & (1 << v) == 0 and v != target]
    complement_B_edges = [
        (u, v) for u, v in itertools.combinations(B, 2) if adj[u] & (1 << v) == 0
    ]
    palettes = {str(v): root_palette(adj, greatest, root, v) for v in B}

    restricted: dict[str, dict] = {}
    all_terminal_rows: list[dict] = []
    for anchor in root:
        banned = {
            (root_mask ^ (1 << anchor)) | (1 << b)
            for b in B
        }
        kernel, rank, rounds = synchronous_kernel(adj, 3, banned)
        start = full_successors[anchor]
        terminal_pairs = (
            reachable_terminals(start, banned, greatest, kernel, rank, adj)
            if start in rank
            else set()
        )
        rows = []
        for predecessor, terminal in sorted(terminal_pairs):
            outside = list(set(subset_vertices(terminal)) - set(root))
            if len(outside) != 1:
                raise AssertionError((anchor, terminal))
            r = outside[0]
            attacked_bits = terminal & ~predecessor
            mover_bits = predecessor & ~terminal
            if attacked_bits.bit_count() != 1 or mover_bits.bit_count() != 1:
                raise AssertionError((predecessor, terminal))
            attacked = attacked_bits.bit_length() - 1
            mover = mover_bits.bit_length() - 1
            base = root_mask ^ (1 << anchor)
            if attacked == r:
                gate = "direct_root_corridor" if mover == anchor else "nonroot_corridor"
            elif base & (1 << attacked):
                gate = "anchor_restoration"
            else:
                raise AssertionError((predecessor, terminal, attacked))
            diamond_missing_edges: list[list[int]] | None = None
            if gate == "nonroot_corridor":
                quartet = (target, anchor, mover, r)
                diamond_missing_edges = [
                    [u, v]
                    for u, v in itertools.combinations(quartet, 2)
                    if adj[u] & (1 << v) == 0
                ]
            row = {
                "color_anchor": anchor,
                "predecessor": list(subset_vertices(predecessor)),
                "attack": attacked,
                "mover": mover,
                "gate": gate,
                "terminal_vertex": r,
                "terminal_state": list(subset_vertices(terminal)),
                "palette": root_palette(adj, greatest, root, r),
                "diamond_missing_edges": diamond_missing_edges,
            }
            rows.append(row)
            all_terminal_rows.append(row)
        restricted[str(anchor)] = {
            "initial_allowed_dominating_states": sum(
                1
                for state in configurations(n, 3)
                if state not in banned and dominates(state, adj)
            ),
            "deletion_rounds": rounds,
            "kernel_size": len(kernel),
            "start_survives": start in kernel,
            "reachable_terminal_rows": rows,
        }

    return {
        "graph6": record,
        "order": n,
        "edge_count": edge_count(adj),
        "parameters": {
            "gamma": gamma,
            "i": indep_dom,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
        },
        "unrestricted_triple_kernel_size": len(greatest),
        "unrestricted_deletion_rounds": unrestricted_rounds,
        "root": list(root),
        "target": target,
        "target_full": target_full,
        "B": B,
        "complement_B_edges": [list(edge) for edge in complement_B_edges],
        "palettes": palettes,
        "restricted": restricted,
        "all_reachable_terminal_rows": all_terminal_rows,
    }


def main() -> None:
    local = local_singleton_exhaustion()
    control = equality_control()
    if local["completion_count"] != 512:
        raise AssertionError(local["completion_count"])
    if local["singleton_terminal_countermodels"] != 0:
        raise AssertionError(local["singleton_terminal_countermodels"])
    if not all(count > 0 for count in local["relax_one_color_counts"].values()):
        raise AssertionError(local["relax_one_color_counts"])
    if control["parameters"] != {
        "gamma": 3,
        "i": 3,
        "alpha": 3,
        "gamma_infinity": 3,
        "theta": 3,
    }:
        raise AssertionError(control["parameters"])
    if control["unrestricted_triple_kernel_size"] != 127:
        raise AssertionError(control["unrestricted_triple_kernel_size"])
    if control["B"] != [6, 8, 10, 11]:
        raise AssertionError(control["B"])
    if control["complement_B_edges"] != [[6, 8], [10, 11]]:
        raise AssertionError(control["complement_B_edges"])
    expected_kernel_sizes = {"1": 0, "2": 0, "3": 64}
    actual_kernel_sizes = {
        color: data["kernel_size"] for color, data in control["restricted"].items()
    }
    if actual_kernel_sizes != expected_kernel_sizes:
        raise AssertionError(actual_kernel_sizes)
    actual_rows = {
        (
            row["color_anchor"],
            tuple(row["predecessor"]),
            row["attack"],
            row["mover"],
            row["gate"],
            row["terminal_vertex"],
            tuple(row["terminal_state"]),
            tuple(row["palette"]),
            tuple(tuple(edge) for edge in (row["diamond_missing_edges"] or [])),
        )
        for row in control["all_reachable_terminal_rows"]
    }
    expected_rows = {
        (1, (2, 3, 4), 10, 4, "nonroot_corridor", 10, (2, 3, 10), (1, 2), ((0, 10),)),
        (1, (2, 3, 5), 11, 5, "nonroot_corridor", 11, (2, 3, 11), (1, 3), ((0, 11),)),
        (2, (1, 3, 7), 6, 7, "nonroot_corridor", 6, (1, 3, 6), (2, 3), ((0, 6),)),
        (2, (1, 3, 9), 8, 9, "nonroot_corridor", 8, (1, 3, 8), (1, 2), ((0, 8),)),
    }
    if actual_rows != expected_rows:
        raise AssertionError(actual_rows)

    result = {
        "schema": "full-list-terminal-gate-hostile-v1",
        "local_singleton_exhaustion": local,
        "equality_control": control,
    }
    canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "independent_result.json").write_text(canonical, encoding="utf-8")
    print(canonical, end="")
    print(
        "result_sha256="
        + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    )


if __name__ == "__main__":
    main()
