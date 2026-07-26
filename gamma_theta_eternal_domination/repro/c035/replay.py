#!/usr/bin/env python3
"""Fail-closed metadata audit and full proof replay for campaign claim C-035.

This module is intentionally standard-library only.  It does not import the
search, synthesis, eternal-domination, or graph-evaluation implementations.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Mapping, Sequence


SCHEMA = "gamma-theta-c035-one-command-replay-v1"
LOCK_SCHEMA = "gamma-theta-c035-replay-lock-v1"
LOCK_SHA256 = "10b52635d90396135b7a529b3d4bca3987cf53d3693790ace07d679d604ae81d"
ACCEPTED_COMMIT = "36d8191ac72c4c04291184f2a6854fa76e181712"
CAMPAIGN_REPOSITORY_PATH = "gamma_theta_eternal_domination"
EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()

CLAIM = (
    "No finite simple graph G on 12 vertices satisfies "
    "gamma(G) = gamma_infinity(G) = 3 < theta(G)."
)
SCOPE_EXCLUSIONS = [
    "This does not exclude order-12 counterexamples with common parameter k at least 4.",
    "This does not exclude counterexamples of order at least 13.",
    "This does not resolve the universal gamma-theta conjecture.",
]

C5_CNF_SHA256 = (
    "c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104"
)
C5_PROOF_SHA256 = (
    "c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3"
)
C5_RAW_PROOF_SHA256 = (
    "c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4"
)
C5_CERTIFICATE_SHA256 = (
    "f54d7bf8a50f24e3a5084442d84f07548a60401faca8ec18bfd07f24f0e337e8"
)
C5_OUTCOME_SHA256 = (
    "ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4"
)
C5_POSTRUN_LOG_SHA256 = (
    "bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5"
)
C5_PACKAGE_LOG_SHA256 = (
    "470f58bf532ae8ff68ac3b8f096ba20166e6bcd91bee4924c1f924e276fea2cb"
)
C5_ACTIVATING_VERDICT = "ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033"

C7_CNF_SHA256 = (
    "6a011e685e58ef517f2ab8253ca40987bd7b742a470bedbacdc3a5e94fc995a7"
)
C7_PROOF_SHA256 = (
    "e8052df40d3e0c39b945a8735889039daba55eacc351e1822828b3d94f7baae9"
)
C7_CERTIFICATE_SHA256 = (
    "c38002e16190065ed13453f9013a294f013846b5ed3651fde64aaa927e2f888e"
)

C9_CNF_SHA256 = (
    "2845f242a094484a8d114e70ca1a8678dfcff79fadd56bd57813e25c2e49523d"
)
C9_PROOF_SHA256 = (
    "24c5647d3a57f2de221fba96747c618575a3aba086c5e4bca17aade55ce7d4ab"
)
C9_ACCEPTANCE_SHA256 = (
    "ebede11b90e6e0b73d75f57c7706ba2e62e699281fcd8c15a208886dd53db291"
)
C9_OUTER_CERTIFICATE_SHA256 = (
    "1a2d4f7fd3efe0138bb7a7a7f0975d3c60a7ed4d6f994157c5383f18e4b5806c"
)

CHECKER_SHA256 = (
    "31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb"
)

MANIFEST_HEADER = [
    "artifact_id",
    "path",
    "sha256",
    "created_at",
    "producer",
    "command",
    "seed",
    "wall_seconds",
    "cpu_seconds",
    "peak_memory_bytes",
    "outcome",
    "verification",
]


class ReplayFailure(RuntimeError):
    """A fail-closed replay rejection."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReplayFailure(message)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def _reject_json_constant(value: str) -> None:
    raise ReplayFailure(f"non-finite JSON constant: {value}")


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_bytes(payload: bytes, label: str) -> object:
    require(not payload.startswith(b"\xef\xbb\xbf"), f"{label}: UTF-8 BOM")
    try:
        text = payload.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise ReplayFailure(f"{label}: invalid UTF-8: {error}") from error
    try:
        return json.loads(
            text,
            object_pairs_hook=_unique_json_object,
            parse_constant=_reject_json_constant,
        )
    except ReplayFailure:
        raise
    except (json.JSONDecodeError, TypeError, ValueError) as error:
        raise ReplayFailure(f"{label}: invalid JSON: {error}") from error


def _safe_relative_path(raw: object, label: str) -> str:
    require(type(raw) is str and raw != "", f"{label}: path is not a string")
    path = PurePosixPath(raw)
    require(
        not path.is_absolute()
        and raw == path.as_posix()
        and all(part not in ("", ".", "..") for part in path.parts),
        f"{label}: unsafe relative path {raw!r}",
    )
    return raw


def _assert_no_symlink_components(root: Path, relative: str) -> Path:
    safe = _safe_relative_path(relative, "artifact")
    current = root
    for index, part in enumerate(PurePosixPath(safe).parts):
        current = current / part
        try:
            info = os.lstat(current)
        except FileNotFoundError as error:
            raise ReplayFailure(f"missing artifact: {safe}") from error
        require(not stat.S_ISLNK(info.st_mode), f"symlink artifact path: {safe}")
        if index + 1 < len(PurePosixPath(safe).parts):
            require(stat.S_ISDIR(info.st_mode), f"non-directory parent: {safe}")
    return current


