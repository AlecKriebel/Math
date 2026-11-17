#!/usr/bin/env python3
"""Finite read-only copy/custody check; no native imports, network or writes."""
import hashlib
import json
import stat
from html.parser import HTMLParser
from pathlib import Path

R = Path(__file__).resolve().parent
P = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024")
S = P / "papers/23174156/sources"
def sha(data):
    return hashlib.sha256(data).hexdigest()
def pin(path):
    path = Path(path)
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), str(path)
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": sha(data),
            "mode": format(stat.S_IMODE(info.st_mode), "04o")}
inputs = json.loads((R / "SOURCES.json").read_text())
for expected in inputs["refs"] + [inputs["stylesheet"]]:
    actual = pin(expected["path"])
    assert all(actual[k] == expected[k] for k in ("bytes", "sha256", "mode")), expected["path"]
manifest = json.loads((S / "SOURCE_MANIFEST.json").read_text())
assert manifest["ordinary_files_including_controls"] == 186
assert manifest["child_directory_count"] == 18
expected_files = {x["path"] for x in manifest["files"]} | {"SOURCE_MANIFEST.json", "SOURCE_FINAL.json"}
expected_dirs = {x["path"] for x in manifest["directories"]}
actual_files, actual_dirs = set(), set()
assert stat.S_IMODE(S.lstat().st_mode) == 0o755
for path in S.rglob("*"):
    kind, rel = path.lstat().st_mode, path.relative_to(S).as_posix()
    if stat.S_ISREG(kind):
        actual_files.add(rel)
    elif stat.S_ISDIR(kind):
        actual_dirs.add(rel)
    else:
        raise AssertionError(("special source object", rel))
assert actual_files == expected_files and len(actual_files) == 186
assert actual_dirs == expected_dirs and len(actual_dirs) == 18
for row in manifest["files"]:
    actual = pin(S / row["path"])
    assert actual["bytes"] == row["bytes"] and actual["sha256"] == row["SHA256"], row["path"]
    assert int(actual["mode"], 8) == int(row["mode"], 8)
for row in manifest["directories"]:
    assert stat.S_IMODE((S / row["path"]).lstat().st_mode) == int(row["mode"], 8)
record = json.loads((S / "record.response.body").read_text())
files_api = json.loads((S / "files-23174156.response.body").read_text())
ready = json.loads((S / "SOURCE_READY.json").read_text())
model = json.loads((R / "model.json").read_text())
assert record["metadata"]["title"] == model["title"]
assert record["metadata"]["description"] == model["native_record_description"]
assert model["native_version"] == record["metadata"]["version"] == "1.0"
assert model["printed_numeric_version"] is None
assert model["record_created"] == record["created"] == "2026-10-05T23:36:06.236810+00:00"
assert model["record_modified"] == record["modified"] == "2026-10-10T21:43:19.907292+00:00"
assert files_api["order"] == []
assert all(x["updated"].startswith("2026-10-10") for x in files_api["entries"])
assert model["native_order"] == ready["native_order"] == [x["key"] for x in record["files"]]
assert model["native_order"][4] == "pr95_note.pdf" and len(model["native_order"]) == 7
for row in ready["native_assets"]:
    name = row["name"]
    assert (R / name).read_bytes() == (S / row["asset"]["path"]).read_bytes()
    assert pin(R / name)["bytes"] == row["asset"]["bytes"]
    assert pin(R / name)["sha256"] == row["asset"]["SHA256"]
for line in (R / "SHA256SUMS.txt").read_text().splitlines():
    digest, name = line.split("  ", 1)
    assert name in model["native_order"] and pin(R / name)["sha256"] == digest
tex = (S / "assets/pr95_note.tex").read_text()
assert len(tex.splitlines()) == 292
source_abstract = tex.split("\\begin{abstract}\n", 1)[1].split("\\end{abstract}", 1)[0]
for before, after in [(r"Reshetikhin--Turaev", "Reshetikhin–Turaev"),
                      (r"\Z", "ℤ"), (r"\wt", "τ̂"),
                      ("S^3", "S³"), (r"\sqrt5", "√5"), ("$", "")]:
    source_abstract = source_abstract.replace(before, after)
