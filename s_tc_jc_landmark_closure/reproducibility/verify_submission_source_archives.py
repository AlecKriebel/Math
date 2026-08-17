#!/usr/bin/env python3
"""Rebuild every submission PDF from the instructions inside its source ZIP.

This is intentionally an extracted-archive test.  It does not import either
package builder, and it executes the documented archive-local shell commands
verbatim before comparing the resulting PDFs byte for byte with the portal
upload files.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
SOURCE_DATE_EPOCH = "1786838400"


PACKAGES = (
    {
        "name": "biorxiv",
        "zip": PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_source.zip",
        "root": Path("."),
        "anchor": "From the root of the extracted bioRxiv source ZIP",
        "outputs": {
            "paper/main.pdf": PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC.pdf",
            "supplement/supplement.pdf": PROJECT / "biorxiv_submission/Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf",
        },
    },
    {
        "name": "systematic_biology",
        "zip": PROJECT / "journal_submission/systematic_biology/SB_LaTeX_Source.zip",
        "root": Path("SB_LaTeX_Source"),
        "anchor": "From this extracted source directory",
        "outputs": {
            "paper/main.pdf": PROJECT / "journal_submission/systematic_biology/SB_Main_Manuscript.pdf",
            "supplement/supplement.pdf": PROJECT / "journal_submission/systematic_biology/SB_Supplementary_Material.pdf",
        },
    },
    {
        "name": "journal_of_mathematical_biology",
        "zip": PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_LaTeX_Source.zip",
        "root": Path("JMB_LaTeX_Source"),
        "anchor": "From this extracted source directory",
        "outputs": {
            "paper/main.pdf": PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Main_Manuscript.pdf",
            "supplement/supplement.pdf": PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Supplementary_Information.pdf",
        },
    },
)

COVER_LETTERS = (
    (
        PROJECT / "journal_submission/systematic_biology/SB_Cover_Letter.tex",
        PROJECT / "journal_submission/systematic_biology/SB_Cover_Letter.pdf",
    ),
    (
        PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Cover_Letter.tex",
        PROJECT / "journal_submission/journal_of_mathematical_biology/JMB_Cover_Letter.pdf",
    ),
)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def safe_extract(archive_path: Path, destination: Path) -> None:
    with zipfile.ZipFile(archive_path) as archive:
        names = archive.namelist()
        require(names, f"empty source archive: {archive_path}")
        for name in names:
            candidate = Path(name)
            require(not candidate.is_absolute() and ".." not in candidate.parts,
                    f"unsafe ZIP member: {archive_path}: {name}")
            data = archive.read(name)
            if Path(name).suffix.lower() in {".md", ".tex", ".bib", ".sty", ".cls"}:
                text = data.decode("utf-8")
                for leaked in ("/Users/", "/private/tmp/", "file://"):
                    require(leaked not in text,
                            f"local path leaked into {archive_path.name}:{name}")
        archive.extractall(destination)


def documented_commands(build_text: str, anchor: str) -> str:
    require(anchor in build_text, f"archive-local build anchor missing: {anchor}")
    suffix = build_text.split(anchor, 1)[1]
    match = re.search(r"```bash\s*\n(.*?)```", suffix, flags=re.DOTALL)
    require(match is not None, f"archive-local bash block missing after: {anchor}")
    commands = match.group(1).strip()
    require(commands == (
        "cd paper\n"
        "tectonic main.tex\n"
        "cd ../supplement\n"
        "tectonic supplement.tex"
    ), f"unexpected archive-local commands after {anchor}: {commands!r}")
    return commands


def verify_package(spec: dict[str, object]) -> dict[str, str]:
    archive_path = spec["zip"]
    assert isinstance(archive_path, Path)
    require(archive_path.is_file(), f"source archive missing: {archive_path}")
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    with tempfile.TemporaryDirectory(prefix=f"stc-jc-source-replay-{spec['name']}-") as name:
        extracted = Path(name)
        safe_extract(archive_path, extracted)
        root = extracted / spec["root"]
        assert isinstance(root, Path)
        build = root / "BUILD.md"
        require(build.is_file(), f"archive BUILD.md missing: {archive_path}")
        commands = documented_commands(build.read_text(encoding="utf-8"), spec["anchor"])
        subprocess.run(
            ["/bin/bash", "-euo", "pipefail", "-c", commands],
            cwd=root,
            env=env,
            check=True,
        )
        hashes: dict[str, str] = {}
        outputs = spec["outputs"]
        assert isinstance(outputs, dict)
        for relative, expected in outputs.items():
            rebuilt = root / relative
            assert isinstance(expected, Path)
            require(rebuilt.is_file(), f"documented command did not build: {relative}")
            rebuilt_hash = digest(rebuilt)
            expected_hash = digest(expected)
            require(rebuilt_hash == expected_hash,
                    f"extracted-source replay differs: {spec['name']}:{relative}")
            hashes[relative] = rebuilt_hash
        return hashes


def verify_cover_letter(source: Path, expected: Path) -> str:
    require(source.is_file() and expected.is_file(),
            f"cover-letter source/PDF missing: {source}")
    source_text = source.read_text(encoding="utf-8")
    for leaked in ("/Users/", "/private/tmp/", "file://"):
        require(leaked not in source_text, f"local path leaked into {source}")
    env = os.environ.copy()
    env["SOURCE_DATE_EPOCH"] = SOURCE_DATE_EPOCH
    with tempfile.TemporaryDirectory(prefix="stc-jc-cover-replay-") as name:
        root = Path(name)
        copied = root / source.name
        shutil.copyfile(source, copied)
        subprocess.run(["tectonic", copied.name], cwd=root, env=env, check=True)
        rebuilt = copied.with_suffix(".pdf")
        require(digest(rebuilt) == digest(expected),
                f"cover-letter replay differs: {source.name}")
    return digest(expected)


def main() -> None:
    if shutil.which("tectonic") is None and not Path("/opt/homebrew/bin/tectonic").is_file():
        raise RuntimeError("Tectonic is required for extracted-source replay")
    # Make the archive's literal `tectonic` command portable on the standard
    # local setup even when Homebrew is not already in PATH.
    if shutil.which("tectonic") is None:
        os.environ["PATH"] = f"/opt/homebrew/bin:{os.environ.get('PATH', '')}"
    records = {str(spec["name"]): verify_package(spec) for spec in PACKAGES}
    covers = {
        source.name: verify_cover_letter(source, expected)
        for source, expected in COVER_LETTERS
    }
    print("VERIFIED: source replays reproduce all eight delivered PDFs")
    for package, outputs in records.items():
        for relative, value in sorted(outputs.items()):
            print(f"{package}:{relative} {value}")
    for name, value in sorted(covers.items()):
        print(f"cover:{name} {value}")


if __name__ == "__main__":
    main()
