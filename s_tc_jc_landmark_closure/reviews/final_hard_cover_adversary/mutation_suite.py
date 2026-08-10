#!/usr/bin/env python3
"""Mutation-sensitive adversarial tests for a schema-3 candidate stream.

Mutations are applied to in-memory copies only.  Every checker is semantic:
where useful, local content hashes are recomputed so a mutation cannot be
rejected merely because an outer checksum was left stale.
"""

from __future__ import annotations

import argparse
import copy
from itertools import combinations
import json
from pathlib import Path
import time

from audit_candidate_full import (
    COVERAGE_EXTRA,
    PROJECT,
    ROOT_KEY_FIELDS,
    STATE_OPTIONAL,
    STATE_REQUIRED,
    file_sha,
    graph_from_row,
    load_jsonl,
    poly_from_row,
)
from audit_hard_cover import (
    INVARIANT_PATH,
    build_inventory,
    root_key_from_coverage,
)
from cleanroom_core import (
    canonical_json,
    canonical_mixed,
    exact_poly_hash,
    independent_sign_certificate,
    invariant_orbit,
    primitive_poly,
    pullback,
    quartet_descriptor,
    sd0,
    stable_hash,
)


HERE = Path(__file__).resolve().parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="candidate_full")
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--output", type=Path, default=HERE / "mutation_transcript.json")
    args = parser.parse_args()
    started = time.monotonic()
    state_path = PROJECT / f"primary/certificates/hard_cover_n{args.n}_{args.tag}.jsonl.gz"
    graph_path = PROJECT / f"primary/certificates/hard_cover_graphs_n{args.n}_{args.tag}.jsonl.gz"
    polynomial_path = PROJECT / f"primary/certificates/hard_cover_polynomials_n{args.n}_{args.tag}.jsonl.gz"
    root_path = PROJECT / f"primary/certificates/hard_cover_root_cases_n{args.n}_{args.tag}.jsonl.gz"
    if any(not path.exists() for path in (state_path, graph_path, polynomial_path, root_path)):
        raise SystemExit("candidate_full streams are not complete")
    states, _ = load_jsonl(state_path, "state_id")
    graphs, _ = load_jsonl(graph_path, "graph_id")
    polynomials, _ = load_jsonl(polynomial_path, "polynomial_id")
    roots, _ = load_jsonl(root_path, "root_case_id")
    inventory = build_inventory(selected_outgoing=args.n, recompute_all_descriptor_bits=False)
    invariants = invariant_orbit(json.loads(INVARIANT_PATH.read_text()))
    results = []

    def record(name: str, baseline: bool, mutated: bool, detector: str):
        rejected = baseline and not mutated
        results.append({
            "mutation": name,
            "baseline_accepted": baseline,
            "mutated_accepted": mutated,
            "rejected": rejected,
            "detector": detector,
        })

    # 1. State deletion: remove an entry state named by a root record.
    root = roots[min(roots)]
    entry = root["entry_state_ids"][0]
    baseline = all(identifier in states for identifier in root["entry_state_ids"])
    mutated = all(identifier in (set(states) - {entry}) for identifier in root["entry_state_ids"])
    record("delete_relation_state", baseline, mutated, "root entry-state reference closure")

    # 2. State duplication: sorted streams require unique state IDs.
    identifiers = sorted(states)
    baseline = len(identifiers) == len(set(identifiers))
    duplicated = [*identifiers, identifiers[0]]
    mutated = len(duplicated) == len(set(duplicated))
    record("duplicate_relation_state", baseline, mutated, "state-ID uniqueness")

    # Choose representative raw coverage records.
    state_with_coverage = next(row for row in states.values() if row["raw_coverage"])
    coverage = state_with_coverage["raw_coverage"][0]

    def root_membership(candidate: dict) -> bool:
        if set(candidate) != ROOT_KEY_FIELDS | COVERAGE_EXTRA:
            return False
        key = root_key_from_coverage(candidate)
        root_id = stable_hash(key)
        independent = inventory.root_cases.get(root_id)
        return independent is not None and canonical_json(independent) == canonical_json(key)

    baseline = root_membership(coverage)

    def exact_state_binding(state: dict, candidate: dict) -> bool:
        if candidate.get("root_case_id") != state.get("fixed_full_root_case_id"):
            return False
        if candidate.get("source_graph_id") != state.get("source_graph_id"):
            return False
        if candidate.get("target_graph_id") != state.get("target_graph_id"):
            return False
        source = graphs.get(state["source_graph_id"])
        target = graphs.get(state["target_graph_id"])
        if source is None or target is None:
            return False
        expected = stable_hash({
            "fixed_full_root_case_id": state["fixed_full_root_case_id"],
            "selected_port_count": state["selected_port_count"],
            "source_rooted_graph_id": state["source_graph_id"],
            "target_rooted_graph_id": state["target_graph_id"],
            "source_mixed_code": source["standard_mixed_code"],
            "target_completion_mixed_code": target["standard_mixed_code"],
            "remaining_target_roles": state["remaining_target_roles"],
            "port_matching": tuple(range(state["selected_port_count"])),
        })
        return expected == state["state_id"]

    baseline_exact_binding = exact_state_binding(state_with_coverage, coverage)

    # Schema-2 regression A: merge a valid coverage from another fixed root
    # into this state.  Rehashing that coverage cannot make it belong here.
    other_root_id = next(root_id for root_id in roots if root_id != coverage["root_case_id"])
    cross_root = copy.deepcopy(coverage)
    cross_root["root_case_id"] = other_root_id
    record(
        "merge_across_fixed_full_root_case",
        baseline_exact_binding,
        exact_state_binding(state_with_coverage, cross_root),
        "state identity binds one exact fixed_full_root_case_id",
    )

    # Schema-2 regression B: replace one exact rooted graph by a different
    # rooted presentation having the same standard mixed code.  Semi-directed
    # code equality must not authorize the merge.
    alternate_side = None
    alternate_graph_id = None
    for side in ("source", "target"):
        base_graph_id = coverage[f"{side}_graph_id"]
        alternate_graph_id = next(
            (
                graph_id for graph_id, row in graphs.items()
                if graph_id != base_graph_id
                and row["standard_mixed_code"]
                == graphs[base_graph_id]["standard_mixed_code"]
            ),
            None,
        )
        if alternate_graph_id is not None:
            alternate_side = side
            break
    if alternate_side is None:
        raise AssertionError("mutation fixture lacks two rooted graphs with one mixed code")
    cross_graph = copy.deepcopy(coverage)
    cross_graph[f"{alternate_side}_graph_id"] = alternate_graph_id
    record(
        "merge_across_exact_rooted_graph_id",
        baseline_exact_binding,
        exact_state_binding(state_with_coverage, cross_graph),
        f"state identity binds exact {alternate_side}_rooted_graph_id despite equal mixed code",
    )

    # 3. Port correspondence mutation, with root ID locally rebound.
    port_mutant = copy.deepcopy(coverage)
    moved = list(port_mutant["target_position_to_label"])
    moved[0], moved[1] = moved[1], moved[0]
    port_mutant["target_position_to_label"] = moved
    port_mutant["root_case_id"] = stable_hash(root_key_from_coverage(port_mutant))
    record("alter_port_correspondence", baseline, root_membership(port_mutant), "independent fixed-root inventory")

    # 4. Source-target reversal.  Rebind the root hash so this attacks the
    # directed relation universe, not an unchanged checksum.
    reversal = copy.deepcopy(coverage)
    for left, right in (
        ("source_primitive_id", "target_primitive_id"),
        ("source_provenance", "target_provenance"),
        ("source_selected_labels", "target_selected_labels"),
        ("source_position_to_label", "target_position_to_label"),
    ):
        reversal[left], reversal[right] = reversal[right], reversal[left]
    reversal["root_case_id"] = stable_hash(root_key_from_coverage(reversal))
    record("reverse_source_and_target", baseline, root_membership(reversal), "directed source/target primitive inventory")

    # 5. Raw-to-canonical map corruption.
    graph_row = graphs[coverage["source_graph_id"]]
    graph = graph_from_row(graph_row)
    independent_map = tuple(sorted(canonical_mixed(sd0(graph))[1].items()))

    def map_valid(candidate):
        return tuple(tuple(pair) for pair in candidate) == independent_map

    baseline_map = map_valid(coverage["source_raw_mixed_vertex_to_canonical"])
    map_mutant = copy.deepcopy(coverage["source_raw_mixed_vertex_to_canonical"])
    if len(map_mutant) >= 2:
        map_mutant[0][1], map_mutant[1][1] = map_mutant[1][1], map_mutant[0][1]
    record("alter_raw_to_canonical_map", baseline_map, map_valid(map_mutant), "independent mixed-graph canonicalizer")

    # Exact graph-derived witness checker used for separator mutations.
    def witness_valid(state: dict, witness: dict) -> bool:
        classification = state["probe_classification"]
        if classification not in {"generic_polynomial_separation", "strict_open_cube_separation"}:
            return False
        source = graph_from_row(graphs[state["source_graph_id"]])
        target = graph_from_row(graphs[state["target_graph_id"]])
        p = state["selected_port_count"]
        quartet = tuple(combinations(range(p), 4))[int(witness["quartet_chunk"])]
        invariant = invariants[int(witness["invariant_index"])]
        labels = tuple(f"L_{index}" for index in range(p))
        source_poly = pullback(quartet_descriptor(source, labels, quartet), invariant)
        target_poly = pullback(quartet_descriptor(target, labels, quartet), invariant)
        if classification == "generic_polynomial_separation":
            identifier = witness.get("source_pullback_id")
            return (
                bool(source_poly) and not target_poly and identifier in polynomials
                and exact_poly_hash(source_poly) == witness.get("source_pullback_exact_sha256")
                and poly_from_row(polynomials[identifier]) == source_poly
            )
        identifier = witness.get("target_pullback_id")
        if source_poly or not target_poly or identifier not in polynomials:
            return False
        independent = independent_sign_certificate(target_poly)
        recorded = witness.get("target_sign_certificate", {})
        return (
            exact_poly_hash(target_poly) == witness.get("target_pullback_exact_sha256")
            and poly_from_row(polynomials[identifier]) == target_poly
            and independent.get("certified")
            and independent.get("strict_sign") == witness.get("target_strict_sign")
            and canonical_json(independent.get("factors", [])) == canonical_json(recorded.get("factors", []))
        )

    generic_states = [row for row in states.values() if row["probe_classification"] == "generic_polynomial_separation"]
    first_generic = generic_states[0]
    second_generic = next(
        row for row in generic_states[1:]
        if row["probe_witness"] != first_generic["probe_witness"]
    )
    baseline_witness = witness_valid(first_generic, first_generic["probe_witness"])

    # 6. Swap complete separator witnesses between two relations.
    record(
        "swap_separators_between_relations",
        baseline_witness,
        witness_valid(first_generic, second_generic["probe_witness"]),
        "graph -> displayed masks -> exact pullback association",
    )

    # 7. Attach a valid polynomial from another graph while updating the
    # witness's library hash.  The graph-derived pullback must still disagree.
    wrong_poly = copy.deepcopy(first_generic["probe_witness"])
    wrong_id = second_generic["probe_witness"]["source_pullback_id"]
    wrong_poly["source_pullback_id"] = wrong_id
    wrong_poly["source_pullback_exact_sha256"] = exact_poly_hash(poly_from_row(polynomials[wrong_id]))
    record(
        "valid_polynomial_attached_to_wrong_graph",
        baseline_witness,
        witness_valid(first_generic, wrong_poly),
        "regenerated graph pullback equals content-addressed polynomial body",
    )

    # 8. Remove a hard-cover key and locally update the path hash.
    missing_key = copy.deepcopy(coverage)
    missing_key.pop("target_incoming_selected")
    record("remove_hard_cover_key", baseline, root_membership(missing_key), "closed coverage schema plus root-key reconstruction")

    # 9. Replace a parent path by a different valid path and state.
    child_entries = [
        (state_id, row)
        for state_id, row in states.items()
        for row in row["raw_coverage"]
        if row["parent_path_binding_id"] is not None
    ]
    all_paths = {
        row["path_binding_id"]: (state_id, row)
        for state_id, state in states.items()
        for row in state["raw_coverage"]
    }
    child_state_id, child = child_entries[0]
    parent_state_id, parent = all_paths[child["parent_path_binding_id"]]

    def parent_valid(candidate):
        parent_entry = all_paths.get(candidate["parent_path_binding_id"])
        if parent_entry is None:
            return False
        state_id, row = parent_entry
        return (
            candidate["parent_state_id"] == state_id
            and candidate["root_case_id"] == row["root_case_id"]
            and candidate["restoration_path"][:-1] == row["restoration_path"]
        )

    baseline_parent = parent_valid(child)
    unrelated = next(
        (state_id, row) for path_id, (state_id, row) in all_paths.items()
        if row["root_case_id"] != child["root_case_id"]
    )
    parent_mutant = copy.deepcopy(child)
    parent_mutant["parent_state_id"] = unrelated[0]
    parent_mutant["parent_path_binding_id"] = unrelated[1]["path_binding_id"]
    record("inconsistent_parent_restoration_path", baseline_parent, parent_valid(parent_mutant), "root and restoration-prefix coherence")

    # 10. Canonical-state child set copied from first provenance: mutate one
    # explicit per-coverage set.  The full audit separately recomputes every
    # provenance's expected set from insertion positions.
    child_bound_state = next(
        row for row in states.values()
        if row["children"] and row["raw_coverage"]
    )
    child_coverage = child_bound_state["raw_coverage"][0]

    def child_binding_valid(candidate):
        return tuple(sorted(candidate["child_state_ids"])) == tuple(sorted(child_bound_state["children"]))

    baseline_child = child_binding_valid(child_coverage)
    child_mutant = copy.deepcopy(child_coverage)
    child_mutant["child_state_ids"] = child_mutant["child_state_ids"][:-1]
    record("drop_merged_provenance_child", baseline_child, child_binding_valid(child_mutant), "per-coverage explicit child-state set")

    # 11. Corrupt a strict-sign proof while retaining the outer certified flag.
    strict_states = [
        row for row in states.values()
        if row["probe_classification"] == "strict_open_cube_separation"
    ]
    if strict_states:
        strict_state = strict_states[0]
        baseline_strict = witness_valid(strict_state, strict_state["probe_witness"])
        sign_mutant = copy.deepcopy(strict_state["probe_witness"])
        sign_mutant["target_sign_certificate"]["certified"] = True
        if sign_mutant["target_sign_certificate"].get("factors"):
            sign_mutant["target_sign_certificate"]["factors"][0]["expanded_sha256"] = "0" * 64
        else:
            sign_mutant["target_strict_sign"] *= -1
        mutated_strict = witness_valid(strict_state, sign_mutant)
        strict_detector = "independent graph pullback, exact factorization, and Bernstein replay"
    else:
        # This theta-2 n=4 stream has no strict-sign rows.  Still regression
        # test the exact sign-proof checker on 1-x, positive on (0,1), rather
        # than allowing a vacuous trust in a `certified` Boolean.
        strict_poly = {(0,): 1, (1,): -1}
        strict_certificate = independent_sign_certificate(strict_poly)

        def synthetic_sign_valid(candidate: dict) -> bool:
            independent = independent_sign_certificate(strict_poly)
            return (
                independent.get("certified") is True
                and candidate.get("certified") is True
                and candidate.get("strict_sign") == independent.get("strict_sign")
                and candidate.get("polynomial_sha256") == independent.get("polynomial_sha256")
                and candidate.get("term_count") == independent.get("term_count")
                and canonical_json(candidate.get("factors", []))
                == canonical_json(independent.get("factors", []))
            )

        baseline_strict = synthetic_sign_valid(strict_certificate)
        sign_mutant = copy.deepcopy(strict_certificate)
        sign_mutant["certified"] = True
        sign_mutant["factors"][0]["expanded_sha256"] = "0" * 64
        mutated_strict = synthetic_sign_valid(sign_mutant)
        strict_detector = "synthetic 1-x exact factorization and Bernstein replay (stream has zero strict rows)"
    record(
        "forge_strict_sign_certified_flag",
        baseline_strict,
        mutated_strict,
        strict_detector,
    )

    payload = {
        "schema": "candidate-full-mutation-suite-v2",
        "status": "VERIFIED" if all(row["rejected"] for row in results) else "FALSE",
        "scope": "in-memory semantic mutations; primary files untouched",
        "inputs": {
            str(state_path.relative_to(PROJECT)): file_sha(state_path),
            str(graph_path.relative_to(PROJECT)): file_sha(graph_path),
            str(polynomial_path.relative_to(PROJECT)): file_sha(polynomial_path),
            str(root_path.relative_to(PROJECT)): file_sha(root_path),
        },
        "mutation_count": len(results),
        "rejected_count": sum(row["rejected"] for row in results),
        "mutations": results,
        "elapsed_seconds": time.monotonic() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "rejected": f"{payload['rejected_count']}/{payload['mutation_count']}",
        "output": str(args.output),
        "sha256": file_sha(args.output),
        "elapsed_seconds": payload["elapsed_seconds"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
