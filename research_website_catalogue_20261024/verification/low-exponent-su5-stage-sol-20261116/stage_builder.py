#!/usr/bin/env python3
"""MIT. Explicit private build/static validation only; default performs no writes."""
import hashlib
import html
import json
import re
import stat
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path("/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/low-exponent-su5-stage-sol-20261116")
P = R.parent.parent
W = Path("/Users/alec/Desktop/alec-dev/aleckriebel.com")
M = Path("/Users/alec/Documents/Math")
ORIGIN = "https://aleckriebel.com/"
NOW = "2026-11-17"
def sha(data):
    return hashlib.sha256(data).hexdigest()
def pin(path, name=None):
    path = Path(path)
    info = path.lstat()
    assert stat.S_ISREG(info.st_mode), ("not regular", str(path))
    data = path.read_bytes()
    return {"path": name if name is not None else str(path), "bytes": len(data),
            "sha256": sha(data), "mode": format(stat.S_IMODE(info.st_mode), "04o")}
def tree(root):
    assert root.is_dir() and not root.is_symlink()
    files, dirs = [], [{"path": ".", "mode": format(stat.S_IMODE(root.lstat().st_mode), "04o")}]
    for path in sorted(root.rglob("*")):
        kind, rel = path.lstat().st_mode, path.relative_to(root).as_posix()
        if stat.S_ISREG(kind):
            files.append(pin(path, rel))
        elif stat.S_ISDIR(kind):
            dirs.append({"path": rel, "mode": format(stat.S_IMODE(kind), "04o")})
        else:
            raise AssertionError(("special object", str(path)))
    return {"root": str(root), "files": files, "directories": dirs}
def require_pin(path, size, digest):
    out = pin(path)
    assert out["bytes"] == size and out["sha256"] == digest, str(path)
    return out
def exact_manifest(root, count, child_dirs, manifest_name, controls):
    snap = tree(root)
    meta = json.loads((root / manifest_name).read_text())
    assert len(snap["files"]) == count and len(snap["directories"]) == child_dirs + 1
    actual = {x["path"]: x for x in snap["files"]}
    assert set(actual) == {x["path"] for x in meta["files"]} | set(controls)
    for row in meta["files"]:
        if row["path"] in controls:
            continue
        a = actual[row["path"]]
        assert a["bytes"] == row["bytes"]
        assert a["sha256"] == row.get("sha256", row.get("SHA256"))
        assert int(a["mode"], 8) == int(row["mode"], 8)
    expected_dirs = {x["path"]: int(x["mode"], 8) for x in meta["directories"]}
    if "." not in expected_dirs:
        expected_dirs["."] = 0o755
    assert {x["path"]: int(x["mode"], 8) for x in snap["directories"]} == expected_dirs
    return snap
def guard():
    public = tree(W / "public")
    assert len(public["files"]) == 747 and len(public["directories"]) == 367
    stores = [x for x in public["files"] if Path(x["path"]).name == ".DS_Store"]
    assert len(stores) == 17
    assert (W / ".git/HEAD").read_text() == "ref: refs/heads/master\n"
    assert (W / ".git/refs/heads/master").read_text().strip() == "3a6e0709bda08d8c913078b4eaa4e591fed7f3c6"
    wi = require_pin(W / ".git/index", 9054454, "71ea221a2bcd9f3919f430d785bbcb940ef2348d9596932778568940fc59d14c")
    header = (W / ".git/index").read_bytes()[:12]
    magic, version, records = struct.unpack(">4sII", header)
    assert magic == b"DIRC" and version in (2, 3, 4)
    assert (M / ".git/HEAD").read_text() == "ref: refs/heads/main\n"
    packed = (M / ".git/packed-refs").read_text().splitlines()
    assert "a4ce3c37dad209339e490d18dcced6c48cf912d2 refs/heads/main" in packed
    mi = require_pin(M / ".git/index", 25854746, "91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11")
    required = [W / ".git/HEAD", W / ".git/refs/heads/master", W / ".git/config",
                M / ".git/HEAD", M / ".git/packed-refs", M / ".git/config"]
    absent = [M / ".git/refs/heads/main", M / ".git/config.worktree"]
    assert all(not x.exists() and not x.is_symlink() for x in absent)
    return {"public": public, "native_indices": [wi, mi],
            "W_index_header": {"version": version, "records": records},
            "raw_HEAD_ref_config_guards": [pin(x) for x in required],
            "explicit_absent_paths": [str(x) for x in absent],
            "DS_Store_rows_included_in_complete_public_guard": stores}
