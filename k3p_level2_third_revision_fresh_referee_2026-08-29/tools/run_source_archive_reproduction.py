#!/usr/bin/env python3
"""Run each sealed PDF source-reproduction command once under Seatbelt."""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import time


AUDIT = Path(__file__).resolve().parents[1]
EXECUTION = AUDIT / "execution/source_archive_reproduction_738b"
REPOSITORY = AUDIT / "execution/release_engineering_738b/repo"
PROJECT = REPOSITORY / "k3p_level2_identifiability_final"
PACKAGE = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_third_revision_referee_final_2026-08-29/proof_package"
)
PROFILE = AUDIT / "logs/source_archive_reproduction_738b.sb"
PYTHON = Path(
    "/Users/alec/Documents/Math/"
    "k3p_level2_identifiability_final/.venv/bin/python"
)
TECTONIC = Path("/opt/homebrew/bin/tectonic")
SOURCE_CACHE = Path("/Users/alec/Library/Caches/Tectonic")
SCRIPT = PROJECT / "release/verify_source_reproduction.py"
WORK = PROJECT / "release/work/source_archive_referee"
ATTEMPT = EXECUTION / "ATTEMPT_STARTED.json"
SUPPLEMENT_ATTEMPT = EXECUTION / "SUPPLEMENT_ATTEMPT_STARTED.json"
SUMMARY = EXECUTION / "SUMMARY.json"
EXPECTED_COMMIT = "738b662aa9c4e6201277f60b249afd4de9bcd9d6"
EXPECTED_TECTONIC = "38eff9059ed622672c9a2590415a8f01c043df4232baa459628a2cd86e512d95"
EXPECTED_BUNDLE = "6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c"
EXPECTED = {
    "article": {
        "archive": "k3p_level2_article_source.zip",
        "archive_sha256": "683285f7ef3271349a996df93ee96e7e29cb44d17543e7871071e00fc4e6a366",
        "pdf": "output/pdf/K3P_Level2_Identifiability_Article.pdf",
        "pdf_sha256": "5fd4fb902ee72c619c75846e2e5f561b018b4096a659b895063c0758dfc5d9df",
        "source_member_count": 23,
        "source_payload_sha256": "78c6ae8ddb0a7d1abbd2b3d81a4637b120a5135e77abb53f657cbb87af2fb9ea",
        "archive_member_count": 25,
        "manifest_payload_sha256": "824cd6a71f0b2d3f1a48f2ed7c1547bf4e5ddc8d97870f9a1b38f197d5a5d5dd",
    },
    "supplement": {
        "archive": "k3p_level2_supplement_source.zip",
        "archive_sha256": "4d235bcafd73017c5a02e9ba8b1c3b9eaba920ff09d02db3bc27da24146b7406",
        "pdf": "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf",
        "pdf_sha256": "e82d1afb01f937872ec06ee1b1529fe736362c3496721b99813d8849ff7327e6",
        "source_member_count": 1,
        "source_payload_sha256": "64480ff653200c335dd71cb12a406648d478f8f1cbb689e53320e9a08833e4de",
        "archive_member_count": 3,
        "manifest_payload_sha256": "1ead4afe3e7522beada82a5a626eeef2dae2c9c3c63d64bfa8142f74da87fdb3",
    },
}


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def exclusive_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write((json.dumps(value, indent=2, sort_keys=True) + "\n").encode())
        handle.flush()
        os.fsync(handle.fileno())


def exclusive_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(value)
        handle.flush()
        os.fsync(handle.fileno())


def inventory(root: Path) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        metadata = path.lstat()
        row: dict[str, object] = {
            "path": path.relative_to(root).as_posix(),
            "mode": format(stat.S_IMODE(metadata.st_mode), "04o"),
        }
        if path.is_symlink():
            row.update({"type": "symlink", "target": os.readlink(path)})
        elif path.is_dir():
            row["type"] = "directory"
        elif path.is_file():
            row.update({
                "type": "file", "bytes": metadata.st_size,
                "sha256": sha256_file(path),
            })
        else:
            raise AuditFailure(("unexpected cache object", str(path)))
        rows.append(row)
    encoded = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return {
        "entry_count": len(rows),
        "file_count": sum(row["type"] == "file" for row in rows),
        "bytes": sum(int(row.get("bytes", 0)) for row in rows),
        "inventory_sha256": sha256_bytes(encoded),
    }


