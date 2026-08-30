#!/usr/bin/env python3
"""Build the exact direct-Zenodo v1.0.0 upload set and metadata guide."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[2]
RELEASE = PROJECT / "release"
DIST = RELEASE / "dist"
VERSION = "1.0.0"
TAG = "k3p-level2-identifiability-v1.0.0"
PUBLICATION_DATE = "2026-08-30"
TITLE = "Triangle Hypersurfaces and a Sharp Identifiability Boundary for Level-2 K3P Networks"
DEFAULT_OUTPUT = DIST / f"zenodo_v{VERSION}"
DEFAULT_REFEREE = DIST / f"K3P_Level2_Independent_Referee_Package_v{VERSION}"
KEYWORDS = (
    "phylogenetic networks", "Kimura three-parameter model", "K3P",
    "generic identifiability", "directed containment", "level-2 networks",
    "strongly tree-child networks", "semi-directed networks",
    "algebraic statistics", "phylogenetic invariants",
    "continuous-time Markov models", "computer-assisted proof",
    "reproducible mathematics", "reticulate evolution",
)

sys.path.insert(0, str(RELEASE))
sys.path.insert(0, str(PROJECT / "reproducibility"))
from archive_tools import (  # noqa: E402
    canonical_mode,
    verify_tar_gz,
    verify_zip,
    zip_datetime,
)
from build_release import (  # noqa: E402
    compact_selection,
    full_selection,
    generated_compact_readme,
    generated_readme,
    load_release_policy,
)
from verify_release import validate_source_reproduction_evidence  # noqa: E402
from verify_source_reproduction import verify_source_archive_contract  # noqa: E402
from release_common import ReleaseFailure  # noqa: E402


class ZenodoBuildFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ZenodoBuildFailure(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(PROJECT), *arguments],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        check=False, timeout=60,
    )
    require(result.returncode == 0,
            ("Git command failed", arguments, result.stderr.strip()))
    return result.stdout.strip()


def head_blob(relative: str) -> bytes:
    prefix = git("rev-parse", "--show-prefix")
    require(prefix == "k3p_level2_identifiability_final/",
            ("unexpected monorepo project prefix", prefix))
    result = subprocess.run(
        ["git", "-C", str(PROJECT), "show", f"HEAD:{prefix}{relative}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=60,
    )
    require(result.returncode == 0, ("missing HEAD blob", relative))
    return result.stdout


def require_release_identity() -> tuple[str, int]:
    require(sys.flags.optimize == 0, "optimized Python is forbidden")
    require(git("status", "--porcelain", "--", ".") == "",
            "Zenodo build requires a clean K3P project")
    commit = git("rev-parse", "HEAD")
    require(commit == git("rev-parse", "origin/main"),
            "HEAD must equal origin/main before the Zenodo build")
    require(git("cat-file", "-t", f"refs/tags/{TAG}") == "tag",
            ("release tag must be annotated", TAG))
    require(git("rev-parse", f"{TAG}^{{}}") == commit,
            ("release tag does not point to HEAD", TAG, commit))
    require(dt.datetime.now(dt.timezone.utc).date().isoformat() == PUBLICATION_DATE,
            ("publication date is no longer current; update and reseal before "
             "publishing", PUBLICATION_DATE))
    epoch_text = git("show", "-s", "--format=%ct", commit)
    require(epoch_text.isdigit(), ("invalid commit epoch", epoch_text))
    return commit, int(epoch_text)


def require_head_file(relative: str) -> Path:
    path = PROJECT / relative
    require(path.is_file() and not path.is_symlink(),
            ("required regular file missing", relative))
    require(path.read_bytes() == head_blob(relative),
            ("release input differs from HEAD", relative))
    return path


def regular_folder_members(root: Path) -> dict[str, tuple[bytes, int]]:
    require(root.is_dir() and not root.is_symlink(),
            ("referee package must be a real directory", str(root)))
    forbidden_parts = {".git", ".venv", "review_runs", "__pycache__"}
    members: dict[str, tuple[bytes, int]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        require(not stat.S_ISLNK(metadata.st_mode),
                ("symlink forbidden in referee package", relative))
        if stat.S_ISDIR(metadata.st_mode):
            continue
        require(stat.S_ISREG(metadata.st_mode),
                ("nonregular referee package member", relative))
        require(not (set(path.relative_to(root).parts) & forbidden_parts),
                ("runtime or VCS member forbidden", relative))
        require(not relative.endswith((".pyc", ".pyo")),
                ("bytecode forbidden", relative))
        require(path.name != ".DS_Store" and not path.name.startswith("._"),
                ("macOS metadata forbidden", relative))
        members[relative] = (path.read_bytes(), stat.S_IMODE(metadata.st_mode))
    require(members, "empty referee package")
    return members


def deterministic_folder_zip(output: Path, *, archive_root: str,
                             source_date_epoch: int,
                             members: dict[str, tuple[bytes, int]]) -> None:
    """Create a deterministic ZIP while preserving the referee seal's modes."""
    require("/" not in archive_root and archive_root not in {"", ".", ".."},
            ("unsafe ZIP root", archive_root))
    buffer = io.BytesIO()
    with zipfile.ZipFile(
        buffer, mode="w", compression=zipfile.ZIP_DEFLATED,
        compresslevel=9, strict_timestamps=True,
    ) as archive:
        for relative in sorted(members):
            pure = PurePosixPath(relative)
            require(not pure.is_absolute() and ".." not in pure.parts and
                    pure.as_posix() == relative,
                    ("unsafe referee ZIP member", relative))
            data, mode = members[relative]
            require(mode in {0o644, 0o755},
                    ("noncanonical referee file mode", relative, oct(mode)))
            info = zipfile.ZipInfo(
                f"{archive_root}/{relative}",
                date_time=zip_datetime(source_date_epoch),
            )
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.flag_bits = 0x800
            archive.writestr(
                info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9
            )
    write_bytes(output, buffer.getvalue())