def inputs(contract):
    authority = require_pin(Path(contract["authority"]["path"]), 2994,
        "0197a043987c861d8f26e0f0e4882b08868e03a12786f0411989a6cd8c216cba")
    writers = []
    for spec in contract["writer_inputs"]:
        root = P / "verification" / spec["folder"]
        assert pin(root / "FINAL.json")["sha256"] == spec["FINAL"]
        assert pin(root / "OWNED_MANIFEST.json")["sha256"] == spec["manifest"]
        writers.append(exact_manifest(root, spec["files"], 0, "OWNED_MANIFEST.json", ["FINAL.json", "OWNED_MANIFEST.json"]))
    original_ref = json.loads((P / "verification" / contract["writer_inputs"][0]["folder"] / "ORIGINAL_REFERENCE.json").read_text())
    original = tree(Path(original_ref["original_root"]))
    assert len(original["files"]) == 22 and len(original["directories"]) == 1
    assert [{k: x[k] for k in ("path", "bytes", "sha256", "mode")} for x in original_ref["files"]] == original["files"]
    sources = []
    specs = [(23331709, 120, 17, "bb80fc71825c75c727cd9f842d6fe38759cdfd6c1cd2d02c5f6ac9b4aa0444c6", "c2fc40cc1154d3aa47ab74e9c7dcfffc202c7238864ff4b86e1ffad094974c25"),
             (23174156, 186, 18, "fdff8a4219c2b4b72f7395079fab6945ab2736784c712a359015c08ff40a35dc", "153bc99484999f9e5bca8623ee88e9935cf2c42557626112161f8f372a5a4827")]
    for record, count, dirs, manifest_hash, final_hash in specs:
        root = P / "papers" / str(record) / "sources"
        assert pin(root / "SOURCE_MANIFEST.json")["sha256"] == manifest_hash
        assert pin(root / "SOURCE_FINAL.json")["sha256"] == final_hash
        sources.append(exact_manifest(root, count, dirs, "SOURCE_MANIFEST.json", ["SOURCE_MANIFEST.json", "SOURCE_FINAL.json"]))
    return {"authority": authority, "writer_packets": writers,
            "original167_packet": original, "source_packets": sources}
def write_private(relative, data):
    dest = R / relative
    assert R in dest.parents and ".." not in Path(relative).parts
    for parent in [dest.parent] + list(dest.parent.parents):
        if parent == R.parent:
            break
        if parent.exists():
            assert parent.is_dir() and not parent.is_symlink()
    dest.parent.mkdir(parents=True, exist_ok=True)
    assert not dest.exists() and not dest.is_symlink(), str(dest)
    with dest.open("xb") as stream:
        stream.write(data)
    assert stat.S_IMODE(dest.lstat().st_mode) == 0o644
def save_json(name, data):
    write_private(name, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())
def ld_json(text):
    matches = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, re.S))
    assert len(matches) == 1
    return matches[0], json.loads(matches[0].group(1))
def main_bytes(text):
    found = re.findall(r'<main id="main">.*?</main>', text, re.S)
    assert len(found) == 1
    return found[0].encode()
