#!/usr/bin/env python3
"""Adversarial refusal tests for the principal-D+ theorem gate."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ASSEMBLY = Path(__file__).resolve().parent
VERIFIER = ASSEMBLY / "verify_theorem_gates.py"


def fail(code: str, detail: object = None) -> "None":
    raise SystemExit(code if detail is None else f"{code}: {detail}")


def environment() -> dict[str, str]:
    result = dict(os.environ)
    result.pop("PYTHONOPTIMIZE", None)
    result["PYTHONDONTWRITEBYTECODE"] = "1"
    return result


def run(extra: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            [sys.executable, "-B", str(VERIFIER), *extra],
            cwd=VERIFIER.parents[2],
            env=environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired:
        fail("THEOREM_GATE_MUTATION_TIMEOUT")


def require(result: subprocess.CompletedProcess[bytes], *, success: bool, marker: bytes) -> None:
    output = result.stdout + result.stderr
    if (result.returncode == 0) != success or marker not in output:
        fail("THEOREM_GATE_MUTATION_EXPECTATION_FAIL", output.decode(errors="replace")[-4000:])


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main() -> None:
    if not __debug__:
        fail("THEOREM_GATE_MUTATION_OPTIMIZED_MODE_FORBIDDEN")
    baseline = run([])
    require(baseline, success=True, marker=b"K2P_SAME_NOT_PROMOTABLE")
    promotion = run(["--require-promotable"])
    require(promotion, success=False, marker=b"K2P_SAME_PROMOTION_REFUSED")
    baseline_output = baseline.stdout + baseline.stderr
    for marker in (b"RAW_LEDGER_GAPS=6", b"RESTORATION_LEDGER_GAP_COUNT=2962"):
        if marker not in baseline_output:
            fail("THEOREM_GATE_HARD_BLOCKER_NOT_REPORTED", marker.decode())

    with tempfile.TemporaryDirectory(prefix="k2p_theorem_gate_mutations_") as temporary:
        temporary_root = Path(temporary)
        config = json.loads((ASSEMBLY / "THEOREM_GATES.json").read_text())

        missing_gate = json.loads(json.dumps(config))
        missing_gate["gates"] = missing_gate["gates"][:-1]
        missing_gate_path = temporary_root / "missing_gate.json"
        write_json(missing_gate_path, missing_gate)
        result = run(["--config", str(missing_gate_path)])
        require(result, success=False, marker=b"THEOREM_GATE_ROW_ID_SET_FAIL")

        false_promotion = json.loads(json.dumps(config))
        false_promotion["status"] = "PROMOTABLE"
        false_promotion_path = temporary_root / "false_promotion.json"
        write_json(false_promotion_path, false_promotion)
        result = run(["--config", str(false_promotion_path)])
        require(result, success=False, marker=b"THEOREM_GATE_CONFIG_STATUS_MISMATCH")

        raw = json.loads((ASSEMBLY / "raw_universe_ledger.status.json").read_text())
        raw["complete"] = True
        raw["gap_count"] = 0
        raw["graph_derived"] = True
        raw["partition_identity_verified"] = True
        raw["raw_to_canonical_map_bound"] = True
        raw["valid_dimension_upper_bounds_certified"] = True
        raw["scopes"]["four_port"]["accounted_presentations"] = 405216
        raw["scopes"]["five_port_theta2"] = {
            "accounted_presentations": 1,
            "expected_presentations": 1,
            "status": "complete"
        }
        raw_path = temporary_root / "fake_zero_raw.json"
        write_json(raw_path, raw)
        result = run(["--raw-ledger", str(raw_path), "--require-promotable"])
        require(result, success=False, marker=b"K2P_SAME_PROMOTION_REFUSED")
        if b"RESTORATION_LEDGER_GAP_COUNT=2962" not in result.stdout + result.stderr:
            fail("THEOREM_GATE_RESTORATION_NOT_INDEPENDENTLY_REQUIRED")

        restoration = json.loads((ASSEMBLY / "restoration_ledger.status.json").read_text())
        restoration.update({
            "all_child_records_hash_bound": True,
            "all_implications_replayed": True,
            "child_records_bound": 2962,
            "closed_child_requests": 2962,
            "coherent_probe_deck_verified": True,
            "complete": True,
            "gap_count": 0,
            "incoherent_survivors": 0,
            "unresolved_child_requests": 0,
        })
        restoration_path = temporary_root / "fake_zero_restoration.json"
        write_json(restoration_path, restoration)
        result = run([
            "--restoration-ledger", str(restoration_path), "--require-promotable"
        ])
        require(result, success=False, marker=b"K2P_SAME_PROMOTION_REFUSED")
        if b"RAW_LEDGER_GAPS=6" not in result.stdout + result.stderr:
            fail("THEOREM_GATE_RAW_LEDGER_NOT_INDEPENDENTLY_REQUIRED")

    optimized = subprocess.run(
        [sys.executable, "-O", "-B", str(VERIFIER)],
        cwd=VERIFIER.parents[2], env=environment(),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False,
    )
    require(optimized, success=False, marker=b"THEOREM_GATE_OPTIMIZED_MODE_FORBIDDEN")
    print("K2P_THEOREM_GATE_FAIL_CLOSED_TESTS_PASS")


if __name__ == "__main__":
    main()
