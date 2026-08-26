#!/usr/bin/env python3
"""Extract stable machine reports and resource data from fresh referee logs."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOGS = ROOT / "logs"
REPRO = ROOT / "independent_checks/reproductions"
REPORTS = ROOT / "reports"
EXECUTION_PROJECT = (
    ROOT / "tmp/execution/k2p_principal_d_plus_submission_referee"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def last_json(path: Path) -> dict:
    for line in reversed(path.read_text(encoding="utf-8").splitlines()):
        if line.startswith("{"):
            value = json.loads(line)
            if isinstance(value, dict):
                return value
    raise ValueError(f"no JSON object line in {path}")


def resources(path: Path) -> dict[str, float | int | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    wall = re.findall(r"^\s*([0-9.]+) real\b", text, flags=re.MULTILINE)
    rss = re.findall(
        r"^\s*([0-9]+)\s+maximum resident set size\b",
        text,
        flags=re.MULTILINE,
    )
    return {
        "wall_seconds": float(wall[-1]) if wall else None,
        "maximum_resident_set_size_bytes": int(rss[-1]) if rss else None,
    }


def command_row(
    name: str,
    command: str,
    stdout: Path,
    stderr: Path,
    *,
    cwd: Path = EXECUTION_PROJECT,
    exit_code: int = 0,
) -> dict:
    row = {
        "name": name,
        "command": command,
        "cwd": str(cwd),
        "exit_code": exit_code,
        "stdout_sha256": sha256(stdout),
        "stderr_sha256": sha256(stderr),
    }
    row.update(resources(stderr))
    return row


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    parsed = {}
    for name in ("release_quick", "release_mutations", "release_full"):
        value = last_json(LOGS / f"{name}.stdout")
        output = LOGS / f"{name}_report.json"
        output.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        parsed[name] = value

    rows = [
        command_row(
            "venv_create",
            "python3 -m venv .venv",
            LOGS / "venv_create.stdout",
            LOGS / "venv_create.stderr",
        ),
        command_row(
            "pip_upgrade",
            ".venv/bin/python -m pip install --upgrade pip",
            LOGS / "pip_upgrade.stdout",
            LOGS / "pip_upgrade.stderr",
        ),
        command_row(
            "requirements_install",
            ".venv/bin/python -m pip install -r work/final_theorem_release/requirements.txt",
            LOGS / "pip_requirements.stdout",
            LOGS / "pip_requirements.stderr",
        ),
        command_row(
            "portable_bundle_check",
            ".venv/bin/python -B output/referee/build_referee_bundle.py --check-only",
            LOGS / "bundle_check.stdout",
            LOGS / "bundle_check.stderr",
        ),
        command_row(
            "release_lock_check",
            ".venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready",
            LOGS / "release_lock_check.stdout",
            LOGS / "release_lock_check.stderr",
        ),
        command_row(
            "release_quick",
            ".venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick",
            LOGS / "release_quick.stdout",
            LOGS / "release_quick.stderr",
        ),
        command_row(
            "release_mutation_output_contract",
            ".venv/bin/python -B work/final_theorem_release/test_release_mutation_output_contract.py",
            LOGS / "release_mutation_output_contract.stdout",
            LOGS / "release_mutation_output_contract.stderr",
        ),
        command_row(
            "nested_mutation_output_contract",
            ".venv/bin/python -B work/final_theorem_release/test_nested_mutation_output_contract.py",
            LOGS / "nested_mutation_output_contract.stdout",
            LOGS / "nested_mutation_output_contract.stderr",
        ),
        command_row(
            "release_mutations",
            ".venv/bin/python -B work/final_theorem_release/run_release_mutations.py",
            LOGS / "release_mutations.stdout",
            LOGS / "release_mutations.stderr",
        ),
        command_row(
            "release_full",
            ".venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full",
            LOGS / "release_full.stdout",
            LOGS / "release_full.stderr",
        ),
        command_row(
            "canonicalizer_missing_dependency_attack",
            "/opt/homebrew/bin/python3 -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output <external-report>",
            REPRO / "canonicalizer_missing_dependency.stdout",
            REPRO / "canonicalizer_missing_dependency.stderr",
            cwd=ROOT / "isolated/k2p_principal_d_plus_submission_referee",
        ),
        command_row(
            "canonicalizer_qualified_control",
            "<qualified-python> -B work/canonicalizer_completeness/test_canonicalizer_mutations.py --output <external-report>",
            REPRO / "canonicalizer_qualified_control.stdout",
            REPRO / "canonicalizer_qualified_control.stderr",
            cwd=ROOT / "isolated/k2p_principal_d_plus_submission_referee",
        ),
        command_row(
            "parameter_transport_mutations",
            "<qualified-python> -B work/canonicalizer_completeness/inheritance_transport/run_parameter_transport_mutations.py --output <external-report>",
            REPRO / "parameter_transport_mutation.stdout",
            REPRO / "parameter_transport_mutation.stderr",
            cwd=ROOT / "isolated/k2p_principal_d_plus_submission_referee",
        ),
        command_row(
            "restoration_mutations_fresh",
            ".venv/bin/python -B work/restoration_sign_reclassification/mutate_corrected_restoration_forest.py",
            REPRO / "restoration_mutation_fresh.stdout",
            REPRO / "restoration_mutation_fresh.stderr",
        ),
        command_row(
            "probe_mutations_fresh",
            ".venv/bin/python -B work/probe_coherence_corrected/run_probe_coherence_mutations.py",
            REPRO / "probe_mutation_fresh.stdout",
            REPRO / "probe_mutation_fresh.stderr",
        ),
    ]

    registry = {
        "schema": "k2p-fresh-referee-root-execution-registry-v1",
        "environment": {
            "os": "macOS 26.5.2 build 25F84",
            "architecture": "arm64",
            "cpu": "Apple M1 Pro",
            "logical_cores": 10,
            "memory_bytes": 17_179_869_184,
            "python": "3.14.6",
            "networkx": "3.5",
            "sympy": "1.14.0",
            "tectonic": "0.16.9",
            "poppler": "26.08.0",
        },
        "commands": rows,
        "fresh_results": {
            "quick_layer_count": len(parsed["release_quick"]["layer_replays"]),
            "quick_status": parsed["release_quick"]["status"],
            "full_layer_count": len(parsed["release_full"]["layer_replays"]),
            "full_status": parsed["release_full"]["status"],
            "mutation_count": parsed["release_mutations"]["observed_mutation_count"],
            "mutation_status": parsed["release_mutations"]["status"],
            "mutation_survivors": parsed["release_mutations"]["survivors"],
        },
    }
    registry["payload_sha256"] = hashlib.sha256(
        json.dumps(registry, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    (REPORTS / "ROOT_EXECUTION_REGISTRY.json").write_text(
        json.dumps(registry, indent=2, sort_keys=True) + "\n"
    )


if __name__ == "__main__":
    main()
