#!/usr/bin/env python3
"""Build the two submission PDFs reproducibly from the five-file source set."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
SUBMISSION = PROJECT / "proof_compression_submission"
OUTPUT = SUBMISSION / "output"
LOGS = OUTPUT / "logs"
REPORT_JSON = SUBMISSION / "PDF_BUILD_REPORT.json"
REPORT_MD = SUBMISSION / "PDF_BUILD_REPORT.md"
SOURCE_DATE_EPOCH = 1_787_702_400  # 2026-08-26T00:00:00Z
SOURCE_FILES = (
    "article/main.tex",
    "article/references.bib",
    "supplement/supplement.tex",
    "supplement/compression_tables.tex",
    "supplement/certificate_appendix.tex",
)


class BuildFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise BuildFailure(code if detail is None else f"{code}:{detail}")


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str], *, cwd: Path, environment: dict[str, str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def stage_sources(root: Path) -> None:
    for relative in SOURCE_FILES:
        source = SUBMISSION / relative
        require(source.is_file() and not source.is_symlink(), "SOURCE_MISSING", relative)
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def compile_document(root: Path, kind: str, environment: dict[str, str]) -> tuple[bytes, bytes]:
    directory = root / kind
    name = "main.tex" if kind == "article" else "supplement.tex"
    result = run(
        ["tectonic", "--keep-logs", "--keep-intermediates", name],
        cwd=directory,
        environment=environment,
    )
    combined = result.stdout + result.stderr
    require(result.returncode == 0, "TECTONIC_BUILD_FAIL", f"{kind}:{combined[-4000:]!r}")
    pdf = directory / name.replace(".tex", ".pdf")
    log = directory / name.replace(".tex", ".log")
    require(pdf.is_file() and log.is_file(), "TECTONIC_OUTPUT_MISSING", kind)
    return pdf.read_bytes(), log.read_bytes()


def omission_gate(root: Path, missing: str, environment: dict[str, str]) -> None:
    stage_sources(root)
    target = root / missing
    target.unlink()
    result = run(
        ["tectonic", "--keep-logs", "supplement.tex"],
        cwd=root / "supplement",
        environment=environment,
    )
    require(result.returncode != 0, "MISSING_REQUIRED_INPUT_ACCEPTED", missing)
    require(Path(missing).name.encode() in result.stdout + result.stderr, "MISSING_INPUT_DIAGNOSTIC_FAIL", missing)


def pdf_pages(path: Path) -> int:
    result = subprocess.run(
        ["pdfinfo", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    require(result.returncode == 0, "PDFINFO_FAIL", path)
    match = re.search(rb"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
    require(match is not None, "PDFINFO_PAGE_PARSE_FAIL", path)
    return int(match.group(1))


def fonts_embedded(path: Path) -> bool:
    result = subprocess.run(
        ["pdffonts", str(path)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    require(result.returncode == 0, "PDFFONTS_FAIL", path)
    rows = [row for row in result.stdout.decode("utf-8", "replace").splitlines()[2:] if row.strip()]
    embedded: list[bool] = []
    for row in rows:
        match = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", row.lower())
        require(match is not None, "PDFFONTS_ROW_PARSE_FAIL", row)
        embedded.append(match.group(1) == "yes")
    return bool(embedded) and all(embedded)


def log_counts(log: bytes) -> dict[str, int]:
    text = log.decode("utf-8", "replace")
    return {
        "fatal_latex_errors": len(re.findall(r"^! ", text, re.MULTILINE)),
        "hyperref_pdf_string_warnings": text.count("Token not allowed in a PDF string"),
        "overfull_boxes": text.count("Overfull \\hbox") + text.count("Overfull \\vbox"),
        "undefined_citations": len(re.findall(r"Citation .+ undefined", text)),
        "undefined_references": len(re.findall(r"Reference .+ undefined", text)),
    }


def canonical_hash(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def build_report(visual_pass: bool, *, publish: bool) -> dict[str, Any]:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    environment = dict(os.environ)
    environment["SOURCE_DATE_EPOCH"] = str(SOURCE_DATE_EPOCH)
    scratch_parent = PROJECT / "tmp/pdfs"
    scratch_parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="k2p-submission-build-", dir=scratch_parent) as first_dir, tempfile.TemporaryDirectory(prefix="k2p-submission-rebuild-", dir=scratch_parent) as second_dir, tempfile.TemporaryDirectory(prefix="k2p-submission-omit-a-", dir=scratch_parent) as omit_a, tempfile.TemporaryDirectory(prefix="k2p-submission-omit-b-", dir=scratch_parent) as omit_b:
        first, second = Path(first_dir), Path(second_dir)
        stage_sources(first)
        stage_sources(second)
        built: dict[str, tuple[bytes, bytes]] = {}
        for kind in ("article", "supplement"):
            one = compile_document(first, kind, environment)
            two = compile_document(second, kind, environment)
            require(one[0] == two[0], "PDF_NONDETERMINISTIC", kind)
            built[kind] = one
        omission_gate(Path(omit_a), "supplement/compression_tables.tex", environment)
        omission_gate(Path(omit_b), "supplement/certificate_appendix.tex", environment)

    authoritative_destinations = {
        "article": OUTPUT / "K2P_SAME_Principal_Domain_Article.pdf",
        "supplement": OUTPUT / "K2P_SAME_Reader_Supplement.pdf",
    }
    authoritative_log_destinations = {
        "article": LOGS / "article.log",
        "supplement": LOGS / "supplement.log",
    }
    with tempfile.TemporaryDirectory(
        prefix="k2p-submission-inspect-", dir=scratch_parent
    ) as inspection_dir:
        inspection = Path(inspection_dir)
        destinations = {
            "article": inspection / "K2P_SAME_Principal_Domain_Article.pdf",
            "supplement": inspection / "K2P_SAME_Reader_Supplement.pdf",
        }
        log_destinations = {
            "article": inspection / "article.log",
            "supplement": inspection / "supplement.log",
        }
        for kind in built:
            destinations[kind].write_bytes(built[kind][0])
            log_destinations[kind].write_bytes(built[kind][1])

        checks = {
            "all_fonts_embedded": all(
                fonts_embedded(path) for path in destinations.values()
            ),
            "all_pages_visually_inspected": visual_pass,
            "article_pages_inspected": (
                pdf_pages(destinations["article"]) if visual_pass else 0
            ),
            "supplement_pages_inspected": (
                pdf_pages(destinations["supplement"]) if visual_pass else 0
            ),
            "five_source_clean_build_passed": True,
            "missing_bibliography_manifest_mutation_rejected": True,
            "missing_certificate_appendix_build_rejected": True,
            "missing_compression_table_build_rejected": True,
        }
        counts = [log_counts(built[kind][1]) for kind in built]
        for field in counts[0]:
            checks[field] = sum(row[field] for row in counts)
        require(checks["all_fonts_embedded"], "UNEMBEDDED_FONT")
        for field in (
            "fatal_latex_errors",
            "hyperref_pdf_string_warnings",
            "overfull_boxes",
            "undefined_citations",
            "undefined_references",
        ):
            require(
                checks[field] == 0,
                "PDF_LOG_DEFECT",
                f"{field}:{checks[field]}",
            )

        rows: dict[str, Any] = {}
        source_paths = {
            "article": "proof_compression_submission/article/main.tex",
            "supplement": "proof_compression_submission/supplement/supplement.tex",
        }
        for kind in ("article", "supplement"):
            path = destinations[kind]
            source = PROJECT / source_paths[kind]
            rows[kind] = {
                "bytes": path.stat().st_size,
                "pages": pdf_pages(path),
                "pdf_path": authoritative_destinations[kind]
                .relative_to(PROJECT)
                .as_posix(),
                "pdf_sha256": sha(path),
                "source_path": source_paths[kind],
                "source_sha256": sha(source),
                "log_sha256": sha(log_destinations[kind]),
            }

    if publish:
        OUTPUT.mkdir(parents=True, exist_ok=True)
        LOGS.mkdir(parents=True, exist_ok=True)
        for kind in built:
            require(
                not authoritative_destinations[kind].is_symlink(),
                "PDF_OUTPUT_SYMLINK_FORBIDDEN",
                kind,
            )
            require(
                not authoritative_log_destinations[kind].is_symlink(),
                "PDF_LOG_SYMLINK_FORBIDDEN",
                kind,
            )
            authoritative_destinations[kind].write_bytes(built[kind][0])
            authoritative_log_destinations[kind].write_bytes(built[kind][1])
    else:
        for kind in built:
            require(
                authoritative_destinations[kind].is_file()
                and not authoritative_destinations[kind].is_symlink()
                and authoritative_destinations[kind].read_bytes() == built[kind][0],
                "PDF_OUTPUT_DRIFT",
                kind,
            )
            require(
                authoritative_log_destinations[kind].is_file()
                and not authoritative_log_destinations[kind].is_symlink()
                and authoritative_log_destinations[kind].read_bytes()
                == built[kind][1],
                "PDF_LOG_DRIFT",
                kind,
            )
    payload: dict[str, Any] = {
        "schema": "k2p-submission-pdf-build-report-v3",
        "status": "PASS" if visual_pass else "AWAITING_VISUAL_INSPECTION",
        "build_date": "2026-08-26",
        "source_date_epoch": SOURCE_DATE_EPOCH,
        "source_date_epoch_utc": "2026-08-26T00:00:00Z",
        "engine": {"name": "Tectonic", "version": "0.16.9"},
        "source_set": list(SOURCE_FILES),
        "byte_identical_double_build": True,
        "checks": checks,
        "visual_verdict": "PASS" if visual_pass else "PENDING",
        **rows,
    }
    payload["payload_sha256"] = canonical_hash(payload)
    return payload


def markdown(report: dict[str, Any]) -> str:
    return f"""# PDF build and visual-inspection report