def activate(spec):
    root = P / "verification" / spec["folder"]
    model = json.loads((root / "model.json").read_text())
    source = (root / "index.html").read_bytes().decode("utf-8")
    head = (root / "HEAD.html").read_bytes().decode("utf-8").rstrip("\n")
    assert source.count(head) == 1
    canonical = ORIGIN + "research/" + spec["slug"] + "/"
    assert model["proposed_canonical"] == model["deployment_metadata"]["canonical"] == canonical
    assert model["canonical"] is None and model["AA"] is None and not model["publication_authority"]
    assert model["native_order"] == spec["natives"]
    match, scholarly = ld_json(head)
    skey = "scholarly_schema" if "scholarly_schema" in model else "schema"
    assert scholarly == model[skey] and scholarly["abstract"] == model["abstract"]
    assert [x["contentUrl"] for x in scholarly["encoding"]] == spec["natives"]
    scholarly["url"], scholarly["@id"] = canonical, canonical + "#article"
    scholarly["mainEntityOfPage"] = canonical
    for row in scholarly["encoding"]:
        row["contentUrl"] = canonical + row["contentUrl"]
    new_head = head[:match.start(1)] + json.dumps(scholarly, ensure_ascii=False, indent=2) + head[match.end(1):]
    private = '<meta name="robots" content="noindex, nofollow">\n'
    assert new_head.count(private) == 1
    new_head = new_head.replace(private, "", 1)
    pdf = "pr95_note.pdf" if spec["record"] == 23174156 else "low_exponent_supersolvability.pdf"
    old_pdf = '<meta name="citation_pdf_url" content="' + pdf + '">'
    assert new_head.count(old_pdf) == 1
    new_head = new_head.replace(old_pdf, '<meta name="citation_pdf_url" content="' + canonical + pdf + '">', 1)
    assert 'rel="canonical"' not in new_head and 'property="og:url"' not in new_head
    added = '<link rel="canonical" href="' + canonical + '">\n<meta property="og:url" content="' + canonical + '">\n'
    new_head = new_head.replace("</head>", added + "</head>", 1)
    result = source.replace(head, new_head, 1)
    assert result[result.index("<body>"):] == source[source.index("<body>"):]
    assert main_bytes(result) == main_bytes(source) == (root / "MAIN.html").read_bytes().rstrip(b"\n")
    assert "noindex" not in result[:result.index("</head>")]
    assert 'href="../research.css"' in new_head and model["abstract"] in result
    expected_schema = model[skey].copy()
    expected_schema.update({"url": canonical, "@id": canonical + "#article", "mainEntityOfPage": canonical})
    expected_schema["encoding"] = [dict(row, contentUrl=canonical + row["contentUrl"]) for row in model[skey]["encoding"]]
    assert ld_json(new_head)[1] == expected_schema
    return result.encode(), model, {"record": spec["record"], "MAIN": {"bytes": len(main_bytes(result)), "sha256": sha(main_bytes(result))},
        "entire_body_exact": True, "full_abstract_exact": True, "metadata_only_activation": True, "canonical": canonical}
def raw_array_units(js):
    marker = '"itemListElement": ['
    assert js.count(marker) == 1
    start = js.index(marker) + len(marker) - 1
    array, consumed = json.JSONDecoder().raw_decode(js[start:])
    end = start + consumed - 1
    assert js[end] == "]" and isinstance(array, list)
    raw, pos = [], start + 1
    while pos < end:
        while pos < end and js[pos] in " \r\n\t,":
            pos += 1
        if pos == end:
            break
        value, size = json.JSONDecoder().raw_decode(js[pos:])
        raw.append(js[pos:pos + size])
        pos += size
    assert len(raw) == len(array)
    return array, raw, end
