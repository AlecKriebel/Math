#!/usr/bin/env python3
"""Exact independent diagnostics for PR31's adaptive capped exploration.

No author/reviewer module is imported. Transcript branching only generates
primitive variables actually read; untouched reservoir slots are integrated
analytically. Finite controls do not establish an infinite-volume theorem.
"""
from collections import Counter, defaultdict, deque
from datetime import datetime, timezone
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
CHECKS = Counter()


def check(condition, family):
    CHECKS[family] += 1
    if not condition:
        raise AssertionError(family)


def edge(a, b):
    return tuple(sorted((a, b)))


def finite_model(base_edges, heights):
    base = tuple(sorted(edge(*e) for e in base_edges))
    nodes = sorted({u for e in base for u in e})
    vertices = [(u, h) for u in nodes for h in heights]
    physical = set()
    for u, h in vertices:
        if h + 1 in heights:
            physical.add(edge((u, h), (u, h + 1)))
    for u, v in base:
        for h in heights:
            physical.add(edge((u, h), (v, h)))
    physical = tuple(sorted(physical))
    adjacency = {u: [] for u in vertices}
    for a, b in physical:
        adjacency[a].append(b)
        adjacency[b].append(a)
    for neighbors in adjacency.values():
        neighbors.sort()
    return base, physical, adjacency


def explore(adjacency, cap, reader, root, reverse=False, cache=True):
    accepted = {root}
    counts = Counter({root[0]: 1})
    queue = deque([root])
    states = {}
    trace = []
    uses = Counter()
    rejections = []
    while queue:
        u = queue.popleft()
        neighbors = adjacency[u][::-1] if reverse else adjacency[u]
        for v in neighbors:
            physical = edge(u, v)
            if cache and physical in states:
                continue
            primitive = ("vertical", physical)
            if u[0] != v[0]:
                base = edge(u[0], v[0])
                primitive = ("horizontal", base, uses[base])
                uses[base] += 1
            state, actual_primitive = reader(physical, primitive)
            states[physical] = state
            trace.append((physical, actual_primitive, state))
            if state and v not in accepted:
                if counts[v[0]] < cap:
                    accepted.add(v)
                    counts[v[0]] += 1
                    queue.append(v)
                else:
                    rejections.append((physical, v))
    return {
        "accepted": tuple(sorted(accepted)), "states": states,
        "trace": trace, "uses": uses, "rejections": rejections,
        "counts": counts,
    }


class NeedBit(Exception):
    def __init__(self, primitive):
        self.primitive = primitive


def transcript_leaves(adjacency, cap, root, reverse=False, mutant=None):
    """Exhaust query transcript tree, including adaptive variable labels."""
    stack = [{}]
    while stack:
        assignment = stack.pop()

        def reader(physical, requested):
            primitive = requested
            if mutant == "reuse_first_horizontal_slot" and requested[0] == "horizontal":
                primitive = requested[:2] + (0,)
            if mutant == "share_pool_across_base_edges" and requested[0] == "horizontal":
                primitive = ("global_horizontal", requested[2])
            if primitive not in assignment:
                raise NeedBit(primitive)
            return assignment[primitive], primitive

        try:
            out = explore(adjacency, cap, reader, root, reverse=reverse)
        except NeedBit as missing:
            for bit in (0, 1):
                child = dict(assignment)
                child[missing.primitive] = bit
                stack.append(child)
            continue
        yield assignment, out


def bernoulli_mass(ones, length, p):
    return p ** ones * (1 - p) ** (length - ones)


