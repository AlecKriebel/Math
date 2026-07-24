#!/usr/bin/env python3
"""Run and verify a preregistered multi-start degree-switch pilot."""

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


def verify_artifact(
    *,
    candidate: Path,
    base: Path,
    search_json: Path,
    output_prefix: Path,
    expected: dict[str, object],
    improvement_ordinal: int | None,
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
    python_path = Path(str(output_prefix) + ".python.json")
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
    cpp_path = Path(str(output_prefix) + ".cpp.json")
    cpp_sha = write_json(cpp_path, cpp_result)

    structural_path = Path(str(output_prefix) + ".structural.json")
    structural_command = [
        sys.executable,
        plan["verification"]["structural_source"],
        str(candidate.relative_to(ROOT)),
        "--base",
        str(base.relative_to(ROOT)),
        "--search-json",
        str(search_json.relative_to(ROOT)),
        "--output",
        str(structural_path.relative_to(ROOT)),
    ]
    if improvement_ordinal is not None:
        structural_command.extend(
            ["--improvement-ordinal", str(improvement_ordinal)]
        )
    structural_run = run_process(
        structural_command,
        allowed=(0,),
        timeout=120,
    )
    structural_result = checked_json(
        structural_run.stdout, "degree-switch structural verifier"
    )

    objective = int(expected["E"])
    cliques = int(expected["C5"])
    independent = int(expected["I5"])
    if (
        python_result.get("objective") != objective
        or python_result.get("clique_count") != cliques
        or python_result.get("independent_count") != independent
        or structural_result.get("objective") != objective
        or structural_result.get("clique_count") != cliques
        or structural_result.get("independent_count") != independent
        or structural_result.get("accepted") is not True
        or cpp_result.get("clique_k_found") != (cliques > 0)
        or cpp_result.get("independent_k_found") != (independent > 0)
        or cpp_result.get("valid") != (objective == 0)
        or python_result.get("valid") != (objective == 0)
    ):
        raise RuntimeError("independent artifact verification disagrees")

    return {
        "kind": (
            "final"
            if improvement_ordinal is None
            else "strict_improvement"
        ),
        "improvement_ordinal": improvement_ordinal,
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
        "degree_vector_preserved": structural_result[
            "structural_checks"
        ]["labeled_degree_vector_exact"],
        "edge_hamming_distance": structural_result[
            "edge_hamming_distance"
        ],
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
        / f"results/best_candidates/degree_switch_{start_label}_seed_"
        f"{seed}.canonical.json"
    )
    run_process(
        [
            sys.executable,
            "src/export_artifact.py",
            str(candidate.relative_to(ROOT)),
            str(canonical.relative_to(ROOT)),
            "--source",
            "degree_preserving_2switch_compound_lns_v1",
            "--seed",
            str(seed),
        ],
        allowed=(0,),
        timeout=120,
    )
    audit_dir = (
        ROOT
        / f"results/audit/degree_switch_{start_label}_seed_{seed}"
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
        raise RuntimeError("E=0 adversarial artifact audit failed")
    audit_path = (
        ROOT
        / f"results/verification/degree_switch_{start_label}_seed_"
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
        raise SystemExit("compiled binary hash mismatch")

    for start in plan["starts"]:
        python_audit = json.loads(
            (ROOT / start["python_verification"]).read_text(encoding="utf-8")
        )
        cpp_audit = json.loads(
            (ROOT / start["cpp_verification"]).read_text(encoding="utf-8")
        )
        if (
            python_audit.get("objective") != 2
            or cpp_audit.get("valid") is not False
            or cpp_audit.get("clique_k_found")
            == cpp_audit.get("independent_k_found")
        ):
            raise SystemExit(
                f"start is not the registered independently verified E=2 graph: "
                f"{start['label']}"
            )

    search = plan["search"]
    output_root = ROOT / plan["output_root"]
    runs: list[dict[str, object]] = []
    certified: dict[str, object] | None = None

    for start in plan["starts"]:
        if certified is not None:
            break
        start_label = str(start["label"])
        base = ROOT / start["path"]
        for seed in plan["seeds"]:
            run_dir = output_root / start_label / f"seed_{seed}"
            run_dir.mkdir(parents=True, exist_ok=True)
            candidate = run_dir / "final.g6"
            search_json = run_dir / "search.json"
            improvement_prefix = run_dir / "improvement"
            for output in (candidate, search_json):
                if output.exists():
                    raise SystemExit(
                        f"refusing to overwrite preregistered output: {output}"
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
                "--tabu",
                str(search["tabu_tenure"]),
                "--random-walk-per-million",
                str(search["random_walk_per_million"]),
                "--breakout-interval",
                str(search["breakout_interval"]),
                "--restart-switches",
                str(search["restart_switches"]),
                "--targeted-samples",
                str(search["targeted_samples"]),
                "--global-samples",
                str(search["global_samples"]),
                "--compound-samples",
                str(search["compound_samples"]),
                "--full-audit-interval",
                str(search["full_audit_interval"]),
                "--output",
                str(candidate.relative_to(ROOT)),
                "--json-output",
                str(search_json.relative_to(ROOT)),
                "--improvement-prefix",
                str(improvement_prefix.relative_to(ROOT)),
            ]
            search_run = run_process(
                command,
                allowed=(0,),
                timeout=float(plan["per_run_wall_limit_seconds"]),
            )
            search_result = checked_json(
                search_run.stdout, "degree-switch search"
            )
            retained_search = json.loads(
                search_json.read_text(encoding="utf-8")
            )
            if retained_search != search_result:
                raise RuntimeError(
                    "search stdout and retained JSON do not match"
                )

            verified_artifacts: list[dict[str, object]] = []
            for improvement in search_result["improvements"]:
                ordinal = int(improvement["ordinal"])
                improvement_path = ROOT / improvement["path"]
                verified_artifacts.append(
                    verify_artifact(
                        candidate=improvement_path,
                        base=base,
                        search_json=search_json,
                        output_prefix=run_dir
                        / f"improvement_{ordinal}.verification",
                        expected=improvement,
                        improvement_ordinal=ordinal,
                        plan=plan,
                    )
                )

            final_expected = {
                "E": search_result["E"],
                "C5": search_result["C5"],
                "I5": search_result["I5"],
            }
            final_verification = verify_artifact(
                candidate=candidate,
                base=base,
                search_json=search_json,
                output_prefix=run_dir / "final.verification",
                expected=final_expected,
                improvement_ordinal=None,
                plan=plan,
            )
            verified_artifacts.append(final_verification)
            objective = int(search_result["E"])

            run_record = {
                "start_label": start_label,
                "start": str(base.relative_to(ROOT)),
                "start_sha256": sha256(base),
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
                "steps_executed": search_result["steps_executed"],
                "evaluated_moves": search_result["evaluated_moves"],
                "evaluated_compound_moves": search_result[
                    "evaluated_compound_moves"
                ],
                "runtime_seconds": search_result["runtime_seconds"],
                "strict_improvement_count": len(
                    search_result["improvements"]
                ),
                "verified_artifacts": verified_artifacts,
                "all_retained_artifacts_independently_verified": True,
                "evidence_label": (
                    "CERTIFIED"
                    if objective == 0
                    else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
                ),
            }
            runs.append(run_record)

            if objective == 0:
                if not all(
                    artifact["E"] == 0
                    or artifact["kind"] == "strict_improvement"
                    for artifact in verified_artifacts
                ):
                    raise RuntimeError("unexpected E=0 verification state")
                certified = certify_construction(
                    candidate=candidate,
                    start_label=start_label,
                    seed=seed,
                    plan=plan,
                )
                run_record["construction_certification"] = certified
                break

    best = min(int(run["E"]) for run in runs)
    summary = {
        "schema": "ramsey55.degree_switch_pilot_result.v1",
        "evidence_label": (
            "CERTIFIED"
            if certified is not None
            else "REPRODUCIBLE COMPUTATIONAL OBSERVATION"
        ),
        "claim_boundary": (
            "Only an E=0 graph accepted by the Python exhaustive verifier, "
            "the separately compiled C++ graph/complement verifier, the "
            "independent degree-preservation/search-record audit, canonical "
            "export, and adversarial artifact audit is a certified "
            "construction. Every nonzero retained graph is only a bounded "
            "search observation."
        ),
        "plan": str(args.plan),
        "plan_sha256": sha256(args.plan),
        "registered_run_count": len(plan["starts"]) * len(plan["seeds"]),
        "completed_run_count": len(runs),
        "stopped_early_on_E0": certified is not None,
        "best_objective": best,
        "valid_candidate_found": certified is not None,
        "construction": certified,
        "runs": runs,
    }
    summary_path = ROOT / plan["summary_output"]
    write_json(summary_path, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
