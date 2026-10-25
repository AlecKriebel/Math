"""Source/editorial integrity checks only. No rendering, source writes or publication."""
from pathlib import Path, PurePosixPath
import argparse
import copy
import datetime
import hashlib
import json
import re
import stat
import subprocess
import sys
import zipfile

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[2]
E = Path(__file__).resolve().parent
R = P.parents[1]
sys.path.insert(0, str(R / "scripts"))
from published_assets import PublishedAssets

parser = argparse.ArgumentParser()
parser.add_argument("--output-stem", default="editorial-checks")
args = parser.parse_args()
assert re.fullmatch(r"[a-zA-Z0-9_-]+", args.output_stem)
output = E / (args.output_stem + ".json")
assert not output.exists(), "Choose a fresh output stem; never overwrite a prior check."


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snap(root):
    return {str(x.relative_to(P)): {"bytes": x.stat().st_size, "sha256": sha(x)}
            for x in sorted(root.rglob("*")) if x.is_file()}


def require(condition, name):
    if not condition:
        raise ValueError(name)


c = json.loads((P / "publication.json").read_text())
g = json.loads((P / "promotion.json").read_text())
b = c["source_binding"]
raw = json.loads((P / b["receipt_path"]).read_text())
record = json.loads((P / b["record_path"]).read_text())
clearance_path = R / g["root_clearance_file"]
clearance = json.loads(clearance_path.read_text())
source_tex = (P / b["source_tex_path"]).read_text()
abstract_tex = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", source_tex, re.S).group(1).strip()
abstract = " ".join(abstract_tex.replace("--", "–").split())
checks = {}


def test(name, value):
    checks[name] = bool(value)
    require(value, name)


def core(config, gate):
    binding = config["source_binding"]
    require(config["title"] == record["metadata"]["title"], "exact title")
    require(config["author"] == "Alec Kriebel" and config["orcid"] == "https://orcid.org/0009-0001-9320-500X", "author and ORCID")
    require(config["doi"] == record["doi"] == "10.5281/zenodo.23203100", "record DOI")
    require(config["version"] is None and binding["zenodo_version"] is None and binding["manuscript_version"] is None and "version" not in record["metadata"], "no invented version")
    require(config["publication_date"] == record["metadata"]["publication_date"] == binding["manuscript_date"] == "2026-10-06", "declared manuscript date")
    require(config["publication_date_label"] == "Manuscript dated" and config["edition_label"] == config["citation_edition_label"] == "No version number supplied", "honest visible labels")
    require(binding["record_created_utc"] == record["created"] == "2026-10-07T04:42:47.312983+00:00", "separate creation date")
    require(config["abstract"] == abstract and len(abstract.split()) == 146, "complete original abstract")
    require(config["follow_up"] is None and gate["follow_up"] is None, "null followup")
    require(config["canonical_url"] == "https://aleckriebel.com/research/" + config["slug"] + "/", "slug canonical")
    require(gate["root_clearance_record"] == clearance and gate["root_clearance_sha256"] == sha(clearance_path) == "e186543476c3a507b7ba5fc59df50432963efce03d6791015eb8f48becb61ca6", "root authority")
    require(gate["approved_scope"] == clearance["approved_scope"] and gate["scope_gate_resolution"] == clearance["scope_gate_resolution"], "literal root scope")
    require(set(gate["reviews"]) == {"scope", "analytic", "adversarial", "upstream_analytic", "upstream_adversarial"}, "five independent families")
    for family, review in gate["reviews"].items():
        require(review["sha256"] == sha(P/review["report"]) == clearance["reviews"][family]["report_sha256"], family+" report")
        require(review["verdict_sha256"] == sha(P/review["verdict_file"]) == clearance["reviews"][family]["verdict_sha256"], family+" verdict bytes")
        require(review["verdict"] == json.loads((P/review["verdict_file"]).read_text()), family+" original verdict object")
    require(gate["source_receipt_sha256"] == binding["source_receipt_sha256"] == binding["receipt_sha256"] == sha(P/binding["receipt_path"]) == clearance["source_receipt_sha256"], "raw receipt binding")
    require(gate["source_files"] == binding["files"], "derived original-layout bindings")
    for item in binding["files"]:
        require(sha(P/item["source_relative_path"]) == item["sha256"], "original asset hash")
    require(gate["source_repair"] is gate["human_peer_review"] is gate["formal_machine_verification"] is False, "no source repair/human/formal claims")


