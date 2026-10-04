"""Freeze actual review bindings; only writes this reviewer's folder."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess

A = Path(__file__).resolve().parent
R = Path("/Users/alec/Documents/Math")
P = A.parent / "publication_package_v3"
NOW = lambda: dt.datetime.now(dt.timezone.utc).isoformat()
def bind(path):
    body = path.read_bytes()
    return {"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest()}
source = Path(__file__).read_bytes()
(A / "PRELAUNCH_FREEZE_SOURCE.py").write_bytes(source)
run = json.loads((A / "REPRODUCTION.json").read_text())
commands = json.loads((A / "COMMANDS.json").read_text())
for record in commands:
    assert record["exit_code"] == 0
    for label in ("stdout","stderr"):
        saved = record[label]
        assert bind(A / saved["path"]) == {"bytes":saved["bytes"],"sha256":saved["sha256"]}
pins = {name:bind(P/name) for name in run["input_pins"]}
assert pins == run["input_pins"]
manifest = json.loads((A.parent / "ORIGINAL_MANIFEST.json").read_text())
original = {}
for item in manifest["files"]:
    path = A.parent / "original" / item["path"]
    observed = bind(path)
    assert observed == {"bytes":item["bytes"],"sha256":item["sha256"]}
    assert path.stat().st_mode & 0o7777 == item["snapshot_full_mode"]
    original[item["path"]] = observed
assert len(original) == 15
started = NOW()
argv = ["/opt/homebrew/bin/gh","pr","view","50","--repo","AlecKriebel/Math",
        "--json","number,title,state,isDraft,headRefOid,headRefName,baseRefName,url"]
child = subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
out,err = child.communicate()
receipt = {"argv":argv,"cwd":str(R),"child_pid":child.pid,"started_utc":started,
           "finished_utc":NOW(),"exit_code":child.returncode,"stdin_supplied":False,
           "separately_instrumented_child_timestamps":False}
for label,body in (("stdout",out),("stderr",err)):
    path = A/("current_pr50."+label+".bin")
    path.write_bytes(body)
    receipt[label] = {"path":path.name,**bind(path)}
(A/"CURRENT_PR_COMMAND.json").write_text(json.dumps(receipt,indent=2)+"\n")
assert child.returncode == 0
pr = json.loads(out)
assert pr["number"] == 50 and pr["headRefOid"] == manifest["head"]
assert pr["state"] == "OPEN" and pr["isDraft"] is True and pr["baseRefName"] == "main"
primary_base = A.parent/"current_promotion_adversary_20261004"/"private"
primary = {name:bind(primary_base/name) for name in
    ("survey.pdf","survey_publisher_correct.pdf","kamada.pdf","kl.pdf","gks.pdf",
     "nencka_scan_153.webp","nencka_scan_154.webp","nencka_scan_004.webp")}
bindings = {"UTC":NOW(),"operative_payload_pins":pins,"original_scientific_files":original,
            "primary_bodies_personally_read_at_relevant_pages":primary,
            "reproduction_record":bind(A/"REPRODUCTION.json"),
            "actual_command_receipts":bind(A/"COMMANDS.json"),
            "report":bind(A/"REPORT.md"),"current_remote_pr":pr,
            "current_remote_pr_command":bind(A/"CURRENT_PR_COMMAND.json")}
(A/"INPUT_PINS.json").write_text(json.dumps(bindings,indent=2)+"\n")
verdict = {"schema":"PR50-qualified-note-new-independent-round2/v1","UTC":NOW(),
    "reviewer":"/root/pr50_qualified_publication_round2_adversary",
    "review_started_from_scratch":True,"first_qualified_review_consulted":False,
    "verdict":"PASS_QUALIFIED_RESEARCH_NOTE_RELEASE","required_repairs":[],
    "mathematical_result":"PASS_CONDITIONAL_ON_EXPLICIT_ESTABLISHED_UNRESTRICTED_THEOREMS",
    "universal_soundness_and_completeness_personally_reconstructed":True,
    "new_central_proof_attempts":0,"original_turns_used":1,"original_turn_limit":5,
    "scope":"Ordinary oriented unframed nonempty classical and virtual closure, tagged even word states",
    "qualified_publication_authorized_by_human":True,"exception_applies_to_PR50_only":True,
    "priority_audit_complete":False,"historical_priority":"UNRESOLVED",
    "first_discovery_or_contemporary_openness_certified":False,
    "fuller_Nencka1998_1999_CPT1996_bodies_accessed":False,
    "human_peer_review":False,"formal_proof_certification":False,
    "global_priority_AI_unrefereed_disclosures_checked":True,
    "author_checker_exact_reproduction":True,"checks":7114,
    "independent_invariant_stress":run["independent_stress"],
    "archive_exact_ten_members_and_rebuild":True,
    "PDF_source_and_rebuilt_five_page_pixels_match":True,
    "all_five_pages_personally_visually_reviewed":True,"visual_defects_found":[],
    "metadata_license_authorship_support_consistent":True,
    "operative_payload_pins":pins,"input_bindings":bind(A/"INPUT_PINS.json"),
    "current_remote_head":pr["headRefOid"],"current_remote_PR_open_draft":True,
    "all_original_15_scientific_bytes_and_snapshot_modes_preserved":True,
    "review_completion_percent":100,"goal_completion_asserted":False,
    "upload_DOI_sheet_merge_or_native_acceptance_asserted":False,
    "Git_index_ref_native_PR_Zenodo_Sheets_outreach_mutated":False,
    "next_authorized_action":"Publish this exact qualified note with unresolved priority retained, then complete registration/merge/reconciliation and resume the original goal"}
(A/"VERDICT.json").write_text(json.dumps(verdict,indent=2)+"\n")
with (A/"RESEARCH_LOG.md").open("a") as log:
    log.write("\n"+NOW()+": Final checkpoint. Universal proof reconstructed; actual portable checker7114 exact, archive rebuilt exactly, all5 source/PDF page pixels match and personally inspected. Independent finite-field/crossing stress passed22829 pairs/68487 necessary comparisons. Fresh remotePR50 remains OPEN/draft at the pinned submitted head. All15 original bytes/modes retained. No substantive issue or required repair. Review100%; priority remains unresolved; broader goal/publication workflow not claimed complete. Zero new central attempts, no external or Git/native mutations.\n")
assert Path(__file__).read_bytes() == source
print(json.dumps(verdict,indent=2))
