"""One private overlay build. Standard-library data processing only; writes OWN only."""
import copy
import datetime
import hashlib
import html
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import stat
import xml.etree.ElementTree as ET

OWN = Path(__file__).resolve().parent
assert OWN.name == "gram-thompson-d4-overlay-sol-20261117"
P = OWN.parent.parent
W = Path("/Users/alec/Desktop/alec-dev/aleckriebel.com")
PUBLIC = W / "public"
BASE = "https://aleckriebel.com"
ADOPTIONS = [P / "verification" / name for name in (
    "root-binary-gram-locus-editorial-adoption-20261117.json",
    "root-thompson-cstar-editorial-adoption-20261117.json",
    "root-d4-canonical-potential-editorial-adoption-20261117.json")]
PAPERS = [
    {"id": "23318851", "slug": "binary-gram-locus-polynomial-obstruction", "writer": "binary-gram-locus-editorial-sol-20261117", "source_counts": (95, 16), "asset_dir": "zenodo-files", "pages": 5, "date": "2026-10-12", "date_label": "12 October 2026", "version_label": "Version 1.0.0", "source_pins": ("c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317", "ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8"), "page_sha": "53e6593171f35b50514c9b1797901775a2272afc09fe0f07819c5465129feedc"},
    {"id": "23204212", "slug": "thompson-reduced-cstar-consequences", "writer": "thompson-cstar-editorial-corrected-v2-sol-20261117", "source_counts": (55, 14), "asset_dir": "zenodo-files", "pages": 4, "date": "2026-10-06", "date_label": "6 October 2026", "version_label": "Zenodo display edition: v1", "source_pins": ("b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5", "afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be"), "page_sha": "1885856dbf199b10703652fb9a07d55119c2c02ae2d3f081d441fd68892514e3"},
    {"id": "23439776", "slug": "d4-canonical-potential-exponent-converse", "writer": "d4-canonical-potential-editorial-v2-sol-20261117", "source_counts": (72, 7), "asset_dir": "assets", "pages": 5, "date": "2026-10-17", "date_label": "17 October 2026", "version_label": "Version 1.0", "source_pins": ("e95d8717aee6b39ba23b73d85462a20340c823ff3ee5a09bc66470775a5b5a03", "d3041e24a1c481a2c4c9657edfa65a94c7db239be603d7b2a00c7fc0f560f6c0"), "page_sha": "24bff5057a9f09fdfbc85020bb48c676c7940bf622cac8728dfb0dcb0f47ea0a"},
]
ROOT_PINS = {
    "23318851": ("d6d6efca566214ccb39080bd7160c3437ede74c026150bc74e149d6878867d5f", "ef479bc20bdcd8d789736abd17b9999184fee354b3a15d41bc53a6c872b807d9"),
    "23204212": ("71136fd6de5610566ccffa7142a2ecabac093e33bad245e06eb7a3d456d85501", "cf26226d4c236473c5cb75ede27c50f77e486761df16a624d39cf26abdbb797c"),
    "23439776": ("4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62", "d6a171c2f2a3b5480bd5bdc71e4c9fcb63bb2130bea2524e7e9df3cb9f6c6590"),
}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(262144), b""):
            digest.update(block)
    return digest.hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def save_json(name, value):
    target = OWN / name
    assert not target.exists(), str(target)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

def object_meta(path, rel):
    info = path.lstat()
    assert stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), str(path)
    result = {"path": rel, "mode": oct(stat.S_IMODE(info.st_mode)), "mtime_ns": info.st_mtime_ns,
              "ctime_ns": info.st_ctime_ns, "hidden": any(x.startswith(".") for x in Path(rel).parts if x != ".")}
    if stat.S_ISDIR(info.st_mode):
        result.update(kind="directory", empty=not any(path.iterdir()))
    else:
        result.update(kind="file", bytes=info.st_size, SHA256=file_sha(path), empty=info.st_size == 0)
    return result