@dataclass(frozen=True)
class FileSnapshot:
    path: str
    size: int
    sha256: str
    device: int
    inode: int
    mtime_ns: int
    ctime_ns: int

    def public(self) -> dict[str, object]:
        return {
            "path": self.path,
            "size": self.size,
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class ExpectedFile:
    path: str
    size: int
    sha256: str
    git_anchor: bool = True


def snapshot_file(root: Path, relative: str) -> FileSnapshot:
    path = _assert_no_symlink_components(root, relative)
    flags = os.O_RDONLY
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise ReplayFailure(f"cannot securely open {relative}: {error}") from error
    digest = hashlib.sha256()
    try:
        before = os.fstat(descriptor)
        require(
            stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
            f"artifact is not a single-link regular file: {relative}",
        )
        while True:
            block = os.read(descriptor, 1 << 20)
            if not block:
                break
            digest.update(block)
        after = os.fstat(descriptor)
    finally:
        os.close(descriptor)
    stable_fields = (
        "st_dev",
        "st_ino",
        "st_size",
        "st_mtime_ns",
        "st_ctime_ns",
        "st_nlink",
        "st_mode",
    )
    require(
        all(getattr(before, field) == getattr(after, field) for field in stable_fields),
        f"artifact changed while hashing: {relative}",
    )
    return FileSnapshot(
        path=relative,
        size=before.st_size,
        sha256=digest.hexdigest(),
        device=before.st_dev,
        inode=before.st_ino,
        mtime_ns=before.st_mtime_ns,
        ctime_ns=before.st_ctime_ns,
    )


def read_file_bytes(root: Path, relative: str, maximum: int) -> bytes:
    snapshot = snapshot_file(root, relative)
    require(snapshot.size <= maximum, f"{relative}: file exceeds read limit")
    path = _assert_no_symlink_components(root, relative)
    payload = path.read_bytes()
    require(
        len(payload) == snapshot.size and sha256_bytes(payload) == snapshot.sha256,
        f"{relative}: changed between secure snapshot and read",
    )
    return payload


def _parse_expected_record(
    record: object, label: str, *, default_git_anchor: bool = True
) -> ExpectedFile:
    require(isinstance(record, dict), f"{label}: record is not an object")
    allowed = {"path", "size", "size_bytes", "sha256", "git_anchor"}
    require(set(record) <= allowed, f"{label}: unexpected record keys")
    path = _safe_relative_path(record.get("path"), label)
    raw_size = record.get("size", record.get("size_bytes"))
    require(
        type(raw_size) is int and raw_size >= 0,
        f"{label}: invalid byte size",
    )
    sha = record.get("sha256")
    require(
        type(sha) is str and re.fullmatch(r"[0-9a-f]{64}", sha) is not None,
        f"{label}: invalid SHA-256",
    )
    anchor = record.get("git_anchor", default_git_anchor)
    require(type(anchor) is bool, f"{label}: git_anchor is not boolean")
    return ExpectedFile(path=path, size=raw_size, sha256=sha, git_anchor=anchor)


def _merge_expected(
    expected: dict[str, ExpectedFile], record: ExpectedFile, label: str
) -> None:
    prior = expected.get(record.path)
    if prior is None:
        expected[record.path] = record
    else:
        require(
            prior.size == record.size
            and prior.sha256 == record.sha256
            and prior.git_anchor == record.git_anchor,
            f"{label}: conflicting binding for {record.path}",
        )


def _run_git(
    repository: Path,
    arguments: Sequence[str],
    *,
    timeout: int = 30,
    accepted_codes: tuple[int, ...] = (0,),
) -> subprocess.CompletedProcess[bytes]:
    command = ["git", "-C", str(repository), *arguments]
    completed = subprocess.run(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
        env={
            "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            "LANG": "C",
            "LC_ALL": "C",
        },
    )
    require(
        completed.returncode in accepted_codes,
        "Git command failed: "
        + " ".join(arguments)
        + f" (exit {completed.returncode})",
    )
    return completed


@dataclass
class GitAnchor:
    repository: Path
    campaign_prefix: str
    commit: str
    blob_cache: dict[str, tuple[int, str]]


def open_git_anchor(campaign_root: Path, commit: str) -> GitAnchor:
    top = _run_git(campaign_root, ["rev-parse", "--show-toplevel"]).stdout
    try:
        repository = Path(top.decode("utf-8", "strict").strip()).resolve(strict=True)
    except (UnicodeDecodeError, OSError) as error:
        raise ReplayFailure(f"invalid Git repository root: {error}") from error
    try:
        prefix = campaign_root.relative_to(repository).as_posix()
    except ValueError as error:
        raise ReplayFailure("campaign root is outside its Git repository") from error
    require(
        prefix == CAMPAIGN_REPOSITORY_PATH,
        f"unexpected repository-relative campaign path: {prefix}",
    )
    resolved = _run_git(
        repository, ["rev-parse", "--verify", f"{commit}^{{commit}}"]
    ).stdout.decode("ascii", "strict").strip()
    require(resolved == commit, "accepted commit does not resolve exactly")
    _run_git(
        repository,
        ["merge-base", "--is-ancestor", commit, "HEAD"],
        accepted_codes=(0,),
    )
    return GitAnchor(repository, prefix, commit, {})


def _git_blob_digest(anchor: GitAnchor, object_id: str) -> tuple[int, str]:
    cached = anchor.blob_cache.get(object_id)
    if cached is not None:
        return cached
    size_text = _run_git(
        anchor.repository, ["cat-file", "-s", object_id]
    ).stdout.decode("ascii", "strict").strip()
    require(size_text.isdigit(), f"Git blob {object_id}: invalid size")
    command = [
        "git",
        "-C",
        str(anchor.repository),
        "cat-file",
        "blob",
        object_id,
    ]
    process = subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={
            "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
            "LANG": "C",
            "LC_ALL": "C",
        },
    )
    require(process.stdout is not None and process.stderr is not None, "Git pipe")
    digest = hashlib.sha256()
    count = 0
    with process.stdout as stdout, process.stderr as stderr_stream:
        while True:
            block = stdout.read(1 << 20)
            if not block:
                break
            digest.update(block)
            count += len(block)
        stderr = stderr_stream.read()
    return_code = process.wait(timeout=30)
    require(
        return_code == 0 and stderr == b"",
        f"cannot read accepted Git blob {object_id}",
    )
    result = (count, digest.hexdigest())
    require(count == int(size_text), f"Git blob {object_id}: size changed")
    anchor.blob_cache[object_id] = result
    return result


def verify_git_file(anchor: GitAnchor, expected: ExpectedFile) -> None:
    spec = f"{anchor.commit}:{anchor.campaign_prefix}/{expected.path}"
    object_id = _run_git(
        anchor.repository, ["rev-parse", "--verify", spec]
    ).stdout.decode("ascii", "strict").strip()
    require(
        re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", object_id) is not None,
        f"{expected.path}: invalid Git object ID",
    )
    kind = _run_git(
        anchor.repository, ["cat-file", "-t", object_id]
    ).stdout.decode("ascii", "strict").strip()
    require(kind == "blob", f"{expected.path}: accepted object is not a blob")
    size, sha = _git_blob_digest(anchor, object_id)
    require(
        size == expected.size and sha == expected.sha256,
        f"{expected.path}: accepted Git blob differs from lock",
    )


def _regular_tree_paths(root: Path, relative_directory: str) -> set[str]:
    directory = _assert_no_symlink_components(root, relative_directory)
    require(directory.is_dir(), f"{relative_directory}: package is not a directory")
    result: set[str] = set()
    for current, directories, files in os.walk(directory, followlinks=False):
        current_path = Path(current)
        for name in list(directories):
            path = current_path / name
            info = os.lstat(path)
            require(
                stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode),
                f"{relative_directory}: unsafe package directory",
            )
        for name in files:
            path = current_path / name
            info = os.lstat(path)
            require(
                stat.S_ISREG(info.st_mode)
                and not stat.S_ISLNK(info.st_mode)
                and info.st_nlink == 1,
                f"{relative_directory}: unsafe package file",
            )
            result.add(path.relative_to(directory).as_posix())
    return result


def _collect_c5_run(
    root: Path, outcome: Mapping[str, object], expected: dict[str, ExpectedFile]
) -> None:
    base = "results/synthesis_k3_hole5_signature_seed0_600s_binary"
    artifacts = outcome.get("artifacts")
    require(isinstance(artifacts, dict), "C5 outcome artifact ledger missing")
    names = {"outcome.json"}
    for name, record in artifacts.items():
        safe_name = _safe_relative_path(name, "C5 outcome artifact")
        require("/" not in safe_name, "C5 outcome artifact is not a direct child")
        require(isinstance(record, dict), "C5 outcome artifact record malformed")
        item = _parse_expected_record(
            {
                "path": f"{base}/{safe_name}",
                "size_bytes": record.get("size_bytes"),
                "sha256": record.get("sha256"),
            },
            f"C5 outcome {safe_name}",
        )
        _merge_expected(expected, item, "C5 outcome")
        names.add(safe_name)
    require(
        _regular_tree_paths(root, base) == names,
        "C5 retained run has omitted or extra files",
    )


def _collect_c7_package(
    root: Path,
    certificate: Mapping[str, object],
    expected: dict[str, ExpectedFile],
) -> None:
    base = "certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2"
    artifacts = certificate.get("artifacts")
    require(isinstance(artifacts, dict), "C7 package artifact ledger missing")
    names = {"certificate.json"}
    for relative, record in artifacts.items():
        safe = _safe_relative_path(relative, "C7 package artifact")
        require(isinstance(record, dict), "C7 package artifact record malformed")
        require(record.get("path") == safe, "C7 package path self-binding differs")
        item = _parse_expected_record(
            {
                "path": f"{base}/{safe}",
                "size_bytes": record.get("size_bytes"),
                "sha256": record.get("sha256"),
            },
            f"C7 package {safe}",
        )
        _merge_expected(expected, item, "C7 package")
        names.add(safe)
    require(
        _regular_tree_paths(root, base) == names,
        "C7 package has omitted or extra files",
    )

    source_audit = certificate.get("source_audit")
    require(isinstance(source_audit, dict), "C7 source audit missing")
    records = source_audit.get("records")
    require(isinstance(records, dict), "C7 source record ledger missing")
    for role, record in records.items():
        require(isinstance(record, dict), f"C7 source record {role} malformed")
        path = _safe_relative_path(record.get("path"), f"C7 source {role}")
        item = _parse_expected_record(
            {
                "path": path,
                "size_bytes": record.get("size_bytes"),
                "sha256": record.get("sha256"),
                "git_anchor": not path.startswith("tools/"),
            },
            f"C7 source {role}",
        )
        _merge_expected(expected, item, "C7 source")


