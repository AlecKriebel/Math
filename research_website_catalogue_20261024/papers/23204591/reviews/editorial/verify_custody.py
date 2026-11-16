#!/usr/bin/env python3
"""Pure offline custody/content guard; no mathematical program execution."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import html
import json
import re
import sys

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[3]
SOURCE = HERE.parent.parent / "sources"
TERMINALS = ["CUSTODY_RUN_RECEIPT.json", "FINAL_SEAL.json", "LOCAL_MANIFEST.json", "custody-normal.stderr", "custody-normal.stdout.json", "custody-optimized.stderr", "custody-optimized.stdout.json"]
CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def read(path):
    require(path.is_file() and not path.is_symlink(), "Not a regular unlinked file: " + str(path))
    raw = path.read_bytes()
    return raw, {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def read_json(path):
    raw, pin = read(path)
    return json.loads(raw), raw, pin


def match_file(path, expected):
    raw, pin = read(path)
    require(pin["bytes"] == expected["bytes"], "Byte count differs: " + str(path))
    require(pin["sha256"] == expected.get("sha256", expected.get("SHA256")), "Hash differs: " + str(path))
    return raw, pin


def inventory(root):
    files = []
    dirs = []
    for item in sorted(root.rglob("*")):
        require(not item.is_symlink(), "Symlink in namespace: " + str(item))
        rel = item.relative_to(root).as_posix()
        if item.is_dir():
            dirs.append(rel)
        elif item.is_file():
            files.append(rel)
        else:
            raise ValueError("Nonregular namespace entry: " + str(item))
    return files, dirs


class Probe(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.ids = {}
        self.meta = {}
        self.links = []
        self.iframes = []
        self.script_bodies = []
        self.main_count = 0
        self.h1_count = 0
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            require(a.get("id") == "main", "Unexpected MAIN identifier")
            self.main_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta":
            self.meta[a.get("name")] = a.get("content")
        if tag == "a":
            self.links.append(a)
        if tag == "iframe":
            self.iframes.append(a)
        if tag in ("br", "meta", "link", "img", "hr", "input", "source", "wbr"):
            return
        self.stack.append((tag, a.get("id"), a))
        if a.get("id"):
            require(a["id"] not in self.ids, "Duplicate HTML ID")
            self.ids[a["id"]] = []
        if tag == "script":
            self.script_bodies.append([])

    def handle_endtag(self, tag):
        require(bool(self.stack) and self.stack[-1][0] == tag, "Unbalanced HTML at " + tag)
        self.stack.pop()

    def handle_data(self, data):
        self.text.append(data)
        for _, element_id, _ in self.stack:
            if element_id:
                self.ids[element_id].append(data)
        if self.stack and self.stack[-1][0] == "script":
            self.script_bodies[-1].append(data)


def flat(value):
    return re.sub(r"\s+", "", value)


def run():
    manifest, manifest_raw, manifest_pin = read_json(HERE / "LOCAL_MANIFEST.json")
    require(manifest["terminal_files"] == TERMINALS, "Terminal exclusion list changed")
    require(all("/" not in x and "*" not in x for x in TERMINALS), "Non-root or wildcard exclusion")
    files, dirs = inventory(HERE)
    require(dirs == manifest["directories"], "Local directory closure changed")
    declared = [x["path"] for x in manifest["files"]]
    require(declared == sorted(declared) and len(declared) == len(set(declared)), "Malformed manifest file list")
    require([f for f in files if f not in TERMINALS] == declared, "Local finite file closure changed")
    for row in manifest["files"]:
        require(not Path(row["path"]).is_absolute() and ".." not in Path(row["path"]).parts, "Unsafe manifest path")
        match_file(HERE / row["path"], row)

    protected, _, _ = read_json(HERE / "PROTECTED_NAMESPACES.json")
    expected_counts = [(92, 10), (270, 5), (352, 8), (19, 3)]
    namespace_results = []
    for ns, (file_count, dir_count) in zip(protected["namespaces"], expected_counts, strict=True):
        root = Path(ns["path"])
        actual_files, actual_dirs = inventory(root)
        require(actual_files == [r["path"] for r in ns["files"]], "Protected file closure changed")
        require(actual_dirs == ns["directories"], "Protected directory closure changed")
        require((len(actual_files), len(actual_dirs)) == (file_count, dir_count), "Protected namespace count changed")
        for row in ns["files"]:
            match_file(root / row["path"], row)
        namespace_results.append({"path": str(root), "files": file_count, "child_directories": dir_count})

    core, _, _ = read_json(HERE / "PROTECTED_CORE.json")
    reference = core["reference"]
    ref_raw, _ = match_file(Path(reference["path"]), reference)
    ref = json.loads(ref_raw)
    require(core["core_17_original_pins"] == ref["core_17_original_pins"], "Core reference changed")
    require(len(core["core_17_original_pins"]) == 17, "Wrong original core extent")
    for row in core["core_17_original_pins"]:
        match_file(Path(row["path"]), row)
    extra = core["sole_checkpoint_helper_separate"]
    require(extra["bytes"] == 6213 and extra["SHA256"] == "405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0", "Wrong checkpoint-helper pin")
    match_file(Path(extra["path"]), extra)
    require(core["global_cache_or_index_immutability_claim"] is False, "Unowned global immutability scope")

    authority_raw, authority_pin = match_file(PROJECT / "verification/root-clearance-23204591-20261115.json", {"bytes": 29352, "sha256": "6fecf14e6de99fbec8e684d3224276054f439644cf5302ceb401d64a9dab5833"})
    authority = json.loads(authority_raw)
    require(authority["status"] == "PASS_FULL_ORIGINAL_SCIENTIFIC_CLAIM" and authority["full_original_claim_preserved"] is True, "Full original scientific authority absent")
    require(authority["private_full_original_editorial_preparation_authorized"] is True and authority["production_publish_or_deploy_authority"] is False, "Authority boundary changed")
    match_file(HERE.parent / "root/ROOT_REVIEW_20261115.md", {"bytes": 9321, "sha256": "3430f3770a7f33add54655f3c7739d3f29b014ef15f345acfb4200dbd479ca75"})

    initial, _, initial_pin = read_json(HERE / "INITIAL_SEAL.json")
    for row in initial["files"]:
        match_file(HERE / row["path"], row)
    ack, _, _ = read_json(HERE / "PARENT_ACKNOWLEDGMENT.json")
    require(ack["initial_seal_sha256"] == initial_pin["sha256"], "Parent acknowledgment does not bind initial")
    require(ack["production_authority"] is False, "Private authorization changed")

    model, _, _ = read_json(HERE / "PAGE_MODEL.json")
    metadata, _, _ = read_json(HERE / "METADATA.json")
    ready, _, _ = read_json(SOURCE / "SOURCE_READY.json")
    record, _, _ = read_json(SOURCE / "record.response.body")
    main_raw, main_pin = read(HERE / "public-main.html")
    preview_raw, preview_pin = read(HERE / "preview.html")
    main = main_raw.decode("utf-8").strip()
    preview = preview_raw.decode("utf-8")
    require(re.search(r"<body>(.*)</body>", preview, re.S).group(1) == main, "Preview does not contain exact entire public MAIN")
    require(main.startswith('<main id="main">') and main.endswith('</main>'), "Public MAIN boundary changed")
    require('rel="canonical"' not in preview and '<base ' not in preview, "Premature canonical/base assignment")
    p = Probe()
    p.feed(preview)
    require(not p.stack and p.main_count == 1 and p.h1_count == 1, "Bad document structure")
    require(p.meta["robots"] == "noindex,nofollow", "Private preview indexable")
    require(p.meta["description"] == model["meta_description"] and 60 <= len(model["meta_description"]) <= 200, "SEO description mismatch")
    require(html.escape(model["page_title"]) in preview, "SEO title mismatch")
    for key in ("canonical_url", "base_url", "AA", "follow_up"):
        require(model[key] is None and metadata[key] is None, "Premature publication field: " + key)
    require(model["private_preview"] is True and metadata["production_authority"] is False, "Publication boundary")
    native = record["metadata"]
    require(metadata["native_version_field_present"] is True and metadata["native_version"] == native["version"] == "1.0.0", "Native version mismatch")
    require(metadata["printed_version"] is None and metadata["printed_date"] == "October 6, 2026", "Printed metadata conflated")
    require(metadata["native_publication_date"] == "2026-10-06" and metadata["native_created_UTC"] == "2026-10-07T05:57:22.109880+00:00", "Date fields conflated")
    require(metadata["whole_native_description_original"] == native["description"], "Original description truncated")
    require(''.join(p.ids["native-description"]) == html.unescape(native["description"]), "Whole native description not separately present")
    tex_raw, _ = read(Path(ready["controlling_TeX"]["extracted_path"]))
    tex_abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex_raw.decode(), re.S).group(1)
    for before, after in [("$S,T$", "S,T"), ("$f,g\\in L^3$", "f,g ∈ L3"), ("$r$", "r"), ("$L^{3/2}$", "L3/2"), ("$r>2$", "r > 2")]:
        tex_abstract = tex_abstract.replace(before, after)
    require(flat(''.join(p.ids["printed-abstract"])) == flat(tex_abstract), "Full printed abstract changed or truncated")
    normalized_description = model["abstract_text"].replace("L^(3/2)", "L3/2").replace("L^3", "L3")
    require(flat(normalized_description) == flat(tex_abstract), "Scholarly abstract differs from printed abstract")
    require(len(p.script_bodies) == 1, "Unexpected script count")
    scholarly = json.loads(''.join(p.script_bodies[0]))
    require(scholarly == metadata["scholarly"], "Structured data mismatch")
    require(scholarly["name"] == native["title"] and scholarly["version"] == "1.0.0" and scholarly["datePublished"] == "2026-10-06", "Scholarly edition metadata mismatch")
    require(scholarly["identifier"]["value"] == "10.5281/zenodo.23204591" and scholarly["creativeWorkStatus"] == "Preprint", "Scholarly status or DOI mismatch")
    for key, value in metadata["citation_meta"].items():
        require(p.meta[key] == value, "Citation meta mismatch: " + key)
    require(len(p.iframes) == 1 and p.iframes[0]["src"] == "assets/paper.pdf#view=FitH", "Original PDF FitH embed absent")
    links = [a["href"] for a in p.links]
    require("assets/paper.pdf#view=FitH" in links and any(a.get("href") == "assets/paper.pdf" and "download" in a for a in p.links), "PDF open/download missing")
    assets = []
    for row in ready["all_native_assets_in_original_order"]:
        native_file = row["original_api_file_object"]
        raw, pin = match_file(HERE / "assets" / native_file["key"], row)
        require(raw == Path(row["path"]).read_bytes(), "Native asset bytes changed")
        require(native_file["links"]["self"] in links, "Native original file link absent")
        require('md5:' + hashlib.md5(raw).hexdigest() == native_file["checksum"], "Native asset MD5 mismatch")
        assets.append({"key": native_file["key"], **pin})
    require([a["key"] for a in assets] == ["README.md", "verification-supplement.zip", "source.zip", "paper.pdf"], "Native asset order changed")
    for a in p.links:
        target = a.get("href", "")
        if target.startswith("assets/") or target == "citation.bib":
            require((HERE / target.split("#")[0]).is_file(), "Missing local download")
    bib_raw, _ = read(HERE / "citation.bib")
    require(native["title"] in bib_raw.decode() and "version = {1.0.0}" in bib_raw.decode() and "doi = {10.5281/zenodo.23204591}" in bib_raw.decode(), "BibTeX mismatch")
    text = ''.join(p.ids["main"])
    for token in ["pointwise", "each point may choose its own list", "complex bilinear", "maximal-tail", "No ergodicity or freeness", "signed kernel", "positive-area", "Calderón", "footnote 36", "Section 5", "opposite powers", "AI tools were used extensively", "not undergone conventional human peer review", "actual contributions"]:
        require(token in text, "Required full-claim/context wording absent: " + token)
    require(not any(s in text for s in ["14,850", "14850", "23,150", "23150", "2026-11-15", "2026-11-16", "MIT License"]), "Internal counts/logs or invented license in public copy")
    require("https://creativecommons.org/licenses/by/4.0/" in links, "CC BY4 license absent")
    layout, _, _ = read_json(HERE / "LAYOUT_INSPECTION.json")
    require(len(layout) == 2, "Layout view count")
    for row in layout:
        require(row["state"]["scrollWidth"] == row["state"]["width"] and not row["state"]["elementsOutsideViewport"], "Horizontal layout overflow")
        require(row["state"]["mainCount"] == 1 and row["state"]["bodyBackground"] == "rgb(255, 255, 255)" and row["state"]["fontFamily"].startswith("Arial"), "Layout style mismatch")
        require(not row["pageErrors"] and not row["attemptedExternalRequests"], "Offline layout error/request")
    code_reads, _, _ = read_json(HERE / "CODE_READ_LEDGER.json")
    for code in ("render_preview.py", "inspect_preview.cjs", "verify_custody.py"):
        raw, pin = read(HERE / code)
        require(any(r["sha256"] == pin["sha256"] and r["entire_current_body_personally_read_before_execution"] is True for r in code_reads["reads"]), "Current helper not fully read: " + code)
    require(code_reads["native_source_program_executions"] == 0, "Unexpected native source run")
    final_bound = False
    if (HERE / "FINAL_SEAL.json").exists():
        final, _, _ = read_json(HERE / "FINAL_SEAL.json")
        require(final["local_manifest_pin"] == manifest_pin, "FINAL does not bind current manifest")
        require(sorted(row["path"] for row in final["terminal_pins"]) == [x for x in TERMINALS if x != "FINAL_SEAL.json"], "Incomplete final terminal closure")
        require(all(x in files for x in TERMINALS), "Final terminal file missing")
        for row in final["terminal_pins"]:
            require(row["path"] in TERMINALS and row["path"] != "FINAL_SEAL.json", "Unexpected terminal pin")
            match_file(HERE / row["path"], row)
        final_bound = True
    print(json.dumps({"status": "PASS_PRIVATE_EDITORIAL_CUSTODY_CONTENT", "checks": CHECKS, "local_files_excluding_exact_terminals": len(declared), "local_child_directories": len(dirs), "protected_namespaces": namespace_results, "core_original_files": 17, "checkpoint_helper_separate": extra["SHA256"], "native_assets_in_original_order": assets, "public_main": main_pin, "preview": preview_pin, "root_scientific_authority": authority_pin, "final_seal_bound": final_bound, "source_program_executions": 0, "scope": "Finite custody/content/layout consistency only; no new scientific validation, external link fetch, website/Sheet/Git/deployment or publication authority"}, indent=2))


if __name__ == "__main__":
    try:
        run()
    except Exception as error:
        print(type(error).__name__ + ": " + str(error), file=sys.stderr)
        raise SystemExit(1)
