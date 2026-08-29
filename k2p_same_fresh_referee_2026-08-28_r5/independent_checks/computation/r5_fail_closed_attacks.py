#!/usr/bin/env python3
"""Reviewer-owned attacks on the two R4 fail-closed defects.

This script does not import a submitted verifier as its decision procedure.
It constructs the exact former duplicate-name attack, performs a coherent
probe-layer reseal, invokes the production verifier as the object under test,
and independently exercises the portable entry points and atlas invariants in
normal and optimized Python modes.  All mutated files live in temporary
directories.
"""

from __future__ import annotations

import argparse
import ast
import gzip
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


class AttackFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise AttackFailure(code if detail is None else f"{code}:{detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha_object(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_fingerprint(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        relative = path.relative_to(root).as_posix().encode("utf-8")
        payload = path.read_bytes()
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        digest.update(len(payload).to_bytes(8, "big"))
        digest.update(payload)
    return digest.hexdigest()


def write_mutant_ledger(
    source: Path, destination: Path, *, conflicting: bool
) -> dict[str, Any]:
    with gzip.open(source, "rb") as incoming, destination.open("wb") as raw:
        first = incoming.readline()
        require(first.startswith(b"{") and first.endswith(b"\n"), "DUPLICATE_FIXTURE")
        original = json.loads(first)
        name = "parent_anchor_id"
        require(name in original, "DUPLICATE_FIELD_MISSING")
        earlier = "R5-CONFLICTING-EARLIER-VALUE" if conflicting else original[name]
        prefix = canonical_bytes(name) + b":" + canonical_bytes(earlier) + b","
        mutant = b"{" + prefix + first[1:]
        require(json.loads(mutant) == original, "LAST_VALUE_SEMANTICS_CHANGED")
        with gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, mtime=0, compresslevel=6
        ) as encoded:
            encoded.write(mutant)
            for block in iter(lambda: incoming.read(1024 * 1024), b""):
                encoded.write(block)
    return {
        "conflicting": conflicting,
        "duplicate_name": name,
        "earlier_value": earlier,
        "later_effective_value": original[name],
        "default_decoder_semantics_unchanged": True,
        "mutated_line_is_noncanonical": mutant != canonical_bytes(original) + b"\n",
    }


