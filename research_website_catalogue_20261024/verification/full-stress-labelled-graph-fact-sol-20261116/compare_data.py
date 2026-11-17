#!/usr/bin/env python3
"""One explicit data-only comparison. Reads fixed packets; writes only own fresh result."""
import hashlib
import json
from pathlib import Path
import re
import stat
import sys
from html.parser import HTMLParser

P = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024")
OWN = P / "verification/full-stress-labelled-graph-fact-sol-20261116"
WRITER = P / "verification/full-stress-labelled-graph-editorial-sol-20261116"
SOURCE = P / "papers/23331540/sources"
RESULT = OWN / "DATA_CHECK.json"
FINAL_PIN = (4968, "f588e3eeeb3767df2b456eea3bd5857e78ff0c8dda553beb165352e2ce77b554")
MANIFEST_PIN = (4065, "7cd793fe07a003e76c50a91d829697d98f72c55b916c3011e1a32f28c5398f3d")
INITIAL_CONTROL_PINS = {
    "INITIAL_MANIFEST.json": (2177, "7af4428f6f7e3a79441c3f48555019ee604082bf8f4eb75b50473b0e4c480a53"),
    "INITIAL_SEAL.json": (2957, "4f6549e48ad20617d1792fe378db7e74b0de1a3e5cda368ac108b34d655a9070"),
}

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def raw(path):
    need(stat.S_ISREG(path.lstat().st_mode), "not an ordinary file: " + str(path))
    return path.read_bytes()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def obj(path):
    return json.loads(raw(path))

def pinned(path, size, sha):
    data = raw(path)
    need(len(data) == size and digest(data) == sha, "pin mismatch: " + str(path))
    return data

def snapshot(root):
    files, directories = {}, {}
    need(stat.S_ISDIR(root.lstat().st_mode), "root type")
    directories["."] = stat.S_IMODE(root.lstat().st_mode)
    for path in sorted(root.rglob("*")):
        info = path.lstat()
        rel = path.relative_to(root).as_posix()
        if stat.S_ISDIR(info.st_mode):
            directories[rel] = stat.S_IMODE(info.st_mode)
        else:
            need(stat.S_ISREG(info.st_mode), "symlink/special object: " + rel)
            data = raw(path)
            files[rel] = {"bytes": len(data), "SHA256": digest(data),
                          "mode": stat.S_IMODE(info.st_mode)}
    return {"files": files, "directories": directories}

def mode(value):
    return value if isinstance(value, int) else int(value, 8)