core(c, g)
test("core_source_and_original_verdict_bindings", True)
test("publication_hash_in_promotion", g["publication_sha256"] == sha(P/"publication.json"))
test("metadata_raw_hash", b["metadata_sha256"] == b["record_sha256"] == g["metadata_sha256"] == sha(P/b["record_path"]) == "023aff8aa7f44ba7e522b3d557bbbe9eaaff060990c8b8032c93aed794e78778")
test("original_transport_list_schema", isinstance(raw, list) and len(raw) == 3 and {x["saved"] for x in raw} == {"record/zenodo_record.json", "assets/paper.pdf", "assets/zenodo-upload-kit.zip"} and all(x["status"] == 200 for x in raw))
for item in raw:
    path = P/"sources"/item["saved"]
    test("receipt_" + item["saved"], path.is_file() and sha(path) == item["sha256"] and path.stat().st_size == item["bytes"])
for item in b["files"]:
    api = next(x for x in record["files"] if x["key"] == item["filename"])
    raw_item = raw[item["receipt_index"]]
    data = (P/item["source_relative_path"]).read_bytes()
    test("api_receipt_match_" + item["filename"], api["links"]["self"] == item["url"] == raw_item["url"] and api["size"] == item["bytes"] == len(data) and api["checksum"] == item["api_checksum"] == raw_item["record_checksum"] == "md5:"+hashlib.md5(data).hexdigest() and item["md5"] == hashlib.md5(data).hexdigest())
    test("safe_original_asset_" + item["filename"], item["source_relative_path"] == "sources/assets/"+item["filename"] and all(not x.startswith(".") for x in PurePosixPath(item["source_relative_path"]).parts) and not (P/item["source_relative_path"]).is_symlink())

assets = PublishedAssets(P/b["asset_root"], {"record_id": "23203100", "files": b["files"]}, [])
for name in [c["pdf_filename"], c["supplement_filename"]]:
    resolved = assets.resolve(name)
    test("existing_asset_helper_in_memory_view_"+name, resolved.read_bytes() == (P/"sources/assets"/name).read_bytes())

test("tex_and_abstract_hashes", sha(P/b["source_tex_path"]) == b["source_tex_sha256"] == b["abstract_source_sha256"] == "eda0b20fb843fda3b7b70203b63628e36ebf5d4a1b6c817624d3a5810f9beaab" and hashlib.sha256(abstract_tex.encode()).hexdigest() == b["abstract_tex_sha256"] and hashlib.sha256(abstract.encode()).hexdigest() == b["abstract_sha256"])
scope = json.loads((P/b["frozen_scope_content_path"]).read_text())
test("frozen_scope_original_abstract", scope["abstract"] == abstract == (E/"ABSTRACT.txt").read_text().strip() == (P/"reviews/scope/ORIGINAL_ABSTRACT.txt").read_text().strip() and sha(P/b["frozen_scope_content_path"]) == b["frozen_scope_content_sha256"])
test("date_and_no_version_in_tex", r"\date{October 6, 2026}" in source_tex and not re.search(r"(?i)\\date\{[^}]*version", source_tex))
test("eight_abstract_sentences", len(re.findall(r"\.(?:\s|$)", abstract)) == 8)
test("metadata_description_not_substituted", c["abstract"] != record["metadata"]["description"])

for item in clearance["root_review_seals_rehashed"]:
    test("original_review_seal_"+Path(item["path"]).parent.name, sha(R/item["path"]) == item["sha256"])
