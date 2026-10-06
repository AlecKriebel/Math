#!/usr/bin/env python3
"""Independent model, frozen before reading original verifier or review.

Enumerates every edge subset of size |V|-1, then recognizes trees generically.
No construction-specific parent-choice enumeration is used by the optimizer.
The objective is evaluated from a full destination-by-edge table and BFS paths.
"""
import argparse
import hashlib
import itertools
import json
import random


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normalize(n, clauses):
    out = []
    for clause in clauses:
        require(all(isinstance(x, int) and 1 <= abs(x) <= n for x in clause), "invalid literal")
        literals = set(clause)
        if any(-x in literals for x in literals):
            continue
        if not literals:
            return 1, ((1,), (-1,)), "fixed_no"
        require(len(literals) <= 3, "not at-most-three-literal CNF")
        out.append(tuple(sorted(literals, key=lambda x: (abs(x), x))))
    if not out:
        return 1, ((1,),), "fixed_yes"
    return n, tuple(out), "ordinary"


def construct(n, clauses):
    # Integer indices: root; true/false copies; assignment vertices; clauses.
    vertices = tuple(range(1 + 3 * n + len(clauses)))
    edges = []
    levels = [0] + [1] * (2 * n) + [2] * n + [3] * len(clauses)
    for i in range(n):
        t, f, v = 1 + 2 * i, 2 + 2 * i, 1 + 2 * n + i
        edges.extend(((0, t), (0, f), (t, v), (f, v)))
    for j, clause in enumerate(clauses):
        require(clause and len(set(map(abs, clause))) == len(clause), "clause was not normalized")
        z = 1 + 3 * n + j
        edges.extend((1 + 2 * n + abs(lit) - 1, z) for lit in clause)
    edges = tuple(edges)
    dense = [[0 for _ in edges] for _ in vertices]
    for j, clause in enumerate(clauses):
        z = 1 + 3 * n + j
        for k, (tail, head) in enumerate(edges):
            if tail == 0:
                i = (head - 1) // 2 + 1
                polarity = 1 if head % 2 == 1 else -1
                dense[z][k] = int(-polarity * i in clause)
    return {"vertices": vertices, "edges": edges, "dense": dense, "levels": levels, "root": 0}


def tree_paths(graph, subset):
    vertices, edges, root = graph["vertices"], graph["edges"], graph["root"]
    if len(subset) != len(vertices) - 1:
        return None
    incoming = {v: 0 for v in vertices}
    outgoing = {v: [] for v in vertices}
    for k in subset:
        u, v = edges[k]
        incoming[v] += 1
        outgoing[u].append((v, k))
    if incoming[root] != 0 or any(incoming[v] != 1 for v in vertices if v != root):
        return None
    paths = {root: ()}
    frontier = [root]
    for u in frontier:
        for v, k in outgoing[u]:
            if v in paths:
                return None
            paths[v] = paths[u] + (k,)
            frontier.append(v)
    return paths if len(paths) == len(vertices) else None


def dense_path_cost(graph, paths):
    return sum(graph["dense"][v][k] for v in graph["vertices"]
               if v != graph["root"] for k in paths[v])


def optimize_all_subsets(graph):
    minimum = None
    counts = {"edge_subsets_examined": 0, "feasible_trees": 0, "noncanonical_trees": 0}
    values = []
    for subset in itertools.combinations(range(len(graph["edges"])), len(graph["vertices"]) - 1):
        counts["edge_subsets_examined"] += 1
        paths = tree_paths(graph, subset)
        if paths is None:
            continue
        counts["feasible_trees"] += 1
        value = dense_path_cost(graph, paths)
        values.append((subset, value, paths))
        minimum = value if minimum is None else min(minimum, value)
    return minimum, counts, values


def truth_optimum(n, clauses):
    return min(sum(not any(bits[abs(lit)-1] == (lit > 0) for lit in clause) for clause in clauses)
               for bits in itertools.product((False, True), repeat=n))


def verify_formula(n, raw):
    original_min = truth_optimum(n, raw)
    k, clauses, route = normalize(n, raw)
    graph = construct(k, clauses)
    expected = truth_optimum(k, clauses)
    require((original_min == 0) == (expected == 0), "preprocessing decision changed")
    minimum, counts, trees = optimize_all_subsets(graph)
    require(minimum == expected, "generic optimum differs from truth enumeration")
    require(len(graph["edges"]) == len(set(graph["edges"])), "parallel arcs")
    require(all(graph["levels"][v] == graph["levels"][u]+1 for u, v in graph["edges"]), "nonadjacent layers")
    require(all(sum(b == v for a, b in graph["edges"]) <= 3 for v in graph["vertices"]), "indegree")
    require(all(c in (0, 1) for row in graph["dense"] for c in row), "nonbinary cost")
    offset = 4*k + 3*len(clauses)
    positive = dict(graph, dense=[[c+1 for c in row] for row in graph["dense"]])
    positive_min = None
    for subset, value, paths in trees:
        # Check derived identity for every generic tree; do not use it in optimizer.
        bits = tuple(any(graph["edges"][edge] == (1+2*i, 1+2*k+i) for edge in subset) for i in range(k))
        selected_false = 0
        canonical = True
        for j, clause in enumerate(clauses):
            z = 1+3*k+j
            last_tail = graph["edges"][paths[z][-1]][0]
            i = last_tail-(1+2*k)
            signs = [lit for lit in clause if abs(lit) == i+1]
            canonical = canonical and len(signs) == 1 and len(paths[z]) == 3
            if len(signs) == 1:
                selected_false += int(bits[i] != (signs[0] > 0))
        counts["noncanonical_trees"] += int(not canonical)
        require(value == selected_false, "tree identity failed")
        shifted = dense_path_cost(positive, paths)
        require(shifted == value+offset, "positive shift depends on tree")
        positive_min = shifted if positive_min is None else min(positive_min, shifted)
    require(positive_min == expected+offset, "positive optimum failed")
    require((positive_min <= offset) == (expected == 0), "positive threshold failed")
    return {"n": n, "raw": raw, "route": route, "normalized_n": k, "normalized": clauses,
            "minimum": minimum, "truth_minimum": expected, "positive_minimum": positive_min,
            "offset": offset, **counts}


