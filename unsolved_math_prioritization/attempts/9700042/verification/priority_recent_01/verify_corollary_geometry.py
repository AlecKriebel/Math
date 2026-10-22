"""Finite sanity checks for OLD_ESTIMATE_COROLLARY.md; not an asymptotic proof."""
import heapq
import itertools
import json
import random
from pathlib import Path


def edges(n):
    return [(u, (u[0] + dx, u[1] + dy))
            for u in itertools.product(range(n + 1), repeat=2)
            for dx, dy in [(1, 0), (0, 1)]
            if u[0] + dx <= n and u[1] + dy <= n]


def optimal(n, marked):
    end = (n, n)
    distances, previous, queue = {(0, 0): 0}, {}, [(0, (0, 0))]
    while queue:
        distance, u = heapq.heappop(queue)
        if distance != distances[u]:
            continue
        if u == end:
            break
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            v = (u[0] + dx, u[1] + dy)
            if not all(0 <= x <= n for x in v):
                continue
            cost = int((u, v) not in marked) if dx + dy > 0 else 0
            candidate = distance + cost
            if candidate < distances.get(v, 10**9):
                distances[v] = candidate
                previous[v] = u
                heapq.heappush(queue, (candidate, v))
    path = [end]
    while path[-1] != (0, 0):
        path.append(previous[path[-1]])
    return 2 * n - distances[end], path[::-1]


def backwards(path):
    return sum(v[0] + v[1] < u[0] + u[1] for u, v in zip(path, path[1:]))


def chain_score(size, open_sites):
    points = sorted(u for u in open_sites if 0 <= u[0] < size and 0 <= u[1] < size)
    values = {}
    for u in points:
        values[u] = 1 + max((values[v] for v in values
                             if v[0] < u[0] and v[1] < u[1]), default=0)
    return max(values.values(), default=0)


def check(n, marked):
    defect, path = optimal(n, marked)
    assert len(path) == len(set(path))
    open_sites = {u for u, v in marked}
    b = backwards(path)
    k = sum((u, v) in marked for u, v in zip(path, path[1:])
            if v[0] + v[1] > u[0] + u[1])
    assert defect == k - b
    origin_open = int((0, 0) in open_sites)
    listed = [(0, 0)] + [u for u in path[1:-1] if u in open_sites] + [(n + 1, n + 1)]
    p = len(listed) - 2
    chosen = [0]
    while chosen[-1] != len(listed) - 1:
        last = chosen[-1]
        chosen.append(next(i for i in range(last + 1, len(listed))
                           if all(listed[last][j] < listed[i][j] for j in (0, 1))))
    G = H = L = 0
    path_indices = {u: i for i, u in enumerate(path)}
    for gap, (left, right) in enumerate(zip(chosen, chosen[1:])):
        length = right - left - 1
        L += length
        start, end = listed[left], listed[right]
        increments = [(listed[i][0] - listed[i - 1][0], listed[i][1] - listed[i - 1][1])
                      for i in range(left + 1, right)]
        last = listed[right - 1]
        distinguished = next((j for j in (0, 1) if last[j] <= start[j]), 0)
        other = 1 - distinguished
        assert sum(g[distinguished] for g in increments) <= 0
        G += sum(abs(g[distinguished]) for g in increments)
        H += sum(max(0, -g[other]) for g in increments)
        assert last[other] - end[other] <= 2 * (length + 1)
        if gap < len(chosen) - 2:
            segment = path[path_indices[start]:path_indices[end] + 1]
            assert backwards(segment) <= length
    assert p == len(chosen) - 2 + L
    assert k <= p + origin_open
    score_upper = chain_score(n + 1, open_sites)
    score_lower = chain_score(n, open_sites)
    assert score_upper >= len(chosen) - 2 + origin_open
    assert defect - score_upper <= L - b
    assert 2 * b >= G + 2 * H
    assert defect >= score_lower
    return b > 0


def main():
    cases = backtracking_cases = 0
    base_edges = edges(2)
    for mask in range(1 << len(base_edges)):
        marked = {e for i, e in enumerate(base_edges) if (mask >> i) & 1}
        backtracking_cases += check(2, marked)
        cases += 1
    rng = random.Random(8859700042)
    for n in (3, 4, 6):
        extended = [(u, (u[0] + dx, u[1] + dy))
                    for u in itertools.product(range(n + 1), repeat=2)
                    for dx, dy in [(1, 0), (0, 1)]]
        for probability in (.03, .15, .4, .8):
            for _ in range(120):
                marked = {e for e in extended if rng.random() < probability}
                backtracking_cases += check(n, marked)
                cases += 1
    output = {"status": "pass", "cases": cases,
              "cases_with_a_backward_step_in_selected_minimizer": backtracking_cases,
              "exhaustive": "All 4096 edge fields on Q_2, external marks zero",
              "random": "1440 fixed-seed extended fields on Q_3,Q_4,Q_6 at four densities",
              "checks": ["D=k-b", "strict-chain lower comparison", "open-site list reward domination",
                         "nonlast local backward count <= intervening open sites", "BGT Item 4",
                         "b >= G/2+H", "D-S_upper <= L-b"],
              "limitation": "Finite deterministic sanity checks only; not a proof of BGT's analytic estimate or the asymptotic"}
    Path(__file__).with_name("GEOMETRY_CHECKS.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
