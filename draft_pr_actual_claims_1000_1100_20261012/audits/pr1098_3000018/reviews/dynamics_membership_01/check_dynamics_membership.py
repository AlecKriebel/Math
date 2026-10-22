#!/usr/bin/env python3
"""Independent exact finite controls. No candidate program or asserts are used."""
import collections
import itertools
import json
import math
import platform
import random
import sys
from pathlib import Path


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def compositions(total, n):
    if n == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, n - 1):
                yield (first,) + rest


def strongly_connected(adj):
    n = len(adj)
    for start in range(n):
        seen = {start}
        pending = [start]
        while pending:
            u = pending.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    pending.append(v)
        if len(seen) != n:
            return False
    return True


def valid_graph(adj, oriented=False):
    n = len(adj)
    return (n >= 2 and all(len(row) == len(set(row)) and u not in row
            and all(type(v) is int and 0 <= v < n for v in row)
            for u, row in enumerate(adj)) and strongly_connected(adj)
            and (not oriented or all(u not in adj[v]
                                    for u, row in enumerate(adj) for v in row)))


def fire(adj, x, u):
    need(x[u] >= len(adj[u]), "illegal firing")
    y = list(x)
    y[u] -= len(adj[u])
    for v in adj[u]:
        y[v] += 1
    need(min(y) >= 0 and sum(y) == sum(x), "conservation or nonnegativity")
    return tuple(y)


def stable(adj, x):
    return all(0 <= x[u] < len(adj[u]) for u in range(len(adj)))


def balance(adj, x, f):
    z = [x[u] - len(adj[u]) * f[u] for u in range(len(adj))]
    for u, row in enumerate(adj):
        for v in row:
            z[v] += f[u]
    return tuple(z)


def certificate(adj, x, f):
    return (len(f) == len(adj) and all(type(a) is int and a >= 0 for a in f)
            and stable(adj, balance(adj, x, f)))


