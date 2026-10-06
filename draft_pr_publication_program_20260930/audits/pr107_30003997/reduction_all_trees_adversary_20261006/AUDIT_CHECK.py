#!/usr/bin/env python3
"""Independent finite challenges; correctness for arbitrary size is in REPORT.md.

No original verifier or review was read. The strongest finite family enumerates
ALL (|V|-1)-arc subsets and filters them by generic arborescence conditions.
"""
from datetime import datetime, timezone
from itertools import combinations, combinations_with_replacement, product
from math import prod
from pathlib import Path
import hashlib
import json


def construction(n, clauses):
    vertices = ["r"]
    layer = {"r": 0}
    for i in range(1, n + 1):
        vertices += [f"t{i}", f"f{i}", f"v{i}"]
        layer.update({f"t{i}": 1, f"f{i}": 1, f"v{i}": 2})
    for j in range(len(clauses)):
        vertices.append(f"z{j}")
        layer[f"z{j}"] = 3
    arcs = []
    for i in range(1, n + 1):
        arcs += [("r", f"t{i}"), ("r", f"f{i}"),
                 (f"t{i}", f"v{i}"), (f"f{i}", f"v{i}")]
    for j, clause in enumerate(clauses):
        arcs += [(f"v{i}", f"z{j}") for i in sorted(set(map(abs, clause)))]
    assert len(arcs) == len(set(arcs))
    table = {v: {a: 0 for a in arcs} for v in vertices if v != "r"}
    for j, clause in enumerate(clauses):
        for i in range(1, n + 1):
            table[f"z{j}"][("r", f"t{i}")] = int(-i in clause)
            table[f"z{j}"][("r", f"f{i}")] = int(i in clause)
    return vertices, arcs, layer, table


def generic_tree_paths(vertices, edge_set):
    """Return paths iff this edge set is a spanning root-out-arborescence."""
    if len(edge_set) != len(vertices) - 1:
        return None
    incoming = {v: [] for v in vertices}
    outgoing = {v: [] for v in vertices}
    for a, b in edge_set:
        incoming[b].append(a)
        outgoing[a].append(b)
    if incoming["r"] or any(len(incoming[v]) != 1 for v in vertices if v != "r"):
        return None
    paths = {"r": ()}
    queue = ["r"]
    for a in queue:
        for b in outgoing[a]:
            if b in paths:
                return None
            paths[b] = paths[a] + ((a, b),)
            queue.append(b)
    return paths if len(paths) == len(vertices) else None


def enumerate_trees(vertices, arcs, method):
    if method == "all_arc_subsets":
        candidates = combinations(arcs, len(vertices) - 1)
    else:
        # This still uses a GENERIC one-parent enumeration and does not assume
        # assignment/literal gadget semantics. Every candidate is BFS checked.
        incoming = [[a for a in arcs if a[1] == v] for v in vertices if v != "r"]
        candidates = product(*incoming)
    for edges in candidates:
        paths = generic_tree_paths(vertices, edges)
        if paths is not None:
            yield frozenset(edges), paths


def truth_unsatisfied(n, clauses, bits):
    return sum(not any(bits[abs(lit) - 1] == (lit > 0) for lit in c) for c in clauses)


def check_one(n, clauses, method="all_arc_subsets"):
    vertices, arcs, layer, table = construction(n, clauses)
    assert all(1 <= len(c) <= 3 for c in clauses)
    assert all(len(set(map(abs, c))) == len(c) for c in clauses)
    assert len(vertices) == 1 + 3 * n + len(clauses)
    assert len(arcs) == 4 * n + sum(map(len, clauses))
    assert all(layer[b] == layer[a] + 1 for a, b in arcs)
    assert all(sum(b == v for a, b in arcs) <= 3 for v in vertices if v != "r")
    assert set(c for row in table.values() for c in row.values()) <= {0, 1}
    reach = {"r"}
    for lev in range(1, 4):
        reach.update(b for a, b in arcs if layer[b] == lev and a in reach)
    assert reach == set(vertices)
    assert sum(len(row) for row in table.values()) == (len(vertices) - 1) * len(arcs)
    all_assignments = list(product([False, True], repeat=n))
    truth_best = min(truth_unsatisfied(n, clauses, b) for b in all_assignments)
    per_assignment_best = {}
    seen_keys = set()
    count = 0
    best = None
    positive_best = None
    forced = {("r", f"{s}{i}") for i in range(1, n + 1) for s in ("t", "f")}
    baseline = 4 * n + 3 * len(clauses)
    for edges, paths in enumerate_trees(vertices, arcs, method):
        count += 1
        assert forced <= edges
        bits = tuple((f"t{i}", f"v{i}") in edges for i in range(1, n + 1))
        assert all(((f"t{i}", f"v{i}") in edges) !=
                   ((f"f{i}", f"v{i}") in edges) for i in range(1, n + 1))
        selected = []
        selected_false = 0
        for j, clause in enumerate(clauses):
            parents = [int(a[1:]) for a, b in edges if b == f"z{j}"]
            assert len(parents) == 1
            i = parents[0]
            assert i in set(map(abs, clause))
            literal = i if i in clause else -i
            selected.append(i)
            selected_false += (bits[i - 1] != (literal > 0))
        key = (bits, tuple(selected))
        assert key not in seen_keys
        seen_keys.add(key)
        actual = sum(table[v][a] for v in vertices if v != "r" for a in paths[v])
        actual_positive = sum(table[v][a] + 1 for v in vertices if v != "r" for a in paths[v])
        assert actual == selected_false
        assert actual_positive - actual == baseline
        assert all(len(paths[v]) == layer[v] for v in vertices)
        best = actual if best is None else min(best, actual)
        positive_best = actual_positive if positive_best is None else min(positive_best, actual_positive)
        per_assignment_best[bits] = min(actual, per_assignment_best.get(bits, actual))
    assert count == 2 ** n * prod(map(len, clauses))
    assert len(seen_keys) == count
    assert best == truth_best
    assert positive_best == baseline + truth_best
    assert all(per_assignment_best[b] == truth_unsatisfied(n, clauses, b) for b in all_assignments)
    return {"variables": n, "clauses": [list(c) for c in clauses], "method": method,
            "vertices": len(vertices), "arcs": len(arcs), "dense_entries": (len(vertices)-1)*len(arcs),
            "all_feasible_tree_count": count, "optimum": best,
            "positive_optimum": positive_best, "positive_baseline": baseline}


