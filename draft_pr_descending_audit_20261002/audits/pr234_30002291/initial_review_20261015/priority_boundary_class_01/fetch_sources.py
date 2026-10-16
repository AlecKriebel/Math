"""Fetch public primary originals into ignored private cache; record hashes only publicly."""
from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
import datetime, hashlib, json, subprocess

ROOT = Path(__file__).resolve().parent
SOURCES = {
    "AOP_preprint": "https://arxiv.org/pdf/1506.06679v1",
    "BEJ_preprint_v2": "https://arxiv.org/pdf/1604.02307v2",
    "EJP_functionals": "https://arxiv.org/pdf/1806.10352v1",
    "EJP_fields_v3": "https://arxiv.org/pdf/2008.01412v3",
    "critical_preprint": "https://repec.econ.au.dk/repec/creates/rp/15/rp15_57.pdf",
    "multiple_singularities": "https://www.vmsta.org/journal/VMSTA/article/122/file/pdf",
    "frontiers_v2": "https://arxiv.org/pdf/2410.00566v2",
    "zero_odd_variation": "https://www.numdam.org/item/10.1051/ps/2014031.pdf",
}

def fetch(item):
    key, url = item
    entry = {"id": key, "requested_url": url, "accessed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={"User-Agent":"Independent mathematical source audit"}), timeout=50) as response:
            data = response.read()
            entry.update(final_url=response.url, content_type=response.headers.get("Content-Type"), status=response.status)
        if not data.startswith(b"%PDF"):
            raise ValueError("Response was not a PDF")
        path = ROOT / "private" / (key + ".pdf")
        path.write_bytes(data)
        entry.update(pdf_sha256=hashlib.sha256(data).hexdigest(), pdf_bytes=len(data), local_pdf=str(path.relative_to(ROOT)))
        textpath = path.with_suffix(".txt")
        subprocess.run(["pdftotext", "-layout", str(path), str(textpath)], check=True)
        textdata = textpath.read_bytes()
        entry.update(text_sha256=hashlib.sha256(textdata).hexdigest(), text_bytes=len(textdata), local_text=str(textpath.relative_to(ROOT)))
    except Exception as error:
        entry["error"] = repr(error)
    return entry

if __name__ == "__main__":
    (ROOT / "private").mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        entries = list(pool.map(fetch, SOURCES.items()))
    (ROOT / "source_provenance.json").write_text(json.dumps(entries, indent=2) + "\n")
    for entry in entries:
        print(entry["id"], entry.get("pdf_bytes"), entry.get("error", "OK"))
