#!/usr/bin/env python3
"""Static consistency and privacy checks for Paper II's submission handoff."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
import sys
import tarfile


HERE = Path(__file__).resolve().parent
PAPER = HERE.parent

REQUIRED = {
    "README.md",
    "BIORXIV_SUBMISSION_INSTRUCTIONS.md",
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
MANUSCRIPT_TITLE = (
    "A fitness-independent family of simultaneous amplifiers beyond "
    "relative fitness $3/2$"
)
PORTAL_TITLE = (
    "A fitness-independent family of simultaneous amplifiers beyond "
    "relative fitness 3/2"
)
PORTAL_ABSTRACT_WORDS = 224
PORTAL_ABSTRACT_SHA256 = (
    "38722f1785b0c24316face5ae2891e5725bf44f84c351e2745adfd2ffd8524b5"
)
MANUSCRIPT_ABSTRACT_WORDS = 208
PORTAL_RUNNING_TITLE = "Simultaneous amplification beyond 3/2"
PORTAL_KEYWORDS = (
    "evolutionary graph theory; Moran process; fixation probability; "
    "simultaneous amplification; Birth-death updating; death-Birth updating"
)
METADATA_CONTRIBUTION = (
    "Alec Kriebel: Conceptualization, formal analysis, methodology, software, "
    "validation, visualization, writing - original draft, and writing - review and "
    "editing. The author determined the scope and claims and accepts "
    "responsibility for the proof, software, manuscript, and accompanying "
    "materials."
)
DECLARATIONS_CONTRIBUTION = (
    "Alec Kriebel: Conceptualization, formal analysis, methodology, software, "
    "validation, visualization, writing - original draft, and writing - review and "
    "editing. The author determined the scope and claims and accepts "
    "responsibility for the proof, software, manuscript, and accompanying "
    "materials."
)
METADATA_FUNDING = (
    "No external funding supported this work. Do not select or invent a funder or "
    "grant number."
)
METADATA_COMPETING_INTERESTS = "The author declares no competing interests."
METADATA_ETHICS = (
    "Not applicable. This study uses no human participants, animals, clinical "
    "material, identifiable personal information, or empirical biological data."
)
DECLARATIONS_ETHICS = (
    "Ethics approval, consent to participate, and consent for publication are not "
    "applicable. The work is mathematical and computational and involves no human "
    "participants, animals, clinical material, or identifiable personal information."
)
PDF_NAME = "simultaneous_amplification_beyond_three_halves.pdf"
PDF_SHA256 = "4e86597bb0baff388e8ce7ccf6ffd808f86b5ea846acf6f2188b31016fd2572c"
SUPPLEMENT_NAME = (
    "simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
)
SUPPLEMENT_SHA256 = (
    "d2145513f8abe295e9e7fab62f062fa9d0f7a6282de95e8155f3db4621485274"
)
AI_DISCLOSURE = (
    "Generative-AI systems were used substantively in mathematical exploration, "
    "derivation, adversarial proof analysis, software development, and manuscript "
    "preparation. The author determined the scope and claims and accepts "
    "responsibility for the manuscript and accompanying materials. All exact "
    "certificates are supplied for independent replay, and numerical evidence is "
    "explicitly separated from proof."
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


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
        normalized(manuscript_title) == normalized(MANUSCRIPT_TITLE),
        "manuscript and submission-metadata titles differ",
    )

    manuscript_abstract = main_tex.split("\\begin{abstract}", 1)[1].split(
        "\\end{abstract}", 1
    )[0]
    abstract_words = words(manuscript_abstract)
    require(
        abstract_words == MANUSCRIPT_ABSTRACT_WORDS,
        "manuscript abstract word count changed: "
        f"{abstract_words} instead of {MANUSCRIPT_ABSTRACT_WORDS}",
    )

    metadata = (HERE / "BIORXIV_METADATA.md").read_text(encoding="utf-8")
    portal_title = metadata.split("**Title**", 1)[1].split(
        "**Running title, if requested**", 1
    )[0].strip()
    require(portal_title == PORTAL_TITLE, "bioRxiv metadata has a stale title")
    require(
        "New Results" in metadata and "Evolutionary Biology" in metadata,
        "bioRxiv metadata has the wrong article category or subject area",
    )
    metadata_normalized = normalized(metadata)
    for exact_line in (
        "- **Server:** bioRxiv",
        "- **Number of authors:** 1",
        "- **Article category:** New Results",
        "- **Author type, only if the live portal presents this exact option:** Regular Article",
        "- **Subject area:** Evolutionary Biology",
        "- **Language:** English",
        "- **Given name:** Alec",
        "- **Family name:** Kriebel",
        "- **Display affiliation:** Independent Researcher",
        "- **Corresponding author:** Yes",
        "- **Corresponding email:** me@aleckriebel.com",
        "- **ORCID:** 0009-0001-9320-500X",
    ):
        require(exact_line in metadata, f"metadata identity mismatch: {exact_line}")
    portal_running_title = metadata.split(
        "**Running title, if requested**", 1
    )[1].split("## Author and correspondence", 1)[0].strip()
    require(
        portal_running_title == PORTAL_RUNNING_TITLE,
        "bioRxiv running title is stale",
    )
    portal_abstract = metadata.split("## Portal abstract", 1)[1].split(
        "\nThe portal abstract", 1
    )[0]
    portal_abstract_words = words(portal_abstract)
    require(
        portal_abstract_words == PORTAL_ABSTRACT_WORDS,
        "portal abstract word count changed: "
        f"{portal_abstract_words} instead of {PORTAL_ABSTRACT_WORDS}",
    )
    require(portal_abstract.isascii(), "portal abstract is not ASCII-safe")
    require(
        hashlib.sha256(normalized(portal_abstract).encode("ascii")).hexdigest()
        == PORTAL_ABSTRACT_SHA256,
        "portal abstract differs from the approved plain-text rendering",
    )
    raw_latex = (
        "$",
        "\\[",
        "\\]",
        "\\Rsim",
        "\\Rhyb",
        "\\geq",
        "\\sigma",
        "\\lambda",
    )
    require(
        not any(marker in portal_abstract for marker in raw_latex),
        "portal abstract contains raw LaTeX markup",
    )
    for phrase in (
        "fitness-independent family",
        "1.5028569127905696",
        "first-order dilute pair-pendant response model",
        "finite universal upper bound",
    ):
        require(
            phrase in metadata_normalized,
            f"bioRxiv metadata is missing required phrase: {phrase}",
        )

    main_normalized = normalized(main_tex)
    portal_keywords = metadata.split("## Keywords", 1)[1].split(
        "\n## Optional significance statement", 1
    )[0].strip()
    require(portal_keywords == PORTAL_KEYWORDS, "bioRxiv keywords are stale")
    for manuscript_keyword, portal_keyword in (
        ("evolutionary graph theory", "evolutionary graph theory"),
        ("Moran process", "Moran process"),
        ("fixation probability", "fixation probability"),
        ("simultaneous amplification", "simultaneous amplification"),
        ("Birth--death updating", "Birth-death updating"),
        ("death--Birth updating", "death-Birth updating"),
    ):
        require(
            manuscript_keyword in main_normalized
            and portal_keyword in metadata_normalized,
            "manuscript/metadata keyword mismatch: "
            f"{manuscript_keyword} / {portal_keyword}",
        )
    for msc in ("92D15", "60J10", "05C81"):
        require(
            msc in main_tex and msc in metadata,
            f"manuscript/metadata MSC mismatch: {msc}",
        )

    instructions = (HERE / "BIORXIV_SUBMISSION_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )
    checklist = (HERE / "BIORXIV_CHECKLIST.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    declarations = (HERE / "DECLARATIONS.md").read_text(encoding="utf-8")
    instructions_overview = instructions.split(
        "## Submission at a glance", 1
    )[1].split("\n## Upload exactly these two files", 1)[0]
    for exact_line in (
        "- **Server:** bioRxiv",
        "- **Subject area:** Evolutionary Biology",
        "- **Article category:** New Results",
        "- **Author count:** 1",
        "- **Main manuscript files:** 1",
        "- **Separate image files:** 0; all figures are embedded in the PDF",
        "- **Supplemental files:** 1",
        "- **Recommended license:** CC BY 4.0, unless the author prefers another option",
    ):
        require(
            exact_line in instructions_overview,
            f"bioRxiv overview mismatch: {exact_line}",
        )
    metadata_contribution = metadata.split("**Author contribution**", 1)[1].split(
        "**Data and code availability**", 1
    )[0].strip()
    require(
        normalized(metadata_contribution) == normalized(METADATA_CONTRIBUTION),
        "bioRxiv author contribution is stale or has extra roles",
    )
    declarations_contribution = declarations.split(
        "## Author contribution", 1
    )[1].split("\n## Data and code availability", 1)[0].strip()
    require(
        normalized(declarations_contribution)
        == normalized(DECLARATIONS_CONTRIBUTION),
        "unified author contribution is stale or has extra roles",
    )
    metadata_funding = metadata.split("**Funding**", 1)[1].split(
        "**Competing interests**", 1
    )[0].strip()
    metadata_competing = metadata.split("**Competing interests**", 1)[1].split(
        "**Ethics and consent**", 1
    )[0].strip()
    metadata_ethics = metadata.split("**Ethics and consent**", 1)[1].split(
        "**Author contribution**", 1
    )[0].strip()
    require(
        normalized(metadata_funding) == normalized(METADATA_FUNDING),
        "bioRxiv funding declaration is stale",
    )
    require(
        normalized(metadata_competing)
        == normalized(METADATA_COMPETING_INTERESTS),
        "bioRxiv competing-interests declaration is stale",
    )
    require(
        normalized(metadata_ethics) == normalized(METADATA_ETHICS),
        "bioRxiv ethics declaration is stale",
    )
    declarations_funding = declarations.split("## Funding", 1)[1].split(
        "\n## Competing interests", 1
    )[0].strip()
    declarations_competing = declarations.split(
        "## Competing interests", 1
    )[1].split("\n## Author contribution", 1)[0].strip()
    declarations_ethics = declarations.split(
        "## Ethics approval and consent", 1
    )[1].split("\n## Materials and permissions", 1)[0].strip()
    require(
        normalized(declarations_funding) == "No external funding supported this work.",
        "unified funding declaration is stale",
    )
    require(
        normalized(declarations_competing) == METADATA_COMPETING_INTERESTS,
        "unified competing-interests declaration is stale",
    )
    require(
        normalized(declarations_ethics) == normalized(DECLARATIONS_ETHICS),
        "unified ethics declaration is stale",
    )
    for marker in (
        "No external funding supported this work.",
        "The author declares no competing interests.",
        "Not applicable. This study uses no human participants, animals, or empirical biological data.",
    ):
        require(
            marker in main_normalized,
            f"frozen manuscript declaration is stale: {marker}",
        )
    for label, document in (
        ("metadata", metadata),
        ("instructions", instructions),
        ("checklist", checklist),
    ):
        for marker in (PDF_SHA256, SUPPLEMENT_SHA256):
            require(marker in document, f"{label} omits frozen marker: {marker}")
        require(
            "New Results" in document and "Evolutionary Biology" in document,
            f"{label} omits the selected category or subject",
        )
    for label, document, markers in (
        (
            "metadata",
            metadata,
            (
                f"`output/pdf/{PDF_NAME}`",
                "- Pages: 21",
                f"`output/release/{SUPPLEMENT_NAME}`",
                "- Archive members: 23",
            ),
        ),
        (
            "instructions",
            instructions,
            (
                f"`output/pdf/{PDF_NAME}`",
                "- 21 pages",
                f"`output/release/{SUPPLEMENT_NAME}`",
                "- 23 regular members",
            ),
        ),
        (
            "checklist",
            checklist,
            ("21-page", "23 regular members"),
        ),
    ):
        for marker in markers:
            require(marker in document, f"{label} omits exact marker: {marker}")
    for doi in (
        "https://doi.org/10.5281/zenodo.21852072",
        "https://doi.org/10.5281/zenodo.21850042",
    ):
        require(doi in metadata, f"bioRxiv metadata omits prior record: {doi}")
    for label, document in (
        ("metadata", metadata),
        ("instructions", instructions),
        ("checklist", checklist),
    ):
        require(
            "do not answer **No**" in document,
            f"{label} omits the prior-online-material decision gate",
        )
        require(
            "copyright" in document and "license" in document,
            f"{label} omits the license-authority decision gate",
        )
    for marker in (
        PDF_NAME,
        SUPPLEMENT_NAME,
        "Main manuscript files:** 1",
        "Separate image files:** 0",
        "Supplemental files:** 1",
        "https://www.biorxiv.org/submit-a-manuscript",
        "https://submit.biorxiv.org/help/submissionhelp.dtl",
        "https://www.biorxiv.org/about-biorxiv",
        "https://connect.biorxiv.org/news/2022/06/13/screening_procedures",
    ):
        require(marker in instructions, f"bioRxiv instructions omit: {marker}")
    require(
        "BIORXIV_SUBMISSION_INSTRUCTIONS.md" in readme,
        "submission README omits the bioRxiv walkthrough",
    )
    require(
        "Only one field is intentionally unresolved" not in readme,
        "submission README understates unresolved human-only decisions",
    )
    for label, document in (
        ("manuscript", main_tex),
        ("metadata", metadata),
        ("declarations", declarations),
        (
            "JMB cover letter",
            (HERE / "JMB_COVER_LETTER.md").read_text(encoding="utf-8"),
        ),
        (
            "TPB cover letter",
            (HERE / "TPB_COVER_LETTER.md").read_text(encoding="utf-8"),
        ),
    ):
        require(
            normalized(AI_DISCLOSURE) in normalized(document),
            f"{label} AI-assistance statement is inconsistent",
        )

    pdf = PAPER / "output" / "pdf" / PDF_NAME
    supplement = PAPER / "output" / "release" / SUPPLEMENT_NAME
    require(pdf.is_file(), f"missing frozen manuscript PDF: {pdf}")
    require(supplement.is_file(), f"missing frozen supplement: {supplement}")
    require(sha256(pdf) == PDF_SHA256, "frozen manuscript PDF digest mismatch")
    require(
        sha256(supplement) == SUPPLEMENT_SHA256,
        "frozen supplemental archive digest mismatch",
    )
    with tarfile.open(supplement, "r:gz") as archive:
        regular_members = [
            member for member in archive.getmembers() if member.isfile()
        ]
    require(
        len(regular_members) == 23,
        f"supplement has {len(regular_members)} regular members instead of 23",
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
        "PASS: submission identity, plain-text metadata, frozen upload hashes, "
        "bioRxiv instructions, provenance, dependency boundary, and highlights"
    )


if __name__ == "__main__":
    main()