def preprocess(raw_clauses):
    """Total preprocessing, with explicitly fixed promise-preserving constants."""
    if any(len(c) == 0 for c in raw_clauses):
        return 1, [(1,), (-1,)], "fixed_no_empty_clause"
    clean = []
    for c in raw_clauses:
        s = set(c)
        if any(-x in s for x in s):
            continue
        clean.append(tuple(sorted(s, key=lambda x: (abs(x), x))))
    if not clean:
        return 1, [(1,)], "fixed_yes_no_nontrivial_clauses"
    names = sorted({abs(x) for c in clean for x in c})
    rename = {x: i + 1 for i, x in enumerate(names)}
    return len(names), [tuple(rename[abs(x)] if x > 0 else -rename[abs(x)] for x in c) for c in clean], "ordinary"


def canonical_clauses(n):
    return [tuple(i if s else -i for i, s in zip(names, signs))
            for k in range(1, min(3, n) + 1)
            for names in combinations(range(1, n + 1), k)
            for signs in product([False, True], repeat=k)]


def main():
    started = datetime.now(timezone.utc).isoformat()
    cases = []
    # 165 canonical two-variable clause multisets, including duplicated clauses,
    # empty conjunction, unused variables, units, and all binary sign patterns.
    for m in range(4):
        for clauses in combinations_with_replacement(canonical_clauses(2), m):
            cases.append(check_one(2, clauses))
    # All 26 one-clause canonical three-variable formulas plus no-clause case.
    cases.append(check_one(3, []))
    for clause in canonical_clauses(3):
        cases.append(check_one(3, [clause]))
    # Eight complementary ternary clauses: exactly one unsatisfied for EVERY
    # assignment; tests 52,488 trees and global sharing across many clauses.
    cube = canonical_clauses(3)[-8:]
    cube_result = check_one(3, cube, "generic_parent_product")
    assert cube_result["optimum"] == 1
    cases.append(cube_result)
    # A satisfying assignment still allows bad literal choices in feasible trees;
    # the theorem concerns minimum cost, not all trees on satisfiable formulas.
    cases.append(check_one(3, [(1, 2), (-1, 3), (-2, -3)], "generic_parent_product"))
    # Explicit total-reduction boundary cases.
    boundaries = []
    raw_cases = [[], [()], [(1, -1)], [(1, 1, 1)], [(1,), (-1,)],
                 [(1, -1), ()], [(10**12,)], [(10**12,), (-10**12,)],
                 [(1, -1), (2, 2, 2)], [(1, 1, 2), (-1, -1, -2)]]
    for raw in raw_cases:
        n, clean, route = preprocess(raw)
        result = check_one(n, clean)
        names = sorted({abs(x) for c in raw for x in c})
        raw_best = min(sum(not any(dict(zip(names, b))[abs(lit)] == (lit > 0) for lit in c) for c in raw)
                       for b in product([False, True], repeat=len(names)))
        assert (raw_best == 0) == (result["optimum"] == 0)
        boundaries.append({"raw": [list(c) for c in raw], "route": route,
                           "raw_satisfiable": raw_best == 0, "result": result})
    # Honest failing negative controls: demonstrate EXACT necessity of assumptions.
    v, a, _, c = construction(1, [()])
    empty_trees = sum(1 for _ in enumerate_trees(v, a, "all_arc_subsets"))
    assert empty_trees == 0
    v, a, _, c = construction(1, [(1, -1)])
    tautology_costs = [sum(c[x][e] for x in v if x != "r" for e in paths[x])
                       for _, paths in enumerate_trees(v, a, "all_arc_subsets")]
    assert min(tautology_costs) == 1
    negatives = [{"challenge": "Apply raw gadget to an empty clause",
                  "expected_identity_or_promise_failed": "z0 is unreachable; no feasible spanning tree",
                  "observed_feasible_tree_count": empty_trees,
                  "resolution": "explicitly route any empty clause to fixed contradictory-unit no-instance"},
                 {"challenge": "Apply raw gadget to an undeleted tautological clause (x1 or not x1)",
                  "expected_identity_or_promise_failed": "Boolean optimum is 0 but tree optimum is 1",
                  "observed_tree_costs": tautology_costs,
                  "resolution": "delete tautological clauses as candidate requires"}]
    result = {"started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
              "status": "PASS", "independence": "written without reading original verifier or reviews",
              "finite_checks_are_not_proof_for_arbitrary_size": True,
              "formula_cases": len(cases), "boundary_cases": len(boundaries),
              "total_feasible_trees_checked": sum(c["all_feasible_tree_count"] for c in cases) +
                                               sum(b["result"]["all_feasible_tree_count"] for b in boundaries),
              "methods": ["generic all (|V|-1)-arc subset enumeration", "generic one-parent products + BFS"],
              "cases": cases, "boundaries": boundaries, "failed_negative_controls": negatives}
    out = Path(__file__).with_name("FINITE_CHECK_RESULTS.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("cases", "boundaries")}, indent=2))
    print("output_sha256:", hashlib.sha256(out.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
