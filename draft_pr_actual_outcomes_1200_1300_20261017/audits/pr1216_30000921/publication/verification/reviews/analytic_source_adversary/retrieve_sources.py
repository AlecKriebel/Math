#!/usr/bin/env python3
"""Fresh direct publisher retrieval; source bodies stay in ignored sources/."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import urllib.request

BASE = Path(__file__).resolve().parent
SPECS = [
    ("costakis2008", "https://ems.press/content/serial-article-files/46147", "9bd27d84931841479eaf5e0915e4a99e720c4c135a7d57c97dff43e4687d03a5", [32, 33, 34, 35], [34]),
    ("costakis2010", "https://www.impan.pl/shop/en/publication/transaction/download/product/90964", "ee55f0f14a36216e03533bf568976f9bc83c6d7ef68f3ac8dcecfdc8371d96ae", [5, 21, 22], [5]),
    ("bernal2018", "https://jot.theta.ro/jot/archive/2018-080-001/2018-080-001-011.pdf", "7093a8989e3f5da15db5ff82cb0d158fb67c74c72bbd9cc1b5e8687dc8a01e43", [1, 2, 3], []),
]

def main():
    records = []
    for name, url, historical_hash, pages, renders in SPECS:
        req = urllib.request.Request(url, headers={"User-Agent": "Independent mathematical source verification"})
        with urllib.request.urlopen(req, timeout=40) as response:
            body = response.read()
            final_url = response.url
        if not body.startswith(b"%PDF-"):
            raise RuntimeError(f"Not a PDF: {name}")
        pdf = BASE / "sources" / f"{name}.pdf"
        pdf.write_bytes(body)
        record = {"name": name, "url": url, "final_url": final_url, "bytes": len(body), "sha256": sha256(body).hexdigest(), "matches_submitted_historical_pdf_hash": sha256(body).hexdigest() == historical_hash, "fresh_retrieval_utc": datetime.now(timezone.utc).isoformat(), "text_pages_extracted": pages, "pages_rendered": renders, "full_pdf_read": False, "source_proofs_audited": False}
        record["pdfinfo"] = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
        for page in pages:
            subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), str(BASE / "sources" / f"{name}_p{page}.txt")], check=True)
        for page in renders:
            subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-scale-to", "1600", "-singlefile", "-png", str(pdf), str(BASE / "sources" / f"{name}_p{page}")], check=True)
        records.append(record)
    (BASE / "source_receipt.json").write_text(json.dumps({"schema": "fresh-source-receipt-v1", "sources": records, "source_bodies_location": "ignored sources/", "historical_retrievals_not_reproduced": True}, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "fresh_sources": [{k: r[k] for k in ("name", "bytes", "sha256", "matches_submitted_historical_pdf_hash")} for r in records]}, sort_keys=True))

if __name__ == "__main__":
    main()
