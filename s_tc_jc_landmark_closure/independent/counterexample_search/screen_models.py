#!/usr/bin/env python3
"""Exact modular and numerical screens for bounded S_TC model relations.

Finite-field ranks are exact at the recorded evaluation points but are used
only as screening evidence about generic ranks.  Numerical fitting nominates
candidates; it never certifies overlap or containment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

from audit_io import load_json
from clean_graph import MixedGraph, class_membership, edge_key
from fourier_engine import (
    JCModel,
    build_model,
    evaluate,
    evaluate_and_jacobian,
    evaluate_mod_prime,
    rank_mod_prime,
)


PRIMES = (1000003, 1000033)


def graph_from_record(record: dict) -> MixedGraph:
    arrows = {}
    edges = []
    for item in record["edges"]:
        e = edge_key(item["u"], item["v"])
        edges.append(e)
        arrows[e] = set(item["arrowheads"])
    return MixedGraph.make(record["n"], record["m"], record["reticulations"], edges, arrows)


def deterministic_parameters(model: JCModel, prime: int, salt: str) -> List[int]:
    seed = hashlib.sha256(salt.encode()).digest()
    rng = random.Random(int.from_bytes(seed[:16], "big"))
    return [rng.randrange(2, prime - 1) for _ in range(model.parameter_count)]


def _xor_tuple(values: Sequence[int]) -> int:
    answer = 0
    for x in values:
        answer ^= x
    return answer


def _full_fourier_mod(model: JCModel, parameters: Sequence[int], prime: int) -> Dict[Tuple[int, ...], int]:
    # Evaluate orbit representatives, then use the fact that every permutation
    # of the three nonzero characters is a JC symmetry.
    rep_values, _ = evaluate_mod_prime(model, parameters, prime)
    rep_map = dict(zip(model.coordinates, rep_values))
    autos = tuple(__import__("itertools").permutations((1, 2, 3)))

    def canonical(g: Tuple[int, ...]) -> Tuple[int, ...]:
        variants = []
        for perm in autos:
            table = (0,) + perm
            variants.append(tuple(table[x] for x in g))
        return min(variants)

    out = {}
    for flat in range(4 ** model.n):
        q = flat
        g = []
        for _ in range(model.n):
            g.append(q % 4)
            q //= 4
        tup = tuple(g)
        if _xor_tuple(tup):
            out[tup] = 0
        elif not any(tup):
            out[tup] = 1
        else:
            out[tup] = rep_map[canonical(tup)]
    return out


def flattening_rank_deck(model: JCModel, parameters: Sequence[int], prime: int) -> Dict[str, int]:
    tensor = _full_fourier_mod(model, parameters, prime)
    n = model.n
    deck = {}
    # One representative of each labelled split, with the smaller side first
    # and lexicographic tie-breaking against its complement.
    for mask in range(1, (1 << n) - 1):
        comp = ((1 << n) - 1) ^ mask
        left = tuple(i for i in range(n) if mask & (1 << i))
        right = tuple(i for i in range(n) if comp & (1 << i))
        if len(left) > len(right) or (len(left) == len(right) and left > right):
            continue
        rows = list(__import__("itertools").product(range(4), repeat=len(left)))
        cols = list(__import__("itertools").product(range(4), repeat=len(right)))
        matrix = []
        for a in rows:
            row = []
            for b in cols:
                g = [0] * n
                for i, x in zip(left, a):
                    g[i] = x
                for i, x in zip(right, b):
                    g[i] = x
                row.append(tensor[tuple(g)])
            matrix.append(row)
        key = "".join(map(str, left)) + "|" + "".join(map(str, right))
        deck[key] = rank_mod_prime(matrix, prime)
    return deck


def modular_profile(record: dict) -> dict:
    graph = graph_from_record(record)
    membership, roots = class_membership(graph)
    if membership != "S_TC":
        raise ValueError("screen input is not S_TC")
    root_profiles = []
    for root_index, rooting in enumerate(roots):
        model = build_model(graph, rooting)
        evaluations = []
        for prime in PRIMES:
            params = deterministic_parameters(model, prime, repr(record["canonical_code"]) + f":{root_index}:{prime}")
            _, jac = evaluate_mod_prime(model, params, prime)
            evaluations.append(
                {
                    "prime": prime,
                    "parameters": params,
                    "jacobian_rank": rank_mod_prime(jac, prime),
                    "flattening_ranks": flattening_rank_deck(model, params, prime),
                }
            )
        root_profiles.append(
            {
                "root_edge": list(rooting.root_edge),
                "parameter_count": model.parameter_count,
                "coordinate_count": len(model.coordinates),
                "evaluations": evaluations,
            }
        )
    ranks = {e["jacobian_rank"] for rp in root_profiles for e in rp["evaluations"]}
    return {
        "canonical_code": record["canonical_code"],
        "T_class_code": record["T_class_code"],
        "n": record["n"],
        "reticulations": len(record["reticulations"]),
        "root_profiles": root_profiles,
        "observed_rank_set": sorted(ranks),
        "root_rank_consistent": len(ranks) == 1,
    }


def sigmoid(y: np.ndarray) -> np.ndarray:
    # Stable enough because trial steps are clipped below.
    y = np.clip(y, -9.0, 9.0)
    return 1.0 / (1.0 + np.exp(-y))


def fit_target(model: JCModel, target_values: np.ndarray, rng: np.random.Generator, starts: int = 8, iterations: int = 120) -> dict:
    best = None
    log_target = np.log(target_values)
    p = model.parameter_count
    ecount = model.edge_parameter_count
    rcount = len(model.reticulations)

    def subset_xor(g, mask):
        answer = 0
        i = 0
        while mask:
            if mask & 1:
                answer ^= g[i]
            mask >>= 1
            i += 1
        return answer

    active = np.asarray(
        [
            [
                [bool(mask and subset_xor(g, mask)) for mask in switching.descendant_masks]
                for switching in model.switchings
            ]
            for g in model.coordinates
        ],
        dtype=float,
    )
    choices = np.asarray([s.choices for s in model.switchings], dtype=int)

    def fast_values_jac(theta):
        x = theta[:ecount]
        lambdas = theta[ecount:]
        log_monomials = np.einsum("cse,e->cs", active, np.log(x))
        monomials = np.exp(log_monomials)
        if rcount:
            factors = np.where(choices == 0, lambdas[None, :], 1.0 - lambdas[None, :])
            weights = np.prod(factors, axis=1)
        else:
            weights = np.ones(len(model.switchings))
        terms = monomials * weights[None, :]
        values = np.sum(terms, axis=1)
        edge_jac = np.einsum("cs,cse->ce", terms, active) / x[None, :]
        if rcount:
            dweights = weights[:, None] * np.where(
                choices == 0,
                1.0 / lambdas[None, :],
                -1.0 / (1.0 - lambdas[None, :]),
            )
            lambda_jac = monomials @ dweights
            jac = np.concatenate((edge_jac, lambda_jac), axis=1)
        else:
            jac = edge_jac
        return values, jac

    def fast_values(theta):
        return fast_values_jac(theta)[0]

    for start in range(starts):
        y = rng.uniform(-1.6, 1.6, size=p)
        damping = 1e-3
        for _ in range(iterations):
            theta = sigmoid(y)
            values, jac_theta = fast_values_jac(theta)
            residual = np.log(values) - log_target
            jac = jac_theta * (theta * (1.0 - theta))[None, :] / values[:, None]
            lhs = jac.T @ jac + damping * np.eye(p)
            rhs = -(jac.T @ residual)
            try:
                step = np.linalg.solve(lhs, rhs)
            except np.linalg.LinAlgError:
                step = np.linalg.lstsq(lhs, rhs, rcond=None)[0]
            step_norm = np.linalg.norm(step)
            if step_norm > 3.0:
                step *= 3.0 / step_norm
            trial_y = np.clip(y + step, -9.0, 9.0)
            trial_values = fast_values(sigmoid(trial_y))
            trial_residual = np.log(trial_values) - log_target
            if np.linalg.norm(trial_residual) < np.linalg.norm(residual):
                y = trial_y
                damping = max(damping / 3.0, 1e-12)
            else:
                damping = min(damping * 10.0, 1e12)
            if np.max(np.abs(trial_residual)) < 1e-11:
                y = trial_y
                break
        theta = sigmoid(y)
        values, jac = fast_values_jac(theta)
        log_residual = np.log(np.asarray(values)) - log_target
        record = {
            "max_log_residual": float(np.max(np.abs(log_residual))),
            "l2_log_residual": float(np.linalg.norm(log_residual)),
            "parameters": theta.tolist(),
            "target_jacobian_rank_numeric": int(np.linalg.matrix_rank(np.asarray(jac), tol=1e-9)),
        }
        if best is None or record["l2_log_residual"] < best["l2_log_residual"]:
            best = record
    assert best is not None
    return best


def numerical_pair_screen(records: Sequence[dict], profiles: Mapping[Tuple[int, ...], dict], samples: int, starts: int) -> dict:
    # One representative per T-class.  Positive controls are handled
    # separately; the adversarial survivor search compares non-T classes.
    reps = {}
    for rec in records:
        reps.setdefault(tuple(rec["T_class_code"]), rec)
    reps = list(reps.values())
    models = {}
    dims = {}
    flatten = {}
    for rec in reps:
        key = tuple(rec["canonical_code"])
        graph = graph_from_record(rec)
        _, roots = class_membership(graph)
        models[key] = build_model(graph, roots[0])
        profile = profiles[key]
        dims[key] = max(profile["observed_rank_set"])
        first_eval = profile["root_profiles"][0]["evaluations"][0]
        flatten[key] = first_eval["flattening_ranks"]

    directed_pairs = []
    dimension_rejected = 0
    flattening_rejected = 0
    for source in reps:
        skey = tuple(source["canonical_code"])
        for target in reps:
            tkey = tuple(target["canonical_code"])
            if skey == tkey:
                continue
            if dims[skey] > dims[tkey]:
                dimension_rejected += 1
                continue
            if any(flatten[skey][split] > flatten[tkey][split] for split in flatten[skey]):
                flattening_rejected += 1
                continue
            directed_pairs.append((source, target))

    rng = np.random.default_rng(20260809)
    survivors = []
    closest_failures = []
    for pair_index, (source, target) in enumerate(directed_pairs):
        skey = tuple(source["canonical_code"])
        tkey = tuple(target["canonical_code"])
        smodel, tmodel = models[skey], models[tkey]
        fits = []
        for sample in range(samples):
            source_theta = rng.uniform(0.17, 0.83, size=smodel.parameter_count)
            source_values = np.asarray(evaluate(smodel, source_theta.tolist()))
            fit = fit_target(tmodel, source_values, rng, starts=starts)
            fit["source_parameters"] = source_theta.tolist()
            fits.append(fit)
            if fit["max_log_residual"] > 1e-8:
                break
        pair_score = max(f["max_log_residual"] for f in fits)
        closest_failures.append(
            {
                "score": pair_score,
                "source_code": source["canonical_code"],
                "target_code": target["canonical_code"],
                "source_reticulations": len(source["reticulations"]),
                "target_reticulations": len(target["reticulations"]),
                "source_observed_dimension": dims[skey],
                "target_observed_dimension": dims[tkey],
                "completed_samples": len(fits),
            }
        )
        if len(fits) == samples and max(f["max_log_residual"] for f in fits) <= 1e-8:
            survivors.append(
                {
                    "source_code": source["canonical_code"],
                    "target_code": target["canonical_code"],
                    "source_reticulations": len(source["reticulations"]),
                    "target_reticulations": len(target["reticulations"]),
                    "source_observed_dimension": dims[skey],
                    "target_observed_dimension": dims[tkey],
                    "fits": fits,
                    "status": "NUMERICALLY_OBSERVED_CANDIDATE_ONLY",
                }
            )
        if pair_index % 100 == 0:
            print(f"screened {pair_index}/{len(directed_pairs)} survivors={len(survivors)}", flush=True)
    return {
        "T_class_representative_count": len(reps),
        "ordered_nonidentity_pair_count": len(reps) * (len(reps) - 1),
        "dimension_rejected": dimension_rejected,
        "flattening_rejected_after_dimension": flattening_rejected,
        "numerically_fitted_pair_count": len(directed_pairs),
        "survivors": survivors,
        "twenty_closest_nonsurvivors": sorted(closest_failures, key=lambda x: x["score"])[:20],
        "warning": "Numerical fitting and modular ranks are candidate screens, not proofs of separation or containment.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--screen", type=Path)
    parser.add_argument("--n", type=int, default=4)
    parser.add_argument("--samples", type=int, default=2)
    parser.add_argument("--starts", type=int, default=6)
    args = parser.parse_args()
    census = load_json(args.census)
    records = [t for t in census["topologies"] if t["membership"] == "S_TC" and t["n"] == args.n]
    profile_records = []
    for i, record in enumerate(records):
        profile_records.append(modular_profile(record))
        if i % 10 == 0:
            print(f"profile {i}/{len(records)}", flush=True)
    payload = {
        "schema": 1,
        "scope": {"n": args.n, "S_TC_only": True, "primes": list(PRIMES)},
        "profiles": profile_records,
    }
    args.profiles.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("profiles_sha256", hashlib.sha256(args.profiles.read_bytes()).hexdigest())

    inconsistent = [p for p in profile_records if not p["root_rank_consistent"]]
    print("root_rank_inconsistent", len(inconsistent))
    if args.screen:
        pmap = {tuple(p["canonical_code"]): p for p in profile_records}
        result = numerical_pair_screen(records, pmap, args.samples, args.starts)
        args.screen.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("screen_sha256", hashlib.sha256(args.screen.read_bytes()).hexdigest())
        print("survivors", len(result["survivors"]))


if __name__ == "__main__":
    main()
