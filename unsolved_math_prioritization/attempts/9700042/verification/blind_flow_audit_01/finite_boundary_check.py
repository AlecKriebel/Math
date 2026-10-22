"""Independent diagnostic only: exhaustive directed cuts versus face-dual distances.

Uses standard library only. Does not import or mirror candidate verification code.
The tested identity is not taken as an asymptotic proof. Run with python3 -I -S -B.
"""

import heapq
import itertools
import json
import random


def primal_edges(n):
    return [((x, y), (x + dx, y + dy))
            for x in range(n) for y in range(n)
            for dx, dy in ((1, 0), (0, 1))
            if x + dx < n and y + dy < n]


def minimum_cut(n, capacity):
    sources = {(0, y) for y in range(n - 1)} | {(x, 0) for x in range(n - 1)}
    sinks = {(x, n - 1) for x in range(n)} | {(n - 1, y) for y in range(n)}
    assert not sources.intersection(sinks)
    free = [(x, y) for x in range(1, n - 1) for y in range(1, n - 1)]
    best = sum(capacity.values())
    for bits in itertools.product((0, 1), repeat=len(free)):
        side = sources | {v for v, bit in zip(free, bits) if bit}
        val = sum(c for (u, v), c in capacity.items() if u in side and v not in side)
        best = min(best, val)
    return best


def dual_distance(n, capacity):
    # Face (i,j) has southwest primal corner (i,n-2-j).
    last = n - 2
    distances = {(0, 0): 0}
    pending = [(0, (0, 0))]
    while pending:
        dist, (i, j) = heapq.heappop(pending)
        if dist != distances[(i, j)]:
            continue
        if (i, j) == (last, last):
            return dist
        for di, dj in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            ni, nj = i + di, j + dj
            if not (0 <= ni <= last and 0 <= nj <= last):
                continue
            if di == 1:
                edge = ((i + 1, last - j), (i + 1, last - j + 1))
                cost = capacity[edge]
            elif dj == 1:
                edge = ((i, last - j), (i + 1, last - j))
                cost = capacity[edge]
            else:
                cost = 0
            nd = dist + cost
            if nd < distances.get((ni, nj), 10 ** 9):
                distances[(ni, nj)] = nd
                heapq.heappush(pending, (nd, (ni, nj)))
    raise AssertionError("dual corners disconnected")


def verify(n, bits):
    edges = primal_edges(n)
    capacity = dict(zip(edges, bits))
    value = minimum_cut(n, capacity)
    forced = capacity[((0, n - 2), (0, n - 1))] + capacity[((n - 2, 0), (n - 1, 0))]
    dual = dual_distance(n, capacity)
    assert value == forced + dual, (n, bits, value, forced, dual)
    return value


def main():
    counts = {}
    for n in (2, 3):
        count = 0
        for bits in itertools.product((0, 1), repeat=len(primal_edges(n))):
            verify(n, bits)
            count += 1
        counts[str(n)] = {"type": "all capacity configurations", "count": count}
    rng = random.Random(9700042)
    for n, samples in ((4, 300), (5, 100)):
        for _ in range(samples):
            verify(n, [rng.randrange(2) for _ in primal_edges(n)])
        counts[str(n)] = {"type": "deterministic random sample", "count": samples}
    extremes = {}
    for n in range(2, 7):
        edges = primal_edges(n)
        extremes[str(n)] = {"all_open": verify(n, [1] * len(edges)),
                            "all_closed": verify(n, [0] * len(edges))}
        assert extremes[str(n)] == {"all_open": 2 * (n - 1), "all_closed": 0}
    # A direct source-heuristic trap. For n=2, close only the top horizontal edge.
    # V remains 2. Covering that closed edge needs exactly one source-sink path.
    n = 2
    edges = primal_edges(n)
    top = ((0, 1), (1, 1))
    bits = [int(edge != top) for edge in edges]
    assert verify(n, bits) == 2
    result = {"status": "PASS", "seed": 9700042, "dual_identity_checks": counts,
              "extreme_configurations": extremes,
              "literal_source_U_identity_counterexample": {
                  "n": 2, "closed_edges": [[[0, 1], [1, 1]]],
                  "V": 2, "all_open_baseline_minus_V": 0, "minimum_closed_edge_cover_U": 1,
                  "scope": "Rejects exact literal U-complement identity; does not refute C1/C4, which use direct cut duality."},
              "limitation": "Finite diagnostics do not certify planar duality for all n or any dilute asymptotic."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
