"""Independent deterministic checks; standard-library only; no original checker imports.

Run using python3 -I -S -B independent_finite_checks.py, optionally with -O.
All mathematical checks use require(), so optimization cannot erase them.
The tests are finite validation, never an inference of the limiting theorem.
"""
import heapq
import itertools
import json
import math


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def model(n):
    N = n - 2
    vertices = [(x, y) for x in range(n) for y in range(n)]
    edges = [(v, (v[0] + dx, v[1] + dy)) for v in vertices
             for dx, dy in [(1, 0), (0, 1)]
             if v[0] + dx < n and v[1] + dy < n]
    sources = {v for v in vertices if (v[0] == 0 or v[1] == 0)
               and v not in {(0, n - 1), (n - 1, 0)}}
    sinks = {v for v in vertices if v[0] == n - 1 or v[1] == n - 1}
    optional = sorted(set(vertices) - sources - sinks)
    dual = [(x, y) for x in range(N + 1) for y in range(N + 1)]
    # Each record is (forward dual tail, head, positively oriented primal edge).
    records = []
    for x, y in dual:
        if x < N:
            records.append(((x, y), (x + 1, y),
                            ((x + 1, N - y), (x + 1, N - y + 1))))
        if y < N:
            records.append(((x, y), (x, y + 1),
                            ((x, N - y), (x + 1, N - y))))
    forced = [((0, n - 2), (0, n - 1)), ((n - 2, 0), (n - 1, 0))]
    essential = [r[2] for r in records] + forced
    require(len(set(essential)) == len(essential), (n, "duplicate crossing"))
    require(set(essential) <= set(edges), (n, "invalid primal edge"))
    return N, vertices, edges, sources, sinks, optional, dual, records, forced, essential


def all_cuts(sources, optional):
    for mask in range(1 << len(optional)):
        yield sources | {v for j, v in enumerate(optional) if mask >> j & 1}


def arbitrary_cut_interfaces(n):
    N, vertices, edges, sources, sinks, optional, dual, records, forced, essential = model(n)
    cut_count = junction_cuts = junction_faces = 0
    for A in all_cuts(sources, optional):
        cut_count += 1
        crossing = {e for e in edges if (e[0] in A) != (e[1] in A)}
        require(set(forced) <= crossing, (n, "forced crossing absent"))
        require(crossing <= set(essential), (n, "unexpected boundary crossing"))
        adjacency = {v: [] for v in dual}
        balance = {v: 0 for v in dual}
        degree = {v: 0 for v in dual}
        for u, v, (a, b) in records:
            if (a in A) == (b in A):
                continue
            start, end = (u, v) if a in A else (v, u)
            adjacency[start].append(end)
            balance[start] += 1
            balance[end] -= 1
            degree[u] += 1
            degree[v] += 1
        # The exterior stubs complete even interface degree at the two corners.
        degree[(0, 0)] += 1
        degree[(N, N)] += 1
        for v in dual:
            target = int(v == (0, 0)) - int(v == (N, N))
            require(balance[v] == target, (n, "unbalanced interface", v, balance[v]))
            require(degree[v] in {0, 2, 4}, (n, "odd face degree", v))
        js = sum(d == 4 for d in degree.values())
        junction_faces += js
        junction_cuts += int(js > 0)
        reachable = {(0, 0)}
        stack = [(0, 0)]
        while stack:
            for v in adjacency[stack.pop()]:
                if v not in reachable:
                    reachable.add(v)
                    stack.append(v)
        require((N, N) in reachable, (n, "no directed interface path"))
    return {"n": n, "cuts": cut_count, "cuts_with_four_valent_faces": junction_cuts,
            "four_valent_face_occurrences": junction_faces}


def capacity_exhaustion(n):
    N, vertices, edges, sources, sinks, optional, dual, records, forced, essential = model(n)
    cut_masks = []
    for A in all_cuts(sources, optional):
        cut_masks.append(sum(1 << j for j, e in enumerate(essential)
                             if e[0] in A and e[1] not in A))
    graph = {v: [] for v in dual}
    for j, (u, v, _) in enumerate(records):
        graph[u].append((v, j, True))
        graph[v].append((u, j, False))
    values = {}
    for open_mask in range(1 << len(essential)):
        primal_cut = min((mask & open_mask).bit_count() for mask in cut_masks)
        dist = {(0, 0): 0}
        queue = [(0, (0, 0))]
        while queue:
            cost, u = heapq.heappop(queue)
            if cost != dist[u]:
                continue
            if u == (N, N):
                break
            for v, j, forward in graph[u]:
                new_cost = cost + int(forward and bool(open_mask >> j & 1))
                if new_cost < dist.get(v, math.inf):
                    dist[v] = new_cost
                    heapq.heappush(queue, (new_cost, v))
        boundary = sum(open_mask >> (len(records) + j) & 1 for j in range(2))
        require(primal_cut == boundary + dist[(N, N)],
                (n, "primal/dual mismatch", open_mask, primal_cut, boundary, dist))
        D = 2 * N - dist[(N, N)]
        require(0 <= D <= 2 * N, (n, "deficit range"))
        require((2 * n - 2) - primal_cut == 2 - boundary + D,
                (n, "normalization mismatch"))
        values[primal_cut] = values.get(primal_cut, 0) + 1
    return {"n": n, "essential_edges": len(essential), "capacity_patterns": 1 << len(essential),
            "irrelevant_boundary_edges": len(edges) - len(essential),
            "mincut_histogram": values}


