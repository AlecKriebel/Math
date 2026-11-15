#!/usr/bin/env python3
"""Read-only offline closure for the bounded official-link proposal."""
from pathlib import Path
import hashlib
import json
import re

OWN = Path(__file__).resolve().parent
EXCLUDED = {"OWNED_MANIFEST.json", "FINAL_SEAL.json", "CLOSURE_RESULTS.json"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


inputs = json.loads((OWN/"INPUT_BINDINGS.json").read_text())
for item in inputs["original_bindings"]:
    p = Path(item["absolute_path"])
    require(p.is_file() and p.stat().st_size == item["bytes"] and sha(p) == item["sha256"], "Protected input changed")
receipts = json.loads((OWN/"HTTP_RECEIPTS.json").read_text())
require([x["HTTP_status"] for x in receipts] == [200,404], "Landing/dated URL status evidence changed")
for item in receipts+[json.loads((OWN/"POST_GET_RECEIPT.json").read_text())]:
    p = OWN/item["body_file"]
    require(p.stat().st_size == item["bytes"] and sha(p) == item["sha256"], "GET body/receipt mismatch")
    require(item["requested_url"] == item["final_url"], "Recorded final URL changed")
pdf = json.loads((OWN/"CURRENT_PDF_GET_RECEIPT.json").read_text())
require(pdf["HTTP_status"] == 200 and pdf["PDF_magic_verified"] is True and pdf["fresh_GET_exactly_matches_existing_cache"] is True, "Current PDF GET proof changed")
require(pdf["complete_response_sha256"] == sha(Path(pdf["reused_existing_immutable_native_cache_path"])) == "45420f88b0246f2558b581bf813184275972de2fd0a7c87cf4942f777c9d833d", "Current PDF/cache identity mismatch")
require(pdf["body_stored_in_new_folder"] is False and pdf["large_asset_written"] is False and pdf["bytes_streamed"] <= pdf["safety_max_bytes"], "Bounded GET condition changed")
links = json.loads((OWN/"OFFICIAL_NAVIGATION_LINKS.json").read_text())["extracted_actual_links"]
require(any(x["href"] == pdf["requested_url"] for x in links), "PDF URL not an actual homepage link")
scope = json.loads((OWN/"CLAIM_SCOPE.json").read_text())
require(scope["proposed_replacement_URL"] == "https://kourovkanotebookorg.wordpress.com/" and scope["current_problem_printed_and_physical_page"] == 201, "Proposed locator changed")
require(scope["source_paper_or_editorial_or_config_or_old_audit_edited"] is False and scope["science_authority_changed"] is False and scope["proposal_adopted"] is False and scope["publication_authority"] is False, "Authority boundary changed")
locator = json.loads((OWN/"CURRENT_PROBLEM_LOCATOR.json").read_text())
current = locator["exact_target_matches"][0]["target_question_only"]
historical = (OWN/"historical-oct06-problem-page.txt").read_text().split("21.149.",1)[1]
historical = "21.149."+historical.split("A. V. Zenkov",1)[0]+"A. V. Zenkov"
norm = lambda s: re.sub(r"\s+", " ", s).strip()
require(norm(current) == norm(historical), "Examined question-interface comparison changed")
require(locator["no_current_openness_or_solution_status_inference"] is True, "Unlicensed status inference")
if (OWN/"OWNED_MANIFEST.json").exists():
    manifest = json.loads((OWN/"OWNED_MANIFEST.json").read_text())
    actual = {str(f.relative_to(OWN)) for f in OWN.rglob("*") if f.is_file() and str(f.relative_to(OWN)) not in EXCLUDED}
    require(actual == {x["relative_path"] for x in manifest["files"]}, "Owned inventory mismatch")
    for item in manifest["files"]:
        p = OWN/item["relative_path"]
        require(p.stat().st_size == item["bytes"] and sha(p) == item["sha256"], "Owned proposal file changed")
if (OWN/"FINAL_SEAL.json").exists():
    seal = json.loads((OWN/"FINAL_SEAL.json").read_text())
    for key, name in (("owned_manifest_sha256","OWNED_MANIFEST.json"), ("input_bindings_sha256","INPUT_BINDINGS.json"), ("report_sha256","REPORT.md"), ("claim_scope_sha256","CLAIM_SCOPE.json"), ("closure_result_sha256","CLOSURE_RESULTS.json")):
        require(seal[key] == sha(OWN/name), "Final seal mismatch")
print(json.dumps({"status":"PASS_READ_ONLY_ADDITIVE_LINK_PROPOSAL", "protected_original_files_checked":len(inputs["original_bindings"]), "bounded_ordinary_GETs":4, "official_landing_status":200, "dated_asset_status":404, "current_PDF_status":200, "actual_current_problem_page":201, "historical_source_page":199, "question_interface_actually_compared":True, "network_or_writes_in_this_verifier":False, "original_or_science_authority_mutation":False, "proposal_adopted_or_published":False}, indent=2))
