#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One finite read-only editorial data check; no scientific execution or file writes."""
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

R = Path(__file__).resolve().parent
S = R.parent.parent / "sources"
if len(sys.argv) != 1:
    raise SystemExit("No arguments accepted; this checker only reads and prints JSON.")

def sha(body, kind="sha256"):
    return hashlib.new(kind, body).hexdigest()
def read(name):
    return (R / name).read_text(encoding="utf-8")
def fold(value):
    return re.sub(r"\s+", " ", value).strip()

class Surface(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.urls, self.metas = [], [], {}
        self.main_count = self.h1_count = self.base_count = self.canonical_count = 0
    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "meta" and "name" in a:
            self.metas.setdefault(a["name"], []).append(a.get("content"))
        if tag == "main":
            self.main_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "base":
            self.base_count += 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical_count += 1
        for key in ("href", "src"):
            if key in a:
                self.urls.append({"tag": tag, "attribute": key, "value": a[key]})

checks = []
def check(name, result, detail=None):
    checks.append({"name": name, "passed": bool(result), "detail": detail})

seal = json.loads(read("INITIAL_SEAL.json"))
for item in seal["payload"]:
    b = (R / item["path"]).read_bytes()
    check("immutable-initial:" + item["path"],
          len(b) == item["bytes"] and sha(b) == item["sha256"])
check("immutable-initial-seal", sha((R / "INITIAL_SEAL.json").read_bytes()) ==
      "b7eaf8fe6d69b9dc103c20d373ec8f2837e751048a6d5a8ff17505664c05699d")
pins = json.loads(read("SOURCE_PINS.json"))
for field in ("native_record", "native_files_endpoint"):
    item = pins[field]
    b = (S / item["path"]).read_bytes()
    check("source-identity:" + field,
          len(b) == item["bytes"] and sha(b) == item["sha256"])
for item in pins["reused_actual_root_rasters_by_reference"]:
    b = (R / item["path"]).read_bytes()
    check("reused-source-pixel:" + item["path"],
          len(b) == item["bytes"] and sha(b) == item["sha256"])
expected = json.loads(read("EXPECTATIONS.json"))
model = json.loads(read("PAGE_MODEL.json"))
record = json.loads((S / "record.response.body").read_text())
tex = (S / "assets/taut_godbillon_vey.tex").read_text()
raw = tex.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
check("source-abstract-vs-frozen-TeX", fold(raw) ==
      fold(expected["manuscript_abstract_complete_TeX"]))
plain = fold(raw.replace("--", "–").replace("~", " ").replace("Calegari's", "Calegari’s"))
main, head, index = read("MAIN.html"), read("HEAD.html"), read("preview/index.html")
surface = Surface()
surface.feed(index)
schema = json.loads(re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
                              head, re.S).group(1))
visible = html.unescape(re.search(r'<p id="original-abstract">(.*?)</p>', main, re.S).group(1))
check("complete-abstract-visible-model-schema-DC",
      all(fold(value) == plain for value in
          (visible, model["abstract"], schema["abstract"],
           model["scholarly_article"]["abstract"], surface.metas["DC.description"][0])))
check("whole-MAIN-and-HEAD-once",
      index.count(main) == 1 and index.count(head) == 1)
check("semantic-MAIN-h1-unique-ids",
      surface.main_count == surface.h1_count == 1 and '<main id="main">' in main and
      len(surface.ids) == len(set(surface.ids)))
check("private-head-and-unset-authority",
      surface.metas["robots"] == ["noindex,nofollow,noarchive"] and
      surface.base_count == surface.canonical_count == 0 and
      all(model[k] is None for k in
          ("canonical_url", "base_url", "production_url", "AA", "follow_up")) and
      model["publication_authority"] is False and
      "Private preview" not in main and "editorial-status" not in main)
metadata = record["metadata"]
h1 = html.unescape(re.search(r"<h1[^>]*>(.*?)</h1>", main, re.S).group(1))
check("original-title-author-date-version",
      h1.replace("–", "-") == metadata["title"] == model["original_title"] == schema["name"]
      and metadata["publication_date"] == model["publication_date"] == schema["datePublished"] == "2026-10-13"
      and metadata["version"] == model["native_version"] == schema["version"] == "1.0"
      and surface.metas["citation_publication_date"] == ["2026/10/13"]
      and surface.metas["citation_author_orcid"] == [metadata["creators"][0]["orcid"]])
