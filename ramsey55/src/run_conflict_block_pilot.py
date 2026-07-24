#!/usr/bin/env python3
"""Run a preregistered multi-start conflict-block ProbSAT comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return sha256(path)


def checked_json(stdout: str, label: str) -> dict[str, object]:
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"{label} did not emit one JSON object") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} JSON root is not an object")
    return value


def run_process(
    command: list[str],
    *,
    allowed: tuple[int, ...],
    timeout: float,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    if completed.returncode not in allowed:
        raise RuntimeError(
            f"command failed with {completed.returncode}: {command}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def directory_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def verify_candidate(
    *,
    candidate: Path,
    base: Path,
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
            "--base",
            str(base.relative_to(ROOT)),
            "--search-json",
            str(search_json.relative_to(ROOT)),
            "--output",
            str(structural_path.relative_to(ROOT)),
        ],
        allowed=(0,),
        timeout=120,
    )
    structural = checked_json(
        structural_run.stdout, "independent conflict-block audit"
    )

    objective = int(expected["E"])
    cliques = int(expected["C5"])
    independent = int(expected["I5"])
    if (
        python_result.get("objective") != objective
        or python_result.get("clique_count") != cliques
        or python_result.get("independent_count") != independent
        or structural.get("objective") != objective
        or structural.get("clique_count") != cliques
        or structural.get("independent_count") != independent
        or structural.get("accepted") is not True
        or cpp_result.get("clique_k_found") != (cliques > 0)
        or cpp_result.get("independent_k_found") != (independent > 0)
        or python_result.get("valid") != (objective == 0)
        or cpp_result.get("valid") != (objective == 0)
    ):
        raise RuntimeError("independent conflict-block verification disagrees")
    return {
        "candidate": str(candidate.relative_to(ROOT)),
        "candidate_sha256": sha256(candidate),
        "E": objective,
        "C5": cliques,
        "I5": independent,
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
    start_label: str,
    seed: int,
    plan: dict[str, object],
) -> dict[str, object]:
    canonical = (
        ROOT
        / f"results/best_candidates/conflict_block_{start_label}_seed_"
        f"{seed}.canonical.json"
    )
    run_process(
        [
            sys.executable,
            "src/export_artifact.py",
            str(candidate.relative_to(ROOT)),
            str(canonical.relative_to(ROOT)),
            "--source",
            "conflict_hypergraph_probsat_blocks_v1",
            "--seed",
            str(seed),
        ],
        allowed=(0,),
        timeout=120,
    )
    audit_dir = (
        ROOT / f"results/audit/conflict_block_{start_label}_seed_{seed}"
    )
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
    audit = checked_json(audit_run.stdout, "adversarial artifact audit")
    if audit.get("status") != "PASS":
        raise RuntimeError("E=0 adversarial audit failed")
    audit_path = (
        ROOT
        / f"results/verification/conflict_block_{start_label}_seed_"
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
        raise SystemExit("compiled search binary hash mismatch")

    for start in plan["starts"]:
        python_record = json.loads(
            (ROOT / start["python_verification"]).read_text(encoding="utf-8")
        )
        cpp_record = json.loads(
            (ROOT / start["cpp_verification"]).read_text(encoding="utf-8")
        )
        if (
            python_record.get("objective") != start["E"]
            or python_record.get("clique_count") != start["C5"]
            or python_record.get("independent_count") != start["I5"]
            or cpp_record.get("clique_k_found") != (start["C5"] > 0)
            or cpp_record.get("independent_k_found") != (start["I5"] > 0)
        ):
            raise SystemExit(f"start verification mismatch: {start['label']}")

    output_root = ROOT / plan["output_root"]
    search = plan["search"]
    runs: list[dict[str, object]] = []
    certified: dict[str, object] | None = None

    for start in plan["starts"]:
        if certified is not None:
            break
        base = ROOT / start["path"]
        label = str(start["label"])
        for seed in plan["seeds"]:
            run_dir = output_root / label / f"seed_{seed}"
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
                search_run.stdout, "conflict-block search"
            )
            if json.loads(search_json.read_text(encoding="utf-8")) != search_result:
                raise RuntimeError("stdout and retained search JSON differ")
            if (
                search_result.get("initial_E") != start["E"]
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
            record = {
                "start_label": label,
                "start": str(base.relative_to(ROOT)),
                "start_sha256": sha256(base),
                "initial_E": start["E"],
                "seed": seed,
                "search_json": str(search_json.relative_to(ROOT)),
                "search_json_sha256": sha256(search_json),
                "final_candidate": str(candidate.relative_to(ROOT)),
                "final_candidate_sha256": sha256(candidate),
                "E": objective,
                "C5": search_result["C5"],
                "I5": search_result["I5"],
                "edge_hamming_distance": search_result[
                    "edge_hamming_distance"
                ],
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

    best = min(int(record["E"]) for record in runs)
    summary = {
        "schema": "ramsey55.conflict_block_pilot_result.v1",
        "evidence_label": (
            "CERTIFIED"
            if certified is not None
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "hypothesis": plan["hypothesis"],
        "claim_boundary": (
            "Only an E=0 graph accepted by direct Python enumeration, the "
            "separately compiled C++ graph/complement verifier, the "
            "independent search-record audit, canonical export, and the "
            "adversarial artifact audit is a certified construction. "
            "Nonzero results are bounded search observations."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "registered_run_count": len(plan["starts"]) * len(plan["seeds"]),
        "completed_run_count": len(runs),
        "stopped_early_on_E0": certified is not None,
        "best_objective": best,
        "valid_candidate_found": certified is not None,
        "construction": certified,
        "artifact_bytes": directory_bytes(output_root),
        "storage_limit_bytes": plan["storage_limit_bytes"],
        "runs": runs,
    }
    summary_path = ROOT / plan["summary_output"]
    write_json(summary_path, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
