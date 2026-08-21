#!/usr/bin/env python3
"""Read-only replay of the root/probe claims used by Outcome P.

The historical ``verify_all.py`` also audits superseded primary atlas streams
and is intentionally scope-limited.  This active verifier regenerates only
the independently proved structural root, incoming-role, probe-coherence, and
path-product submersion certificates.  It writes exclusively to a temporary
directory and requires byte-for-byte agreement with the committed records.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run(*args: str) -> None:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    subprocess.run([sys.executable, *args], cwd=HERE, env=env, check=True)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compare(generated: Path, committed: Path) -> None:
    require(generated.read_bytes() == committed.read_bytes(),
            f"regenerated certificate differs: {committed.relative_to(PROJECT)}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="stc-jc-root-probe-") as raw:
        tmp = Path(raw)
        root_path = tmp / "root.json"
        probe_path = tmp / "probe.json"
        incoming_path = tmp / "incoming.json"
        counterexample_path = tmp / "incoming_counterexample.json"
        parameter_path = tmp / "parameter.json"

        run("verify_root_probe.py", "--output", str(root_path))
        run("verify_probe_coherence.py", "--output", str(probe_path))
        run(
            "verify_incoming_coverage.py",
            "--output", str(incoming_path),
            "--counterexample-output", str(counterexample_path),
        )
        run(
            "verify_parameter_submersion.py",
            "--core-certificate",
            str(PROJECT / "primary/certificates/core_universe.json"),
            "--output", str(parameter_path),
        )

        compare(root_path, HERE / "root_probe_certificate.json")
        compare(probe_path, HERE / "probe_coherence_certificate.json")
        compare(incoming_path, HERE / "incoming_coverage_certificate.json")
        compare(
            counterexample_path,
            HERE / "counterexamples/fixed_incoming_relative_role.json",
        )
        compare(parameter_path, HERE / "parameter_submersion_certificate.json")

        root = load(root_path)["summary"]
        require(root["theta_core_count"] == 4, "theta core count changed")
        require(root["two_reticulate_branch_class_count"] == 0,
                "forbidden two-reticulate-branch core appeared")
        require(root["root_move_failure_count"] == 0, "root move failure")
        require(root["intrinsic_criterion_mismatch_count"] == 0,
                "repair/root census mismatch")
        require(root["k4_minus_edge_tree_child_rootings"] == 0,
                "double-triangle K4-e acquired a tree-child rooting")
        require(all(value == 1 for rows in root["support_stabilizers"]
                    for value in rows), "support rigidity changed")

        probe = load(probe_path)
        require(probe["one_port_ambiguity_group_count"] == 372,
                "one-port ambiguity census changed")
        require(probe["one_port_max_two_port_completion_multiplicity"] == 2,
                "one-port completion multiplicity changed")
        require(
            probe["two_port_full_graph_bindings"]
            == probe["two_extra_port_presentation_count"],
            "two-port binding coverage changed",
        )
        require(probe["max_eligible_triangle_count_in_any_probe"] <= 1,
                "multiple probe triangles")
        require(all(row["collision_count"] == 0
                    for row in probe["abstract_three_extra_label_checks"]),
                "word-order deck collision")

        incoming = load(incoming_path)
        require(
            incoming["boundary_bijection_counts"][
                "bijections_without_common_rootable_boundary"
            ] == 144,
            "incoming-role counterexample census changed",
        )
        require(
            incoming["verdicts"][
                "anchored_source_full_target_boundary_permutations_exhaustive"
            ] == "VERIFIED",
            "full target boundary quotient is no longer exhaustive",
        )
        require(incoming["group_action_check"]["counterexample_in_full_group"],
                "incoming-role counterexample left the full target group")
        require(not incoming["group_action_check"][
            "counterexample_in_fixed_incoming_subgroup"
        ], "false fixed-incoming quotient was restored")

        parameter = load(parameter_path)
        require(parameter["full_row_rank_failure_count"] == 0,
                "path-product submersion rank failure")
        require(
            parameter["raw_to_normalized_class_reduction_counts"]
            == {"1": 14878, "2": 27806, "3": 208, "4": 16},
            "zero-sum split/complement normalization census changed",
        )
        require(
            parameter["general_open_product_certificate"][
                "jacobian_constructed_and_ranked_over_Q"
            ],
            "product-map Jacobian was not independently ranked",
        )
        require(
            parameter["normalization_mutation_tests"][
                "all_mutations_rejected"
            ],
            "zero-sum normalization mutations were not rejected",
        )
        require(parameter["input_stable_during_run"],
                "parameter-submersion input changed during replay")

        print(json.dumps({
            "status": "VERIFIED",
            "scope": (
                "active root reduction, incoming role, honest one-port ambiguity "
                "diagnostics, pair-order sanity checks, and submersion"
            ),
            "root_certificate_sha256": sha256(root_path),
            "probe_presentations": probe["two_extra_port_presentation_count"],
            "incoming_bijections": incoming["boundary_bijection_counts"][
                "ordered_support_boundary_bijections"
            ],
            "submersion_completions": parameter["completion_count"],
        }, sort_keys=True))


if __name__ == "__main__":
    main()
