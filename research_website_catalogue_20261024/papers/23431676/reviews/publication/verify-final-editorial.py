"""Read-only checks of completed paper-specific editorial bindings.

Writes only EDITORIAL_QA.json in this owned publication review folder.
Does not render, execute mathematical helpers, or modify any input.
"""
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys
import zipfile

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[4]
PAPER = ROOT / "papers/23431676"
OWNED = PAPER / "reviews/publication"
GOAL = Path("/Users/alec/.codex/attachments/97d02095-52a0-400f-a038-cbc727c7c885/goal-objective.md")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


checks = []


def check(name, passed, detail=None):
    result = {"name": name, "passed": bool(passed)}
    if detail is not None:
        result["detail"] = detail
    checks.append(result)
    if not passed:
        raise ValueError(name)


publication_path = PAPER / "publication.json"
promotion_path = PAPER / "promotion.json"
receipt_path = PAPER / "sources/receipt.json"
record_path = PAPER / "sources/record.json"
clearance_path = ROOT / "verification/root-clearance-23431676-20261025.json"
publication = read(publication_path)
promotion = read(promotion_path)
draft = read(OWNED / "publication.draft.json")
receipt = read(receipt_path)
record = read(record_path)
clearance = read(clearance_path)
before = read(OWNED / "finalization-preservation-before.json")["files"]

check("root_clearance_exact_object", promotion["root_clearance_record"] == clearance)
check("root_clearance_PASS", clearance["status"] == promotion["status"] == "PASS"
      and clearance["disposition_by"] == promotion["disposition_by"] == "root"
      and clearance["record_id"] == promotion["record_id"] == "23431676")
check("root_clearance_hashes", sha(clearance_path)
      == promotion["root_clearance_sha256"]
      == publication["review_metadata"]["root_clearance_sha256"])
check("root_scope_and_authorization", promotion["approved_scope"] == clearance["approved_scope"]
      and promotion["root_clearance"] == clearance["authorization"]
      and promotion["scope_gate_resolution"] == clearance["scope_gate_resolution"])
check("final_publication_hash", sha(publication_path) == promotion["publication_sha256"])
check("raw_receipt_shape_preserved", "assets" in receipt and "files" not in receipt)
check("raw_receipt_binding", sha(receipt_path)
      == clearance["source_receipt_sha256"]
      == promotion["source_receipt_sha256"]
      == publication["source_binding"]["source_receipt_sha256"]
      == publication["source_binding"]["receipt_sha256"])
check("raw_asset_field_recorded", promotion["source_receipt_asset_field"]
      == publication["source_binding"]["receipt_asset_field"] == "assets")
check("complete_original_asset_objects", promotion["source_files"]
      == publication["source_binding"]["files"] == receipt["assets"])
check("metadata_binding", sha(record_path) == receipt["record_sha256"]
      == publication["source_binding"]["metadata_sha256"])

assets = receipt["assets"]
check("exact_two_downloads", len(assets) == 2
      and {a["name"] for a in assets} == {"paper.pdf", "pr1097_support_v1_0.zip"}
      and publication["pdf_filename"] == "paper.pdf"
      and publication["supplement_filename"] is None
      and publication["additional_assets"]
      == [{"filename": "pr1097_support_v1_0.zip", "label": "Source and verification package (ZIP)"}])
for asset in assets:
    path = PAPER / "sources" / asset["name"]
    raw = path.read_bytes()
    check("asset_" + asset["name"], len(raw) == asset["bytes"]
          and hashlib.sha256(raw).hexdigest() == asset["sha256"]
          and hashlib.md5(raw).hexdigest() == asset["md5"])
    copies = [a for a in publication["source_binding"]["all_public_assets"]
              if a["filename"] == asset["name"]]
    check("public_asset_binding_" + asset["name"], len(copies) == 1
          and all(copies[0][key] == asset[key] for key in ("bytes", "sha256", "md5", "url")))
check("pdf_binding", sha(PAPER / "sources/paper.pdf") == promotion["pdf_sha256"]
      == clearance["pdf_sha256"] == publication["source_binding"]["pdf_sha256"])