def _collect_c9_package(
    root: Path,
    certificate: Mapping[str, object],
    expected: dict[str, ExpectedFile],
) -> None:
    base = "certificates/synthesis_k3_hole9_orphan_000170_recovery"
    records = certificate.get("package_artifacts")
    require(isinstance(records, list), "C9 package artifact ledger missing")
    names = {"certificate.json"}
    for index, record in enumerate(records):
        require(isinstance(record, dict), f"C9 package record {index} malformed")
        safe = _safe_relative_path(record.get("path"), f"C9 package record {index}")
        item = _parse_expected_record(
            {
                "path": f"{base}/{safe}",
                "size_bytes": record.get("size_bytes"),
                "sha256": record.get("sha256"),
            },
            f"C9 package {safe}",
        )
        _merge_expected(expected, item, "C9 package")
        names.add(safe)
    require(
        _regular_tree_paths(root, base) == names,
        "C9 package has omitted or extra files",
    )


def _expect_mapping(value: object, label: str) -> Mapping[str, object]:
    require(isinstance(value, dict), f"{label}: expected object")
    return value


def validate_c5_bindings(
    acceptance: Mapping[str, object],
    certificate: Mapping[str, object],
    outcome: Mapping[str, object],
    postrun: Mapping[str, object],
    package_audit: Mapping[str, object],
    postrun_review: str,
    package_review: str,
) -> dict[str, object]:
    expected_branch = {
        "cnf_path": "results/synthesis_k3_hole5_signature_package/instance.cnf",
        "cnf_sha256": C5_CNF_SHA256,
        "variables": 6886,
        "clauses": 23968,
        "literals": 192169,
        "addition_only_proof_path": (
            "results/synthesis_k3_hole5_signature_seed0_600s_binary/"
            "proof.additions.bdrat"
        ),
        "addition_only_proof_sha256": C5_PROOF_SHA256,
        "addition_only_proof_bytes": 6337621,
        "additions": 247981,
        "addition_literals": 4372774,
        "maximum_variable": 6886,
        "final_addition_is_empty": True,
        "strict_checker_command": (
            "drat-trim instance.cnf proof.additions.bdrat -i -f -W -U -t 1200"
        ),
        "strict_checker_exit_code": 0,
        "strict_checker_status_line": "s VERIFIED",
        "strict_checker_rat_lemmas": 0,
        "strict_checker_resolution_steps": 10912555,
    }
    require(
        acceptance.get("hole5_certificate") == expected_branch,
        "C5 C-035 branch binding differs",
    )
    require(
        acceptance.get("hole5_acceptance_artifacts")
        == {
            "outcome_json_sha256": C5_OUTCOME_SHA256,
            "certificate_json_sha256": C5_CERTIFICATE_SHA256,
            "run_config_json_sha256": (
                "6d899e212d2f349b48eefad5037ea007981a331b7e581966165ae861c741221b"
            ),
            "checker_stdout_sha256": (
                "582074fe80efc122bef5586bc9768e32dfbb3a7bb5758f04b5fe23d0862b6515"
            ),
            "raw_binary_proof_sha256": C5_RAW_PROOF_SHA256,
        },
        "C5 acceptance artifact bindings differ",
    )
    require(
        certificate.get("schema") == "gamma-theta-hole5-binary-certificate-v1"
        and certificate.get("schema_version") == 1
        and certificate.get("status") == "UNSAT_REPLAY_ARTIFACT"
        and certificate.get("claim_status")
        == "NO_STANDALONE_MATHEMATICAL_CLAIM"
        and certificate.get("cnf_sha256") == C5_CNF_SHA256,
        "C5 replay certificate identity/status differs",
    )
    proof = _expect_mapping(
        certificate.get("addition_only_binary_proof"), "C5 proof record"
    )
    raw = _expect_mapping(certificate.get("raw_binary_proof"), "C5 raw proof")
    require(
        proof.get("sha256") == C5_PROOF_SHA256
        and proof.get("size_bytes") == 6337621
        and raw.get("sha256") == C5_RAW_PROOF_SHA256
        and raw.get("preserved") is True,
        "C5 certificate proof binding differs",
    )
    requirements = _expect_mapping(
        certificate.get("strict_checker_requirements"), "C5 checker requirements"
    )
    require(
        set(requirements)
        == {
            "binary_input",
            "exactly_one_verified_line",
            "forward",
            "rup_only",
            "warning_fatal",
            "zero_rat_lemmas",
        }
        and all(value is True for value in requirements.values()),
        "C5 strict checker requirements are incomplete",
    )
    require(
        outcome.get("schema")
        == "gamma-theta-hole5-binary-production-outcome-v1"
        and outcome.get("status") == "UNSAT_VERIFIED_FINITE_CERTIFICATE"
        and outcome.get("claim_status") == "VERIFIED_FINITE_CERTIFICATE"
        and outcome.get("cnf_sha256") == C5_CNF_SHA256,
        "C5 terminal outcome identity/status differs",
    )
    semantic = _expect_mapping(outcome.get("semantic_checks"), "C5 semantics")
    require(
        set(semantic)
        == {
            "addition_only_reparsed",
            "all_deletions_removed",
            "checker_warning_free",
            "checker_zero_rat_lemmas",
            "clean_room_parser_max_var",
            "raw_binary_proof_preserved",
            "solver_result_unsat",
            "strict_binary_forward_rup_replay",
        }
        and semantic.get("clean_room_parser_max_var") == 6886
        and all(
            semantic.get(key) is True
            for key in semantic
            if key != "clean_room_parser_max_var"
        ),
        "C5 outcome semantic flags differ",
    )
    require(
        postrun.get("schema")
        == "gamma-theta-hole5-binary-postrun-hostile-audit-v1"
        and postrun.get("schema_version") == 1
        and postrun.get("verdict") == C5_ACTIVATING_VERDICT
        and postrun.get("production_runner_imported_or_trusted") is False
        and postrun.get("production_solver_launched") is False,
        "C5 activating post-run verdict differs",
    )
    replay = _expect_mapping(
        _expect_mapping(postrun.get("checks"), "C5 postrun checks").get(
            "strict_checker_replay"
        ),
        "C5 fresh checker replay",
    )
    require(
        replay.get("exit_code") == 0
        and replay.get("recorded_and_fresh_semantics_identical") is True
        and replay.get("stderr_sha256") == EMPTY_SHA256,
        "C5 retained fresh checker replay differs",
    )
    require(
        package_audit.get("schema")
        == "gamma-theta-hole5-binary-run-package-audit-v1"
        and package_audit.get("audit_status") == "PASS"
        and package_audit.get("claim_status") == "NO_NEW_MATHEMATICAL_CLAIM"
        and package_audit.get("audited_run_status")
        == "UNSAT_VERIFIED_FINITE_CERTIFICATE"
        and package_audit.get("audited_run_claim_status")
        == "VERIFIED_FINITE_CERTIFICATE",
        "C5 retained package audit status differs",
    )
    readonly = _expect_mapping(
        _expect_mapping(
            _expect_mapping(
                package_audit.get("proof_evidence"), "C5 package proof evidence"
            ).get("readonly_replay"),
            "C5 package read-only replay",
        ).get("checker"),
        "C5 package fresh checker",
    )
    require(
        readonly.get("exit_code") == 0
        and readonly.get("verified_status_count") == 1
        and readonly.get("rat_lemmas_in_core") == 0
        and readonly.get("warning_free") is True
        and readonly.get("stderr_sha256") == EMPTY_SHA256,
        "C5 package checker replay status differs",
    )
    require(
        f"`{C5_ACTIVATING_VERDICT}`" in postrun_review
        and "certificate side of the C033 activation gate is satisfied"
        in postrun_review,
        "C5 activating human review scope differs",
    )
    require(
        "`PASS_EXACT_RETAINED_PACKAGE`" in package_review
        and "no new mathematical claim" in package_review
        and "does **not** certify the whole" in package_review,
        "C5 package human review scope differs",
    )
    return {
        "branch": "hub-free induced C5 in complement",
        "claim_id": "C-034",
        "acceptance": C5_ACTIVATING_VERDICT,
        "cnf_sha256": C5_CNF_SHA256,
        "proof_sha256": C5_PROOF_SHA256,
    }


