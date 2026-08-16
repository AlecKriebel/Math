#!/usr/bin/env python3
"""Read-only release-layout and reproducibility audit.

This script deliberately does not decide the mathematical theorem.  It checks
whether the repository is in a state from which a theorem release could be
built and audited without relying on stale generated artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    message: str
    evidence: list[str]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def add(findings: list[Finding], level: str, code: str, message: str, *evidence: str) -> None:
    findings.append(Finding(level, code, message, list(evidence)))


def command_version(command: str) -> str:
    executable = shutil.which(command)
    if executable is None:
        return "MISSING"
    if command in {"pdfinfo", "pdffonts", "pdftoppm"}:
        probes = ([executable, "-v"], [executable, "--version"])
    else:
        probes = ([executable, "--version"], [executable, "-version"], [executable, "-v"])
    for probe in probes:
        try:
            result = subprocess.run(
                probe,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        line = next((line.strip() for line in result.stdout.splitlines() if line.strip()), "")
        if line:
            return line
    return executable


def audit_status(root: Path, findings: list[Finding]) -> None:
    status = root / "repair" / "STATUS.md"
    if not status.exists():
        add(
            findings,
            "BLOCKER",
            "STATUS_LOCK_MISSING",
            "The authoritative repair status is absent from this checkout.",
            rel(status, root),
        )
        return
    text = read_text(status).lower()
    if "withheld" not in text or ("unresolved" not in text and "open" not in text):
        add(
            findings,
            "BLOCKER",
            "STATUS_LOCK_NOT_WITHHELD",
            "The repair status does not fail closed while the theorem gates remain unresolved.",
            rel(status, root),
        )
    else:
        add(
            findings,
            "PASS",
            "STATUS_LOCK",
            "The working repair tree explicitly withholds the positive theorem release.",
            rel(status, root),
        )


INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
BIB_RE = re.compile(r"\\addbibresource\{([^}]+)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}")


def resolve_tex_reference(candidate: str, current: Path, source_root: Path, extensions: tuple[str, ...]) -> Path | None:
    raw = Path(candidate)
    choices: list[Path] = []
    for base in (current.parent, source_root):
        choices.append(base / raw)
        if raw.suffix == "":
            choices.extend(base / f"{candidate}{suffix}" for suffix in extensions)
    for choice in choices:
        if choice.exists():
            return choice.resolve()
    return None


def audit_tex_graph(root: Path, findings: list[Finding]) -> None:
    source_root = root / "source" / "paper"
    main = source_root / "main.tex"
    if not main.exists():
        add(findings, "BLOCKER", "MAIN_SOURCE_MISSING", "Canonical manuscript source is absent.", rel(main, root))
        return

    missing: list[str] = []
    visited: set[Path] = set()
    queue = [main.resolve()]
    while queue:
        current = queue.pop()
        if current in visited:
            continue
        visited.add(current)
        text = read_text(current)
        for reference in INPUT_RE.findall(text):
            target = resolve_tex_reference(reference, current, source_root, (".tex",))
            if target is None:
                missing.append(f"{rel(current, root)} -> {reference}")
            elif target.suffix == ".tex":
                queue.append(target)
        for reference in BIB_RE.findall(text):
            target = resolve_tex_reference(reference, current, source_root, (".bib",))
            if target is None:
                missing.append(f"{rel(current, root)} -> {reference}")
        for reference in GRAPHICS_RE.findall(text):
            target = resolve_tex_reference(reference, current, source_root, (".pdf", ".png", ".jpg", ".jpeg", ".eps"))
            if target is None:
                missing.append(f"{rel(current, root)} -> {reference}")

    if missing:
        add(
            findings,
            "BLOCKER",
            "TEX_INPUT_GRAPH_BROKEN",
            "One or more manuscript inputs cannot be resolved statically.",
            *sorted(missing),
        )
    else:
        add(
            findings,
            "PASS",
            "TEX_INPUT_GRAPH",
            f"The manuscript input graph closes over {len(visited)} TeX files.",
            rel(main, root),
        )

    generated_in_source = sorted(path for path in source_root.rglob("*") if path.is_file() and path.suffix.lower() in {".pdf", ".aux", ".bbl", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".log", ".run.xml", ".synctex.gz"})
    if generated_in_source:
        add(
            findings,
            "BLOCKER",
            "GENERATED_FILES_IN_SOURCE",
            "Generated build products are mixed into the canonical source tree.",
            *(rel(path, root) for path in generated_in_source),
        )


def audit_toolchain(findings: list[Finding]) -> None:
    tools = ("python3", "g++", "latexmk", "biber", "pdfinfo", "pdffonts", "pdftoppm")
    versions = {tool: command_version(tool) for tool in tools}
    missing = [tool for tool, version in versions.items() if version == "MISSING"]
    evidence = [f"{tool}: {versions[tool]}" for tool in tools]
    if missing:
        add(
            findings,
            "BLOCKER",
            "TOOLCHAIN_INCOMPLETE",
            "The advertised paper/release build cannot run in this environment; missing: " + ", ".join(missing),
            *evidence,
        )
    else:
        add(findings, "PASS", "TOOLCHAIN_PRESENT", "All advertised build and PDF-inspection commands are available.", *evidence)


def manifest_inventory(root: Path) -> dict[str, str]:
    excluded_roots = {"repair"}
    excluded_parts = {"transcripts", "tmp", "__pycache__", ".git"}
    excluded_suffixes = {".pyc"}
    inventory: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts[0] in excluded_roots or any(part in excluded_parts for part in relative.parts):
            continue
        if path.suffix in excluded_suffixes or path == root / "MANIFEST.sha256":
            continue
        inventory[relative.as_posix()] = sha256(path)
    return inventory


def parse_manifest(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for number, line in enumerate(read_text(path).splitlines(), 1):
        if not line.strip():
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+\*?(.+)", line)
        if match is None:
            raise ValueError(f"invalid manifest line {number}: {line!r}")
        result[match.group(2)] = match.group(1).lower()
    return result


def audit_manifest(root: Path, findings: list[Finding]) -> None:
    manifest_path = root / "MANIFEST.sha256"
    if not manifest_path.exists():
        add(findings, "BLOCKER", "MANIFEST_MISSING", "The advertised integrity manifest is absent.", rel(manifest_path, root))
        return
    try:
        expected = parse_manifest(manifest_path)
    except ValueError as error:
        add(findings, "BLOCKER", "MANIFEST_INVALID", str(error), rel(manifest_path, root))
        return
    actual = manifest_inventory(root)
    missing = sorted(set(expected) - set(actual))
    extra = sorted(set(actual) - set(expected))
    mismatched = sorted(path for path in set(expected) & set(actual) if expected[path] != actual[path])
    if missing or extra or mismatched:
        evidence = [*(f"missing: {path}" for path in missing), *(f"extra: {path}" for path in extra)]
        evidence.extend(f"hash mismatch: {path} expected={expected[path]} actual={actual[path]}" for path in mismatched)
        add(
            findings,
            "BLOCKER",
            "MANIFEST_NOT_REPRODUCIBLE",
            "The committed manifest does not describe the clean Git mirror inventory.",
            *evidence,
        )
    else:
        add(findings, "PASS", "MANIFEST_MATCH", f"Manifest matches {len(actual)} nontransient files.", rel(manifest_path, root))


def line_hits(path: Path, patterns: tuple[str, ...], root: Path) -> list[str]:
    if not path.exists():
        return []
    hits: list[str] = []
    lowered_patterns = tuple(pattern.lower() for pattern in patterns)
    for number, line in enumerate(read_text(path).splitlines(), 1):
        lowered = line.lower()
        if any(pattern in lowered for pattern in lowered_patterns):
            hits.append(f"{rel(path, root)}:{number}: {line.strip()}")
    return hits


def audit_status_contradictions(root: Path, findings: list[Finding]) -> None:
    bridge = root / "source" / "paper" / "sections" / "04_bridges.tex"
    bridge_hits = line_hits(
        bridge,
        (
            "complete factorization ambiguity",
            "one positive scalar per bridge",
            "removing only the reciprocal arm gauge",
        ),
        root,
    )
    if bridge_hits:
        add(
            findings,
            "BLOCKER",
            "STALE_BRIDGE_CHART",
            "The manuscript still promotes the audited-as-invalid one-scalar bridge chart; downstream localization and dimension claims cannot be released from this source.",
            *bridge_hits,
        )

    candidates = (
        root / "README.md",
        root / "RELEASE_METADATA.json",
        root / "CITATION.cff",
        root / "source" / "paper" / "main.tex",
        root / "source" / "paper" / "sections" / "01_introduction.tex",
        root / "source" / "paper" / "sections" / "03_main_results.tex",
        root / "source" / "paper" / "sections" / "08_global.tex",
        root / "source" / "paper" / "sections" / "11_conclusion.tex",
        root / "docs" / "REFEREE_GUIDE.tex",
        root / "docs" / "COVER_LETTER.tex",
        root / "docs" / "COVER_LETTER_JMB.tex",
        root / "docs" / "COVER_LETTER_BMB.tex",
    )
    phrases = (
        "we prove",
        "main theorem",
        "complete identifiability",
        "generic identifiability",
        "submission-ready",
        "all binary strongly tree-child",
    )
    hits: list[str] = []
    for candidate in candidates:
        hits.extend(line_hits(candidate, phrases, root))
    if hits:
        add(
            findings,
            "BLOCKER",
            "WITHHELD_STATUS_CONTRADICTIONS",
            "Positive theorem/release claims coexist with the authoritative WITHHELD repair status and must remain quarantined until the proof gates close.",
            *hits[:40],
        )


def audit_bibliography(root: Path, findings: list[Finding]) -> None:
    bibliography = root / "source" / "paper" / "references.bib"
    if not bibliography.exists():
        add(findings, "BLOCKER", "BIBLIOGRAPHY_MISSING", "The manuscript bibliography is absent.", rel(bibliography, root))
        return
    text = read_text(bibliography)
    stale = line_hits(bibliography, ("december 23, 2025",), root)
    if stale:
        add(
            findings,
            "BLOCKER",
            "ENGLANDER_VERSION_STALE",
            "The Englander et al. entry is not the current bioRxiv version (v4 was posted July 4, 2026); theorem/proposition numbering must be rechecked against that version.",
            *stale,
        )
    if "2507.23056" not in text:
        add(
            findings,
            "WARNING",
            "PRIOR_WORK_SCOPE_MISSING",
            "The bibliography omits Sullivant, arXiv:2507.23056, which is directly relevant to local modifications and 2-blob/stacked-reticulation nonidentifiability.",
            rel(bibliography, root),
        )
    required_tokens = ("2104.12479", "2607.12919", "2606.26673", "10.1007/s12064-025-00453-8", "10.1007/s11538-025-01506-1")
    absent = [token for token in required_tokens if token not in text]
    if absent:
        add(findings, "WARNING", "PRIOR_WORK_METADATA_GAPS", "Expected current prior-work identifiers are absent.", *(f"missing token: {token}" for token in absent))
    else:
        add(findings, "PASS", "PRIOR_WORK_CORE_PRESENT", "The core Ardiyansyah/Brits/Currie/Holtgrefe/Cox records are present.", rel(bibliography, root))


def audit_release_outputs(root: Path, findings: list[Finding]) -> None:
    source_pdf = root / "source" / "paper" / "main.pdf"
    submission_pdf = root / "submission" / "Generic_Identifiability_STC_Level2_JC.pdf"
    if source_pdf.exists() and submission_pdf.exists():
        source_hash = sha256(source_pdf)
        submission_hash = sha256(submission_pdf)
        if source_hash == submission_hash:
            add(
                findings,
                "WARNING",
                "DUPLICATE_GENERATED_PDF",
                "The same generated manuscript PDF is stored in both source and submission trees; neither location is a safe canonical build target.",
                f"{rel(source_pdf, root)} sha256={source_hash}",
                f"{rel(submission_pdf, root)} sha256={submission_hash}",
            )
        else:
            add(
                findings,
                "BLOCKER",
                "SOURCE_SUBMISSION_PDF_DIVERGENCE",
                "Source-tree and submission manuscript PDFs differ.",
                f"{rel(source_pdf, root)} sha256={source_hash}",
                f"{rel(submission_pdf, root)} sha256={submission_hash}",
            )

    quarantine = [
        "submission/Generic_Identifiability_STC_Level2_JC.pdf",
        "submission/Referee_Guide.pdf",
        "submission/Cover_Letter.pdf",
        "submission/Cover_Letter_JMB.pdf",
        "submission/Cover_Letter_BMB.pdf",
        "source/paper/main.pdf",
        "reproducibility/exact_release/report/FINAL_SHARP_BOUNDARY_THEOREM.md",
        "reproducibility/exact_release/report/FINAL_SHARP_BOUNDARY_THEOREM.pdf",
        "reproducibility/exact_release/certificates/final_theorem.json",
        "reproducibility/exact_release/certificates/final_theorem_output.txt",
        "reproducibility/exact_release/review/final_synthesis_review.json",
        "reproducibility/exact_release/review/final_synthesis_review_output.txt",
        "reproducibility/exact_release/verification_output.txt",
        "reproducibility/exact_release/full_adversarial_verification_output.txt",
        "MANIFEST.sha256",
    ]
    existing = [path for path in quarantine if (root / path).exists()]
    if existing:
        add(
            findings,
            "BLOCKER",
            "HISTORICAL_POSITIVE_RELEASE_PRESENT",
            "Historical positive-theorem release products remain in the active release tree; preserve them as audit history but exclude them from any repaired distribution.",
            *existing,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[3],
        help="project root (default: inferred from script location)",
    )
    parser.add_argument("--json-only", action="store_true", help="emit JSON only")
    args = parser.parse_args()
    root = args.root.resolve()
    findings: list[Finding] = []

    if not (root / "source" / "paper" / "main.tex").exists():
        add(findings, "BLOCKER", "WRONG_PROJECT_ROOT", "The supplied root does not look like this release tree.", str(root))
    else:
        audit_status(root, findings)
        audit_tex_graph(root, findings)
        audit_toolchain(findings)
        audit_manifest(root, findings)
        audit_status_contradictions(root, findings)
        audit_bibliography(root, findings)
        audit_release_outputs(root, findings)

    blockers = [finding for finding in findings if finding.level == "BLOCKER"]
    warnings = [finding for finding in findings if finding.level == "WARNING"]
    payload = {
        "root": str(root),
        "status": "BLOCKED" if blockers else "PASS",
        "counts": {
            "blockers": len(blockers),
            "warnings": len(warnings),
            "passes": sum(finding.level == "PASS" for finding in findings),
        },
        "findings": [asdict(finding) for finding in findings],
    }
    if args.json_only:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"release audit: {payload['status']}")
        print(f"root: {root}")
        print(
            "counts: "
            f"{payload['counts']['blockers']} blocker(s), "
            f"{payload['counts']['warnings']} warning(s), "
            f"{payload['counts']['passes']} pass(es)"
        )
        for finding in findings:
            print(f"\n[{finding.level}] {finding.code}: {finding.message}")
            for item in finding.evidence:
                print(f"  - {item}")
    return 1 if blockers else 0


if __name__ == "__main__":
    sys.exit(main())
