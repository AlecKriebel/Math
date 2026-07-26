#!/usr/bin/env python3
"""External hostile audit of the exact C-057 acceptance wrapper.

The target wrapper and acceptance JSON are treated as immutable inputs.  This
audit binds their exact bytes, independently checks the complete acceptance
graph, runs a fresh full replay, directly exercises parser/path guards, and
tests private mutations.  It launches no SAT solver.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from types import ModuleType
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE_REL = "results/order13_k3_hole9_certificate_acceptance.json"
REPLAY_REL = "repro/c057/replay.py"
README_REL = "repro/c057/README.md"

TARGETS: Mapping[str, tuple[int, str, str]] = {
    ACCEPTANCE_REL: (
        8_249,
        "f9ee1ce8657206a23353f52cc64210fb015149f12fdb3f7eeeac11a6948c32b7",
        "sole C-057 promotion record",
    ),
    REPLAY_REL: (
        13_150,
        "83497204ee32158f123a873d2b682373c04d5dd63999fdcfcad2e85197301d88",
        "one-command C-057 replay",
    ),
    README_REL: (
        1_183,
        "abd3fcf4df966645d2c3c9585e6667e36307ed2a127376535f5e667ec83a74e4",
        "C-057 reproduction instructions",
    ),
}

EXPECTED_BOUND_PATHS = {
    "results/order12_frontier_acceptance.json",
    "math/lemmas/order13_k3_hole11_exclusion.md",
    "math/lemmas/order13_k3_synthesis_target.md",
    "math/lemmas/order13_k3_hole9_certificate_exclusion.md",
    "instances/order13_k3_hole9/instance.cnf",
    "instances/order13_k3_hole9/coloring-bank.json",
    "instances/order13_k3_hole9/constructor-manifest.json",
    "certificates/order13_k3_hole9_attempt000001_lrat/candidate-manifest.json",
    "certificates/order13_k3_hole9_attempt000001_lrat/README.md",
    "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf",
    "certificates/order13_k3_hole9_attempt000001_lrat/proof.normalized.bdrat",
    "certificates/order13_k3_hole9_attempt000001_lrat/proof.lrat",
    "src/verifier_b/order13_k3_hole9_certificate.py",
    "tests/test_order13_k3_hole9_certificate_verifier_b.py",
    "reviews/order13_k3_hole9_certificate_verifier_b/REVIEW.md",
    "reviews/order13_k3_hole9_certificate_verifier_b/evidence.json",
    "reviews/order13_k3_hole9_certificate_verifier_b/tool-source-provenance.json",
    "reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/REVIEW.md",
    "reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/evidence.json",
    "reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/replay.py",
    "reviews/order13_k3_hole9_math_coverage/REVIEW.md",
    "reviews/order13_k3_hole9_math_coverage/audit.py",
    "reviews/order13_k3_hole9_math_coverage/evidence.json",
    "results/order13_k3_hole9_production/attempts/attempt-000001/outcome.json",
    "results/order13_k3_hole9_attempt1_audit_v3.json",
}

EXPECTED_SCOPE_EXCLUSIONS = [
    "This does not exclude the order-13 parameter-three hole5 branch.",
    "This does not exclude the order-13 parameter-three hole7 branch.",
    "This is not a complete order-13 parameter-three exclusion.",
    "This says nothing decisive about the order-13 parameter-four or parameter-five slices.",
    "This does not exclude every order-13 counterexample or raise the global lower bound to 14.",
    "This is not a counterexample or a universal proof of the gamma-theta conjecture.",
    "No novelty or priority claim is made.",
]


class AuditError(RuntimeError):
    """The exact wrapper, a dependency, or a hostile test failed closed."""


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def strict_json(payload: bytes, label: str) -> Any:
    def reject_constant(token: str) -> Any:
        raise AuditError(f"nonfinite JSON token in {label}: {token}")

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise AuditError(f"duplicate JSON key in {label}: {key!r}")
            result[key] = value
        return result

    try:
        return json.loads(
            payload,
            object_pairs_hook=unique_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditError(f"malformed JSON in {label}: {exc}") from exc


def safe_relative(relative: str, root: Path = ROOT) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or not pure.parts or any(
        part in ("", ".", "..") for part in pure.parts
    ):
        raise AuditError(f"unsafe relative path: {relative!r}")
    current = root
    for part in pure.parts:
        current = current / part
        if current.is_symlink():
            raise AuditError(f"symlink component rejected: {relative}")
    return current


def read_regular(relative: str, root: Path = ROOT) -> bytes:
    path = safe_relative(relative, root)
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise AuditError(f"cannot open {relative}: {exc}") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise AuditError(f"not a regular file: {relative}")
        chunks: list[bytes] = []
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            chunks.append(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    before_identity = (
        before.st_dev,
        before.st_ino,
        before.st_size,
        before.st_mtime_ns,
    )
    after_identity = (
        after.st_dev,
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
    )
    if before_identity != after_identity:
        raise AuditError(f"file changed while read: {relative}")
    return b"".join(chunks)


def bind_targets() -> tuple[dict[str, bytes], list[dict[str, Any]]]:
    payloads: dict[str, bytes] = {}
    records: list[dict[str, Any]] = []
    for relative in sorted(TARGETS):
        expected_size, expected_hash, role = TARGETS[relative]
        payload = read_regular(relative)
        actual_hash = sha256(payload)
        require(
            len(payload) == expected_size and actual_hash == expected_hash,
            f"target binding mismatch: {relative}",
        )
        payloads[relative] = payload
        records.append(
            {
                "path": relative,
                "role": role,
                "sha256": actual_hash,
                "size_bytes": len(payload),
            }
        )
    return payloads, records


def collect_binding_records(
    value: Any,
    location: str = "$",
    result: list[tuple[str, dict[str, Any]]] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    if result is None:
        result = []
    if isinstance(value, dict):
        if (
            isinstance(value.get("path"), str)
            and "size_bytes" in value
            and isinstance(value.get("sha256"), str)
        ):
            result.append((location, value))
        for key, child in value.items():
            collect_binding_records(child, f"{location}.{key}", result)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            collect_binding_records(child, f"{location}[{index}]", result)
    return result


def check_recursive_bindings(
    acceptance: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, bytes]]:
    located = collect_binding_records(acceptance)
    require(len(located) == 25, f"expected 25 bindings, found {len(located)}")
    paths = [record["path"] for _, record in located]
    require(len(set(paths)) == 25, "recursive acceptance paths are not unique")
    require(set(paths) == EXPECTED_BOUND_PATHS, "recursive path universe mismatch")
    payloads: dict[str, bytes] = {}
    checked: list[dict[str, Any]] = []
    for location, record in located:
        size = record.get("size_bytes")
        digest = record.get("sha256")
        require(
            type(size) is int
            and size >= 0
            and isinstance(digest, str)
            and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            f"malformed binding at {location}",
        )
        relative = record["path"]
        payload = read_regular(relative)
        actual = sha256(payload)
        require(
            len(payload) == size and actual == digest,
            f"recursive binding mismatch at {location}: {relative}",
        )
        payloads[relative] = payload
        checked.append(
            {
                "location": location,
                "path": relative,
                "sha256": actual,
                "size_bytes": len(payload),
            }
        )
    return checked, payloads


def validate_acceptance_scope(record: dict[str, Any]) -> None:
    require(
        record.get("schema")
        == "gamma-theta-order13-k3-hole9-certificate-acceptance-v1",
        "wrong acceptance schema",
    )
    require(record.get("schema_version") == 1, "wrong schema version")
    require(record.get("claim_id") == "C-057", "wrong claim identifier")
    require(record.get("claim_status") == "CERTIFIED-FINITE", "wrong claim status")
    require(
        record.get("status") == "ACCEPTED_EXACT_HOLE9_TEMPLATE_EXCLUSION",
        "wrong acceptance status",
    )
    require(
        record.get("verdict")
        == "ACCEPT_CERTIFIED_FINITE_ORDER13_K3_HOLE9_TEMPLATE_EXCLUSION",
        "wrong acceptance verdict",
    )
    require(
        record.get("claim")
        == (
            "Relative to C-050 and the accepted inputs of C-055, no order-13 "
            "graph G with gamma(G) = gamma_infinity(G) = 3 < theta(G) has a "
            "complement containing a hub-free induced C9."
        ),
        "accepted claim text changed",
    )
    require(
        record.get("consequence")
        == (
            "Together with C-053, every remaining order-13 counterexample "
            "with common parameter 3 lies in the overlapping hub-free "
            "complement-C5 or complement-C7 template cover."
        ),
        "accepted consequence changed",
    )
    require(
        record.get("scope_exclusions") == EXPECTED_SCOPE_EXCLUSIONS,
        "scope exclusions changed or reordered",
    )
    require(
        record["relative_inputs"]["order12_frontier_acceptance"]["boundary"]
        == (
            "C-050 remains explicitly relative to the published "
            "MacGillivray-Mynhardt-Virgile through-order-11 computation."
        ),
        "C-050 published-premise boundary changed",
    )
    formula = record["exact_boolean_object"]["formula"]
    require(
        (
            formula["variables"],
            formula["clauses"],
            formula["literal_occurrences"],
            formula["sha256"],
        )
        == (
            9_802,
            32_108,
            281_028,
            "3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea",
        ),
        "exact Boolean object changed",
    )
    require(
        record["exact_boolean_object"]["coloring_bank"]["canonical_rows"] == 2_295,
        "coloring bank count changed",
    )
    rup = record["certificate"]["addition_only_binary_rup"]
    require(
        (
            rup["additions_total"],
            rup["nonempty_additions"],
            rup["empty_additions"],
            rup["deletions"],
            rup["post_empty_records"],
        )
        == (45_281, 45_280, 1, 0, 0),
        "binary proof census changed",
    )


def validate_nested_statuses(
    record: dict[str, Any], payloads: Mapping[str, bytes]
) -> dict[str, Any]:
    candidate = strict_json(
        payloads[
            "certificates/order13_k3_hole9_attempt000001_lrat/"
            "candidate-manifest.json"
        ],
        "candidate manifest",
    )
    require(
        candidate["certificate_status"]
        == "CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT",
        "candidate status was promoted in place",
    )
    require(
        record["certificate"]["immutable_candidate_manifest"]["frozen_status"]
        == candidate["certificate_status"],
        "candidate wrapper status disagrees",
    )
    outcome = strict_json(
        payloads[
            "results/order13_k3_hole9_production/attempts/"
            "attempt-000001/outcome.json"
        ],
        "original outcome",
    )
    require(
        outcome["status"] == "RETRYABLE_NONCLAIM"
        and outcome["claim_status"] == "NO_SAT_OR_UNSAT_CLAIM"
        and outcome["details"]["phase_status"] == "RAW_FORWARD_REJECTED_NONCLAIM",
        "original production nonclaim was rewritten",
    )
    original_audit = strict_json(
        payloads["results/order13_k3_hole9_attempt1_audit_v3.json"],
        "original attempt audit",
    )
    require(
        original_audit["status"] == "RETRYABLE_NONCLAIM"
        and original_audit["proof_freshly_replayed"] is False,
        "original audit boundary was rewritten",
    )
    verifier = strict_json(
        payloads[
            "reviews/order13_k3_hole9_certificate_verifier_b/evidence.json"
        ],
        "verifier evidence",
    )
    require(
        verifier["verdict"]
        == "VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_PENDING_HOSTILE_ACCEPTANCE"
        and verifier["hostile_mutations"]["count"] == 24
        and verifier["hostile_mutations"]["all_rejected"] is True,
        "verifier candidate-only verdict changed",
    )
    external = strict_json(
        payloads[
            "reviews/order13_k3_hole9_certificate_verifier_b/"
            "external_code_audit/evidence.json"
        ],
        "external code-audit evidence",
    )
    require(
        external["verdict"] == "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER"
        and external["no_soundness_blocker"] is True
        and external["provenance_repair"]["corrected_final_sha256"]
        == "95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275",
        "external code-audit verdict changed",
    )
    mathematics = strict_json(
        payloads["reviews/order13_k3_hole9_math_coverage/evidence.json"],
        "mathematical coverage evidence",
    )
    require(
        mathematics["verdict"]
        == "ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION"
        and mathematics["certificate_acceptance"]["formula_unsat"] is True
        and mathematics["mathematical_implication"][
            "remaining_live_formula_templates"
        ]
        == ["hole5", "hole7"],
        "mathematical coverage verdict changed",
    )
    frontier = strict_json(
        payloads["results/order12_frontier_acceptance.json"],
        "C-050 acceptance",
    )
    require(
        frontier["status"]
        == "ACCEPTED_WITH_EXPLICIT_PUBLISHED_THROUGH_ORDER_11_PREMISE",
        "C-050 boundary changed",
    )
    require(
        payloads["instances/order13_k3_hole9/instance.cnf"]
        == payloads[
            "certificates/order13_k3_hole9_attempt000001_lrat/instance.cnf"
        ],
        "constructor and certificate formulas differ",
    )
    return {
        "candidate_status": candidate["certificate_status"],
        "external_code_audit": external["verdict"],
        "mathematical_coverage": mathematics["verdict"],
        "original_attempt_audit_status": original_audit["status"],
        "original_outcome_claim_status": outcome["claim_status"],
        "original_outcome_status": outcome["status"],
        "verifier_verdict": verifier["verdict"],
    }


def inspect_subprocess_surface(replay_payload: bytes) -> dict[str, Any]:
    source = replay_payload.decode("utf-8")
    tree = ast.parse(source, filename=REPLAY_REL)
    subprocess_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess"
        and node.func.attr == "run"
    ]
    require(len(subprocess_calls) == 1, "unexpected subprocess.run call count")
    call = subprocess_calls[0]
    require(
        all(keyword.arg != "shell" for keyword in call.keywords),
        "target wrapper sets a shell option",
    )
    require("shell=True" not in source, "shell execution found")
    require(source.count("run_json_process(") == 4, "wrong child-call census")
    expected_commands = (
        '[sys.executable, "-B", "-W", "error", str(verifier)]',
        '[sys.executable, "-B", "-W", "error", str(external_replay)]',
        '[sys.executable, "-B", "-W", "error", str(math_replay)]',
    )
    for command in expected_commands:
        require(command in source, f"missing exact child command {command}")
    require("stdin=subprocess.DEVNULL" in source, "child stdin is not closed")
    require("timeout=180" in source, "verifier timeout missing")
    require("timeout=240" in source, "external-audit timeout missing")
    require("timeout=120" in source, "mathematical-audit timeout missing")
    return {
        "direct_children": [
            "exact verifier-B Python source",
            "exact external code-audit replay",
            "exact mathematical coverage audit",
        ],
        "direct_subprocess_run_sites": 1,
        "shell_used": False,
        "stdin_closed": True,
        "timeouts_seconds": [180, 240, 120],
        "transitive_non_python_children": [
            "/usr/bin/cc",
            "private SHA-bound drat-trim",
            "private SHA-bound lrat-check",
        ],
        "sat_solver_in_call_graph": False,
    }


def import_exact_wrapper(replay_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "c057_wrapper_under_hostile_audit", replay_path
    )
    require(spec is not None and spec.loader is not None, "cannot load wrapper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def direct_guard_tests(module: ModuleType) -> dict[str, bool]:
    results: dict[str, bool] = {}
    probes = {
        "duplicate_json": b'{"a":1,"a":2}',
        "nonfinite_json": b'{"a":NaN}',
    }
    for name, payload in probes.items():
        try:
            module.load_json_bytes(payload, name)
        except module.ReplayError:
            results[name] = True
        else:
            raise AuditError(f"target wrapper accepted {name}")
    for name, relative in {
        "absolute_path": "/tmp/x",
        "parent_path": "../x",
        "embedded_parent_path": "a/../x",
        "empty_path": "",
    }.items():
        try:
            module.safe_repository_path(relative)
        except module.ReplayError:
            results[name] = True
        else:
            raise AuditError(f"target wrapper accepted {name}")
    with tempfile.TemporaryDirectory(prefix="c057-direct-guard-") as temporary:
        temporary_path = Path(temporary)
        real = temporary_path / "real"
        real.write_bytes(b"x")
        link = temporary_path / "link"
        link.symlink_to(real)
        old_campaign = module.CAMPAIGN
        module.CAMPAIGN = temporary_path
        try:
            try:
                module.safe_repository_path("link")
            except module.ReplayError:
                results["final_symlink"] = True
            else:
                raise AuditError("target wrapper accepted a final symlink")
        finally:
            module.CAMPAIGN = old_campaign
    try:
        module.check_binding(
            {"path": README_REL, "size_bytes": True, "sha256": "0" * 64},
            "$.probe",
        )
    except module.ReplayError:
        results["boolean_size"] = True
    else:
        raise AuditError("target wrapper accepted a Boolean size")
    return results


def run_process(
    command: list[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    timeout: int,
) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            env=dict(environment),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise AuditError(f"process timed out: {command[-1]}") from exc


def clean_environment(temporary: str) -> dict[str, str]:
    return {
        "HOME": temporary,
        "LC_ALL": "C",
        "PATH": "/usr/bin:/bin:/opt/homebrew/bin",
        "TMPDIR": temporary,
    }


def full_replay() -> dict[str, Any]:
    expected_fields = {
        "acceptance_sha256": TARGETS[ACCEPTANCE_REL][1],
        "bound_artifacts_checked": 25,
        "candidate_status_preserved": "CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT",
        "claim_id": "C-057",
        "external_code_audit_verdict": "ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER",
        "hostile_mutations_rejected": 24,
        "mathematical_coverage_verdict": (
            "ACCEPT_EXACT_HOLE9_TEMPLATE_EXCLUSION_AND_C5_C7_REDUCTION"
        ),
        "original_production_status_preserved": "RETRYABLE_NONCLAIM",
        "remaining_live_parameter3_templates": ["hole5", "hole7"],
        "sat_solver_invoked": False,
        "schema": "gamma-theta-c057-replay-v1",
        "schema_version": 1,
        "verdict": "VERIFIED_C057_HOLE9_TEMPLATE_EXCLUSION_BINDINGS_AND_PROOFS",
    }
    outputs: list[dict[str, Any]] = []
    commands = [
        [
            sys.executable,
            "-B",
            "-W",
            "error",
            str(ROOT / REPLAY_REL),
        ],
        [
            sys.executable,
            "-I",
            "-B",
            "-W",
            "error",
            str(ROOT / REPLAY_REL),
        ],
    ]
    for index, command in enumerate(commands):
        with tempfile.TemporaryDirectory(
            prefix=f"c057-full-replay-{index}-"
        ) as temporary:
            process = run_process(
                command,
                cwd=ROOT,
                environment=clean_environment(temporary),
                timeout=300,
            )
        require(process.returncode == 0, f"fresh full replay {index} failed")
        require(process.stderr == b"", f"fresh full replay {index} wrote stderr")
        output = strict_json(process.stdout, f"fresh full replay {index}")
        require(isinstance(output, dict), "fresh replay output is not an object")
        require(
            output == expected_fields,
            f"fresh replay {index} output differs from exact result",
        )
        outputs.append(output)
    require(outputs[0] == outputs[1], "documented and isolated replays differ")
    return {
        "documented_command_passed": True,
        "documented_command_result": outputs[0],
        "isolated_command_passed": True,
        "isolated_command_result_byte_identical": True,
    }


def populate_private_campaign(
    private: Path,
    acceptance_payload: bytes,
    replay_payload: bytes,
    bound_payloads: Mapping[str, bytes],
) -> None:
    for relative, payload in {
        ACCEPTANCE_REL: acceptance_payload,
        REPLAY_REL: replay_payload,
        **bound_payloads,
    }.items():
        path = private / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def rejected_process(
    private: Path, *, expected_fragment: str | None = None
) -> str:
    with tempfile.TemporaryDirectory(prefix="c057-mutation-env-") as environment_dir:
        process = run_process(
            [
                sys.executable,
                "-I",
                "-B",
                "-W",
                "error",
                str(private / REPLAY_REL),
            ],
            cwd=private,
            environment=clean_environment(environment_dir),
            timeout=30,
        )
    require(process.returncode != 0, "mutated wrapper unexpectedly exited zero")
    require(
        b"VERIFIED_C057_HOLE9_TEMPLATE_EXCLUSION_BINDINGS_AND_PROOFS"
        not in process.stdout,
        "mutated wrapper emitted the success verdict",
    )
    stderr = process.stderr.decode("utf-8", "replace")
    require("REJECT:" in stderr, "mutated wrapper lacked fail-closed marker")
    if expected_fragment is not None:
        require(expected_fragment in stderr, f"missing rejection {expected_fragment!r}")
    return stderr.splitlines()[-1]


def mutate_json(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
        )
        + "\n"
    ).encode("ascii")


def mutation_suite(
    acceptance_payload: bytes,
    replay_payload: bytes,
    bound_payloads: Mapping[str, bytes],
) -> list[dict[str, Any]]:
    acceptance = strict_json(acceptance_payload, "mutation baseline acceptance")
    require(isinstance(acceptance, dict), "mutation acceptance is not an object")
    results: list[dict[str, Any]] = []

    def run_case(
        name: str,
        *,
        acceptance_bytes: bytes = acceptance_payload,
        mutations: Mapping[str, bytes | tuple[str, str]] | None = None,
        expected: str | None = None,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix=f"c057-mutation-{name}-") as temporary:
            private = Path(temporary)
            populate_private_campaign(
                private, acceptance_bytes, replay_payload, bound_payloads
            )
            for relative, mutation in (mutations or {}).items():
                path = private / relative
                if isinstance(mutation, tuple) and mutation[0] == "symlink":
                    path.unlink()
                    path.symlink_to(mutation[1])
                else:
                    require(isinstance(mutation, bytes), "bad mutation fixture")
                    path.write_bytes(mutation)
            reason = rejected_process(private, expected_fragment=expected)
            results.append({"name": name, "reason": reason, "rejected": True})

    flipped_acceptance = bytearray(acceptance_payload)
    flipped_acceptance[len(flipped_acceptance) // 2] ^= 1
    run_case(
        "acceptance_bit_flip",
        acceptance_bytes=bytes(flipped_acceptance),
        expected="acceptance record exact-byte binding mismatch",
    )
    overclaim = json.loads(acceptance_payload)
    overclaim["claim"] = "The universal gamma-theta conjecture is resolved."
    run_case(
        "acceptance_scope_overclaim",
        acceptance_bytes=mutate_json(overclaim),
        expected="acceptance record exact-byte binding mismatch",
    )
    duplicate = acceptance_payload.replace(
        b'  "schema_version": 1,',
        b'  "schema_version": 1,\\n  "schema_version": 1,',
        1,
    )
    run_case(
        "acceptance_duplicate_json_key",
        acceptance_bytes=duplicate,
        expected="acceptance record exact-byte binding mismatch",
    )
    nonfinite = acceptance_payload.replace(b'"campaign_day": 2', b'"campaign_day": NaN')
    run_case(
        "acceptance_nonfinite_json",
        acceptance_bytes=nonfinite,
        expected="acceptance record exact-byte binding mismatch",
    )

    formula_path = "instances/order13_k3_hole9/instance.cnf"
    formula_flip = bytearray(bound_payloads[formula_path])
    formula_flip[-2] ^= 1
    run_case(
        "bound_formula_bit_flip",
        mutations={formula_path: bytes(formula_flip)},
        expected="binding mismatch",
    )
    math_path = "reviews/order13_k3_hole9_math_coverage/evidence.json"
    math_flip = bytearray(bound_payloads[math_path])
    math_flip[len(math_flip) // 2] ^= 1
    run_case(
        "bound_math_evidence_bit_flip",
        mutations={math_path: bytes(math_flip)},
        expected="binding mismatch",
    )
    candidate_path = (
        "certificates/order13_k3_hole9_attempt000001_lrat/"
        "candidate-manifest.json"
    )
    candidate_mutated = bound_payloads[candidate_path].replace(
        b"CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT",
        b"ACCEPTED_PENDING_INDEPENDENT_HOSTILE_AUDIT_",
        1,
    )
    run_case(
        "candidate_status_rewrite",
        mutations={candidate_path: candidate_mutated},
        expected="binding mismatch",
    )
    outcome_path = (
        "results/order13_k3_hole9_production/attempts/"
        "attempt-000001/outcome.json"
    )
    outcome_mutated = bound_payloads[outcome_path].replace(
        b"RETRYABLE_NONCLAIM", b"ACCEPTED_UNSAT_CLAIM", 1
    )
    run_case(
        "production_nonclaim_rewrite",
        mutations={outcome_path: outcome_mutated},
        expected="binding mismatch",
    )
    external_path = (
        "reviews/order13_k3_hole9_certificate_verifier_b/"
        "external_code_audit/evidence.json"
    )
    external_mutated = bound_payloads[external_path].replace(
        b'"no_soundness_blocker": true',
        b'"no_soundness_blocker":false',
        1,
    )
    run_case(
        "external_verdict_rewrite",
        mutations={external_path: external_mutated},
        expected="binding mismatch",
    )
    run_case(
        "bound_formula_symlink",
        mutations={formula_path: ("symlink", str(ROOT / formula_path))},
        expected="symlink rejected",
    )

    coordinated_acceptance = json.loads(acceptance_payload)
    coordinated_acceptance["exact_boolean_object"]["formula"]["sha256"] = sha256(
        bytes(formula_flip)
    )
    run_case(
        "coordinated_formula_and_acceptance_mutation",
        acceptance_bytes=mutate_json(coordinated_acceptance),
        mutations={formula_path: bytes(formula_flip)},
        expected="acceptance record exact-byte binding mismatch",
    )

    with tempfile.TemporaryDirectory(prefix="c057-acceptance-symlink-") as temporary:
        private = Path(temporary)
        populate_private_campaign(
            private, acceptance_payload, replay_payload, bound_payloads
        )
        target = private / "acceptance-target.json"
        target.write_bytes(acceptance_payload)
        acceptance_path = private / ACCEPTANCE_REL
        acceptance_path.unlink()
        acceptance_path.symlink_to(target)
        reason = rejected_process(
            private, expected_fragment="acceptance record exact-byte binding mismatch"
        )
        results.append(
            {"name": "acceptance_final_symlink", "reason": reason, "rejected": True}
        )

    replay_mutated = replay_payload.replace(
        b"accepted claim C-057", b"accepted claim X-057", 1
    )
    require(replay_mutated != replay_payload, "wrapper mutation fixture failed")
    require(
        len(replay_mutated) == len(replay_payload)
        and sha256(replay_mutated) != TARGETS[REPLAY_REL][1],
        "wrapper mutation did not change the trust root",
    )
    results.append(
        {
            "name": "coordinated_wrapper_and_acceptance_attack",
            "reason": (
                "rejected by this external audit's exact replay.py SHA-256 "
                "binding; the target cannot authenticate altered code after "
                "that code has already been loaded"
            ),
            "rejected": True,
        }
    )
    require(len(results) == 13, f"wrong mutation count: {len(results)}")
    return results


def main() -> None:
    target_payloads, target_records = bind_targets()
    acceptance = strict_json(target_payloads[ACCEPTANCE_REL], ACCEPTANCE_REL)
    require(isinstance(acceptance, dict), "acceptance is not an object")
    validate_acceptance_scope(acceptance)
    checked_bindings, bound_payloads = check_recursive_bindings(acceptance)
    statuses = validate_nested_statuses(acceptance, bound_payloads)
    subprocess_surface = inspect_subprocess_surface(target_payloads[REPLAY_REL])
    wrapper_module = import_exact_wrapper(ROOT / REPLAY_REL)
    guard_tests = direct_guard_tests(wrapper_module)
    replay_result = full_replay()
    mutations = mutation_suite(
        target_payloads[ACCEPTANCE_REL],
        target_payloads[REPLAY_REL],
        bound_payloads,
    )
    for relative, payload in target_payloads.items():
        expected_size, expected_hash, _ = TARGETS[relative]
        current = read_regular(relative)
        require(
            current == payload
            and len(current) == expected_size
            and sha256(current) == expected_hash,
            f"target changed during audit: {relative}",
        )
    output = {
        "schema": "gamma-theta-c057-acceptance-wrapper-hostile-audit-v1",
        "schema_version": 1,
        "verdict": "ACCEPT_EXACT_C057_ACCEPTANCE_WRAPPER",
        "target_bindings": target_records,
        "acceptance": {
            "claim_id": acceptance["claim_id"],
            "claim_status": acceptance["claim_status"],
            "exact_byte_trust_root": True,
            "promotion_record_is_separate_from_candidate": True,
            "recursive_artifact_bindings": len(checked_bindings),
            "recursive_paths_unique": True,
            "scope_exclusions_exact": True,
            "sha256": TARGETS[ACCEPTANCE_REL][1],
            "status": acceptance["status"],
            "verdict": acceptance["verdict"],
        },
        "nested_boundaries": statuses,
        "subprocess_surface": subprocess_surface,
        "fresh_full_replay": replay_result,
        "direct_guard_tests": guard_tests,
        "hostile_mutations": {
            "all_rejected": all(item["rejected"] for item in mutations),
            "count": len(mutations),
            "tests": mutations,
        },
        "coordinated_mutation_boundary": {
            "acceptance_plus_bound_artifact": (
                "rejected by immutable acceptance SHA-256 in exact wrapper"
            ),
            "acceptance_plus_wrapper": (
                "rejected by this external audit's exact target bindings; "
                "no running program can authenticate maliciously replaced "
                "code solely by that code's own constants"
            ),
            "false_acceptance_found_in_exact_bytes": False,
        },
        "no_sat_solver": {
            "fresh_replay_invoked_sat_solver": False,
            "static_exact_call_graph_audited": True,
            "transitive_children": subprocess_surface[
                "transitive_non_python_children"
            ],
        },
        "caveats": [
            {
                "blocking": False,
                "id": "loaded-code-self-authentication",
                "statement": (
                    "The wrapper cannot authenticate a malicious replacement "
                    "of its own already-loaded bytes. This external review "
                    "supplies the exact replay.py and acceptance-record trust "
                    "root."
                ),
            },
            {
                "blocking": False,
                "id": "static-symlink-toctou",
                "statement": (
                    "The target rejects static symlink components but uses "
                    "Path checks followed by read_bytes rather than descriptor-"
                    "stable O_NOFOLLOW reads. A concurrent local filesystem "
                    "attacker is outside the campaign replay threat model; "
                    "this audit uses descriptor-stable reads."
                ),
            },
            {
                "blocking": False,
                "id": "environment-isolation",
                "statement": (
                    "The README command and target child commands omit Python "
                    "-I and inherit the caller environment. The accepted fresh "
                    "replay passed both the documented invocation and an "
                    "isolated-mode invocation under a minimal environment. "
                    "Adding isolated-mode child launches would improve "
                    "defense in depth."
                ),
            },
        ],
        "scope_exclusions": EXPECTED_SCOPE_EXCLUSIONS,
    }
    print(
        json.dumps(
            output,
            allow_nan=False,
            ensure_ascii=True,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
