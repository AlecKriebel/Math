"""Reproducible public-source retrieval for the independent exact-target audit."""
import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "documents"
DOCS.mkdir(exist_ok=True)
SOURCES = [
    ("geometry_discotopes_publisher_2022.pdf", "https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734"),
    ("geometry_discotopes_arxiv_v1.pdf", "https://arxiv.org/pdf/2111.01241v1"),
    ("geometry_discotopes_arxiv_v2.pdf", "https://arxiv.org/pdf/2111.01241v2"),
    ("owr_2023_15.pdf", "https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4"),
    ("meroni_thesis_2022.pdf", "https://ul.qucosa.de/api/qucosa%3A81971/attachment/ATT-0/"),
    ("fiber_convex_bodies.pdf", "https://arxiv.org/pdf/2105.12406"),
    ("meroni_semialgebraic_slides_2022.pdf", "https://glivshyts6.math.gatech.edu/Meroni_slides.pdf"),
]

def fetch(item):
    filename, url = item
    record = {"filename":filename, "url":url, "retrieved_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent":"Research literature audit; public document retrieval"})
        with urllib.request.urlopen(request, timeout=50) as response:
            data = response.read()
            record.update(final_url=response.url, content_type=response.headers.get("Content-Type"), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        if not data.startswith(b"%PDF"):
            raise ValueError("Retrieved data is not a PDF")
        (DOCS / filename).write_bytes(data)
        subprocess.run(["pdftotext", "-layout", str(DOCS/filename), str(DOCS/filename).replace(".pdf",".txt")], check=True, capture_output=True)
        record["status"] = "downloaded_and_text_extracted"
    except Exception as error:
        record.update(status="failed", error=str(error))
    return record

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        records = list(pool.map(fetch,SOURCES))
    (ROOT/"download_manifest.json").write_text(json.dumps(records,indent=2)+"\n")
    print(json.dumps(records,indent=2))
