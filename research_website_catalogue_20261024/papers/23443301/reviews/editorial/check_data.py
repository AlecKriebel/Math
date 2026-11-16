#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One bounded read-only data check of this private article; no scientific execution."""
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
    raise SystemExit("This checker accepts no arguments and never writes files.")

def digest(data, algorithm="sha256"):
    return hashlib.new(algorithm, data).hexdigest()

def read(name):
    return (R / name).read_text(encoding="utf-8")

def fold(value):
    return re.sub(r"\s+", " ", value).strip()

class Surface(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.metas = {}
        self.urls = []
        self.main_count = 0
        self.base_count = 0
        self.canonical_count = 0
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "meta" and "name" in attrs:
            self.metas.setdefault(attrs["name"], []).append(attrs.get("content"))
        if tag == "main":
            self.main_count += 1
        if tag == "base":
            self.base_count += 1
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical_count += 1
        for key in ("href", "src"):
            if key in attrs:
                self.urls.append({"tag": tag, "attribute": key, "value": attrs[key]})

checks = []
def check(name, result, detail=None):
    checks.append({"name": name, "passed": bool(result), "detail": detail})

initial = json.loads(read("INITIAL_SEAL.json"))
for item in initial["finite_initial_payload"]:
    body = (R / item["path"]).read_bytes()
    if item["path"] == "RESEARCH_LOG.md":
        body = body[:item["bytes"]]
    check("initial-payload:" + item["path"],
          len(body) == item["bytes"] and digest(body) == item["sha256"])
check("initial-seal-identity",
      digest((R / "INITIAL_SEAL.json").read_bytes()) ==
      "02d8afe9f2f51a13c70c0ffa140f3dc0033c9de711063d1b6d4c9442e3753aeb")
expected = json.loads(read("EXPECTATIONS.json"))
model = json.loads(read("PAGE_MODEL.json"))
record = json.loads((S / "record.response.body").read_text())
tex = (S / "published-source/container-001/tree/main.tex").read_text()
raw_abstract = tex.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
check("source-abstract-vs-frozen-expectation",
      fold(raw_abstract) == fold(expected["manuscript_abstract_complete_TeX"]))
plain = re.sub(r"\\\((.*?)\\\)", lambda m: m.group(1).replace("^8", "⁸"),
               raw_abstract, flags=re.S)
plain = fold(plain.replace("--", "–").replace("O'Donnell", "O’Donnell"))
main = read("MAIN.html")
head = read("HEAD.html")
index = read("preview/index.html")
surface = Surface()
surface.feed(index)
visible_match = re.search(r'<p id="original-abstract">(.*?)</p>', main, re.S)
visible = html.unescape(re.sub(r"<[^>]+>", "", visible_match.group(1)))
schema = json.loads(re.search(
    r'<script type="application/ld\+json">\s*(.*?)\s*</script>', head, re.S).group(1))
check("complete-source-abstract-visible-model-schema-DC",
      all(fold(value) == plain for value in (
          visible, model["abstract"], schema["abstract"],
          model["scholarly_article"]["abstract"], surface.metas["DC.description"][0])))
check("whole-MAIN-exactly-once", index.count(main.strip()) == 1)
check("whole-HEAD-exactly-once", index.count(head.strip()) == 1)
check("semantic-single-main-and-unique-ids",
      surface.main_count == 1 and main.lstrip().startswith('<main id="main">') and
      len(surface.ids) == len(set(surface.ids)))
check("private-head-no-canonical-or-base",
      surface.metas.get("robots") == ["noindex,nofollow,noarchive"] and
      surface.canonical_count == 0 and surface.base_count == 0 and
      "private candidate" in surface.metas["editorial-status"][0] and
      "Private preview" not in main and "editorial-status" not in main)
check("private-unset-authorities",
      all(model[key] is None for key in
          ("canonical_url", "base_url", "production_url", "AA", "follow_up")) and
      model["publication_authority"] is False)
native = record["metadata"]
check("native-title-date-version-author",
      native["title"] == model["original_title"] == schema["name"] and
      native["publication_date"] == model["publication_date"] == schema["datePublished"] and
      native["version"] == model["native_version"] == schema["version"] == "1.0.0" and
      surface.metas["citation_publication_date"] == ["2026/10/17"] and
      surface.metas["citation_author_orcid"] == ["0009-0001-9320-500X"])
check("creation-distinct-and-printed-version-absent",
      record["created"] == model["native_created"] == schema["dateCreated"] and
      model["printed_numeric_version"] is None and
      model["printed_numeric_version_present"] is False and
      "prints no numeric version" in main)
check("full-distinct-native-description-retained-privately",
      native["description"] == expected["native_metadata_original"]["description"] and
      native["description"] not in main and
      model["full_native_Description_body_duplication"] is False)
license_text = (S / "published-source/container-001/tree/LICENSE.txt").read_text()
check("targeted-license-and-no-native-MIT-inference",
      license_text == expected["actual_LICENSE_text"] and
      model["rights"]["MIT_inference"] is False and
      model["rights"]["authored_paper_code_analysis"] == "CC BY 4.0" and
      "Third-party works retain their own rights" in main)
asset_list = re.search(r'<ol id="native-assets">(.*?)</ol>', main, re.S).group(1)
asset_surface = Surface()
asset_surface.feed(asset_list)
native_links = [item["value"] for item in asset_surface.urls
                if not urlsplit(item["value"]).scheme]
native_names = [item["key"] for item in record["files"]]
check("ZIP-first-native-order", native_names == native_links ==
      [item["name"] for item in model["native_assets"]])
for native_file, asset in zip(record["files"], model["native_assets"]):
    local_body = (R / "preview" / asset["name"]).read_bytes()
    source_body = (S / "assets" / asset["name"]).read_bytes()
    check("native-byte-identity:" + asset["name"],
          local_body == source_body and len(local_body) == asset["bytes"] == native_file["size"]
          and digest(local_body) == asset["sha256"]
          and digest(local_body, "md5") == native_file["checksum"].split(":", 1)[1])
    check("native-original-URL:" + asset["name"],
          asset["original_url"] == native_file["links"]["self"] and
          asset["original_url"] in asset_list)
check("PDF-FitH-title-open-download",
      'src="polynomial-compatibility.pdf#view=FitH"' in main and
      'title="Original four-page manuscript:' in main and
      '<a href="polynomial-compatibility.pdf">' in main and
      '<a href="polynomial-compatibility.pdf" download>' in main)
check("Bib-identical-native-date-version-DOI",
      (R / "citation.bib").read_bytes() == (R / "preview/citation.bib").read_bytes() and
      all(value in read("citation.bib") for value in
          ("2026-10-17", "1.0.0", native["doi"])))
check("shared-1170-byte-CSS",
      len((R / "preview/research.css").read_bytes()) == 1170 and
      digest((R / "preview/research.css").read_bytes()) ==
      "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a")
tested_local = []
untested = []
for item in surface.urls:
    value = item["value"]
    parts = urlsplit(value)
    if parts.scheme or parts.netloc:
        untested.append(dict(item, reason="External or non-file URL; no GET or navigation"))
    elif parts.path.startswith("/"):
        untested.append(dict(item, reason="Root-relative site navigation; no site staging"))
    elif parts.path:
        resolved = (R / "preview" / unquote(parts.path)).resolve()
        exists = resolved.is_file()
        tested_local.append(dict(item, exists=exists))
        check("local-file:" + value, exists)
    elif parts.fragment:
        check("local-fragment:" + value, parts.fragment in surface.ids)
out = {
    "scope": "One read-only finite data check; no science, render, GET, download or live-page certification",
    "helper_sha256": digest(Path(__file__).read_bytes()),
    "checks": checks,
    "failed_checks": [item for item in checks if not item["passed"]],
    "local_files_checked": tested_local,
    "external_and_root_relative_links_untested": untested,
    "scientific_program_executions": [],
    "GETs": [],
    "all_checks_pass": all(item["passed"] for item in checks)
}
print(json.dumps(out, indent=2, ensure_ascii=False))
raise SystemExit(0 if out["all_checks_pass"] else 1)

