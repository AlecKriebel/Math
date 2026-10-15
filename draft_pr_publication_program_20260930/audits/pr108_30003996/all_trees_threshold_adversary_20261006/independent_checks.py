#!/usr/bin/env python3
"""Independent finite audit of literal all-root costs, without author code.

No check depends on assert: explicit exceptions still fire under python -O.
Finite results support the separately frozen universal proof; they do not prove it.
"""

import ast
from collections import Counter, deque
from datetime import datetime, timezone
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import hashlib
import json
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def edge(a, b):
    require(a != b, "loop is not a permitted edge")
    return tuple(sorted((a, b)))


def normalize(raw_clauses):
    """Use distinct symbols, never maximum numeric label; discard unused names."""
    clauses = []
    for raw in raw_clauses:
        require(all(isinstance(x, int) and x != 0 for x in raw), "bad literal")
        deduplicated = set(raw)
        if not deduplicated:
            return "fixed_no", 0, ()
        if any(-literal in deduplicated for literal in deduplicated):
            continue
        require(len(deduplicated) <= 3, "source clause has more than three literals")
        clauses.append(tuple(sorted(deduplicated, key=lambda x: (abs(x), x))))
    if not clauses:
        return "fixed_yes", 0, ()
    symbols = sorted({abs(x) for clause in clauses for x in clause})
    relabel = {symbol: i + 1 for i, symbol in enumerate(symbols)}
    dense = tuple(tuple((1 if x > 0 else -1) * relabel[abs(x)] for x in clause)
                  for clause in clauses)
    return "main", len(symbols), dense


def fixed_instance(yes):
    # Connected simple graph with one undirected edge and threshold zero.
    return 2, ((0, 1),), [(0, 1), (1, 0)], [[0, 0], [0, 0]] if yes else [[1, 1], [0, 0]], 0


def construct(n, clauses, B):
    require(n >= 1 and clauses and B >= 1, "main construction assumptions")
    require(all(1 <= len(c) <= 3 for c in clauses), "nonempty 3-CNF clauses required")
    require(all(len(set(c)) == len(c) and not any(-x in c for x in c) for c in clauses),
            "clauses must be deduplicated and non-tautological")
    require(all(1 <= abs(x) <= n for c in clauses for x in c), "literal outside indexed variables")
    m = len(clauses)
    N = n + m + 2
    edges = [edge(0, 1)]
    for i in range(n):
        edges.extend((edge(0, i + 2), edge(1, i + 2)))
    for j, clause in enumerate(clauses):
        edges.extend(edge(2 + n + j, 1 + abs(literal)) for literal in clause)
    require(len(edges) == len(set(edges)), "construction did not produce a simple graph")
    edges = tuple(sorted(edges))
    arcs = [arc for a, b in edges for arc in ((a, b), (b, a))]
    arc_index = {arc: i for i, arc in enumerate(arcs)}
    costs = [[0 for _ in arcs] for _ in range(N)]
    for a, b in edges:
        if edge(a, b) == (0, 1):
            weight = 0
        elif a < 2 or b < 2:
            weight = 1
        else:
            weight = B
        costs[0][arc_index[a, b]] = weight
        costs[0][arc_index[b, a]] = weight
    for j, clause in enumerate(clauses):
        root = 2 + n + j
        for literal in clause:
            variable = 1 + abs(literal)
            costs[root][arc_index[variable, 0]] = int(literal < 0)
            costs[root][arc_index[variable, 1]] = int(literal > 0)
    require(sum(len(row) for row in costs) == 2 * N * len(edges), "dense table count")
    return N, edges, arcs, costs, B * m + n


def is_tree(N, selected):
    if len(selected) != N - 1:
        return False
    parent = list(range(N))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for a, b in selected:
        u, v = find(a), find(b)
        if u == v:
            return False
        parent[u] = v
    return len({find(i) for i in range(N)}) == 1


def all_trees(N, edges):
    for selected in combinations(edges, N - 1):
        if is_tree(N, selected):
            yield selected


def root_arcs(N, selected, root):
    neighbors = [[] for _ in range(N)]
    for a, b in selected:
        neighbors[a].append(b)
        neighbors[b].append(a)
    seen = {root}
    queue = deque([root])
    oriented = []
    while queue:
        a = queue.popleft()
        for b in neighbors[a]:
            if b not in seen:
                seen.add(b)
                queue.append(b)
                oriented.append((a, b))
    require(len(seen) == N and len(oriented) == N - 1, "root traversal must span tree")
    return oriented


