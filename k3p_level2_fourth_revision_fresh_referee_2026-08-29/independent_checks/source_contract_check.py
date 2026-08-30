#!/usr/bin/env python3
"""Independent checks for the fourth-revision PDF/source contract.

This audit utility intentionally imports no code from the reviewed package.
It reads the canonical source ZIPs, the named Git commit, the Tectonic cache
inventory, the outer referee-package seal, and optional fresh build reports.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import zipfile
import zlib


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")


def git_bytes(repo: Path, spec: str) -> bytes:
    return subprocess.run(
        ["git", "show", spec], cwd=repo, check=True, capture_output=True
    ).stdout


def git_paths(repo: Path, commit: str, prefix: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", commit, "--", prefix],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def source_pairs(repo: Path, commit: str, project_prefix: str,
                 kind: str) -> list[tuple[str, str]]:
    if kind == "supplement":
        return [(
            f"{project_prefix}/supplement/reader_supplement.tex",
            "reader_supplement.tex",
        )]
    prefix = f"{project_prefix}/manuscript/"
    selected = []
    for path in git_paths(repo, commit, prefix):
        if path in (prefix + "main.tex", prefix + "references.bib") or \
                path.startswith(prefix + "sections/") or \
                path.startswith(prefix + "figures/"):
            selected.append((path, path.removeprefix(prefix)))
    return sorted(selected)


def check_source_zip(path: Path, *, repo: Path, commit: str,
                     project_prefix: str, kind: str) -> dict:
    raw = path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        assert names == sorted(names) and len(names) == len(set(names))
        assert archive.testzip() is None
        root = names[0].split("/", 1)[0]
        payload = {
            name.removeprefix(root + "/"): archive.read(name) for name in names
        }
        manifest = json.loads(payload["ARCHIVE_MANIFEST.json"])
        body = dict(manifest)
        claimed_payload = body.pop("payload_sha256")
        assert digest(canonical_json(body)) == claimed_payload
        assert manifest["source_commit"] == commit
        rows = {row["path"]: row for row in manifest["members"]}
        observed = set(payload) - {"ARCHIVE_MANIFEST.json"}
        assert observed == set(rows)
        expected_time = (2026, 8, 29, 22, 59, 0)
        for info in infos:
            relative = info.filename.removeprefix(root + "/")
            assert info.date_time == expected_time
            assert info.create_system == 3
            assert (info.external_attr >> 16) & 0o7777 == 0o644
            assert info.extra == b"" and info.comment == b""
            if relative != "ARCHIVE_MANIFEST.json":
                data = payload[relative]
                assert rows[relative] == {
                    "path": relative,
                    "bytes": len(data),
                    "sha256": digest(data),
                    "mode": "0644",
                }

        pairs = source_pairs(repo, commit, project_prefix, kind)
        metadata = {
            "ARCHIVE_MANIFEST.json", "SOURCE_BUILD.json",
            "TECTONIC_CACHE_MANIFEST.json",
        }
        assert set(payload) - metadata == {relative for _, relative in pairs}
        mismatches = []
        for git_path, relative in pairs:
            if payload[relative] != git_bytes(repo, f"{commit}:{git_path}"):
                mismatches.append(relative)
        assert not mismatches
        committed_payload = digest(canonical_json({
            relative: digest(payload[relative]) for _, relative in pairs
        }))

        rebuilt = io.BytesIO()
        with zipfile.ZipFile(
            rebuilt, "w", compression=zipfile.ZIP_DEFLATED,
            compresslevel=9, strict_timestamps=True,
        ) as output:
            for name in sorted(names):
                relative = name.removeprefix(root + "/")
                info = zipfile.ZipInfo(name, date_time=expected_time)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.flag_bits = 0x800
                output.writestr(
                    info, payload[relative], compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )
        assert rebuilt.getvalue() == raw
        return {
            "kind": kind,
            "source_members": len(pairs),
            "archive_members": len(names),
            "source_mismatches": mismatches,
            "committed_source_payload_sha256": committed_payload,
            "manifest_payload_sha256": claimed_payload,
            "archive_sha256": digest(raw),
            "byte_identical_reconstruction": True,
            "cache_manifest_sha256": digest(
                payload["TECTONIC_CACHE_MANIFEST.json"]
            ),
        }


def check_cache(manifest_path: Path, cache_root: Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    body = dict(manifest)
    claim = body.pop("payload_sha256")
    assert digest(canonical_json(body)) == claim
    assert manifest["file_count"] == len(manifest["files"])
    assert manifest["total_bytes"] == sum(
        row["bytes"] for row in manifest["files"]
    )
    observed = {}
    for path in cache_root.rglob("*"):
        if path.is_file():
            assert not path.is_symlink()
            data = path.read_bytes()
            observed[path.relative_to(cache_root).as_posix()] = (
                len(data), digest(data)
            )
    expected = {
        row["path"]: (row["bytes"], row["sha256"])
        for row in manifest["files"]
    }
    missing = sorted(set(expected) - set(observed))
    extra = sorted(set(observed) - set(expected))
    mismatched = sorted(
        path for path in set(expected) & set(observed)
        if expected[path] != observed[path]
    )
    assert not missing and not extra and not mismatched
    return {
        "manifest_sha256": digest(manifest_path.read_bytes()),
        "payload_sha256": claim,
        "file_count": len(observed),
        "total_bytes": sum(size for size, _ in observed.values()),
        "missing": missing,
        "extra": extra,
        "mismatched": mismatched,
    }


def logical_report_hash(report: dict) -> str:
    logical = dict(report)
    logical.pop("logical_payload_sha256")
    logical["builds"] = [
        {key: row[key] for key in ("run", "sha256", "bytes")}
        for row in logical["builds"]
    ]
    logical.pop("tool_versions")
    return digest(canonical_json(logical))


def check_report(package: Path, outer_seal: dict[str, tuple[int, str, str]],
                 kind: str, fresh_root: Path | None) -> dict:
    base = package / "proof_package/release/source_reproduction_evidence"
    path = base / f"{kind}.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    assert logical_report_hash(report) == report["logical_payload_sha256"]
    transcript_checks = []
    for row in report["builds"]:
        transcript = package / "proof_package" / row["transcript"]
        actual = digest(transcript.read_bytes())
        assert actual == row["transcript_sha256"]
        transcript_checks.append(actual)
    relative = f"proof_package/release/source_reproduction_evidence/{kind}.json"
    assert outer_seal[relative] == (
        path.stat().st_size, digest(path.read_bytes()), "0644"
    )
    result = {
        "kind": kind,
        "source_commit": report["source_commit"],
        "logical_payload_sha256": report["logical_payload_sha256"],
        "report_sha256": digest(path.read_bytes()),
        "transcript_sha256": transcript_checks,
        "outer_seal_match": True,
    }
    if fresh_root is not None:
        fresh = json.loads((fresh_root / f"{kind}.json").read_text(encoding="utf-8"))
        assert logical_report_hash(fresh) == fresh["logical_payload_sha256"]
        assert fresh["logical_payload_sha256"] == report["logical_payload_sha256"]
        result["fresh_logical_payload_match"] = True
        result["fresh_builds"] = [
            {
                "run": row["run"], "sha256": row["sha256"],
                "bytes": row["bytes"], "elapsed_seconds": row["elapsed_seconds"],
                "transcript_sha256": row["transcript_sha256"],
            }
            for row in fresh["builds"]
        ]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--cache-root", type=Path, required=True)
    parser.add_argument("--fresh-reports", type=Path)
    args = parser.parse_args()

    package = args.package.resolve()
    package_manifest = json.loads(
        (package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8")
    )
    commit = package_manifest["proof_source_commit"]
    outer_seal = {
        row["path"]: (row["bytes"], row["sha256"], row["mode"])
        for row in package_manifest["payload"]
    }
    archive_root = package / "proof_package/release/dist"
    archive_results = [
        check_source_zip(
            archive_root / f"k3p_level2_{kind}_source.zip",
            repo=args.repo.resolve(), commit=commit,
            project_prefix="k3p_level2_identifiability_final", kind=kind,
        )
        for kind in ("article", "supplement")
    ]
    cache_result = check_cache(
        package / "proof_package/release/TECTONIC_CACHE_MANIFEST.json",
        args.cache_root.resolve(),
    )
    report_results = [
        check_report(package, outer_seal, kind, args.fresh_reports)
        for kind in ("article", "supplement")
    ]
    print(json.dumps({
        "status": "PASS",
        "proof_source_commit": commit,
        "python": sys.version.split()[0],
        "zlib_compile": zlib.ZLIB_VERSION,
        "zlib_runtime": zlib.ZLIB_RUNTIME_VERSION,
        "archives": archive_results,
        "cache": cache_result,
        "reports": report_results,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
