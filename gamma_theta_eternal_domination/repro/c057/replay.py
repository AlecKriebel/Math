#!/usr/bin/env python3
"""Fail-closed replay for accepted claim C-057.

The replay binds the exact acceptance record and every artifact it names,
checks the deliberately preserved candidate/nonclaim boundaries, reproduces
the independent certificate verifier, and reproduces both hostile audits.
It invokes no SAT solver.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
from typing import Any


CAMPAIGN = Path(__file__).resolve().parents[2]
ACCEPTANCE = (
    CAMPAIGN / "results/order13_k3_hole9_certificate_acceptance.json"
)

EXPECTED_ACCEPTANCE_SIZE = 8_249
EXPECTED_ACCEPTANCE_SHA256 = (
    "f9ee1ce8657206a23353f52cc64210fb015149f12fdb3f7eeeac11a6948c32b7"
)
EXPECTED_SCHEMA = "gamma-theta-order13-k3-hole9-certificate-acceptance-v1"
EXPECTED_STATUS = "ACCEPTED_EXACT_HOLE9_TEMPLATE_EXCLUSION"
EXPECTED_VERDICT = (
    "ACCEPT_CERTIFIED_FINITE_ORDER13_K3_HOLE9_TEMPLATE_EXCLUSION"
)
EXPECTED_CLAIM_ID = "C-057"


class ReplayError(RuntimeError):
    """A binding, subprocess, or claim-boundary check failed."""


def reject_constant(value: str) -> None:
    raise ReplayError(f"non-finite JSON constant rejected: {value}")


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReplayError(f"duplicate JSON key rejected: {key!r}")
        result[key] = value
    return result


def load_json_bytes(payload: bytes, label: str) -> Any:
    try:
        return json.loads(
            payload,
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReplayError(f"cannot parse strict JSON for {label}: {error}") from error


def load_json(path: Path) -> Any:
    try:
        return load_json_bytes(path.read_bytes(), str(path))
    except OSError as error:
        raise ReplayError(f"cannot read {path}: {error}") from error


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def safe_repository_path(relative: str) -> Path:
    pure = PurePosixPath(relative)
    if (
        pure.is_absolute()
        or not pure.parts
        or any(part in ("", ".", "..") for part in pure.parts)
    ):
        raise ReplayError(f"unsafe repository-relative path: {relative!r}")
    path = CAMPAIGN.joinpath(*pure.parts)
    current = CAMPAIGN
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise ReplayError(f"symlink rejected in bound path: {relative}")
    if not path.is_file() or path.is_symlink():
        raise ReplayError(f"not a nonsymlink regular file: {relative}")
    return path


def check_binding(record: dict[str, Any], location: str) -> dict[str, Any]:
    relative = record.get("path")
    expected_size = record.get("size_bytes")
    expected_sha = record.get("sha256")
    if (
        not isinstance(relative, str)
        or not isinstance(expected_size, int)
        or isinstance(expected_size, bool)
        or expected_size < 0
        or not isinstance(expected_sha, str)
        or len(expected_sha) != 64
    ):
        raise ReplayError(f"malformed artifact binding at {location}")
    path = safe_repository_path(relative)
    payload = path.read_bytes()
    actual_sha = sha256_bytes(payload)
    if len(payload) != expected_size or actual_sha != expected_sha:
        raise ReplayError(
            f"binding mismatch at {location}: {relative}, "
            f"size={len(payload)}, sha256={actual_sha}"
        )
    return {
        "path": relative,
        "size_bytes": len(payload),
        "sha256": actual_sha,
    }


def walk_bindings(
    value: Any,
    location: str = "$",
    checked: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    if checked is None:
        checked = []
    if isinstance(value, dict):
        if (
            isinstance(value.get("path"), str)
            and "size_bytes" in value
            and isinstance(value.get("sha256"), str)
        ):
            checked.append(check_binding(value, location))
        for key, child in value.items():
            walk_bindings(child, f"{location}.{key}", checked)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            walk_bindings(child, f"{location}[{index}]", checked)
    return checked


def require_acceptance(record: dict[str, Any]) -> None:
    if record.get("schema") != EXPECTED_SCHEMA:
        raise ReplayError("unexpected acceptance schema")
    if record.get("schema_version") != 1:
        raise ReplayError("unexpected acceptance schema version")
    if record.get("claim_id") != EXPECTED_CLAIM_ID:
        raise ReplayError("unexpected claim ID")
    if record.get("claim_status") != "CERTIFIED-FINITE":
        raise ReplayError("claim status is not CERTIFIED-FINITE")
    if record.get("status") != EXPECTED_STATUS:
        raise ReplayError("acceptance status mismatch")
    if record.get("verdict") != EXPECTED_VERDICT:
        raise ReplayError("acceptance verdict mismatch")
    consequence = record.get("consequence")
    if (
        not isinstance(consequence, str)
        or "complement-C5 or complement-C7" not in consequence
    ):
        raise ReplayError("accepted C5/C7 consequence is missing")
    exclusions = record.get("scope_exclusions")
    required = {
        "This is not a complete order-13 parameter-three exclusion.",
        "This does not exclude every order-13 counterexample or raise the global lower bound to 14.",
        "This is not a counterexample or a universal proof of the gamma-theta conjecture.",
    }
    if not isinstance(exclusions, list) or not required.issubset(set(exclusions)):
        raise ReplayError("required scope exclusions are missing")


def require_nested_boundaries(record: dict[str, Any]) -> dict[str, Any]:
    candidate_record = record["certificate"]["immutable_candidate_manifest"]
    candidate = load_json(safe_repository_path(candidate_record["path"]))
    if (
        candidate.get("certificate_status")
        != "CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT"
        or candidate_record.get("frozen_status")
        != "CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT"
    ):
        raise ReplayError("immutable candidate status was rewritten")

    outcome_record = record["production_history_boundary"]["original_outcome"]
    outcome = load_json(safe_repository_path(outcome_record["path"]))
    if (
        outcome.get("status") != "RETRYABLE_NONCLAIM"
        or outcome.get("claim_status") != "NO_SAT_OR_UNSAT_CLAIM"
        or outcome.get("details", {}).get("phase_status")
        != "RAW_FORWARD_REJECTED_NONCLAIM"
        or outcome_record.get("status") != "RETRYABLE_NONCLAIM"
        or outcome_record.get("phase_status")
        != "RAW_FORWARD_REJECTED_NONCLAIM"
    ):
        raise ReplayError("original production outcome is not the frozen nonclaim")

    code_evidence_path = record["external_exact_byte_code_audit"]["evidence"][
        "path"
    ]
    code_evidence = load_json(safe_repository_path(code_evidence_path))
    if (
        code_evidence.get("verdict")
        != "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER"
        or code_evidence.get("no_soundness_blocker") is not True
        or code_evidence.get("provenance_repair", {}).get(
            "corrected_final_sha256"
        )
        != "95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275"
    ):
        raise ReplayError("external exact-byte code audit is not accepted")

    math_evidence_path = record["hostile_mathematical_coverage_audit"][
        "evidence"
    ]["path"]
    math_evidence = load_json(safe_repository_path(math_evidence_path))
    if (
        math_evidence.get("verdict")
        != "ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION"
        or math_evidence.get("certificate_acceptance", {}).get(
            "formula_unsat"
        )
        is not True
        or math_evidence.get("mathematical_implication", {}).get(
            "remaining_live_formula_templates"
        )
        != ["hole5", "hole7"]
    ):
        raise ReplayError("hostile mathematical coverage audit is not accepted")

    return {
        "candidate_status_preserved": candidate["certificate_status"],
        "original_production_status_preserved": outcome["status"],
        "external_code_audit_verdict": code_evidence["verdict"],
        "mathematical_coverage_verdict": math_evidence["verdict"],
    }


def run_json_process(
    command: list[str],
    *,
    timeout: int,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=CAMPAIGN,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as error:
        raise ReplayError(f"replay timed out: {command[-1]}") from error
    if completed.returncode != 0:
        raise ReplayError(
            f"replay failed ({completed.returncode}): {command[-1]}\n"
            + completed.stderr.decode("utf-8", "replace")
        )
    if completed.stderr:
        raise ReplayError(
            f"replay wrote stderr: {command[-1]}\n"
            + completed.stderr.decode("utf-8", "replace")
        )
    output = load_json_bytes(completed.stdout, command[-1])
    if not isinstance(output, dict):
        raise ReplayError(f"replay output is not an object: {command[-1]}")
    return output


def main() -> int:
    if (
        not ACCEPTANCE.is_file()
        or ACCEPTANCE.is_symlink()
        or ACCEPTANCE.stat().st_size != EXPECTED_ACCEPTANCE_SIZE
        or sha256_bytes(ACCEPTANCE.read_bytes()) != EXPECTED_ACCEPTANCE_SHA256
    ):
        raise ReplayError("acceptance record exact-byte binding mismatch")

    record = load_json(ACCEPTANCE)
    if not isinstance(record, dict):
        raise ReplayError("acceptance record is not a JSON object")
    require_acceptance(record)
    checked = walk_bindings(record)
    boundaries = require_nested_boundaries(record)

    verifier = safe_repository_path(
        record["independent_certificate_verifier"]["source"]["path"]
    )
    verifier_output = run_json_process(
        [sys.executable, "-B", "-W", "error", str(verifier)],
        timeout=180,
    )
    if (
        verifier_output.get("verdict")
        != "VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_PENDING_HOSTILE_ACCEPTANCE"
        or verifier_output.get("hostile_mutations", {}).get("count") != 24
    ):
        raise ReplayError("independent certificate verifier returned wrong scope")

    external_replay = safe_repository_path(
        record["external_exact_byte_code_audit"]["replay"]["path"]
    )
    external_output = run_json_process(
        [sys.executable, "-B", "-W", "error", str(external_replay)],
        timeout=240,
    )
    if (
        external_output.get("verdict")
        != "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER"
        or external_output.get("hostile_mutations_rejected") != 24
        or external_output.get("candidate_only") is not True
    ):
        raise ReplayError("external code replay returned wrong scope")

    math_replay = safe_repository_path(
        record["hostile_mathematical_coverage_audit"]["audit"]["path"]
    )
    math_output = run_json_process(
        [sys.executable, "-B", "-W", "error", str(math_replay)],
        timeout=120,
    )
    if (
        math_output.get("verdict")
        != "ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION"
        or math_output.get("mathematical_implication", {}).get(
            "remaining_live_formula_templates"
        )
        != ["hole5", "hole7"]
    ):
        raise ReplayError("mathematical coverage replay returned wrong scope")

    result = {
        "acceptance_sha256": EXPECTED_ACCEPTANCE_SHA256,
        "bound_artifacts_checked": len(checked),
        "candidate_status_preserved": boundaries[
            "candidate_status_preserved"
        ],
        "claim_id": EXPECTED_CLAIM_ID,
        "external_code_audit_verdict": external_output["verdict"],
        "hostile_mutations_rejected": 24,
        "mathematical_coverage_verdict": math_output["verdict"],
        "original_production_status_preserved": boundaries[
            "original_production_status_preserved"
        ],
        "remaining_live_parameter3_templates": ["hole5", "hole7"],
        "sat_solver_invoked": False,
        "schema": "gamma-theta-c057-replay-v1",
        "schema_version": 1,
        "verdict": "VERIFIED_C057_HOLE9_TEMPLATE_EXCLUSION_BINDINGS_AND_PROOFS",
    }
    print(
        json.dumps(
            result,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReplayError as error:
        print(f"REJECT: {error}", file=sys.stderr)
        raise SystemExit(1)
