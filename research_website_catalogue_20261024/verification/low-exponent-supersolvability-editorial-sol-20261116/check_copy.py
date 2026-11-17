#!/usr/bin/env python3
"""Read-only finite copy/custody checks. No native imports, network or writes."""
import hashlib
import json
import re
import stat
from html.parser import HTMLParser
from pathlib import Path

R = Path(__file__).resolve().parent
P = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024")
S = P / "papers/23331709/sources"
def digest(b):
    return hashlib.sha256(b).hexdigest()
def pin(path):
    p = Path(path)
    s = p.lstat()
    assert stat.S_ISREG(s.st_mode), str(p)
    b = p.read_bytes()
    return {"path": str(p), "bytes": len(b), "sha256": digest(b),
            "mode": format(stat.S_IMODE(s.st_mode), "04o")}
inputs = json.loads((R / "SOURCES.json").read_text())
for expected in inputs["refs"] + [inputs["stylesheet"]]:
    actual = pin(expected["path"])
    for key in ("bytes", "sha256", "mode"):
        assert actual[key] == expected[key], (expected["path"], key)
manifest = json.loads((S / "SOURCE_MANIFEST.json").read_text())
assert manifest["ordinary_files_including_controls"] == 120
assert manifest["child_directory_count"] == 17
expected_files = {x["path"] for x in manifest["files"]}
expected_files |= {"SOURCE_MANIFEST.json", "SOURCE_FINAL.json"}
expected_dirs = {x["path"] for x in manifest["directories"]}
actual_files, actual_dirs = set(), set()
for path in S.rglob("*"):
    mode = path.lstat().st_mode
    rel = path.relative_to(S).as_posix()
    if stat.S_ISREG(mode):
        actual_files.add(rel)
    elif stat.S_ISDIR(mode):
        actual_dirs.add(rel)
    else:
        raise AssertionError(("special-source-object", rel))
assert actual_files == expected_files and len(actual_files) == 120
assert actual_dirs == expected_dirs and len(actual_dirs) == 17
for row in manifest["files"]:
    actual = pin(S / row["path"])
    assert actual["bytes"] == row["bytes"]
    assert actual["sha256"] == row["SHA256"]
    assert int(actual["mode"], 8) == int(row["mode"], 8)
for row in manifest["directories"]:
    assert stat.S_IMODE((S / row["path"]).lstat().st_mode) == int(row["mode"], 8)
model = json.loads((R / "model.json").read_text())
record = json.loads((S / "record.response.body").read_text())
files_api = json.loads((S / "files-23331709.response.body").read_text())
assert record["metadata"]["description"] == model["native_record_description"]
assert record["metadata"]["title"] == model["title"]
assert record["metadata"]["version"] == model["native_version"] == "1.0"
assert files_api["order"] == []
assert model["native_order"] == [x["key"] for x in record["files"]]
assert model["printed_numeric_version"] is None
assert all(model[k] is None for k in ("canonical", "base_url", "production_url", "AA", "follow_up"))
assert model["publication_authority"] is False and model["private_noindex"] is True
for name in model["native_order"]:
    assert (R / name).read_bytes() == (S / "assets" / name).read_bytes()
tex = (S / "published-source/container-001/tree/low_exponent_supersolvability.tex").read_text()
assert len(tex.splitlines()) == 132
abstract_tex = tex.split("\\begin{abstract}\n", 1)[1].split("\\end{abstract}", 1)[0]
abstract_tex = abstract_tex.replace("Toh\\u{a}neanu", "Tohăneanu").replace("$K_4$", "K4").replace("$", "")
expected_abstract = (R / "EXPECTED_ABSTRACT.txt").read_text().strip()
assert " ".join(abstract_tex.split()) == expected_abstract
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.meta, self.links, self.jsonld = [], {}, [], ""
        self.abstract, self.in_abstract, self.in_jsonld = "", False, False
        self.main_count, self.main_ends, self.iframes = 0, 0, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "main":
            self.main_count += 1
            assert a.get("id") == "main"
        if tag == "meta":
            self.meta[a.get("name", a.get("property"))] = a.get("content")
        if tag == "link":
            self.links.append(a)
        if tag == "iframe":
            self.iframes.append(a)
        if a.get("id") == "original-abstract":
            self.in_abstract = True
        if tag == "script":
            assert a.get("type") == "application/ld+json"
            self.in_jsonld = True
    def handle_endtag(self, tag):
        if tag == "main":
            self.main_ends += 1
        if tag == "p":
            self.in_abstract = False
        if tag == "script":
            self.in_jsonld = False
    def handle_data(self, data):
        if self.in_abstract:
            self.abstract += data
        if self.in_jsonld:
            self.jsonld += data
