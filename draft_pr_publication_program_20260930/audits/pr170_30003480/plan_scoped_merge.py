"""Freeze concrete selected publication/native bodies after actual publication."""
from pathlib import Path
import datetime,hashlib,json
A=Path(__file__).resolve().parent;C=A.parents[2]
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {"local_path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest(),"git_blob":hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()}
def main():
 gate=json.loads((A/"ROOT_PUBLICATION_GATE.json").read_text());pub=json.loads((A/"ZENODO_PUBLICATION_READBACK.json").read_text());tracker=json.loads((A/"TRACKER_ACCEPTANCE.json").read_text())
 require(gate["status"]=="READY_FOR_AUTHORIZED_PUBLICATION" and gate["fresh_seal_first_review_clean"],"Scientific gate required")
 require(pub["state"]=="published" and pub["doi"]==tracker["DOI"] and tracker["DOI_count"]==1,"Actual publication/tracker required")
 selected={}
 def add(repo,p):
  require(p.is_file() and not p.is_symlink(),"Missing own ordinary path "+str(p))
  require(not any(part in ["private","scratch","__pycache__", ".secrets",".zenodo-state","gws_generated_reference"] for part in Path(repo).parts),"Private path selected")
  selected[repo]=pin(p)
 names=["ROOT_PUBLICATION_GATE.json","ROOT_R1_AUTHENTICATION.json","ROOT_R2_INITIAL_SEAL_OBSERVATION.json","ROOT_WHOLE_PACKAGE_R2_AUTHENTICATION.json","CURRENT_CASE_STATUS.json","RESEARCH_LOG.md","PACKAGE_V1_PREPARATION.json","PACKAGE_V2_PREPARATION.json","ROOT_V2_PACKAGE_REPRODUCTION.json","PR_BODY_ACCEPTED.md","PR_METADATA_ACCEPTANCE.json","ZENODO_STAGE_READBACK.json","ZENODO_DRAFT_READBACK.json","ZENODO_PUBLICATION_RESPONSE.json","ZENODO_PUBLICATION_READBACK.json","TRACKER_ACCEPTANCE.json","TRACKER_READ_ONLY_PREPARATION.json","ZENODO_PUBLIC_DOWNLOAD_ACCEPTANCE.json","AUDIT_CHECKPOINT_ACCEPTANCE.json","integration_preparation/CURRENT_TEMPLATE.json","zenodo-deposit.v2.json","run_zenodo.py","append_tracker.py","prepare_accepted_native.py","plan_scoped_merge.py","prepare_scoped_merge.py","accept_scoped_merge.py","final_checkpoint.py","accept_final_checkpoint.py","verify_publication_files.py"]
 names += ["ROOT_PUBLICATION_TRANSPORT_GATE.json","ZENODO_HTML_REPRESENTATION_DIAGNOSTIC.json","ROOT_ZENODO_DESCRIPTION_GUARD_CONTROLS.json","zenodo_exact_description_guard.py","test_zenodo_description_guard.py","authenticate_transport_and_gate.py","accept_pr_metadata.py"]
 for n in names:
  p=A/n;add(str(p.relative_to(C)),p)
 for family in ["whole_package_r1","whole_package_r2"]:
  D=A/family;allow=D/("PUBLIC_ALLOWLIST.json" if family=="whole_package_r1" else "PUBLICATION_ALLOWLIST.json");j=json.loads(allow.read_text())
  names=j.get("allowlisted_paths",j.get("included_paths",j.get("allowed_relative_paths",j.get("public_output_whitelist"))))
  require(isinstance(names,list),"Unrecognized reviewer public allowlist")
  for n in names: add(str((D/n).relative_to(C)),D/n)
 D=A/"zenodo_transport_adversary"
 for n in json.loads((D/"PUBLIC_ALLOWLIST.json").read_text())["allowlisted_files"]:add(str((D/n).relative_to(C)),D/n)
 K=A/gate["package"]
 for p in K.rglob("*"):
  if p.is_file():add(str(p.relative_to(C)),p)
 N=A/"integration_preparation/native_accepted";prefix="unsolved_math_prioritization/attempts/30003480/"
 for p in N.rglob("*"):
  if p.is_file():add(prefix+str(p.relative_to(N)),p)
 originals=json.loads((A/"ORIGINAL_FILE_MANIFEST.json").read_text())["files"]
 deletion=[v["repo_path"] for v in originals if v["repo_path"] not in selected]
 base="draft_pr_publication_program_20260930/"
 finals=[base+n for n in ["CURRENT_PROGRESS.json","CURRENT_PROGRESS.md","RESEARCH_LOG.md"]]
 finals+=[prefix+n for n in ["README.md","COUNTEREXAMPLE.md","readiness.json","RESEARCH_LOG.md","source_record.json","audit_status.json","upstream_report.json","SHA256SUMS"]]
 finals+=[str((A/n).relative_to(C)) for n in ["WORKFLOW_COMPLETION.json","CURRENT_CASE_STATUS.json","RESEARCH_LOG.md","MERGE_AND_NATIVE_ACCEPTANCE.json","SCOPED_MERGE_PREPARATION.json","PR_BODY_MERGED.md","PR_METADATA_MERGED_ACCEPTANCE.json","integration_preparation/CURRENT_TEMPLATE.json"]]
 result={"UTC":datetime.datetime.now(datetime.UTC).isoformat(),"status":"FROZEN_PUBLISHED_REVIEWED_MERGE_SCOPE_NO_REMOTE_OBJECTS","PR":170,"original_head":"d04c7991532ef65d70782c7d7fdfc1dcbfdf90a7","selected_files":selected,"selected_bytes":sum(v["bytes"] for v in selected.values()),"conditional_original_native_deletions":deletion,"programme_metadata_paths":[base+n for n in ["CURRENT_PROGRESS.json","CURRENT_PROGRESS.md","RESEARCH_LOG.md"]],"QUEUE_path":"unsolved_math_prioritization/QUEUE.md","QUEUE_target_problem_id":30003480,"QUEUE_rows_changed":1,"merge_parent_order":["fresh actual granted MAIN","d04c7991532ef65d70782c7d7fdfc1dcbfdf90a7"],"post_merge_fact_only_metadata_scope":finals,"DOI":pub["doi"],"tracker_range":tracker["range"],"requires_fresh_explicit_bounded_MAIN_acknowledgement":True,"all_other_actual_MAIN_paths_preserved":True,"exclusive_priority_or_mutual_independence_certified":False,"remote_objects_or_ref_mutations":False}
 p=A/"SCOPED_MERGE_SCOPE_PLAN.json";require(not p.exists(),"Existing plan cannot be silently replaced");p.write_text(json.dumps(result,indent=2)+"\n")
 print(json.dumps({"plan":str(p),"sha256":pin(p)["sha256"],"selected_paths":len(selected),"selected_bytes":result["selected_bytes"],"conditional_deletions":len(deletion),"programme_paths":3,"QUEUE_rows":1,"fact_only_postscope_paths":len(finals),"DOI":pub["doi"]}))
if __name__=="__main__":main()
