"""Bounded legitimate reads of two discovered CPT preprint/library routes."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import html.parser
import json
import os
import urllib.error
import urllib.request

F = Path(__file__).resolve().parent
D = F / "private"
D.mkdir(exist_ok=True)
class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.forms = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
        if tag == "form":
            self.forms.append(attributes)

def get(item):
    label, url = item
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    record = {"label": label, "url": url, "started_utc": start, "pid": os.getpid(),
              "full_text_acquired": False, "certificate_verification_disabled": False}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Math-Research-Source-Audit/1.0"})
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(2_000_001)
            assert len(body) <= 2_000_000, "Bounded landing-page response limit exceeded"
            record.update(http_status=response.status, final_url=response.url,
                          content_type=response.headers.get("Content-Type"),
                          bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
            dest = D / (label + ".body")
            assert not dest.exists()
            dest.write_bytes(body)
            parser = Links()
            parser.feed(body.decode("utf-8", "replace"))
            record["discovered_links"] = [x for x in parser.links if not ("@" in x or x.startswith("mailto:"))]
            record["form_actions"] = [{"action": x.get("action"), "method": x.get("method")} for x in parser.forms]
            record["status"] = "LANDING_PAGE_ACCESSED"
    except Exception as error:
        record["status"] = "ACCESS_FAILED"
        record["error_type"] = type(error).__name__
        record["error"] = str(error)
    record["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return record

items = [
    ("cpt_historical_preprint_search", "https://www.cpt.univ-mrs.fr/~vittot/FindPreprint.htm"),
    ("cpt_official_laboratory", "https://www.cpt.univ-mrs.fr/fr/laboratory/")]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(get, items))
dest = F / "CPT_ROUTE_ACCESS.json"
assert not dest.exists()
dest.write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, indent=2))
