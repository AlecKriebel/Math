#!/usr/bin/env python3
"""Independent bounded audit of the rank-one anchor-exit theorem.

No campaign or candidate Python is imported.  Graphs and configurations use
integer bitmasks.  The audit exhausts every labeled graph through order five
over every fixed-anchor ban, plus a deterministic order-six target-ban slice.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parents[1]
CANDIDATE = CAMPAIGN / "math" / "working" / "full_list_rank_one_anchor_exit"
C175 = CAMPAIGN / "math" / "working" / "full_list_rank_rebound_iteration"
C175_REVIEW = CAMPAIGN / "reviews" / "full_list_rank_rebound_iteration_hostile"

PINNED_CANDIDATE = {
    "NOTE.md": "b3aeccda5f44540510559712ee18840560e82646062b1be279afe4f03791d1df",
    "RESEARCH_LOG.md": "3a8594767ec76cca76af3a62fe0b885177b48803f1401ae957069dd4de28092c",
    "verify_strict.sh": "07c7c6f3b9f42e1ff690b6ab02367c5d6dee841f13545515b4f2769f0de101f5",
}

PINNED_C175 = {
    "NOTE.md": "378633621b759c31d1b747b0f1a7bd657f17d8b60da9b8356488640e8fbb8f19",
    "review_manifest": "8c4449ca53a0243830750abdad0fc7e67e2b529de9086b6b454c15487a68f0c0",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def bits(mask: int):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def state(*vertices: int) -> int:
    return sum(1 << vertex for vertex in vertices)


def state_list(mask: int) -> list[int]:
    return list(bits(mask))


def states(n: int, k: int) -> tuple[int, ...]:
    return tuple(state(*chosen) for chosen in itertools.combinations(range(n), k))


def graph_from_code(n: int, code: int) -> tuple[int, ...]:
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if code & (1 << cursor):
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return tuple(adjacency)


def dominates(graph: tuple[int, ...], guards: int) -> bool:
    covered = guards
    for guard in bits(guards):
        covered |= graph[guard]
    return covered == (1 << len(graph)) - 1


def independent(graph: tuple[int, ...], chosen: int) -> bool:
    return all(not (graph[vertex] & chosen) for vertex in bits(chosen))


def successors(
    graph: tuple[int, ...], guards: int, attacked: int
) -> tuple[int, ...]:
    require(not (guards & (1 << attacked)), ("occupied attack", guards, attacked))
    return tuple(
        (guards ^ (1 << guard)) | (1 << attacked)
        for guard in bits(guards)
        if graph[guard] & (1 << attacked)
    )


def greatest_kernel(
    graph: tuple[int, ...], banned: frozenset[int] = frozenset()
) -> tuple[frozenset[int], dict[int, int], tuple[int, ...]]:
    active = {
        guards
        for guards in states(len(graph), 3)
        if guards not in banned and dominates(graph, guards)
    }
    ranks: dict[int, int] = {}
    rounds: list[int] = []
    rank = 0
    while True:
        deleted = set()
        for guards in active:
            for attacked in range(len(graph)):
                if guards & (1 << attacked):
                    continue
                if not any(
                    endpoint in active
                    for endpoint in successors(graph, guards, attacked)
                ):
                    deleted.add(guards)
                    break
        if not deleted:
            return frozenset(active), ranks, tuple(rounds)
        for guards in deleted:
            ranks[guards] = rank
        rounds.append(len(deleted))
        active.difference_update(deleted)
        rank += 1


def deletion_witnesses(
    graph: tuple[int, ...],
    guards: int,
    banned: frozenset[int],
    kernel: frozenset[int],
    ranks: dict[int, int],
) -> tuple[int, ...]:
    rank = ranks[guards]
    result = []
    for attacked in range(len(graph)):
        if guards & (1 << attacked):
            continue
        legal_initial = [
            endpoint
            for endpoint in successors(graph, guards, attacked)
            if endpoint not in banned and dominates(graph, endpoint)
        ]
        if all(
            endpoint not in kernel
            and endpoint in ranks
            and ranks[endpoint] < rank
            for endpoint in legal_initial
        ):
            result.append(attacked)
    return tuple(result)


def distance_to_ban(guards: int, banned: frozenset[int]) -> int:
    return min(3 - (guards & target).bit_count() for target in banned)


def has_retained_unbanned_response(
    graph: tuple[int, ...],
    guards: int,
    attacked: int,
    greatest: frozenset[int],
    banned: frozenset[int],
) -> bool:
    if guards & (1 << attacked):
        return False
    return any(
        endpoint in greatest and endpoint not in banned
        for endpoint in successors(graph, guards, attacked)
    )


def complement_neighbors(graph: tuple[int, ...], vertex: int) -> int:
    return ((1 << len(graph)) - 1) ^ (1 << vertex) ^ graph[vertex]


def anchored_ban(v: int, t: int, region: int) -> frozenset[int]:
    anchors = (1 << v) | (1 << t)
    return frozenset(anchors | (1 << b) for b in bits(region))


class Counters:
    def __init__(self) -> None:
        self.data: dict[str, int] = {}

    def add(self, key: str, amount: int = 1) -> None:
        self.data[key] = self.data.get(key, 0) + amount


def audit_ban_instance(
    graph: tuple[int, ...],
    greatest: frozenset[int],
    v: int,
    t: int,
    region: int,
    count: Counters,
    target: int | None = None,
) -> None:
    banned = anchored_ban(v, t, region)
    kernel, ranks, _ = greatest_kernel(graph, banned)
    anchor_mask = (1 << v) | (1 << t)
    count.add("ban_instances")

    # Lemmas 2.1 and 2.2 reduce to the same one-anchor survival fact.
    for retained in greatest:
        if retained & (1 << v) and not retained & (1 << t):
            if has_retained_unbanned_response(
                graph, retained, t, greatest, banned
            ):
                count.add("v_only_escape_barriers")
                require(
                    ranks.get(retained) != 0,
                    ("v-only barrier deleted at zero", graph, v, t, retained),
                )
        if retained & (1 << t) and not retained & (1 << v):
            if has_retained_unbanned_response(
                graph, retained, v, greatest, banned
            ):
                count.add("t_only_escape_barriers")
                require(
                    ranks.get(retained) != 0,
                    ("t-only barrier deleted at zero", graph, v, t, retained),
                )

    for retained in greatest:
        if retained & anchor_mask:
            continue
        if ranks.get(retained) != 1:
            continue
        if distance_to_ban(retained, banned) != 2:
            continue
        count.add("rank_one_distance_two_states")
        witnesses = deletion_witnesses(graph, retained, banned, kernel, ranks)
        for attacked in witnesses:
            count.add("rank_one_deletion_witnesses")
            require(
                attacked in (v, t),
                ("C175 nonanchor witness", graph, v, t, retained, attacked),
            )
            if attacked == v:
                count.add("raw_v_anchor_witnesses")
            else:
                count.add("raw_t_anchor_witnesses")

            retained_endpoints = [
                endpoint
                for endpoint in successors(graph, retained, attacked)
                if endpoint in greatest
            ]
            require(retained_endpoints, "unrestricted closure")
            for endpoint in retained_endpoints:
                count.add("retained_tight_shell_responses")
                require(
                    ranks.get(endpoint) == 0
                    and distance_to_ban(endpoint, banned) == 1,
                    (
                        "C175 tight response",
                        graph,
                        v,
                        t,
                        retained,
                        attacked,
                        endpoint,
                    ),
                )
                other_anchor = t if attacked == v else v
                if has_retained_unbanned_response(
                    graph, endpoint, other_anchor, greatest, banned
                ):
                    count.add("retained_responses_with_escape_barrier")
                    raise AssertionError(
                        (
                            "rank-zero response has escape barrier",
                            graph,
                            v,
                            t,
                            retained,
                            attacked,
                            endpoint,
                        )
                    )

            # Physical endpoints with a barrier are exactly the kind which
            # Lemma 2.2 proves must be omitted from the greatest family.
            for endpoint in successors(graph, retained, attacked):
                if endpoint in greatest:
                    continue
                other_anchor = t if attacked == v else v
                if not (endpoint & (1 << attacked)):
                    continue
                if endpoint & (1 << other_anchor):
                    continue
                if any(
                    response in greatest and response not in banned
                    for response in successors(
                        graph, endpoint, other_anchor
                    )
                ):
                    count.add("omitted_physical_endpoints_with_escape_return")

        if target is not None:
            audit_local_rows(
                graph,
                greatest,
                banned,
                kernel,
                ranks,
                target,
                v,
                t,
                region,
                retained,
                count,
            )

    # This is the rank-zero next-attack argument, independent of fan labels.
    for retained in greatest:
        if not retained & (1 << t) or retained & (1 << v):
            continue
        if ranks.get(retained) != 0:
            continue
        count.add("rank_zero_t_only_states")
        witnesses = deletion_witnesses(graph, retained, banned, kernel, ranks)
        require(witnesses, "rank-zero state has no witness")
        for attacked in witnesses:
            count.add("rank_zero_t_only_witnesses")
            require(
                attacked == v,
                ("rank-zero next attack not v", graph, v, t, retained, attacked),
            )


def audit_local_rows(
    graph: tuple[int, ...],
    greatest: frozenset[int],
    banned: frozenset[int],
    kernel: frozenset[int],
    ranks: dict[int, int],
    x: int,
    v: int,
    t: int,
    region: int,
    guards: int,
    count: Counters,
) -> None:
    # Look for the exact six-role fragment used by Theorem 3.1:
    # K={r,y,e}, J={v,r,y}, Y={v,t,y}, E={v,t,r}.
    for r, y, e in itertools.permutations(bits(guards), 3):
        if not region & (1 << r) or region & (1 << y):
            continue
        if x in (r, y, e):
            continue
        required_edges = ((v, e), (v, r), (t, r), (t, y))
        required_nonedges = ((v, y), (r, y), (r, e), (y, e))
        if not all(graph[a] & (1 << b) for a, b in required_edges):
            continue
        if not all(not (graph[a] & (1 << b)) for a, b in required_nonedges):
            continue
        J = state(v, r, y)
        Y = state(v, t, y)
        E = state(v, t, r)
        if not all(endpoint in greatest for endpoint in (J, Y, E)):
            continue
        count.add("exact_local_role_rows")

        witnesses = deletion_witnesses(graph, guards, banned, kernel, ranks)
        require(witnesses == (t,), ("local K witnesses", witnesses))

        D = state(r, t, e)
        A = state(t, y, e)
        C = state(r, y, t)
        retained_at_t = {
            endpoint
            for endpoint in successors(graph, guards, t)
            if endpoint in greatest
        }
        require(retained_at_t == {D}, ("local retained t responses", retained_at_t))
        require(A not in greatest and C not in greatest, "barrier endpoints retained")
        require(ranks.get(D) == 0, ("local D rank", ranks.get(D)))
        require(
            deletion_witnesses(graph, D, banned, kernel, ranks) == (v,),
            "local D witness",
        )

        R = state(v, t, e)
        physical_at_v = set(successors(graph, D, v))
        require(physical_at_v == {E, R}, ("local alternate table", physical_at_v))
        require(E in greatest and E in banned, "selected banned endpoint")
        if region & (1 << e):
            require(R in banned, "e in B alternate not banned")
            count.add("exact_local_banned_alternates")
        else:
            require(R not in banned and not dominates(graph, R), "alternate dominates")
            count.add("exact_local_nondominating_alternates")


def run_audit() -> dict[str, object]:
    count = Counters()
    count.data["graphs_considered"] = 0
    count.data["graphs_with_eternal_triples"] = 0

    # Complete labeled census through order five, with every nonempty region.
    for n in range(3, 6):
        for code in range(1 << (n * (n - 1) // 2)):
            graph = graph_from_code(n, code)
            count.add("graphs_considered")
            greatest, _, _ = greatest_kernel(graph)
            if not greatest:
                continue
            count.add("graphs_with_eternal_triples")
            for v in range(n):
                for t in range(n):
                    if t == v:
                        continue
                    available = [z for z in range(n) if z not in (v, t)]
                    for selector in range(1, 1 << len(available)):
                        region = sum(
                            1 << available[index]
                            for index in range(len(available))
                            if selector & (1 << index)
                        )
                        audit_ban_instance(
                            graph, greatest, v, t, region, count
                        )

    # Deterministic target-derived order-six slice.  This adds genuinely
    # nonanchor unoccupied attacks while retaining a bounded laptop audit.
    for code in range(7, 1 << 15, 16):
        graph = graph_from_code(6, code)
        count.add("graphs_considered")
        greatest, _, _ = greatest_kernel(graph)
        if not greatest:
            continue
        count.add("graphs_with_eternal_triples")
        for x in range(6):
            region = complement_neighbors(graph, x)
            if not region:
                continue
            neighbors = list(bits(graph[x]))
            for v in neighbors:
                for t in neighbors:
                    if t == v or graph[v] & (1 << t):
                        continue
                    audit_ban_instance(
                        graph, greatest, v, t, region, count, target=x
                    )

    count.data.setdefault("retained_responses_with_escape_barrier", 0)
    count.data.setdefault("exact_local_role_rows", 0)
    count.data.setdefault("exact_local_banned_alternates", 0)
    count.data.setdefault("exact_local_nondominating_alternates", 0)
    return {
        "scope": {
            "complete_labeled_graphs": "orders 3 through 5",
            "order6_target_slice": "graph code == 7 (mod 16)",
            "model": (
                "unoccupied attacks; one occupied guard moves along one edge; "
                "successor retained in literal greatest eternal triple-family"
            ),
        },
        "counts": count.data,
    }


def main() -> None:
    for relative, expected in PINNED_CANDIDATE.items():
        actual = hashlib.sha256((CANDIDATE / relative).read_bytes()).hexdigest()
        require(actual == expected, ("candidate hash", relative, actual))
    require(
        hashlib.sha256((C175 / "NOTE.md").read_bytes()).hexdigest()
        == PINNED_C175["NOTE.md"],
        "C175 source hash",
    )
    require(
        hashlib.sha256((C175_REVIEW / "MANIFEST.json").read_bytes()).hexdigest()
        == PINNED_C175["review_manifest"],
        "C175 review hash",
    )

    result = {
        "schema": "full-list-rank-one-anchor-exit-hostile-clean-v1",
        "candidate_commit": "ffb16daa",
        "candidate_hashes": PINNED_CANDIDATE,
        "dependency": {
            "claim": "C-175",
            "source_sha256": PINNED_C175["NOTE.md"],
            "review_manifest_sha256": PINNED_C175["review_manifest"],
        },
        "bounded_audit": run_audit(),
        "verdict": "PASS",
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
