#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One bounded read-only corpus authentication/search. No script evaluation, network or writes."""
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat
import sys
import unicodedata
from urllib.parse import unquote

R = Path(__file__).resolve().parent
if len(sys.argv) != 1:
    raise SystemExit("No arguments accepted; this utility only reads fixed data and prints JSON.")

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
def digest(body, kind="sha256"):
    return hashlib.new(kind, body).hexdigest()
def pinned(item, root=None):
    p = (root / item["path"]) if root is not None else Path(item["path"])
    body = p.read_bytes()
    require(len(body) == item["bytes"], "Byte mismatch: " + str(p))
    require(digest(body) == item["sha256"], "SHA256 mismatch: " + str(p))
    return body
def normalized(value):
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.sub(r"[\W_]+", " ", value).split())

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.ids, self.h1s, self.title_parts = [], [], [], []
        self.in_title = self.in_h1 = False
    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.in_h1 = True
        self.parts.append(" ")
    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_h1 = False
        self.parts.append(" ")
    def handle_data(self, data):
        self.parts.append(data)
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h1:
            self.h1s.append(data)

plan = json.loads((R / "TARGETS.json").read_text())
for item in plan["checkpoint_files"]:
    pinned(item, R)
for target in plan["targets"]:
    record = json.loads(pinned(target["record_source"]))
    require(record["id"] == target["record_id"], "Wrong native record")
    require(int(record["conceptrecid"]) == target["concept_id"], "Wrong concept record")
    require(record["metadata"]["title"] == target["title"], "Wrong native title")
inventory = json.loads(pinned(plan["input_inventory"]))
wrapper = json.loads(pinned(plan["input_tree"]))
require(wrapper.get("isError") is False, "Cached tree connector isError is not false")
tree = json.loads(wrapper["structuredContent"]["content"])
require(tree["sha"] == plan["docs_tree"] and tree["truncated"] is False,
        "Wrong or truncated docs metadata")
entries = tree["tree"]
require(len(entries) == plan["expected_tree_entries"], "Wrong recursive entry count")
by_path = {x["path"]: x for x in entries}
require(len(by_path) == len(entries), "Duplicate docs path")
tree_hashes = {"": tree["sha"]}
children = {}
for entry in entries:
    require(entry["type"] in ("tree", "blob"), "Unexpected Git object type")
    parent, _, name = entry["path"].rpartition("/")
    require(name and "\0" not in name, "Invalid Git entry name")
    children.setdefault(parent, []).append((name, entry))
    if entry["type"] == "tree":
        tree_hashes[entry["path"]] = entry["sha"]
authenticated_trees = []
for directory, expected in sorted(tree_hashes.items()):
    child_list = children.get(directory, [])
    child_list.sort(key=lambda pair: (pair[0] + ("/" if pair[1]["type"] == "tree" else "")).encode())
    raw_tree = b""
    for name, item in child_list:
        mode = format(int(item["mode"], 8), "o").encode()
        raw_tree += mode + b" " + name.encode() + b"\0" + bytes.fromhex(item["sha"])
    actual = digest(b"tree " + str(len(raw_tree)).encode() + b"\0" + raw_tree, "sha1")
    require(actual == expected, "Git tree mismatch: " + directory)
    authenticated_trees.append({"path": "docs" + ("/" + directory if directory else ""),
                                "Git_tree": actual, "children": len(child_list)})
require(len(authenticated_trees) == plan["expected_tree_objects_including_root"], "Wrong tree count")
html_entries = {p: x for p, x in by_path.items()
                if x["type"] == "blob" and p.lower().endswith(".html")}
require(len(html_entries) == plan["expected_HTML_bodies"], "Wrong HTML count")
old_rows = {x["path"].removeprefix("docs/"): x for x in inventory["rows"]}
require(set(old_rows) == set(html_entries), "Cached47-body paths differ from current HTML paths")
compiled = {str(t["record_id"]): [(q, re.compile(q["pattern"], re.I)) for q in t["queries"]]
            for t in plan["targets"]}
rows = []
for relative, entry in sorted(html_entries.items()):
    old = old_rows[relative]
    require(old["Git_blob"] == entry["sha"] and old["bytes"] == entry["size"],
            "Current HTML Git metadata mismatch: " + relative)
    ref = old["body_reference"]
    body = pinned({"path": ref["path"], "bytes": ref["bytes"], "sha256": ref["SHA256"]})
    require(len(body) == entry["size"] and digest(body) == old["SHA256"],
            "Cached HTML byte/SHA mismatch: " + relative)
    blob = digest(b"blob " + str(len(body)).encode() + b"\0" + body, "sha1")
    require(blob == entry["sha"], "HTML Git blob mismatch: " + relative)
    decoding_error = None
    try:
        raw = body.decode("utf-8")
    except UnicodeDecodeError as error:
        decoding_error = str(error)
        raw = body.decode("utf-8", errors="replace")
    tags = Tags()
    tags.feed(raw)
    text = " ".join("".join(tags.parts).split())
    norm = normalized(text)
    channels = {"raw": raw, "decoded": html.unescape(raw), "text": text,
                "url_decoded": unquote(html.unescape(raw)), "normalized": norm,
                "compact": re.sub(r"[\W_]+", "", norm)}
    matched = {}
    for record, queries in compiled.items():
        hits = []
        for query, expression in queries:
            for channel in query["channels"]:
                m = expression.search(channels[channel])
                if m:
                    context = channels[channel][max(0, m.start()-100):m.end()+140]
                    hits.append({"label": query["label"], "channel": channel,
                                 "match": m.group(0), "context": context})
        matched[record] = hits
    rows.append({"path": "docs/" + relative, "Git_blob": blob, "Git_mode": entry["mode"],
                 "bytes": len(body), "SHA256": digest(body),
                 "body_reference": {"path": ref["path"], "bytes": len(body), "SHA256": digest(body),
                                    "filesystem_mode": format(stat.S_IMODE(Path(ref["path"]).stat().st_mode), "04o")},
                 "UTF8_decoding_error": decoding_error,
                 "title": " ".join(tags.title_parts).strip(), "h1_text": " ".join(tags.h1s).strip(),
                 "ids": tags.ids, "matched_queries": matched})
candidates = {str(t["record_id"]): [x["path"] for x in rows if x["matched_queries"][str(t["record_id"])]]
              for t in plan["targets"]}
out = {"scope": plan["search_scope"], "docs_tree": tree["sha"],
       "metadata_entries": len(entries), "tree_objects_authenticated": authenticated_trees,
       "whole_HTML_buffers_authenticated_and_searched": len(rows),
       "raw_body_fetches": 0, "old_helper_executions": [],
       "helper_sha256": digest(Path(__file__).read_bytes()),
       "TARGETS_sha256": digest((R / "TARGETS.json").read_bytes()),
       "candidate_paths_requiring_human_semantic_assessment": candidates,
       "correspondence_verdict": None, "history_or_global_absence_claim": False,
       "redirect_or_publication_authority": False, "rows": rows,
       "normalization_note": "Tag-stripped data includes script/style text; it is not rendered-visibility certification. Raw/decoded channels also search markup and attributes. No scripts evaluated."}
print(json.dumps(out, indent=2, ensure_ascii=False))
