#!/usr/bin/env python3
"""Pure editorial/custody closure; no network, subprocess, writes or project imports.

No rendering or scientific programme is imported or executed. --preseal accepts
only the exact not-yet-created root closure/seal controls, not basename matches.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib
import html
import json
import stat
import sys

A = Path(__file__).resolve().parent
TERMINALS = ["MANIFEST.json", "CLOSURE_RECEIPT.json", "FINAL_SEAL.json"]
checks = 0


def require(ok, reason):
    global checks
    checks += 1
    if not ok:
        raise ValueError(reason)


def load(p):
    return json.loads(p.read_bytes())


def pin(x):
    p = Path(x["path"])
    require(p.is_absolute() and p.is_file() and not p.is_symlink(), "regular pinned file")
    b = p.read_bytes()
    require(len(b) == x["bytes"] and hashlib.sha256(b).hexdigest() == x["SHA256"], "whole input bytes: " + str(p))
    return p


def typed(a, b):
    require(type(a) is type(b), "literal original JSON type")
    if isinstance(a, dict):
        require(list(a) == list(b), "whole original key order")
        for k in a:
            typed(a[k], b[k])
    elif isinstance(a, list):
        require(len(a) == len(b), "whole original array length")
        for x, y in zip(a, b):
            typed(x, y)
    else:
        require(a == b, "literal scalar/null/history")


def namespace(root):
    require(root.is_dir() and not root.is_symlink(), "regular namespace root")
    files, dirs = [], []
    for p in root.rglob("*"):
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), "symlink rejected")
        if stat.S_ISDIR(mode):
            dirs.append(str(p.relative_to(root)))
        else:
            require(stat.S_ISREG(mode), "nonregular rejected")
            files.append(str(p.relative_to(root)))
    return sorted(files), sorted(dirs)


def protected(group):
    root = Path(group["root"])
    fs, ds = namespace(root)
    require(fs == sorted(x["relative_path"] for x in group["files"]), "entire protected file namespace")
    require(ds == group["directories"], "entire protected directory namespace")
    for x in group["files"]:
        require(pin(x) == root / x["relative_path"], "exact protected path")
    return root


class Structure(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


def main():
    require(sys.argv[1:] in ([], ["--preseal"]), "only optional --preseal")
    preseal = sys.argv[1:] == ["--preseal"]
    m = load(A / "MANIFEST.json")
    require(m["schema"] == "editorial_exact_namespace_manifest_23418581_v1", "manifest schema")
    require(m["exact_root_terminal_controls"] == TERMINALS, "exact root controls only")
    names = [x["relative_path"] for x in m["files"]]
    require(len(names) == len(set(names)), "unique owned paths")
    for x in m["files"]:
        r = Path(x["relative_path"])
        require(not r.is_absolute() and ".." not in r.parts and str(r) == x["relative_path"] and str(r) not in TERMINALS, "safe owned path")
        pin({"path": str(A / r), "bytes": x["bytes"], "SHA256": x["SHA256"]})
    fs, ds = namespace(A)
    require(fs == sorted(names + (["MANIFEST.json"] if preseal else TERMINALS)), "strict entire owned file namespace")
    require(ds == m["directories"], "strict entire owned directory namespace")
    if preseal:
        require(not (A / TERMINALS[1]).exists() and not (A / TERMINALS[2]).exists(), "no pre-existing terminal ignored")
    else:
        s = load(A / "FINAL_SEAL.json")
        require(s["record_id"] == 23418581 and s["production_authority"] is False, "source-only seal")
        require(s["canonical_url"] is None and s["AA"] is None, "no canonical authority")
        require(s["exact_root_terminal_controls"] == TERMINALS, "sealed root controls")
        require(pin(s["manifest"]) == A / "MANIFEST.json", "whole final manifest")
        require(pin(s["closure"]) == A / "CLOSURE_RECEIPT.json", "whole closure receipt")
        require(load(A / "CLOSURE_RECEIPT.json")["status"] == "PASS", "successful actual preseal")

    initial = load(A / "INITIAL_SEAL.json")
    for x in initial["files"]:
        pin(x)
    inputs = load(A / "INPUT_BINDINGS.json")
    source = protected(inputs["source_namespace"])
    protected(inputs["root_namespace"])
    require(len(inputs["source_namespace"]["files"]) == 291, "whole291 original source files")
    copy = Path(inputs["source_private_copy_root"])
    require(copy.is_relative_to(A / "raw"), "private source copy")
    cfs, cds = namespace(copy)
    require(cfs == sorted(x["relative_path"] for x in inputs["source_namespace"]["files"]), "whole private source-copy files")
    require(cds == inputs["source_namespace"]["directories"], "whole private source-copy directories")
    for x in inputs["source_namespace"]["files"]:
        require(Path(x["path"]).read_bytes() == (copy / x["relative_path"]).read_bytes(), "whole original/private-copy equality")
    authority = pin(inputs["root_authority"])
    require(hashlib.sha256(authority.read_bytes()).hexdigest() == "cf6112b19e69eb16523c97689d31e6a471cbe206057e5fde4de37c87953a0f6b", "root authority pin")
    require(len(inputs["qualified_core_actual18"]) == 18 and inputs["original17_unchanged"] == 17, "qualified original core")
    for x in inputs["qualified_core_actual18"]:
        p = pin(x)
        if p.name == "checkpoint_subtree.py":
            require(x["SHA256"] == "405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0", "only authorized checkpoint qualification")

    protocol = load(A / "SOURCE_PROTOCOL_BINDINGS.json")
    ready = load(source / "SOURCE_READY.json")
    typed(ready, protocol["whole_original_source_ready"])
    typed(load(authority), protocol["whole_literal_root_authority"])
    for x in protocol["whole_original_source_JSON_objects"]:
        typed(load(pin(x["original"])), x["whole_original_object"])
    for x in protocol["whole_native_API_objects_in_original_role_order"]:
        typed(load(pin(x["original"])), x["whole_original_object"])
    for x in protocol["whole_original_scientific_verdicts"]:
        typed(load(pin(x["original"])), x["whole_original_object"])
    require(ready["version_field_present"] is True and ready["version"] == "1.0", "native1.0 literal")
    require(ready["printed_title_date_version_inspected"] is False and ready["printed_date"] is None and ready["printed_version"] is None, "historical acquisition UNREAD flags")
    require(ready["recursive_archive_container_count"] == 4 and ready["whole_regular_payload_occurrences"] == 243 and ready["embedded_PDFs"] == [], "complete original archive extent")
    require([x["original_api_file_object"]["key"] for x in ready["all_native_assets_in_original_order"]] == ["source-and-verification.zip", "paper.pdf"], "native asset order")
    for x in ready["all_native_assets_in_original_order"]:
        p = pin(x)
        require(hashlib.md5(p.read_bytes()).hexdigest() == x["original_api_file_object"]["checksum"].removeprefix("md5:"), "native checksum")
        q = A / "candidate" / x["original_api_file_object"]["key"]
        require(q.read_bytes() == p.read_bytes(), "unchanged original download")

    c = load(A / "public-sections.json")
    pub = load(A / "publication.json")
    for k, v in c.items():
        typed(v, pub[k])
    typed(pub["source_binding"]["whole_original_source_ready"], ready)
    typed(pub["source_binding"]["whole_native_API_objects"], protocol["whole_native_API_objects_in_original_role_order"])
    typed(pub["review_metadata"]["root_authority"]["whole_literal_object"], load(authority))
    typed(pub["review_metadata"]["whole_original_scientific_verdicts"], protocol["whole_original_scientific_verdicts"])
    desc = load(source / "record.response.body")["metadata"]["description"]
    require(desc == protocol["native_description_HTML_original"] == pub["source_binding"]["native_deposit_description_HTML_original"] == (A / "raw/NATIVE_DESCRIPTION.html").read_text(), "whole distinct native description")
    tex = Path(ready["controlling_TeX"]["extracted_path"]).read_text()
    abstract = tex.split("\\begin{abstract}\n", 1)[1].split("\\end{abstract}", 1)[0]
    require(abstract == (A / "ORIGINAL_ABSTRACT.tex").read_text() == protocol["original_printed_abstract_TeX"], "whole original abstract TeX")
    for old, new in [(r"\(p\)", "p"), (r"\(\lambda=(2p-2,1)\)", "λ = (2p−2,1)"), (r"\(I_n(\lambda)\)", "I_n(λ)"), (r"\(n\ge2\)", "n≥2"), (r"\(q=1\)", "q=1"), ("~", " "), ("Miyachi's", "Miyachi’s")]:
        abstract = abstract.replace(old, new)
    require(" ".join(abstract.split()) == c["abstract"], "complete printed abstract wording")
    for key in ("follow_up", "canonical_url", "AA", "native_sheet_aa_url", "proposed_canonical_url", "code_license"):
        require(pub[key] is None, "literal null boundary")
    require(pub["version"] == pub["printed_version"] == "1.0" and pub["publication_date"] == "2026-10-16", "native/printed edition")
    require(pub["production_authority"] is False and pub["license"] == "CC BY 4.0", "rights/authority")
    require((A / "citation.bib").read_bytes() == (A / "candidate/citation.bib").read_bytes() == pub["prepared_bibtex"].encode(), "whole BibTeX")
    require(sorted(p.name for p in (A / "candidate").iterdir()) == ["citation.bib", "index.html", "paper.pdf", "source-and-verification.zip"], "exact four candidate leaves")
    main_text = (A / "PUBLIC_MAIN.html").read_text()
    candidate = (A / "candidate/index.html").read_text()
    require(candidate.count(main_text) == 1, "candidate contains entire exact main")
    structure = Structure()
    structure.feed(candidate)
    require(sum(t == "main" for t, a in structure.tags) == sum(t == "h1" for t, a in structure.tags) == sum(t == "article" for t, a in structure.tags) == 1, "one main/article/title")
    frames = [a for t, a in structure.tags if t == "iframe"]
    require(len(frames) == 1 and frames[0]["src"] == "paper.pdf#view=FitH" and frames[0].get("title"), "accessible original PDF iframe")
    metas = {a.get("name"): a.get("content") for t, a in structure.tags if t == "meta" and "name" in a}
    require(metas["robots"] == "noindex,nofollow" and metas["citation_doi"] == "10.5281/zenodo.23418581" and metas["citation_version"] == "1.0", "private scholarly head")
    require(not any(t == "link" and a.get("rel") == "canonical" for t, a in structure.tags), "no production canonical introduced")
    scripts = [a for t, a in structure.tags if t == "script"]
    require(len(scripts) == 1 and scripts[0].get("type") == "application/ld+json" and "src" not in scripts[0], "no executable external script")
    require("background:#fff" in candidate and "Arial,Helvetica,sans-serif" in candidate and "@media(max-width:600px)" in candidate, "simple responsive white Arial layout")
    visible = " ".join(structure.text)
    copy_text = (A / "PUBLIC_COPY.md").read_text()
    for k in ("plain_language", "result", "why_it_works", "definitions_and_limits", "background"):
        for paragraph in c[k]:
            require(html.escape(paragraph) in main_text and paragraph in copy_text, "full public paragraph parity")
    for k in ("abstract", "collaboration", "ai_disclosure", "rights_notice", "reader_intro"):
        require(c[k] in visible and c[k] in copy_text, "full public wording parity")
    for forbidden in ("SOURCE_READY", "root-clearance", "preseal", "3136", "291-file", "NumPy2.3.5", "PASS1095", "checkpoint7da7"):
        require(forbidden not in visible, "no public internal custody/replay narrative")
    metadata = load(A / "SCHOLARLY_METADATA.json")
    require(metadata["abstract"] == c["abstract"] and metadata["url"] == "https://doi.org/10.5281/zenodo.23418581", "scholarly native identity")
    for name in ("promotion.json", "PUBLICATION_REQUIREMENTS.json", "SCHEMA_ADAPTER.json", "VERDICT.json"):
        obj = load(A / name)
        require(obj["production_authority"] is False and obj["canonical_url"] is None and obj["AA"] is None and obj["follow_up"] is None, "source-only interface boundary")
    build = load(A / "BUILD_RECEIPT.json")
    require(build["exit_code"] == 0 and build["first_render_is_current_render"] is True and build["rerender_count"] == 0, "actual first/current rendering history")
    require(pin(build["whole_stderr"]).read_bytes() == b"", "actual empty rendering stderr")
    require(json.loads(pin(build["whole_stdout"]).read_bytes())["status"] == "SOURCE_ONLY_EDITORIAL_RENDERED", "whole first rendering stdout")
    pin(build["helper"])
    return {"status": "PASS", "mode": "preseal" if preseal else "final", "checks": checks, "owned_payloads": len(names), "source_files": 291, "root_files": 29, "qualified_original_core_unchanged": 17, "authorized_checkpoint_SHA256": "405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0", "native_assets": 2, "candidate_leaves": 4, "project_imports_network_subprocess_writes_science": False}


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, separators=(",", ":")))