def validate_c7_bindings(
    acceptance: Mapping[str, object],
    certificate: Mapping[str, object],
    review: str,
) -> dict[str, object]:
    require(
        acceptance.get("hole7_certificate")
        == {
            "cnf_path": "results/synthesis_k3_template_bank_packages/hole7/instance.cnf",
            "cnf_sha256": C7_CNF_SHA256,
            "addition_only_proof_path": (
                "certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2/"
                "proof/addition-only.rup.drat"
            ),
            "addition_only_proof_sha256": C7_PROOF_SHA256,
            "accepted_review_path": "reviews/hole7_addition_only_hostile_review.md",
            "accepted_review_sha256": (
                "b904fcec9df16eff06640f36241a7589e1686777a57b7f32f9825832a8cecaa2"
            ),
        },
        "C7 C-035 branch binding differs",
    )
    require(
        certificate.get("schema")
        == "gamma-theta-hole7-addition-only-recovery-v2"
        and certificate.get("schema_version") == 2
        and certificate.get("status") == "VERIFIED_FINITE_CERTIFICATE"
        and certificate.get("claim")
        == "the exact full-bank order-12 parameter-three hole7 CNF is unsatisfiable",
        "C7 certificate identity/status differs",
    )
    boundary = certificate.get("claim_boundary")
    require(
        boundary
        == {
            "graph_theoretic_use_requires_separate_coverage_proofs": True,
            "hole5_addressed": False,
            "order": 12,
            "parameter": 3,
            "template": "hole7",
            "universal_conjecture_resolved": False,
        },
        "C7 certificate boundary differs",
    )
    require(
        certificate.get("cnf")
        == {
            "clause_count": 21718,
            "literal_count": 148551,
            "sha256": C7_CNF_SHA256,
            "size_bytes": 621864,
            "variable_count": 6886,
        },
        "C7 CNF record differs",
    )
    strict = _expect_mapping(
        certificate.get("strict_checker"), "C7 strict checker"
    )
    require(
        strict.get("exit_code") == 0
        and strict.get("verified_line_count") == 1
        and strict.get("warning_free") is True
        and strict.get("zero_rat_lemmas_in_core") is True
        and strict.get("proof_sha256_before") == C7_PROOF_SHA256
        and strict.get("proof_sha256_after") == C7_PROOF_SHA256
        and strict.get("cnf_sha256_before") == C7_CNF_SHA256
        and strict.get("cnf_sha256_after") == C7_CNF_SHA256
        and strict.get("command_flags")
        == ["-I", "-f", "-W", "-U", "-t", "600"],
        "C7 strict checker semantics differ",
    )
    require(
        "**ACCEPT the v2 recovery without mathematical reservation.**" in review
        and "The slice is **not** complete until `hole5`" in review
        and "There is no connected graph" in review,
        "C7 human review verdict/scope differs",
    )
    return {
        "branch": "hub-free induced C7 in complement",
        "claim_id": "C-030",
        "acceptance": "ACCEPT_V2_WITHOUT_MATHEMATICAL_RESERVATION",
        "cnf_sha256": C7_CNF_SHA256,
        "proof_sha256": C7_PROOF_SHA256,
    }


def validate_c9_bindings(
    acceptance: Mapping[str, object],
    branch_acceptance: Mapping[str, object],
    certificate: Mapping[str, object],
    implication: str,
    implication_review: str,
) -> dict[str, object]:
    require(
        acceptance.get("hole9_certificate")
        == {
            "cnf_sha256": C9_CNF_SHA256,
            "addition_only_proof_sha256": C9_PROOF_SHA256,
            "acceptance_path": "results/synthesis_k3_hole9_orphan_recovery_acceptance.json",
            "acceptance_sha256": C9_ACCEPTANCE_SHA256,
            "graph_implication_path": "math/lemmas/hole9_template_exclusion.md",
            "graph_implication_sha256": (
                "4305dcfc170f665d0c97b5d4601c3dd226099b61e11a2ad28a15fc66ee36c1f2"
            ),
            "hostile_review_path": "reviews/hole9_template_exclusion_hostile_review.md",
            "hostile_review_sha256": (
                "e17707945f3420c4ba2ecb6b3056b14789e2648e12e4c641772dfb7cee6452b7"
            ),
        },
        "C9 C-035 branch binding differs",
    )
    require(
        branch_acceptance.get("schema")
        == "gamma-theta-hole9-orphan-recovery-acceptance-v1"
        and branch_acceptance.get("status")
        == "accepted_with_two_validated_errata"
        and branch_acceptance.get("claim_id") == "C-028"
        and branch_acceptance.get("claim_classification") == "CERTIFIED-FINITE",
        "C9 branch acceptance identity/status differs",
    )
    require(
        branch_acceptance.get("mathematical_claim")
        == (
            "There is no connected 12-vertex graph G such that "
            "gamma(G)=alpha(G)=gamma_infinity(G)=3<theta(G) and "
            "complement(G) contains a hub-free induced C9."
        ),
        "C9 accepted mathematical claim differs",
    )
    formula = _expect_mapping(branch_acceptance.get("formula"), "C9 formula")
    proof = _expect_mapping(branch_acceptance.get("proof"), "C9 proof")
    package = _expect_mapping(branch_acceptance.get("package"), "C9 package")
    require(
        formula.get("template") == "hole9"
        and formula.get("order") == 12
        and formula.get("guard_parameter") == 3
        and formula.get("variable_count") == 6886
        and formula.get("total_clause_count") == 20200
        and formula.get("cnf_sha256") == C9_CNF_SHA256
        and formula.get("byte_identical_independent_reconstruction") is True
        and formula.get("globally_valid_coloring_cuts") is True,
        "C9 formula acceptance record differs",
    )
    require(
        proof.get("addition_only_proof_sha256") == C9_PROOF_SHA256
        and proof.get("addition_count") == 4705
        and proof.get("all_additions_independently_rup_verified") is True
        and proof.get("final_addition_is_empty_clause") is True
        and proof.get("rat_lemmas_used") == 0,
        "C9 proof acceptance record differs",
    )
    require(
        package.get("outer_certificate_path")
        == "certificates/synthesis_k3_hole9_orphan_000170_recovery/certificate.json"
        and package.get("outer_certificate_sha256")
        == C9_OUTER_CERTIFICATE_SHA256,
        "C9 outer certificate binding differs",
    )
    require(
        certificate.get("schema")
        == "gamma-theta-hole9-recovered-certificate-v1"
        and certificate.get("schema_version") == 1
        and certificate.get("status") == "verified_pending_hostile_review"
        and certificate.get("order") == 12
        and certificate.get("template") == "hole9",
        "C9 outer package identity/status differs",
    )
    validation = _expect_mapping(certificate.get("validation"), "C9 validation")
    require(
        validation.get("addition_only_proof_rup_verified") is True
        and validation.get("checker_warning_free") is True
        and validation.get("formula_exactly_reconstructed") is True
        and validation.get("package_pending_hostile_review") is True,
        "C9 outer package validation flags differ",
    )
    require(
        "# Certified exclusion of the order-12 `hole9` template" in implication
        and "There is no connected 12-vertex graph" in implication
        and "does not assert that the original\nCEGAR run reached a terminal"
        in implication,
        "C9 graph implication scope differs",
    )
    require(
        "**ACCEPT without reservation.**" in implication_review
        and "No\nquantifier error, complement reversal, one-guard-model error"
        in implication_review,
        "C9 graph implication review verdict differs",
    )
    return {
        "branch": "hub-free induced C9 in complement",
        "claim_id": "C-028",
        "acceptance": "ACCEPTED_WITH_TWO_VALIDATED_ERRATA",
        "cnf_sha256": C9_CNF_SHA256,
        "proof_sha256": C9_PROOF_SHA256,
    }


