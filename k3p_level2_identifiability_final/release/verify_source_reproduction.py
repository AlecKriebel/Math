#!/usr/bin/env python3
"""Rebuild a delivered PDF twice and require byte identity with the release PDF."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import shutil
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


def validate_source_build(build: dict, *, kind: str, config: dict,
                          commit: str, pdf_source_date_epoch: int,
                          tectonic_version: str, tectonic_sha256: str) -> None:
    require(set(build) == {
        "schema", "kind", "source_commit", "source_date_epoch", "main", "command",
        "toolchain", "environment", "expected_output",
    }, "source-build metadata field set")
    require(build.get("schema") == "k3p-tectonic-source-build-v1" and
            build.get("kind") == kind and build.get("main") == config["main"] and
            build.get("expected_output") == config["output"],
            "source-build metadata")
    require(build.get("source_commit") == commit, "source-build commit binding")
    require(build.get("source_date_epoch") == pdf_source_date_epoch,
            ("PDF source-date epoch policy", build.get("source_date_epoch"),
             pdf_source_date_epoch))
    require(build.get("command") == ["tectonic", config["main"], "--outdir", "."],
            ("source build command policy", build.get("command")))
    require(build.get("toolchain") == {
        "name": "tectonic",
        "version": tectonic_version,
        "executable_sha256": tectonic_sha256,
    }, ("source build toolchain policy", build.get("toolchain")))
    require(build.get("environment") == {
        "SOURCE_DATE_EPOCH": str(pdf_source_date_epoch),
        "TZ": "UTC",
        "LC_ALL": "C",
    }, ("source build environment policy", build.get("environment")))


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
            if relative in (MANIFEST_NAME, "SOURCE_BUILD.json"):
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
    require(archive_report.get("metadata") == {"source_build": "SOURCE_BUILD.json"},
            "source archive metadata policy")
    with tempfile.TemporaryDirectory(prefix="k3p-source-metadata-") as directory:
        temporary = Path(directory)
        safe_extract_zip(source_archive, temporary)
        build_path = temporary / config["root"] / "SOURCE_BUILD.json"
        require(build_path.is_file(), "SOURCE_BUILD.json missing")
        build = json.loads(build_path.read_text(encoding="utf-8"))
    active_policy = (validate_release_policy(policy) if policy is not None else
                     load_release_policy(project))
    validate_source_build(
        build, kind=kind, config=config, commit=head_commit(project),
        pdf_source_date_epoch=active_policy["pdf_source_date_epoch"],
        tectonic_version=active_policy["tectonic_version"],
        tectonic_sha256=active_policy["tectonic_sha256"],
    )
    binding = verify_committed_source_members(
        source_archive, kind=kind, config=config, project=project
    )
    return archive_report, build, binding


def version(command: list[str]) -> str:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            text=True, check=False, timeout=60)
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


def one_build(source_archive: Path, config: dict, build: dict, run_number: int,
              tectonic: str) -> tuple[bytes, str, float]:
    with tempfile.TemporaryDirectory(prefix=f"k3p-{config['root']}-{run_number}-") as directory:
        temporary = Path(directory)
        safe_extract_zip(source_archive, temporary)
        root = temporary / config["root"]
        require(root.is_dir(), ("source archive root", config["root"]))
        command = [tectonic, config["main"], "--outdir", "."]
        expected_command = build.get("command")
        require(expected_command == ["tectonic", *command[1:]],
                ("source build command policy", expected_command))
        environment = dict(os.environ)
        environment.update({
            "SOURCE_DATE_EPOCH": str(build["source_date_epoch"]),
            "TZ": "UTC",
            "LC_ALL": "C",
            "LANG": "C",
            "PYTHONDONTWRITEBYTECODE": "1",
            "TEXMFVAR": str(temporary / "texmf-var"),
            "TEXMFCONFIG": str(temporary / "texmf-config"),
        })
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
        parser.add_argument("--report", type=Path)
        args = parser.parse_args(argv)
        config = dict(DEFAULTS[args.kind])
        source_archive = (args.source_archive or config["source"]).resolve()
        expected_pdf = (args.expected_pdf or config["pdf"]).resolve()
        report_path = (args.report or
                       HERE / f"work/source_reproduction/{args.kind}.json").resolve()
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
        toolchain = verify_tectonic_identity(tectonic, load_release_policy(PROJECT))
        first, transcript_first, elapsed_first = one_build(
            source_archive, config, build, 1, tectonic
        )
        second, transcript_second, elapsed_second = one_build(
            source_archive, config, build, 2, tectonic
        )
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
            "schema": "k3p-pdf-source-reproduction-v1",
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
