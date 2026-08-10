#!/usr/bin/env python3
"""Replay every clean verifier and enforce the review's exact assertions."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


def run(*args: str) -> None:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([sys.executable, *args], cwd=HERE, env=env, check=True)


def load(name: str) -> dict:
    return json.loads((HERE / name).read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    run("verify_root_probe.py", "--output", "root_probe_certificate.json")
    run("verify_probe_coherence.py", "--output", "probe_coherence_certificate.json")
    run(
        "verify_incoming_coverage.py",
        "--output", "incoming_coverage_certificate.json",
        "--counterexample-output", "counterexamples/fixed_incoming_relative_role.json",
    )
    run(
        "verify_parameter_submersion.py",
        "--core-certificate", str(REPO / "primary/certificates/core_universe.json"),
        "--output", "parameter_submersion_certificate.json",
    )
    run(
        "verify_redstar_partition.py",
        "--repo", str(REPO),
        "--output", "redstar_partition_certificate.json",
    )
    run(
        "verify_primary_artifacts.py",
        "--repo", str(REPO),
        "--output", "primary_artifact_audit.json",
    )

    root = load("root_probe_certificate.json")
    require(root["summary"]["theta_core_count"] == 4, "theta core count")
    require(root["summary"]["two_reticulate_branch_class_count"] == 0, "RR branch case")
    require(root["summary"]["root_move_failure_count"] == 0, "root move")
    require(root["summary"]["intrinsic_criterion_mismatch_count"] == 0, "repair/root census")
    require(root["summary"]["k4_minus_edge_tree_child_rootings"] == 0, "K4-e")
    require(all(x == 1 for rows in root["summary"]["support_stabilizers"] for x in rows), "support rigidity")
    require(root["summary"]["sink_omission_is_intrinsically_strong"], "sink omission boundary case")
    require(not root["summary"]["sink_omission_preserves_core"], "sink omission must lose core")

    probe = load("probe_coherence_certificate.json")
    require(probe["coherence_collision_count"] == 0, "probe coherence")
    require(probe["max_eligible_triangle_count_in_any_probe"] <= 1, "one triangle")
    require(all(row["collision_count"] == 0 for row in probe["abstract_three_extra_label_checks"]), "word order deck")

    incoming = load("incoming_coverage_certificate.json")
    require(
        incoming["boundary_bijection_counts"]["bijections_without_common_rootable_boundary"] > 0,
        "fixed-incoming counterexample",
    )
    require(
        incoming["verdicts"]["individual_rootability_implies_common_rootability"] == "FALSE",
        "common incoming quantifier",
    )
    require(
        not incoming["group_action_check"]["counterexample_in_fixed_incoming_subgroup"],
        "counterexample must leave outgoing-only subgroup",
    )
    require(
        incoming["group_action_check"]["counterexample_in_full_group"],
        "full target group must recover counterexample role",
    )

    parameter = load("parameter_submersion_certificate.json")
    require(parameter["full_row_rank_failure_count"] == 0, "parameter submersion")
    require(parameter["input_stable_during_run"], "parameter input changed")

    redstar = load("redstar_partition_certificate.json")
    require(redstar["partition"]["descriptor_partition_failure_count"] == 0, "red_* partition")
    require(redstar["routing"]["all_source_routing_checks_pass"], "nonretaining route")
    require(redstar["core_input_stable"], "red_* core input changed")

    primary = load("primary_artifact_audit.json")
    require(primary["inputs_stable_during_run"], "primary inputs changed")
    require(primary["core"]["canonical_universes_equal"], "primary core universe")
    require(not primary["core"]["repair_mismatches"], "primary repairs")
    require(primary["completion"]["all_counts_match"], "completion counts")
    require(not primary["support"]["validation_failures"], "primary supports")
    require(not primary["support"]["t_quotient_pointwise_stabilizer_exceptions"], "T pointwise stabilizer")
    require(primary["simultaneous_label_quotient"]["source_text"]["all_checks_pass"], "label quotient source")
    require(all(row["exhaustive"] for row in primary["simultaneous_label_quotient"]["transversal_table"]), "label quotient group action")

    print(json.dumps({
        "status": "PASS",
        "hard_cover_contract_satisfied": redstar["routing"]["hard_cover_contract_satisfied"],
        "note": "Structural PASS does not promote the local theorem when hard_cover_contract_satisfied is false.",
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