def simple_path_cut_completion(N):
    n = N + 2
    _, vertices, edges, sources, sinks, optional, dual, records, forced, essential = model(n)
    graph = {v: [] for v in dual}
    for u, v, primal in records:
        graph[u].append((v, primal, True))
        graph[v].append((u, primal, False))
    paths = backward_paths = 0

    def check_path(path):
        nonlocal paths, backward_paths
        paths += 1
        backward_paths += int(any(not step[2] for step in path))
        removed = set(forced) | {step[1] for step in path}
        undirected = {v: [] for v in vertices}
        for a, b in edges:
            if (a, b) not in removed:
                undirected[a].append(b)
                undirected[b].append(a)
        A = set(sources)
        stack = list(sources)
        while stack:
            for v in undirected[stack.pop()]:
                if v not in A:
                    A.add(v)
                    stack.append(v)
        require(not (A & sinks), (N, "dual path fails source/sink separation", path))
        outgoing = {e for e in edges if e[0] in A and e[1] not in A}
        incoming = {e for e in edges if e[0] not in A and e[1] in A}
        expected_out = set(forced) | {e for _, e, forward in path if forward}
        expected_in = {e for _, e, forward in path if not forward}
        require(outgoing == expected_out, (N, "outward crossing mismatch", path))
        require(incoming == expected_in, (N, "inward crossing mismatch", path))
        f = sum(forward for _, _, forward in path)
        b = len(path) - f
        require(f - b == 2 * N, (N, "net variation mismatch"))

    def visit(u, visited, path):
        if u == (N, N):
            check_path(path)
            return
        for v, primal, forward in graph[u]:
            if v not in visited:
                visit(v, visited | {v}, path + [(v, primal, forward)])

    visit((0, 0), {(0, 0)}, [])
    return {"N": N, "simple_corner_paths": paths, "paths_with_backward_steps": backward_paths}


def coordinate_list_counts():
    cases = lists = 0
    minimum_slack = None
    for N in range(5):
        for k in range(1, 6):
            cases += 1
            exact = 0
            for middle in itertools.product(range(N + 1), repeat=k):
                xs = (0,) + middle + (N,)
                variation = sum(max(a - b, 0) for a, b in zip(xs, xs[1:]))
                exact += int(variation <= k)
                # Every deletion must weakly reduce negative variation.
                for j in range(1, len(xs) - 1):
                    shortened = xs[:j] + xs[j + 1:]
                    reduced = sum(max(a - b, 0) for a, b in zip(shortened, shortened[1:]))
                    require(reduced <= variation, "negative variation increased on deletion")
            bound = sum(math.comb(k + 1, t) * math.comb(k, t)
                        * math.comb(N + 2 * k - t, k - t) for t in range(k + 1))
            require(exact <= bound, (N, k, exact, bound))
            ratio_bound = math.comb(N + 2 * k, k) * (1 + math.sqrt(k / (N + 2 * k))) ** (2 * k + 1)
            require(bound <= ratio_bound + 1e-7 * max(1, ratio_bound),
                    (N, k, "binomial simplification failed"))
            lists += (N + 1) ** k
            slack = bound - exact
            minimum_slack = slack if minimum_slack is None else min(slack, minimum_slack)
    return {"parameter_pairs": cases, "coordinate_lists": lists, "minimum_integer_slack": minimum_slack}


def main():
    result = {
        "scope": "independent finite geometry and counting checks; not an asymptotic proof",
        "all_cut_interfaces": [arbitrary_cut_interfaces(n) for n in range(2, 7)],
        "all_essential_capacity_configurations": [capacity_exhaustion(n) for n in range(2, 5)],
        "all_simple_dual_path_completions": [simple_path_cut_completion(N) for N in range(5)],
        "coordinate_list_counts": coordinate_list_counts(),
        "check_failures": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
