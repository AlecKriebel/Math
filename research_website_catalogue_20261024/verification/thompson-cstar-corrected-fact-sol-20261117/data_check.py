"""One bounded passive factual-data check; never imports or executes project code."""
import datetime
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import stat

OWN = Path(__file__).resolve().parent
P = OWN.parent.parent
assert OWN.name == "thompson-cstar-corrected-fact-sol-20261117"
S = P / "papers/23204212/sources"
W = P / "verification/thompson-cstar-editorial-sol-20261117"
F = P / "verification/thompson-cstar-editorial-fact-sol-20261117"
FAILED = P / "verification/thompson-cstar-editorial-corrected-sol-20261117"
V = P / "verification/thompson-cstar-editorial-corrected-v2-sol-20261117"
REVIEW = P / "papers/23204212/reviews/root-continuation-20261117/ROOT_REVIEW.md"
CLEARANCE = P / "verification/root-clearance-23204212-20261117.json"
TREES = {"source": (S, 55, 14), "original_writer": (W, 27, 1),
         "original_fact": (F, 14, 0), "failed_correction": (FAILED, 6, 0),
         "corrected_v2": (V, 22, 1)}
PINS = {
    S / "SOURCE_FINAL.json": "b68fbb425b7d910a2508c46ff311491a1c797568dcf39d3c7deb0a0545e1afd5",
    S / "SOURCE_MANIFEST.json": "afa64c126da0aabc4a44ec242553e5b2354540eb1b0b60e55ab7b1a9855a09be",
    W / "FINAL.json": "36c84f224773aa954a4e59a3152b2089e60c95710e88a12231931c646b1e8557",
    W / "MANIFEST.json": "4c5cb453d5fec1544e0b6556b5d858c059657f24dd547b161358f40e14314a55",
    W / "SEAL.json": "eee46ef4f3c64b6f428538d38b64af343404fad31a152912ca926e1d7bba92d9",
    F / "FINAL.json": "2c4723092ac4d6e7c7a1a7fae7842090fa91bdfbb857b2d3e613dd697b748ead",
    F / "FACT_REPORT.md": "06796566a85580cfaa67bdf671ba24eb848c0acee1e18f0460d2bc2abad9f36c",
    F / "FINAL_MANIFEST.json": "056a582ec4ca0525882a8a95f1db67f267050932b50febd44d409fa8e8637afa",
    F / "FINAL_SEAL.json": "eb51f8476628f017a55f0855ec80de3a34c65e3d66ac79014a881575f0a71817",
    FAILED / "TRANSFORM.stderr": "5e98b958e0f182c61f39299dd71d53080985920d61ac1cbfc2274aeb0f786322",
    V / "FINAL.json": "67d0f85b610b011d1079889cb8932971ab6e9f8e0bb7c04e02946359aa27e533",
    V / "MANIFEST.json": "b1cef893c874b1c6502f5107fb4ae93d352828f0a830fb587c92a1fe9378243e",
    V / "SEAL.json": "e1adb487c49b1f6232c6d635e571ea2ae3aa445835cc3dddceaf83063c4797a4",
    V / "private-page/index.html": "1885856dbf199b10703652fb9a07d55119c2c02ae2d3f081d441fd68892514e3",
    V / "MODEL.json": "81e047addf166e36e766d0a12b2b286ccee852e64db9a1117d36633e8fdacd3a",
    REVIEW: "71136fd6de5610566ccffa7142a2ecabac093e33bad245e06eb7a3d456d85501",
    CLEARANCE: "cf26226d4c236473c5cb75ede27c50f77e486761df16a624d39cf26abdbb797c",
}

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    return json.loads(path.read_bytes())

def write(name, obj):
    path = OWN / name
    assert not path.exists(), str(path)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")

def object_record(path, rel):
    info = path.lstat()
    assert stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode), str(path)
    result = {"path": rel, "mode_octal": format(stat.S_IMODE(info.st_mode), "04o"),
              "mtime_ns": info.st_mtime_ns, "ctime_ns": info.st_ctime_ns,
              "hidden_component": any(s.startswith(".") for s in Path(rel).parts if s != ".")}
    if stat.S_ISDIR(info.st_mode):
        result.update(kind="directory", empty=not any(path.iterdir()))
    else:
        data = path.read_bytes()
        result.update(kind="file", bytes=len(data), empty=not data,
                      sha256=sha(data), md5=hashlib.md5(data).hexdigest())
    return result

