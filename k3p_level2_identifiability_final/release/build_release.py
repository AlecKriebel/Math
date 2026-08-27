#!/usr/bin/env python3
"""Build deterministic K3P compact/full archives and the final envelope.

Archive source bytes come only from the committed ``HEAD`` tree.  This is a
hard boundary: untracked and merely staged material cannot be packaged.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import zipfile


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
REPRO = PROJECT / "reproducibility"
SUBMISSION = PROJECT / "submission"
if str(REPRO) not in sys.path:
    sys.path.insert(0, str(REPRO))
if str(SUBMISSION) not in sys.path:
    sys.path.insert(0, str(SUBMISSION))

from release_common import (  # noqa: E402
    ReleaseFailure,
    atomic_write,
    canonical_json_bytes,
    exact_head_tags,
    head_commit,
    head_commit_epoch,
    load_json,
    load_head_json,
    read_head_blob,
    refuse_optimized_python,
    require,
    resolve_inside,
    safe_relative_path,
    scoped_status,
    sha256_bytes,
    sha256_file,
    tracked_head_entries,
)
from archive_tools import (  # noqa: E402
    deterministic_tar_gz,
    deterministic_zip,
    safe_extract_tar_gz,
    safe_extract_zip,
    verify_tar_gz,
    verify_zip,
)
from validate_submission_packages import validate as validate_submissions  # noqa: E402
from run_release_suite import verify_suite_report  # noqa: E402


POLICY_RELATIVE = "release/RELEASE_FILESET.json"
DIST = HERE / "dist"
FULL_ARCHIVE = DIST / "k3p_level2_reproducibility.tar.gz"
COMPACT_ARCHIVE = DIST / "k3p_level2_compact_verifier.zip"
ARTICLE_PDF = "output/pdf/K3P_Level2_Identifiability_Article.pdf"
SUPPLEMENT_PDF = "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf"
SUBMISSION_PACKAGE_MANIFEST = "SUBMISSION_PACKAGE_MANIFEST.json"
SUBMISSION_KINDS = {"systematic_biology", "journal_of_mathematical_biology"}
SUBMISSION_ROOTS = {
    "systematic_biology": "k3p_systematic_biology_submission",
    "journal_of_mathematical_biology": "k3p_journal_of_mathematical_biology_submission",
}
SUBMISSION_REQUIRED_FILES = {
    "systematic_biology": {
        "K3P_level2_main_SB.pdf", "K3P_level2_supplement_SB.pdf", "cover_letter.pdf",
    },
    "journal_of_mathematical_biology": {
        "K3P_level2_main_JMB.pdf", "ESM_1.pdf", "cover_letter.pdf",
    },
}
RELEASE_TOKEN_RE = re.compile(rb"@@[A-Z][A-Z0-9_]*@@")


def validate_release_policy(policy: dict) -> dict:
    require(set(policy) == {
        "schema", "archive_root", "compact_root", "pdf_source_date_epoch",
        "tectonic_version", "tectonic_sha256", "expected_full_selection_count",
        "expected_full_selection_sha256", "expected_compact_selection_count",
        "expected_compact_selection_sha256", "include_files", "include_prefixes",
        "exclude_globs", "required_full_files", "required_release_pdf_files",
        "forbidden_generated_members",
    }, "release fileset policy field set")
    require(policy.get("schema") == "k3p-release-fileset-policy-v1",
            "release fileset schema")
    require(policy.get("archive_root") == "k3p_level2_reproducibility" and
            policy.get("compact_root") == "k3p_level2_compact_verifier",
            "release fileset archive roots")
    require(isinstance(policy.get("pdf_source_date_epoch"), int) and
            policy["pdf_source_date_epoch"] > 0,
            "release fileset PDF source-date epoch")
    require(policy.get("tectonic_version") == "Tectonic 0.16.9" and
            re.fullmatch(r"[0-9a-f]{64}", str(policy.get("tectonic_sha256"))) is not None,
            "release fileset Tectonic toolchain")
    for kind in ("full", "compact"):
        require(isinstance(policy.get(f"expected_{kind}_selection_count"), int) and
                policy[f"expected_{kind}_selection_count"] > 0 and
                re.fullmatch(r"[0-9a-f]{64}", str(
                    policy.get(f"expected_{kind}_selection_sha256")
                )) is not None,
                ("release fileset selection lock", kind))
    list_fields = (
        "include_files", "include_prefixes", "exclude_globs", "required_full_files",
        "required_release_pdf_files", "forbidden_generated_members",
    )
    for field in list_fields:
        values = policy.get(field)
        require(isinstance(values, list) and all(
            isinstance(value, str) and value for value in values
        ), ("release fileset list field", field))
        require(len(values) == len(set(values)),
                ("duplicate release fileset value", field))
    require(set(policy["required_release_pdf_files"]) == {ARTICLE_PDF, SUPPLEMENT_PDF},
            "release fileset canonical PDF paths")
    for relative in policy["include_files"] + policy["required_full_files"] + \
            policy["required_release_pdf_files"] + policy["forbidden_generated_members"]:
        safe_relative_path(relative)
    for prefix in policy["include_prefixes"]:
        require(prefix.endswith("/") and prefix.count("/") >= 1,
                ("release fileset prefix", prefix))
        safe_relative_path(prefix[:-1])
    for pattern in policy["exclude_globs"]:
        require(not pattern.startswith("/") and "\\" not in pattern and
                ".." not in pattern.split("/"),
                ("release fileset exclusion glob", pattern))
    return policy


def load_release_policy(project: Path) -> dict:
    return validate_release_policy(load_head_json(project, POLICY_RELATIVE))


def require_submission_readiness_report(report: dict, exit_code: int) -> None:
    claimed = report.get("payload_sha256")
    body = dict(report)
    body.pop("payload_sha256", None)
    require(claimed == sha256_bytes(canonical_json_bytes(body)),
            "submission readiness payload hash")
    require(exit_code == 0 and report.get("status") == "READY" and
            report.get("structural_error_count") == 0 and
            report.get("release_blocker_count") == 0,
            ("submission packages are not READY", report.get("status"),
             report.get("structural_error_count"), report.get("release_blocker_count")))


def submission_readiness_binding(project: Path) -> dict:
    require(project.resolve() == PROJECT.resolve(), "submission validator project binding")
    report, exit_code = validate_submissions()
    require_submission_readiness_report(report, exit_code)
    relatives = [
        "submission/validate_submission_packages.py",
        "submission/systematic_biology/MANIFEST.json",
        "submission/journal_of_mathematical_biology/MANIFEST.json",
        "submission/arxiv/MANIFEST.json",
    ]
    entries = tracked_head_entries(project)
    hashes = {}
    for relative in relatives:
        require(relative in entries, ("submission readiness input not committed", relative))
        path = resolve_inside(project, relative)
        head_bytes = read_head_blob(project, relative)
        require(path.read_bytes() == head_bytes,
                ("submission readiness input differs from HEAD", relative))
        hashes[relative] = sha256_bytes(head_bytes)
    binding = {
        "schema": "k3p-submission-readiness-binding-v1",
        "status": "READY",
        "source_commit": head_commit(project),
        "input_sha256": hashes,
        "validation_report": report,
    }
    binding["payload_sha256"] = sha256_bytes(canonical_json_bytes(binding))
    return binding


def submission_argument_map(values: list[str]) -> dict[str, Path]:
    result = {}
    for raw in values:
        name, path = named_asset(raw)
        require(name not in result, ("duplicate submission package name", name))
        result[name] = path
    require(set(result) == SUBMISSION_KINDS,
            ("submission package kinds", sorted(result), sorted(SUBMISSION_KINDS)))
    return result


def expected_submission_uploads(project: Path, kind: str) -> dict[str, dict]:
    manifest_relative = {
        "systematic_biology": "submission/systematic_biology/MANIFEST.json",
        "journal_of_mathematical_biology":
            "submission/journal_of_mathematical_biology/MANIFEST.json",
    }[kind]
    manifest = load_head_json(project, manifest_relative)
    rows = manifest.get("initial_portal_uploads")
    require(isinstance(rows, list), ("journal upload manifest list", kind))
    require({row.get("filename") for row in rows if isinstance(row, dict)} ==
            SUBMISSION_REQUIRED_FILES[kind] and len(rows) == len(SUBMISSION_REQUIRED_FILES[kind]),
            ("journal upload manifest exact coverage", kind))
    uploads = {}
    for row in rows:
        require(isinstance(row, dict), ("journal upload manifest row", kind))
        filename = row.get("filename") if isinstance(row, dict) else None
        require(row.get("present") is True,
                ("required journal upload not present", kind, filename))
        require(isinstance(row.get("bytes"), int) and row["bytes"] >= 0 and
                re.fullmatch(r"[0-9a-f]{64}", str(row.get("sha256"))) is not None and
                isinstance(row.get("path"), str),
                ("required journal upload binding", kind, filename))
        safe_relative_path(row["path"])
        upload_path = resolve_inside(project, row["path"])
        require(upload_path.is_file() and not upload_path.is_symlink(),
                ("required journal upload is not a regular file", kind, filename))
        require(upload_path.stat().st_size == row["bytes"] and
                sha256_file(upload_path) == row["sha256"],
                ("required journal upload bytes differ from manifest", kind, filename))
        uploads[filename] = {
            "sha256": row["sha256"], "bytes": row["bytes"], "path": row["path"],
        }
    require(set(uploads) == SUBMISSION_REQUIRED_FILES[kind],
            ("required journal upload manifest coverage", kind,
             sorted(SUBMISSION_REQUIRED_FILES[kind] - set(uploads))))
    return uploads


def expected_submission_members(project: Path, kind: str,
                                expected_uploads: dict[str, dict]) -> dict[str, bytes]:
    manifest_relative = {
        "systematic_biology": "submission/systematic_biology/MANIFEST.json",
        "journal_of_mathematical_biology":
            "submission/journal_of_mathematical_biology/MANIFEST.json",
    }[kind]
    manifest = load_head_json(project, manifest_relative)
    entries = tracked_head_entries(project)
    source_map = manifest.get("source_map")
    require(isinstance(source_map, list) and source_map,
            ("journal source-map coverage", kind))
    members: dict[str, bytes] = {}
    for row in source_map:
        require(isinstance(row, dict), ("journal source-map row", kind))
        source = row.get("source")
        destination = row.get("destination")
        mode = row.get("mode", "copy_file")
        safe_relative_path(source)
        safe_relative_path(destination)
        require(mode in {"copy_file", "copy_tree"},
                ("journal source-map mode", kind, mode))
        if mode == "copy_file":
            require(source in entries, ("journal source-map file not committed", kind, source))
            expanded = [(destination, source)]
        else:
            prefix = source.rstrip("/") + "/"
            sources = sorted(relative for relative in entries if relative.startswith(prefix))
            require(bool(sources), ("journal source-map tree empty", kind, source))
            expanded = [
                (f"{destination.rstrip('/')}/{relative.removeprefix(prefix)}", relative)
                for relative in sources
            ]
        for target, relative in expanded:
            safe_relative_path(target)
            require(target not in members,
                    ("journal source-map destination collision", kind, target))
            members[target] = read_head_blob(project, relative)
    for filename, record in sorted(expected_uploads.items()):
        safe_relative_path(filename)
        require(filename not in members,
                ("journal upload/source destination collision", kind, filename))
        upload_path = resolve_inside(project, record["path"])
        data = upload_path.read_bytes()
        require(len(data) == record["bytes"] and sha256_bytes(data) == record["sha256"],
                ("journal upload changed after readiness validation", kind, filename))
        members[filename] = data
    return members


def verify_submission_package(path: Path, *, kind: str, commit: str,
                              expected_uploads: dict[str, dict],
                              expected_members: dict[str, bytes]) -> dict:
    require(kind in SUBMISSION_KINDS, ("unknown submission package kind", kind))
    try:
        archive = zipfile.ZipFile(path, mode="r")
    except zipfile.BadZipFile as error:
        raise ReleaseFailure(("not a ZIP submission package", kind, str(path))) from error
    with archive:
        require(archive.testzip() is None, ("submission package CRC", kind))
        observed = {}
        root = None
        for info in archive.infolist():
            require(not info.is_dir(), ("directory submission member forbidden", info.filename))
            safe_relative_path(info.filename)
            parts = PurePosixPath(info.filename).parts
            require(len(parts) >= 2, ("submission member missing package root", info.filename))
            root = root or parts[0]
            require(parts[0] == root, ("multiple submission package roots", info.filename))
            relative = PurePosixPath(*parts[1:]).as_posix()
            require(relative not in observed, ("duplicate submission member", relative))
            observed[relative] = archive.read(info)
    require(SUBMISSION_PACKAGE_MANIFEST in observed,
            ("submission package manifest missing", kind))
    require(root == SUBMISSION_ROOTS[kind],
            ("submission package root", kind, root, SUBMISSION_ROOTS[kind]))
    manifest = json.loads(observed.pop(SUBMISSION_PACKAGE_MANIFEST).decode("utf-8"))
    require(set(manifest) == {
        "schema", "status", "kind", "source_commit", "members", "payload_sha256"
    }, ("submission package manifest field set", kind))
    require(manifest.get("schema") == "k3p-journal-submission-package-v1" and
            manifest.get("status") == "READY",
            ("submission package manifest schema/status", kind))
    require(manifest.get("kind") == kind, ("submission package kind", kind,
                                            manifest.get("kind")))
    require(manifest.get("source_commit") == commit,
            ("submission package source commit", kind))
    claimed_manifest_payload = manifest.get("payload_sha256")
    manifest_body = dict(manifest)
    manifest_body.pop("payload_sha256", None)
    require(claimed_manifest_payload == sha256_bytes(canonical_json_bytes(manifest_body)),
            ("submission package manifest payload", kind))
    rows = manifest.get("members")
    require(isinstance(rows, list), ("submission package member manifest", kind))
    expected = {}
    for row in rows:
        require(isinstance(row, dict) and set(row) == {"path", "sha256", "bytes"},
                ("submission member row", kind))
        relative = row.get("path")
        safe_relative_path(relative)
        require(relative not in expected, ("duplicate submission manifest member", relative))
        expected[relative] = (row.get("sha256"), row.get("bytes"))
    require(set(expected) == set(observed), ("submission member set", kind))
    require(set(observed) == set(expected_members),
            ("journal package exact HEAD/source-map member set", kind,
             sorted(set(expected_members) - set(observed)),
             sorted(set(observed) - set(expected_members))))
    for relative, data in observed.items():
        expected_hash, expected_bytes = expected[relative]
        require(sha256_bytes(data) == expected_hash and len(data) == expected_bytes,
                ("submission member hash or size", kind, relative))
        require(data == expected_members[relative],
                ("journal package member differs from HEAD/source-map bytes", kind, relative))
        if Path(relative).suffix.lower() in {".tex", ".md", ".json", ".txt"}:
            require(RELEASE_TOKEN_RE.search(data) is None,
                    ("unresolved release token in submission package", kind, relative))
    basenames = {Path(relative).name for relative in observed}
    require(SUBMISSION_REQUIRED_FILES[kind].issubset(basenames),
            ("required journal upload missing", kind,
             sorted(SUBMISSION_REQUIRED_FILES[kind] - basenames)))
    for filename, upload in expected_uploads.items():
        matches = [data for relative, data in observed.items()
                   if Path(relative).name == filename]
        require(len(matches) == 1 and len(matches[0]) == upload["bytes"] and
                sha256_bytes(matches[0]) == upload["sha256"],
                ("journal package/upload binding", kind, filename))
    return {
        "kind": kind,
        "root": root,
        "member_count_excluding_manifest": len(observed),
        "manifest_payload_sha256": claimed_manifest_payload,
        "validated_uploads": expected_uploads,
        "member_payload_sha256": sha256_bytes(canonical_json_bytes({
            relative: sha256_bytes(expected_members[relative])
            for relative in sorted(expected_members)
        })),
    }


def excluded(relative: str, policy: dict) -> bool:
    return any(fnmatch.fnmatchcase(relative, pattern)
               for pattern in policy.get("exclude_globs", []))


def full_selection(project: Path, policy: dict, *, require_pdfs: bool) -> list[str]:
    entries = tracked_head_entries(project)
    include_files = set(policy.get("include_files", []))
    prefixes = tuple(policy.get("include_prefixes", []))
    selected = [
        relative for relative in entries
        if (relative in include_files or relative.startswith(prefixes))
        and not excluded(relative, policy)
    ]
    require(len(selected) == policy["expected_full_selection_count"] and
            sha256_bytes(canonical_json_bytes(selected)) ==
            policy["expected_full_selection_sha256"],
            ("full release selection lock", len(selected),
             sha256_bytes(canonical_json_bytes(selected))))
    if not require_pdfs:
        selected = [relative for relative in selected
                    if relative not in set(policy.get("required_release_pdf_files", []))]
    required = list(policy.get("required_full_files", []))
    if require_pdfs:
        required += list(policy.get("required_release_pdf_files", []))
    missing = sorted(set(required) - set(selected))
    require(missing == [], ("required committed release members missing", missing))
    forbidden = set(policy.get("forbidden_generated_members", []))
    require(not (forbidden & set(selected)),
            ("self-referential generated member selected", sorted(forbidden & set(selected))))
    require(selected == sorted(selected) and len(selected) == len(set(selected)),
            "full release selection ordering")
    return selected


def add_paths(paths: set[str], values) -> None:
    if isinstance(values, dict):
        for key, value in values.items():
            if key in ("path", "support_path") and isinstance(value, str):
                try:
                    safe_relative_path(value)
                    paths.add(value)
                except ReleaseFailure:
                    pass
            elif key in ("active_verifier_hashes", "generated_evidence_sha256",
                          "observed_sha256", "artifacts",
                          "independent_implementations", "bindings") and \
                    isinstance(value, dict):
                for candidate in value:
                    if not isinstance(candidate, str):
                        continue
                    try:
                        safe_relative_path(candidate)
                        paths.add(candidate)
                    except ReleaseFailure:
                        pass
                add_paths(paths, value)
            else:
                add_paths(paths, value)
    elif isinstance(values, list):
        for value in values:
            add_paths(paths, value)


def compact_selection(project: Path, policy: dict) -> list[str]:
    entries = tracked_head_entries(project)
    required = {
        "FINAL_CLAIM_LOCK.json",
        "clean_room/verify_h21_transport_and_fourteen_orbits.py",
        "reproducibility/verify_k3p_same_classification.py",
        "reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json",
        "reproducibility/test_k3p_same_classification_mutations.py",
        "reproducibility/K3P_SAME_CLASSIFICATION_MUTATION_REPORT.json",
        "restoration/verify_k3p_restoration.py",
    }
    report = json.loads(read_head_blob(
        project, "reproducibility/K3P_SAME_CLASSIFICATION_GATE_REPORT.json"
    ))
    required.update(report.get("bindings", {}).keys())
    hardened = json.loads(read_head_blob(
        project, "clean_room/adversarial/HARDENED_H21_REAUDIT.json"
    ))
    required.update(
        "input_frozen/k3p_cloud_artifacts/" + row["filename"]
        for row in hardened.get("active_input_hashes", [])
    )
    # The integrated verifier follows several secondary hash tables.  Recursively
    # collect every syntactically safe bound path from its committed JSON inputs;
    # the extracted-bundle replay below is the final dependency-completeness test.
    queue = list(required)
    seen_json: set[str] = set()
    while queue:
        relative = queue.pop()
        if relative not in entries or not relative.endswith(".json") or relative in seen_json:
            continue
        seen_json.add(relative)
        try:
            value = json.loads(read_head_blob(project, relative))
        except (UnicodeError, json.JSONDecodeError):
            continue
        discovered: set[str] = set()
        add_paths(discovered, value)
        # Some manifests store paths as mapping keys.
        for key in ("active_verifier_hashes", "generated_evidence_sha256",
                    "observed_sha256", "artifacts", "independent_implementations",
                    "bindings"):
            mapping = value.get(key, {}) if isinstance(value, dict) else {}
            if isinstance(mapping, dict):
                discovered.update(path for path in mapping if isinstance(path, str))
        for path in discovered:
            if path in entries and path not in required:
                required.add(path)
                queue.append(path)
    missing = sorted(required - set(entries))
    require(missing == [], ("compact dependency missing at HEAD", missing))
    selected = sorted(required)
    require(len(selected) == policy["expected_compact_selection_count"] and
            sha256_bytes(canonical_json_bytes(selected)) ==
            policy["expected_compact_selection_sha256"],
            ("compact release selection lock", len(selected),
             sha256_bytes(canonical_json_bytes(selected))))
    return selected


def source_zip(project: Path, *, kind: str, commit: str, epoch: int,
               pdf_source_date_epoch: int, tectonic_version: str,
               tectonic_sha256: str, source_paths: list[str]) -> bytes:
    if kind == "article":
        root = "k3p_level2_article_source"
        transform = lambda path: path.removeprefix("manuscript/")
        main = "main.tex"
    else:
        root = "k3p_level2_supplement_source"
        transform = lambda path: Path(path).name
        main = "reader_supplement.tex"
    members = {transform(path): read_head_blob(project, path) for path in source_paths}
    build = {
        "schema": "k3p-tectonic-source-build-v1",
        "kind": kind,
        "source_commit": commit,
        "source_date_epoch": pdf_source_date_epoch,
        "main": main,
        "command": ["tectonic", main, "--outdir", "."],
        "toolchain": {
            "name": "tectonic",
            "version": tectonic_version,
            "executable_sha256": tectonic_sha256,
        },
        "environment": {
            "SOURCE_DATE_EPOCH": str(pdf_source_date_epoch),
            "TZ": "UTC",
            "LC_ALL": "C",
        },
        "expected_output": Path(main).with_suffix(".pdf").name,
    }
    members["SOURCE_BUILD.json"] = (json.dumps(build, indent=2, sort_keys=True) + "\n").encode()
    with tempfile.TemporaryDirectory(prefix="k3p-source-zip-") as directory:
        output = Path(directory) / f"{kind}.zip"
        deterministic_zip(
            output, kind=f"{kind}_latex_source", archive_root=root,
            source_commit=commit, source_date_epoch=epoch, members=members,
            extra={"source_build": "SOURCE_BUILD.json"},
        )
        verify_zip(output)
        return output.read_bytes()


def generated_readme(commit: str) -> bytes:
    return f"""K3P level-2 full reproducibility archive

