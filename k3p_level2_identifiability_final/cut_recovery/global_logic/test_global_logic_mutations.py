#!/usr/bin/env python3
"""Adversarial mutations for the K3P directed-cut global-logic report."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from verify_global_logic import HERE, REPORT, validate_report


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    baseline = json.loads(Path(REPORT).read_text(encoding="utf-8"))
    validate_report(baseline)

    mutations = []

    def add(name, mutate):
        candidate = copy.deepcopy(baseline)
        mutate(candidate)
        mutations.append((name, candidate))

    add("promote_k3p_same", lambda d: d.__setitem__("k3p_same_status", "CERTIFIED"))
    add("reverse_source_target", lambda d: d["directed_relation"].update(
        {"source": "N_prime", "target": "N"}))
    add("assume_target_regular", lambda d: d["directed_relation"].__setitem__(
        "target_regular_not_assumed", False))
    add("forbid_larger_target", lambda d: d["directed_relation"].__setitem__(
        "target_dimension_may_be_larger", False))
    add("reverse_proved_inclusion", lambda d: d["generic_cut_consequences"].__setitem__(
        "proved_inclusion", "Cut(N)_subseteq_Cut(N_prime)"))
    add("promote_reverse_inclusion", lambda d: d["generic_cut_consequences"].__setitem__(
        "reverse_inclusion_proved", True))
    add("invent_equal_dimensions", lambda d: d["generic_cut_consequences"].__setitem__(
        "equal_image_dimension_is_available", True))
    add("delete_bridge_precondition", lambda d: d["localization_scope"].__setitem__(
        "common_bridge_tree_required", False))
    add("extend_atlas_without_evidence", lambda d: d["localization_scope"].__setitem__(
        "existing_atlas_closes_missing_scope", True))
    add("change_atlas_source_scope", lambda d: d["localization_scope"].__setitem__(
        "existing_atlas_source_scope", "arbitrary_multi_blob_network"))
    add("mislabel_outer_witness_strong", lambda d: d["exact_inference_counterexample"].__setitem__(
        "strong_class_counterexample", True))
    add("weaken_target_rank", lambda d: d["exact_inference_counterexample"].__setitem__(
        "target_rank", 14))
    add("change_source_rank", lambda d: d["exact_inference_counterexample"].__setitem__(
        "source_rank", 10))
    add("drop_required_repair", lambda d: d["sufficient_repairs"].pop())

    rejected = []
    for name, candidate in mutations:
        try:
            validate_report(candidate)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise RuntimeError(f"mutation escaped validation: {name}")

    require(len(rejected) == len(mutations), "not all mutations were rejected")
    stored = json.loads((HERE / "MUTATION_RESULTS.json").read_text(encoding="utf-8"))
    require(stored.get("schema") == "k3p-cut-global-logic-mutations-v1",
            "wrong mutation-results schema")
    require(stored.get("baseline_passed") is True,
            "stored baseline result changed")
    require(stored.get("mutations_attempted") == len(mutations),
            "stored mutation-attempt count changed")
    require(stored.get("mutations_rejected") == len(rejected),
            "stored mutation-rejection count changed")
    require(stored.get("escaped") == 0, "stored escaped-mutation count changed")
    require(stored.get("rejected") == rejected, "stored rejected-mutation list changed")
    print(f"GLOBAL LOGIC MUTATIONS PASS: {len(rejected)}/{len(mutations)} rejected")
    for name in rejected:
        print(f"  rejected {name}")


if __name__ == "__main__":
    main()