test("root_custody_receipt", sha(R/clearance["root_custody_receipt"]) == clearance["root_custody_receipt_sha256"])
test("actual_upstream_pdf_identity", sha(P/"sources/primary/.cache/openai-epni-pinned.pdf") == clearance["upstream"]["pdf_sha256"])
test("original_conditionality_preserved", g["reviews"]["scope"]["verdict"]["mathematical_verdict"] is None and g["reviews"]["analytic"]["verdict"]["publication_clearance"] is False and g["reviews"]["adversarial"]["verdict"]["unconditional_global_capacity_clearance"] is False)
test("later_dependency_resolution_separate", g["reviews"]["upstream_analytic"]["verdict"]["verdict"] == "PASS" and g["reviews"]["upstream_adversarial"]["verdict"]["verdict"] == "PASS_UPSTREAM_REQUIRED_VE" and "current_mathematical_disposition" in g["dependency_resolution"])

archive = P/"sources/assets/zenodo-upload-kit.zip"
archive_names = []
with zipfile.ZipFile(archive) as z:
    for info in z.infolist():
        require(not info.is_dir() and not stat.S_ISLNK(info.external_attr >> 16), "regular archive member")
        parts = PurePosixPath(info.filename).parts
        require(parts and not PurePosixPath(info.filename).is_absolute() and all(x not in (".", "..") and not x.startswith(".") for x in parts) and "\\" not in info.filename, "safe ZIP path")
        data = z.read(info)
        require(data == (P/"sources/extracted/zenodo-upload-kit"/info.filename).read_bytes(), "archive/extracted identity")
        archive_names.append(info.filename)
test("forty_regular_members_exactly_match_extraction", len(archive_names) == len(set(archive_names)) == 40 and all(not x.lower().endswith((".pdf", ".zip", ".tar", ".gz")) for x in archive_names))

fresh = subprocess.run(["pdftotext", "-layout", str(P/"sources/assets/paper.pdf"), "-"], check=True, capture_output=True).stdout
info = subprocess.run(["pdfinfo", str(P/"sources/assets/paper.pdf")], check=True, capture_output=True, text=True).stdout
test("fresh_searchable_seven_page_pdf", re.search(r"^Pages:\s+7$", info, re.M) is not None and fresh.count(b"\x0c") == 7 and all(len(x.split()) > 20 for x in fresh.split(b"\x0c")[:7]))
test("fresh_extraction_matches_both_saved_copies", fresh == (P/"sources/assets/paper.pdf.txt").read_bytes() == (E/"published-pdf-fresh.txt").read_bytes())

result_text = " ".join(c["result"])
expected_formulas = ["C+2Q ≤ g(λN)+g(ηN)−g((1−η)λN)", "Q+E ≤ g(ηλN)−g((1−η)λN)", "C+Q+E ≤ g(ηN)−g((1−η)λN)", "R+P ≤ g(ηN)", "P+S ≤ g(ηλN)−g((1−η)λN)", "R+P+S ≤ g(ηN)−g((1−η)λN)"]
test("all_six_exact_region_inequalities", all(x in result_text for x in expected_formulas))
test("literal_obstruction_and_GEN_both_explicit", all(x in result_text for x in ["1 ≤ 1/(d_M d_T_A)+(ε_sec+ε_rel)/2", "2(1−1/d)", "W=(M,T_A)", "V=(J,S_B)", "traced out", "Eve does not additionally receive", "corrected model’s region"]))
test("public_scope_disclosures", all(any(x in p for p in c["limitations"]) for x in ["finite N", "averaged over", "finite gross", "logarithmic dimensions O(n)", "No peak", "semantic-security", "unrefereed EPnI proof", "Wilde, Hayden and Guha"]) and "used extensively" in c["ai_disclosure"] and "human or journal peer review" in c["ai_disclosure"] and "No reproduced Lean build or proof-assistant certification is claimed" in c["ai_disclosure"] and "actual research contributions" in c["collaboration"])
test("public_implementation_audit_details_removed_abstract_untouched", all(x not in " ".join(c["limitations"]) for x in ["formal-source theorem interface", "axiom closure", "comparator", "sorry"]) and c["abstract"] == abstract and "Its analytical arguments and formal-source semantics were audited, but its Lean build was not reproduced." in c["abstract"])

