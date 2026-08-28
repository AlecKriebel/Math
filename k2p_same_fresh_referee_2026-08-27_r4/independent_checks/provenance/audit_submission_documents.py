#!/usr/bin/env python3
"""Independent binding checks for the five sources, two PDFs, and logs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path
from typing import Any


SOURCE_FILES = (
    "article/main.tex",
    "article/references.bib",
    "supplement/supplement.tex",
    "supplement/compression_tables.tex",
    "supplement/certificate_appendix.tex",
)


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key: {key}")
        result[key] = value
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def command(*args: str) -> str:
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise ValueError(f"command failed: {args}: {result.stderr.decode('utf-8', 'replace')}")
    return result.stdout.decode("utf-8", "replace")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-archive", type=Path)
    args = parser.parse_args()
    root = args.project.resolve()
    submission = root / "proof_compression_submission"
    report_path = submission / "PDF_BUILD_REPORT.json"
    report = json.loads(report_path.read_text(), object_pairs_hook=unique_object)
    payload = report["payload_sha256"]
    unsigned = dict(report)
    unsigned.pop("payload_sha256")

    source_rows = {
        relative: {
            "bytes": (submission / relative).stat().st_size,
            "sha256": sha(submission / relative),
        }
        for relative in SOURCE_FILES
    }
    document_rows: dict[str, dict[str, Any]] = {}
    all_fonts_embedded = True
    for kind in ("article", "supplement"):
        row = report[kind]
        pdf = root / row["pdf_path"]
        info = command("pdfinfo", str(pdf))
        page_match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
        fonts = command("pdffonts", str(pdf)).splitlines()[2:]
        font_rows = [line for line in fonts if line.strip()]
        embedded = bool(font_rows) and all(
            re.search(r"\s+yes\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", line.lower())
            is not None
            for line in font_rows
        )
        all_fonts_embedded &= embedded
        document_rows[kind] = {
            "pdf_bytes": pdf.stat().st_size,
            "pdf_sha256": sha(pdf),
            "declared_pdf_bytes": row["bytes"],
            "declared_pdf_sha256": row["pdf_sha256"],
            "pages": int(page_match.group(1)) if page_match else None,
            "declared_pages": row["pages"],
            "fonts_embedded": embedded,
            "font_count": len(font_rows),
            "source_sha256": sha(root / row["source_path"]),
            "declared_source_sha256": row["source_sha256"],
            "log_sha256": sha(submission / "output/logs" / f"{kind}.log"),
            "declared_log_sha256": row["log_sha256"],
        }

    article = (submission / "article/main.tex").read_text()
    supplement = (submission / "supplement/supplement.tex").read_text()
    result = {
        "report": {
            "bytes": report_path.stat().st_size,
            "sha256": sha(report_path),
            "schema": report.get("schema"),
            "status": report.get("status"),
            "payload_sha256": payload,
            "recomputed_payload_sha256": canonical_hash(unsigned),
            "source_set": report.get("source_set"),
            "source_set_exact": report.get("source_set") == list(SOURCE_FILES),
            "engine": report.get("engine"),
            "source_date_epoch": report.get("source_date_epoch"),
            "byte_identical_double_build_claim": report.get("byte_identical_double_build"),
        },
        "source_files": source_rows,
        "documents": document_rows,
        "all_document_bindings_match": all(
            row["pdf_bytes"] == row["declared_pdf_bytes"]
            and row["pdf_sha256"] == row["declared_pdf_sha256"]
            and row["pages"] == row["declared_pages"]
            and row["source_sha256"] == row["declared_source_sha256"]
            and row["log_sha256"] == row["declared_log_sha256"]
            for row in document_rows.values()
        ),
        "all_fonts_embedded": all_fonts_embedded,
        "article_bibliography_unconditional": "\\bibliography{references}" in article,
        "supplement_table_input_unconditional": "\\input{compression_tables.tex}" in supplement,
        "supplement_appendix_input_unconditional": "\\input{certificate_appendix.tex}" in supplement,
        "log_defect_counts": {},
    }
    if args.source_archive is not None:
        archive_path = args.source_archive.resolve()
        with zipfile.ZipFile(archive_path) as archive:
            infos = archive.infolist()
            names = [info.filename for info in infos if not info.is_dir()]
            archive_rows = {
                name: {
                    "bytes": len(archive.read(name)),
                    "sha256": hashlib.sha256(archive.read(name)).hexdigest(),
                    "date_time": list(archive.getinfo(name).date_time),
                    "mode": oct((archive.getinfo(name).external_attr >> 16) & 0o177777),
                }
                for name in names
            }
            bad_member = archive.testzip()
        sidecar = Path(str(archive_path) + ".sha256")
        sidecar_text = sidecar.read_text().strip() if sidecar.is_file() else None
        archive_sha = sha(archive_path)
        result["five_source_archive"] = {
            "path": str(archive_path),
            "bytes": archive_path.stat().st_size,
            "sha256": archive_sha,
            "sidecar_text": sidecar_text,
            "sidecar_matches": bool(sidecar_text) and sidecar_text.split()[0] == archive_sha,
            "file_count": len(archive_rows),
            "member_order": names,
            "exact_five_file_set": names == list(SOURCE_FILES),
            "members_exactly_match_sources": all(
                archive_rows[relative]["bytes"] == source_rows[relative]["bytes"]
                and archive_rows[relative]["sha256"] == source_rows[relative]["sha256"]
                for relative in SOURCE_FILES
            ) if set(archive_rows) == set(SOURCE_FILES) else False,
            "all_fixed_timestamp": all(row["date_time"] == [2026, 8, 27, 0, 0, 0] for row in archive_rows.values()),
            "all_mode_100644": all(row["mode"] == "0o100644" for row in archive_rows.values()),
            "testzip_bad_member": bad_member,
        }
    combined_logs = "\n".join(
        (submission / "output/logs" / f"{kind}.log").read_text(errors="replace")
        for kind in ("article", "supplement")
    )
    result["log_defect_counts"] = {
        "fatal_latex_errors": len(re.findall(r"^! ", combined_logs, re.MULTILINE)),
        "overfull_boxes": combined_logs.count("Overfull \\hbox") + combined_logs.count("Overfull \\vbox"),
        "undefined_citations": len(re.findall(r"Citation .+ undefined", combined_logs)),
        "undefined_references": len(re.findall(r"Reference .+ undefined", combined_logs)),
        "hyperref_pdf_string_warnings": combined_logs.count("Token not allowed in a PDF string"),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
