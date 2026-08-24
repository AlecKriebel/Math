#!/usr/bin/env python3
"""Build the frozen, self-contained Paper I AI-referee handoff."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile


TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent.parent
PAPER_REL = Path(
    "universal_simultaneous_amplification/phase5_exact_threshold/"
    "paper_db_extremality"
)
PAPER = REPO / PAPER_REL
ARCHIVE_NAME = "complete_graph_extremality_db_source_and_certificates.tar.gz"
PDF_NAME = "complete_graph_extremality_db.pdf"
EPOCH = 1_787_270_400
STATIC_FILES = (
    "REFEREE_PROMPT.md",
    "CLAIM_CODE_MAP.md",
    "REFEREE_REPORT_TEMPLATE.md",
    "run_all_referee_checks.sh",
    "verify_referee_package.py",
)


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def regular_files(root: Path) -> list[Path]:
    files: list[Path] = []

    def visit(directory: Path) -> None:
        with os.scandir(directory) as entries:
            for entry in entries:
                details = entry.stat(follow_symlinks=False)
                mode = details.st_mode
                path = Path(entry.path)
                if stat.S_ISLNK(mode):
                    raise RuntimeError(f"package tree contains a symlink: {path}")
                if stat.S_ISDIR(mode):
                    if entry.name.casefold() == "__pycache__":
                        raise RuntimeError(
                            f"package tree contains a forbidden cache directory: {path}"
                        )
                    visit(path)
                elif stat.S_ISREG(mode):
                    if path.suffix.casefold() in {".pyc", ".pyo"}:
                        raise RuntimeError(f"package tree contains bytecode: {path}")
                    files.append(path)
                else:
                    raise RuntimeError(f"package tree contains a special node: {path}")

    visit(root)
    return sorted(files)


def git_output(*args: str) -> str:
    return subprocess.run(
        ("git", *args), cwd=REPO, check=True, text=True, capture_output=True
    ).stdout.strip()


def require_frozen_tracked_tree() -> str:
    status = git_output("status", "--porcelain", "--untracked-files=no")
    if status:
        raise RuntimeError("tracked files are not frozen; commit them before packaging")
    return git_output("rev-parse", "HEAD")


def tracked_paths() -> set[str]:
    result = subprocess.run(
        ("git", "ls-files", "-z"), cwd=REPO, check=True, stdout=subprocess.PIPE
    )
    return {
        name.decode("utf-8")
        for name in result.stdout.split(b"\0")
        if name
    }


def verify_archive_against_commit(archive_path: Path, source_commit: str) -> int:
    tracked = tracked_paths()
    verified = 0
    with tarfile.open(archive_path, mode="r:gz") as archive:
        for member in archive.getmembers():
            name = PurePosixPath(member.name)
            if (
                not member.isfile()
                or name.is_absolute()
                or ".." in name.parts
                or name.as_posix() != member.name
            ):
                raise RuntimeError(f"unsafe source archive member: {member.name}")
            if member.name in {"BUNDLE_METADATA.txt", "MANIFEST.sha256"}:
                continue
            if member.name not in tracked:
                raise RuntimeError(
                    f"source archive contains an untracked file: {member.name}"
                )
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f"cannot read archive member: {member.name}")
            committed = subprocess.run(
                ("git", "show", f"{source_commit}:{member.name}"),
                cwd=REPO,
                check=True,
                stdout=subprocess.PIPE,
            ).stdout
            if source.read() != committed:
                raise RuntimeError(
                    f"source archive differs from commit {source_commit}: {member.name}"
                )
            verified += 1
    return verified


def safely_replace_directory(target: Path) -> None:
    expected_parent = (REPO / "referee_packages").resolve()
    target = target.resolve()
    if target.parent != expected_parent or not target.name.startswith(
        "paper_i_complete_graph_extremality_referee_package_"
    ):
        raise RuntimeError(f"refusing unexpected output directory: {target}")
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)


def extract_regular_archive(archive_path: Path, target: Path) -> int:
    count = 0
    with tarfile.open(archive_path, mode="r:gz") as archive:
        members = archive.getmembers()
        names = [member.name for member in members]
        if names != sorted(names) or len(names) != len(set(names)):
            raise RuntimeError("source archive members are not unique and sorted")
        for member in members:
            name = PurePosixPath(member.name)
            if (
                not member.isfile()
                or name.is_absolute()
                or ".." in name.parts
                or name.as_posix() != member.name
            ):
                raise RuntimeError(f"unsafe source archive member: {member.name}")
            destination = target / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f"cannot read archive member: {member.name}")
            destination.write_bytes(source.read())
            destination.chmod(0o755 if member.mode & 0o111 else 0o644)
            count += 1
    return count


def write_package_manifest(target: Path) -> int:
    rows: list[str] = []
    manifest_path = target / "PACKAGE_MANIFEST.sha256"
    for path in regular_files(target):
        if path == manifest_path:
            continue
        relative = path.relative_to(target).as_posix()
        rows.append(f"{sha256(path)}  {relative}\n")
    (target / "PACKAGE_MANIFEST.sha256").write_text("".join(rows), encoding="ascii")
    return len(rows)


def tar_info(name: str, size: int, executable: bool) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = size
    info.mtime = EPOCH
    info.uid = 0
    info.gid = 0
    info.uname = "root"
    info.gname = "root"
    info.mode = 0o755 if executable else 0o644
    return info


def write_transport_archive(target: Path) -> tuple[Path, str]:
    output = target.with_name(f"{target.name}.tar.gz")
    sidecar = output.with_name(f"{output.name}.sha256")
    output.unlink(missing_ok=True)
    sidecar.unlink(missing_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{output.name}.", dir=output.parent, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with temporary_path.open("wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, mtime=EPOCH, compresslevel=9
            ) as compressed:
                with tarfile.open(
                    fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT
                ) as archive:
                    for path in regular_files(target):
                        data = path.read_bytes()
                        name = f"{target.name}/{path.relative_to(target).as_posix()}"
                        info = tar_info(name, len(data), bool(path.stat().st_mode & 0o111))
                        archive.addfile(info, io.BytesIO(data))
        os.replace(temporary_path, output)
        output.chmod(0o644)
    finally:
        temporary_path.unlink(missing_ok=True)
    output_digest = sha256(output)
    sidecar.write_text(f"{output_digest}  {output.name}\n", encoding="ascii")
    return output, output_digest


def write_readme(
    target: Path, source_commit: str, archive_digest: str, pdf_digest: str
) -> None:
    content = f"""# Read this first

