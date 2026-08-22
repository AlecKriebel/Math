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
    certificate_tex_path = submission / "supplement" / "certificate_appendix.tex"
    certificate_json_path = submission / "templates" / "PRINTED_CERTIFICATE_APPENDIX.json"
    sharpness_columns_path = submission / "analysis" / "WEAK_SHARPNESS_COLUMN_CROSSWALK.json"
    bib_path = submission / "article" / "references.bib"
    release_path = project / "work" / "final_theorem_release" / "RELEASE_LOCK.json"
    full_replay_path = submission / "output" / "FINAL_CLEAN_FULL_REPLAY.json"
    full_replay_telemetry_path = (
        submission / "output" / "FINAL_CLEAN_FULL_REPLAY_TELEMETRY.json"
    )
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
        certificate_tex_path,
        certificate_json_path,
        sharpness_columns_path,
        bib_path,
        release_path,
        universe_path,
        full_replay_path,
        full_replay_telemetry_path,
    ):
        require(path.is_file(), f"MISSING_REQUIRED_FILE:{path}")

    article = article_path.read_text(encoding="utf-8")
    supplement = supplement_path.read_text(encoding="utf-8")
    compression = compression_path.read_text(encoding="utf-8")
    certificate_tex = certificate_tex_path.read_text(encoding="utf-8")
    certificate_json = read_json(certificate_json_path)
    sharpness_columns = read_json(sharpness_columns_path)
    bib = bib_path.read_text(encoding="utf-8")
    supplement_source = supplement + "\n" + compression + "\n" + certificate_tex
    all_tex = article + "\n" + supplement_source

    require(isinstance(certificate_json, dict), "PRINTED_APPENDIX_NOT_OBJECT")
    require(
        certificate_json.get("schema") == "k2p-printed-certificate-appendix-v1"
        and certificate_json.get("status") == "PASS"
        and certificate_json.get("quadratic_template_count") == 23
        and certificate_json.get("high_degree_base_count") == 5,
        "PRINTED_APPENDIX_SCHEMA_OR_CENSUS_DRIFT",
    )
    require(isinstance(sharpness_columns, dict), "SHARPNESS_CROSSWALK_NOT_OBJECT")
    require(
        sharpness_columns.get("schema")
        == "k2p-weak-sharpness-column-crosswalk-v1",
        "SHARPNESS_CROSSWALK_SCHEMA_DRIFT",
    )
    require(
        sha256(certificate_json_path) in supplement
        and sha256(sharpness_columns_path) in supplement,
        "PRINTED_SUBMISSION_HASH_BINDING_STALE",
    )

    require(
        sha256(release_path)
        == "58e32bd29f7a039e3da4e47398e32ee8277ad46cf62271a7ed80bf41688b18fb",
        "FROZEN_RELEASE_LOCK_DRIFT",
    )
    release = read_json(release_path)
    require(isinstance(release, dict), "RELEASE_LOCK_NOT_OBJECT")
    require(release.get("promotion_ready") is True, "RELEASE_NOT_PROMOTION_READY")

    full_replay = read_json(full_replay_path)
    full_replay_telemetry = read_json(full_replay_telemetry_path)
    require(isinstance(full_replay, dict), "FULL_REPLAY_NOT_OBJECT")
    require(isinstance(full_replay_telemetry, dict), "FULL_REPLAY_TELEMETRY_NOT_OBJECT")
    require(
        sha256(full_replay_path)
        == "7939b389880de80b7d8abd69022e0b69d2dc4188815854b294d3384fa24c9e18",
        "FULL_REPLAY_REPORT_DRIFT",
    )
    require(
        sha256(full_replay_telemetry_path)
        == "8779854633d9a52ba3d7bc9278ccbcc3918e51987bb4c30204c0adcd9771ce16",
        "FULL_REPLAY_TELEMETRY_DRIFT",
    )
    require(
        full_replay.get("status") == "PASS"
        and full_replay.get("mode") == "full"
        and full_replay.get("promotion_ready") is True
        and full_replay.get("blockers") == []
        and len(full_replay.get("layer_replays", [])) == 35
        and full_replay.get("lock_payload_sha256") == release.get("payload_sha256"),
        "FULL_REPLAY_NOT_PROMOTION_READY_PASS",
    )
    require(
        full_replay_telemetry.get("status") == "PASS"
        and full_replay_telemetry.get("clean_detached_checkout") is True
        and full_replay_telemetry.get("report", {}).get("sha256")
        == sha256(full_replay_path)
        and full_replay_telemetry.get("time_l", {}).get("real_seconds") == 5172.89,
        "FULL_REPLAY_TELEMETRY_INCOHERENT",
    )

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

    for source_name, source in (("article", article), ("supplement", supplement_source)):
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
    citations = tex_keys(article, "cite") + tex_keys(supplement_source, "cite")
    require(not (set(citations) - bib_keys), "UNRESOLVED_CITATION_KEY")
    require(not (bib_keys - set(citations)), "UNUSED_BIBLIOGRAPHY_ENTRY")

    for relative in re.findall(r"\\path\{([^}]+)\}", supplement_source):
        if (
            "/" not in relative
            or relative.startswith("supplement/")
            or relative.startswith("k2p_")
        ):
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
    require("Huber et al." in article and "HuberEtAl2025" in all_tex, "HUBER_ATTRIBUTION_MISSING")
    require(
        "topology-only primitive theorem of Englander" not in article,
        "STALE_ENGLANDER_OVERATTRIBUTION",
    )
    require(
        "Complete graph-derived marginal descriptor" in article
        and "tensor-invisible" in article
        and "not an inheritance-complement quotient" in article,
        "MARGINAL_DESCRIPTOR_GUARDS_MISSING",
    )
    require(
        "analytic submersion theorem" in article
        and "J_0=" in article
        and "J_\\perp=" in article
        and "The inverse function theorem gives strict analytic sections" not in article,
        "TRIANGLE_SUBMERSION_REPAIR_MISSING",
    )
    require(
        "repair-tagged directed completion descriptors" in article
        and "untagged cycle convention" in article,
        "REPAIR_TAGGED_COMPLETION_SEMANTICS_MISSING",
    )
    require(
        "23 literal quadratic bodies" in certificate_tex
        and "Five high-degree bases" in certificate_tex
        and "Three worked paths" in certificate_tex
        and "schema/version" in certificate_tex,
        "PRINTED_CERTIFICATE_APPENDIX_INCOMPLETE",
    )
    require(
        "s_{ZX}" in article and "s_{VX_1}" in article
        and "WEAK_SHARPNESS_COLUMN_CROSSWALK.json" in supplement,
        "NAMED_SHARPNESS_COLUMNS_MISSING",
    )
    require(
        "Proposition~2.8.2" in article and "generic complex Jacobian rank" in article,
        "GENERIC_DIMENSION_HARDENING_MISSING",
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
        "producer command",
        "replay command",
        "mutation command",
        "file SHA-256",
    )
    if not all(field in supplement_source for field in crosswalk_fields):
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
            "supplement/certificate_appendix.tex": sha256(certificate_tex_path),
            "templates/PRINTED_CERTIFICATE_APPENDIX.json": sha256(certificate_json_path),
            "analysis/WEAK_SHARPNESS_COLUMN_CROSSWALK.json": sha256(sharpness_columns_path),
        },
        "frozen_release_sha256": sha256(release_path),
        "clean_full_replay": {
            "status": full_replay["status"],
            "layers": len(full_replay["layer_replays"]),
            "wall_seconds": full_replay_telemetry["time_l"]["real_seconds"],
            "maximum_resident_set_size_bytes": full_replay_telemetry["time_l"]["maximum_resident_set_size_bytes"],
            "peak_memory_footprint_bytes": full_replay_telemetry["time_l"]["peak_memory_footprint_bytes"],
            "report_sha256": sha256(full_replay_path),
            "telemetry_sha256": sha256(full_replay_telemetry_path),
        },
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