def environment() -> dict[str, str]:
    home = EXECUTION / "runtime_home"
    temporary = EXECUTION / "runtime_tmp"
    return {
        "PATH": "/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin",
        "HOME": str(home), "TMPDIR": str(temporary),
        "LC_ALL": "C", "LANG": "C", "TZ": "UTC",
        "SOURCE_DATE_EPOCH": "1787677101",
        "PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0", "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/usr/bin/false", "SSH_ASKPASS": "/usr/bin/false",
        "GIT_CEILING_DIRECTORIES": str(AUDIT / "execution/release_engineering_738b"),
        "__CF_USER_TEXT_ENCODING": "0x1F5:0:0",
    }


def git(arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["/opt/homebrew/bin/git", "-C", str(REPOSITORY), *arguments],
        env=environment(), text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False, timeout=120,
    )


def terminate(process: subprocess.Popen[bytes]) -> None:
    for current_signal, wait in ((signal.SIGTERM, 5), (signal.SIGKILL, 5)):
        try:
            os.killpg(process.pid, current_signal)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=wait)
            return
        except subprocess.TimeoutExpired:
            continue
    raise AuditFailure(("could not terminate source reproduction", process.pid))


def parse_console(output: bytes) -> dict:
    sentinel = b"K3P_SOURCE_REPRODUCTION_PASS\n"
    require(output.endswith(sentinel) and output.count(sentinel) == 1,
            "source reproduction sentinel")
    lines = output[:-len(sentinel)].decode("utf-8").strip().splitlines()
    require(len(lines) == 1, ("unexpected source reproduction console", lines))
    value = json.loads(lines[0])
    require(isinstance(value, dict), "source reproduction console object")
    return value


