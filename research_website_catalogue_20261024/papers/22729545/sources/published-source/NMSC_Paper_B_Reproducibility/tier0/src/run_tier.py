#!/usr/bin/env python3
"""Bounded, blocking tier runner with content-addressed resume checkpoints."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shlex
import subprocess
import sys

from record_schema import canonical_bytes, validate_output


CHECKPOINT_SCHEMA = "nmsc-local-checkpoint-v3"
COMPLETION_SCHEMA = "nmsc-local-tier-completion-v3"


@dataclass(frozen=True)
class Job:
    name: str
    command: tuple[str, ...]
    output: Path
    expected_job: str
    minimum_records: int
    inputs: tuple[Path, ...] = ()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_hash(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def relative(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        return str(path.resolve())


def interpreter_identifier() -> str:
    version = ".".join(map(str, sys.version_info[:3]))
    return f"python:{sys.implementation.name}-{version}"


def portable_argument(root: Path, value: str) -> str:
    """Normalize an absolute in-tree argument without resolving flag values."""
    candidate = Path(value)
    if not candidate.is_absolute():
        return value
    try:
        return str(candidate.resolve().relative_to(root.resolve())) or "."
    except ValueError:
        return value


def recorded_job_command(root: Path, job: Job) -> list[str]:
    if not job.command:
        raise ValueError(f"{job.name} has an empty command")
    executable = Path(job.command[0]).resolve()
    if executable != Path(sys.executable).resolve():
        raise ValueError(f"{job.name} does not use the locked Python interpreter")
    return [
        interpreter_identifier(),
        *(portable_argument(root, value) for value in job.command[1:]),
    ]


def recorded_runner_invocation(root: Path, argv: list[str]) -> list[str]:
    return [
        interpreter_identifier(),
        *(portable_argument(root, value) for value in argv),
    ]


def checked_environment() -> dict:
    version = sys.version_info[:3]
    try:
        packages = {
            name: importlib.metadata.version(name)
            for name in ("networkx", "sympy")
        }
    except importlib.metadata.PackageNotFoundError as error:
        raise SystemExit(f"environment lock mismatch: missing {error.name}") from error
    failures = []
    if not ((3, 11) <= version < (3, 14)):
        failures.append(f"Python {version!r} is outside >=3.11,<3.14")
    expected = {"networkx": "3.5", "sympy": "1.14.0"}
    for name, wanted in expected.items():
        if packages[name] != wanted:
            failures.append(f"{name}=={packages[name]} but lock requires {wanted}")
    if failures:
        raise SystemExit("environment lock mismatch: " + "; ".join(failures))
    return {
        "python_identifier": interpreter_identifier(),
        "python_implementation": sys.implementation.name,
        "python_version": ".".join(map(str, version)),
        "packages": packages,
    }


def source_hashes(root: Path) -> dict[str, str]:
    sources = sorted((root / "src").glob("*.py"))
    if not sources:
        raise ValueError("no verifier sources found")
    return {relative(root, path): sha256(path) for path in sources}


def fingerprint(root: Path, job: Job, sources: dict[str, str]) -> dict:
    replay_inputs = tuple(
        sorted(set(job.inputs).union({root / "environment.lock", root / "requirements.lock"}))
    )
    missing = [path for path in replay_inputs if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            f"{job.name} missing inputs: {[relative(root, path) for path in missing]}"
        )
    command = recorded_job_command(root, job)
    return {
        "command": command,
        "command_hash": json_hash(command),
        "source_hashes": sources,
        "source_bundle_hash": json_hash(sources),
        "input_hashes": {
            relative(root, path): sha256(path) for path in replay_inputs
        },
    }


def write_checkpoint(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def can_resume(
    root: Path,
    job: Job,
    checkpoint: Path,
    current_fingerprint: dict,
) -> tuple[bool, str]:
    if not checkpoint.is_file():
        return False, "checkpoint missing"
    try:
        stored = json.loads(checkpoint.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return False, f"checkpoint unreadable: {error}"
    if stored.get("schema_version") != CHECKPOINT_SCHEMA:
        return False, "checkpoint schema changed"
    if stored.get("status") != "complete" or stored.get("returncode") != 0:
        return False, "checkpoint is not a successful completion"
    if stored.get("fingerprint") != current_fingerprint:
        return False, "command/source/input fingerprint changed"
    output = stored.get("output", {})
    if not job.output.is_file():
        return False, "output missing"
    if output.get("sha256") != sha256(job.output):
        return False, "output hash changed"
    try:
        records = validate_output(
            job.output,
            expected_job=job.expected_job,
            minimum_records=job.minimum_records,
        )
    except Exception as error:  # retained verbatim in the run log
        return False, f"output schema/status validation failed: {error}"
    if output.get("record_count") != len(records):
        return False, "output record count changed"
    return True, "command/source/input/output hashes and schema match"


def execute_job(
    *,
    root: Path,
    tier: int,
    job: Job,
    checkpoint: Path,
    current_fingerprint: dict,
    log,
) -> None:
    print(f"RUN {job.name}", flush=True)
    log.write(f"$ {shlex.join(recorded_job_command(root, job))}\n")
    log.flush()
    # A successful command must create its output during this invocation.
    # Otherwise a truncated/silent no-op verifier could inherit a stale PASS
    # artifact and be accepted after its source fingerprint changed.
    job.output.unlink(missing_ok=True)
    completed = subprocess.run(
        job.command,
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    log.write(completed.stdout)
    log.write(completed.stderr)
    log.flush()
    checkpoint_payload = {
        "schema_version": CHECKPOINT_SCHEMA,
        "tier": tier,
        "job": job.name,
        "fingerprint": current_fingerprint,
        "returncode": completed.returncode,
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "stdout_sha256": hashlib.sha256(completed.stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(completed.stderr.encode()).hexdigest(),
    }
    validation_error = None
    records = []
    if completed.returncode == 0:
        try:
            records = validate_output(
                job.output,
                expected_job=job.expected_job,
                minimum_records=job.minimum_records,
            )
        except Exception as error:
            validation_error = str(error)
    else:
        validation_error = f"command exited {completed.returncode}"

    if job.output.is_file():
        checkpoint_payload["output"] = {
            "path": relative(root, job.output),
            "sha256": sha256(job.output),
            "record_count": len(records) if records else None,
        }
    if validation_error is None:
        checkpoint_payload["status"] = "complete"
    else:
        checkpoint_payload["status"] = "failed"
        checkpoint_payload["validation_error"] = validation_error
    write_checkpoint(checkpoint, checkpoint_payload)
    if validation_error is not None:
        raise SystemExit(f"{job.name} failed: {validation_error}")
    print(f"PASS {job.name} records={len(records)}", flush=True)


def jobs_for_tier(root: Path, tier: int) -> list[Job]:
    output = root / "outputs"
    source = root / "src"
    data = root / "data"
    python = sys.executable
    max_m = (4, 8, 12, 12)[tier]
    cores = output / "independent_cores.jsonl"
    exposure = output / "independent_exposure_loss.jsonl"
    exposure_manifest = data / "independent_exposure_manifest.json"
    literal_manifest = data / "independent_literal_cylinder_manifest.json"
    law_manifest = data / "independent_law_interface_manifest.json"
    finite_eight_manifest = data / "independent_finite_eight_full_sweep_manifest.json"
    anchors = output / "anchor_certificates.jsonl"
    reattachment = output / "peeling_reattachment.jsonl"
    jobs = [
        Job(
            "enum",
            (python, str(source / "independent_graph_enumerator.py"), "--max-path", "3", "--out", str(cores)),
            cores,
            "independent_graph_enumerator",
            5,
        ),
        Job(
            "exposure",
            (
                python,
                str(source / "independent_exposure_verifier.py"),
                "--manifest",
                str(exposure_manifest),
                "--out",
                str(exposure),
            ),
            exposure,
            "independent_exposure_loss",
            4,
            (exposure_manifest,),
        ),
        Job(
            "literal",
            (
                python,
                str(source / "independent_literal_cylinder_verifier.py"),
                "--manifest",
                str(literal_manifest),
                "--out",
                str(output / "independent_literal_cylinders.jsonl"),
            ),
            output / "independent_literal_cylinders.jsonl",
            "independent_literal_cylinders",
            5,
            (literal_manifest,),
        ),
        Job(
            "law_interfaces",
            (
                python,
                str(source / "independent_law_interface_verifier.py"),
                "--manifest",
                str(law_manifest),
                "--out",
                str(output / "independent_law_interfaces.json"),
            ),
            output / "independent_law_interfaces.json",
            "independent_law_interfaces",
            1,
            (law_manifest,),
        ),
        Job(
            "finite_eight",
            (
                python,
                str(source / "independent_finite_eight_full_sweep.py"),
                "--manifest",
                str(finite_eight_manifest),
                "--out",
                str(output / "independent_finite_eight_full_sweep.json"),
            ),
            output / "independent_finite_eight_full_sweep.json",
            "independent_finite_eight_full_sweep",
            1,
            (finite_eight_manifest,),
        ),
        Job(
            "hankel",
            (python, str(source / "observable_hankel_rows.py"), "--out", str(output / "observable_hankel_certificates.json")),
            output / "observable_hankel_certificates.json",
            "observable_hankel_rows",
            1,
        ),
        Job(
            "routing",
            (python, str(source / "routing_tomography.py"), "--max-m", str(max_m), "--out", str(output / "routing_tomography.json")),
            output / "routing_tomography.json",
            "routing_tomography",
            1,
        ),
        Job(
            "triangle",
            (python, str(source / "triangle_response.py"), "--out", str(output / "triangle_certificates.json")),
            output / "triangle_certificates.json",
            "triangle_response",
            1,
        ),
        Job(
            "separator",
            (python, str(source / "one_port_separator.py"), "--out", str(output / "separator_certificates.json")),
            output / "separator_certificates.json",
            "one_port_separator",
            1,
        ),
        Job(
            "anchors",
            (python, str(source / "anchor_verifier.py"), "--cores", str(cores), "--out", str(anchors)),
            anchors,
            "anchor_verifier",
            18,
            (cores,),
        ),
        Job(
            "reattach",
            (python, str(source / "peeling_reattachment.py"), "--cores", str(cores), "--out", str(reattachment)),
            reattachment,
            "peeling_reattachment",
            18,
            (cores,),
        ),
        Job(
            "diff",
            (
                python,
                str(source / "differential_harness.py"),
                "--topology-reference",
                str(data / "proof_topology_reference.json"),
                "--reattachment-reference",
                str(data / "proof_reattachment_reference.json"),
                "--cores",
                str(cores),
                "--anchors",
                str(anchors),
                "--reattach",
                str(reattachment),
                "--exposure",
                str(exposure),
                "--out",
                str(output / "differential_report.json"),
            ),
            output / "differential_report.json",
            "differential_harness",
            1,
            (
                data / "proof_topology_reference.json",
                data / "proof_reattachment_reference.json",
                cores,
                anchors,
                reattachment,
                exposure,
            ),
        ),
    ]
    if tier >= 2:
        limit = "4" if tier == 2 else "6"
        jobs.append(
            Job(
                "compare",
                (python, str(source / "bounded_response_comparator.py"), "--limit", limit, "--out", str(output / "response_comparisons.jsonl")),
                output / "response_comparisons.jsonl",
                "bounded_response_comparator",
                1,
            )
        )
    return jobs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tier", type=int, required=True, choices=range(4))
    parser.add_argument("--root", default=".")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--shards", type=int, default=1)
    args = parser.parse_args()
    if args.shards != 1:
        raise SystemExit("shards other than 1 are not implemented; refusing a false sharding claim")

    root = Path(args.root).resolve()
    output = root / "outputs"
    logs = root / "logs"
    checkpoints = root / "checkpoints"
    for directory in (output, logs, checkpoints):
        directory.mkdir(parents=True, exist_ok=True)
    environment = checked_environment()
    sources = source_hashes(root)
    jobs = jobs_for_tier(root, args.tier)
    log_path = logs / f"tier{args.tier}.log"
    marker_path = output / f"TIER_{args.tier}_COMPLETE.json"
    # A failed or interrupted fresh invocation must not leave an older
    # completion marker that appears to certify the new source bundle.
    marker_path.unlink(missing_ok=True)

    with log_path.open("a" if args.resume else "w") as log:
        log.write(
            json.dumps(
                {
                    "event": "tier-start",
                    "tier": args.tier,
                    "resume": args.resume,
                    "shards": 1,
                    "environment": environment,
                    "source_bundle_hash": json_hash(sources),
                },
                sort_keys=True,
            )
            + "\n"
        )
        for job in jobs:
            checkpoint = checkpoints / f"tier{args.tier}_{job.name}.json"
            current_fingerprint = fingerprint(root, job, sources)
            if args.resume:
                reusable, reason = can_resume(
                    root, job, checkpoint, current_fingerprint
                )
                if reusable:
                    message = f"SKIP {job.name}: {reason}"
                    print(message, flush=True)
                    log.write(message + "\n")
                    log.flush()
                    continue
                log.write(f"RERUN {job.name}: {reason}\n")
                log.flush()
            execute_job(
                root=root,
                tier=args.tier,
                job=job,
                checkpoint=checkpoint,
                current_fingerprint=current_fingerprint,
                log=log,
            )

    completed_outputs = {relative(root, job.output): sha256(job.output) for job in jobs}
    marker = {
        "schema_version": COMPLETION_SCHEMA,
        "tier": args.tier,
        "status": "complete",
        "shards": 1,
        "command": recorded_runner_invocation(root, sys.argv),
        "environment": environment,
        "source_hashes": sources,
        "source_bundle_hash": json_hash(sources),
        "output_hashes": completed_outputs,
        "checkpoint_hashes": {
            relative(root, checkpoints / f"tier{args.tier}_{job.name}.json"): sha256(
                checkpoints / f"tier{args.tier}_{job.name}.json"
            )
            for job in jobs
        },
    }
    marker_path.write_text(json.dumps(marker, indent=2, sort_keys=True) + "\n")
    print(f"TIER_{args.tier}_COMPLETE jobs={len(jobs)}", flush=True)


if __name__ == "__main__":
    main()
