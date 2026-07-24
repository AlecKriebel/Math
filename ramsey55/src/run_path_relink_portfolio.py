#!/usr/bin/env python3
"""Run and verify the preregistered aligned path-relinking portfolio."""

from __future__ import annotations

import argparse
import json
import shutil
import statistics
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from graph_io import read_graph  # noqa: E402
from run_conflict_block_pilot import (  # noqa: E402
    checked_json,
    directory_bytes,
    run_process,
    sha256,
    write_json,
)


def edge_hamming(left: list[int], right: list[int]) -> int:
    return sum(
        ((left[a] >> b) & 1) != ((right[a] >> b) & 1)
        for a in range(len(left))
        for b in range(a + 1, len(left))
    )


def numeric_summary(values: list[int]) -> dict[str, float | int] | None:
    if not values:
        return None
    return {
        "minimum": min(values),
        "maximum": max(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
    }


def verify_final(
    *,
    candidate: Path,
    child: Path,
    parent_a: Path,
    parent_b: Path,
    search_json: Path,
    run_dir: Path,
    expected: dict[str, object],
    plan: dict[str, object],
) -> dict[str, object]:
    python_run = run_process(
        [
            sys.executable,
            plan["verification"]["python_source"],
            str(candidate.relative_to(ROOT)),
        ],
        allowed=(0, 1),
        timeout=120,
    )
    python_result = checked_json(python_run.stdout, "Python graph verifier")
    python_path = run_dir / "final.python.json"
    python_sha = write_json(python_path, python_result)

    cpp_run = run_process(
        [
            str(ROOT / plan["verification"]["bitset_binary"]),
            str(candidate.relative_to(ROOT)),
        ],
        allowed=(0, 1),
        timeout=120,
    )
    cpp_result = checked_json(cpp_run.stdout, "C++ graph verifier")
    cpp_path = run_dir / "final.cpp.json"
    cpp_sha = write_json(cpp_path, cpp_result)

    structural_path = run_dir / "final.structural.json"
    structural_run = run_process(
        [
            sys.executable,
            plan["verification"]["structural_source"],
            str(candidate.relative_to(ROOT)),
            "--child",
            str(child.relative_to(ROOT)),
            "--parent-a",
            str(parent_a.relative_to(ROOT)),
            "--parent-b",
            str(parent_b.relative_to(ROOT)),
            "--search-json",
            str(search_json.relative_to(ROOT)),
            "--output",
            str(structural_path.relative_to(ROOT)),
        ],
        allowed=(0,),
        timeout=180,
    )
    structural = checked_json(
        structural_run.stdout, "independent path-relink structural audit"
    )

    objective = int(expected["E"])
    cliques = int(expected["C5"])
    independent = int(expected["I5"])
    if (
        python_result.get("objective") != objective
        or python_result.get("clique_count") != cliques
        or python_result.get("independent_count") != independent
        or structural.get("E") != objective
        or structural.get("C5") != cliques
        or structural.get("I5") != independent
        or structural.get("accepted") is not True
        or cpp_result.get("clique_k_found") != (cliques > 0)
        or cpp_result.get("independent_k_found") != (independent > 0)
        or python_result.get("valid") != (objective == 0)
        or cpp_result.get("valid") != (objective == 0)
    ):
        raise RuntimeError("independent path-relink verification disagrees")
    return {
        "candidate": str(candidate.relative_to(ROOT)),
        "candidate_sha256": sha256(candidate),
        "child": str(child.relative_to(ROOT)),
        "child_sha256": sha256(child),
        "E": objective,
        "C5": cliques,
        "I5": independent,
        "conflict_topology": structural["conflict_topology"],
        "python_verifier": str(python_path.relative_to(ROOT)),
        "python_verifier_sha256": python_sha,
        "cpp_verifier": str(cpp_path.relative_to(ROOT)),
        "cpp_verifier_sha256": cpp_sha,
        "structural_verifier": str(structural_path.relative_to(ROOT)),
        "structural_verifier_sha256": sha256(structural_path),
        "verified": True,
    }


def certify_construction(
    *,
    candidate: Path,
    job_label: str,
    seed: int,
    plan: dict[str, object],
) -> dict[str, object]:
    canonical = (
        ROOT
        / f"results/best_candidates/path_relink_{job_label}_seed_"
        f"{seed}.canonical.json"
    )
    run_process(
        [
            sys.executable,
            "src/export_artifact.py",
            str(candidate.relative_to(ROOT)),
            str(canonical.relative_to(ROOT)),
            "--source",
            "aligned_path_relink_minconflicts_v1",
            "--seed",
            str(seed),
        ],
        allowed=(0,),
        timeout=120,
    )
    audit_dir = ROOT / f"results/audit/path_relink_{job_label}_seed_{seed}"
    audit_run = run_process(
        [
            sys.executable,
            "verify/adversarial_audit.py",
            str(candidate.relative_to(ROOT)),
            "--json-copy",
            str(canonical.relative_to(ROOT)),
            "--seed",
            str(seed),
            "--output-dir",
            str(audit_dir.relative_to(ROOT)),
            "--cpp",
            plan["verification"]["bitset_binary"],
        ],
        allowed=(0,),
        timeout=300,
    )
    audit = checked_json(audit_run.stdout, "adversarial path-relink audit")
    if audit.get("status") != "PASS":
        raise RuntimeError("E=0 path-relink adversarial audit failed")
    audit_path = (
        ROOT
        / f"results/verification/path_relink_{job_label}_seed_"
        f"{seed}.adversarial.json"
    )
    audit_sha = write_json(audit_path, audit)
    return {
        "candidate": str(candidate.relative_to(ROOT)),
        "canonical": str(canonical.relative_to(ROOT)),
        "canonical_sha256": sha256(canonical),
        "adversarial_audit": str(audit_path.relative_to(ROOT)),
        "adversarial_audit_sha256": audit_sha,
        "status": "CERTIFIED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan["status"] != "PREREGISTERED_BEFORE_PRODUCTION_RUNS":
        raise SystemExit("plan does not authorize production searches")
    for record in plan["pinned_files"]:
        path = ROOT / record["path"]
        if sha256(path) != record["sha256"]:
            raise SystemExit(f"pinned hash mismatch: {path}")
    binary = ROOT / plan["binary"]["path"]
    if sha256(binary) != plan["binary"]["sha256"]:
        raise SystemExit("compiled path-relink binary hash mismatch")
    disk_free_before = shutil.disk_usage(ROOT).free
    disk_required_before = (
        int(plan["storage_limit_bytes"])
        + int(plan["disk_reserve_bytes_after_registered_cap"])
    )
    if disk_free_before < disk_required_before:
        raise SystemExit(
            "disk reserve gate failed: "
            f"{disk_free_before} free bytes < {disk_required_before} required"
        )

    pair_audit_path = ROOT / plan["pairing"]["audit"]
    pair_audit = json.loads(pair_audit_path.read_text(encoding="utf-8"))
    if (
        sha256(pair_audit_path) != plan["pairing"]["audit_sha256"]
        or pair_audit.get("selected_pair_count") != 11
    ):
        raise SystemExit("pair audit does not match the registered portfolio")
    elite_by_line = {
        int(item["catalog_line"]): item for item in pair_audit["elites"]
    }
    jobs: list[dict[str, object]] = []
    next_seed = int(plan["pairing"]["production_seed_base"])
    for pair_index, pair in enumerate(
        pair_audit["selected_pairs"], start=1
    ):
        left_line = int(pair["left_catalog_line"])
        right_line = int(pair["right_catalog_line"])
        parent_a = elite_by_line[left_line]
        parent_b = elite_by_line[right_line]
        mapping = [int(value) for value in pair["right_vertex_for_left_label"]]
        disagreement = int(pair["aligned_hamming"])
        alignment_policy = "local_swap_minimum"
        if disagreement == 0:
            if (
                plan["pairing"]["zero_alignment_policy"]
                != "identity_embedding"
            ):
                raise SystemExit("unsupported zero-alignment policy")
            mapping = list(range(43))
            disagreement = int(pair["oriented_labeled_hamming"])
            alignment_policy = (
                "identity_embedding_fallback_for_isomorphic_pair"
            )
        for direction in ("a_to_b", "b_to_a"):
            jobs.append(
                {
                    "label": (
                        f"pair_{pair_index:02d}_{left_line:03d}_"
                        f"{right_line:03d}_{direction}"
                    ),
                    "pair_index": pair_index,
                    "left_catalog_line": left_line,
                    "right_catalog_line": right_line,
                    "parent_a": parent_a["path"],
                    "parent_a_sha256": parent_a["sha256"],
                    "parent_b": parent_b["path"],
                    "parent_b_sha256": parent_b["sha256"],
                    "complement_a": parent_a[
                        "complemented_to_C5_only"
                    ],
                    "complement_b": parent_b[
                        "complemented_to_C5_only"
                    ],
                    "alignment_policy": alignment_policy,
                    "mapping": mapping,
                    "effective_parent_disagreement": disagreement,
                    "direction": direction,
                    "seed": next_seed,
                }
            )
            next_seed += 1
    if len(jobs) != plan["registered_run_count"]:
        raise SystemExit("registered job count mismatch")
    if len({int(job["seed"]) for job in jobs}) != len(jobs):
        raise SystemExit("production seeds are not unique")
    output_root = ROOT / plan["output_root"]
    search = plan["search"]
    runs: list[dict[str, object]] = []
    certified: dict[str, object] | None = None

    for job in jobs:
        if certified is not None:
            break
        parent_a = ROOT / job["parent_a"]
        parent_b = ROOT / job["parent_b"]
        if (
            sha256(parent_a) != job["parent_a_sha256"]
            or sha256(parent_b) != job["parent_b_sha256"]
        ):
            raise SystemExit(f"parent hash mismatch: {job['label']}")
        mapping = [int(value) for value in job["mapping"]]
        if sorted(mapping) != list(range(43)):
            raise SystemExit(f"invalid mapping: {job['label']}")

        run_dir = output_root / job["label"]
        run_dir.mkdir(parents=True, exist_ok=True)
        candidate = run_dir / "final.g6"
        child = run_dir / "child.g6"
        search_json = run_dir / "search.json"
        for path in (candidate, child, search_json):
            if path.exists():
                raise SystemExit(
                    f"refusing to overwrite preregistered output: {path}"
                )
        command = [
            str(binary),
            "--parent-a",
            str(parent_a.relative_to(ROOT)),
            "--parent-b",
            str(parent_b.relative_to(ROOT)),
            "--complement-a",
            "1" if job["complement_a"] else "0",
            "--complement-b",
            "1" if job["complement_b"] else "0",
            "--mapping",
            ",".join(str(value) for value in mapping),
            "--direction",
            job["direction"],
            "--seed",
            str(job["seed"]),
            "--steps",
            str(search["steps"]),
            "--path-sample",
            str(search["path_sample"]),
            "--path-flips",
            str(search["path_flips"]),
            "--tabu-tenure",
            str(search["tabu_tenure"]),
            "--random-walk-per-million",
            str(search["random_walk_per_million"]),
            "--breakout-interval",
            str(search["breakout_interval"]),
            "--agreement-penalty",
            str(search["agreement_penalty"]),
            "--corridor-penalty",
            str(search["corridor_penalty"]),
            "--full-audit-interval",
            str(search["full_audit_interval"]),
            "--output",
            str(candidate.relative_to(ROOT)),
            "--child-output",
            str(child.relative_to(ROOT)),
            "--json-output",
            str(search_json.relative_to(ROOT)),
        ]
        search_run = run_process(
            command,
            allowed=(0,),
            timeout=float(plan["per_run_wall_limit_seconds"]),
        )
        search_result = checked_json(search_run.stdout, "path-relink search")
        if json.loads(search_json.read_text(encoding="utf-8")) != search_result:
            raise RuntimeError("stdout and retained path-relink JSON differ")
        if (
            search_result.get("parent_a_E") != 2
            or search_result.get("parent_b_E") != 2
            or search_result.get("parent_disagreement")
            != job["effective_parent_disagreement"]
        ):
            raise RuntimeError("path-relink parent facts disagree with plan")

        verification = verify_final(
            candidate=candidate,
            child=child,
            parent_a=parent_a,
            parent_b=parent_b,
            search_json=search_json,
            run_dir=run_dir,
            expected=search_result,
            plan=plan,
        )
        objective = int(search_result["E"])
        record: dict[str, object] = {
            "label": job["label"],
            "pair_index": job["pair_index"],
            "left_catalog_line": job["left_catalog_line"],
            "right_catalog_line": job["right_catalog_line"],
            "direction": job["direction"],
            "seed": job["seed"],
            "alignment_policy": job["alignment_policy"],
            "parent_disagreement": search_result["parent_disagreement"],
            "child_E": search_result["child_E"],
            "child_C5": search_result["child_C5"],
            "child_I5": search_result["child_I5"],
            "child_distance_a": search_result["child_distance_a"],
            "child_distance_b": search_result["child_distance_b"],
            "child_agreement_breaks": search_result[
                "child_agreement_breaks"
            ],
            "E": objective,
            "C5": search_result["C5"],
            "I5": search_result["I5"],
            "distance_a": search_result["distance_a"],
            "distance_b": search_result["distance_b"],
            "agreement_breaks": search_result["agreement_breaks"],
            "steps_executed": search_result["steps_executed"],
            "delta_evaluations": search_result["delta_evaluations"],
            "strict_improvements": search_result["strict_improvements"],
            "runtime_seconds": search_result["runtime_seconds"],
            "child": str(child.relative_to(ROOT)),
            "child_sha256": sha256(child),
            "final_candidate": str(candidate.relative_to(ROOT)),
            "final_candidate_sha256": sha256(candidate),
            "search_json": str(search_json.relative_to(ROOT)),
            "search_json_sha256": sha256(search_json),
            "verification": verification,
            "evidence_label": (
                "CERTIFIED"
                if objective == 0
                else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
            ),
        }
        runs.append(record)
        if directory_bytes(output_root) > plan["storage_limit_bytes"]:
            raise RuntimeError("path-relink artifact storage limit exceeded")
        disk_free_now = shutil.disk_usage(ROOT).free
        if disk_free_now < plan["disk_reserve_bytes_after_registered_cap"]:
            raise RuntimeError(
                "path-relink disk reserve was consumed during the portfolio"
            )
        if objective == 0:
            certified = certify_construction(
                candidate=candidate,
                job_label=job["label"],
                seed=int(job["seed"]),
                plan=plan,
            )
            record["construction_certification"] = certified
            break

    completed = len(runs)
    topologies = [
        item["verification"]["conflict_topology"] for item in runs
    ]
    e2_topologies = [
        topology
        for item, topology in zip(runs, topologies)
        if int(item["E"]) == 2
    ]
    final_graphs = [
        read_graph(ROOT / str(item["final_candidate"])) for item in runs
    ]
    pairwise = [
        edge_hamming(final_graphs[left], final_graphs[right])
        for left in range(len(final_graphs))
        for right in range(left + 1, len(final_graphs))
    ]
    summary = {
        "schema": "ramsey55.path_relink_portfolio_result.v1",
        "evidence_label": (
            "CERTIFIED"
            if certified is not None
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "claim_boundary": (
            "Only an E=0 graph accepted by both full graph verifiers, the "
            "independent path/crossover audit, canonical export, and the "
            "adversarial audit is a certified construction. Nonzero results "
            "are bounded search observations."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "registered_run_count": len(jobs),
        "completed_run_count": completed,
        "stopped_early_on_E0": certified is not None,
        "best_objective": min(int(item["E"]) for item in runs),
        "E0_count": sum(int(item["E"]) == 0 for item in runs),
        "E1_count": sum(int(item["E"]) == 1 for item in runs),
        "E2_count": sum(int(item["E"]) == 2 for item in runs),
        "construction": certified,
        "topology": {
            "E2_output_count": len(e2_topologies),
            "E2_mixed_color_count": sum(
                topology.get("mixed_colors") is True
                for topology in e2_topologies
            ),
            "E2_overlap_le_3_count": sum(
                isinstance(topology.get("pair_overlap"), int)
                and int(topology["pair_overlap"]) <= 3
                for topology in e2_topologies
            ),
            "E2_same_color_overlap_4_count": sum(
                topology.get("mixed_colors") is False
                and topology.get("pair_overlap") == 4
                for topology in e2_topologies
            ),
        },
        "child_objective": numeric_summary(
            [int(item["child_E"]) for item in runs]
        ),
        "final_parent_distance": {
            "minimum_to_either_parent": numeric_summary(
                [
                    min(int(item["distance_a"]), int(item["distance_b"]))
                    for item in runs
                ]
            ),
            "maximum_to_either_parent": numeric_summary(
                [
                    max(int(item["distance_a"]), int(item["distance_b"]))
                    for item in runs
                ]
            ),
        },
        "distinct_raw_final_graph_count": len(
            {str(item["final_candidate_sha256"]) for item in runs}
        ),
        "pairwise_labeled_final_hamming": numeric_summary(pairwise),
        "pairwise_final_pair_count": len(pairwise),
        "total_steps_executed": sum(
            int(item["steps_executed"]) for item in runs
        ),
        "total_delta_evaluations": sum(
            int(item["delta_evaluations"]) for item in runs
        ),
        "total_runtime_seconds": sum(
            float(item["runtime_seconds"]) for item in runs
        ),
        "artifact_bytes": directory_bytes(output_root),
        "storage_limit_bytes": plan["storage_limit_bytes"],
        "disk_free_bytes_before_launch": disk_free_before,
        "disk_free_bytes_after_run": shutil.disk_usage(ROOT).free,
        "disk_reserve_bytes_after_registered_cap": plan[
            "disk_reserve_bytes_after_registered_cap"
        ],
        "runs": runs,
    }
    write_json(ROOT / plan["summary_output"], summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
