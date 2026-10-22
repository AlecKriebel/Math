"""Read-only primary-source retrieval. Raw bodies stay in ignored private/."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "winter_current.pdf": "https://martinwintermath.github.io/pdf/publications/Stokers_conjecture.pdf",
    "winter_pinned.pdf": "https://raw.githubusercontent.com/martinwintermath/martinwintermath.github.io/766c313bc2187a5eafd5757dca43ffefc6a9ced6/pdf/publications/Stokers_conjecture.pdf",
    "winter_commit.json": "https://api.github.com/repos/martinwintermath/martinwintermath.github.io/commits/766c313bc2187a5eafd5757dca43ffefc6a9ced6",
    "winter_git_commit.json": "https://api.github.com/repos/martinwintermath/martinwintermath.github.io/git/commits/766c313bc2187a5eafd5757dca43ffefc6a9ced6",
    "winter_old_v2.pdf": "https://arxiv.org/pdf/2302.14194v2",
    "winter_old_abs.html": "https://arxiv.org/abs/2302.14194v2",
    "winter_old_doi.json": "https://api.crossref.org/works/10.1093/imrn/rnad298",
    "winter_wrap.html": "https://wrap.warwick.ac.uk/id/eprint/182244/",
    "owr2017.pdf": "https://publications.mfo.de/bitstream/handle/mfo/3583/OWR_2017_19.pdf?isAllowed=y&sequence=1",
    "akopyan_karasev_v2.pdf": "https://arxiv.org/pdf/1505.05263v2",
}

def fetch(item):
    name, url = item
    row = {"name": name, "requested_url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={"User-Agent": "Independent-source-audit/1.0"}), timeout=40) as r:
            data = r.read()
            (ROOT / "private" / name).write_bytes(data)
            row.update(status=r.status, final_url=r.url, response_headers=dict(r.headers), bytes=len(data), sha256=sha256(data).hexdigest())
    except Exception as exc:
        row["error"] = repr(exc)
    return row

if __name__ == "__main__":
    rows = list(ThreadPoolExecutor(max_workers=8).map(fetch, SOURCES.items()))
    (ROOT / "private" / "FETCH_RECEIPTS.json").write_text(json.dumps(rows, indent=2) + "\n")
    for row in rows:
        print(json.dumps({key: row.get(key) for key in ["name", "status", "bytes", "sha256", "error"]}))