def aggregate_pages(models, specs):
    old = (W / "public/research/index.html").read_bytes().decode("utf-8")
    old_xml = (W / "public/research/sitemap.xml").read_bytes().decode("utf-8")
    require_pin(W / "public/research/index.html", 95089, "ccbfb37873ce08d8c70387f8465a7c625f4d5e9c5d08819b4f8525edf181322b")
    require_pin(W / "public/research/sitemap.xml", 15735, "7969e7019709275fd4c8af27a28e12f0315c4cd41cd5da0d59dca8e69ce57362")
    sm, data = ld_json(old)
    old_js = sm.group(1)
    items, raw, end = raw_array_units(old_js)
    assert len(items) == 121 and type(data["mainEntity"]["numberOfItems"]) is int
    assert data["mainEntity"]["numberOfItems"] == 121 and items == data["mainEntity"]["itemListElement"]
    assert [x["position"] for x in items] == list(range(1, 122))
    new_items, visible, xml_nodes = [], [], []
    for i, (model, spec) in enumerate(zip(models, specs), 122):
        url = ORIGIN + "research/" + spec["slug"] + "/"
        assert url not in [x["url"] for x in items]
        new_items.append({"@type": "ListItem", "position": i, "url": url, "name": model["title"]})
        pdf = "pr95_note.pdf" if spec["record"] == 23174156 else "low_exponent_supersolvability.pdf"
        date = "Manuscript dated 5 October 2026; current files 10 October 2026" if spec["record"] == 23174156 else "13 October 2026"
        item = '<li><a href="/research/' + spec["slug"] + '/">' + html.escape(model["title"]) + '</a><br><span class="entry-meta">' + date + ' · Unrefereed preprint</span><p>' + html.escape(model["description"]) + '</p><p><a href="/research/' + spec["slug"] + '/' + pdf + '">PDF</a> · <a href="https://doi.org/10.5281/zenodo.' + str(spec["record"]) + '">Zenodo</a></p></li>'
        visible.append(item)
        xml_nodes.append('<url><loc>' + url + '</loc><lastmod>' + NOW + '</lastmod></url>')
    insertion = ", " + ", ".join(json.dumps(x, ensure_ascii=False) for x in new_items)
    new_js = old_js[:end] + insertion + old_js[end:]
    assert new_js.count('"numberOfItems": 121') == 1
    new_js = new_js.replace('"numberOfItems": 121', '"numberOfItems": 123', 1)
    interim = old[:sm.start(1)] + new_js + old[sm.end(1):]
    visible_insert = "\n".join(visible) + "\n"
    assert interim.count("    </ul>") == 1 and old.count("<ul>") == 1
    new = interim.replace("    </ul>", visible_insert + "    </ul>", 1)
    new_sm, new_data = ld_json(new)
    new_array, new_raw, _ = raw_array_units(new_sm.group(1))
    old_lis = re.findall(r"<li\b[^>]*>.*?</li>", old.split("<ul>", 1)[1].split("</ul>", 1)[0], re.S)
    new_lis = re.findall(r"<li\b[^>]*>.*?</li>", new.split("<ul>", 1)[1].split("</ul>", 1)[0], re.S)
    assert len(old_lis) == 121 and len(new_lis) == 123 and new_lis[:121] == old_lis
    assert new_raw[:121] == raw and new_array[:121] == items and new_array[121:] == new_items
    assert new_data["mainEntity"]["numberOfItems"] == 123
    reversed_index = new.replace(visible_insert, "", 1).replace(new_js, old_js, 1)
    assert reversed_index.encode() == old.encode()
    old_nodes = re.findall(r"<url>.*?</url>", old_xml, re.S)
    assert len(old_nodes) == 122 and old_xml.count("</urlset>") == 1
    xml_insert = "\n".join(xml_nodes) + "\n"
    new_xml = old_xml.replace("</urlset>", xml_insert + "</urlset>", 1)
    assert re.findall(r"<url>.*?</url>", new_xml, re.S) == old_nodes + xml_nodes
    assert new_xml.replace(xml_insert, "", 1).encode() == old_xml.encode()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    parsed = ET.fromstring(new_xml)
    locs = [x.text for x in parsed.findall("s:url/s:loc", namespace)]
    assert len(locs) == len(set(locs)) == 124
    return new.encode(), new_xml.encode(), {"old_visible_units": 121, "new_visible_units": 123,
        "old_JSON_units": 121, "new_JSON_units": 123, "old_XML_units": 122, "new_XML_units": 124,
        "all_old_visible_raw_JSON_typed_units_XML_nodes_prefix_order_exact": True,
        "whole_index_and_sitemap_reversible_to_baseline_exact_bytes": True,
        "new_visible_units": visible, "new_JSON_typed_units": new_items, "new_XML_nodes": xml_nodes}
