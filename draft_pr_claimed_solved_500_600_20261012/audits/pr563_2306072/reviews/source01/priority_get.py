"""Legitimate direct GETs for source-priority custody; no access bypass."""
from pathlib import Path
import datetime
import hashlib
import json
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
if len(sys.argv) != 3:
    raise SystemExit("usage: priority_get.py NAME URL")
name, url = sys.argv[1:]
record = {"name": name, "requested_url": url,
          "retrieved_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read()
        record.update(status=response.status, resolved_url=response.url,
                      content_type=response.headers.get("Content-Type"), bytes=len(data),
                      sha256=hashlib.sha256(data).hexdigest())
    extension = ".pdf" if data.startswith(b"%PDF") else ".html" if b"<html" in data[:1000].lower() else ".bin"
    path = ROOT / ".cache" / f"{name}{extension}"
    path.write_bytes(data)
    record.update(cache_path=str(path.relative_to(ROOT)), pdf_signature=extension == ".pdf")
except Exception as error:
    record["error"] = repr(error)
with (ROOT / "PRIORITY_RETRIEVALS.jsonl").open("a") as stream:
    stream.write(json.dumps(record) + "\n")
print(json.dumps(record))
