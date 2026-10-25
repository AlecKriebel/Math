#!/usr/bin/env python3
"""Fetch public primary sources solely to record reproducible byte identities.

Source bodies are discarded, never copied into the audit package. Separate
web-tool text/image inspections are described in REPORT.md.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

SOURCES = [
    ("original_owr", "https://ems.press/content/serial-article-files/46798"),
    ("current_arxiv_abs", "https://arxiv.org/abs/1905.09903"),
    ("current_arxiv_pdf", "https://arxiv.org/pdf/1905.09903"),
    ("historical_arxiv_v5_pdf", "https://arxiv.org/pdf/1905.09903v5"),
    ("behrend_primary_archive", "https://pmc.ncbi.nlm.nih.gov/articles/PMC1078964/"),
    ("ruzsa_szemeredi_volume_contents", "https://www.bolyai.hu/files/kotetek_18_1978.pdf"),
]


def fetch(source):
    key, url = source
    result = dict(key=key, requested_url=url,
                  retrieved_utc=datetime.now(timezone.utc).isoformat())
    try:
        with urlopen(Request(url, headers={"User-Agent": "Independent mathematical audit"}),
                     timeout=30) as r:
            data = r.read()
            result.update(status=r.status, final_url=r.url,
                          content_type=r.headers.get("Content-Type"),
                          bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                          pdf=data.startswith(b"%PDF"))
    except Exception as exc:
        result["error"] = repr(exc)
    return result


with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(fetch, SOURCES))
output = Path(__file__).resolve().parent / "SOURCE_LEDGER.json"
output.write_text(json.dumps(dict(sources=results, copied_source_bodies=False), indent=2) + "\n")
print(output.read_text())
