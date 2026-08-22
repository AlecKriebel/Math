#!/usr/bin/env python3
"""Static consistency and privacy checks for Paper II's submission handoff."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
import sys


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
VENDOR_HASHES = {
    "mpmath-1.3.0-py3-none-any.whl":
        "a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c",
    "sympy-1.14.0-py3-none-any.whl":
        "e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5",
}


class VerificationError(RuntimeError):
    """Raised when the submission handoff is internally inconsistent."""


def require(condition: object, message: str) -> None:
    """Fail closed without relying on optimization-sensitive assertions."""
    if not bool(condition):
        raise VerificationError(message)


def reject_optimized_python() -> None:
    if sys.flags.optimize != 0:
        raise SystemExit(
            "ERROR: optimized Python is unsupported because verification "
            "checks must remain active"
        )


def words(text: str) -> int:
    plain = re.sub(r"\\[A-Za-z]+|[$\\{}~]", " ", text)
    return len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", plain))


def normalized(text: str) -> str:
    return " ".join(text.replace("\\\\", " ").split())


def main() -> None:
    reject_optimized_python()
    names = {path.name for path in HERE.iterdir() if path.is_file()}
    missing = REQUIRED - names
    require(not missing, f"missing submission files: {sorted(missing)}")

    main_tex = (PAPER / "main.tex").read_text(encoding="utf-8")
    manuscript_title = main_tex.split("\\title{", 1)[1].split(
        "}\n\\author", 1
    )[0]
    require(
        normalized(manuscript_title) == normalized(TITLE),
        "manuscript and submission-metadata titles differ",
    )

    manuscript_abstract = main_tex.split("\\begin{abstract}", 1)[1].split(
        "\\end{abstract}", 1
    )[0]
    abstract_words = words(manuscript_abstract)
    require(
        150 <= abstract_words <= 250,
        f"bioRxiv abstract word count is outside [150,250]: {abstract_words}",
    )

    metadata = (HERE / "BIORXIV_METADATA.md").read_text(encoding="utf-8")
    require(TITLE in normalized(metadata), "bioRxiv metadata has a stale title")
    require(
        "New Results" in metadata and "Evolutionary Biology" in metadata,
        "bioRxiv metadata has the wrong article type or subject category",
    )
    metadata_normalized = normalized(metadata)
    for phrase in (
        "fitness-independent family",
        "1.5028569127905696",
        "first-order dilute pair--pendant response model",
        "finite universal upper bound",
    ):
        require(
            phrase in metadata_normalized,
            f"bioRxiv metadata is missing required phrase: {phrase}",
        )

    main_normalized = normalized(main_tex)
    for keyword in (
        "evolutionary graph theory",
        "Moran process",
        "fixation probability",
        "simultaneous amplification",
        "Birth--death updating",
        "death--Birth updating",
    ):
        require(
            keyword in main_normalized and keyword in metadata_normalized,
            f"manuscript/metadata keyword mismatch: {keyword}",
        )
    for msc in ("92D15", "60J10", "05C81"):
        require(
            msc in main_tex and msc in metadata,
            f"manuscript/metadata MSC mismatch: {msc}",
        )

    highlights = (HERE / "TPB_HIGHLIGHTS.txt").read_text(encoding="utf-8").splitlines()
    require(
        3 <= len(highlights) <= 5,
        f"TPB highlights must contain 3--5 lines, found {len(highlights)}",
    )
    invalid_highlights = [
        (len(line), line) for line in highlights if not line or len(line) > 85
    ]
    require(
        not invalid_highlights,
        f"empty or overlong TPB highlights: {invalid_highlights}",
    )

    text_files = [
        path
        for path in HERE.iterdir()
        if path.is_file() and path.suffix in {".md", ".txt"}
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in text_files)
    placeholders = set(re.findall(r"\[\[([A-Z_]+)\]\]", combined))
    require(
        placeholders <= ALLOWED_PLACEHOLDERS,
        f"unexpected submission placeholders: {sorted(placeholders)}",
    )
    require("[HUMAN:" not in combined, "unresolved human-action marker remains")
    require(
        not re.search(r"PLOS", combined, re.I),
        "submission handoff contains stale PLOS text",
    )

    for doi in ("21753405", "21850042", "21852072"):
        require(
            re.search(
                rf"{doi}.{{0,240}}(?:source/software|software/source) archive",
                combined,
                re.I | re.S,
            ),
            f"DOI {doi} is not labelled as a prior source/software archive",
        )
    require(
        "major superseding revision" in combined,
        "submission handoff omits superseding-revision provenance",
    )
    require(
        "no new Zenodo" in combined,
        "submission handoff omits the no-new-Zenodo instruction",
    )

    requirements = [
        line
        for line in (PAPER / "requirements.txt").read_text(encoding="utf-8").splitlines()
        if line
    ]
    expected_requirements = [
        "--no-index",
        "--find-links vendor",
        "--only-binary=:all:",
        "--require-hashes",
        "mpmath==1.3.0 \\",
        "    --hash=sha256:"
        "a0b2b9fe80bbcd81a6647ff13108738cfb482d481d826cc0e02f5b35e5c88d2c",
        "sympy==1.14.0 \\",
        "    --hash=sha256:"
        "e091cc3e99d2141a0ba2847328f5479b05d94a6635cb96148ccb3f34671bd8f5",
    ]
    require(
        requirements == expected_requirements,
        f"unexpected Python requirements: {requirements}",
    )
    vendor = PAPER / "vendor"
    require(
        {path.name for path in vendor.iterdir() if path.is_file()}
        == {"README.md", *VENDOR_HASHES},
        "vendor directory has a missing or unexpected file",
    )
    for name, expected_digest in VENDOR_HASHES.items():
        wheel = vendor / name
        require(not wheel.is_symlink(), f"vendored wheel is a symlink: {wheel}")
        actual_digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
        require(
            actual_digest == expected_digest,
            f"vendored wheel digest mismatch: {name}",
        )
    vendor_note = (vendor / "README.md").read_text(encoding="utf-8")
    for marker in ("pypi.org/project/mpmath/1.3.0", "pypi.org/project/sympy/1.14.0"):
        require(marker in vendor_note, f"vendor provenance note omits {marker}")
    environment = (HERE / "ENVIRONMENT.md").read_text(encoding="utf-8")
    for version in ("3.14.6", "1.14.0", "1.3.0", "0.16.9", "26.08.0"):
        require(
            version in environment,
            f"environment record omits pinned version {version}",
        )
    require(
        "python-flint" not in environment,
        "environment record includes an undeclared python-flint dependency",
    )
    require(
        "without network access" in " ".join(environment.split()),
        "environment record does not state the offline Python replay boundary",
    )
    reproduction = (HERE / "REPRODUCTION_TEST.md").read_text(encoding="utf-8")
    for marker in (
        "23 regular members",
        "21-page PDF",
        "d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274",
        "4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c",
        "simultaneous-amplification-beyond-three-halves-v2.0.2",
    ):
        require(
            marker in reproduction,
            f"reproduction record omits current freeze marker: {marker}",
        )
    bundle_record = (HERE / "BUNDLE_REPRODUCTION.md").read_text(encoding="utf-8")
    for marker in ("21 source files", "23 regular members"):
        require(
            marker in bundle_record,
            f"bundle record omits current member count: {marker}",
        )

    replay = (PAPER / "replay.sh").read_text(encoding="utf-8")
    bundler = (PAPER / "bundle_manifest.py").read_text(encoding="utf-8")
    for forbidden in ("endpoint_affine_global", "audit_core_uniformity.py"):
        require(
            forbidden not in replay,
            f"replay invokes forbidden discovery artifact: {forbidden}",
        )
    # The bundler names excluded patterns in its defensive archive scan; make
    # sure that protection is present rather than mistaking the literal guard
    # text for an included dependency.
    require(
        "forbidden non-proof dependency in archive" in bundler,
        "archive builder omits its forbidden-dependency guard",
    )

    for executable in (
        PAPER / "replay.sh",
        PAPER / "build.sh",
        PAPER / "all.sh",
        PAPER / "release_bundle.sh",
        PAPER / "bootstrap_replay.sh",
    ):
        require(
            executable.stat().st_mode & 0o111,
            f"not executable: {executable}",
        )

    print(
        "PASS: submission identity, abstract range, keywords, placeholders, "
        "provenance, dependency boundary, and highlights"
    )


if __name__ == "__main__":
    main()
