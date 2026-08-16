#!/usr/bin/env python3
"""Build deterministic bioRxiv and persistent-archive release artifacts."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
SUBMISSION = PROJECT / "biorxiv_submission"
SOURCE = PROJECT / "source"
RELEASE_ASSETS = PROJECT / "release_artifacts"
SOURCE_DATE_EPOCH = "1786838400"  # 2026-08-16 00:00:00 UTC
ZIP_TIME = (2026, 8, 16, 0, 0, 0)

MAIN_NAME = "Strong_Tree_Childness_Sharp_Level2_JC.pdf"
SUPPLEMENT_NAME = "Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf"
SOURCE_ZIP_NAME = "Strong_Tree_Childness_Sharp_Level2_JC_source.zip"
ARCHIVE_NAME = "stc_jc_sharp_boundary_reproducibility.tar.gz"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> None:
    subprocess.run(command, cwd=cwd, env=env, check=True)


def build_pdfs() -> None:
    tectonic = shutil.which("tectonic") or "/opt/homebrew/bin/tectonic"
    if not Path(tectonic).is_file():
        raise RuntimeError("Tectonic is required to build the submission PDFs")
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    with tempfile.TemporaryDirectory(prefix="stc-jc-tex-") as temp_name:
        temp = Path(temp_name)
        main_out = temp / "main"
        supplement_out = temp / "supplement"
        main_out.mkdir()
        supplement_out.mkdir()
        run(
            [tectonic, "-X", "compile", str(SOURCE / "paper/main.tex"),
             "--outdir", str(main_out), "--keep-logs"],
            cwd=REPO,
            env=env,
        )
        run(
            [tectonic, "-X", "compile", str(SOURCE / "supplement/supplement.tex"),
             "--outdir", str(supplement_out), "--keep-logs"],
            cwd=REPO,
            env=env,
        )
        for log in (main_out / "main.log", supplement_out / "supplement.log"):
            text = log.read_text(encoding="utf-8", errors="replace")
            if "Overfull \\hbox" in text or "Undefined control sequence" in text:
                raise RuntimeError(f"fatal layout/build warning in {log}")
        shutil.copyfile(main_out / "main.pdf", SUBMISSION / MAIN_NAME)
        shutil.copyfile(supplement_out / "supplement.pdf", SUBMISSION / SUPPLEMENT_NAME)


def source_members() -> list[tuple[Path, str]]:
    members: list[tuple[Path, str]] = []
    for path in sorted(SOURCE.rglob("*")):
        if path.is_file() and path.suffix not in {
            ".aux", ".bbl", ".blg", ".log", ".out", ".pdf"
        }:
            members.append((path, path.relative_to(SOURCE).as_posix()))
    return members


def build_source_zip() -> None:
    output = SUBMISSION / SOURCE_ZIP_NAME
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path, name in source_members():
            info = zipfile.ZipInfo(name, ZIP_TIME)
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)


def write_submission_sums() -> None:
    names = [
        MAIN_NAME,
        SUPPLEMENT_NAME,
        SOURCE_ZIP_NAME,
        "BIORXIV_METADATA.md",
        "BIORXIV_UPLOAD_MAP.md",
        "FINAL_HUMAN_CHECKLIST.md",
    ]
    lines = [f"{digest(SUBMISSION / name)}  {name}" for name in names]
    (SUBMISSION / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_submission() -> None:
    SUBMISSION.mkdir(parents=True, exist_ok=True)
    build_pdfs()
    build_source_zip()
    write_submission_sums()


def build_persistent_archive(commit: str) -> None:
    resolved = subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{commit}^{{commit}}"], cwd=REPO, text=True
    ).strip()
    prefixes = ["s_tc_jc_landmark_closure"]
    RELEASE_ASSETS.mkdir(parents=True, exist_ok=True)
    output = RELEASE_ASSETS / ARCHIVE_NAME
    archive_command = [
        "git", "archive", "--format=tar",
        "--prefix=stc_jc_sharp_boundary_reproducibility/",
        resolved,
        *prefixes,
    ]
    with tempfile.TemporaryDirectory(prefix="stc-jc-archive-") as temp_name:
        raw_tar = Path(temp_name) / "release.tar"
        with raw_tar.open("wb") as stream:
            subprocess.run(archive_command, cwd=REPO, stdout=stream, check=True)
        prefix = "stc_jc_sharp_boundary_reproducibility"
        with tarfile.open(raw_tar, "a") as archive:
            commit_bytes = (resolved + "\n").encode()
            info = tarfile.TarInfo(f"{prefix}/ARCHIVE_SOURCE_COMMIT.txt")
            info.size = len(commit_bytes)
            info.mode = 0o644
            info.mtime = 0
            archive.addfile(info, io.BytesIO(commit_bytes))
            transcript_dir = RELEASE_ASSETS / "clean_clone_transcripts"
            for path in sorted(transcript_dir.glob("*.log")):
                data = path.read_bytes()
                info = tarfile.TarInfo(
                    f"{prefix}/s_tc_jc_landmark_closure/release/final_biorxiv/transcripts/{path.name}"
                )
                info.size = len(data)
                info.mode = 0o644
                info.mtime = 0
                archive.addfile(info, io.BytesIO(data))
        with output.open("wb") as raw, gzip.GzipFile(
            filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=0
        ) as compressed, raw_tar.open("rb") as source:
            shutil.copyfileobj(source, compressed, length=1 << 20)
    checksum = f"{digest(output)}  {ARCHIVE_NAME}\n"
    (RELEASE_ASSETS / f"{ARCHIVE_NAME}.sha256").write_text(checksum, encoding="utf-8")
    print(f"source_commit={resolved}")
    print(f"archive={output.relative_to(REPO)}")
    print(f"archive_sha256={digest(output)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("submission", "archive", "all"))
    parser.add_argument("--commit", default="HEAD")
    args = parser.parse_args()
    if args.mode in {"submission", "all"}:
        build_submission()
    if args.mode in {"archive", "all"}:
        build_persistent_archive(args.commit)


if __name__ == "__main__":
    main()
