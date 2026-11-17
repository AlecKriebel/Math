"""One passive bounded factual-data check; no project imports or executions."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat

OWN = Path(__file__).resolve().parent
assert OWN.name == "d4-canonical-potential-editorial-fact-sol-20261117"
P = OWN.parent.parent
S = P / "papers/23439776/sources"
W = P / "verification/d4-canonical-potential-editorial-v2-sol-20261117"
OLD = P / "verification/d4-canonical-potential-editorial-sol-20261117"
REVIEW = P / "papers/23439776/reviews/root-continuation-20261117/ROOT_REVIEW.md"
CLEARANCE = P / "verification/root-clearance-23439776-20261117.json"
TEX = S / "published-source/container-001/tree/manuscript/main.tex"
PINS = {
    S / "SOURCE_FINAL.json": "e95d8717aee6b39ba23b73d85462a20340c823ff3ee5a09bc66470775a5b5a03",
    S / "SOURCE_MANIFEST.json": "d3041e24a1c481a2c4c9657edfa65a94c7db239be603d7b2a00c7fc0f560f6c0",
    W / "FINAL.json": "36eb02cf832f6734d40610a199f523b866e16505ee5e5d1ed252b63f2d27db4a",
    W / "FINAL_MANIFEST.json": "37b95cdf70d9cd8a4c7f521b6961bcbc52d4ff9726d2c5df7f2528bbda307a72",
    W / "MODEL.json": "b6143b34a0d45cf5b3a8c7af64887d8bbc03ccf6463355b372fba7a7056d8444",
    W / "private-page/index.html": "24bff5057a9f09fdfbc85020bb48c676c7940bf622cac8728dfb0dcb0f47ea0a",
    W / "ROOT_SETUP_DISPOSITION.json": "73d8bf89943fbeb721688157cb45a9484383161195d27963c54dc399041a94ea",
    OLD / "FINAL.json": "acb8535df05beb69ea59098769b2900f7f7cb8c12a311872a1e41fbfb9038ecd",
    OLD / "FINAL_MANIFEST.json": "4f71ba0ba35c9e56c40dd7cb1f7604a51a6362ed33ba73f67e04c3522aa9313a",
    OLD / "BUILDER.stderr.bin": "9360ef7e604fa529df9aae496fd0c6fa7f48aa4335faaf9b6f7f3892f3ae4773",
    TEX: "d15c70dcc7ee0744a6ea34cd72049abacddebb43dd7034becd8d6fa153d86c22",
    S / "record.response.body": "ba2d02f401bbfd7c482a0edaee717a170b6f65e0157f480f916c7fbe17762724",
    REVIEW: "4836979d83da2747da766a2defc76bc0e5bbd6b48b25025c0de434aefd580e62",
    CLEARANCE: "d6a171c2f2a3b5480bd5bdc71e4c9fcb63bb2130bea2524e7e9df3cb9f6c6590",
}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def write(name, value):
    target = OWN / name
    assert not target.exists(), str(target)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")

def record(path, relative):
    info = path.lstat()
    assert stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), str(path)
    value = {"path": relative, "mode": oct(stat.S_IMODE(info.st_mode)),
             "mtime_ns": info.st_mtime_ns, "ctime_ns": info.st_ctime_ns,
             "hidden": any(x.startswith(".") for x in Path(relative).parts if x != ".")}
    if stat.S_ISDIR(info.st_mode):
        value.update(kind="directory", empty=not any(path.iterdir()))
    else:
        data = path.read_bytes()
        value.update(kind="file", bytes=len(data), SHA256=sha(data),
                     MD5=hashlib.md5(data).hexdigest(), empty=not data)
    return value

def snapshot():
    result = {"trees": {}, "specific_root_inputs": {}}
    for label, root, expected in (("source", S, (72, 7)), ("writer", W, (30, 1)), ("failed_original", OLD, (22, 0))):
        assert root.resolve() == root
        paths = [root] + sorted(root.rglob("*"), key=lambda p: p.relative_to(root).as_posix())
        entries = [record(p, "." if p == root else p.relative_to(root).as_posix()) for p in paths]
        files = sum(e["kind"] == "file" for e in entries)
        dirs = sum(e["kind"] == "directory" for e in entries) - 1
        assert (files, dirs) == expected, (label, files, dirs)
        result["trees"][label] = {"file_count": files, "child_directory_count": dirs, "entries": entries}
    for path in (REVIEW, CLEARANCE):
        result["specific_root_inputs"][str(path)] = record(path, path.name)
    for path, expected in PINS.items():
        assert sha(path.read_bytes()) == expected, ("external pin", str(path))
    return result

def compare_fields(actual, declared, label):
    for key, value in declared.items():
        if key == "path":
            assert actual["path"] == value
        elif key == "mode":
            assert int(actual["mode"], 8) == int(value, 8), (label, key)
        else:
            assert key in actual and actual[key] == value, (label, key)

def source_manifest(tree):
    manifest = load(S / "SOURCE_MANIFEST.json")
    actual = {e["path"]: e for e in tree["entries"]}
    files = {e["path"]: e for e in tree["entries"] if e["kind"] == "file"}
    dirs = {e["path"]: e for e in tree["entries"] if e["kind"] == "directory" and e["path"] != "."}
    assert manifest["schema"] == "opaque-native-source-manifest-v1"
    assert actual["."]["mode"] == manifest["root_mode"]
    assert manifest["ordinary_files_including_controls"] == 72 and manifest["child_directory_count"] == 7
    assert set(files) == set(manifest["actual_file_paths_including_controls"])
    terminals = {"SOURCE_FINAL.json", "SOURCE_MANIFEST.json"}
    assert set(manifest["root_controls_excluded_from_own_list"]) == terminals
    assert len(manifest["files"]) == 70
    assert {e["path"] for e in manifest["files"]} == set(files) - terminals
    assert {e["path"] for e in manifest["directories"]} == set(dirs)
    for entry in manifest["files"] + manifest["directories"]:
        compare_fields(actual[entry["path"]], entry, ("source", entry["path"]))
    final = load(S / "SOURCE_FINAL.json")
    for key in ("SOURCE_READY", "SOURCE_MANIFEST"):
        compare_fields(actual[final[key]["path"]], final[key], key)

def editorial_manifest(root, tree):
    manifest = load(root / "FINAL_MANIFEST.json")
    actual = {e["path"]: e for e in tree["entries"]}
    files = {e["path"] for e in tree["entries"] if e["kind"] == "file"}
    dirs = {e["path"] for e in tree["entries"] if e["kind"] == "directory" and e["path"] != "."}
    assert actual["."]["mode"] == manifest["root_mode"]
    assert manifest["file_count"] == tree["file_count"] and manifest["child_directory_count"] == tree["child_directory_count"]
    terminals = {"FINAL.json", "FINAL_MANIFEST.json"}
    assert {e["path"] for e in manifest["terminal_pair"]} == terminals
    assert set(manifest["payload_files"]) == files - terminals
    assert set(manifest["directories"]) == dirs
    for name, metadata in manifest["payload_files"].items():
        compare_fields(actual[name], metadata, (root.name, name))
    for name, mode in manifest["directories"].items():
        assert int(actual[name]["mode"], 8) == int(mode, 8)
    for entry in manifest["terminal_pair"]:
        assert entry["recursive_hash_excluded"] is True and root / entry["path"] in PINS
        compare_fields(actual[entry["path"]], {k: v for k, v in entry.items() if k != "recursive_hash_excluded"}, entry["path"])
    assert manifest["hidden_paths"] == sorted(e["path"] for e in tree["entries"] if e["hidden"])
    assert manifest["empty_files"] == sorted(e["path"] for e in tree["entries"] if e["kind"] == "file" and e["empty"])
    assert manifest["empty_directories"] == sorted(e["path"] for e in tree["entries"] if e["kind"] == "directory" and e["empty"])
    final = load(root / "FINAL.json")
    compare_fields(actual["FINAL_MANIFEST.json"], final["manifest"], "final manifest receipt")
    assert actual["FINAL.json"]["bytes"] == final["own_bytes"]
    assert actual["FINAL.json"]["mode"] == final["own_mode"]

class PageData(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.links = []
        self.anchors = []
        self.iframes = []
        self.tags = []
        self.scripts = []
        self.current_script = None
        self.abstract_open = False
        self.abstract = []
        self.files_section = False
        self.file_order = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "meta":
            key = values.get("name", values.get("property"))
            assert key not in self.meta
            self.meta[key] = values.get("content")
        if tag == "link":
            self.links.append(values)
        if tag == "a":
            self.anchors.append(values)
            if self.files_section and "download" in values and values.get("href") != "citation.bib":
                self.file_order.append(values["href"])
        if tag == "iframe":
            self.iframes.append(values)
        if tag == "script":
            assert self.current_script is None
            self.current_script = {"attrs": values, "text": []}
        if tag == "p" and values.get("id") == "manuscript-abstract":
            self.abstract_open = True
        if tag == "section" and values.get("aria-labelledby") == "files-heading":
            self.files_section = True
    def handle_endtag(self, tag):
        if tag == "script":
            self.scripts.append(self.current_script)
            self.current_script = None
        if tag == "p":
            self.abstract_open = False
        if tag == "section":
            self.files_section = False
    def handle_data(self, data):
        if self.current_script is not None:
            self.current_script["text"].append(data)
        if self.abstract_open:
            self.abstract.append(data)

started = utc()
before = snapshot()
write("CUSTODY_BEFORE.json", {"UTC": started, **before})
try:
    source_manifest(before["trees"]["source"])
    editorial_manifest(W, before["trees"]["writer"])
    editorial_manifest(OLD, before["trees"]["failed_original"])
    model = load(W / "MODEL.json")
    api = load(S / "record.response.body")
    clearance = load(CLEARANCE)
    assert clearance["status"] == "PASS_ORIGINAL_HISTORICAL_CANONICAL_W_COUNTEREXAMPLE"
    assert clearance["central_defect_or_unsupported_inference"] is None
    assert clearance["follow_up"] is None and clearance["no_formal_or_human_certificate"] is True
    assert api["id"] == 23439776 and model["record_id"] == "23439776"
    assert api["metadata"]["title"] == model["title"]
    assert api["doi"] == model["DOI"] == "10.5281/zenodo.23439776"
    assert api["metadata"]["version"] == model["native_version"] == "1.0"
    assert api["metadata"]["publication_date"] == model["native_publication_date"] == "2026-10-17"
    assert api["created"] == model["native_record_created"] and api["updated"] == model["native_record_updated"]
    assert api["metadata"]["license"]["id"] == "cc-by-4.0"
    tex = TEX.read_text()
    assert len(tex.splitlines()) == 343 and len(TEX.read_bytes()) == 15136
    literal = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
    abstract_model = model["abstract"]
    assert literal == abstract_model["literal_source_TeX_span"]
    replacements = [{"from": "$D_4$", "to": "D₄"}, {"from": "$22$", "to": "22"},
                    {"from": "$-2$", "to": "−2"}, {"from": "$\\{-1,0,1\\}$", "to": "{−1,0,1}"}]
    assert abstract_model["literal_rendering_replacements"] == replacements
    normalized = literal
    for item in replacements:
        normalized = normalized.replace(item["from"], item["to"])
    normalized = " ".join(normalized.split())
    assert normalized == abstract_model["normalized_full_text"]
    assert sha(normalized.encode()) == abstract_model["normalized_SHA256"]
    page_bytes = (W / "private-page/index.html").read_bytes()
    assert len(page_bytes) == 14855
    html = page_bytes.decode()
    page = PageData()
    page.feed(html)
    assert " ".join("".join(page.abstract).split()) == normalized
    assert page.meta["citation_abstract"] == page.meta["DC.description"] == normalized
    assert len(page.scripts) == 1 and page.scripts[0]["attrs"] == {"type": "application/ld+json"}
    schema = json.loads("".join(page.scripts[0]["text"]))
    assert schema == model["structured_data"] and schema["@type"] == "ScholarlyArticle" and "@graph" not in schema
    assert schema["abstract"] == normalized and schema["version"] == "1.0" and schema["datePublished"] == "2026-10-17"
    assert schema["identifier"]["value"] == api["doi"] and schema["license"] == "https://creativecommons.org/licenses/by/4.0/"
    assert page.meta["citation_title"] == page.meta["DC.title"] == model["title"]
    assert page.meta["citation_author"] == model["author"] == "Alec Kriebel"
    assert page.meta["citation_author_orcid"] == model["ORCID"]
    assert page.meta["citation_author_institution"] == api["metadata"]["creators"][0]["affiliation"]
    assert page.meta["citation_version"] == "1.0" and page.meta["citation_date"] == page.meta["citation_publication_date"] == "2026/10/17"
    assert page.meta["citation_doi"] == api["doi"] and page.meta["DC.identifier"] == api["doi_url"]
    names = ["Canonical_W_D4_Verification_v1.0.zip", "Canonical_W_D4_Note_v1.0.pdf"]
    assert [f["key"] for f in api["files"]] == names
    assert page.file_order == names
    assert [f["name"] for f in schema["encoding"]] == names
    assert [f["native_filename"] for f in model["native_assets_in_original_order"]] == names
    assets = []
    for index, (native, item, encoding) in enumerate(zip(api["files"], model["native_assets_in_original_order"], schema["encoding"]), 1):
        name = native["key"]
        data = (W / "private-page" / name).read_bytes()
        assert data == (S / "assets" / name).read_bytes()
        assert len(data) == native["size"] == item["bytes"]
        assert sha(data) == item["SHA256"] and hashlib.md5(data).hexdigest() == item["MD5"]
        assert "md5:" + item["MD5"] == native["checksum"]
        assert item["native_order"] == index and item["native_url"] == encoding["contentUrl"] == native["links"]["self"]
        assert encoding["contentSize"] == str(len(data)) + " bytes"
        assets.append({"name": name, "bytes": len(data), "SHA256": sha(data), "MD5": item["MD5"]})
    pdf = names[1]
    assert page.meta["citation_pdf_url"] == api["files"][1]["links"]["self"]
    assert len(page.iframes) == 1 and page.iframes[0]["src"] == pdf and page.iframes[0]["class"] == "paper-pdf"
    assert any(a.get("href") == pdf and "download" in a for a in page.anchors)
    assert all(any(a.get("href") == f["links"]["self"] for a in page.anchors) for f in api["files"])
    for a in page.anchors:
        href = a.get("href", "")
        if href and not href.startswith(("/", "#", "https://")):
            assert (W / "private-page" / href).is_file(), href
    assert sha((W / "private-page/research.css").read_bytes()) == model["stylesheet"]["SHA256"] == "f8cc0b3df011584d4e0266047af9c7c930266d0378909c0ca14e69e642653a6a"
    bib = (W / "private-page/citation.bib").read_text()
    assert "version = {1.0}" in bib and model["title"] in bib and api["doi"] in bib
    assert "17 October 2026" in bib and "Unrefereed" in bib
    assert page.meta["robots"] == model["robots"] == "noindex,nofollow"
    fields = ["actual_canonical", "base_url", "production_url", "page_publication_date", "AA", "legacy_redirect", "follow_up"]
    assert all(model[k] is None for k in fields)
    final = load(W / "FINAL.json")
    assert all(final[k] is None for k in ["canonical", "base_url", "production_url", "page_publication_date", "AA", "redirect", "follow_up"])
    assert model["private_only"] is True and model["publication_authority"] is False and final["publication_authority"] is False
    assert not {"base", "form"}.intersection(page.tags) and not any(l.get("rel") == "canonical" for l in page.links)
    assert "necessary direction of the historical" in html and "later string-coordinate converse is not refuted" in html
    assert "complete string-coordinate support" in html and "Case 267" in html
    assert html.index("Earlier computation") < html.index("The explicit example")
    assert "coefficient criterion" in html and "KS sufficient-criterion theorem" in html
    assert "does not supply a general replacement proof" in html
    assert "exclusive-priority or current-openness" in html and "AI tools were used extensively" in html
    assert "conventional external human peer review" in html and "not a formal proof-assistant certificate" in html
    assert "work actually contributed" in html and "CC BY 4.0" in html and "MIT licensed" in html
    assert not any(x in html for x in ["BUILDER_RUN", "SyntaxError", "16:30", "A2 audit", "CUSTODY_AFTER"])
    license_text = (S / "published-source/container-001/tree/LICENSE.txt").read_text()
    assert "Original manuscript, certificates and review text" in license_text and "MIT License" in license_text
    assert not any(q.suffix.lower() in {".xz", ".pdf"} for q in (S / "published-source/container-001/tree").rglob("*") if q.is_file())
    assert load(OLD / "BUILDER_RUN.json")["exit"] == 1
    assert len((OLD / "BUILDER.stderr.bin").read_bytes()) == 680
    assert (OLD / "BUILDER.stdout.bin").read_bytes() == b""
    assert load(W / "BUILDER_RUN.json")["exit"] == 0 and (W / "BUILDER.stderr.bin").read_bytes() == b""
    assert load(W / "ROOT_SETUP_DISPOSITION.json")["prior_V2_builder_invocations"] == 0
    write("NATIVE_ASSETS.json", assets)
finally:
    after = snapshot()
    exact = after == before
    write("CUSTODY_AFTER.json", {"UTC": utc(), **after, "before_after_exact": exact})
    assert exact, "Protected input changed during this passive check"

result = {"UTC_start": started, "UTC_end": utc(), "status": "PASS_PRIVATE_FACTUAL_COPY",
          "remaining_issue_count": 0, "scientific_PASS_unchanged": True,
          "source72_7_writer30_1_failed22_0_specific_root_before_after_exact": True,
          "schema_aware_individual_modes_terminal_external_pins_exact": True,
          "complete_native_abstract_rendering_metadata_assets_order_rights_private_fields_pass": True,
          "data_reader_attempts": 1, "repair_or_retry_count": 0,
          "native_scientific_source_producer_helper_execution": 0,
          "W_Git_network_Sheet_UI_stage_deploy_redirect_operations": 0,
          "new_mathematical_question": None, "follow_up": None,
          "publication_or_future_action_authority": False}
write("DATA_RESULT.json", result)
print(json.dumps(result, indent=2))
