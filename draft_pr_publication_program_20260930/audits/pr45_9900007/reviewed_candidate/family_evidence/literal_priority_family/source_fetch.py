#!/usr/bin/env python3
"""Independent bounded primary-source retrieval. No candidate imports."""
import hashlib
import json
import pathlib
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
SOURCES = (
    ("original_preprint_https", "https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf"),
    ("original_preprint_http", "http://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf"),
    ("publisher_pdf", "https://link.springer.com/content/pdf/10.1007/s11134-011-9241-2.pdf"),
    ("published_metadata", "https://link.springer.com/article/10.1007/s11134-011-9241-2"),
    ("density_preprint", "https://interacting.math.cnrs.fr/HT_Skorohod-Dudley%204.pdf"),
)
records = []
for key, url in SOURCES:
    rec = {"key": key, "url": url, "publication_allowed": False}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Independent mathematical source audit"})
        with urllib.request.urlopen(req, timeout=18) as response:
            body = response.read()
            rec.update(status=response.status, effective_url=response.url,
                       headers=dict(response.headers), success=True)
    except urllib.error.HTTPError as exc:
        body = exc.read()
        rec.update(status=exc.code, effective_url=exc.url, headers=dict(exc.headers),
                   success=False, exception=repr(exc))
    except Exception as exc:
        body = b""
        rec.update(success=False, exception=repr(exc))
    suffix = ".pdf" if body.startswith(b"%PDF-") else ".bin"
    path = ROOT / "foreign_primary" / (key + suffix)
    path.write_bytes(body)
    rec.update(path=str(path), bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
               is_pdf=body.startswith(b"%PDF-"))
    records.append(rec)
    print(json.dumps(rec, sort_keys=True), flush=True)
(ROOT / "foreign_primary" / "FETCH_MANIFEST.json").write_text(
    json.dumps({"records": records, "publication_allowed": False}, indent=2) + "\n")