def logical_payload(report: dict) -> str:
    logical = dict(report)
    logical["builds"] = [
        {key: row[key] for key in ("run", "sha256", "bytes")}
        for row in report["builds"]
    ]
    logical.pop("tool_versions", None)
    logical.pop("logical_payload_sha256", None)
    return sha256_bytes(json.dumps(
        logical, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii"))


def validate_report(kind: str, report: dict, console: dict) -> dict[str, object]:
    expected = EXPECTED[kind]
    require(report.get("schema") == "k3p-pdf-source-reproduction-v1" and
            report.get("status") == "PASS_BYTE_FOR_BYTE" and
            report.get("kind") == kind and
            report.get("source_commit") == EXPECTED_COMMIT,
            ("source report identity", kind))
    archive = report.get("source_archive", {})
    structural = archive.get("structural_verification", {})
    require(archive.get("sha256") == expected["archive_sha256"] and
            structural.get("source_commit") == EXPECTED_COMMIT and
            structural.get("sha256") == expected["archive_sha256"] and
            structural.get("member_count") == expected["archive_member_count"] and
            structural.get("manifest_payload_sha256") ==
            expected["manifest_payload_sha256"],
            ("source archive report binding", kind))
    pdf = report.get("expected_pdf", {})
    require(pdf.get("sha256") == expected["pdf_sha256"] and
            isinstance(pdf.get("bytes"), int) and pdf["bytes"] > 0,
            ("expected PDF report binding", kind))
    binding = report.get("committed_source_binding", {})
    require(binding.get("member_count") == expected["source_member_count"] and
            binding.get("payload_sha256") == expected["source_payload_sha256"],
            ("committed source binding", kind))
    builds = report.get("builds")
    require(isinstance(builds, list) and len(builds) == 2 and
            [row.get("run") for row in builds] == [1, 2] and
            all(row.get("sha256") == expected["pdf_sha256"] and
                row.get("bytes") == pdf["bytes"] and
                isinstance(row.get("elapsed_seconds"), (int, float)) and
                row["elapsed_seconds"] >= 0 for row in builds),
            ("two byte-identical PDF builds", kind))
    for row in builds:
        transcript = PROJECT / row["transcript"]
        require(transcript.is_file() and
                sha256_file(transcript) == row["transcript_sha256"],
                ("source build transcript", kind, row["run"]))
    tool = report.get("tool_versions", {}).get("tectonic", {})
    require(tool.get("sha256") == EXPECTED_TECTONIC and
            tool.get("version") == "Tectonic 0.16.9",
            ("source report Tectonic binding", kind))
    observed_logical = logical_payload(report)
    require(report.get("logical_payload_sha256") == observed_logical,
            ("source report logical payload", kind))
    require(console.get("status") == "PASS_BYTE_FOR_BYTE" and
            console.get("kind") == kind and
            console.get("pdf_sha256") == expected["pdf_sha256"] and
            console.get("logical_payload_sha256") == observed_logical,
            ("source reproduction console/report mismatch", kind))
    return {
        "status": "PASS_BYTE_FOR_BYTE",
        "source_archive_sha256": expected["archive_sha256"],
        "pdf_sha256": expected["pdf_sha256"],
        "pdf_bytes": pdf["bytes"],
        "logical_payload_sha256": observed_logical,
        "builds": [
            {"run": row["run"], "sha256": row["sha256"],
             "bytes": row["bytes"], "elapsed_seconds": row["elapsed_seconds"],
             "transcript_sha256": row["transcript_sha256"]}
            for row in builds
        ],
    }


def run_kind(kind: str) -> dict[str, object]:
    expected = EXPECTED[kind]
    input_path = WORK / "inputs" / expected["archive"]
    report_path = WORK / "reports" / f"{kind}.json"
    outer_transcript = AUDIT / "logs" / f"source_archive_{kind}_738b.log"
    require(not report_path.exists() and not outer_transcript.exists(),
            ("refusing source reproduction evidence overwrite", kind))
    command = [
        "/usr/bin/sandbox-exec", "-f", str(PROFILE), str(PYTHON), str(SCRIPT),
        "--kind", kind,
        "--source-archive", str(input_path),
        "--expected-pdf", str(PROJECT / expected["pdf"]),
        "--tectonic", str(TECTONIC),
        "--report", str(report_path),
    ]
    started_utc = dt.datetime.now(dt.timezone.utc).isoformat()
    started = time.monotonic()
    process = subprocess.Popen(
        command, cwd=PROJECT, env=environment(), stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, start_new_session=True,
    )
    try:
        output, _ = process.communicate(timeout=1_200)
    except subprocess.TimeoutExpired as error:
        terminate(process)
        raise AuditFailure(("source reproduction outer timeout", kind)) from error
    elapsed = time.monotonic() - started
    exclusive_bytes(outer_transcript, output)
    require(process.returncode == 0,
            ("source reproduction return code", kind, process.returncode,
             output[-4000:]))
    console = parse_console(output)
    require(report_path.is_file(), ("missing source reproduction report", kind))
    report = json.loads(report_path.read_text(encoding="utf-8"))
    validated = validate_report(kind, report, console)
    return {
        **validated,
        "command_invocations": 1,
        "package_internal_build_count": 2,
        "started_utc": started_utc,
        "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "outer_elapsed_seconds": elapsed,
        "outer_transcript": {
            "path": str(outer_transcript), "bytes": len(output),
            "sha256": sha256_file(outer_transcript),
        },
        "package_report": {
            "path": str(report_path), "bytes": report_path.stat().st_size,
            "sha256": sha256_file(report_path),
        },
    }


def prepare() -> tuple[dict[str, object], dict[str, object]]:
    require(PROFILE.is_file() and SCRIPT.is_file() and PYTHON.is_file(),
            "source reproduction prerequisites")
    require(not (REPOSITORY / ".git/objects/info/alternates").exists(),
            "exact checkout uses alternates")
    require(not any((REPOSITORY / ".git/objects/pack").glob("*.promisor")),
            "exact checkout uses a promisor pack")
    head = git(["rev-parse", "HEAD"])
    status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    require(head.returncode == 0 and head.stdout.strip() == EXPECTED_COMMIT,
            "source reproduction exact checkout commit")
    require(status.returncode == 0 and status.stdout == "",
            ("source reproduction checkout is not clean", status.stdout))
    require(TECTONIC.resolve().is_file() and sha256_file(TECTONIC.resolve()) ==
            EXPECTED_TECTONIC, "pinned Tectonic executable")
    version = subprocess.run(
        [str(TECTONIC), "--version"], env=environment(), text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60, check=False,
    )
    require(version.returncode == 0 and version.stdout.strip() == "Tectonic 0.16.9",
            ("pinned Tectonic version", version.stdout))
    home = EXECUTION / "runtime_home"
    temporary = EXECUTION / "runtime_tmp"
    home.mkdir(parents=True, exist_ok=True)
    temporary.mkdir(parents=True, exist_ok=True)
    target_cache = home / "Library/Caches/Tectonic"
    require(not target_cache.exists(), "refusing to replace Tectonic cache copy")
    shutil.copytree(SOURCE_CACHE, target_cache, symlinks=True,
                    copy_function=shutil.copy2)
    hashes = target_cache / "bundles/hashes"
    hash_values = {path.read_text(encoding="utf-8").strip()
                   for path in hashes.iterdir() if path.is_file()}
    require(hash_values == {EXPECTED_BUNDLE}, ("Tectonic bundle cache identity", hash_values))
    cache_before = inventory(target_cache)
    input_root = WORK / "inputs"
    input_root.mkdir(parents=True, exist_ok=True)
    for expected in EXPECTED.values():
        source = PACKAGE / "source_archives" / expected["archive"]
        target = input_root / expected["archive"]
        require(source.is_file() and sha256_file(source) == expected["archive_sha256"],
                ("delivered source archive identity", source.name))
        require(not target.exists(), ("refusing source archive overwrite", target.name))
        shutil.copy2(source, target)
        require(sha256_file(target) == expected["archive_sha256"],
                ("copied source archive identity", target.name))
    return cache_before, {
        "tectonic_path": str(TECTONIC.resolve()),
        "tectonic_sha256": EXPECTED_TECTONIC,
        "tectonic_version": version.stdout.strip(),
        "bundle_payload_sha256": EXPECTED_BUNDLE,
    }


def main() -> int:
    if ATTEMPT.exists():
        return resume_supplement_after_article_failure()
    require(not ATTEMPT.exists() and not SUMMARY.exists(),
            "source reproduction has already been attempted; never relaunch")
    cache_before, toolchain = prepare()
    exclusive_json(ATTEMPT, {
        "schema": "k3p-source-archive-referee-attempt-v1",
        "source_commit": EXPECTED_COMMIT,
        "commands": ["article", "supplement"],
        "at_most_once": True,
        "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    })
    started = time.monotonic()
    results = {kind: run_kind(kind) for kind in ("article", "supplement")}
    target_cache = EXECUTION / "runtime_home/Library/Caches/Tectonic"
    cache_after = inventory(target_cache)
    require(cache_after == cache_before,
            ("Tectonic cache byte/path/mode drift", cache_before, cache_after))
    status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    require(status.returncode == 0 and status.stdout == "",
            ("source reproduction checkout drift", status.stdout))
    summary = {
        "schema": "k3p-third-revision-source-archive-reproduction-v1",
        "status": "PASS_BYTE_FOR_BYTE",
        "source_commit": EXPECTED_COMMIT,
        "checkout_clean_before_and_after": True,
        "network": "DENIED_BY_SEATBELT",
        "environment_allowlist": sorted(environment()),
        "toolchain": toolchain,
        "tectonic_cache_before": cache_before,
        "tectonic_cache_after": cache_after,
        "tectonic_cache_unchanged": True,
        "commands": results,
        "command_invocations": 2,
        "package_internal_builds": 4,
        "elapsed_seconds": time.monotonic() - started,
        "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "sandbox_profile": {
            "path": str(PROFILE), "sha256": sha256_file(PROFILE),
        },
    }
    exclusive_json(SUMMARY, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


def resume_supplement_after_article_failure() -> int:
    """Run only the never-started supplement after preserving article failure."""
    article_log = AUDIT / "logs/source_archive_article_738b.log"
    article_report = WORK / "reports/article.json"
    supplement_log = AUDIT / "logs/source_archive_supplement_738b.log"
    supplement_report = WORK / "reports/supplement.json"
    require(not SUMMARY.exists() and not SUPPLEMENT_ATTEMPT.exists(),
            "supplement source reproduction has already been attempted; never relaunch")
    require(article_log.is_file() and not article_report.exists() and
            b"K3P_SOURCE_REPRODUCTION_FAIL" in article_log.read_bytes(),
            "article failure evidence required before supplement-only continuation")
    require(not supplement_log.exists() and not supplement_report.exists(),
            "supplement command has already started")
    target_cache = EXECUTION / "runtime_home/Library/Caches/Tectonic"
    cache_before = inventory(target_cache)
    require(cache_before == {
        "entry_count": 730,
        "file_count": 725,
        "bytes": 57_507_581,
        "inventory_sha256":
            "e9612d0f190a5078122514e8df625e04d0904cdbe5041a368e068800303e4de7",
    }, ("copied Tectonic cache drift before supplement", cache_before))
    status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    require(status.returncode == 0 and status.stdout == "",
            ("source reproduction checkout drift before supplement", status.stdout))
    exclusive_json(SUPPLEMENT_ATTEMPT, {
        "schema": "k3p-source-archive-referee-supplement-attempt-v1",
        "source_commit": EXPECTED_COMMIT,
        "command": "supplement",
        "at_most_once": True,
        "article_command_relaunch": False,
        "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    })
    started = time.monotonic()
    supplement = run_kind("supplement")
    cache_after = inventory(target_cache)
    require(cache_after == cache_before,
            ("Tectonic cache byte/path/mode drift", cache_before, cache_after))
    final_status = git(["status", "--porcelain=v1", "--untracked-files=all"])
    require(final_status.returncode == 0 and final_status.stdout == "",
            ("source reproduction checkout drift after supplement", final_status.stdout))
    current_profile = PROFILE.read_bytes()
    mach_rule = (
        b'(allow mach-lookup\n'
        b'  (global-name "com.apple.SystemConfiguration.configd"))\n'
    )
    require(current_profile.count(mach_rule) == 1,
            "narrow SystemConfiguration rule identity")
    article_profile = current_profile.replace(mach_rule, b"")
    summary = {
        "schema": "k3p-third-revision-source-archive-reproduction-v1",
        "status": "PARTIAL_ARTICLE_SANDBOX_FAILURE_SUPPLEMENT_PASS",
        "source_commit": EXPECTED_COMMIT,
        "checkout_clean_before_and_after": True,
        "network": "DENIED_BY_SEATBELT",
        "toolchain": {
            "tectonic_path": str(TECTONIC.resolve()),
            "tectonic_sha256": EXPECTED_TECTONIC,
            "tectonic_version": "Tectonic 0.16.9",
            "bundle_payload_sha256": EXPECTED_BUNDLE,
        },
        "tectonic_cache_before": cache_before,
        "tectonic_cache_after": cache_after,
        "tectonic_cache_unchanged": True,
        "commands": {
            "article": {
                "status": "FAIL_SANDBOX_SYSTEMCONFIGURATION",
                "command_invocations": 1,
                "completed_builds": 0,
                "relaunch_performed": False,
                "outer_transcript": {
                    "path": str(article_log),
                    "bytes": article_log.stat().st_size,
                    "sha256": sha256_file(article_log),
                },
                "sandbox_profile_sha256": sha256_bytes(article_profile),
            },
            "supplement": supplement,
        },
        "command_invocations": 2,
        "package_internal_completed_builds": 2,
        "article_relaunch_performed": False,
        "elapsed_seconds_supplement_continuation": time.monotonic() - started,
        "finished_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "supplement_sandbox_profile": {
            "path": str(PROFILE), "sha256": sha256_bytes(current_profile),
            "narrow_mach_service": "com.apple.SystemConfiguration.configd",
        },
    }
    exclusive_json(SUMMARY, summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