expected_abstract = (R / "EXPECTED_ABSTRACT.txt").read_text().strip()
assert " ".join(source_abstract.split()) == expected_abstract
class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.meta, self.links, self.iframes = [], {}, [], []
        self.abstract, self.jsonld = "", ""
        self.in_abstract, self.in_jsonld = False, False
        self.main_count, self.main_ends = 0, 0
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
main = (R / "MAIN.html").read_text().rstrip("\n")
head = (R / "HEAD.html").read_text().rstrip("\n")
assert html.count(main) == html.count(head) == 1
page = Page()
page.feed(html)
assert page.main_count == page.main_ends == 1 and len(page.ids) == len(set(page.ids))
assert page.abstract == model["abstract"] == page.meta["DC.description"] == expected_abstract
schema = json.loads(page.jsonld)
assert schema == model["scholarly_schema"] and schema["abstract"] == expected_abstract
assert [x["contentUrl"] for x in schema["encoding"]] == model["native_order"]
assert schema["datePublished"] == "2026-10-05" and schema["dateModified"].startswith("2026-10-10")
assert page.meta["citation_publication_date"] == "2026/10/05"
assert page.meta["citation_pdf_url"] == "pr95_note.pdf" and page.meta["citation_title"] == model["title"]
assert page.meta["description"] == page.meta["og:description"] == model["description"]
assert model["description"].startswith("Full ordinary SU(5) at WZW level 5 (shifted level 10)")
assert page.meta["robots"] == "noindex, nofollow"
assert not any(x.get("rel") == "canonical" for x in page.links)
assert {"rel": "stylesheet", "href": "../research.css"} in page.links
assert all(model[k] is None for k in ("canonical", "base_url", "production_url", "AA", "follow_up", "webpage_publication_date"))
assert not model["publication_authority"] and model["private_noindex"]
assert len(page.iframes) == 1 and page.iframes[0]["src"] == "pr95_note.pdf#view=FitH"
assert page.iframes[0]["title"].startswith("Original five-page manuscript:")
block = main.split('<ol id="native-assets">', 1)[1].split("</ol>", 1)[0]
positions = [block.index('href="' + n + '"') for n in model["native_order"]]
assert positions == sorted(positions)
assert "All 126 dominant labels" in main and "computational part of the full-category formula" in main
assert "full-weight NumPy reproduction was not completed" in main
assert "Kuriya" in main and "could not be obtained" in main and "Historical priority therefore remains unresolved" in main
assert "3475 + 1550√5" in main and "4025 + 1800√5" in main and "550 + 250√5" in main
assert "current deposited files were updated on 10 October 2026" in main
assert "Manuscript dated" in main and "Private preview" not in main
bib = (R / "citation.bib").read_text()
assert "10.5281/zenodo.23174156" in bib and "version = {1.0}" in bib and "day = {5}" in bib
inner = main.split(">", 1)[1].rsplit("</main>", 1)[0].encode()
print(json.dumps({"status": "PASS_BOUNDED_DATA_ONLY", "record": 23174156,
    "source_files_whole_bytes_modes": 186, "source_child_directories": 18,
    "external_input_refs_unchanged": len(inputs["refs"]) + 1,
    "all_seven_native_assets_byte_identical_in_exact_order": True,
    "full_abstract_source_visible_DC_schema_model_equal": True,
    "semantic_MAIN_unique_ids_HEAD_MAIN_index_equal": True,
    "native_creation_update_printed_version_distinction_retained": True,
    "ordinary_full_category_and_no_successful_full_weight_replay_claim": True,
    "private_noindex_canonical_AA_publication_followup_null": True,
    "whole_MAIN_inner": {"bytes": len(inner), "sha256": sha(inner)},
    "whole_MAIN_file": pin(R / "MAIN.html"), "index": pin(R / "index.html"),
    "HEAD": pin(R / "HEAD.html"), "model": pin(R / "model.json"), "BibTeX": pin(R / "citation.bib"),
    "native_scientific_old_helper_browser_renderer_or_network_execution": False,
    "live_native_viewer_download_mobile_or_hosting_certification": False}, indent=2))
