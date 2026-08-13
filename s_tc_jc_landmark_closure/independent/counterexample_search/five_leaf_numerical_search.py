#!/usr/bin/env python3
"""Adversarial numerical search over the exact five-leaf S_TC census.

This script is deliberately labelled as a candidate finder.  It does not turn
failed fits into algebraic separation claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

import numpy as np

from audit_io import load_json
from clean_graph import class_membership
from fourier_engine import build_model, evaluate
from screen_models import fit_target, graph_from_record


def algebra_key(profile):
    return json.dumps(profile["evaluations"], sort_keys=True)


def dominates(source, target):
    for s, t in zip(source["evaluations"], target["evaluations"]):
        if s["full_rank"] > t["full_rank"]:
            return False
        if any(a > b for a, b in zip(s["four_leaf_marginal_ranks"], t["four_leaf_marginal_ranks"])):
            return False
        if any(a > b for a, b in zip(s["three_leaf_marginal_ranks"], t["three_leaf_marginal_ranks"])):
            return False
        if any(a > b for a, b in zip(s["random_coordinate_subset_ranks"], t["random_coordinate_subset_ranks"])):
            return False
        # If a polynomial is observed identically zero on the target but
        # nonzero on the source, containment is impossible at generic points.
        if any(tz and not sz for sz, tz in zip(s["three_leaf_tree_separator_zero"], t["three_leaf_tree_separator_zero"])):
            return False
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-one-sided", type=int, default=3000)
    args = parser.parse_args()

    census = load_json(args.census)
    pdata = load_json(args.profiles)
    records = {tuple(t["canonical_code"]): t for t in census["topologies"] if t["n"] == 5 and t["membership"] == "S_TC"}
    profiles = pdata["profiles"]
    by_code = {tuple(p["canonical_code"]): p for p in profiles}

    models = {}
    for index, p in enumerate(profiles):
        code = tuple(p["canonical_code"])
        graph = graph_from_record(records[code])
        membership, roots = class_membership(graph)
        assert membership == "S_TC"
        models[code] = build_model(graph, roots[0])
        if index % 250 == 0:
            print("models", index, len(profiles), flush=True)

    clusters = defaultdict(list)
    for p in profiles:
        clusters[algebra_key(p)].append(p)
    symmetric_pairs = []
    for cluster in clusters.values():
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                symmetric_pairs.append((cluster[i], cluster[j], "equal_finite_field_profile"))

    one_sided_pool = []
    for source in profiles:
        for target in profiles:
            if source is target:
                continue
            if algebra_key(source) == algebra_key(target):
                continue
            if dominates(source, target):
                one_sided_pool.append((source, target, "profile_dominance_sample"))
    sampler = random.Random(20260809)
    if len(one_sided_pool) > args.max_one_sided:
        one_sided_pairs = sampler.sample(one_sided_pool, args.max_one_sided)
    else:
        one_sided_pairs = one_sided_pool

    pairs = symmetric_pairs + one_sided_pairs
    rng = np.random.default_rng(314159265)
    source_samples = {}
    candidates = []
    closest = []
    for index, (source, target, reason) in enumerate(pairs):
        scode = tuple(source["canonical_code"])
        tcode = tuple(target["canonical_code"])
        smodel, tmodel = models[scode], models[tcode]
        if scode not in source_samples:
            samples = []
            for _ in range(1):
                theta = rng.uniform(0.18, 0.82, size=smodel.parameter_count)
                samples.append((theta, np.asarray(evaluate(smodel, theta.tolist()))))
            source_samples[scode] = samples
        fits = []
        best_score = float("inf")
        for theta, values in source_samples[scode]:
            fit = fit_target(tmodel, values, rng, starts=1, iterations=60)
            best_score = min(best_score, fit["max_log_residual"])
            fits.append({"source_parameters": theta.tolist(), **fit})
        record = {
            "source_code": list(scode),
            "target_code": list(tcode),
            "reason": reason,
            "source_rank": source["evaluations"][0]["full_rank"],
            "target_rank": target["evaluations"][0]["full_rank"],
            "best_max_log_residual": best_score,
        }
        closest.append(record)
        if best_score < 1e-8:
            record["fits"] = fits
            record["status"] = "NUMERICALLY_OBSERVED_CANDIDATE_REQUIRES_EXACT_CERTIFICATE"
            candidates.append(record)
        if index % 250 == 0:
            print("pairs", index, len(pairs), "candidates", len(candidates), flush=True)

    payload = {
        "schema": 1,
        "status": "NUMERICALLY_OBSERVED",
        "warning": "A failed nonlinear fit is not a proof of separation. Any candidate below must be independently converted to exact open-domain equality/containment and rank certificates.",
        "T_class_count": len(profiles),
        "equal_profile_unordered_pairs_tested": len(symmetric_pairs),
        "profile_dominant_directed_pool_size": len(one_sided_pool),
        "profile_dominant_directions_sampled": len(one_sided_pairs),
        "total_pairs_tested": len(pairs),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "fifty_closest": sorted(closest, key=lambda x: x["best_max_log_residual"])[:50],
        "fifty_closest_equal_profile": sorted(
            (x for x in closest if x["reason"] == "equal_finite_field_profile"),
            key=lambda x: x["best_max_log_residual"],
        )[:50],
        "fifty_closest_one_sided_sample": sorted(
            (x for x in closest if x["reason"] == "profile_dominance_sample"),
            key=lambda x: x["best_max_log_residual"],
        )[:50],
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(args.output.read_bytes()).hexdigest())
    print("candidates", len(candidates))


if __name__ == "__main__":
    main()