def validate_theorem_scope(
    acceptance: Mapping[str, object],
    theorem: str,
    first_review: str,
    second_review: str,
) -> dict[str, object]:
    require(
        acceptance.get("acceptance_version") == 1
        and acceptance.get("campaign_day") == 1
        and acceptance.get("claim_id") == "C-035"
        and acceptance.get("claim_status") == "CERTIFIED-FINITE"
        and acceptance.get("claim") == CLAIM
        and acceptance.get("scope_exclusions") == SCOPE_EXCLUSIONS
        and acceptance.get("source_commit")
        == "6f3ef0a0970b7214c34018fe32ea1ceeb5764d17"
        and acceptance.get("frozen_run_commit")
        == "dff45f4239e4acabc461533a0a213beec18ec56d"
        and acceptance.get("verdict")
        == "ACCEPT_CERTIFIED_FINITE_ORDER12_PARAMETER3_EXCLUSION",
        "C-035 acceptance identity/scope differs",
    )
    complete = _expect_mapping(
        acceptance.get("complete_slice_proof"), "C-035 complete-slice proof"
    )
    require(
        complete.get("theorem_path") == "math/lemmas/order12_k3_exclusion.md"
        and complete.get("theorem_sha256")
        == "b6010d6f365a62845e24666603f6417d87f14c37876e3406dc2a7c6b6ee91ae4"
        and complete.get("first_review_verdict")
        == "ACCEPT_COMPLETE_ORDER12_K3_EXCLUSION"
        and complete.get("second_review_verdict") == "ACCEPT_NO_BLOCKER"
        and complete.get("disconnected_case_explicitly_covered") is True
        and complete.get("exhaustive_connected_template_branches")
        == [
            "hub-free induced C5 in complement: C-034",
            "hub-free induced C7 in complement: C-030",
            "hub-free induced C9 in complement: C-028",
        ],
        "C-035 complete-slice branch/coverage binding differs",
    )
    theorem_markers = [
        "**Theorem 1 (order 12, parameter 3).**  No finite simple graph",
        "The theorem includes disconnected graphs.",
        "attacks are only at unoccupied vertices, and one guard moves along one edge",
        "exclude order-12 counterexamples with common parameter \\(k\\ge4\\);",
        "resolve the universal \\(\\gamma\\)--\\(\\theta\\) conjecture.",
    ]
    require(
        all(marker in theorem for marker in theorem_markers),
        "C-035 theorem statement/model/scope marker differs",
    )
    require(
        "**`ACCEPT_COMPLETE_ORDER12_K3_EXCLUSION`.**" in first_review
        and "assigns `CERTIFIED-FINITE`, not `PROVED`" in first_review
        and "**`ACCEPT_NO_BLOCKER`.**" in second_review
        and "does not certify:" in second_review,
        "C-035 review verdict/scope marker differs",
    )
    return {
        "claim_id": "C-035",
        "classification": "CERTIFIED-FINITE",
        "disconnected_graphs_covered": True,
        "template_branches": ["C5", "C7", "C9"],
        "universal_conjecture_resolved": False,
    }


def parse_manifest_bytes(payload: bytes, label: str) -> dict[str, dict[str, str]]:
    require(b"\x00" not in payload and b"\r" not in payload, f"{label}: bad bytes")
    try:
        text = payload.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise ReplayFailure(f"{label}: invalid UTF-8") from error
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    try:
        header = next(reader)
    except StopIteration as error:
        raise ReplayFailure(f"{label}: empty manifest") from error
    require(header == MANIFEST_HEADER, f"{label}: manifest header differs")
    rows: dict[str, dict[str, str]] = {}
    for row_number, values in enumerate(reader, start=2):
        require(
            len(values) == len(MANIFEST_HEADER),
            f"{label}: row {row_number} has wrong width",
        )
        row = dict(zip(MANIFEST_HEADER, values, strict=True))
        artifact_id = row["artifact_id"]
        require(
            re.fullmatch(r"ART-[0-9]{3,}", artifact_id) is not None,
            f"{label}: malformed artifact ID at row {row_number}",
        )
        require(artifact_id not in rows, f"{label}: duplicate {artifact_id}")
        require(
            re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None,
            f"{label}: malformed SHA-256 at row {row_number}",
        )
        rows[artifact_id] = row
    return rows


def validate_manifest_rows(
    rows: Mapping[str, Mapping[str, str]],
    expected_rows: Mapping[str, object],
    label: str,
) -> None:
    for artifact_id, expected in expected_rows.items():
        require(isinstance(expected, dict), f"{label}: lock row malformed")
        actual = rows.get(artifact_id)
        require(actual is not None, f"{label}: missing {artifact_id}")
        require(
            all(actual.get(key) == value for key, value in expected.items()),
            f"{label}: scope/binding mismatch in {artifact_id}",
        )


@dataclass
class MetadataResult:
    report: dict[str, object]
    snapshots: dict[str, FileSnapshot]
    expected: dict[str, ExpectedFile]


def _load_locked_json(root: Path, relative: str, label: str) -> Mapping[str, object]:
    value = strict_json_bytes(read_file_bytes(root, relative, 2 << 20), label)
    return _expect_mapping(value, label)


