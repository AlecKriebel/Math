"""Retrieve original-article bytes, preferring the publisher, recording provenance."""
import datetime
import hashlib
import json
from pathlib import Path
import urllib.error
import urllib.request

root = Path(__file__).resolve().parent
evidence = root / "evidence"
evidence.mkdir(exist_ok=True)
urls = [
    "https://www.ams.org/journals/tran/1970-151-00/S0002-9947-1970-0268976-9/S0002-9947-1970-0268976-9.pdf",
    "https://artefacts-discovery.researcher.life/full_text/DA-2/70/701906b973143f3a95ae9d71ba1f1921/full_text/2f02b7d15c78d9518a4b31fc4f6ed046.pdf",
]
attempts = []
for url in urls:
    record = {"url": url, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=40) as response:
            payload = response.read()
            record.update({"status": response.status, "final_url": response.url,
                           "headers": dict(response.headers), "length": len(payload)})
        if not payload.startswith(b"%PDF-"):
            raise ValueError("Response did not begin with PDF magic")
        target = evidence / "erickson1970_original_article.pdf"
        target.write_bytes(payload)
        record.update({"saved_as": str(target.relative_to(root)),
                       "sha256": hashlib.sha256(payload).hexdigest()})
        attempts.append(record)
        print(json.dumps(record, indent=2))
        break
    except Exception as error:
        record.update({"error_type": type(error).__name__, "error": str(error)})
        attempts.append(record)
        print(json.dumps(record, indent=2))
(evidence / "source_retrieval.json").write_text(json.dumps(attempts, indent=2) + "\n")
if not any("saved_as" in entry for entry in attempts):
    raise SystemExit("No original article was retrieved")
