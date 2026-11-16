#!/usr/bin/env python3
"""One bounded read-only data comparison; no project imports, renders or GETs."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import struct

R = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/mixed-kato-editorial-fact-sol-20261116")
W = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23444050/reviews/editorial")
checks = []
def need(ok, name):
    if not ok:
        raise ValueError(name)
    checks.append(name)
def pin(p):
    need(p.is_file() and not p.is_symlink(), "regular:" + str(p))
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def norm(s):
    return " ".join(s.split())
def extent():
    entries = sorted(W.rglob("*"))
    need(not any(p.is_symlink() for p in entries), "writer_no_symlinks")
    return [(p.relative_to(W).as_posix(), pin(p)) for p in entries if p.is_file()]
before = extent()
need(pin(W / "FINAL.json") == {"bytes": 6018, "sha256": "0c4e3d8dc81255308a469d3994346a0c87c16370fb13f0a0ddb411ff74d1107d"}, "actual_writer_FINAL")
need(pin(W / "OWNED_MANIFEST.json") == {"bytes": 5580, "sha256": "565a480382a0ec14bf4c66dabc7415dda296029f74a52fef8598c71b72adba44"}, "actual_writer_manifest")
manifest = json.loads((W / "OWNED_MANIFEST.json").read_text())
controls = ["OWNED_MANIFEST.json", "FINAL.json"]
need(manifest["root_controls_excluded_from_own_payload_list"] == controls, "exact_writer_controls")
actual = [{"path": name, "bytes": data["bytes"], "SHA256": data["sha256"]} for name, data in before if name not in controls]
need(actual == manifest["files"] and len(before) == 35, "whole_writer_files_exact")
dirs = sorted(p.relative_to(W).as_posix() for p in W.rglob("*") if p.is_dir())
need(dirs == manifest["child_directories"] == ["preview", "renders"], "whole_writer_directories_exact")
initial = json.loads((R / "INITIAL_SEAL.json").read_text())
need(pin(R / "INITIAL_SEAL.json")["sha256"] == "de13cd855921005cb1487bc2cd432937a259cf2d8846b3db633fde79f85c52be", "fact_INITIAL_seal_exact")
for item in initial["finite_initial_payload"]:
    data = (R / item["path"]).read_bytes()
    if item["path"] == "RESEARCH_LOG.md":
        data = data[:item["bytes"]]
    need(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"], "fact_initial:" + item["path"])
for item in json.loads((R / "SOURCE_PINS.json").read_text())["references"]:
    need(pin(Path(item["path"])) == {k: item[k] for k in ("bytes", "sha256")}, "source_reference:" + item["path"])

class Surface(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.frames, self.meta, self.ld = [], [], [], {}, []
        self.sections, self.abstract, self.native_links = [], [], []
        self.in_abstract_p = False
        self.in_native = False
        self.in_ld = False
        self.bases, self.canonical, self.main_count = [], [], 0
    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "main":
            self.main_count += 1
        if tag == "section":
            self.sections.append(a.get("id"))
        if tag == "p" and self.sections and self.sections[-1] == "original-abstract":
            self.in_abstract_p = True
        if tag == "ol" and a.get("id") == "native-downloads":
            self.in_native = True
        if tag == "a":
            self.links.append(a.get("href", ""))
            if self.in_native:
                self.native_links.append(a.get("href", ""))
        if tag == "iframe":
            self.frames.append(a)
        if tag == "meta" and "name" in a:
            self.meta[a["name"]] = a.get("content", "")
        if tag == "base":
            self.bases.append(a)
        if tag == "link" and "canonical" in a.get("rel", "").split():
            self.canonical.append(a)
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_ld = True
            self.ld.append("")
    def handle_endtag(self, tag):
        if tag == "section":
            self.sections.pop()
        if tag == "p":
            self.in_abstract_p = False
        if tag == "ol":
            self.in_native = False
        if tag == "script":
            self.in_ld = False
    def handle_data(self, data):
        if self.in_abstract_p:
            self.abstract.append(data)
        if self.in_ld:
            self.ld[-1] += data

page = (W / "preview/index.html").read_text()
main = (W / "MAIN.html").read_text()
head = (W / "HEAD.html").read_text()
model = json.loads((W / "PAGE_MODEL.json").read_text())
expect = json.loads((R / "EXPECTATIONS.json").read_text())
surface = Surface()
surface.feed(page)
need(page.count(main) == 1 and page.count(head) == 1, "whole_MAIN_and_HEAD_exactly_embedded")
need(surface.main_count == 1 and '<main id="main">' in main, "semantic_main")
need(len(surface.ids) == len(set(surface.ids)), "unique_ids")
raw = expect["manuscript_abstract_complete_TeX"]
abstract = norm(raw.replace("\\(H_2^2\\)", "H₂²").replace("--", "–").replace("'", "’"))
visible = norm("".join(surface.abstract))
need(len(surface.ld) == 1, "one_JSONLD")
ld = json.loads(surface.ld[0])
need(visible == abstract == model["original_abstract"] == ld["abstract"] == surface.meta["DC.description"], "complete_original_abstract_all_surfaces")
native = expect["native_metadata_original"]
need(model["title"] == native["title"] == ld["name"] == surface.meta["citation_title"], "title")
need(ld["datePublished"] == model["publication_date"] == native["publication_date"] == "2026-10-17", "original_publication_date")
need(surface.meta["citation_publication_date"] == "2026/10/17", "citation_date")
need(ld["version"] == model["version"] == native["version"] == surface.meta["citation_version"] == "1.0.0", "native_version")
need(model["native_created"] == expect["native_created_original"], "creation_distinct")
need("no numeric version printed in PDF" in model["version_source"], "printed_version_absent")
need(surface.meta["citation_author_orcid"] == model["author"]["ORCID"] == ld["author"]["identifier"] == "https://orcid.org/0009-0001-9320-500X", "ORCID")
need(surface.meta["citation_doi"] == model["native_DOI"] == native["doi"], "DOI")
need(ld["creativeWorkStatus"] == "Unrefereed preprint", "unrefereed_metadata")
need(surface.meta["robots"] == "noindex, nofollow" and not surface.bases and not surface.canonical, "private_noindex_no_canonical_or_base")
need(model["public_canonical"] is None and model["AA"] is None and model["follow_up"] is None and model["production_authority"] is False, "private_nulls")
description_hash = hashlib.sha256(native["description"].encode()).hexdigest()
need(model["native_Description_source"]["SHA256_of_HTML"] == description_hash, "native_Description_private_reference")
need(model["native_Description_source"]["not_the_manuscript_abstract"] is True, "abstract_Description_distinct")
need('Private preview' not in main and 'Arial' in page and 'background:#fff' in page, "plain_public_MAIN")
items = expect["native_record_file_objects_original_order"]
need([x["name"] for x in model["native_assets_in_order"]] == [x["key"] for x in items], "native_asset_order")
native_links = []
for i, item in enumerate(items):
    declared = model["native_assets_in_order"][i]
    source, target = Path(declared["source_path"]), W / "preview" / item["key"]
    b = source.read_bytes()
    need(target.read_bytes() == b and len(b) == item["size"] == declared["bytes"], "native_bytes:" + item["key"])
    need("md5:" + hashlib.md5(b).hexdigest() == item["checksum"] == declared["native_MD5"], "native_MD5:" + item["key"])
    need(hashlib.sha256(b).hexdigest() == declared["SHA256"], "native_SHA256:" + item["key"])
    need(ld["encoding"][i]["name"] == item["key"] and ld["encoding"][i]["contentSize"] == str(item["size"]) + " bytes", "encoding_order:" + item["key"])
    native_links.extend([item["key"], item["links"]["self"]])
need(surface.native_links == native_links, "visible_native_download_links_order")
need(len(surface.frames) == 1 and surface.frames[0]["src"] == items[0]["key"] + "#view=FitH" and surface.frames[0].get("title"), "titled_local_PDF_embed")
local_links = []
for href in surface.links:
    parsed = urlsplit(href)
    if not parsed.scheme and not parsed.netloc and parsed.path:
        target = W / "preview" / unquote(parsed.path)
        need(target.is_file(), "local_link:" + href)
        local_links.append(href)
need((W / "citation.bib").read_bytes() == (W / "preview/citation.bib").read_bytes(), "BibTeX_duplicate_exact")
bib = (W / "citation.bib").read_text()
need(native["title"] in bib and native["doi"] in bib and "no numeric version printed in the PDF" in bib, "BibTeX_identity_and_version_scope")
need(model["license_url"] == ld["license"] == "https://creativecommons.org/licenses/by/4.0/" and "code and analysis" in model["rights"] and "third-party" in model["rights"], "authored_CCBY_rights_scope")
views = []
for name in ["desktop-top", "desktop-result", "desktop-downloads", "mobile-top", "mobile-explanation", "mobile-abstract"]:
    b = (W / "renders" / (name + ".png")).read_bytes()
    need(b[:8] == b"\x89PNG\r\n\x1a\n", "PNG:" + name)
    width, height = struct.unpack(">II", b[16:24])
    views.append({"name": name, "width": width, "height": height})
render = json.loads((W / "RENDER_RESULT.json").read_text())
after = extent()
need(after == before, "writer_whole_bytes_and_extent_unchanged")
print(json.dumps({"status": "PASS_INDEPENDENT_FACT_DATA_ONLY",
    "checks_passed": len(checks), "writer_files": len(before), "writer_child_directories": dirs,
    "whole_page": pin(W / "preview/index.html"), "whole_MAIN": pin(W / "MAIN.html"),
    "full_abstract_characters": len(abstract), "local_links_checked": local_links,
    "saved_image_dimensions": views,
    "literal_writer_errors": {k: render[k] for k in ["blockedHTTP", "requestFailures", "consoleErrors", "pageErrors"]},
    "literal_writer_downloadClicks": render["downloadClicks"],
    "literal_writer_nativePDFOrLiveDownloadCertification": render["nativePDFOrLiveDownloadCertification"],
    "writer_before_after_equal": after == before, "scientific_or_render_or_GET_executions": [],
    "limits": "Data comparison only. Six existing screenshots were personally viewed separately; mobile PDF partial compositor image, no clean/live/download certification."}, indent=2))
