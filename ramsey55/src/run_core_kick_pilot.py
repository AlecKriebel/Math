#!/usr/bin/env python3
"""Execute a preregistered multi-seed core-kick pilot and its verifiers."""

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


def run_process(
    command: list[str], *, allowed: tuple[int, ...], timeout: float
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    if plan["status"] != "PREREGISTERED_BEFORE_PRODUCTION_RUNS":
        raise SystemExit("plan is not an unambiguous production preregistration")

    for record in plan["pinned_files"]:
        path = ROOT / record["path"]
        if sha256(path) != record["sha256"]:
            raise SystemExit(f"pinned file hash mismatch: {path}")

    binary = ROOT / plan["binary"]["path"]
    if sha256(binary) != plan["binary"]["sha256"]:
        raise SystemExit("compiled binary hash mismatch")
    search = plan["search"]
    results: list[dict[str, object]] = []
    for seed in plan["seeds"]:
        candidate = ROOT / f"results/best_candidates/core_kick_seed_{seed}.g6"
        search_json = (
            ROOT / f"results/verification/core_kick_seed_{seed}_search.json"
        )
        command = [
            str(binary),
            "--seed-graph",
            search["seed_graph"],
            "--metadata",
            search["metadata"],
            "--ranking",
            search["ranking"],
            "--seed",
            str(seed),
            "--steps",
            str(search["steps_per_restart"]),
            "--restarts",
            str(search["restarts"]),
            "--tabu",
            str(search["tabu_tenure"]),
            "--random-walk",
            str(search["random_walk"]),
            "--breakout-interval",
            str(search["breakout_interval"]),
            "--boundary-perturbation",
            str(search["boundary_perturbation"]),
            "--initial-core-distance",
            str(search["initial_core_distance"]),
            "--min-core-distance",
            str(search["min_core_distance"]),
            "--max-core-distance",
            str(search["max_core_distance"]),
            "--guided-initial-edges",
            str(search["guided_initial_edges"]),
            "--guided-pool",
            str(search["guided_pool"]),
            "--swap-samples",
            str(search["swap_samples"]),
            "--global-swap-interval",
            str(search["global_swap_interval"]),
            "--output",
            str(candidate.relative_to(ROOT)),
            "--json-output",
            str(search_json.relative_to(ROOT)),
        ]
        search_run = run_process(
            command,
            allowed=(0,),
            timeout=float(plan["per_seed_wall_limit_seconds"]),
        )
        search_result = checked_json(search_run.stdout, "constructive search")
        retained_search = json.loads(search_json.read_text(encoding="utf-8"))
        if retained_search != search_result:
            raise RuntimeError("stdout and retained search JSON differ")

        python_path = (
            ROOT / f"results/verification/core_kick_seed_{seed}_python.json"
        )
        python_run = run_process(
            [
                sys.executable,
                "verify/exhaustive_verify.py",
                str(candidate.relative_to(ROOT)),
            ],
            allowed=(0, 1),
            timeout=120,
        )
        python_result = checked_json(python_run.stdout, "Python verifier")
        python_sha = write_json(python_path, python_result)

        cpp_path = ROOT / f"results/verification/core_kick_seed_{seed}_cpp.json"
        cpp_run = run_process(
            ["build/bitset_verify", str(candidate.relative_to(ROOT))],
            allowed=(0, 1),
            timeout=120,
        )
        cpp_result = checked_json(cpp_run.stdout, "C++ verifier")
        cpp_sha = write_json(cpp_path, cpp_result)

        audit_path = (
            ROOT / f"results/verification/core_kick_seed_{seed}_audit.json"
        )
        audit_run = run_process(
            [
                sys.executable,
                "verify/core_kick_candidate_check.py",
                str(candidate.relative_to(ROOT)),
                "--base",
                search["seed_graph"],
                "--metadata",
                search["metadata"],
                "--search-json",
                str(search_json.relative_to(ROOT)),
                "--incident-vertices",
                search["incident_vertices"],
                "--min-core-distance",
                str(search["min_core_distance"]),
                "--max-core-distance",
                str(search["max_core_distance"]),
                "--output",
                str(audit_path.relative_to(ROOT)),
            ],
            allowed=(0, 1),
            timeout=120,
        )
        audit_result = checked_json(audit_run.stdout, "structural verifier")

        objective = int(search_result["E"])
        if (
            python_result["objective"] != objective
            or audit_result["objective"] != objective
            or cpp_result["clique_k_found"]
            != (int(search_result["C5"]) > 0)
            or cpp_result["independent_k_found"]
            != (int(search_result["I5"]) > 0)
            or not audit_result["structural_valid"]
        ):
            raise RuntimeError("independent candidate verification disagrees")

        adversarial: dict[str, object] | None = None
        if objective == 0:
            if not (
                python_result["valid"]
                and cpp_result["valid"]
                and audit_result["accepted"]
            ):
                raise RuntimeError("E=0 candidate did not pass all verifiers")
            canonical = (
                ROOT
                / f"results/best_candidates/core_kick_seed_{seed}.canonical.json"
            )
            run_process(
                [
                    sys.executable,
                    "src/export_artifact.py",
                    str(candidate.relative_to(ROOT)),
                    str(canonical.relative_to(ROOT)),
                    "--source",
                    "core_kick_dynamic_swap_lns_v1",
                    "--seed",
                    str(seed),
                ],
                allowed=(0,),
                timeout=120,
            )
            adversarial_dir = (
                ROOT / f"results/audit/core_kick_seed_{seed}"
            )
            adversarial_run = run_process(
                [
                    sys.executable,
                    "verify/adversarial_audit.py",
                    str(candidate.relative_to(ROOT)),
                    "--json-copy",
                    str(canonical.relative_to(ROOT)),
                    "--seed",
                    str(seed),
                    "--output-dir",
                    str(adversarial_dir.relative_to(ROOT)),
                    "--cpp",
                    "build/bitset_verify",
                ],
                allowed=(0,),
                timeout=240,
            )
            adversarial = checked_json(
                adversarial_run.stdout, "adversarial artifact audit"
            )
            if adversarial["status"] != "PASS":
                raise RuntimeError("adversarial artifact audit failed")
            write_json(
                ROOT
                / f"results/verification/core_kick_seed_{seed}_adversarial.json",
                adversarial,
            )

        results.append(
            {
                "seed": seed,
                "evidence_label": (
                    "CERTIFIED"
                    if objective == 0 and adversarial is not None
                    else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
                "candidate": str(candidate.relative_to(ROOT)),
                "candidate_sha256": sha256(candidate),
                "search_json": str(search_json.relative_to(ROOT)),
                "search_json_sha256": sha256(search_json),
                "python_verifier_json": str(python_path.relative_to(ROOT)),
                "python_verifier_json_sha256": python_sha,
                "cpp_verifier_json": str(cpp_path.relative_to(ROOT)),
                "cpp_verifier_json_sha256": cpp_sha,
                "structural_audit_json": str(audit_path.relative_to(ROOT)),
                "structural_audit_json_sha256": sha256(audit_path),
                "E": objective,
                "C5": search_result["C5"],
                "I5": search_result["I5"],
                "changed_core_edge_count": search_result[
                    "changed_core_edge_count"
                ],
                "changed_boundary_edges": search_result[
                    "changed_boundary_edges"
                ],
                "runtime_seconds": search_result["runtime_seconds"],
            }
        )

    best = min(int(record["E"]) for record in results)
    summary = {
        "schema": "ramsey55.core_kick_pilot_result.v1",
        "evidence_label": (
            "CERTIFIED"
            if best == 0
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "claim_boundary": (
            "A valid construction is claimed only for an E=0 artifact accepted "
            "by both graph verifiers, the structural audit, canonical export, "
            "and adversarial artifact audit. Nonzero outcomes are bounded "
            "search observations only."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "best_objective": best,
        "valid_candidate_found": best == 0,
        "runs": results,
    }
    summary_path = ROOT / plan["summary_output"]
    write_json(summary_path, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
