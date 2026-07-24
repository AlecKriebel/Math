#!/usr/bin/env python3
"""Run the preregistered conflict-block follow-up on 22 E=2 starts."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

from graph_io import read_graph
from run_conflict_block_pilot import (
    ROOT,
    certify_construction,
    checked_json,
    directory_bytes,
    run_process,
    sha256,
    verify_candidate,
    write_json,
)


def edge_hamming(left: list[int], right: list[int]) -> int:
    if len(left) != len(right):
        raise ValueError("graphs have different orders")
    return sum(
        ((left[a] >> b) & 1) != ((right[a] >> b) & 1)
        for a in range(len(left))
        for b in range(a + 1, len(left))
    )


def color_side(cliques: int, independent: int) -> str:
    if cliques == 0 and independent == 0:
        return "E0"
    if cliques > 0 and independent == 0:
        return "C5_only"
    if cliques == 0 and independent > 0:
        return "I5_only"
    return "mixed"


def numeric_summary(values: list[int]) -> dict[str, float | int] | None:
    if not values:
        return None
    return {
        "minimum": min(values),
        "maximum": max(values),
        "mean": statistics.mean(values),
        "median": statistics.median(values),
    }


def rate(count: int, denominator: int) -> dict[str, float | int | None]:
    return {
        "count": count,
        "denominator": denominator,
        "rate": count / denominator if denominator else None,
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
        raise SystemExit("compiled search binary hash mismatch")

    if len(plan["starts"]) != 22:
        raise SystemExit("follow-up plan must contain exactly 22 starts")
    if len({int(item["catalog_line"]) for item in plan["starts"]}) != 22:
        raise SystemExit("catalog lines are not unique")
    if len({int(item["seed"]) for item in plan["starts"]}) != 22:
        raise SystemExit("production seeds are not unique")
    for start in plan["starts"]:
        base = ROOT / start["path"]
        if sha256(base) != start["sha256"]:
            raise SystemExit(f"start hash mismatch: {base}")
        if int(start["C5"]) + int(start["I5"]) != 2 or start["E"] != 2:
            raise SystemExit(f"start is not registered at E=2: {base}")

    output_root = ROOT / plan["output_root"]
    search = plan["search"]
    runs: list[dict[str, object]] = []
    certified: dict[str, object] | None = None

    for start in plan["starts"]:
        if certified is not None:
            break
        label = str(start["label"])
        seed = int(start["seed"])
        base = ROOT / start["path"]
        run_dir = output_root / label
        run_dir.mkdir(parents=True, exist_ok=True)
        candidate = run_dir / "final.g6"
        search_json = run_dir / "search.json"
        for path in (candidate, search_json):
            if path.exists():
                raise SystemExit(
                    f"refusing to overwrite preregistered output: {path}"
                )

        command = [
            str(binary),
            "--seed-graph",
            str(base.relative_to(ROOT)),
            "--seed",
            str(seed),
            "--steps",
            str(search["steps_per_restart"]),
            "--restarts",
            str(search["restarts"]),
            "--block2-samples",
            str(search["block2_samples"]),
            "--block3-samples",
            str(search["block3_samples"]),
            "--pair-samples",
            str(search["pair_samples"]),
            "--global-samples",
            str(search["global_samples"]),
            "--noise-per-million",
            str(search["noise_per_million"]),
            "--degree-penalty-weight",
            str(search["degree_penalty_weight"]),
            "--breakout-interval",
            str(search["breakout_interval"]),
            "--shake-interval",
            str(search["shake_interval"]),
            "--shake-conflicts",
            str(search["shake_conflicts"]),
            "--restart-shakes",
            str(search["restart_shakes"]),
            "--full-audit-interval",
            str(search["full_audit_interval"]),
            "--output",
            str(candidate.relative_to(ROOT)),
            "--json-output",
            str(search_json.relative_to(ROOT)),
        ]
        search_run = run_process(
            command,
            allowed=(0,),
            timeout=float(plan["per_run_wall_limit_seconds"]),
        )
        search_result = checked_json(
            search_run.stdout, "conflict-block corpus search"
        )
        if json.loads(search_json.read_text(encoding="utf-8")) != search_result:
            raise RuntimeError("stdout and retained search JSON differ")
        if (
            search_result.get("initial_E") != 2
            or search_result.get("initial_C5") != start["C5"]
            or search_result.get("initial_I5") != start["I5"]
        ):
            raise RuntimeError("search initial objective mismatch")

        verification = verify_candidate(
            candidate=candidate,
            base=base,
            search_json=search_json,
            run_dir=run_dir,
            expected=search_result,
            plan=plan,
        )
        objective = int(search_result["E"])
        initial_side = color_side(int(start["C5"]), int(start["I5"]))
        final_side = color_side(
            int(search_result["C5"]), int(search_result["I5"])
        )
        record: dict[str, object] = {
            "catalog_line": start["catalog_line"],
            "start_label": label,
            "start": str(base.relative_to(ROOT)),
            "start_sha256": sha256(base),
            "initial_C5": start["C5"],
            "initial_I5": start["I5"],
            "initial_E": 2,
            "initial_color_side": initial_side,
            "seed": seed,
            "search_json": str(search_json.relative_to(ROOT)),
            "search_json_sha256": sha256(search_json),
            "final_candidate": str(candidate.relative_to(ROOT)),
            "final_candidate_sha256": sha256(candidate),
            "E": objective,
            "C5": search_result["C5"],
            "I5": search_result["I5"],
            "final_color_side": final_side,
            "color_side_transition": f"{initial_side}->{final_side}",
            "edge_hamming_distance": search_result["edge_hamming_distance"],
            "degree_penalty": search_result["degree_penalty"],
            "steps_executed": search_result["steps_executed"],
            "evaluated_moves": search_result["evaluated_moves"],
            "shake_events": search_result["shake_events"],
            "strict_improvements": search_result["strict_improvements"],
            "improvement_trace": search_result["improvements"],
            "runtime_seconds": search_result["runtime_seconds"],
            "verification": verification,
            "evidence_label": (
                "CERTIFIED"
                if objective == 0
                else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
            ),
        }
        runs.append(record)

        artifact_bytes = directory_bytes(output_root)
        if artifact_bytes > plan["storage_limit_bytes"]:
            raise RuntimeError(
                f"artifact storage limit exceeded: {artifact_bytes}"
            )
        if objective == 0:
            certified = certify_construction(
                candidate=candidate,
                start_label=label,
                seed=seed,
                plan=plan,
            )
            record["construction_certification"] = certified
            break

    completed = len(runs)
    e0_count = sum(int(item["E"]) == 0 for item in runs)
    e1_count = sum(int(item["E"]) == 1 for item in runs)
    e2_escape_count = sum(
        int(item["E"]) == 2 and int(item["edge_hamming_distance"]) > 0
        for item in runs
    )
    mobility_count = sum(
        int(item["E"]) <= 2 and int(item["edge_hamming_distance"]) > 0
        for item in runs
    )
    transition_counts: dict[str, int] = {}
    for item in runs:
        transition = str(item["color_side_transition"])
        transition_counts[transition] = transition_counts.get(transition, 0) + 1

    start_distances = [int(item["edge_hamming_distance"]) for item in runs]
    final_graphs = [
        read_graph(ROOT / str(item["final_candidate"])) for item in runs
    ]
    pairwise_distances = [
        edge_hamming(final_graphs[left], final_graphs[right])
        for left in range(len(final_graphs))
        for right in range(left + 1, len(final_graphs))
    ]

    prior_path = ROOT / plan["comparison"]["pilot_summary"]
    prior = json.loads(prior_path.read_text(encoding="utf-8"))
    prior_e2_runs = [
        item for item in prior["runs"] if int(item["initial_E"]) == 2
    ]
    prior_e2_escapes = sum(
        int(item["E"]) == 2 and int(item["edge_hamming_distance"]) > 0
        for item in prior_e2_runs
    )
    comparison = {
        "pilot_summary": str(prior_path.relative_to(ROOT)),
        "pilot_summary_sha256": sha256(prior_path),
        "pilot_registered_runs": prior["registered_run_count"],
        "pilot_best_objective": prior["best_objective"],
        "pilot_E0_count": sum(int(item["E"]) == 0 for item in prior["runs"]),
        "pilot_E1_count": sum(int(item["E"]) == 1 for item in prior["runs"]),
        "pilot_E2_start_escape_rate": rate(
            prior_e2_escapes, len(prior_e2_runs)
        ),
        "followup_best_objective": min(int(item["E"]) for item in runs),
        "followup_E0_rate": rate(e0_count, completed),
        "followup_E1_rate": rate(e1_count, completed),
        "followup_positive_hamming_E2_escape_rate": rate(
            e2_escape_count, completed
        ),
    }

    summary = {
        "schema": "ramsey55.conflict_block_catalog22_followup_result.v1",
        "evidence_label": (
            "CERTIFIED"
            if certified is not None
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "claim_boundary": (
            "Only an E=0 graph accepted by direct Python enumeration, the "
            "separately compiled C++ graph/complement verifier, the "
            "independent search-record audit, canonical export, and the "
            "adversarial artifact audit is a certified construction. "
            "Nonzero results are bounded search observations."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "registered_run_count": len(plan["starts"]),
        "completed_run_count": completed,
        "stopped_early_on_E0": certified is not None,
        "best_objective": min(int(item["E"]) for item in runs),
        "valid_candidate_found": certified is not None,
        "construction": certified,
        "rates": {
            "E0": rate(e0_count, completed),
            "E1": rate(e1_count, completed),
            "positive_hamming_E2_escape": rate(
                e2_escape_count, completed
            ),
            "positive_hamming_E_le_2_mobility": rate(
                mobility_count, completed
            ),
        },
        "color_side_transition_counts": transition_counts,
        "hamming_diversity": {
            "distance_from_registered_start": numeric_summary(
                start_distances
            ),
            "nonzero_distance_count": sum(value > 0 for value in start_distances),
            "distinct_raw_final_graph_count": len(
                {str(item["final_candidate_sha256"]) for item in runs}
            ),
            "pairwise_labeled_final_edge_hamming": numeric_summary(
                pairwise_distances
            ),
            "pair_count": len(pairwise_distances),
        },
        "comparison_to_ten_run_pilot": comparison,
        "total_steps_executed": sum(
            int(item["steps_executed"]) for item in runs
        ),
        "total_evaluated_moves": sum(
            int(item["evaluated_moves"]) for item in runs
        ),
        "total_shake_events": sum(int(item["shake_events"]) for item in runs),
        "total_runtime_seconds": sum(
            float(item["runtime_seconds"]) for item in runs
        ),
        "artifact_bytes": directory_bytes(output_root),
        "storage_limit_bytes": plan["storage_limit_bytes"],
        "runs": runs,
    }
    write_json(ROOT / plan["summary_output"], summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
