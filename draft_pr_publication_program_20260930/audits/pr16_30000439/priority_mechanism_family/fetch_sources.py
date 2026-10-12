"""Download primary public sources into an ignored, audit-local cache.

This is read-only research: no individual communications or external writes.
"""
from pathlib import Path
from urllib.request import Request, urlopen
import concurrent.futures, datetime, hashlib, json, subprocess

HERE = Path(__file__).resolve().parent
CACHE = HERE / "tmp"
SOURCES = {
    "newman_v1": "https://arxiv.org/pdf/2212.09576v1.pdf",
    "newman_v2": "https://arxiv.org/pdf/2212.09576v2",
    "newman_v3": "https://arxiv.org/pdf/2212.09576v3",
    "lee_nevo_v1": "https://arxiv.org/pdf/2307.14195v1",
    "lee_nevo_v2": "https://arxiv.org/pdf/2307.14195v2.pdf",
    "lee_nevo_v3": "https://arxiv.org/pdf/2307.14195v3",
    "heise_et_al_2014": "https://opikhurko.warwick.ac.uk/E/HeisePanagiotouPikhurkoTaraz14dcg.pdf",
    "gundert_2009_arxiv2018": "https://arxiv.org/pdf/1812.08447v1",
    "skopenkov_v7": "https://arxiv.org/pdf/1402.0658v7",
    "horsley_pike_v2": "https://arxiv.org/pdf/1209.6111v2",
    "abrahamsen_et_al_2023": "https://drops.dagstuhl.de/opus/volltexte/2023/17851/pdf/LIPIcs-SoCG-2023-1.pdf",
    "sparse_codes_v1": "https://arxiv.org/pdf/2309.14862v1",
}

def get(item):
    key, url = item
    record = {"key": key, "requested_url": url, "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urlopen(Request(url, headers={"User-Agent": "Independent scholarly source audit"}), timeout=45) as response:
            data = response.read()
            record.update(final_url=response.url, content_type=response.headers.get("Content-Type"))
        if not data.startswith(b"%PDF"):
            raise ValueError("Expected PDF")
        path = CACHE / (key + ".pdf")
        path.write_bytes(data)
        record.update(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), local_file=str(path.relative_to(HERE)))
        txt = CACHE / (key + ".txt")
        subprocess.run(["pdftotext", "-layout", str(path), str(txt)], check=True)
        record.update(text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest(), text_file=str(txt.relative_to(HERE)), status="success")
    except Exception as exc:
        record.update(status="failed", error=repr(exc))
    return record

if __name__ == "__main__":
    CACHE.mkdir(exist_ok=True)
    ledger = HERE / "SOURCE_HASH_LEDGER.json"
    old = json.loads(ledger.read_text()) if ledger.exists() else []
    good_keys = {record["key"] for record in old if record["status"] == "success"}
    pending = {key: url for key, url in SOURCES.items() if key not in good_keys}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(get, pending.items()))
    new_keys = {record["key"] for record in results}
    all_results = [r for r in old if r["key"] not in new_keys] + results
    ledger.write_text(json.dumps(all_results, indent=2) + "\n")
    for record in results:
        print(record["key"], record["status"], record.get("sha256", record.get("error")))
