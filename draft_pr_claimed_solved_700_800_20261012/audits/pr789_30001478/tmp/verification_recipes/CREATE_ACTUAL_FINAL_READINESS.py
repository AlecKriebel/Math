from pathlib import Path
import datetime,hashlib,importlib.util,json,subprocess,sys
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr789_30001478/tmp";M=T/"root-receipts";P=T/"preprint"
assert not(T/"FINAL_READINESS.json").exists(),"Actual readiness already exists; reconcile"
plan=json.loads((T/"READINESS_PLAN.json").read_text());peer=json.loads((M/"WHOLE03_ROOT_REPLAY.json").read_text());inv=json.loads((P/"PACKAGE_INVENTORY.json").read_text())
assert peer["result"]=="PASS"and peer["completed"]is True and peer["review_actionable_issues"]==0 and peer["freshly_initialized"]is True
assert peer["source_manifest_sha256"]==inv["source_manifest_sha256"]=="50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de"and peer["publication_files"]==inv["files"]
assert len(plan["completed_whole_reviews"])==2 and plan["actual_whole_preprint_rounds"]==2
row={"round":3,"reviewer":peer["reviewer"],"freshly_initialized":True,"packet":"whole_preprint_round03","manifest_sha256":peer["manifest_sha256"],"checker_name":peer["checker_name"],"checker_sha256":peer["checker_sha256"],"root_replay_receipt":"root-receipts/WHOLE03_ROOT_REPLAY.json","root_replay_sha256":hashlib.sha256((M/"WHOLE03_ROOT_REPLAY.json").read_bytes()).hexdigest(),"reviewed_source_manifest_sha256":peer["source_manifest_sha256"],"reviewed_publication_files":peer["publication_files"],"actionable_issues":0}
assert json.loads((M/"MATH_GATE.json").read_text())["result"]=="PASS"
assert json.loads((M/"PRIORITY_GATE.json").read_text())["known_full_predecessors"]==[]
for n in["ROOT_RELEASE_REPRODUCTION_V3.json","ROOT_V3_ARCHIVE_FULL_REPLAY.json"]:
 assert json.loads((M/n).read_text())["result"]=="PASS"
g=dict(plan);g.update(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),result="PASS",actual_whole_preprint_rounds=3,completed_whole_reviews=plan["completed_whole_reviews"]+[row],final_current_round_clean=True,paper_ready=True,source_checker_sha256="700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489",native_acceptance_state="NEXT_AFTER_PUBLICATION_TRACKER_AND_EXACT_MERGE",PR_completion_estimate_percent=90,shard_completion_estimate_percent=83,publication_status="PENDING_AUTHORIZED_PRODUCTION",known_full_predecessors=[],priority_status="PRIORITY_UNRESOLVED",final_actionable_issues=0)
spec=importlib.util.spec_from_file_location("pr789_actual_approved_driver",T/"publication_driver.py");driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
driver.completed_reviews(g,inv)
(T/"FINAL_READINESS.json").write_text(json.dumps(g,indent=2,ensure_ascii=False)+"\n")
got,_=driver.gate();assert got==g
u=T/"publication/READINESS_AT_PUBLICATION.json";assert not u.exists();u.write_bytes((T/"FINAL_READINESS.json").read_bytes())
print(json.dumps({"result":"PASS_CURRENT_PACKAGE_READY","actual_fresh_whole_reviews":3,"final_actionable_issues":0,"source_manifest_sha256":g["source_manifest_sha256"],"readiness_sha256":hashlib.sha256((T/"FINAL_READINESS.json").read_bytes()).hexdigest(),"case_percent":90,"shard_percent":83,"production_created":False}))