def direct_distribution(physical, adjacency, cap, root, p, reverse=False):
    law = defaultdict(Fraction)
    cap_preserving = 0
    rejection_cases = 0
    for bits in product((0, 1), repeat=len(physical)):
        states = dict(zip(physical, bits))
        reader = lambda e, label: (states[e], ("physical", e))
        out = explore(adjacency, cap, reader, root, reverse=reverse)
        law[out["accepted"]] += bernoulli_mass(sum(bits), len(bits), p)
        check(len(set(t[0] for t in out["trace"])) == len(out["trace"]), "direct_physical_injectivity")
        check(all(n <= cap for n in out["counts"].values()), "direct_cap")
        check(all(n <= 2 * cap for n in out["uses"].values()), "direct_2M")
        if cap == 1:
            check(all(n <= 1 for n in out["uses"].values()), "M1_sharper_bound")
        full = explore(adjacency, len(adjacency), reader, root, reverse=reverse)
        full_counts = Counter(u for u, h in full["accepted"])
        if all(n <= cap for n in full_counts.values()):
            check(out["accepted"] == full["accepted"], "cap_never_binds_when_actual_cluster_fits")
            cap_preserving += 1
        rejection_cases += bool(out["rejections"])
    check(sum(law.values()) == 1, "direct_mass")
    return law, cap_preserving, rejection_cases


def reservoir_distribution(base, physical, adjacency, cap, root, p, reverse=False,
                           mutant=None, close_unqueried=False, check_invariants=True):
    accepted_law = defaultdict(Fraction)
    completed_law = defaultdict(Fraction)
    joint_y = defaultdict(Fraction)
    leaves = 0
    duplicated_primitive_witness = None
    for assignment, out in transcript_leaves(adjacency, cap, root, reverse, mutant):
        leaves += 1
        mass = bernoulli_mass(sum(assignment.values()), len(assignment), p)
        accepted_law[out["accepted"]] += mass
        primitive_labels = [t[1] for t in out["trace"]]
        if len(set(primitive_labels)) < len(primitive_labels) and duplicated_primitive_witness is None:
            duplicated_primitive_witness = out["trace"]
        if check_invariants:
            check(len(set(primitive_labels)) == len(primitive_labels), "reservoir_primitive_injectivity")
            check(len(set(t[0] for t in out["trace"])) == len(out["trace"]), "reservoir_physical_injectivity")
            check(all(n <= 2 * cap for n in out["uses"].values()), "reservoir_2M")

        # Conditional Y law integrates unused slots. All base pools are disjoint.
        conditional_q = []
        for e in base:
            used = [v for key, v in assignment.items() if key[0] == "horizontal" and key[1] == e]
            conditional_q.append(Fraction(1) if any(used) else 1 - (1 - p) ** (2 * cap - len(used)))
        shared_used = [v for key, v in assignment.items() if key[0] == "global_horizontal"]
        shared_q = Fraction(1) if any(shared_used) else 1 - (1 - p) ** (2 * cap - len(shared_used))
        for y in product((0, 1), repeat=len(base)):
            y_mass = mass
            if mutant == "share_pool_across_base_edges":
                y_mass *= shared_q if all(y) else (1 - shared_q if not any(y) else 0)
            else:
                for bit, q in zip(y, conditional_q):
                    y_mass *= q if bit else 1 - q
            joint_y[y] += y_mass
            if check_invariants and y_mass:
                reachable = {root[0]}
                changed = True
                while changed:
                    changed = False
                    for e, bit in zip(base, y):
                        if bit and reachable.intersection(e) and not set(e) <= reachable:
                            reachable.update(e)
                            changed = True
                check(all(u in reachable for u, h in out["accepted"]), "projection_domination")

        unseen = [e for e in physical if e not in out["states"]]
        tails = [tuple(0 for e in unseen)] if close_unqueried else product((0, 1), repeat=len(unseen))
        for tail in tails:
            full = dict(out["states"])
            full.update(zip(unseen, tail))
            key = tuple(full[e] for e in physical)
            tail_mass = Fraction(1) if close_unqueried else bernoulli_mass(sum(tail), len(tail), p)
            completed_law[key] += mass * tail_mass
    if check_invariants:
        check(sum(accepted_law.values()) == 1, "reservoir_mass")
        check(sum(completed_law.values()) == 1, "completion_mass")
        check(sum(joint_y.values()) == 1, "joint_Y_mass")
        q = 1 - (1 - p) ** (2 * cap)
        for y, mass in joint_y.items():
            check(mass == bernoulli_mass(sum(y), len(y), q), "joint_Y_exact_product_law")
    return accepted_law, completed_law, joint_y, leaves, duplicated_primitive_witness