def evaluate(N, selected, arcs, costs, inward=False):
    index = {arc: i for i, arc in enumerate(arcs)}
    contributions = []
    for root in range(N):
        oriented = root_arcs(N, selected, root)
        if inward:
            oriented = [(b, a) for a, b in oriented]
        contributions.append(sum(costs[root][index[a, b]] for a, b in oriented))
    return sum(contributions), contributions


def reverse_costs(arcs, costs):
    index = {arc: i for i, arc in enumerate(arcs)}
    return [[row[index[b, a]] for a, b in arcs] for row in costs]


def assignment_min_unsatisfied(n, clauses):
    values = []
    for assignment in product((False, True), repeat=n):
        unsatisfied = sum(not any(assignment[abs(x) - 1] == (x > 0) for x in c) for c in clauses)
        values.append((unsatisfied, assignment))
    return min(values)


def structural_counts(n, selected):
    m_start = 2 + n
    h = int((0, 1) in selected)
    p = sum(a < 2 or b < 2 for a, b in selected if (a, b) != (0, 1))
    q = sum(a >= m_start or b >= m_start for a, b in selected)
    return h, p, q


def structured_assignment(n, m, selected):
    selected_set = set(selected)
    degrees = Counter(v for a, b in selected for v in (a, b))
    require((0, 1) in selected_set, "structured tree lacks hub edge")
    require(all(degrees[2 + n + j] == 1 for j in range(m)), "structured clause is not a leaf")
    assignment = []
    for i in range(n):
        attachments = [h for h in (0, 1) if edge(h, 2 + i) in selected_set]
        require(len(attachments) == 1, "structured variable must have one hub")
        assignment.append(attachments[0] == 0)
    return tuple(assignment)


def selected_false_count(n, clauses, selected, assignment):
    count = 0
    for j, clause in enumerate(clauses):
        root = 2 + n + j
        neighbors = [b if a == root else a for a, b in selected if root in (a, b)]
        require(len(neighbors) == 1, "clause selection must be unique")
        literal = next(x for x in clause if 1 + abs(x) == neighbors[0])
        count += int(assignment[abs(literal) - 1] != (literal > 0))
    return count


def labels(n, selected):
    def name(v):
        return "t" if v == 0 else "f" if v == 1 else f"v{v-1}" if v < 2 + n else f"q{v-1-n}"
    return [[name(a), name(b)] for a, b in selected]