def verify_metadata(root: Path) -> MetadataResult:
    campaign = root.resolve(strict=True)
    require(campaign.is_dir(), "campaign root is not a directory")
    lock_relative = "repro/c035/accepted_artifacts.json"
    lock_payload = read_file_bytes(campaign, lock_relative, 1 << 20)
    require(
        sha256_bytes(lock_payload) == LOCK_SHA256,
        "C-035 replay lock hash differs",
    )
    lock = _expect_mapping(strict_json_bytes(lock_payload, "C-035 lock"), "C-035 lock")
    require(
        lock.get("schema") == LOCK_SCHEMA
        and lock.get("schema_version") == 1
        and lock.get("claim_id") == "C-035"
        and lock.get("accepted_commit") == ACCEPTED_COMMIT,
        "C-035 replay lock identity differs",
    )
    records = lock.get("artifacts")
    require(isinstance(records, list) and records, "C-035 lock artifact list missing")
    expected: dict[str, ExpectedFile] = {}
    for index, record in enumerate(records):
        item = _parse_expected_record(record, f"lock artifact {index}")
        _merge_expected(expected, item, "C-035 lock")
    _merge_expected(
        expected,
        ExpectedFile(
            path=lock_relative,
            size=len(lock_payload),
            sha256=LOCK_SHA256,
            git_anchor=False,
        ),
        "C-035 lock self-binding",
    )
    replay_relative = "repro/c035/replay.py"
    replay_snapshot = snapshot_file(campaign, replay_relative)
    _merge_expected(
        expected,
        ExpectedFile(
            path=replay_relative,
            size=replay_snapshot.size,
            sha256=replay_snapshot.sha256,
            git_anchor=False,
        ),
        "C-035 executing replay snapshot",
    )

    snapshots: dict[str, FileSnapshot] = {}
    for path, item in expected.items():
        snapshot = snapshot_file(campaign, path)
        require(
            snapshot.size == item.size and snapshot.sha256 == item.sha256,
            f"locked artifact hash/size mismatch: {path}",
        )
        snapshots[path] = snapshot

    acceptance = _load_locked_json(
        campaign,
        "results/order12_k3_exclusion_acceptance.json",
        "C-035 acceptance",
    )
    c5_certificate = _load_locked_json(
        campaign,
        "results/synthesis_k3_hole5_signature_seed0_600s_binary/certificate.json",
        "C5 certificate",
    )
    c5_outcome = _load_locked_json(
        campaign,
        "results/synthesis_k3_hole5_signature_seed0_600s_binary/outcome.json",
        "C5 outcome",
    )
    c5_postrun = _load_locked_json(
        campaign,
        "reviews/hole5_binary_production_postrun_hostile_probe_log.json",
        "C5 postrun log",
    )
    c5_package_audit = _load_locked_json(
        campaign,
        "results/logs/hole5-binary-run-package-audit.json",
        "C5 package audit",
    )
    c7_certificate = _load_locked_json(
        campaign,
        "certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2/certificate.json",
        "C7 certificate",
    )
    c9_acceptance = _load_locked_json(
        campaign,
        "results/synthesis_k3_hole9_orphan_recovery_acceptance.json",
        "C9 acceptance",
    )
    c9_certificate = _load_locked_json(
        campaign,
        "certificates/synthesis_k3_hole9_orphan_000170_recovery/certificate.json",
        "C9 certificate",
    )

    _collect_c5_run(campaign, c5_outcome, expected)
    _collect_c7_package(campaign, c7_certificate, expected)
    _collect_c9_package(campaign, c9_certificate, expected)

    for path, item in expected.items():
        if path in snapshots:
            continue
        snapshot = snapshot_file(campaign, path)
        require(
            snapshot.size == item.size and snapshot.sha256 == item.sha256,
            f"certificate-led artifact hash/size mismatch: {path}",
        )
        snapshots[path] = snapshot

    theorem = read_file_bytes(
        campaign, "math/lemmas/order12_k3_exclusion.md", 1 << 20
    ).decode("utf-8", "strict")
    first_review = read_file_bytes(
        campaign, "reviews/order12_k3_exclusion_hostile_review.md", 1 << 20
    ).decode("utf-8", "strict")
    second_review = read_file_bytes(
        campaign, "reviews/order12_k3_exclusion_second_review.md", 1 << 20
    ).decode("utf-8", "strict")
    c5_postrun_review = read_file_bytes(
        campaign,
        "reviews/hole5_binary_production_postrun_hostile_review.md",
        1 << 20,
    ).decode("utf-8", "strict")
    c5_package_review = read_file_bytes(
        campaign, "reviews/hole5_binary_run_package_audit_review.md", 1 << 20
    ).decode("utf-8", "strict")
    c7_review = read_file_bytes(
        campaign, "reviews/hole7_addition_only_hostile_review.md", 1 << 20
    ).decode("utf-8", "strict")
    c9_implication = read_file_bytes(
        campaign, "math/lemmas/hole9_template_exclusion.md", 1 << 20
    ).decode("utf-8", "strict")
    c9_implication_review = read_file_bytes(
        campaign, "reviews/hole9_template_exclusion_hostile_review.md", 1 << 20
    ).decode("utf-8", "strict")

    branches = {
        "C5": validate_c5_bindings(
            acceptance,
            c5_certificate,
            c5_outcome,
            c5_postrun,
            c5_package_audit,
            c5_postrun_review,
            c5_package_review,
        ),
        "C7": validate_c7_bindings(acceptance, c7_certificate, c7_review),
        "C9": validate_c9_bindings(
            acceptance,
            c9_acceptance,
            c9_certificate,
            c9_implication,
            c9_implication_review,
        ),
    }
    theorem_scope = validate_theorem_scope(
        acceptance, theorem, first_review, second_review
    )

    expected_rows = _expect_mapping(lock.get("manifest_rows"), "manifest rows")
    manifest_payload = read_file_bytes(
        campaign, "results/manifest.csv", 16 << 20
    )
    current_rows = parse_manifest_bytes(manifest_payload, "current manifest")
    validate_manifest_rows(current_rows, expected_rows, "current manifest")

    anchor = open_git_anchor(campaign, ACCEPTED_COMMIT)
    for item in expected.values():
        if item.git_anchor:
            verify_git_file(anchor, item)
    accepted_manifest = _run_git(
        anchor.repository,
        [
            "show",
            f"{ACCEPTED_COMMIT}:{CAMPAIGN_REPOSITORY_PATH}/results/manifest.csv",
        ],
    ).stdout
    accepted_rows = parse_manifest_bytes(accepted_manifest, "accepted manifest")
    validate_manifest_rows(accepted_rows, expected_rows, "accepted manifest")

    public_snapshot = [
        snapshots[path].public() for path in sorted(snapshots)
    ]
    snapshot_payload = canonical_json_bytes(public_snapshot)
    report = {
        "accepted_commit": ACCEPTED_COMMIT,
        "accepted_commit_is_ancestor_of_head": True,
        "artifact_snapshot_sha256": sha256_bytes(snapshot_payload),
        "branch_bindings": branches,
        "claim_id": "C-035",
        "claim_status": "NO_MATHEMATICAL_CLAIM",
        "git_anchored_artifact_count": sum(
            1 for item in expected.values() if item.git_anchor
        ),
        "locked_artifact_count": len(expected),
        "manifest_rows": sorted(expected_rows),
        "mode": "fast",
        "non_git_anchored_artifacts": sorted(
            item.path for item in expected.values() if not item.git_anchor
        ),
        "proofs_freshly_replayed": False,
        "schema": SCHEMA,
        "status": "PASS_METADATA_ONLY",
        "theorem_scope": theorem_scope,
        "warning": (
            "Metadata mode validates exact accepted bytes, bindings, status "
            "markers, scope, and Git anchors but makes NO_MATHEMATICAL_CLAIM."
        ),
    }
    return MetadataResult(report=report, snapshots=snapshots, expected=expected)


