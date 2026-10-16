"""Finite falsification checks for the disposition's deterministic corollary.

No external dependencies. Enumerates all square reward environments through N=2,
with both closed/open independent-extension boundary choices, then tests seeded
random environments through N=5. This is a falsification check, not the proof.
"""
import heapq
import itertools
import json
import random
from pathlib import Path


def edges(n):
    return [((x, y), (x + 1, y)) for x in range(n) for y in range(n + 1)] + [
        ((x, y), (x, y + 1)) for x in range(n + 1) for y in range(n)
    ]


def solve(n, reward):
    origin, terminal = (0, 0), (n, n)
    dist, previous = {origin: (0, 0)}, {}
    queue = [(0, 0, origin)]
    while queue:
        cost, length, vertex = heapq.heappop(queue)
        if (cost, length) != dist[vertex]:
            continue
        if vertex == terminal:
            break
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nxt = vertex[0] + dx, vertex[1] + dy
            if not all(0 <= v <= n for v in nxt):
                continue
            step_cost = int((vertex, nxt) not in reward) if dx + dy > 0 else 0
            trial = cost + step_cost, length + 1
            if trial < dist.get(nxt, (10**9, 10**9)):
                dist[nxt] = trial
                previous[nxt] = vertex
                heapq.heappush(queue, (*trial, nxt))
    path = [terminal]
    while path[-1] != origin:
        path.append(previous[path[-1]])
    return dist[terminal][0], path[::-1]


def strict_chain(a, tail_open):
    scores = {}
    for x, y in itertools.product(range(a), repeat=2):
        scores[x, y] = int(tail_open(x, y)) + max(
            [scores[i, j] for i in range(x) for j in range(y)] + [0]
        )
    return max(scores.values(), default=0)


def check(n, reward, extension_open):
    cost, path = solve(n, reward)
    assert len(set(path)) == len(path)
    path_index = {vertex: index for index, vertex in enumerate(path)}

    def tail_open(x, y):
        return any(
            ((x, y), (x + dx, y + dy)) in reward
            if x + dx <= n and y + dy <= n else extension_open
            for dx, dy in [(1, 0), (0, 1)]
        )

    backward = sum(sum(v) < sum(u) for u, v in zip(path, path[1:]))
    collected = sum((u, v) in reward for u, v in zip(path, path[1:]))
    deficit = 2 * n - cost
    assert deficit == collected - backward
    a0 = int(tail_open(0, 0))
    special = [v for v in path[1:-1] if tail_open(*v)]
    b = [(0, 0)] + special + [(n + 1, n + 1)]
    anchors = [0]
    while anchors[-1] != len(b) - 1:
        start = anchors[-1]
        anchors.append(next(i for i in range(start + 1, len(b))
                            if all(x < y for x, y in zip(b[start], b[i]))))
    h = len(anchors) - 1
    total_ell = x_actual = 0
    assert collected <= len(special) + a0
    a_upper = strict_chain(n + 1, tail_open)
    assert a_upper >= h - 1 + a0
    for block, (start, stop) in enumerate(zip(anchors, anchors[1:])):
        ell = stop - start - 1
        total_ell += ell
        chosen = next((j for j in range(2) if b[stop - 1][j] <= b[start][j]), 0)
        if ell:
            assert b[stop - 1][chosen] <= b[start][chosen]
        increments = [tuple(b[i][j] - b[i - 1][j] for j in range(2))
                      for i in range(start + 1, stop)]
        x_actual += sum(abs(g[chosen]) + max(-g[1 - chosen], 0) for g in increments)
        if block < h - 1:
            subpath = path[path_index[b[start]]:path_index[b[stop]] + 1]
            block_b = sum(sum(v) < sum(u) for u, v in zip(subpath, subpath[1:]))
            assert block_b <= ell
            if ell:
                assert b[stop - 1][1 - chosen] - b[stop][1 - chosen] <= ell
        assert 2 * (ell + 1) + b[stop][1 - chosen] - b[stop - 1][1 - chosen] >= 0
    assert len(special) == h - 1 + total_ell
    assert deficit - a_upper <= total_ell - backward
    assert x_actual <= 2 * backward
    assert 2 * (deficit - a_upper) <= 2 * total_ell - x_actual
    assert strict_chain(n, tail_open) <= deficit
    return {"backward": backward, "excess": deficit - a_upper}


def main():
    count = 0
    positive_back = positive_excess = 0
    for n in [1, 2]:
        square_edges = edges(n)
        for mask in range(1 << len(square_edges)):
            reward = {edge for i, edge in enumerate(square_edges) if mask & (1 << i)}
            for extension in [False, True]:
                result = check(n, reward, extension)
                count += 1
                positive_back += result["backward"] > 0
                positive_excess += result["excess"] > 0
    rng = random.Random(9700042)
    random_count = 0
    for n in [3, 4, 5]:
        for _ in range(1000):
            q = rng.choice([0.03, 0.1, 0.3, 0.5, 0.8])
            reward = {edge for edge in edges(n) if rng.random() < q}
            result = check(n, reward, rng.choice([False, True]))
            random_count += 1
            positive_back += result["backward"] > 0
            positive_excess += result["excess"] > 0
    receipt = {
        "status": "PASS", "exhaustive_cases": count,
        "exhaustive_N": [1, 2], "boundary_extensions": ["closed", "open"],
        "random_cases": random_count, "random_N": [3, 4, 5], "seed": 9700042,
        "selected_geodesics_with_backward_steps": positive_back,
        "selected_geodesics_with_positive_chain_excess": positive_excess,
        "claims_checked": ["simple minimizing path", "D=K-B", "K<=p+a0",
                           "A>=h-1+a0", "local B_k<=ell_k", "Lemma19 Item4",
                           "D-A<=L-B", "X_actual<=2B", "2(D-A)<=2L-X_actual",
                           "A(N)<=D"],
        "limitation": "Finite tests falsify bookkeeping errors; they do not prove asymptotics or priority."
    }
    output = Path(__file__).with_name("verification_receipt.json")
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
