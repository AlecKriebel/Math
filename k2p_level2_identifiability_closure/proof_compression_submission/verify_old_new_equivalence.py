#!/usr/bin/env python3
"""Replay every load-bearing old/new proof-compression comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
OUTPUT = ROOT / "results/OLD_NEW_EQUIVALENCE_RESULT.json"

COMMANDS = (
    {
        "id": "baseline_and_finite_universe_producer",
        "script": "proof_compression_submission/analysis/derive_baseline_and_universe.py",
        "payload_key": "payload_sha256",
        "payload": "3ea5a391742ecb5cfe413f4578af8ebca5ce02ebddb3ab45f7f52b7a79556c70",
    },
    {
        "id": "direct_template_producer",
        "script": "proof_compression_submission/templates/derive_direct_templates.py",
        "payload_key": "payload_sha256",
        "payload": "c5ce4176e0020cfc01b8d8351f02c87df6e87663b37d372669216ad5bd08be47",
    },
    {
        "id": "independent_family_coverage_equivalence",
        "script": "proof_compression_submission/analysis/verify_family_coverage_equivalence.py",
        "payload_key": "payload_sha256",
        "payload": "8f100ed7c3e98b05d16956f80a50f0f2d61e6349c376e32acfdfb55c15a33987",
    },
    {
        "id": "restoration_archetype_producer",
        "script": "proof_compression_submission/restoration/analyze_restoration_archetypes.py",
        "payload_key": "payload_sha256",
        "payload": "f0215c897773be25ae756e61f8ed2942705ce8f400163f80c32f204b60cea454",
    },
    {
        "id": "independent_restoration_archetype_replay",
        "script": "proof_compression_submission/restoration/verify_restoration_archetypes.py",
        "payload_key": "payload_sha256",
        "payload": "8f3134bd2cb2f01f6a91cfe90fe536cce5f209d4edaaa2e6d25b0c2c64de776c",
    },
    {
        "id": "independent_probe_word_replay",
        "script": "proof_compression_submission/probe/verify_probe_word_theorem.py",
        "payload_key": "payload_sha256",
        "payload": "1d4248028b38f6b731f066960d9e584240de68a17323539fe5b47f119a8086f6",
    },
    {
        "id": "minimal_compressed_release_verifier",
        "script": "proof_compression_submission/verify_compressed_release.py",
        "payload_key": "result_payload_sha256",
        "payload": "8a41ecd5d3ddca14210805cec6c33ce2c4ceb31d446e160d20893d4cd8d04c5a",
    },
)


class EquivalenceFailure(RuntimeError):
    pass


def need(condition: bool, code: str, detail: Any | None = None) -> None:
    if not condition:
        raise EquivalenceFailure(code if detail is None else f"{code}:{detail}")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def object_sha(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def seal(payload: dict[str, Any]) -> dict[str, Any]:
    need("payload_sha256" not in payload, "ALREADY_SEALED")
    return {**payload, "payload_sha256": object_sha(payload)}


def parse_last_json(stdout: str, command_id: str) -> dict[str, Any]:
    lines = [line for line in stdout.splitlines() if line.strip()]
    need(bool(lines), "EMPTY_STDOUT", command_id)
    try:
        value = json.loads(lines[-1])
    except json.JSONDecodeError as error:
        raise EquivalenceFailure(f"NON_JSON_STDOUT:{command_id}:{error}") from error
    need(isinstance(value, dict), "STDOUT_NOT_OBJECT", command_id)
    return value


def run_suite() -> tuple[dict[str, Any], float]:
    rows: list[dict[str, Any]] = []
    started = time.perf_counter()
    for spec in COMMANDS:
        command = [sys.executable, spec["script"], "--check"]
        completed = subprocess.run(
            command,
            cwd=PROJECT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        need(completed.returncode == 0, "COMMAND_FAILED", f"{spec['id']}:{completed.stderr[-1000:]}")
        report = parse_last_json(completed.stdout, spec["id"])
        need(report.get("status") == "PASS", "COMMAND_STATUS", spec["id"])
        need(report.get(spec["payload_key"]) == spec["payload"], "COMMAND_PAYLOAD", spec["id"])
        rows.append(
            {
                "command_id": spec["id"],
                "argv": [spec["script"], "--check"],
                "reported_payload_key": spec["payload_key"],
                "reported_payload_sha256": spec["payload"],
                "status": "PASS",
            }
        )
    elapsed = time.perf_counter() - started
    result = seal(
        {
            "schema": "k2p-pc-partial-old-new-equivalence-result-v1",
            "status": "PASS",
            "compression_status": "PC-PARTIAL",
            "frozen_theorem_outcome": "K2P-SAME",
            "unresolved_mathematical_records": 0,
            "commands": rows,
            "equivalence_claim": "The compressed censuses and family assignments equal the frozen exact ledgers under the corrected directed record convention; irreducible ledgers remain bound rather than discarded.",
            "nonclaim": "The 297 restoration archetypes are not asserted to be exact labelled transport quotients, and the probe ledgers are not replaced by the word induction.",
        }
    )
    return result, elapsed


def load_existing() -> dict[str, Any]:
    need(OUTPUT.is_file() and not OUTPUT.is_symlink(), "RESULT_MISSING")
    value = json.loads(OUTPUT.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "RESULT_NOT_OBJECT")
    observed = value.get("payload_sha256")
    payload = dict(value)
    payload.pop("payload_sha256", None)
    need(observed == object_sha(payload), "RESULT_SEAL")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    need(__debug__ and sys.flags.optimize == 0, "OPTIMIZED_PYTHON_FORBIDDEN")
    args = parse_args()
    result, elapsed = run_suite()
    if args.write:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(
            json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    else:
        need(load_existing() == result, "RESULT_REPLAY_MISMATCH")
    print(
        json.dumps(
            {
                "commands": len(COMMANDS),
                "payload_sha256": result["payload_sha256"],
                "runtime_seconds": round(elapsed, 3),
                "status": "PASS",
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EquivalenceFailure as error:
        print(json.dumps({"status": "FAIL", "error": str(error)}, sort_keys=True))
        raise SystemExit(1)