html = (R / "index.html").read_text()
head = (R / "HEAD.html").read_text().rstrip("\n")
main = (R / "MAIN.html").read_text().rstrip("\n")
assert html.count(head) == 1 and html.count(main) == 1
assert html.split("<main", 1)[1].split("</main>", 1)[0] == main.split("<main", 1)[1].split("</main>", 1)[0]
page = Page()
page.feed(html)
assert page.main_count == page.main_ends == 1
assert len(page.ids) == len(set(page.ids))
assert page.abstract == expected_abstract == model["abstract"]
schema = json.loads(page.jsonld)
assert schema == model["schema"] and schema["abstract"] == expected_abstract
assert page.meta["DC.description"] == expected_abstract
assert page.meta["robots"] == "noindex, nofollow"
assert page.meta["citation_publication_date"] == "2026/10/13"
assert page.meta["citation_pdf_url"] == "low_exponent_supersolvability.pdf"
assert page.meta["citation_title"] == model["title"]
assert not any(x.get("rel") == "canonical" for x in page.links)
assert {"rel": "stylesheet", "href": "../research.css"} in page.links
assert len(page.iframes) == 1
assert page.iframes[0]["src"] == "low_exponent_supersolvability.pdf#view=FitH"
assert page.iframes[0]["title"].startswith("Original five-page manuscript:")
assert "Private preview" not in main and "172" not in main
native_block = main.split('<ol id="native-assets">', 1)[1].split("</ol>", 1)[0]
assert native_block.index('href="low_exponent_supersolvability.pdf"') < native_block.index('href="low_exponent_verification.zip"')
assert "Ferudun’s 12 October 2026 preprint" in main and "same complete theorem" in main
assert "at most one exponent equal to 3" in main and "Rank zero" in main
assert "DiPasquale’s Corollary 4.10 and Proposition 6.1" in main
assert "arXiv:1806.05295v1" in main and "one-dimensional kernel" in main
bib = (R / "citation.bib").read_text()
assert "10.5281/zenodo.23331709" in bib and "version = {1.0}" in bib
assert "year = {2026}" in bib and "day = {13}" in bib
print(json.dumps({"status": "PASS_BOUNDED_DATA_ONLY", "record": 23331709,
    "source_files_whole_bytes_modes": 120, "source_child_directories": 17,
    "external_input_refs_unchanged": len(inputs["refs"]) + 1,
    "two_native_assets_byte_identical_in_original_order": True,
    "abstract_equal_controlling_TeX_visible_DC_schema_model": True,
    "whole_HEAD_and_MAIN_equal_index": True, "unique_semantic_MAIN_and_ids": True,
    "private_noindex_canonical_AA_followup_null": True,
    "deployment_metadata_proposed_only": model["deployment_metadata"],
    "whole_MAIN": {"bytes": len(main.encode()), "sha256": digest(main.encode())},
    "whole_MAIN_file": pin(R / "MAIN.html"), "index": pin(R / "index.html"),
    "HEAD": pin(R / "HEAD.html"), "model": pin(R / "model.json"), "BibTeX": pin(R / "citation.bib"),
    "browser_or_renderer_or_native_or_scientific_code_execution": False,
    "live_native_viewer_download_or_mobile_certification": False}, indent=2))
