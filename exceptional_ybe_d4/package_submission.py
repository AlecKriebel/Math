#!/usr/bin/env python3
"""Create deterministic Zenodo and arXiv submission artifacts."""

from hashlib import sha256
from pathlib import Path
import shutil
import stat
import sys
from zipfile import ZIP_STORED, ZipFile, ZipInfo

from verify_checksums import main as verify_package_checksums


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "submission"
VERSION = "1.1.2"
# ZIP timestamps have no timezone field; use the visible release time in PDT.
ZIP_TIME = (2026, 8, 16, 11, 0, 0)
PDF_NAME = f"exceptional-ybe-d4-v{VERSION}.pdf"
SOURCE_NAME = f"exceptional-ybe-d4-v{VERSION}-source.zip"
ARXIV_NAME = f"exceptional-ybe-d4-v{VERSION}-arxiv.zip"
CURRENT_OUTPUTS = {
    PDF_NAME,
    SOURCE_NAME,
    ARXIV_NAME,
    "SHA256SUMS",
    "ARXIV_SHA256SUMS",
}
DEPRECATED_OUTPUTS = {
    f"exceptional-ybe-d4-v{VERSION}-source.tar.gz",
    f"exceptional-ybe-d4-v{VERSION}-arxiv.tar.gz",
    "exceptional-ybe-d4-v1.1.1.pdf",
    "exceptional-ybe-d4-v1.1.1-source.zip",
    "exceptional-ybe-d4-v1.1.1-arxiv.zip",
}


def package_files():
    """Yield exactly the verified manifest files, plus the manifest itself."""

    names = ["SHA256SUMS"]
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        _, name = line.split("  ", 1)
        names.append(name)
    for name in names:
        path = ROOT / name
        yield path, Path(name)


def make_zip(path, members):
    with ZipFile(path, mode="w", compression=ZIP_STORED) as archive:
        for data, name, mode in members:
            info = ZipInfo(name, date_time=ZIP_TIME)
            info.create_system = 3
            info.compress_type = ZIP_STORED
            info.external_attr = (stat.S_IFREG | mode) << 16
            archive.writestr(info, data)


def digest(path):
    result = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def main():
    if sys.flags.optimize:
        raise RuntimeError("optimized Python is not permitted for packaging")
    verify_package_checksums()
    if OUT.is_symlink():
        raise RuntimeError("submission output path must not be a symbolic link")
    OUT.mkdir(exist_ok=True)
    if not OUT.is_dir():
        raise RuntimeError("submission output path is not a directory")
    unexpected = sorted(
        path.name
        for path in OUT.iterdir()
        if (
            path.name not in CURRENT_OUTPUTS | DEPRECATED_OUTPUTS
            or path.is_symlink()
            or not path.is_file()
        )
    )
    if unexpected:
        raise RuntimeError(f"unexpected files in submission directory: {unexpected}")
    for name in DEPRECATED_OUTPUTS:
        (OUT / name).unlink(missing_ok=True)
    pdf_source = ROOT / "output" / "pdf" / "exceptional_ybe_d4.pdf"
    pdf_target = OUT / PDF_NAME
    shutil.copyfile(pdf_source, pdf_target)

    prefix = f"exceptional-ybe-d4-v{VERSION}"
    source_members = []
    for path, relative in package_files():
        mode = 0o755 if path.suffix == ".sh" or path.name.endswith(".py") else 0o644
        source_members.append((path.read_bytes(), f"{prefix}/{relative.as_posix()}", mode))
    source_archive = OUT / SOURCE_NAME
    make_zip(source_archive, source_members)

    arxiv_archive = OUT / ARXIV_NAME
    make_zip(arxiv_archive, [((ROOT / "main.tex").read_bytes(), "main.tex", 0o644)])

    zenodo_artifacts = (pdf_target, source_archive)
    checksum_text = "".join(
        f"{digest(path)}  {path.name}\n" for path in zenodo_artifacts
    )
    (OUT / "SHA256SUMS").write_text(checksum_text, encoding="utf-8", newline="\n")
    arxiv_checksum = f"{digest(arxiv_archive)}  {arxiv_archive.name}\n"
    (OUT / "ARXIV_SHA256SUMS").write_text(
        arxiv_checksum,
        encoding="utf-8",
        newline="\n",
    )
    for path in (*zenodo_artifacts, arxiv_archive):
        print(f"created {path.relative_to(ROOT)}")
    print("created submission/SHA256SUMS")
    print("created submission/ARXIV_SHA256SUMS")


if __name__ == "__main__":
    main()
