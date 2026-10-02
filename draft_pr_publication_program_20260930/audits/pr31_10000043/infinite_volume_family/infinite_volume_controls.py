#!/usr/bin/env python3
"""Independent exact/deterministic falsifiers for proof steps, never an infinite-volume simulation."""
from collections import Counter, defaultdict, deque
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import datetime
import hashlib
import json

HERE = Path(__file__).resolve().parent
checks = Counter()
negative_controls = []


def ck(family, condition):
    checks[family] += 1
    if not condition:
        raise AssertionError(family)


def reject(name, false_claim, witness, scope):
    if false_claim:
        raise AssertionError("Negative control failed to reject: " + name)
    negative_controls.append(dict(name=name, rejected=True, witness=witness, scope=scope))


def components(vertices, edges):
    adj = defaultdict(set)
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    todo = set(vertices)
    answer = []
    while todo:
        start = min(todo)
        part = {start}
        queue = deque([start])
        todo.remove(start)
        while queue:
            u = queue.popleft()
            for v in adj[u] & todo:
                todo.remove(v)
                part.add(v)
                queue.append(v)
        answer.append(part)
    return answer


# Conditional success count for every cluster of a five-height outside-fiber
# revealed graph, at asymmetric as well as symmetric exact probabilities.
heights = list(range(5))
conditional_cases = 0
for outside in product((0, 1), repeat=4):
    exposed = [(i, i + 1) for i, b in enumerate(outside) if b]
    for D in components(heights, exposed):
        for p in [F(1, 3), F(1, 2), F(2, 3)]:
            counts = defaultdict(F)
            for bridge in product((0, 1), repeat=5):
                wt = p ** sum(bridge) * (1 - p) ** (5 - sum(bridge))
                counts[sum(bridge[i] for i in D)] += wt
            for k in range(len(D) + 1):
                expected = comb(len(D), k) * p**k * (1 - p) ** (len(D) - k)
                ck("whole_fiber_conditional_law", counts[k] == expected)
            ck("whole_fiber_conditional_law", 1 - counts[0] == 1 - (1 - p) ** len(D))
            conditional_cases += 1

# Conditioning instead on the original cluster avoiding the neighbor fiber
# forces each connecting edge closed, even when its unconditional law is p.
p = F(1, 3)
event_mass = (1 - p) ** 5
conditional_open_mass = F(0)
reject("conditioning_on_full_cluster_is_not_deferred_revelation",
       conditional_open_mass / event_mass == p,
       {"p": str(p), "event": "five known-connected outside vertices, no neighbor-fiber vertex in full cluster",
        "event_probability": str(event_mass), "conditional_bridge_open_probability": "0"},
       "Exact finite bias witness. It falsifies an invalid conditioning step, not the submitted whole-fiber proof.")

# An adaptive selector permitted to inspect unread outcomes invalidates the
# Bernoulli law: the first closed edge is closed by construction.
reject("future_dependent_candidate_selection",
       F(0) == p,
       {"p": str(p), "candidate": "first closed bit among five, conditional on at least one closed bit",
        "selection_event_probability": str(1 - p**5), "selected_open_probability": "0"},
       "Distinct exact false-control for nonanticipation; the submitted cap uses only past revealed outcomes.")

# Finite-cylinder mixing: translate the support until disjoint, and compare
# to the overlapping control. Coordinates stand for one fixed horizontal base edge.
mixing_rows = []
for shift in [0, 1, 2, 3, 5]:
    support = sorted({0, 1, shift, shift + 1})
    joint = F(0)
    for bits in product((0, 1), repeat=len(support)):
        states = dict(zip(support, bits))
        wt = p**sum(bits) * (1 - p) ** (len(bits) - sum(bits))
        if any(states[i] for i in [0, 1]) and any(states[i] for i in [shift, shift + 1]):
            joint += wt
    marginal = 1 - (1 - p)**2
    mixing_rows.append({"shift": shift, "joint": str(joint), "product": str(marginal**2)})
    if shift >= 2:
        ck("finite_cylinder_mixing", joint == marginal**2)
reject("mixing_does_not_mean_independence_at_overlapping_shifts",
       mixing_rows[0]["joint"] == mixing_rows[0]["product"], mixing_rows[0],
       "Exact support-overlap control; large-shift disjointness is necessary.")

