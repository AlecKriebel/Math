"""Retrieve public primary-source evidence for the citation audit.

All writes are confined to this script's directory. No credentials or outreach.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidence"
OUT.mkdir(exist_ok=True)
SOURCES = [
    ("gesmundo_meroni_2022", "https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734"),
    ("meroni_owr_2023", "https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4"),
    ("fiber_convex_bodies_published", "https://d-nb.info/1279787392/34"),
    ("line_multiview_2203_01694", "https://arxiv.org/pdf/2203.01694"),
    ("operatopes_2602_08103v1", "https://arxiv.org/pdf/2602.08103v1"),
    ("meroni_thesis_2022", "https://ul.qucosa.de/api/qucosa%3A81971/attachment/ATT-0/"),
    ("mathis_thesis_2022", "https://iris.sissa.it/retrieve/ef5d249b-5948-4b72-b3fa-eef9f375f9ec/The_Handbook_of_zonoid_calculus%20bw.pdf"),
    ("meroni_slides_bielefeld_2022", "https://www.math.uni-bielefeld.de/geocomb/assets/Slides_Meroni.pdf"),
    ("meroni_mtns_2022", "https://epub.uni-bayreuth.de/id/eprint/6809/1/MTNS2022_ExtendedAbstracts_2022-12-22.pdf"),
    ("improofbench_2509_26076v2", "https://arxiv.org/pdf/2509.26076v2"),
    ("chirikjian_shiffman_2012_15163", "https://arxiv.org/pdf/2012.15163"),
    ("ruan_chirikjian_2012_15461", "https://arxiv.org/pdf/2012.15461"),
]

manifest = []
for stem, url in SOURCES:
    record = {"stem": stem, "url": url, "retrieved_utc": datetime.now(timezone.utc).isoformat()}
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0 (research source retrieval)"})
        with urlopen(req, timeout=45) as response:
            data = response.read()
            record["final_url"] = response.url
            record["content_type"] = response.headers.get("Content-Type")
        if not data.startswith(b"%PDF"):
            raise ValueError("Response was not a PDF")
        pdf = OUT / f"{stem}.pdf"
        pdf.write_bytes(data)
        txt = OUT / f"{stem}.txt"
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], check=True)
        record.update(status="retrieved_and_extracted", bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), pdf=pdf.name, text=txt.name)
        if stem == "meroni_mtns_2022":
            # Retain the two-page relevant abstract instead of the 77 MB proceedings.
            parts = [OUT / f"mtns_page_{page}.pdf" for page in (150, 151)]
            subprocess.run(["pdfseparate", "-f", "150", "-l", "151", str(pdf), str(OUT / "mtns_page_%d.pdf")], check=True)
            excerpt = OUT / "meroni_mtns_2022_relevant_pages.pdf"
            subprocess.run(["pdfunite", *map(str, parts), str(excerpt)], check=True)
            for part in parts:
                part.unlink()
            pdf.unlink()
            record.update(pdf=excerpt.name, retained_pdf_pages=[150, 151], full_pdf_retained=False)
        print(stem, "OK", len(data))
    except Exception as exc:
        record.update(status="failed", error=str(exc))
        print(stem, "FAILED", str(exc))
    manifest.append(record)
(OUT / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
