#!/usr/bin/env python3
"""Static consistency checks for Paper I's submission handoff files."""

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
    "bootstrap_replay.sh",
}
ALLOWED_PLACEHOLDERS = {"POSTAL_ADDRESS"}
TITLE = (
    "Complete-Graph Extremality under Death--Birth Updating: "
    "Fitness-Two Local Optimality and Strong-Selection Rigidity"
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
    manuscript_title = main_tex.split("\\title{", 1)[1].split("}\n\\author", 1)[0]
    assert normalized(manuscript_title) == normalized(TITLE)

    manuscript_abstract = main_tex.split("\\begin{abstract}", 1)[1].split(
        "\\end{abstract}", 1
    )[0]
    abstract_words = words(manuscript_abstract)
    assert 150 <= abstract_words <= 250, abstract_words

    metadata = (HERE / "BIORXIV_METADATA.md").read_text(encoding="utf-8")
    assert TITLE in normalized(metadata)
    assert "New Results" in metadata and "Evolutionary Biology" in metadata
    assert "strict nondegenerate local maximizer" in metadata
    assert "full normalized kernel polytope" in metadata

    highlights = (HERE / "TPB_HIGHLIGHTS.txt").read_text(encoding="utf-8").splitlines()
    assert 3 <= len(highlights) <= 5
    assert all(line and len(line) <= 85 for line in highlights)

    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in HERE.iterdir()
        if path.is_file() and path.suffix in {".md", ".txt"}
    )
    placeholders = set(re.findall(r"\[\[([A-Z_]+)\]\]", combined))
    # The tracked handoff templates retain the private-address token, while a
    # human-prepared submission copy may already have replaced it. Reject any
    # unknown token, but accept either state of that final author-only field.
    assert placeholders <= ALLOWED_PLACEHOLDERS, placeholders
    for doi in ("21850042", "21852072"):
        assert re.search(rf"{doi}.{{0,180}}software archive", combined, re.I | re.S)
    assert "major superseding version" in combined

    requirements = [
        line
        for line in (PAPER / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line
    ]
    assert requirements == [
        "sympy==1.14.0",
        "python-flint==0.9.0",
    ]
    environment = (HERE / "ENVIRONMENT.md").read_text(encoding="utf-8")
    for version in ("3.14.6", "1.14.0", "0.9.0", "0.16.9", "26.08.0"):
        assert version in environment

    bootstrap = HERE / "bootstrap_replay.sh"
    assert bootstrap.stat().st_mode & 0o111
    print(
        "PASS: submission identity, abstract range, placeholders, provenance, "
        "and highlights"
    )


if __name__ == "__main__":
    main()