def duplicate_attack(project: Path, python: Path, conflicting: bool) -> dict[str, Any]:
    layer = project / "work/probe_coherence_corrected"
    verifier = layer / "verify_probe_coherence_corrected.py"
    required = (
        "exact_transport_ledger.jsonl.gz",
        "parent_restriction_ledger.jsonl.gz",
        "separation_proof_registry.json.gz",
        "two_port_parent_inventory.jsonl.gz",
        "two_port_ledger.jsonl.gz",
    )
    with tempfile.TemporaryDirectory(prefix="r5_duplicate_attack_") as raw_temp:
        clone = Path(raw_temp) / "probe"
        clone.mkdir()
        for name in required:
            os.link(layer / name, clone / name)
        mutation = write_mutant_ledger(
            layer / "one_port_ledger.jsonl.gz",
            clone / "one_port_ledger.jsonl.gz",
            conflicting=conflicting,
        )
        certificate = json.loads(
            (layer / "probe_coherence_certificate.json").read_text(encoding="utf-8")
        )
        old_hash = certificate["one_port"]["ledger_sha256"]
        new_hash = sha_file(clone / "one_port_ledger.jsonl.gz")
        require(old_hash != new_hash, "DUPLICATE_HASH_UNCHANGED")
        certificate["one_port"]["ledger_sha256"] = new_hash
        certificate.pop("payload_sha256", None)
        logical = dict(certificate)
        logical.pop("operational", None)
        certificate["payload_sha256"] = sha_object(logical)
        (clone / "probe_coherence_certificate.json").write_text(
            json.dumps(certificate, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        output = clone / "verification.json"
        command = [
            str(python),
            "-B",
            str(verifier),
            "--package-dir",
            str(clone),
            "--output",
            str(output),
        ]
        completed = subprocess.run(
            command,
            cwd=project,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=240,
            check=False,
        )
        kind = "conflicting" if conflicting else "same"
        expected = (
            "CORRECTED_PROBE_REPLAY_FAIL:STRICT_JSON_DUPLICATE_NAME:"
            "one_port_ledger.jsonl.gz:line=1:name='parent_anchor_id'"
        )
        require(completed.returncode == 1, "DUPLICATE_EXIT", (kind, completed.returncode))
        require(completed.stdout.strip() == expected, "DUPLICATE_DIAGNOSTIC", completed.stdout)
        require(not output.exists(), "DUPLICATE_SUCCESS_ARTIFACT", kind)
        return {
            "kind": kind,
            "attack": mutation,
            "old_ledger_sha256": old_hash,
            "mutant_ledger_sha256": new_hash,
            "coherent_layer_payload_sha256": certificate["payload_sha256"],
            "verifier_exit_code": completed.returncode,
            "observed_diagnostic": completed.stdout.strip(),
            "success_artifact_absent": True,
            "status": "REJECTED_FOR_DUPLICATE_NAME",
        }


def invoke_optimized(
    python: Path,
    path: Path,
    arguments: tuple[str, ...],
    *,
    mode: str,
    cwd: Path,
    shell: bool = False,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.pop("PYTHONOPTIMIZE", None)
    if shell:
        if mode == "dash_O":
            wrapper = cwd / "python-O"
            wrapper.write_text(
                "#!/usr/bin/env bash\n"
                f'exec {shlex.quote(str(python))} -O "$@"\n',
                encoding="utf-8",
            )
            wrapper.chmod(0o700)
            environment["PYTHON_BIN"] = str(wrapper)
        else:
            environment["PYTHON_BIN"] = str(python)
            environment["PYTHONOPTIMIZE"] = "1"
        command = ["bash", str(path), *arguments]
    else:
        command = [str(python), "-B", str(path), *arguments]
        if mode == "dash_O":
            command.insert(1, "-O")
        else:
            environment["PYTHONOPTIMIZE"] = "1"
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=30,
        check=False,
    )


def optimized_entrypoint_attacks(project: Path, python: Path) -> list[dict[str, Any]]:
    portable = project / "package/referee/k2p_offline_sweep_portable"
    cases = (
        ("verify_package", "verify_package.py", ("--skip-smoke", "--skip-mutations", "--skip-prepared-audit"), False),
        ("guarded_run", "guarded_run.py", ("SCRATCH/guarded", "--skip-package-verify", "--min-start-free-gib", "0", "--min-runtime-free-gib", "0"), False),
        ("resumable_driver", "resumable_four_port_driver.py", ("--package-root", str(portable), "--output-root", "SCRATCH/driver", "--source-index", "0", "--start", "0", "--end", "1"), False),
        ("merge_manifests", "merge_manifests.py", ("--package-root", str(portable), "--run-root", "SCRATCH/merge"), False),
        ("compare_semantic_runs", "compare_semantic_runs.py", ("SCRATCH/left", "SCRATCH/right"), False),
        ("direct_residual_replay", "proofs/verify_four_port_direct_residual_closure.py", (), False),
        ("run_all_sources", "run_all_sources.sh", ("SCRATCH/shell",), True),
    )
    rows = []
    for mode in ("dash_O", "environment"):
        for name, relative, raw_arguments, shell in cases:
            with tempfile.TemporaryDirectory(prefix="r5_optimized_entry_") as raw_temp:
                scratch = Path(raw_temp)
                arguments = tuple(
                    value.replace("SCRATCH", str(scratch)) for value in raw_arguments
                )
                completed = invoke_optimized(
                    python,
                    portable / relative,
                    arguments,
                    mode=mode,
                    cwd=scratch,
                    shell=shell,
                )
                expected = "K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN"
                require(completed.returncode == 1, "OPTIMIZED_EXIT", (name, mode, completed.returncode))
                require(completed.stdout.strip() == expected, "OPTIMIZED_DIAGNOSTIC", (name, mode, completed.stdout))
                residuals = sorted(
                    item.relative_to(scratch).as_posix()
                    for item in scratch.rglob("*")
                    if item.name != "python-O"
                )
                require(not residuals, "OPTIMIZED_RESIDUAL", (name, mode, residuals))
                rows.append(
                    {
                        "entry_point": name,
                        "mode": mode,
                        "exit_code": 1,
                        "diagnostic": expected,
                        "residual_output_absent": True,
                    }
                )
    return rows


SEMANTIC_PROBE = r'''
import importlib.util
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("r5_atlas_probe", path)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
constant = (((), ((0, 1),)),)
outputs = tuple(constant for _ in module.orbit_assignments(4))
descriptor = module.MapDescriptor(4, 0, 0, outputs, ())
unit = lambda columns: ((1,) + (0,) * (len(columns) - 1),)
tests = (
    ("reference", "ATLAS_TARGET_PULLBACK_NONZERO degree=2 engine=reference",
     "exact_kernel_sparse_columns", lambda: module.quadratic_separator(descriptor, descriptor)),
    ("fast", "ATLAS_TARGET_PULLBACK_NONZERO degree=2 engine=fast",
     "kernel_sparse_columns_fast", lambda: module.quadratic_separator_fast(descriptor, descriptor)),
    ("cubic", "ATLAS_TARGET_PULLBACK_NONZERO degree=3 engine=fast",
     "kernel_sparse_columns_fast", lambda: module.cubic_separator_fast(descriptor, descriptor)),
    ("homogeneous", "ATLAS_TARGET_PULLBACK_NONZERO degree=4 engine=homogeneous",
     "kernel_sparse_columns_fast", lambda: module.homogeneous_separator_fast(descriptor, descriptor, 4, 1000)),
    ("subset", "ATLAS_TARGET_PULLBACK_NONZERO degree=3 engine=subset",
     "kernel_sparse_columns_fast", lambda: module.homogeneous_separator_subset(descriptor, descriptor, 3, tuple(range(len(outputs))))),
    ("positive_target", "ATLAS_SOURCE_PULLBACK_NONZERO degree=2 engine=positive_target",
     "kernel_sparse_columns_fast", lambda: module.source_invariant_positive_target(descriptor, descriptor)),
)
observed = []
for name, expected, kernel_name, operation in tests:
    original = getattr(module, kernel_name)
    setattr(module, kernel_name, unit)
    try:
        operation()
    except module.AtlasInvariantError as error:
        if str(error) != expected:
            raise
        observed.append(name)
    else:
        raise SystemExit("FALSE_CERTIFICATE_ACCEPTED:" + name)
    finally:
        setattr(module, kernel_name, original)
print(",".join(observed))
'''


def atlas_assertion_attacks(project: Path, python: Path) -> dict[str, Any]:
    atlas = project / "package/referee/k2p_offline_sweep_portable/atlas/k2p_atlas_core.py"
    parsed = ast.parse(atlas.read_text(encoding="utf-8"), filename=str(atlas))
    assert_lines = [node.lineno for node in ast.walk(parsed) if isinstance(node, ast.Assert)]
    require(not assert_lines, "ATLAS_ASSERTS_REMAIN", assert_lines)
    expected = "reference,fast,cubic,homogeneous,subset,positive_target"
    rows = []
    for mode in ("normal", "dash_O", "environment"):
        environment = os.environ.copy()
        environment.pop("PYTHONOPTIMIZE", None)
        command = [str(python), "-B", "-c", SEMANTIC_PROBE, str(atlas)]
        if mode == "dash_O":
            command.insert(1, "-O")
        elif mode == "environment":
            environment["PYTHONOPTIMIZE"] = "1"
        completed = subprocess.run(
            command,
            cwd=project,
            env=environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=60,
            check=False,
        )
        require(completed.returncode == 0, "ATLAS_PROBE_EXIT", (mode, completed.stdout))
        require(completed.stdout.strip() == expected, "ATLAS_PROBE_RESULT", (mode, completed.stdout))
        rows.append({"mode": mode, "invariants_rejected": expected.split(",")})
    return {"atlas_sha256": sha_file(atlas), "assert_statement_count": 0, "modes": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--python", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    # Keep a virtual-environment interpreter's lexical path.  Resolving its
    # symlink to the base executable would discard the venv's site-packages.
    python = args.python.absolute()
    require(project.is_dir(), "PROJECT_MISSING", project)
    require(python.is_file(), "PYTHON_MISSING", python)
    portable = project / "package/referee/k2p_offline_sweep_portable"
    before = tree_fingerprint(portable)
    started = time.monotonic()
    result = {
        "schema": "r5-reviewer-fail-closed-attacks-v1",
        "source_project": str(project),
        "source_portable_fingerprint_before": before,
        "duplicate_jsonl_attacks": [
            duplicate_attack(project, python, False),
            duplicate_attack(project, python, True),
        ],
        "optimized_entrypoint_attacks": optimized_entrypoint_attacks(project, python),
        "atlas_assertion_attacks": atlas_assertion_attacks(project, python),
        "runtime_seconds": time.monotonic() - started,
        "status": "PASS",
    }
    after = tree_fingerprint(portable)
    require(after == before, "SOURCE_PORTABLE_DRIFT", (before, after))
    result["source_portable_fingerprint_after"] = after
    result["payload_sha256"] = sha_object(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "duplicate_attacks_rejected": len(result["duplicate_jsonl_attacks"]),
                "optimized_entrypoint_attacks_rejected": len(result["optimized_entrypoint_attacks"]),
                "atlas_modes": len(result["atlas_assertion_attacks"]["modes"]),
                "payload_sha256": result["payload_sha256"],
                "status": result["status"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except AttackFailure as error:
        raise SystemExit(f"R5_FAIL_CLOSED_ATTACK_FAIL:{error}")
