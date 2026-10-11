"""Read observed public year indexes after mp_arc's search endpoint returned500."""
from pathlib import Path
import concurrent.futures
import datetime as dt
import hashlib
import html.parser
import json
import os
import re
import urllib.parse
import urllib.request

F = Path(__file__).resolve().parent
D = F / "private"
class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.text = [], []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"])
    def handle_data(self, data):
        self.text.append(data)

def get(label, url):
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    record = {"label": label, "url": url, "started_utc": start, "pid": os.getpid(),
              "full_mathematical_body_acquired": False, "certificate_verification_disabled": False}
    parser = None
    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            body = response.read(1_000_001)
            assert len(body) <= 1_000_000, "Full index exceeds chosen byte limit; do not infer absence"
            path = D / (label + ".body")
            assert not path.exists()
            path.write_bytes(body)
            record.update(http_status=response.status, final_url=response.url, bytes=len(body),
                          sha256=hashlib.sha256(body).hexdigest(), status="FULL_STATIC_INDEX_ACCESSED")
            parser = Page()
            parser.feed(body.decode("utf-8", "replace"))
            text = " ".join(parser.text)
            matches = []
            for term in ["Nencka", "Cantorian", "braid"]:
                hits = list(re.finditer(re.escape(term), text, flags=re.IGNORECASE))
                matches.append({"term": term, "count": len(hits),
                    "bounded_contexts": [text[max(0, m.start()-160):m.end()+240] for m in hits[:8]]})
            record["literal_index_matches"] = matches
    except Exception as error:
        record.update(status="ACCESS_FAILED", error_type=type(error).__name__, error=str(error))
    record["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return record, parser

source = Path(__file__).read_bytes()
(D / "static_archive_prelaunch.py").write_bytes(source)
base = "https://web.ma.utexas.edu/mp_arc/mp_arc-home.html"
home, parser = get("current_mp_arc_home", base)
assert parser is not None
desired = {"index-95.html", "index-96.html", "index-97.html", "index-98.html", "index-99.html"}
selected = {}
for href in parser.links:
    path = urllib.parse.urlsplit(href).path
    if Path(path).name in desired:
        selected[Path(path).name] = urllib.parse.urljoin(base, href.split("#")[0])
assert set(selected) == desired, "Only fetch links actually present in the primary homepage"
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(lambda item: get(item[0].replace(".html", ""), item[1])[0], sorted(selected.items())))
record = {"UTC": dt.datetime.now(dt.timezone.utc).isoformat(), "homepage": home,
          "observed_links_only": True, "indexes": results,
          "browser_search_endpoint": "https://web.ma.utexas.edu/cgi-bin/mps?src=abstracts&yra=1991&yrz=2023&key=Nencka&max=64&len=32",
          "browser_search_observation": "Actual visible500 Internal Server Error; not interpreted as zero results",
          "source_sha256": hashlib.sha256(source).hexdigest(), "source_unchanged": source == Path(__file__).read_bytes(),
          "limitations": "Bounded exact title/author index lookup for1995-1999 only. No literature absence, novelty, theorem invalidity or full-source scope inference.",
          "publication_approval": False}
dest = F / "STATIC_ARCHIVE_READBACK.json"
assert not dest.exists()
dest.write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record, indent=2))
