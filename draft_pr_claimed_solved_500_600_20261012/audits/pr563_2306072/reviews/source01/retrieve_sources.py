"""Fresh primary-source download and immutable byte receipt; caches are ignored."""
from pathlib import Path
import datetime
import hashlib
import json
import urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("hayman_lingham_v2", "https://arxiv.org/pdf/1809.07200v2"),
    ("duren_1981_eth", "https://www.e-periodica.ch/cntmng?pid=com-001%3A1981%3A56%3A%3A30&bot=1"),
]

receipt = []
for name, url in SOURCES:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        item = {"source_id": name, "requested_url": url, "resolved_url": response.url,
                "status": response.status, "content_type": response.headers.get("Content-Type"),
                "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
                "pdf_signature": data.startswith(b"%PDF"), "cache_path": f".cache/{name}.pdf"}
    if not item["pdf_signature"]:
        raise RuntimeError(f"Not a PDF: {item}")
    (ROOT / item["cache_path"]).write_bytes(data)
    receipt.append(item)
    print(json.dumps(item))
(ROOT / "SOURCE_RETRIEVAL.json").write_text(json.dumps(receipt, indent=2) + "\n")