Source commit: {commit}

Quick verification:
  bash reproducibility/verify_quick.sh

Fresh independent replay (does not run the hour-scale probe producer):
  bash reproducibility/verify_full.sh

All-active-producer regeneration (run once and let it finish):
  K3P_CONFIRM_FULL_REGENERATION=YES bash reproducibility/verify_regenerate_all.sh

Historical or exploratory material is not active theorem evidence.  The
universal arbitrary-network pointwise K3P cut-rank iff claim is withdrawn and
unused.  The active theorem is the directional strong-class cut-transfer
statement bound by FINAL_CLAIM_LOCK.json.

The bundled submission/ tree records its own readiness state.  It is not a
journal-portal or arXiv-ready package unless the independent submission
validator reports READY with zero errors and zero blockers; the final-envelope
gate enforces that condition.
""".encode()


def generated_compact_readme() -> bytes:
    return (
        "Compact K3P containment-classification verifier\n\n"
        "Run: python3 reproducibility/verify_k3p_same_classification.py "
        "--artifact-only --no-write-report\n\n"
        "This portal-size bundle checks the sealed mathematical promotion. "
        "The full external canonical proof archive contains primitive inputs, "
        "all active theorem producers, ledgers, manuscripts, and source archives.\n"
    ).encode()


def require_builder_clean(project: Path, *, allow_dirty: bool) -> list[str]:
    status = scoped_status(project)
    if not allow_dirty:
        require(status == [], ("canonical archive build requires a clean project", status))
    return status


def require_project_output(project: Path, output: Path) -> Path:
    output = output.resolve()
    try:
        output.relative_to(project.resolve())
    except ValueError as error:
        raise ReleaseFailure(("archive output outside project", str(output))) from error
    return output


def run_extracted_gate(root: Path) -> dict:
    command = [
        sys.executable, "reproducibility/verify_k3p_same_classification.py",
        "--artifact-only", "--no-write-report",
    ]
    environment = dict(os.environ)
    environment.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0",
                        "LC_ALL": "C", "TZ": "UTC"})
    result = subprocess.run(
        command, cwd=root, env=environment, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=False, timeout=1_800,
    )
    require(result.returncode == 0 and "K3P_SAME_CLASSIFICATION_GATE_PASS" in result.stdout,
            ("extracted archive artifact replay failed", result.stdout[-4000:]))
    return {"status": "PASS", "transcript_sha256": sha256_bytes(result.stdout.encode()),
            "sentinel": "K3P_SAME_CLASSIFICATION_GATE_PASS"}


def build_compact(project: Path, output: Path, *, allow_dirty: bool = False) -> dict:
    initial_status = require_builder_clean(project, allow_dirty=allow_dirty)
    policy = load_release_policy(project)
    commit, epoch = head_commit(project), head_commit_epoch(project)
    selected = compact_selection(project, policy)
    members = {relative: read_head_blob(project, relative) for relative in selected}
    members["README_VERIFY.txt"] = generated_compact_readme()
    result = deterministic_zip(
        output, kind="compact_verifier", archive_root=policy["compact_root"],
        source_commit=commit, source_date_epoch=epoch, members=members,
        extra={"entrypoint": "reproducibility/verify_k3p_same_classification.py",
               "entrypoint_mode": "--artifact-only --no-write-report",
               "full_archive_is_external_canonical": True},
    )
    structural = verify_zip(output)
    with tempfile.TemporaryDirectory(prefix="k3p-compact-replay-") as directory:
        destination = Path(directory)
        safe_extract_zip(output, destination)
        replay = run_extracted_gate(destination / policy["compact_root"])
    sidecar = output.with_name(output.name + ".sha256")
    atomic_write(sidecar, f"{result['sha256']}  {output.name}\n".encode())
    if not allow_dirty:
        require(scoped_status(project) == initial_status == [],
                "canonical compact build changed the project worktree")
    return {**result, "sidecar": str(sidecar), "structural_verification": structural,
            "extracted_artifact_replay": replay, "selected_head_files": len(selected)}


def build_full(project: Path, output: Path, *, proof_only: bool,
               allow_dirty: bool = False) -> dict:
    initial_status = require_builder_clean(project, allow_dirty=allow_dirty)
    policy = load_release_policy(project)
    commit, epoch = head_commit(project), head_commit_epoch(project)
    selected = full_selection(project, policy, require_pdfs=not proof_only)
    members = {relative: read_head_blob(project, relative) for relative in selected}
    article_sources = [path for path in selected if path == "manuscript/main.tex" or
                       path == "manuscript/references.bib" or
                       path.startswith("manuscript/sections/") or
                       path.startswith("manuscript/figures/")]
    supplement_sources = [path for path in selected if path == "supplement/reader_supplement.tex"]
    article_source = source_zip(
        project, kind="article", commit=commit, epoch=epoch,
        pdf_source_date_epoch=policy["pdf_source_date_epoch"],
        tectonic_version=policy["tectonic_version"],
        tectonic_sha256=policy["tectonic_sha256"],
        source_paths=article_sources,
    )
    supplement_source = source_zip(
        project, kind="supplement", commit=commit, epoch=epoch,
        pdf_source_date_epoch=policy["pdf_source_date_epoch"],
        tectonic_version=policy["tectonic_version"],
        tectonic_sha256=policy["tectonic_sha256"],
        source_paths=supplement_sources,
    )
    members["source_archives/k3p_level2_article_source.zip"] = article_source
    members["source_archives/k3p_level2_supplement_source.zip"] = supplement_source
    source_output_root = output.parent
    article_source_path = source_output_root / "k3p_level2_article_source.zip"
    supplement_source_path = source_output_root / "k3p_level2_supplement_source.zip"
    atomic_write(article_source_path, article_source)
    atomic_write(supplement_source_path, supplement_source)
    members["REPRODUCIBILITY_README.txt"] = generated_readme(commit)
    result = deterministic_tar_gz(
        output, kind="full_reproducibility" if not proof_only else "proof_only_development",
        archive_root=policy["archive_root"], source_commit=commit,
        source_date_epoch=epoch, members=members,
        extra={
            "fileset_policy_sha256": sha256_bytes(
                read_head_blob(project, POLICY_RELATIVE)
            ),
            "source_archives_generated_from_committed_tex": True,
            "release_pdfs_included": not proof_only,
            "untracked_files_included": False,
        },
    )
    structural = verify_tar_gz(output)
    with tempfile.TemporaryDirectory(prefix="k3p-full-replay-") as directory:
        destination = Path(directory)
        safe_extract_tar_gz(output, destination)
        replay = run_extracted_gate(destination / policy["archive_root"])
    sidecar = output.with_name(output.name + ".sha256")
    atomic_write(sidecar, f"{result['sha256']}  {output.name}\n".encode())
    if not allow_dirty:
        require(scoped_status(project) == initial_status == [],
                "canonical full build changed the project worktree")
    return {**result, "sidecar": str(sidecar), "structural_verification": structural,
            "extracted_artifact_replay": replay, "selected_head_files": len(selected),
            "proof_only": proof_only,
            "source_archives": {
                "article": {"path": str(article_source_path),
                            "sha256": sha256_file(article_source_path)},
                "supplement": {"path": str(supplement_source_path),
                               "sha256": sha256_file(supplement_source_path)},
            }}


def project_asset_record(project: Path, path: Path) -> dict:
    path = path.resolve()
    try:
        relative = path.relative_to(project.resolve()).as_posix()
    except ValueError as error:
        raise ReleaseFailure(("release asset outside project", str(path))) from error
    safe_relative_path(relative)
    require(path.is_file(), ("missing release asset", relative))
    return {"path": relative, "bytes": path.stat().st_size, "sha256": sha256_file(path)}


def committed_asset_record(project: Path, relative: str) -> dict:
    entries = tracked_head_entries(project)
    require(relative in entries, ("release PDF is not committed at HEAD", relative))
    path = resolve_inside(project, relative)
    record = project_asset_record(project, path)
    require(path.read_bytes() == read_head_blob(project, relative),
            ("release PDF differs from HEAD", relative))
    return record


def named_asset(value: str) -> tuple[str, Path]:
    require("=" in value, ("named asset must be NAME=PATH", value))
    name, raw_path = value.split("=", 1)
    require(repr(name)[1:-1] == name and name and "/" not in name and "\\" not in name,
            ("unsafe asset name", name))
    return name, Path(raw_path)


def build_envelope(project: Path, args) -> dict:
    require(scoped_status(project) == [],
            ("final envelope requires a clean project worktree", scoped_status(project)))
    commit = head_commit(project)
    epoch = head_commit_epoch(project)
    policy = load_release_policy(project)
    submission_paths = submission_argument_map(args.submission_package)
    readiness = submission_readiness_binding(project)
    readiness_path = HERE / "work/submission_readiness/FINAL_SUBMISSION_READINESS.json"
    atomic_write(readiness_path,
                 (json.dumps(readiness, indent=2, sort_keys=True) + "\n").encode())
    readiness_record = project_asset_record(project, readiness_path)
    tags = exact_head_tags(project)
    require(args.tag in tags, ("tag does not point exactly at HEAD", args.tag, tags))
    article = committed_asset_record(project, ARTICLE_PDF)
    supplement = committed_asset_record(project, SUPPLEMENT_PDF)
    full = project_asset_record(project, args.full_archive)
    compact = project_asset_record(project, args.compact_archive)
    full_sidecar_path = args.full_archive.with_name(args.full_archive.name + ".sha256")
    full_sidecar = project_asset_record(project, full_sidecar_path)
    expected_sidecar = f"{full['sha256']}  {args.full_archive.name}\n"
    require(full_sidecar_path.read_text(encoding="utf-8") == expected_sidecar,
            "full archive sidecar mismatch")
    compact_sidecar_path = args.compact_archive.with_name(args.compact_archive.name + ".sha256")
    compact_sidecar = project_asset_record(project, compact_sidecar_path)
    require(compact_sidecar_path.read_text(encoding="utf-8") ==
            f"{compact['sha256']}  {args.compact_archive.name}\n",
            "compact archive sidecar mismatch")
    source_archives = {
        "article": project_asset_record(
            project, args.full_archive.parent / "k3p_level2_article_source.zip"
        ),
        "supplement": project_asset_record(
            project, args.full_archive.parent / "k3p_level2_supplement_source.zip"
        ),
    }
    full_verification = verify_tar_gz(args.full_archive)
    compact_verification = verify_zip(args.compact_archive)
    require(full_verification["kind"] == "full_reproducibility" and
            compact_verification["kind"] == "compact_verifier" and
            full_verification["source_commit"] == compact_verification["source_commit"] == commit and
            full_verification["source_date_epoch"] ==
            compact_verification["source_date_epoch"] == epoch and
            full_verification["archive_root"] == policy["archive_root"] and
            compact_verification["archive_root"] == policy["compact_root"],
            "archive kind/root/commit/epoch disagreement")
    require(full_verification.get("metadata") == {
        "fileset_policy_sha256": sha256_bytes(read_head_blob(project, POLICY_RELATIVE)),
        "source_archives_generated_from_committed_tex": True,
        "release_pdfs_included": True,
        "untracked_files_included": False,
    }, "full archive metadata binding")
    require(compact_verification.get("metadata") == {
        "entrypoint": "reproducibility/verify_k3p_same_classification.py",
        "entrypoint_mode": "--artifact-only --no-write-report",
        "full_archive_is_external_canonical": True,
    }, "compact archive metadata binding")
    transcripts = [project_asset_record(project, value) for value in args.transcript]
    reproductions = [project_asset_record(project, value) for value in args.reproduction_report]
    transcript_paths = {record["path"] for record in transcripts}
    suite_reports = []
    for record in transcripts:
        if Path(record["path"]).suffix != ".json":
            continue
        value = load_json(resolve_inside(project, record["path"]))
        if value.get("schema") == "k3p-release-suite-report-v1":
            suite_reports.append(verify_suite_report(
                project, resolve_inside(project, record["path"]), transcript_paths
            ))
    require(len(transcripts) == 6 and {row["mode"] for row in suite_reports} ==
            {"quick", "full", "regenerate"},
            "exact quick/full/regeneration report+transcript assets required")
    source_reproduction_transcripts = []
    source_transcript_paths: set[str] = set()
    for record in reproductions:
        report = load_json(resolve_inside(project, record["path"]))
        for build in report.get("builds", []):
            require(isinstance(build, dict) and isinstance(build.get("transcript"), str),
                    "source reproduction transcript reference")
            relative = build["transcript"]
            require(relative not in source_transcript_paths,
                    ("duplicate source reproduction transcript", relative))
            source_transcript_paths.add(relative)
            source_reproduction_transcripts.append(project_asset_record(
                project, resolve_inside(project, relative)
            ))
    require(len(source_reproduction_transcripts) == 4,
            "two source-reproduction transcripts per PDF required")
    submissions = {}
    submission_contracts = {}
    for name, path in submission_paths.items():
        submission_contracts[name] = verify_submission_package(
            path.resolve(), kind=name, commit=commit,
            expected_uploads=(uploads := expected_submission_uploads(project, name)),
            expected_members=expected_submission_members(project, name, uploads),
        )
        submissions[name] = project_asset_record(project, path)
    require(len(reproductions) == 2, "article and supplement source-reproduction reports required")
    assets = {
        "article_pdf": article,
        "supplement_pdf": supplement,
        "full_reproducibility_archive": full,
        "full_reproducibility_archive_sidecar": full_sidecar,
        "compact_verifier_archive": compact,
        "compact_verifier_archive_sidecar": compact_sidecar,
        "latex_source_archives": source_archives,
        "clean_clone_transcripts": transcripts,
        "source_reproduction_reports": reproductions,
        "source_reproduction_transcripts": source_reproduction_transcripts,
        "submission_readiness_report": readiness_record,
        "submission_packages": submissions,
    }
    flat = [article, supplement, full, full_sidecar, compact, compact_sidecar,
            *source_archives.values(), *transcripts, *reproductions,
            *source_reproduction_transcripts, readiness_record, *submissions.values()]
    unique_paths = {row["path"] for row in flat}
    require(len(unique_paths) == len(flat), "duplicate release asset path")
    checksum_lines = [f"{row['sha256']}  {row['path']}" for row in sorted(flat,
                      key=lambda value: value["path"])]
    checksums_path = HERE / "RELEASE_ASSET_SHA256SUMS"
    atomic_write(checksums_path, ("\n".join(checksum_lines) + "\n").encode())
    envelope = {
        "schema": "k3p-final-release-envelope-v1",
        "status": "ASSETS_BOUND_EXTERNAL_HUMAN_ACTIONS_PENDING",
        "source_commit": commit,
        "tag": args.tag,
        "assets": assets,
        "submission_package_contracts": submission_contracts,
        "release_asset_checksums": project_asset_record(project, checksums_path),
        "self_reference_policy": {
            "full_archive_contains_its_own_hash": False,
            "full_archive_contains_release_envelope": False,
            "checksum_list_contains_itself": False,
            "envelope_hash_is_not_embedded_in_envelope": True,
        },
        "doi": {"status": "NOT_MINTED", "value": None},
        "license": {"status": "NOT_AUTHORIZED_OR_SELECTED", "value": None},
        "github_release": {"created": False},
        "zenodo_record": {"created": False},
        "external_submission_performed": False,
        "human_only_remaining": [
            "authorize explicit licenses",
            "create immutable GitHub release after final human audit",
            "mint Zenodo DOI",
            "rebuild DOI-bearing PDFs and submission packages",
            "perform journal portal submissions",
        ],
        "tag_scope": "LOCAL_EXACT_HEAD_TAG_EXTERNAL_PUSH_NOT_VERIFIED",
    }
    envelope["payload_sha256"] = sha256_bytes(canonical_json_bytes(envelope))
    output = HERE / "RELEASE_ENVELOPE.json"
    atomic_write(output, (json.dumps(envelope, indent=2, sort_keys=True) + "\n").encode())
    return {"envelope": project_asset_record(project, output),
            "checksum_list": envelope["release_asset_checksums"],
            "payload_sha256": envelope["payload_sha256"]}


def main(argv: list[str] | None = None) -> int:
    try:
        refuse_optimized_python()
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command", required=True)
        plan = subparsers.add_parser("plan")
        plan.add_argument("--kind", choices=("compact", "full"), required=True)
        plan.add_argument("--proof-only", action="store_true")
        compact = subparsers.add_parser("compact")
        compact.add_argument("--output", type=Path, default=COMPACT_ARCHIVE)
        compact.add_argument("--allow-dirty", action="store_true",
                             help="development only; canonical release builds forbid this")
        full = subparsers.add_parser("full")
        full.add_argument("--output", type=Path, default=FULL_ARCHIVE)
        full.add_argument("--allow-dirty", action="store_true",
                          help="development only; canonical release builds forbid this")
        full.add_argument("--proof-only", action="store_true",
                          help="development artifact; canonical filename is refused")
        envelope = subparsers.add_parser("envelope")
        envelope.add_argument("--tag", required=True)
        envelope.add_argument("--full-archive", type=Path, default=FULL_ARCHIVE)
        envelope.add_argument("--compact-archive", type=Path, default=COMPACT_ARCHIVE)
        envelope.add_argument("--transcript", type=Path, action="append", default=[])
        envelope.add_argument("--reproduction-report", type=Path, action="append", default=[])
        envelope.add_argument("--submission-package", action="append", default=[])
        args = parser.parse_args(argv)
        policy = load_release_policy(PROJECT)
        if args.command == "plan":
            selected = (compact_selection(PROJECT, policy) if args.kind == "compact" else
                        full_selection(PROJECT, policy, require_pdfs=not args.proof_only))
            result = {"status": "PASS", "kind": args.kind, "source_commit": head_commit(PROJECT),
                      "selected_head_files": len(selected),
                      "selection_sha256": sha256_bytes(canonical_json_bytes(selected))}
        elif args.command == "compact":
            output = require_project_output(PROJECT, args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            result = build_compact(PROJECT, output, allow_dirty=args.allow_dirty)
        elif args.command == "full":
            output = require_project_output(PROJECT, args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            if args.proof_only:
                require(output != FULL_ARCHIVE.resolve(),
                        "proof-only build cannot use canonical full-archive filename")
            result = build_full(PROJECT, output, proof_only=args.proof_only,
                                allow_dirty=args.allow_dirty)
        else:
            result = build_envelope(PROJECT, args)
        print(json.dumps(result, indent=2, sort_keys=True))
        print("K3P_RELEASE_BUILD_PASS")
        return 0
    except (ReleaseFailure, OSError, UnicodeError, json.JSONDecodeError,
            subprocess.SubprocessError) as error:
        print(f"K3P_RELEASE_BUILD_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