def rows_equal(snap, rows):
    for row in rows:
        need(row["path"] in snap["files"], "missing: " + row["path"])
        expected = {"bytes": row["bytes"], "SHA256": row["SHA256"],
                    "mode": mode(row["mode"])}
        need(snap["files"][row["path"]] == expected, "row mismatch: " + row["path"])

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta, self.links, self.iframes, self.anchors = {}, [], [], []
        self.main_count, self.abstract_depth = 0, 0
        self.abstract_text = []
        self.in_ld, self.ld_text, self.ld = False, [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            self.meta[a.get("name", a.get("property", ""))] = a.get("content")
        if tag == "link":
            self.links.append(a)
        if tag == "iframe":
            self.iframes.append(a)
        if tag == "a":
            self.anchors.append(a)
        if tag == "main" and a.get("id") == "main":
            self.main_count += 1
        if a.get("id") == "abstract-text":
            self.abstract_depth = 1
        elif self.abstract_depth:
            self.abstract_depth += 1
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_ld, self.ld_text = True, []
    def handle_endtag(self, tag):
        if self.abstract_depth:
            self.abstract_depth -= 1
        if tag == "script" and self.in_ld:
            self.ld.append(json.loads("".join(self.ld_text)))
            self.in_ld = False
    def handle_data(self, data):
        if self.abstract_depth:
            self.abstract_text.append(data)
        if self.in_ld:
            self.ld_text.append(data)

def check():
    need(not RESULT.exists(), "one-run result already exists; do not replay")
    expect = obj(OWN / "EXPECTATIONS.json")
    own_initial = obj(OWN / "INITIAL_MANIFEST.json")
    for name, (size, sha) in INITIAL_CONTROL_PINS.items():
        pinned(OWN / name, size, sha)
    for row in own_initial["files"]:
        if not row.get("terminal_control"):
            data = pinned(OWN / row["path"], row["bytes"], row["SHA256"])
            need(stat.S_IMODE((OWN / row["path"]).lstat().st_mode) == mode(row["mode"]),
                 "INITIAL mode mismatch")
    writer_final = json.loads(pinned(WRITER / "FINAL.json", *FINAL_PIN))
    writer_manifest = json.loads(pinned(WRITER / "MANIFEST.json", *MANIFEST_PIN))
    before_writer, before_source = snapshot(WRITER), snapshot(SOURCE)
    rows_equal(before_writer, writer_manifest["payload_files"])
    need(set(before_writer["files"]) == {r["path"] for r in writer_manifest["payload_files"]}
         | {"FINAL.json", "MANIFEST.json"}, "writer exact file boundary")
    expected_dirs = {".": mode(writer_manifest["root_mode"])}
    expected_dirs.update({r["path"]: mode(r["mode"]) for r in writer_manifest["directories"]})
    need(before_writer["directories"] == expected_dirs, "writer exact directories/modes")
    need(len(before_writer["files"]) == 22 and len(expected_dirs) == 3, "writer22/2")
    source_custody = obj(OWN / "SOURCE_CUSTODY.json")
    rows_equal(before_source, source_custody["files"])
    need(set(before_source["files"]) == {r["path"] for r in source_custody["files"]},
         "source exact files")
    need(before_source["directories"] == {r["path"]: mode(r["mode"])
          for r in source_custody["directories"]}, "source exact directories/modes")
    need(len(before_source["files"]) == 133 and len(before_source["directories"]) == 15,
         "source133/14")
    for ref in source_custody["authority_and_reading_references"]:
        pinned(Path(ref["path"]), ref["bytes"], ref["SHA256"])
    aliases = {
        "original-objects/record.json": "record.response.body",
        "original-objects/files.json": "files-23331540.response.body",
        "original-objects/authored-metadata.json":
            "published-source/container-001/tree/full_stress_stratifications_v1/metadata.json",
        "original-objects/RIGHTS_README.md":
            "published-source/container-001/tree/full_stress_stratifications_v1/README.md",
    }
    for dest, original in aliases.items():
        need(raw(WRITER / dest) == raw(SOURCE / original), "native object copy " + dest)
    model = obj(WRITER / "page-model.json")
    record = obj(SOURCE / "record.response.body")
    html = raw(WRITER / "article.html").decode("utf-8")
    head = raw(WRITER / "head.html").decode("utf-8")
    main = raw(WRITER / "public-main.html").decode("utf-8")
    need(re.search(r"<head>.*?</head>", html, re.S).group(0) + "\n" == head,
         "whole head bytes")
    need(re.search(r'<main id="main">.*?</main>', html, re.S).group(0) + "\n" == main,
         "whole MAIN bytes")
    page = Page()
    page.feed(html)
    need(page.main_count == 1 and len(page.ld) == 1, "semantic MAIN/JSON-LD count")
    tex = raw(SOURCE / "published-source/container-001/tree/full_stress_stratifications_v1/research_note.tex").decode()
    native_abstract = tex.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0]
    native_abstract = " ".join(native_abstract.replace("~", " ").split())
    need(native_abstract == expect["full_original_abstract"], "sealed abstract/native")
    visible = " ".join("".join(page.abstract_text).split())
    need(visible == native_abstract == page.meta["DC.description"] ==
         page.ld[0]["abstract"] == model["abstract"], "all complete abstract surfaces")
    need(model["title"] == record["metadata"]["title"] == page.meta["citation_title"]
         == page.ld[0]["name"], "title surfaces")
    need(model["native_version"] == "1.0" and model["printed_version"] is None, "version")
    need(model["publication_date"] == "2026-10-12" == page.ld[0]["datePublished"],
         "publication date")
    need(model["record_created"] == record["created"], "creation date")
    for key in ["canonical_url", "base_url", "production_url", "AA", "follow_up"]:
        need(model[key] is None, "private null: " + key)
    need(model["publication_authority"] is False, "private authority")
    need(page.meta["robots"] == page.meta["googlebot"] == "noindex, nofollow",
         "private indexing")
    need(not any(x.get("rel") == "canonical" for x in page.links) and "<base" not in html,
         "no active canonical/base")
    assets = expect["native_assets"]
    need([x["name"] for x in model["native_asset_order"]] == [x["key"] for x in assets],
         "native order in model")
    need([x["name"] for x in page.ld[0]["encoding"]] == [x["key"] for x in assets],
         "native order in schema")
    for asset in assets:
        rel = "assets/" + asset["key"]
        copy = pinned(WRITER / rel, asset["bytes"], asset["SHA256"])
        need(copy == raw(SOURCE / rel), "native whole copy")
        need(hashlib.md5(copy).hexdigest() == asset["MD5"], "native MD5")
        need(any(a.get("href") == rel and "download" in a for a in page.anchors),
             "download anchor")
        need(any(a.get("href") == asset["original_content_URL"] for a in page.anchors),
             "Zenodo original anchor")
    pdf = "assets/" + assets[0]["key"]
    need(len(page.iframes) == 1 and page.iframes[0].get("title")
         and page.iframes[0].get("src") == pdf, "actual frozen titled iframe")
    need(any(a.get("href") == pdf and a.get("target") == "_blank" for a in page.anchors),
         "direct PDF open")
    need(digest(raw(WRITER / "research.css")) ==
         "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a",
         "1170-byte shared CSS")
    bib = raw(WRITER / "citation.bib").decode()
    need(expect["DOI"] in bib and expect["source_title"] in bib and "version = {1.0}" in bib,
         "Bib identity/version")
    need(snapshot(WRITER) == before_writer and snapshot(SOURCE) == before_source,
         "whole writer/source changed during data read")
    result = {
        "status": "PASS_BOUNDED_DATA_CONSISTENCY_WITH_PRESENTATION_NOTE",
        "writer_regular_files": 22, "writer_child_directories": 2,
        "source_regular_files": 133, "source_child_directories": 14,
        "initial_payloads_and_controls_unchanged": True,
        "all_writer_and_source_whole_bytes_modes_topology_unchanged": True,
        "complete_original_abstract_visible_model_schema_DC_equal": True,
        "whole_HEAD_and_MAIN_exact": True, "native_two_asset_order_bytes_MD5_exact": True,
        "private_noindex_null_authority_and_metadata_consistent": True,
        "presentation_note": {
            "actual_iframe_src": pdf, "initial_contract_expected": pdf + "#view=FitH",
            "root_clarification": "FitH itself was not an explicit user requirement; presentation-contract discrepancy, not scientific/source-fidelity defect.",
            "working_reader_or_download_certified": False},
        "manual_whole_copy_review_separate": True,
        "native_science_producer_old_helpers_render_browser_network_W_Git_Sheet_actions": [],
        "follow_up": None, "publication_authority": False}
    RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "writer": [22, 2], "source": [133, 14],
                      "result": "DATA_CHECK.json"}, sort_keys=True))

if __name__ == "__main__":
    if sys.argv[1:] != ["--check"]:
        raise SystemExit("No action. This fixed data comparison requires --check.")
    check()

