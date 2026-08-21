#!/usr/bin/env python3
"""Static consistency and privacy checks for Paper II's submission handoff."""

from __future__ import annotations

import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent

REQUIRED = {
    "README.md",
    "BIORXIV_METADATA.md",
    "BIORXIV_CHECKLIST.md",
    "JMB_COVER_LETTER.md",
    "JMB_CHECKLIST.md",
    "TPB_COVER_LETTER.md",
    "TPB_HIGHLIGHTS.txt",
    "TPB_CHECKLIST.md",
    "DECLARATIONS.md",
    "PROVENANCE_AND_RELATED_RELEASES.md",
    "EXTERNAL_COMMUNICATION_BOUNDARY.md",
    "BUNDLE_REPRODUCTION.md",
    "ENVIRONMENT.md",
    "REPRODUCTION_TEST.md",
}
ALLOWED_PLACEHOLDERS = {"POSTAL_ADDRESS"}
TITLE = (
    "A fitness-independent family of simultaneous amplifiers beyond "
    "relative fitness $3/2$"
)


def words(text: str) -> int:
    plain = re.sub(r"\\[A-Za-z]+|[$\\{}~]", " ", text)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", plain))


def normalized(text: str) -> str:
    return " ".join(text.replace("\\\\", " ").split())


def main() -> None:
    names = {path.name for path in HERE.iterdir() if path.is_file()}
    missing = REQUIRED - names
    assert not missing, f"missing submission files: {sorted(missing)}"

    main_tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    manuscript_title = main_tex.split("\\title{", 1)[1].split(
        "}\n\\author", 1
    )[0]
    assert normalized(manuscript_title) == normalized(TITLE)

    manuscript_abstract = main_tex.split("\\begin{abstract}", 1)[1].split(
        "\\end{abstract}", 1
    )[0]
    abstract_words = words(manuscript_abstract)
    assert 150 <= abstract_words <= 250, abstract_words

    metadata = (HERE / "BIORXIV_METADATA.md").read_text(encoding="utf-8")
    assert TITLE in normalized(metadata)
    assert "New Results" in metadata and "Evolutionary Biology" in metadata
    metadata_normalized = normalized(metadata)
    for phrase in (
        "fitness-independent family",
        "1.5028569127905696",
        "first-order dilute pair--pendant response model",
        "finite universal upper bound",
    ):
        assert phrase in metadata_normalized, phrase

    main_normalized = normalized(main_tex)
    for keyword in (
        "evolutionary graph theory",
        "Moran process",
        "fixation probability",
        "simultaneous amplification",
        "Birth--death updating",
        "death--Birth updating",
    ):
        assert keyword in main_normalized and keyword in metadata_normalized
    for msc in ("92D15", "60J10", "05C81"):
        assert msc in main_tex and msc in metadata

    highlights = (HERE / "TPB_HIGHLIGHTS.txt").read_text(encoding="utf-8").splitlines()
    assert 3 <= len(highlights) <= 5
    assert all(line and len(line) <= 85 for line in highlights), [
        (len(line), line) for line in highlights
    ]

    text_files = [
        path
        for path in HERE.iterdir()
        if path.is_file() and path.suffix in {".md", ".txt"}
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in text_files)
    placeholders = set(re.findall(r"\[\[([A-Z_]+)\]\]", combined))
    assert placeholders <= ALLOWED_PLACEHOLDERS, placeholders
    assert "[HUMAN:" not in combined
    assert not re.search(r"PLOS", combined, re.I)

    for doi in ("21753405", "21850042", "21852072"):
        assert re.search(
            rf"{doi}.{{0,240}}(?:source/software|software/source) archive",
            combined,
            re.I | re.S,
        ), doi
    assert "major superseding revision" in combined
    assert "no new Zenodo" in combined

    requirements = [
        line
        for line in (PAPER / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert requirements == ["mpmath==1.3.0", "sympy==1.14.0"]
    environment = (HERE / "ENVIRONMENT.md").read_text(encoding="utf-8")
    for version in ("3.14.6", "1.14.0", "1.3.0", "0.16.9", "26.08.0"):
        assert version in environment
    assert "python-flint" not in environment

    replay = (PAPER / "replay.sh").read_text(encoding="utf-8")
    bundler = (PAPER / "bundle_manifest.py").read_text(encoding="utf-8")
    for forbidden in ("endpoint_affine_global", "audit_core_uniformity.py"):
        assert forbidden not in replay
    # The bundler names excluded patterns in its defensive archive scan; make
    # sure that protection is present rather than mistaking the literal guard
    # text for an included dependency.
    assert "forbidden non-proof dependency in archive" in bundler

    for executable in (
        PAPER / "replay.sh",
        PAPER / "build.sh",
        PAPER / "all.sh",
        PAPER / "release_bundle.sh",
        PAPER / "bootstrap_replay.sh",
    ):
        assert executable.stat().st_mode & 0o111, f"not executable: {executable}"

    print(
        "PASS: submission identity, abstract range, keywords, placeholders, "
        "provenance, dependency boundary, and highlights"
    )


if __name__ == "__main__":
    main()