def audit_formula(n, clauses, B, totals):
    N, edges, arcs, costs, K = construct(n, clauses, B)
    reversed_costs = reverse_costs(arcs, costs)
    positive_costs = [[x + 1 for x in row] for row in costs]
    m = len(clauses)
    minimum = None
    minimum_tree = None
    structured_minimum = None
    cases = 0
    categories = Counter()
    for selected in all_trees(N, edges):
        cases += 1
        F, contributions = evaluate(N, selected, arcs, costs)
        h, p, q = structural_counts(n, selected)
        require(q >= m, "arbitrary tree has too few clause incidences")
        require(p + q + h == N - 1, "edge partition failed")
        require(contributions[0] == p + B * q, "actual hub-root cost not symmetric edge sum")
        require(p + B * q == K + (1 - h) + (B - 1) * (q - m), "parameter identity failed")
        if B == n + 1:
            require(p + B * q == K + (1 - h) + n * (q - m), "original threshold identity failed")
        require(all(x >= 0 for x in contributions[1:]), "nonnegative other-root premise failed")
        require(evaluate(N, selected, arcs, reversed_costs, inward=True) == (F, contributions),
                "inward orientation with reversed tables changed objective")
        F_positive, _ = evaluate(N, selected, arcs, positive_costs)
        require(F_positive == F + N * (N - 1), "positive shift not exact")
        categories["all_trees"] += 1
        categories["missing_tf"] += 1 - h
        categories["multiply_attached_clause"] += int(q > m)
        categories["bridge_variable_both_hubs"] += int(any(edge(0, 2+i) in selected and edge(1, 2+i) in selected for i in range(n)))
        structured = h == 1 and q == m
        categories["structured"] += int(structured)
        if F <= K:
            require(B >= 2 and structured, "threshold permitted unstructured tree")
        if structured:
            assignment = structured_assignment(n, m, selected)
            false_count = selected_false_count(n, clauses, selected, assignment)
            require(F == K + false_count, "literal selection objective failed")
            require(contributions[1] == 0 and all(contributions[2+i] == 0 for i in range(n)),
                    "zero-root cost was accidentally nonzero")
            for j, clause in enumerate(clauses):
                root = 2 + n + j
                selected_neighbor = next(b if a == root else a for a, b in selected if root in (a,b))
                oriented = set(root_arcs(N, selected, root))
                for i in range(n):
                    v = 2 + i
                    hub = 0 if assignment[i] else 1
                    require(((v,hub) in oriented) == (v == selected_neighbor), "unselected hub edge points upward")
                literal = next(x for x in clause if 1 + abs(x) == selected_neighbor)
                expected = int(assignment[abs(literal)-1] != (literal > 0))
                require(contributions[root] == expected, "clause root cost differs from selected literal")
            structured_minimum = F if structured_minimum is None else min(structured_minimum, F)
        if minimum is None or F < minimum:
            minimum, minimum_tree = F, selected
    require(cases > 0, "connected gadget has no spanning tree")
    min_unsatisfied, assignment = assignment_min_unsatisfied(n, clauses)
    require((minimum <= K) == (min_unsatisfied == 0), "decision equivalence failed")
    require(structured_minimum == K + min_unsatisfied, "minimum among structured trees differs")
    # Direct satisfying assignment witness, independently built from clause truth.
    if min_unsatisfied == 0:
        witness = [edge(0, 1)] + [edge(0 if truth else 1, i + 2) for i, truth in enumerate(assignment)]
        for j, clause in enumerate(clauses):
            literal = next(x for x in clause if assignment[abs(x)-1] == (x > 0))
            witness.append(edge(2 + n + j, 1 + abs(literal)))
        require(is_tree(N, witness), "satisfying assignment witness is not a spanning tree")
        require(evaluate(N, witness, arcs, costs)[0] == K, "satisfying witness did not meet threshold")
    totals["formula_parameter_cases"] += 1
    totals["tree_parameter_cases"] += cases
    totals["root_orientations_outward"] += cases * N
    totals["root_orientations_inward_reversed_table"] += cases * N
    totals["root_orientations_positive_shift"] += cases * N
    for key, value in categories.items():
        totals[key] += value
    return {"n": n, "clauses": clauses, "B": B, "K": K, "N": N, "edges": len(edges),
            "dense_entries": 2*N*len(edges), "tree_cases": cases, "minimum": minimum,
            "structured_minimum": structured_minimum, "min_unsatisfied": min_unsatisfied,
            "minimum_tree": labels(n, minimum_tree), "categories": dict(categories)}


def clause_universe(n):
    result = []
    for size in range(1, min(3, n) + 1):
        for indices in combinations(range(1, n + 1), size):
            for signs in product((-1, 1), repeat=size):
                result.append(tuple(i * sign for i, sign in zip(indices, signs)))
    return tuple(result)


def boundary_checks():
    raw = {
        "empty_formula_no_variables": [],
        "empty_clause": [[]],
        "empty_clause_after_tautology": [[1,-1], []],
        "tautology_only": [[1,-1,2]],
        "duplicate_unit": [[17,17,17]],
        "sparse_large_ids": [[10**30, -(10**60)], [10**60]],
        "tautology_with_contradiction": [[1,-1], [19], [-19]],
    }
    expected = {"empty_formula_no_variables":"fixed_yes", "empty_clause":"fixed_no",
                "empty_clause_after_tautology":"fixed_no", "tautology_only":"fixed_yes",
                "duplicate_unit":"main", "sparse_large_ids":"main", "tautology_with_contradiction":"main"}
    records = []
    for name, clauses in raw.items():
        route, n, dense = normalize(clauses)
        require(route == expected[name], "wrong preprocessing route")
        record = {"name":name,"route":route,"n_after_relabeling":n,"clauses_after_preprocessing":dense}
        if route != "main":
            N, edges, arcs, costs, K = fixed_instance(route == "fixed_yes")
            selected = next(all_trees(N, edges))
            F, _ = evaluate(N, selected, arcs, costs)
            require((F <= K) == (route == "fixed_yes"), "fixed yes/no encoding failed")
            require(evaluate(N, selected, arcs, reverse_costs(arcs,costs),inward=True)[0] == F,
                    "fixed case inward orientation failed")
            require(evaluate(N, selected, arcs, [[x+1 for x in row] for row in costs])[0] == F+2,
                    "fixed case positive shift failed")
            record.update(cost=F, threshold=K, N=N)
        else:
            require(n <= sum(len(c) for c in clauses), "sparse IDs expanded to huge vertex count")
        records.append(record)
    return records


