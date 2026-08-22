#!/usr/bin/env python3
"""Recursively restore the 32 zero/zero first children that retain a dummy."""

from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS_PATH = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
RESTORATION_PATH = PROJECT / "work/restoration_forest/enumerate_five_port.py"
FIRST_PARTITION = HERE / "exploratory_partition.json"
OUTPUT = HERE / "exploratory_second_restoration.json"


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


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


def split_payload(value):
    result = []
    for item in sorted(value, key=repr):
        if item == ("star",):
            result.append(["star"])
        else:
            result.append([list(item[0]), list(item[1])])
    return result


def main():
    atlas = import_path("second_restoration_atlas", ATLAS_PATH)
    restoration = import_path("second_restoration_generator", RESTORATION_PATH)
    sources = atlas.source_supports()
    targets = atlas.target_completions(4, True) + atlas.target_completions(4, False)
    roots, _, count = restoration.reconstruct_roots(atlas, sources, targets)
    if count != 997:
        raise RuntimeError(count)
    root_by_id = {root["root_id"]: root for root in roots}
    unresolved = [
        row for row in json.loads(FIRST_PARTITION.read_text())["results"]
        if row["category"] == "unresolved"
    ]
    requests = []
    for row in unresolved:
        root = root_by_id[row["row_id"]["root_id"]]
        remaining = [role for role in root["dummy_roles"] if role != row["row_id"]["restored_role"]]
        if remaining:
            if len(remaining) != 1:
                raise RuntimeError((row, remaining))
            requests.append((row, root, remaining[0]))
    if len(requests) != 32:
        raise RuntimeError(len(requests))

    results = []
    census = Counter()
    for first_row, root, remaining_role in requests:
        first_index = first_row["row_id"]["source_insertion_index"]
        first_source = restoration.insert_source_leaf(
            atlas,
            sources[root["source_index"]].graph,
            root["source_insertion_edge_candidates"][first_index],
            4,
        )
        target_full, _ = restoration.promoted_target(
            atlas,
            targets,
            root["target_index"],
            tuple(root["port_match"]),
            first_row["row_id"]["restored_role"],
            4,
        )
        second_target_full = target_full.copy()
        nodes = [
            node for node, data in second_target_full.nodes(data=True)
            if data.get("dummy_name") == remaining_role
        ]
        if len(nodes) != 1:
            raise RuntimeError((root["root_id"], remaining_role, nodes))
        data = second_target_full.nodes[nodes[0]]
        data["label"] = 5
        data["dummy"] = False
        data["dummy_name"] = None
        second_target = atlas.restrict_rooted(second_target_full, set(range(6)))

        candidates = restoration.source_insertion_candidates(first_source)
        if len(candidates) != 8:
            raise RuntimeError((root["root_id"], len(candidates)))
        for second_index, candidate in enumerate(candidates):
            second_source = restoration.insert_source_leaf(
                atlas, first_source, candidate, 5
            )
            row_id = {
                "root_id": root["root_id"],
                "first_restored_role": first_row["row_id"]["restored_role"],
                "first_source_insertion_index": first_index,
                "second_restored_role": remaining_role,
                "second_source_insertion_index": second_index,
            }
            proof = None
            for quartet in itertools.combinations(range(6), 4):
                source_splits = atlas.quartet_splits(second_source, quartet)
                target_splits = atlas.quartet_splits(second_target, quartet)
                if source_splits != target_splits:
                    proof = {
                        "category": "displayed_quartet_mismatch",
                        "quartet": list(quartet),
                        "source_splits": split_payload(source_splits),
                        "target_splits": split_payload(target_splits),
                    }
                    break
            if proof is None:
                relation = atlas.mixed_relation_exact_prepared(
                    atlas.prepare_mixed_source(second_source), second_target
                )
                if relation != "none":
                    proof = {"category": f"exact_{relation}"}
                else:
                    source_descriptor = atlas.model_descriptor_fast2(second_source)
                    target_descriptor = atlas.model_descriptor_fast2(second_target_full)
                    source_outputs = atlas.output_sparse_polynomials(source_descriptor)
                    target_outputs = atlas.output_sparse_polynomials(target_descriptor)
                    asymmetric = []
                    for triple in itertools.combinations(range(6), 3):
                        for orientation in triple:
                            source_polynomial = t_pullback(
                                atlas, source_descriptor, source_outputs, triple, orientation
                            )
                            target_polynomial = t_pullback(
                                atlas, target_descriptor, target_outputs, triple, orientation
                            )
                            if not source_polynomial and target_polynomial:
                                asymmetric.append((len(target_polynomial), triple, orientation, "target"))
                            elif not target_polynomial and source_polynomial:
                                asymmetric.append((len(source_polynomial), triple, orientation, "source"))
                    if asymmetric:
                        terms, triple, orientation, nonzero_side = min(asymmetric)
                        proof = {
                            "category": "asymmetric_full_map_T",
                            "triple": list(triple),
                            "orientation": orientation,
                            "nonzero_side": nonzero_side,
                            "term_count": terms,
                        }
                    else:
                        proof = {"category": "unresolved"}
            census[proof["category"]] += 1
            results.append({"row_id": row_id, **proof})
    if len(results) != 256:
        raise RuntimeError(len(results))
    report = {
        "schema": "k2p-restoration-second-child-exploration-v1",
        "status": "PASS" if not census["unresolved"] else "INCOMPLETE",
        "first_children_expanded": len(requests),
        "second_children": len(results),
        "census": dict(sorted(census.items())),
        "results": results,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in ("status", "first_children_expanded", "second_children", "census")}, sort_keys=True))


if __name__ == "__main__":
    main()
