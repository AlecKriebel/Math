import datetime
import hashlib
import json
from pathlib import Path
import urllib.request

root = Path(__file__).resolve().parent
url = "https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf"
record = {"url": url, "utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
    with urllib.request.urlopen(url, timeout=25) as response:
        payload = response.read()
        record.update({"status": response.status, "final_url": response.url,
                       "headers": dict(response.headers), "length": len(payload)})
    if not payload.startswith(b"%PDF-"):
        raise ValueError("Response did not begin with PDF magic")
    target = root / "evidence/thorisson_original_preprint.pdf"
    target.write_bytes(payload)
    record.update({"saved_as": str(target.relative_to(root)),
                   "sha256": hashlib.sha256(payload).hexdigest()})
except Exception as error:
    record.update({"error_type": type(error).__name__, "error": str(error)})
(root / "evidence/thorisson_retrieval.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
if "saved_as" not in record:
    raise SystemExit(1)