def build():
    assert Path(__file__).resolve() == R / "stage_builder.py"
    assert not (R / "public").exists()
    contract = json.loads((R / "CONTRACT.json").read_text())
    assert len(contract["targets"]) == 15 and len(set(contract["targets"])) == 15
    read = json.loads((R / "HELPER_READ.json").read_text())
    assert read["helper"]["sha256"] == pin(R / "stage_builder.py")["sha256"]
    assert read["entire_current_saved_body_personally_read_before_execution"] is True
    before, source_before = guard(), inputs(contract)
    require_pin(W / "public/research/research.css", 1170, "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a")
    payloads, models, page_checks = {}, [], []
    for spec in contract["writer_inputs"]:
        folder = W / "public/research" / spec["slug"]
        assert not folder.exists() and not folder.is_symlink()
        body, model, check = activate(spec)
        prefix = "research/" + spec["slug"] + "/"
        payloads[prefix + "index.html"] = body
        root = P / "verification" / spec["folder"]
        for name in spec["natives"] + ["citation.bib"]:
            payloads[prefix + name] = (root / name).read_bytes()
            assert pin(root / name)["mode"] == "0644"
        models.append(model)
        page_checks.append(check)
    payloads["research/index.html"], payloads["research/sitemap.xml"], agg = aggregate_pages(models, contract["writer_inputs"])
    assert set(payloads) == set(contract["targets"])
    for relative in contract["targets"]:
        write_private("public/" + relative, payloads[relative])
    candidate = tree(R / "public")
    assert len(candidate["files"]) == 15 and len(candidate["directories"]) == 4
    for row in candidate["files"]:
        assert (R / "public" / row["path"]).read_bytes() == payloads[row["path"]]
    current = {x["path"]: x for x in before["public"]["files"]}
    targets = []
    for relative in contract["targets"]:
        proposed = pin(R / "public" / relative, relative)
        targets.append({"target": relative, "operation": "MODIFY" if relative in current else "ADD",
                        "before": current.get(relative), "after": proposed})
        current[relative] = proposed
    assert len(current) == 760 and sum(x["operation"] == "ADD" for x in targets) == 13
    assert sum(x["operation"] == "MODIFY" for x in targets) == 2
    after, source_after = guard(), inputs(contract)
    assert before == after and source_before == source_after
    save_json("GUARDS_BEFORE.json", before)
    save_json("GUARDS_AFTER.json", after)
    save_json("INPUT_CUSTODY.json", {"before": source_before, "after_equal_before_complete_bytes_modes_extent": True})
    save_json("TARGET_PLAN.json", {"targets": targets, "public_before": 747, "public_after_if_installed": 760,
        "public_child_dirs_before": 366, "public_child_dirs_after_if_installed": 368,
        "only_candidate_files_15": True, "CSS_hosting_redirect_followup_changes": False,
        "production_install_deploy_authority": False})
    save_json("AGGREGATE_PROOF.json", agg)
    result = {"status": "PASS_PRIVATE_BUILD_AND_STATIC_VALIDATION", "records": contract["records"],
        "target_count": 15, "new_files": 13, "modified_aggregates": 2,
        "index_items_after": 123, "sitemap_nodes_after": 124, "public_files_after_if_installed": 760,
        "approved_entire_bodies_MAIN_abstracts_Bib_native_bytes_unchanged": True,
        "page_checks": page_checks, "aggregate_checks": agg,
        "all747_public_files_modes_topology_and_native_indices_HEAD_configs_unchanged": True,
        "all47_writer_plus_original22_and306_native_source_files_unchanged": True,
        "full_input_and_public_after_snapshots_equal_before": True,
        "no_Git_W_production_deploy_Sheet_network_CUA_science_or_old_helper_execution": True,
        "no_render_browser_live_reader_mobile_or_download_certification": True}
    save_json("BUILD_RESULTS.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if sys.argv[1:] != ["--build"]:
        print("Read-only default: explicit --build is required for private owned staging.")
    else:
        build()
