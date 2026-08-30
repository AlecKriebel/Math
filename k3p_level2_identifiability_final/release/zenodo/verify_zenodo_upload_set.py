#!/usr/bin/env python3
"""Independently verify the exact direct-Zenodo v1.0.0 upload folder."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[2]
RELEASE = PROJECT / "release"
VERSION = "1.0.0"
TAG = "k3p-level2-identifiability-v1.0.0"
PUBLICATION_DATE = "2026-08-30"
TITLE = "Triangle Hypersurfaces and a Sharp Identifiability Boundary for Level-2 K3P Networks"
DEFAULT_ROOT = RELEASE / "dist" / f"zenodo_v{VERSION}"
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
    safe_extract_tar_gz,
    safe_extract_zip,
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


class ZenodoVerificationFailure(RuntimeError):
    pass


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ZenodoVerificationFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def command(*arguments: str) -> str:
    result = subprocess.run(
        list(arguments), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, check=False, timeout=120,
    )
    require(result.returncode == 0,
            ("command failed", arguments, result.stderr.strip()))
    return result.stdout


def git(*arguments: str) -> str:
    return command("git", "-C", str(PROJECT), *arguments).strip()


def tagged_blob(commit: str, relative: str) -> bytes:
    prefix = git("rev-parse", "--show-prefix")
    require(prefix == "k3p_level2_identifiability_final/",
            ("unexpected monorepo project prefix", prefix))
    result = subprocess.run(
        ["git", "-C", str(PROJECT), "show", f"{commit}:{prefix}{relative}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=60,
    )
    require(result.returncode == 0,
            ("missing tagged source blob", relative, result.stderr.decode(errors="replace")))
    return result.stdout


def tracked_paths(pathspec: str) -> list[str]:
    rows = git("ls-files", "--", pathspec).splitlines()
    require(rows == sorted(rows) and len(rows) == len(set(rows)),
            ("tracked path enumeration", pathspec))
    return rows


def folder_members(root: Path) -> dict[str, tuple[bytes, int]]:
    members: dict[str, tuple[bytes, int]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        require(not stat.S_ISLNK(metadata.st_mode),
                ("symlink in referee folder", relative))
        if stat.S_ISDIR(metadata.st_mode):
            continue
        require(stat.S_ISREG(metadata.st_mode) and path.name != ".DS_Store" and
                not path.name.startswith("._") and
                path.suffix not in {".pyc", ".pyo"} and
                not ({".git", ".venv", "review_runs", "__pycache__"} &
                     set(path.relative_to(root).parts)),
                ("forbidden referee folder member", relative))
        members[relative] = (path.read_bytes(), stat.S_IMODE(metadata.st_mode))
    return members


def tar_members(path: Path, archive_root: str) -> dict[str, bytes]:
    observed: dict[str, bytes] = {}
    with tarfile.open(path, mode="r:gz") as archive:
        for info in archive.getmembers():
            prefix = archive_root + "/"
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
    return hashlib.sha256(result.stdout.encode()).hexdigest()


def expected_description(commit: str, full_sha256: str) -> str:
    return f"""We classify regular full-dimensional stochastic containment among binary standard semi-directed strongly tree-child level-2 phylogenetic networks under the Kimura three-parameter (K3P) model. On the principal positive Fourier domain, a directed containment germ exists if and only if the labelled reduced trees of blobs agree and corresponding complete factors are either labelled-isomorphic or ordinarily triangle-redirected, with coherent boundary transports. The same condition is equivalent to a common full-dimensional regular germ and remains exact in strict continuous time. Thus no proper one-sided containment occurs in the strong class, and the semi-directed topology is generically identifiable and exactly reconstructible outside a proper exceptional set, modulo ordinary triangle redirection.

The three ordinary K3P triangle orientations have generic normalized rank 14, share the same irreducible eight-term quartic hypersurface H₁₄ in normalized three-leaf Fourier space, and meet in a common strict continuous-time smooth rank-14 germ. The bounded residue consists of fourteen four-port directed relation orbits—nine polynomially separated and five directed-rank separated—plus two separately separated sink swaps. Exact restoration and coherent one- and two-port probes extend the bounded classification to arbitrary labelled subdivision words.

Strong tree-childness is sharp against weakening to weak tree-childness. For every n ≥ 3, two weakly but not strongly tree-child networks have strict continuous-time K3P images sharing a common full-dimensional regular germ of dimension 6n − 3.

