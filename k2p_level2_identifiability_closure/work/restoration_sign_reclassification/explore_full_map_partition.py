#!/usr/bin/env python3
"""Independent exploratory partition of the 646 revoked restoration leaves.

This script is diagnostic, not a release certificate.  It reconstructs the
physical children through the released restoration generator, ignores the
rooted witness types, searches all 30 labelled T_i restrictions, and then
tries an exact quadratic when no asymmetric T_i identity exists.
"""

from __future__ import annotations

import collections
import importlib.util
import itertools
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RESTORATION_PATH = PROJECT / "work/restoration_forest/enumerate_five_port.py"
METADATA = PROJECT / "work/adversarial_proof_review/restoration_tree_sunlet_metadata_cache.json"
OUTPUT = HERE / "exploratory_partition.json"


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def sparse_payload(polynomial):
    return [[list(exponent), str(coefficient)] for exponent, coefficient in sorted(polynomial.items())]


def t_pullback(atlas, descriptor, outputs, triple, orientation):
    assignments = atlas.orbit_assignments(descriptor.k)
    index = {assignment: number for number, assignment in enumerate(assignments)}
    others = sorted(set(triple) - {orientation})
    order = (others[0], others[1], orientation)

    def coordinate(characters):
        assignment = [0] * descriptor.k
        for label, character in zip(order, characters):
            assignment[label] = character
        return outputs[index[atlas.ct_orbit_rep(tuple(assignment))]]

    v = coordinate((1, 3, 2))
    xs = coordinate((1, 1, 0))
    xg = coordinate((2, 2, 0))
    yg = coordinate((2, 0, 2))
    zg = coordinate((0, 2, 2))
    return atlas.sparse_lincomb(
        [atlas.sparse_mul_many([v, v, xg]), atlas.sparse_mul_many([xs, xs, yg, zg])],
        [1, -1],
    )


def evaluate_sparse(polynomial, point):
    total = 0
    for exponent, coefficient in polynomial.items():
        term = coefficient
        for value, power in zip(point, exponent):
            if power:
                term *= value ** power
        total += term
    return total


def physical_witness(atlas, descriptor, polynomial):
    for salt in range(16):
        edge_pairs, lambdas = atlas.default_exact_point(descriptor, salt)
        point = tuple(value for pair in edge_pairs for value in pair) + tuple(lambdas)
        value = evaluate_sparse(polynomial, point)
        if value:
            return salt, str(value)
    return None


def main():
    atlas = import_path("restoration_partition_atlas", ATLAS_PATH)
    restoration = import_path("restoration_partition_generator", RESTORATION_PATH)
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    roots, _, parent_count = restoration.reconstruct_roots(atlas, sources, targets)
    if parent_count != 997:
        raise RuntimeError(parent_count)
    root_by_id = {root["root_id"]: root for root in roots}
    rows = json.loads(METADATA.read_text())["rows"]
    if len(rows) != 646:
        raise RuntimeError(len(rows))

    source_graphs = {}
    target_graphs = {}
    descriptor_outputs = {}

    def graph_pair(row):
        source_key = tuple(row["source_key"])
        target_key = (row["target_key"][0], tuple(row["target_key"][1]), row["target_key"][2])
        root = root_by_id[row["row_id"]["root_id"]]
        if source_key not in source_graphs:
            candidate = root["source_insertion_edge_candidates"][source_key[1]]
            source_graphs[source_key] = restoration.insert_source_leaf(
                atlas, sources[source_key[0]].graph, candidate, 4
            )
        if target_key not in target_graphs:
            target_graphs[target_key] = restoration.promoted_target(
                atlas,
                targets,
                target_key[0],
                target_key[1],
                target_key[2],
                4,
            )[0]
        return source_key, target_key, source_graphs[source_key], target_graphs[target_key]

    def compile_one(side, key, graph):
        cache_key = (side, key)
        if cache_key not in descriptor_outputs:
            descriptor = atlas.model_descriptor_fast2(graph)
            descriptor_outputs[cache_key] = (
                descriptor,
                atlas.output_sparse_polynomials(descriptor),
            )
        return descriptor_outputs[cache_key]

    pullbacks = {}
    result_rows = []
    census = collections.Counter()
    for ordinal, row in enumerate(rows):
        source_key, target_key, source_graph, target_graph = graph_pair(row)
        source_descriptor, source_outputs = compile_one("source", source_key, source_graph)
        target_descriptor, target_outputs = compile_one("target", target_key, target_graph)
        asymmetric = []
        for triple in itertools.combinations(range(5), 3):
            for orientation in triple:
                for side, key, descriptor, outputs in (
                    ("source", source_key, source_descriptor, source_outputs),
                    ("target", target_key, target_descriptor, target_outputs),
                ):
                    pullback_key = (side, key, triple, orientation)
                    if pullback_key not in pullbacks:
                        pullbacks[pullback_key] = t_pullback(
                            atlas, descriptor, outputs, triple, orientation
                        )
                source_polynomial = pullbacks[("source", source_key, triple, orientation)]
                target_polynomial = pullbacks[("target", target_key, triple, orientation)]
                if not source_polynomial and target_polynomial:
                    asymmetric.append(
                        (len(target_polynomial), triple, orientation, "target", target_polynomial)
                    )
                elif not target_polynomial and source_polynomial:
                    asymmetric.append(
                        (len(source_polynomial), triple, orientation, "source", source_polynomial)
                    )

        public = {
            "row_id": row["row_id"],
            "legacy_triple": row["triple"],
            "asymmetric_T_count": len(asymmetric),
        }
        if asymmetric:
            term_count, triple, orientation, nonzero_side, polynomial = min(
                asymmetric, key=lambda item: (item[0], item[1], item[2], item[3])
            )
            descriptor = source_descriptor if nonzero_side == "source" else target_descriptor
            witness = physical_witness(atlas, descriptor, polynomial)
            if witness is None:
                raise RuntimeError((row["row_id"], "missing T witness"))
            public.update({
                "category": "asymmetric_full_map_T",
                "triple": list(triple),
                "orientation": orientation,
                "nonzero_side": nonzero_side,
                "term_count": term_count,
                "physical_witness": list(witness),
            })
            census["asymmetric_full_map_T"] += 1
        else:
            quadratic = atlas.quadratic_separator_fast(
                source_descriptor, target_descriptor, max_block_size=16
            )
            if quadratic is not None:
                public.update({
                    "category": "exact_quadratic",
                    "coordinate_pairs": [list(pair) for pair in quadratic["coordinate_pairs"]],
                    "coefficients": [str(value) for value in quadratic["coefficients"]],
                    "weight": list(quadratic["weight"]),
                })
                census["exact_quadratic"] += 1
            else:
                public.update({
                    "category": "unresolved",
                    "source_rank_lower": atlas.rank_certificate(source_descriptor)["rank"],
                    "target_rank_lower": atlas.rank_certificate(target_descriptor)["rank"],
                })
                census["unresolved"] += 1
        result_rows.append(public)
        if ordinal and ordinal % 100 == 0:
            print(f"restoration partition:{ordinal}/{len(rows)} {dict(census)}", flush=True)

    report = {
        "schema": "k2p-restoration-revoked-sign-exploration-v1",
        "status": "PASS" if not census["unresolved"] else "INCOMPLETE",
        "rows": len(rows),
        "source_graphs": len(source_graphs),
        "target_graphs": len(target_graphs),
        "census": dict(sorted(census.items())),
        "results": result_rows,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "rows", "source_graphs", "target_graphs", "census")}, sort_keys=True))


if __name__ == "__main__":
    main()
