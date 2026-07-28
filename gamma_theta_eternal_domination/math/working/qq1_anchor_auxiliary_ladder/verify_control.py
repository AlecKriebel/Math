#!/usr/bin/env python3
"""Standalone audit of the order-18 QQ1 anchor-protection control.

The verifier imports neither the SAT discovery encoder nor another campaign
evaluator.  It decodes one fixed labeled graph6 record into integer bitsets,
recomputes all five parameters, constructs literal one-guard kernels by
synchronous greatest-fixed-point deletion, and checks the complete named
QQ1 data and every protected or dominating pair.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
from collections import Counter
from pathlib import Path


LABELED_GRAPH6 = "QslallyN\\~Y^v^|^z~~V|ve~^}G"
CANONICAL_GRAPH6 = "QpMu]qnvvJb~Tz]mnx~nnZ~|~~W"
LABELS = {
    "u": 0,
    "x": 1,
    "p": 2,
    "q": 3,
    "r": 4,
    "b": 5,
    "c": 6,
    "d": 7,
    "w": 8,
    "z": 9,
}

EXPECTED_DOMINATING_PAIRS = (
    (0, 14),
    (0, 17),
    (4, 14),
    (5, 10),
    (5, 12),
    (5, 14),
    (7, 12),
    (7, 14),
    (7, 15),
    (7, 17),
    (8, 10),
    (8, 12),
    (8, 13),
    (8, 14),
    (8, 17),
    (9, 11),
    (9, 14),
    (9, 15),
    (9, 16),
    (9, 17),
    (10, 11),
    (10, 12),
    (10, 13),
    (10, 14),
    (10, 15),
    (10, 16),
    (10, 17),
    (12, 15),
    (13, 16),
    (15, 16),
)

EXPECTED_AUXILIARY_WITNESSES = {
    "2,10": (1,),
    "2,11": (16,),
    "2,12": (6,),
    "2,13": (6, 17),
    "2,14": (17,),
    "2,15": (3, 17),
    "2,16": (11,),
    "2,17": (14,),
    "3,10": (1,),
    "3,11": (2, 5),
    "3,12": (2,),
    "3,13": (15,),
    "3,14": (2,),
    "3,15": (5,),
    "3,16": (2,),
    "3,17": (2, 15),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_graph6(record: str) -> tuple[int, ...]:
    values = tuple(ord(character) - 63 for character in record)
    require(values and 0 <= values[0] <= 62, "only short graph6 is supported")
    order = values[0]
    bits = tuple(
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    )
    needed = order * (order - 1) // 2
    require(len(bits) >= needed, "truncated graph6 record")
    require(not any(bits[needed:]), "nonzero graph6 padding")
    adjacency = [0] * order
    cursor = 0
    for right in range(1, order):
        for left in range(right):
            if bits[cursor]:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
            cursor += 1
    return tuple(adjacency)


def encode_graph6(adjacency: tuple[int, ...]) -> str:
    order = len(adjacency)
    require(order <= 62, "only short graph6 is supported")
    bits = [
        int(bool(adjacency[left] & (1 << right)))
        for right in range(1, order)
        for left in range(right)
    ]
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for offset in range(0, len(bits), 6):
        value = 0
        for bit in bits[offset : offset + 6]:
            value = 2 * value + bit
        payload.append(chr(value + 63))
    return chr(order + 63) + "".join(payload)


def mask(vertices) -> int:
    result = 0
    for vertex in vertices:
        result |= 1 << vertex
    return result


def vertices(state: int):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def subsets(order: int, size: int):
    for choice in itertools.combinations(range(order), size):
        yield mask(choice)


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(not (adjacency[vertex] & (state ^ (1 << vertex))) for vertex in vertices(state))


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("finite search found no witness")


def independence_number(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    for size in range(order, 0, -1):
        if any(independent(adjacency, state) for state in subsets(order, size)):
            return size
    return 0


def kernel_with_ranks(adjacency: tuple[int, ...], guard_count: int):
    order = len(adjacency)
    family = {
        state
        for state in subsets(order, guard_count)
        if dominates(adjacency, state)
    }
    ranks: dict[int, int] = {}
    waves: list[int] = []
    round_number = 1
    while True:
        removed = set()
        for state in family:
            for target in range(order):
                target_bit = 1 << target
                if state & target_bit:
                    continue
                if not any(
                    adjacency[guard] & target_bit
                    and ((state ^ (1 << guard)) | target_bit) in family
                    for guard in vertices(state)
                ):
                    removed.add(state)
                    break
        if not removed:
            return family, ranks, tuple(waves)
        for state in removed:
            ranks[state] = round_number
        family.difference_update(removed)
        waves.append(len(removed))
        round_number += 1


def clique_partition(adjacency: tuple[int, ...]):
    order = len(adjacency)
    ordering = sorted(range(order), key=lambda vertex: (-adjacency[vertex].bit_count(), vertex))
    for part_count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(part_count)]

        def extend(offset: int, used: int) -> bool:
            if offset == order:
                return True
            vertex = ordering[offset]
            for part in range(min(used + 1, part_count)):
                if part == used and used == part_count:
                    continue
                if all(adjacency[vertex] & (1 << member) for member in parts[part]):
                    parts[part].append(vertex)
                    if extend(offset + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if extend(0, 0):
            return tuple(tuple(sorted(part)) for part in parts if part)
    raise AssertionError("singleton clique partition must exist")


def common_nonneighbors(adjacency: tuple[int, ...], left: int, right: int):
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (left, right)
        and not adjacency[left] & (1 << vertex)
        and not adjacency[right] & (1 << vertex)
    )


def edge_list(adjacency: tuple[int, ...]):
    return tuple(
        (left, right)
        for left in range(len(adjacency))
        for right in range(left + 1, len(adjacency))
        if adjacency[left] & (1 << right)
    )


def canonicalize(labelg: Path, record: str) -> str:
    process = subprocess.run(
        [str(labelg.resolve()), "-q"],
        input=record + "\n",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    require(not process.stderr, f"labelg stderr is nonempty: {process.stderr!r}")
    rows = process.stdout.splitlines()
    require(len(rows) == 1, "labelg did not emit exactly one record")
    return rows[0]


def evaluate(labelg: Path):
    adjacency = decode_graph6(LABELED_GRAPH6)
    require(encode_graph6(adjacency) == LABELED_GRAPH6, "graph6 round trip failed")
    require(canonicalize(labelg, LABELED_GRAPH6) == CANONICAL_GRAPH6, "canonical graph6 mismatch")
    order = len(adjacency)
    edges = edge_list(adjacency)
    require((order, len(edges)) == (18, 114), "wrong graph order or size")

    gamma = minimum_size(order, lambda state: dominates(adjacency, state))
    i_value = minimum_size(
        order,
        lambda state: independent(adjacency, state) and dominates(adjacency, state),
    )
    alpha = independence_number(adjacency)
    kernels = {
        guard_count: kernel_with_ranks(adjacency, guard_count)
        for guard_count in (1, 2, 3)
    }
    gamma_infinity = next(
        guard_count for guard_count in (1, 2, 3) if kernels[guard_count][0]
    )
    partition = clique_partition(adjacency)
    theta = len(partition)
    require([gamma, i_value, alpha, gamma_infinity, theta] == [2, 3, 3, 3, 3], "wrong parameter vector")
    require(
        partition
        == (
            (0, 3, 7, 10, 11, 12, 13, 14),
            (2, 4, 8, 9, 15),
            (1, 5, 6, 16, 17),
        ),
        "unexpected minimum clique partition",
    )

    family, ranks, waves = kernels[3]
    require(len(family) == 473, "wrong greatest triple-family size")
    require(waves == (2, 8, 11, 28, 33, 18, 17, 34, 18), "wrong triple deletion waves")
    require(not kernels[1][0] and not kernels[2][0], "too few guards survive")
    require(kernels[2][2] == (30,), "wrong two-guard deletion wave")

    u, x, p, q, r, b, c, d, w, z = range(10)
    required_edges = (
        (u, x), (u, p), (u, q), (u, r), (u, d),
        (p, r), (q, r), (p, b), (q, c),
        (x, b), (x, c), (b, c),
        (d, p), (d, q), (d, b), (d, c),
        (w, x), (w, r), (z, d), (z, w),
    )
    required_nonedges = (
        (x, p), (x, q), (p, q), (x, r),
        (u, b), (b, r), (b, q),
        (u, c), (c, r), (c, p),
        (x, d), (r, d), (u, w), (d, w), (u, z), (x, z),
    )
    require(all(adjacency[left] & (1 << right) for left, right in required_edges), "missing named QQ1 edge")
    require(not any(adjacency[left] & (1 << right) for left, right in required_nonedges), "present named QQ1 nonedge")

    states = {
        "T": (x, p, q),
        "U": (u, b, c),
        "R": (r, b, c),
        "I": (x, r, d),
        "A": (u, x, d),
        "K": (u, d, w),
        "E": (x, d, w),
        "F": (r, d, w),
        "bridge": (u, w, z),
        "ux_ridge": (u, x, z),
        "outer_bow_tie": (b, w, 16),
    }
    state_masks = {name: mask(state) for name, state in states.items()}
    require(all(state in family for state in state_masks.values()), "missing retained named state")
    B = mask((u, p, q))
    O = mask((u, r, d))
    require(dominates(adjacency, B) and ranks.get(B) == 1, "B must have deletion rank one")
    require(dominates(adjacency, O) and ranks.get(O) == 3, "O must have deletion rank three")

    deleting_successors = {}
    expected_misses = {u: x, p: b, q: c}
    for guard in (u, p, q):
        successor = (B ^ (1 << guard)) | (1 << r)
        missed = tuple(
            vertex
            for vertex in range(order)
            if not (successor & (1 << vertex))
            and not any(adjacency[member] & (1 << vertex) for member in vertices(successor))
        )
        require(not dominates(adjacency, successor), "rank-one successor unexpectedly dominates")
        require(expected_misses[guard] in missed, "private witness is absent")
        deleting_successors[str(guard)] = {
            "state": tuple(vertices(successor)),
            "missed_vertices": missed,
        }

    activity_sources = []
    for third in range(order):
        source = mask((u, b, third))
        if source.bit_count() == 3 and independent(adjacency, source):
            target = (source ^ (1 << u)) | (1 << x)
            activity_sources.append(
                {
                    "third": third,
                    "source_retained": source in family,
                    "target_retained": target in family,
                }
            )
    require(activity_sources == [{"third": 8, "source_retained": True, "target_retained": True}], "wrong u-to-x activity roots")
    require(B not in family, "reverse x-to-u state unexpectedly survives")

    require(common_nonneighbors(adjacency, u, x) == (z,), "wrong ux witness set")
    require(common_nonneighbors(adjacency, u, d) == (w,), "wrong ud witness set")
    require(common_nonneighbors(adjacency, p, w) == (16,), "wrong pw repair witness")
    require(common_nonneighbors(adjacency, u, w) == (b,), "wrong outer u,w completion")
    require(common_nonneighbors(adjacency, d, w) == (16,), "wrong outer d,w completion")

    auxiliary_witnesses = {
        f"{anchor},{vertex}": common_nonneighbors(adjacency, anchor, vertex)
        for anchor in (p, q)
        for vertex in range(10, order)
    }
    require(auxiliary_witnesses == EXPECTED_AUXILIARY_WITNESSES, "wrong p/q auxiliary witnesses")

    dominating_pairs = tuple(
        tuple(vertices(state))
        for state in subsets(order, 2)
        if dominates(adjacency, state)
    )
    require(dominating_pairs == EXPECTED_DOMINATING_PAIRS, "wrong dominating-pair list")
    protected_anchor_pairs = {
        anchor: tuple(
            vertex
            for vertex in range(order)
            if vertex != anchor and dominates(adjacency, mask((anchor, vertex)))
        )
        for anchor in (x, p, q)
    }
    require(protected_anchor_pairs == {x: (), p: (), q: ()}, "a pair touching T dominates")
    require(all(adjacency[left] & (1 << right) for left, right in dominating_pairs), "i=3 should make every dominating pair adjacent")

    edge_text = "".join(f"{left} {right}\n" for left, right in edges)
    require(sha256_bytes(LABELED_GRAPH6.encode("ascii")) == "99ddf436936152440c778efb79270a89e10feb8dd95d7033052e571a1bc3142c", "labeled graph6 digest mismatch")
    require(sha256_bytes(edge_text.encode("ascii")) == "6a6256204cff1a80d67e16be7efa67377f02b5c9d7c6a924cf6bbfc4ec7b738e", "edge-list digest mismatch")

    return {
        "schema": "QQ1-anchor-protection-control-audit-v1",
        "status": "VERIFIED",
        "classification": "FIXED_GAMMA2_BOUNDARY_CONTROL",
        "graph": {
            "labeled_graph6": LABELED_GRAPH6,
            "canonical_graph6": CANONICAL_GRAPH6,
            "labeled_graph6_sha256": sha256_bytes(LABELED_GRAPH6.encode("ascii")),
            "edge_list_sha256": sha256_bytes(edge_text.encode("ascii")),
            "order": order,
            "size": len(edges),
            "edge_list": edges,
        },
        "parameters": {
            "gamma": gamma,
            "i": i_value,
            "alpha": alpha,
            "gamma_infinity": gamma_infinity,
            "theta": theta,
            "minimum_clique_partition": partition,
        },
        "one_guard_kernel": {
            "sizes_k1_k2_k3": tuple(len(kernels[count][0]) for count in (1, 2, 3)),
            "triple_deletion_waves": waves,
            "triple_positive_rank_histogram": dict(sorted(Counter(ranks.values()).items())),
        },
        "qq1": {
            "labels": LABELS,
            "retained_states": {
                name: tuple(vertices(state)) for name, state in state_masks.items()
            },
            "B_rank": ranks[B],
            "O_rank": ranks[O],
            "rank_one_successors": deleting_successors,
            "u_to_x_activity_roots": activity_sources,
            "x_to_u_reverse_retained": B in family,
            "W_ux": common_nonneighbors(adjacency, u, x),
            "W_ud": common_nonneighbors(adjacency, u, d),
            "W_pw": common_nonneighbors(adjacency, p, w),
            "outer_completion_u_w": common_nonneighbors(adjacency, u, w),
            "outer_completion_d_w": common_nonneighbors(adjacency, d, w),
        },
        "anchor_protection": {
            "all_dominating_partners_of_x_p_q": protected_anchor_pairs,
            "p_q_auxiliary_common_nonneighbors": auxiliary_witnesses,
        },
        "escape": {
            "dominating_pair_count": len(dominating_pairs),
            "dominating_pairs": dominating_pairs,
            "core_auxiliary_pair_count": sum(left < 10 <= right for left, right in dominating_pairs),
            "auxiliary_auxiliary_pair_count": sum(10 <= left for left, _ in dominating_pairs),
            "displayed_dominating_pair": (u, 14),
        },
        "scope": (
            "This fixed gamma=2 graph refutes only the proposed all-order "
            "anchor-auxiliary obstruction. It is not a counterexample to "
            "the gamma-theta conjecture and certifies no finite UNSAT claim."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labelg", type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(evaluate(arguments.labelg), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
