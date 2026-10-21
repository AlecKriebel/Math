"""Read-only public-primary retrieval; no authentication or access controls bypassed."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import urllib.request

HERE = Path(__file__).resolve().parent
REQUESTS = [
    ("ajls_chapter", "https://link.springer.com/chapter/10.1007/978-3-319-56478-4_4"),
    ("ajls_chapter_pdf", "https://link.springer.com/content/pdf/10.1007/978-3-319-56478-4_4.pdf"),
    ("ajls_book_pdf", "https://link.springer.com/content/pdf/10.1007/978-3-319-56478-4.pdf"),
    ("le2006_pdf", "https://link.springer.com/content/pdf/10.1007/s00022-005-0030-0.pdf"),
    ("le2007_pdf", "https://www.worldscientific.com/doi/pdf/10.1142/9789812770493_0012"),
    ("amari2021_full", "https://onlinelibrary.wiley.com/doi/full/10.1111/insr.12464"),
    ("amari2021_pdf", "https://onlinelibrary.wiley.com/doi/pdf/10.1111/insr.12464"),
    ("google_books_preview", "https://books.google.com/books?id=pLsyDwAAQBAJ&pg=PA222"),
    ("le_home", "https://users.math.cas.cz/~hvle/"),
    ("lauritzen_publications", "https://web.math.ku.dk/~lauritzen/publications.html"),
]


def retrieve(item):
    key, url = item
    rec = {"key": key, "request_url": url, "utc": datetime.now(timezone.utc).isoformat(),
           "method": "GET", "mode": "fresh_network", "contact": "none"}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=40) as response:
            body = response.read()
            rec.update(final_url=response.url, status=response.status,
                       content_type=response.headers.get("Content-Type"),
                       bytes=len(body), sha256=sha256(body).hexdigest(),
                       actual_pdf=body.startswith(b"%PDF"))
            name = key + (".pdf" if rec["actual_pdf"] else ".html")
            (HERE / "private" / name).write_bytes(body)
            rec["private_body"] = "private/" + name
    except Exception as exc:
        rec["error"] = str(exc)
    return rec


if __name__ == "__main__":
    (HERE / "private").mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=5) as pool:
        records = list(pool.map(retrieve, REQUESTS))
    (HERE / "PUBLIC_RETRIEVAL.json").write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(records, indent=2))