check("creation-and-printed-version-distinct",
      schema["dateCreated"] == model["native_created"] == record["created"]
      and model["printed_numeric_version"] is None
      and model["printed_numeric_version_present"] is False
      and "no numeric version printed" in main and "14 October 2026 (UTC)" in main)
check("distinct-Description-retained-privately",
      expected["native_metadata_original"]["description"] == metadata["description"]
      and metadata["description"] not in main
      and model["full_native_Description_body_duplication"] is False)
check("native-rights-no-MIT-inference",
      metadata["license"] == {"id": "cc-by-4.0"}
      and model["rights"]["native_MIT_inference"] is False
      and model["rights"]["separate_LICENSE_filename_found"] is False
      and "third-party works retain their own rights" in main)
native_block = re.search(r'<ol id="native-assets">(.*?)</ol>', main, re.S).group(1)
native_surface = Surface()
native_surface.feed(native_block)
locals_in_order = [x["value"] for x in native_surface.urls if not urlsplit(x["value"]).scheme]
check("all-three-native-assets-ZIP-PDF-TeX-order",
      locals_in_order == [x["key"] for x in record["files"]] ==
      [x["name"] for x in model["native_assets"]])
for original, item in zip(record["files"], model["native_assets"]):
    local = (R / "preview" / item["name"]).read_bytes()
    source = (S / "assets" / item["name"]).read_bytes()
    check("native-byte-identity:" + item["name"],
          local == source and len(local) == item["bytes"] == original["size"]
          and sha(local) == item["sha256"]
          and sha(local, "md5") == item["md5"] == original["checksum"].split(":", 1)[1])
    check("native-original-link:" + item["name"],
          item["original_url"] == original["links"]["self"] and item["original_url"] in native_block)
check("PDF-FitH-title-open-download",
      'src="taut_godbillon_vey.pdf#view=FitH"' in main
      and 'title="Original four-page manuscript:' in main
      and '<a href="taut_godbillon_vey.pdf">' in main
      and '<a href="taut_godbillon_vey.pdf" download>' in main)
check("Bib-native-date-version-DOI",
      (R / "citation.bib").read_bytes() == (R / "preview/citation.bib").read_bytes()
      and all(x in read("citation.bib") for x in ("2026-10-13", "1.0", metadata["doi"])))
css = (R / "preview/research.css").read_bytes()
check("shared-white-Arial-1170B-style", len(css) == 1170 and sha(css) ==
      "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a")
outside = re.sub(r'<section id="(?:abstract|references)"[\s\S]*?</section>', "", main)
word_count = len(html.unescape(re.sub(r"<[^>]+>", " ", outside)).split())
check("requested-prose-length", 600 <= word_count <= 900,
      {"word_count_outside_abstract_references": word_count, "requested_range": [600, 900]})
untested = []
for item in surface.urls:
    value = item["value"]
    u = urlsplit(value)
    if u.scheme or u.netloc:
        untested.append(dict(item, reason="External URL; no GET/navigation"))
    elif u.path.startswith("/"):
        untested.append(dict(item, reason="Root-relative site navigation; no staging"))
    elif u.path:
        check("local-linked-file:" + value, (R / "preview" / unquote(u.path)).resolve().is_file())
    elif u.fragment:
        check("local-fragment:" + value, u.fragment in surface.ids)
out = {"scope": "One read-only finite copy/data check; no science, render, GET, download or live certification",
       "helper_sha256": sha(Path(__file__).read_bytes()), "checks": checks,
       "failed_checks": [x for x in checks if not x["passed"]],
       "links_untested": untested, "scientific_program_executions": [], "GETs": [],
       "all_checks_pass": all(x["passed"] for x in checks)}
print(json.dumps(out, indent=2, ensure_ascii=False))
raise SystemExit(0 if out["all_checks_pass"] else 1)
