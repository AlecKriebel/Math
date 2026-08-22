#!/usr/bin/env python3
"""Fail-closed static audit of the K2P article and reader supplement."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def line_number(text: str, needle: str) -> int | None:
    for number, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return number
    return None


def offset_line(text: str, offset: int) -> int:
    """Return the one-based source line containing a character offset."""
    return text.count("\n", 0, offset) + 1


def tex_keys(text: str, command: str) -> list[str]:
    pattern = rf"\\{command}(?:\[[^]]*\])?\{{([^}}]+)\}}"
    values: list[str] = []
    for group in re.findall(pattern, text):
        values.extend(item.strip() for item in group.split(","))
    return values


def main() -> None:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")

    submission = Path(__file__).resolve().parents[1]
    project = submission.parent
    article_path = submission / "article" / "main.tex"
    supplement_path = submission / "supplement" / "supplement.tex"
    compression_path = submission / "supplement" / "compression_tables.tex"
    bib_path = submission / "article" / "references.bib"
    release_path = project / "work" / "final_theorem_release" / "RELEASE_LOCK.json"
    universe_path = (
        project
        / "work"
        / "final_theorem_release"
        / "corrected_universe_certificate.json"
    )

    for path in (
        article_path,
        supplement_path,
        compression_path,
        bib_path,
        release_path,
        universe_path,
    ):
        require(path.is_file(), f"MISSING_REQUIRED_FILE:{path}")

    article = article_path.read_text(encoding="utf-8")
    supplement = supplement_path.read_text(encoding="utf-8")
    compression = compression_path.read_text(encoding="utf-8")
    bib = bib_path.read_text(encoding="utf-8")
    all_tex = article + "\n" + supplement + "\n" + compression

    require(
        sha256(release_path)
        == "0c17eeaa3344f0982998ea694c1eb92f72f5ced0841e2acad0d39566e2ec71c3",
        "FROZEN_RELEASE_LOCK_DRIFT",
    )
    release = read_json(release_path)
    require(isinstance(release, dict), "RELEASE_LOCK_NOT_OBJECT")
    require(release.get("promotion_ready") is True, "RELEASE_NOT_PROMOTION_READY")

    universe = read_json(universe_path)
    require(isinstance(universe, dict), "UNIVERSE_NOT_OBJECT")
    families = universe.get("families")
    require(isinstance(families, dict), "UNIVERSE_FAMILIES_MISSING")
    expected_inputs = {
        "raw4": 405216,
        "theta2": 2946240,
        "cycle": 13440,
        "restoration": 2540,
        "probe": 574535,
    }
    for family, expected in expected_inputs.items():
        row = families.get(family)
        require(isinstance(row, dict), f"FAMILY_MISSING:{family}")
        require(row.get("input_count") == expected, f"FAMILY_COUNT_DRIFT:{family}")
        require(row.get("unresolved") == 0, f"FAMILY_UNRESOLVED:{family}")

    for token in (
        "405{,}216",
        "2{,}946{,}240",
        "36,824",
        "29,964",
        "544,571",
        "997",
        "297",
        "PC-PARTIAL",
    ):
        require(token in all_tex, f"SUBMISSION_COUNT_OR_STATUS_MISSING:{token}")

    for source_name, source in (("article", article), ("supplement", supplement)):
        label_occurrences = re.findall(r"\\label\{([^}]+)\}", source)
        require(
            len(label_occurrences) == len(set(label_occurrences)),
            f"DUPLICATE_TEX_LABEL:{source_name}",
        )
        references: list[str] = []
        for command in ("ref", "eqref", "cref", "Cref"):
            references.extend(tex_keys(source, command))
        require(
            not (set(references) - set(label_occurrences)),
            f"UNRESOLVED_INTERNAL_REFERENCE:{source_name}",
        )

    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    citations = tex_keys(article, "cite") + tex_keys(supplement, "cite")
    require(not (set(citations) - bib_keys), "UNRESOLVED_CITATION_KEY")
    require(not (bib_keys - set(citations)), "UNUSED_BIBLIOGRAPHY_ENTRY")

    for relative in re.findall(r"\\path\{([^}]+)\}", supplement):
        if relative.startswith("supplement/") or relative.startswith("k2p_"):
            continue
        require((project / relative).exists(), f"CROSSWALK_PATH_MISSING:{relative}")

    require("whole semi-directed maps" in all_tex, "WHOLE_MAP_TI_CLAUSE_MISSING")
    require(
        "A rooted restriction type\nis not used as a topology oracle" in supplement,
        "ROOTED_ORACLE_REJECTION_MISSING",
    )
    require(
        "not asserted to be a\ngraph-transport quotient" in article,
        "RESTORATION_NONQUOTIENT_CLAUSE_MISSING",
    )
    require(
        "not\nmisreported as three literal polynomials" in article,
        "DIRECT36_LITERAL_BODY_WARNING_MISSING",
    )
    require(
        "It does not assert equality of the complete\nstochastic images" in article,
        "COMPLETE_IMAGE_NONCLAIM_GUARD_MISSING",
    )

    for pending in (
        "Corresponding email: \\emph{pending human confirmation}",
        "Funding statement: \\textbf{pending human confirmation}",
        "Competing-interests declaration: \\textbf{pending human confirmation}",
    ):
        require(pending in article, f"PENDING_METADATA_GUARD_MISSING:{pending}")

    findings: list[dict[str, object]] = []
    local_relation_is_defined = (
        "\\Theta_+(H)" in article
        or "projective local containment" in article.lower()
        or "ported-factor containment" in article.lower()
    )
    if "H\\preceqplus H'" in article and not local_relation_is_defined:
        findings.append(
            {
                "severity": "major_formal",
                "code": "LOCAL_PROJECTIVE_RELATION_UNDEFINED",
                "lines": [
                    line_number(article, "source-relative full-dimensional regular germ"),
                    line_number(article, "H\\preceqplus H'"),
                ],
            }
        )

    if (
        "smooth\nsemialgebraic constant-rank strata" in article
        and "Nash" not in article
        and "physical analytic target section" in article
    ):
        findings.append(
            {
                "severity": "major_formal",
                "code": "ANALYTIC_SECTION_NOT_JUSTIFIED_BY_SMOOTH_STRATIFICATION",
                "lines": [
                    line_number(article, "semialgebraic constant-rank strata"),
                    line_number(article, "constant-rank theorem supplies a physical analytic"),
                ],
            }
        )

    if (
        "Adjoin the zero\nsets of only those finitely many" in article
        and "\\V_N\\cap Z(" not in article
    ):
        findings.append(
            {
                "severity": "major_formal",
                "code": "PARAMETER_PULLBACK_ZERO_SET_ADJOINED_TO_OUTPUT_VARIETY",
                "lines": [line_number(article, "sets of only those finitely many")],
                "note": (
                    "Use output zero sets V_N intersect Z(P), with nonzero "
                    "P composed with Phi_N proving properness; use closures of "
                    "images for parameter-only rank loci."
                ),
            }
        )

    if "\\binom" not in article + supplement + compression:
        findings.append(
            {
                "severity": "minor_exposition",
                "code": "CLAIMED_COMPLETION_FORMULA_NOT_DISPLAYED_IN_PAPER",
                "lines": [line_number(article, "one stars-and-bars formula")],
            }
        )

    if "three orbit propositions" in article:
        findings.append(
            {
                "severity": "minor_precision",
                "code": "ORBIT_WORDING_BROADER_THAN_CERTIFIED_FAMILY_WORDING",
                "lines": [line_number(article, "three orbit propositions")],
            }
        )

    if "Q_{j=C,a=C,b=0" not in all_tex:
        findings.append(
            {
                "severity": "moderate_proof_exposition",
                "code": "CHERRY_QUANTITIES_NOT_SHOWN_TO_BE_TENSOR_OBSERVABLES",
                "lines": [line_number(article, "use the four local observables")],
                "note": (
                    "The exact Fourier ratios and recovery-by-division are "
                    "available in work/weak_sharpness_audit/PROOF_AUDIT.md."
                ),
            }
        )

    crosswalk_fields = (
        "schema/version",
        "semantic payload SHA-256",
        "expected runtime",
    )
    if not all(field in supplement for field in crosswalk_fields):
        findings.append(
            {
                "severity": "moderate_submission",
                "code": "READER_CROSSWALK_OMITS_REQUESTED_PER_LAYER_FIELDS",
                "lines": [
                    line_number(supplement, "Theorem-to-artifact crosswalk"),
                    line_number(supplement, "Frozen hash anchors"),
                    line_number(supplement, "Replay protocol"),
                ],
                "note": (
                    "The machine-readable crosswalk carries more detail, but "
                    "the reader supplement does not tabulate every requested "
                    "schema/payload/runtime/command field per theorem layer."
                ),
            }
        )

    sharpness = re.search(
        r"\\begin\{theorem\}\[Weak-class.*?\\end\{theorem\}",
        article,
        flags=re.DOTALL,
    )
    require(sharpness is not None, "SHARPNESS_THEOREM_MISSING")
    if "full-dimensional" not in sharpness.group(0):
        findings.append(
            {
                "severity": "minor_precision",
                "code": "SHARPNESS_STATEMENT_OMITS_FULL_DIMENSIONAL_QUALIFIER",
                "lines": [line_number(article, "contain a common regular analytic germ")],
            }
        )

    if "\\M_{\\mathrm{CT}}(N)" not in article:
        findings.append(
            {
                "severity": "minor_definition",
                "code": "CONTINUOUS_TIME_IMAGE_AND_MAXIMAL_RANK_NOT_DEFINED",
                "lines": [line_number(article, "\\Theta_{\\mathrm{CT}}(N)")],
                "note": (
                    "Define the CT image and note that openness gives the same "
                    "maximal rank and complex image closure as the principal domain."
                ),
            }
        )

    englander = re.search(
        r"@article\{EnglanderEtAl2026,.*?year\s*=\s*\{(\d{4})\}",
        bib,
        flags=re.DOTALL,
    )
    require(englander is not None, "ENGLANDER_BIB_ENTRY_MISSING")
    if englander.group(1) != "2025":
        findings.append(
            {
                "severity": "minor_bibliography",
                "code": "ENGLANDER_ISSUED_YEAR_NEEDS_RECONCILIATION",
                "lines": [offset_line(bib, englander.start(1))],
                "note": "Crossref issued/posted metadata are 24 April 2025; version 4 is dated 4 July 2026.",
            }
        )

    findings.append(
        {
            "severity": "human_confirmation",
            "code": "AUTHOR_CONTRIBUTION_AND_SUBMISSION_METADATA_REQUIRE_HUMAN_SIGNOFF",
            "lines": [
                line_number(article, "Alec Kriebel conceived and directed"),
                line_number(article, "pending explicit human confirmation"),
            ],
        }
    )

    result = {
        "status": "PASS_WITH_REVIEW_FINDINGS",
        "source_sha256": {
            "article/main.tex": sha256(article_path),
            "article/references.bib": sha256(bib_path),
            "supplement/supplement.tex": sha256(supplement_path),
            "supplement/compression_tables.tex": sha256(compression_path),
        },
        "frozen_release_sha256": sha256(release_path),
        "frozen_counts": expected_inputs,
        "findings": findings,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except AuditFailure as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True))
        raise SystemExit(1) from exc