This is a frozen, self-contained project-source and certificate handoff for
*Local Complete-Graph
Optimality at Fitness Two and Strong-Selection Rigidity under Death--Birth
Updating*. The package is intended for an independent, submission-style audit;
it does not prescribe a favorable verdict.

Start by reading `REFEREE_PROMPT.md`. Inspect the paper and code before running
the sole certified package replay. `CLAIM_CODE_MAP.md` is only a navigation
index, and `REFEREE_REPORT_TEMPLATE.md` is optional.

## Frozen identity

- Scientific source commit: `{source_commit}`
- Source archive SHA-256: `{archive_digest}`
- Manuscript PDF SHA-256: `{pdf_digest}`
- Source archive: `{ARCHIVE_NAME}`
- Detached archive checksum: `{ARCHIVE_NAME}.sha256`
- Whole-package manifest: `PACKAGE_MANIFEST.sha256`

The package may itself be added by a later wrapping commit. The scientific
source commit above identifies the tracked state from which both the archive
and PDF were generated, avoiding a self-referential package hash.

## Layout

- `{PDF_NAME}`: convenience copy of the compiled paper.
- `{ARCHIVE_NAME}`: exact deterministic source, certificate, test, and replay
  archive supplied with the paper.
- `source_and_certificates/`: byte-identical extraction of that archive for
  immediate inspection.
- `verify_referee_package.py`: standard-library integrity verifier.
- `run_all_referee_checks.sh`: the sole certified end-to-end entry point. It
  verifies the exact package tree, safely extracts the verified source archive
  to a disposable directory, provisions the pinned runtime, runs all internal
  stages, rebuilds the PDF, and compares it byte-for-byte.

Prior review verdicts, research diaries, and saved successful output are
deliberately absent. Proof documents and independent checking programs remain.
The three imported exploratory helper modules have inert guarded mains: only
the function-level reach described in `CLAIM_CODE_MAP.md` is advertised.

## Suggested order

1. Independently inspect the PDF, LaTeX, proof documents, certified launcher,
   internal bootstrap/replay stages, every invoked verifier, and imported
   helpers.
