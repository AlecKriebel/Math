#!/usr/bin/env python3
"""Independent structural/text audit of the two sealed submission PDFs."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path
from typing import Any


SOURCE_RELATIVES = (
    "article/main.tex",
    "article/references.bib",
    "supplement/supplement.tex",
    "supplement/compression_tables.tex",
    "supplement/certificate_appendix.tex",
)


class PDFAuditFailure(RuntimeError):
    pass


def require(condition: bool, code: str, detail: object | None = None) -> None:
    if not condition:
        raise PDFAuditFailure(code if detail is None else f"{code}:{detail}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            allow_nan=False,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def strict_json(path: Path) -> dict[str, Any]:
    def pairs_hook(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            require(key not in value, "DUPLICATE_JSON_NAME", f"{path}:{key}")
            value[key] = item
        return value

    def reject_constant(token: str) -> None:
        raise PDFAuditFailure(f"NONFINITE_JSON_NUMBER:{path}:{token}")

    def finite_float(token: str) -> float:
        value = float(token)
        require(math.isfinite(value), "NONFINITE_JSON_FLOAT", token)
        return value

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=pairs_hook,
            parse_constant=reject_constant,
            parse_float=finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError) as error:
        raise PDFAuditFailure(f"JSON_DECODE_FAIL:{path}:{error}") from error
    require(isinstance(value, dict), "JSON_NOT_OBJECT", path)
    return value


def command_text(arguments: list[str]) -> str:
    result = subprocess.run(
        arguments,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    require(result.returncode == 0, "COMMAND_FAIL", f"{arguments}:{result.stderr}")
    return result.stdout


def pdfinfo(path: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in command_text(["pdfinfo", str(path)]).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            rows[key.strip()] = value.strip()
    return rows


def font_audit(path: Path) -> dict[str, int | bool]:
    lines = command_text(["pdffonts", str(path)]).splitlines()[2:]
    rows = [line for line in lines if line.strip()]
    embedded = []
    for line in rows:
        match = re.search(
            r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$",
            line.lower(),
        )
        require(match is not None, "PDFFONTS_ROW_PARSE", line)
        embedded.append(match.group(1) == "yes")
    require(bool(embedded) and all(embedded), "UNEMBEDDED_FONT", path)
    return {"all_embedded": True, "font_rows": len(rows)}


def extracted_text(path: Path) -> str:
    return command_text(["pdftotext", "-layout", str(path), "-"])


def log_audit(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "fatal_latex_errors": len(re.findall(r"^! ", text, re.MULTILINE)),
        "hyperref_pdf_string_warnings": text.count("Token not allowed in a PDF string"),
        "overfull_boxes": text.count("Overfull \\hbox") + text.count("Overfull \\vbox"),
        "underfull_boxes": text.count("Underfull \\hbox") + text.count("Underfull \\vbox"),
        "undefined_citations": len(re.findall(r"Citation .+ undefined", text)),
        "undefined_references": len(re.findall(r"Reference .+ undefined", text)),
    }


def main() -> int:
    require(__debug__, "OPTIMIZED_PYTHON_FORBIDDEN")
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = args.project.resolve()
    submission = project / "proof_compression_submission"
    report_path = submission / "PDF_BUILD_REPORT.json"
    report = strict_json(report_path)
    claimed_payload = report.get("payload_sha256")
    unsigned = dict(report)
    unsigned.pop("payload_sha256", None)
    require(claimed_payload == canonical_hash(unsigned), "PDF_REPORT_PAYLOAD")
    require(report.get("source_set") == list(SOURCE_RELATIVES), "PDF_SOURCE_SET")
    source_rows = {
        relative: {
            "bytes": (submission / relative).stat().st_size,
            "sha256": sha256(submission / relative),
        }
        for relative in SOURCE_RELATIVES
    }

    documents = {
        "article": {
            "pdf": submission / "output/K2P_SAME_Principal_Domain_Article.pdf",
            "log": submission / "output/logs/article.log",
            "expected_pages": 26,
            "required_text": [
                "Generic Identiﬁability and Directed Containment",
                "405,216",
                "2,946,240",
                "36,824",
                "544,571",
                "PC-PARTIAL",
                "4n − 3",
            ],
        },
        "supplement": {
            "pdf": submission / "output/K2P_SAME_Reader_Supplement.pdf",
            "log": submission / "output/logs/supplement.log",
            "expected_pages": 24,
            "required_text": [
                "Reader Supplement",
                "405,216",
                "2,946,240",
                "36,824",
                "544,571",
                "PC-PARTIAL",
                "Frozen hash anchors",
            ],
        },
    }
    document_results: dict[str, Any] = {}
    for kind, specification in documents.items():
        pdf_path = specification["pdf"]
        log_path = specification["log"]
        require(isinstance(pdf_path, Path) and isinstance(log_path, Path), "INTERNAL_PATH_TYPE")
        info = pdfinfo(pdf_path)
        fonts = font_audit(pdf_path)
        text = extracted_text(pdf_path)
        missing = [marker for marker in specification["required_text"] if marker not in text]
        require(not missing, "PDF_TEXT_MARKER_MISSING", f"{kind}:{missing}")
        require(int(info.get("Pages", "0")) == specification["expected_pages"], "PDF_PAGE_COUNT", kind)
        require(info.get("Encrypted") == "no" and info.get("Form") == "none", "PDF_ACTIVE_OR_ENCRYPTED", kind)
        require(info.get("JavaScript") == "no", "PDF_JAVASCRIPT", kind)
        logs = log_audit(log_path)
        for field in (
            "fatal_latex_errors",
            "hyperref_pdf_string_warnings",
            "overfull_boxes",
            "undefined_citations",
            "undefined_references",
        ):
            require(logs[field] == 0, "PDF_LOG_DEFECT", f"{kind}:{field}:{logs[field]}")
        report_row = report.get(kind)
        require(isinstance(report_row, dict), "PDF_REPORT_ROW", kind)
        require(
            report_row.get("pdf_sha256") == sha256(pdf_path)
            and report_row.get("bytes") == pdf_path.stat().st_size
            and report_row.get("pages") == specification["expected_pages"]
            and report_row.get("log_sha256") == sha256(log_path),
            "PDF_REPORT_OUTPUT_DRIFT",
            kind,
        )
        source_relative = report_row.get("source_path")
        require(
            isinstance(source_relative, str)
            and report_row.get("source_sha256") == sha256(project / source_relative),
            "PDF_REPORT_SOURCE_DRIFT",
            kind,
        )
        document_results[kind] = {
            "bytes": pdf_path.stat().st_size,
            "fonts": fonts,
            "log_counts": logs,
            "log_sha256": sha256(log_path),
            "page_size": info.get("Page size"),
            "pages": specification["expected_pages"],
            "pdf_sha256": sha256(pdf_path),
            "pdf_version": info.get("PDF version"),
            "required_text_markers_found": specification["required_text"],
        }

    result: dict[str, Any] = {
        "schema": "k2p-r5-independent-pdf-source-consistency-v1",
        "status": "PASS",
        "source_files": source_rows,
        "pdf_build_report": {
            "bytes": report_path.stat().st_size,
            "payload_sha256": claimed_payload,
            "sha256": sha256(report_path),
            "status": report.get("status"),
            "engine": report.get("engine"),
            "source_date_epoch": report.get("source_date_epoch"),
        },
        "documents": document_results,
    }
    result["payload_sha256"] = canonical_hash(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "payload_sha256": result["payload_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PDFAuditFailure as error:
        raise SystemExit(f"INDEPENDENT_PDF_AUDIT_FAIL:{error}") from error
