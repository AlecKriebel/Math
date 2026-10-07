"""Exact small-instance validation of the count-to-sample reduction.

Run from the project root: python3 code/test_sampling.py
This writes data/sampling_verification.json and does not test the upstream
FPRAS. Successful oracle responses and specified failures are synthetic.
"""

from __future__ import annotations

import json
import platform
import random
from fractions import Fraction
from itertools import combinations
from pathlib import Path

from gadget import exact_hafnian, expand_rational_matrix
from sampling import (
    Graph, Stats, exact_count_oracle, exact_matchings, exact_sampler_law,
    exact_witness, parameters, rounded_probabilities, sample_perfect_matching,
    total_variation, uniform_law,
)


def graph_from_mask(n: int, mask: int) -> Graph:
    pairs = list(combinations(range(n), 2))
    return Graph.make(range(n), (edge for i, edge in enumerate(pairs) if mask & (1 << i)))


def signed_multiplier(graph: Graph, neighbor: int, alpha: Fraction) -> Fraction:
    # Uses residual history and child index, so the perturbation is adaptive.
    sign = 1 if (sum(graph.vertices) + neighbor + len(graph.edges)) % 2 else -1
    return 1 + sign * alpha


def verify() -> dict:
    rng = random.Random(20261006)
    graphs = {Graph.make([], [])}
    for n in (2, 4):
        graphs.update(graph_from_mask(n, mask) for mask in range(1 << (n * (n - 1) // 2)))
    graphs.update(graph_from_mask(6, rng.getrandbits(15)) for _ in range(128))
    graphs.update(graph_from_mask(6, mask) for mask in (0, 1, (1 << 15) - 1))
    graphs.add(Graph.make(range(6), [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)]))
    graphs.add(Graph.make(range(6), [(0, 1), (2, 3), (4, 5)]))
    graphs.add(Graph.make(range(6), [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]))
    graphs.add(Graph.make(range(6), [(u, v) for u in range(3) for v in range(3, 6)]))
    graphs.add(Graph.make(range(8), combinations(range(8), 2)))
    graphs.add(Graph.make(range(8), [(0, 1), (2, 3), (4, 5), (6, 7)]))
    graphs = sorted(graphs, key=lambda graph: (len(graph.vertices), graph.edges))
    etas = (Fraction(1, 2), Fraction(1, 10), Fraction(1, 100))
    maximum = {scenario: (Fraction(0), None) for scenario in ("exact_estimates", "extremal_relative_errors", "errors_and_failures")}
    exact_laws = 0
    feasible_graphs = 0
    imperative_runs = 0
    fallback_runs = 0
    caps_observed = {"count_calls": 0, "witness_calls": 0, "decisions": 0, "random_bits": 0}
    for graph in graphs:
        reference = uniform_law(graph)
        if reference:
            feasible_graphs += 1
        for eta in etas:
            par = parameters(len(graph.vertices), eta)
            scenarios = (
                ("exact_estimates", None, Fraction(0)),
                ("extremal_relative_errors", signed_multiplier, Fraction(0)),
                ("errors_and_failures", signed_multiplier, par.call_failure),
            )
            for name, multiplier, failure in scenarios:
                law = exact_sampler_law(graph, eta, multiplier, failure)
                assert sum(law.values(), Fraction(0)) == (1 if reference else 0)
                assert set(law) <= set(reference)
                tv = total_variation(law, reference)
                assert tv <= eta
                if par.pairs:
                    theorem_bound = par.pairs * par.relative_error / (1 - par.relative_error) + par.call_cap * par.call_failure + Fraction(par.call_cap, 1 << par.bits_per_draw)
                    assert tv <= theorem_bound < eta
                ratio = tv / eta
                if ratio > maximum[name][0]:
                    maximum[name] = (ratio, {"vertices": list(graph.vertices), "edges": [list(edge) for edge in graph.edges], "eta": str(eta), "tv": str(tv)})
                exact_laws += 1
            # The executable sampler is compared with graph feasibility and
            # the per-execution call/bit caps, including deliberately failed
            # estimates. draw_bits uses exactly b independently generated bits.
            for fail_all in (False, True):
                stats = Stats()
                oracle = (lambda _g, _e, _d: Fraction(0)) if fail_all else exact_count_oracle
                result = sample_perfect_matching(graph, eta, oracle, exact_witness, rng.getrandbits, stats)
                assert (result is not None) == bool(reference)
                if result is not None:
                    assert result in reference
                assert stats.count_calls <= par.call_cap
                assert stats.witness_calls <= par.call_cap + 1
                assert stats.decisions <= par.pairs
                assert stats.random_bits <= par.pairs * par.bits_per_draw
                assert stats.bit_draws <= par.pairs
                fallback_runs += stats.witness_fallbacks
                imperative_runs += 1
                for name in caps_observed:
                    caps_observed[name] = max(caps_observed[name], getattr(stats, name))
    # A zero branch may never be revived by cumulative-floor rounding.
    rounded = rounded_probabilities((Fraction(1, 10**40), Fraction(0), Fraction(10**40)), 13)
    assert rounded[1] == 0 and sum(rounded) == 1
    # Empty instance, unique matching, no matching, and all-zero fallback.
    assert sample_perfect_matching(Graph.make([], []), Fraction(1, 10), exact_count_oracle, exact_witness, rng.getrandbits) == ()
    odd = Graph.make(range(3), [(0, 1), (1, 2), (0, 2)])
    assert sample_perfect_matching(odd, Fraction(1, 10), exact_count_oracle, exact_witness, rng.getrandbits) is None
    complete_four = Graph.make(range(4), combinations(range(4), 2))
    forced_stats = Stats()
    assert sample_perfect_matching(complete_four, Fraction(1, 10), lambda *_: Fraction(0), exact_witness, rng.getrandbits, forced_stats) in exact_matchings(complete_four)
    assert forced_stats.witness_fallbacks == 1 and forced_stats.bit_draws == 0
    # Dyadic selection has a bounded number of bits even for a target count
    # ratio vastly smaller than the selected grid unit.
    tiny = rounded_probabilities((Fraction(1), Fraction(1 << 10000)), 17)
    assert tiny == (Fraction(0), Fraction(1))
    # Integrate the implemented sampler on actual expanded gadgets and then
    # project. Original weighted laws are computed independently on support.
    weighted_cases = []
    matrices = [
        [],
        [[0, 2], [2, 0]],
        [[0, 2, 1, 1], [2, 0, 1, 1], [1, 1, 0, 2], [1, 1, 2, 0]],
        [[0, Fraction(1, 2), 1, 1], [Fraction(1, 2), 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]],
        [[0, Fraction(1, 3), 0, 0], [Fraction(1, 3), 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]],
    ]
    eta = Fraction(1, 10)
    for matrix in matrices:
        expansion = expand_rational_matrix(matrix)
        expanded = Graph.make(range(expansion.graph.order), expansion.graph.edges)
        support = Graph.make(range(len(matrix)), ((u, v) for u, v in combinations(range(len(matrix)), 2) if matrix[u][v]))
        hafnian = exact_hafnian(matrix)
        weighted_reference = {}
        for matching in exact_matchings(support):
            weight = Fraction(1)
            for u, v in matching:
                weight *= matrix[u][v]
            weighted_reference[matching] = weight / hafnian
        for name, multiplier, failure in (
            ("exact_estimates", None, Fraction(0)),
            ("extremal_relative_errors", signed_multiplier, Fraction(0)),
            ("errors_and_failures", signed_multiplier, parameters(len(expanded.vertices), eta).call_failure),
        ):
            expanded_law = exact_sampler_law(expanded, eta, multiplier, failure)
            projected = {}
            for matching, probability in expanded_law.items():
                image = expansion.project(matching)
                projected[image] = projected.get(image, Fraction(0)) + probability
            expanded_tv = total_variation(expanded_law, uniform_law(expanded))
            projected_tv = total_variation(projected, weighted_reference)
            assert projected_tv <= expanded_tv <= eta
            weighted_cases.append({"original_order": len(matrix), "expanded_order": expansion.graph.order, "denominator": str(expansion.denominator), "hafnian": str(hafnian), "scenario": name, "expanded_tv": str(expanded_tv), "pushforward_tv": str(projected_tv)})
    return {
        "status": "passed",
        "scope": "exact finite-instance validation of the reduction; no certification or implementation of the upstream FPRAS",
        "python_version": platform.python_version(),
        "arithmetic": "Python arbitrary-precision integers and fractions.Fraction; no floating-point TV estimates",
        "seed": 20261006,
        "graph_instances": len(graphs),
        "feasible_graph_instances": feasible_graphs,
        "eta_values": [str(eta) for eta in etas],
        "exact_output_laws_integrated": exact_laws,
        "imperative_sampler_runs": imperative_runs,
        "all_zero_estimate_fallbacks_observed": fallback_runs,
        "maximum_observed_counters": caps_observed,
        "maximum_exact_tv_divided_by_eta": {name: {"ratio": str(ratio), "attaining_case": case} for name, (ratio, case) in maximum.items()},
        "weighted_gadget_pushforward_cases": weighted_cases,
        "checks": [
            "all simple graphs on 0, 2, and 4 vertices; seeded six-vertex instances; explicit disconnected and complete fixtures",
            "exact integration of every finite-bit choice via dyadic cumulative boundaries",
            "relative-error endpoint perturbations dependent on the residual graph",
            "exact integration of all independent per-call zero-estimate failures at the prescribed failure probability",
            "output feasibility on arbitrary all-zero estimates and witness fallback",
            "empty graph, odd infeasible graph, unique matching, disconnected support, tiny positive probability",
            "per-execution count-call, witness-call, decision, and random-bit caps",
            "exact gadget sampler pushforward to weighted matching laws, including rational weights below one",
        ],
    }


if __name__ == "__main__":
    result = verify()
    destination = Path(__file__).resolve().parents[1] / "data" / "sampling_verification.json"
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("status", "graph_instances", "exact_output_laws_integrated", "imperative_sampler_runs")}))