def extract_referee_zip(path: Path, destination: Path, archive_root: str,
                        source_date_epoch: int) -> Path:
    """Validate and safely extract a deterministic referee ZIP."""
    expected_prefix = archive_root + "/"
    seen: set[str] = set()
    expected_time = zip_datetime(source_date_epoch)
    with zipfile.ZipFile(path, mode="r") as archive:
        require(archive.comment == b"", "referee ZIP archive comment")
        require(archive.testzip() is None, "referee ZIP CRC failure")
        names = [info.filename for info in archive.infolist()]
        require(names == sorted(names) and len(names) == len(set(names)) and names,
                "referee ZIP ordering or duplication")
        for info in archive.infolist():
            require(not info.is_dir() and info.filename.startswith(expected_prefix),
                    ("referee ZIP root", info.filename))
            relative = info.filename.removeprefix(expected_prefix)
            pure = PurePosixPath(relative)
            require(not pure.is_absolute() and ".." not in pure.parts and
                    pure.as_posix() == relative and relative not in seen,
                    ("unsafe referee ZIP path", relative))
            seen.add(relative)
            mode = (info.external_attr >> 16) & 0o7777
            require(mode in {0o644, 0o755},
                    ("referee ZIP mode", relative, oct(mode)))
            require(info.create_system == 3 and
                    (info.external_attr >> 16) == (stat.S_IFREG | mode) and
                    info.compress_type == zipfile.ZIP_DEFLATED and
                    info.extra == b"" and info.comment == b"" and
                    info.date_time == expected_time,
                    ("referee ZIP canonical metadata", relative))
            target = (destination / archive_root / relative).resolve()
            target.relative_to(destination.resolve())
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(info))
            target.chmod(mode)
    require("PACKAGE_MANIFEST.json" in seen and "SHA256SUMS" in seen,
            "referee ZIP seal files")
    return destination / archive_root


def asset_record(path: Path, role: str, media_type: str) -> dict[str, object]:
    return {
        "path": path.name,
        "role": role,
        "media_type": media_type,
        "bytes": path.stat().st_size,
        "sha256": sha256_file(path),
    }


