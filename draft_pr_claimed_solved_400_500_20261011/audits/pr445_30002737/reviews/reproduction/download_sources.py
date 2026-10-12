#!/usr/bin/env python3
"""Read-only primary-source retrieval; foreign files stay private."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import urllib.request

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / "private/sources"
PRIVATE.mkdir(parents=True, exist_ok=True)
SOURCES = [
    ("owr", "https://ems.press/content/serial-article-files/46543", [10],
     "23b89a2f8f2ac139fc32feb347ae05724ec3dd22aed540c59c24f8477ed7b3af"),
    ("rs", "https://arxiv.org/pdf/0810.5750v2", [2, 3],
     "637b2eb51d7b75ca0e2f73392bf79b232f445e23cacd88bfb7476a01e64e5734"),
    ("precursor", "https://arxiv.org/pdf/1310.0267v2", [2, 3],
     "d34826964104fd26d1f05ca852f2e40c0b8d99a6a549114977b8263d29011291"),
]
records = []
for name, url, pages, expected in SOURCES:
    record = {"name": name, "requested_url": url, "expected_historical_sha256": expected,
              "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
            record.update({"resolved_url": response.url, "content_type": response.headers.get("Content-Type"),
                           "http_status": response.status})
        if not data.startswith(b"%PDF-"):
            raise ValueError("Retrieved content is not a PDF")
        pdf = PRIVATE / (name + ".pdf")
        pdf.write_bytes(data)
        record.update({"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        record["matches_historical_hash"] = record["sha256"] == expected
        for tool in ["pdftotext", "pdftoppm", "pdfinfo"]:
            if not shutil.which(tool):
                raise RuntimeError(f"Missing required read-only tool: {tool}")
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
        record["pdfinfo_returncode"] = info.returncode
        record["pdfinfo_stdout"] = info.stdout
        subprocess.run(["pdftotext", "-layout", str(pdf), str(PRIVATE / (name + ".txt"))], check=True)
        for page in pages:
            subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-r", "110",
                            "-png", str(pdf), str(PRIVATE / (name + f"_page_{page}"))], check=True)
        record['rendered_pdf_pages'] = pages
        record["status"] = "retrieved_extracted_rendered"
    except Exception as exc:
        record.update({"status": "failed", "error_type": type(exc).__name__, "error": str(exc)})
    records.append(record)
    print(json.dumps(record, indent=2), flush=True)
(HERE / "records/source_provenance.json").write_text(json.dumps({"sources": records}, indent=2) + "\n")