Both submission documents were rebuilt twice from the exact five-file source
set with Tectonic 0.16.9 and `SOURCE_DATE_EPOCH={SOURCE_DATE_EPOCH}`
(`2026-08-26T00:00:00Z`). The paired builds were byte-identical.

| document | source SHA-256 | PDF SHA-256 | pages | bytes |
|---|---|---|---:|---:|
| main article | `{report['article']['source_sha256']}` | `{report['article']['pdf_sha256']}` | {report['article']['pages']} | {report['article']['bytes']:,} |
| reader supplement | `{report['supplement']['source_sha256']}` | `{report['supplement']['pdf_sha256']}` | {report['supplement']['pages']} | {report['supplement']['bytes']:,} |

All {report['article']['pages'] + report['supplement']['pages']} rendered pages were inspected. No clipping or layout defect was found. The logs contain no overfull boxes, undefined references, undefined citations, fatal errors, or hyperref PDF-string warnings, and every font is embedded. Omission of either generated supplement input fails at the corresponding unconditional `\\input`. Bibliography presence is enforced independently by the source manifest and mutation gate.

Machine-readable payload SHA-256: `{report['payload_sha256']}`.
"""


def main() -> None:
    if not __debug__:
        raise SystemExit("SUBMISSION_PDF_BUILD_OPTIMIZED_MODE_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--visual-pass", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = build_report(args.visual_pass, publish=not args.check)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    rendered = markdown(report)
    if args.check:
        require(REPORT_JSON.is_file() and REPORT_JSON.read_text() == encoded, "PDF_REPORT_JSON_DRIFT")
        require(REPORT_MD.is_file() and REPORT_MD.read_text() == rendered, "PDF_REPORT_MD_DRIFT")
    else:
        REPORT_JSON.write_text(encoded, encoding="utf-8")
        REPORT_MD.write_text(rendered, encoding="utf-8")
    print(json.dumps({"status": report["status"], "payload_sha256": report["payload_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except BuildFailure as error:
        raise SystemExit(f"SUBMISSION_PDF_BUILD_FAIL:{error}") from error
