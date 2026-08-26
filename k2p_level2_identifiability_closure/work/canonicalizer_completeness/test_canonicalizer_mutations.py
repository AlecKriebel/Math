#!/usr/bin/env python3
"""Targeted live mutations of the two formerly missing triangle guards."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ATLAS = PROJECT / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
AUTHORITATIVE_OUTPUT = HERE / "canonicalizer_completeness_mutation_certificate.json"
MUTATION_DIAGNOSTICS = {
    "accept_nonordinary_split_heads": (
        "CANONICALIZER_COMPLETENESS_FAIL:NONORDINARY_ATLAS_ACCEPTED"
    ),
    "erase_without_marking_selected_triangle": (
        "CANONICALIZER_COMPLETENESS_FAIL:SELECTED_TRIANGLE_ATLAS_ACCEPTED: triangle"
    ),
}
FORBIDDEN_FAILURE_MARKERS = (
    "Traceback (most recent call last)",
    "ModuleNotFoundError",
    "ImportError",
    "No module named",
)


def sha_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_output_path(output: Path, allow_authoritative_output: bool) -> Path:
    lexical = Path(os.path.abspath(os.fspath(output)))
    normalized = lexical.parent.resolve() / lexical.name
    resolved = lexical.resolve()
    authoritative = AUTHORITATIVE_OUTPUT.parent.resolve() / AUTHORITATIVE_OUTPUT.name
    if allow_authoritative_output:
        if normalized != authoritative or lexical.is_symlink():
            raise SystemExit(
                "CANONICALIZER_MUTATION_OUTPUT_POLICY_FAIL: authoritative override "
                "licenses only the nonsymbolic canonical mutation certificate"
            )
        return normalized
    try:
        resolved.relative_to(PROJECT.resolve())
    except ValueError:
        return normalized
    raise SystemExit(
        "CANONICALIZER_MUTATION_OUTPUT_POLICY_FAIL: routine output must be "
        "outside the project source tree"
    )


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
    finally:
        if temporary.exists():
            temporary.unlink()


def prepare_output(path: Path) -> None:
    """Remove stale caller-owned PASS bytes before any fallible audit work."""

    path.unlink(missing_ok=True)


def run_semantic_audit(atlas: Path, success_artifact: Path):
    try:
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(HERE / "canonicalizer_audit.py"),
                "--semantic-only",
                "--atlas",
                str(atlas),
                "--output",
                str(success_artifact),
            ],
            cwd=PROJECT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise SystemExit("CANONICALIZER_MUTATION_TIMEOUT") from error
    return completed


def require_clean_baseline():
    with tempfile.TemporaryDirectory(prefix="k2p-canonicalizer-baseline-") as temporary:
        success_artifact = Path(temporary) / "semantic-success.json"
        completed = run_semantic_audit(ATLAS, success_artifact)
        output = completed.stdout.strip()
        if completed.returncode != 0:
            raise SystemExit(
                f"CANONICALIZER_MUTATION_BASELINE_EXIT:{completed.returncode}:{output[-1000:]}"
            )
        if any(marker in output for marker in FORBIDDEN_FAILURE_MARKERS):
            raise SystemExit(f"CANONICALIZER_MUTATION_BASELINE_CRASH:{output[-1000:]}")
        if success_artifact.exists():
            raise SystemExit("CANONICALIZER_MUTATION_BASELINE_UNEXPECTED_ARTIFACT")
        try:
            parsed = json.loads(output)
        except json.JSONDecodeError as error:
            raise SystemExit(
                f"CANONICALIZER_MUTATION_BASELINE_OUTPUT:{output[-1000:]}"
            ) from error
        expected_contract = {
            "nonordinary_triangle": {
                "atlas_ordinary_candidates": 0,
                "conclusion": "rejected",
                "independent_ordinary_candidates": 0,
                "legacy_all_three_cycles_would_accept": True,
            },
            "selected_triangle_mismatch": {
                "atlas_marked_relation": "none",
                "conclusion": "rejected",
                "independent_marked_relation": "none",
                "unmarked_head_erasure_relation": "triangle",
            },
        }
        if parsed != {
            "status": "PASS",
            "semantic_mutation_contract": expected_contract,
        }:
            raise SystemExit(f"CANONICALIZER_MUTATION_BASELINE_SEMANTICS:{parsed}")
        return {
            "returncode": 0,
            "status": "PASS",
            "mode": "semantic-only",
            "artifact_contract": (
                "The semantic-only auditor reports PASS on stdout and intentionally "
                "must not create the supplied --output success artifact."
            ),
            "semantic_mutation_contract": expected_contract,
            "success_artifact_absent": True,
            "timeout": False,
            "signal": False,
        }


def qualify_mutation_failure(name: str, completed, success_artifact: Path):
    diagnostic = completed.stdout.strip()
    expected = MUTATION_DIAGNOSTICS[name]
    if completed.returncode < 0:
        raise SystemExit(f"CANONICALIZER_MUTATION_SIGNAL:{name}:{completed.returncode}")
    if completed.returncode != 1:
        raise SystemExit(
            f"CANONICALIZER_MUTATION_BAD_EXIT:{name}:{completed.returncode}:{diagnostic[-1000:]}"
        )
    if any(marker in diagnostic for marker in FORBIDDEN_FAILURE_MARKERS):
        raise SystemExit(f"CANONICALIZER_MUTATION_CRASH:{name}:{diagnostic[-1000:]}")
    if success_artifact.exists():
        raise SystemExit(f"CANONICALIZER_MUTATION_SUCCESS_ARTIFACT:{name}")
    if diagnostic != expected:
        raise SystemExit(
            f"CANONICALIZER_MUTATION_WRONG_DIAGNOSTIC:{name}:{diagnostic[-1000:]}"
        )
    return {
        "name": name,
        "rejected": True,
        "exit_code": 1,
        "expected_diagnostic": expected,
        "observed_diagnostic": diagnostic,
        "success_artifact_absent": True,
        "timeout": False,
        "signal": False,
    }


def run_mutation(name, old, new):
    source = ATLAS.read_text()
    if source.count(old) != 1:
        raise SystemExit(f"MUTATION_SITE_FAIL:{name}:{source.count(old)}")
    with tempfile.TemporaryDirectory(prefix=f"k2p-canonicalizer-{name}-") as temporary:
        mutated = Path(temporary) / "k2p_atlas_core.py"
        mutated.write_text(source.replace(old, new))
        success_artifact = Path(temporary) / "semantic-success.json"
        completed = run_semantic_audit(mutated, success_artifact)
        result = qualify_mutation_failure(name, completed, success_artifact)
        result["mutated_atlas_sha256"] = sha_file(mutated)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-authoritative-output", action="store_true")
    args = parser.parse_args()
    output = validate_output_path(args.output, args.allow_authoritative_output)
    prepare_output(output)
    if not __debug__:
        raise SystemExit("CANONICALIZER_MUTATIONS_OPTIMIZED_MODE_FORBIDDEN")
    baseline = require_clean_baseline()
    results = [
        run_mutation(
            "accept_nonordinary_split_heads",
            "if not valid or len(headed)!=2 or headed[0]!=headed[1]:continue",
            "if not valid or len(headed)!=2:continue",
        ),
        run_mutation(
            "erase_without_marking_selected_triangle",
            "kind='forgotten_triangle_edge' if forget else 'edge',",
            "kind='edge',",
        ),
    ]
    report = {
        "schema": "k2p-canonicalizer-completeness-mutations-v2",
        "status": "PASS",
        "clean_baseline": baseline,
        "diagnostic_contract": MUTATION_DIAGNOSTICS,
        "mutations": results,
        "rejected": len(results),
        "survived": 0,
        "atlas_sha256": sha_file(ATLAS),
        "auditor_sha256": sha_file(HERE / "canonicalizer_audit.py"),
        "mutation_runner_sha256": sha_file(Path(__file__).resolve()),
    }
    payload = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["payload_sha256"] = hashlib.sha256(payload).hexdigest()
    atomic_write_text(output, json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("K2P_CANONICALIZER_MUTATIONS_PASS rejected=2 survived=0")


if __name__ == "__main__":
    main()
