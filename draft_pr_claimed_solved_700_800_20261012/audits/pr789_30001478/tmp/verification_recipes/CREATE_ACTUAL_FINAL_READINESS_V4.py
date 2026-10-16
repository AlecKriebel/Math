from pathlib import Path
import datetime,hashlib,importlib.util,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";P=T/"preprint"
assert json.loads((T/"FINAL_READINESS.json").read_text())["result"]=="PENDING_FRESH_WHOLE04_CANONICAL_METADATA","Only the exact retired V3 authorization may be replaced"
plan=json.loads((T/"READINESS_PLAN.json").read_text());peer=json.loads((M/"WHOLE04_ROOT_REPLAY.json").read_text());inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
assert peer["result"]=="PASS"and peer["completed"]is True and peer["review_actionable_issues"]==0 and peer["freshly_initialized"]is True
assert peer["source_manifest_sha256"]==inv["source_manifest_sha256"]=="b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa"and peer["publication_files"]==inv["files"]
assert len(plan["completed_whole_reviews"])==3 and plan["actual_whole_preprint_rounds"]==3
row={"round":4,"reviewer":peer["reviewer"],"freshly_initialized":True,"packet":"whole_preprint_round04","manifest_sha256":peer["manifest_sha256"],"checker_name":peer["checker_name"],"checker_sha256":peer["checker_sha256"],"root_replay_receipt":"root-receipts/WHOLE04_ROOT_REPLAY.json","root_replay_sha256":hashlib.sha256((M/"WHOLE04_ROOT_REPLAY.json").read_bytes()).hexdigest(),"reviewed_source_manifest_sha256":peer["source_manifest_sha256"],"reviewed_publication_files":peer["publication_files"],"actionable_issues":0}
assert json.loads((M/"MATH_GATE.json").read_text())["result"]=="PASS"
assert json.loads((M/"PRIORITY_GATE.json").read_text())["known_full_predecessors"]==[]
for n in["ROOT_RELEASE_REPRODUCTION_V4.json","ROOT_ARCHIVE_PORTABILITY_V4.json"]:
 assert json.loads((M/n).read_text())["result"]=="PASS"
g=dict(plan);g.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),result="PASS",actual_whole_preprint_rounds=4,completed_whole_reviews=plan["completed_whole_reviews"]+[row],final_current_round_clean=True,paper_ready=True,source_checker_sha256="700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489",native_acceptance_state="NEXT_AFTER_PUBLICATION_TRACKER_AND_EXACT_MERGE",PR_completion_estimate_percent=90,shard_completion_estimate_percent=83,publication_status="SOLE_KNOWN_DRAFT_23423736_READY_FOR_REPAIR_AND_PUBLICATION",publication_created=True,known_unpublished_draft_id=23423736,known_deposition_creations=1,published=False,known_full_predecessors=[],priority_status="PRIORITY_UNRESOLVED",final_actionable_issues=0)
spec=importlib.util.spec_from_file_location("pr789_actual_approved_driver",T/"publication_driver.py");driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
driver.completed_reviews(g,inv)
(T/"FINAL_READINESS.json").write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
got,_=driver.gate();assert got==g
u=T/"publication/READINESS_AT_PUBLICATION_V4.json";assert not u.exists();assert (T/"publication/READINESS_AT_PUBLICATION.json").read_bytes()==(T/"package_versions/v3_review03/READINESS_AT_PUBLICATION_ORIGINAL.json").read_bytes();u.write_bytes((T/"FINAL_READINESS.json").read_bytes())
print(json.dumps({"result":"PASS_CURRENT_PACKAGE_READY","actual_fresh_whole_reviews":4,"final_actionable_issues":0,"source_manifest_sha256":g["source_manifest_sha256"],"readiness_sha256":hashlib.sha256((T/"FINAL_READINESS.json").read_bytes()).hexdigest(),"case_percent":90,"shard_percent":83,"new_production_creation_in_this_gate_action":False,"known_only_existing_unpublished_draft":23423736}))