def tree(root, expected=None):
    assert root.resolve() == root
    paths = [root] + sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix())
    entries = [object_meta(path, "." if path == root else path.relative_to(root).as_posix()) for path in paths]
    files = sum(e["kind"] == "file" for e in entries)
    dirs = sum(e["kind"] == "directory" for e in entries) - 1
    if expected is not None:
        assert (files, dirs) == expected, (str(root), files, dirs, expected)
    return {"root": str(root), "files": files, "child_directories": dirs, "entries": entries}

def packet_path(text):
    candidate = P / text if text.startswith("verification/") else P / "verification" / text
    assert candidate.parent == P / "verification"
    return candidate

def fixed_inputs():
    result = {"sources": {}, "accepted_packets": {}, "root_inputs": {}}
    for paper in PAPERS:
        source = P / "papers" / paper["id"] / "sources"
        result["sources"][paper["id"]] = tree(source, paper["source_counts"])
        for name, expected in zip(("SOURCE_FINAL.json", "SOURCE_MANIFEST.json"), paper["source_pins"]):
            assert file_sha(source / name) == expected
        root_paths = (P / "papers" / paper["id"] / "reviews/root-continuation-20261117/ROOT_REVIEW.md",
                      P / "verification" / ("root-clearance-" + paper["id"] + "-20261117.json"))
        for path, expected in zip(root_paths, ROOT_PINS[paper["id"]]):
            assert file_sha(path) == expected
            result["root_inputs"][str(path)] = object_meta(path, path.name)
    for adoption_path in ADOPTIONS:
        adoption = load(adoption_path)
        assert adoption["follow_up"] is None and adoption["status"].startswith("ACCEPTED_")
        result["root_inputs"][str(adoption_path)] = object_meta(adoption_path, adoption_path.name)
        for packet in adoption["packets"]:
            root = packet_path(packet["path"])
            result["accepted_packets"][str(root)] = tree(root, (packet["files"], packet["child_directories"]))
            if "external_controls" in packet:
                for name, expected in packet["external_controls"].items():
                    assert file_sha(root / name) == expected, (root, name)
            else:
                assert file_sha(root / "FINAL_MANIFEST.json") == packet["manifest_SHA256"]
                candidates = [root / name for name in ("FINAL_SEAL.json", "FINAL.json") if (root / name).is_file()]
                assert sum(file_sha(path) == packet["terminal_SHA256"] for path in candidates) == 1
    assert len(result["accepted_packets"]) == 9
    assert file_sha(ADOPTIONS[2]) == "4eb74780ca57774a77f0c8c0bbd116806bdb4ad36c1696714aa1c8e03a83c5b9"
    return result

def website():
    public = tree(PUBLIC, (803, 387))
    assert public["entries"][0]["mode"] == "0o750"
    assert (W / ".git/HEAD").read_bytes() == b"ref: refs/heads/master\n"
    assert (W / ".git/refs/heads/master").read_text().strip() == "4cc09d6bbbad61aa11077c5002cf84a1e93b1344"
    assert file_sha(W / ".git/index") == "6b76dc0a4e7a631587aec1c081057479883573f7ff284dfc88b5adad02317179"
    native = {}
    for name in (".git/HEAD", ".git/index", ".git/config", ".git/config.worktree", ".git/packed-refs",
                 ".git/shallow", "firebase.json", ".firebaserc", ".gitignore"):
        path = W / name
        native[name] = object_meta(path, name) if path.exists() else {"path": name, "absent": True}
    native["local_heads"] = tree(W / ".git/refs/heads")
    assert file_sha(PUBLIC / "research/index.html") == "9a155532097fdd8c027e5feaa28eb2955dbe17afd161d6c164ac1ebe6643ef77"
    assert file_sha(PUBLIC / "research/sitemap.xml") == "3058b3cbe0fcae4012ac3c8dce078f92185d5781beae2a1af37df1a63abe12ca"
    assert file_sha(PUBLIC / "research/research.css") == "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a"
    return {"public": public, "native_and_configuration": native}

