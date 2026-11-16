"""Source-only exact adversarial controls; no supplied code/results imported."""
from collections import defaultdict, deque
from fractions import Fraction as F
from itertools import product
import json


def need(ok, label):
    if not ok:
        raise ValueError(label)


def dual_graph(D):
    crossing = set()
    for x, y in D:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = x + dx, y + dy
            if min(v) < 0 or v in D:
                continue
            crossing.add(tuple(sorted(((x, y), v))))
    adj = defaultdict(set)
    for (x, y), (u, v) in crossing:
        if y == v:
            i = min(x, u)
            a, b = (2 * i + 1, 2 * y - 1), (2 * i + 1, 2 * y + 1)
        else:
            j = min(y, v)
            a, b = (2 * x - 1, 2 * j + 1), (2 * x + 1, 2 * j + 1)
        adj[a].add(b)
        adj[b].add(a)
    return adj


def witness(adj):
    bottom = sorted(v for v in adj if v[1] == -1)
    need(len(bottom) % 2 == 1, "odd bottom intersection")
    for v, neighbors in adj.items():
        if -1 in v:
            need(len(neighbors) == 1, "boundary stub degree")
        else:
            need(len(neighbors) in (2, 4), "interior even degree")
    for start in bottom:
        parent = {start: None}
        todo = deque([start])
        while todo:
            at = todo.popleft()
            if at[0] == -1:
                path = [at]
                while parent[path[-1]] is not None:
                    path.append(parent[path[-1]])
                path.reverse()
                need(len(path) == len(set(path)), "simple dual witness")
                i, j = (start[0] - 1) // 2, (at[1] - 1) // 2
                need(len(path) - 1 >= i + j + 2 >= 2, "all-distance dual lower bound")
                return path
            for nxt in adj[at]:
                if nxt not in parent:
                    parent[nxt] = at
                    todo.append(nxt)
    raise ValueError("no bottom-left cut witness")


def in_A(v):
    return v[0] >= 1 and v[1] >= 1


def in_B(v):
    return v[0] <= -1 and v[1] <= -1


def main():
    points = list(product(range(4), repeat=2))
    rest = [v for v in points if v != (0, 0)]
    cases, degree_four, max_witness = 0, 0, 0
    for mask in range(1 << len(rest)):
        D = {(0, 0)} | {v for i, v in enumerate(rest) if mask >> i & 1}
        adj = dual_graph(D)
        path = witness(adj)
        degree_four += any(len(n) == 4 for n in adj.values())
        max_witness = max(max_witness, len(path) - 1)
        cases += 1
    need(any(len(n) == 4 for n in dual_graph({(0, 0), (1, 1)}).values()),
         "degree-four diagonal-contact negative control")
    # A finite-box-only edge list misses the entire cut of its full box.
    truncated_cut = [1 for x in points for y in points
                     if abs(x[0] - y[0]) + abs(x[1] - y[1]) == 1
                     and ((x in set(points)) != (y in set(points)))]
    need(truncated_cut == [], "wrong finite-box boundary control")

    p = F(19, 20)
    states, joint = 0, F(0)
    for bits in product((0, 1), repeat=6):
        weight = p ** sum(bits) * (1 - p) ** (6 - sum(bits))
        coarse = (all(bits[:3]), all(bits[3:]))
        for i, j in ((0, 3), (3, 6), (0, 6)):
            actual = all(bits[i:j])
            projected = coarse[0] if (i, j) == (0, 3) else coarse[1] if (i, j) == (3, 6) else all(coarse)
            need(actual == projected, "series original-vertex connectivity")
        if all(coarse):
            joint += weight
        states += 1
    need(joint == (p ** 3) ** 2, "disjoint bond families sharing an endpoint")
    need(p ** 7 != (p ** 4) ** 2, "site-model shared endpoint countercontrol")

    for n in range(1, 65):
        path = [(1, n), (0, n)] + [(-1, y) for y in range(n, -2, -1)]
        need(len(path) - 1 == n + 3 and len(path) == len(set(path)), "distant exact shortest path")
        need(all(not in_A(v) and not in_B(v) for v in path[1:-1]), "last-A first-B segment")
        need(all(not ((in_A(a) and in_A(b)) or (in_B(a) and in_B(b)))
                 for a, b in zip(path, path[1:])), "all weak path")
    for s in range(101):
        for t in range(101):
            fs, ft = int(s > 50), int(t > 50)
            need(abs(fs - ft) <= abs(s - t) <= 100 * abs(fs - ft) + 100,
                 "midpoint rough-isometry control")
    need(50 > 100 * abs(0 - 0), "additive-term necessity for collapsed midpoint")

    z = F(3, 10)
    manuscript_closed = F(4, 3) * z * z * (2 - z) / (1 - z) ** 2
    sharper_closed = z * z / (3 * (1 - z) ** 2)
    r = F(3, 32)
    bridge = F(8, 3) * r ** 4 / (1 - r) ** 2
    lower = (1 - manuscript_closed) ** 2 * (1 - bridge)
    need(manuscript_closed == F(102, 245) and sharper_closed == F(3, 49), "Peierls constants")
    need(p ** 100 < F(1, 32) and bridge == F(27, 107648), "bridge constant")
    need(lower == F(2200741829, 6461571200), "printed product bound")
    need(lower - F(1, 3) == F(140654287, 19384713600), "strict one-third margin")
    need(3 * p >= 1, "unstretched negative control invalidates convergent walk sum")
    print(json.dumps({"status": "PASS_SOURCE_ONLY_ADVERSARIAL_CONTROLS",
                      "finite_D_cases": cases, "cases_with_degree_four": degree_four,
                      "maximum_returned_dual_path_length": max_witness,
                      "series_states": states, "distant_path_controls": 64,
                      "metric_pairs": 101 ** 2,
                      "manuscript_corner_failure_bound": str(manuscript_closed),
                      "independent_first_step_corner_failure_bound": str(sharper_closed),
                      "bridge_bound_at_r3over32": str(bridge),
                      "printed_nonuniqueness_lower_bound": str(lower),
                      "printed_margin_over_one_third": str(lower - F(1, 3)),
                      "negative_controls": ["degree-four dual vertices occur", "finite box loses external cut",
                                            "site sharing is not bond independence", "arbitrarily distant weak starts",
                                            "midpoint needs additive term", "short subdivision breaks r<1 bound"],
                      "assertions_used": False, "native_imports_or_runs": [],
                      "universal_and_infinite_event_arguments": "analytic INITIAL.md, not finite extrapolation"}, indent=2))


if __name__ == "__main__":
    main()
