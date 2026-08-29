#!/usr/bin/env python3
"""Run and independently bind the excluded release-engineering mutations."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


AUDIT = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_second_revision_referee_2026-08-28"
)
EXECUTION = AUDIT / "execution/release_engineering_5a6d"
REPOSITORY = EXECUTION / "repo"
PROJECT = REPOSITORY / "k3p_level2_identifiability_final"
PROFILE = AUDIT / "logs/release_engineering_5a6d.sb"
TRANSCRIPT = AUDIT / "logs/release_engineering_5a6d_transcript.log"
SUMMARY = AUDIT / "logs/release_engineering_5a6d_summary.json"
PYTHON = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_identifiability_final/.venv/bin/python"
)
SCRIPT = PROJECT / "reproducibility/test_release_engineering_mutations.py"
SOURCE_REPOSITORY = Path("/Users/alec/Documents/Math")
EXPECTED_COMMIT = "5a6d64cb2a76e890d7baaef3ba5ac9861c1d029f"
EXPECTED_PAYLOAD_SHA256 = "fd931f0df94ae456baff232dbc713c70233ee9f15fcf3debb35c8617b06a0d16"
EXPECTED_PRETTY_REPORT_SHA256 = "3e45c348d4fa276cdd0fb4f41d2d6ad087a8ea3f664ae88472a33995fa89e31e"
EXPECTED_MUTATIONS = {
    "stale_checksum",
    "stale_archive_member_hash",
    "self_referential_archive_hash",
    "self_referential_checksum_list",
    "path_traversal_primitive",
    "path_traversal_zip",
    "noncanonical_zip_timestamp",
    "noncanonical_tar_mode",
    "optimized_input_gate",
    "optimized_archive_builder",
    "forbidden_active_evidence",
    "missing_active_evidence_path",
    "wrong_source_build_engine",
    "fake_tectonic_executable",
    "wrong_pdf_source_date_epoch",
    "inconsistent_source_build_environment",
    "pdf_equivalent_source_archive_tamper",
    "malformed_fileset_policy",
    "wrong_fileset_selection_lock",
    "not_ready_submission_report",
    "arbitrary_submission_files",
    "mislabeled_submission_archive",
    "malicious_submission_extra",
    "enforced_command_timeout",
    "enforced_descendant_timeout",
    "forged_suite_command_plan",
    "unknown_release_envelope_field",
    "tampered_generated_readme",
    "tampered_archive_sidecar",
    "dirty_final_verification",
    "forged_source_reproduction_builds",
    "certified_manifest_input_drift",
}


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def clean_environment() -> dict[str, str]:
    home = EXECUTION / "runtime_home"
    temporary = EXECUTION / "runtime_tmp"
    home.mkdir(parents=True, exist_ok=True)
    temporary.mkdir(parents=True, exist_ok=True)
    return {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "LC_ALL": "C",
        "LANG": "C",
        "TZ": "UTC",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "HOME": str(home),
        "TMPDIR": str(temporary),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/usr/bin/false",
        "SSH_ASKPASS": "/usr/bin/false",
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
    }


def git(repository: Path, arguments: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    environment = clean_environment()
    return subprocess.run(
        ["/opt/homebrew/bin/git", "-C", str(repository), *arguments],
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
        timeout=120,
    )


def repository_state(repository: Path, *, scoped_path: str | None = None) -> dict[str, object]:
    head = git(repository, ["rev-parse", "HEAD"]).stdout.strip()
    status_arguments = ["status", "--porcelain=v1", "--untracked-files=all"]
    if scoped_path is not None:
        status_arguments.extend(["--", scoped_path])
    status = git(repository, status_arguments).stdout
    symbolic = git(repository, ["symbolic-ref", "-q", "HEAD"], check=False)
    return {
        "head": head,
        "status": status,
        "status_sha256": hashlib.sha256(status.encode()).hexdigest(),
        "detached": symbolic.returncode == 1,
        "symbolic_stdout": symbolic.stdout,
        "symbolic_stderr": symbolic.stderr,
    }


def process_table() -> dict[int, list[int]]:
    completed = subprocess.run(
        ["/bin/ps", "-axo", "pid=,ppid="],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
    )
    children: dict[int, list[int]] = {}
    for line in completed.stdout.splitlines():
        pid_text, parent_text = line.split()
        children.setdefault(int(parent_text), []).append(int(pid_text))
    return children


def descendants(root_pid: int) -> list[int]:
    table = process_table()
    result: list[int] = []

    def visit(pid: int) -> None:
        for child in table.get(pid, []):
            visit(child)
            result.append(child)

    visit(root_pid)
    return result


def terminate_tree(root_pid: int) -> None:
    targets = descendants(root_pid) + [root_pid]
    for sig, pause in ((signal.SIGTERM, 0.5), (signal.SIGKILL, 0.0)):
        for pid in targets:
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                pass
        if pause:
            time.sleep(pause)


def parse_report(transcript: str) -> dict:
    sentinel = "K3P_RELEASE_ENGINEERING_MUTATIONS_PASS"
    require(transcript.count(sentinel) == 1, "release mutation PASS sentinel count")
    prefix, suffix = transcript.split(sentinel)
    require(not suffix.strip(), "unexpected output after release mutation sentinel")
    start = prefix.find("{")
    require(start >= 0, "release mutation JSON report missing")
    report = json.loads(prefix[start:].strip())
    require(isinstance(report, dict), "release mutation report object")
    return report


def verify_report(report: dict) -> dict[str, object]:
    require(report.get("schema") == "k3p-release-engineering-mutations-v1", "report schema")
    require(
        report.get("status") == "PASS"
        and report.get("mutation_count") == 32
        and report.get("rejected") == 32
        and report.get("survived") == 0,
        "release mutation summary",
    )
    rows = report.get("mutations")
    require(isinstance(rows, list) and len(rows) == 32, "release mutation rows")
    names = {row.get("name") for row in rows if isinstance(row, dict)}
    require(names == EXPECTED_MUTATIONS, ("release mutation name set", sorted(names)))
    require(all(row.get("status") == "REJECTED" for row in rows), "mutation survived")
    controls = report.get("controls")
    require(isinstance(controls, list) and len(controls) == 10, "release controls")
    require(
        all(row.get("status") in {"PASS", "PASS_IDENTICAL"} for row in controls),
        "release control failure",
    )
    claimed = report.get("payload_sha256")
    logical = dict(report)
    logical.pop("payload_sha256", None)
    observed = hashlib.sha256(
        json.dumps(
            logical, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("ascii")
    ).hexdigest()
    require(claimed == observed, "release mutation payload hash")
    require(observed == EXPECTED_PAYLOAD_SHA256, "fresh/stored release mutation payload")
    pretty_sha256 = hashlib.sha256(
        (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest()
    require(pretty_sha256 == EXPECTED_PRETTY_REPORT_SHA256,
            "fresh/stored release mutation report bytes")
    return {
        "status": report["status"],
        "mutation_count": report["mutation_count"],
        "rejected": report["rejected"],
        "survived": report["survived"],
        "mutation_names": sorted(names),
        "controls": controls,
        "payload_sha256": observed,
        "pretty_report_sha256": pretty_sha256,
    }


def exclusive_json(path: Path, value: dict) -> None:
    encoded = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(encoded)
        handle.flush()
        os.fsync(handle.fileno())


def main() -> int:
    started_wall = dt.datetime.now(dt.timezone.utc).isoformat()
    started = time.monotonic()
    process: subprocess.Popen[bytes] | None = None
    try:
        require(PROFILE.is_file() and PYTHON.is_file() and SCRIPT.is_file(), "audit inputs missing")
        require(not TRANSCRIPT.exists() and not SUMMARY.exists(), "refusing to overwrite audit evidence")
        before = repository_state(REPOSITORY)
        source_before = repository_state(
            SOURCE_REPOSITORY, scoped_path="k3p_level2_identifiability_final"
        )
        require(before["head"] == EXPECTED_COMMIT, "detached checkout commit")
        require(before["status"] == "" and before["detached"] is True, "checkout is not clean detached")
        require(source_before["status"] == "", "source project is not clean")

        command = [
            "/usr/bin/sandbox-exec",
            "-f",
            str(PROFILE),
            str(PYTHON),
            str(SCRIPT),
            "--no-write-report",
        ]
        descriptor = os.open(
            TRANSCRIPT, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
        )
        with os.fdopen(descriptor, "wb") as transcript:
            process = subprocess.Popen(
                command,
                cwd=PROJECT,
                env=clean_environment(),
                stdout=transcript,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                returncode = process.wait(timeout=600)
            except subprocess.TimeoutExpired as error:
                terminate_tree(process.pid)
                process.wait()
                raise AuditFailure("release mutation suite timed out") from error
            transcript.flush()
            os.fsync(transcript.fileno())
        require(returncode == 0, ("release mutation exit", returncode))

        transcript_text = TRANSCRIPT.read_text(encoding="utf-8")
        report_summary = verify_report(parse_report(transcript_text))
        after = repository_state(REPOSITORY)
        source_after = repository_state(
            SOURCE_REPOSITORY, scoped_path="k3p_level2_identifiability_final"
        )
        require(after == before, ("detached checkout drift", before, after))
        require(source_after == source_before, ("source repository drift", source_before, source_after))

        release_work = PROJECT / "release/work"
        runtime_paths = sorted(
            path.relative_to(PROJECT).as_posix()
            for path in release_work.rglob("*")
        ) if release_work.exists() else []
        summary = {
            "schema": "k3p-independent-release-mutation-replay-v1",
            "status": "PASS",
            "started_utc": started_wall,
            "elapsed_seconds": time.monotonic() - started,
            "expected_commit": EXPECTED_COMMIT,
            "checkout_before": before,
            "checkout_after": after,
            "source_project_before": source_before,
            "source_project_after": source_after,
            "command": command,
            "environment": clean_environment(),
            "bindings": {
                "supervisor_sha256": sha256_file(Path(__file__).resolve()),
                "sandbox_profile_sha256": sha256_file(PROFILE),
                "mutation_driver_sha256": sha256_file(SCRIPT),
                "python_executable": str(PYTHON),
                "python_executable_sha256": sha256_file(Path(os.path.realpath(PYTHON))),
                "git_version": git(REPOSITORY, ["--version"]).stdout.strip(),
            },
            "transcript": {
                "path": str(TRANSCRIPT),
                "bytes": TRANSCRIPT.stat().st_size,
                "sha256": sha256_file(TRANSCRIPT),
            },
            "release_work_runtime_paths": runtime_paths,
            "report": report_summary,
        }
        exclusive_json(SUMMARY, summary)
        print(json.dumps(summary, sort_keys=True))
        print("K3P_INDEPENDENT_RELEASE_MUTATION_REPLAY_PASS")
        return 0
    except KeyboardInterrupt:
        if process is not None and process.poll() is None:
            terminate_tree(process.pid)
        return 130
    except (AuditFailure, OSError, UnicodeError, ValueError, json.JSONDecodeError,
            subprocess.SubprocessError) as error:
        print(f"K3P_INDEPENDENT_RELEASE_MUTATION_REPLAY_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
