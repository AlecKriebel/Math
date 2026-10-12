"""Preserve independently fetched primary-source bytes and retrieval receipts."""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import urllib.request

BASE = pathlib.Path(__file__).resolve().parent
SOURCES = {
    "bln2021-published.pdf": "https://proceedings.mlr.press/v134/bubeck21a/bubeck21a.pdf",
    "bln2020.pdf": "https://arxiv.org/pdf/2009.14444v2",
    "owr2021-15.pdf": "https://ems.press/content/serial-article-files/46893",
    "shmalo2026.pdf": "https://arxiv.org/pdf/2607.07778v1",
    "wu2023.pdf": "https://proceedings.mlr.press/v202/wu23g/wu23g.pdf",
    "wu2202.pdf": "https://arxiv.org/pdf/2202.11592v2",
    "bubeck_sellke2022.pdf": "https://arxiv.org/pdf/2105.12806v4",
    "shmalo_repository_README.md": "https://raw.githubusercontent.com/yspennstate/law-of-robustness-two-layer/6b1f35f7f70a9d98f1c0251cfb5a5dd8f0115b1f/README.md",
}

def fetch(item):
    name, url = item
    req = urllib.request.Request(url, headers={"User-Agent": "Independent mathematical source audit"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        final_url = response.url
    if name.endswith(".pdf"):
        assert data.startswith(b"%PDF"), name
    (BASE / "raw_sources" / name).write_bytes(data)
    return {
        "path": "raw_sources/" + name,
        "url": url,
        "final_url": final_url,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

if __name__ == "__main__":
    (BASE / "raw_sources").mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        receipts = list(executor.map(fetch, SOURCES.items()))
    (BASE / "SOURCE_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps(receipts, indent=2))
