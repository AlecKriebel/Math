#!/usr/bin/env python3
"""Black-box mutation tests for the unified direct-closure verifier."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
AUDIT = Path(__file__).resolve().parent
SANDBOX = AUDIT / "_mutation_sandbox"
PRIMARY_SCRIPT = ROOT / "work/verify_four_port_direct_residual_closure.py"
PRIMARY_CERTIFICATE = ROOT / "work/four_port_direct_residual_closure_certificate.json"
PROOF_FILES = (
    "theta0_quintic_orbit_certificate.json",
    "theta_quartic_obstruction_certificates.json",
    "verify_theta_quartic_obstructions_independent.py",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_case(name: str, run_root: Path, *, optimized: bool = False):
    command = [sys.executable]
    if optimized:
        command.append("-O")
    command.extend(
        [
            str(SANDBOX / "work/verify_four_port_direct_residual_closure.py"),
            str(run_root),
            "--certificate",
            str(SANDBOX / f"outputs/{name}.json"),
        ]
    )
    started = time.perf_counter()
    completed = subprocess.run(command, text=True, capture_output=True)
    return {
        "name": name,
        "optimized": optimized,
        "returncode": completed.returncode,
        "elapsed_seconds": time.perf_counter() - started,
        "stdout_tail": completed.stdout.strip().splitlines()[-4:],
        "stderr_tail": completed.stderr.strip().splitlines()[-6:],
    }


def require_outcome(row: dict, should_pass: bool):
    observed = row["returncode"] == 0
    if observed != should_pass:
        raise RuntimeError(
            f"mutation outcome mismatch for {row['name']}: "
            f"expected pass={should_pass}, observed={observed}, row={row}"
        )


def copy_clean_artifacts():
    work = SANDBOX / "work"
    shutil.copy2(PRIMARY_SCRIPT, work / PRIMARY_SCRIPT.name)
    for filename in PROOF_FILES:
        shutil.copy2(ROOT / "work" / filename, work / filename)


def main():
    primary_before = {
        "verifier": sha(PRIMARY_SCRIPT),
        "certificate": sha(PRIMARY_CERTIFICATE),
    }
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    (SANDBOX / "work").mkdir(parents=True)
    (SANDBOX / "outputs").mkdir()
    (SANDBOX / "runs/higher_degree").mkdir(parents=True)
    (SANDBOX / "package").symlink_to(ROOT / "package", target_is_directory=True)
    cubic_name = "cubic_streaming_replay_s5_c9.json"
    shutil.copy2(
        ROOT / "runs/higher_degree" / cubic_name,
        SANDBOX / "runs/higher_degree" / cubic_name,
    )
    copy_clean_artifacts()

    results = []
    baseline = run_case("baseline", ROOT / "runs/four_port_full_v2")
    require_outcome(baseline, True)
    results.append({**baseline, "expected": "reject=False"})

    quintic_path = SANDBOX / "work/theta0_quintic_orbit_certificate.json"
    original_quintic = quintic_path.read_bytes()
    quintic = json.loads(original_quintic)
    quintic["invariant"][0][1] += 1
    quintic_path.write_text(json.dumps(quintic, indent=2, sort_keys=True) + "\n")
    row = run_case("mutated_quintic_coefficient", ROOT / "runs/four_port_full_v2")
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    quintic_path.write_bytes(original_quintic)

    quartic_path = SANDBOX / "work/theta_quartic_obstruction_certificates.json"
    original_quartic = quartic_path.read_bytes()
    quartic = json.loads(original_quartic)
    quartic["transports"][0]["port_match"] = [3, 2, 1, 0]
    quartic_path.write_text(json.dumps(quartic, indent=2, sort_keys=True) + "\n")
    row = run_case("mutated_quartic_transport", ROOT / "runs/four_port_full_v2")
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    optimized_row = run_case(
        "mutated_quartic_transport_python_O",
        ROOT / "runs/four_port_full_v2",
        optimized=True,
    )
    # This currently passes, documenting that assert-only validation is not
    # fail-closed under Python optimization.
    require_outcome(optimized_row, True)
    results.append(
        {
            **optimized_row,
            "expected": "known_fail_open=True",
            "finding": "Python -O removes every verifier assertion",
        }
    )
    quartic_path.write_bytes(original_quartic)

    cubic_path = SANDBOX / "runs/higher_degree" / cubic_name
    original_cubic = cubic_path.read_bytes()
    cubic = json.loads(original_cubic)
    cubic["results"][0]["certificate"]["coefficients"][0] += 1
    cubic_path.write_text(json.dumps(cubic, indent=2, sort_keys=True) + "\n")
    row = run_case("mutated_cubic_coefficient", ROOT / "runs/four_port_full_v2")
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    cubic_path.write_bytes(original_cubic)

    mutated_run = SANDBOX / "mutated_run"
    shutil.copytree(ROOT / "runs/four_port_full_v2", mutated_run)

    residual_9 = mutated_run / "source_5/records/class_000009.json"
    residual_10 = mutated_run / "source_5/records/class_000010.json"
    bytes_9 = residual_9.read_bytes()
    bytes_10 = residual_10.read_bytes()

    residual_9.unlink()
    row = run_case("dropped_expected_residual_record", mutated_run)
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    residual_9.write_bytes(bytes_9)

    residual_9.write_bytes(bytes_10)
    residual_10.write_bytes(bytes_9)
    row = run_case("swapped_expected_residual_records", mutated_run)
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    residual_9.write_bytes(bytes_9)
    residual_10.write_bytes(bytes_10)

    mutated_record = json.loads(bytes_9)
    mutated_record["members"][0]["port_match"] = [1, 0, 2, 3]
    residual_9.write_text(json.dumps(mutated_record, indent=2, sort_keys=True) + "\n")
    row = run_case("mutated_expected_record_mapping", mutated_run)
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    residual_9.write_bytes(bytes_9)

    manifest_path = mutated_run / "source_5/residual_manifest.json"
    original_manifest = manifest_path.read_bytes()
    manifest = json.loads(original_manifest)
    manifest["unresolved"].remove(9)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    row = run_case("dropped_expected_residual_manifest_mapping", mutated_run)
    require_outcome(row, False)
    results.append({**row, "expected": "reject=True"})
    manifest_path.write_bytes(original_manifest)

    # The unified verifier does not reopen nonresidual records or recompute the
    # manifest/sweep roots.  Demonstrate this bounded census gap explicitly.
    nonresidual = mutated_run / "source_0/records/class_000000.json"
    nonresidual.unlink()
    row = run_case("dropped_nonresidual_production_record", mutated_run)
    require_outcome(row, True)
    results.append(
        {
            **row,
            "expected": "known_fail_open=True",
            "finding": "unified verifier trusts stale completion/semantic-root fields outside the 36 residual records",
        }
    )

    primary_after = {
        "verifier": sha(PRIMARY_SCRIPT),
        "certificate": sha(PRIMARY_CERTIFICATE),
    }
    if primary_after != primary_before:
        raise RuntimeError("primary artifacts changed during mutation sandbox audit")

    report = {
        "schema": "k2p-four-port-unified-verifier-black-box-mutations-v1",
        "result": "PASS_WITH_TWO_FAIL_CLOSED_GAPS",
        "primary_sha256": primary_before,
        "cases": results,
        "rejections_observed": sum(
            row["returncode"] != 0 for row in results
        ),
        "known_fail_open_cases": [
            row["name"] for row in results if row.get("expected") == "known_fail_open=True"
        ],
    }
    destination = AUDIT / "mutation_test_report.json"
    destination.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    shutil.rmtree(SANDBOX)
    print("UNIFIED_VERIFIER_MUTATION_AUDIT_COMPLETE")
    print(f"cases={len(results)} rejected={report['rejections_observed']}")
    print(f"known_fail_open={report['known_fail_open_cases']}")
    print(f"report_sha256={sha(destination)}")


if __name__ == "__main__":
    main()