extraction = read(PAPER / "sources/extraction-integrity.json")
with zipfile.ZipFile(PAPER / "sources/pr1097_support_v1_0.zip") as archive:
    check("archive_CRC", archive.testzip() is None)
    check("all_198_archive_members", len(archive.infolist())
          == len(extraction["regular_files"]) == 198)
    for member in extraction["regular_files"]:
        raw = archive.read(member["member"])
        check("member_" + member["member"], raw == Path(member["path"]).read_bytes()
              and len(raw) == member["bytes"]
              and hashlib.sha256(raw).hexdigest() == member["sha256"])

tex_path = PAPER / publication["source_binding"]["source_tex_path"]
tex = tex_path.read_text()
abstract_tex = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.S).group(1)
abstract = " ".join(abstract_tex.replace("T\\'othm\\'er\\'esz", "Tóthmérész").split())
check("complete_exact_original_abstract", publication["abstract"] == draft["abstract"] == abstract)
check("abstract_125_words", len(abstract.split())
      == publication["source_binding"]["abstract_word_count"] == 125)
check("TeX_binding", sha(tex_path) == publication["source_binding"]["source_tex_sha256"]
      == publication["source_binding"]["abstract_source_sha256"])
check("printed_date_version", r"\date{15 October 2026, version 1.0}" in tex)

for role, bound in clearance["reviews"].items():
    entry = promotion["reviews"][role]
    report = ROOT / bound["report"]
    verdict = ROOT / bound["verdict"]
    check(role + "_paper_relative_report", entry["report"] == str(report.relative_to(PAPER)))
    check(role + "_paper_relative_verdict", entry["verdict_file"] == str(verdict.relative_to(PAPER)))
    check(role + "_exact_report_hash", sha(report) == bound["report_sha256"] == entry["sha256"])
    check(role + "_exact_verdict_hash", sha(verdict) == bound["verdict_sha256"] == entry["verdict_sha256"])
    check(role + "_complete_original_verdict_object", entry["verdict"] == read(verdict))
check("frozen_scope_pending_verdict_retained",
      promotion["reviews"]["scope"]["verdict"]["status"] == "SCOPE_COMPLETE_MATHEMATICAL_REVIEW_PENDING"
      and promotion["reviews"]["scope"]["verdict"]["publication_authorized"] is False
      and promotion["reviews"]["scope"]["root_disposition"] == "SCOPE_COMPLETE")
check("all_275_immutable_inputs_unchanged", len(before) == 275
      and all((PAPER / name).stat().st_size == bound["bytes"]
              and sha(PAPER / name) == bound["sha256"] for name, bound in before.items()))

# The completed config retains the source-bound draft copy, with one explicit
# manuscript convention and the later root/provenance state only.
expected = deepcopy(draft)
expected.pop("candidate_only")
expected.pop("candidate_gate")
expected["result"][1] += " In the one-vertex loopless case, reachability is exactly equality of the two configurations."
for key in ("files", "receipt_asset_field", "source_receipt_sha256", "review_boundary", "publication_state"):
    expected["source_binding"][key] = deepcopy(publication["source_binding"][key])
expected["review_metadata"] = deepcopy(publication["review_metadata"])
check("only_authorized_changes_from_frozen_draft", expected == publication)
result = " ".join(publication["result"])
check("precise_multigraph_language", "finite nonempty loopless strongly connected directed multigraphs" in result
      and all(term in result for term in ("nonnegative", "binary", "empty firing word", "may stop",
                                          "Malformed inputs", "number of vertices varies", "one-vertex")))
check("credited_HKT_membership", "Prior work by Hujter, Kiss and Tóthmérész supplies coNP membership" in result)
check("arbitrary_target_words_and_bit_complexity", "every target-reaching word" in " ".join(publication["why_it_works"])
      and "polynomially many bits" in " ".join(publication["why_it_works"]))
check("bounded_scope_no_extension", all(term in " ".join(publication["limitations"])
      for term in ("simple graphs", "unary encodings", "bounded degrees", "bounded total chip counts",
                   "Signed intermediate", "not the running time", "Priority")))
policy = clearance["publication_date_policy"]
check("exact_manuscript_date_label", publication["publication_date"]
      == record["metadata"]["publication_date"] == policy["publication_date"] == "2026-10-15"
      and publication["publication_date_label"] == policy["publication_date_label"] == "Manuscript dated")