def write_bytes(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(value)
    temporary.chmod(0o644)
    os.replace(temporary, path)


def write_text(path: Path, value: str) -> None:
    write_bytes(path, value.encode("utf-8"))


def copy_asset(source: Path, destination: Path) -> None:
    require(source.is_file() and not source.is_symlink(),
            ("missing release asset", str(source)))
    write_bytes(destination, source.read_bytes())


def tar_member_bytes(path: Path, archive_root: str, relative: str) -> bytes:
    with tarfile.open(path, mode="r:gz") as archive:
        handle = archive.extractfile(f"{archive_root}/{relative}")
        require(handle is not None, ("unreadable full-archive member", relative))
        return handle.read()


def tar_members(path: Path, archive_root: str) -> dict[str, bytes]:
    observed: dict[str, bytes] = {}
    with tarfile.open(path, mode="r:gz") as archive:
        prefix = archive_root + "/"
        for info in archive.getmembers():
            require(info.name.startswith(prefix), ("full archive root", info.name))
            relative = info.name.removeprefix(prefix)
            handle = archive.extractfile(info)
            require(handle is not None, ("unreadable full archive member", relative))
            observed[relative] = handle.read()
    return observed


def zip_members(path: Path, archive_root: str) -> dict[str, bytes]:
    with zipfile.ZipFile(path, mode="r") as archive:
        prefix = archive_root + "/"
        require(all(info.filename.startswith(prefix) for info in archive.infolist()),
                ("ZIP archive root", path.name))
        return {
            info.filename.removeprefix(prefix): archive.read(info)
            for info in archive.infolist()
        }


def run_extracted_gate(root: Path) -> str:
    environment = {
        "PATH": "/usr/bin:/bin",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
        "LC_ALL": "C",
        "TZ": "UTC",
    }
    result = subprocess.run(
        [sys.executable, "reproducibility/verify_k3p_same_classification.py",
         "--artifact-only", "--no-write-report"],
        cwd=root, env=environment, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, check=False, timeout=1_800,
    )
    require(result.returncode == 0 and
            "K3P_SAME_CLASSIFICATION_GATE_PASS" in result.stdout,
            ("extracted artifact gate failed", result.stdout[-4000:]))
    return sha256_bytes(result.stdout.encode())


def run_trusted_referee_integrity(package: Path, trusted_verifier: Path) -> str:
    result = subprocess.run(
        [sys.executable, str(trusted_verifier), "--package-root", str(package)],
        cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, check=False, timeout=600,
    )
    require(result.returncode == 0 and
            "K3P_REFEREE_PACKAGE_INTEGRITY_PASS" in result.stdout,
            ("trusted referee-package integrity failed", result.stdout[-4000:]))
    return sha256_bytes(result.stdout.encode())


def tracked_paths(pathspec: str) -> list[str]:
    rows = git("ls-files", "--", pathspec).splitlines()
    require(rows == sorted(rows) and len(rows) == len(set(rows)),
            ("tracked path enumeration", pathspec))
    return rows


def validate_referee_payload(package: Path,
                             full_members: dict[str, bytes]) -> \
        dict[str, tuple[bytes, int]]:
    members = regular_folder_members(package)
    tool_sources = [
        relative for relative in tracked_paths("referee_handoff/referee_tools/**")
        if relative.endswith((".py", ".json"))
    ]
    require(len(tool_sources) == 4, ("referee tool source count", tool_sources))
    interface_sources = {
        "START_HERE.md": "referee_handoff/START_HERE.md",
        "REFEREE_PROMPT.md": "referee_handoff/REFEREE_PROMPT.md",
        "RUN_REVIEW.sh": "referee_handoff/RUN_REVIEW.sh",
        **{
            relative.removeprefix("referee_handoff/"): relative
            for relative in tool_sources
        },
    }
    for destination, source in interface_sources.items():
        expected_mode = 0o755 if destination == "RUN_REVIEW.sh" or \
            destination.endswith(".py") else 0o644
        require(destination in members and
                members[destination] == (head_blob(source), expected_mode),
                ("referee interface/tag binding", destination, source))

    work_logs = tracked_paths("*WORK_LOG.md")
    require(len(work_logs) == 20, ("referee tracked work-log count", len(work_logs)))
    evidence = [
        "release/source_reproduction_evidence/article.json",
        "release/source_reproduction_evidence/supplement.json",
        "release/source_reproduction_evidence/article_transcripts/run1.log",
        "release/source_reproduction_evidence/article_transcripts/run2.log",
        "release/source_reproduction_evidence/supplement_transcripts/run1.log",
        "release/source_reproduction_evidence/supplement_transcripts/run2.log",
        "release/dist/k3p_level2_article_source.zip",
        "release/dist/k3p_level2_supplement_source.zip",
    ]
    proof_extras = work_logs + ["release/FINAL_RELEASE_ENGINEERING_REPORT.md"] + evidence
    expected_proof = set(full_members) | set(proof_extras)
    observed_proof = {
        relative.removeprefix("proof_package/")
        for relative in members if relative.startswith("proof_package/")
    }
    require(observed_proof == expected_proof,
            ("referee proof-package exact file set",
             sorted(expected_proof - observed_proof),
             sorted(observed_proof - expected_proof)))
    for relative, data in full_members.items():
        require(members[f"proof_package/{relative}"] == (
                    data, canonical_mode(relative)
                ),
                ("referee/full archive byte mismatch", relative))
    for relative in work_logs + ["release/FINAL_RELEASE_ENGINEERING_REPORT.md"]:
        require(members[f"proof_package/{relative}"] == (
                    head_blob(relative), 0o644
                ),
                ("referee tracked extra/tag binding", relative))
    for relative in evidence:
        path = PROJECT / relative
        require(path.is_file() and not path.is_symlink() and
                members[f"proof_package/{relative}"] == (path.read_bytes(), 0o644),
                ("referee ignored evidence/local binding", relative))

    paper_names = {
        "paper/K3P_Level2_Identifiability_Article.pdf":
            "output/pdf/K3P_Level2_Identifiability_Article.pdf",
        "paper/K3P_Level2_Identifiability_Reader_Supplement.pdf":
            "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf",
    }
    for destination, source in paper_names.items():
        require(destination in members and
                members[destination] == (head_blob(source), 0o644),
                ("referee paper/tag binding", destination))
    expected_package = (
        {f"proof_package/{relative}" for relative in expected_proof} |
        set(interface_sources) | set(paper_names) |
        {"PACKAGE_MANIFEST.json", "SHA256SUMS"}
    )
    require(set(members) == expected_package,
            ("referee package exact file set",
             sorted(expected_package - set(members)),
             sorted(set(members) - expected_package)))
    require(members["PACKAGE_MANIFEST.json"][1] == 0o644 and
            members["SHA256SUMS"][1] == 0o644,
            "referee outer seal modes")
    return members


def validate_source_evidence(commit: str, referee: Path) -> list[dict[str, object]]:
    policy = load_release_policy(PROJECT)
    rows = []
    for kind, pdf_name in (
        ("article", "K3P_Level2_Identifiability_Article.pdf"),
        ("supplement", "K3P_Level2_Identifiability_Reader_Supplement.pdf"),
    ):
        report_path = RELEASE / "source_reproduction_evidence" / f"{kind}.json"
        require(report_path.is_file() and not report_path.is_symlink(),
                ("missing source-reproduction report", kind))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        pdf = PROJECT / "output/pdf" / pdf_name
        source_relative = f"release/dist/k3p_level2_{kind}_source.zip"
        source_archive = PROJECT / source_relative
        archive_report, _build, committed_binding = verify_source_archive_contract(
            source_archive, kind=kind, project=PROJECT, policy=policy
        )
        expected_source_record = {
            "path": source_relative,
            "sha256": sha256_file(source_archive),
            "structural_verification": archive_report,
        }
        require(report.get("source_archive") == expected_source_record and
                report.get("committed_source_binding") == committed_binding,
                ("source archive/report semantic binding", kind))
        transcript_records: dict[str, dict[str, str]] = {}
        transcript_rows = []
        for run_number in (1, 2):
            relative = (
                "release/source_reproduction_evidence/"
                f"{kind}_transcripts/run{run_number}.log"
            )
            transcript = PROJECT / relative
            require(transcript.is_file() and not transcript.is_symlink(),
                    ("source-reproduction transcript missing", kind, run_number))
            transcript_records[relative] = {"sha256": sha256_file(transcript)}
            transcript_rows.append({
                "run": run_number,
                "sealed_path": f"proof_package/{relative}",
                "sha256": sha256_file(transcript),
            })
        validate_source_reproduction_evidence(
            report, kind=kind, commit=commit,
            pdf_record={"sha256": sha256_file(pdf), "bytes": pdf.stat().st_size},
            policy=policy, transcript_records=transcript_records,
        )

        sealed_paths = [
            (report_path, f"proof_package/{report_path.relative_to(PROJECT).as_posix()}"),
            (source_archive, f"proof_package/{source_relative}"),
            *[
                (PROJECT / row["sealed_path"].removeprefix("proof_package/"),
                 row["sealed_path"])
                for row in transcript_rows
            ],
        ]
        for local, sealed_relative in sealed_paths:
            sealed = referee / sealed_relative
            require(sealed.is_file() and not sealed.is_symlink() and
                    sealed.read_bytes() == local.read_bytes(),
                    ("referee/local source evidence mismatch", sealed_relative))
        rows.append({
            "kind": kind,
            "report_path": report_path.relative_to(PROJECT).as_posix(),
            "sealed_report_path": (
                "proof_package/" + report_path.relative_to(PROJECT).as_posix()
            ),
            "report_sha256": sha256_file(report_path),
            "source_archive_path": source_relative,
            "sealed_source_archive_path": f"proof_package/{source_relative}",
            "source_archive_sha256": sha256_file(source_archive),
            "transcripts": transcript_rows,
            "pdf_sha256": sha256_file(pdf),
            "two_builds_match_release_pdf": True,
        })
    return rows


def description_text(commit: str, full_sha256: str) -> str:
    return f"""We classify regular full-dimensional stochastic containment among binary standard semi-directed strongly tree-child level-2 phylogenetic networks under the Kimura three-parameter (K3P) model. On the principal positive Fourier domain, a directed containment germ exists if and only if the labelled reduced trees of blobs agree and corresponding complete factors are either labelled-isomorphic or ordinarily triangle-redirected, with coherent boundary transports. The same condition is equivalent to a common full-dimensional regular germ and remains exact in strict continuous time. Thus no proper one-sided containment occurs in the strong class, and the semi-directed topology is generically identifiable and exactly reconstructible outside a proper exceptional set, modulo ordinary triangle redirection.

The three ordinary K3P triangle orientations have generic normalized rank 14, share the same irreducible eight-term quartic hypersurface H₁₄ in normalized three-leaf Fourier space, and meet in a common strict continuous-time smooth rank-14 germ. The bounded residue consists of fourteen four-port directed relation orbits—nine polynomially separated and five directed-rank separated—plus two separately separated sink swaps. Exact restoration and coherent one- and two-port probes extend the bounded classification to arbitrary labelled subdivision words.

Strong tree-childness is sharp against weakening to weak tree-childness. For every n ≥ 3, two weakly but not strongly tree-child networks have strict continuous-time K3P images sharing a common full-dimensional regular germ of dimension 6n − 3.

This is the first Zenodo/DOI-bearing archival release of version {VERSION} of the complete K3P level-2 classification and its reproducibility evidence. It contains the article, reader supplement, compile-complete source archives, canonical full proof archive, compact verifier, independent-referee replay package, exact manifest, checksums, citation metadata, and a file-level license notice. The deposited bytes correspond to immutable Git commit {commit}, annotated tag {TAG} resolving to that commit, and full-archive SHA-256 {full_sha256}.

The archive includes the previously completed all-producer regeneration evidence bound to unchanged mathematical inputs, together with successful exact and independently implemented replays, rigorous interval arithmetic where required, and fail-closed mutation tests. The present release changes bibliography, nonmathematical administrative/public-release prose, and release engineering only; unchanged multi-hour mathematical producers were not rerun during this dependency-scoped reseal. No empirical data set is used.

Preprint; not peer reviewed by a journal. Generative-AI assistance and its verification workflow are disclosed in the article. Article, supplement, figures, documentation, and mathematical certificate data are licensed under CC BY 4.0; original verifier and build code are licensed under MIT, as mapped in LICENSES.md. No specific funding supported this work. The author declares no competing interests."""


def metadata_guide(*, commit: str, full_sha256: str,
                   records: list[dict[str, object]], description: str) -> str:
    file_lines = "\n".join(
        f"{index}. `{row['path']}` — {row['bytes']} bytes — SHA-256 `{row['sha256']}`"
        for index, row in enumerate(records, 1)
    )
    keywords = "\n".join(f"- `{value}`" for value in KEYWORDS)
    return f"""# Zenodo metadata and upload guide — K3P level-2 v{VERSION}

This guide stays local. Upload **only** the files in `UPLOAD_THESE_FILES/`.
Publishing the record, rather than saving a draft or merely reserving a DOI,
creates the Zenodo record's public timestamped archival disclosure.

## Record fields

- **Upload type / resource type:** Publication → Preprint
- **Title:** {TITLE}
- **Publication date:** {PUBLICATION_DATE}
- **Version:** {VERSION}
- **Language:** English
- **Access:** Public / Open access
- **License:** add both `Creative Commons Attribution 4.0 International` and `MIT License`
- **Publisher:** leave Zenodo's default
- **DOI:** do not enter or predict one; let Zenodo assign it when the record is published
- **Community:** none required
- **Preview/default file:** select `K3P_Level2_Identifiability_Article_v{VERSION}.pdf`

## Creator

- **Family name:** Kriebel
- **Given name:** Alec
- **Affiliation:** Independent Researcher
- **ORCID:** 0009-0001-9320-500X
- **Creator role:** leave blank (optional)
- **Contributors:** none

## Description — copy and paste into Zenodo's Description field

```text
{description}
```

## Keywords

{keywords}

## Related works

Add these four identifiers:

| Identifier | Relation | Resource type |
|---|---|---|
| `10.5281/zenodo.22089373` | References | Publication → Preprint |
| `10.5281/zenodo.22168797` | References | Publication → Preprint |
| `10.5281/zenodo.22136869` | References | Publication → Preprint |
| `https://github.com/AlecKriebel/Math/tree/{commit}/k3p_level2_identifiability_final` | Is derived from | Software |

The collision record's public metadata has inconsistent version text, so this
release deliberately cites its DOI and title without repeating a version.

## Exact files to upload

{file_lines}

The full reproducibility archive SHA-256 is `{full_sha256}`. The exact source
commit is `{commit}` and the annotated tag is `{TAG}`.

## Before clicking Publish

1. Confirm all listed files are present and no extra file is attached.
2. Compare every displayed byte size with this guide. Zenodo commonly displays
   MD5 rather than SHA-256; the authoritative SHA-256 values are in this guide
   and `SHA256SUMS` and are checked after downloading the published files.
3. Confirm that the actual Zenodo publication date is still {PUBLICATION_DATE}.
   If publication is delayed to another date, stop and regenerate the manifest,
   guide, commit, tag, and checksums rather than backdating the record.
4. Preview both PDFs, with the article selected as the default preview.
5. Recheck title, creator, ORCID, version, date, both licenses, and all four
   related identifiers.
6. Confirm the remote annotated tag `{TAG}` resolves to `{commit}`.
7. Publish the record. A draft or reserved DOI is not yet a public release.

## Immediately after publication

1. Copy the issued DOI and landing-page URL into the local release ledger and
   future citation metadata.
2. Download every deposited file and verify it against `SHA256SUMS`.
3. Confirm the DOI resolves and the record is publicly visible.
4. Do not rebuild, replace, move, or retag version {VERSION} solely to embed
   its DOI. Any later byte revision must use a new version, commit, tag,
   manifest, and checksum set.

This is a scholarly public-disclosure record, not legal advice about patent or
other jurisdiction-specific priority rules.
"""


def build(output: Path, referee: Path) -> dict[str, object]:
    commit, epoch = require_release_identity()
    require(not output.exists(), ("output already exists", str(output)))

    article = require_head_file(
        "output/pdf/K3P_Level2_Identifiability_Article.pdf"
    )
    supplement = require_head_file(
        "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf"
    )
    licenses = require_head_file("LICENSES.md")
    citation = require_head_file("CITATION.cff")
    qa_article = json.loads(require_head_file(
        "output/pdf/K3P_Level2_Identifiability_Article.visual_qa.json"
    ).read_text(encoding="utf-8"))
    qa_supplement = json.loads(require_head_file(
        "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.visual_qa.json"
    ).read_text(encoding="utf-8"))
    require(qa_article.get("status") == qa_supplement.get("status") == "PASS" and
            qa_article.get("pdf_sha256") == sha256_file(article) and
            qa_supplement.get("pdf_sha256") == sha256_file(supplement),
            "visual-QA bindings do not match the release PDFs")

    full = DIST / "k3p_level2_reproducibility.tar.gz"
    compact = DIST / "k3p_level2_compact_verifier.zip"
    article_source = DIST / "k3p_level2_article_source.zip"
    supplement_source = DIST / "k3p_level2_supplement_source.zip"
    full_info = verify_tar_gz(full)
    compact_info = verify_zip(compact)
    article_source_info = verify_zip(article_source)
    supplement_source_info = verify_zip(supplement_source)
    for label, record, expected_kind, expected_root in (
        ("full", full_info, "full_reproducibility", "k3p_level2_reproducibility"),
        ("compact", compact_info, "compact_verifier", "k3p_level2_compact_verifier"),
        ("article source", article_source_info, "article_latex_source",
         "k3p_level2_article_source"),
        ("supplement source", supplement_source_info, "supplement_latex_source",
         "k3p_level2_supplement_source"),
    ):
        require(record.get("source_commit") == commit and
                record.get("kind") == expected_kind and
                record.get("archive_root") == expected_root and
                record.get("source_date_epoch") == epoch,
                ("archive identity or source commit", label, record))
    policy = load_release_policy(PROJECT)
    require(full_info.get("metadata") == {
        "fileset_policy_sha256": sha256_file(RELEASE / "RELEASE_FILESET.json"),
        "source_archives_generated_from_committed_tex": True,
        "release_pdfs_included": True,
        "untracked_files_included": False,
    }, "full-archive metadata policy")
    require(compact_info.get("metadata") == {
        "entrypoint": "reproducibility/verify_k3p_same_classification.py",
        "entrypoint_mode": "--artifact-only --no-write-report",
        "full_archive_is_external_canonical": True,
    }, "compact-archive metadata policy")
    full_member_map = tar_members(full, policy["archive_root"])
    selected_full = set(full_selection(PROJECT, policy, require_pdfs=True))
    generated_full = {
        "ARCHIVE_MANIFEST.json", "REPRODUCIBILITY_README.txt",
        "source_archives/k3p_level2_article_source.zip",
        "source_archives/k3p_level2_supplement_source.zip",
    }
    require(set(full_member_map) == selected_full | generated_full,
            "full archive exact committed-fileset coverage")
    for relative in selected_full:
        require(full_member_map[relative] == head_blob(relative),
                ("full archive differs from HEAD", relative))
    require(full_member_map["REPRODUCIBILITY_README.txt"] == generated_readme(commit),
            "full archive generated README binding")
    compact_member_map = zip_members(compact, policy["compact_root"])
    selected_compact = set(compact_selection(PROJECT, policy))
    require(set(compact_member_map) == selected_compact | {
        "ARCHIVE_MANIFEST.json", "README_VERIFY.txt"
    }, "compact archive exact committed-fileset coverage")
    for relative in selected_compact:
        require(compact_member_map[relative] == head_blob(relative),
                ("compact archive differs from HEAD", relative))
    require(compact_member_map["README_VERIFY.txt"] == generated_compact_readme(),
            "compact archive generated README binding")
    for source, relative in (
        (article_source, "source_archives/k3p_level2_article_source.zip"),
        (supplement_source, "source_archives/k3p_level2_supplement_source.zip"),
    ):
        require(full_member_map[relative] == source.read_bytes(),
                ("full/external source archive mismatch", relative))

    referee_manifest_path = referee / "PACKAGE_MANIFEST.json"
    require(referee_manifest_path.is_file(),
            ("missing referee package manifest", str(referee_manifest_path)))
    referee_manifest = json.loads(referee_manifest_path.read_text(encoding="utf-8"))
    require(referee_manifest.get("package_builder_commit") == commit and
            referee_manifest.get("proof_source_commit") == commit and
            referee_manifest.get("canonical_archive_sha256") == sha256_file(full),
            "referee package is not bound to the final commit/archive")
    trusted_referee_verifier = require_head_file(
        "referee_handoff/referee_tools/verify_package_integrity.py"
    )
    run_trusted_referee_integrity(referee, trusted_referee_verifier)
    for relative, data in full_member_map.items():
        sealed = referee / "proof_package" / relative
        require(sealed.is_file() and not sealed.is_symlink() and
                sealed.read_bytes() == data,
                ("referee/full archive byte mismatch", relative))
    require((referee / "paper/K3P_Level2_Identifiability_Article.pdf").read_bytes()
            == article.read_bytes() and
            (referee / "paper/K3P_Level2_Identifiability_Reader_Supplement.pdf").read_bytes()
            == supplement.read_bytes(),
            "referee paper/direct PDF binding")
    for source, relative in (
        (article, "output/pdf/K3P_Level2_Identifiability_Article.pdf"),
        (supplement, "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf"),
        (licenses, "LICENSES.md"),
        (citation, "CITATION.cff"),
    ):
        expected = source.read_bytes()
        require(tar_member_bytes(full, policy["archive_root"], relative) == expected,
                ("full/direct asset mismatch", relative))
        sealed = referee / "proof_package" / relative
        require(sealed.is_file() and not sealed.is_symlink() and
                sealed.read_bytes() == expected,
                ("referee/direct asset mismatch", relative))
    source_evidence = validate_source_evidence(commit, referee)
    referee_members = validate_referee_payload(referee, full_member_map)

    work_root = RELEASE / "work"
    work_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="zenodo-archive-gates-",
                                     dir=work_root) as directory:
        temporary = Path(directory)
        from archive_tools import safe_extract_tar_gz, safe_extract_zip
        safe_extract_zip(compact, temporary / "compact")
        compact_replay = run_extracted_gate(
            temporary / "compact" / policy["compact_root"]
        )
        safe_extract_tar_gz(full, temporary / "full")
        full_replay = run_extracted_gate(
            temporary / "full" / policy["archive_root"]
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="zenodo-v1-", dir=work_root) as directory:
        staging = Path(directory) / output.name
        upload = staging / "UPLOAD_THESE_FILES"
        upload.mkdir(parents=True)

        names = {
            "article": f"K3P_Level2_Identifiability_Article_v{VERSION}.pdf",
            "supplement": f"K3P_Level2_Identifiability_Reader_Supplement_v{VERSION}.pdf",
            "article_source": f"K3P_Level2_Article_Source_v{VERSION}.zip",
            "supplement_source": f"K3P_Level2_Supplement_Source_v{VERSION}.zip",
            "full": f"K3P_Level2_Full_Reproducibility_v{VERSION}.tar.gz",
            "compact": f"K3P_Level2_Compact_Verifier_v{VERSION}.zip",
            "referee": f"K3P_Level2_Independent_Referee_Package_v{VERSION}.zip",
            "manifest": f"K3P_Level2_Zenodo_Manifest_v{VERSION}.json",
        }
        copy_asset(article, upload / names["article"])
        copy_asset(supplement, upload / names["supplement"])
        copy_asset(article_source, upload / names["article_source"])
        copy_asset(supplement_source, upload / names["supplement_source"])
        copy_asset(full, upload / names["full"])
        copy_asset(compact, upload / names["compact"])
        copy_asset(licenses, upload / "LICENSES.md")
        copy_asset(citation, upload / "CITATION.cff")

        write_text(
            upload / (names["full"] + ".sha256"),
            f"{sha256_file(upload / names['full'])}  {names['full']}\n",
        )
        write_text(
            upload / (names["compact"] + ".sha256"),
            f"{sha256_file(upload / names['compact'])}  {names['compact']}\n",
        )

        referee_zip = upload / names["referee"]
        referee_root = f"K3P_Level2_Independent_Referee_Package_v{VERSION}"
        deterministic_folder_zip(
            referee_zip,
            archive_root=f"K3P_Level2_Independent_Referee_Package_v{VERSION}",
            source_date_epoch=epoch,
            members=referee_members,
        )
        with tempfile.TemporaryDirectory(prefix="referee-zip-check-", dir=work_root) as check:
            destination = Path(check)
            root = extract_referee_zip(
                referee_zip, destination, referee_root, epoch
            )
            run_trusted_referee_integrity(root, trusted_referee_verifier)
        write_text(
            upload / (names["referee"] + ".sha256"),
            f"{sha256_file(referee_zip)}  {names['referee']}\n",
        )

        role_map = {
            names["article"]: ("article", "application/pdf"),
            names["supplement"]: ("reader_supplement", "application/pdf"),
            names["article_source"]: ("article_source", "application/zip"),
            names["supplement_source"]: ("supplement_source", "application/zip"),
            names["full"]: ("full_reproducibility", "application/gzip"),
            names["full"] + ".sha256": ("full_archive_sidecar", "text/plain"),
            names["compact"]: ("compact_verifier", "application/zip"),
            names["compact"] + ".sha256": ("compact_verifier_sidecar", "text/plain"),
            names["referee"]: ("independent_referee_package", "application/zip"),
            names["referee"] + ".sha256": ("referee_package_sidecar", "text/plain"),
            "LICENSES.md": ("file_level_license_map", "text/markdown"),
            "CITATION.cff": ("citation_metadata", "text/yaml"),
        }
        records = [
            asset_record(upload / name, *role_map[name])
            for name in sorted(role_map)
        ]
        description = description_text(commit, sha256_file(upload / names["full"]))
        manifest = {
            "schema": "k3p-zenodo-public-release-manifest-v1",
            "title": TITLE,
            "version": VERSION,
            "publication_date": PUBLICATION_DATE,
            "resource_type": {"type": "publication", "subtype": "preprint"},
            "access": "open",
            "creator": {
                "name": "Alec Kriebel",
                "affiliation": "Independent Researcher",
                "orcid": "0009-0001-9320-500X",
            },
            "source_commit": commit,
            "annotated_tag": TAG,
            "repository_tree": f"https://github.com/AlecKriebel/Math/tree/{commit}/k3p_level2_identifiability_final",
            "doi": None,
            "doi_policy": "Zenodo assigns the DOI at publication; it is authoritative record metadata and is not embedded in v1.0.0 bytes.",
            "license_map": {
                "article_supplement_figures_documentation_certificate_data": "CC-BY-4.0",
                "original_verifier_and_build_code": "MIT",
                "authoritative_file": "LICENSES.md",
            },
            "related_identifiers": [
                {"identifier": "10.5281/zenodo.22089373", "relation": "references"},
                {"identifier": "10.5281/zenodo.22168797", "relation": "references"},
                {"identifier": "10.5281/zenodo.22136869", "relation": "references"},
                {"identifier": f"https://github.com/AlecKriebel/Math/tree/{commit}/k3p_level2_identifiability_final", "relation": "isDerivedFrom"},
            ],
            "zenodo_metadata": {
                "language": "eng",
                "default_preview": names["article"],
                "keywords": list(KEYWORDS),
                "description_plain_text": description,
                "peer_reviewed_by_journal": False,
                "funding": "No specific funding supported this work.",
                "competing_interests": "The author declares no competing interests.",
            },
            "files_excluding_manifest_and_sha256sums": records,
            "source_reproduction": source_evidence,
            "visual_qa": {
                "article_report_sha256": sha256_file(PROJECT / "output/pdf/K3P_Level2_Identifiability_Article.visual_qa.json"),
                "supplement_report_sha256": sha256_file(PROJECT / "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.visual_qa.json"),
                "article_pages": qa_article.get("page_count"),
                "supplement_pages": qa_supplement.get("page_count"),
            },
            "verification_boundary": {
                "mathematical_theorem_or_producer_input_changed": False,
                "bibliography_and_public_release_engineering_changed": True,
                "unchanged_multi_hour_producers_rerun": False,
                "dependency_scoped_reseal_completed": True,
                "full_archive_artifact_replay_sha256": full_replay,
                "compact_archive_artifact_replay_sha256": compact_replay,
            },
            "self_reference_policy": {
                "manifest_lists_its_own_hash": False,
                "sha256sums_lists_its_own_hash": False,
                "sha256sums_covers_manifest": True,
            },
        }
        manifest_path = upload / names["manifest"]
        write_text(manifest_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")

        checksum_paths = sorted(
            path for path in upload.iterdir()
            if path.is_file() and path.name != "SHA256SUMS"
        )
        write_text(
            upload / "SHA256SUMS",
            "".join(f"{sha256_file(path)}  {path.name}\n" for path in checksum_paths),
        )
        final_records = [
            asset_record(path, "public_release_manifest" if path == manifest_path
                         else "aggregate_checksums", "application/json" if path == manifest_path
                         else "text/plain")
            for path in sorted(upload.iterdir()) if path.is_file()
        ]
        guide = metadata_guide(
            commit=commit,
            full_sha256=sha256_file(upload / names["full"]),
            records=final_records,
            description=description,
        )
        write_text(staging / "ZENODO_METADATA_GUIDE.md", guide)
        os.replace(staging, output)

    return {
        "status": "PASS",
        "output": str(output),
        "upload_directory": str(output / "UPLOAD_THESE_FILES"),
        "metadata_guide": str(output / "ZENODO_METADATA_GUIDE.md"),
        "source_commit": commit,
        "annotated_tag": TAG,
        "upload_file_count": len(list((output / "UPLOAD_THESE_FILES").iterdir())),
        "full_archive_sha256": full_info["sha256"],
        "compact_archive_sha256": compact_info["sha256"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--referee-package", type=Path, default=DEFAULT_REFEREE)
    args = parser.parse_args(argv)
    try:
        result = build(args.output.resolve(), args.referee_package.resolve())
        print(json.dumps(result, indent=2, sort_keys=True))
        print("K3P_ZENODO_UPLOAD_SET_BUILD_PASS")
        return 0
    except (ZenodoBuildFailure, ReleaseFailure, OSError, UnicodeError,
            ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile,
            tarfile.TarError, subprocess.SubprocessError) as error:
        print(f"K3P_ZENODO_UPLOAD_SET_BUILD_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
