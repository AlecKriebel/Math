"""Bounded, read-only primary source retrieval with byte receipts. No author code is run."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent

def fetch(item):
    name, url = item
    receipt = {"name": name, "url": url,
               "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Independent bibliographic audit"})
        with urllib.request.urlopen(request, timeout=15) as response:
            body = response.read(6000001)
            if len(body) > 6000000:
                raise ValueError("Source exceeds six MB cap")
            receipt.update(final_url=response.url, status=response.status,
                           content_type=response.headers.get("Content-Type"), bytes=len(body),
                           sha256=hashlib.sha256(body).hexdigest())
        path = ROOT / "sources" / name
        path.write_bytes(body)
        if body.startswith(b"%PDF"):
            subprocess.run(["pdftotext", "-layout", str(path), str(path.with_suffix(".txt"))], check=True)
    except Exception as error:
        receipt["error"] = str(error)
    return receipt

if __name__ == "__main__":
    items = json.loads(sys.argv[1])
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for receipt in executor.map(fetch, items):
            with (ROOT / "FETCH_RECEIPTS.jsonl").open("a") as stream:
                stream.write(json.dumps(receipt, ensure_ascii=False) + "\n")
            print(json.dumps(receipt, ensure_ascii=False), flush=True)