check("separate_exact_record_creation", publication["source_binding"]["record_created_utc"]
      == record["created"] == policy["record_created_utc"] == "2026-10-17T05:45:36.045033+00:00")
check("no_backdated_availability_or_priority", all(term in publication["edition_note"]
      for term in ("15 October 2026", "created on 17 October 2026", "not verified public availability",
                   "Neither date establishes first priority")))
check("version_identity", publication["version"] == publication["source_binding"]["zenodo_version"]
      == record["metadata"]["version"] == "1.0")
check("null_follow_up", publication["follow_up"] is promotion["follow_up"] is clearance["follow_up"] is None)
check("professional_collaboration", "actual research contributions" in publication["collaboration"])
check("AI_unrefereed_disclosure", "Unrefereed preprint" in publication["status"]
      and "extensively" in publication["ai_disclosure"]
      and "external human peer review" in publication["ai_disclosure"]
      and promotion["human_peer_review"] is promotion["formal_machine_verification"] is False)
check("no_source_repair", promotion["source_repair"] is clearance["source_repair"] is False)
check("render_and_deployment_still_pending", publication["review_metadata"]["rendered"]
      is publication["review_metadata"]["deployed"] is False
      and publication["review_metadata"]["publication_state"]
      == promotion["preparation_state"] == "BINDINGS_READY_RENDERING_PENDING")
prior = read(OWNED / "finalization-checks.json")
check("prior_finalization_receipt_still_current", prior["all_checks_passed"]
      and all(item["passed"] for item in prior["checks"])
      and prior["publication_sha256"] == sha(publication_path)
      and prior["promotion_sha256"] == sha(promotion_path))

# Import only the local, dependency-free receipt proposal; no shared pipeline.
spec = importlib.util.spec_from_file_location("receipt_proposal", OWNED / "receipt-normalization-proposal.py")
proposal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(proposal)
raw_before = deepcopy(receipt)
view = proposal.normalized_receipt_view(receipt)
check("normalization_exact_complete_view", view["files"] == receipt["assets"])
view["files"][0]["name"] = "VIEW_ONLY_NEGATIVE_CONTROL"
check("normalization_no_input_mutation", receipt == raw_before and sha(receipt_path) == promotion["source_receipt_sha256"])
rejections = 0
for bad in ({}, {"assets": None}, {"assets": ["bad"]}, {"files": [], "assets": [{"name": "a"}]}):
    try:
        proposal.normalized_receipt_view(bad)
    except ValueError:
        rejections += 1
check("normalization_four_negative_controls", rejections == 4)

output = {
    "utc": datetime.now(timezone.utc).isoformat(),
    "record_id": "23431676",
    "agent": "/root/sol_reach_editor",
    "requested_model": "gpt-6.1-sol",
    "requested_reasoning_effort": "ultra",
    "status": "EDITORIAL_BINDINGS_READY_RENDERING_PENDING",
    "completion_percent": 100,
    "scope": "Editorial verification of actual completed configs; no new mathematical review or publication action.",
    "all_checks_passed": all(item["passed"] for item in checks),
    "check_count": len(checks),
    "checks": checks,
    "source_asset_count": len(assets),
    "archive_members_compared": 198,
    "immutable_input_files_rehashed": len(before),
    "previous_finalization_checks": len(prior["checks"]),
    "public_abstract_words": len(abstract.split()),
    "publication_sha256": sha(publication_path),
    "promotion_sha256": sha(promotion_path),
    "source_receipt_sha256": sha(receipt_path),
    "root_clearance_sha256": sha(clearance_path),
    "goal_objective_sha256": sha(GOAL),
    "model_policy_sha256": sha(ROOT / "MODEL_POLICY.md"),
    "scientific_helpers_executed": False,
    "finalizer_restarted": False,
    "raw_receipt_modified": False,
    "shared_code_modified_or_executed": False,
    "rendered": False,
    "deployed": False,
    "sheet_ui_git_redirect_outreach_actions": False,
    "descendant_agents_started": False,
}
(OWNED / "EDITORIAL_QA.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: output[key] for key in ("status", "all_checks_passed", "check_count",
                 "publication_sha256", "promotion_sha256", "immutable_input_files_rehashed")}, indent=2))
