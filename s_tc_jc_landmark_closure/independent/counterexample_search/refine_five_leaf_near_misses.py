#!/usr/bin/env python3
"""High-effort numerical refinement of the closest five-leaf near misses."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from audit_io import load_json
from clean_graph import class_membership
from fourier_engine import build_model, evaluate
from screen_models import fit_target, graph_from_record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--screen", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    census = load_json(args.census)
    screen = load_json(args.screen)
    records = {tuple(t["canonical_code"]): t for t in census["topologies"]}
    closest = screen["fifty_closest"]
    chosen = screen.get("fifty_closest_one_sided_sample", closest)[:20]
    equal = screen.get("fifty_closest_equal_profile", [])[:20]
    keys = {(tuple(x["source_code"]), tuple(x["target_code"])): x for x in chosen + equal}
    model_cache = {}

    def model(code):
        if code not in model_cache:
            graph = graph_from_record(records[code])
            _, roots = class_membership(graph)
            model_cache[code] = build_model(graph, roots[0])
        return model_cache[code]

    rng = np.random.default_rng(2718281828)
    results = []
    candidates = []
    for index, ((scode, tcode), old) in enumerate(keys.items()):
        smodel, tmodel = model(scode), model(tcode)
        fits = []
        for sample in range(5):
            theta = rng.uniform(0.16, 0.84, size=smodel.parameter_count)
            values = np.asarray(evaluate(smodel, theta.tolist()))
            fit = fit_target(tmodel, values, rng, starts=20, iterations=240)
            fits.append(
                {
                    "max_log_residual": fit["max_log_residual"],
                    "target_parameter_min": min(fit["parameters"]),
                    "target_parameter_max": max(fit["parameters"]),
                }
            )
        result = {
            "source_code": list(scode),
            "target_code": list(tcode),
            "reason": old["reason"],
            "coarse_best_residual": old["best_max_log_residual"],
            "refined_fits": fits,
            "best_refined_residual": min(x["max_log_residual"] for x in fits),
            "all_five_below_1e-10": all(x["max_log_residual"] < 1e-10 for x in fits),
        }
        if result["all_five_below_1e-10"]:
            result["status"] = "NUMERICALLY_OBSERVED_CANDIDATE_REQUIRES_EXACT_CERTIFICATE"
            candidates.append(result)
        results.append(result)
        print(index, len(keys), result["best_refined_residual"], flush=True)
    payload = {
        "schema": 1,
        "status": "NUMERICALLY_OBSERVED",
        "near_misses_refined": len(results),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "results": results,
        "warning": "Failed numerical refinement is not an algebraic separation proof.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("PASS", hashlib.sha256(args.output.read_bytes()).hexdigest(), "candidates", len(candidates))


if __name__ == "__main__":
    main()
