#!/usr/bin/env python3
"""Standalone exact audit of the supported asymmetric-edge bow tie."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


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


def adjacency_from_code(order: int, code: int) -> tuple[int, ...]:
    adjacency = [0] * order
    for index, (left, right) in enumerate(
        itertools.combinations(range(order), 2)
    ):
        if code & (1 << index):
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return tuple(adjacency)


def decode_graph6(record: str) -> tuple[int, ...]:
    values = tuple(ord(character) - 63 for character in record)
    require(values and 0 <= values[0] <= 62, "short graph6 only")
    order = values[0]
    bits = tuple(
        (value >> shift) & 1
        for value in values[1:]
        for shift in range(5, -1, -1)
    )
    needed = order * (order - 1) // 2
    require(len(bits) >= needed, "truncated graph6")
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


def independent(adjacency: tuple[int, ...], state: int) -> bool:
    return all(
        not adjacency[vertex] & (state ^ (1 << vertex))
        for vertex in vertices(state)
    )


def dominates(adjacency: tuple[int, ...], state: int) -> bool:
    covered = state
    for vertex in vertices(state):
        covered |= adjacency[vertex]
    return covered == (1 << len(adjacency)) - 1


def eternal(adjacency: tuple[int, ...], family: set[int]) -> bool:
    if not family or not all(dominates(adjacency, state) for state in family):
        return False
    for state in family:
        for target in range(len(adjacency)):
            target_bit = 1 << target
            if state & target_bit:
                continue
            if not any(
                adjacency[guard] & target_bit
                and ((state ^ (1 << guard)) | target_bit) in family
                for guard in vertices(state)
            ):
                return False
    return True


def greatest_family(adjacency: tuple[int, ...], size: int = 3) -> set[int]:
    family = {
        state
        for state in subsets(len(adjacency), size)
        if dominates(adjacency, state)
    }
    while True:
        removed = set()
        for state in family:
            for target in range(len(adjacency)):
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
            return family
        family.difference_update(removed)


def common_nonneighbors(
    adjacency: tuple[int, ...], left: int, right: int
) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(adjacency))
        if vertex not in (left, right)
        and not adjacency[left] & (1 << vertex)
        and not adjacency[right] & (1 << vertex)
    )


def active(
    adjacency: tuple[int, ...],
    family: set[int],
    source: int,
    target: int,
) -> bool:
    if not adjacency[source] & (1 << target):
        return False
    for state in subsets(len(adjacency), 3):
        if (
            state in family
            and state & (1 << source)
            and not state & (1 << target)
            and independent(adjacency, state)
            and ((state ^ (1 << source)) | (1 << target)) in family
        ):
            return True
    return False


def exact_static_three(adjacency: tuple[int, ...]) -> bool:
    order = len(adjacency)
    if any(dominates(adjacency, state) for state in subsets(order, 2)):
        return False
    if not any(dominates(adjacency, state) for state in subsets(order, 3)):
        return False
    if not any(independent(adjacency, state) for state in subsets(order, 3)):
        return False
    return not any(
        independent(adjacency, state) for state in subsets(order, 4)
    )


def clique(adjacency: tuple[int, ...], members: tuple[int, ...]) -> bool:
    return all(
        adjacency[left] & (1 << right)
        for left, right in itertools.combinations(members, 2)
    )


def supported(
    family: set[int], left: int, right: int
) -> bool:
    pair = (1 << left) | (1 << right)
    return any(state & pair == pair for state in family)


def retained_fan(
    adjacency: tuple[int, ...],
    family: set[int],
    left: int,
    right: int,
) -> bool:
    witnesses = common_nonneighbors(adjacency, left, right)
    return bool(witnesses) and all(
        mask((left, right, witness)) in family for witness in witnesses
    )


def audit_orientation(
    adjacency: tuple[int, ...],
    family: set[int],
    u: int,
    x: int,
) -> Counter:
    require(adjacency[u] & (1 << x), "orientation is not a graph edge")
    require(supported(family, u, x), "asymmetric edge is not supported")
    require(active(adjacency, family, u, x), "forward activity absent")
    require(not active(adjacency, family, x, u), "reverse activity present")

    counts = Counter()
    Z = common_nonneighbors(adjacency, u, x)
    require(Z and clique(adjacency, Z), "bad supported central fan")
    require(
        all(mask((u, x, z)) in family for z in Z),
        "supported ux fan is not retained",
    )

    for z in Z:
        P = common_nonneighbors(adjacency, u, z)
        Q = common_nonneighbors(adjacency, x, z)
        require(P and Q, "gamma-three side completion is empty")
        require(set(P).isdisjoint(Q), "bow-tie sides overlap")
        require(clique(adjacency, P), "P is not a clique")
        require(clique(adjacency, Q), "Q is not a clique")
        require(clique(adjacency, tuple(P) + tuple(Q)), "join is incomplete")
        R = mask((u, x, z))
        require(R in family, "central state absent")

        for g in P:
            S = mask((u, z, g))
            X = mask((x, z, g))
            require(independent(adjacency, S) and S in family, "bad P root")
            require(X in family, "active transport state absent")
            require(adjacency[x] & (1 << g), "xg edge absent")
            require(
                retained_fan(adjacency, family, x, g),
                "xg retained fan absent",
            )
            require(
                active(adjacency, family, x, g)
                and active(adjacency, family, g, x),
                "xg is not reciprocal",
            )

            for h in Q:
                T = mask((x, z, h))
                O = mask((u, z, h))
                M = mask((z, g, h))
                require(
                    independent(adjacency, T) and T in family,
                    "bad Q root",
                )
                require(O not in family, "inactive central state retained")
                require(M in family, "mixed bow-tie state absent")
                require(adjacency[u] & (1 << h), "uh edge absent")
                require(adjacency[g] & (1 << h), "gh edge absent")
                require(
                    all(
                        mask((u, h, e)) not in family
                        for e in common_nonneighbors(adjacency, u, h)
                    ),
                    "uh omitted fan is mixed",
                )
                require(
                    active(adjacency, family, u, h)
                    and active(adjacency, family, h, u),
                    "uh is not reciprocal",
                )
                require(
                    retained_fan(adjacency, family, g, h),
                    "gh retained fan absent",
                )
                counts["mixed_cells"] += 1
        counts["ux_witnesses"] += 1
    counts["orientations"] += 1
    return counts


def minimum_size(order: int, predicate) -> int:
    for size in range(1, order + 1):
        if any(predicate(state) for state in subsets(order, size)):
            return size
    raise AssertionError("minimum absent")


def independence_number(adjacency: tuple[int, ...]) -> int:
    for size in range(len(adjacency), 0, -1):
        if any(
            independent(adjacency, state)
            for state in subsets(len(adjacency), size)
        ):
            return size
    return 0


def clique_cover_number(adjacency: tuple[int, ...]) -> int:
    order = len(adjacency)
    for count in range(1, order + 1):
        parts: list[list[int]] = [[] for _ in range(count)]

        def extend(vertex: int, used: int) -> bool:
            if vertex == order:
                return True
            for part in range(min(used + 1, count)):
                if all(
                    adjacency[vertex] & (1 << member)
                    for member in parts[part]
                ):
                    parts[part].append(vertex)
                    if extend(vertex + 1, max(used, part + 1)):
                        return True
                    parts[part].pop()
            return False

        if extend(0, 0):
            return count
    raise AssertionError("clique cover absent")


def exact_eternal_number(adjacency: tuple[int, ...]) -> int:
    for size in range(1, len(adjacency) + 1):
        if greatest_family(adjacency, size):
            return size
    raise AssertionError("eternal number absent")


def parameter_vector(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    order = len(adjacency)
    return (
        minimum_size(order, lambda state: dominates(adjacency, state)),
        minimum_size(
            order,
            lambda state: independent(adjacency, state)
            and dominates(adjacency, state),
        ),
        independence_number(adjacency),
        exact_eternal_number(adjacency),
        clique_cover_number(adjacency),
    )


def census() -> dict[str, object]:
    labeled_graphs = 0
    applicable_families = 0
    applicable_graphs = set()
    audit_counts = Counter()
    for order in range(3, 6):
        for code in range(1 << (order * (order - 1) // 2)):
            labeled_graphs += 1
            adjacency = adjacency_from_code(order, code)
            if not exact_static_three(adjacency):
                continue
            triples = tuple(
                state
                for state in subsets(order, 3)
                if dominates(adjacency, state)
            )
            for family_code in range(1, 1 << len(triples)):
                family = {
                    state
                    for index, state in enumerate(triples)
                    if family_code & (1 << index)
                }
                if not eternal(adjacency, family):
                    continue
                applicable_families += 1
                applicable_graphs.add((order, code))
                for u in range(order):
                    for x in range(order):
                        if (
                            u != x
                            and adjacency[u] & (1 << x)
                            and supported(family, u, x)
                            and active(adjacency, family, u, x)
                            and not active(adjacency, family, x, u)
                        ):
                            audit_counts.update(
                                audit_orientation(
                                    adjacency, family, u, x
                                )
                            )
    return {
        "labeled_graphs_examined_orders_3_to_5": labeled_graphs,
        "applicable_graphs": len(applicable_graphs),
        "applicable_eternal_families": applicable_families,
        "theorem_obligations": dict(sorted(audit_counts.items())),
    }


def equality_control() -> dict[str, object]:
    record = "D]?"
    adjacency = decode_graph6(record)
    require(encode_graph6(adjacency) == record, "D]? round trip")
    family = {
        mask(state)
        for state in ((0, 1, 4), (0, 2, 4), (0, 3, 4), (1, 2, 4), (2, 3, 4))
    }
    require(eternal(adjacency, family), "specified D]? family not eternal")
    require(
        parameter_vector(adjacency) == (3, 3, 3, 3, 3),
        "wrong D]? parameters",
    )
    counts = audit_orientation(adjacency, family, 1, 2)
    return {
        "graph6": record,
        "parameters": [3, 3, 3, 3, 3],
        "family": [list(vertices(state)) for state in sorted(family)],
        "orientation": [1, 2],
        "W_ux": list(common_nonneighbors(adjacency, 1, 2)),
        "P": list(common_nonneighbors(adjacency, 1, 4)),
        "Q": list(common_nonneighbors(adjacency, 2, 4)),
        "audit_counts": dict(sorted(counts.items())),
    }


def gamma_two_qq1_boundary() -> dict[str, object]:
    record = "QslallyN\\~Y^v^|^z~~V|ve~^}G"
    adjacency = decode_graph6(record)
    require(encode_graph6(adjacency) == record, "C-169 round trip")
    family = greatest_family(adjacency, 3)
    require(len(family) == 473, "wrong C-169 triple kernel")
    require(
        parameter_vector(adjacency) == (2, 3, 3, 3, 3),
        "wrong C-169 parameters",
    )
    u, x, d, w, z = 0, 1, 7, 8, 9
    require(active(adjacency, family, u, x), "C-169 forward inactive")
    require(not active(adjacency, family, x, u), "C-169 reverse active")
    counts = audit_orientation(adjacency, family, u, x)
    require(
        common_nonneighbors(adjacency, u, x) == (z,),
        "wrong C-169 W_ux",
    )
    require(
        common_nonneighbors(adjacency, u, d) == (w,),
        "wrong C-169 W_ud",
    )
    require(mask((u, w, z)) in family, "C-167 bridge absent")
    require(adjacency[w] & (1 << z), "hot bridge is not edge branch")
    require(
        common_nonneighbors(adjacency, w, z) == (u,),
        "wrong supported hot fan",
    )
    return {
        "graph6": record,
        "graph6_sha256": hashlib.sha256(record.encode("ascii")).hexdigest(),
        "parameters": [2, 3, 3, 3, 3],
        "greatest_triple_family_size": len(family),
        "orientation": [u, x],
        "W_ux": [z],
        "P": list(common_nonneighbors(adjacency, u, z)),
        "Q": list(common_nonneighbors(adjacency, x, z)),
        "hot_bridge": [u, w, z],
        "hot_bridge_edge_branch": True,
        "W_wz": list(common_nonneighbors(adjacency, w, z)),
        "audit_counts": dict(sorted(counts.items())),
    }


def main() -> None:
    result = {
        "schema": "qq1-supported-asymmetry-bowtie-audit-v1",
        "status": "VERIFIED",
        "model": "one guard moves; attacks only at unoccupied vertices",
        "arbitrary_family_census": census(),
        "equality_control": equality_control(),
        "gamma_two_qq1_boundary": gamma_two_qq1_boundary(),
        "scope": (
            "The theorem supplies a size-independent normal form. "
            "It does not eliminate QQ1, prove complete k=3, or resolve "
            "the gamma-theta conjecture."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