def trees(adj):
    n = len(adj)
    counts = []
    for root in range(n):
        other = [v for v in range(n) if v != root]
        good = 0
        for chosen in itertools.product(*(adj[v] for v in other)):
            parent = dict(zip(other, chosen))
            ok = True
            for u in other:
                visited = set()
                v = u
                while v != root:
                    if v in visited:
                        ok = False
                        break
                    visited.add(v)
                    v = parent[v]
                if not ok:
                    break
            good += int(ok)
        counts.append(good)
    gcd = math.gcd(*counts)
    need(gcd > 0, "missing rooted tree")
    pi = tuple(c // gcd for c in counts)
    need(balance(adj, (0,) * n, pi) == (0,) * n, "tree kernel orientation")
    need(max(pi) <= (n - 1) ** (n - 1), "tree bound")
    return pi, tuple(counts)


def all_states(adj, initial):
    """Explore every legal successor, detecting cycles without a firing cap."""
    seen = {initial: (0,) * len(adj)}
    edges = {}
    queue = collections.deque([initial])
    terminals = []
    while queue:
        x = queue.popleft()
        outgoing = []
        for u in range(len(adj)):
            if x[u] >= len(adj[u]):
                y = fire(adj, x, u)
                outgoing.append((u, y))
                f = list(seen[x])
                f[u] += 1
                f = tuple(f)
                if y not in seen:
                    seen[y] = f
                    queue.append(y)
        edges[x] = outgoing
        if not outgoing:
            terminals.append(x)
    indegree = {x: 0 for x in seen}
    for row in edges.values():
        for _, y in row:
            indegree[y] += 1
    q = collections.deque(x for x, degree in indegree.items() if degree == 0)
    removed = 0
    while q:
        x = q.popleft()
        removed += 1
        for _, y in edges[x]:
            indegree[y] -= 1
            if indegree[y] == 0:
                q.append(y)
    has_cycle = removed < len(seen)
    need(bool(terminals) != has_cycle, "halting dichotomy")
    need(len(terminals) <= 1, "unique stable configuration")
    if terminals:
        f = seen[terminals[0]]
        need(certificate(adj, initial, f), "actual odometer certificate")
        for x, word in seen.items():
            need(all(a <= b for a, b in zip(word, f)), "least action prefix")
            for u, y in edges[x]:
                extended = list(word)
                extended[u] += 1
                need(tuple(extended) == seen[y], "unique firing vector")
    return seen, edges, terminals, has_cycle


def run_schedule(adj, initial, policy, stabilizer=None, nonhalt_period=None):
    x = initial
    visited = {}
    f = [0] * len(adj)
    rng = random.Random(4317)
    for step in range(2000000):
        if nonhalt_period is not None and all(a >= b for a, b in zip(f, nonhalt_period)):
            # A nonzero positive kernel vector already fired in every coordinate
            # contradicts least action against every hypothetical stabilizer.
            need(balance(adj, (0,) * len(adj), nonhalt_period) == (0,) * len(adj),
                 "period-vector nonhalting witness")
            return False, tuple(f), step, 1
        if stabilizer is None and nonhalt_period is None:
            if x in visited:
                return False, tuple(f), step, step - visited[x]
            visited[x] = step
        choices = [u for u in range(len(adj)) if x[u] >= len(adj[u])]
        if not choices:
            need(certificate(adj, initial, tuple(f)), "schedule certificate")
            return True, tuple(f), step, 0
        if policy == "low":
            u = choices[0]
        elif policy == "high":
            u = choices[-1]
        else:
            u = rng.choice(choices)
        x = fire(adj, x, u)
        f[u] += 1
        if stabilizer is not None:
            need(all(a <= b for a, b in zip(f, stabilizer)), "all-schedule least action bound")
    raise RuntimeError("finite test budget exhausted; not a verdict")


def bank(q, allowed, wrong_sign=False):
    h = lambda k: int(k % q in allowed)
    sign = -1 if wrong_sign else 1
    copies = []
    for a in range(q):
        c = 1 + sign * (h(-a - 1) - h(-a))
        copies.extend([a] * c)
    need(len(copies) == q, "counter cardinality")
    return copies


def construct(banks, oriented=False, extra_root=0):
    Q = sum(q for q, _ in banks)
    P = max(q for q, _ in banks)
    returns = P if oriented else P - 1
    n = 1 + Q + returns
    adj = [[] for _ in range(n)]
    x = [0] * n
    data = []
    offset = 1
    B = 0
    for q, allowed in banks:
        vertices = []
        for a in bank(q, allowed):
            v = offset
            offset += 1
            vertices.append((v, a))
            adj[0].append(v)
            adj[v] = ([] if oriented else [0]) + list(range(1 + Q, 1 + Q + q - (0 if oriented else 1)))
            x[v] = a
        B += q * (q - 1) // 2 - len(allowed) + q
        data.append((q, allowed, vertices))
    for t in range(1 + Q, n):
        adj[t] = [0]
    S0 = sum(x)
    x[0] = Q + B - 1 - S0 + extra_root
    need(min(x) >= 0, "initial nonnegativity")
    need(valid_graph(adj, oriented), "reduction graph language")
    expected_n = Q + P + int(oriented)
    expected_e = Q + sum(q * q for q, _ in banks) + P - 1 + int(oriented)
    need(n == expected_n and sum(map(len, adj)) == expected_e, "exact graph size")
    need(all(v >= 1 + Q for u in range(1, 1 + Q) for v in adj[u] if v != 0), "root deletion depth")
    need(sum(x) == Q + B - 1 + extra_root, "total chip count")
    return adj, tuple(x), data, Q, B


def canonical(adj, initial, data, Q, B, extra_root=0):
    x = initial
    f = [0] * len(adj)
    period = math.lcm(*(q for q, _, _ in data))
    steps = 0
    for k in range(period + 1):
        S = 0
        simultaneous = True
        for q, allowed, vertices in data:
            for v, a in vertices:
                need(x[v] == (a + k) % q, "checkpoint counter residue")
                S += x[v]
            simultaneous = simultaneous and k % q in allowed
        need(all(x[t] == 0 for t in range(1 + Q, len(adj))), "checkpoint empty returns")
        need(x[0] == Q + B - 1 + extra_root - S, "checkpoint root balance")
        if extra_root == 0:
            need((x[0] < Q) == simultaneous, "checkpoint SAT equivalence")
        if x[0] < Q:
            need(stable(adj, x), "checkpoint stability")
            need(certificate(adj, initial, tuple(f)), "canonical certificate")
            return True, k, steps, tuple(f)
        if k == period:
            need(x == initial, "unsatisfiable full checkpoint lasso")
            return False, period, steps, tuple(f)
        x = fire(adj, x, 0)
        f[0] += 1
        steps += 1
        for v in range(1, 1 + Q):
            if x[v] >= len(adj[v]):
                x = fire(adj, x, v)
                f[v] += 1
                steps += 1
        for t in range(1 + Q, len(adj)):
            while x[t] >= len(adj[t]):
                x = fire(adj, x, t)
                f[t] += 1
                steps += 1
    raise RuntimeError("unreachable checkpoint branch")


def sat_banks(n, clauses):
    primes = [3, 5, 7, 11, 13]
    need(1 <= n <= len(primes), "test-only prime list")
    result = [(primes[i], {0, 1}) for i in range(n)]
    for clause in clauses:
        used = sorted(set(abs(a) - 1 for a in clause))
        need(clause and len(used) == len(clause) <= 3, "normalized test clause")
        modulus = math.prod(primes[i] for i in used)
        # Independent local enumeration of residues, not constructive CRT.
        allowed = set()
        for k in range(modulus):
            values = {i: k % primes[i] for i in used}
            if all(a in (0, 1) for a in values.values()) and any(
                    values[abs(a) - 1] == int(a > 0) for a in clause):
                allowed.add(k)
        result.append((modulus, allowed))
    truth = any(all(any(bits[abs(a) - 1] == int(a > 0) for a in clause)
                    for clause in clauses) for bits in itertools.product((0, 1), repeat=n))
    return result, truth


def main():
    result = {"runtime": {"python": platform.python_version(), "platform": platform.platform()},
              "claim": "exact finite controls, not a general proof"}
    bsets = positions = 0
    for q in range(2, 9):
        for mask in range(1, 1 << q):
            allowed = {a for a in range(q) if mask >> a & 1}
            copies = bank(q, allowed)
            K = q * (q - 1) // 2 - len(allowed)
            for k in range(-q, 2 * q):
                got = sum((a + k) % q for a in copies)
                need(got == K + q * int(k % q in allowed), "bank storage")
                positions += 1
            bsets += 1
    result["banks"] = {"nonempty_sets": bsets, "positions": positions, "moduli": [2, 8]}

    graphs = inputs = states = edges_count = halting = treechecks = boundchecks = 0
    synthetic = 0
    source_slack = None
    for n in range(2, 5):
        ordered = [(u, v) for u in range(n) for v in range(n) if u != v]
        for mask in range(1 << len(ordered)):
            adj = [[] for _ in range(n)]
            for i, (u, v) in enumerate(ordered):
                if mask >> i & 1:
                    adj[u].append(v)
            if not strongly_connected(adj):
                continue
            graphs += 1
            pi, treecounts = trees(adj)
            treechecks += n
            for C in range(4):
                for x in compositions(C, n):
                    seen, edges, terminals, cyclic = all_states(adj, x)
                    inputs += 1
                    states += len(seen)
                    edges_count += sum(map(len, edges.values()))
                    if terminals:
                        halting += 1
                        f = seen[terminals[0]]
                        need(any(a < b for a, b in zip(f, pi)), "odometer period reduction")
                        need(max(f) + 1 <= (n - 1) ** (2 * n - 2), "NP bit bound")
                        for u, row in enumerate(adj):
                            for v in row:
                                need(f[u] + 1 <= len(adj[v]) * (f[v] + 1), "additive path slack")
                                boundchecks += 1
                    need(bool(terminals) != cyclic, "finite all-schedule dichotomy")
            if n <= 3:
                stable_z = list(itertools.product(*(range(len(row)) for row in adj)))
                for proposed in itertools.product(range(3), repeat=n):
                    for z in stable_z:
                        x = balance(adj, z, tuple(-a for a in proposed))
                        if min(x) < 0:
                            continue
                        need(certificate(adj, x, proposed), "synthetic certificate soundness")
                        truth, actual, _, _ = run_schedule(adj, x, "low")
                        need(truth and all(a <= b for a, b in zip(actual, proposed)), "least action arbitrary stabilizer")
                        synthetic += 1
    adj = [[1], [0, 2], [0]]
    x = (1, 0, 0)
    f = (1, 0, 0)
    need(certificate(adj, x, f) and f[0] > len(adj[1]) * f[1], "source slack counterexample")
    source_slack = {"adjacency": adj, "initial": x, "legal_word": [0], "odometer": f,
                    "terminal": balance(adj, x, f), "printed_without_slack_false": "1 <= 2*0",
                    "candidate_with_slack_true": "1+1 <= 2*(0+1)"}
    result["all_simple_graphs"] = {"vertices": [2, 4], "strongly_connected_graphs": graphs,
                                  "configurations": inputs, "reachable_states": states,
                                  "legal_edges": edges_count, "halting": halting,
                                  "rooted_tree_coordinates": treechecks, "path_edge_checks": boundchecks,
                                  "arbitrary_stabilizing_certificates": synthetic}
    result["primary_printed_slack_counterexample"] = source_slack

    reductions = schedule_cases = individual_firings = checkpoint_roots = 0
    sat_cases = nonsat_cases = 0
    # Independent family: all pairs of nonempty predicates on one small modulus.
    bank_cases = []
    for q in (2, 3, 4):
        subsets = [{a for a in range(q) if mask >> a & 1} for mask in range(1, 1 << q)]
        for a in subsets:
            for b in subsets:
                bank_cases.append(([(q, a), (q, b)], bool(a & b), "predicate"))
    formula_cases = []
    units = [(1,), (-1,), (2,), (-2,), (3,), (-3,)]
    for mask in range(64):
        clauses = [c for i, c in enumerate(units) if mask >> i & 1]
        banks, truth = sat_banks(3, clauses)
        formula_cases.append((banks, truth, "sat"))
    extra = [[(1, 2, 3)], [(-1, -2, -3)], [(1, 2), (-1, 3), (-2, -3)],
             [(1,), (-1, 2, 3), (-2,), (-3,)],
             [tuple((i + 1) if bit else -(i + 1) for i, bit in enumerate(bits))
              for bits in itertools.product((0, 1), repeat=3)]]
    for clauses in extra:
        banks, truth = sat_banks(3, clauses)
        formula_cases.append((banks, truth, "sat"))
    for banks, truth, kind in bank_cases + formula_cases:
        for oriented in (False, True):
            adj, x, data, Q, B = construct(banks, oriented)
            need(sum(x) <= sum(map(len, adj)) - len(adj), "stable capacity consistency")
            got, roots, steps, odometer = canonical(adj, x, data, Q, B)
            need(got == truth, "canonical logical equivalence")
            individual_firings += steps
            checkpoint_roots += roots
            reductions += 1
            sat_cases += int(truth)
            nonsat_cases += int(not truth)
            # Exact deterministic noncanonical schedules on every bank case and
            # selected formula cases; complete repeated states certify lassos.
            if kind == "predicate" or (reductions % 16 == 0 and len(adj) <= 64):
                for policy in ("low", "high", "random"):
                    actual, f, steps, lasso = run_schedule(
                        adj, x, policy, stabilizer=odometer if truth else None,
                        nonhalt_period=odometer if not truth else None)
                    need(actual == truth, "noncanonical schedule logical equivalence")
                    if truth:
                        need(f == odometer, "order-independent odometer")
                    else:
                        need(lasso > 0, "explicit legal nonhalting period witness")
                    schedule_cases += 1
                    individual_firings += steps
    result["reductions"] = {"graph_cases": reductions, "satisfiable_predicates_or_formulas": sat_cases,
                            "unsatisfiable_predicates_or_formulas": nonsat_cases,
                            "noncanonical_schedules": schedule_cases, "individual_legal_firings": individual_firings,
                            "checkpoint_root_firings": checkpoint_roots,
                            "predicate_pairs": len(bank_cases), "three_variable_formula_cases": len(formula_cases)}

    # Exhaustive full-state exploration on reduction graphs distinct from the
    # arbitrary small-graph enumeration; both valid and inconsistent predicates.
    reduction_bfs_inputs = reduction_bfs_states = 0
    for allowed_a in ({0}, {1}, {0, 1}):
        for allowed_b in ({0}, {1}, {0, 1}):
            for oriented in (False, True):
                adj, x, _, _, _ = construct([(2, allowed_a), (2, allowed_b)], oriented)
                seen, _, terminals, _ = all_states(adj, x)
                need(bool(terminals) == bool(allowed_a & allowed_b), "reduction all-state SAT iff halting")
                reduction_bfs_inputs += 1
                reduction_bfs_states += len(seen)
    result["reduction_all_successors"] = {"inputs": reduction_bfs_inputs, "states": reduction_bfs_states}

    fault_results = []
    def rejected(name, operation):
        try:
            operation()
        except RuntimeError:
            fault_results.append({"name": name, "detected": True})
        else:
            raise RuntimeError("undetected deliberately damaged control: " + name)
    rejected("reversed multiplicity difference", lambda: need(
        all(sum((a + k) % 3 for a in bank(3, {0}, True)) == 2 + 3 * int(k % 3 == 0)
            for k in range(3)), "wrong sign"))
    adj, x, data, Q, B = construct([(3, {0})], extra_root=1)
    rejected("extra root chip removes a genuine YES", lambda: need(
        canonical(adj, x, data, Q, B, 1)[0], "SAT false negative"))
    rejected("parallel ordered pair", lambda: need(valid_graph([[1, 1], [0]]), "parallel edge"))
    rejected("invalid claimed stabilizing certificate", lambda: need(
        certificate([[1], [0]], (1, 0), (0, 0)), "bad certificate"))
    rejected("transpose tree kernel", lambda: need(
        all(len(adj[u]) * trees(adj)[0][u] == sum(trees(adj)[0][v] for v in adj[u])
            for u in range(len(adj))), "transpose"))
    rejected("omitted certificate additive slack", lambda: need(
        1 <= 2 * 0, "source inequality"))
    rejected("sink silently destroys a returned chip", lambda: need(
        sum((0, 0)) == sum((0, 1)), "dissipation"))
    result["fault_controls"] = fault_results

    # Complete fixed cases, malformed syntax and unused huge variable indices.
    fixed = []
    for oriented in (False, True):
        adj = [[1], [2], [0]] if oriented else [[1], [0]]
        for x, truth in (((0,) * len(adj), True), ((1,) + (0,) * (len(adj) - 1), False)):
            got, _, steps, lasso = run_schedule(adj, x, "high")
            need(valid_graph(adj, oriented) and got == truth, "fixed totality cases")
            fixed.append({"oriented": oriented, "chips": x, "halts": got, "steps": steps, "lasso": lasso})
    result["fixed_totality_cases"] = fixed
    result["representation_totality"] = {"malformed_rejects_to": "fixed NO",
                                        "empty_clause_to": "fixed NO", "empty_conjunction_to": "fixed YES",
                                        "huge_unused_declarations": "discard before choosing primes",
                                        "variable_names": "relabel distinct names occurring in literals"}
    return result


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test-invalid"]:
        need(False, "explicit optimized-runtime fault guard")
    need(len(sys.argv) == 2, "usage: check_dynamics_membership.py output.json")
    output = main()
    Path(sys.argv[1]).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))