# Product-shaped deterministic obstruction when local finiteness is removed:
# base u--a_i--w for i>=1, with infinite degree at u,w. In the open
# subgraph, (w,0) joins a_i's vertical path 0..i to (u,i).
deletion_rows = []
for N in range(1, 33):
    V = {(0, i) for i in range(1, N + 1)} | {(1, 0)}
    E = []
    for i in range(1, N + 1):
        a = i + 1
        V.update((a, j) for j in range(i + 1))
        E.extend([((1, 0), (a, 0)), ((a, i), (0, i))])
        E.extend(((a, j), (a, j + 1)) for j in range(i))
    ck("finite_deletion_local_finiteness_control", len(components(V, E)) == 1)
    remainder = V - {(1, 0)}
    pieces = components(remainder, [(u, v) for u, v in E if u in remainder and v in remainder])
    ck("finite_deletion_local_finiteness_control", len(pieces) == N)
    ck("finite_deletion_local_finiteness_control", all(len({x for x in D if x[0] == 0}) == 1 for D in pieces))
    deletion_rows.append({"branches": N, "pieces_after_one_deleted_vertex": len(pieces)})
reject("countability_alone_controls_finite_deletion",
       deletion_rows[-1]["pieces_after_one_deleted_vertex"] <= 1,
       {"finite_prefix": deletion_rows[-1], "infinite_extension": "one deletion leaves countably infinitely many finite branches, each with one (u,i)"},
       "Explicit infinite non-locally-finite deterministic product construction; outside the target hypotheses and outside iid Bernoulli law.")


def stretched_tree(depth):
    # Binary labels identify original branch vertices; internal subdivision
    # vertices have unique tuples. Root original vertex is the empty string.
    V = {("b", "")}
    E = []
    original = {0: [("b", "")]}
    for n in range(1, depth + 1):
        original[n] = []
        for parent in original[n - 1]:
            for bit in ["0", "1"]:
                label = parent[1] + bit
                target = ("b", label)
                original[n].append(target)
                path = [parent] + [("s", label, j) for j in range(1, 2**n)] + [target]
                V.update(path)
                E.extend(zip(path, path[1:]))
    return V, E, original


def mincut(V, E, starts, targets):
    S, T = ("source",), ("target",)
    cap = defaultdict(dict)
    big = len(E) + 1
    def add(u, v, value):
        cap[u][v] = cap[u].get(v, 0) + value
        cap[v].setdefault(u, 0)
    for u, v in E:
        add(u, v, 1)
        add(v, u, 1)
    for v in starts:
        add(S, v, big)
    for v in targets:
        add(v, T, big)
    flow = 0
    while True:
        parent = {S: None}
        queue = deque([S])
        while queue and T not in parent:
            u = queue.popleft()
            for v, c in cap[u].items():
                if c and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if T not in parent:
            return flow
        d, v = big, T
        while parent[v] is not None:
            u = parent[v]
            d = min(d, cap[u][v])
            v = u
        v = T
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= d
            cap[v][u] = cap[v].get(u, 0) + d
            v = u
        flow += d


cutset_rows = []
for n in range(1, 5):
    V, E, original = stretched_tree(n + 2)
    # Full subdivided finite set through original level n.
    A = {v for v in V if len(v[1]) <= n}
    fullcut = mincut(V, E, A, original[n + 2])
    rootcut = mincut(V, E, [("b", "")], original[n + 2])
    ck("arbitrary_finite_set_cutsets", fullcut == 2**(n + 1))
    ck("arbitrary_finite_set_cutsets", rootcut == 2)
    cutset_rows.append({"original_level": n, "finite_set_size": len(A),
                        "all_A_vertices_cut": fullcut, "root_only_cut": rootcut})
reject("root_cut_bound_is_an_arbitrary_finite_set_cut_bound",
       cutset_rows[-1]["all_A_vertices_cut"] == cutset_rows[-1]["root_only_cut"],
       cutset_rows[-1],
       "Exact finite max-flow witnesses support the separately proved infinite edge-disjoint-ray lower bound. They do not prove pc=1.")

# Exact finite-level probabilities computed by a branching recursion,
# independent of the author's path-count union-bound checker.
tree_rows = []
for p in [F(1, 3), F(1, 2), F(4, 5)]:
    for n in range(1, 7):
        success = F(1)
        for level in range(n, 0, -1):
            success = 1 - (1 - p**(2**level) * success)**2
        bound = 2**n * p**(2**(n + 1) - 2)
        ck("stretched_tree_exact_branching_probability", success <= bound)
        tree_rows.append({"p": str(p), "level": n, "exact_success": str(success), "union_bound": str(bound)})