def generic_negative_controls():
    # These are arbitrary graphs: disconnected components and incoming-root arc.
    cases = [
        {"vertices": (0,1,2), "edges": ((0,1),(1,2),(2,1)), "root":0},
        {"vertices": (0,1,2,3), "edges": ((0,1),(2,3),(3,2)), "root":0},
        {"vertices": (0,1), "edges": ((1,0),), "root":0},
        {"vertices": (0,), "edges": (), "root":0},
        {"vertices": (0,1,2), "edges": ((0,1),(0,2),(1,2),(2,1)), "root":0},
    ]
    wanted = (1,0,0,1,3)
    out = []
    for graph, count in zip(cases, wanted):
        graph["dense"] = [[2*v+k for k in range(len(graph["edges"]))] for v in graph["vertices"]]
        optimum, counts, trees = optimize_all_subsets(graph)
        require(counts["feasible_trees"] == count, "generic false-positive/negative control")
        out.append({"graph": graph, "minimum": optimum, **counts})
    return out


def larger_witness_checks():
    # Checks construction/mechanism at larger sizes, not a claim of exhaustive verification.
    out = []
    for n in (3,7,16,40):
        for m in (1,5,25):
            clauses = tuple(tuple((i+1) * (-1 if (i+j)%2 else 1) for i in sorted({j%n,(j+1)%n,(j+2)%n})) for j in range(m))
            graph = construct(n, clauses)
            for bits in (tuple(False for _ in range(n)), tuple(True for _ in range(n)), tuple(i%2==0 for i in range(n))):
                subset = []
                selected_false = 0
                for i in range(n):
                    subset.extend((4*i,4*i+1,4*i+2+int(not bits[i])))
                for j, clause in enumerate(clauses):
                    chosen = next((lit for lit in clause if bits[abs(lit)-1] == (lit>0)), clause[0])
                    edge = (1+2*n+abs(chosen)-1,1+3*n+j)
                    subset.append(graph["edges"].index(edge))
                    selected_false += int(bits[abs(chosen)-1] != (chosen>0))
                paths = tree_paths(graph, tuple(subset))
                require(paths is not None, "large witness infeasible")
                require(dense_path_cost(graph, paths) == selected_false, "large mechanism cost failed")
                shifted = dict(graph, dense=[[v+1 for v in row] for row in graph["dense"]])
                require(dense_path_cost(shifted, paths) == selected_false+4*n+3*m, "large offset failed")
                out.append({"n":n,"m":m,"assignment_sha256":hashlib.sha256(bytes(bits)).hexdigest(),"cost":selected_false})
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument("--false-control", action="store_true")
    options = parser.parse_args()
    if options.false_control:
        require(0 == 1, "known-false independent control rejected")
    clauses2 = [(1,),(-1,),(2,),(-2,),(1,2),(1,-2),(-1,2),(-1,-2)]
    results = []
    for m in range(4):
        results.extend(verify_formula(2, raw) for raw in itertools.product(clauses2, repeat=m))
    controls = [(0,()),(0,((),)),(1,((1,),)),(1,((1,),(-1,))),
                (1,((1,-1),)),(1,((1,1,1),(-1,-1))),
                (2,((1,-1,2),(2,2),(-2,))),
                (2,((1,2),(1,-2),(-1,2),(-1,-2))),
                (2,((1,),(),(2,-2))), (2,((1,2,2),(-1,-2,-2)))]
    results.extend(verify_formula(n, raw) for n, raw in controls)
    rng = random.Random(30003997)
    clauses3 = [c for size in (1,2,3) for variables in itertools.combinations(range(1,4),size)
                for signs in itertools.product((-1,1), repeat=size)
                for c in [tuple(v*s for v,s in zip(variables,signs))]]
    for _ in range(50):
        results.append(verify_formula(3,tuple(rng.choice(clauses3) for _ in range(rng.randrange(1,3)))))
    report = {"model":"dense destination-specific edge table; BFS root paths; unfiltered edge subsets of size |V|-1",
              "cases":results,"formula_cases":len(results),
              "total_edge_subsets_examined":sum(x["edge_subsets_examined"] for x in results),
              "total_feasible_trees":sum(x["feasible_trees"] for x in results),
              "total_noncanonical_trees":sum(x["noncanonical_trees"] for x in results),
              "generic_negative_controls":generic_negative_controls(),"larger_witness_checks":larger_witness_checks(),
              "claim_limit":"finite checks support the candidate; arbitrary-size hardness requires the written reduction; novelty unestablished"}
    rendered = json.dumps(report, indent=2)+"\n"
    if options.output:
        with open(options.output,"w") as stream:
            stream.write(rendered)
    print(json.dumps({k:v for k,v in report.items() if k not in ("cases","generic_negative_controls","larger_witness_checks")},sort_keys=True))


if __name__ == "__main__":
    main()
