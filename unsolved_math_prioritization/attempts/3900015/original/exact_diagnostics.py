#!/usr/bin/env python3
"""Small exact model diagnostics; no claim to solve the infinite problem."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import isqrt, lcm
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


def separated(a, b):
    x, y, w, h = a
    u, v, s, t = b
    return x + w <= u or u + s <= x or y + h <= v or v + t <= y


def check_packing(rects):
    for x, y, w, h in rects:
        require(w > 0 and h > 0, "positive dimensions required")
        require(0 <= x and 0 <= y and x + w <= 1 and y + h <= 1,
                "containment failed")
    for a, b in combinations(rects, 2):
        require(separated(a, b), "interior overlap")


def compact_to_grid(rects, denominator):
    """Freeze one satisfied separator per pair and use longest paths."""
    check_packing(rects)
    n = len(rects)
    edges = [[], []]
    for i, j in combinations(range(n), 2):
        x, y, w, h = rects[i]
        u, v, s, t = rects[j]
        if x + w <= u:
            edges[0].append((i, j, w))
        elif u + s <= x:
            edges[0].append((j, i, s))
        elif y + h <= v:
            edges[1].append((i, j, h))
        else:
            require(v + t <= y, "no valid separator")
            edges[1].append((j, i, t))

    def longest_paths(es):
        indegrees = [0] * n
        outgoing = [[] for _ in range(n)]
        for i, j, w in es:
            require(w > 0, "positive edge required")
            outgoing[i].append((j, w))
            indegrees[j] += 1
        stack = [i for i in range(n) if indegrees[i] == 0]
        values = [F(0)] * n
        count = 0
        while stack:
            i = stack.pop()
            count += 1
            for j, w in outgoing[i]:
                values[j] = max(values[j], values[i] + w)
                indegrees[j] -= 1
                if indegrees[j] == 0:
                    stack.append(j)
        require(count == n, "separator graph is cyclic")
        return values

    xs, ys = [longest_paths(es) for es in edges]
    result = [(xs[i], ys[i], r[2], r[3]) for i, r in enumerate(rects)]
    check_packing(result)
    for old, new in zip(rects, result):
        require(new[0] <= old[0] and new[1] <= old[1], "compaction increased coordinate")
        require((new[0] * denominator).denominator == 1, "x grid failed")
        require((new[1] * denominator).denominator == 1, "y grid failed")
    return result


def exhaustive_grid_pack(dimensions, denominator):
    """Enumerate ALL integer lower-left positions and both orientations."""
    D = denominator
    options = []
    for a, b in dimensions:
        aa, bb = F(a) * D, F(b) * D
        require(aa.denominator == bb.denominator == 1, "off-grid dimensions")
        placements = []
        for w, h in sorted({(int(aa), int(bb)), (int(bb), int(aa))}):
            for y in range(D - h + 1):
                for x in range(D - w + 1):
                    row = ((1 << w) - 1) << x
                    mask = sum(row << (D * (y + j)) for j in range(h))
                    placements.append((mask, (x, y, w, h)))
        options.append(placements)
    # Fixed deterministic order; no geometric symmetry assumption.
    order = sorted(range(len(dimensions)), key=lambda i: (len(options[i]), i))
    states = 0
    trials = 0

    @lru_cache(None)
    def visit(depth, occupied):
        nonlocal states, trials
        states += 1
        if depth == len(order):
            return ()
        index = order[depth]
        for mask, placement in options[index]:
            trials += 1
            if occupied & mask:
                continue
            answer = visit(depth + 1, occupied | mask)
            if answer is not None:
                return ((index, placement),) + answer
        return None

    witness = visit(0, 0)
    return {
        "denominator": D,
        "feasible": witness is not None,
        "placement_counts": [len(p) for p in options],
        "piece_order": order,
        "states": states,
        "candidate_trials": trials,
        "witness_grid": None if witness is None else sorted(witness),
    }


def diagnostics():
    partial = F(0)
    for n in range(1, 201):
        partial += F(1, n * (n + 1))
        require(partial == 1 - F(1, n + 1), "telescoping identity")

    # Boundary contact is allowed; tiny positive overlap cannot be rounded away.
    first = (F(0), F(0), F(1, 2), F(1, 2))
    contact = (F(1, 2), F(0), F(1, 2), F(1, 2))
    epsilon = F(1, 10**30)
    overlapping = (F(1, 2) - epsilon, F(0), F(1, 2), F(1, 2))
    check_packing([first, contact])
    overlap_rejected = False
    try:
        check_packing([first, overlapping])
    except ValueError:
        overlap_rejected = True
    require(overlap_rejected, "tiny positive overlap accepted")

    prefix = [(F(0), F(0), F(1), F(1, 2)),
              (F(0), F(1, 2), F(1, 2), F(1, 3)),
              (F(1, 2), F(1, 2), F(1, 3), F(1, 4))]
    check_packing(prefix)
    # A feasible non-grid translation exercises the rationalization operation.
    shifted = [prefix[0],
               (F(1, 100), F(1, 2) + F(1, 100), F(1, 2), F(1, 3)),
               (F(1, 2) + F(1, 100), F(1, 2) + F(1, 100), F(1, 3), F(1, 4))]
    D = lcm(1, 2, 3, 4)
    require(any((r[0] * D).denominator != 1 for r in shifted), "test was already on grid")
    grid = compact_to_grid(shifted, D)

    dims = [(F(1), F(1, 2)), (F(1, 2), F(1, 3)), (F(1, 3), F(1, 4))]
    prefix_search = exhaustive_grid_pack(dims, D)
    require(prefix_search["feasible"], "three-rectangle prefix should fit")
    hole_search = exhaustive_grid_pack(dims + [(F(1, 2), F(1, 2))], D)
    require(not hole_search["feasible"], "m=4 square-hole obstruction failed")
    # Exact masks represent interiors of unit grid cells, allowing edge contact.
    for index, placement in prefix_search["witness_grid"]:
        x, y, w, h = placement
        require(sorted([F(w, D), F(h, D)]) == sorted(dims[index]), "wrong rectangle size")
    witness_rects = [tuple(F(v, D) for v in p) for _, p in prefix_search["witness_grid"]]
    check_packing(witness_rects)

    squares = [m for m in range(1, 101) if isqrt(m)**2 == m]
    threshold = 10**1000
    require(isqrt(threshold)**2 == threshold, "late-tail threshold is a square")
    N = 135_000_000_000
    return {
        "schema": "reciprocal-rectangle-exact-diagnostics-v1",
        "problem_id": "3900015",
        "telescoping_prefixes_checked": 200,
        "reported_literature_cutoff": N,
        "uncovered_area_after_reported_cutoff": str(F(1, N + 1)),
        "contact_allowed": True,
        "overlap_of_width_1_over_10_pow_30_rejected": overlap_rejected,
        "prefix_three_witness_valid": True,
        "grid_compaction_denominator": D,
        "compacted_rectangles": [[str(x) for x in r] for r in grid],
        "prefix_three_complete_grid_search": prefix_search,
        "m4_square_hole_complete_grid_search": hole_search,
        "square_hole_arithmetic_admissible_m_up_to_100": squares,
        "preprint_threshold_is_perfect_square": True,
        "full_problem_resolved": False,
        "scope": "exact finite axis-parallel diagnostics; arbitrary rotations and infinite existence not certified",
    }


if __name__ == "__main__":
    print(json.dumps(diagnostics(), sort_keys=True, indent=2))