2. Verify package identity with `python3 -I verify_referee_package.py`.
3. With Python 3.14.6 available, run `./run_all_referee_checks.sh`. If
   `python3` is not that exact interpreter, set for example
   `BOOTSTRAP_PYTHON=/path/to/python3.14.6`.
4. Preserve the transcript and complete an independent mathematical and code
   audit using the neutral prompt.

The bootstrap's explicit `--development` mode is a convenience rather than a
certificate; `replay.sh` is internal-only and rejects standalone invocation.
Neither lower-stage status certifies package identity or execution of the
delivered source. The certified launcher rejects links, special nodes, extra
files/directories, and bytecode/cache entries before any project import, then
uses a fresh private cache prefix for every Python process that can import
project code. The preceding exact-tree scanner is standard-library-only and
imports no project module.

The certified replay binds the accepted wheels for SymPy 1.14.0,
python-flint 0.9.0, and mpmath 1.3.0 by SHA-256. The PDF rebuild requires
Tectonic 0.16.9, the pinned standard v33 bundle content, and Poppler 26.08.0
(`pdfinfo` and `pdftoppm`). The bootstrap may access the configured Python
package index to retrieve only hash-matching wheels; it does not contact any
person or submit any artifact. The exact theorem replay is independent of the
document tools, and the final PDF comparison detects any rendering difference.
"""
    (target / "README_FIRST.md").write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=REPO
        / "referee_packages/paper_i_complete_graph_extremality_referee_package_2026-08-23_r4",
    )
    args = parser.parse_args()

    source_commit = require_frozen_tracked_tree()
    archive = PAPER / "output/release" / ARCHIVE_NAME
    archive_sidecar = archive.with_name(f"{archive.name}.sha256")
    pdf = PAPER / "output/pdf" / PDF_NAME
    for required in (archive, archive_sidecar, pdf):
        if not required.is_file():
            raise FileNotFoundError(required)

    archive_digest = sha256(archive)
    expected_sidecar = f"{archive_digest}  {ARCHIVE_NAME}\n"
    if archive_sidecar.read_text(encoding="ascii") != expected_sidecar:
        raise RuntimeError("source archive sidecar is stale")
    pdf_digest = sha256(pdf)
    commit_member_count = verify_archive_against_commit(archive, source_commit)

    target = args.output_dir.resolve()
    safely_replace_directory(target)
    shutil.copy2(pdf, target / PDF_NAME)
    shutil.copy2(archive, target / ARCHIVE_NAME)
    shutil.copy2(archive_sidecar, target / f"{ARCHIVE_NAME}.sha256")
    for name in STATIC_FILES:
        shutil.copy2(TOOLS / name, target / name)

    extracted = target / "source_and_certificates"
    extracted.mkdir()
    source_members = extract_regular_archive(archive, extracted)
    nested_pdf = extracted / PAPER_REL / "output/pdf" / PDF_NAME
    if nested_pdf.read_bytes() != pdf.read_bytes():
        raise RuntimeError("source archive PDF differs from development PDF")

    version = f"""# Frozen package identity

- Scientific source commit: `{source_commit}`
- Source archive SHA-256: `{archive_digest}`
- Manuscript PDF SHA-256: `{pdf_digest}`
- Internal source-archive members: {source_members}
- Archive members byte-checked against the source commit: {commit_member_count}
- Package format date: 2026-08-23
- Package remediation level: R4 layout/date refresh on the R3 exact-tree hardening

The scientific source commit predates the wrapping commit that may add this
copied referee folder. It is the commit from which the archive and PDF were
built. `PACKAGE_MANIFEST.sha256` checks every other delivered file; the
detached transport-archive digest binds the package as a whole.
"""
    (target / "VERSION.md").write_text(version, encoding="utf-8")
    write_readme(target, source_commit, archive_digest, pdf_digest)
    payload_count = write_package_manifest(target)

    subprocess.run(
        (sys.executable, "-I", str(target / "verify_referee_package.py")),
        check=True,
    )
    transport, transport_digest = write_transport_archive(target)
    print(f"WROTE_FOLDER: {target}")
    print(f"PACKAGE_PAYLOAD_FILES: {payload_count}")
    print(f"WROTE_TRANSPORT_ARCHIVE: {transport}")
    print(f"TRANSPORT_SHA256: {transport_digest}")


if __name__ == "__main__":
    main()