def snapshot():
    result = {"trees": {}, "specific_root_inputs": {}}
    for name, (root, expected_files, expected_dirs) in TREES.items():
        assert root.resolve() == root and stat.S_ISDIR(root.lstat().st_mode)
        objects = [root] + sorted(root.rglob("*"), key=lambda q: q.relative_to(root).as_posix())
        entries = [object_record(q, "." if q == root else q.relative_to(root).as_posix()) for q in objects]
        files = sum(e["kind"] == "file" for e in entries)
        dirs = sum(e["kind"] == "directory" for e in entries) - 1
        assert (files, dirs) == (expected_files, expected_dirs), (name, files, dirs)
        result["trees"][name] = {"files": files, "child_directories": dirs, "entries": entries}
    for path in (REVIEW, CLEARANCE):
        result["specific_root_inputs"][str(path)] = object_record(path, path.name)
    for path, expected in PINS.items():
        assert sha(path.read_bytes()) == expected, ("external pin", str(path))
    return result

def validate_manifest(root, records, filename, terminal_pair, excluded=False):
    manifest = load(root / filename)
    actual = {e["path"]: e for e in records["entries"]}
    declared = manifest["entries"]
    assert len({e["path"] for e in declared}) == len(declared)
    if excluded:
        assert sorted(manifest["excluded_control_files"]) == sorted(terminal_pair)
        assert {e["path"] for e in declared} == set(actual) - set(terminal_pair)
        assert manifest["file_count"] == records["files"] - len(terminal_pair)
        assert manifest["directory_count"] == records["child_directories"] + 1
    else:
        key = "exact_recursive_digest_exclusions" if root == W else "terminal_content_hash_exclusions_exact"
        assert sorted(manifest[key]) == sorted(terminal_pair)
        assert {e["path"] for e in declared} == set(actual)
        assert manifest["file_count"] == records["files"]
        assert manifest["child_directory_count"] == records["child_directories"]
    for entry in declared:
        record = actual[entry["path"]]
        for key, value in entry.items():
            if key in ("digest_exclusion", "content_hash_exclusion"):
                assert entry["path"] in terminal_pair and isinstance(value, str)
            elif key == "mode_octal":
                assert int(record[key], 8) == int(value, 8), (root, entry["path"], key)
            elif key == "sha256" and value is None:
                assert root == F and entry["path"] in terminal_pair
            else:
                assert key in record and record[key] == value, (root, entry["path"], key)
        if record["kind"] == "file" and entry["path"] not in terminal_pair:
            assert isinstance(entry.get("sha256"), str)
    if root == F:
        assert all(next(e for e in declared if e["path"] == name)["sha256"] is None for name in terminal_pair)