def full_law_mismatches(physical, law, p):
    mismatch_count = 0
    witness = None
    for bits in product((0, 1), repeat=len(physical)):
        expected = bernoulli_mass(sum(bits), len(bits), p)
        actual = law.get(bits, Fraction(0))
        if actual != expected:
            mismatch_count += 1
            if witness is None:
                witness = {"physical_edges": physical, "bits": bits,
                           "actual": str(actual), "expected": str(expected)}
    return mismatch_count, witness


def sharp_bound_controls():
    controls = []
    for cap in range(2, 9):
        base, physical, adjacency = finite_model([(0, 1), (1, 2), (2, 3), (0, 3), (0, 4)],
                                                  tuple(range(-1, 4 * cap - 2)))
        starts = [0, cap - 1, 2 * cap - 2, 3 * cap - 3]
        opened = set()
        for u, start in enumerate(starts):
            for h in range(start, start + cap - 1):
                opened.add(edge((u, h), (u, h + 1)))
        for u in range(3):
            h = starts[u + 1]
            opened.add(edge((u, h), (u + 1, h)))
        out = explore(adjacency, cap, lambda e, label: (int(e in opened), ("physical", e)), (0, 0))
        check(out["uses"][(0, 3)] == 2 * cap, "sharp_2M_family")
        check(out["counts"] == Counter({u: cap for u in range(4)}), "sharp_accepted_fibers")
        heights = {u: [h for v, h in out["accepted"] if v == u] for u in range(4)}
        check(not set(heights[0]).intersection(heights[3]), "sharp_disjoint_endpoint_heights")
        controls.append({"cap": cap, "base_edge": [0, 3], "query_count": out["uses"][(0, 3)],
                         "accepted_heights": heights, "open_physical_edges": sorted(opened),
                         "embedding": "four-cycle with an infinite ray attached at 0; boundary vertical queries closed"})
    return controls


def unbounded_degree_prefix(process_limit):
    """Lazy infinite locally finite graph: ray spine n with n pendant leaves."""
    def base_neighbors(v):
        kind, n, k = v
        if kind == 1:
            return [(0, n, 0)]
        ans = [(0, n + 1, 0)]
        if n:
            ans.append((0, n - 1, 0))
        ans.extend((1, n, k) for k in range(n))
        return sorted(ans)

    root = ((0, 0, 0), 0)
    accepted = {root}
    queue = deque([root])
    queried = set()
    uses = Counter()
    max_degree = 0
    processed = []
    while queue and len(processed) < process_limit:
        u = queue.popleft()
        processed.append(u)
        neighbors = [(u[0], u[1] - 1), (u[0], u[1] + 1)]
        neighbors.extend((v, u[1]) for v in base_neighbors(u[0]))
        max_degree = max(max_degree, len(neighbors))
        for v in sorted(neighbors):
            e = edge(u, v)
            if e in queried:
                continue
            queried.add(e)
            if u[0] != v[0]:
                uses[edge(u[0], v[0])] += 1
                if v not in accepted:
                    accepted.add(v)
                    queue.append(v)
            # All edges open, but M=1 rejects every vertical proposal.
        check(all(n <= 1 for n in uses.values()), "unbounded_degree_prefix_2M")
    check(len(processed) == process_limit, "unbounded_degree_prefix_fair_steps")
    check(len(set(processed)) == len(processed), "unbounded_degree_prefix_no_vertex_reprocess")
    return {"processed_vertices": len(processed), "accepted_vertices": len(accepted),
            "queued_vertices": len(queue), "largest_product_degree_seen": max_degree,
            "furthest_processed_spine": max(v[0][1] for v in processed if v[0][0] == 0),
            "interpretation": "deterministic prefix only; all-open state at p<1 is not claimed probabilistically"}


