#!/usr/bin/env python3
"""Rebuild a delivered PDF twice and require byte identity with the release PDF."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPRO = PROJECT / "reproducibility"
if str(REPRO) not in sys.path:
    sys.path.insert(0, str(REPRO))

from release_common import (  # noqa: E402
    ReleaseFailure,
    atomic_write,
    canonical_json_bytes,
    head_commit,
    head_commit_epoch,
    read_head_blob,
    refuse_optimized_python,
    require,
    sha256_bytes,
    sha256_file,
    tracked_head_entries,
)
from archive_tools import MANIFEST_NAME, safe_extract_zip, verify_zip  # noqa: E402
from build_release import load_release_policy, validate_release_policy  # noqa: E402


DEFAULTS = {
    "article": {
        "source": HERE / "dist/k3p_level2_article_source.zip",
        "pdf": PROJECT / "output/pdf/K3P_Level2_Identifiability_Article.pdf",
        "root": "k3p_level2_article_source",
        "main": "main.tex",
        "output": "main.pdf",
    },
    "supplement": {
        "source": HERE / "dist/k3p_level2_supplement_source.zip",
        "pdf": PROJECT / "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf",
        "root": "k3p_level2_supplement_source",
        "main": "reader_supplement.tex",
        "output": "reader_supplement.pdf",
    },
}

CACHE_MANIFEST_RELATIVE = "release/TECTONIC_CACHE_MANIFEST.json"
CACHE_MANIFEST_MEMBER = "TECTONIC_CACHE_MANIFEST.json"
STABLE_BUILD_ENVIRONMENT_KEYS = {
    "SOURCE_DATE_EPOCH", "TZ", "LC_ALL", "LANG", "PYTHONDONTWRITEBYTECODE",
}
RUNTIME_ENVIRONMENT_KEYS = STABLE_BUILD_ENVIRONMENT_KEYS | {
    "HOME", "PATH", "TMPDIR", "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
    "TEXMFVAR", "TEXMFCONFIG",
}


def validate_source_build(build: dict, *, kind: str, config: dict,
                          commit: str, pdf_source_date_epoch: int,
                          tectonic_version: str, tectonic_sha256: str,
                          tectonic_bundle_url: str, tectonic_bundle_digest: str,
                          tectonic_cache_manifest_sha256: str) -> None:
    require(set(build) == {
        "schema", "kind", "source_commit", "source_date_epoch", "main", "command",
        "toolchain", "resource_contract", "environment", "execution_policy",
        "expected_output",
    }, "source-build metadata field set")
    require(build.get("schema") == "k3p-tectonic-source-build-v2" and
            build.get("kind") == kind and build.get("main") == config["main"] and
            build.get("expected_output") == config["output"],
            "source-build metadata")
    require(build.get("source_commit") == commit, "source-build commit binding")
    require(build.get("source_date_epoch") == pdf_source_date_epoch,
            ("PDF source-date epoch policy", build.get("source_date_epoch"),
             pdf_source_date_epoch))
    require(build.get("command") == [
        "tectonic", "--bundle", tectonic_bundle_url, "--only-cached",
        config["main"], "--outdir", ".",
    ],
            ("source build command policy", build.get("command")))
    require(build.get("toolchain") == {
        "name": "tectonic",
        "version": tectonic_version,
        "executable_sha256": tectonic_sha256,
    }, ("source build toolchain policy", build.get("toolchain")))
    require(build.get("resource_contract") == {
        "bundle_url": tectonic_bundle_url,
        "bundle_digest": tectonic_bundle_digest,
        "cache_manifest": CACHE_MANIFEST_MEMBER,
        "cache_manifest_sha256": tectonic_cache_manifest_sha256,
        "cache_payload_vendored": False,
    }, ("source build resource contract", build.get("resource_contract")))
    require(build.get("environment") == {
        "SOURCE_DATE_EPOCH": str(pdf_source_date_epoch),
        "TZ": "UTC",
        "LC_ALL": "C",
        "LANG": "C",
        "PYTHONDONTWRITEBYTECODE": "1",
    }, ("source build environment policy", build.get("environment")))
    require(build.get("execution_policy") == {
        "parent_environment_inherited": False,
        "only_cached": True,
        "private_home": True,
        "private_tmp": True,
        "cache_verified_before_and_after": True,
        "fixed_path": "/usr/bin:/bin",
        "private_directory_variables": [
            "HOME", "TEXMFCONFIG", "TEXMFVAR", "TMPDIR",
            "XDG_CACHE_HOME", "XDG_CONFIG_HOME",
        ],
        "runtime_environment_keys": sorted(RUNTIME_ENVIRONMENT_KEYS),
    }, ("source build execution policy", build.get("execution_policy")))


def validate_cache_manifest(manifest: dict, *, policy: dict) -> dict:
    require(set(manifest) == {
        "schema", "bundle_url", "bundle_digest", "cache_layout",
        "bundle_hash_pointer", "file_count", "total_bytes", "files",
        "payload_sha256",
    }, "Tectonic cache manifest field set")
    claimed = manifest.get("payload_sha256")
    logical = dict(manifest)
    logical.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(logical)),
            "Tectonic cache manifest payload hash")
    require(manifest.get("schema") == "k3p-tectonic-cache-manifest-v1" and
            manifest.get("bundle_url") == policy["tectonic_bundle_url"] and
            manifest.get("bundle_digest") == policy["tectonic_bundle_digest"] and
            manifest.get("cache_layout") ==
            "contents of the Tectonic per-user cache root",
            "Tectonic cache manifest bundle binding")
    pointer_name = manifest["bundle_url"].replace(":", ",58,").replace("/", ",47,")
    expected_pointer = f"bundles/hashes/{pointer_name}"
    require(manifest.get("bundle_hash_pointer") == expected_pointer,
            "Tectonic cache manifest bundle-pointer path")
    rows = manifest.get("files")
    require(isinstance(rows, list) and rows,
            "Tectonic cache manifest file inventory")
    observed_paths = []
    observed_total = 0
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"},
                "Tectonic cache manifest row fields")
        relative = PurePosixPath(str(row.get("path", "")))
        require(relative.as_posix() not in ("", ".") and not relative.is_absolute() and
                ".." not in relative.parts and "\\" not in relative.as_posix(),
                ("Tectonic cache manifest path", relative.as_posix()))
        require(isinstance(row.get("bytes"), int) and row["bytes"] >= 0 and
                isinstance(row.get("sha256"), str) and len(row["sha256"]) == 64,
                ("Tectonic cache manifest row values", relative.as_posix()))
        observed_paths.append(relative.as_posix())
        observed_total += row["bytes"]
    require(observed_paths == sorted(set(observed_paths)),
            "Tectonic cache manifest paths must be unique and sorted")
    require(manifest.get("file_count") == len(rows) and
            manifest.get("total_bytes") == observed_total,
            "Tectonic cache manifest census")
    pointer_rows = [row for row in rows if row["path"] == expected_pointer]
    pointer_bytes = (manifest["bundle_digest"] + "\n").encode("ascii")
    require(pointer_rows == [{
        "path": expected_pointer,
        "bytes": len(pointer_bytes),
        "sha256": sha256_bytes(pointer_bytes),
    }], "Tectonic cache manifest bundle-pointer content")
    return manifest


def load_cache_manifest(project: Path, *, policy: dict) -> dict:
    raw = read_head_blob(project, CACHE_MANIFEST_RELATIVE)
    require(sha256_bytes(raw) == policy["tectonic_cache_manifest_sha256"],
            "Tectonic cache manifest file binding")
    value = json.loads(raw.decode("utf-8"))
    return validate_cache_manifest(value, policy=policy)


def verify_tectonic_cache(cache_root: Path, manifest: dict) -> dict:
    cache_root = cache_root.resolve()
    require(cache_root.is_dir() and not cache_root.is_symlink(),
            ("Tectonic cache root must be a real directory", str(cache_root)))
    observed: dict[str, tuple[int, str]] = {}
    for path in sorted(cache_root.rglob("*")):
        relative = path.relative_to(cache_root).as_posix()
        metadata = path.lstat()
        require(not stat.S_ISLNK(metadata.st_mode),
                ("Tectonic cache symlink forbidden", relative))
        if stat.S_ISDIR(metadata.st_mode):
            continue
        require(stat.S_ISREG(metadata.st_mode),
                ("Tectonic cache nonregular object forbidden", relative))
        observed[relative] = (metadata.st_size, sha256_file(path))
    expected = {
        row["path"]: (row["bytes"], row["sha256"])
        for row in manifest["files"]
    }
    require(set(observed) == set(expected),
            ("Tectonic cache exact file set",
             sorted(set(expected) - set(observed)),
             sorted(set(observed) - set(expected))))
    for relative in sorted(expected):
        require(observed[relative] == expected[relative],
                ("Tectonic cache member mismatch", relative,
                 observed[relative], expected[relative]))
    return {
        "file_count": len(observed),
        "total_bytes": sum(size for size, _digest in observed.values()),
        "manifest_payload_sha256": manifest["payload_sha256"],
    }


def committed_source_members(project: Path, kind: str) -> dict[str, bytes]:
    entries = tracked_head_entries(project)
    if kind == "article":
        paths = sorted(
            path for path in entries
            if path in ("manuscript/main.tex", "manuscript/references.bib") or
            path.startswith("manuscript/sections/") or
            path.startswith("manuscript/figures/")
        )
        transform = lambda path: path.removeprefix("manuscript/")
    else:
        paths = ["supplement/reader_supplement.tex"]
        transform = lambda path: Path(path).name
    require(all(path in entries for path in paths) and bool(paths),
            ("committed source member set", kind, paths))
    return {transform(path): read_head_blob(project, path) for path in paths}


def verify_committed_source_members(source_archive: Path, *, kind: str,
                                    config: dict, project: Path) -> dict:
    expected = committed_source_members(project, kind)
    observed: dict[str, bytes] = {}
    with zipfile.ZipFile(source_archive, mode="r") as archive:
        for info in archive.infolist():
            parts = PurePosixPath(info.filename).parts
            require(parts and parts[0] == config["root"],
                    ("source archive root", info.filename))
            relative = PurePosixPath(*parts[1:]).as_posix()
            if relative in (MANIFEST_NAME, "SOURCE_BUILD.json", CACHE_MANIFEST_MEMBER):
                continue
            require(relative not in observed,
                    ("duplicate source archive member", relative))
            observed[relative] = archive.read(info)
    require(set(observed) == set(expected),
            ("source archive committed member set", kind,
             sorted(set(expected) - set(observed)),
             sorted(set(observed) - set(expected))))
    for relative in sorted(expected):
        require(observed[relative] == expected[relative],
                ("source archive member differs from HEAD", kind, relative))
    return {
        "kind": kind,
        "member_count": len(expected),
        "payload_sha256": sha256_bytes(canonical_json_bytes({
            relative: sha256_bytes(expected[relative]) for relative in sorted(expected)
        })),
    }


def verify_source_archive_contract(source_archive: Path, *, kind: str,
                                   project: Path,
                                   policy: dict | None = None) -> tuple[dict, dict, dict]:
    config = dict(DEFAULTS[kind])
    archive_report = verify_zip(source_archive)
    require(archive_report["kind"] == f"{kind}_latex_source",
            ("source archive kind", archive_report["kind"]))
    require(archive_report["archive_root"] == config["root"],
            ("source archive root policy", archive_report["archive_root"], config["root"]))
    require(archive_report["source_commit"] == head_commit(project),
            "source archive commit differs from HEAD")
    require(archive_report["source_date_epoch"] == head_commit_epoch(project),
            ("source archive outer epoch differs from HEAD",
             archive_report["source_date_epoch"], head_commit_epoch(project)))
    require(archive_report.get("metadata") == {
        "source_build": "SOURCE_BUILD.json",
        "tectonic_cache_manifest": CACHE_MANIFEST_MEMBER,
    },
            "source archive metadata policy")
    active_policy = (validate_release_policy(policy) if policy is not None else
                     load_release_policy(project))
    expected_cache_manifest = read_head_blob(project, CACHE_MANIFEST_RELATIVE)
    require(sha256_bytes(expected_cache_manifest) ==
            active_policy["tectonic_cache_manifest_sha256"],
            "committed Tectonic cache manifest policy binding")
    with tempfile.TemporaryDirectory(prefix="k3p-source-metadata-") as directory:
        temporary = Path(directory)
        safe_extract_zip(source_archive, temporary)
        build_path = temporary / config["root"] / "SOURCE_BUILD.json"
        cache_manifest_path = temporary / config["root"] / CACHE_MANIFEST_MEMBER
        require(build_path.is_file(), "SOURCE_BUILD.json missing")
        require(cache_manifest_path.is_file() and
                cache_manifest_path.read_bytes() == expected_cache_manifest,
                "source archive Tectonic cache manifest differs from HEAD")
        build = json.loads(build_path.read_text(encoding="utf-8"))
        validate_cache_manifest(
            json.loads(cache_manifest_path.read_text(encoding="utf-8")),
            policy=active_policy,
        )
    validate_source_build(
        build, kind=kind, config=config, commit=head_commit(project),
        pdf_source_date_epoch=active_policy["pdf_source_date_epoch"],
        tectonic_version=active_policy["tectonic_version"],
        tectonic_sha256=active_policy["tectonic_sha256"],
        tectonic_bundle_url=active_policy["tectonic_bundle_url"],
        tectonic_bundle_digest=active_policy["tectonic_bundle_digest"],
        tectonic_cache_manifest_sha256=
        active_policy["tectonic_cache_manifest_sha256"],
    )
    binding = verify_committed_source_members(
        source_archive, kind=kind, config=config, project=project
    )
    return archive_report, build, binding


def version(command: list[str]) -> str:
    environment = {
        "HOME": "/var/empty",
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "LC_ALL": "C",
        "TZ": "UTC",
    }
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, check=False, timeout=60, env=environment)
    require(result.returncode == 0, ("tool version command failed", command))
    return result.stdout.strip()


def verify_tectonic_identity(executable: str, policy: dict) -> dict:
    path = Path(executable).resolve()
    observed_hash = sha256_file(path)
    require(observed_hash == policy["tectonic_sha256"],
            ("Tectonic executable SHA-256 policy", observed_hash,
             policy["tectonic_sha256"]))
    observed_version = version([str(path), "--version"])
    require(observed_version == policy["tectonic_version"],
            ("Tectonic version policy", observed_version,
             policy["tectonic_version"]))
    return {"path": str(path), "sha256": observed_hash, "version": observed_version}


def project_relative(path: Path, *, label: str) -> str:
    try:
        return path.resolve().relative_to(PROJECT.resolve()).as_posix()
    except ValueError as error:
        raise ReleaseFailure((f"{label} outside project", str(path))) from error


def discover_tectonic_cache(cache_argument: Path | None) -> Path:
    if cache_argument is not None:
        return cache_argument.expanduser().resolve()
    home = Path.home()
    candidates = [
        home / "Library/Caches/Tectonic",
        home / ".cache/Tectonic",
        home / ".cache/tectonic",
    ]
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        candidates = [Path(xdg).expanduser() / "Tectonic", *candidates]
    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()
    raise ReleaseFailure((
        "Tectonic cache unavailable; pass --tectonic-cache-root",
        [str(path) for path in candidates],
    ))


def minimal_build_environment(temporary: Path, *, build: dict,
                              cache_root: Path) -> dict[str, str]:
    private_home = temporary / "private-home"
    private_tmp = temporary / "private-tmp"
    xdg_cache = private_home / ".cache"
    xdg_config = private_home / ".config"
    texmf_var = temporary / "texmf-var"
    texmf_config = temporary / "texmf-config"
    for directory in (
        private_tmp, xdg_cache, xdg_config, texmf_var, texmf_config,
        private_home / "Library/Caches",
    ):
        directory.mkdir(parents=True, exist_ok=True)
    # Tectonic's platform cache resolver uses the first location on Darwin and
    # the second on freedesktop platforms.  Both point at the same verified,
    # content-addressed external cache; --only-cached forbids resource fetches.
    for link in (
        private_home / "Library/Caches/Tectonic",
        xdg_cache / "Tectonic",
    ):
        link.symlink_to(cache_root, target_is_directory=True)
    environment = {
        "HOME": str(private_home),
        "PATH": "/usr/bin:/bin",
        "TMPDIR": str(private_tmp),
        "XDG_CACHE_HOME": str(xdg_cache),
        "XDG_CONFIG_HOME": str(xdg_config),
        "TEXMFVAR": str(texmf_var),
        "TEXMFCONFIG": str(texmf_config),
        **build["environment"],
    }
    require(set(environment) == RUNTIME_ENVIRONMENT_KEYS,
            ("source build minimal environment keys", sorted(environment)))
    return environment


def one_build(source_archive: Path, config: dict, build: dict, run_number: int,
              tectonic: str, cache_root: Path) -> tuple[bytes, str, float]:
    with tempfile.TemporaryDirectory(prefix=f"k3p-{config['root']}-{run_number}-") as directory:
        temporary = Path(directory)
        safe_extract_zip(source_archive, temporary)
        root = temporary / config["root"]
        require(root.is_dir(), ("source archive root", config["root"]))
        resource = build["resource_contract"]
        command = [
            tectonic, "--bundle", resource["bundle_url"], "--only-cached",
            config["main"], "--outdir", ".",
        ]
        expected_command = build.get("command")
        require(expected_command == ["tectonic", *command[1:]],
                ("source build command policy", expected_command))
        environment = minimal_build_environment(
            temporary, build=build, cache_root=cache_root
        )
        started = time.monotonic()
        result = subprocess.run(command, cwd=root, env=environment,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, check=False, timeout=1_800)
        elapsed = time.monotonic() - started
        require(result.returncode == 0,
                ("LaTeX source reproduction failed", run_number, result.stdout[-6000:]))
        output = root / config["output"]
        require(output.is_file(), ("expected PDF not produced", config["output"]))
        return output.read_bytes(), result.stdout, elapsed


def main(argv: list[str] | None = None) -> int:
    try:
        refuse_optimized_python()
        parser = argparse.ArgumentParser()
        parser.add_argument("--kind", choices=("article", "supplement"), required=True)
        parser.add_argument("--source-archive", type=Path)
        parser.add_argument("--expected-pdf", type=Path)
        parser.add_argument("--tectonic", default="tectonic")
        parser.add_argument("--tectonic-cache-root", type=Path)
        parser.add_argument("--report", type=Path)
        args = parser.parse_args(argv)
        config = dict(DEFAULTS[args.kind])
        source_archive = (args.source_archive or config["source"]).resolve()
        expected_pdf = (args.expected_pdf or config["pdf"]).resolve()
        report_path = (args.report or
                       HERE / f"source_reproduction_evidence/{args.kind}.json").resolve()
        source_archive_relative = project_relative(
            source_archive, label="source archive"
        )
        project_relative(report_path, label="source reproduction report")
        require(source_archive.is_file(), ("missing source archive", str(source_archive)))
        require(expected_pdf.is_file(), ("missing delivered PDF", str(expected_pdf)))
        entries = tracked_head_entries(PROJECT)
        pdf_relative = project_relative(expected_pdf, label="expected PDF")
        require(pdf_relative in entries, ("delivered PDF not committed at HEAD", pdf_relative))
        require(expected_pdf.read_bytes() == read_head_blob(PROJECT, pdf_relative),
                ("delivered PDF differs from HEAD", pdf_relative))
        archive_report, build, committed_binding = verify_source_archive_contract(
            source_archive, kind=args.kind, project=PROJECT
        )
        tectonic = shutil.which(args.tectonic)
        require(tectonic is not None, ("tectonic unavailable", args.tectonic))
        policy = load_release_policy(PROJECT)
        toolchain = verify_tectonic_identity(tectonic, policy)
        cache_manifest = load_cache_manifest(PROJECT, policy=policy)
        cache_root = discover_tectonic_cache(args.tectonic_cache_root)
        cache_before = verify_tectonic_cache(cache_root, cache_manifest)
        first, transcript_first, elapsed_first = one_build(
            source_archive, config, build, 1, tectonic, cache_root
        )
        second, transcript_second, elapsed_second = one_build(
            source_archive, config, build, 2, tectonic, cache_root
        )
        cache_after = verify_tectonic_cache(cache_root, cache_manifest)
        require(cache_before == cache_after,
                ("Tectonic cache changed during only-cached builds",
                 cache_before, cache_after))
        expected_hash = sha256_file(expected_pdf)
        first_hash, second_hash = sha256_bytes(first), sha256_bytes(second)
        require(first_hash == second_hash, ("NONDETERMINISTIC_PDF_BUILD", first_hash, second_hash))
        require(first_hash == expected_hash,
                ("SOURCE_REPRODUCTION_PDF_MISMATCH", expected_hash, first_hash))
        transcript_root = report_path.parent / (report_path.stem + "_transcripts")
        transcript_root.mkdir(parents=True, exist_ok=True)
        first_path, second_path = transcript_root / "run1.log", transcript_root / "run2.log"
        atomic_write(first_path, transcript_first.encode())
        atomic_write(second_path, transcript_second.encode())
        report = {
            "schema": "k3p-pdf-source-reproduction-v2",
            "status": "PASS_BYTE_FOR_BYTE",
            "kind": args.kind,
            "source_commit": head_commit(PROJECT),
            "source_archive": {
                "path": source_archive_relative,
                "sha256": sha256_file(source_archive),
                "structural_verification": archive_report,
            },
            "expected_pdf": {"path": pdf_relative, "sha256": expected_hash,
                             "bytes": expected_pdf.stat().st_size},
            "committed_source_binding": committed_binding,
            "builds": [
                {"run": 1, "sha256": first_hash, "bytes": len(first),
                 "elapsed_seconds": elapsed_first,
                 "transcript": str(first_path.relative_to(PROJECT)),
                 "transcript_sha256": sha256_file(first_path)},
                {"run": 2, "sha256": second_hash, "bytes": len(second),
                 "elapsed_seconds": elapsed_second,
                 "transcript": str(second_path.relative_to(PROJECT)),
                 "transcript_sha256": sha256_file(second_path)},
            ],
            "byte_identical_across_two_builds": True,
            "byte_identical_to_delivered_pdf": True,
            "tool_versions": {
                "tectonic": toolchain,
            },
            "environment": build["environment"],
            "execution_policy": build["execution_policy"],
            "resource_bundle": {
                "bundle_url": cache_manifest["bundle_url"],
                "bundle_digest": cache_manifest["bundle_digest"],
                "cache_manifest_path": CACHE_MANIFEST_RELATIVE,
                "cache_manifest_sha256": sha256_file(
                    PROJECT / CACHE_MANIFEST_RELATIVE
                ),
                "cache_manifest_payload_sha256": cache_manifest["payload_sha256"],
                "cache_file_count": cache_manifest["file_count"],
                "cache_total_bytes": cache_manifest["total_bytes"],
                "cache_verified_before_and_after": True,
                "cache_payload_vendored": False,
            },
        }
        logical = dict(report)
        logical["builds"] = [
            {key: row[key] for key in ("run", "sha256", "bytes")}
            for row in report["builds"]
        ]
        logical.pop("tool_versions", None)
        report["logical_payload_sha256"] = sha256_bytes(canonical_json_bytes(logical))
        atomic_write(report_path, (json.dumps(report, indent=2, sort_keys=True) + "\n").encode())
        print(json.dumps({"status": report["status"], "kind": args.kind,
                          "pdf_sha256": expected_hash,
                          "logical_payload_sha256": report["logical_payload_sha256"],
                          "report": str(report_path.relative_to(PROJECT))}, sort_keys=True))
        print("K3P_SOURCE_REPRODUCTION_PASS")
        return 0
    except (ReleaseFailure, OSError, UnicodeError, ValueError, json.JSONDecodeError,
            subprocess.SubprocessError) as error:
        print(f"K3P_SOURCE_REPRODUCTION_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