ray_rows = []
author_product = F(1)
capacity_product = F(1)
for n in range(1, 65):
    author_product *= 1 - F(1, 2**(n + 1))
    # At p=1/2, M_v=v+1 and edge (v,v+1), v=n-1, use M_v+M_(v+1)=2n+1 trials.
    capacity_product *= 1 - F(1, 2**(2*n + 1))
    ck("unbounded_capacity_ray", author_product >= F(1, 2))
    ck("unbounded_capacity_ray", capacity_product >= F(5, 6))
    ray_rows.append({"edges": n, "authors_q_product": str(author_product), "capacity_q_product": str(capacity_product)})
reject("edgewise_q_less_than_one_forces_homogeneous_subcriticality",
       capacity_product == 0,
       {"p": "1/2", "M_v": "v+1", "q_edge_v": "1-2^(-(2v+3))", "failure_sum": "1/6", "infinite_product_lower_bound": "5/6"},
       "Checkable infinite union-bound argument on a ray; it falsifies an inhomogeneous-to-homogeneous transfer, not the target.")

# A connected triangular region of ray x Z meets fiber v in v+1 vertices.
# Its deterministic limit refutes finite=>uniform from graph geometry alone.
triangular_rows = []
for N in range(1, 33):
    V = {(v, h) for v in range(N + 1) for h in range(v + 1)}
    E = [((v, h), (v, h + 1)) for v, h in V if (v, h + 1) in V]
    E += [((v, h), (v + 1, h)) for v, h in V if (v + 1, h) in V]
    ck("finite_but_unbounded_deterministic_geometry", len(components(V, E)) == 1)
    counts = Counter(v for v, h in V)
    ck("finite_but_unbounded_deterministic_geometry", all(counts[v] == v + 1 for v in range(N + 1)))
    triangular_rows.append({"last_base_vertex": N, "largest_fiber_intersection": max(counts.values())})
reject("finite_in_each_fiber_implies_uniform_finite_bound",
       triangular_rows[-1]["largest_fiber_intersection"] <= 1,
       {"finite_prefix": triangular_rows[-1], "infinite_extension": "C={(v,h):v>=0,0<=h<=v}; |C intersect F_v|=v+1"},
       "Deterministic open/closed configuration on a base ray with pc=1. At homogeneous p<1 its prescribed infinite-open-edge event has probability zero; it is not a Bernoulli counterexample.")

# On ray x Z open all horizontal edges and close all vertical edges.
# This Dirac law is vertically invariant and ergodic: infinite-cluster union
# occupies density one in each fiber; every individual cluster meets it once.
row_clusters = [{(v, h) for v in range(20)} for h in range(-10, 11)]
fiber = {(0, h) for h in range(-10, 11)}
union_density = F(len(set.union(*row_clusters) & fiber), len(fiber))
ck("union_density_individual_cluster_gap", union_density == 1)
ck("union_density_individual_cluster_gap", all(len(C & fiber) == 1 for C in row_clusters))
reject("Birkhoff_union_density_is_density_of_each_cluster",
       all(F(len(C & fiber), len(fiber)) == union_density for C in row_clusters),
       {"union_density": "1", "each_infinite_horizontal_row_cluster_fiber_intersection": "1", "law": "vertically invariant ergodic Dirac, horizontal open/vertical closed"},
       "Logical false-control outside iid bond percolation; it isolates exactly why uniqueness is required by the submitted Birkhoff argument.")

output = {
    "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "all_positive_controls_passed": True,
    "positive_assertions": sum(checks.values()),
    "assertions_by_family": dict(checks),
    "negative_controls": negative_controls,
    "whole_fiber_conditional_cases": conditional_cases,
    "finite_cylinder_mixing": mixing_rows,
    "finite_deletion_rows": deletion_rows,
    "cutset_rows": cutset_rows,
    "exact_stretched_tree_level_probabilities": tree_rows,
    "ray_products": ray_rows,
    "triangular_rows": triangular_rows,
    "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope": "Finite exact and deterministic controls, plus separately stated infinite limiting constructions. No finite control proves a universal infinite-volume theorem or refutes the original target.",
}
(HERE / "infinite_volume_controls_results.json").write_text(json.dumps(output, indent=2) + "\n")
(HERE / "negative_controls.json").write_text(json.dumps(negative_controls, indent=2) + "\n")
print(json.dumps({k: output[k] for k in ["all_positive_controls_passed", "positive_assertions", "assertions_by_family", "whole_fiber_conditional_cases"]}, indent=2))
print("Rejected false claims:", len(negative_controls))