public_keys = ["title", "description", "abstract", "plain_language", "result", "why_it_works", "limitations", "background", "collaboration", "ai_disclosure", "edition_note", "edition_label", "citation_edition_label", "related_resources", "bibtex_note"]
public_text = json.dumps({k:c[k] for k in public_keys}, ensure_ascii=False)
test("no_private_audit_narrative", all(x not in public_text for x in ["2026-10-25", "root-clearance", "reviews/editorial", "92 frozen", "40 regular", "8170b3100a1e00bb", "BINDINGS_READY", "/Users/"]) and re.search(r"\b[0-9a-f]{64}\b", public_text) is None)
test("publication_gates_pending", c["review_metadata"]["rendered"] is c["review_metadata"]["deployed"] is False and all(g[x] is False for x in ["rendered_public_copy_approved", "live_http_verified", "browser_verified", "native_sheet_publication_verified"]))

baseline = json.loads((E/"frozen-before.json").read_text())
after_sources = snap(P/"sources")
after_reviews = {str(x.relative_to(P)): {"bytes": x.stat().st_size, "sha256": sha(x)}
                 for x in sorted((P/"reviews").rglob("*")) if x.is_file() and not x.is_relative_to(E)}
test("all_92_sources_unchanged", len(after_sources) == 92 and after_sources == baseline["sources"])
test("all_original_review_files_unchanged", after_reviews == baseline["original_reviews"])
test("no_source_aliases_added", not (P/"sources/receipt.json").exists() and not (P/"sources/record.json").exists() and not (P/"sources/paper.pdf").exists())

mutants = []
def mutation(name, mutate):
    cc, gg = copy.deepcopy(c), copy.deepcopy(g)
    mutate(cc, gg)
    try:
        core(cc, gg)
    except (ValueError, KeyError, TypeError) as err:
        mutants.append({"name": name, "rejected": True, "reason": str(err)})
    else:
        raise ValueError("Undetected mutation: "+name)

mutation("invent_v1", lambda cc,gg: cc.update(version="1.0"))
mutation("replace_manuscript_date_with_creation", lambda cc,gg: cc.update(publication_date="2026-10-07"))
mutation("truncate_abstract", lambda cc,gg: cc.update(abstract=cc["abstract"].split(" We rely")[0]))
mutation("wrong_DOI", lambda cc,gg: cc.update(doi="10.5281/zenodo.23203099"))
mutation("rewrite_original_scope_verdict", lambda cc,gg: gg["reviews"]["scope"]["verdict"].update(mathematical_verdict="PASS"))
mutation("rewrite_original_conditional_review", lambda cc,gg: gg["reviews"]["adversarial"]["verdict"].update(unconditional_global_capacity_clearance=True))
mutation("omit_later_upstream_review", lambda cc,gg: gg["reviews"].pop("upstream_analytic"))
mutation("corrupt_asset_hash", lambda cc,gg: cc["source_binding"]["files"][0].update(sha256="0"*64))
mutation("replace_raw_receipt_hash_with_normalized_hash", lambda cc,gg: gg.update(source_receipt_sha256="0"*64))

output.write_text(json.dumps({"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "status": "PASS_EDITORIAL_BINDINGS_ONLY", "check_count": len(checks), "checks": checks, "mutation_controls": mutants, "source_file_count": len(after_sources), "original_review_file_count": len(after_reviews), "archive_regular_members": len(archive_names), "publication_sha256": sha(P/"publication.json"), "promotion_sha256": sha(P/"promotion.json"), "limits": "Pre-render source/editorial checks only; no mathematical re-proof, site render, shared checker pass, live/browser verification, native Sheet update, Git action or publication."}, ensure_ascii=False, indent=2)+"\n")
(E/(args.output_stem+"-custody-after.json")).write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(), "sources":after_sources, "original_reviews":after_reviews, "unchanged":True},indent=2)+"\n")
print(json.dumps({"status":"PASS_EDITORIAL_BINDINGS_ONLY", "checks":len(checks), "mutations_rejected":len(mutants), "output":str(output)}))