def _available_memory_bytes() -> int:
    if sys.platform == "darwin":
        completed = subprocess.run(
            ["/usr/bin/vm_stat"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            check=False,
            env={"PATH": "/usr/bin:/bin", "LANG": "C", "LC_ALL": "C"},
        )
        require(
            completed.returncode == 0 and completed.stderr == b"",
            "cannot read macOS memory availability",
        )
        text = completed.stdout.decode("ascii", "strict")
        first, *lines = text.splitlines()
        match = re.search(r"page size of ([0-9]+) bytes", first)
        require(match is not None, "cannot parse vm_stat page size")
        page_size = int(match.group(1))
        counts: dict[str, int] = {}
        for line in lines:
            field = re.fullmatch(r"([^:]+):\s+([0-9]+)\.", line.strip())
            if field is not None:
                counts[field.group(1)] = int(field.group(2))
        names = ("Pages free", "Pages inactive", "Pages speculative")
        require(all(name in counts for name in names), "vm_stat fields missing")
        return page_size * sum(counts[name] for name in names)
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        for line in meminfo.read_text(encoding="ascii").splitlines():
            match = re.fullmatch(r"MemAvailable:\s+([0-9]+) kB", line)
            if match is not None:
                return int(match.group(1)) << 10
    try:
        pages = os.sysconf("SC_AVPHYS_PAGES")
        page_size = os.sysconf("SC_PAGE_SIZE")
    except (OSError, ValueError):
        pages = 0
        page_size = 0
    require(
        type(pages) is int
        and type(page_size) is int
        and pages > 0
        and page_size > 0,
        "cannot determine available physical memory",
    )
    return pages * page_size


def _logical_cpu_count() -> int:
    count = os.cpu_count()
    require(type(count) is int and count >= 1, "cannot determine logical CPUs")
    return count


def _one_minute_load() -> float:
    try:
        load = float(os.getloadavg()[0])
    except (AttributeError, OSError) as error:
        raise ReplayFailure("cannot determine one-minute CPU load") from error
    require(math.isfinite(load) and load >= 0.0, "invalid one-minute CPU load")
    return load


def default_maximum_one_minute_load() -> float:
    return 0.75 * _logical_cpu_count()


def _resource_gate(
    scratch: Path,
    *,
    minimum_available_mib: int,
    minimum_disk_mib: int,
    maximum_one_minute_load: float,
) -> dict[str, int | float]:
    require(
        type(minimum_available_mib) is int and minimum_available_mib >= 2048,
        "full replay memory floor must be at least 2048 MiB",
    )
    require(
        type(minimum_disk_mib) is int and minimum_disk_mib >= 512,
        "full replay disk floor must be at least 512 MiB",
    )
    logical_cpus = _logical_cpu_count()
    require(
        type(maximum_one_minute_load) is float
        and math.isfinite(maximum_one_minute_load)
        and 0.0 < maximum_one_minute_load < float(logical_cpus),
        "full replay load ceiling must be positive and below logical CPU count",
    )
    available = _available_memory_bytes()
    disk_free = shutil.disk_usage(scratch).free
    one_minute_load = _one_minute_load()
    require(
        available >= (minimum_available_mib << 20),
        "full replay refused by available-memory gate",
    )
    require(
        disk_free >= (minimum_disk_mib << 20),
        "full replay refused by scratch-disk gate",
    )
    require(
        one_minute_load <= maximum_one_minute_load,
        "full replay refused by one-minute CPU-load gate",
    )
    return {
        "available_memory_bytes": available,
        "disk_free_bytes": disk_free,
        "logical_cpu_count": logical_cpus,
        "maximum_one_minute_load": maximum_one_minute_load,
        "minimum_available_memory_bytes": minimum_available_mib << 20,
        "minimum_disk_free_bytes": minimum_disk_mib << 20,
        "one_minute_load": one_minute_load,
    }


@dataclass(frozen=True)
class AuditSpec:
    name: str
    arguments: tuple[str, ...]
    validator: Callable[[Mapping[str, object], str], dict[str, object]]


def _validate_c5_postrun_fresh(
    result: Mapping[str, object], stdout_sha256: str
) -> dict[str, object]:
    require(stdout_sha256 == C5_POSTRUN_LOG_SHA256, "fresh C5 postrun log differs")
    require(
        result.get("schema")
        == "gamma-theta-hole5-binary-postrun-hostile-audit-v1"
        and result.get("schema_version") == 1
        and result.get("verdict") == C5_ACTIVATING_VERDICT
        and result.get("production_runner_imported_or_trusted") is False
        and result.get("production_solver_launched") is False,
        "fresh C5 postrun status differs",
    )
    checks = _expect_mapping(result.get("checks"), "fresh C5 checks")
    proof = _expect_mapping(checks.get("proofs"), "fresh C5 proof checks")
    checker = _expect_mapping(
        checks.get("strict_checker_replay"), "fresh C5 checker"
    )
    require(
        _expect_mapping(proof.get("addition_only"), "fresh C5 addition proof").get(
            "proof_sha256"
        )
        == C5_PROOF_SHA256
        and proof.get("addition_subsequence_byte_exact") is True
        and checker.get("exit_code") == 0
        and checker.get("recorded_and_fresh_semantics_identical") is True
        and checker.get("stderr_sha256") == EMPTY_SHA256,
        "fresh C5 proof/checker semantics differ",
    )
    return {
        "status": C5_ACTIVATING_VERDICT,
        "stdout_sha256": stdout_sha256,
        "strict_warning_fatal_forward_rup_replay": True,
    }


def _validate_c5_package_fresh(
    result: Mapping[str, object], stdout_sha256: str
) -> dict[str, object]:
    require(stdout_sha256 == C5_PACKAGE_LOG_SHA256, "fresh C5 package log differs")
    require(
        result.get("schema")
        == "gamma-theta-hole5-binary-run-package-audit-v1"
        and result.get("audit_status") == "PASS"
        and result.get("claim_status") == "NO_NEW_MATHEMATICAL_CLAIM",
        "fresh C5 package audit status differs",
    )
    proof = _expect_mapping(result.get("proof_evidence"), "fresh C5 package proof")
    readonly = _expect_mapping(proof.get("readonly_replay"), "fresh C5 replay")
    checker = _expect_mapping(readonly.get("checker"), "fresh C5 checker")
    parser = _expect_mapping(readonly.get("parser"), "fresh C5 parser")
    require(
        checker.get("exit_code") == 0
        and checker.get("verified_status_count") == 1
        and checker.get("rat_lemmas_in_core") == 0
        and checker.get("warning_free") is True
        and checker.get("stderr_sha256") == EMPTY_SHA256
        and parser.get("exit_code") == 0
        and parser.get("exact_retained_report_match") is True
        and parser.get("addition_proof_sha256") == C5_PROOF_SHA256,
        "fresh C5 package proof replay differs",
    )
    return {
        "status": "PASS_EXACT_RETAINED_PACKAGE",
        "stdout_sha256": stdout_sha256,
        "strict_warning_fatal_forward_rup_replay": True,
    }


def _validate_c7_fresh(
    result: Mapping[str, object], stdout_sha256: str
) -> dict[str, object]:
    expected_keys = {
        "certificate_sha256",
        "addition_only_proof_sha256",
        "addition_only_proof_size_bytes",
        "addition_count",
        "deleted_record_count",
        "strict_checker_replayed",
        "strict_checker_warning_free",
        "strict_checker_rup_only",
    }
    require(set(result) == expected_keys, "fresh C7 audit fields differ")
    require(
        result.get("certificate_sha256") == C7_CERTIFICATE_SHA256
        and result.get("addition_only_proof_sha256") == C7_PROOF_SHA256
        and result.get("addition_only_proof_size_bytes") == 18093724
        and result.get("addition_count") == 284317
        and result.get("deleted_record_count") == 263162
        and result.get("strict_checker_replayed") is True
        and result.get("strict_checker_warning_free") is True
        and result.get("strict_checker_rup_only") is True,
        "fresh C7 proof replay status differs",
    )
    return {
        "status": "VERIFIED_FINITE_CERTIFICATE",
        "stdout_sha256": stdout_sha256,
        "strict_warning_fatal_forward_rup_replay": True,
    }


def _validate_c9_fresh(
    result: Mapping[str, object], stdout_sha256: str
) -> dict[str, object]:
    require(
        result.get("schema") == "gamma-theta-hole9-orphan-recovery-v1"
        and result.get("status") == "audit_passed_pending_hostile_review"
        and result.get("cnf_sha256") == C9_CNF_SHA256
        and result.get("addition_only_proof_sha256") == C9_PROOF_SHA256
        and result.get("checker_exit_code") == 0
        and result.get("checker_flags") == ["-I", "-f", "-W", "-U", "-t", "60"]
        and result.get("exact_verified_line_count") == 1
        and result.get("warning_count") == 0,
        "fresh C9 proof replay status differs",
    )
    return {
        "status": "AUDIT_PASSED_THEN_ACCEPTED_BY_C028_REVIEW",
        "stdout_sha256": stdout_sha256,
        "strict_warning_fatal_forward_rup_replay": True,
    }


def full_audit_specs(root: Path) -> tuple[AuditSpec, ...]:
    python = str(Path(sys.executable).resolve(strict=True))
    checker = str(
        (root / "tools/drat_trim_2023_05_22/drat-trim").resolve(strict=True)
    )
    c7_package = str(
        (
            root
            / "certificates/synthesis_k3_hole7_full_bank_seed0_addition_only_v2"
        ).resolve(strict=True)
    )
    c9_package = str(
        (
            root / "certificates/synthesis_k3_hole9_orphan_000170_recovery"
        ).resolve(strict=True)
    )
    return (
        AuditSpec(
            "c5_postrun_clean_room",
            (
                python,
                "-I",
                "-B",
                str(
                    (
                        root
                        / "reviews/hole5_binary_production_postrun_hostile_probe.py"
                    ).resolve(strict=True)
                ),
            ),
            _validate_c5_postrun_fresh,
        ),
        AuditSpec(
            "c5_retained_package_clean_room",
            (
                python,
                "-I",
                "-B",
                str(
                    (
                        root / "reviews/hole5_binary_run_package_auditor.py"
                    ).resolve(strict=True)
                ),
            ),
            _validate_c5_package_fresh,
        ),
        AuditSpec(
            "c7_sealed_addition_only",
            (
                python,
                "-I",
                "-B",
                str(
                    (
                        root
                        / "certificates/"
                        "synthesis_k3_hole7_full_bank_seed0_addition_only_v2/"
                        "repro/hole7_deletion_strip_auditor.py"
                    ).resolve(strict=True)
                ),
                "audit",
                "--package",
                c7_package,
                "--replay-checker",
            ),
            _validate_c7_fresh,
        ),
        AuditSpec(
            "c9_sealed_orphan_recovery",
            (
                python,
                "-I",
                "-B",
                str(
                    (
                        root
                        / "certificates/synthesis_k3_hole9_orphan_000170_recovery/"
                        "repro/hole9_orphan_recovery.py"
                    ).resolve(strict=True)
                ),
                "audit",
                "--package",
                c9_package,
                "--drat-trim",
                checker,
            ),
            _validate_c9_fresh,
        ),
    )


def _terminate_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    process.wait(timeout=5)


def run_isolated_audit(
    spec: AuditSpec,
    *,
    root: Path,
    scratch_root: Path,
    timeout_seconds: int,
) -> dict[str, object]:
    require(
        type(timeout_seconds) is int and 60 <= timeout_seconds <= 3600,
        "audit timeout must be between 60 and 3600 seconds",
    )
    audit_directory = scratch_root / spec.name
    audit_directory.mkdir(mode=0o700)
    require(
        stat.S_IMODE(os.lstat(audit_directory).st_mode) == 0o700,
        f"{spec.name}: scratch mode differs",
    )
    child_tmp = audit_directory / "tmp"
    child_home = audit_directory / "home"
    child_tmp.mkdir(mode=0o700)
    child_home.mkdir(mode=0o700)
    stdout_path = audit_directory / "stdout.json"
    stderr_path = audit_directory / "stderr.txt"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    stdout_fd = os.open(stdout_path, flags, 0o600)
    stderr_fd = os.open(stderr_path, flags, 0o600)
    env = {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(child_home),
        "TMPDIR": str(child_tmp),
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    try:
        with os.fdopen(stdout_fd, "wb") as stdout_handle, os.fdopen(
            stderr_fd, "wb"
        ) as stderr_handle:
            process = subprocess.Popen(
                spec.arguments,
                cwd=root,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=stdout_handle,
                stderr=stderr_handle,
                start_new_session=True,
            )
            try:
                return_code = process.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired as error:
                _terminate_process_group(process)
                raise ReplayFailure(f"{spec.name}: audit timed out") from error
            stdout_handle.flush()
            os.fsync(stdout_handle.fileno())
            stderr_handle.flush()
            os.fsync(stderr_handle.fileno())
    except BaseException:
        if "process" in locals() and process.poll() is None:
            _terminate_process_group(process)
        raise
    stdout = read_file_bytes(
        audit_directory, "stdout.json", maximum=4 << 20
    )
    stderr = read_file_bytes(
        audit_directory, "stderr.txt", maximum=4 << 20
    )
    require(return_code == 0, f"{spec.name}: audit exit {return_code}")
    require(stderr == b"", f"{spec.name}: nonempty stderr")
    parsed = strict_json_bytes(stdout, f"{spec.name} stdout")
    result = _expect_mapping(parsed, f"{spec.name} stdout")
    accepted = spec.validator(result, sha256_bytes(stdout))
    return {
        **accepted,
        "command_sha256": sha256_bytes(
            b"\x00".join(argument.encode("utf-8") for argument in spec.arguments)
        ),
        "exit_code": return_code,
        "stderr_sha256": sha256_bytes(stderr),
    }


def verify_snapshots_unchanged(
    root: Path,
    before: Mapping[str, FileSnapshot],
    expected: Mapping[str, ExpectedFile],
) -> dict[str, FileSnapshot]:
    after: dict[str, FileSnapshot] = {}
    for path in sorted(expected):
        current = snapshot_file(root, path)
        prior = before[path]
        requirement = expected[path]
        require(
            current.size == requirement.size
            and current.sha256 == requirement.sha256
            and current.device == prior.device
            and current.inode == prior.inode
            and current.mtime_ns == prior.mtime_ns
            and current.ctime_ns == prior.ctime_ns,
            f"accepted artifact changed during full replay: {path}",
        )
        after[path] = current
    return after


def run_full_replay(
    root: Path,
    metadata: MetadataResult,
    *,
    timeout_seconds: int,
    minimum_available_mib: int,
    minimum_disk_mib: int,
    maximum_one_minute_load: float,
    scratch_parent: Path | None,
) -> dict[str, object]:
    if scratch_parent is not None:
        raw_parent = scratch_parent.absolute()
        require(
            raw_parent.exists() and not raw_parent.is_symlink(),
            "unsafe scratch parent",
        )
        parent = raw_parent.resolve(strict=True)
    else:
        parent = Path(tempfile.gettempdir()).resolve(strict=True)
    require(parent.is_dir() and not parent.is_symlink(), "unsafe scratch parent")
    with tempfile.TemporaryDirectory(prefix="gamma-theta-c035.", dir=parent) as raw:
        scratch = Path(raw)
        os.chmod(scratch, 0o700)
        gates: list[dict[str, int]] = []
        audit_results: dict[str, object] = {}
        for spec in full_audit_specs(root):
            gates.append(
                _resource_gate(
                    scratch,
                    minimum_available_mib=minimum_available_mib,
                    minimum_disk_mib=minimum_disk_mib,
                    maximum_one_minute_load=maximum_one_minute_load,
                )
            )
            audit_results[spec.name] = run_isolated_audit(
                spec,
                root=root,
                scratch_root=scratch,
                timeout_seconds=timeout_seconds,
            )
        verify_snapshots_unchanged(
            root, metadata.snapshots, metadata.expected
        )
    report = dict(metadata.report)
    report.update(
        {
            "audit_results": audit_results,
            "claim_status": "CERTIFIED-FINITE",
            "mode": "full",
            "proofs_freshly_replayed": True,
            "resource_gates": gates,
            "status": "PASS_FULL_C035_REPLAY",
            "warning": (
                "This replays the accepted finite C5, C7, and C9 proof "
                "branches. It does not resolve the universal conjecture."
            ),
        }
    )
    return report


def write_new_file(path: Path, payload: bytes) -> None:
    unresolved = path.absolute()
    require(
        unresolved.name not in ("", ".", ".."),
        "unsafe output filename",
    )
    try:
        os.lstat(unresolved)
    except FileNotFoundError:
        pass
    else:
        raise ReplayFailure("output already exists")
    parent = unresolved.parent.resolve(strict=True)
    require(parent.is_dir() and not parent.is_symlink(), "unsafe output parent")
    target = parent / unresolved.name
    try:
        os.lstat(target)
    except FileNotFoundError:
        pass
    else:
        raise ReplayFailure("output already exists")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_CLOEXEC"):
        flags |= os.O_CLOEXEC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(target, flags, 0o600)
    installed = False
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        installed = True
        directory = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if not installed:
            try:
                target.unlink()
            except FileNotFoundError:
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("fast", "full"),
        default="fast",
        help="fast validates metadata only; full freshly replays all three proofs",
    )
    parser.add_argument(
        "--campaign-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--scratch-parent", type=Path)
    parser.add_argument("--audit-timeout-seconds", type=int, default=1200)
    parser.add_argument("--minimum-available-mib", type=int, default=3072)
    parser.add_argument("--minimum-disk-mib", type=int, default=1024)
    parser.add_argument(
        "--maximum-one-minute-load",
        type=float,
        help=(
            "full-mode ceiling; defaults to 75%% of detected logical CPUs "
            "and must remain below the logical CPU count"
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = build_parser().parse_args(argv)
    mode = arguments.mode
    try:
        root = arguments.campaign_root.resolve(strict=True)
        metadata = verify_metadata(root)
        if mode == "fast":
            result = metadata.report
        else:
            maximum_load = (
                default_maximum_one_minute_load()
                if arguments.maximum_one_minute_load is None
                else arguments.maximum_one_minute_load
            )
            result = run_full_replay(
                root,
                metadata,
                timeout_seconds=arguments.audit_timeout_seconds,
                minimum_available_mib=arguments.minimum_available_mib,
                minimum_disk_mib=arguments.minimum_disk_mib,
                maximum_one_minute_load=maximum_load,
                scratch_parent=arguments.scratch_parent,
            )
        payload = canonical_json_bytes(result)
        if arguments.output is None:
            sys.stdout.buffer.write(payload)
        else:
            write_new_file(arguments.output, payload)
        return 0
    except (
        ReplayFailure,
        OSError,
        subprocess.SubprocessError,
        UnicodeError,
        ValueError,
    ) as error:
        failure = canonical_json_bytes(
            {
                "claim_status": "NO_MATHEMATICAL_CLAIM",
                "error": f"{type(error).__name__}: {error}",
                "mode": mode,
                "proofs_freshly_replayed": False,
                "schema": SCHEMA,
                "status": "REJECT",
            }
        )
        sys.stderr.buffer.write(failure)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
