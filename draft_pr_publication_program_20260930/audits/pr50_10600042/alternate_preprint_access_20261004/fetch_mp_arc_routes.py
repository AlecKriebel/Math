"""Follow the public mathematical-physics archive links found on CPT's page."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import html.parser
import json
import os
import urllib.request

F = Path(__file__).resolve().parent
D = F / "private"
class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.forms = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href") and "@" not in attributes["href"]:
            self.links.append(attributes["href"])
        if tag == "form" and "@" not in attributes.get("action", ""):
            self.forms.append(attributes)

def get(item):
    label, url = item
    record = {"label": label, "url": url, "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "pid": os.getpid(), "certificate_verification_disabled": False, "full_text_acquired": False}
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            body = response.read(2_000_001)
            assert len(body) <= 2_000_000
            record.update(http_status=response.status, final_url=response.url,
                          bytes=len(body), sha256=hashlib.sha256(body).hexdigest(),
                          content_type=response.headers.get("Content-Type"))
            dest = D / (label + ".body")
            assert not dest.exists()
            dest.write_bytes(body)
            parser = Links()
            parser.feed(body.decode("utf-8", "replace"))
            record.update(discovered_links=parser.links, public_forms=parser.forms, status="LANDING_PAGE_ACCESSED")
    except Exception as error:
        record.update(status="ACCESS_FAILED", error_type=type(error).__name__, error=str(error))
    record["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return record

urls = [("mp_arc_texas", "https://www.ma.utexas.edu/mp_arc/mp_arc-home.html"),
        ("mp_arc_geneva", "https://mpej.unige.ch/mp_arc/mp_arc-home.html")]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(get, urls))
dest = F / "MP_ARC_ROUTE_ACCESS.json"
assert not dest.exists()
dest.write_text(json.dumps(results, indent=2) + "\n")
raw = F / "CPT_ROUTE_ACCESS.json"
private_raw = D / "CPT_ROUTE_ACCESS_ORIGINAL.json"
assert not private_raw.exists()
private_raw.write_bytes(raw.read_bytes())
records = json.loads(raw.read_text())
for record in records:
    if "form_actions" in record:
        count = len(record["form_actions"])
        record["form_actions"] = [x for x in record["form_actions"] if "@" not in (x.get("action") or "")]
        record["omitted_embedded_guest_credential_form_count"] = count - len(record["form_actions"])
    record["public_record_note"] = "Raw actual receipt retained privately; embedded historical guest-credential form action omitted from this public derived record and never used"
    record["original_raw_receipt_sha256"] = hashlib.sha256(private_raw.read_bytes()).hexdigest()
raw.write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps(results, indent=2))