This is the first Zenodo/DOI-bearing archival release of version {VERSION} of the complete K3P level-2 classification and its reproducibility evidence. It contains the article, reader supplement, compile-complete source archives, canonical full proof archive, compact verifier, independent-referee replay package, exact manifest, checksums, citation metadata, and a file-level license notice. The deposited bytes correspond to immutable Git commit {commit}, annotated tag {TAG} resolving to that commit, and full-archive SHA-256 {full_sha256}.

The archive includes the previously completed all-producer regeneration evidence bound to unchanged mathematical inputs, together with successful exact and independently implemented replays, rigorous interval arithmetic where required, and fail-closed mutation tests. The present release changes bibliography, nonmathematical administrative/public-release prose, and release engineering only; unchanged multi-hour mathematical producers were not rerun during this dependency-scoped reseal. No empirical data set is used.

Preprint; not peer reviewed by a journal. Generative-AI assistance and its verification workflow are disclosed in the article. Article, supplement, figures, documentation, and mathematical certificate data are licensed under CC BY 4.0; original verifier and build code are licensed under MIT, as mapped in LICENSES.md. No specific funding supported this work. The author declares no competing interests."""


def expected_metadata_guide(*, commit: str, full_sha256: str,
                            upload: Path, description: str) -> str:
    paths = sorted(path for path in upload.iterdir() if path.is_file())
    file_lines = "\n".join(
        f"{index}. `{path.name}` — {path.stat().st_size} bytes — "
        f"SHA-256 `{sha256_file(path)}`"
        for index, path in enumerate(paths, 1)
    )
    keywords = "\n".join(f"- `{value}`" for value in KEYWORDS)
    repository_tree = (
        f"https://github.com/AlecKriebel/Math/tree/{commit}/"
        "k3p_level2_identifiability_final"
    )
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
| `{repository_tree}` | Is derived from | Software |

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


def parse_sums(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        require(match is not None, ("malformed SHA256SUMS line", line))
        digest, name = match.groups()
        require(name not in rows and name != "SHA256SUMS",
                ("duplicate or self-referential checksum", name))
        rows[name] = digest
        names.append(name)
    require(names == sorted(names), "SHA256SUMS canonical ordering")
    return rows


def extract_referee_zip(path: Path, destination: Path, archive_root: str,
                        source_date_epoch: int) -> Path:
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
            require(pure.name != ".DS_Store" and not pure.name.startswith("._") and
                    pure.suffix not in {".pyc", ".pyo"} and
                    not ({".git", ".venv", "review_runs", "__pycache__"} &
                         set(pure.parts)),
                    ("forbidden referee ZIP member", relative))
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


def verify_pdf(path: Path, expected_pages: int) -> dict[str, object]:
    info = command("pdfinfo", str(path))
    page_match = re.search(r"^Pages:\s+(\d+)$", info, flags=re.MULTILINE)
    require(page_match is not None and int(page_match.group(1)) == expected_pages,
            ("PDF page count", path.name, page_match.group(1) if page_match else None))
    fonts = command("pdffonts", str(path)).splitlines()
    rows = [line for line in fonts[2:] if line.strip()]
    require(rows and all(line.split()[-5].lower() == "yes" for line in rows),
            ("PDF font embedding", path.name))
    return {"pages": expected_pages, "embedded_fonts": len(rows)}


def verify(root: Path, *, require_remote_tag: bool = False) -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is forbidden")
    require(root.is_dir() and not root.is_symlink(),
            ("missing release root", str(root)))
    guide = root / "ZENODO_METADATA_GUIDE.md"
    upload = root / "UPLOAD_THESE_FILES"
    require(guide.is_file() and not guide.is_symlink() and
            upload.is_dir() and not upload.is_symlink(),
            "release root structure")

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
    expected = {
        names["article"], names["supplement"], names["article_source"],
        names["supplement_source"], names["full"], names["full"] + ".sha256",
        names["compact"], names["compact"] + ".sha256", names["referee"],
        names["referee"] + ".sha256", names["manifest"], "LICENSES.md",
        "CITATION.cff", "SHA256SUMS",
    }
    observed = set()
    for path in upload.iterdir():
        metadata = path.lstat()
        require(stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode),
                ("nonregular upload member", path.name))
        observed.add(path.name)
    require(observed == expected,
            ("Zenodo upload allowlist mismatch", sorted(expected - observed),
             sorted(observed - expected)))

    sums = parse_sums(upload / "SHA256SUMS")
    require(set(sums) == expected - {"SHA256SUMS"}, "SHA256SUMS path set")
    for name, digest in sums.items():
        require(sha256_file(upload / name) == digest,
                ("SHA256SUMS mismatch", name))

    manifest_path = upload / names["manifest"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(set(manifest) == {
        "schema", "title", "version", "publication_date", "resource_type",
        "access", "creator", "source_commit", "annotated_tag",
        "repository_tree", "doi", "doi_policy", "license_map",
        "related_identifiers", "zenodo_metadata",
        "files_excluding_manifest_and_sha256sums", "source_reproduction",
        "visual_qa", "verification_boundary", "self_reference_policy",
    }, "Zenodo manifest top-level field set")
    commit = manifest.get("source_commit")
    require(isinstance(commit, str) and re.fullmatch(r"[0-9a-f]{40}", commit),
            ("manifest commit", commit))
    repository_tree = (
        f"https://github.com/AlecKriebel/Math/tree/{commit}/"
        "k3p_level2_identifiability_final"
    )
    require(manifest.get("schema") == "k3p-zenodo-public-release-manifest-v1" and
            manifest.get("title") == TITLE and manifest.get("version") == VERSION and
            manifest.get("publication_date") == PUBLICATION_DATE and
            manifest.get("resource_type") == {
                "type": "publication", "subtype": "preprint"
            } and manifest.get("access") == "open" and
            manifest.get("creator") == {
                "name": "Alec Kriebel", "affiliation": "Independent Researcher",
                "orcid": "0009-0001-9320-500X",
            } and manifest.get("annotated_tag") == TAG and
            manifest.get("repository_tree") == repository_tree and
            manifest.get("doi") is None and
            manifest.get("doi_policy") ==
            "Zenodo assigns the DOI at publication; it is authoritative record metadata and is not embedded in v1.0.0 bytes.",
            "Zenodo manifest identity and bibliographic metadata")
    require(manifest.get("license_map") == {
        "article_supplement_figures_documentation_certificate_data": "CC-BY-4.0",
        "original_verifier_and_build_code": "MIT",
        "authoritative_file": "LICENSES.md",
    }, "Zenodo manifest license map")
    require(manifest.get("related_identifiers") == [
        {"identifier": "10.5281/zenodo.22089373", "relation": "references"},
        {"identifier": "10.5281/zenodo.22168797", "relation": "references"},
        {"identifier": "10.5281/zenodo.22136869", "relation": "references"},
        {"identifier": repository_tree, "relation": "isDerivedFrom"},
    ], "Zenodo related identifiers")
    require(manifest.get("self_reference_policy") == {
        "manifest_lists_its_own_hash": False,
        "sha256sums_lists_its_own_hash": False,
        "sha256sums_covers_manifest": True,
    }, "Zenodo manifest self-reference policy")

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
    records = manifest.get("files_excluding_manifest_and_sha256sums")
    require(isinstance(records, list) and len(records) == len(role_map),
            "manifest substantive file count")
    require(all(isinstance(row, dict) for row in records),
            "manifest file-row objects")
    require([row.get("path") for row in records] == sorted(role_map),
            "manifest file-row canonical ordering")
    record_names = set()
    for row in records:
        require(isinstance(row, dict) and set(row) == {
            "path", "role", "media_type", "bytes", "sha256"
        }, "manifest file-row schema")
        name = row.get("path")
        require(name in role_map and name not in record_names,
                ("manifest file path", name))
        record_names.add(name)
        role, media_type = role_map[name]
        path = upload / name
        require(row.get("role") == role and row.get("media_type") == media_type and
                row.get("sha256") == sha256_file(path) and
                row.get("bytes") == path.stat().st_size,
                ("manifest file binding", name))
    require(record_names == set(role_map), "manifest file coverage")

    tag_object = git("cat-file", "-t", f"refs/tags/{TAG}")
    tag_commit = git("rev-parse", f"{TAG}^{{}}")
    require(tag_object == "tag" and tag_commit == commit and
            git("rev-parse", "HEAD") == commit and
            git("rev-parse", "origin/main") == commit and
            git("status", "--porcelain", "--", ".") == "",
            ("local immutable release identity", tag_object, tag_commit, commit))
    epoch_text = git("show", "-s", "--format=%ct", commit)
    require(epoch_text.isdigit(), ("tagged commit epoch", epoch_text))
    epoch = int(epoch_text)
    policy = load_release_policy(PROJECT)

    full_path, compact_path = upload / names["full"], upload / names["compact"]
    article_source_path = upload / names["article_source"]
    supplement_source_path = upload / names["supplement_source"]
    full = verify_tar_gz(full_path)
    compact = verify_zip(compact_path)
    article_source, _article_build, _article_binding = verify_source_archive_contract(
        article_source_path, kind="article", project=PROJECT, policy=policy
    )
    supplement_source, _supplement_build, _supplement_binding = \
        verify_source_archive_contract(
            supplement_source_path, kind="supplement", project=PROJECT, policy=policy
        )
    for label, record, expected_kind, expected_root in (
        ("full", full, "full_reproducibility", policy["archive_root"]),
        ("compact", compact, "compact_verifier", policy["compact_root"]),
        ("article source", article_source, "article_latex_source",
         "k3p_level2_article_source"),
        ("supplement source", supplement_source, "supplement_latex_source",
         "k3p_level2_supplement_source"),
    ):
        require(record.get("source_commit") == commit and
                record.get("kind") == expected_kind and
                record.get("archive_root") == expected_root and
                record.get("source_date_epoch") == epoch,
                ("archive identity/commit/epoch mismatch", label, record))
    require(full.get("metadata") == {
        "fileset_policy_sha256": hashlib.sha256(
            tagged_blob(commit, "release/RELEASE_FILESET.json")
        ).hexdigest(),
        "source_archives_generated_from_committed_tex": True,
        "release_pdfs_included": True,
        "untracked_files_included": False,
    }, "full archive metadata")
    require(compact.get("metadata") == {
        "entrypoint": "reproducibility/verify_k3p_same_classification.py",
        "entrypoint_mode": "--artifact-only --no-write-report",
        "full_archive_is_external_canonical": True,
    }, "compact archive metadata")

    full_members = tar_members(full_path, policy["archive_root"])
    expected_full = set(full_selection(PROJECT, policy, require_pdfs=True))
    generated_full = {
        "ARCHIVE_MANIFEST.json", "REPRODUCIBILITY_README.txt",
        "source_archives/k3p_level2_article_source.zip",
        "source_archives/k3p_level2_supplement_source.zip",
    }
    require(set(full_members) == expected_full | generated_full,
            "full archive tagged-fileset coverage")
    for relative in expected_full:
        require(full_members[relative] == tagged_blob(commit, relative),
                ("full archive differs from tagged source", relative))
    require(full_members["REPRODUCIBILITY_README.txt"] == generated_readme(commit) and
            full_members["source_archives/k3p_level2_article_source.zip"] ==
            article_source_path.read_bytes() and
            full_members["source_archives/k3p_level2_supplement_source.zip"] ==
            supplement_source_path.read_bytes(),
            "full archive generated/source-archive binding")

    compact_members = zip_members(compact_path, policy["compact_root"])
    expected_compact = set(compact_selection(PROJECT, policy))
    require(set(compact_members) == expected_compact | {
        "ARCHIVE_MANIFEST.json", "README_VERIFY.txt"
    }, "compact archive tagged-fileset coverage")
    for relative in expected_compact:
        require(compact_members[relative] == tagged_blob(commit, relative),
                ("compact archive differs from tagged source", relative))
    require(compact_members["README_VERIFY.txt"] == generated_compact_readme(),
            "compact generated README binding")

    direct_bindings = {
        names["article"]: "output/pdf/K3P_Level2_Identifiability_Article.pdf",
        names["supplement"]:
            "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.pdf",
        "LICENSES.md": "LICENSES.md",
        "CITATION.cff": "CITATION.cff",
    }
    for direct_name, relative in direct_bindings.items():
        expected_bytes = tagged_blob(commit, relative)
        require((upload / direct_name).read_bytes() == expected_bytes and
                full_members[relative] == expected_bytes,
                ("direct/full/tagged asset mismatch", direct_name))

    for key in ("full", "compact", "referee"):
        sidecar = (upload / (names[key] + ".sha256")).read_text(encoding="utf-8")
        require(sidecar == f"{sha256_file(upload / names[key])}  {names[key]}\n",
                ("sidecar mismatch", key))

    qa_specs = (
        ("article", names["article"],
         "output/pdf/K3P_Level2_Identifiability_Article.visual_qa.json"),
        ("supplement", names["supplement"],
         "output/pdf/K3P_Level2_Identifiability_Reader_Supplement.visual_qa.json"),
    )
    qa_rows: dict[str, dict] = {}
    pdf_results = {}
    for kind, pdf_name, qa_relative in qa_specs:
        qa_bytes = tagged_blob(commit, qa_relative)
        require(full_members[qa_relative] == qa_bytes,
                ("visual QA full/tag binding", kind))
        qa = json.loads(qa_bytes.decode("utf-8"))
        pdf = upload / pdf_name
        require(qa.get("status") == "PASS" and
                qa.get("pdf_sha256") == sha256_file(pdf) and
                isinstance(qa.get("page_count"), int) and qa["page_count"] > 0,
                ("visual QA/PDF binding", kind))
        qa_rows[kind] = qa
        pdf_results[kind] = verify_pdf(pdf, qa["page_count"])
    require(manifest.get("visual_qa") == {
        "article_report_sha256": hashlib.sha256(tagged_blob(
            commit, qa_specs[0][2]
        )).hexdigest(),
        "supplement_report_sha256": hashlib.sha256(tagged_blob(
            commit, qa_specs[1][2]
        )).hexdigest(),
        "article_pages": qa_rows["article"]["page_count"],
        "supplement_pages": qa_rows["supplement"]["page_count"],
    }, "manifest visual-QA binding")

    with tempfile.TemporaryDirectory(prefix="zenodo-release-check-") as directory:
        temporary = Path(directory)
        package_root_name = f"K3P_Level2_Independent_Referee_Package_v{VERSION}"
        package = extract_referee_zip(
            upload / names["referee"], temporary / "referee", package_root_name,
            epoch,
        )
        trusted_referee_verifier = (
            PROJECT / "referee_handoff/referee_tools/verify_package_integrity.py"
        )
        require(trusted_referee_verifier.is_file() and
                trusted_referee_verifier.read_bytes() == tagged_blob(
                    commit, "referee_handoff/referee_tools/verify_package_integrity.py"
                ), "trusted referee verifier/tag binding")
        integrity = subprocess.run(
            [sys.executable, str(trusted_referee_verifier),
             "--package-root", str(package)],
            cwd=PROJECT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, check=False, timeout=600,
        )
        require(integrity.returncode == 0 and
                "K3P_REFEREE_PACKAGE_INTEGRITY_PASS" in integrity.stdout,
                ("referee package integrity", integrity.stdout[-3000:]))
        package_manifest = json.loads(
            (package / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8")
        )
        require(package_manifest.get("package_builder_commit") == commit and
                package_manifest.get("proof_source_commit") == commit and
                package_manifest.get("canonical_archive_sha256") ==
                sha256_file(full_path),
                "referee manifest release binding")
        proof = package / "proof_package"
        for relative, data in full_members.items():
            sealed = proof / relative
            require(sealed.is_file() and not sealed.is_symlink() and
                    sealed.read_bytes() == data and
                    stat.S_IMODE(sealed.stat().st_mode) == canonical_mode(relative),
                    ("referee/full archive byte mismatch", relative))
        require((package / "paper/K3P_Level2_Identifiability_Article.pdf").read_bytes()
                == (upload / names["article"]).read_bytes() and
                (package / "paper/K3P_Level2_Identifiability_Reader_Supplement.pdf").read_bytes()
                == (upload / names["supplement"]).read_bytes(),
                "referee paper/direct PDF binding")

        source_rows = []
        for kind, pdf_name, source_name, source_record in (
            ("article", names["article"], names["article_source"], article_source),
            ("supplement", names["supplement"], names["supplement_source"],
             supplement_source),
        ):
            report_relative = f"release/source_reproduction_evidence/{kind}.json"
            source_relative = f"release/dist/k3p_level2_{kind}_source.zip"
            report_path = proof / report_relative
            source_path = proof / source_relative
            direct_source = upload / source_name
            require(report_path.is_file() and source_path.is_file() and
                    source_path.read_bytes() == direct_source.read_bytes(),
                    ("referee source evidence/archive binding", kind))
            transcript_records = {}
            transcript_rows = []
            for run in (1, 2):
                transcript_relative = (
                    f"release/source_reproduction_evidence/{kind}_transcripts/"
                    f"run{run}.log"
                )
                transcript = proof / transcript_relative
                require(transcript.is_file() and not transcript.is_symlink(),
                        ("referee source transcript", kind, run))
                transcript_records[transcript_relative] = {
                    "sha256": sha256_file(transcript)
                }
                transcript_rows.append({
                    "run": run,
                    "sealed_path": f"proof_package/{transcript_relative}",
                    "sha256": sha256_file(transcript),
                })
            report = json.loads(report_path.read_text(encoding="utf-8"))
            archive_contract, _build, committed_binding = \
                verify_source_archive_contract(
                    direct_source, kind=kind, project=PROJECT, policy=policy
                )
            require(report.get("source_archive") == {
                "path": source_relative,
                "sha256": sha256_file(direct_source),
                "structural_verification": archive_contract,
            } and report.get("committed_source_binding") == committed_binding,
                    ("source report/archive semantic binding", kind))
            validate_source_reproduction_evidence(
                report, kind=kind, commit=commit,
                pdf_record={
                    "sha256": sha256_file(upload / pdf_name),
                    "bytes": (upload / pdf_name).stat().st_size,
                }, policy=policy, transcript_records=transcript_records,
            )
            source_rows.append({
                "kind": kind,
                "report_path": report_relative,
                "sealed_report_path": f"proof_package/{report_relative}",
                "report_sha256": sha256_file(report_path),
                "source_archive_path": source_relative,
                "sealed_source_archive_path": f"proof_package/{source_relative}",
                "source_archive_sha256": sha256_file(direct_source),
                "transcripts": transcript_rows,
                "pdf_sha256": sha256_file(upload / pdf_name),
                "two_builds_match_release_pdf": True,
            })
        require(manifest.get("source_reproduction") == source_rows,
                "manifest source-reproduction binding")

        package_members = folder_members(package)
        tool_sources = [
            relative for relative in tracked_paths(
                "referee_handoff/referee_tools/**"
            ) if relative.endswith((".py", ".json"))
        ]
        require(len(tool_sources) == 4,
                ("referee tool source count", tool_sources))
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
            require(destination in package_members and
                    package_members[destination] == (
                        tagged_blob(commit, source), expected_mode
                    ), ("referee interface/tag binding", destination, source))
        work_logs = tracked_paths("*WORK_LOG.md")
        require(len(work_logs) == 20,
                ("referee tracked work-log count", len(work_logs)))
        evidence_paths = [
            "release/source_reproduction_evidence/article.json",
            "release/source_reproduction_evidence/supplement.json",
            "release/source_reproduction_evidence/article_transcripts/run1.log",
            "release/source_reproduction_evidence/article_transcripts/run2.log",
            "release/source_reproduction_evidence/supplement_transcripts/run1.log",
            "release/source_reproduction_evidence/supplement_transcripts/run2.log",
            "release/dist/k3p_level2_article_source.zip",
            "release/dist/k3p_level2_supplement_source.zip",
        ]
        proof_extras = work_logs + [
            "release/FINAL_RELEASE_ENGINEERING_REPORT.md"
        ] + evidence_paths
        expected_proof = set(full_members) | set(proof_extras)
        observed_proof = {
            relative.removeprefix("proof_package/")
            for relative in package_members
            if relative.startswith("proof_package/")
        }
        require(observed_proof == expected_proof,
                ("referee proof-package exact file set",
                 sorted(expected_proof - observed_proof),
                 sorted(observed_proof - expected_proof)))
        for relative in work_logs + ["release/FINAL_RELEASE_ENGINEERING_REPORT.md"]:
            require(package_members[f"proof_package/{relative}"] == (
                        tagged_blob(commit, relative), 0o644
                    ),
                    ("referee tracked extra/tag binding", relative))
        paper_paths = {
            "paper/K3P_Level2_Identifiability_Article.pdf",
            "paper/K3P_Level2_Identifiability_Reader_Supplement.pdf",
        }
        expected_package = (
            {f"proof_package/{relative}" for relative in expected_proof} |
            set(interface_sources) | paper_paths |
            {"PACKAGE_MANIFEST.json", "SHA256SUMS"}
        )
        require(set(package_members) == expected_package,
                ("referee package exact file set",
                 sorted(expected_package - set(package_members)),
                 sorted(set(package_members) - expected_package)))
        for relative in evidence_paths:
            require(package_members[f"proof_package/{relative}"][1] == 0o644,
                    ("referee evidence mode", relative))
        require(all(package_members[relative][1] == 0o644
                    for relative in paper_paths | {
                        "PACKAGE_MANIFEST.json", "SHA256SUMS"
                    }), "referee paper/outer seal modes")

        safe_extract_zip(compact_path, temporary / "compact")
        compact_replay = run_extracted_gate(
            temporary / "compact" / policy["compact_root"]
        )
        safe_extract_tar_gz(full_path, temporary / "full")
        full_replay = run_extracted_gate(
            temporary / "full" / policy["archive_root"]
        )

    require(manifest.get("verification_boundary") == {
        "mathematical_theorem_or_producer_input_changed": False,
        "bibliography_and_public_release_engineering_changed": True,
        "unchanged_multi_hour_producers_rerun": False,
        "dependency_scoped_reseal_completed": True,
        "full_archive_artifact_replay_sha256": full_replay,
        "compact_archive_artifact_replay_sha256": compact_replay,
    }, "manifest verification boundary")
    full_hash = sha256_file(full_path)
    description = expected_description(commit, full_hash)
    require(manifest.get("zenodo_metadata") == {
        "language": "eng",
        "default_preview": names["article"],
        "keywords": list(KEYWORDS),
        "description_plain_text": description,
        "peer_reviewed_by_journal": False,
        "funding": "No specific funding supported this work.",
        "competing_interests": "The author declares no competing interests.",
    }, "manifest Zenodo form metadata")

    require(guide.read_text(encoding="utf-8") == expected_metadata_guide(
        commit=commit, full_sha256=full_hash, upload=upload,
        description=description,
    ), "metadata guide exact canonical binding")

    remote_tag_verified = False
    if require_remote_tag:
        require(dt.datetime.now(dt.timezone.utc).date().isoformat() ==
                PUBLICATION_DATE,
                ("publication date is no longer current; regenerate and reseal",
                 PUBLICATION_DATE))
        remote = command(
            "git", "-C", str(PROJECT), "ls-remote", "--tags", "origin",
            f"refs/tags/{TAG}", f"refs/tags/{TAG}^{{}}",
        )
        rows = {}
        for line in remote.splitlines():
            fields = line.split("\t")
            require(len(fields) == 2 and re.fullmatch(r"[0-9a-f]{40}", fields[0]),
                    ("remote tag row", line))
            rows[fields[1]] = fields[0]
        require(set(rows) == {f"refs/tags/{TAG}", f"refs/tags/{TAG}^{{}}"} and
                rows[f"refs/tags/{TAG}^{{}}"] == commit and
                rows[f"refs/tags/{TAG}"] != commit,
                ("remote annotated tag binding", rows, commit))
        remote_tag_verified = True

    return {
        "status": "PASS",
        "source_commit": commit,
        "annotated_tag": TAG,
        "remote_tag_verified": remote_tag_verified,
        "upload_file_count": len(expected),
        "article_pdf": pdf_results["article"],
        "supplement_pdf": pdf_results["supplement"],
        "full_archive_sha256": full["sha256"],
        "compact_archive_sha256": compact["sha256"],
        "referee_package_sha256": sha256_file(upload / names["referee"]),
        "sha256sums_sha256": sha256_file(upload / "SHA256SUMS"),
        "manifest_sha256": sha256_file(manifest_path),
        "full_archive_artifact_replay_sha256": full_replay,
        "compact_archive_artifact_replay_sha256": compact_replay,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument(
        "--require-remote-tag", action="store_true",
        help="also require origin's annotated tag to peel to the manifest commit",
    )
    args = parser.parse_args(argv)
    try:
        result = verify(
            args.root.resolve(), require_remote_tag=args.require_remote_tag
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        print("K3P_ZENODO_UPLOAD_SET_VERIFY_PASS")
        return 0
    except (ZenodoVerificationFailure, ReleaseFailure, OSError, UnicodeError,
            ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile,
            tarfile.TarError, subprocess.SubprocessError) as error:
        print(f"K3P_ZENODO_UPLOAD_SET_VERIFY_FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