class Tags(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.events = []
    def handle_starttag(self, tag, attrs):
        self.events.append(["start", tag, list(attrs)])
        if tag == "meta":
            values = dict(attrs)
            key = values.get("name", values.get("property"))
            if key is not None:
                assert key not in self.meta
                self.meta[key] = values.get("content")
    def handle_endtag(self, tag):
        self.events.append(["end", tag])
    def handle_data(self, data):
        self.events.append(["data", data])

def typed_html(raw):
    parser = Tags()
    parser.feed(raw.decode())
    return parser.events

SCRIPT = re.compile(rb'<script type="application/ld\+json">(.*?)</script>', re.S)

def json_items(script):
    decoder = json.JSONDecoder()
    marker = '"itemListElement"'
    assert script.count(marker) == 1
    start = script.index("[", script.index(marker) + len(marker))
    items, end = decoder.raw_decode(script, start)
    pos = start + 1
    records = []
    for expected in items:
        while script[pos].isspace():
            pos += 1
        item_start = pos
        item, pos = decoder.raw_decode(script, pos)
        assert item == expected
        records.append({"raw": script[item_start:pos], "typed": item, "position": item["position"],
                        "character_start": item_start, "character_end": pos})
        while script[pos].isspace():
            pos += 1
        if script[pos] == ",":
            pos += 1
    return start, end, records

def xml_typed(node):
    return {"tag": node.tag, "attributes_in_order": list(node.attrib.items()), "text": node.text,
            "tail": node.tail, "children": [xml_typed(child) for child in node]}

def patch(buffer, old, new, label, scope, changes):
    old = old.encode() if isinstance(old, str) else old
    new = new.encode() if isinstance(new, str) else new
    assert old and buffer.count(old) == 1, (label, "old-span count", buffer.count(old))
    start = buffer.index(old)
    if scope == "HEAD":
        assert buffer.index(b"<head>") < start and start + len(old) <= buffer.index(b"</head>")
    changed = buffer[:start] + new + buffer[start + len(old):]
    assert changed[:start] + old + changed[start + len(new):] == buffer
    changes.append({"label": label, "scope": scope, "start_byte": start,
                    "old": old.decode(), "new": new.decode(), "before_SHA256": sha(buffer),
                    "after_SHA256": sha(changed), "single_step_reverse_exact": True})
    return changed

def replay(original, candidate, changes):
    forward = original
    for change in changes:
        start, old, new = change["start_byte"], change["old"].encode(), change["new"].encode()
        assert sha(forward) == change["before_SHA256"] and forward[start:start + len(old)] == old
        forward = forward[:start] + new + forward[start + len(old):]
        assert sha(forward) == change["after_SHA256"]
    assert forward == candidate
    reverse = candidate
    for change in reversed(changes):
        start, old, new = change["start_byte"], change["old"].encode(), change["new"].encode()
        assert reverse[start:start + len(new)] == new and sha(reverse) == change["after_SHA256"]
        reverse = reverse[:start] + old + reverse[start + len(new):]
        assert sha(reverse) == change["before_SHA256"]
    assert reverse == original

def write_overlay(relative, data, mode):
    target = OWN / "overlay" / relative
    assert not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    for directory in (OWN / "overlay", OWN / "overlay/research", target.parent):
        os.chmod(directory, 0o755)
    target.write_bytes(data)
    os.chmod(target, int(mode, 8))
    return {"path": relative, "bytes": len(data), "SHA256": sha(data), "mode": mode}

started = utc()
fixed_before = fixed_inputs()
web_before = website()
save_json("FIXED_INPUTS_BEFORE.json", {"UTC": started, **fixed_before})
save_json("WEBSITE_BEFORE.json", {"UTC": started, **web_before})
try:
    assert not (OWN / "overlay").exists() and not (OWN / "before").exists()
    old_index = (PUBLIC / "research/index.html").read_bytes()
    old_xml = (PUBLIC / "research/sitemap.xml").read_bytes()
    assert (len(old_index), len(old_xml)) == (104569, 17182)
    (OWN / "before").mkdir()
    (OWN / "before/index.html").write_bytes(old_index)
    (OWN / "before/sitemap.xml").write_bytes(old_xml)
    matches = list(SCRIPT.finditer(old_index))
    assert len(matches) == 1
    old_collection_raw = matches[0].group(1).decode()
    old_collection = json.loads(old_collection_raw)
    assert old_collection["mainEntity"]["numberOfItems"] == 133
    array_start, array_end, old_json_records = json_items(old_collection_raw)
    assert [r["position"] for r in old_json_records] == list(range(1, 134))
    old_units = list(re.finditer(rb"<li\b[^>]*>.*?</li>", old_index, re.S))
    assert len(old_units) == 133 and old_index.count(b"</ul>") == 1
    xml_root = ET.fromstring(old_xml)
    old_xml_nodes = list(xml_root)
    old_xml_units = list(re.finditer(rb"<url(?:\s[^>]*)?>.*?</url>", old_xml, re.S))
    assert len(old_xml_nodes) == len(old_xml_units) == 134
    old_locs = [node.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text for node in old_xml_nodes]
    public_paths = [entry["path"].casefold() for entry in web_before["public"]["entries"]]
    new_items, new_list_units, new_xml_units, activations, targets, projected_pages = [], [], [], [], [], []
    for number, paper in enumerate(PAPERS, 134):
        slug = paper["slug"]
        route = "/research/" + slug + "/"
        canonical = BASE + route
        for path in public_paths:
            assert not (path == "research/" + slug.casefold() or path.startswith("research/" + slug.casefold() + "/")
                        or path in {"research/" + slug.casefold() + ".html", "research/" + slug.casefold() + ".htm"}), ("route collision", slug, path)
        assert canonical.casefold() not in [r["typed"]["url"].casefold() for r in old_json_records]
        assert canonical.casefold() not in [url.casefold() for url in old_locs]
        assert slug.casefold().encode() not in old_index.lower()
        writer = P / "verification" / paper["writer"]
        model = load(writer / "MODEL.json")
        assert model["follow_up"] is None and model["publication_authority"] is False
        source_page = (writer / "private-page/index.html").read_bytes()
        assert sha(source_page) == paper["page_sha"]
        parser = Tags()
        parser.feed(source_page.decode())
        title, description = model["title"], parser.meta["description"]
        native_assets = model["native_assets_in_original_order"]
        names = [asset["native_filename"] for asset in native_assets]
        pdfs = [name for name in names if name.endswith(".pdf")]
        assert len(pdfs) == 1
        pdf = pdfs[0]
        data, changes = source_page, []
        robot = re.search(rb'<meta name="robots" content="[^"]+">', data).group()
        data = patch(data, robot, b'<meta name="robots" content="index,follow">', "candidate robots", "HEAD", changes)
        old_pdf_meta = re.search(rb'<meta name="citation_pdf_url" content="[^"]+">', data).group()
        data = patch(data, old_pdf_meta, '<meta name="citation_pdf_url" content="' + canonical + pdf + '">', "absolute candidate Scholar PDF", "HEAD", changes)
        css_old = b'<link rel="stylesheet" href="research.css">'
        assert b'rel="canonical"' not in source_page and 'og:url' not in parser.meta
        lines = ['<link rel="canonical" href="' + canonical + '">']
        if "og:type" not in parser.meta:
            lines += ['<meta property="og:type" content="article">', '<meta property="og:title" content="' + html.escape(title, quote=True) + '">', '<meta property="og:description" content="' + html.escape(description, quote=True) + '">']
        lines += ['<meta property="og:url" content="' + canonical + '">', '<meta property="og:site_name" content="Alec Kriebel">', '<link rel="stylesheet" href="/research/research.css">']
        data = patch(data, css_old, "\n".join(lines), "candidate canonical/OG/shared CSS", "HEAD", changes)
        scripts = list(SCRIPT.finditer(data))
        assert len(scripts) == 1
        old_schema = json.loads(scripts[0].group(1))
        new_schema = copy.deepcopy(old_schema)
        new_schema["url"] = canonical
        assert [item["name"] for item in new_schema["encoding"]] == names
        for encoding in new_schema["encoding"]:
            encoding["contentUrl"] = canonical + encoding["name"]
        restore = copy.deepcopy(new_schema)
        restore["url"] = old_schema["url"]
        for restored, original in zip(restore["encoding"], old_schema["encoding"]):
            restored["contentUrl"] = original["contentUrl"]
        assert restore == old_schema
        new_script = '<script type="application/ld+json">' + json.dumps(new_schema, ensure_ascii=False) + '</script>'
        data = patch(data, scripts[0].group(), new_script, "only schema URL/encoding URLs semantically changed", "HEAD", changes)
        marker = b'<p class="entry-meta">Private editorial draft</p>\n'
        expected_body = source_page[source_page.index(b"<body>"):]
        if paper["id"] == "23318851":
            assert expected_body.count(marker) == 1
            data = patch(data, marker, b"", "remove authorized Gram private marker plus LF", "BODY", changes)
            expected_body = expected_body.replace(marker, b"", 1)
        else:
            assert marker not in source_page
        assert data[data.index(b"<body>"):] == expected_body
        replay(source_page, data, changes)
        candidate_parser = Tags()
        candidate_parser.feed(data.decode())
        for key in ("citation_abstract", "citation_publication_date", "citation_version"):
            assert candidate_parser.meta.get(key) == parser.meta.get(key)
        assert candidate_parser.meta["citation_pdf_url"] == canonical + pdf
        if paper["id"] == "23204212":
            assert model["native_version"] is None and "citation_version" not in candidate_parser.meta
            assert b"complex linear span" in expected_body
        html_relative = "research/" + slug + "/index.html"
        targets.append({"action": "A", **write_overlay(html_relative, data, oct(stat.S_IMODE((writer / "private-page/index.html").stat().st_mode)))})
        activations.append({"record": paper["id"], "source_path": str(writer / "private-page/index.html"), "source_SHA256": sha(source_page), "candidate_path": html_relative, "candidate_SHA256": sha(data), "candidate_canonical_private_until_deploy": canonical, "literal_changes": changes, "whole_forward_exact": True, "whole_reverse_exact": True, "BODY_exact_except_sole_authorized_Gram_marker": True})
        for name in names + ["citation.bib"]:
            asset_path = writer / "private-page" / name
            payload = asset_path.read_bytes()
            if name != "citation.bib":
                native_path = P / "papers" / paper["id"] / "sources" / paper["asset_dir"] / name
                assert payload == native_path.read_bytes()
                item = next(item for item in native_assets if item["native_filename"] == name)
                assert len(payload) == item["bytes"] and sha(payload) == item.get("SHA256", item.get("sha256"))
            targets.append({"action": "A", **write_overlay("research/" + slug + "/" + name, payload, oct(stat.S_IMODE(asset_path.stat().st_mode)))})
        new_items.append({"@type": "ListItem", "position": number, "url": canonical, "name": title})
        esc = lambda value: html.escape(value, quote=True)
        unit = '<li><a href="' + route + '">' + esc(title) + '</a><br><span class="entry-meta"><time datetime="' + paper["date"] + '">' + paper["date_label"] + '</time> · ' + paper["version_label"] + ' · Unrefereed, AI-assisted preprint</span><p>' + esc(description) + '</p><p><a href="' + route + pdf + '">PDF (' + str(paper["pages"]) + ' pages)</a> · <a href="https://doi.org/10.5281/zenodo.' + paper["id"] + '">Zenodo</a></p></li>'
        new_list_units.append(unit)
        new_xml_units.append('<url><loc>' + canonical + '</loc><lastmod>2026-11-17</lastmod></url>\n')
        projected_pages.append({"record": paper["id"], "route": route, "candidate_canonical": canonical, "native_publication_date": paper["date"], "native_version": model["native_version"], "PDF_pages": paper["pages"], "native_assets_in_original_order": names, "page_publication_date": None, "AA": None, "redirect": None, "follow_up": None, "private_stage_only": True})
    index_changes = []
    new_array = old_collection_raw[array_start:array_end - 1] + ", " + ", ".join(json.dumps(item, ensure_ascii=False) for item in new_items) + "]"
    new_collection_raw = old_collection_raw[:array_start] + new_array + old_collection_raw[array_end:]
    assert new_collection_raw.count('"numberOfItems": 133') == 1
    new_collection_raw = new_collection_raw.replace('"numberOfItems": 133', '"numberOfItems": 136', 1)
    new_index = patch(old_index, matches[0].group(), '<script type="application/ld+json">' + new_collection_raw + '</script>', "Collection count plus three appended JSON items; original lexemes retained", "HEAD", index_changes)
    new_index = patch(new_index, b"</ul>", ("\n".join(new_list_units) + "\n</ul>").encode(), "append only three complete listing units", "LIST", index_changes)
    replay(old_index, new_index, index_changes)
    new_collection = json.loads(new_collection_raw)
    _, _, new_json_records = json_items(new_collection_raw)
    assert new_collection["mainEntity"]["numberOfItems"] == 136
    assert new_collection["mainEntity"]["itemListElement"][:133] == old_collection["mainEntity"]["itemListElement"]
    assert [r["raw"] for r in new_json_records[:133]] == [r["raw"] for r in old_json_records]
    assert [r["position"] for r in new_json_records] == list(range(1, 137))
    new_units = list(re.finditer(rb"<li\b[^>]*>.*?</li>", new_index, re.S))
    assert len(new_units) == 136 and [m.group() for m in new_units[:133]] == [m.group() for m in old_units]
    xml_changes = []
    new_xml = patch(old_xml, b"</urlset>", ("".join(new_xml_units) + "</urlset>").encode(), "append only three complete sitemap URLs", "XML", xml_changes)
    replay(old_xml, new_xml, xml_changes)
    new_xml_root = ET.fromstring(new_xml)
    assert xml_root.tag == new_xml_root.tag and xml_root.attrib == new_xml_root.attrib and xml_root.text == new_xml_root.text
    assert len(new_xml_root) == 137 and [xml_typed(n) for n in list(new_xml_root)[:134]] == [xml_typed(n) for n in old_xml_nodes]
    new_xml_raw = list(re.finditer(rb"<url(?:\s[^>]*)?>.*?</url>", new_xml, re.S))
    assert [m.group() for m in new_xml_raw[:134]] == [m.group() for m in old_xml_units]
    for relative, payload in (("research/index.html", new_index), ("research/sitemap.xml", new_xml)):
        targets.append({"action": "M", **write_overlay(relative, payload, oct(stat.S_IMODE((PUBLIC / relative).stat().st_mode)))})
    assert len(targets) == 15 and sum(t["action"] == "A" for t in targets) == 13
    assert len({t["path"].casefold() for t in targets}) == 15
    content_fields = lambda item: {k: item[k] for k in ("bytes", "SHA256", "mode")}
    baseline_files = {e["path"]: content_fields(e) for e in web_before["public"]["entries"] if e["kind"] == "file"}
    baseline_dirs = {e["path"]: e["mode"] for e in web_before["public"]["entries"] if e["kind"] == "directory"}
    projected_files, projected_dirs = copy.deepcopy(baseline_files), dict(baseline_dirs)
    for target in targets:
        assert (target["path"] in baseline_files) == (target["action"] == "M")
        projected_files[target["path"]] = content_fields(target)
    for paper in PAPERS:
        name = "research/" + paper["slug"]
        assert name not in projected_dirs
        projected_dirs[name] = "0o755"
    target_names = {t["path"] for t in targets}
    assert all(projected_files[name] == item for name, item in baseline_files.items() if name not in target_names)
    assert all(projected_dirs[name] == mode for name, mode in baseline_dirs.items())
    assert len(projected_files) == 816 and len(projected_dirs) - 1 == 390
    overlay_paths = list((OWN / "overlay").rglob("*"))
    assert (sum(p.is_file() for p in overlay_paths), sum(p.is_dir() for p in overlay_paths)) == (15, 4)
    assert not any(path.name == "research.css" for path in (OWN / "overlay").rglob("*"))
    save_json("TARGETS.json", {"scope": "Private physical overlay only, not a complete public tree", "changes": targets, "A": 13, "M": 2, "total": 15, "new_public_directories": ["research/" + p["slug"] for p in PAPERS]})
    save_json("PAGE_ACTIVATIONS.json", activations)
    save_json("PROJECTED_PAGE_METADATA.json", projected_pages)
    save_json("INDEX_PRESERVATION.json", {"old_count": 133, "new_count": 136, "complete_prefix_raw_typed_positions_exact": True, "old_units": [{"position": i + 1, "start_byte": unit.start(), "end_byte": unit.end(), "raw": unit.group().decode(), "typed_HTML": typed_html(unit.group()), "JSON": old_json_records[i]} for i, unit in enumerate(old_units)], "new_units": [{"raw": raw, "typed_HTML": typed_html(raw.encode()), "JSON": item} for raw, item in zip(new_list_units, new_items)], "whole_forward_reverse_exact": True, "literal_changes": index_changes})
    save_json("SITEMAP_PRESERVATION.json", {"old_count": 134, "new_count": 137, "complete_raw_and_full_parsed_prefix_exact": True, "old_root_tag": xml_root.tag, "old_root_attributes": list(xml_root.attrib.items()), "old_root_text": xml_root.text, "old_units": [{"position": i + 1, "start_byte": raw.start(), "end_byte": raw.end(), "raw": raw.group().decode(), "full_parsed": xml_typed(node)} for i, (raw, node) in enumerate(zip(old_xml_units, old_xml_nodes))], "new_units": [xml_typed(node) for node in list(new_xml_root)[134:]], "literal_changes": xml_changes, "whole_forward_reverse_exact": True})
    save_json("PUBLIC_PROJECTION.json", {"physical_full_public_copy": False, "basis": "Whole baseline file metadata map plus exact15overlay changes", "baseline_files": 803, "baseline_child_directories": 387, "projected_files": 816, "projected_child_directories": 390, "public_root_mode": baseline_dirs["."], "files": projected_files, "directories_including_root": projected_dirs, "all_untargeted_files_modes_directories_exact": True, "candidate_publication_authority": False})
finally:
    fixed_after = fixed_inputs()
    web_after = website()
    fixed_exact, web_exact = fixed_after == fixed_before, web_after == web_before
    save_json("FIXED_INPUTS_AFTER.json", {"UTC": utc(), **fixed_after, "before_after_exact": fixed_exact})
    save_json("WEBSITE_AFTER.json", {"UTC": utc(), **web_after, "before_after_exact": web_exact})
    assert fixed_exact and web_exact, "Protected fixed inputs or native website changed"

result = {"UTC_start": started, "UTC_end": utc(), "status": "PRIVATE_OVERLAY_PREPARED_PENDING_INDEPENDENT_AUDIT", "builder_attempts": 1, "repair_or_retry_count": 0, "overlay_files": 15, "A": 13, "M": 2, "whole_public_projection_files": 816, "whole_public_projection_child_directories": 390, "listing_articles": 136, "sitemap_URLs": 137, "all_133_HTML_JSON_old_units_and_134_XML_units_preserved": True, "fixed_inputs_and_W_native_public_configuration_before_after_exact": True, "whole_public_or_W_copies": 0, "scientific_source_oldhelper_Git_network_Sheet_server_install_deploy_operations": 0, "page_publication_date": None, "AA": None, "redirect": None, "follow_up": None, "publication_or_future_action_authority": False}
save_json("BUILD_RESULT.json", result)
print(json.dumps(result, indent=2))
