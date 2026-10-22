"""Recheck the finite overlap comparison, not an all-list or priority theorem.

Run from any directory: python3 check_fiala_comparison.py
Input is the auditor's transcription of Fiala--Skrekovski Fig. 4 (printed p.14).
The source PDF/figure must be inspected separately to validate that transcription.
No source-author code or third-party Python package is needed.
"""
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def constraints(vertices, edges):
    adjacent = {v: set() for v in vertices}
    for u, v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    needed = {v: {} for v in vertices}
    for v in vertices:
        for w in adjacent[v]:
            needed[v][w] = 2
        for w in adjacent[v]:
            for u in adjacent[w]:
                if u != v:
                    needed[v][u] = max(needed[v].get(u, 0), 1)
    return needed


def witness_valid(vertices, edges, lists, witness):
    if set(witness) != set(vertices):
        return False
    if any(witness[v] not in lists[v] for v in vertices):
        return False
    needed = constraints(vertices, edges)
    return all(abs(witness[v] - witness[w]) >= gap
               for v in vertices for w, gap in needed[v].items())


def feasible(vertices, edges, lists):
    needed = constraints(vertices, edges)
    chosen = {}

    def search():
        if len(chosen) == len(vertices):
            return dict(chosen)
        candidates = {}
        for v in vertices:
            if v not in chosen:
                candidates[v] = [x for x in lists[v]
                                 if all(abs(x - chosen[w]) >= gap
                                        for w, gap in needed[v].items() if w in chosen)]
        v = min(candidates, key=lambda x: (len(candidates[x]), -len(needed[x]), x))
        for x in candidates[v]:
            chosen[v] = x
            result = search()
            if result is not None:
                return result
            del chosen[v]
        return None

    return search()


def connected(vertices, edges):
    neighbours = {v: set() for v in vertices}
    for u, v in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)
    found = {vertices[0]}
    stack = list(found)
    while stack:
        v = stack.pop()
        for w in neighbours[v] - found:
            found.add(w)
            stack.append(w)
    return len(found) == len(vertices)


def edge_key(edges):
    return tuple(sorted(tuple(sorted(e)) for e in edges))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    data = json.loads((ROOT / "FIALA_PREPRINT_COMPARISON.json").read_text())
    vertices, edges, lists = data["vertex_names"], data["edges"], data["lists"]
    require(len(vertices) == 10 and len(edges) == 12, "Wrong graph size")
    require(connected(vertices, edges), "Source graph disconnected")
    require(len(edges) - len(vertices) + 1 == 3, "Wrong cycle rank")
    require(all(len(set(lists[v])) == 5 for v in vertices), "Lists must have five elements")
    require(feasible(vertices, edges, lists) is None, "Displayed source assignment is feasible")
    interval = {v: list(range(1, 6)) for v in vertices}
    require(witness_valid(vertices, edges, interval, data["source_ordinary_witness"]),
            "Source ordinary witness invalid")
    require(feasible(vertices, edges, {v: list(range(1, 5)) for v in vertices}) is None,
            "Ordinary four-label lower bound fails")
    expected = {edge_key(es) for es in itertools.combinations(edges, len(vertices) - 1)
                if connected(vertices, es)}
    reported = data["spanning_tree_witnesses"]
    observed = {edge_key(item["edges"]) for item in reported}
    require(len(expected) == 66, "Wrong spanning tree count")
    require(len(reported) == 66 and observed == expected, "Incomplete or duplicate tree witnesses")
    for item in reported:
        require(witness_valid(vertices, item["edges"], lists, item["witness"]),
                "Invalid displayed-list witness for spanning tree")
    result = {"status": "pass", "source_graph_order": len(vertices),
              "source_graph_size": len(edges), "source_graph_cycle_rank": 3,
              "source_ordinary_palette_size": 5, "source_bad_five_lists": True,
              "spanning_trees_checked": 66, "all_displayed_list_restrictions_feasible": True,
              "limit": "Only this transcribed graph and these displayed lists are checked; no priority clearance or all-list theorem follows."}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
