#!/usr/bin/env python3
"""Finite diagnostics only. This does not decide the 3-manifold problem."""
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math
import sys

class Rejected(Exception):
    pass

def require(value, message):
    if not value:
        raise Rejected(message)

def unique_object(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, "duplicate JSON key")
        result[k] = v
    return result

def reject_constant(value):
    raise Rejected("nonfinite JSON constant")

def read_json(path):
    require(path.is_file() and not path.is_symlink(), "JSON file type")
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)

def determinant(matrix):
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    require(all(len(row) == n for row in a), "square matrix")
    value = F(1)
    for j in range(n):
        k = next((k for k in range(j, n) if a[k][j]), None)
        if k is None:
            return F(0)
        if k != j:
            a[k], a[j] = a[j], a[k]
            value = -value
        pivot = a[j][j]
        value *= pivot
        for i in range(j + 1, n):
            ratio = a[i][j] / pivot
            if ratio:
                for h in range(j + 1, n):
                    a[i][h] -= ratio * a[j][h]
            a[i][j] = F(0)
    return value

def return_path(n, edges, source, target):
    adj = [[] for _ in range(n)]
    for k, (u, v) in enumerate(edges):
        adj[u].append((v, k))
    prev = {source: None}
    q = deque([source])
    while q:
        u = q.popleft()
        if u == target:
            path = []
            while prev[u] is not None:
                old, edge = prev[u]
                path.append(edge)
                u = old
            return path[::-1], set(prev)
        for v, k in adj[u]:
            if v not in prev:
                prev[v] = (u, k)
                q.append(v)
    return None, set(prev)

def graph_controls():
    cases = positive = cut = 0
    for n in range(1, 5):
        universe = [(u, v) for u in range(n) for v in range(n) if u != v]
        for mask in range(1 << len(universe)):
            edges = [e for j, e in enumerate(universe) if mask & (1 << j)]
            reach = [[u == v or (u, v) in edges for v in range(n)] for u in range(n)]
            for k in range(n):
                for u in range(n):
                    for v in range(n):
                        reach[u][v] = reach[u][v] or (reach[u][k] and reach[k][v])
            expected = all(reach[v][u] for u, v in edges)
            weights = [0] * len(edges)
            successful = True
            for j, (u, v) in enumerate(edges):
                path, reached = return_path(n, edges, v, u)
                if path is None:
                    require(u not in reached and v in reached, "cut endpoints")
                    require(not any(a in reached and b not in reached for a, b in edges),
                            "reachable cut has an outgoing edge")
                    successful = False
                    break
                weights[j] += 1
                for k in path:
                    weights[k] += 1
            require(successful == expected, "cycle predicate disagrees")
            if successful:
                require(all(w > 0 for w in weights), "nonpositive circulation")
                for u in range(n):
                    incoming = sum(w for w, (_, b) in zip(weights, edges) if b == u)
                    outgoing = sum(w for w, (a, _) in zip(weights, edges) if a == u)
                    require(incoming == outgoing, "unbalanced circulation")
                positive += 1
            else:
                cut += 1
            cases += 1
    return {"cases": cases, "positive_circulations": positive, "cut_obstructions": cut}

def run():
    require(len(sys.argv) == 1, "no command-line arguments accepted")
    root = Path(__file__).resolve().parent
    claims = read_json(root / "CLAIMS.json")
    require(claims["schema"] == "transverse-surgery-claims-v1", "claims schema")
    require(type(claims["problem_id"]) is int and claims["problem_id"] == 10300034,
            "problem identity")
    require(claims["disposition"] == "unsolved" and type(claims["approaches"]) is int
            and claims["approaches"] == 5, "disposition")
    require(claims["full_solution"] is False and claims["novelty_claim"] is False
            and claims["formal_proof"] is False, "claim inflation")
    ledger = read_json(root / "APPROACH_LEDGER.json")
    require(ledger["schema"] == "transverse-surgery-approach-ledger-v1", "ledger schema")
    require(type(ledger["count"]) is int and ledger["count"] == 5, "ledger count")
    require([x["turn"] for x in ledger["approaches"]] == [1, 2, 3, 4, 5], "turn list")
    require(len({x["approach"] for x in ledger["approaches"]}) == 5, "distinct routes")

    basis_cases = 0
    for g in range(1, 33):
        n = 2 * g + 1
        matrix = [[0] * n for _ in range(n)]
        matrix[0][0] = 1
        for j in range(1, n):
            matrix[0][j] = matrix[j][j] = 1
        require(determinant(matrix) == 1, "positive section basis determinant")
        basis_cases += 1

    slope_cases = 0
    for p, q in product(range(-20, 21), repeat=2):
        if math.gcd(p, q) != 1:
            continue
        for degree in range(1, 21):
            require((q * degree == 0) == (q == 0 and abs(p) == 1), "slope extension")
            slope_cases += 1

    contact_cases = 0
    for r in map(F, range(-10, 11)):
        c, s = (1 - r * r) / (1 + r * r), 2 * r / (1 + r * r)
        require(c * c + s * s == 1, "rational circle")
        for k in range(1, 21):
            eps = F(1, k)
            # Coefficient after factoring out the positive angular speed 2*pi.
            coefficient = (eps * c) * (-eps * c) - (eps * s) * (eps * s)
            require(coefficient == -eps * eps and coefficient < 0, "contact wedge")
            require(eps > 0 and F(0) == 0, "fixed knot evaluations")
            contact_cases += 1

    margin_cases = 0
    for c, error in product(range(1, 21), repeat=2):
        c, error = F(c, 20), F(error, 20)
        require((c - error > 0) == (c > error), "strict margin criterion")
        margin_cases += 1

    graph = graph_controls()
    return {"schema": "transverse-surgery-diagnostics-v1", "status": "pass",
            "problem_id": 10300034, "section_basis_cases": basis_cases,
            "primitive_slope_degree_cases": slope_cases, "contact_rational_cases": contact_cases,
            "strict_margin_cases": margin_cases, "directed_graphs": graph,
            "scope": "finite diagnostics; not a topological or universal-existence proof"}

if __name__ == "__main__":
    try:
        print(json.dumps(run(), sort_keys=True, separators=(",", ":")))
    except (Rejected, OSError, ValueError, TypeError, KeyError) as exc:
        print("REJECT: " + str(exc), file=sys.stderr)
        sys.exit(1)
