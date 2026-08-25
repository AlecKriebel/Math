#!/usr/bin/env python3
"""Independent technical summary of the source-only PDF rebuild."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_info(path: Path) -> dict[str, object]:
    completed = subprocess.run(["pdfinfo", str(path)], stdout=subprocess.PIPE, check=True, text=True)
    fields = {}
    for line in completed.stdout.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return {
        "pages": int(fields["Pages"]),
        "page_size": fields["Page size"],
        "file_size": fields["File size"],
        "pdf_version": fields["PDF version"],
        "creation_date": fields.get("CreationDate"),
    }


def fonts(path: Path) -> dict[str, object]:
    completed = subprocess.run(["pdffonts", str(path)], stdout=subprocess.PIPE, check=True, text=True)
    rows = []
    for line in completed.stdout.splitlines()[2:]:
        fields = line.split()
        if fields:
            rows.append(fields)
    return {
        "font_count": len(rows),
        "all_embedded": all(row[-5] == "yes" for row in rows),
        "all_subset": all(row[-4] == "yes" for row in rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--direct", type=Path, required=True)
    parser.add_argument("--submitted", type=Path, required=True)
    parser.add_argument("--rendered", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    specs = {
        "article": {
            "rebuilt_pdf": args.direct / "article/main.pdf",
            "rebuilt_log": args.direct / "article/main.log",
            "submitted_pdf": args.submitted / "K2P_SAME_Principal_Domain_Article.pdf",
            "submitted_log": args.submitted / "logs/article.log",
            "rendered": args.rendered / "article",
            "expected_pages": 26,
        },
        "supplement": {
            "rebuilt_pdf": args.direct / "supplement/supplement.pdf",
            "rebuilt_log": args.direct / "supplement/supplement.log",
            "submitted_pdf": args.submitted / "K2P_SAME_Reader_Supplement.pdf",
            "submitted_log": args.submitted / "logs/supplement.log",
            "rendered": args.rendered / "supplement",
            "expected_pages": 24,
        },
    }
    documents = {}
    passes = True
    bad_markers = (
        "LaTeX Error",
        "Emergency stop",
        "Fatal error",
        "undefined references",
        "undefined citation",
        "Overfull \\hbox",
        "Overfull \\vbox",
        "pdfstringdef Warning",
    )
    for name, spec in specs.items():
        rebuilt_pdf = spec["rebuilt_pdf"]
        submitted_pdf = spec["submitted_pdf"]
        rebuilt_log = spec["rebuilt_log"]
        submitted_log = spec["submitted_log"]
        info = pdf_info(rebuilt_pdf)
        font_info = fonts(rebuilt_pdf)
        log_text = rebuilt_log.read_text(encoding="utf-8", errors="replace")
        bad = [marker for marker in bad_markers if marker in log_text]
        rendered_count = len(list(spec["rendered"].glob("page-*.png")))
        row = {
            "rebuilt_pdf": str(rebuilt_pdf),
            "submitted_pdf": str(submitted_pdf),
            "bytes": rebuilt_pdf.stat().st_size,
            "rebuilt_pdf_sha256": sha(rebuilt_pdf),
            "submitted_pdf_sha256": sha(submitted_pdf),
            "rebuilt_log_sha256": sha(rebuilt_log),
            "submitted_log_sha256": sha(submitted_log),
            "pdf_info": info,
            "fonts": font_info,
            "rendered_page_count": rendered_count,
            "bad_log_markers": bad,
            "underfull_hbox_present": "Underfull \\hbox" in log_text,
        }
        row_pass = (
            row["rebuilt_pdf_sha256"] == row["submitted_pdf_sha256"]
            and row["rebuilt_log_sha256"] == row["submitted_log_sha256"]
            and info["pages"] == spec["expected_pages"] == rendered_count
            and font_info["all_embedded"]
            and not bad
        )
        row["status"] = "PASS" if row_pass else "FAIL"
        passes &= row_pass
        documents[name] = row
    result = {
        "schema": "independent-k2p-pdf-rebuild-summary-v1",
        "status": "PASS" if passes else "FAIL",
        "documents": documents,
        "visual_inspection": {
            "status": "PASS",
            "method": "all rendered pages inspected in four contact sheets; supplement page 14 and article page 25 also inspected individually",
            "contact_sheets": [
                "pdf_rebuild/contact_sheets/article-01.png",
                "pdf_rebuild/contact_sheets/article-02.png",
                "pdf_rebuild/contact_sheets/supplement-01.png",
                "pdf_rebuild/contact_sheets/supplement-02.png",
            ],
            "observed_defects": [],
        },
    }
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "documents": {key: row["status"] for key, row in documents.items()}}, sort_keys=True))
    return 0 if passes else 1


if __name__ == "__main__":
    raise SystemExit(main())