def main():
    report = {"started_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
              "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "exact_tests": [], "mutants": [], "scope": "finite diagnostic controls; universal proof is separate"}
    specifications = [
        ("four-cycle x height interval of length 2", [(0, 1), (1, 2), (2, 3), (0, 3)], (0, 1),
         (1, 2), ((0, 0), (3, 1)), (False, True), (Fraction(2, 7),)),
        ("triangle x height interval of length 3", [(0, 1), (1, 2), (0, 2)], (-1, 0, 1),
         (2,), ((0, 0),), (False, True), (Fraction(3, 5),)),
    ]
    for name, base_edges, heights, caps, roots, orders, parameters in specifications:
        base, physical, adjacency = finite_model(base_edges, heights)
        for cap, root, reverse, p in product(caps, roots, orders, parameters):
            actual, preserving, rejecting = direct_distribution(physical, adjacency, cap, root, p, reverse)
            accepted, completed, joint_y, leaves, _ = reservoir_distribution(base, physical, adjacency, cap, root, p, reverse)
            check(dict(actual) == dict(accepted), "exact_accepted_law")
            mismatches, witness = full_law_mismatches(physical, completed, p)
            check(mismatches == 0, "exact_completed_product_law")
            report["exact_tests"].append({"geometry": name, "cap": cap, "root": root,
                                          "reverse_neighbor_order": reverse, "p": str(p),
                                          "physical_edges": len(physical), "direct_configurations": 2 ** len(physical),
                                          "adaptive_transcript_leaves": leaves, "cap_preserving_configurations": preserving,
                                          "cap_rejection_configurations": rejecting, "full_law_mismatches": mismatches,
                                          "Y_joint_atoms": len(joint_y), "accepted_atoms": len(actual)})
            print(json.dumps(report["exact_tests"][-1]), flush=True)

    base, physical, adjacency = finite_model([(0, 1), (1, 2), (2, 3), (0, 3)], (0, 1))
    p = Fraction(2, 7)
    for name, mutant, close_unqueried in [
        ("reuse_first_horizontal_slot", "reuse_first_horizontal_slot", False),
        ("share_pool_across_base_edges", "share_pool_across_base_edges", False),
        ("force_unqueried_physical_edges_closed", None, True),
    ]:
        _, completed, yy, leaves, duplicate = reservoir_distribution(base, physical, adjacency, 2, (0, 0), p,
                                                                    mutant=mutant, close_unqueried=close_unqueried,
                                                                    check_invariants=False)
        mismatches, witness = full_law_mismatches(physical, completed, p)
        check(mismatches > 0, "mutation_detection")
        report["mutants"].append({"mutation": name, "detected": True, "full_law_mismatches": mismatches,
                                 "first_witness": witness, "primitive_alias_trace": duplicate,
                                 "adaptive_transcript_leaves": leaves})
        if mutant == "share_pool_across_base_edges":
            q = 1 - (1 - p) ** 4
            shared_atom = yy[(1,) * len(base)]
            expected = q ** len(base)
            check(shared_atom != expected, "mutation_detection")
            report["mutants"][-1]["joint_Y_all_open_actual"] = str(shared_atom)
            report["mutants"][-1]["joint_Y_all_open_independent_expected"] = str(expected)

    # A missing physical query cache gives two distinct trials to the same edge.
    seen_by_reader = Counter()

    def conflicting_requery_reader(e, label):
        ordinal = seen_by_reader[e]
        seen_by_reader[e] += 1
        return int(ordinal == 0), ("fresh_requery", e, ordinal)

    requery = explore(adjacency, 2, conflicting_requery_reader, (0, 0), cache=False)
    counts = Counter(t[0] for t in requery["trace"])
    repeated = [(e, n) for e, n in counts.items() if n > 1]
    check(bool(repeated), "mutation_detection")
    report["mutants"].append({"mutation": "remove_physical_edge_query_cache", "detected": True,
                             "repeated_physical_edges": repeated,
                             "conflicting_trace": requery["trace"],
                             "note": "The numerical 2M attempt bound can survive; product-edge state consistency fails."})

    # Indexing pools by orientation but defining Y with only one orientation is invalid.
    _, _, directed_adjacency = finite_model([(0, 1)], (0, 1))
    reverse_pool = (1, 0)

    def directed_reader(e, label):
        if label[0] == "vertical":
            return 0, label
        return reverse_pool[label[2]], ("directed_horizontal", (1, 0), label[2])

    directed_out = explore(directed_adjacency, 1, directed_reader, (1, 0))
    directed_witness = {"base_edge": [0, 1], "root": [1, 0], "forward_pool": [0, 0],
                        "reverse_pool": reverse_pool,
                        "accepted_base_vertices": sorted({u for u, h in directed_out["accepted"]}),
                        "forward_Y": 0, "executed_trace": directed_out["trace"]}
    check(directed_witness["forward_Y"] == 0 and 0 in directed_witness["accepted_base_vertices"], "mutation_detection")
    report["mutants"].append({"mutation": "orientation_pools_but_forward_only_Y", "detected": True,
                             "first_witness": directed_witness})

    # Conditioning on the global cap event destroys the original edge law.
    conditioned_mass = Fraction(0)
    conditioned_vertical_open = Fraction(0)
    root_vertical = edge((0, 0), (0, 1))
    for bits in product((0, 1), repeat=len(physical)):
        states = dict(zip(physical, bits))
        out = explore(adjacency, len(adjacency), lambda e, label: (states[e], ("physical", e)), (0, 0))
        if all(n <= 1 for n in Counter(u for u, h in out["accepted"]).values()):
            mass = bernoulli_mass(sum(bits), len(bits), p)
            conditioned_mass += mass
            conditioned_vertical_open += mass * states[root_vertical]
    check(conditioned_mass > 0 and conditioned_vertical_open == 0, "conditioning_counterexample")
    report["mutants"].append({"mutation": "condition_product_law_on_actual_root_cluster_fiber_cap_1", "detected": True,
                             "conditioning_event_probability": str(conditioned_mass),
                             "conditional_root_vertical_open_probability": str(conditioned_vertical_open / conditioned_mass),
                             "unconditional_probability": str(p)})

    report["sharp_2M_controls"] = sharp_bound_controls()
    budget_witnesses = []
    for control in report["sharp_2M_controls"]:
        cap = control["cap"]
        _, _, adjacency_for_budget = finite_model([(0, 1), (1, 2), (2, 3), (0, 3), (0, 4)],
                                                  tuple(range(-1, 4 * cap - 2)))
        opened = {tuple(tuple(v) for v in e) for e in control["open_physical_edges"]}
        attempted = []

        def short_budget_reader(e, label):
            attempted.append((e, label))
            if label[0] == "horizontal" and label[2] >= 2 * cap - 1:
                raise IndexError((e, label, "reservoir length 2M-1 exhausted"))
            return int(e in opened), label

        try:
            explore(adjacency_for_budget, cap, short_budget_reader, (0, 0))
        except IndexError as failure:
            check(True, "mutation_detection")
            budget_witnesses.append({"cap": cap, "error": repr(failure), "last_attempt": attempted[-1]})
        else:
            raise AssertionError("short reservoir failed to be detected")
    report["mutants"].append({"mutation": "reduce_reservoir_length_to_2M_minus_1", "detected": True,
                             "witness_caps": list(range(2, 9)),
                             "required_queries": [2 * cap for cap in range(2, 9)],
                             "executed_budget_failures": budget_witnesses})
    report["unbounded_degree_prefix_controls"] = [unbounded_degree_prefix(n) for n in (100, 1000, 5000)]
    for p in (Fraction(0), Fraction(1), Fraction(2, 7), Fraction(99, 100)):
        for cap in (1, 2, 100):
            q = 1 - (1 - p) ** (2 * cap)
            check((q < 1) == (p < 1), "endpoint_q_exact")
    report["checks_by_family"] = dict(CHECKS)
    report["total_checks"] = sum(CHECKS.values())
    report["all_passed"] = True
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    (HERE / "INDEPENDENT_CONTROLS_RECEIPT.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"all_passed": True, "checks": report["total_checks"],
                      "exact_tests": len(report["exact_tests"]), "mutants_detected": len(report["mutants"])}), flush=True)


if __name__ == "__main__":
    main()
