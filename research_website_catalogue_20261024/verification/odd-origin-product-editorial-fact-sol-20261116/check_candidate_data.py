#!/usr/bin/env python3
"""Bounded read-only fact data comparison; no project imports, rendering or GET."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import struct

R = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/odd-origin-product-editorial-fact-sol-20261116")
W = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23334001/reviews/editorial")
S = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23334001/sources")
checks = []
def need(ok, label):
    if not ok:
        raise ValueError(label)
    checks.append(label)
def pin(p):
    need(p.is_file() and not p.is_symlink(), "regular:" + str(p))
    b = p.read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
def canonical(s):
    return " ".join(s.replace("$", "").replace("k_{403,a}", "k403,a").replace("’", "'").split())
def extent():
    entries = sorted(W.rglob("*"))
    need(not any(p.is_symlink() for p in entries), "writer_no_symlinks")
    return [(p.relative_to(W).as_posix(), pin(p)) for p in entries if p.is_file()]
before = extent()
need(pin(W / "FINAL.json") == {"bytes": 4338, "sha256": "13e5f4a4acaab90ac9474006d6ef4f45ad5b546a4d5aeac0215c244ce783baf3"}, "specific_writer_FINAL")
need(pin(W / "OWNED_MANIFEST.json") == {"bytes": 5072, "sha256": "36ce5160efc4dd37db9dd124f31a9b0af9b3a4a5b5d33a362355627358dc0eb0"}, "specific_writer_manifest")
final = json.loads((W / "FINAL.json").read_text())
manifest = json.loads((W / "OWNED_MANIFEST.json").read_text())
controls = ["OWNED_MANIFEST.json", "FINAL.json"]
need(manifest["excluded_seal_files"] == controls, "exact_writer_controls")
need([{"path": n, **p} for n, p in before if n not in controls] == manifest["files"], "whole_writer_file_pins")
dirs = sorted(p.relative_to(W).as_posix() for p in W.rglob("*") if p.is_dir())
need(len(before) == 32 and dirs == manifest["child_directories"] == ["preview", "renders"], "whole_writer_extent")
need(pin(R / "INITIAL_SEAL.json")["sha256"] == "cd363fbd78742e9ba67011e0dbc8054b82b2e5c064b517cf8fd4fb4bb9154cc3", "fact_INITIAL_seal")
initial = json.loads((R / "INITIAL_SEAL.json").read_text())
for e in initial["finite_initial_payload"]:
    b = (R / e["path"]).read_bytes()
    if e["path"] == "RESEARCH_LOG.md":
        b = b[:e["bytes"]]
    need(len(b) == e["bytes"] and hashlib.sha256(b).hexdigest() == e["sha256"], "initial_payload:" + e["path"])
for e in json.loads((R / "SOURCE_PINS.json").read_text())["references"]:
    need(pin(Path(e["path"])) == {k: e[k] for k in ("bytes", "sha256")}, "source_reference:" + e["path"])

class Surface(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.frames, self.meta, self.ld = [], [], [], {}, []
        self.sections, self.abstract, self.native_links, self.styles = [], [], [], []
        self.in_abstract_p = self.in_native = self.in_ld = False
        self.bases, self.canonicals, self.main_count, self.h1_count = [], [], 0, 0
    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "main":
            self.main_count += 1
        if tag == "h1":
            self.h1_count += 1
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
            self.canonicals.append(a)
        if tag == "link" and "stylesheet" in a.get("rel", "").split():
            self.styles.append(a["href"])
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
model = json.loads((W / "PAGE_MODEL.json").read_text())
expected = json.loads((R / "EXPECTATIONS.json").read_text())
native = expected["native_metadata_original"]
surface = Surface()
surface.feed(page)
need(page.count(main) == 1 and surface.main_count == surface.h1_count == 1 and '<main id="main">' in main, "whole_MAIN_exact_semantic_wrapper")
need(len(surface.ids) == len(set(surface.ids)), "unique_ids")
need(len(surface.ld) == 1, "one_ScholarlyArticle")
ld = json.loads(surface.ld[0])
abstract = canonical(expected["manuscript_abstract_complete_TeX"])
need(abstract == canonical("".join(surface.abstract)) == canonical(model["abstract"]) == canonical(ld["abstract"]) == canonical(surface.meta["DC.description"]), "complete_source_abstract_all_surfaces")
need(model["abstract_tex"].replace("\\n", "\n").strip() == expected["manuscript_abstract_complete_TeX"].strip(), "private_source_abstract_tex_encoding")
need(model["native_metadata_original"] == native and model["native_description_original"] == native["description"], "native_metadata_Description_literal")
need(model["native_record_files"] == expected["native_record_file_objects_original_order"] and model["native_files_response"] == expected["native_files_endpoint_complete_original"], "native_file_objects_literal")
need(model["visible_duplicate_description"] is False, "Description_not_duplicated")
need(model["title"] == ld["name"] == surface.meta["citation_title"] == native["title"], "title")
need(ld["datePublished"] == native["publication_date"] == "2026-10-13" and surface.meta["citation_publication_date"] == "2026/10/13", "publication_date")
need(model["native_created"] == expected["native_created_original"], "creation_timestamp")
need(model["printed_version"] is None and model["printed_date"] == "13 October 2026", "printed_date_and_absent_version")
need(model["native_version"] == ld["version"] == surface.meta["citation_version"] == native["version"] == "1.0", "native_version")
need(surface.meta["citation_author_orcid"] == ld["author"]["identifier"] == "https://orcid.org/0009-0001-9320-500X", "ORCID")
need(surface.meta["citation_doi"] == ld["identifier"]["value"] == native["doi"], "DOI")
need("noindex" in surface.meta["robots"] and "nofollow" in surface.meta["robots"] and not surface.bases and not surface.canonicals, "private_robots_no_canonical_base")
need(all(model[k] is None for k in ["canonical_url", "base_url", "production_url", "AA", "follow_up"]) and model["publication_authority"] is False, "private_nulls")
need("Private preview" not in main and "Private candidate" not in main, "no_private_admin_in_MAIN")
need(surface.styles == ["research.css"], "shared_stylesheet_link")
need(pin(W / "preview/research.css") == {"bytes": 1170, "sha256": "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a"}, "exact_stylesheet")
css = (W / "preview/research.css").read_text()
need("Arial, Helvetica, sans-serif" in css and "background: #fff;" in css, "white_Arial")
items = expected["native_record_file_objects_original_order"]
need(model["native_asset_order"] == [e["key"] for e in items], "ZIP_then_PDF_order")
links = []
for i, e in enumerate(items):
    b = (S / "assets" / e["key"]).read_bytes()
    need((W / "preview" / e["key"]).read_bytes() == b and len(b) == e["size"], "native_bytes:" + e["key"])
    need("md5:" + hashlib.md5(b).hexdigest() == e["checksum"], "native_MD5:" + e["key"])
    need(ld["encoding"][i]["name"] == e["key"] and ld["encoding"][i]["contentSize"] == str(e["size"]) + " bytes" and ld["encoding"][i]["sameAs"] == e["links"]["self"], "encoding:" + e["key"])
    links.extend([e["key"], e["links"]["self"]])
need(surface.native_links == links, "visible_native_link_order")
need(len(surface.frames) == 1 and surface.frames[0]["src"] == items[1]["key"] + "#view=FitH" and surface.frames[0].get("title"), "titled_unchanged_PDF_reference")
local, root_relative = [], []
for href in surface.links + surface.styles:
    parsed = urlsplit(href)
    if parsed.path.startswith("/"):
        root_relative.append(href)
    elif not parsed.scheme and not parsed.netloc and parsed.path:
        need((W / "preview" / unquote(parsed.path)).is_file(), "local_file:" + href)
        local.append(href)
bib = (W / "preview/citation.bib").read_text()
need(native["title"] in bib and native["doi"] in bib and "no version number printed in the manuscript" in bib and "version = {1.0}" in bib, "BibTeX_identity_native_version")
need(model["rights"]["authored_manuscript_and_verification"] == "CC BY 4.0" and model["rights"]["third_party_papers_raw_extracts_excluded"] is True and model["rights"]["MIT_not_inferred"] is True and ld["license"] == "https://creativecommons.org/licenses/by/4.0/", "authored_CCBY_exclusions_noMIT")
render = json.loads((W / "RENDER_RECEIPT.json").read_text())
views = []
for view in render["captures"]:
    b = (W / view["path"]).read_bytes()
    need(b[:8] == b"\x89PNG\r\n\x1a\n", "PNG:" + view["path"])
    width, height = struct.unpack(">II", b[16:24])
    need((width, height) == (view["width"], view["height"]), "PNG_dimensions:" + view["path"])
    views.append({"path": view["path"], "width": width, "height": height})
need(len(views) == 6, "six_existing_saved_views")
need(len(render["diagnostics"]["console_errors"]) == len(render["diagnostics"]["failed_requests"]) == len(render["diagnostics"]["nonlocal_page_routes_aborted"]) == 12, "literal_twelve_failures_retained")
need(render["actual_embedded_PDF_display_certified"] is False and final["actual_download_clicks_or_live_checks"] is False, "no_display_live_download_certification")
after = extent()
need(after == before, "whole_writer_bytes_and_extent_unchanged")
print(json.dumps({"status": "PASS_INFORMED_FACT_DATA_ONLY_WITH_READER_LIMITS", "checks_passed": len(checks),
    "writer_files": len(before), "writer_child_directories": dirs,
    "whole_page": pin(W / "preview/index.html"), "whole_MAIN": pin(W / "MAIN.html"),
    "source_abstract_characters_after_math_markup_normalization": len(abstract),
    "source_abstract_math_normalization": "Only whitespace, apostrophe typography and k403,a subscript/TeX markup normalized.",
    "local_file_links_checked": local, "root_relative_navigation_untested": root_relative,
    "saved_image_dimensions": views, "literal_writer_render_diagnostics": render["diagnostics"],
    "literal_writer_render_failure": render["failure"], "literal_writer_context_offline": render["context_offline"],
    "literal_writer_actual_embedded_PDF_display_certified": render["actual_embedded_PDF_display_certified"],
    "literal_writer_actual_download_clicks_or_live_checks": final["actual_download_clicks_or_live_checks"],
    "writer_before_after_equal": after == before, "scientific_stage_render_oldhelper_or_GET_executions": [],
    "limits": "Saved HTML views only: desktop PDF dark, mobile PDF blank, no visible manuscript page, no native/live/download certification."}, indent=2))