def main():
    # Self-test makes optimized mode failure behavior checkable without assert.
    if "--self-test-failure" in sys.argv:
        require(False, "intentional explicit-exception self-test")
    start = datetime.now(timezone.utc).isoformat()
    totals = Counter()
    suite = []
    for n, max_m in ((1, 3), (2, 3), (3, 2)):
        universe = clause_universe(n)
        for m in range(1, max_m + 1):
            suite.extend((n, clauses) for clauses in combinations_with_replacement(universe, m))
    # Three-literal clauses, repeated occurrences across clauses, absent/unused variables.
    suite.extend((3, clauses) for clauses in (
        ((1,2,3), (-1,-2,-3), (1,-2,3)),
        ((1,), (-1,), (2,3)),
        ((1,2), (-1,2), (1,-2), (-1,-2)),
        ((1,), (-1,)),
    ))
    results = []
    for n, clauses in suite:
        for B in sorted({n+1, 2}):
            results.append(audit_formula(n, clauses, B, totals))
    # Boundary self-test deliberately checks that malformed input raises even under -O.
    try:
        normalize([[0]])
    except RuntimeError:
        malformed_rejected = True
    else:
        malformed_rejected = False
    require(malformed_rejected, "malformed zero literal did not raise")
    # Verify syntactically that no check relies on Python's removable assertions.
    source = Path(__file__).read_text()
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(source))),
            "checker must not rely on removable assertions")
    boundary = boundary_checks()
    for item in boundary:
        if item["route"] == "main":
            clauses = tuple(tuple(c) for c in item["clauses_after_preprocessing"])
            item["main_audit"] = audit_formula(item["n_after_relabeling"], clauses, item["n_after_relabeling"]+1, totals)
    # B=1 fails: y has no hub edge and both unit-clause roots miss the x attachment.
    n, clauses = 2, ((1,2), (2,), (-2,))
    N, edges, arcs, costs, K = construct(n, clauses, 1)
    witness = tuple(sorted((edge(0,1),edge(0,2),edge(4,2),edge(4,3),edge(5,3),edge(6,3))))
    require(is_tree(N,witness), "B=1 failure control is not a tree")
    F, contributions = evaluate(N,witness,arcs,costs)
    require(F == K == 5 and assignment_min_unsatisfied(n,clauses)[0] == 1, "B=1 control no longer falsifies decision")
    b1 = {"n":n,"clauses":clauses,"B":1,"K":K,"cost":F,"root_contributions":contributions,
          "tree":labels(n,witness),"min_unsatisfied":1,"purpose":"falsifies extension B=1, not original theorem"}
    # Exact original B: all-tree OPT need not equal K+minimum-unsatisfied.
    clauses = ((1,2),) + ((2,),)*3 + ((-2,),)*3
    opt_control = audit_formula(2, clauses, 3, totals)
    require(opt_control["minimum"] < opt_control["structured_minimum"], "global optimum control did not separate")
    result = {"started_utc":start,"completed_utc":datetime.now(timezone.utc).isoformat(),
              "python_version":sys.version,"optimized_mode":bool(sys.flags.optimize),
              "uses_explicit_exceptions_not_asserts":True,
              "all_checks_passed":True,"original_checker_or_review_used":False,
              "finite_support_only":True,"totals":dict(totals),"distinct_base_formula_cases":len(suite),
              "boundary_cases":boundary,"B1_counterexample":b1,"nonclaimed_global_optimum_counterexample":opt_control,
              "per_formula_summary":results,
              "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output = Path(__file__).with_name("independent_results_optimized.json" if sys.flags.optimize else "independent_results.json")
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({key:result[key] for key in ("started_utc","completed_utc","optimized_mode","all_checks_passed","totals","distinct_base_formula_cases")},indent=2))


if __name__ == "__main__":
    main()
