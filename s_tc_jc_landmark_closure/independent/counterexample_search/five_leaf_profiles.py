#!/usr/bin/env python3
"""Exact finite-field risk profiles for five-leaf S_TC T-classes."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

from audit_io import load_json
from clean_graph import class_membership
from fourier_engine import build_model, evaluate_mod_prime, rank_mod_prime
from networkx_isomorphism_crosscheck import incidence_graph
from screen_models import PRIMES, deterministic_parameters, graph_from_record


def canonical_character(g):
    variants = []
    for perm in itertools.permutations((1, 2, 3)):
        table = (0,) + perm
        variants.append(tuple(table[x] for x in g))
    return min(variants)


def profile_at_prime(model, params, prime):
    values, jac = evaluate_mod_prime(model, params, prime)
    row = {g: i for i, g in enumerate(model.coordinates)}
    full_rank = rank_mod_prime(jac, prime)
    marginal4 = []
    for omitted in range(5):
        inds = [i for i, g in enumerate(model.coordinates) if g[omitted] == 0]
        marginal4.append(rank_mod_prime([jac[i] for i in inds], prime))
    marginal3 = []
    separator_zero = []
    for triple in itertools.combinations(range(5), 3):
        inds = [i for i, g in enumerate(model.coordinates) if all(g[j] == 0 for j in range(5) if j not in triple)]
        marginal3.append(rank_mod_prime([jac[i] for i in inds], prime))
        a, b, c = triple
        assignments = []
        for chars in ((0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 2, 3)):
            g = [0] * 5
            for pos, char in zip(triple, chars):
                g[pos] = char
            assignments.append(canonical_character(tuple(g)))
        A, B, C, D = (values[row[g]] for g in assignments)
        separator_zero.append((A * B % prime * C - D * D) % prime == 0)

    rng = random.Random(712367 + prime)
    subset_ranks = []
    for _ in range(24):
        size = rng.randrange(4, len(jac) + 1)
        inds = sorted(rng.sample(range(len(jac)), size))
        subset_ranks.append(rank_mod_prime([jac[i] for i in inds], prime))
    return {
        "prime": prime,
        "full_rank": full_rank,
        "four_leaf_marginal_ranks": marginal4,
        "three_leaf_marginal_ranks": marginal3,
        "three_leaf_tree_separator_zero": separator_zero,
        "random_coordinate_subset_ranks": subset_ranks,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    census = load_json(args.census)
    representatives = {}
    for rec in census["topologies"]:
        if rec["n"] == 5 and rec["membership"] == "S_TC":
            representatives.setdefault(tuple(rec["T_class_code"]), rec)
    profiles = []
    for index, rec in enumerate(representatives.values()):
        graph = graph_from_record(rec)
        membership, roots = class_membership(graph)
        assert membership == "S_TC"
        model = build_model(graph, roots[0])
        evals = []
        for prime in PRIMES:
            params = deterministic_parameters(model, prime, repr(rec["canonical_code"]) + f":five:{prime}")
            evals.append(profile_at_prime(model, params, prime))
        unlabeled = incidence_graph(rec)
        for node, attrs in unlabeled.nodes(data=True):
            if attrs["color"].startswith("leaf:"):
                attrs["color"] = "leaf"
        structural_hash = nx.weisfeiler_lehman_graph_hash(unlabeled, node_attr="color", iterations=8)
        profiles.append(
            {
                "canonical_code": rec["canonical_code"],
                "T_class_code": rec["T_class_code"],
                "reticulations": len(rec["reticulations"]),
                "unlabelled_incidence_WL_hash": structural_hash,
                "evaluations": evals,
            }
        )
        if index % 100 == 0:
            print(index, len(representatives), flush=True)

    def algebra_key(p):
        return json.dumps(p["evaluations"], sort_keys=True)

    cluster_counts = Counter(algebra_key(p) for p in profiles)
    structural_algebra_counts = Counter((p["unlabelled_incidence_WL_hash"], algebra_key(p)) for p in profiles)
    payload = {
        "schema": 1,
        "status": "EXACTLY_COMPUTED_FINITE_FIELD_SCREEN",
        "warning": "Ranks and zero tests are exact at the recorded finite-field points but are only generic-risk screens, not ideal-containment proofs.",
        "T_class_count": len(profiles),
        "profiles": profiles,
        "algebra_profile_cluster_size_distribution": dict(sorted(Counter(cluster_counts.values()).items())),
        "structural_plus_algebra_cluster_size_distribution": dict(sorted(Counter(structural_algebra_counts.values()).items())),
        "largest_algebra_profile_cluster": max(cluster_counts.values()),
        "largest_structural_plus_algebra_cluster": max(structural_algebra_counts.values()),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(args.output.read_bytes()).hexdigest())
    print(json.dumps({k: payload[k] for k in payload if k not in {"profiles", "warning", "schema", "status"}}, sort_keys=True))


if __name__ == "__main__":
    main()