class PageData(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.tags = []
        self.links = []
        self.anchors = []
        self.iframes = []
        self.scripts = []
        self.script = None
        self.abstract_open = False
        self.abstract = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "meta" and "name" in values:
            assert values["name"] not in self.meta
            self.meta[values["name"]] = values.get("content")
        if tag == "link":
            self.links.append(values)
        if tag == "a":
            self.anchors.append(values)
        if tag == "iframe":
            self.iframes.append(values)
        if tag == "script":
            assert self.script is None
            self.script = {"attrs": values, "text": []}
        if tag == "p" and values.get("id") == "original-abstract":
            self.abstract_open = True
    def handle_endtag(self, tag):
        if tag == "script":
            assert self.script is not None
            self.scripts.append(self.script)
            self.script = None
        if tag == "p":
            self.abstract_open = False
    def handle_data(self, data):
        if self.script is not None:
            self.script["text"].append(data)
        if self.abstract_open:
            self.abstract.append(data)

started = utc()
before = snapshot()
write("CUSTODY_BEFORE.json", {"UTC": started, **before})
try:
    validate_manifest(S, before["trees"]["source"], "SOURCE_MANIFEST.json", ["SOURCE_FINAL.json", "SOURCE_MANIFEST.json"], True)
    validate_manifest(W, before["trees"]["original_writer"], "MANIFEST.json", ["MANIFEST.json", "SEAL.json"])
    validate_manifest(F, before["trees"]["original_fact"], "FINAL_MANIFEST.json", ["FINAL_MANIFEST.json", "FINAL_SEAL.json"])
    validate_manifest(V, before["trees"]["corrected_v2"], "MANIFEST.json", ["MANIFEST.json", "SEAL.json"])
    old = (W / "private-page/index.html").read_bytes()
    new = (V / "private-page/index.html").read_bytes()
    old_clause = b"then takes their operator-norm closure."
    new_clause = b"then takes the operator-norm closure of their complex linear span."
    assert old.count(old_clause) == 1 and old.count(new_clause) == 0
    assert new.count(new_clause) == 1 and new.count(old_clause) == 0
    assert new == old.replace(old_clause, new_clause, 1)
    assert old == new.replace(new_clause, old_clause, 1)
    prefix, suffix = old.split(old_clause)
    assert new == prefix + new_clause + suffix
    assert len(old) == 15497 and len(new) == 15524
    assert sha(old) == "e5a368d2f5c82e10b048c21fe9e3137e503b62fa17be962e04f71bfca60eaee4"
    assert (W / "MODEL.json").read_bytes() == (V / "MODEL.json").read_bytes()
    model = load(V / "MODEL.json")
    assert sha((V / "MODEL.json").read_bytes()) == "81e047addf166e36e766d0a12b2b286ccee852e64db9a1117d36633e8fdacd3a"
    old_names = {q.name for q in (W / "private-page").iterdir()}
    assert old_names == {q.name for q in (V / "private-page").iterdir()}
    assert old_names == {"index.html", "citation.bib", "research.css", "paper.pdf", "thompson-cstar-source.zip", "thompson-cstar-verification.zip"}
    for name in old_names - {"index.html"}:
        a, b = W / "private-page" / name, V / "private-page" / name
        assert a.read_bytes() == b.read_bytes(), name
        assert stat.S_IMODE(a.stat().st_mode) == stat.S_IMODE(b.stat().st_mode), name
    api = load(S / "native-metadata/record-api.json")
    assert api["id"] == 23204212 and api["doi"] == model["doi"]
    assert api["metadata"]["title"] == model["title"]
    assert "version" not in api["metadata"]
    assert model["native_version"] is None and model["native_version_field_present"] is False
    assert model["host_edition_label"] == "v1"
    assert api["metadata"]["publication_date"] == model["native_publication_date"] == "2026-10-06"
    assert api["created"] == model["native_record_created"] == "2026-10-07T05:35:37.608378+00:00"
    assert api["updated"] == model["native_record_updated"]
    assert api["metadata"]["license"]["id"] == "cc-by-4.0"
    names = ["thompson-cstar-verification.zip", "thompson-cstar-source.zip", "paper.pdf"]
    assert [x["key"] for x in api["files"]] == names
    assert [x["native_filename"] for x in model["native_assets_in_original_order"]] == names
    assets = []
    for index, (native, item) in enumerate(zip(api["files"], model["native_assets_in_original_order"]), 1):
        name = native["key"]
        data = (V / "private-page" / name).read_bytes()
        assert data == (S / "zenodo-files" / name).read_bytes()
        assert len(data) == native["size"] == item["bytes"]
        assert sha(data) == item["sha256"]
        assert "md5:" + hashlib.md5(data).hexdigest() == native["checksum"]
        assert hashlib.md5(data).hexdigest() == item["md5"]
        assert item["ordinal"] == index and item["native_url"] == native["links"]["self"]
        assets.append({"name": name, "bytes": len(data), "sha256": sha(data)})
    tex = (S / "archives/02-thompson-cstar-source.zip.extracted/main.tex").read_text()
    assert "norm closure of the linear span" in tex
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
    norm = lambda text: " ".join(text.split())
    assert norm(abstract) == model["original_abstract_tex"]
    replacements = [{"from": "$\\Aut(F)$", "to": "Aut(F)"}, {"from": "$\\Comm(F)$", "to": "Comm(F)"},
                    {"from": "$F$", "to": "F"}, {"from": "$T$", "to": "T"}]
    assert model["abstract_rendering_replacements"] == replacements
    for replacement in replacements:
        abstract = abstract.replace(replacement["from"], replacement["to"])
    abstract = norm(abstract)
    assert abstract == model["original_abstract_normalized"]
    assert sha(abstract.encode()) == model["abstract_normalized_sha256"]
    page = PageData()
    html = new.decode()
    page.feed(html)
    assert norm("".join(page.abstract)) == abstract == page.meta["citation_abstract"]
    assert page.meta["robots"] == "noindex,nofollow"
    assert page.meta["citation_doi"] == api["doi"]
    assert page.meta["citation_title"] == model["title"]
    assert page.meta["citation_author_orcid"] == model["author"]["orcid"]
    assert page.meta["citation_publication_date"] == "2026/10/06"
    assert page.meta["citation_pdf_url"] == api["files"][2]["links"]["self"]
    assert page.meta["DC.identifier"] == model["doi_url"]
    assert len(page.scripts) == 1 and page.scripts[0]["attrs"] == {"type": "application/ld+json"}
    schema = json.loads("".join(page.scripts[0]["text"]))
    assert schema["@type"] == "ScholarlyArticle" and schema["abstract"] == abstract
    assert schema["datePublished"] == model["native_publication_date"]
    assert schema["dateCreated"] == model["native_record_created"]
    assert schema["identifier"] == model["doi_url"] and schema["url"] == model["native_record_url"]
    assert "version" not in schema
    assert [e["name"] for e in schema["encoding"]] == names
    assert [e["contentUrl"] for e in schema["encoding"]] == [e["links"]["self"] for e in api["files"]]
    first_native = [a["href"] for a in page.anchors if a.get("href") in names]
    assert first_native[:3] == names
    assert len(page.iframes) == 1 and page.iframes[0]["src"] == "paper.pdf"
    assert page.iframes[0]["class"] == "paper-pdf"
    assert not {"base", "form"}.intersection(page.tags)
    assert not any(link.get("rel") == "canonical" for link in page.links)
    assert any(link == {"rel": "stylesheet", "href": "research.css"} for link in page.links)
    fields = ["actual_canonical", "base_url", "production_url", "page_publication_date", "AA", "legacy_route", "legacy_redirect", "follow_up"]
    assert all(model[key] is None for key in fields)
    assert model["publication_authority"] is False and model["private_only"] is True
    corrected_final = load(V / "FINAL.json")
    assert all(corrected_final["all_publication_fields"][key] is None for key in fields)
    assert corrected_final["publication_authority"] is False
    assert corrected_final["scientific_manuscript_PASS_unchanged"] is True
    clearance = load(CLEARANCE)
    assert clearance["status"] == "PASS_BOUNDED_ATTRIBUTED_CONSEQUENCE_AND_UPSTREAM_WRITTEN_PROOF"
    assert clearance["follow_up"] is None and clearance["no_formal_or_human_certificate"] is True
    assert model["upstream_commit"] == clearance["upstream_commit"] == "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
    assert model["upstream_commit"] in html and "No first-priority claim" in html
    assert "already known unconditionally" in html and "no author version" in html
    assert "AI tools were used extensively" in html and "conventional human peer review" in html
    assert "No formalization" in html and "work actually contributed" in html
    assert "CC BY 4.0" in html and "MIT licensed" in html
    assert "version" not in (V / "private-page/citation.bib").read_text().lower()
    assert load(FAILED / "TRANSFORM_RUN.json")["exit"] == 1
    assert (FAILED / "TRANSFORM.stdout").read_bytes() == b""
    assert len((FAILED / "TRANSFORM.stderr").read_bytes()) == 1052
    v2_run = load(V / "TRANSFORM_RUN.json")
    assert v2_run["exit"] == 0 and v2_run["attempt_count_in_this_authorized_lane"] == 1
    assert v2_run["repair_or_retry_count"] == 0 and (V / "TRANSFORM.stderr").read_bytes() == b""
    comparison = {"old_page_bytes": len(old), "corrected_page_bytes": len(new),
                  "old_page_sha256": sha(old), "corrected_page_sha256": sha(new),
                  "old_clause": old_clause.decode(), "corrected_clause": new_clause.decode(),
                  "old_and_new_clause_counts": [1, 1], "whole_forward_exact": True,
                  "whole_reverse_exact": True, "unchanged_prefix_bytes": len(prefix),
                  "unchanged_prefix_sha256": sha(prefix), "unchanged_suffix_bytes": len(suffix),
                  "unchanged_suffix_sha256": sha(suffix), "model_Bib_CSS_assets_byte_exact": True}
    write("BYTE_COMPARISON.json", comparison)
    write("NATIVE_ASSETS.json", assets)
finally:
    after = snapshot()
    exact = after == before
    write("CUSTODY_AFTER.json", {"UTC": utc(), **after, "before_after_exact": exact})
    assert exact, "Protected input changed during the passive factual check"

result = {"UTC_start": started, "UTC_end": utc(), "status": "PASS_CORRECTED_PRIVATE_COPY",
          "issue_count": 0, "original_P2_resolved": True, "scientific_manuscript_PASS_unchanged": True,
          "whole_forward_reverse_exact": True, "source55_14_writer27_1_fact14_0_failed6_0_v2_22_1_root_exact": True,
          "terminal_nulls_checked_as_exclusion_markers_with_external_pins_and_full_metadata": True,
          "full_abstract_metadata_assets_schema_private_nulls_exact": True,
          "data_reader_attempts": 1, "scientific_source_producer_helper_execution": 0,
          "network_Git_W_stage_Sheet_operations": 0, "follow_up": None,
          "publication_or_future_action_authority": False}
write("DATA_RESULT.json", result)
print(json.dumps(result, indent=2))
